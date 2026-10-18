"""SpCampaigns 接入前离线契约；合成输入不作为真实 fixture 验收。"""
from __future__ import annotations

import asyncio
import ast
from copy import deepcopy
import inspect
import json
from pathlib import Path
import textwrap
from types import SimpleNamespace
from unittest.mock import AsyncMock

from pydantic import ValidationError
import pytest

from lingxingapi.ads.api import AdsAPI
from lingxingapi.ads import schema, route
from response_contract import ContractError, validate_response
from sp_campaigns_contract import validate_sp_campaigns_response
from documentation_contract import validate_documentation, validate_field_examples


def response():
    return {"code": 0, "message": "success", "error_details": [], "request_id": "synthetic-request",
            "response_time": "2001-05-07 05:14:42", "next_token": None, "total": 1,
            "data": [{"profile_id": "62609628290910", "portfolio_id": None, "campaign_id": "123456789012345678",
                      "name": "synthetic-campaign", "campaign_type": None, "targeting_type": "manual",
                      "premium_bid_adjustment": 0, "daily_budget": "12.5", "lastOverBudgetAt": None, "bidding": None,
                      "start_date": None, "end_date": None, "state": None, "serving_status": None,
                      "creation_date": None, "last_updated_date": ""}]}


def test_full_schema_aliases_null_conversions_and_exact_large_id_preserve_source():
    raw = response()
    before = deepcopy(raw)
    parsed = validate_sp_campaigns_response(raw)
    row = parsed.data[0]
    assert raw == before and type(row.campaign_id) is int and row.campaign_id == 123456789012345678
    assert row.profile_id == 62609628290910 and row.portfolio_id == row.create_time_ts == row.update_time_ts == 0
    assert row.campaign_name == "synthetic-campaign" and row.targeting_type == "manual"
    assert row.campaign_type == row.bidding == row.start_time == row.end_time == row.state == row.status == ""
    assert row.daily_budget == 12.5 and type(row.daily_budget) is float
    assert parsed.next_token == "" and parsed.response_count == parsed.total_count == 1
    assert row.model_dump()["campaign_name"] == row.model_dump(mode="json", by_alias=True)["campaign_name"]


@pytest.mark.parametrize("field", ["profile_id", "campaign_id", "name", "targeting_type", "premium_bid_adjustment", "daily_budget"])
def test_required_scalar_nulls_remain_invalid(field):
    raw = response()
    raw["data"][0][field] = None
    with pytest.raises(ValidationError):
        schema.SpCampaigns.model_validate(raw)


def test_missing_end_date_is_sdk_default_none_but_strict_raw_difference():
    raw = response()
    del raw["data"][0]["end_date"]
    assert schema.SpCampaigns.model_validate(raw).data[0].end_time is None
    with pytest.raises(ContractError) as caught:
        validate_sp_campaigns_response(raw)
    assert caught.value.status == "difference" and any("end_date" in text for text in caught.value.issues)


@pytest.mark.parametrize("tags", [[], [{"parent": "synthetic-parent", "child": "synthetic-child"}], None, {"unknown": True}, "opaque"])
def test_tags_are_explicitly_unmodelled_only_in_sp_campaign_contract(tags):
    raw = response()
    raw["data"][0]["tags"] = tags
    before = deepcopy(raw)
    parsed = validate_sp_campaigns_response(raw)
    assert raw == before and "tags" not in parsed.data[0].model_dump()
    with pytest.raises(ContractError) as caught:
        validate_response(raw, schema.SpCampaigns)
    assert caught.value.status == "difference" and any("响应多字段" in text for text in caught.value.issues)


@pytest.mark.parametrize("location", ["root", "row", "nested"])
def test_tags_exemption_never_suppresses_other_unknown_fields_or_locations(location):
    raw = response()
    raw["data"][0]["tags"] = []
    if location == "root":
        raw["tags"] = []
    elif location == "row":
        raw["data"][0]["unexpected"] = None
    else:
        raw["data"][0]["unexpected"] = {"tags": []}
    with pytest.raises(ContractError) as caught:
        validate_sp_campaigns_response(raw)
    assert caught.value.status == "difference"


