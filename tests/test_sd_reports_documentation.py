"""SD 报告静态文档与公开模型契约；不读取每日可覆盖的报告文件。"""

import ast
from copy import deepcopy
import inspect
import json
from pathlib import Path
from typing import get_args

import pytest

from lingxingapi.ads import schema
from lingxingapi.ads.api import AdsAPI
from documentation_contract import (
    documentation_example,
    validate_documentation,
    validate_field_examples,
)
from report_examples_contract import validate_report_metric_examples

METHODS = {
    "SdCampaignReports": "sdCampaignReports",
    "SdCampaignHourData": "sdCampaignHourData",
    "SdAdGroupReports": "sdAdGroupReports",
    "SdAdGroupHourData": "sdAdGroupHourData",
    "SdProductReports": "sdProductAdReports",
    "SdProductHourData": "sdAdvertiseHourData",
    "SdTargetReports": "sdTargetReports",
    "SdTargetHourData": "sdTargetHourData",
    "SdMatchedTargetReports": "sdMatchTargetReports",
}
DAILY = tuple(name for name in METHODS if name.endswith("Reports"))
NEW_CUSTOMER_MODELS = (
    schema.SdCampaignReport,
    schema.SdAdGroupReport,
    schema.SdProductReport,
    schema.SdTargetReport,
)
NEW_CUSTOMER_FIELDS = {
    "new_to_brand_orders_14d": ("attributed_orders_new_to_brand_14d", 0),
    "new_to_brand_units_14d": ("attributed_units_ordered_new_to_brand_14d", 0),
    "new_to_brand_sales_14d": ("attributed_sales_new_to_brand_14d", 0.0),
}
NEW_CUSTOMER_DESCRIPTIONS = {
    "new_to_brand_orders_14d": "品牌新客14天订单数",
    "new_to_brand_units_14d": "品牌新客14天商品件数",
    "new_to_brand_sales_14d": "品牌新客14天销售额",
}


@pytest.mark.parametrize("method,slug", METHODS.items())
def test_method_documentation_has_google_sections_actual_call_and_complete_public_row(
    method, slug
):
    model = getattr(schema, method)
    function = getattr(AdsAPI, method)
    doc = inspect.getdoc(function)
    assert "领星接口文档: 新广告 - 报告." in doc
    assert f"https://apidoc.lingxing.com/new/api-docs/newAd/report/{slug}/" in doc
    assert (
        doc.index("## Docs")
        < doc.index("Args:")
        < doc.index("Returns:")
        < doc.index("Examples:")
    )
    assert f"ads.schema.{method}:" in doc
    assert all(word not in doc for word in ("实测", "样本", "采集", "本次"))
    assert ":param " not in doc and "```" not in doc
    for name in inspect.signature(function).parameters:
        if name != "self":
            assert f"{name} (" in doc
    shown = validate_documentation(function, model)
    assert shown["data"] and shown["data"][0]
    field = model.model_fields["data"]
    assert field.description and "\n" not in field.description
    assert type(field.examples) is list and len(field.examples) == 1
    assert type(field.examples[0]) is list and len(field.examples[0]) == 1
    assert all(value is not Ellipsis for value in field.examples[0])
    validate_report_metric_examples(function, model)


def row_models():
    return tuple(
        get_args(getattr(schema, method).model_fields["data"].annotation)[0]
        for method in METHODS
    )


@pytest.mark.parametrize("model", row_models(), ids=lambda model: model.__name__)
def test_row_fields_have_single_typed_examples_and_single_line_descriptions(model):
    record = validate_field_examples(model)
    assert set(record) == set(model.__annotations__)
    for field in model.model_fields.values():
        assert all(
            word not in field.description for word in ("实测", "样本", "采集", "本次")
        )


@pytest.mark.parametrize("method", DAILY)
def test_daily_example_respects_required_signature_and_explicit_none_identifier(method):
    function = getattr(AdsAPI, method)
    signature = inspect.signature(function)
    assert signature.parameters["sid"].default is inspect.Parameter.empty
    assert signature.parameters["profile_id"].default is inspect.Parameter.empty
    call, shown = documentation_example(function)
    args = {item.arg: ast.literal_eval(item.value) for item in call.keywords}
    assert args["sid"] is None
    assert args["profile_id"] == shown["data"][0]["profile_id"]
    assert args["report_date"] == shown["data"][0]["report_date"]
    assert "显式传None" in inspect.getdoc(function)


@pytest.mark.parametrize(
    "method", [name for name in METHODS if name.endswith("HourData")]
)
def test_hourly_example_uses_the_same_campaign_and_date_as_its_output(method):
    call, shown = documentation_example(getattr(AdsAPI, method))
    args = {item.arg: ast.literal_eval(item.value) for item in call.keywords}
    row = shown["data"][0]
    assert args == {
        "report_date": row["report_date"],
        "campaign_id": row["campaign_id"],
    }


@pytest.mark.parametrize("model", NEW_CUSTOMER_MODELS, ids=lambda model: model.__name__)
def test_new_customer_examples_keep_real_zero_types_and_existing_required_aliases(
    model,
):
    for name, (alias, value) in NEW_CUSTOMER_FIELDS.items():
        field = model.model_fields[name]
        assert field.is_required() and field.validation_alias == alias
        assert field.description == NEW_CUSTOMER_DESCRIPTIONS[name]
        assert type(field.examples[0]) is type(value) and field.examples == [value]


def test_metric_projection_registers_all_38_methods_and_all_nine_sd_methods():
    frozen = json.loads(
        Path(__file__).with_name("report_examples_metrics.json").read_bytes()
    )
    assert frozen["format"] == "report-example-metrics-v1"
    names = set(frozen["methods"])
    assert len(names) == 38
    assert {name for name in names if name.startswith("Sd")} == set(METHODS)
    assert len({name for name in names if name.startswith(("Sp", "Sb"))}) == 29


def test_public_product_hour_row_keeps_its_existing_class_name():
    assert (
        get_args(schema.SdProductHourData.model_fields["data"].annotation)[0]
        is schema.SpdProductHour
    )


def test_matched_target_description_keeps_the_product_detail_page_click_scope():
    doc = inspect.getdoc(AdsAPI.SdMatchedTargetReports)
    assert "ASIN商品详情页展示且发生点击" in doc


@pytest.mark.parametrize("block", [1, 2], ids=["call", "output"])
def test_documentation_rejects_code_at_the_directive_indentation(monkeypatch, block):
    function = AdsAPI.SdCampaignReports
    parts = function.__doc__.split(".. code-block:: python")
    assert len(parts) == 3
    parts[block] = "\n".join(
        line[4:] if line.strip() else line for line in parts[block].split("\n")
    )
    monkeypatch.setattr(function, "__doc__", ".. code-block:: python".join(parts))
    with pytest.raises(AssertionError, match="代码块缩进"):
        validate_report_metric_examples(function, schema.SdCampaignReports)


def test_full_row_metric_projection_rejects_a_changed_business_metric(monkeypatch):
    function = AdsAPI.SdCampaignReports
    parts = function.__doc__.split(".. code-block:: python")
    assert len(parts) == 3
    _, shown = documentation_example(function)
    changed = deepcopy(shown)
    changed["data"][0]["cost"] += 1.0
    parts[2] = "\n\n" + "\n".join(
        "                " + line
        for line in repr(changed).replace("Ellipsis", "...").splitlines()
    )
    monkeypatch.setattr(function, "__doc__", ".. code-block:: python".join(parts))
    with pytest.raises(AssertionError, match="冻结真实行不一致|真实完整行"):
        validate_report_metric_examples(function, schema.SdCampaignReports)
