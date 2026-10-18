"""仅 EditExchangeRate 的获准契约；不改变 SDK 或通用业务成功门禁。"""
from copy import deepcopy
from pathlib import Path

from pydantic import ValidationError
from lingxingapi.base.schema import ResponseResult
from response_contract import (
    ContractError, contract_issues, load_json_bytes, parsed_value_issues, validate_response,
)

CONTRACT_NOTICE = (
    "EditExchangeRate 专用契约：仅允许整数 total=0；失败须精确匹配已观察的 code100 错误结构。"
    "失败样本核验成功表示预期失败已验证，SDK业务层仍应抛错。"
)


def validate_edit_exchange_rate_response(raw, *, scenario: str) -> ResponseResult:
    """成功复用通用核验；固定失败保留 code100，直接核对完整原有 Schema。"""
    if scenario not in {"success", "failure"}:
        raise ContractError("input_error", ["EditExchangeRate 必须指定 success 或 failure 场景"])
    if type(raw) is not dict:
        raise ContractError("difference", ["EditExchangeRate 响应不是 JSON 对象"])
    if "total" in raw and (type(raw["total"]) is not int or raw["total"] != 0):
        raise ContractError("difference", ["$.total: 仅批准整数0"])
    view = {key: value for key, value in raw.items() if key != "total"}
    if scenario == "success":
        return validate_response(view, ResponseResult)

    expected = {"code": 100, "message": "未知异常", "error_details": ["操作失败"], "data": None, "total": 0}
    if any(key not in raw or type(raw[key]) is not type(value) or raw[key] != value
           for key, value in expected.items()):
        raise ContractError("difference", ["EditExchangeRate 失败场景不符：仅批准code100及已观察到的完整错误结构"])

    # 不把 code100 改成0，也不让通用 checker 接受非零码；模型值和dump均保留真实失败。
    issues = contract_issues(view, ResponseResult)
    try:
        parsed = ResponseResult.model_validate(deepcopy(view))
    except ValidationError:
        raise ContractError("difference", [*issues, "EditExchangeRate失败响应不满足原SDK Schema类型/约束；未显示输入"]) from None
    except Exception as exc:
        raise ContractError("difference", [*issues, f"SDK Schema解析失败：{type(exc).__name__}；未显示输入"]) from None
    issues += parsed_value_issues(view, parsed)
    if parsed.code != 100 or parsed.errors != ["操作失败"] or parsed.data is not None:
        issues.append("SDK Schema改变了已确认失败的业务值")
    try:
        dumped = parsed.model_dump(mode="json", by_alias=True, warnings="error")
    except Exception as exc:
        raise ContractError("difference", [f"SDK模型序列化失败：{type(exc).__name__}；未显示输入"]) from None
    issues += contract_issues(dumped, ResponseResult, direction="output")
    issues += parsed_value_issues(dumped, parsed, direction="output")
    if issues:
        raise ContractError("coverage" if all("覆盖不足" in issue for issue in issues) else "difference", sorted(set(issues)))
    return parsed


def validate_edit_exchange_rate_fixture(path: Path, *, scenario: str) -> ResponseResult:
    path = Path(path)
    if path.suffix != ".json" or path.is_symlink() or not path.is_file():
        raise ContractError("input_error", [f"EditExchangeRate fixture不存在或不是普通JSON文件：{path}"])
    try:
        fixture = load_json_bytes(path.read_bytes())
    except OSError:
        raise ContractError("input_error", ["EditExchangeRate fixture无法读取"]) from None
    if type(fixture) is not dict or fixture.get("source") not in {"local_raw", "live"}:
        raise ContractError("input_error", ["mock/synthetic不能作为样本验收输入；local_raw不证明真实来源"])
    if fixture.get("endpoint") != "basic.EditExchangeRate":
        raise ContractError("input_error", ["fixture不是basic.EditExchangeRate响应"])
    return validate_edit_exchange_rate_response(fixture.get("response"), scenario=scenario)
