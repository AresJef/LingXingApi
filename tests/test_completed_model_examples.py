"""已完成接口的字段示例语义；不依赖引号、尾逗号或换行布局。"""
from __future__ import annotations

import ast
import io
import json
from pathlib import Path
import tokenize
from typing import get_args

from pydantic import BaseModel
import pytest

from lingxingapi.ads import param as ads_param, schema as ads_schema
from lingxingapi.basic import param as basic_param
from documentation_contract import validate_field_examples


PARAMETERS = (basic_param.CountryCode, basic_param.RenameSeller, basic_param.RenameSellers,
              basic_param.ExchangeRate, basic_param.EditExchangeRate, ads_param.AdProfiles,
              ads_param.AdEntities, ads_param.SpNegativeTargeting, ads_param.SbTargeting, ads_param.AdsOperationLogs)


def completed_models():
    from lingxingapi.ads.api import AdsAPI
    from lingxingapi.basic.api import BasicAPI
    from test_documentation_contract import BASIC_METHODS, ADS_METHODS
    from typing import get_type_hints

    models = set()
    def visit(annotation):
        if isinstance(annotation, type) and issubclass(annotation, BaseModel):
            if annotation in models:
                return
            models.add(annotation)
            for field in annotation.model_fields.values():
                visit(field.annotation)
        for item in get_args(annotation):
            visit(item)
    for api, methods in ((BasicAPI, BASIC_METHODS), (AdsAPI, ADS_METHODS)):
        for method in methods:
            visit(get_type_hints(getattr(api, method))["return"])
    models.update(PARAMETERS)
    return tuple(sorted((model for model in models if model.__module__ in {
        "lingxingapi.basic.schema", "lingxingapi.basic.param", "lingxingapi.ads.schema", "lingxingapi.ads.param"
    }), key=lambda model: (model.__module__, model.__name__)))


@pytest.mark.parametrize("model", completed_models(), ids=lambda model: model.__module__ + "." + model.__name__)
def test_completed_own_fields_have_serializable_single_element_examples(model):
    def check(value):
        if type(value) is list:
            assert len(value) <= 1
            for item in value:
                check(item)
        elif type(value) is dict:
            for item in value.values():
                check(item)

    for name in model.__annotations__:
        if name not in model.model_fields:
            continue
        field = model.model_fields[name]
        assert field.description
        assert isinstance(field.examples, list) and len(field.examples) == 1
        json.dumps(field.examples)
        check(field.examples[0])  # 表达式仍为不透明字符串，不解析或截断内部条件。
    if model not in PARAMETERS and model.model_fields.keys() <= model.__annotations__.keys():
        validate_field_examples(model)


@pytest.mark.parametrize("model", PARAMETERS, ids=lambda model: model.__name__)
def test_parameter_examples_form_valid_safe_requests(model):
    data = {}
    for name, field in model.model_fields.items():
        if field.examples:
            data[field.alias or name] = field.examples[0]
        elif name in {"offset", "length"}:
            data[name] = 0 if name == "offset" else 2  # base只读，分页边界不补写元数据。
    parsed = model.model_validate_params(data)
    assert type(parsed) is dict and parsed
    assert not any(key in parsed for key in {"password", "app_secret", "access_token"})


@pytest.mark.parametrize("field,value", [("collection_type", "THEMED"), ("title", "000AA AA & AAA - 0000+ Aaaaao")])
def test_sb_nested_examples_use_existing_nonempty_redacted_evidence(field, value):
    assert ads_schema.SbCreativeConfig.model_fields[field].examples == [value]
    assert ads_schema.SbCreative.model_fields["creative_config"].examples[0][field] == value
    assert ads_schema.SbCreatives.model_fields["data"].examples[0][0]["creative_config"][field] == value


@pytest.mark.parametrize("module,filename,boundary", [
    ("basic", "schema.py", None), ("basic", "param.py", None),
    ("ads", "schema.py", "SpCampaignReport"), ("ads", "param.py", "AdReports"),
])
def test_completed_regions_have_no_formatter_disable_comments(module, filename, boundary):
    path = Path(__file__).parents[1] / "src/lingxingapi" / module / filename
    source = path.read_text()
    end = next(node.lineno for node in ast.parse(source).body
               if isinstance(node, ast.ClassDef) and node.name == boundary) if boundary else len(source.splitlines()) + 1
    assert not [token for token in tokenize.generate_tokens(io.StringIO(source).readline)
                if token.type == tokenize.COMMENT and token.start[0] < end
                and token.string.strip() in {"# fmt: off", "# fmt: on"}]
