"""已验证Ads账号规则的公开调用回归；既有真实响应离线重放，不发送网络请求。"""
from __future__ import annotations

import asyncio
from copy import deepcopy
import inspect
from pathlib import Path
from typing import get_type_hints
from unittest.mock import AsyncMock

import pytest
from pydantic import ValidationError

from lingxingapi import API, errors
from lingxingapi.ads import route, schema
from lingxingapi.ads.api import AdsAPI
from sample_collection import load_collection


CASES = {
    'Portfolios': ('common/portfolios', route.PORTFOLIOS, {}),
    'SpCampaigns': ('sp/sp_campaigns', route.SP_CAMPAIGNS, {}),
    'SpAdGroups': ('sp/sp_ad_groups', route.SP_AD_GROUPS, {}),
    'SpProducts': ('sp/sp_products', route.SP_PRODUCTS, {}),
    'SpKeywords': ('sp/sp_keywords', route.SP_KEYWORDS, {}),
    'SpTargets': ('sp/sp_targets', route.SP_TARGETS, {}),
    'SpNegativeKeywords': ('sp/sp_negative_keywords', route.SP_NEGATIVE_TARGETING, {'target_type': 'keyword'}),
    'SpNegativeTargets': ('sp/sp_negative_targets', route.SP_NEGATIVE_TARGETING, {'target_type': 'target'}),
    'SbCampaigns': ('sb/sb_campaigns', route.SB_CAMPAIGNS, {}),
    'SbAdGroups': ('sb/sb_ad_groups', route.SB_AD_GROUPS, {}),
    'SbCreatives': ('sb/sb_creatives', route.SB_CREATIVES, {}),
    'SbKeywords': ('sb/sb_keywords', route.SB_TARGETING, {'ads_type': 'ALL', 'targeting_type': 'keyword'}),
    'SbTargets': ('sb/sb_targets', route.SB_TARGETING, {'ads_type': 'ALL', 'targeting_type': 'producttarget'}),
    'SbNegativeKeywords': ('sb/sb_negative_keywords', route.SB_NEGATIVE_KEYWORDS, {}),
    'SbNegativeTargets': ('sb/sb_negative_targets', route.SB_NEGATIVE_TARGETS, {}),
    'SdAdGroups': ('sd/sd_ad_groups', route.SD_AD_GROUPS, {}),
    'SdCampaigns': ('sd/sd_campaigns', route.SD_CAMPAIGNS, {}),
    'SdProducts': ('sd/sd_products', route.SD_PRODUCTS, {}),
    'SdTargets': ('sd/sd_targets', route.SD_TARGETS, {}),
    'SdNegativeTargets': ('sd/sd_negative_targets', route.SD_NEGATIVE_TARGETS, {}),
}
IDENTIFIER_SCENES = ('account-A-sid-only', 'account-A-profile-only', 'account-A-both',
                     'account-B-profile-only', 'account-A-sid-B-profile', 'account-B-sid-A-profile')


@pytest.fixture(scope='module')
def datasets():
    folder = Path(__file__).with_name('fixtures') / 'ads/basic'
    loaded = {}
    for method, (prefix, _, _) in CASES.items():
        manifest, records, responses = load_collection(folder / (prefix + '-manifest.json'), 'ads.' + method)
        assert manifest['checks']['identifiers']['status'] == 'proved'
        assert manifest['checks']['cross_identifier_priority']['status'] == 'proved'
        loaded[method] = records, responses
    return loaded


@pytest.fixture
def client():
    # 只使用构造值初始化实际公开客户端；传输在每项测试中替换，不读开发凭据。
    return API('0' * 16, 'offline-public-identifiers-only')


def request_arguments(method, body):
    """从冻结请求提取公开参数，分支选择仍由SDK方法完成。"""
    arguments = deepcopy(body)
    for key, value in CASES[method][2].items():
        assert arguments.pop(key) == value
    if method in ('SbKeywords', 'SbTargets'):
        arguments['ad_type'] = body['ads_type']
    return arguments


def assert_request(signed, method, body):
    expected = {'body': body, 'headers': {'X-API-VERSION': '2'}}
    signed.assert_awaited_once_with('POST', CASES[method][1], **expected)


@pytest.mark.parametrize('method', CASES)
@pytest.mark.parametrize('scene', IDENTIFIER_SCENES)
def test_public_client_replays_sid_profile_and_matching_or_mismatched_identifiers(client, monkeypatch, datasets, method, scene):
    records, responses = datasets[method]
    expected_body = records[scene]['request']
    raw = deepcopy(responses[scene]);before = deepcopy(raw)
    signed = AsyncMock(return_value=raw)
    monkeypatch.setattr(client.ads, '_request_with_sign', signed)

    async def invoke():
        return await getattr(client.ads, method)(**request_arguments(method, expected_body))

    result = asyncio.run(invoke())  # 同步调用者与协程内await使用同一个公开入口。
    assert_request(signed, method, expected_body)
    account = 'B' if scene in ('account-B-profile-only', 'account-A-sid-B-profile') else 'A'
    profile = records[f'account-{account}-profile-only']['request']['profile_id']
    assert type(result) is getattr(schema, method) and result.data
    assert all(row.profile_id == profile for row in result.data)
    assert raw == before


