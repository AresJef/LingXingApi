"""六个 SP 实体严格契约；显式空状态仅核对外层，不豁免任何响应字段。"""
from __future__ import annotations

from copy import deepcopy
import re
from pydantic import ValidationError
from lingxingapi.ads import schema
from response_contract import ContractError, contract_issues, parsed_value_issues, validate_response

MODELS = {"ads." + name: getattr(schema, name) for name in (
    "SpAdGroups", "SpProducts", "SpKeywords", "SpTargets", "SpNegativeKeywords", "SpNegativeTargets")}


def validate_sp_entity_response(raw, model, *, scenario: str | None = None):
    if model not in MODELS.values():
        raise ContractError("input_error", ["未登记的 SP 实体 Schema"])
    if model in (schema.SpNegativeKeywords, schema.SpNegativeTargets):
        raw = deepcopy(raw)
        key, expected = ("negative_type", "negativeKeyword") if model is schema.SpNegativeKeywords else ("negative_match_type", "")
        if type(raw) is dict and type(raw.get("data")) is list:
            for index, row in enumerate(raw["data"]):
                if type(row) is dict:
                    if key not in row or type(row[key]) is not str or row[key] != expected:
                        raise ContractError("difference", [f"$.data[{index}].{key}: 不满足该否定分支已确认的固定值契约"])
                    row.pop(key)
    if scenario != "empty_expected" and model is not schema.SpProducts:
        return validate_response(raw, model)
    if not (type(raw) is dict and type(raw.get("code")) is int and raw["code"] == 0
            and type(raw.get("data")) is list and (scenario != "empty_expected" or raw["data"] == [])):
        raise ContractError("difference", ["SP 实体显式空结果场景不符"])
    try:
        parsed = model.model_validate(deepcopy(raw))
        dumped = parsed.model_dump(mode="json", by_alias=True, warnings="error")
    except ValidationError:
        raise ContractError("difference", ["SP 实体空结果不满足原 Schema 类型/约束；未显示输入"]) from None
    except Exception as exc:
        raise ContractError("difference", [f"SP 实体空结果解析或序列化失败：{type(exc).__name__}"]) from None
    issues = contract_issues(raw, model) + parsed_value_issues(raw, parsed)
    issues += contract_issues(dumped, model, direction="output") + parsed_value_issues(dumped, parsed, direction="output")
    if scenario == "empty_expected":
        issues = [issue for issue in issues if issue != "$.data: 覆盖不足，空列表无法观察元素结构"]
    if model is schema.SpProducts:
        # 空视频数组是合法行；整集合发布另要求固定、真实的非空视频补充证据。
        issues = [issue for issue in issues if not re.fullmatch(r"\$\.data\[\d+\]\.video_details: 覆盖不足，空列表无法观察元素结构", issue)]
    if issues:
        raise ContractError("coverage" if all("覆盖不足" in issue for issue in issues) else "difference", sorted(set(issues)))
    if (scenario == "empty_expected" and (parsed.response_count != 0 or parsed.data != [])) or parsed.errors:
        raise ContractError("difference", ["SP 实体空结果的数量/错误明细不符"])
    return parsed
