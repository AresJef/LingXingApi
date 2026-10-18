"""Ads 参数、SDK 请求组装与真实脱敏 fixture 的离线契约测试。"""

from __future__ import annotations

import asyncio
import ast
from contextlib import asynccontextmanager
from copy import deepcopy
import datetime
import inspect
import json
from pathlib import Path
from types import SimpleNamespace
from typing import get_type_hints
from unittest.mock import AsyncMock

import pytest
from aiohttp import ClientSession
from cytimes import Pydt
from pydantic import ValidationError

from lingxingapi import API, errors
from lingxingapi.ads import param, route, schema
from lingxingapi.ads.api import AdsAPI
from response_contract import load_json_bytes, validate_response
from documentation_contract import validate_documentation, documentation_example, validate_field_examples


@pytest.mark.parametrize("key", ["profile_type", "type"])
@pytest.mark.parametrize("profile_type", ["seller", "dsp", "vendor", "other"])
def test_ad_profiles_type_alias_and_existing_nonempty_rule(key: str, profile_type: str) -> None:
    # Literal 是签名提示，现有模型不把账号类型限制为枚举。
    assert param.AdProfiles.model_validate_params({key: " " + profile_type + " "}) == {"type": profile_type}


@pytest.mark.parametrize(
    "values, expected",
    [
        ({}, {"type": "seller"}),
        ({"offset": None, "length": None}, {"type": "seller"}),
        ({"offset": 0, "length": 0}, {"type": "seller", "offset": 0, "length": 0}),
        ({"offset": "2", "length": "20"}, {"type": "seller", "offset": 2, "length": 20}),
        ({"offset": 2.0, "length": 20.0}, {"type": "seller", "offset": 2, "length": 20}),
        ({"offset": None, "length": 20}, {"type": "seller", "length": 20}),
        ({"offset": 2, "length": None}, {"type": "seller", "offset": 2}),
    ],
)
def test_ad_profiles_pagination_dump_and_input_unchanged(values: dict, expected: dict) -> None:
    raw = {"profile_type": "seller", **values}
    before = deepcopy(raw)
    parsed = param.AdProfiles.model_validate(raw)
    assert parsed.model_dump_params() == expected
    assert param.AdProfiles.model_validate_params(raw) == expected
    assert raw == before
    for key in ("offset", "length"):
        if key in expected:
            assert type(getattr(parsed, key)) is int


def test_ad_profiles_existing_alias_precedence_and_field_name_dump() -> None:
    parsed = param.AdProfiles.model_validate({"type": "vendor", "profile_type": "seller"})
    assert parsed.model_dump_params() == {"type": "vendor"}
    assert parsed.model_dump_params(by_alias=False) == {"profile_type": "vendor"}


@pytest.mark.parametrize(
    "raw",
    [{}, {"profile_type": None}, {"profile_type": ""}, {"profile_type": "  "}, {"profile_type": 1},
     {"profile_type": "seller", "offset": -1}, {"profile_type": "seller", "length": -1},
     {"profile_type": "seller", "offset": 1.5}, {"profile_type": "seller", "length": 1.5}],
)
def test_ad_profiles_invalid_parameters(raw: dict) -> None:
    with pytest.raises(ValidationError):
        param.AdProfiles.model_validate_params(raw)


