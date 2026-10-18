"""SbCreatives发布集合契约；只将已确认且证据相符的分页失败报告为警告。"""
from __future__ import annotations

import inspect
import warnings

from lingxingapi.ads import param, schema
from lingxingapi.ads.api import AdsAPI
from sample_collection import same_data
from sb_entities_contract import validate_sb_entity_response


class SbCreativePaginationWarning(UserWarning):
    """仅SbCreatives已确认的上游分页异常；不代替其他契约错误。"""


def validate_creative_collection(manifest, records, responses):
    """核对本轮完整数据与清单状态；通过不报警，其他错误保持硬失败。"""
    assert manifest['endpoint'] == 'ads.SbCreatives'
    assert len(records) == manifest['planned_requests'] == 11 and manifest['not_run'] == []
    assert records.keys() == responses.keys()
    checks = manifest['checks']
    paging = ('offset_concat', 'token_concat', 'token_priority')
    assert set(checks) == {'identifiers', 'cross_identifier_priority', 'baseline_stability', *paging}
    for record in records.values():
        inspect.signature(AdsAPI.SbCreatives).bind(None, **record['request'])
        normalized = param.AdEntities.model_validate_params(record['request'])
        assert same_data([normalized], [record['request']]), '请求字段不符合已有参数序列化契约'
    for raw in responses.values():
        parsed = validate_sb_entity_response(raw, schema.SbCreatives)
        assert parsed.response_count == len(raw['data'])
        assert same_data([row.video_creatives for row in parsed.data],
                         [[] if row['video_creatives'] is None else row['video_creatives'] for row in raw['data']])

    rel = manifest['relationships']
    reference, end = rel['reference'], rel['end_reference']
    assert records[reference]['request'] == records[end]['request']
    assert records[reference]['next_token_from'] is records[end]['next_token_from'] is None
    assert same_data(responses[reference]['data'], responses[end]['data']), '同参数参考复读发生变化'
    assert responses[reference]['total'] == responses[end]['total'], '同参数参考总数发生变化'
    reference_rows = responses[reference]['data']
    assert len(reference_rows) == 4
    equal = {}
    for kind in ('offset', 'token'):
        pages = rel[kind+'_pages']
        assert len(pages) == 2 and all(len(responses[label]['data']) == 2 for label in pages)
        combined = [row for label in pages for row in responses[label]['data']]
        equal[kind+'_concat'] = same_data(combined, reference_rows)
    source, control, conflict = rel['token_source'], rel['token_control'], rel['token_conflict']
    assert rel['token_pages'] == [source, control]
    assert records[control]['next_token_from'] == records[conflict]['next_token_from'] == source
    assert len(responses[control]['data']) == len(responses[conflict]['data']) == 2
    equal['token_priority'] = (same_data(responses[control]['data'], responses[conflict]['data'])
                               and same_data(responses[control]['data'], reference_rows[2:4]))

    failures = []
    for name in paging:
        check = checks[name]
        status = check['status']
        if status == 'inconclusive':
            assert check.get('observed_status') == 'failed' and check.get('complete_data_equal') is False, '未获准的分页无法判定状态'
            status = 'failed'  # 仅解释历史记录；不改写清单或原始证据。
        assert status in {'proved', 'failed'}, '未知分页状态'
        assert check.get('complete_data_equal') is equal[name], '分页清单与完整数据不符'
        assert status == ('proved' if equal[name] else 'failed'), '分页状态与本轮证据不符'
        if name == 'token_priority' and equal[name]:
            assert not same_data(reference_rows[:2], reference_rows[2:4]), '分页区间无法区分，不能证明游标优先级'
        if status == 'failed':failures.append(name)
    for name in ('identifiers', 'cross_identifier_priority'):
        assert checks[name]['status'] in {'proved', 'observed'}, '非分页检查未通过'
    baseline = checks['baseline_stability']['status']
    assert baseline == 'proved' or baseline == 'inconclusive' and failures, '参考稳定性未通过'
    expected_validation = {'schema': 'passed', 'redaction': 'passed',
                           'pagination': 'accepted_upstream_limit' if failures else 'proved',
                           'real_nonempty_video_observed': any(row.get('video_creatives') for raw in responses.values() for row in raw['data'])}
    assert same_data([manifest['validation']], [expected_validation]), '发布验收标记与本轮结果不符'
    assert isinstance(manifest['limitations'], list) and all(isinstance(item, str) for item in manifest['limitations'])
    if failures:
        assert any('分页' in item for item in manifest['limitations']), '缺少已接受分页限制说明'
        warnings.warn('ads.SbCreatives：已确认上游分页异常（'+', '.join(failures)+'）；分页可能重复或遗漏。'
                      '原失败checks及完整响应保留，本次通过不表示分页一致性通过；其他接口及非分页错误仍硬失败。',
                      SbCreativePaginationWarning, stacklevel=2)
