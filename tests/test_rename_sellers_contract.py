"""用户确认的 RenameSellers 专用契约；所有失败明细为离线合成值。"""
from copy import deepcopy
import json

import pytest
from pydantic import BaseModel
from lingxingapi.basic.schema import Marketplaces, RenameSellersResult
from response_contract import (
    ContractError, validate_response, validate_rename_sellers_response, validate_rename_sellers_fixture,
)


def response(failure=0):
    return {"code": 0, "message": "success", "error_details": [], "request_id": "synthetic-id",
            "response_time": "2000-01-01 00:00:00", "total": 0,
            "data": {"success_num": 1, "failure_num": failure,
                     "failure_detail": [] if not failure else [{"sid": 123, "name": "synthetic-name", "error": "synthetic failure"}]}}


@pytest.mark.parametrize("total", [0, 3, None, "synthetic-ignored-metadata"])
def test_explicit_contract_ignores_only_wire_total_without_mutation(total):
    raw = response()
    raw["total"] = total
    before = deepcopy(raw)
    parsed = validate_rename_sellers_response(raw)
    assert parsed.data.success == 1 and parsed.data.failure == 0 and parsed.data.failure_detail == []
    assert not hasattr(parsed, "total") and raw == before


def test_public_default_remains_strict_even_for_rename_model():
    with pytest.raises(ContractError) as caught:
        validate_response(response(), RenameSellersResult)
    assert any("响应多字段" in issue for issue in caught.value.issues)
    assert any("failure_detail" in issue and "覆盖不足" in issue for issue in caught.value.issues)


@pytest.mark.parametrize("location", ["root", "data", "nested_total"])
def test_other_unknown_fields_are_never_ignored(location):
    raw = response()
    if location == "root":
        raw["synthetic_extra"] = 1
    else:
        raw["data"]["total" if location == "nested_total" else "synthetic_extra"] = 1
    with pytest.raises(ContractError, match="响应多字段"):
        validate_rename_sellers_response(raw)


@pytest.mark.parametrize("failure", [1, "1", -1])
def test_nonzero_model_failure_cannot_allow_empty_details(failure):
    raw = response()
    raw["data"]["failure_num"] = failure
    with pytest.raises(ContractError, match="failure_detail.*覆盖不足"):
        validate_rename_sellers_response(raw)


@pytest.mark.parametrize("detail", [None, {}, "", [None], [{"sid": 1}]])
def test_null_and_invalid_detail_shapes_do_not_gain_exception(detail):
    raw = response()
    raw["data"]["failure_detail"] = detail
    with pytest.raises(ContractError):
        validate_rename_sellers_response(raw)


@pytest.mark.parametrize("field", ["failure_num", "success_num"])
def test_numbers_still_use_full_sdk_model_validation(field):
    raw = response()
    raw["data"][field] = "not-a-number"
    with pytest.raises(ContractError, match="Schema类型/约束"):
        validate_rename_sellers_response(raw)


def test_existing_sdk_numeric_conversion_is_preserved():
    raw = response()
    raw["data"].update(success_num="1", failure_num="0")
    assert validate_rename_sellers_response(raw).data.failure == 0
    assert raw["data"]["failure_num"] == "0"


@pytest.mark.parametrize("target", ["failure_num", "success_num", "failure_detail"])
def test_missing_fields_are_still_rejected(target):
    raw = response()
    del raw["data"][target]
    with pytest.raises(ContractError, match="缺失"):
        validate_rename_sellers_response(raw)


@pytest.mark.parametrize("data", [None, [], {}])
def test_missing_or_null_model_structure_does_not_gain_exception(data):
    raw = response()
    raw["data"] = data
    with pytest.raises(ContractError):
        validate_rename_sellers_response(raw)


@pytest.mark.parametrize("code", [1, False, "0"])
def test_unsuccessful_envelope_never_passes(code):
    raw = response()
    raw["code"] = code
    with pytest.raises(ContractError, match="不是成功业务响应"):
        validate_rename_sellers_response(raw)


def test_synthetic_failure_proves_model_branch_without_claiming_real_coverage():
    raw = response(1)
    raw["data"]["success_num"] = 0
    parsed = validate_rename_sellers_response(raw)
    assert parsed.data.failure_detail[0].message == "synthetic failure"
    raw["data"]["failure_detail"][0]["synthetic_extra"] = True
    with pytest.raises(ContractError, match="响应多字段"):
        validate_rename_sellers_response(raw)


def test_existing_other_model_empty_list_behavior_is_unchanged():
    class Other(BaseModel):
        failure_num: int
        failure_detail: list[int]
    class Envelope(BaseModel):
        code: int
        data: Other
    with pytest.raises(ContractError, match="覆盖不足"):
        validate_response({"code": 0, "data": {"failure_num": 0, "failure_detail": []}}, Envelope)
    with pytest.raises(ContractError):
        validate_response(response(), Marketplaces)


def test_output_direction_still_checks_fields_and_empty_failure_rule():
    dumped = RenameSellersResult.model_validate(response()).model_dump(mode="json", by_alias=True)
    assert validate_rename_sellers_response(dumped, direction="output").data.failure == 0
    dumped["total"] = 0
    with pytest.raises(ContractError, match="响应多字段"):
        validate_rename_sellers_response(dumped, direction="output")


def test_fixture_path_uses_same_explicit_contract_and_preserves_bytes(tmp_path):
    # 临时包装仅证明 fixture 检查入口，不是正式样本或实际真实来源证明。
    path = tmp_path / "unit-only.json"
    payload = json.dumps({"source": "local_raw", "endpoint": "basic.RenameSellers", "response": response()}).encode()
    path.write_bytes(payload)
    assert validate_rename_sellers_fixture(path).data.failure == 0
    assert path.read_bytes() == payload


@pytest.mark.parametrize("source,endpoint", [("mock", "basic.RenameSellers"), ("synthetic", "basic.RenameSellers"), ("local_raw", "basic.Marketplaces")])
def test_fixture_identity_rejects_mock_source_and_other_endpoint(tmp_path, source, endpoint):
    path = tmp_path / "unit-only.json"
    path.write_text(json.dumps({"source": source, "endpoint": endpoint, "response": response()}))
    with pytest.raises(ContractError):
        validate_rename_sellers_fixture(path)


@pytest.mark.parametrize("damage", ["extra", "nonzero_empty", "null"])
def test_fixture_uses_same_rejection_boundaries(tmp_path, damage):
    raw = response()
    if damage == "extra":
        raw["extra"] = 0
    elif damage == "nonzero_empty":
        raw["data"]["failure_num"] = 1
    else:
        raw["data"]["failure_detail"] = None
    path = tmp_path / "unit-only.json"
    path.write_text(json.dumps({"source": "local_raw", "endpoint": "basic.RenameSellers", "response": raw}))
    with pytest.raises(ContractError):
        validate_rename_sellers_fixture(path)


def test_fixture_missing_or_symlink_is_not_read(tmp_path):
    path = tmp_path / "unit-only.json"
    with pytest.raises(ContractError):
        validate_rename_sellers_fixture(path)
    original = tmp_path / "other.json"
    original.write_text("{}")
    path.symlink_to(original)
    with pytest.raises(ContractError):
        validate_rename_sellers_fixture(path)