@pytest.fixture
def synthetic_response() -> dict:
    return {
        "code": 0, "message": "success", "error_details": [],
        "request_id": "synthetic-ad-profiles-only", "response_time": "2001-05-07 05:14:42",
        "total": 50,
        "data": [{"sid": None, "name": "sample-profile", "country_code": "GB", "currency_code": "GBP",
                  "profile_id": "12345", "type": "seller", "status": "1"}],
    }


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({}, {"type": "seller"}),
        ({"profile_type": "dsp", "offset": 0, "length": 20}, {"type": "dsp", "offset": 0, "length": 20}),
        ({"profile_type": "vendor", "offset": "2", "length": "20"}, {"type": "vendor", "offset": 2, "length": 20}),
        ({"profile_type": "other", "offset": 0, "length": 0}, {"type": "other", "offset": 0, "length": 0}),
    ],
)
def test_sdk_ad_profiles_request_and_response_model(kwargs: dict, expected: dict, synthetic_response: dict) -> None:
    synthetic_response["data"][0]["type"] = expected["type"]
    before = deepcopy(synthetic_response)
    signed = AsyncMock(return_value=synthetic_response)
    api = SimpleNamespace(_request_with_sign=signed)

    result = asyncio.run(AdsAPI.AdProfiles(api, **kwargs))

    signed.assert_awaited_once_with("POST", route.AD_PROFILES, body=expected, headers={"X-API-VERSION": "2"})
    assert isinstance(result, schema.AdProfiles)
    assert result.data[0].model_dump() == {
        "sid": 0, "seller_name": "sample-profile", "country_code": "GB", "currency_code": "GBP",
        "profile_id": 12345, "profile_type": expected["type"], "profile_status": 1,
    }
    assert result.errors == [] and result.response_count == 1 and result.total_count == 50
    assert synthetic_response == before


@pytest.mark.parametrize("kwargs", [{"profile_type": ""}, {"profile_type": None}, {"offset": -1}, {"length": 1.5}])
def test_sdk_ad_profiles_invalid_parameters_never_request(kwargs: dict) -> None:
    signed = AsyncMock()
    with pytest.raises(errors.InvalidParametersError) as caught:
        asyncio.run(AdsAPI.AdProfiles(SimpleNamespace(_request_with_sign=signed), **kwargs))
    assert isinstance(caught.value.__cause__, ValidationError)
    signed.assert_not_awaited()


def test_ad_profiles_frozen_documentation_fixture_contract() -> None:
    """冻结20条文档样例；无tools/raw/pass依赖，不代表当前四请求集合。"""
    path = Path(__file__).with_name("fixtures") / "ads/basic/common/ad_profiles.json"
    assert path.is_file() and not path.is_symlink()
    fixture = load_json_bytes(path.read_bytes())
    assert fixture["source"] in {"live", "local_raw"} and fixture["endpoint"] == "ads.AdProfiles"
    raw = fixture["response"]
    before = deepcopy(raw)
    parsed = validate_response(raw, schema.AdProfiles)
    assert raw == before
    assert len(raw["data"]) == len(parsed.data) == parsed.response_count == 20
    assert parsed.total_count == raw["total"] == 240 and parsed.response_count < parsed.total_count
    assert parsed.errors == raw["error_details"] == []
    for wire, profile in zip(raw["data"], parsed.data, strict=True):
        assert type(wire["sid"]) is type(wire["profile_id"]) is str
        assert type(profile.sid) is type(profile.profile_id) is int
        assert profile.sid == int(wire["sid"]) and profile.profile_id == int(wire["profile_id"])
        assert profile.seller_name == wire["name"]
        assert profile.profile_type == wire["type"] == "seller"
        assert profile.profile_status == wire["status"]
        assert profile.country_code == wire["country_code"] and profile.currency_code == wire["currency_code"]
    doc = inspect.getdoc(AdsAPI.AdProfiles)
    assert doc.count(".. code-block:: python") == 2
    assert "Args:" in doc and "Returns:" in doc and "Examples:" in doc
    assert "profile_type (" in doc and "account_type" not in doc
    shown = validate_documentation(AdsAPI.AdProfiles, schema.AdProfiles)
    call, _ = documentation_example(AdsAPI.AdProfiles)
    arguments = {item.arg: ast.literal_eval(item.value) for item in call.keywords}
    assert all(row['profile_type'] == arguments['profile_type'] for row in shown['data'] if row is not Ellipsis)


