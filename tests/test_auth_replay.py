"""Bounded offline checks for signed-request replay and refresh coordination."""

import asyncio
from collections import Counter
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from lingxingapi import API, errors, utils
from lingxingapi.base import route
from test_client_isolation import APP_A, APP_B, Transport


AUTH_URLS = (route.AUTH_GET_TOKEN, route.AUTH_REFRESH_TOKEN)


class ReplayTransport(Transport):
    def __init__(self):
        super().__init__()
        self.business = None
        self.auth = None
        self.same_access_token = False

    async def reply(self, call):
        if call["url"] in AUTH_URLS:
            if self.auth is not None:
                result = await self.auth(call)
                if result is not None:
                    return result
            result = await super().reply(call)
            if self.same_access_token:
                result["data"]["access_token"] = f'{call["params"]["appId"]}-stable-access'
            return result
        if self.business is not None:
            return await self.business(call)
        return await super().reply(call)


class AuthReplayTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.transport = ReplayTransport()
        self.stack = self.transport.patches()
        self.addCleanup(self.stack.close)
        self.a = API(APP_A, "fake-secret-a", timeout=7)
        self.b = API(APP_B, "fake-secret-b", timeout=19)
        self.addAsyncCleanup(self.a.close)
        self.addAsyncCleanup(self.b.close)

    async def bounded(self, operation, timeout=3):
        return await asyncio.wait_for(operation, timeout)

    def assert_current_account_token(self, call):
        account = call["params"]["app_key"]
        self.assertEqual(call["params"]["access_token"],
                         self.transport.tokens[account]["access_token"])

    def parallel_expiry(self, count):
        attempts, ready = Counter(), asyncio.Event()
        first_count = 0

        async def business(call):
            nonlocal first_count
            key = (call["params"]["app_key"], call["url"])
            attempts[key] += 1
            if attempts[key] == 1:
                first_count += 1
                if first_count == count:
                    ready.set()
                await ready.wait()
                return {"code": 2001003}
            self.assert_current_account_token(call)
            return {"code": 0, "data": {"account": key[0], "url": key[1]}}

        self.transport.business = business
        return attempts

    async def test_replay_preserves_every_request_option_and_extract_data_value(self):
        for code in (2001003, 2001005, 2001007):
            for method, extract in (("GET", False), ("POST", True),
                                    ("PUT", False), ("DELETE", True)):
                with self.subTest(code=code, method=method, extract=extract):
                    await self.a.AccessToken()
                    calls = []
                    payload = {"code": 0, "data": {"items": [3]}, "request_id": "fake"}

                    async def business(call):
                        calls.append(call)
                        return {"code": code} if len(calls) == 1 else payload

                    self.transport.business = business
                    params, body = {"query": "value", "page": 2}, {"items": [2, 1]}
                    headers = {"X-API-VERSION": "2", "X-Custom": "keep-me"}
                    original_request = self.a.basic._request
                    with patch.object(self.a.basic, "_request", wraps=original_request) as request, \
                            patch.object(utils, "now_ts", side_effect=[123, 124]):
                        result = await self.bounded(self.a.basic._request_with_sign(
                            method, "/options", params, body, headers, extract))
                    self.assertEqual(result, payload["data"] if extract else payload)
                    business_calls = [c for c in request.await_args_list if c.args[1] not in AUTH_URLS]
                    self.assertEqual(len(business_calls), 2)
                    for c in business_calls:
                        self.assertEqual(c.args[:2], (method, "/options"))
                        self.assertEqual(c.kwargs, dict(body=body, headers=headers, extract_data=extract))
                    for call, timestamp in zip(calls, (123, 124)):
                        self.assertEqual((call["method"], call["url"]), (method, "/options"))
                        self.assertEqual(call["headers"], headers)
                        self.assertEqual(call["json"], body)
                        for name, value in params.items():
                            self.assertEqual(call["params"][name], value)
                        self.assertEqual(call["params"]["timestamp"], timestamp)
                        signing = dict(call["params"])
                        signing.pop("sign")
                        signing.update(body)
                        self.assertEqual(call["params"]["sign"],
                                         utils.generate_sign(signing, self.a._app_cipher))
                    self.assertEqual(params, {"query": "value", "page": 2})
                    self.assertEqual(body, {"items": [2, 1]})

    async def test_parallel_expiry_refreshes_once_even_when_access_token_string_repeats(self):
        for stable in (False, True):
            with self.subTest(same_access_token=stable):
                self.transport.same_access_token = stable
                await self.a.AccessToken()
                before = self.transport.generations[APP_A]
                attempts = self.parallel_expiry(4)
                modules = (self.a.basic, self.a.sales, self.a.product, self.a.fba)
                await self.bounded(asyncio.gather(*[
                    module._request_with_sign("GET", f"/parallel/{i}", extract_data=True)
                    for i, module in enumerate(modules)]))
                self.assertEqual(self.transport.generations[APP_A], before + 1)
                self.assertEqual(list(attempts.values()), [2] * 4)

    async def test_late_expired_response_uses_already_refreshed_token(self):
        await self.a.AccessToken()
        late_entered, release_late = asyncio.Event(), asyncio.Event()
        attempts = Counter()

        async def business(call):
            url = call["url"]
            attempts[url] += 1
            if attempts[url] == 1:
                if url == "/late":
                    late_entered.set()
                    await release_late.wait()
                return {"code": 2001003}
            self.assert_current_account_token(call)
            return {"code": 0, "data": {"url": url}}

        self.transport.business = business
        late = asyncio.create_task(self.a.basic._request_with_sign("GET", "/late", extract_data=True))
        try:
            await self.bounded(late_entered.wait())
            await self.bounded(self.a.sales._request_with_sign("GET", "/early", extract_data=True))
            self.assertEqual(self.transport.generations[APP_A], 2)
            release_late.set()
            self.assertEqual(await self.bounded(late), {"url": "/late"})
            self.assertEqual(self.transport.generations[APP_A], 2)
        finally:
            release_late.set()
            await self.bounded(late)

    async def test_explicit_auth_update_prevents_late_response_from_refreshing_again(self):
        self.transport.same_access_token = True
        for method in ("AccessToken", "RefreshToken"):
            with self.subTest(method=method):
                token = await self.a.AccessToken()
                before = self.transport.generations[APP_A]
                entered, release = asyncio.Event(), asyncio.Event()
                attempt = 0

                async def business(call):
                    nonlocal attempt
                    attempt += 1
                    if attempt == 1:
                        entered.set()
                        await release.wait()
                        return {"code": 2001003}
                    self.assert_current_account_token(call)
                    return {"code": 0, "data": []}

                self.transport.business = business
                late = asyncio.create_task(self.a.basic._request_with_sign("GET", "/manual"))
                try:
                    await self.bounded(entered.wait())
                    if method == "AccessToken":
                        updated = await self.a.AccessToken()
                    else:
                        updated = await self.a.RefreshToken(token.refresh_token)
                    self.assertEqual(updated.access_token, token.access_token)
                    release.set()
                    await self.bounded(late)
                    self.assertEqual(self.transport.generations[APP_A], before + 1)
                finally:
                    release.set()
                    await self.bounded(late)

    async def test_two_accounts_each_refresh_once_without_crossing_tokens(self):
        await self.a.AccessToken()
        await self.b.AccessToken()
        attempts = self.parallel_expiry(4)
        results = await self.bounded(asyncio.gather(*[
            module._request_with_sign("GET", f"/account/{i}", extract_data=True)
            for i, module in enumerate((self.a.basic, self.a.sales, self.b.basic, self.b.sales))]))
        self.assertEqual([r["account"] for r in results], [APP_A, APP_A, APP_B, APP_B])
        self.assertEqual(self.transport.generations, {APP_A: 2, APP_B: 2})
        self.assertEqual(list(attempts.values()), [2] * 4)
        refreshes = [c["params"] for c in self.transport.calls if c["url"] == route.AUTH_REFRESH_TOKEN]
        self.assertEqual({(r["appId"], r["refreshToken"]) for r in refreshes},
                         {(APP_A, f"{APP_A}-refresh-1"), (APP_B, f"{APP_B}-refresh-1")})

    async def test_failed_refresh_releases_lock_for_waiters_and_other_accounts(self):
        await self.a.AccessToken()
        await self.b.AccessToken()
        self.parallel_expiry(2)
        refreshes = 0

        async def auth(call):
            nonlocal refreshes
            if call["url"] == route.AUTH_REFRESH_TOKEN:
                refreshes += 1
                if refreshes == 1:
                    return {"code": 500}

        self.transport.auth = auth
        results = await self.bounded(asyncio.gather(
            self.a.basic._request_with_sign("GET", "/failure/1"),
            self.a.sales._request_with_sign("GET", "/failure/2"), return_exceptions=True))
        self.assertEqual(sum(isinstance(r, errors.InternalServerError) for r in results), 1)
        self.assertEqual(sum(isinstance(r, dict) for r in results), 1)
        self.assertEqual(refreshes, 2)
        self.transport.business = None
        await self.bounded(self.a.basic.Marketplaces())
        await self.bounded(self.b.basic.Marketplaces())
        self.assertEqual(self.transport.generations, {APP_A: 2, APP_B: 1})

    async def test_cancelled_refresh_allows_waiter_to_refresh_without_poisoning_state(self):
        await self.a.AccessToken()
        await self.b.AccessToken()
        refreshing, waiter_sent = asyncio.Event(), asyncio.Event()
        attempts, refreshes = Counter(), 0

        async def business(call):
            url = call["url"]
            attempts[url] += 1
            if attempts[url] == 1:
                if url == "/waiter":
                    waiter_sent.set()
                return {"code": 2001003}
            self.assert_current_account_token(call)
            return {"code": 0, "data": []}

        async def auth(call):
            nonlocal refreshes
            if call["url"] == route.AUTH_REFRESH_TOKEN:
                refreshes += 1
                if refreshes == 1:
                    refreshing.set()
                    await asyncio.Event().wait()

        self.transport.business, self.transport.auth = business, auth
        first = asyncio.create_task(self.a.basic._request_with_sign("GET", "/cancel"))
        waiter = None
        try:
            await self.bounded(refreshing.wait())
            waiter = asyncio.create_task(self.a.sales._request_with_sign("GET", "/waiter"))
            await self.bounded(waiter_sent.wait())
            first.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await first
            await self.bounded(waiter)
            self.assertEqual(refreshes, 2)
            self.transport.business = None
            await self.bounded(self.a.basic.Marketplaces())
            await self.bounded(self.b.basic.Marketplaces())
            self.assertEqual(self.transport.generations, {APP_A: 2, APP_B: 1})
        finally:
            first.cancel()
            if waiter is not None and not waiter.done():
                waiter.cancel()
            await self.bounded(asyncio.gather(*[t for t in (first, waiter) if t is not None],
                                               return_exceptions=True))

    async def test_expired_refresh_token_falls_back_once_for_parallel_requests(self):
        await self.a.AccessToken()
        self.parallel_expiry(2)

        async def auth(call):
            if call["url"] == route.AUTH_REFRESH_TOKEN:
                return {"code": 2001008}

        self.transport.auth = auth
        await self.bounded(asyncio.gather(
            self.a.basic._request_with_sign("GET", "/fallback/1"),
            self.a.sales._request_with_sign("GET", "/fallback/2")))
        self.assertEqual(self.transport.generations[APP_A], 2)
        self.assertEqual(sum(c["url"] == route.AUTH_REFRESH_TOKEN for c in self.transport.calls), 1)
        self.assertEqual(sum(c["url"] == route.AUTH_GET_TOKEN for c in self.transport.calls), 2)

    async def test_auth_replay_continues_beyond_recursion_and_100_attempt_limits(self):
        await self.a.AccessToken()
        failures, attempts = 1100, 0

        async def business(call):
            nonlocal attempts
            attempts += 1
            return {"code": 2001003} if attempts <= failures else {"code": 0, "data": []}

        self.transport.business = business
        result = await self.bounded(self.a.basic._request_with_sign(
            "GET", "/continuous", headers={"X-Custom": "keep"}, extract_data=True), timeout=6)
        self.assertEqual(result, [])
        self.assertEqual(attempts, failures + 1)
        self.assertEqual(self.transport.generations[APP_A], failures + 1)
        calls = [c for c in self.transport.calls if c["url"] == "/continuous"]
        self.assertTrue(all(c["headers"] == {"X-Custom": "keep"} for c in calls))
        self.assertEqual(self.transport.sessions[0].settings["timeout"].total, 7)
