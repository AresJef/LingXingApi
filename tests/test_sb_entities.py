"""SB 参数、SDK组装、真实脱敏数据与独立文档；全部离线。"""
from __future__ import annotations

import asyncio
import ast
from copy import deepcopy
import inspect
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from pydantic import ValidationError

from lingxingapi import errors
from lingxingapi.ads import param, route, schema
from lingxingapi.ads.api import AdsAPI
from sb_entities_contract import MODELS, validate_sb_entity_response
from response_contract import ContractError
from documentation_contract import documentation_example, validate_documentation, validate_field_examples

METHODS = tuple(endpoint.split('.')[1] for endpoint in MODELS)
STATE_METHODS = ('SbCampaigns', 'SbAdGroups', 'SbNegativeKeywords', 'SbNegativeTargets')
TARGET_METHODS = ('SbKeywords', 'SbTargets')
ROUTES = dict(zip(METHODS, (route.SB_CAMPAIGNS, route.SB_AD_GROUPS, route.SB_CREATIVES,
    route.SB_TARGETING, route.SB_TARGETING, route.SB_NEGATIVE_KEYWORDS, route.SB_NEGATIVE_TARGETS), strict=True))
COMPLETED = {'SbCampaigns': ('sb_campaigns', schema.SbCampaign),
             'SbAdGroups': ('sb_ad_groups', schema.SbAdGroup),
             'SbKeywords': ('sb_keywords', schema.SbKeyword),
             'SbTargets': ('sb_targets', schema.SbTarget),
             'SbNegativeKeywords': ('sb_negative_keywords', schema.SbNegativeKeyword),
             'SbNegativeTargets': ('sb_negative_targets', schema.SbNegativeTarget)}


def empty_response():
    return {'code': 0, 'message': 'success', 'error_details': [], 'request_id': 'synthetic-only',
            'response_time': '2001-05-07 00:00:00', 'total': 0, 'next_token': None, 'data': []}


@pytest.mark.parametrize('method', METHODS)
@pytest.mark.parametrize('ids,expected', [({'sid': 1, 'profile_id': None}, {'sid': 1}),
    ({'sid': None, 'profile_id': '2'}, {'profile_id': 2}), ({'sid': 0, 'profile_id': 2}, {'sid': 0, 'profile_id': 2})])
def test_each_sdk_route_body_aliases_optional_omission_and_version(method, ids, expected):
    signed = AsyncMock(return_value=empty_response())
    args = {**ids, 'next_token': ' cursor ', 'offset': '2', 'length': 0}
    body = {**expected, 'next_token': 'cursor', 'offset': 2, 'length': 0}
    if method in STATE_METHODS:
        args['state'] = ' enabled '
        body['state'] = 'enabled'
    if method in TARGET_METHODS:
        args['ad_type'] = ' SBV '
        body.update(ads_type='SBV', targeting_type='keyword' if method == 'SbKeywords' else 'producttarget')
    parsed = asyncio.run(getattr(AdsAPI, method)(SimpleNamespace(_request_with_sign=signed), **args))
    signed.assert_awaited_once_with('POST', ROUTES[method], body=body, headers={'X-API-VERSION': '2'})
    assert type(parsed) is MODELS['ads.' + method] and parsed.data == []


@pytest.mark.parametrize('method', METHODS)
def test_sdk_default_body_and_missing_identifiers_fail_before_transport(method):
    signed = AsyncMock(return_value=empty_response())
    asyncio.run(getattr(AdsAPI, method)(SimpleNamespace(_request_with_sign=signed), None, 2))
    expected = {'profile_id': 2}
    if method in TARGET_METHODS:
        expected.update(ads_type='ALL', targeting_type='keyword' if method == 'SbKeywords' else 'producttarget')
    assert signed.await_args.kwargs['body'] == expected
    signed.reset_mock()
    with pytest.raises(errors.InvalidParametersError):
        asyncio.run(getattr(AdsAPI, method)(SimpleNamespace(_request_with_sign=signed), None, None))
    signed.assert_not_awaited()


