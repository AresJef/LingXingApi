"""操作日志专用契约的离线合成边界，不读取凭据或真实采集文件。"""
from __future__ import annotations

from copy import deepcopy
import json

import pytest

from lingxingapi.ads import schema
from ads_operation_logs_contract import validate_operation_logs_response
from response_contract import ContractError, validate_response


ROW_KEYS = (
    "profile_id", "campaign_id", "campaign_name", "ad_group_id", "ad_group_name",
    "object_id", "object_name", "sponsored_type", "user_id", "user_name",
    "operate_type", "change_type", "function_name", "operate_time",
    "operate_before", "operate_after",
)
ROOT_KEYS = ("code", "message", "error_details", "request_id", "response_time", "total", "data")


class DerivedOperationLogs(schema.AdsOperationLogs):
    """即便自行声明游标，派生模型也不得使用获准入口。"""

    next_token: str | None = None


def response():
    return {
        "code": 0, "message": "success", "error_details": [],
        "request_id": "synthetic-only-request", "response_time": "2001-05-07 12:35:00",
        "total": 1, "next_token": None,
        "data": [{
            "profile_id": "900000000000000101", "campaign_id": "700000000000000102",
            "campaign_name": "synthetic-only-campaign", "ad_group_id": None,
            "ad_group_name": None, "object_id": "700000000000000102",
            "object_name": "synthetic-only-campaign", "sponsored_type": "sp",
            "user_id": None, "user_name": None, "operate_type": "campaigns",
            "change_type": "update", "function_name": "history",
            "operate_time": "2001-05-07 12:34:56",
            "operate_before": [
                {"code": "IN_BUDGET", "value": "false"},
                {"code": "BUDGET_AMOUNT", "value": " 12.3400 "},
            ],
            "operate_after": [
                {"code": "IN_BUDGET", "value": "true"},
                {"code": "BUDGET_AMOUNT", "value": "1.230000000000000000e+2"},
            ],
        }],
    }


def empty_response():
    return {**response(), "total": 0, "data": []}


def test_null_token_view_accepts_all_sixteen_fields_and_preserves_raw():
    raw = response()
    before = deepcopy(raw)
    serialized_before = json.dumps(raw, ensure_ascii=False)

    parsed = validate_operation_logs_response(raw)

    assert tuple(raw["data"][0]) == ROW_KEYS
    assert type(parsed) is schema.AdsOperationLogs
    assert parsed.response_count == parsed.total_count == 1
    assert parsed.data[0].model_dump(mode="json", by_alias=True) == {
        "profile_id": 900000000000000101, "campaign_id": 700000000000000102,
        "campaign_name": "synthetic-only-campaign", "ad_group_id": 0,
        "ad_group_name": "", "ad_object_id": 700000000000000102,
        "ad_object_name": "synthetic-only-campaign", "ad_type": "sp",
        "operator_id": 0, "operator_name": "", "operation_target": "campaigns",
        "operation_type": "update", "operation_source": "history",
        "operation_time": "2001-05-07 12:34:56",
        "before": deepcopy(raw["data"][0]["operate_before"]),
        "after": deepcopy(raw["data"][0]["operate_after"]),
    }
    assert "next_token" not in parsed.model_dump()
    assert raw == before and raw["next_token"] is None
    assert json.dumps(raw, ensure_ascii=False) == serialized_before


def test_public_validator_keeps_rejecting_the_approved_null_token():
    with pytest.raises(ContractError) as caught:
        validate_response(response(), schema.AdsOperationLogs)
    assert caught.value.status == "difference"
    assert any("响应多字段" in issue for issue in caught.value.issues)


def test_response_without_the_optional_unmodeled_token_uses_the_same_contract():
    raw = response()
    del raw["next_token"]
    before = deepcopy(raw)
    parsed = validate_operation_logs_response(raw)
    assert parsed.model_dump() == validate_response(raw, schema.AdsOperationLogs).model_dump()
    assert raw == before


@pytest.mark.parametrize("token", ["", 0, False, [], {}, 1, True, "synthetic-cursor", [None], {"cursor": None}])
@pytest.mark.parametrize("scenario", [None, "empty_expected"])
def test_only_exact_top_level_null_token_is_approved(token, scenario):
    raw = empty_response() if scenario else response()
    raw["next_token"] = token
    before = deepcopy(raw)
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response(raw, scenario=scenario)
    assert caught.value.status == "difference"
    assert raw == before and type(raw["next_token"]) is type(token)


@pytest.mark.parametrize("model", [schema.SdCampaigns, schema.AdsOperationLog, DerivedOperationLogs, None])
@pytest.mark.parametrize("scenario", [None, "empty_expected"])
def test_only_the_exact_registered_response_model_can_use_the_entrypoint(model, scenario):
    raw = empty_response() if scenario else response()
    before = deepcopy(raw)
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response(raw, model, scenario=scenario)
    assert caught.value.status == "input_error"
    assert raw == before