ENTITY_MODELS = [
    (param.AdEntities, {}, {}),
    (param.SpNegativeTargeting, {"target_type": "keyword"}, {"target_type": "keyword"}),
    (param.SbTargeting, {"ad_type": "SB", "target_type": "product"},
     {"ads_type": "SB", "targeting_type": "producttarget"}),
    (param.AdReports, {"report_date": "2026-10-15"}, {"report_date": "2026-10-15"}),
    (param.SpQueryReports, {"report_date": "2026-10-15", "target_type": "keyword"},
     {"report_date": "2026-10-15", "target_type": "keyword"}),
    (param.SbTargetingReports, {"report_date": "2026-10-15", "ad_type": "ALL", "target_type": "product"},
     {"report_date": "2026-10-15", "sponsored_type": "ALL", "target_type": "producttarget"}),
    (param.SbQueryReports, {"report_date": "2026-10-15", "target_type": "keyword"},
     {"report_date": "2026-10-15", "target_type": "keyword"}),
]


@pytest.mark.parametrize("model,extra,wire", ENTITY_MODELS)
@pytest.mark.parametrize(
    "identifiers,expected",
    [
        ({"sid": 1}, {"sid": 1}),
        ({"profile_id": 2}, {"profile_id": 2}),
        ({"sid": 1, "profile_id": 2}, {"sid": 1, "profile_id": 2}),
        ({"sid": 1, "profile_id": None}, {"sid": 1}),
        ({"sid": None, "profile_id": 2}, {"profile_id": 2}),
        ({"sid": " 1 ", "profile_id": 2.0}, {"sid": 1, "profile_id": 2}),
        ({"sid": 0}, {"sid": 0}),
        ({"profile_id": 0}, {"profile_id": 0}),
        ({"sid": 0, "profile_id": 0}, {"sid": 0, "profile_id": 0}),
        ({"sid": False, "profile_id": True}, {"sid": 0, "profile_id": 1}),
    ],
)
def test_ad_entities_identifiers_across_derived_models(model, extra, wire, identifiers, expected):
    raw = {**extra, **identifiers}
    untouched = deepcopy(raw)
    parsed = model.model_validate(raw)
    assert parsed.model_dump_params() == model.model_validate_params(raw) == {**wire, **expected}
    assert raw == untouched
    assert all(type(getattr(parsed, key)) is int for key in expected)
    assert parsed.model_dump_params(exclude_none=False)["sid"] == expected.get("sid")
    assert parsed.model_dump_params(exclude_none=False)["profile_id"] == expected.get("profile_id")


@pytest.mark.parametrize("model,extra,wire", ENTITY_MODELS)
@pytest.mark.parametrize("identifiers", [{}, {"sid": None}, {"profile_id": None}, {"sid": None, "profile_id": None}])
def test_ad_entities_requires_at_least_one_identifier(model, extra, wire, identifiers):
    with pytest.raises(ValidationError, match="sid 和 profile_id 至少提供一个") as caught:
        model.model_validate_params({**extra, **identifiers})
    assert caught.value.errors()[0]["loc"] == ()


@pytest.mark.parametrize("model,extra,wire", ENTITY_MODELS)
@pytest.mark.parametrize("bad_key", ["sid", "profile_id"])
@pytest.mark.parametrize("bad_value", [-1, 1.5, "invalid", "", []])
def test_ad_entities_does_not_discard_invalid_identifier_when_other_is_valid(model, extra, wire, bad_key, bad_value):
    raw = {**extra, "sid": 1, "profile_id": 2, bad_key: bad_value}
    with pytest.raises(ValidationError) as caught:
        model.model_validate(raw)
    assert [error["loc"] for error in caught.value.errors()] == [(bad_key,)]


def test_ad_entities_preserves_pagination_state_token_and_serialization():
    raw = {"sid": 1, "state": " other ", "next_token": " opaque-token ", "offset": "2", "length": 0}
    untouched = deepcopy(raw)
    expected = {"sid": 1, "state": "other", "next_token": "opaque-token", "offset": 2, "length": 0}
    parsed = param.AdEntities.model_validate(raw)
    assert parsed.model_dump_params() == expected
    assert list(parsed.model_dump_params()) == sorted(expected)
    assert parsed.model_dump_params(include={"sid", "length"}) == {"length": 0, "sid": 1}
    assert parsed.model_dump_params(exclude={"next_token"}) == {key: value for key, value in expected.items() if key != "next_token"}
    assert raw == untouched


