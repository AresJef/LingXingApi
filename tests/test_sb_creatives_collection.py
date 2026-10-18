"""分页警告只接受精确证据；构造变化只在内存/临时目录，不改真实fixture。"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import shutil
import warnings

import pytest
from pydantic import ValidationError

from sample_collection import load_collection
from sb_creatives_collection import SbCreativePaginationWarning, validate_creative_collection


def current_collection():
    path = Path(__file__).with_name('fixtures')/'ads/basic/sb/sb_creatives-manifest.json'
    return load_collection(path, 'ads.SbCreatives')


@pytest.mark.parametrize('change', ['endpoint', 'schema_extra', 'schema_type', 'code_type', 'parameter',
    'unknown_check', 'identifier_failure', 'unknown_paging_state', 'unapproved_inconclusive',
    'false_equality_claim', 'validation_claim', 'missing_page', 'reference_drift'])
def test_non_paging_errors_and_inconsistent_evidence_remain_hard_failures_without_warning(change):
    manifest, records, responses = current_collection()
    label = next(iter(records))
    if change == 'endpoint':manifest['endpoint'] = 'ads.SbAdGroups'
    elif change == 'schema_extra':responses[label]['unapproved_root'] = True
    elif change == 'schema_type':responses[label]['data'][0]['campaign_id'] = 'invalid-int'
    elif change == 'code_type':responses[label]['code'] = '0'
    elif change == 'parameter':records[label]['request']['length'] = -1
    elif change == 'unknown_check':manifest['checks']['unknown_error'] = {'status': 'failed'}
    elif change == 'identifier_failure':manifest['checks']['identifiers']['status'] = 'failed'
    elif change == 'unknown_paging_state':manifest['checks']['offset_concat']['status'] = 'unknown'
    elif change == 'unapproved_inconclusive':manifest['checks']['token_priority'] = {'status': 'inconclusive', 'complete_data_equal': True}
    elif change == 'false_equality_claim':
        manifest['checks']['offset_concat']['complete_data_equal'] = not manifest['checks']['offset_concat']['complete_data_equal']
    elif change == 'validation_claim':
        manifest['validation']['pagination'] = 'proved' if manifest['validation']['pagination'] == 'accepted_upstream_limit' else 'accepted_upstream_limit'
    elif change == 'missing_page':del responses[manifest['relationships']['token_control']]
    else:responses[manifest['relationships']['end_reference']]['data'][0]['name'] = 'constructed-reference-change'
    with warnings.catch_warnings(record=True) as emitted:
        warnings.simplefilter('always')
        with pytest.raises((AssertionError, ValidationError, TypeError)):
            validate_creative_collection(manifest, records, responses)
    assert not [item for item in emitted if issubclass(item.category, SbCreativePaginationWarning)]


def test_fixture_byte_tampering_fails_before_any_pagination_warning(tmp_path):
    source = Path(__file__).with_name('fixtures')/'ads/basic/sb/sb_creatives-manifest.json'
    manifest, _, _ = current_collection()
    shutil.copyfile(source, tmp_path/source.name)
    for record in manifest['samples']:shutil.copyfile(source.parent/record['fixture'], tmp_path/record['fixture'])
    changed = tmp_path/manifest['samples'][0]['fixture']
    changed.write_bytes(changed.read_bytes()+b'\n')
    with warnings.catch_warnings(record=True) as emitted:
        warnings.simplefilter('always')
        with pytest.raises(AssertionError):
            validate_creative_collection(*load_collection(tmp_path/source.name, 'ads.SbCreatives'))
    assert not [item for item in emitted if issubclass(item.category, SbCreativePaginationWarning)]


def test_historical_observed_failed_format_warns_only_when_complete_data_and_real_reference_support_it():
    manifest, records, responses = current_collection()
    rel = manifest['relationships']
    reference = responses[rel['reference']]['data']
    reference[0]['name'] = 'constructed-unit-reference-0'
    reference[2]['name'] = 'constructed-unit-reference-2'
    responses[rel['end_reference']]['data'] = deepcopy(reference)
    for key in ('offset_concat', 'token_concat', 'token_priority'):
        manifest['checks'][key] = {'status': 'inconclusive', 'observed_status': 'failed', 'complete_data_equal': False}
    manifest['checks']['baseline_stability'] = {'status': 'inconclusive', 'complete_data_equal': False}
    manifest['validation']['pagination'] = 'accepted_upstream_limit'
    manifest['limitations'].append('构造测试的已确认分页限制；不冒充真实采集。')
    before = deepcopy((manifest, records, responses))
    with pytest.warns(SbCreativePaginationWarning, match='重复或遗漏') as emitted:
        validate_creative_collection(manifest, records, responses)
    assert len(emitted) == 1 and (manifest, records, responses) == before
