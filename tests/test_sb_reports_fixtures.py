"""SB报告完整真实响应契约；不依赖首次接入附注，不继承SP豁免。"""
from __future__ import annotations

import asyncio
from copy import deepcopy
import json
from pathlib import Path
import re
from types import SimpleNamespace
from typing import get_args
from unittest.mock import AsyncMock

import pytest

from lingxingapi.ads import schema
from lingxingapi.ads.api import AdsAPI
from response_contract import ContractError, field_keys, validate_response
from sample_collection import load_collection, same_data
from sb_reports_contract import validate_sb_report_response
from test_contract import test_api_contract as run_raw_contract
from test_sb_reports_requests import DAILY, HOURLY

DIRECTORY = Path(__file__).with_name("fixtures")/"ads/reports/sb"
PREFIXES = {
    "SbCampaignReports": "sb_campaign_reports", "SbCampaignHourData": "sb_campaign_hour_data",
    "SbPlacementReports": "sb_placement_reports", "SbPlacementHourData": "sb_placement_hour_data",
    "SbAdGroupReports": "sb_ad_group_reports", "SbAdGroupHourData": "sb_ad_group_hour_data",
    "SbCreativeReports": "sb_creative_reports", "SbKeywordReports": "sb_keyword_reports",
    "SbKeywordQueryReports": "sb_keyword_query_reports", "SbKeywordPlacementReports": "sb_keyword_placement_reports",
    "SbTargetReports": "sb_target_reports", "SbTargetQueryReports": "sb_target_query_reports",
    "SbTargetingHourData": "sb_targeting_hour_data", "SbAsinAttributionReports": "sb_asin_attribution_reports",
    "SbCostAllocationReports": "sb_cost_allocation_reports",
}
QUERIES = {"SbKeywordQueryReports", "SbTargetQueryReports"}


def same_hour_rows(left, right):
    """比较整行多重集，保留重复数量和行内列表顺序。"""
    from collections import Counter
    import json
    def canonical(value):
        return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False)
    return Counter(map(canonical, left)) == Counter(map(canonical, right))


def assert_targeting_identity_projection(identities, response_list):
    """正常集合和独立补样共用身份契约；每个位置只能被完整身份覆盖一次。"""
    assert identities
    positions, keys = set(), set()
    for item in identities:
        key = tuple(item[name] for name in ("profile_id", "campaign_id", "group_id", "targeting_id"))
        assert all(type(value) is int and value > 0 for value in key)
        assert key not in keys
        keys.add(key)
        if item["classification"] == "keyword":
            assert item["text_exact"] is True
            assert type(item["match_type"]) is str and item["match_type"]
        else:
            assert item["classification"] == "producttarget" and item["asin_exact"] is True
            assert item["expression_type"] == "asinSameAs"
            assert type(item["asin"]) is str and re.fullmatch(r"[A-Z0-9]{10}", item["asin"])
            assert item["targeting"] == f'asin="{item["asin"]}"'
            assert "match_type" not in item and "text_exact" not in item
        assert item["hourly_occurrences"] == len(item["hourly_locations"]) > 0
        assert set(item["source"]) == {"manifest_sha256", "sha256", "row_index"}
        assert all(re.fullmatch(r"[0-9a-f]{64}", item["source"][name])
            for name in ("manifest_sha256", "sha256"))
        assert type(item["source"]["row_index"]) is int and item["source"]["row_index"] >= 0
        for location in item["hourly_locations"]:
            position = (location["response_index"], location["row_index"])
            assert all(type(value) is int and value >= 0 for value in position)
            assert position not in positions
            positions.add(position)
            row = response_list[position[0]]["data"][position[1]]
            assert all(type(row[name]) is type(item[name]) and row[name] == item[name]
                for name in ("profile_id", "campaign_id", "group_id", "targeting_id", "targeting"))
    assert positions == {(i, j) for i, raw in enumerate(response_list) for j, _ in enumerate(raw["data"])}


