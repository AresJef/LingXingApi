"""Marketplace wire/SDK 派生结果与合成诊断；正式入口默认检查固定 raw。"""

import json
import copy
from pathlib import Path

import pytest
from pydantic import AliasChoices, BaseModel, Field, model_validator
from lingxingapi.basic.schema import Marketplace, Marketplaces
from lingxingapi.base.schema import ResponseV1
from response_contract import (
    ContractError, contract_issues, parsed_value_issues, select_fixture_path, validate_fixture, validate_response,
)


@pytest.fixture
def response():
    # 合成完整样本；不得当作领星真实字段完整性的证据。
    return {
        "code": 0,
        "message": "success",
        "error_details": ["synthetic-error-detail"],
        "request_id": "11111111-2222-4333-8444-555555555555",
        "response_time": "2026-01-02 03:04:05",
        "response_count": 1,
        "total": 1,
        "data": [
            {
                "mid": 1,
                "region": "NA",
                "aws_region": "NA",
                "country": "美国",
                "code": "US",
                "marketplace_id": "OFFLINE-MARKET",
            }
        ],
    }


@pytest.mark.parametrize("nested", [False, True])
def test_recursive_extra_fields_fail_even_when_pydantic_ignores_them(response, nested):
    target = response["data"][0] if nested else response
    target["unexpected"] = "synthetic"
    assert any("响应多字段" in issue for issue in contract_issues(response, Marketplaces))


@pytest.mark.parametrize("field", ["message", "error_details", "request_id", "response_time", "total"])
def test_optional_and_default_model_fields_missing_from_wire_fail(response, field):
    del response[field]
    assert any(field in issue and "缺失" in issue for issue in contract_issues(response, Marketplaces))


def test_alias_wire_name_is_required(response):
    item = response["data"][0]
    item["country_code"] = item.pop("code")
    issues = contract_issues(response, Marketplaces)
    assert any("country_code" in issue and "响应多字段" in issue for issue in issues)
    assert any(".code:" in issue and "缺失" in issue for issue in issues)


@pytest.mark.parametrize("value", ["1", True, 1.0])
def test_schema_allowed_integer_conversion_preserves_raw(response, value):
    response["data"][0]["mid"] = value
    before = copy.deepcopy(response)
    assert validate_response(response).data[0].mid == 1
    assert response == before


def test_schema_rejects_invalid_integer_with_safe_field_path(response):
    response["data"][0]["mid"] = None
    with pytest.raises(ContractError, match=r"\.mid:.*Schema"):
        validate_response(response)


def test_empty_nested_list_reports_insufficient_coverage(response):
    response["data"] = []
    assert any("覆盖不足" in issue for issue in contract_issues(response, Marketplaces))


def test_success_empty_error_details_is_legal_and_values_stay_equal(response):
    response["error_details"] = []
    del response["response_count"]
    assert contract_issues(response, Marketplaces) == []
    parsed = validate_response(response)
    assert parsed.errors == [] and parsed.response_count == len(response["data"])
    assert parsed_value_issues(response, parsed) == []
    assert parsed.total_count == response["total"]


def test_derived_quantity_missing_only_allowed_for_sdk_input(response):
    del response["response_count"]
    parsed = validate_response(response)
    output = parsed.model_dump(mode="json", by_alias=True)
    del output["response_count"]
    assert any("response_count" in issue and "缺失" in issue for issue in contract_issues(output, Marketplaces, direction="output"))
    class Unrelated(BaseModel):
        code: int
        response_count: int = 0
    assert any("response_count" in issue and "缺失" in issue for issue in contract_issues({"code": 0}, Unrelated))


@pytest.mark.parametrize("wrong_count", [0, True])
def test_missing_wire_count_still_checks_model_derived_value(response, wrong_count):
    del response["response_count"]
    class WrongCount(Marketplaces):
        @model_validator(mode="after")
        def wrong_quantity(self):
            self.response_count = wrong_count
            return self
    with pytest.raises(ContractError, match="response_count"):
        validate_response(response, WrongCount)


@pytest.mark.parametrize("value", ["", {}, False, 0])
def test_empty_error_rule_does_not_hide_schema_type_errors(response, value):
    response["error_details"] = value
    with pytest.raises(ContractError, match="error_details"):
        validate_response(response)


def test_existing_optional_errors_validator_accepts_none(response):
    response["error_details"] = None
    assert validate_response(response).errors == []
    assert response["error_details"] is None


def test_empty_error_rule_is_not_global_or_for_business_failures(response):
    class Other(BaseModel):
        code: int
        errors: list = Field(validation_alias="error_details")
    assert any("覆盖不足" in issue for issue in contract_issues({"code": 0, "error_details": []}, Other))
    response["error_details"] = []
    response["code"] = 1
    assert any("error_details" in issue and "覆盖不足" in issue for issue in contract_issues(response, Marketplaces))
    with pytest.raises(ContractError, match="成功业务响应"):
        validate_response(response)


