"""只读共享契约检查；输入/输出别名按各自语义解释，不读取 Secret。"""

import copy
import json
import types
from pathlib import Path
from typing import Any, Union, get_args, get_origin

from pydantic import AliasChoices, BaseModel, ValidationError
from pydantic_core import SchemaValidator
from lingxingapi.base.schema import BaseResponse, ResponseV1
from lingxingapi.basic.schema import Marketplaces, RenameSellersResult

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RAW = ROOT / "tools/data_raw/basic/marketplace-原始数据.json"
DEFAULT_FIXTURE = ROOT / "tests/fixtures/basic/marketplaces.json"

RENAME_SELLERS_CONTRACT_NOTICE = (
    "RenameSellers 明确契约：仅忽略原始顶层 total；模型验证失败数为 0 时允许空 failure_detail。"
    "真实失败明细已观察到 sid=0、TEST 的店铺记录不存在；不代表其他失败原因已覆盖。"
)


class ContractError(AssertionError):
    def __init__(self, status, issues):
        self.status, self.issues = status, tuple(issues)
        super().__init__("\n".join(self.issues))


def select_fixture_path(dataset=None):
    return DEFAULT_FIXTURE if dataset is None else Path(dataset).expanduser().resolve()


def has_model(annotation):
    return isinstance(annotation, type) and issubclass(annotation, BaseModel) or any(has_model(arg) for arg in get_args(annotation))


def _successful_response(value):
    return type(value) is dict and (type(value.get("code")) is int and value["code"] == 0
                                   or type(value.get("code")) is str and value["code"] == "200")


def input_keys(model, name, field):
    alias = field.validation_alias or field.alias or name
    keys = alias.choices if isinstance(alias, AliasChoices) else [alias]
    if any(type(key) is not str for key in keys):
        raise ContractError("coverage", [f"{model.__name__}.{name}: 覆盖不足，alias 结构未支持"])
    if model.model_config.get("populate_by_name") or model.model_config.get("validate_by_name"):
        keys = [*keys, name]
    return tuple(dict.fromkeys(keys))


def field_keys(model, direction="input"):
    keys = {}
    for name, field in model.model_fields.items():
        aliases = input_keys(model, name, field) if direction == "input" else (field.serialization_alias or field.alias or name,)
        for key in aliases:
            if key in keys and keys[key][0] != name:
                raise ContractError("difference", [f"{model.__name__}: 字段 alias 冲突"])
            keys[key] = (name, field.annotation)
    return keys


def contract_issues(value, annotation, path="$", direction="input"):
    """只核对字段及可观察的嵌套结构；类型、约束与转换由完整Schema验证。"""
    origin, args = get_origin(annotation), get_args(annotation)
    if origin in (Union, types.UnionType):
        if value is None and has_model(annotation):
            return [f"{path}: 覆盖不足，null 无法观察嵌套模型字段"]
        choices = [contract_issues(value, arg, path, direction) for arg in args if value is None or arg is not type(None)]
        return [] if any(not issues for issues in choices) else min(choices, key=len)
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        if type(value) is not dict:
            return [f"{path}: JSON 类型应为 object，实际 {type(value).__name__}"]
        keys = field_keys(annotation, direction)
        trusted_names = set(annotation.model_fields) | set(field_keys(annotation, "input")) | set(field_keys(annotation, "output"))
        issues = [f"{path}.{key if key in trusted_names else '<未知字段' + str(index + 1) + '>'}: 响应多字段"
                  for index, key in enumerate(sorted(value.keys() - keys.keys()))]
        for name in annotation.model_fields:
            present = [key for key, (field_name, _) in keys.items() if field_name == name and key in value]
            expected = next(key for key, (field_name, _) in keys.items() if field_name == name)
            if not present:
                # 已批准：SDK ResponseV1 的派生数量不是 wire 必须字段；输出仍须有它。
                if direction == "input" and name == "response_count" and issubclass(annotation, ResponseV1):
                    continue
                issues.append(f"{path}.{expected}: 模型字段在样本中缺失")
            elif len(present) != 1:
                issues.append(f"{path}.{expected}: 同一语义字段重复或冲突输入")
            else:
                key = present[0]
                # 仅成功 SDK 响应的 errors/error_details 空列表；不放宽其他列表。
                if (name == "errors" and issubclass(annotation, BaseResponse) and _successful_response(value)
                        and type(value[key]) is list and not value[key]):
                    continue
                issues += contract_issues(value[key], keys[key][1], f"{path}.{key}", direction)
        return issues
    if origin is list or annotation is list:
        if type(value) is not list:
            return [f"{path}: JSON 类型应为 array，实际 {type(value).__name__}"]
        if not value:
            return [f"{path}: 覆盖不足，空列表无法观察元素结构"]
        if not args and any(isinstance(item, (dict, list)) for item in value):
            return [f"{path}: 覆盖不足，模型未声明列表元素结构"]
        return [issue for index, item in enumerate(value) for issue in contract_issues(item, args[0], f"{path}[{index}]", direction)] if args else []
    if origin is dict or annotation is dict:
        if type(value) is not dict:
            return [f"{path}: JSON 类型应为 object，实际 {type(value).__name__}"]
        if not value:
            return [f"{path}: 覆盖不足，空对象无法观察元素结构"]
        return [issue for item in value.values() for issue in contract_issues(item, args[1], f"{path}.<元素>", direction)] if args else []
    if annotation is Any:
        return []
    return []