@pytest.mark.parametrize("method", tuple(row[0] for row in DAILY))
def test_real_daily_all_fields_identifiers_dates_and_complete_pagination(method):
    manifest, records, responses = load_collection(DIRECTORY/(PREFIXES[method] + "-manifest.json"), "ads." + method)
    before = deepcopy((manifest, records, responses))
    expected = 7 if method == "SbCostAllocationReports" else 12 if method in QUERIES else 13
    assert len(records) + len(manifest.get("diagnostics", [])) == manifest["planned_requests"] == expected
    assert manifest["not_run"] == []
    assert all(check["status"] in {"proved", "observed"} for check in manifest["checks"].values())
    for label, raw in responses.items():
        parsed = validate_sb_report_response(raw, getattr(schema, method))
        assert parsed.response_count == len(raw["data"]) and parsed.total_count == raw["total"]
        request = records[label]["request"]
        assert all(row["report_date"] == request["report_date"] for row in raw["data"])
        if "profile_id" in request:
            assert all(row["profile_id"] == request["profile_id"] for row in raw["data"])
        if method == "SbCostAllocationReports":
            assert "sid" not in request
    relation = manifest["relationships"]
    reference = responses[relation["reference"]]["data"]
    assert len(reference) == 4 and same_data(reference, responses[relation["end_reference"]]["data"])
    for kind in ("offset_pages", "token_pages"):
        assert same_data([row for label in relation[kind] for row in responses[label]["data"]], reference)
    if method in QUERIES:
        assert "token_conflict" not in relation and "token_priority" not in manifest["checks"]
    else:
        assert same_data(responses[relation["token_control"]]["data"], responses[relation["token_conflict"]]["data"])
        assert not same_data(reference[:2], reference[2:])
    assert (manifest, records, responses) == before


@pytest.mark.parametrize("method,url,fixed", DAILY)
def test_real_daily_replays_existing_sdk_wire_parameters_and_actual_cursor_source(method, url, fixed):
    _, records, responses = load_collection(DIRECTORY/(PREFIXES[method] + "-manifest.json"), "ads." + method)
    for label, record in records.items():
        request = deepcopy(record["request"])
        if record["next_token_from"] is not None:
            request["next_token"] = responses[record["next_token_from"]]["next_token"]
        kwargs = dict(request)
        for key, value in fixed.items():
            assert kwargs.pop(key) == value
        if method != "SbCostAllocationReports":
            kwargs = {"sid": kwargs.get("sid"), "profile_id": kwargs.get("profile_id"), **kwargs}
        if method in QUERIES and record["next_token_from"] is not None:
            assert "offset" not in request
        signed = AsyncMock(return_value=responses[label])
        parsed = asyncio.run(getattr(AdsAPI, method)(SimpleNamespace(_request_with_sign=signed), **kwargs))
        options = {"headers": {"X-API-VERSION": "2"}}
        signed.assert_awaited_once_with("POST", url, body=request, **options)
        assert isinstance(parsed, getattr(schema, method))


@pytest.mark.parametrize("method,url,fixed", HOURLY)
def test_real_hourly_strict_fields_source_membership_full_multiset_and_raw_order(method, url, fixed):
    manifest, records, responses = load_collection(DIRECTORY/(PREFIXES[method] + "-manifest.json"), "ads." + method)
    before = deepcopy((manifest, records, responses))
    assert len(records) == manifest["planned_requests"] == 3 and manifest["not_run"] == []
    assert all(check["status"] == "proved" for check in manifest["checks"].values())
    assert manifest["checks"]["baseline_stability"]["comparison"] == "complete_rows_multiset"
    sources = {source["label"]: source for source in manifest["campaign_sources"]}
    assert set(sources) == {"campaign-A", "campaign-B"}
    for label, raw in responses.items():
        parsed = validate_sb_report_response(raw, getattr(schema, method))
        assert parsed.response_count == len(raw["data"])
        request = records[label]["request"]
        assert records[label]["next_token_from"] is None
        assert all(row["report_date"] == request["report_date"] and row["campaign_id"] == request["campaign_id"]
            and 0 <= row["hour"] <= 23 for row in raw["data"])
        source = sources["campaign-A" if label == "reference-end" else label]
        assert source["report_date"] == request["report_date"]
        assert all(row["profile_id"] == source["profile_id"] and row["campaign_id"] == source["campaign_id"] for row in raw["data"])
        kwargs = dict(request)
        for key, value in fixed.items():
            assert kwargs.pop(key) == value
        signed = AsyncMock(return_value=raw)
        asyncio.run(getattr(AdsAPI, method)(SimpleNamespace(_request_with_sign=signed), **kwargs))
        signed.assert_awaited_once_with("POST", url, body=request, headers={"X-API-VERSION": "2"})
    assert same_hour_rows(responses["campaign-A"]["data"], responses["reference-end"]["data"])
    assert manifest["checks"]["baseline_stability"]["ordered_data_equal"] is same_data(responses["campaign-A"]["data"], responses["reference-end"]["data"])
    if method == "SbTargetingHourData":
        assert_targeting_identity_projection(manifest["targeting_identities"], list(responses.values()))
    assert (manifest, records, responses) == before