def test_tags_exemption_keeps_missing_fields_type_checks_and_contract_notice():
    from sp_campaigns_contract import CONTRACT_NOTICE
    assert "data[*].tags" in CONTRACT_NOTICE and "SDK" in CONTRACT_NOTICE
    for patch in ({"daily_budget": None}, {"campaign_id": "invalid"}):
        raw = response();raw["data"][0].update(tags=[],**patch)
        with pytest.raises(ContractError):
            validate_sp_campaigns_response(raw)
    raw = response();raw["data"][0]["tags"] = []
    del raw["data"][0]["end_date"]
    with pytest.raises(ContractError):
        validate_sp_campaigns_response(raw)


def test_bidding_is_preserved_as_complete_opaque_string_without_enum_or_date_parsing():
    raw = response()
    raw["data"][0].update(bidding='{ "strategy": "futureStrategy", "adjustments": [] }',
                          start_date="not-parsed-as-date", state="other", campaign_type="other", premium_bid_adjustment=5)
    row = validate_sp_campaigns_response(raw).data[0]
    assert row.bidding == raw["data"][0]["bidding"] and row.start_time == "not-parsed-as-date"
    assert row.state == row.campaign_type == "other" and row.premium_bid_adjustment == 5


def empty_response():
    return {**response(), "data": [], "total": 0}


def test_explicit_empty_result_checks_outer_contract_without_claiming_row_coverage():
    raw = empty_response()
    before = deepcopy(raw)
    parsed = validate_sp_campaigns_response(raw, scenario="empty_expected")
    assert parsed.response_count == 0 and raw == before
    with pytest.raises(ContractError) as caught:
        validate_response(raw, schema.SpCampaigns)
    assert caught.value.status == "coverage"


@pytest.mark.parametrize("patch", [{"extra": True}, {"data": None}, {"code": 400}, {"code": "0"},
    {"error_details": ["failure"]}, {"next_token": []}, {"total": "bad"}, {"response_count": 3}])
def test_explicit_empty_result_does_not_hide_other_differences(patch):
    with pytest.raises(ContractError):
        validate_sp_campaigns_response({**empty_response(), **patch}, scenario="empty_expected")


@pytest.mark.parametrize("key", ["code", "message", "error_details", "request_id", "response_time", "next_token", "total"])
def test_empty_result_still_requires_all_wire_fields(key):
    raw = empty_response()
    del raw[key]
    with pytest.raises(ContractError):
        validate_sp_campaigns_response(raw, scenario="empty_expected")


@pytest.mark.parametrize("kwargs", [{"sid": 1, "profile_id": 2, "campaign_id": 3},
                                    {"sid": 1, "profile_id": 2, "targeting_type": "manual"}])
def test_public_signature_rejects_unexposed_filters(kwargs):
    signed = AsyncMock()
    with pytest.raises(TypeError):
        asyncio.run(AdsAPI.SpCampaigns(SimpleNamespace(_request_with_sign=signed), **kwargs))
    signed.assert_not_awaited()


def test_default_sdk_request_omits_optional_fields_and_uses_version_two():
    raw = empty_response()
    signed = AsyncMock(return_value=raw)
    parsed = asyncio.run(AdsAPI.SpCampaigns(SimpleNamespace(_request_with_sign=signed), None, 62609628290910))
    signed.assert_awaited_once_with("POST", route.SP_CAMPAIGNS, body={"profile_id": 62609628290910}, headers={"X-API-VERSION": "2"})
    assert parsed.data == []


@pytest.mark.parametrize("value", [None, "2026-10-12 22:17:35", "", " 2026-10-12 22:17:35 ", "opaque-time-value"])
def test_last_over_budget_at_preserves_string_or_null_and_output_alias_semantics(value):
    raw = response();raw["data"][0]["lastOverBudgetAt"] = value
    before = deepcopy(raw)
    parsed = validate_sp_campaigns_response(raw)
    row = parsed.data[0]
    assert raw == before and row.last_over_budget_at == value and type(row.last_over_budget_at) is type(value)
    for mode in ("python", "json"):
        for aliases in (False, True):
            dumped = row.model_dump(mode=mode, by_alias=aliases)
            assert dumped["last_over_budget_at"] == value and "lastOverBudgetAt" not in dumped


