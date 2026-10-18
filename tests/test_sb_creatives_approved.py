"""已批准的SB创意契约；所有构造视频仅在内存测试，不冒充真实采集。"""
from __future__ import annotations

from copy import deepcopy

import pytest
from pydantic import ValidationError

from lingxingapi.ads import schema
from response_contract import ContractError, validate_response
from sb_entities_contract import validate_sb_entity_response
from test_sb_approved_fields import response

DEFAULTS = {
    "asins": ("asins", None),
    'asinExclusions': ('asin_excluded', None), 'consentToTranslate': ('consent_to_translate', False),
    'brandName': ('brand_name', None), 'brandLogoAssetID': ('brand_logo_asset_id', None),
    'brandLogoUrl': ('brand_logo_url', None), 'headline': ('headline', None),
    'headlines': ('headlines', None), 'originalHeadline': ('headline_original', None),
    'originalHeadlines': ('headlines_original', None), 'customImageAssetId': ('custom_image_asset_id', None),
    'customImageUrl': ('custom_image_url', None), 'customImages': ('custom_images', None),
    'creativePropertiesToOptimize': ('optimize_properties', None), 'videoAssetIds': ('video_asset_ids', None),
    'originalVideoAssetIds': ('video_original_asset_ids', None), 'collectionType': ('collection_type', None),
    'subpages': ('subpages', None), 'title': ('title', None),
}


def raw_creative():
    raw = response('SbCreatives')
    raw['data'][0]['video_creatives'] = []
    raw['data'][0]['creative']['customImages'] = [{'assetId': 'synthetic-only', 'url': 'https://example.test/synthetic'}]
    return raw


@pytest.mark.parametrize('wire,definition', tuple(DEFAULTS.items()))
def test_only_approved_missing_config_fields_retain_existing_sdk_defaults(wire, definition):
    raw = raw_creative();del raw['data'][0]['creative'][wire];before = deepcopy(raw)
    parsed = validate_sb_entity_response(raw, schema.SbCreatives)
    name, expected = definition
    actual = getattr(parsed.data[0].creative_config, name)
    assert actual == expected and type(actual) is type(expected) and raw == before
    assert parsed.model_dump()['data'][0]['creative_config'][name] == expected
    with pytest.raises(ContractError):
        validate_response(raw, schema.SbCreatives)  # 通用checker保持原严格覆盖。


def test_missing_default_and_explicit_null_string_behavior_remains_distinct():
    raw = raw_creative();del raw['data'][0]['creative']['brandName']
    assert validate_sb_entity_response(raw, schema.SbCreatives).data[0].creative_config.brand_name is None
    raw['data'][0]['creative']['brandName'] = None
    assert validate_sb_entity_response(raw, schema.SbCreatives).data[0].creative_config.brand_name == ''


@pytest.mark.parametrize('landing_page,expected', [
    ({'pageType': 'STORE'}, None),
    ({'pageType': 'STORE', 'url': None}, ''),
    ({'pageType': 'STORE', 'url': 'https://example.test/store'}, 'https://example.test/store'),
])
def test_exact_landing_url_missing_null_and_value_keep_existing_sdk_semantics(landing_page, expected):
    raw = raw_creative();raw['data'][0]['landing_page'] = landing_page;before = deepcopy(raw)
    parsed = validate_sb_entity_response(raw, schema.SbCreatives)
    sdk = schema.SbCreatives.model_validate(raw)
    assert parsed.data[0].landing_page.page_url == sdk.data[0].landing_page.page_url == expected
    assert raw == before
    field = schema.SbCreativeLandingPage.model_fields['page_url']
    assert not field.is_required() and field.default is None
    if 'url' not in landing_page:
        with pytest.raises(ContractError) as error:validate_response(raw, schema.SbCreatives)
        assert '$.data[0].landing_page.url: 模型字段在样本中缺失' in error.value.issues


@pytest.mark.parametrize('change', ['outer_missing', 'page_type_missing', 'unknown', 'subpage_url_missing', 'bad_url_object', 'bad_url_array', 'bad_url_number', 'bad_url_bool'])
def test_landing_url_missing_exception_does_not_extend_to_other_fields_paths_or_bad_values(change):
    raw = raw_creative();del raw['data'][0]['landing_page']['url']
    if change == 'outer_missing':del raw['data'][0]['landing_page']
    elif change == 'page_type_missing':del raw['data'][0]['landing_page']['pageType']
    elif change == 'unknown':raw['data'][0]['landing_page']['unapproved'] = None
    elif change == 'subpage_url_missing':del raw['data'][0]['creative']['subpages'][0]['url']
    else:raw['data'][0]['landing_page']['url'] = {'bad_url_object': {}, 'bad_url_array': [], 'bad_url_number': 123, 'bad_url_bool': False}[change]
    with pytest.raises(ContractError):validate_sb_entity_response(raw, schema.SbCreatives)


