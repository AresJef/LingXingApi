"""四SD日报的新客指标：真实零值与合成null/错误边界分开验证。"""

from __future__ import annotations

from copy import deepcopy
from typing import get_args

import pytest
from pydantic import TypeAdapter, ValidationError

from lingxingapi.ads import schema
from lingxingapi.fields import IntOrNone2Zero, FloatOrNone2Zero
from response_contract import ContractError, validate_response

MODELS = (
    schema.SdCampaignReports,
    schema.SdAdGroupReports,
    schema.SdProductReports,
    schema.SdTargetReports,
)
FIELDS = (
    (
        "attributed_orders_new_to_brand_14d",
        "new_to_brand_orders_14d",
        IntOrNone2Zero,
        "品牌新客14天订单数",
        0,
    ),
    (
        "attributed_units_ordered_new_to_brand_14d",
        "new_to_brand_units_14d",
        IntOrNone2Zero,
        "品牌新客14天商品件数",
        0,
    ),
    (
        "attributed_sales_new_to_brand_14d",
        "new_to_brand_sales_14d",
        FloatOrNone2Zero,
        "品牌新客14天销售额",
        0.0,
    ),
)


def response(model):
    row = {
        "profile_id": 1,
        "campaign_id": 2,
        "tactic": "T00030",
        "cost": 1.0,
        "impressions": 2,
        "view_impressions": 0,
        "clicks": 1,
        "orders": 0,
        "same_orders": 0,
        "units": 0,
        "sales": 0.0,
        "same_sales": 0.0,
        "report_date": "2026-10-01",
    }
    if model is not schema.SdCampaignReports:
        row["ad_group_id"] = 3
    if model is schema.SdProductReports:
        row.update(ad_id=4, asin="B0AAAA1234", sku="synthetic")
    if model is schema.SdTargetReports:
        row.update(
            target_id=5,
            targeting_expression="synthetic",
            targeting_type=None,
            targeting_text="synthetic",
        )
    row.update({wire: value for wire, _, _, _, value in FIELDS})
    return {
        "code": 0,
        "message": "success",
        "error_details": [],
        "request_id": "synthetic",
        "response_time": "2001-05-07 00:00:00",
        "total": 1,
        "next_token": None,
        "data": [row],
    }


@pytest.mark.parametrize("model", MODELS)
@pytest.mark.parametrize("wire,name,kind,description,zero", FIELDS)
def test_approved_fields_have_exact_names_converter_alias_and_required_no_default(
    model, wire, name, kind, description, zero
):
    row_model = get_args(model.model_fields["data"].annotation)[0]
    field = row_model.model_fields[name]
    assert (
        field.annotation is kind
        and field.validation_alias == wire
        and field.is_required()
    )
    assert field.description == description and field.examples == [zero]
    raw = response(model)
    parsed = validate_response(raw, model).data[0].model_dump()
    assert (
        parsed[name] == zero and type(parsed[name]) is type(zero) and wire not in parsed
    )
    del raw["data"][0][wire]
    with pytest.raises(ValidationError):
        model.model_validate(raw)
    with pytest.raises(ContractError):
        validate_response(raw, model)


@pytest.mark.parametrize("model", MODELS)
@pytest.mark.parametrize("wire,name,kind,description,zero", FIELDS)
@pytest.mark.parametrize(
    "value", [0, 0.0, None, "", False, True, -2, 1.0, 1.5, "2", "2.5", "bad", [], {}]
)
def test_synthetic_inputs_follow_the_existing_shared_converter_without_raw_rewriting(
    model, wire, name, kind, description, zero, value
):
    raw = response(model)
    raw["data"][0][wire] = deepcopy(value)
    before = deepcopy(raw)
    try:
        expected = TypeAdapter(kind).validate_python(value)
    except ValidationError:
        with pytest.raises(ValidationError):
            model.model_validate(raw)
    else:
        actual = getattr(model.model_validate(raw).data[0], name)
        assert actual == expected and type(actual) is type(expected)
        if value is None or value == "":
            assert actual == zero and type(actual) is type(zero)
    assert raw == before


@pytest.mark.parametrize("model", MODELS)
def test_strict_contract_accepts_synthetic_null_zero_conversion_but_no_unapproved_fields(
    model,
):
    raw = response(model)
    for wire, *_ in FIELDS:
        raw["data"][0][wire] = None
    parsed = validate_response(raw, model)
    for wire, name, _, _, zero in FIELDS:
        assert raw["data"][0][wire] is None
        assert getattr(parsed.data[0], name) == zero
    raw["data"][0]["unapproved_metric"] = None
    with pytest.raises(ContractError):
        validate_response(raw, model)
