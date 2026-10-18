"""SD报告9方法的现有请求契约；仅合成传输，不冒充真实报告fixture。"""

from __future__ import annotations

import asyncio
from copy import deepcopy
from datetime import date, datetime, timezone
import inspect
from types import SimpleNamespace
from typing import get_args
from unittest.mock import AsyncMock

import pytest
from pydantic import ValidationError

from lingxingapi import errors
from lingxingapi.ads import param, route, schema
from lingxingapi.ads.api import AdsAPI

DAILY = (
    ("SdCampaignReports", route.SD_CAMPAIGN_REPORTS, {}),
    ("SdAdGroupReports", route.SD_AD_GROUP_REPORTS, {}),
    ("SdProductReports", route.SD_PRODUCT_REPORTS, {}),
    ("SdTargetReports", route.SD_TARGET_REPORTS, {}),
    ("SdMatchedTargetReports", route.SD_MATCHED_TARGET_REPORTS, {}),
)
HOURLY = (
    ("SdCampaignHourData", route.SD_CAMPAIGN_HOUR_DATA, {}),
    ("SdAdGroupHourData", route.SD_AD_GROUP_HOUR_DATA, {}),
    ("SdProductHourData", route.SD_PRODUCT_HOUR_DATA, {"agg_dimension": "ad"}),
    ("SdTargetHourData", route.SD_TARGET_HOUR_DATA, {"agg_dimension": "both_ad_target"}),
)

def synthetic_response():
    return {
        "code": 0,
        "message": "success",
        "error_details": [],
        "request_id": "synthetic-report-request-only",
        "response_time": "2001-05-07 00:00:00",
        "total": 0,
        "next_token": None,
        "data": [],
    }


@pytest.mark.parametrize("method,url,fixed", DAILY)
@pytest.mark.parametrize(
    "ids,wire",
    [
        ({"sid": 1, "profile_id": None}, {"sid": 1}),
        ({"sid": None, "profile_id": 2}, {"profile_id": 2}),
        ({"sid": 1, "profile_id": 2}, {"sid": 1, "profile_id": 2}),
        ({"sid": 0, "profile_id": None}, {"sid": 0}),
    ],
)
@pytest.mark.parametrize(
    "paging",
    [
        {},
        {"offset": 0, "length": 0},
        {"next_token": "opaque-cursor", "offset": 2, "length": 4},
    ],
)
def test_daily_exact_route_headers_fixed_discriminator_and_no_none(
    method, url, fixed, ids, wire, paging
):
    raw = synthetic_response()
    before = deepcopy(raw)
    signed = AsyncMock(return_value=raw)
    parsed = asyncio.run(
        getattr(AdsAPI, method)(
            SimpleNamespace(_request_with_sign=signed),
            report_date="2026-10-01",
            **ids,
            **paging,
        )
    )
    signed.assert_awaited_once_with(
        "POST",
        url,
        body={"report_date": "2026-10-01", "show_detail": 0, **fixed, **wire, **paging},
        headers={"X-API-VERSION": "2"},
    )
    assert isinstance(parsed, getattr(schema, method)) and parsed.data == []
    assert parsed.response_count == 0 and raw == before


@pytest.mark.parametrize("method,url,fixed", HOURLY)
@pytest.mark.parametrize("campaign_id,wire", [(1, 1), (0, 0), (" 12 ", 12)])
def test_hourly_exact_single_campaign_and_aggregation_without_pagination(
    method, url, fixed, campaign_id, wire
):
    raw = synthetic_response()
    before = deepcopy(raw)
    signed = AsyncMock(return_value=raw)
    parsed = asyncio.run(
        getattr(AdsAPI, method)(
            SimpleNamespace(_request_with_sign=signed),
            report_date="2026-10-01",
            campaign_id=campaign_id,
        )
    )
    signed.assert_awaited_once_with(
        "POST", url, body={"report_date": "2026-10-01", "campaign_id": wire, **fixed},
        headers={"X-API-VERSION": "2"},
    )
    assert isinstance(parsed, getattr(schema, method)) and parsed.data == []
    assert parsed.response_count == 0 and raw == before


