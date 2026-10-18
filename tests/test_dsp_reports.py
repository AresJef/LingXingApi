"""DSP 的官方文档契约与独立合成边界测试，不代表真实账号采集验收。"""
from __future__ import annotations

import asyncio
from copy import deepcopy
from contextlib import asynccontextmanager
import datetime
import inspect
import json
from types import SimpleNamespace
from typing import get_type_hints
from unittest.mock import AsyncMock

import pytest
from aiohttp import ClientSession
from pydantic import ValidationError, ValidationInfo

from lingxingapi import API, errors
from lingxingapi.ads import param, route, schema
from lingxingapi.ads.api import AdsAPI
from documentation_contract import documentation_example, validate_documentation, validate_field_examples

SOURCE_URL = "https://apidoc.lingxing.com/new/api-docs/newAd/report/dspReportOrderList/"

# 官方成功示例的独立副本：只替换标识、名称、请求ID、时间和游标；业务指标未改动。
DOCUMENTATION_ROW = {
    "id": 700000000000001,
    "date": "2022-10-05",
    "profile_id": "90000000000001",
    "order_id": "700000000000001",
    "order_name": "ORDER-00001",
    "advertiser_id": "80000000000001",
    "advertiser_name": "ADVERTISER-00001",
    "order_start_date": "2022-09-13",
    "order_end_date": "2023-01-01",
    "order_budget": "2715.00",
    "total_cost": 26.88,
    "spends": "26.88",
    "sales": "330.59",
    "orders": "10",
    "impressions": "4053",
    "viewable_impressions": "2176",
    "clicks": "3",
    "dpv": "51",
    "total_add_to_cart": "22",
    "order_currency": "USD",
    "ad_units": "11",
}
DOCUMENTATION_RESPONSE = {
    "code": 0,
    "message": "success",
    "error_details": [],
    "request_id": "00000000-0000-4000-8000-000000000001",
    "response_time": "2001-01-01 00:00:00",
    "next_token": "NzAwMDAwMDAwMDAwMDAx",
    "data": [DOCUMENTATION_ROW],
    "total": 1,
}
EXISTING_CORE_FIELDS = {
    "profile_id": ("profile_id", int),
    "advertiser_id": ("advertiser_id", int),
    "advertiser_name": ("advertiser_name", str),
    "order_id": ("order_id", str),
    "order_name": ("order_name", str),
    "order_start_date": ("order_start_date", str),
    "order_end_date": ("order_end_date", str),
    "budget": ("order_budget", float),
    "costs": ("spends", float),
    "impressions": ("impressions", int),
    "viewable_impressions": ("viewable_impressions", int),
    "clicks": ("clicks", int),
    "page_views": ("dpv", int),
    "add_to_cart_count": ("total_add_to_cart", int),
    "orders": ("orders", int),
    "units": ("ad_units", int),
    "sales": ("sales", float),
    "currency_code": ("order_currency", str),
}


