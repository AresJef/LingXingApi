"""广告操作日志专用契约；仅检查视图可忽略顶层精确 null 游标。"""
from __future__ import annotations

from copy import deepcopy

from pydantic import ValidationError
from lingxingapi.ads import schema
from response_contract import ContractError, contract_issues, parsed_value_issues, validate_response


def validate_operation_logs_response(
    raw, model=schema.AdsOperationLogs, *, scenario: str | None = None
) -> schema.AdsOperationLogs:
    """保留原文和 SDK 语义，成功响应的非空错误明细作为本接口硬失败。"""
    if model is not schema.AdsOperationLogs:
        raise ContractError("input_error", ["操作日志专用契约仅允许 AdsOperationLogs Schema"])
    if type(raw) is dict and "next_token" in raw:
        if raw["next_token"] is not None:
            raise ContractError("difference", ["$.next_token: 仅批准顶层精确 null 核验视图"])
        raw = deepcopy(raw)
        del raw["next_token"]  # 仅核验视图；caller、raw/pass 和 fixture 原键保留。
    if scenario != "empty_expected":
        parsed = validate_response(raw, model)
        if parsed.errors:
            raise ContractError("difference", ["操作日志成功响应含非空错误明细"])
        return parsed
    if not (type(raw) is dict and type(raw.get("code")) is int and raw["code"] == 0
            and type(raw.get("data")) is list and raw["data"] == []):
        raise ContractError("difference", ["操作日志显式空结果场景不符"])
    try:
        parsed = model.model_validate(deepcopy(raw))
    except ValidationError:
        raise ContractError("difference", ["操作日志空结果不满足 Schema 类型或约束；未显示输入"]) from None
    except Exception as exc:
        raise ContractError("difference", [f"操作日志解析失败：{type(exc).__name__}；未显示输入"]) from None
    issues = contract_issues(raw, model) + parsed_value_issues(raw, parsed)
    try:
        dumped = parsed.model_dump(mode="json", by_alias=True, warnings="error")
    except Exception as exc:
        raise ContractError("difference", [f"操作日志序列化失败：{type(exc).__name__}；未显示输入"]) from None
    issues += contract_issues(dumped, model, direction="output")
    issues += parsed_value_issues(dumped, parsed, direction="output")
    root_gap = "$.data: 覆盖不足，空列表无法观察元素结构"
    issues = [issue for issue in issues if issue != root_gap]
    if issues:
        raise ContractError("difference", sorted(set(issues)))
    if parsed.response_count != 0 or parsed.data != [] or parsed.errors:
        raise ContractError("difference", ["操作日志空结果数量或错误明细不符"])
    return parsed