@pytest.mark.parametrize(
    "model,extra",
    [
        (param.AdReports, {"sid": 1}),
        (param.AdHourData, {"campaign_id": 1}),
    ],
)
@pytest.mark.parametrize(
    "value,normalized",
    [
        ("2026-10-01", "2026-10-01"),
        (date(2026, 10, 1), "2026-10-01"),
        (datetime(2026, 10, 1, 23, 30, tzinfo=timezone.utc), "2026-10-01"),
        ("2026-10-01T23:30:00-05:00", "2026-10-01"),
        ("2026-10", "2026-10-01"),
        ("2026-02-31", "2026-02-28"),
        (1, "1970-01-01"),
    ],
)
def test_existing_date_normalization_is_characterized_without_new_calendar_or_timezone_rule(
    model, extra, value, normalized
):
    assert (
        model.model_validate_params({"report_date": value, **extra})["report_date"]
        == normalized
    )


@pytest.mark.parametrize("method,url,fixed", (*DAILY, *HOURLY))
@pytest.mark.parametrize("value", [None, {}, "not-a-date"])
def test_invalid_report_date_never_sends_a_request(method, url, fixed, value):
    signed = AsyncMock()
    kwargs = (
        {"campaign_id": 1} if "HourData" in method else {"sid": 1, "profile_id": None}
    )
    with pytest.raises(errors.InvalidParametersError) as caught:
        asyncio.run(
            getattr(AdsAPI, method)(
                SimpleNamespace(_request_with_sign=signed), report_date=value, **kwargs
            )
        )
    assert isinstance(caught.value.__cause__, ValidationError)
    signed.assert_not_awaited()


@pytest.mark.parametrize("method,url,fixed", DAILY)
@pytest.mark.parametrize(
    "ids",
    [
        {"sid": None, "profile_id": None},
        {"sid": -1, "profile_id": 2},
        {"sid": 1, "profile_id": "invalid"},
    ],
)
def test_daily_invalid_identifiers_are_not_discarded(method, url, fixed, ids):
    signed = AsyncMock()
    with pytest.raises(errors.InvalidParametersError):
        asyncio.run(
            getattr(AdsAPI, method)(
                SimpleNamespace(_request_with_sign=signed),
                report_date="2026-10-01",
                **ids,
            )
        )
    signed.assert_not_awaited()


@pytest.mark.parametrize("method,url,fixed", HOURLY)
@pytest.mark.parametrize("value", [-1, 1.5, None, []])
def test_hourly_invalid_campaign_never_sends_request(method, url, fixed, value):
    signed = AsyncMock()
    with pytest.raises(errors.InvalidParametersError):
        asyncio.run(
            getattr(AdsAPI, method)(
                SimpleNamespace(_request_with_sign=signed),
                report_date="2026-10-01",
                campaign_id=value,
            )
        )
    signed.assert_not_awaited()


def test_scope_and_existing_sdk_boundaries_are_explicit():
    assert len(DAILY) == 5 and len(HOURLY) == 4
    assert len({method for method, _, _ in (*DAILY, *HOURLY)}) == 9
    for method, _, _ in DAILY:
        signature = inspect.signature(getattr(AdsAPI, method))
        assert "show_detail" not in signature.parameters
        assert (
            signature.parameters["sid"].default
            is signature.parameters["profile_id"].default
            is inspect.Parameter.empty
        )
    for method, _, _ in HOURLY:
        signature = inspect.signature(getattr(AdsAPI, method))
        assert all(
            name not in signature.parameters
            for name in ("campaign_ids", "offset", "length", "next_token")
        )


def test_original_product_hour_public_class_name_is_preserved():
    assert get_args(schema.SdProductHourData.model_fields["data"].annotation)[0] is schema.SpdProductHour
