"""静态文档的公开输出契约；不读取或比较可覆盖的采集fixture。"""
from __future__ import annotations

import ast
from copy import deepcopy
import inspect
import json
import textwrap
import types
from typing import Any, Union, get_args, get_origin

from pydantic import BaseModel, TypeAdapter
from lingxingapi.ads.schema import SbCreativeConfig, SbCreativeLandingPage
from sb_entities_contract import CREATIVE_DEFAULT_FIELDS


def documentation_example(method) -> tuple[ast.Call, dict]:
    """只解析示例语法和实际方法签名，不执行代码或请求。"""
    parts = inspect.getdoc(method).split(".. code-block:: python")
    assert len(parts) == 3, "文档必须有调用、输出两个代码块"
    source = textwrap.dedent(parts[1]).strip()
    compile(source, "<documentation>", "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
    statements = ast.parse(source).body
    statement = statements[0]
    assert isinstance(statement, ast.Assign) and isinstance(statement.value, ast.Await)
    call = statement.value.value
    assert isinstance(call, ast.Call)
    module = method.__module__.split(".")[-2]
    assert ast.unparse(call.func) == f"client.{module}.{method.__name__}"
    assert all(item.arg is not None for item in call.keywords)
    inspect.signature(method).bind(None, *call.args, **{item.arg: item.value for item in call.keywords})
    assert ast.dump(statements[-1]) == ast.dump(ast.parse("print(result.model_dump())").body[0])
    shown = ast.literal_eval(textwrap.dedent(parts[2]).strip())
    assert type(shown) is dict
    return call, shown


def _wire(value: Any, annotation: Any, path: str) -> Any:
    """严格检查公开字段/输出类型后转回输入别名，仅供离线模型重放。"""
    origin, arguments = get_origin(annotation), get_args(annotation)
    if origin in (Union, types.UnionType):
        for option in arguments:
            try:
                return _wire(value, option, path)
            except (AssertionError, ValueError, TypeError):
                continue
        raise AssertionError(f"{path}: 输出类型不符合 {annotation}")
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        assert type(value) is dict and value.keys() == annotation.model_fields.keys(), f"{path}: 公开字段缺失、多余或使用了输入别名"
        wire = {}
        for name, field in annotation.model_fields.items():
            alias = field.validation_alias or field.alias or name
            assert isinstance(alias, str), f"{path}.{name}: 未支持的输入别名"
            if ((annotation is SbCreativeConfig and name in CREATIVE_DEFAULT_FIELDS.values()
                    or annotation is SbCreativeLandingPage and name == "page_url")
                    and not field.is_required() and field.default is None and value[name] is None):
                continue  # 真实SDK缺键默认None；不能补成显式null后误转为空字符串。
            if field.examples and any(has_information(item) for item in field.examples):
                assert has_information(value[name]), f"{path}.{name}: 已有非空静态示例，文档不能仅展示空值"
            wire[alias] = _wire(value[name], field.annotation, path + "." + name)
        return wire
    if origin is list or annotation is list:
        assert type(value) is list, f"{path}: 必须为列表"
        if any(item is Ellipsis for item in value):
            assert len(value) >= 2 and value[-1] is Ellipsis and sum(item is Ellipsis for item in value) == 1, f"{path}: 省略号仅可跟在具体列表项之后"
        return [_wire(item, arguments[0] if arguments else Any, f"{path}[{index}]")
                for index, item in enumerate(value) if item is not Ellipsis]
    assert value is not Ellipsis, f"{path}: 省略号只能用于列表尾部"
    checked = TypeAdapter(annotation).validate_python(value, strict=True)
    assert type(checked) is type(value), f"{path}: 必须使用模型输出类型"
    return value


def _concrete(value: Any) -> Any:
    if type(value) is dict:
        return {key: _concrete(item) for key, item in value.items()}
    if type(value) is list:
        return [_concrete(item) for item in value if item is not Ellipsis]
    return value


def validate_public_example(shown: dict, model: type[BaseModel]) -> dict:
    """核对完整公开结构、精确输出类型、模型转换及展示计数的一致性。"""
    wire = _wire(shown, model, model.__name__)
    concrete = _concrete(shown)
    if "response_count" in concrete:
        data = shown["data"]
        if type(data) is list:
            count = len(concrete["data"])
            if data and data[-1] is Ellipsis:
                assert shown["response_count"] > count
            else:
                assert shown["response_count"] == count
        else:
            count = 1 if isinstance(data, dict) else 0
            assert shown["response_count"] == count
        assert shown["total_count"] >= shown["response_count"]
        # 只为缩略展示的根data调整派生计数；不能忽略其他字段或嵌套值。
        concrete["response_count"] = count
    actual = model.model_validate(deepcopy(wire)).model_dump()
    assert json.dumps(actual, sort_keys=True) == json.dumps(concrete, sort_keys=True), "示例不是模型可输出的值或类型"
    return _concrete(shown)


def validate_field_examples(model: type[BaseModel]) -> dict:
    """静态Field.examples组装成公开记录，按完整模型检查其类型和关联转换。"""
    record = {}
    for name, field in model.model_fields.items():
        assert field.description and "\n" not in field.description and "\\n" not in field.description
        assert isinstance(field.examples, list) and len(field.examples) == 1
        record[name] = field.examples[0]
    json.dumps(record)  # Field.examples必须可序列化，不允许文档展示用的省略号。
    validate_public_example(record, model)
    return record


def has_information(value: Any) -> bool:
    """0/False有信息量；None、空字符串和空容器没有。"""
    return value is not None and value != "" and value != [] and value != {}


def validate_documentation(method, model: type[BaseModel]) -> dict:
    """校验静态文档自身；可覆盖fixture不参与文档期望值的构造。"""
    _, shown = documentation_example(method)
    validate_public_example(shown, model)
    assert has_information(shown["data"]) or shown["data"] is None
    return shown