def test_documentation_roundtrip_retains_landing_url_missing_default_without_relaxing_public_structure():
    from documentation_contract import validate_public_example
    shown = schema.SbCreativeLandingPage.model_validate({'pageType': 'STORE'}).model_dump()
    assert shown == {'page_type': 'STORE', 'page_url': None}
    assert validate_public_example(shown, schema.SbCreativeLandingPage) == shown
    del shown['page_type']
    with pytest.raises(AssertionError):validate_public_example(shown, schema.SbCreativeLandingPage)


@pytest.mark.parametrize('wire,public', [('customImages', 'custom_images'), ('creativePropertiesToOptimize', 'optimize_properties'), ('asins', 'asins')])
def test_three_exact_config_arrays_accept_empty_and_keep_empty(wire, public):
    raw = raw_creative();raw['data'][0]['creative'][wire] = [];before = deepcopy(raw)
    assert getattr(validate_sb_entity_response(raw, schema.SbCreatives).data[0].creative_config, public) == []
    assert raw == before
    with pytest.raises(ContractError):validate_response(raw, schema.SbCreatives)


@pytest.mark.parametrize('change', ['required', 'unknown', 'bad_bool', 'bad_image', 'other_empty_array', 'missing_outer'])
def test_creative_exemptions_do_not_weaken_other_required_types_fields_or_paths(change):
    raw = raw_creative();config = raw['data'][0]['creative']
    if change == 'required':del config['type']
    elif change == 'unknown':config['unapproved'] = None
    elif change == 'bad_bool':config['consentToTranslate'] = None
    elif change == 'bad_image':config['customImages'] = [{'assetId': 'synthetic-only'}]
    elif change == 'other_empty_array':config['headlines'] = []
    else:del raw['data'][0]['campaign_id']
    with pytest.raises(ContractError):validate_sb_entity_response(raw, schema.SbCreatives)


@pytest.mark.parametrize('value', [[], None])
def test_video_creatives_required_empty_and_null_to_empty(value):
    raw = raw_creative();raw['data'][0]['video_creatives'] = value;before = deepcopy(raw)
    parsed = validate_sb_entity_response(raw, schema.SbCreatives)
    assert parsed.data[0].video_creatives == [] and raw == before
    field = schema.SbCreative.model_fields['video_creatives'];assert field.is_required()
    del raw['data'][0]['video_creatives']
    with pytest.raises(ValidationError):schema.SbCreatives.model_validate(raw)
    with pytest.raises(ContractError):validate_sb_entity_response(raw, schema.SbCreatives)


@pytest.mark.parametrize('videos', [
    [{'unobserved': {'versions': [None, {}, [], '02', 12, False]}}],
    [{}, [], None, 'constructed-only', 123456789012345678, False, 0.25],
    [{'creative_version': {'untyped': True}, 'videos': None, 'future': ['01', '02']},
     {'creative_version': {'untyped': True}, 'videos': None, 'future': ['01', '02']}],
])
def test_nonempty_video_lists_keep_arbitrary_json_content_types_order_and_duplicates(videos):
    import json
    raw = raw_creative();raw['data'][0]['video_creatives'] = deepcopy(videos);before = deepcopy(raw)
    parsed = validate_sb_entity_response(raw, schema.SbCreatives)
    sdk = schema.SbCreatives.model_validate(raw)
    for result in (parsed, sdk):
        actual = result.model_dump(mode='json')['data'][0]['video_creatives']
        assert json.dumps(actual, sort_keys=True) == json.dumps(videos, sort_keys=True)
    assert raw == before


@pytest.mark.parametrize('value', ['', 'not-a-list', {}, {'videos': []}, 123, False, 0.25])
def test_video_outer_non_list_values_remain_invalid(value):
    raw = raw_creative();raw['data'][0]['video_creatives'] = value
    with pytest.raises(ValidationError):schema.SbCreatives.model_validate(raw)
    with pytest.raises(ContractError):validate_sb_entity_response(raw, schema.SbCreatives)


