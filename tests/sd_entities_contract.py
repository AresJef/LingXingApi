"""SD基础数据严格契约；仅明确空结果豁免根data的元素覆盖。"""
from __future__ import annotations

from copy import deepcopy
from pydantic import ValidationError
from lingxingapi.ads import schema
from response_contract import ContractError, contract_issues, parsed_value_issues, validate_response

MODELS = {'ads.' + name: getattr(schema, name) for name in (
    'SdCampaigns', 'SdAdGroups', 'SdProducts', 'SdTargets', 'SdNegativeTargets')}


def validate_sd_entity_response(raw, model, *, scenario: str | None = None):
    """核对原文、解析值及默认序列化结果，不静默丢弃未知字段。"""
    if model not in MODELS.values():
        raise ContractError('input_error', ['未登记的SD基础Schema'])
    if model is schema.SdCampaigns and type(raw) is dict and type(raw.get('data')) is list:
        raw = deepcopy(raw)
        for row in raw['data']:
            if type(row) is dict:
                row.pop('tags', None)  # 仅获准的活动检查视图；raw/pass完整原文不变。
    if scenario != 'empty_expected':
        return validate_response(raw, model)
    if not (type(raw) is dict and type(raw.get('code')) is int and raw['code'] == 0
            and type(raw.get('data')) is list and raw['data'] == []):
        raise ContractError('difference', ['SD显式空结果场景不符'])
    try:
        parsed = model.model_validate(deepcopy(raw))
        dumped = parsed.model_dump(mode='json', by_alias=True, warnings='error')
    except ValidationError:
        raise ContractError('difference', ['SD空结果不满足Schema类型或约束']) from None
    issues = contract_issues(raw, model) + parsed_value_issues(raw, parsed)
    issues += contract_issues(dumped, model, direction='output') + parsed_value_issues(dumped, parsed, direction='output')
    issues = [issue for issue in issues if issue != '$.data: 覆盖不足，空列表无法观察元素结构']
    if issues or parsed.response_count != 0 or parsed.data != [] or parsed.errors:
        raise ContractError('difference', sorted(set(issues)) or ['SD空结果数量或错误明细不符'])
    return parsed
