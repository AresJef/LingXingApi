"""六个 SP 实体契约的离线边界；合成输入不作为真实采集证据。"""
from __future__ import annotations

from copy import deepcopy
import asyncio
import ast
import inspect
import json
from pathlib import Path
import textwrap
from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest

from lingxingapi.ads import schema
from response_contract import ContractError, validate_response
from sp_entities_contract import MODELS, validate_sp_entity_response
from lingxingapi.ads.api import AdsAPI
from lingxingapi import errors
from documentation_contract import validate_documentation, validate_field_examples


def synthetic_response(method):
    row={"profile_id":62609628290910,"campaign_id":10001,"ad_group_id":20001,
         "state":"enabled","serving_status":"enabled","creation_date":1,"last_updated_date":2}
    row.update({
        "SpAdGroups":{"name":"synthetic-group","default_bid":1.0},
        "SpProducts":{"ad_id":30001,"asin":"B000000001","sku":"synthetic-sku","video_details":[]},
        "SpKeywords":{"keyword_id":40001,"keyword_text":"synthetic keyword","match_type":"exact","bid":1.0},
        "SpTargets":{"target_id":50001,"expression_type":"auto","expression":"[]","resolved_expression":"[]","bid":1.0},
        "SpNegativeKeywords":{"target_id":60001,"negative_text":"synthetic keyword","negative_match_type":"negativeExact","negative_type":"negativeKeyword"},
        "SpNegativeTargets":{"target_id":70001,"negative_text":"B000000001","negative_type":"negativeAsin","negative_match_type":""},
    }[method])
    return {"code":0,"message":"success","error_details":[],"request_id":"synthetic-request",
            "response_time":"2001-05-07 00:00:00","total":1,"next_token":None,"data":[row]}


@pytest.mark.parametrize("endpoint,model",tuple(MODELS.items()))
def test_nonempty_contract_keeps_full_original_response_and_required_fields(endpoint,model):
    raw=synthetic_response(endpoint.split('.')[1]);before=deepcopy(raw)
    parsed=validate_sp_entity_response(raw,model)
    assert raw==before and parsed.response_count==1 and parsed.total_count==1
    for key in ("profile_id","campaign_id","ad_group_id"):
        assert getattr(parsed.data[0],key)==raw['data'][0][key]
    for key in tuple(raw['data'][0]):
        bad=deepcopy(raw);del bad['data'][0][key]
        with pytest.raises(ContractError):validate_sp_entity_response(bad,model)


@pytest.mark.parametrize("extra",["tags","bid_optimization","video_details","other"])
@pytest.mark.parametrize("endpoint,model",tuple(MODELS.items()))
def test_no_sp_campaigns_field_exemption_is_applied(endpoint,model,extra):
    raw=synthetic_response(endpoint.split('.')[1]);raw['data'][0][extra]=[]
    if model is schema.SpProducts and extra=='video_details':
        raw['data'][0][extra]=[{'asset_id':'synthetic','asset_version':'version_v1','headline':'Synthetic',
                              'description':'Synthetic','name':None,'url':None,'other':True}]
    with pytest.raises(ContractError) as caught:validate_sp_entity_response(raw,model)
    assert caught.value.status=='difference' and any('多字段' in item for item in caught.value.issues)


@pytest.mark.parametrize("endpoint,model",tuple(MODELS.items()))
def test_explicit_empty_case_only_waives_element_coverage(endpoint,model):
    raw=synthetic_response(endpoint.split('.')[1]);raw.update(data=[],total=0)
    assert validate_sp_entity_response(raw,model,scenario='empty_expected').response_count==0
    with pytest.raises(ContractError):validate_response(raw,model)
    for patch in ({'tags':[]},{'code':1},{'next_token':[]},{'error_details':['failure']},{'response_count':1}):
        with pytest.raises(ContractError):validate_sp_entity_response(raw|patch,model,scenario='empty_expected')
    for key in ('request_id','response_time','message','error_details','next_token','total'):
        bad=deepcopy(raw);del bad[key]
        with pytest.raises(ContractError):validate_sp_entity_response(bad,model,scenario='empty_expected')


def test_unregistered_schema_is_rejected():
    with pytest.raises(ContractError):validate_sp_entity_response({},schema.SpCampaigns)


@pytest.mark.parametrize('method,key', [('SpNegativeKeywords','negative_type'),('SpNegativeTargets','negative_match_type')])
@pytest.mark.parametrize('invalid',[None,False,0,[],{},'other','negativeExact'])
def test_negative_branch_exemption_keeps_missing_invalid_and_independent_semantics_strict(method,key,invalid):
    raw=synthetic_response(method);before=deepcopy(raw);model=MODELS['ads.'+method]
    parsed=validate_sp_entity_response(raw,model)
    assert raw==before and key not in parsed.data[0].model_dump()
    raw['data'][0][key]=invalid
    with pytest.raises(ContractError):validate_sp_entity_response(raw,model)