def test_real_targeting_hour_producttarget_supplement_proves_single_asin_cross_interface_identity():
    fixture = json.loads((DIRECTORY/"sb_targeting_hour_data-producttarget-supplemental.json").read_bytes())
    before = deepcopy(fixture)
    assert fixture["source"] == "local_raw" and fixture["endpoint"] == "ads.SbTargetingHourData"
    assert fixture["coverage"] == "independent_single_asin_producttarget_supplement"
    assert "checks" not in fixture and "samples" not in fixture
    assert fixture["entity_projection_scope"] == "identity_fields_only"
    assert all(re.fullmatch(r"[0-9a-f]{64}", fixture[name])
        for name in ("source_sha256", "reference_source_sha256"))
    raw = fixture["response"]
    parsed = validate_sb_report_response(raw, schema.SbTargetingHourData)
    assert parsed.response_count == len(raw["data"]) == 45
    identities = fixture["targeting_identities"]
    assert len(identities) == len(fixture["entity_projections"]) == 14
    assert_targeting_identity_projection(identities, [raw])
    keyed = {(item["profile_id"], item["campaign_id"], item["group_id"], item["targeting_id"]): item
        for item in identities}
    seen = set()
    for entity in fixture["entity_projections"]:
        assert set(entity) == {"profile_id", "campaign_id", "ad_group_id", "target_id", "targeting_type",
            "expression", "resolved_expression", "source"}
        assert entity["targeting_type"] == "producttarget"
        key = tuple(entity[name] for name in ("profile_id", "campaign_id", "ad_group_id", "target_id"))
        assert key not in seen
        seen.add(key)
        identity = keyed[key]
        assert identity["classification"] == "producttarget" and entity["source"] == identity["source"]
        for name in ("expression", "resolved_expression"):
            assert type(entity[name]) is str
            assert json.loads(entity[name]) == [{"type": "asinSameAs", "value": identity["asin"]}]
    assert seen == set(keyed)
    for row, output in zip(raw["data"], parsed.data, strict=True):
        dumped = output.model_dump()
        assert dumped["ad_group_id"] == row["group_id"]
        assert dumped["targeting_text"] == row["targeting"]
        assert dumped["targeting_id"] == row["targeting_id"]
        assert dumped["direct_orders"] == row["same_orders"] and dumped["direct_sales"] == row["same_sales"]
    assert fixture == before


@pytest.mark.parametrize("method", tuple(row[0] for row in HOURLY))
def test_sp_null_token_exception_does_not_apply_to_sb(method):
    from sp_reports_contract import HOURLY_MODELS, validate_sp_report_response
    assert getattr(schema, method) not in HOURLY_MODELS
    raw = {"code": 0, "message": "success", "error_details": [], "request_id": "synthetic",
        "response_time": "2001-05-07 00:00:00", "total": 0, "data": [], "next_token": None}
    with pytest.raises(ContractError, match="响应多字段"):
        validate_sp_report_response(raw, getattr(schema, method))


def country_rule_response(method="SbTargetQueryReports"):
    """仅用于精确忽略边界的完整合成响应，不发布为真实fixture。"""
    model = getattr(schema, method)
    row_model = get_args(model.model_fields["data"].annotation)[0]
    row = {key: "2026-10-01" if key == "report_date" else
        "synthetic" if issubclass(annotation, str) else
        1.5 if issubclass(annotation, float) else 1
        for key, (_, annotation) in field_keys(row_model).items()}
    raw = {"code": 0, "message": "success", "error_details": [], "request_id": "synthetic",
        "response_time": "2001-05-07 00:00:00", "total": 1, "data": [row]}
    if "next_token" in model.model_fields:
        raw["next_token"] = None
    return raw


@pytest.mark.parametrize("country", [None, "", "DE", 0, False, 1.5, [], {}, {"future": "value"}])
def test_target_query_country_is_ignored_at_only_approved_row_path_without_mutating_raw(country):
    raw = country_rule_response()
    raw["data"][0]["country"] = country
    before = deepcopy(raw)
    with pytest.raises(ContractError, match="响应多字段"):
        validate_response(raw, schema.SbTargetQueryReports)
    run_raw_contract({"endpoint": "ads.SbTargetQueryReports", "schema": schema.SbTargetQueryReports,
        "snapshot": json.dumps(raw).encode()})
    assert raw == before
    parsed = schema.SbTargetQueryReports.model_validate(raw)
    assert "country" not in parsed.data[0].model_dump() and "country_code" not in parsed.data[0].model_dump()


@pytest.mark.parametrize("location,key", [("root", "country"), ("row", "country_code"),
    ("row", "click_units"), ("row", "view_units"), ("row", "unapproved")])
def test_target_query_country_rule_keeps_other_paths_and_unapproved_fields_strict(location, key):
    raw = country_rule_response()
    raw["data"][0]["country"] = "DE"
    (raw if location == "root" else raw["data"][0])[key] = None
    with pytest.raises(ContractError, match="响应多字段"):
        run_raw_contract({"endpoint": "ads.SbTargetQueryReports", "schema": schema.SbTargetQueryReports,
            "snapshot": json.dumps(raw).encode()})


