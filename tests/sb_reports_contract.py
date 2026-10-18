"""SB报告已批准的精确检查视图；原始响应与通用检查器保持不变。"""
from copy import deepcopy

from lingxingapi.ads import schema
from response_contract import validate_response

HOURLY_MODELS = tuple(getattr(schema, name) for name in (
    "SbCampaignHourData", "SbPlacementHourData", "SbAdGroupHourData", "SbTargetingHourData"))
MODELS = {"ads." + model.__name__: model for model in (*HOURLY_MODELS, schema.SbTargetQueryReports)}


def validate_sb_report_response(raw, model):
    """仅忽略目标搜索词行country和四小时顶层严格null的next_token。"""
    view = raw
    if model is schema.SbTargetQueryReports and type(raw) is dict:
        view = deepcopy(raw)
        if type(view.get("data")) is list:
            for row in view["data"]:
                if type(row) is dict:
                    row.pop("country", None)
    if model in HOURLY_MODELS and type(raw) is dict and "next_token" in raw and raw["next_token"] is None:
        view = {key: value for key, value in raw.items() if key != "next_token"}
    return validate_response(view, model)