@pytest.mark.parametrize("key,value", [("offset", -1), ("length", 1.5), ("state", " "), ("next_token", "")])
def test_ad_entities_keeps_existing_nonidentifier_rejections(key, value):
    with pytest.raises(ValidationError) as caught:
        param.AdEntities.model_validate({"sid": 1, key: value})
    assert [error["loc"] for error in caught.value.errors()] == [(key,)]


ENTITY_SDK_CASES = [
    ("Portfolios", route.PORTFOLIOS, {}, {}, {"X-API-VERSION": "2"}),
    ("SpCampaigns", route.SP_CAMPAIGNS, {}, {}, {"X-API-VERSION": "2"}),
    ("SpNegativeKeywords", route.SP_NEGATIVE_TARGETING, {}, {"target_type": "keyword"}, {"X-API-VERSION": "2"}),
    ("SbTargets", route.SB_TARGETING, {}, {"ads_type": "ALL", "targeting_type": "producttarget"}, {"X-API-VERSION": "2"}),
    ("SpCampaignReports", route.SP_CAMPAIGN_REPORTS, {"report_date": "2026-10-15"},
     {"report_date": "2026-10-15", "show_detail": 0}, {"X-API-VERSION": "2"}),
    ("SpKeywordQueryReports", route.SP_QUERY_REPORTS, {"report_date": "2026-10-15"},
     {"report_date": "2026-10-15", "show_detail": 0, "target_type": "keyword"}, {"X-API-VERSION": "2"}),
    ("SbKeywordReports", route.SB_TARGETING_REPORTS, {"report_date": "2026-10-15"},
     {"report_date": "2026-10-15", "sponsored_type": "ALL", "target_type": "keyword"}, {"X-API-VERSION": "2"}),
    ("SbKeywordQueryReports", route.SB_QUERY_REPORTS, {"report_date": "2026-10-15"},
     {"report_date": "2026-10-15", "target_type": "keyword"}, {"X-API-VERSION": "2"}),
]


def synthetic_entity_response() -> dict:
    return {"code": 0, "message": "success", "error_details": [], "request_id": "synthetic-entities-only",
            "response_time": "2001-05-07 05:14:42", "total": 0, "next_token": "", "data": []}


@pytest.mark.parametrize("method,endpoint,extra,wire,headers", ENTITY_SDK_CASES)
@pytest.mark.parametrize(
    "identifiers,expected",
    [({"sid": 1, "profile_id": None}, {"sid": 1}),
     ({"sid": None, "profile_id": 2}, {"profile_id": 2}),
     ({"sid": 1, "profile_id": 2}, {"sid": 1, "profile_id": 2}),
     ({"sid": 0, "profile_id": None}, {"sid": 0}),
     ({"sid": None, "profile_id": 0}, {"profile_id": 0})],
)
def test_ad_entities_sdk_exact_requests_for_each_parameter_branch(method, endpoint, extra, wire, headers, identifiers, expected):
    # 显式 None 测试共用参数模型与发送层的省略行为。
    response = synthetic_entity_response()
    untouched = deepcopy(response)
    signed = AsyncMock(return_value=response)
    kwargs = {"body": {**wire, **expected, "next_token": "cursor", "offset": 0, "length": 1}}
    if headers:
        kwargs["headers"] = headers
    result = asyncio.run(getattr(AdsAPI, method)(
        SimpleNamespace(_request_with_sign=signed), **extra, **identifiers,
        next_token=" cursor ", offset=0, length=1,
    ))
    signed.assert_awaited_once_with("POST", endpoint, **kwargs)
    assert isinstance(result, getattr(schema, method)) and result.data == []
    assert result.response_count == result.total_count == 0
    assert response == untouched


