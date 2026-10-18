"""SP报告静态文档按公开输出验证；真实集合另验，不与每日值绑定。"""
import inspect
from typing import get_args

import pytest

from lingxingapi.ads import schema,param
from lingxingapi.ads.api import AdsAPI
from documentation_contract import validate_documentation,validate_field_examples
from report_examples_contract import validate_report_metric_examples
from test_sp_reports_requests import DAILY,HOURLY

METHODS=tuple(row[0] for row in (*DAILY,*HOURLY))


@pytest.mark.parametrize('method',METHODS)
def test_report_method_documentation_has_real_public_output_and_actual_arguments(method):
    model=getattr(schema,method);doc=inspect.getdoc(getattr(AdsAPI,method))
    assert '## Docs' in doc and '领星接口文档: 新广告 - 报告.' in doc
    assert doc.index('## Docs')<doc.index('Args:')<doc.index('Returns:')<doc.index('Examples:')
    assert all(word not in doc for word in ('实测','样本','采集','本次'))
    assert ':param ' not in doc and '```' not in doc
    shown=validate_documentation(getattr(AdsAPI,method),model)
    assert shown['data'] and shown['data'][0]
    field=model.model_fields['data']
    assert field.description and isinstance(field.examples,list) and len(field.examples)==1 and len(field.examples[0])==1
    validate_report_metric_examples(getattr(AdsAPI, method), model)


def row_models():
    result=set()
    for method in METHODS:
        row=get_args(getattr(schema,method).model_fields['data'].annotation)[0]
        for model in row.__mro__:
            if model.__module__=='lingxingapi.ads.schema':result.add(model)
    return tuple(result)


@pytest.mark.parametrize('model',row_models(),ids=lambda model:model.__name__+':'+','.join(model.__annotations__))
def test_report_row_own_fields_have_real_typed_single_examples(model):
    validate_field_examples(model)


@pytest.mark.parametrize("block", [1, 2], ids=["call", "output"])
def test_report_documentation_rejects_code_at_directive_indentation(monkeypatch, block):
    method = AdsAPI.SpCampaignReports
    parts = method.__doc__.split(".. code-block:: python")
    parts[block] = "\n".join(line[4:] if line.strip() else line for line in parts[block].split("\n"))
    monkeypatch.setattr(method, "__doc__", ".. code-block:: python".join(parts))
    with pytest.raises(AssertionError, match="代码块缩进"):
        validate_report_metric_examples(method, schema.SpCampaignReports)


def test_rich_real_hourly_example_cannot_regress_to_zero_cost(monkeypatch):
    method = AdsAPI.SpCampaignHourData
    assert '"cost": 1.5' in method.__doc__
    monkeypatch.setattr(method, "__doc__", method.__doc__.replace('"cost": 1.5', '"cost": 0.0', 1))
    with pytest.raises(AssertionError, match="已有信息更丰富的真实完整行"):
        validate_report_metric_examples(method, schema.SpCampaignHourData)


@pytest.mark.parametrize('model',[param.AdReports,param.AdHourData,param.SpQueryReports])
def test_report_parameter_docs_and_examples_match_existing_model(model):
    assert 'Args:' in inspect.getdoc(model) and 'Examples:' in inspect.getdoc(model)
    data={}
    for name,field in model.model_fields.items():
        if field.examples:data[field.alias or name]=field.examples[0]
        elif name in {'offset','length'}:data[name]=0 if name=='offset' else 2
    assert model.model_validate_params(data)
    for name in model.__annotations__:
        field=model.model_fields[name]
        assert field.description and isinstance(field.examples,list) and len(field.examples)==1