# 官方字段表与已批准命名/缺省规则；合成非零值仅用于转换测试。
INTEGER_FIELDS = {
    "id": "record_id",
    "add_to_watchlist_views14d": "view_add_to_watchlist_count_14d",
    "dpv_views14d": "view_page_views_14d",
    "total_purchases14d": "total_orders_14d",
    "total_add_to_cart14d": "total_add_to_cart_count_14d",
    "dpv_clicks14d": "click_page_views_14d",
    "total_units_sold14d": "total_units_14d",
    "dpv14d": "page_views_14d",
    "total_detail_page_clicks14d": "click_total_page_views_14d",
    "total_detail_page_views14d": "total_page_views_14d",
    "total_detail_page_view_views14d": "view_total_page_views_14d",
    "reach": "reach",
    "measurable_impressions": "measurable_impressions",
    "gross_click_throughs": "gross_clicks",
    "gross_impressions": "gross_impressions",
    "invalid_click_throughs": "invalid_clicks",
    "invalid_impressions": "invalid_impressions",
    "product_review_page_visits": "product_review_page_visits",
    "product_review_page_visits_clicks": "click_product_review_page_visits",
    "product_review_page_visits_views": "view_product_review_page_visits",
    "total_product_review_page_visits": "total_product_review_page_visits",
    "total_product_review_page_visits_clicks": "click_total_product_review_page_visits",
    "total_product_review_page_visits_views": "view_total_product_review_page_visits",
    "add_to_list": "add_to_list_count",
    "add_to_list_clicks": "click_add_to_list_count",
    "add_to_list_views": "view_add_to_list_count",
    "total_add_to_list": "total_add_to_list_count",
    "total_add_to_list_clicks": "click_total_add_to_list_count",
    "total_add_to_list_views": "view_total_add_to_list_count",
    "add_to_cart": "direct_add_to_cart_count",
    "add_to_cart_clicks": "click_direct_add_to_cart_count",
    "add_to_cart_views": "view_direct_add_to_cart_count",
    "total_add_to_cart_clicks": "click_add_to_cart_count",
    "total_add_to_cart_views": "view_add_to_cart_count",
    "add_to_shopping_cart": "add_to_shopping_cart_count",
    "add_to_shopping_cart_clicks": "click_add_to_shopping_cart_count",
    "add_to_shopping_cart_views": "view_add_to_shopping_cart_count",
    "add_to_watchlist": "add_to_watchlist_count",
    "add_to_watchlist_clicks": "click_add_to_watchlist_count",
    "total_purchases_views": "view_total_orders",
    "total_purchases_clicks": "click_total_orders",
    "purchases": "direct_orders",
    "purchases_clicks": "click_direct_orders",
    "purchases_views": "view_direct_orders",
    "units_sold": "direct_units",
    "combined_purchases": "combined_orders",
    "combined_units_sold": "combined_units",
    "combined_purchases_views": "view_combined_orders",
    "combined_purchases_clicks": "click_combined_orders",
    "brand_searches": "brand_searches",
    "brand_searches_clicks": "click_brand_searches",
    "brand_searches_views": "view_brand_searches",
    "new_to_brand_purchases": "new_to_brand_orders",
    "new_to_brand_purchases_views": "view_new_to_brand_orders",
    "new_to_brand_purchases_clicks": "click_new_to_brand_orders",
    "new_to_brand_units_sold": "new_to_brand_units",
    "new_to_brand_detail_page_views": "new_to_brand_page_views",
    "total_new_to_brand_purchases": "total_new_to_brand_orders",
    "total_new_to_brand_purchases_clicks": "click_total_new_to_brand_orders",
    "total_new_to_brand_purchases_views": "view_total_new_to_brand_orders",
    "total_new_to_brand_units_sold": "total_new_to_brand_units",
    "total_new_to_brand_dpvs": "total_new_to_brand_page_views",
    "video_ad_start": "video_starts",
    "video_ad_first_quartile": "video_25pct_views",
    "video_ad_midpoint": "video_50pct_views",
    "video_ad_third_quartile": "video_75pct_views",
    "video_ad_complete": "video_100pct_views",
    "indirect_purchases": "indirect_orders",
    "indirect_units_sold": "indirect_units",
}
FLOAT_FIELDS = {
    "amazon_platform_fee": "amazon_platform_fee",
    "total_roas14d": "total_roas_14d",
    "total_cost": "total_cost",
    "total_sales14d": "total_sales_14d",
    "frequency_average": "frequency_average",
    "roas": "roas",
    "combined_product_sales": "combined_sales",
    "long_term_sales": "long_term_sales",
    "brand_search_rate": "brand_search_rate",
    "new_to_brand_product_sales": "new_to_brand_sales",
    "new_to_brand_detail_page_view_rate": "new_to_brand_page_view_rate",
    "total_new_to_brand_sales": "total_new_to_brand_sales",
    "total_new_to_brand_purchases_percentage": "total_new_to_brand_order_pct",
    "agency_fee": "agency_fee",
    "total_fee": "total_fee",
    "measurable_rate": "measurable_rate",
    "viewable_rate": "viewable_rate",
    "indirect_sales": "indirect_sales",
    "total_new_to_brand_purchase_rate": "total_new_to_brand_order_rate",
    "new_to_brand_purchases_percentage": "new_to_brand_order_pct",
    "ctr": "ctr",
    "ecpm": "ecpm",
    "eCPC": "cpc",
    "eCPBrandSearch": "cost_per_brand_search",
    "combinedROAS": "combined_roas",
    "longTermROAS": "long_term_roas",
    "newToBrandROAS": "new_to_brand_roas",
    "totalNewToBrandROAS": "total_new_to_brand_roas",
    "totalNewToBrandDPVRate": "total_new_to_brand_page_view_rate",
    "3PFees": "third_party_fees",
    "totalDPVR": "total_page_view_rate",
    "PRPVR": "product_review_page_visit_rate",
    "totalPRPVR": "total_product_review_page_visit_rate",
    "ATCR": "add_to_cart_rate",
    "totalATCR": "total_add_to_cart_rate",
    "ACOS": "acos",
}
NUMERIC_FIELDS = [(wire, name, int) for wire, name in INTEGER_FIELDS.items()] + [
    (wire, name, float) for wire, name in FLOAT_FIELDS.items()
]
COMPUTED_FIELDS = {
    "measurable_rate": "measurable_rate",
    "viewable_rate": "viewable_rate",
    "indirect_purchases": "indirect_orders",
    "indirect_units_sold": "indirect_units",
    "indirect_sales": "indirect_sales",
    "total_new_to_brand_purchase_rate": "total_new_to_brand_order_rate",
    "new_to_brand_purchases_percentage": "new_to_brand_order_pct",
    "eCPC": "cpc",
    "totalDPVR": "total_page_view_rate",
    "PRPVR": "product_review_page_visit_rate",
    "totalPRPVR": "total_product_review_page_visit_rate",
    "ATCR": "add_to_cart_rate",
    "totalATCR": "total_add_to_cart_rate",
    "ACOS": "acos",
}
DEFERRED_FIELDS = (
    "survey_finish_cpa14d",
    "application_views14d",
    "brand_store_engagement5_clicks",
    "click_on_redirect_clicks14d",
    "sign_up_button_views14d",
    "mashup_subscribe_and_save_click_views14d",
    "referral_cvr14d",
    "dpvr14d",
    "mobile_app_first_starts_cpa14d",
    "brand_store_engagement2_clicks",
    "application_cvr14d",
    "widget_interaction_clicks14d",
    "brand_store_engagement1_cpa",
    "email_interaction_clicks14d",
    "rentals_views14d",
    "purchase_button14d",
    "referral_cpa14d",
    "marketing_landing_page14d",
)