@pytest.mark.parametrize("method,endpoint,extra,wire,headers", ENTITY_SDK_CASES)
@pytest.mark.parametrize("identifiers", [
    {"sid": None, "profile_id": None}, {"sid": -1, "profile_id": 2},
    {"sid": 1, "profile_id": -1}, {"sid": "", "profile_id": 2}, {"sid": 1, "profile_id": []},
])
def test_ad_entities_sdk_rejects_invalid_identifiers_before_request(method, endpoint, extra, wire, headers, identifiers):
    signed = AsyncMock()
    with pytest.raises(errors.InvalidParametersError) as caught:
        asyncio.run(getattr(AdsAPI, method)(SimpleNamespace(_request_with_sign=signed), **extra, **identifiers))
    assert isinstance(caught.value.__cause__, ValidationError)
    signed.assert_not_awaited()


def test_profile_only_cost_allocation_sdk_request_remains_compatible():
    signed = AsyncMock(return_value=synthetic_entity_response())
    result = asyncio.run(AdsAPI.SbCostAllocationReports(
        SimpleNamespace(_request_with_sign=signed), report_date="2026-10-15", profile_id=2,
    ))
    signed.assert_awaited_once_with("POST", route.SB_COST_ALLOCATION_REPORTS,
                                  body={"profile_id": 2, "report_date": "2026-10-15", "show_detail": 0}, headers={"X-API-VERSION": "2"})
    assert isinstance(result, schema.SbCostAllocationReports)


@pytest.mark.parametrize("identifiers", [{"sid": 1}, {"profile_id": 2}])
def test_portfolios_public_signature_accepts_one_identifier(identifiers):
    signed = AsyncMock(return_value=synthetic_entity_response())
    result = asyncio.run(AdsAPI.Portfolios(SimpleNamespace(_request_with_sign=signed), **identifiers))
    signed.assert_awaited_once_with("POST", route.PORTFOLIOS, body=identifiers, headers={"X-API-VERSION": "2"})
    assert isinstance(result, schema.Portfolios)


@pytest.mark.parametrize("args, kwargs, expected", [
    ((1, 2), {}, {"sid": 1, "profile_id": 2}),
    ((1,), {"profile_id": 2}, {"sid": 1, "profile_id": 2}),
    ((None, 2), {}, {"profile_id": 2}),
    ((0,), {}, {"sid": 0}),
    ((), {"profile_id": "2", "state": " enabled ", "offset": 0, "length": 2},
     {"profile_id": 2, "state": "enabled", "offset": 0, "length": 2}),
    ((), {"sid": 1, "next_token": " token ", "offset": 10, "length": 2},
     {"sid": 1, "next_token": "token", "offset": 10, "length": 2}),
])
def test_portfolios_positional_compatibility_and_exact_request(args, kwargs, expected):
    signed = AsyncMock(return_value=synthetic_entity_response())
    result = asyncio.run(AdsAPI.Portfolios(SimpleNamespace(_request_with_sign=signed), *args, **kwargs))
    signed.assert_awaited_once_with("POST", route.PORTFOLIOS, body=expected, headers={"X-API-VERSION": "2"})
    assert isinstance(result, schema.Portfolios)


@pytest.mark.parametrize("identifiers", [{}, {"sid": None}, {"profile_id": None},
    {"sid": None, "profile_id": None}, {"sid": -1}, {"profile_id": -1},
    {"sid": 1, "profile_id": "bad"}, {"sid": [], "profile_id": 2}])
def test_portfolios_missing_or_invalid_identifiers_never_request(identifiers):
    signed = AsyncMock()
    with pytest.raises(errors.InvalidParametersError) as caught:
        asyncio.run(AdsAPI.Portfolios(SimpleNamespace(_request_with_sign=signed), **identifiers))
    assert isinstance(caught.value.__cause__, ValidationError)
    signed.assert_not_awaited()


def test_ad_entities_instance_validation_is_idempotent():
    model = param.AdEntities(sid=1)
    assert param.AdEntities.model_validate(model) is model
    assert param.AdEntities.model_validate_params(model) == {"sid": 1}


