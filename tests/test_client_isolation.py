"""Offline client isolation tests: PYTHONPATH=src python -B -m unittest discover -s tests."""

import asyncio
from collections import deque
from contextlib import ExitStack
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock, Mock, patch

import orjson
from aiohttp import ClientSession, TCPConnector
from lingxingapi import API, errors, utils
from lingxingapi.base import route, schema


APP_A = "a" * 16
APP_B = "b" * 16
MODULES = ("basic", "sales", "fba", "product", "purchase", "warehouse",
           "ads", "finance", "tools", "source")


class Response:
    status = 200
    reason = "OK"

    def __init__(self, data):
        self.data = data

    async def read(self):
        return orjson.dumps(self.data)


class Request:
    def __init__(self, transport, call):
        self.transport, self.call = transport, call

    async def __aenter__(self):
        data = await self.transport.reply(self.call)
        if isinstance(data, BaseException):
            raise data
        return Response(data)

    async def __aexit__(self, *args):
        pass


class Session:
    def __init__(self, transport, *args, **kwargs):
        self.transport = transport
        self.settings = kwargs
        self.closed = False
        self.close_count = 0
        self.close_gate = None

    def request(self, method, url, **kwargs):
        if self.closed:
            raise AssertionError("request used a closed session")
        call = dict(method=method, url=url, **kwargs)
        self.transport.calls.append(call)
        return Request(self.transport, call)

    async def close(self):
        self.close_count += 1
        self.closed = True
        self.settings["connector"].closed = True
        if self.close_gate is not None:
            await self.close_gate.wait()


class Transport:
    def __init__(self):
        self.sessions, self.calls = [], []
        self.tokens, self.generations = {}, {}
        self.outcomes = deque()
        self.hook = None

    def session(self, *args, **kwargs):
        session = Session(self, *args, **kwargs)
        self.sessions.append(session)
        return session

    async def reply(self, call):
        await asyncio.sleep(0)
        if self.hook is not None:
            await self.hook(call)
        if self.outcomes:
            return self.outcomes.popleft()
        params, url = call["params"], call["url"]
        if url in (route.AUTH_GET_TOKEN, route.AUTH_REFRESH_TOKEN):
            account = params["appId"]
            if url == route.AUTH_REFRESH_TOKEN:
                if params["refreshToken"] != self.tokens[account]["refresh_token"]:
                    return {"code": 2001009}
            generation = self.generations.get(account, 0) + 1
            self.generations[account] = generation
            token = dict(access_token=f"{account}-access-{generation}",
                         refresh_token=f"{account}-refresh-{generation}", expires_in=3600)
            self.tokens[account] = token
            return {"code": 0, "data": token}
        account = params["app_key"]
        if params["access_token"] != self.tokens[account]["access_token"]:
            raise AssertionError("account used another or stale access token")
        if call["json"] == {"country_code": "US"}:
            return {"code": 0, "data": [{"country_code": "US", "code": "CA",
                                           "state_or_province_name": "California"}]}
        return {"code": 0, "data": []}

    def patches(self):
        stack = ExitStack()
        stack.enter_context(patch("lingxingapi.base.api.ClientSession", self.session))
        stack.enter_context(patch("lingxingapi.base.api.TCPConnector",
                                  side_effect=lambda **kw: Mock(closed=False, **kw)))
        self.probe = stack.enter_context(patch.object(utils, "check_internet_tcp",
                                                      new=AsyncMock(return_value=True)))
        stack.enter_context(patch("asyncio.open_connection", new=AsyncMock(
            side_effect=AssertionError("network access forbidden"))))
        for name in ("connect", "connect_ex"):
            stack.enter_context(patch(f"socket.socket.{name}",
                                      side_effect=AssertionError("network access forbidden")))
        return stack


class ClientTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.transport = Transport()
        self.stack = self.transport.patches()
        self.addCleanup(self.stack.close)
        self.a = API(APP_A, "fake-secret-a", timeout=7, max_tcp_connections=3)
        self.b = API(APP_B, "fake-secret-b", timeout=19, max_tcp_connections=8)
        self.addAsyncCleanup(self.a.close)
        self.addAsyncCleanup(self.b.close)

    async def bounded(self, operation):
        return await asyncio.wait_for(operation, 3)

    async def test_account_tokens_and_all_modules_share_only_their_client(self):
        a_token, b_token = await self.bounded(asyncio.gather(
            self.a.AccessToken(), self.b.AccessToken()))
        self.assertIsInstance(a_token, schema.Token)
        self.assertNotEqual(a_token.access_token, b_token.access_token)
        for client in (self.a, self.b):
            for name in MODULES:
                await getattr(client, name)._request_with_sign("GET", "/mock")
        self.assertEqual(len(self.transport.sessions), 2)
        self.assertEqual([s.settings["timeout"].total for s in self.transport.sessions], [7, 19])
        self.assertEqual([s.settings["connector"].limit for s in self.transport.sessions], [3, 8])
        self.assertIsNot(self.transport.sessions[0].settings["connector"],
                         self.transport.sessions[1].settings["connector"])
        await self.a.RefreshToken(a_token.refresh_token)
        await self.a.basic.Marketplaces()
        await self.b.basic.Marketplaces()
        self.assertEqual(self.transport.generations, {APP_A: 2, APP_B: 1})

    async def test_close_and_module_context_do_not_close_other_client(self):
        await self.a.AccessToken()
        await self.b.AccessToken()
        a_session, b_session = self.transport.sessions
        async with self.a.basic as module:
            self.assertIs(module, self.a.basic)
            await module.Marketplaces()
        await asyncio.gather(self.a.close(), self.a.sales.close(), self.a.close())
        self.assertEqual(a_session.close_count, 1)
        self.assertFalse(b_session.closed)
        await self.b.basic.Marketplaces()
        await self.a.basic.Marketplaces()
        self.assertEqual(len(self.transport.sessions), 3)
        self.assertEqual(self.transport.generations, {APP_A: 1, APP_B: 1})

    async def test_reopened_session_survives_completion_of_old_close(self):
        await self.a.AccessToken()
        old_session = self.transport.sessions[0]
        old_session.close_gate = asyncio.Event()
        closing = asyncio.create_task(self.a.close())
        try:
            await asyncio.sleep(0)
            self.assertTrue(old_session.closed)
            await self.a.basic.Marketplaces()
            new_session = self.transport.sessions[-1]
            old_session.close_gate.set()
            await self.bounded(closing)
            await self.a.sales._request_with_sign("GET", "/mock")
            self.assertEqual(len(self.transport.sessions), 2)
            self.assertFalse(new_session.closed)
        finally:
            old_session.close_gate.set()
            await self.bounded(closing)

    async def test_refresh_waits_only_for_same_client_and_uses_latest_token(self):
        await self.a.AccessToken()
        await self.b.AccessToken()
        entered, release = asyncio.Event(), asyncio.Event()

        async def hold_a(call):
            if call["url"] == route.AUTH_REFRESH_TOKEN and call["params"]["appId"] == APP_A:
                entered.set()
                await release.wait()

        self.transport.hook = hold_a
        first = asyncio.create_task(self.a.basic._UpdateToken())
        second = None
        try:
            await self.bounded(entered.wait())
            second = asyncio.create_task(self.a.sales._UpdateToken())
            await asyncio.sleep(0)
            await self.bounded(self.b.basic._UpdateToken())
            self.assertFalse(first.done())
            self.assertFalse(second.done())
            release.set()
            await self.bounded(asyncio.gather(first, second))
            refreshes = [c["params"]["refreshToken"] for c in self.transport.calls
                         if c["url"] == route.AUTH_REFRESH_TOKEN and c["params"]["appId"] == APP_A]
            self.assertEqual(refreshes, [f"{APP_A}-refresh-1", f"{APP_A}-refresh-2"])
            self.assertEqual(self.transport.generations, {APP_A: 3, APP_B: 2})
        finally:
            release.set()
            await self.bounded(asyncio.gather(*[t for t in (first, second) if t is not None]))

    async def test_cancelled_refresh_releases_client_lock(self):
        await self.a.AccessToken()
        entered = asyncio.Event()

        async def hold(call):
            entered.set()
            await asyncio.Event().wait()

        self.transport.hook = hold
        refreshing = asyncio.create_task(self.a.basic._UpdateToken())
        await self.bounded(entered.wait())
        refreshing.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await refreshing
        self.transport.hook = None
        await self.bounded(self.a.sales._UpdateToken())
        self.assertEqual(self.transport.generations[APP_A], 2)

    async def test_explicit_auth_coordinates_with_automatic_refresh(self):
        await self.a.AccessToken()
        entered, release = asyncio.Event(), asyncio.Event()

        async def hold(call):
            if call["url"] == route.AUTH_GET_TOKEN:
                entered.set()
                await release.wait()

        self.transport.hook = hold
        explicit = asyncio.create_task(self.a.AccessToken())
        automatic = None
        try:
            await self.bounded(entered.wait())
            automatic = asyncio.create_task(self.a.basic._UpdateToken())
            await asyncio.sleep(0)
            release.set()
            await self.bounded(asyncio.gather(explicit, automatic))
            self.assertEqual(self.transport.generations[APP_A], 3)
            self.assertEqual(self.transport.calls[-1]["params"]["refreshToken"],
                             f"{APP_A}-refresh-2")
        finally:
            release.set()
            await self.bounded(asyncio.gather(*[t for t in (explicit, automatic) if t is not None]))

    async def test_independently_supplied_proxy_connectors_close_independently(self):
        from aiohttp_socks import ProxyConnector
        a_connector, b_connector = Mock(spec=ProxyConnector), Mock(spec=ProxyConnector)
        a, b = API(APP_A, "fake-a", proxy_connector=a_connector), API(APP_B, "fake-b", proxy_connector=b_connector)
        try:
            await a.AccessToken()
            await b.AccessToken()
            await a.close()
            self.assertIs(self.transport.sessions[0].settings["connector"], a_connector)
            self.assertFalse(self.transport.sessions[1].closed)
            await b.basic.Marketplaces()
        finally:
            await a.close()
            await b.close()

    async def test_real_aiohttp_sessions_own_separate_connectors_without_network(self):
        sessions = []

        def session_factory(*args, **kwargs):
            session = ClientSession(*args, **kwargs)
            sessions.append(session)
            return session

        def request(session, method, url, **kwargs):
            return Request(self.transport, dict(method=method, url=url, **kwargs))

        with patch("lingxingapi.base.api.ClientSession", session_factory), \
                patch("lingxingapi.base.api.TCPConnector", TCPConnector), \
                patch.object(ClientSession, "request", request):
            try:
                await self.a.AccessToken()
                await self.b.AccessToken()
                a_session, b_session = sessions
                a_connector, b_connector = a_session.connector, b_session.connector
                self.assertIsNot(a_connector, b_connector)
                self.assertTrue(a_session.connector_owner)
                await self.a.close()
                self.assertTrue(a_session.closed)
                self.assertTrue(a_connector.closed)
                self.assertFalse(b_session.closed)
                self.assertFalse(b_connector.closed)
                await self.b.basic.Marketplaces()
            finally:
                await self.a.close()
                await self.b.close()


class SingleAccountTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.transport = Transport()
        self.stack = self.transport.patches()
        self.addCleanup(self.stack.close)
        self.api = API(APP_A, "fake-secret")
        self.addAsyncCleanup(self.api.close)

    async def test_automatic_acquisition_expiry_refresh_and_refresh_fallback(self):
        result = await self.api.basic.Marketplaces()
        self.assertEqual(result.data, [])
        for code in (2001003, 2001007):
            self.transport.outcomes.append({"code": code})
            await self.api.basic.Marketplaces()
        self.assertEqual(self.transport.generations[APP_A], 3)
        self.transport.outcomes.append({"code": 2001008})
        await self.api.basic._UpdateToken()
        self.assertEqual(self.transport.calls[-1]["url"], route.AUTH_GET_TOKEN)

    async def test_signing_and_request_arguments(self):
        token = await self.api.AccessToken()
        params, body, headers = {"query": "value"}, {"items": [2, 1]}, {"X-API-VERSION": "2"}
        with patch.object(utils, "now_ts", return_value=123):
            await self.api.basic._request_with_sign("POST", "/mock", params, body, headers, True)
        call = self.transport.calls[-1]
        signing = dict(app_key=APP_A, access_token=token.access_token, timestamp=123, **params, **body)
        self.assertEqual(call["params"]["sign"], utils.generate_sign(signing, self.api._app_cipher))
        self.assertEqual(call["json"], body)
        self.assertEqual(call["headers"], headers)
        self.assertEqual(params, {"query": "value"})

    async def test_retry_limits_and_unlimited_retries_still_probe_network(self):
        kinds = (("api_limit", {"code": 103}, errors.ApiLimitError, True),
                 ("internal_server_error", {"code": 500}, errors.InternalServerError, True),
                 ("timeout", TimeoutError("mock timeout"), errors.ApiTimeoutError, True),
                 ("internet_connection", TimeoutError("mock offline"), errors.InternetConnectionError, False))
        for kind, outcome, expected_error, online in kinds:
            for retries in (0, 2, -1):
                with self.subTest(kind=kind, retries=retries):
                    transport = Transport()
                    with transport.patches():
                        transport.probe.return_value = online
                        api = API(APP_A, "fake-secret", **{f"ignore_{kind}": True,
                                  f"ignore_{kind}_wait": 0, f"ignore_{kind}_retry": retries})
                        try:
                            failures = 12 if retries == -1 else retries + 1
                            transport.outcomes.extend([outcome] * failures)
                            transport.outcomes.append({"code": 0, "data": []})
                            if retries == -1:
                                await asyncio.wait_for(api._request("GET", "/mock", {}), 3)
                                self.assertEqual(len(transport.calls), 13)
                            else:
                                with self.assertRaises(expected_error):
                                    await asyncio.wait_for(api._request("GET", "/mock", {}), 3)
                                self.assertEqual(len(transport.calls), retries + 1)
                            self.assertEqual(transport.probe.await_count,
                                             failures if isinstance(outcome, TimeoutError) else 0)
                        finally:
                            await api.close()

    async def test_existing_local_auth_and_basic_parameter_assertions_offline(self):
        src = Path(__file__).resolve().parents[1] / "src"
        if not (src / "test_base.py").exists():
            self.skipTest("local ignored API test scripts are unavailable")
        # Read only the credential-free methods; never import local credential setup.
        auth_lines = (src / "test_base.py").open()
        basic_lines = (src / "test_basic.py").open()
        with auth_lines, basic_lines:
            from itertools import islice
            auth = "".join(islice(auth_lines, 74, 83))
            basic = "".join(islice(basic_lines, 7, 27))
        namespace = dict(API=API, errors=errors)
        exec("class Existing(TestCase):\n" + auth + basic, dict(namespace, TestCase=TestCase), namespace)
        existing = namespace["Existing"]()
        existing._app_id, existing._app_secret, existing._test_mode = APP_A, "fake-secret", True
        existing.print_data = lambda *args: None
        await existing.auth()
        await existing.basic_data()


