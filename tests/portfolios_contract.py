"""Portfolios 显式空结果场景；保留通用 checker 对嵌套字段覆盖的严格要求。"""
from __future__ import annotations

from copy import deepcopy

from pydantic import ValidationError
from lingxingapi.ads.schema import Portfolios
from response_contract import ContractError, contract_issues, parsed_value_issues, validate_response


def validate_portfolios_response(raw, *, scenario: str | None = None) -> Portfolios:
    """非空复用完整契约；已约定空状态/终止页只确认外层及空结果，元素覆盖仍缺失。"""
    if scenario != "empty_expected":
        return validate_response(raw, Portfolios)
    if not (type(raw) is dict and type(raw.get("code")) is int and raw["code"] == 0
            and type(raw.get("data")) is list and raw["data"] == []):
        raise ContractError("difference", ["Portfolios 显式空结果场景不符"])
    try:
        parsed = Portfolios.model_validate(deepcopy(raw))
    except ValidationError:
        raise ContractError("difference", ["Portfolios 空结果不满足原 SDK Schema 类型/约束；未显示输入"]) from None
    except Exception as exc:
        raise ContractError("difference", [f"Portfolios 解析失败：{type(exc).__name__}；未显示输入"]) from None
    issues = contract_issues(raw, Portfolios) + parsed_value_issues(raw, parsed)
    try:
        dumped = parsed.model_dump(mode="json", by_alias=True, warnings="error")
    except Exception as exc:
        raise ContractError("difference", [f"Portfolios 序列化失败：{type(exc).__name__}；未显示输入"]) from None
    issues += contract_issues(dumped, Portfolios, direction="output")
    issues += parsed_value_issues(dumped, parsed, direction="output")
    expected_gap = "$.data: 覆盖不足，空列表无法观察元素结构"
    issues = [issue for issue in issues if issue != expected_gap]
    if issues:
        raise ContractError("coverage" if all("覆盖不足" in issue for issue in issues) else "difference", sorted(set(issues)))
    if parsed.response_count != 0 or parsed.data != [] or parsed.errors:
        raise ContractError("difference", ["Portfolios 空结果的派生数量/错误明细不符"])
    return parsed