@pytest.mark.parametrize("location", ["root", "row", "before", "after", "row_token", "before_token", "after_token"])
def test_unknown_keys_are_rejected_at_every_model_level(location):
    raw = response()
    row = raw["data"][0]
    container = {
        "root": raw, "row": row, "before": row["operate_before"][0],
        "after": row["operate_after"][0], "row_token": row,
        "before_token": row["operate_before"][0], "after_token": row["operate_after"][0],
    }[location]
    container["next_token" if location.endswith("token") else "future_field"] = None
    before = deepcopy(raw)
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response(raw)
    assert caught.value.status == "difference"
    assert any("响应多字段" in issue for issue in caught.value.issues)
    assert raw == before


@pytest.mark.parametrize("key", ROOT_KEYS)
def test_missing_root_fields_are_not_filled_by_sdk_defaults(key):
    raw = response()
    del raw[key]
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response(raw)
    assert caught.value.status == "difference"


@pytest.mark.parametrize("key", ROW_KEYS)
def test_every_wire_row_field_remains_required(key):
    raw = response()
    del raw["data"][0][key]
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response(raw)
    assert caught.value.status == "difference"


@pytest.mark.parametrize("side", ["operate_before", "operate_after"])
@pytest.mark.parametrize("key", ["code", "value"])
def test_both_nested_operation_fields_remain_required(side, key):
    raw = response()
    del raw["data"][0][side][0][key]
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response(raw)
    assert caught.value.status == "difference"


@pytest.mark.parametrize("key,value", [
    ("code", False), ("message", {}), ("error_details", "synthetic-error"),
    ("request_id", []), ("response_time", {}), ("total", "not-an-integer"), ("data", {}),
])
def test_wrong_root_types_still_fail_schema_and_raw_checks(key, value):
    raw = response()
    raw[key] = value
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response(raw)
    assert caught.value.status == "difference"


@pytest.mark.parametrize("key", ROW_KEYS)
def test_wrong_types_are_rejected_for_every_row_field(key):
    raw = response()
    raw["data"][0][key] = {}
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response(raw)
    assert caught.value.status == "difference"


@pytest.mark.parametrize("side", ["operate_before", "operate_after"])
@pytest.mark.parametrize("key", ["code", "value"])
def test_wrong_nested_operation_types_are_rejected(side, key):
    raw = response()
    raw["data"][0][side][0][key] = ["synthetic-only"]
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response(raw)
    assert caught.value.status == "difference"


@pytest.mark.parametrize("value", [None, ""])
def test_nullable_integer_fields_follow_existing_sdk_zero_conversion(value):
    raw = response()
    for key in ("ad_group_id", "object_id", "user_id"):
        raw["data"][0][key] = value
    before = deepcopy(raw)
    row = validate_operation_logs_response(raw).data[0]
    assert (row.ad_group_id, row.ad_object_id, row.operator_id) == (0, 0, 0)
    assert all(type(number) is int for number in (row.ad_group_id, row.ad_object_id, row.operator_id))
    assert raw == before


def test_nullable_text_and_nested_values_follow_existing_sdk_blank_conversion():
    raw = response()
    for key in ("ad_group_name", "object_name", "user_name", "operate_type", "change_type", "function_name"):
        raw["data"][0][key] = None
    for side in ("operate_before", "operate_after"):
        raw["data"][0][side][0]["value"] = None
    before = deepcopy(raw)
    row = validate_operation_logs_response(raw).data[0]
    assert (row.ad_group_name, row.ad_object_name, row.operator_name,
            row.operation_target, row.operation_type, row.operation_source) == ("", "", "", "", "", "")
    assert row.before[0].value == row.after[0].value == ""
    assert raw == before


@pytest.mark.parametrize("value", ["", "0", "false", "true", "null", " 12.3400 ", "-0.00", "1e-9",
                                       "12345678901234567890.123456789000"])
def test_business_values_remain_exact_strings_without_json_or_number_parsing(value):
    raw = response()
    for side in ("operate_before", "operate_after"):
        raw["data"][0][side][1]["value"] = value
    before = deepcopy(raw)
    row = validate_operation_logs_response(raw).data[0]
    assert type(row.before[1].value) is type(row.after[1].value) is str
    assert row.before[1].value == row.after[1].value == value
    assert row.model_dump(mode="json")["before"][1]["value"] == value
    assert raw == before


@pytest.mark.parametrize("code", [False, True, "0", 1, 500, None])
@pytest.mark.parametrize("scenario", [None, "empty_expected"])
def test_business_failure_is_never_accepted_as_a_successful_response(code, scenario):
    raw = empty_response() if scenario else response()
    raw["code"] = code
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response(raw, scenario=scenario)
    assert caught.value.status == "difference"


