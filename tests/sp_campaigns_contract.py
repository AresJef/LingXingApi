"""SpCampaigns 显式豁免未建模 tags；其余字段和已约定空状态保持严格契约。"""
from __future__ import annotations

from copy import deepcopy

from lingxingapi.ads.schema import SpCampaigns
from pydantic import ValidationError
from response_contract import ContractError, contract_issues, parsed_value_issues, validate_response

CONTRACT_NOTICE = (
    "SpCampaigns 明确契约：SDK不建模data[*].tags，仅在本接口核验视图豁免该字段；"
    "原始raw/pass保留tags，其余未知字段、缺字段和类型仍严格检查。"
)


def validate_sp_campaigns_response(raw, *, scenario: str | None = None) -> SpCampaigns:
    # 仅修改本接口的深拷贝核验视图；原始快照和通用checker不变。
    raw = deepcopy(raw)
    if type(raw) is dict and type(raw.get("data")) is list:
        for row in raw["data"]:
            if type(row) is dict:
                row.pop("tags", None)
    if scenario != "empty_expected":
        return validate_response(raw, SpCampaigns)
    if not (type(raw) is dict and type(raw.get("code")) is int and raw["code"] == 0
            and type(raw.get("data")) is list and raw["data"] == []):
        raise ContractError("difference", ["SpCampaigns 显式空结果场景不符"])
    try:
        parsed = SpCampaigns.model_validate(deepcopy(raw))
        dumped = parsed.model_dump(mode="json", by_alias=True, warnings="error")
    except ValidationError:
        raise ContractError("difference", ["SpCampaigns 空结果不满足原 SDK Schema 类型/约束；未显示输入"]) from None
    except Exception as exc:
        raise ContractError("difference", [f"SpCampaigns 空结果解析或序列化失败：{type(exc).__name__}；未显示输入"]) from None
    issues = contract_issues(raw, SpCampaigns) + parsed_value_issues(raw, parsed)
    issues += contract_issues(dumped, SpCampaigns, direction="output")
    issues += parsed_value_issues(dumped, parsed, direction="output")
    issues = [issue for issue in issues if issue != "$.data: 覆盖不足，空列表无法观察元素结构"]
    if issues:
        raise ContractError("coverage" if all("覆盖不足" in issue for issue in issues) else "difference", sorted(set(issues)))
    if parsed.response_count != 0 or parsed.data != [] or parsed.errors:
        raise ContractError("difference", ["SpCampaigns 空结果的派生数量/错误明细不符"])
    return parsed
