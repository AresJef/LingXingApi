"""SB报告实际SDK请求的特征测试；响应仅用空合成值隔离传输。"""
import asyncio
from datetime import date, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from lingxingapi import errors
from lingxingapi.ads import param, route, schema
from lingxingapi.ads.api import AdsAPI

DAILY = (
    ("SbCampaignReports", route.SB_CAMPAIGN_REPORTS, {"show_detail": 0}),
    ("SbPlacementReports", route.SB_PLACEMENT_REPORTS, {"show_detail": 0}),
    ("SbAdGroupReports", route.SB_AD_GROUP_REPORTS, {"show_detail": 0}),
    ("SbCreativeReports", route.SB_CREATIVE_REPORTS, {"show_detail": 0}),
    ("SbKeywordReports", route.SB_TARGETING_REPORTS, {"sponsored_type": "ALL", "target_type": "keyword"}),
    ("SbKeywordQueryReports", route.SB_QUERY_REPORTS, {"target_type": "keyword"}),
    ("SbKeywordPlacementReports", route.SB_KEYWORD_PLACEMENT_REPORTS, {"sponsored_type": "ALL", "target_type": "keyword"}),
    ("SbTargetReports", route.SB_TARGETING_REPORTS, {"sponsored_type": "ALL", "target_type": "producttarget"}),
    ("SbTargetQueryReports", route.SB_QUERY_REPORTS, {"target_type": "target"}),
    ("SbAsinAttributionReports", route.SB_ASIN_ATTRIBUTION_REPORTS, {"show_detail": 0}),
    ("SbCostAllocationReports", route.SB_COST_ALLOCATION_REPORTS, {"show_detail": 0}),
)
HOURLY = (
    ("SbCampaignHourData", route.SB_CAMPAIGN_HOUR_DATA, {}),
    ("SbPlacementHourData", route.SB_PLACEMENT_HOUR_DATA, {}),
    ("SbAdGroupHourData", route.SB_AD_GROUP_HOUR_DATA, {}),
    ("SbTargetingHourData", route.SB_TARGETING_HOUR_DATA, {"agg_dimension": "target"}),
)
RAW = {"code": 0, "message": "success", "error_details": [], "request_id": "synthetic",
       "response_time": "2001-05-07 00:00:00", "total": 0, "next_token": None, "data": []}


@pytest.mark.parametrize("method,url,fixed", DAILY)
@pytest.mark.parametrize("ids", [{"sid": 101, "profile_id": None}, {"sid": None, "profile_id": 20001},
    {"sid": 101, "profile_id": 20001}, {"sid": 102, "profile_id": 20001}])
@pytest.mark.parametrize("paging", [{}, {"offset": 2, "length": 2}, {"next_token": "actual-source", "length": 2}])
def test_daily_exact_wire_body_version_and_existing_discriminators(method, url, fixed, ids, paging):
    signed = AsyncMock(return_value=RAW)
    kwargs = {"report_date": "2026-10-01", **ids, **paging}
    if method == "SbCostAllocationReports":
        kwargs.pop("sid")
        if kwargs["profile_id"] is None:
            with pytest.raises(errors.ParametersError):
                asyncio.run(getattr(AdsAPI, method)(SimpleNamespace(_request_with_sign=signed), **kwargs))
            signed.assert_not_awaited()
            return
    expected = {key: value for key, value in kwargs.items() if value is not None} | fixed
    parsed = asyncio.run(getattr(AdsAPI, method)(SimpleNamespace(_request_with_sign=signed), **kwargs))
    signed.assert_awaited_once_with("POST", url, body=expected, headers={"X-API-VERSION": "2"})
    assert isinstance(parsed, getattr(schema, method))


@pytest.mark.parametrize("method,url,fixed", HOURLY)
@pytest.mark.parametrize("day", ["2026-10-01", date(2026, 10, 1), datetime(2026, 10, 1, 15, 12)])
def test_hourly_exact_campaign_date_aggregation_v2_without_paging(method, url, fixed, day):
    signed = AsyncMock(return_value=RAW)
    parsed = asyncio.run(getattr(AdsAPI, method)(SimpleNamespace(_request_with_sign=signed), day, 30001))
    signed.assert_awaited_once_with("POST", url, body={"report_date": "2026-10-01", "campaign_id": 30001, **fixed},
        headers={"X-API-VERSION": "2"})
    assert isinstance(parsed, getattr(schema, method))


def test_sb_targeting_wire_alias_and_product_conversion_preexist():
    assert param.SbTargetingReports.model_validate_params({"report_date": "2026-10-01", "profile_id": 20001,
        "ad_type": "ALL", "target_type": "product"}) == {
        "report_date": "2026-10-01", "profile_id": 20001, "sponsored_type": "ALL", "target_type": "producttarget"}