class LoopLifecycleTests(TestCase):
    def test_same_client_reuse_after_close_in_a_new_loop_with_contention(self):
        client = API(APP_A, "fake-secret")
        transport = Transport()

        async def run():
            with transport.patches():
                try:
                    await asyncio.wait_for(asyncio.gather(
                        client.basic._UpdateToken(), client.sales._UpdateToken()), 3)
                    await client.basic.Marketplaces()
                finally:
                    await client.close()

        asyncio.run(run())
        asyncio.run(run())
        self.assertEqual(transport.generations[APP_A], 4)
        self.assertEqual(len(transport.sessions), 2)
        self.assertTrue(all(session.close_count == 1 for session in transport.sessions))

    def test_construct_outside_loop_and_use_independent_clients_in_separate_loops(self):
        for account in (APP_A, APP_B):
            client = API(account, "fake-secret")
            transport = Transport()

            async def run():
                with transport.patches():
                    try:
                        await asyncio.wait_for(asyncio.gather(
                            client.basic._UpdateToken(), client.sales._UpdateToken()), 3)
                        await client.basic.Marketplaces()
                    finally:
                        await client.close()
                        await client.close()
                self.assertEqual(transport.generations[account], 2)
                self.assertEqual(transport.sessions[0].close_count, 1)

            asyncio.run(run())
