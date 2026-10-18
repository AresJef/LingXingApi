"""用户明确批准的SB字段与限定路径忽略；合成输入不作为采集证据。"""
from __future__ import annotations

from copy import deepcopy

import pytest
from pydantic import ValidationError

from lingxingapi.ads import schema
from response_contract import ContractError
from sb_entities_contract import validate_sb_entity_response


def response(method):
    row = {'profile_id': 123456789012345, 'campaign_id': 234567890123456,
           'ad_group_id': 345678901234567}
    if method == 'SbCampaigns':
        row.pop('ad_group_id')
        row.update(portfolio_id=None, name='Synthetic campaign', creative_type='COLLECTION', budget=5.0,
                   budget_type='daily', lastOverBudgetAt=None, bid_multiplier=None, bid_optimization=0,
                   start_date=None, end_date=None, state='enabled', serving_status='running')
    elif method == 'SbKeywords':
        row.update(ads_type='SB', targeting_type='keyword', keyword_id=456789012345678,
                   keyword_text='Synthetic keyword', match_type='exact', keyword_bid=1.0, keyword_state='enabled')
    elif method == 'SbTargets':
        row.update(ads_type='SB', targeting_type='producttarget', target_id=567890123456789,
                   expression='[{"type":"asinSameAs","value":"B000000001"}]',
                   resolved_expression='[{"type":"asinSameAs","value":"B000000001"}]', target_bid=1.0, target_state='enabled')
    else:
        creative = {field.validation_alias or name: field.default for name, field in schema.SbCreativeConfig.model_fields.items()
                    if not field.is_required()}
        creative.update(type='PRODUCT_COLLECTION', creativeStatus='PUBLISHED', creativeVersion='1')
        creative['subpages'] = [{'asin': None, 'pageTitle': None, 'url': 'https://example.test/page'}]
        row.update(ad_creative_id=678901234567890, name='Synthetic creative', creative_type='PRODUCT_COLLECTION',
                   creative=creative, landing_page={'pageType': 'STORE', 'url': 'https://example.test/store'}, asin=None, state='enabled', serving_status='AD_STATUS_LIVE',
                   creation_date=1, last_updated_date=2, video_creatives=[])
    return {'code': 0, 'message': 'success', 'error_details': [], 'request_id': 'synthetic-only',
            'response_time': '2001-05-07 00:00:00', 'total': 1, 'next_token': None, 'data': [row]}


IGNORED = {
    # 活动两字段已明确忽略，对应内容从SbCreative读取；tags沿用已有批准。
    'SbCampaigns': ('creative', 'landing_page', 'tags'),
    'SbKeywords': ('target_id', 'expression', 'target_bid', 'target_state', 'resolved_expression'),
    'SbTargets': ('keyword_id', 'keyword_text', 'keyword_bid', 'keyword_state', 'match_type'),
}


@pytest.mark.parametrize('method,fields', tuple(IGNORED.items()))
@pytest.mark.parametrize('value', [None, '', 0, False, 'nonempty', ['nonempty'], {'future': 'nonempty'}])
def test_approved_row_fields_are_ignored_without_a_null_only_constraint(method, fields, value):
    """包括活动creative/landing_page的明确忽略；非空值仍通过，原文仍完整。"""
    raw = response(method)
    raw['data'][0].update({field: deepcopy(value) for field in fields})
    before = deepcopy(raw)
    parsed = validate_sb_entity_response(raw, getattr(schema, method))
    assert raw == before and parsed.response_count == 1
    assert all(field not in parsed.data[0].model_dump() for field in fields)


@pytest.mark.parametrize('method', tuple(IGNORED))
@pytest.mark.parametrize('where', ['root', 'other_row_field'])
def test_ignore_rules_do_not_hide_other_paths_or_unlisted_fields(method, where):
    raw = response(method)
    if where == 'root':
        raw[next(iter(IGNORED[method]))] = {'unexpected': True}
    else:
        raw['data'][0]['unapproved'] = None
    with pytest.raises(ContractError):
        validate_sb_entity_response(raw, getattr(schema, method))


