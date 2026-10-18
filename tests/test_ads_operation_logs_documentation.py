"""操作日志静态文档的公开字段、调用和字符串业务值契约。"""

from __future__ import annotations

import ast
from copy import deepcopy
import doctest
import inspect
import io
import json
import textwrap
import tokenize

import pytest
from pydantic import ValidationError

from lingxingapi.ads import param, schema
from lingxingapi.ads.api import AdsAPI
from documentation_contract import (
    documentation_example,
    validate_documentation,
    validate_field_examples,
)

ROW_FIELDS = {
    "profile_id",
    "campaign_id",
    "campaign_name",
    "ad_group_id",
    "ad_group_name",
    "ad_object_id",
    "ad_object_name",
    "ad_type",
    "operator_id",
    "operator_name",
    "operation_target",
    "operation_type",
    "operation_source",
    "operation_time",
    "before",
    "after",
}
ALIASES = {
    "ad_object_id": "object_id",
    "ad_object_name": "object_name",
    "ad_type": "sponsored_type",
    "operator_id": "user_id",
    "operator_name": "user_name",
    "operation_target": "operate_type",
    "operation_type": "change_type",
    "operation_source": "function_name",
    "operation_time": "operate_time",
    "before": "operate_before",
    "after": "operate_after",
}


def test_method_documentation_has_google_sections_and_all_eight_arguments():
    function = AdsAPI.AdsOperationLogs
    doc = inspect.getdoc(function)
    assert "领星接口文档: 新广告.[操作日志（新）]" in doc
    assert "https://apidoc.lingxing.com/new/api-docs/newAd/apiLogStandard/" in doc
    assert (
        doc.index("## Docs")
        < doc.index("Args:")
        < doc.index("Returns:")
        < doc.index("Examples:")
    )
    assert "ads.schema.AdsOperationLogs:" in doc
    assert all(
        word not in doc for word in ("实测", "样本", "采集", "本次", ":param ", "```")
    )
    names = set(inspect.signature(function).parameters) - {"self"}
    assert len(names) == 8
    assert all(f"{name} (" in doc for name in names)
    assert "一个月" in doc and "30天" not in doc
    assert "X-API-VERSION" not in doc and "从0开始的偏移量" in doc
    assert "不添加" not in doc and "从1开始的页码" not in doc


def test_method_example_is_complete_public_output_and_preserves_log_relationships():
    shown = validate_documentation(AdsAPI.AdsOperationLogs, schema.AdsOperationLogs)
    assert set(shown) == {
        "code",
        "message",
        "errors",
        "request_id",
        "response_time",
        "response_count",
        "total_count",
        "data",
    }
    assert shown["response_count"] == 4 and shown["total_count"] == 217
    assert len(shown["data"]) == 2 and shown["data"][-1] is Ellipsis
    row = shown["data"][0]
    assert set(row) == ROW_FIELDS
    assert row["ad_object_id"] == row["campaign_id"]
    assert row["ad_object_name"] == row["campaign_name"]
    assert row["ad_group_id"] == 0 and row["ad_group_name"] == ""
    assert row["operator_id"] == 0
    assert row["before"] == [{"code": "IN_BUDGET", "value": "true"}]
    assert row["after"] == [{"code": "IN_BUDGET", "value": "false"}]
    call, _ = documentation_example(AdsAPI.AdsOperationLogs)
    values = {item.arg: ast.literal_eval(item.value) for item in call.keywords}
    assert values["start_date"] <= row["operation_time"][:10] <= values["end_date"]
    assert values["ad_type"].lower() == row["ad_type"]
    assert values["operation_target"] == row["operation_target"]
    assert values["length"] == shown["response_count"]
    assert type(values["sid"]) is int


def test_response_example_field_comments_are_on_the_preceding_line():
    doc = inspect.getdoc(AdsAPI.AdsOperationLogs)
    example = textwrap.dedent(doc.split(".. code-block:: python")[2])
    lines = example.splitlines()
    comments = [
        token
        for token in tokenize.generate_tokens(io.StringIO(example).readline)
        if token.type == tokenize.COMMENT
    ]
    assert len(comments) == 28
    for token in comments:
        row, column = token.start
        assert not lines[row - 1][:column].strip()
        assert lines[row][:column] == " " * column
        assert lines[row][column:].startswith('"')
    assert '"errors": []' in example


