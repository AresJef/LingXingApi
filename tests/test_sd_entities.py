"""SD基础接口的离线参数、真实响应及公开文档契约。"""
from __future__ import annotations

import asyncio
import ast
from copy import deepcopy
import inspect
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from lingxingapi import errors
from lingxingapi.ads import route, schema
from lingxingapi.ads.api import AdsAPI
from documentation_contract import documentation_example, validate_documentation, validate_field_examples
from response_contract import ContractError
from sample_collection import load_collection, same_data
from sd_entities_contract import MODELS, validate_sd_entity_response

METHODS = tuple(endpoint.split('.')[1] for endpoint in MODELS)
ROUTES = dict(zip(METHODS, (route.SD_CAMPAIGNS, route.SD_AD_GROUPS, route.SD_PRODUCTS,
                           route.SD_TARGETS, route.SD_NEGATIVE_TARGETS), strict=True))
COMPLETED = {'SdCampaigns': ('sd_campaigns', schema.SdCampaign),
             'SdAdGroups': ('sd_ad_groups', schema.SdAdGroup),
             'SdProducts': ('sd_products', schema.SdProduct),
             'SdTargets': ('sd_targets', schema.SdTarget),
             'SdNegativeTargets': ('sd_negative_targets', schema.SdNegativeTarget)}


def empty_response():
    return {'code': 0, 'message': 'success', 'error_details': [], 'request_id': 'synthetic-only',
            'response_time': '2001-05-07 00:00:00', 'total': 0, 'next_token': None, 'data': []}


@pytest.mark.parametrize('method', METHODS)
@pytest.mark.parametrize('ids,expected', [({'sid': 1, 'profile_id': None}, {'sid': 1}),
    ({'sid': None, 'profile_id': '2'}, {'profile_id': 2}), ({'sid': 0, 'profile_id': 2}, {'sid': 0, 'profile_id': 2})])
def test_sdk_routes_aliases_none_omission_version_and_zero_preservation(method, ids, expected):
    signed = AsyncMock(return_value=empty_response())
    parsed = asyncio.run(getattr(AdsAPI, method)(SimpleNamespace(_request_with_sign=signed), **ids,
        state=' enabled ', next_token=' cursor ', offset='2', length=0))
    signed.assert_awaited_once_with('POST', ROUTES[method], body=expected | {
        'state': 'enabled', 'next_token': 'cursor', 'offset': 2, 'length': 0}, headers={'X-API-VERSION': '2'})
    assert type(parsed) is MODELS['ads.'+method] and parsed.data == []


@pytest.mark.parametrize('method', METHODS)
@pytest.mark.parametrize('patch', [{'sid': -1}, {'profile_id': 'bad'}, {'offset': -1}, {'length': 1.5}, {'next_token': ' '}])
def test_invalid_params_fail_before_any_transport(method, patch):
    signed = AsyncMock()
    with pytest.raises(errors.InvalidParametersError):
        asyncio.run(getattr(AdsAPI, method)(SimpleNamespace(_request_with_sign=signed), **{'sid':None,'profile_id':2,**patch}))
    signed.assert_not_awaited()


@pytest.mark.parametrize('method', METHODS)
def test_default_body_and_missing_identifiers_fail_before_transport(method):
    signed = AsyncMock(return_value=empty_response())
    parameters = inspect.signature(getattr(AdsAPI, method)).parameters
    assert list(parameters)[1:3] == ['sid', 'profile_id']
    assert all(parameters[key].default is None for key in ('sid', 'profile_id'))
    asyncio.run(getattr(AdsAPI, method)(SimpleNamespace(_request_with_sign=signed), profile_id=2))
    assert signed.await_args.kwargs['body'] == {'profile_id': 2}
    signed.reset_mock()
    with pytest.raises(errors.InvalidParametersError):
        asyncio.run(getattr(AdsAPI, method)(SimpleNamespace(_request_with_sign=signed)))
    signed.assert_not_awaited()


@pytest.mark.parametrize('method', METHODS)
@pytest.mark.parametrize('key', ['campaign_id','ad_group_id','target_type','ad_type'])
def test_unexposed_filters_are_never_silently_accepted(method, key):
    signed = AsyncMock()
    with pytest.raises(TypeError):
        asyncio.run(getattr(AdsAPI, method)(SimpleNamespace(_request_with_sign=signed), None, 2, **{key: 3}))
    signed.assert_not_awaited()


@pytest.mark.parametrize('method', METHODS)
def test_explicit_empty_checks_all_outer_fields_and_never_relaxes_unexpected_fields(method):
    model = MODELS['ads.'+method]
    assert validate_sd_entity_response(empty_response(), model, scenario='empty_expected').response_count == 0
    with pytest.raises(ContractError):validate_sd_entity_response(empty_response(), model)
    for patch in ({'unknown': []}, {'code': False}, {'data': None}, {'error_details': ['bad']}, {'response_count': 1}):
        with pytest.raises(ContractError):validate_sd_entity_response(empty_response() | patch, model, scenario='empty_expected')
    for key in ('request_id','response_time','total','next_token','message','error_details'):
        raw = empty_response();del raw[key]
        with pytest.raises(ContractError):validate_sd_entity_response(raw, model, scenario='empty_expected')