def test_dsp_existing_fields_parse_documentation_numeric_strings_without_changing_metrics():
    raw = deepcopy(DOCUMENTATION_RESPONSE)
    before = deepcopy(raw)
    parsed = schema.DspReports.model_validate(raw)
    row = parsed.data[0]
    for name, (wire, output_type) in EXISTING_CORE_FIELDS.items():
        assert type(getattr(row, name)) is output_type
        assert getattr(row, name) == output_type(raw["data"][0][wire])
    assert row.budget == 2715.0 and row.costs == 26.88 and row.clicks == 3
    assert parsed.response_count == parsed.total_count == 1 and parsed.errors == []
    assert raw == before


@pytest.mark.parametrize("name, wire_type", EXISTING_CORE_FIELDS.items())
@pytest.mark.parametrize("mode", ["missing", "null"])
def test_dsp_existing_required_fields_keep_null_and_missing_rejection_separate(name, wire_type, mode):
    wire, _ = wire_type
    raw = deepcopy(DOCUMENTATION_ROW)
    if mode == "missing":
        del raw[wire]
    else:
        raw[wire] = None
    with pytest.raises(ValidationError):
        schema.DspReport.model_validate(raw)


def test_dsp_existing_field_examples_are_complete_and_preserve_official_metrics():
    example = validate_field_examples(schema.DspReport)
    for name, (wire, output_type) in EXISTING_CORE_FIELDS.items():
        assert example[name] == output_type(DOCUMENTATION_ROW[wire])


def test_dsp_date_validator_documents_supported_types_without_changing_parser():
    hints = get_type_hints(param.DspReports._validate_date)
    assert hints == {"v": str | datetime.date | datetime.datetime, "info": ValidationInfo, "return": str}
    assert param.DspReports._validate_date.__doc__
    for name in ("start_date", "end_date"):
        field = param.DspReports.model_fields[name]
        assert field.description and field.examples and field.is_required()


