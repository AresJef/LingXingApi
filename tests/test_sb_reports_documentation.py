"""SB报告公开文档与真实类型一致；不将每日可覆盖值当成静态文档值。"""
import inspect
from typing import get_args

import pytest

from lingxingapi.ads import param, schema
from lingxingapi.ads.api import AdsAPI
from documentation_contract import validate_documentation, validate_field_examples
from report_examples_contract import validate_report_metric_examples
from test_sb_reports_requests import DAILY, HOURLY

METHODS = tuple(row[0] for row in (*DAILY, *HOURLY))


@pytest.mark.parametrize("method", METHODS)
def test_method_docs_have_actual_arguments_typed_public_output_and_one_example_row(method):
    model = getattr(schema, method)
    function = getattr(AdsAPI, method)
    doc = inspect.getdoc(function)
    assert "## Docs" in doc and "领星接口文档: 新广告 - 报告." in doc
    assert doc.index("## Docs") < doc.index("Args:") < doc.index("Returns:") < doc.index("Examples:")
    assert all(word not in doc for word in ("实测", "样本", "采集", "本次"))
    assert ":param " not in doc and "```" not in doc
    shown = validate_documentation(function, model)
    assert shown["data"] and shown["data"][0]
    field = model.model_fields["data"]
    assert field.description and len(field.examples) == 1 and len(field.examples[0]) == 1
    validate_report_metric_examples(function, model)


def row_models():
    result = set()
    for method in METHODS:
        row = get_args(getattr(schema, method).model_fields["data"].annotation)[0]
        for model in row.__mro__:
            if model.__module__ == "lingxingapi.ads.schema":
                result.add(model)
    return tuple(result)


@pytest.mark.parametrize("model", row_models(), ids=lambda model: model.__name__)
def test_row_own_fields_have_typed_single_element_examples(model):
    validate_field_examples(model)


@pytest.mark.parametrize("method,field", [("SbTargetingHourData", "sales"), ("SbCostAllocationReports", "orders")])
def test_known_positive_field_evidence_cannot_regress_to_zero(monkeypatch, method, field):
    model = getattr(schema, method)
    row = get_args(model.model_fields["data"].annotation)[0]
    monkeypatch.setattr(row.model_fields[field], "examples", [0.0])
    with pytest.raises(AssertionError, match="已有非零真实证据"):
        validate_report_metric_examples(getattr(AdsAPI, method), model)


@pytest.mark.parametrize("model", [param.SbTargetingReports, param.SbQueryReports])
def test_parameter_docs_examples_and_google_validator_docs(model):
    assert "Args:" in inspect.getdoc(model) and "Examples:" in inspect.getdoc(model)
    data = {}
    for name, field in model.model_fields.items():
        if field.examples:
            data[field.alias or name] = field.examples[0]
        elif name in {"offset", "length"}:
            data[name] = 0 if name == "offset" else 2
    assert model.model_validate_params(data)
    for name in model.__annotations__:
        field = model.model_fields[name]
        assert field.description and isinstance(field.examples, list) and len(field.examples) == 1
