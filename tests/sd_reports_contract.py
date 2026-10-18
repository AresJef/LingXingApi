"""SD 报告已批准的精确核验视图；SDK 和完整原文保持。"""
from __future__ import annotations

from lingxingapi.ads import schema
from response_contract import validate_response

HOURLY_MODELS = (schema.SdCampaignHourData, schema.SdAdGroupHourData,
                 schema.SdProductHourData, schema.SdTargetHourData)
MODELS = {"ads." + model.__name__: model for model in HOURLY_MODELS}


def validate_sd_report_response(raw, model):
    """仅四个精确小时模型的顶层 next_token=null 允许从检查副本移除。"""
    view = raw
    if model in HOURLY_MODELS and type(raw) is dict and "next_token" in raw and raw["next_token"] is None:
        view = {key: value for key, value in raw.items() if key != "next_token"}
    return validate_response(view, model)