def _count_reference(raw, model, direction):
    """复用实际core schema的输入链；独立数量核对前移除根模型after计算。"""
    def input_schema(schema):
        if schema["type"] == "function-after":
            return input_schema(schema["schema"])
        if schema["type"] in {"function-wrap", "definitions"}:
            return {**schema, "schema": input_schema(schema["schema"])}
        return schema  # model内保留字段validator、metadata、config及模型before。

    try:
        value = raw if direction == "input" else _validation_input(raw, model)
        return SchemaValidator(input_schema(model.__pydantic_core_schema__)).validate_python(copy.deepcopy(value))
    except ValidationError as exc:
        raise ContractError("difference", _schema_error_issues(exc, model)) from None
    except Exception as exc:
        raise ContractError("difference", [f"数量输入Schema验证失败：{type(exc).__name__}；未显示字段值"]) from None


def _sdk_expected_counts(reference):
    """独立核验ResponseV1._set_count，不使用其已计算结果作预期。"""
    count, total, data = reference.response_count, reference.total_count, reference.data
    if isinstance(data, list):
        count = len(data)
    elif isinstance(data, (dict, BaseModel)):
        count = 1
    else:
        return count, total
    return count, max(total, count) if count > 0 else total


def _container_annotation(annotation, container):
    if annotation is container or get_origin(annotation) is container:
        return annotation
    if get_origin(annotation) in (Union, types.UnionType):
        return next((arg for arg in get_args(annotation) if arg is container or get_origin(arg) is container), None)
    return None


def parsed_value_issues(raw, parsed, path="$", direction="input", annotation=None):
    """核对实际选中分支的覆盖及数量；类型和值转换由完整Schema决定。"""
    if isinstance(parsed, BaseModel):
        reference = _count_reference(raw, type(parsed), direction) if isinstance(parsed, ResponseV1) and direction == "input" else None
        counts = _sdk_expected_counts(reference) if reference is not None else None
        issues = contract_issues(raw, type(parsed), path, direction)
        for key, (name, child) in field_keys(type(parsed), direction).items():
            if key not in raw:
                continue
            if isinstance(parsed, ResponseV1) and name in {"response_count", "total_count"}:
                if direction == "output":
                    if type(raw[key]) is not int or raw[key] != getattr(parsed, name):
                        issues.append(f"{path}.{key}: 序列化数量类型或值与已核验结果不一致")
                elif name == "response_count" and reference.response_count != parsed.response_count:
                    issues.append(f"{path}.{key}: 原声明与SDK派生数量不一致")
                elif name == "total_count" and (type(parsed.total_count) is not int or parsed.total_count != counts[1]):
                    issues.append(f"{path}.{key}: SDK总数量类型或预期计算不一致")
            elif (name == "errors" and isinstance(parsed, BaseResponse) and _successful_response(raw)
                  and type(raw[key]) is list and not raw[key]):
                continue  # 已批准的成功响应空错误列表。
            else:
                issues += parsed_value_issues(raw[key], getattr(parsed, name), f"{path}.{key}", direction, child)
        if counts is not None and (type(parsed.response_count) is not int or parsed.response_count != counts[0]):
            issues.append(f"{path}.response_count: SDK派生数量与预期计算不一致")
        return issues
    if isinstance(raw, list) and isinstance(parsed, (list, tuple)):
        selected = _container_annotation(annotation, list)
        issues = contract_issues(raw, selected, path, direction) if selected is not None else []
        if len(raw) != len(parsed):
            return [*issues, f"{path}: 模型解析改变数量"]
        args = get_args(selected)
        return issues + [issue for index, (before, after) in enumerate(zip(raw, parsed))
                         for issue in parsed_value_issues(before, after, f"{path}[{index}]", direction, args[0] if args else None)]
    if isinstance(raw, dict) and isinstance(parsed, dict):
        selected = _container_annotation(annotation, dict)
        issues = contract_issues(raw, selected, path, direction) if selected is not None else []
        if len(raw) != len(parsed):
            return [*issues, f"{path}: 模型解析改变元素数量"]
        args = get_args(selected)
        return issues + [issue for before, after in zip(raw.values(), parsed.values())
                         for issue in parsed_value_issues(before, after, f"{path}.<元素>", direction, args[1] if args else None)]
    return []