@pytest.mark.parametrize('method', METHODS)
@pytest.mark.parametrize('patch', [{'sid': -1}, {'profile_id': 'bad'}, {'offset': -1}, {'length': 1.5}, {'next_token': ' '}])
def test_invalid_params_do_not_send_any_request(method, patch):
    signed = AsyncMock()
    with pytest.raises(errors.InvalidParametersError):
        asyncio.run(getattr(AdsAPI, method)(SimpleNamespace(_request_with_sign=signed), **{'sid': None, 'profile_id': 2, **patch}))
    signed.assert_not_awaited()


@pytest.mark.parametrize('method', METHODS)
@pytest.mark.parametrize('unexpected', ['campaign_id', 'ad_group_id', 'target_type'])
def test_unexposed_filters_are_not_silently_added(method, unexpected):
    signed = AsyncMock()
    with pytest.raises(TypeError):
        asyncio.run(getattr(AdsAPI, method)(SimpleNamespace(_request_with_sign=signed), None, 2, **{unexpected: 3}))
    signed.assert_not_awaited()


@pytest.mark.parametrize('method', ('SbCreatives', *TARGET_METHODS))
def test_only_methods_supporting_state_expose_it(method):
    signed = AsyncMock()
    with pytest.raises(TypeError):
        asyncio.run(getattr(AdsAPI, method)(SimpleNamespace(_request_with_sign=signed), None, 2, state='enabled'))
    signed.assert_not_awaited()


@pytest.mark.parametrize('key', ['ad_type', 'ads_type'])
@pytest.mark.parametrize('value', ['SB', 'SBV', 'ALL', 'future-type'])
def test_sb_targeting_aliases_keep_nonempty_string_rule_without_new_enums(key, value):
    raw = {'profile_id': 2, key: ' ' + value + ' ', 'target_type': 'product'}
    before = deepcopy(raw)
    assert param.SbTargeting.model_validate_params(raw) == {'profile_id': 2, 'ads_type': value, 'targeting_type': 'producttarget'}
    assert raw == before


@pytest.mark.parametrize('raw,expected', [('product', 'producttarget'), (' product ', 'product'), ('keyword', 'keyword'), ('ALL', 'ALL')])
def test_target_type_before_validator_keeps_existing_exact_conversion_order(raw, expected):
    assert param.SbTargeting.model_validate_params({'sid': 0, 'ads_type': 'ALL', 'targeting_type': raw}) == {
        'sid': 0, 'ads_type': 'ALL', 'targeting_type': expected}


@pytest.mark.parametrize('value', [None, 1, False, [], {}, ' ', ''])
def test_sb_before_validator_accepts_arbitrary_input_for_field_validation_then_rejects_invalid(value):
    assert param.SbTargeting._validate_target_type(value) is value
    with pytest.raises(ValidationError):
        param.SbTargeting.model_validate_params({'sid': 1, 'ad_type': 'ALL', 'target_type': value})


@pytest.mark.parametrize('method', METHODS)
def test_explicit_empty_result_checks_every_outer_field_and_count(method):
    model = MODELS['ads.' + method]
    assert validate_sb_entity_response(empty_response(), model, scenario='empty_expected').response_count == 0
    with pytest.raises(ContractError):
        validate_sb_entity_response(empty_response(), model)
    for patch in ({'unexpected': []}, {'code': False}, {'data': None}, {'error_details': ['bad']}, {'response_count': 1}):
        with pytest.raises(ContractError):
            validate_sb_entity_response(empty_response() | patch, model, scenario='empty_expected')
    for key in ('request_id', 'response_time', 'total', 'next_token', 'message', 'error_details'):
        raw = empty_response();del raw[key]
        with pytest.raises(ContractError):
            validate_sb_entity_response(raw, model, scenario='empty_expected')


