"""获准的汇率接口专用契约；此处响应均为离线合成测试值。"""
from copy import deepcopy
import json

import pytest
from lingxingapi.base.schema import ResponseResult
from response_contract import ContractError, validate_response
from edit_exchange_rate_contract import validate_edit_exchange_rate_response, validate_edit_exchange_rate_fixture


def response(failure=False):
    return {"code": 100 if failure else 0, "message": "未知异常" if failure else "success",
            "error_details": ["操作失败"] if failure else [], "request_id": "synthetic-exchange-id",
            "response_time": "2001-01-01 00:00:00", "data": None, "total": 0}


@pytest.mark.parametrize("failure", [False, True])
def test_only_explicit_contract_accepts_observed_scenarios_without_mutation(failure):
    raw = response(failure); before = deepcopy(raw)
    parsed = validate_edit_exchange_rate_response(raw, scenario="failure" if failure else "success")
    assert raw == before and parsed.code == (100 if failure else 0) and parsed.data is None
    assert parsed.errors == (["操作失败"] if failure else []) and not hasattr(parsed, "total")
    assert parsed.model_dump(mode="json", by_alias=True)["code"] == raw["code"]
    with pytest.raises(ContractError): validate_response(raw, ResponseResult)


@pytest.mark.parametrize("failure", [False, True])
@pytest.mark.parametrize("field", ["code", "message", "error_details", "request_id", "response_time", "data"])
def test_missing_sdk_fields_are_never_filled_silently(failure, field):
    raw = response(failure); del raw[field]
    with pytest.raises(ContractError):
        validate_edit_exchange_rate_response(raw, scenario="failure" if failure else "success")


@pytest.mark.parametrize("value", [None, "0", False, 0.0, -1, 1, {}, []])
@pytest.mark.parametrize("failure", [False, True])
def test_total_allowance_is_only_exact_integer_zero(value, failure):
    raw = response(failure); raw["total"] = value
    with pytest.raises(ContractError):
        validate_edit_exchange_rate_response(raw, scenario="failure" if failure else "success")


@pytest.mark.parametrize("field,value", [
    ("code", 0), ("code", 101), ("code", "100"), ("code", 100.0), ("code", True),
    ("message", "other"), ("message", None), ("error_details", []),
    ("error_details", ["其他错误"]), ("error_details", ["操作失败", "操作失败"]),
    ("error_details", "操作失败"), ("error_details", [{"message": "操作失败"}]),
    ("data", {}), ("data", []), ("data", ""), ("data", 0),
])
def test_failure_is_exact_observed_error_not_any_nonzero_business_code(field, value):
    raw = response(True); raw[field] = value
    with pytest.raises(ContractError): validate_edit_exchange_rate_response(raw, scenario="failure")


def test_failure_total_is_required_and_success_without_extra_total_keeps_existing_contract():
    raw = response(True); del raw["total"]
    with pytest.raises(ContractError): validate_edit_exchange_rate_response(raw, scenario="failure")
    raw = response(); del raw["total"]
    assert validate_edit_exchange_rate_response(raw, scenario="success").code == 0


@pytest.mark.parametrize("failure", [False, True])
@pytest.mark.parametrize("damage", ["unknown", "duplicate_alias", "wrong_id_type", "wrong_time_type"])
def test_other_fields_aliases_and_full_sdk_types_remain_strict(failure, damage):
    raw = response(failure)
    if damage == "unknown": raw["extra"] = 1
    elif damage == "duplicate_alias": raw["errors"] = raw["error_details"]
    elif damage == "wrong_id_type": raw["request_id"] = {"bad": 1}
    else: raw["response_time"] = []
    with pytest.raises(ContractError):
        validate_edit_exchange_rate_response(raw, scenario="failure" if failure else "success")


@pytest.mark.parametrize("scenario,raw", [("success", response(True)), ("failure", response()), (None, response()), ("other", response())])
def test_scenarios_cannot_be_exchanged_or_implicitly_guessed(scenario, raw):
    with pytest.raises(ContractError): validate_edit_exchange_rate_response(raw, scenario=scenario)


@pytest.mark.parametrize("failure", [False, True])
def test_fixture_checks_endpoint_origin_and_preserves_exact_bytes(tmp_path, failure):
    path = tmp_path/"unit-only.json"
    body = json.dumps({"source": "local_raw", "endpoint": "basic.EditExchangeRate", "response": response(failure)}).encode()
    path.write_bytes(body)
    parsed = validate_edit_exchange_rate_fixture(path, scenario="failure" if failure else "success")
    assert path.read_bytes() == body and parsed.code == (100 if failure else 0)
    with pytest.raises(ContractError):
        validate_edit_exchange_rate_fixture(path, scenario="success" if failure else "failure")


@pytest.mark.parametrize("source,endpoint", [("synthetic", "basic.EditExchangeRate"), ("mock", "basic.EditExchangeRate"), ("local_raw", "basic.RenameSellers")])
def test_fixture_rejects_other_sources_or_endpoints(tmp_path, source, endpoint):
    path = tmp_path/"unit-only.json"
    path.write_text(json.dumps({"source": source, "endpoint": endpoint, "response": response()}))
    with pytest.raises(ContractError): validate_edit_exchange_rate_fixture(path, scenario="success")


def test_fixture_missing_or_symlink_is_not_accepted(tmp_path):
    path = tmp_path/"missing.json"
    with pytest.raises(ContractError): validate_edit_exchange_rate_fixture(path, scenario="success")
    target = tmp_path/"target.json"; target.write_text("{}")
    path.symlink_to(target)
    with pytest.raises(ContractError): validate_edit_exchange_rate_fixture(path, scenario="success")