@pytest.mark.parametrize("value, expected", [
    ("2022-10-05", "2022-10-05"),
    ("2022-10-05 12:30:00", "2022-10-05"),
    (datetime.date(2022, 10, 5), "2022-10-05"),
    (datetime.datetime(2022, 10, 5, 12, 30), "2022-10-05"),
    ("2026-09", "2026-09-01"),
    ("2026-09-31", "2026-09-30"),
])
def test_dsp_advertiser_only_dates_use_existing_parser(value, expected):
    raw = {"start_date": value, "end_date": value, "advertiser_id": 80000000000001}
    before = deepcopy(raw)
    parsed = param.DspReports.model_validate(raw)
    assert parsed.start_date == parsed.end_date == expected
    assert parsed.model_dump_params() == {
        "dsp_advertiser_id": 80000000000001, "start_date": expected, "end_date": expected,
    }
    assert raw == before


@pytest.mark.parametrize("fields, expected", [
    ({}, {}),
    ({"offset": None, "length": None, "next_token": None}, {}),
    ({"offset": 0, "length": 0}, {"offset": 0, "length": 0}),
    ({"offset": "2", "length": "20", "next_token": " NzI1 "}, {"offset": 2, "length": 20, "next_token": "NzI1"}),
])
def test_dsp_advertiser_pagination_none_omission_zero_preservation_and_cursor(fields, expected):
    args = {"start_date": "2022-10-05", "end_date": "2022-12-01", "advertiser_id": 80000000000001, **fields}
    assert param.DspReports.model_validate_params(args) == {
        "start_date": "2022-10-05", "end_date": "2022-12-01", "dsp_advertiser_id": 80000000000001, **expected,
    }


@pytest.mark.parametrize("fields", [
    {}, {"profile_id": None}, {"advertiser_id": None}, {"profile_id": None, "advertiser_id": None},
    {"advertiser_id": -1}, {"advertiser_id": []}, {"advertiser_id": 1.5},
    {"profile_id": -1, "advertiser_id": 1},
    {"profile_id": 1, "advertiser_id": -1},
    {"advertiser_id": 1, "offset": -1},
    {"advertiser_id": 1, "length": -1},
    {"advertiser_id": 1, "next_token": ""},
])
def test_dsp_identifiers_and_pagination_reject_invalid_fields(fields):
    with pytest.raises(ValidationError):
        param.DspReports.model_validate_params({"start_date": "2022-10-05", "end_date": "2022-12-01", **fields})


@pytest.mark.parametrize("start, end", [
    ("2001-01-01", "2001-12-31"),
    ("2026-10-05", "2026-10-01"),
])
def test_dsp_existing_parameter_does_not_add_local_range_or_order_restrictions(start, end):
    parsed = param.DspReports.model_validate_params({"start_date": start, "end_date": end, "advertiser_id": 1})
    assert parsed["start_date"] == start and parsed["end_date"] == end


def test_dsp_sdk_advertiser_only_and_cursor_use_public_request_path():
    signed = AsyncMock(return_value={"code": 0, "message": "success", "data": [], "total": 0, "next_token": ""})
    result = asyncio.run(AdsAPI.DspReports(
        SimpleNamespace(_request_with_sign=signed), "2022-10-05", "2022-12-01",
        advertiser_id=80000000000001, next_token=" NzI1 ", offset=0, length=20,
    ))
    signed.assert_awaited_once_with("POST", route.DSP_REPORTS, body={
        "start_date": "2022-10-05", "end_date": "2022-12-01", "dsp_advertiser_id": 80000000000001,
        "next_token": "NzI1", "offset": 0, "length": 20,
    })
    assert type(result) is schema.DspReports and result.data == [] and result.next_token == ""


def test_dsp_sdk_missing_identifiers_fail_before_request():
    signed = AsyncMock()
    with pytest.raises(errors.InvalidParametersError) as caught:
        asyncio.run(AdsAPI.DspReports(SimpleNamespace(_request_with_sign=signed), "2022-10-05", "2022-12-01"))
    assert isinstance(caught.value.__cause__, ValidationError)
    signed.assert_not_awaited()