def test_nonempty_untyped_error_objects_still_lack_schema_coverage(response):
    response["error_details"] = [{"synthetic": "value"}]
    with pytest.raises(ContractError, match="模型未声明列表元素结构"):
        validate_response(response)


@pytest.mark.parametrize("total", [-1, 0, 3, 7])
def test_approved_total_normalization_checks_expected_value_and_preserves_wire(response, total):
    del response["response_count"]
    response["data"] *= 3
    response["total"] = total
    before = copy.deepcopy(response)
    parsed = validate_response(response)
    assert parsed.total_count == max(total, 3) and parsed.response_count == 3
    assert response == before and parsed_value_issues(response, parsed) == []


@pytest.mark.parametrize("data,count,total,expected_total", [
    ([1, 2], 2, 0, 2), ([], 0, -1, -1), ({"synthetic": 1}, 1, 0, 1), ({}, 1, 3, 3),
    (None, 7, 0, 0), ("synthetic", 7, 0, 0), (0, 7, 0, 0), (False, 7, 0, 0),
])
def test_sdk_count_algorithm_all_existing_branches(data, count, total, expected_total):
    # 非列表/字典时SDK直接返回，已有response_count不触发total归一化。
    wire = {"code": 0, "message": "success", "error_details": [], "request_id": "synthetic-id",
            "response_time": "synthetic-time", "total": total, "data": data}
    if not isinstance(data, (dict, list)):
        wire["response_count"] = count
    before = copy.deepcopy(wire)
    parsed = validate_response(wire, ResponseV1)
    assert type(parsed.response_count) is int and parsed.response_count == count
    assert type(parsed.total_count) is int and parsed.total_count == expected_total
    assert wire == before


def test_sdk_basemodel_data_branch_and_total_aliases_are_checked():
    class Payload(BaseModel):
        item: int
    class Reply(ResponseV1):
        data: Payload
        total_count: int = Field(0, validation_alias="wire_total", serialization_alias="output_total")
    wire = {"code": 0, "message": "success", "error_details": [], "request_id": "synthetic-id",
            "response_time": "synthetic-time", "wire_total": 0, "data": {"item": 7}}
    before = copy.deepcopy(wire)
    parsed = validate_response(wire, Reply)
    assert isinstance(parsed.data, Payload) and parsed.response_count == parsed.total_count == 1
    output = parsed.model_dump(mode="json", by_alias=True)
    assert output["output_total"] == 1 and validate_response(output, Reply, direction="output").total_count == 1
    assert wire == before


@pytest.mark.parametrize("wrong_total", [0, 2, 999, True, "PRIVATE_COUNT_OUTPUT_SENTINEL"])
def test_total_normalization_does_not_skip_wrong_computation(response, wrong_total, recwarn):
    response["total"] = 0
    response["data"] *= 3
    del response["response_count"]
    class WrongTotal(Marketplaces):
        @model_validator(mode="after")
        def wrong_total_value(self):
            self.total_count = wrong_total
            return self
    with pytest.raises(ContractError, match="total"):
        validate_response(response, WrongTotal)
    assert not any("PRIVATE_COUNT_OUTPUT_SENTINEL" in str(warning.message) for warning in recwarn)


@pytest.mark.parametrize("total", ["0", False, 0.0])
def test_total_normalization_uses_schema_allowed_conversion(response, total):
    response["total"] = total
    assert validate_response(response).total_count == 1
    assert response["total"] is total


def test_total_normalization_does_not_accept_none_for_plain_integer(response):
    response["total"] = None
    with pytest.raises(ContractError, match="total.*类型"):
        validate_response(response)


def test_declared_model_validators_define_allowed_value_changes(response):
    class Other(BaseModel):
        code: int
        total_count: int = Field(validation_alias="total")
        @model_validator(mode="after")
        def changed(self):
            self.total_count += 1
            return self
    assert validate_response({"code": 0, "total": 0}, Other).total_count == 1
    class ChangedCountry(Marketplaces):
        @model_validator(mode="after")
        def changed(self):
            self.data[0].country = "changed-synthetic-country"
            return self
    before = copy.deepcopy(response)
    assert validate_response(response, ChangedCountry).data[0].country == "changed-synthetic-country"
    assert response == before


def test_null_nested_model_reports_insufficient_coverage():
    assert any("覆盖不足" in issue for issue in contract_issues(None, Marketplace | None))


