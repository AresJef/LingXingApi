"""操作日志公开请求参数与SDK行为；不加载工具凭据或连接网络。"""

import asyncio
from contextlib import asynccontextmanager
from datetime import date, datetime
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from aiohttp import ClientSession

from lingxingapi import API
from lingxingapi.ads import param, route, schema
from lingxingapi.ads.api import AdsAPI
from test_ads_operation_logs_contract import response


@pytest.mark.parametrize("kind", ["SP", "SB", "SD"])
@pytest.mark.parametrize(
    "target",
    [
        "campaigns",
        "adGroups",
        "productAds",
        "keywords",
        "negativeKeywords",
        "targets",
        "negativeTargets",
        "profiles",
    ],
)
def test_supported_aliases_and_date_types_are_serialized(kind, target):
    actual = param.AdsOperationLogs.model_validate_params(
        {
            "sid": 10105,
            "start_date": date(2026, 10, 1),
            "end_date": datetime(2026, 10, 16, 12, 34),
            "ad_type": kind,
            "operation_target": target,
            "log_source": "all",
        }
    )
    assert actual == {
        "sid": 10105,
        "start_date": "2026-10-01",
        "end_date": "2026-10-16",
        "sponsored_type": kind.lower(),
        "operate_type": target,
        "log_source": "all",
    }


@pytest.mark.parametrize("offset,length", [(None, None), (0, 0), (2, 4)])
def test_public_sdk_sends_v2_and_preserves_none_and_zero(offset, length):
    signed = AsyncMock(return_value=response())
    actual = asyncio.run(
        AdsAPI.AdsOperationLogs(
            SimpleNamespace(_request_with_sign=signed),
            sid=10105,
            start_date="2026-10-01",
            end_date="2026-10-16",
            ad_type="SP",
            operation_target="campaigns",
            offset=offset,
            length=length,
        )
    )
    body = {
        "sid": 10105,
        "start_date": "2026-10-01",
        "end_date": "2026-10-16",
        "sponsored_type": "sp",
        "operate_type": "campaigns",
        "log_source": "all",
    }
    if offset is not None:
        body["offset"] = offset
    if length is not None:
        body["length"] = length
    signed.assert_awaited_once_with(
        "POST", route.ADS_OPERATION_LOGS, body=body, headers={"X-API-VERSION": "2"}
    )
    assert type(actual) is schema.AdsOperationLogs


def test_public_method_passes_v2_to_http_transport_without_observer_injection(monkeypatch):
    calls = []
    payload = json.dumps(response()).encode()

    @asynccontextmanager
    async def request(session, method, url, **kwargs):
        calls.append((method, url, kwargs))
        yield SimpleNamespace(
            status=200, reason="synthetic", read=AsyncMock(return_value=payload)
        )

    monkeypatch.setattr(ClientSession, "request", request)

    async def run():
        async with API("0" * 16, "fake-operation-log-secret") as client:
            client._state.access_token = "synthetic-token"
            result = await client.ads.AdsOperationLogs(
                sid=10105,
                start_date="2026-10-01",
                end_date="2026-10-16",
                ad_type="SP",
                operation_target="campaigns",
                offset=0,
                length=4,
            )
            assert type(result) is schema.AdsOperationLogs
            assert result.response_count == len(result.data) == len(response()["data"])

    asyncio.run(run())
    assert len(calls) == 1
    method, url, options = calls[0]
    assert (method, url) == ("POST", route.ADS_OPERATION_LOGS)
    assert options["headers"] == {"X-API-VERSION": "2"}
    assert options["json"]["offset"] == 0 and options["json"]["length"] == 4


def test_existing_calendar_month_and_parameter_acceptance_are_not_narrowed_to_thirty_days():
    body = param.AdsOperationLogs.model_validate_params(
        {
            "sid": "10105",
            "start_date": "2026-10-01",
            "end_date": "2026-11-01",
            "ad_type": "SP",
            "operation_target": "campaigns",
            "log_source": "all",
        }
    )
    assert body["start_date"] == "2026-10-01" and body["end_date"] == "2026-11-01"
    assert body["sid"] == 10105