@pytest.mark.parametrize("wire, name, output_type", NUMERIC_FIELDS)
@pytest.mark.parametrize("mode", ["missing", "null", "blank", "number", "numeric_string"])
def test_dsp_added_numeric_fields_parse_values_aliases_and_zero_defaults(wire, name, output_type, mode):
    raw = deepcopy(DOCUMENTATION_ROW)
    raw.pop(wire, None)
    expected = output_type(0)
    if mode != "missing":
        value = output_type(7) if output_type is int else 7.125
        raw[wire] = {"null": None, "blank": "", "number": value, "numeric_string": str(value)}[mode]
        if mode in ("number", "numeric_string"):
            expected = value
    before = deepcopy(raw)
    parsed = schema.DspReport.model_validate(raw)
    assert type(getattr(parsed, name)) is output_type and getattr(parsed, name) == expected
    dumped = parsed.model_dump()
    assert type(dumped[name]) is output_type and dumped[name] == expected
    assert json.loads(parsed.model_dump_json())[name] == expected
    if wire != name:
        assert wire not in dumped and wire not in parsed.model_dump(by_alias=True)
        assert schema.DspReport.model_fields[name].validation_alias == wire
    assert raw == before


@pytest.mark.parametrize("wire, name, output_type", NUMERIC_FIELDS)
@pytest.mark.parametrize("bad", ["invalid", [], {}])
def test_dsp_added_numeric_fields_reject_invalid_values_instead_of_zeroing_errors(wire, name, output_type, bad):
    raw = deepcopy(DOCUMENTATION_ROW)
    raw[wire] = bad
    with pytest.raises(ValidationError) as caught:
        schema.DspReport.model_validate(raw)
    assert any(error["loc"] == (wire,) for error in caught.value.errors())


@pytest.mark.parametrize("wire, name", INTEGER_FIELDS.items())
def test_dsp_added_integer_fields_reject_fractional_values(wire, name):
    with pytest.raises(ValidationError):
        schema.DspReport.model_validate({**DOCUMENTATION_ROW, wire: 1.5})


@pytest.mark.parametrize("wire, name", COMPUTED_FIELDS.items())
def test_dsp_computed_metrics_use_response_or_zero_without_recalculation(wire, name):
    raw = {**DOCUMENTATION_ROW, "measurable_impressions": 1000, "purchases": 2,
           "total_purchases14d": 15, "units_sold": 3, "total_units_sold14d": 20,
           "total_sales14d": 500, "total_new_to_brand_purchases": 1,
           "new_to_brand_purchases": 1, "total_detail_page_views14d": 100,
           "product_review_page_visits": 6, "total_product_review_page_visits": 8,
           "add_to_cart": 9, "total_add_to_cart14d": 12}
    assert getattr(schema.DspReport.model_validate(raw), name) == 0
    raw[wire] = 19 if wire in INTEGER_FIELDS else 19.125
    assert getattr(schema.DspReport.model_validate(raw), name) == raw[wire]


@pytest.mark.parametrize("wire", DEFERRED_FIELDS)
def test_dsp_deferred_fields_are_still_unmodelled_and_do_not_change_existing_fields(wire):
    result = schema.DspReport.model_validate({**DOCUMENTATION_ROW, wire: "unconfirmed"})
    assert wire not in result.model_dump()
    assert wire not in {f.validation_alias or f.alias or key for key, f in schema.DspReport.model_fields.items()}
    assert result.costs == 26.88 and result.clicks == 3


@pytest.mark.parametrize("name", ["entity_id", "order_external_id"])
@pytest.mark.parametrize("value", [None, "", " synthetic-id "])
def test_dsp_optional_text_fields_preserve_strings_and_convert_null(name, value):
    result = schema.DspReport.model_validate({**DOCUMENTATION_ROW, name: value})
    assert getattr(result, name) == ("" if value is None else value)
    assert getattr(schema.DspReport.model_validate(DOCUMENTATION_ROW), name) == ""


@pytest.mark.parametrize("bad", [None, 123, [], {}])
def test_dsp_report_date_is_a_required_response_string(bad):
    raw = deepcopy(DOCUMENTATION_ROW)
    raw["date"] = bad
    with pytest.raises(ValidationError):
        schema.DspReport.model_validate(raw)
    del raw["date"]
    with pytest.raises(ValidationError):
        schema.DspReport.model_validate(raw)