@pytest.mark.parametrize("method", [method for method in PREFIXES if method != "SbTargetQueryReports"])
def test_country_ignore_does_not_apply_to_any_other_sb_report_method(method):
    raw = country_rule_response(method)
    validate_response(raw, getattr(schema, method))
    raw["data"][0]["country"] = None
    with pytest.raises(ContractError, match="响应多字段"):
        run_raw_contract({"endpoint": "ads." + method, "schema": getattr(schema, method),
            "snapshot": json.dumps(raw).encode()})


@pytest.mark.parametrize("model,public,wire", [
    (schema.SbKeywordQueryReport, "new_to_brand_units", "new_to_brand_units"),
    (schema.SbTargetQueryReport, "click_order_units", "units_ordered"),
    (schema.SbTargetQueryReport, "view_order_units", "view_units_ordered"),
])
def test_approved_sales_units_fields_are_required_aliased_and_preserve_counts(model, public, wire):
    from lingxingapi.fields import IntOrNone2Zero
    from pydantic import ValidationError
    field = model.model_fields[public]
    assert field.annotation is IntOrNone2Zero and field.is_required()
    assert (field.validation_alias or public) == wire
    method = "SbKeywordQueryReports" if model is schema.SbKeywordQueryReport else "SbTargetQueryReports"
    row = country_rule_response(method)["data"][0]
    for value, expected in ((None, 0), (0, 0), (3, 3), ("4", 4)):
        raw = row | {wire: value}
        parsed = model.model_validate(raw)
        assert getattr(parsed, public) == expected and type(parsed.model_dump()[public]) is int
        if wire != public:
            assert wire not in parsed.model_dump()
        assert raw[wire] is value
    del row[wire]
    with pytest.raises(ValidationError):
        model.model_validate(row)
    row[wire] = []
    with pytest.raises(ValidationError):
        model.model_validate(row)
    assert "country" not in model.model_fields and "country_code" not in model.model_fields


@pytest.mark.parametrize("method", tuple(row[0] for row in HOURLY))
def test_sb_hourly_approved_null_token_is_checking_view_only(method):
    raw = country_rule_response(method)
    raw["next_token"] = None
    before = deepcopy(raw)
    with pytest.raises(ContractError, match="响应多字段"):
        validate_response(raw, getattr(schema, method))
    run_raw_contract({"endpoint": "ads." + method, "schema": getattr(schema, method),
        "snapshot": json.dumps(raw).encode()})
    assert raw == before and "next_token" in raw


@pytest.mark.parametrize("method", tuple(row[0] for row in HOURLY))
@pytest.mark.parametrize("value", [False, 0, "", "MTAwMA==", [], {}])
def test_sb_hourly_nonnull_tokens_still_fail(method, value):
    raw = country_rule_response(method)
    raw["next_token"] = value
    with pytest.raises(ContractError, match="响应多字段"):
        run_raw_contract({"endpoint": "ads." + method, "schema": getattr(schema, method),
            "snapshot": json.dumps(raw).encode()})


@pytest.mark.parametrize("method", tuple(row[0] for row in HOURLY))
def test_sb_hourly_null_token_rule_does_not_hide_nested_or_other_unknown_fields(method):
    for location, field in (("row", "next_token"), ("root", "unapproved")):
        raw = country_rule_response(method)
        raw["next_token"] = None
        (raw if location == "root" else raw["data"][0])[field] = None
        with pytest.raises(ContractError, match="响应多字段"):
            run_raw_contract({"endpoint": "ads." + method, "schema": getattr(schema, method),
                "snapshot": json.dumps(raw).encode()})


def test_real_target_query_supplemental_keeps_country_and_wire_units_without_claiming_full_matrix():
    fixture = json.loads((DIRECTORY/"sb_target_query_reports-fields-supplemental.json").read_bytes())
    assert fixture["endpoint"] == "ads.SbTargetQueryReports" and fixture["coverage"] == "supplemental"
    assert "checks" not in fixture and "samples" not in fixture
    raw = fixture["response"]
    before = deepcopy(raw)
    parsed = validate_sb_report_response(raw, schema.SbTargetQueryReports)
    assert parsed.data and parsed.response_count == len(raw["data"])
    for row, output in zip(raw["data"], parsed.data, strict=True):
        assert row["profile_id"] == fixture["request"]["profile_id"]
        assert row["report_date"] == fixture["request"]["report_date"]
        assert "country" in row and "units_ordered" in row and "view_units_ordered" in row
        dumped = output.model_dump()
        assert "country" not in dumped and "country_code" not in dumped
        assert "units_ordered" not in dumped and "view_units_ordered" not in dumped
        assert type(dumped["click_order_units"]) is int and type(dumped["view_order_units"]) is int
    assert raw == before
