"""SP报告的精确已批准契约；小时null字段和外层多重集不推广到日报。"""
from collections import Counter
import json

from lingxingapi.ads import schema
from response_contract import validate_response

HOURLY_MODELS = tuple(getattr(schema,name) for name in (
    'SpCampaignHourData','SpPlacementHourData','SpAdGroupHourData',
    'SpProductHourData','SpKeywordHourData','SpTargetHourData'))


def validate_sp_report_response(raw, model):
    view = {key:value for key,value in raw.items() if key!='next_token'} if (
        model in HOURLY_MODELS and type(raw) is dict and 'next_token' in raw and raw['next_token'] is None) else raw
    return validate_response(view,model)


def same_hour_rows(left,right):
    """仅小时复读：完整行（含内部列表顺序）及出现次数一致，原列表不改。"""
    canonical=lambda value:json.dumps(value,sort_keys=True,ensure_ascii=True,allow_nan=False)
    return Counter(map(canonical,left))==Counter(map(canonical,right))