@pytest.mark.parametrize("value", ["", None, "NzI1", " NzI1 "])
def test_dsp_response_cursor_is_preserved_using_project_null_to_blank_rule(value):
    result = schema.DspReports.model_validate({**DOCUMENTATION_RESPONSE, "next_token": value})
    assert type(result.next_token) is str
    assert result.next_token == ("" if value is None else value)
    assert result.model_dump()["next_token"] == result.next_token
    assert json.loads(result.model_dump_json())["next_token"] == result.next_token


def test_dsp_response_requires_documented_cursor_and_empty_page_has_zero_counts():
    raw = deepcopy(DOCUMENTATION_RESPONSE)
    del raw["next_token"]
    with pytest.raises(ValidationError):
        schema.DspReports.model_validate(raw)
    result = schema.DspReports.model_validate({**DOCUMENTATION_RESPONSE, "data": [], "total": 0, "next_token": ""})
    assert result.data == [] and result.response_count == result.total_count == 0 and result.next_token == ""


@pytest.mark.parametrize("profile", [0, 90000000000001, "90000000000001", " 90000000000001 "])
def test_dsp_profile_id_preserves_numeric_input_validation_and_serializes_as_string(profile):
    result = param.DspReports(start_date="2022-10-05", end_date="2022-12-01", profile_id=profile)
    assert type(result.profile_id) is int and result.profile_id == int(profile)
    assert result.model_dump_params()["profile_id"] == str(int(profile))
    assert json.loads(result.model_dump_json())["profile_id"] == str(int(profile))


@pytest.mark.parametrize("profile", ["not-an-id", -1, 1.5, [], {}])
def test_dsp_profile_id_does_not_accept_arbitrary_strings_after_wire_type_change(profile):
    with pytest.raises(ValidationError):
        param.DspReports(start_date="2022-10-05", end_date="2022-12-01", profile_id=profile)


def test_dsp_both_ids_validate_and_remain_in_body_with_advertiser_priority_documented():
    result = param.DspReports(start_date="2022-10-05", end_date="2022-12-01", profile_id=0, advertiser_id=0)
    body = result.model_dump_params()
    assert body["profile_id"] == "0" and body["dsp_advertiser_id"] == 0
    assert "优先使用advertiser_id" in param.DspReports.model_fields["profile_id"].description


def test_dsp_public_advertiser_field_uses_only_a_serialization_alias():
    args = {"start_date": "2022-10-05", "end_date": "2022-12-01", "advertiser_id": 80000000000001}
    result = param.DspReports.model_validate(args)
    field = param.DspReports.model_fields["advertiser_id"]
    assert field.serialization_alias == "dsp_advertiser_id"
    assert field.alias is None and field.validation_alias is None
    assert result.advertiser_id == args["advertiser_id"]
    assert result.model_dump(exclude_none=True) == args
    assert result.model_dump_params()[field.serialization_alias] == args["advertiser_id"]
    assert "advertiser_id" not in result.model_dump_params()
    assert json.loads(result.model_dump_json(by_alias=True, exclude_none=True)) == result.model_dump_params()
    input_properties = param.DspReports.model_json_schema(mode="validation")["properties"]
    assert "advertiser_id" in input_properties and field.serialization_alias not in input_properties
    with pytest.raises(ValidationError):
        param.DspReports.model_validate({"start_date": args["start_date"], "end_date": args["end_date"], field.serialization_alias: args["advertiser_id"]})