def test_real_schema_maps_exact_synthetic_values(response):
    assert contract_issues(response, Marketplaces) == []
    parsed = Marketplaces.model_validate(response)
    assert parsed_value_issues(response, parsed) == []
    assert parsed.response_count == len(response["data"]) == 1
    assert parsed.total_count == response["total"]
    assert parsed.data[0].region_aws == "NA"
    assert parsed.data[0].country_code == "US"
    assert parsed.data[0].country == "美国"
    assert type(parsed.data[0].mid) is int


@pytest.mark.parametrize("wire", ["wire", "alternate"])
def test_legal_input_alias_choices_and_serialization_alias(wire):
    from response_contract import validate_response
    class Reply(BaseModel):
        code: int
        value: int = Field(validation_alias=AliasChoices("wire", "alternate"), serialization_alias="output")
    data = {"code": 0, wire: 7}
    parsed = validate_response(data, Reply)
    assert parsed.model_dump(by_alias=True) == {"code": 0, "output": 7}
    assert validate_response({"code": 0, "output": 7}, Reply, direction="output").value == 7
    assert data == {"code": 0, wire: 7}


def test_alias_conflicting_inputs_are_rejected_before_parsing():
    from response_contract import validate_response
    class Reply(BaseModel):
        code: int
        value: int = Field(validation_alias=AliasChoices("wire", "alternate"), serialization_alias="output")
    with pytest.raises(AssertionError, match="重复或冲突"):
        validate_response({"code": 0, "wire": 7, "alternate": 7}, Reply)
    with pytest.raises(AssertionError):
        validate_response({"code": 0, "output": 7}, Reply)
    with pytest.raises(AssertionError):
        validate_response({"code": 0, "wire": 7}, Reply, direction="output")


def test_private_values_and_unknown_keys_are_not_in_contract_errors(response):
    from response_contract import validate_response
    response["sensitive-key-sentinel"] = "sensitive-value-sentinel"
    response["data"][0]["mid"] = "sensitive-value-sentinel"
    with pytest.raises(AssertionError) as error:
        validate_response(response)
    assert "sensitive" not in str(error.value)
    assert "input_value" not in str(error.value) and "repr" not in str(error.value)


def test_model_quantity_normalization_is_reported(response):
    response["response_count"] = 99
    assert contract_issues(response, Marketplaces) == []
    assert any("response_count" in issue for issue in parsed_value_issues(response, Marketplaces.model_validate(response)))


def test_default_fixture_path_is_direct_dataset():
    expected = Path(__file__).resolve().parent / "fixtures" / "basic" / "marketplaces.json"
    assert select_fixture_path() == expected


def test_explicit_dataset_selection_is_read_only(monkeypatch, tmp_path, response):
    import response_contract

    default = tmp_path / "default.json"
    default.write_bytes(b"existing dataset remains unchanged\n")
    dataset = tmp_path / "dataset.json"
    dataset.write_text(json.dumps({"source": "mock", "endpoint": "basic.Marketplaces", "response": response}), encoding="utf-8")
    original_dataset = dataset.read_bytes()
    monkeypatch.setattr(response_contract, "DEFAULT_FIXTURE", default)
    assert select_fixture_path() == default
    assert select_fixture_path(str(dataset)) == dataset
    with pytest.raises(AssertionError, match="mock"):
        validate_fixture(select_fixture_path(str(dataset)))
    assert default.read_bytes() == b"existing dataset remains unchanged\n"
    assert dataset.read_bytes() == original_dataset


def test_explicit_missing_dataset_is_not_a_silent_pass(tmp_path):
    with pytest.raises(FileNotFoundError):
        validate_fixture(select_fixture_path(tmp_path / "missing.json"))


def test_local_raw_dataset_checks_schema_read_only(tmp_path, response):
    # 合成文件只验证数据集检查逻辑，不声称来自真实 API。
    path = tmp_path / "dataset.json"
    path.write_text(json.dumps({"source": "local_raw", "endpoint": "basic.Marketplaces", "response": response}), encoding="utf-8")
    before = path.read_bytes()
    parsed = validate_fixture(path)
    assert parsed.response_count == 1
    assert path.read_bytes() == before


@pytest.mark.parametrize("code", [1, False, "401"])
def test_dataset_cannot_accept_an_error_response(tmp_path, response, code):
    response["code"] = code
    path = tmp_path / "dataset.json"
    path.write_text(json.dumps({"source": "local_raw", "endpoint": "basic.Marketplaces", "response": response}))
    with pytest.raises(AssertionError, match="成功业务响应"):
        validate_fixture(path)


@pytest.mark.parametrize("content", [b'\xff', b'{', b'{"source":"live","source":"local_raw"}', b'{"number":NaN}'])
def test_dataset_parse_errors_are_not_silently_accepted(tmp_path, content):
    path = tmp_path / "dataset.json"
    path.write_bytes(content)
    with pytest.raises(AssertionError):
        validate_fixture(path)
