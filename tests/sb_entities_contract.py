"""SB 严格契约；仅在用户批准的接口与路径移除检查视图中的字段。"""
from __future__ import annotations

from copy import deepcopy
from pydantic import ValidationError
from lingxingapi.ads import schema
from response_contract import ContractError, contract_issues, parsed_value_issues, validate_response, _schema_error_issues

MODELS = {"ads." + name: getattr(schema, name) for name in (
    "SbCampaigns", "SbAdGroups", "SbCreatives", "SbKeywords", "SbTargets", "SbNegativeKeywords", "SbNegativeTargets")}
IGNORED_ROW_FIELDS = {
    # 用户明确忽略活动creative/landing_page；对应内容由SbCreative提供，不以空值为条件。
    schema.SbCampaigns: ("creative", "landing_page", "tags"),
    schema.SbKeywords: ("target_id", "expression", "target_bid", "target_state", "resolved_expression"),
    schema.SbTargets: ("keyword_id", "keyword_text", "keyword_bid", "keyword_state", "match_type"),
    schema.SbCreatives: ("creative_id",),  # 已作废的原字段；公开creative_id仍读取ad_creative_id。
}
CREATIVE_DEFAULT_FIELDS = {
    "asins": "asins",
    "asinExclusions": "asin_excluded", "consentToTranslate": "consent_to_translate",
    "brandName": "brand_name", "brandLogoAssetID": "brand_logo_asset_id", "brandLogoUrl": "brand_logo_url",
    "headline": "headline", "headlines": "headlines", "originalHeadline": "headline_original",
    "originalHeadlines": "headlines_original", "customImageAssetId": "custom_image_asset_id",
    "customImageUrl": "custom_image_url", "customImages": "custom_images",
    "creativePropertiesToOptimize": "optimize_properties", "videoAssetIds": "video_asset_ids",
    "originalVideoAssetIds": "video_original_asset_ids", "collectionType": "collection_type",
    "subpages": "subpages", "title": "title",
}


def validate_creatives(raw):
    """直接解析原检查视图；精确豁免获准的缺键/空元素覆盖，不填充或改写原文。"""
    try:
        parsed = schema.SbCreatives.model_validate(deepcopy(raw))
        dumped = parsed.model_dump(mode="json", by_alias=True, warnings="error")
    except ValidationError as exc:
        raise ContractError("difference", _schema_error_issues(exc, schema.SbCreatives)) from None
    except Exception as exc:
        raise ContractError("difference", [f"SB创意解析或序列化失败：{type(exc).__name__}"]) from None
    if type(raw) is not dict or type(raw.get("code")) is not int or raw["code"] != 0:
        raise ContractError("difference", ["SB创意不是成功业务响应"])
    allowed = set()

    def empty_list(value, input_path, output_path):
        if type(value) is list and not value:
            for path in (input_path, output_path):
                allowed.add(path + ": 覆盖不足，空列表无法观察元素结构")

    for index, row in enumerate(raw.get("data", [])):
        if type(row) is not dict:
            continue
        prefix = f"$.data[{index}]"
        empty_list(row.get("asin"), prefix + ".asin", prefix + ".asins")
        if type(landing_page := row.get("landing_page")) is dict and "url" not in landing_page:
            field = schema.SbCreativeLandingPage.model_fields["page_url"]
            if field.is_required() or field.default is not None or parsed.data[index].landing_page.page_url is not None:
                raise ContractError("difference", [prefix + ".landing_page.url: 已批准的SDK默认值不符"])
            allowed.add(prefix + ".landing_page.url: 模型字段在样本中缺失")
        if type(config := row.get("creative")) is dict:
            for wire, name in CREATIVE_DEFAULT_FIELDS.items():
                if wire not in config:
                    field = schema.SbCreativeConfig.model_fields[name]
                    expected = False if name == "consent_to_translate" else None
                    actual = getattr(parsed.data[index].creative_config, name)
                    if field.is_required() or field.default is not expected or actual is not expected:
                        raise ContractError("difference", [prefix + ".creative." + wire + ": 已批准的SDK默认值不符"])
                    allowed.add(prefix + ".creative." + wire + ": 模型字段在样本中缺失")
                    if name in {"custom_images", "subpages"}:
                        allowed.add(prefix + ".creative_config." + name + ": 覆盖不足，null 无法观察嵌套模型字段")
            for wire, name in (("customImages", "custom_images"), ("creativePropertiesToOptimize", "optimize_properties"), ("asins", "asins")):
                empty_list(config.get(wire), prefix + ".creative." + wire, prefix + ".creative_config." + name)
        videos = row.get("video_creatives")
        if videos is None and "video_creatives" in row:
            allowed.add(prefix + ".video_creatives: JSON 类型应为 array，实际 NoneType")
            empty_list([], prefix + ".video_creatives", prefix + ".video_creatives")
        else:
            empty_list(videos, prefix + ".video_creatives", prefix + ".video_creatives")
    issues = contract_issues(raw, schema.SbCreatives) + parsed_value_issues(raw, parsed)
    issues += contract_issues(dumped, schema.SbCreatives, direction="output") + parsed_value_issues(dumped, parsed, direction="output")
    issues = sorted(set(issues) - allowed)
    if issues:
        raise ContractError("coverage" if all("覆盖不足" in item for item in issues) else "difference", issues)
    return parsed


def checking_view(raw, model):
    """完整raw/pass不变；获准字段的所有值都忽略，其他结构仍交给严格契约。"""
    view = deepcopy(raw)
    if type(view) is not dict or type(view.get("data")) is not list:
        return view
    for row in view["data"]:
        if type(row) is not dict:
            continue
        for key in IGNORED_ROW_FIELDS.get(model, ()):
            row.pop(key, None)
        if model is schema.SbCreatives and type(creative := row.get("creative")) is dict:
            creative.pop("brandLogoCrop", None)
            creative.pop("customImageCrop", None)
            if type(images := creative.get("customImages")) is list:
                for image in images:
                    if type(image) is dict:
                        image.pop("crop", None)
    return view


def validate_sb_entity_response(raw, model, *, scenario: str | None = None):
    if model not in MODELS.values():
        raise ContractError("input_error", ["未登记的 SB Schema"])
    raw = checking_view(raw, model)
    if model is schema.SbCreatives and scenario != "empty_expected":
        return validate_creatives(raw)
    if scenario != "empty_expected":
        return validate_response(raw, model)
    if not (type(raw) is dict and type(raw.get("code")) is int and raw["code"] == 0
            and type(raw.get("data")) is list and raw["data"] == []):
        raise ContractError("difference", ["SB 显式空结果场景不符"])
    try:
        parsed = model.model_validate(deepcopy(raw))
        dumped = parsed.model_dump(mode="json", by_alias=True, warnings="error")
    except ValidationError:
        raise ContractError("difference", ["SB 空结果不满足原 Schema 类型/约束；未显示输入"]) from None
    except Exception as exc:
        raise ContractError("difference", [f"SB 空结果解析或序列化失败：{type(exc).__name__}"]) from None
    issues = contract_issues(raw, model) + parsed_value_issues(raw, parsed)
    issues += contract_issues(dumped, model, direction="output") + parsed_value_issues(dumped, parsed, direction="output")
    issues = [issue for issue in issues if issue != "$.data: 覆盖不足，空列表无法观察元素结构"]
    if issues:
        raise ContractError("difference", sorted(set(issues)))
    if parsed.response_count != 0 or parsed.data != [] or parsed.errors:
        raise ContractError("difference", ["SB 空结果的数量/错误明细不符"])
    return parsed
