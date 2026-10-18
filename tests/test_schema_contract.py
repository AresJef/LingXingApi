"""完整Schema负责转换/约束，独立结构检查仍防止字段被忽略或补造。"""

import copy
from typing import Annotated

import pytest
from pydantic import BaseModel, ConfigDict, Field, create_model, field_serializer, field_validator, model_validator
from lingxingapi.base.schema import ResponseV1
from lingxingapi.fields import FloatOrNone2Zero, IntOrNone2Zero
from response_contract import ContractError, validate_response


@pytest.mark.parametrize("annotation,value,expected", [
    (int, "7", 7), (int, "7.0", 7), (float, "7.25", 7.25), (float, 7, 7.0),
    (IntOrNone2Zero, "7", 7), (IntOrNone2Zero, None, 0), (IntOrNone2Zero, "", 0),
    (FloatOrNone2Zero, "7.25", 7.25), (FloatOrNone2Zero, None, 0.0), (FloatOrNone2Zero, "", 0.0),
])
def test_declared_numeric_conversion_is_accepted_without_changing_wire(annotation, value, expected):
    model = create_model("Reply", code=(int, ...), value=(annotation, ...))
    raw = {"code": 0, "value": value}
    before = copy.deepcopy(raw)
    parsed = validate_response(raw, model)
    assert type(parsed.value) is type(expected) and parsed.value == expected
    assert raw == before


@pytest.mark.parametrize("annotation,value", [
    (int, "7.25"), (int, 7.25), (float, "bad"), (IntOrNone2Zero, "bad"),
    (FloatOrNone2Zero, "bad"), (float, None), (int, ""),
])
def test_unparseable_or_unsupported_numeric_input_still_fails(annotation, value):
    model = create_model("Reply", code=(int, ...), value=(annotation, ...))
    with pytest.raises(ContractError, match=r"\$\.value:.*Schema"):
        validate_response({"code": 0, "value": value}, model)


@pytest.mark.parametrize("annotation,value,config", [
    (Annotated[int, Field(gt=0)], "-1", {}),
    (Annotated[float, Field(allow_inf_nan=False)], "NaN", {}),
    (Annotated[float, Field(strict=True)], "7.25", {}),
    (int, "7", {"strict": True}), (FloatOrNone2Zero, "7.25", {"strict": True}),
])
def test_field_constraints_and_model_strict_are_not_overridden(annotation, value, config):
    model = create_model("Reply", __config__=ConfigDict(**config), code=(int, ...), value=(annotation, ...))
    with pytest.raises(ContractError, match="Schema"):
        validate_response({"code": 0, "value": value}, model)


def test_custom_before_zero_rule_still_applies_under_actual_model_strict():
    model = create_model("Reply", __config__=ConfigDict(strict=True), code=(int, ...), value=(IntOrNone2Zero, ...))
    assert validate_response({"code": 0, "value": None}, model).value == 0


class Amount(BaseModel):
    value: float = Field(gt=0, validation_alias="wire", serialization_alias="output")


class NestedReply(BaseModel):
    code: int
    rows: list[Amount]
    mapping: dict[int, Amount]


def nested_raw():
    return {"code": 0, "rows": [{"wire": "7.25"}], "mapping": {"7": {"wire": "2.5"}}}


def test_nested_input_output_aliases_and_dictionary_key_conversion():
    raw = nested_raw()
    before = copy.deepcopy(raw)
    parsed = validate_response(raw, NestedReply)
    assert parsed.rows[0].value == 7.25 and parsed.mapping[7].value == 2.5
    output = parsed.model_dump(mode="json", by_alias=True)
    assert validate_response(output, NestedReply, direction="output").rows[0].value == 7.25
    assert raw == before


@pytest.mark.parametrize("mutation", ["missing", "extra", "alias", "constraint"])
def test_nested_structure_alias_and_constraints_are_still_checked(mutation):
    raw = nested_raw()
    value = raw["rows"][0]
    if mutation == "missing":
        value.clear()
    elif mutation == "extra":
        value["unrelated"] = "private-record"
    elif mutation == "alias":
        value["output"] = value.pop("wire")
    else:
        value["wire"] = "-1"
    with pytest.raises(ContractError) as exc:
        validate_response(raw, NestedReply)
    assert "private-record" not in str(exc.value)