def test_documentation_roundtrip_keeps_missing_string_defaults_as_none_and_required_types_strict():
    from documentation_contract import validate_public_example
    model = schema.SbCreativeConfig
    shown = model.model_validate({'type': 'VIDEO', 'creativeStatus': 'PUBLISHED', 'creativeVersion': '1', 'asins': ['SYNTHETIC-ONLY']}).model_dump()
    assert validate_public_example(shown, model)['brand_name'] is None
    shown['creative_type'] = None
    with pytest.raises((AssertionError, TypeError, ValueError)):validate_public_example(shown, model)


def test_both_exact_asins_paths_accept_empty_lists_and_keep_nonempty_types_strict():
    raw = raw_creative();raw['data'][0]['asin'] = [];raw['data'][0]['creative']['asins'] = []
    parsed = validate_sb_entity_response(raw, schema.SbCreatives).data[0]
    assert parsed.asins == parsed.creative_config.asins == []
    raw['data'][0]['asin'] = [{'unapproved': 'not an ASIN string'}]
    with pytest.raises(ContractError):validate_sb_entity_response(raw, schema.SbCreatives)


def test_real_primary_creative_collection_keeps_failed_paging_and_has_legal_responses(request):
    from pathlib import Path
    from sample_collection import load_collection
    from sb_creatives_collection import validate_creative_collection
    path = getattr(request.config, '_sb_creatives_manifest',
                   Path(__file__).with_name('fixtures')/'ads/basic/sb/sb_creatives-manifest.json')
    validate_creative_collection(*load_collection(path, 'ads.SbCreatives'))


def test_creative_static_documentation_uses_public_fields_and_retains_pagination_limit():
    import inspect
    from lingxingapi.ads.api import AdsAPI
    from documentation_contract import validate_documentation, validate_field_examples
    for model in (schema.SbCreative, schema.SbCreativeConfig, schema.SbCreativeCustomImage, schema.SbCreativeLandingPage, schema.SbCreativeSubpage):
        validate_field_examples(model)
    doc = inspect.getdoc(AdsAPI.SbCreatives)
    assert all(text in doc for text in ('offset/length', 'next_token', '重复或遗漏', '不保证与单次查询一致', '去重也不能保证恢复完整数据'))
    assert all(text not in doc for text in ('本次', '实测', '样本', '采集'))
    validate_documentation(AdsAPI.SbCreatives, schema.SbCreatives)
    videos = schema.SbCreative.model_fields["video_creatives"].examples[0]
    assert isinstance(videos, list) and len(videos) == 1 and videos[0]
    assert schema.SbCreative.model_fields['video_creatives'].description == '视频创意列表'
    assert '显式null转换为空列表' not in doc and '非空列表内容原样保留' not in doc
    assert all(field.description and field.examples[0] for field in schema.SbCreativeSubpage.model_fields.values())


from pathlib import Path
SUPPLEMENT_FIXTURES = sorted((Path(__file__).with_name('fixtures')/'ads/basic/sb/evidence/sb_creatives').rglob('*.json'))


@pytest.mark.parametrize('path', SUPPLEMENT_FIXTURES, ids=lambda p: str(p.relative_to(Path(__file__).with_name('fixtures'))))
def test_real_verified_creative_supplemental_fixtures_are_independently_valid(path):
    import json
    wrapper = json.loads(path.read_bytes())
    assert wrapper['source'] == 'local_raw' and wrapper['endpoint'] == 'ads.SbCreatives'
    before = deepcopy(wrapper['response']);parsed = validate_sb_entity_response(wrapper['response'], schema.SbCreatives)
    assert wrapper['response'] == before and parsed.response_count == len(before['data'])
    assert all(
        row.video_creatives == ([] if original["video_creatives"] is None else original["video_creatives"])
        for row, original in zip(parsed.data, before["data"], strict=True)
    )


def test_real_subpages_and_incidental_nonempty_evidence_cover_existing_fields():
    import json

    directory = Path(__file__).with_name("fixtures") / "ads/basic/sb/evidence/sb_creatives/subpages-probe"
    videos, excluded, subpages = [
        json.loads((directory / name).read_bytes())["response"]
        for name in ("source-01.json", "source-02.json", "source-03.json")
    ]
    assert videos["data"][77]["video_creatives"]
    assert excluded["data"][57]["creative"]["asinExclusions"]
    row = subpages["data"][148]
    assert "asins" not in row["creative"]
    parsed = validate_sb_entity_response(subpages, schema.SbCreatives)
    assert parsed.data[148].creative_config.asins is None
    assert len(row["creative"]["subpages"]) == 3
    for subpage in row["creative"]["subpages"]:
        assert set(subpage) == {"asin", "pageTitle", "url"}
        assert all(isinstance(value, str) and value for value in subpage.values())
        assert subpage["asin"] in row["asin"]
