"""17个V2方法及两个无版本头方法的离线HTTP边界，使用合成凭据。"""

import asyncio
from contextlib import asynccontextmanager
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from aiohttp import ClientSession

from lingxingapi import API
from lingxingapi.ads import route, schema
from test_sp_reports_requests import HOURLY as SP_HOURLY
from test_sb_reports_requests import HOURLY as SB_HOURLY
from test_sd_reports_requests import HOURLY as SD_HOURLY

CASES = (
    ("AdProfiles", route.AD_PROFILES,
     {"profile_type": "seller", "offset": 0, "length": 2},
     {"type": "seller", "offset": 0, "length": 2}),
    ("Portfolios", route.PORTFOLIOS,
     {"sid": 101, "profile_id": 20001, "state": "enabled", "next_token": "opaque-cursor", "offset": 0, "length": 2},
     {"sid": 101, "profile_id": 20001, "state": "enabled", "next_token": "opaque-cursor", "offset": 0, "length": 2}),
    ("SbCostAllocationReports", route.SB_COST_ALLOCATION_REPORTS,
     {"report_date": "2026-10-01", "profile_id": 20001, "next_token": "opaque-cursor", "offset": 0, "length": 2},
     {"report_date": "2026-10-01", "profile_id": 20001, "next_token": "opaque-cursor", "offset": 0, "length": 2, "show_detail": 0}),
    *((name, url,
       {"report_date": "2026-10-01", "campaign_id": 30001},
       {"report_date": "2026-10-01", "campaign_id": 30001, **fixed})
      for name, url, fixed in (*SP_HOURLY, *SB_HOURLY, *SD_HOURLY)),
)


def response(data):
    return {"code": 0, "message": "success", "error_details": [], "data": data,
            "total": 0, "next_token": None, "request_id": "synthetic-only",
            "response_time": "2001-05-07 00:00:00"}


@pytest.mark.parametrize("method,url,parameters,wire", CASES, ids=[case[0] for case in CASES])
def test_public_method_sends_one_v2_header_preserving_body_model_and_session(
    monkeypatch, method, url, parameters, wire
):
    calls = []

    @asynccontextmanager
    async def request(session, verb, target, **options):
        # 只观察公开请求链交给HTTP边界的头，并按当前session规则合并。
        calls.append((verb, target, options, session._prepare_headers(options.get("headers"))))
        yield SimpleNamespace(status=200, reason="synthetic", read=AsyncMock(return_value=json.dumps(response([])).encode()))

    monkeypatch.setattr(ClientSession, "request", request)

    async def run():
        async with API("0" * 16, "synthetic-only-secret") as client:
            client._state.access_token = "synthetic-only-token"
            client._state.session = ClientSession(headers={"Content-Type": "application/json", "X-Session-Test": "preserved"})
            before = dict(client._state.session.headers)
            parsed = await getattr(client.ads, method)(**parameters)
            assert type(parsed) is getattr(schema, method) and parsed.data == []
            assert parsed.response_count == 0
            assert dict(client._state.session.headers) == before

    asyncio.run(run())
    assert len(calls) == 1
    verb, target, options, effective = calls[0]
    assert (verb, target, options["json"]) == ("POST", url, wire)
    assert options["headers"] == {"X-API-VERSION": "2"}
    assert effective.getall("X-API-VERSION") == ["2"]
    assert effective["Content-Type"] == "application/json"
    assert effective["X-Session-Test"] == "preserved"


@pytest.mark.parametrize("method,parameters,data", [
    ("DspReports", {"start_date": "2026-10-01", "end_date": "2026-10-01", "profile_id": 20001, "advertiser_id": 30001,
                    "next_token": "opaque-cursor", "offset": 0, "length": 2}, []),
    ("DownloadAbaReport", {"country": "US", "start_date": "2026-10-04"},
     {"country": "US", "data_start_time": "2026-10-04", "report_period": "WEEK", "url": "https://example.invalid/report.zip"}),
])
def test_unselected_methods_still_send_no_version_header(monkeypatch, method, parameters, data):
    calls = []

    @asynccontextmanager
    async def request(session, verb, url, **options):
        calls.append(session._prepare_headers(options.get("headers")))
        yield SimpleNamespace(status=200, reason="synthetic", read=AsyncMock(return_value=json.dumps(response(data)).encode()))

    monkeypatch.setattr(ClientSession, "request", request)

    async def run():
        async with API("0" * 16, "synthetic-only-secret") as client:
            client._state.access_token = "synthetic-only-token"
            await getattr(client.ads, method)(**parameters)

    asyncio.run(run())
    assert len(calls) == 1 and "X-API-VERSION" not in calls[0]