@pytest.mark.parametrize('method', tuple(COMPLETED))
def test_real_completed_collections_preserve_rows_paging_and_state_relationships(method):
    from sample_collection import load_collection, same_data
    prefix, _ = COMPLETED[method]
    path = Path(__file__).with_name('fixtures') / 'ads/basic/sb' / (prefix + '-manifest.json')
    manifest, records, responses = load_collection(path, 'ads.' + method)
    count = 24 if method == 'SbNegativeTargets' else 13 if method in TARGET_METHODS else 14
    assert manifest['planned_requests'] == len(records) == count and manifest['not_run'] == []
    for label, raw in responses.items():
        before = deepcopy(raw)
        parsed = validate_sb_entity_response(raw, MODELS['ads.' + method], scenario=records[label]['scenario'])
        assert raw == before and parsed.response_count == len(raw['data']) and parsed.total_count == raw['total']
    assert same_data(responses['account-A-profile-only']['data'], responses['account-A-sid-only']['data'])
    assert same_data(responses['account-A-profile-only']['data'], responses['account-A-both']['data'])
    assert same_data(responses['account-A-sid-B-profile']['data'], responses['account-B-profile-only']['data'])
    assert same_data(responses['account-B-sid-A-profile']['data'], responses['account-A-profile-only']['data'])
    if method in STATE_METHODS:
        for state in ('enabled', 'paused', 'archived'):
            assert all(row['state'] == state for row in responses['state-' + state]['data'])
    else:
        for ad_type in ('SB', 'SBV'):
            assert all(row['ads_type'] == ad_type for row in responses['ad-type-' + ad_type]['data'])
    rel = manifest['relationships'];reference = responses[rel['reference']]['data']
    for mode in ('offset', 'token'):
        assert same_data([row for label in rel[mode + '_pages'] for row in responses[label]['data']], reference)
    assert same_data(responses[rel['token_control']]['data'], responses[rel['token_conflict']]['data'])
    assert same_data(reference, responses[rel['end_reference']]['data'])
    if method == 'SbNegativeTargets':
        first_b = responses['account-B-profile-only']['data']
        assert same_data(first_b, responses['account-B-sid-only']['data'])
        assert same_data(first_b, responses['account-B-both']['data'])
        for state in ('enabled', 'paused', 'archived'):
            assert all(row['state'] == state for row in responses['account-B-state-' + state]['data'])
        rel_b = rel['account_B'];reference_b = responses[rel_b['reference']]['data']
        for mode in ('offset', 'token'):
            assert same_data([row for label in rel_b[mode + '_pages'] for row in responses[label]['data']], reference_b)
        assert same_data(responses[rel_b['token_control']]['data'], responses[rel_b['token_conflict']]['data'])
        assert same_data(reference_b, responses[rel_b['end_reference']]['data'])


@pytest.mark.parametrize('method', tuple(COMPLETED))
def test_static_sb_docs_have_their_own_output_contract_independent_of_current_fixtures(method):
    _, row_model = COMPLETED[method]
    validate_field_examples(row_model)
    function = getattr(AdsAPI, method)
    doc = inspect.getdoc(function)
    assert doc.index('## Docs') < doc.index('Args:') < doc.index('Returns:') < doc.index('Examples:')
    assert all(word not in doc for word in ('本次', '实测', '采集', '样本'))
    call, _ = documentation_example(function)
    args = {item.arg: ast.literal_eval(item.value) for item in call.keywords}
    shown = validate_documentation(function, MODELS['ads.' + method])
    assert args == {'profile_id': shown['data'][0]['profile_id'], 'offset': 0, 'length': 2}


def test_campaign_time_supplement_preserves_nonempty_strings_and_nulls():
    path = Path(__file__).with_name('fixtures') / 'ads/basic/sb/sb_campaigns-last-over-budget-at.json'
    wrapper = json.loads(path.read_bytes())
    assert wrapper['source'] == 'local_raw' and wrapper['endpoint'] == 'ads.SbCampaigns'
    raw = wrapper['response'];before = deepcopy(raw)
    parsed = validate_sb_entity_response(raw, schema.SbCampaigns)
    values = [r.last_over_budget_at for r in parsed.data if r.last_over_budget_at]
    assert raw == before and parsed.response_count == 40 and len(values) == 6
    assert all(r.last_over_budget_at == source['lastOverBudgetAt'] for r, source in zip(parsed.data, raw['data'], strict=True))
