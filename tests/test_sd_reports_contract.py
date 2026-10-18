"""已批准的 SD 小时 null 游标例外；合成响应只在测试内存中。"""
from __future__ import annotations

from copy import deepcopy
from typing import get_args

import pytest

from lingxingapi.ads import schema
from response_contract import ContractError, field_keys, validate_response
from sd_reports_contract import HOURLY_MODELS, validate_sd_report_response


def hour(model):
    row_model = get_args(model.model_fields["data"].annotation)[0]
    values = {"profile_id": 1, "campaign_id": 2, "group_id": 3, "ad_id": 4,
        "targeting_id": 5, "targeting": "synthetic", "asin": "B0AAAA1234", "msku": "synthetic",
        "cost": 1.0, "impressions": 2, "clicks": 1, "orders": 0, "same_orders": 0,
        "units": 0, "sales": 0.0, "same_sales": 0.0, "ctr": 0.5, "cpc": 1.0,
        "cvr": 0.0, "cpa": None, "acos": None, "roas": 0.0,
        "hour": 3, "report_date": "2026-10-01"}
    return {"code": 0, "message": "success", "error_details": [], "request_id": "synthetic",
        "response_time": "2001-05-07 00:00:00", "total": 1, "next_token": None,
        "data": [{key: values[key] for key in field_keys(row_model)}]}


@pytest.mark.parametrize("model", HOURLY_MODELS)
def test_only_top_level_null_is_removed_from_check_view_and_wire_sdk_stay_same(model):
    raw = hour(model)
    before = deepcopy(raw)
    with pytest.raises(ContractError):
        validate_response(raw, model)
    parsed = validate_sd_report_response(raw, model)
    assert raw == before
    assert parsed.model_dump() == model.model_validate(raw).model_dump()
    assert "next_token" not in parsed.model_dump()
    del raw["next_token"]
    assert validate_sd_report_response(raw, model).model_dump() == parsed.model_dump()


@pytest.mark.parametrize("model", HOURLY_MODELS)
@pytest.mark.parametrize("value", ["", "cursor", 0, False, [], {}])
def test_every_non_null_token_stays_an_unexpected_field(model, value):
    with pytest.raises(ContractError):
        validate_sd_report_response(hour(model) | {"next_token": value}, model)


@pytest.mark.parametrize("model", HOURLY_MODELS)
@pytest.mark.parametrize("location", ["other_root", "nested_token", "nested_other", "missing_required"])
def test_null_exception_never_hides_another_field_or_missing_required_key(model, location):
    raw = hour(model)
    if location == "other_root":
        raw["unknown"] = None
    elif location == "nested_token":
        raw["data"][0]["next_token"] = None
    elif location == "nested_other":
        raw["data"][0]["unknown"] = None
    else:
        del raw["data"][0]["cost"]
    with pytest.raises(ContractError):
        validate_sd_report_response(raw, model)


def test_allowlist_is_four_exact_models_and_never_expands_to_other_endpoints(monkeypatch):
    import sd_reports_contract
    assert HOURLY_MODELS == (schema.SdCampaignHourData, schema.SdAdGroupHourData,
        schema.SdProductHourData, schema.SdTargetHourData)
    class Unregistered(schema.SdCampaignHourData):
        pass
    with pytest.raises(ContractError):
        validate_sd_report_response(hour(Unregistered), Unregistered)
    seen = []
    monkeypatch.setattr(sd_reports_contract, "validate_response", lambda raw, model: seen.append(raw))
    raw = {"next_token": None}
    for model in (schema.SdCampaignReports, schema.SbCampaignHourData, schema.SpCampaignHourData):
        validate_sd_report_response(raw, model)
        assert seen[-1] is raw and "next_token" in seen[-1]