@pytest.mark.parametrize("model", [schema.AdsOperation, schema.AdsOperationLog])
def test_response_fields_have_single_typed_examples_from_the_complete_example(model):
    record = validate_field_examples(model)
    _, shown = documentation_example(AdsAPI.AdsOperationLogs)
    expected = shown["data"][0]
    if model is schema.AdsOperation:
        expected = expected["before"][0]
    assert record == expected
    for field in model.model_fields.values():
        assert all(
            word not in field.description for word in ("实测", "样本", "采集", "本次")
        )
        assert field.is_required()
    if model is schema.AdsOperationLog:
        assert set(record) == ROW_FIELDS
        assert {
            name: field.validation_alias
            for name, field in model.model_fields.items()
            if field.validation_alias
        } == ALIASES


def test_outer_data_example_matches_the_complete_public_row_without_wire_keys():
    field = schema.AdsOperationLogs.model_fields["data"]
    _, shown = documentation_example(AdsAPI.AdsOperationLogs)
    assert field.description and "\n" not in field.description
    assert field.examples == [[shown["data"][0]]]
    json.dumps(field.examples)
    assert "next_token" not in schema.AdsOperationLogs.model_fields


def test_parameter_examples_use_wire_aliases_and_keep_existing_defaults():
    model = param.AdsOperationLogs
    values = {}
    for name in model.__annotations__:
        field = model.model_fields[name]
        assert field.description and "\n" not in field.description
        assert type(field.examples) is list and len(field.examples) == 1
        assert field.is_required()
        values[name] = field.examples[0]
    result = model.model_validate(values).model_dump_params()
    assert result == {
        "sid": 10105,
        "start_date": "2026-10-01",
        "end_date": "2026-10-16",
        "sponsored_type": "sp",
        "operate_type": "campaigns",
        "log_source": "all",
    }
    assert model.model_fields["ad_type"].alias == "sponsored_type"
    assert model.model_fields["operation_target"].alias == "operate_type"
    assert model.model_fields["offset"].default is None
    assert model.model_fields["length"].default is None


def test_parameter_and_validator_documentation_examples_run_without_network():
    parser = doctest.DocTestParser()
    runner = doctest.DocTestRunner()
    objects = (
        param.AdsOperationLogs,
        param.AdsOperationLogs._validate_date,
        param.AdsOperationLogs._validate_ad_type,
    )
    for item in objects:
        doc = inspect.getdoc(item)
        assert all(section in doc for section in ("Args:", "Raises:", "Examples:"))
        example = parser.get_doctest(
            doc, vars(param).copy(), item.__qualname__, item.__module__, 0
        )
        assert example.examples
        runner.run(example)
    result = runner.summarize()
    assert result.failed == 0 and result.attempted >= 4


@pytest.mark.parametrize("value", ["true", "false", "1.0", "5.0", '{ "amount": 1.00 }'])
def test_nested_operation_values_remain_exact_strings(value):
    item = schema.AdsOperation(code="BUDGET_AMOUNT", value=value)
    assert type(item.value) is str and item.model_dump()["value"] == value
    assert json.loads(item.model_dump_json())["value"] == value
    assert schema.AdsOperation(code="BUDGET_AMOUNT", value=None).value == ""


def test_documentation_validation_rejects_a_decoded_boolean(monkeypatch):
    function = AdsAPI.AdsOperationLogs
    parts = function.__doc__.split(".. code-block:: python")
    _, shown = documentation_example(function)
    changed = deepcopy(shown)
    changed["data"][0]["before"][0]["value"] = True
    parts[2] = "\n\n" + "\n".join(
        "                " + line
        for line in repr(changed).replace("Ellipsis", "...").splitlines()
    )
    monkeypatch.setattr(function, "__doc__", ".. code-block:: python".join(parts))
    with pytest.raises(ValidationError, match="valid string"):
        validate_documentation(function, schema.AdsOperationLogs)