@pytest.mark.parametrize("method",["SpNegativeKeywords","SpNegativeTargets"])
@pytest.mark.parametrize("campaign,expected",[(None,None),(0,0),(123,123),("123",123),(123.0,123),(True,1)])
def test_negative_campaign_id_correct_name_preserves_parameter_rules(method,campaign,expected):
    target_type='keyword' if method=='SpNegativeKeywords' else 'target'
    signed=AsyncMock(return_value=synthetic_response(method))
    asyncio.run(getattr(AdsAPI,method)(SimpleNamespace(_request_with_sign=signed),None,62609628290910,campaign_id=campaign))
    body={'profile_id':62609628290910,'target_type':target_type}
    if expected is not None:body['campaign_id']=expected
    signed.assert_awaited_once_with('POST','/pb/openapi/newad/spNegativeTargetsOrKeywords',body=body,headers={'X-API-VERSION':'2'})


@pytest.mark.parametrize("method",["SpNegativeKeywords","SpNegativeTargets"])
def test_negative_campaign_old_spelling_is_rejected_without_request(method):
    signed=AsyncMock()
    with pytest.raises(TypeError):
        asyncio.run(getattr(AdsAPI,method)(SimpleNamespace(_request_with_sign=signed),None,62609628290910,champaign_id=123))
    signed.assert_not_awaited()


@pytest.mark.parametrize("method",["SpNegativeKeywords","SpNegativeTargets"])
@pytest.mark.parametrize("campaign",[-1,1.5,"bad",[],{}])
def test_negative_campaign_invalid_values_fail_before_request(method,campaign):
    signed=AsyncMock()
    with pytest.raises(errors.InvalidParametersError):
        asyncio.run(getattr(AdsAPI,method)(SimpleNamespace(_request_with_sign=signed),None,62609628290910,campaign_id=campaign))
    signed.assert_not_awaited()


@pytest.mark.parametrize("method",[endpoint.split('.')[1] for endpoint in MODELS])
@pytest.mark.parametrize("identifiers,expected",[({'sid':1,'profile_id':None},{'sid':1}),({'sid':None,'profile_id':2},{'profile_id':2}),({'sid':0,'profile_id':2},{'sid':0,'profile_id':2})])
def test_six_sdk_methods_exact_identifiers_pagination_and_optional_key_omission(method,identifiers,expected):
    signed=AsyncMock(return_value=synthetic_response(method))
    extra={'next_token':' cursor ','offset':'2','length':0}
    if 'Negative' not in method:extra['state']=' enabled '
    args={**identifiers,**extra}
    asyncio.run(getattr(AdsAPI,method)(SimpleNamespace(_request_with_sign=signed),**args))
    body={**expected,'next_token':'cursor','offset':2,'length':0}
    if 'Negative' in method:body['target_type']='keyword' if method=='SpNegativeKeywords' else 'target'
    else:body['state']='enabled'
    assert signed.await_args.kwargs=={'body':body,'headers':{'X-API-VERSION':'2'}}


@pytest.mark.parametrize("method",[endpoint.split('.')[1] for endpoint in MODELS])
@pytest.mark.parametrize("unexpected",['match_type','ad_group_id','target_type'])
def test_unexposed_entity_filters_are_rejected_without_network(method,unexpected):
    signed=AsyncMock()
    with pytest.raises(TypeError):
        asyncio.run(getattr(AdsAPI,method)(SimpleNamespace(_request_with_sign=signed),None,2,**{unexpected:'synthetic'}))
    signed.assert_not_awaited()


@pytest.mark.parametrize("method",[endpoint.split('.')[1] for endpoint in MODELS])
def test_six_sdk_methods_omit_none_options_and_reject_missing_both_identifiers(method):
    signed=AsyncMock(return_value=synthetic_response(method))
    asyncio.run(getattr(AdsAPI,method)(SimpleNamespace(_request_with_sign=signed),None,2))
    expected={'profile_id':2}
    if 'Negative' in method:expected['target_type']='keyword' if method=='SpNegativeKeywords' else 'target'
    assert signed.await_args.kwargs['body']==expected
    signed.reset_mock()
    with pytest.raises(errors.InvalidParametersError):
        asyncio.run(getattr(AdsAPI,method)(SimpleNamespace(_request_with_sign=signed),None,None))
    signed.assert_not_awaited()


@pytest.mark.parametrize("method",['SpAdGroups','SpProducts','SpKeywords','SpTargets'])
def test_standard_entities_do_not_expose_campaign_filter(method):
    with pytest.raises(TypeError):
        asyncio.run(getattr(AdsAPI,method)(SimpleNamespace(_request_with_sign=AsyncMock()),None,2,campaign_id=1))


