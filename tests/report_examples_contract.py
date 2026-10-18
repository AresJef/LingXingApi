"""报告文档与冻结真实指标投影保持一致；不读取可覆盖的 raw/pass/fixture。"""
from copy import deepcopy
import inspect
import json
from pathlib import Path
import re
import types
from typing import Annotated, Union, get_args, get_origin

from pydantic import TypeAdapter
from documentation_contract import documentation_example


NON_METRIC_NUMBERS = {
    "profile_id", "campaign_id", "ad_group_id", "ad_id", "creative_id", "keyword_id",
    "target_id", "targeting_id", "department_id", "hour", "placement_type", "is_asin_target",
}


def canonical(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, allow_nan=False)


def numeric_annotation(annotation):
    origin, arguments = get_origin(annotation), get_args(annotation)
    if origin is Annotated:
        return numeric_annotation(arguments[0])
    if origin in (Union, types.UnionType):
        return any(numeric_annotation(option) for option in arguments)
    return isinstance(annotation, type) and issubclass(annotation, (int, float))


def validate_source(source):
    assert isinstance(source["path"], str) and source["path"].startswith("tools/data_raw/ads/reports/")
    assert re.fullmatch(r"[0-9a-f]{64}", source["sha256"])
    assert type(source["row_index"]) is int and source["row_index"] >= 0
    assert isinstance(source["scope"], str) and source["scope"]


def validate_report_metric_examples(function, model):
    """检查完整单行、每个数值指标、wire 别名和实际 SDK null 转换。"""
    lines = inspect.getdoc(function).splitlines()
    for index, line in enumerate(lines):
        if line.strip() == ".. code-block:: python":
            content = next(item for item in lines[index + 1:] if item.strip())
            indentation = len(line) - len(line.lstrip())
            assert content.startswith(" " * (indentation + 4)), "代码块缩进必须比 directive 多一级"
    frozen = json.loads(Path(__file__).with_name("report_examples_metrics.json").read_bytes())
    assert frozen["format"] == "report-example-metrics-v1" and len(frozen["methods"]) == 38
    evidence = frozen["methods"][function.__name__]
    row_model = get_args(model.model_fields["data"].annotation)[0]
    fields = {name: field for name, field in row_model.model_fields.items()
        if numeric_annotation(field.annotation) and name not in NON_METRIC_NUMBERS}
    wire_fields = {field.validation_alias or field.alias or name: name for name, field in fields.items()}
    assert set(evidence["fields"]) == set(fields)
    _, shown = documentation_example(function)
    actual_rows = {"api": shown["data"][0], "schema_data": model.model_fields["data"].examples[0][0]}
    quality = evidence["representative_quality"]
    validate_source(quality["source"])
    positive = lambda value: type(value) in (int, float) and value > 0
    assert set(quality["public_metrics"]) == set(fields)
    assert quality["maximum_positive_metrics"] == sum(map(positive, quality["public_metrics"].values()))
    for kind, actual in actual_rows.items():
        assert sum(positive(actual[name]) for name in fields) == quality["maximum_positive_metrics"], "已有信息更丰富的真实完整行，不能退回零值指标示例"
        entry = evidence[kind]
        validate_source(entry["source"])
        assert canonical(actual) == canonical(entry["public_row"]), "完整文档记录与冻结真实行不一致"
        assert set(entry["wire_metrics"]) == set(wire_fields)
        assert set(entry["public_metrics"]) == set(fields)
        assert canonical(entry["public_metrics"]) == canonical({name: actual[name] for name in fields})
        wire = {field.validation_alias or field.alias or name: deepcopy(actual[name])
            for name, field in row_model.model_fields.items()}
        wire.update(entry["wire_metrics"])
        assert canonical(row_model.model_validate(wire).model_dump()) == canonical(actual), "完整指标组合不能由该真实行经 SDK 输出"
    for name, field in fields.items():
        entry = evidence["fields"][name]
        if entry["positive_available_in_owner"]:
            assert positive(field.examples[0]), "该字段已有非零真实证据，不能只展示零值"
        validate_source(entry["source"])
        owner = next(cls for cls in row_model.__mro__ if name in cls.__dict__.get("__annotations__", {}))
        assert entry["owner"]["class"] == owner.__name__
        assert set(entry["owner"]["own_fields"]) == set(owner.__annotations__)
        assert entry["wire_name"] == (field.validation_alias or field.alias or name)
        assert canonical(field.examples) == canonical([entry["example"]])
        assert canonical(entry["example"]) == canonical(entry["public_value"])
        parsed = TypeAdapter(field.rebuild_annotation()).validate_python(entry["wire_value"])
        assert canonical(parsed) == canonical(entry["public_value"]), "单字段示例与真实原值的 SDK 转换不同"