@pytest.mark.parametrize('value', [None, '', '2026-10-03 01:06:43', ' opaque time '])
def test_last_over_budget_at_is_required_and_preserves_exact_string_or_null(value):
    raw = response('SbCampaigns');raw['data'][0]['lastOverBudgetAt'] = value
    parsed = validate_sb_entity_response(raw, schema.SbCampaigns).data[0]
    assert parsed.last_over_budget_at == value and type(parsed.last_over_budget_at) is type(value)
    assert parsed.model_dump()['last_over_budget_at'] == value
    assert schema.SbCampaign.model_fields['last_over_budget_at'].is_required()
    assert schema.SbCampaign.model_fields['last_over_budget_at'].validation_alias == 'lastOverBudgetAt'
    del raw['data'][0]['lastOverBudgetAt']
    with pytest.raises(ValidationError):
        schema.SbCampaigns.model_validate(raw)


@pytest.mark.parametrize('value', [0, False, 1.5, [], {}])
def test_new_time_field_does_not_accept_non_string_values(value):
    raw = response('SbCampaigns');raw['data'][0]['lastOverBudgetAt'] = value
    with pytest.raises(ValidationError):
        schema.SbCampaigns.model_validate(raw)


def test_creative_type_is_required_without_new_enum_and_has_semantic_field_order():
    raw = response('SbCampaigns');raw['data'][0]['creative_type'] = 'FUTURE_TYPE'
    assert validate_sb_entity_response(raw, schema.SbCampaigns).data[0].creative_type == 'FUTURE_TYPE'
    fields = list(schema.SbCampaign.model_fields)
    assert fields.index('campaign_name') < fields.index('creative_type') < fields.index('budget')
    assert fields.index('budget_type') < fields.index('last_over_budget_at') < fields.index('bid_multiplier')
    del raw['data'][0]['creative_type']
    with pytest.raises(ValidationError):
        schema.SbCampaigns.model_validate(raw)


@pytest.mark.parametrize('value', [None, {}, {'unknown': 'nonempty'}, [1], 'opaque'])
def test_creative_crop_and_deprecated_wire_id_are_ignored_at_only_the_approved_paths(value):
    raw = response('SbCreatives');row = raw['data'][0]
    row['creative_id'] = deepcopy(value)
    row['creative'].update(brandLogoCrop=deepcopy(value), customImageCrop=deepcopy(value),
        customImages=[{'assetId': 'synthetic-asset', 'url': 'https://example.test/a.jpg', 'crop': deepcopy(value)}])
    before = deepcopy(raw)
    parsed = validate_sb_entity_response(raw, schema.SbCreatives)
    assert raw == before and parsed.data[0].creative_id == row['ad_creative_id']
    for location in ('row', 'creative', 'image'):
        bad = deepcopy(raw)
        target = bad['data'][0] if location == 'row' else bad['data'][0]['creative'] if location == 'creative' else bad['data'][0]['creative']['customImages'][0]
        target['unapproved'] = None
        with pytest.raises(ContractError):
            validate_sb_entity_response(bad, schema.SbCreatives)


def test_approved_crops_keep_video_list_and_required_configuration_strict():
    raw = response('SbCreatives');raw['data'][0]['creative']['customImages'] = []
    validate_sb_entity_response(raw, schema.SbCreatives)
    raw['data'][0]['video_creatives'] = {'unapproved': 'not a list'}
    with pytest.raises(ContractError):
        validate_sb_entity_response(raw, schema.SbCreatives)
    raw = response('SbCreatives');del raw['data'][0]['creative']['creativeStatus']
    with pytest.raises(ContractError):
        validate_sb_entity_response(raw, schema.SbCreatives)