@pytest.mark.parametrize("scenario", [None, "empty_expected"])
def test_nonempty_error_details_are_an_endpoint_hard_failure(scenario):
    raw = empty_response() if scenario else response()
    raw["error_details"] = ["synthetic-only-error"]
    before = deepcopy(raw)
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response(raw, scenario=scenario)
    assert caught.value.status == "difference"
    assert raw == before


def test_endpoint_error_policy_does_not_change_the_public_validator():
    raw = response()
    del raw["next_token"]
    raw["error_details"] = ["synthetic-only-error"]
    assert validate_response(raw, schema.AdsOperationLogs).errors == ["synthetic-only-error"]


@pytest.mark.parametrize("declared", [0, 2, "2"])
@pytest.mark.parametrize("scenario", [None, "empty_expected"])
def test_declared_response_count_must_match_the_sdk_derived_count(declared, scenario):
    raw = empty_response() if scenario else response()
    raw["response_count"] = 1 if scenario and declared == 0 else declared
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response(raw, scenario=scenario)
    assert caught.value.status == "difference"


@pytest.mark.parametrize("with_token", [True, False])
@pytest.mark.parametrize("total", [0, 37])
def test_explicit_empty_scenario_approves_only_root_element_coverage(with_token, total):
    raw = {**empty_response(), "total": total}
    if not with_token:
        del raw["next_token"]
    before = deepcopy(raw)
    parsed = validate_operation_logs_response(raw, scenario="empty_expected")
    assert parsed.response_count == 0 and parsed.data == [] and parsed.errors == []
    assert parsed.total_count == total
    assert raw == before


@pytest.mark.parametrize("scenario", [None, "empty", "unexpected"])
def test_empty_data_without_the_exact_scenario_remains_a_coverage_failure(scenario):
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response(empty_response(), scenario=scenario)
    assert caught.value.status == "coverage"
    assert any(issue == "$.data: 覆盖不足，空列表无法观察元素结构" for issue in caught.value.issues)


@pytest.mark.parametrize("patch", [{"data": None}, {"data": {}}, {"data": ()}, {"code": "200"}])
def test_explicit_empty_scenario_requires_integer_zero_and_an_actual_empty_list(patch):
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response({**empty_response(), **patch}, scenario="empty_expected")
    assert caught.value.status == "difference"


def test_explicit_empty_scenario_does_not_accept_a_nonempty_response():
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response(response(), scenario="empty_expected")
    assert caught.value.status == "difference"


@pytest.mark.parametrize("key", ROOT_KEYS)
def test_explicit_empty_scenario_still_requires_every_root_field(key):
    raw = empty_response()
    del raw[key]
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response(raw, scenario="empty_expected")
    assert caught.value.status == "difference"


def test_explicit_empty_scenario_still_rejects_unknown_root_keys():
    raw = {**empty_response(), "future_field": None}
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response(raw, scenario="empty_expected")
    assert caught.value.status == "difference"


@pytest.mark.parametrize("side", ["operate_before", "operate_after"])
@pytest.mark.parametrize("scenario", [None, "empty_expected"])
def test_nested_empty_operation_lists_never_inherit_the_root_coverage_exemption(side, scenario):
    raw = response()
    raw["data"][0][side] = []
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response(raw, scenario=scenario)
    if scenario is None:
        assert caught.value.status == "coverage"
        assert any(f"$.data[0].{side}: 覆盖不足" in issue for issue in caught.value.issues)
    else:
        assert caught.value.status == "difference"


@pytest.mark.parametrize("scenario", [None, "empty_expected"])
@pytest.mark.parametrize("defect", ["extra", "missing", "count"])
def test_real_serialized_output_keeps_field_and_quantity_checks(monkeypatch, scenario, defect):
    original_dump = schema.AdsOperationLogs.model_dump

    def damaged_dump(self, *args, **kwargs):
        dumped = original_dump(self, *args, **kwargs)
        if defect == "extra":
            dumped["future_field"] = None
        elif defect == "missing":
            del dumped["request_id"]
        else:
            dumped["response_count"] = 99
        return dumped

    monkeypatch.setattr(schema.AdsOperationLogs, "model_dump", damaged_dump)
    raw = empty_response() if scenario else response()
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response(raw, scenario=scenario)
    assert caught.value.status == "difference"


@pytest.mark.parametrize("scenario", [None, "empty_expected"])
def test_unexpected_parsed_count_cannot_bypass_independent_value_checks(monkeypatch, scenario):
    original_validate = schema.AdsOperationLogs.model_validate

    def damaged_validate(cls, value, *args, **kwargs):
        parsed = original_validate(value, *args, **kwargs)
        parsed.response_count = 99
        return parsed

    monkeypatch.setattr(schema.AdsOperationLogs, "model_validate", classmethod(damaged_validate))
    raw = empty_response() if scenario else response()
    with pytest.raises(ContractError) as caught:
        validate_operation_logs_response(raw, scenario=scenario)
    assert caught.value.status == "difference"