def _schema_error_issues(error, model):
    """只显示已声明字段名/索引；不渲染Pydantic的input、msg、ctx或任意字典键。"""
    known, seen, pending = set(), set(), [model]
    while pending:
        annotation = pending.pop()
        if isinstance(annotation, type) and issubclass(annotation, BaseModel) and annotation not in seen:
            seen.add(annotation)
            known.update(annotation.model_fields)
            known.update(field_keys(annotation))
            known.update(field_keys(annotation, "output"))
            pending.extend(field.annotation for field in annotation.model_fields.values())
        else:
            pending.extend(get_args(annotation))
    issues = []
    for detail in error.errors(include_input=False, include_context=False, include_url=False):
        path = "$" + "".join(f"[{part}]" if type(part) is int else "." + (part if type(part) is str and part in known else "<校验位置>") for part in detail["loc"])
        issues.append(path + ": 当前Schema类型/约束验证失败")
    return sorted(set(issues))


def _validation_input(value, annotation):
    """把合法输出名映射到合法输入名，仅供模型验证；不改变实际待写入值。"""
    origin, args = get_origin(annotation), get_args(annotation)
    if origin in (Union, types.UnionType):
        branch = next((arg for arg in args if has_model(arg) and not contract_issues(value, arg, direction="output")), None)
        return _validation_input(value, branch) if branch is not None else value
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        output = field_keys(annotation, "output")
        return {input_keys(annotation, name, annotation.model_fields[name])[0]: _validation_input(value[key], child)
                for key, (name, child) in output.items() if key in value}
    if origin is list and args:
        return [_validation_input(item, args[0]) for item in value]
    if origin is dict and args:
        return {key: _validation_input(item, args[1]) for key, item in value.items()}
    return value


def _validate_response(raw, model, *, direction="input", rename_success_empty=False):
    if not _successful_response(raw):
        raise ContractError("difference", ["$.code: 不是成功业务响应"])
    issues = contract_issues(raw, model, direction=direction)
    try:
        parsed = model.model_validate(copy.deepcopy(raw if direction == "input" else _validation_input(raw, model)))
    except ValidationError as exc:
        raise ContractError("difference", [*sorted(issues), *_schema_error_issues(exc, model)]) from None
    except Exception as exc:
        raise ContractError("difference", [*sorted(issues), f"当前 schema 解析失败：{type(exc).__name__}"]) from None
    def approved_issues(items):
        # 只有固定模型的显式入口启用；计数先经完整 SDK 模型验证，null 明细不获豁免。
        if (rename_success_empty and model is RenameSellersResult and type(raw) is dict
                and type(raw.get("data")) is dict and type(raw["data"].get("failure_detail")) is list
                and not raw["data"]["failure_detail"] and parsed.data.failure == 0):
            allowed = "$.data.failure_detail: 覆盖不足，空列表无法观察元素结构"
            return [item for item in items if item != allowed]
        return items

    issues = approved_issues(issues)
    if issues:
        status = "coverage" if all("覆盖不足" in issue for issue in issues) else "difference"
        raise ContractError(status, ["响应/模型差异：", *sorted(issues)])
    issues = approved_issues(parsed_value_issues(raw, parsed, direction=direction))
    if issues:
        raise ContractError("coverage" if all("覆盖不足" in issue for issue in issues) else "difference", issues)
    # 按输出 alias 检查模型的真实序列化结果，不能拿 wire 与 model_dump 直接比较。
    try:
        serialized = parsed.model_dump(mode="json", by_alias=True, warnings="error")
    except Exception as exc:
        raise ContractError("difference", [f"模型序列化失败：{type(exc).__name__}；未显示字段值"]) from None
    output_issues = approved_issues(contract_issues(serialized, model, direction="output"))
    issues += output_issues + approved_issues(parsed_value_issues(serialized, parsed, direction="output"))
    if issues:
        raise ContractError("coverage" if all("覆盖不足" in issue for issue in issues) else "difference", issues)
    return parsed