@pytest.mark.parametrize('method', CASES)
@pytest.mark.parametrize('identifiers', [{}, {'sid': None}, {'profile_id': None}, {'sid': None, 'profile_id': None}])
def test_public_client_missing_identifiers_use_existing_parameter_validation_without_transport(client, monkeypatch, method, identifiers):
    signed = AsyncMock()
    monkeypatch.setattr(client.ads, '_request_with_sign', signed)
    with pytest.raises(errors.InvalidParametersError) as caught:
        asyncio.run(getattr(client.ads, method)(**identifiers))
    assert isinstance(caught.value.__cause__, ValidationError)
    assert 'sid 和 profile_id 至少提供一个' in str(caught.value.__cause__)
    signed.assert_not_awaited()


@pytest.mark.parametrize('method', CASES)
@pytest.mark.parametrize('positional', [(1, 2), (1, None), (None, 2)])
def test_public_client_preserves_legacy_identifier_positions(client, monkeypatch, method, positional):
    signed = AsyncMock(return_value={'code': 0, 'message': 'success', 'error_details': [],
                                    'request_id': 'constructed-unit-only', 'response_time': '2001-05-07 00:00:00',
                                    'data': [], 'total': 0, 'next_token': None})
    monkeypatch.setattr(client.ads, '_request_with_sign', signed)
    result = asyncio.run(getattr(client.ads, method)(*positional))
    expected = {key: value for key, value in zip(('sid', 'profile_id'), positional) if value is not None}
    assert_request(signed, method, expected | CASES[method][2])
    assert type(result) is getattr(schema, method)


@pytest.mark.parametrize('method', CASES)
def test_public_client_profile_only_preserves_zero_pagination_aliases_and_omits_none(client, monkeypatch, method):
    signed = AsyncMock(return_value={'code': 0, 'message': 'success', 'error_details': [],
                                    'request_id': 'constructed-unit-only', 'response_time': '2001-05-07 00:00:00',
                                    'data': [], 'total': 0, 'next_token': None})
    monkeypatch.setattr(client.ads, '_request_with_sign', signed)
    kwargs = {'profile_id': '2', 'next_token': ' cursor ', 'offset': 0, 'length': 0}
    expected = {'profile_id': 2, 'next_token': 'cursor', 'offset': 0, 'length': 0} | CASES[method][2]
    if method in ('SpNegativeKeywords', 'SpNegativeTargets'):
        kwargs['campaign_id'] = 0;expected['campaign_id'] = 0
    elif method in ('SbKeywords', 'SbTargets'):
        kwargs['ad_type'] = ' SBV ';expected['ads_type'] = 'SBV'
    elif method != 'SbCreatives':
        kwargs['state'] = ' enabled ';expected['state'] = 'enabled'
    asyncio.run(getattr(client.ads, method)(**kwargs))
    assert_request(signed, method, expected)
    assert 'sid' not in expected and 'ad_type' not in expected


@pytest.mark.parametrize('method', CASES)
def test_public_identifier_signature_defaults_types_and_positions_are_consistent(method):
    function = getattr(AdsAPI, method)
    parameters = inspect.signature(function).parameters
    assert list(parameters)[1:3] == ['sid', 'profile_id']
    for name in ('sid', 'profile_id'):
        assert parameters[name].default is None
        assert parameters[name].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
        assert get_type_hints(function)[name] == int | None
    assert inspect.iscoroutinefunction(function)


@pytest.mark.parametrize('method', ['SbKeywords', 'SbTargets'])
def test_sb_targeting_third_positional_ad_type_is_unchanged(client, monkeypatch, method):
    signed = AsyncMock(return_value={'code': 0, 'message': 'success', 'error_details': [],
                                    'request_id': 'constructed-unit-only', 'response_time': '2001-05-07 00:00:00',
                                    'data': [], 'total': 0, 'next_token': None})
    monkeypatch.setattr(client.ads, '_request_with_sign', signed)
    asyncio.run(getattr(client.ads, method)(1, 2, ' SBV '))
    assert_request(signed, method, {'sid': 1, 'profile_id': 2, **CASES[method][2], 'ads_type': 'SBV'})


def test_public_ads_property_returns_the_async_implementation_without_another_request_wrapper(client):
    assert type(client.ads) is AdsAPI and client.ads._state is client._state
    assert not [name for name, value in vars(AdsAPI).items()
                if not name.startswith('_') and inspect.isfunction(value) and not inspect.iscoroutinefunction(value)]