@pytest.mark.parametrize('method', tuple(COMPLETED))
def test_real_fourteen_windows_preserve_fields_scalar_types_order_ids_and_pagination(method):
    prefix, _ = COMPLETED[method]
    path = Path(__file__).with_name('fixtures')/'ads/basic/sd'/(prefix+'-manifest.json')
    manifest, records, responses = load_collection(path,'ads.'+method)
    assert len(records) == manifest['planned_requests'] == 14 and manifest['not_run'] == []
    assert manifest['checks']['cross_identifier_priority']['observed'] == 'profile_id'
    for label, raw in responses.items():
        before = deepcopy(raw)
        parsed = validate_sd_entity_response(raw,MODELS['ads.'+method],scenario=records[label]['scenario'])
        assert raw == before and parsed.response_count == len(raw['data']) and parsed.total_count == raw['total']
    for left, right in [('account-A-profile-only','account-A-sid-only'),('account-A-profile-only','account-A-both'),
                        ('account-A-sid-B-profile','account-B-profile-only'),('account-B-sid-A-profile','account-A-profile-only')]:
        assert same_data(responses[left]['data'],responses[right]['data'])
    for state in ('enabled','paused','archived'):
        assert all(row['state'] == state for row in responses['state-'+state]['data'])
    rel = manifest['relationships'];reference = responses[rel['reference']]['data']
    for mode in ('offset','token'):
        assert same_data([row for label in rel[mode+'_pages'] for row in responses[label]['data']],reference)
    assert same_data(responses[rel['token_control']]['data'],responses[rel['token_conflict']]['data'])
    assert same_data(reference,responses[rel['end_reference']]['data'])


@pytest.mark.parametrize('method', tuple(COMPLETED))
def test_static_public_docs_and_field_examples_are_independent_valid_output(method):
    function = getattr(AdsAPI,method);doc = inspect.getdoc(function)
    assert doc.index('## Docs') < doc.index('Args:') < doc.index('Returns:') < doc.index('Examples:')
    assert all(word not in doc for word in ('本次','实测','采集','样本'))
    call, _ = documentation_example(function)
    args = {item.arg: ast.literal_eval(item.value) for item in call.keywords}
    shown = validate_documentation(function,MODELS['ads.'+method])
    assert args == {'profile_id':shown['data'][0]['profile_id'],'offset':0,'length':2}


@pytest.mark.parametrize('method', tuple(COMPLETED))
def test_documented_field_examples_are_independent_valid_output(method):
    validate_field_examples(COMPLETED[method][1])


@pytest.mark.parametrize('method', METHODS)
def test_sd_response_data_examples_are_full_public_rows_and_match_api_example(method):
    from documentation_contract import validate_public_example
    model = MODELS['ads.'+method]
    field = model.model_fields['data']
    assert field.description and field.examples and len(field.examples) == 1
    rows = field.examples[0]
    assert type(rows) is list and len(rows) == 1
    shown = validate_documentation(getattr(AdsAPI, method), model)
    assert rows[0] == shown['data'][0]
    replay = deepcopy(shown)
    replay['data'] = deepcopy(rows)
    replay['response_count'] = 1
    validate_public_example(replay, model)


@pytest.mark.parametrize('name', ('SdCampaign', 'SdCampaigns', 'SdAdGroup', 'SdAdGroups', 'SdProduct',
    'SdProducts', 'SdTarget', 'SdTargets', 'SdNegativeTarget', 'SdNegativeTargets'))
def test_every_sd_declared_field_has_ordered_metadata_and_original_options_after_separator(name):
    source = Path(inspect.getfile(schema)).read_text()
    lines = source.splitlines()
    node = next(n for n in ast.parse(source).body if isinstance(n, ast.ClassDef) and n.name == name)
    for field in node.body:
        if not isinstance(field, ast.AnnAssign):
            continue
        assert isinstance(field.value, ast.Call) and ast.unparse(field.value.func) == 'Field'
        keywords = field.value.keywords
        assert [item.arg for item in keywords[:2]] == ['description', 'examples']
        model_field = getattr(schema, name).model_fields[field.target.id]
        assert ast.literal_eval(keywords[0].value) == model_field.description
        assert ast.literal_eval(keywords[1].value) == model_field.examples
        if len(keywords) > 2:
            assert '# - - - - - - - - - -' in '\n'.join(lines[keywords[1].value.end_lineno:keywords[2].value.lineno-1])
        assert model_field.description and model_field.examples is not None


@pytest.mark.parametrize('method', tuple(COMPLETED))
def test_unknown_fields_are_hard_errors_in_every_completed_sd_model(method):
    prefix,_ = COMPLETED[method]
    _,_,responses=load_collection(Path(__file__).with_name('fixtures')/'ads/basic/sd'/(prefix+'-manifest.json'),'ads.'+method)
    for key in (('future_field',) if method == 'SdCampaigns' else ('tags','lastOverBudgetAt','future_field')):
        raw=deepcopy(responses['account-A-profile-only']);raw['data'][0][key]=[]
        with pytest.raises(ContractError):validate_sd_entity_response(raw,MODELS['ads.'+method])


@pytest.mark.parametrize('label', ('account-A-profile-only', 'account-B-profile-only'))
def test_shared_sd_accounts_keep_same_redacted_identifier_across_all_four_interfaces(label):
    identifiers = set()
    for method in ('SdCampaigns', 'SdAdGroups', 'SdProducts', 'SdTargets'):
        prefix, _ = COMPLETED[method]
        _, records, responses = load_collection(Path(__file__).with_name('fixtures')/'ads/basic/sd'/(prefix+'-manifest.json'), 'ads.'+method)
        profile = records[label]['request']['profile_id']
        assert responses[label]['data'] and all(row['profile_id'] == profile for row in responses[label]['data'])
        identifiers.add(profile)
    assert len(identifiers) == 1