@pytest.mark.parametrize("country_key", ["country", "country_code"])
@pytest.mark.parametrize("date_key", ["data_start_time", "start_date"])
@pytest.mark.parametrize("value, expected", [
    ("2026-10-04", "2026-10-04"),
    ("2026-10-05", "2026-10-04"),
    ("2026-10-10", "2026-10-04"),
    ("2026-09-14", "2026-09-13"),
    ("2026-09-15", "2026-09-13"),
    ("2026-09-16", "2026-09-13"),
    ("2026-09-17", "2026-09-13"),
    ("2026-09-18", "2026-09-13"),
    ("2026-09-19", "2026-09-13"),
    ("2026-09-20", "2026-09-20"),
    ("2026-10-01", "2026-09-27"),
    ("2026-01-01", "2025-12-28"),
    ("2024-03-01", "2024-02-25"),
    (datetime.date(2026, 9, 18), "2026-09-13"),
    (datetime.datetime(2026, 9, 18, 12, 30), "2026-09-13"),
    ("2026-09-18 12:30:00", "2026-09-13"),
    (Pydt(2026, 9, 18, 12, 30), "2026-09-13"),
    (datetime.datetime(2026, 9, 20, 0, 30, tzinfo=datetime.timezone(datetime.timedelta(hours=14))), "2026-09-20"),
    (datetime.datetime(2026, 9, 19, 23, 30, tzinfo=datetime.timezone(datetime.timedelta(hours=-10))), "2026-09-13"),
    ("2026-09", "2026-08-30"),
    ("2026-09-31", "2026-09-27"),
    (1, "1969-12-28"),
    ("2001-01-07", "2001-01-07"),
    ("2099-01-04", "2099-01-04"),
])
def test_aba_parameters_use_sunday_start_week_preserving_aliases_parser_and_no_local_window(country_key, date_key, value, expected):
    raw = {country_key: " US ", date_key: value}
    before = deepcopy(raw)
    wire = param.DownloadAbaReport.model_validate_params(raw)
    assert wire == {"country": "US", "data_start_time": expected}
    assert param.DownloadAbaReport.model_validate_params(wire) == wire
    assert raw == before


@pytest.mark.parametrize("kwargs", [
    {"country": "U", "start_date": "2026-10-04"},
    {"country": "USA", "start_date": "2026-10-04"},
    {"country": "US", "start_date": None},
    {"country": "US", "start_date": "not-a-date"},
    {"country": "US", "start_date": ""},
    {"country": "US", "start_date": []},
    {"country": "US", "start_date": {}},
])
def test_aba_invalid_parameters_fail_before_request(kwargs):
    signed = AsyncMock()
    with pytest.raises(errors.InvalidParametersError) as caught:
        asyncio.run(AdsAPI.DownloadAbaReport(SimpleNamespace(_request_with_sign=signed), **kwargs))
    assert isinstance(caught.value.__cause__, ValidationError)
    signed.assert_not_awaited()


def synthetic_aba_response(start_date="2026-10-04"):
    """独立合成的传输样例；不是采集fixture，也不含真实签名链接。"""
    return {
        "code": 0,
        "message": "操作成功",
        "data": {"country": "US", "data_start_time": start_date, "report_period": "WEEK", "url": "https://example.com/aba/report"},
        "request_id": "synthetic-aba-only",
        "response_time": "2001-01-07 00:00:00",
    }


@pytest.mark.parametrize("start_date", ["2026-10-04", "2026-09-27"])
def test_aba_response_aliases_required_strings_and_download_information_counts(start_date):
    raw = synthetic_aba_response(start_date)
    before = deepcopy(raw)
    parsed = schema.DownloadAbaReport.model_validate(raw)
    assert parsed.data.model_dump() == {
        "country_code": "US", "start_date": start_date, "report_period": "WEEK", "url": raw["data"]["url"],
    }
    assert parsed.errors == [] and parsed.response_count == parsed.total_count == 1
    assert raw == before


@pytest.mark.parametrize("key", ["country", "data_start_time", "report_period", "url"])
@pytest.mark.parametrize("null", [False, True])
def test_aba_success_information_remains_required(key, null):
    raw = synthetic_aba_response()
    if null:
        raw["data"][key] = None
    else:
        del raw["data"][key]
    with pytest.raises(ValidationError):
        schema.DownloadAbaReport.model_validate(raw)