def test_selected_union_model_cannot_hide_fields_behind_another_branch():
    class Defaults(BaseModel):
        x: int = 0
    class Required(BaseModel):
        y: int
    model = create_model("Reply", code=(int, ...), child=(Defaults | Required, Field(union_mode="left_to_right")))
    raw = {"code": 0, "child": {"y": "1"}}
    assert type(model.model_validate(raw).child) is Defaults
    with pytest.raises(ContractError, match="响应多字段"):
        validate_response(raw, model)


def test_nullable_nested_output_alias_uses_correct_model_branch():
    model = create_model("Reply", code=(int, ...), child=(Amount | None, ...))
    assert validate_response({"code": 0, "child": {"output": "7.25"}}, model, direction="output").child.value == 7.25
    with pytest.raises(ContractError, match="覆盖不足"):
        validate_response({"code": 0, "child": None}, model)


def test_full_model_before_validator_runs_on_a_copy_and_default_does_not_hide_missing_field():
    class Reply(BaseModel):
        code: int
        value: int = 0
        @model_validator(mode="before")
        @classmethod
        def normalized(cls, raw):
            raw["value"] = int(raw["value"]) + 1
            return raw
    raw = {"code": 0, "value": "7"}
    assert validate_response(raw, Reply).value == 8
    assert raw == {"code": 0, "value": "7"}
    with pytest.raises(ContractError, match="缺失"):
        validate_response({"code": 0}, Reply)


def test_schema_validation_diagnostics_hide_values_context_and_dictionary_keys():
    private = "PRIVATE_SCHEMA_NUMERIC_SENTINEL"
    raw = nested_raw()
    raw["rows"][0]["wire"] = private
    raw["mapping"] = {private: {"wire": private}}
    with pytest.raises(ContractError) as exc:
        validate_response(raw, NestedReply)
    assert "$.rows[0].wire" in str(exc.value) and "Schema" in str(exc.value)
    assert private not in str(exc.value) and "input_value" not in str(exc.value)


@pytest.mark.parametrize("annotation,value", [(list[int] | str, []), (dict[str, int] | str, {})])
def test_selected_union_container_cannot_bypass_empty_coverage(annotation, value):
    model = create_model("Reply", code=(int, ...), data=(annotation, ...))
    with pytest.raises(ContractError, match="覆盖不足"):
        validate_response({"code": 0, "data": value}, model)


def sdk_raw(**changes):
    return {"code": 0, "message": "success", "error_details": [], "request_id": "",
            "response_time": "", "response_count": 1, "total": 1, "data": [1], **changes}


def test_sdk_quantity_reference_uses_full_field_and_model_input_validators():
    class Reply(ResponseV1):
        data: list[int]
        @model_validator(mode="before")
        @classmethod
        def count_input(cls, raw):
            if raw["response_count"] == "PRIVATE_RESPONSE_SENTINEL":
                raw["response_count"] = 1
            return raw
        @field_validator("total_count", mode="before")
        @classmethod
        def total_input(cls, value):
            return 2 if value == "PRIVATE_COUNT_SENTINEL" else value
    raw = sdk_raw(response_count="PRIVATE_RESPONSE_SENTINEL", total="PRIVATE_COUNT_SENTINEL")
    before = copy.deepcopy(raw)
    parsed = validate_response(raw, Reply)
    assert parsed.response_count == 1 and parsed.total_count == 2 and raw == before


def test_sdk_quantity_reference_errors_are_private_safe():
    calls = []
    class Reply(ResponseV1):
        data: list[int]
        @field_validator("total_count", mode="before")
        @classmethod
        def total_input(cls, value):
            calls.append(value)
            if len(calls) > 1:
                raise ValueError("PRIVATE_COUNT_ERROR_SENTINEL")
            return value
    with pytest.raises(ContractError) as exc:
        validate_response(sdk_raw(), Reply)
    assert "Schema" in str(exc.value) and "PRIVATE_COUNT_ERROR_SENTINEL" not in str(exc.value)


@pytest.mark.parametrize("field_name", ["response_count", "total_count"])
@pytest.mark.parametrize("serialized_type", [int, str])
def test_serialized_sdk_counts_cannot_change_value_or_type(field_name, serialized_type):
    class Reply(ResponseV1):
        data: list[int]
        @field_serializer(field_name)
        def bad_count(self, value):
            return value + 7 if serialized_type is int else str(value)
    with pytest.raises(ContractError, match="序列化数量"):
        validate_response(sdk_raw(), Reply)