def validate_response(raw, model=Marketplaces, *, direction="input"):
    """公共默认入口始终严格；不因模型名称自动启用接口例外。"""
    return _validate_response(raw, model, direction=direction)


def check_rename_sellers_scenario(parsed: RenameSellersResult, scenario: str | None) -> None:
    """区分固定单项成功与 sid=0/TEST 的预期单项失败，不改变字段或类型规则。"""
    if scenario is None:
        return
    data = parsed.data
    if scenario == "success":
        valid = data.success == 1 and data.failure == 0 and not data.failure_detail
    elif scenario == "failure":
        valid = (data.success == 0 and data.failure == 1 and len(data.failure_detail) == 1
                 and data.failure_detail[0].sid == 0 and data.failure_detail[0].name == "TEST")
    else:
        raise ContractError("input_error", ["未知 RenameSellers 场景"])
    if not valid:
        raise ContractError("difference", [f"RenameSellers 场景不符：{scenario}；成功/失败计数或失败目标与固定请求不符"])


def validate_rename_sellers_response(raw, *, direction="input", scenario=None) -> RenameSellersResult:
    """已确认的专用契约；可额外要求固定成功/失败场景。"""
    # total 是此接口获准忽略的原始字段；只构造核验视图，不修改 caller 或保存的数据。
    view = {key: value for key, value in raw.items() if key != "total"} if direction == "input" and type(raw) is dict else raw
    parsed = _validate_response(view, RenameSellersResult, direction=direction, rename_success_empty=True)
    check_rename_sellers_scenario(parsed, scenario)
    return parsed


def load_json_bytes(data):
    def unique_fields(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ContractError("input_error", ["JSON 包含重复字段，不能静默丢弃"])
            result[key] = value
        return result

    def invalid_number(value):
        raise ContractError("input_error", ["JSON 包含非标准数值"])

    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=unique_fields, parse_constant=invalid_number)
        json.dumps(value, allow_nan=False)
        return value
    except ContractError:
        raise
    except (UnicodeError, ValueError):
        raise ContractError("input_error", ["不是有效 UTF-8 JSON 或包含非标准数值"]) from None


def validate_fixture(path: Path) -> Marketplaces:
    fixture = load_json_bytes(path.read_bytes())
    if type(fixture) is not dict or fixture.get("source") not in {"live", "local_raw"}:
        raise ContractError("input_error", ["mock/synthetic 不能作为样本验收输入；local_raw 不证明真实来源"])
    if fixture.get("endpoint") != "basic.Marketplaces":
        raise ContractError("input_error", ["fixture 不是 basic.Marketplaces 响应"])
    return validate_response(fixture.get("response"))



def validate_rename_sellers_fixture(path: Path, *, scenario=None) -> RenameSellersResult:
    """独立 RenameSellers fixture 入口，复用相同专用契约，不写样本。"""
    path = Path(path)
    if path.suffix != ".json" or path.is_symlink() or not path.is_file():
        raise ContractError("input_error", [f"RenameSellers fixture 不存在或不是普通 JSON 文件：{path}"])
    try:
        fixture = load_json_bytes(path.read_bytes())
    except OSError:
        raise ContractError("input_error", ["RenameSellers fixture 无法读取"]) from None
    if type(fixture) is not dict or fixture.get("source") not in {"live", "local_raw"}:
        raise ContractError("input_error", ["mock/synthetic 不能作为样本验收输入；local_raw 不证明真实来源"])
    if fixture.get("endpoint") != "basic.RenameSellers":
        raise ContractError("input_error", ["fixture 不是 basic.RenameSellers 响应"])
    return validate_rename_sellers_response(fixture.get("response"), scenario=scenario)