@pytest.mark.parametrize("value", [0, 1.0, False, [], {}, ["2026-10-12 22:17:35"]])
def test_last_over_budget_at_rejects_non_string_non_null_types(value):
    raw = response();raw["data"][0]["lastOverBudgetAt"] = value
    with pytest.raises(ValidationError):
        schema.SpCampaigns.model_validate(raw)
    with pytest.raises(ContractError):
        validate_sp_campaigns_response(raw)


def test_last_over_budget_at_is_required_and_immediately_follows_daily_budget():
    field = schema.SpCampaign.model_fields["last_over_budget_at"]
    assert field.is_required() and field.validation_alias == "lastOverBudgetAt"
    fields = list(schema.SpCampaign.model_fields)
    assert fields[fields.index("daily_budget") + 1] == "last_over_budget_at"
    assert fields[fields.index("last_over_budget_at") + 1] == "bidding"
    assert field.examples == ["2026-10-12 22:17:35"]
    assert field.description == "时间字符串，格式为 YYYY-MM-DD HH:MM:SS，可为 None [原字段 'lastOverBudgetAt']"
    for mode,key in (("validation", "lastOverBudgetAt"), ("serialization", "last_over_budget_at")):
        doc = schema.SpCampaign.model_json_schema(mode=mode)
        assert key in doc["required"] and "default" not in doc["properties"][key]
        assert doc["properties"][key]["anyOf"] == [{"type": "string"}, {"type": "null"}]
        assert list(doc["properties"])[list(doc["properties"]).index("daily_budget") + 1] == key
    raw = response();del raw["data"][0]["lastOverBudgetAt"]
    with pytest.raises(ValidationError):
        schema.SpCampaigns.model_validate(raw)


def test_last_over_budget_at_validation_alias_does_not_enable_new_name_population():
    raw = response();del raw["data"][0]["lastOverBudgetAt"]
    raw["data"][0]["last_over_budget_at"] = None
    with pytest.raises(ValidationError):
        schema.SpCampaigns.model_validate(raw)


def test_real_sixteen_scene_fixture_collection_contracts_and_complete_data_relationships():
    from sample_collection import load_collection, same_data
    manifest,records,responses = load_collection(Path(__file__).with_name("fixtures") / "ads/basic/sp/sp_campaigns-manifest.json", "ads.SpCampaigns")
    assert len(records) == manifest["planned_requests"] == 16 and manifest["not_run"] == []
    assert set(records) == {"account-A-sid-only", "account-A-profile-only", "account-A-both", "account-B-sid-only",
        "account-B-profile-only", "account-B-both", "account-A-sid-B-profile", "account-B-sid-A-profile", "state-paused",
        "state-archived", "state-omitted", "reference-direct", "offset-second", "token-second", "token-priority-conflicting-offset", "reference-end"}
    for label,raw in responses.items():
        before = deepcopy(raw)
        parsed = validate_sp_campaigns_response(raw, scenario=records[label]["scenario"])
        assert raw == before and parsed.response_count == len(raw["data"]) and parsed.total_count == raw["total"]
        assert all(row.last_over_budget_at is None for row in parsed.data)
        assert all("tags" in row for row in raw["data"]) and all("tags" not in row.model_dump() for row in parsed.data)
    for account in ("A", "B"):
        baseline = responses[f"account-{account}-profile-only"]["data"]
        assert baseline and all(same_data(responses[f"account-{account}-{kind}"]["data"], baseline) for kind in ("sid-only", "both"))
    assert same_data(responses["account-A-sid-B-profile"]["data"], responses["account-B-both"]["data"])
    assert same_data(responses["account-B-sid-A-profile"]["data"], responses["account-A-both"]["data"])
    for state in ("paused", "archived"):
        assert all(row["state"] == state for row in responses["state-" + state]["data"])
    assert "state" not in records["state-omitted"]["request"]
    relationship = manifest["relationships"];reference = responses[relationship["reference"]]["data"]
    for kind in ("offset", "token"):
        assert same_data([row for label in relationship[kind + "_pages"] for row in responses[label]["data"]], reference)
    assert same_data(responses[relationship["token_control"]]["data"], responses[relationship["token_conflict"]]["data"])
    assert same_data(reference, responses[relationship["end_reference"]]["data"])


