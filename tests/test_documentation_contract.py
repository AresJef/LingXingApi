"""文档独立于可覆盖fixture；合成变化只在内存测试，不写真实来源文件。"""
from __future__ import annotations

import ast
from copy import deepcopy
import json
from pathlib import Path
from typing import Any, get_type_hints

import pytest

from lingxingapi.basic.api import BasicAPI
from lingxingapi.ads.api import AdsAPI
from lingxingapi.ads import schema as ads_schema
from lingxingapi.basic import schema
from documentation_contract import documentation_example, validate_documentation, validate_public_example
import test_sp_campaigns

BASIC_METHODS = ('Marketplaces', 'States', 'Sellers', 'ConceptSellers', 'Accounts', 'ExchangeRates', 'RenameSellers', 'EditExchangeRate')
ADS_METHODS = ('AdProfiles', 'Portfolios', 'SpCampaigns', 'SpAdGroups', 'SpProducts', 'SpKeywords', 'SpTargets', 'SpNegativeKeywords', 'SpNegativeTargets', 'SbCampaigns', 'SbAdGroups', 'SbCreatives', 'SbKeywords', 'SbTargets', 'SbNegativeKeywords', 'SbNegativeTargets', 'SdCampaigns', 'SdAdGroups', 'SdProducts', 'SdTargets', 'SdNegativeTargets', 'AdsOperationLogs')
METHODS = [*(getattr(BasicAPI, name) for name in BASIC_METHODS), *(getattr(AdsAPI, name) for name in ADS_METHODS)]


@pytest.mark.parametrize('method', METHODS, ids=lambda method: method.__name__)
def test_completed_response_data_metadata_and_single_element_example_match_public_docs(method):
    from lingxingapi.base.schema import ResponseResult

    model = get_type_hints(method)['return']
    shown = validate_documentation(method, model)
    if method is BasicAPI.EditExchangeRate:
        assert model is ResponseResult and model.model_fields['data'].annotation is Any
        assert model.model_fields['data'].default is None and shown['data'] is None
        return  # 共享base不改；成功/失败均无集合，不补造列表。
    field = model.model_fields['data']
    assert field.description and '\n' not in field.description
    assert field.examples is not None and len(field.examples) == 1

    def concrete(value):
        if type(value) is dict:
            return {key: concrete(item) for key, item in value.items()}
        if type(value) is list:
            return [concrete(item) for item in value if item is not Ellipsis]
        return value

    expected = concrete(shown['data'])
    if type(expected) is list:
        expected = expected[:1]
    assert field.examples[0] == expected
    replay = deepcopy(shown)
    replay['data'] = deepcopy(expected)
    if 'response_count' in replay:
        replay['response_count'] = len(expected) if type(expected) is list else 1
    validate_public_example(replay, model)


@pytest.mark.parametrize('method', ('SpCampaigns', 'SbCampaigns', 'SdCampaigns'))
def test_campaign_budget_time_docs_share_confirmed_sp_description_and_nonempty_example(method):
    description = "时间字符串，格式为 YYYY-MM-DD HH:MM:SS，可为 None [原字段 'lastOverBudgetAt']"
    example = '2026-10-12 22:17:35'
    model = getattr(ads_schema, method[:-1])
    field = model.model_fields['last_over_budget_at']
    assert field.description == description
    assert field.examples == [example]
    function = getattr(AdsAPI, method)
    assert '# '+description in function.__doc__
    shown = validate_documentation(function, getattr(ads_schema, method))
    assert shown['data'][0]['last_over_budget_at'] == example


@pytest.mark.parametrize('method', METHODS, ids=lambda method: method.__name__)
def test_all_connected_documentation_has_valid_call_and_public_output(method):
    shown = validate_documentation(method, get_type_hints(method)['return'])
    call, _ = documentation_example(method)
    arguments = {item.arg: ast.literal_eval(item.value) for item in call.keywords}
    if method is BasicAPI.States:
        assert all(row['country_code'] == arguments['country_code'] for row in shown['data'] if row is not Ellipsis)
    elif method is BasicAPI.ExchangeRates:
        assert all(row['date'][:7] == arguments['date'] for row in shown['data'] if row is not Ellipsis)