def test_aba_preserves_existing_text_types_and_common_response_semantics():
    raw = synthetic_aba_response()
    raw.update(error_details=["synthetic-detail"], total=9)
    raw["data"].update(report_period="OTHER", data_start_time="date-text", url="opaque-download-location")
    parsed = schema.DownloadAbaReport.model_validate(raw)
    assert parsed.data.report_period == "OTHER" and parsed.data.start_date == "date-text"
    assert parsed.data.url == "opaque-download-location"
    assert parsed.errors == ["synthetic-detail"] and parsed.response_count == 1 and parsed.total_count == 9
    with pytest.raises(ValidationError):
        schema.DownloadAbaReport.model_validate({**raw, "data": None})


@pytest.mark.parametrize("missing_file", [False, True])
@pytest.mark.parametrize("input_date, expected", [
    ("2026-09-18", "2026-09-13"),
    ("2026-09-20", "2026-09-20"),
    ("2026-10-01", "2026-09-27"),
    ("2026-01-01", "2025-12-28"),
])
def test_aba_http_serializes_sunday_start_and_routes_success_or_business_failure(monkeypatch, missing_file, input_date, expected):
    raw = synthetic_aba_response(expected)
    if missing_file:
        raw.update(code=500, message="文件不存在", data=None)

        def unexpected_schema(*args, **kwargs):
            pytest.fail("业务错误不得进入成功Schema")

        monkeypatch.setattr(schema.DownloadAbaReport, "model_validate", unexpected_schema)
    calls = []

    @asynccontextmanager
    async def request(session, verb, target, **options):
        calls.append((verb, target, options["json"], session._prepare_headers(options.get("headers"))))
        yield SimpleNamespace(status=200, reason="synthetic", read=AsyncMock(return_value=json.dumps(raw).encode()))

    monkeypatch.setattr(ClientSession, "request", request)

    async def run():
        async with API("0" * 16, "synthetic-only-secret") as client:
            client._state.access_token = "synthetic-only-token"
            return await client.ads.DownloadAbaReport(country=" US ", start_date=input_date)

    if missing_file:
        with pytest.raises(errors.InternalServerError):
            asyncio.run(run())
    else:
        parsed = asyncio.run(run())
        assert parsed.data.start_date == expected and parsed.data.url == raw["data"]["url"]
    assert len(calls) == 1
    verb, target, body, headers = calls[0]
    assert (verb, target, body) == ("POST", route.DOWNLOAD_ABA_REPORT, {"country": "US", "data_start_time": expected})
    assert "X-API-VERSION" not in headers


def test_aba_documentation_and_field_examples_describe_download_information():
    shown = validate_documentation(AdsAPI.DownloadAbaReport, schema.DownloadAbaReport)
    call, _ = documentation_example(AdsAPI.DownloadAbaReport)
    kwargs = {item.arg: ast.literal_eval(item.value) for item in call.keywords}
    request = param.DownloadAbaReport.model_validate_params(kwargs)
    assert request == {"country": shown["data"]["country_code"], "data_start_time": shown["data"]["start_date"]}
    doc = inspect.getdoc(AdsAPI.DownloadAbaReport)
    assert all(label in doc for label in ("Args:", "Returns:", "Raises:", "Examples:"))
    assert "到当前为止所有" not in doc and "X-API-VERSION" not in doc
    assert "sign=" not in doc and "fmt: off" not in doc and "fmt: on" not in doc
    assert shown["data"] == validate_field_examples(schema.AbaReportUrl)
    assert schema.DownloadAbaReport.model_fields["data"].examples == [shown["data"]]
    fields = param.DownloadAbaReport.model_fields
    values = {name: field.examples[0] for name, field in fields.items() if field.description and field.examples}
    assert values.keys() == fields.keys()
    assert param.DownloadAbaReport.model_validate_params(values) == request
    hints = get_type_hints(param.DownloadAbaReport._validate_start_date)
    assert hints == {"v": str | datetime.date | datetime.datetime, "return": str}
    validator_doc = inspect.getdoc(param.DownloadAbaReport._validate_start_date)
    assert validator_doc and all(label in validator_doc for label in ("Args:", "Returns:", "Raises:"))
