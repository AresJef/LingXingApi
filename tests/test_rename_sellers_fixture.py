"""RenameSellers（返回成功）与 RenameSellers（返回失败）的真实 fixture 契约。"""
from pathlib import Path

from lingxingapi.basic.api import BasicAPI
from lingxingapi.basic import schema

from response_contract import load_json_bytes, validate_rename_sellers_fixture
from documentation_contract import validate_documentation, validate_field_examples

FIXTURES = Path(__file__).with_name('fixtures') / 'basic'


def test_RenameSellers_返回成功() -> None:
    parsed = validate_rename_sellers_fixture(FIXTURES / 'rename_sellers_success.json', scenario='success')
    assert parsed.data.success == 1 and parsed.data.failure == 0


def test_RenameSellers_返回失败() -> None:
    path = FIXTURES / 'rename_sellers_failure.json'
    parsed = validate_rename_sellers_fixture(path, scenario='failure')
    wire = load_json_bytes(path.read_bytes())['response']['data']
    assert parsed.data.success == 0 and parsed.data.failure == 1
    assert len(parsed.data.failure_detail) == 1 and parsed.data.failure_detail[0].sid == 0
    assert type(wire['failure_detail'][0]['sid']) is str and wire['failure_detail'][0]['sid'] == '0'


def test_rename_documentation_preserves_failure_details_and_consistent_counts():
    shown = validate_documentation(BasicAPI.RenameSellers, schema.RenameSellersResult)
    assert shown['data']['failure'] == len(shown['data']['failure_detail']) == 1
    assert shown['data']['success'] == 0
    assert validate_field_examples(schema.RenameSellers)['failure_detail'] == shown['data']['failure_detail']
    # 独立字段取真实失败计数；成功场景的真实0仍由上面的fixture契约保留。
    assert schema.RenameSellers.model_fields['failure'].examples == [1]