@pytest.mark.parametrize('mutation', ['metadata', 'ids', 'record_order'])
def test_legal_fixture_changes_do_not_change_static_documentation_expectations(monkeypatch, mutation: str):
    def forbid_fixture_read(path: Path) -> bytes:
        raise AssertionError('documentation must not read current fixtures')

    datasets = [
        ('basic/sellers.json', BasicAPI.Sellers),
        ('basic/concept_sellers.json', BasicAPI.ConceptSellers),
        ('basic/accounts.json', BasicAPI.Accounts),
        ('basic/exchange_rates.json', BasicAPI.ExchangeRates),
        ('basic/rename_sellers_failure.json', BasicAPI.RenameSellers),
        ('ads/basic/sp/sp_campaigns-account-A-profile-only.json', AdsAPI.SpCampaigns),
        *[(f'ads/basic/sp/{prefix}-account-A-profile-only.json', getattr(AdsAPI, name))
          for name, prefix in [('SpAdGroups', 'sp_ad_groups'), ('SpProducts', 'sp_products'),
              ('SpKeywords', 'sp_keywords'), ('SpTargets', 'sp_targets'),
              ('SpNegativeKeywords', 'sp_negative_keywords'), ('SpNegativeTargets', 'sp_negative_targets')]],
        *[(f'ads/basic/sb/{prefix}-account-A-profile-only.json', getattr(AdsAPI, name))
          for name, prefix in [('SbCampaigns', 'sb_campaigns'), ('SbCreatives', 'sb_creatives'), ('SbKeywords', 'sb_keywords'), ('SbTargets', 'sb_targets')]],
    ]
    for relative, method in datasets:
        wrapper = json.loads((Path(__file__).with_name('fixtures') / relative).read_bytes())
        # Only the unwrapped response is synthesized in memory; it has no source label.
        raw = deepcopy(wrapper['response'])
        model = get_type_hints(method)['return']
        shown_before = validate_documentation(method, model)
        if mutation == 'metadata':
            raw['request_id'] = 'synthetic-documentation-regression'
            raw['response_time'] = '2002-06-08 12:34:56'
        elif mutation == 'record_order' and isinstance(raw.get('data'), list):
            raw['data'].reverse()
        elif mutation == 'ids' and isinstance(raw.get('data'), list):
            for row in raw['data']:
                for key in ('sid', 'profile_id', 'campaign_id', 'ad_group_id'):
                    if key in row and type(row[key]) in {str, int} and str(row[key]).isdecimal():
                        shifted = int(row[key]) + 7
                        row[key] = str(shifted) if type(row[key]) is str else shifted
        # Actual models still parse legal changed data; documentation cannot read fixtures.
        model.model_validate(deepcopy(raw))
        with monkeypatch.context() as guard:
            guard.setattr(Path, 'read_bytes', forbid_fixture_read)
            assert validate_documentation(method, model) == shown_before


@pytest.mark.parametrize('change', ['wrong_type', 'input_alias', 'missing_field', 'extra_field', 'empty_role', 'invalid_count', 'invalid_ellipsis'])
def test_documentation_still_rejects_real_public_output_errors(change: str):
    _, shown = documentation_example(BasicAPI.Accounts)
    shown = deepcopy(shown)
    row = shown['data'][0]
    if change == 'wrong_type':
        row['user_id'] = str(row['user_id'])
    elif change == 'input_alias':
        row['uid'] = row.pop('user_id')
    elif change == 'missing_field':
        del row['user_id']
    elif change == 'extra_field':
        row['unexpected'] = 1
    elif change == 'empty_role':
        row['role'] = ''
    elif change == 'invalid_count':
        shown['response_count'] = 0
    else:
        shown['data'] = [Ellipsis, row]
    with pytest.raises((AssertionError, ValueError, TypeError)):
        validate_public_example(shown, schema.Accounts)


@pytest.mark.parametrize('change', ['parameter_alias', 'parameter_type', 'profile_relationship'])
def test_documented_campaign_call_rejects_wrong_parameters_and_ids(monkeypatch, change: str):
    method = AdsAPI.SpCampaigns
    original = method.__doc__
    _, shown = documentation_example(method)
    profile = shown['data'][0]['profile_id']
    if change == 'parameter_alias':
        altered = original.replace(f'profile_id={profile}', f'profile={profile}', 1)
    elif change == 'parameter_type':
        altered = original.replace(f'profile_id={profile}', 'profile_id="bad"', 1)
    else:
        altered = original.replace(f'profile_id={profile}', f'profile_id={profile + 1}', 1)
    assert altered != original
    monkeypatch.setattr(method, '__doc__', altered)
    with pytest.raises((AssertionError, ValueError, TypeError)):
        test_sp_campaigns.test_sp_campaigns_google_docstring_call_and_output_are_internally_consistent()