@pytest.mark.parametrize("method",['SpNegativeKeywords','SpNegativeTargets'])
def test_negative_entities_do_not_expose_state_filter(method):
    with pytest.raises(TypeError):
        asyncio.run(getattr(AdsAPI,method)(SimpleNamespace(_request_with_sign=AsyncMock()),None,2,state='enabled'))


@pytest.mark.parametrize("method,prefix",[("SpAdGroups","sp_ad_groups"),("SpProducts","sp_products"),("SpKeywords","sp_keywords"),("SpTargets","sp_targets"),("SpNegativeKeywords","sp_negative_keywords"),("SpNegativeTargets","sp_negative_targets")])
def test_real_completed_entity_fixtures_keep_full_data_relations(method,prefix):
    from sample_collection import load_collection,same_data
    manifest,records,responses=load_collection(Path(__file__).with_name('fixtures')/'ads/basic/sp'/f'{prefix}-manifest.json','ads.'+method)
    assert manifest['planned_requests']==(11 if 'Negative' in method else 14) and manifest['not_run']==[]
    assert len(records)==manifest['planned_requests']+(1 if method=='SpProducts' else 0)
    if method=='SpProducts':
        assert manifest['supplemental_samples']==1 and records['video-evidence']['supplemental']
        assert records['video-evidence']['next_token_from']=='external-video-probe'
    for label,raw in responses.items():
        original=deepcopy(raw)
        parsed=validate_sp_entity_response(raw,MODELS['ads.'+method],scenario=records[label]['scenario'])
        assert raw==original and parsed.response_count==len(raw['data']) and parsed.total_count==raw['total']
    assert same_data(responses['account-A-profile-only']['data'],responses['account-A-sid-only']['data'])
    assert same_data(responses['account-A-profile-only']['data'],responses['account-A-both']['data'])
    assert same_data(responses['account-A-sid-B-profile']['data'],responses['account-B-profile-only']['data'])
    assert same_data(responses['account-B-sid-A-profile']['data'],responses['account-A-profile-only']['data'])
    for state in (() if 'Negative' in method else ('enabled','paused','archived')):
        assert all(row['state']==state for row in responses['state-'+state]['data'])
    relationships=manifest['relationships'];reference=responses[relationships['reference']]['data']
    for mode in ('offset','token'):
        assert same_data([row for label in relationships[mode+'_pages'] for row in responses[label]['data']],reference)
    assert same_data(responses[relationships['token_control']]['data'],responses[relationships['token_conflict']]['data'])
    assert same_data(reference,responses[relationships['end_reference']]['data'])


@pytest.mark.parametrize("method,prefix,row_model",[("SpAdGroups","sp_ad_groups",schema.SpAdGroup),("SpProducts","sp_products",schema.SpProduct),("SpKeywords","sp_keywords",schema.SpKeyword),("SpTargets","sp_targets",schema.SpTarget),("SpNegativeKeywords","sp_negative_keywords",schema.SpNegativeKeyword),("SpNegativeTargets","sp_negative_targets",schema.SpNegativeTarget)])
def test_completed_entity_public_documentation_and_current_fixture_have_separate_contracts(method,prefix,row_model):
    path=Path(__file__).with_name('fixtures')/'ads/basic/sp'/f'{prefix}-account-A-profile-only.json'
    wrapper=json.loads(path.read_bytes());parsed=validate_sp_entity_response(wrapper['response'],MODELS['ads.'+method])
    assert wrapper['source']=='local_raw' and wrapper['endpoint']=='ads.'+method
    field_values = validate_field_examples(row_model)
    if method == 'SpProducts':
        assert len(field_values['video_details']) == 1
    for name,field in row_model.model_fields.items():
        assert field.description and '\n' not in field.description
    doc=inspect.getdoc(getattr(AdsAPI,method))
    assert doc.count('.. code-block:: python')==2
    assert doc.index('## Docs')<doc.index('Args:')<doc.index('Returns:')<doc.index('Examples:')
    assert all(word not in doc for word in ('本次','实测','采集','样本','推定时区'))
    source=textwrap.dedent(doc.split('.. code-block:: python')[1]).strip()
    call=ast.parse(source).body[0].value.value
    assert ast.unparse(call.func)=='client.ads.'+method
    args={item.arg:ast.literal_eval(item.value) for item in call.keywords}
    shown = validate_documentation(getattr(AdsAPI,method), MODELS['ads.'+method])
    assert args=={'profile_id':shown['data'][0]['profile_id'],'offset':0,'length':2}
    assert all(row['profile_id']==args['profile_id'] for row in shown['data'] if row is not Ellipsis)
    if method == 'SpProducts':
        assert shown['data'][0]['video_details'] and shown['data'][0]['video_details'][0]['asset_id']
    signed=AsyncMock(return_value=wrapper['response'])
    actual=asyncio.run(getattr(AdsAPI,method)(SimpleNamespace(_request_with_sign=signed),**args))
    assert actual.model_dump()==parsed.model_dump()