def test_real_supplemental_fixture_preserves_null_and_five_nonnull_strings():
    path = Path(__file__).with_name("fixtures") / "ads/basic/sp/sp_campaigns-last-over-budget-at.json"
    fixture = json.loads(path.read_bytes())
    assert fixture["source"] == "local_raw" and fixture["endpoint"] == "ads.SpCampaigns"
    raw = fixture["response"];before = deepcopy(raw)
    parsed = validate_sp_campaigns_response(raw)
    assert raw == before and len(parsed.data) == parsed.response_count == 100 and parsed.total_count == 1565
    assert sum(row.last_over_budget_at is None for row in parsed.data) == 95
    assert [row.last_over_budget_at for row in parsed.data if row.last_over_budget_at is not None] == [
        "2026-10-12 22:17:35", "2026-10-12 00:34:15", "2026-10-11 19:05:13", "2026-10-04 19:42:16", "2026-10-06 23:10:20"]
    for wire,row in zip(raw["data"],parsed.data,strict=True):
        assert row.last_over_budget_at == wire["lastOverBudgetAt"] and type(row.last_over_budget_at) is type(wire["lastOverBudgetAt"])
        assert row.daily_budget == wire["daily_budget"] and row.bidding == wire["bidding"]


def test_sp_campaign_field_documentation_examples_form_a_valid_public_record():
    examples = validate_field_examples(schema.SpCampaign)
    assert examples['last_over_budget_at']
    for name, field in schema.SpCampaign.model_fields.items():
        assert field.description and "\n" not in field.description and "\\n" not in field.description
        assert all(word not in field.description for word in ("本次", "实测", "采集", "样本", "推定时区"))


def test_sp_campaigns_google_docstring_call_and_output_are_internally_consistent():
    path = Path(__file__).with_name("fixtures") / "ads/basic/sp/sp_campaigns-account-A-profile-only.json"
    sample = json.loads(path.read_bytes())
    assert sample["source"] == "local_raw" and sample["endpoint"] == "ads.SpCampaigns"
    parsed = validate_sp_campaigns_response(sample["response"])
    doc = inspect.getdoc(AdsAPI.SpCampaigns)
    assert doc.count(".. code-block:: python") == 2
    assert doc.index("## Docs") < doc.index("Args:") < doc.index("Returns:") < doc.index("Examples:")
    assert "领星接口文档: 新广告 - 基础数据.[SP广告活动]" in doc
    assert "sid 与 profile_id 至少提供一项；同时提供时，以 profile_id 指定的广告账号为准。" in doc
    assert "tags" in doc and "不包含" in doc
    assert all(word not in doc for word in ("本次", "实测", "采集", "样本", "推定时区"))
    call_source = textwrap.dedent(doc.split(".. code-block:: python")[1]).strip()
    call = ast.parse(call_source).body[0].value.value
    assert isinstance(call, ast.Call) and ast.unparse(call.func) == "client.ads.SpCampaigns"
    kwargs = {item.arg: ast.literal_eval(item.value) for item in call.keywords}
    actual = validate_documentation(AdsAPI.SpCampaigns, schema.SpCampaigns)
    assert kwargs == {"profile_id": actual['data'][0]['profile_id'], "state": "enabled", "offset": 0, "length": 2}
    assert all(row['profile_id'] == kwargs['profile_id'] and row['state'] == kwargs['state'] for row in actual['data'] if row is not Ellipsis)
    assert actual['data'][0]['last_over_budget_at']
    signed = AsyncMock(return_value=sample["response"])
    result = asyncio.run(AdsAPI.SpCampaigns(SimpleNamespace(_request_with_sign=signed), **kwargs))
    signed.assert_awaited_once_with("POST", route.SP_CAMPAIGNS,
        body={key: value for key, value in kwargs.items() if value is not None}, headers={"X-API-VERSION": "2"})
    assert result.model_dump() == parsed.model_dump()