def test_dsp_api_exposes_advertiser_id_without_old_public_keyword_compatibility():
    parameters = inspect.signature(AdsAPI.DspReports).parameters
    assert parameters["advertiser_id"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert tuple(parameters)[1:5] == ("start_date", "end_date", "profile_id", "advertiser_id")
    assert parameters["advertiser_id"].default is None
    wire_key = param.DspReports.model_fields["advertiser_id"].serialization_alias
    assert wire_key not in parameters and wire_key not in param.DspReports.model_fields
    signed = AsyncMock()
    with pytest.raises(TypeError):
        asyncio.run(AdsAPI.DspReports(SimpleNamespace(_request_with_sign=signed), "2022-10-05", "2022-12-01", 90000000000001,
                                     **{wire_key: 80000000000001}))
    signed.assert_not_awaited()
    assert "advertiser_id (int | None)" in AdsAPI.DspReports.__doc__
    assert wire_key not in AdsAPI.DspReports.__doc__
    assert "X-API-VERSION" not in AdsAPI.DspReports.__doc__


def test_dsp_preserves_existing_advertiser_positional_call_and_protocol_alias():
    signed = AsyncMock(return_value={"code": 0, "message": "success", "data": [], "total": 0, "next_token": ""})
    result = asyncio.run(AdsAPI.DspReports(SimpleNamespace(_request_with_sign=signed), "2022-10-05", "2022-12-01",
                                         None, 80000000000001))
    signed.assert_awaited_once_with("POST", route.DSP_REPORTS, body={
        "start_date": "2022-10-05", "end_date": "2022-12-01", "dsp_advertiser_id": 80000000000001,
    })
    assert type(result) is schema.DspReports and result.data == []


def test_dsp_old_positional_profile_call_keeps_request_route_and_propagates_validation():
    signed = AsyncMock(return_value=deepcopy(DOCUMENTATION_RESPONSE))
    result = asyncio.run(AdsAPI.DspReports(SimpleNamespace(_request_with_sign=signed), "2022-10-05", "2022-12-01", 90000000000001))
    signed.assert_awaited_once_with("POST", route.DSP_REPORTS, body={
        "start_date": "2022-10-05", "end_date": "2022-12-01", "profile_id": "90000000000001",
    })
    assert result.data[0].costs == 26.88 and result.data[0].clicks == 3
    signed.reset_mock()
    signed.return_value = {**DOCUMENTATION_RESPONSE, "data": [{**DOCUMENTATION_ROW, "eCPC": "bad"}]}
    with pytest.raises(ValidationError):
        asyncio.run(AdsAPI.DspReports(SimpleNamespace(_request_with_sign=signed), "2022-10-05", "2022-12-01", 90000000000001))
    signed.assert_awaited_once()


def test_dsp_http_json_uses_profile_string_and_advertiser_protocol_alias_without_version_header(monkeypatch):
    calls = []

    @asynccontextmanager
    async def request(session, verb, url, **options):
        calls.append((verb, url, options, session._prepare_headers(options.get("headers"))))
        yield SimpleNamespace(status=200, reason="synthetic", read=AsyncMock(return_value=json.dumps(DOCUMENTATION_RESPONSE).encode()))

    monkeypatch.setattr(ClientSession, "request", request)

    async def run():
        async with API("0" * 16, "synthetic-only-secret") as client:
            client._state.access_token = "synthetic-only-token"
            result = await client.ads.DspReports("2022-10-05", "2022-12-01", 90000000000001,
                                                 advertiser_id=80000000000001, next_token=" NzI1 ")
            assert result.next_token == DOCUMENTATION_RESPONSE["next_token"] and result.data[0].record_id == DOCUMENTATION_ROW["id"]

    asyncio.run(run())
    assert len(calls) == 1
    verb, url, options, headers = calls[0]
    assert verb == "POST" and url.endswith(route.DSP_REPORTS)
    assert json.loads(json.dumps(options["json"])) == {
        "profile_id": "90000000000001", "dsp_advertiser_id": 80000000000001,
        "next_token": "NzI1", "start_date": "2022-10-05", "end_date": "2022-12-01",
    }
    assert options.get("headers") is None
    assert "X-API-VERSION" not in headers


def test_dsp_public_documentation_and_field_examples_match_complete_normalized_official_example():
    shown = validate_documentation(AdsAPI.DspReports, schema.DspReports)
    normalized = schema.DspReports.model_validate(deepcopy(DOCUMENTATION_RESPONSE)).model_dump()
    assert shown == normalized and shown["response_count"] == shown["total_count"] == 1
    record = validate_field_examples(schema.DspReport)
    assert record == normalized["data"][0]
    assert schema.DspReports.model_fields["data"].examples == [normalized["data"]]
    assert len(record) == 126 and len(NUMERIC_FIELDS) == 105 and len(COMPUTED_FIELDS) == 14
    assert schema.DspReports.model_fields["data"].description
    call, _ = documentation_example(AdsAPI.DspReports)
    assert {keyword.arg for keyword in call.keywords} == {"start_date", "end_date", "profile_id", "offset", "length"}
    assert SOURCE_URL in AdsAPI.DspReports.__doc__
