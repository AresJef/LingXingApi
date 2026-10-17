# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field, field_validator
from lingxingapi.base.schema import ResponseV1, ResponseV1Token
from lingxingapi.fields import IntOrNone2Zero, FloatOrNone2Zero, StrOrNone2Blank


# 基础数据 ----------------------------------------------------------------------------------------------------------------------
# . Ads Profiles
class AdProfile(BaseModel):
    """广告帐号"""

    sid: IntOrNone2Zero = Field(
        description="领星店铺ID",
        examples=[10105],
    )
    seller_name: str = Field(
        description="领星店铺名称 [原字段 'name']",
        examples=["广告账号名"],
        # - - - - - - - - - -
        validation_alias="name",
    )
    country_code: str = Field(
        description="店铺国家代码",
        examples=["NL"],
    )
    currency_code: str = Field(
        description="店铺货币代码",
        examples=["EUR"],
    )
    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000001],
    )
    profile_type: str = Field(
        description="广告帐号类型 [原字段 'type']",
        examples=["seller"],
        # - - - - - - - - - -
        validation_alias="type",
    )
    profile_status: int = Field(
        description="广告帐号状态 [原字段 'status'] (-1: 删除, 0: 停用, 1: 正常, 2: 异常)",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="status",
    )


class AdProfiles(ResponseV1):
    """广告帐号列表"""

    data: list[AdProfile] = Field(
        description="广告帐号列表",
        examples=[
            [
                {
                    "sid": 10105,
                    "seller_name": "广告账号名",
                    "country_code": "NL",
                    "currency_code": "EUR",
                    "profile_id": 90000000000001,
                    "profile_type": "seller",
                    "profile_status": 1,
                },
            ],
        ],
    )


# . Portfolios
class Portfolio(BaseModel):
    """广告组合"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000003],
    )
    portfolio_id: int = Field(
        description="广告组合ID",
        examples=[800000000004],
    )
    portfolio_name: str = Field(
        description="广告组合名称 [原字段 'name']",
        examples=["A000000AAA-000 0A0A 组"],
        # - - - - - - - - - -
        validation_alias="name",
    )
    budget: StrOrNone2Blank = Field(
        description="广告预算 (JSON 字符串)",
        examples=[
            '{"amount": 1.0, "policy": "dateRange", "startDate": "20260313", "currencyCode": "GBP"}'
        ],
    )
    in_budget: int = Field(
        description="当前是否在预算范围内 (0: 超出预算, 1: 在预算内)",
        examples=[0],
    )
    state: StrOrNone2Blank = Field(
        description="广告状态",
        examples=["enabled"],
    )
    status: StrOrNone2Blank = Field(
        description="服务状态 [原字段 'serving_status']",
        examples=["PORTFOLIO_OUT_OF_BUDGET"],
        # - - - - - - - - - -
        validation_alias="serving_status",
    )
    create_time_ts: IntOrNone2Zero = Field(
        description="创建时间 (UTC毫秒时间戳) [原字段 'creation_date']",
        examples=[1755676941815],
        # - - - - - - - - - -
        validation_alias="creation_date",
    )
    update_time_ts: IntOrNone2Zero = Field(
        description="更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']",
        examples=[1773498441693],
        # - - - - - - - - - -
        validation_alias="last_updated_date",
    )


class Portfolios(ResponseV1Token):
    """广告组合列表"""

    data: list[Portfolio] = Field(
        description="广告组合列表",
        examples=[
            [
                {
                    "profile_id": 90000000000003,
                    "portfolio_id": 800000000004,
                    "portfolio_name": "A000000AAA-000 0A0A 组",
                    "budget": '{"amount": 1.0, "policy": "dateRange", "startDate": "20260313", "currencyCode": "GBP"}',
                    "in_budget": 0,
                    "state": "enabled",
                    "status": "PORTFOLIO_OUT_OF_BUDGET",
                    "create_time_ts": 1755676941815,
                    "update_time_ts": 1773498441693,
                },
            ],
        ],
    )


# 基础数据 - Sponsored Products - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# . SP Campaigns
class SpCampaign(BaseModel):
    """SP 广告活动"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000004],
    )
    portfolio_id: IntOrNone2Zero = Field(
        description="广告组合ID",
        examples=[800000000000006],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000058],
    )
    campaign_name: str = Field(
        description="广告活动名称 [原字段 'name']",
        examples=["AA-000-AA-广告-示示-0.00aaa  06.7"],
        # - - - - - - - - - -
        validation_alias="name",
    )
    campaign_type: StrOrNone2Blank = Field(
        description="广告活动类型",
        examples=["sponsoredProducts"],
    )
    targeting_type: str = Field(
        description="投放类型",
        examples=["manual"],
    )
    premium_bid_adjustment: int = Field(
        description="溢价报价调整 (0: 不调整, 1: 调整)",
        examples=[1],
    )
    daily_budget: float = Field(
        description="每日预算",
        examples=[5.0],
    )
    last_over_budget_at: str | None = Field(
        description="时间字符串，格式为 YYYY-MM-DD HH:MM:SS，可为 None [原字段 'lastOverBudgetAt']",
        examples=["2026-10-12 22:17:35"],
        # - - - - - - - - - -
        validation_alias="lastOverBudgetAt",
    )
    bidding: StrOrNone2Blank = Field(
        description="竞价策略 (JSON 字符串)",
        examples=[
            '{"strategy": "manual", "adjustments": [{"predicate": "placementRestOfSearch", "percentage": 50}, {"predicate": "placementTop", "percentage": 80}]}'
        ],
    )
    start_time: StrOrNone2Blank = Field(
        description="开始时间 [原字段 'start_date']",
        examples=["2025-06-14 00:00:00"],
        # - - - - - - - - - -
        validation_alias="start_date",
    )
    end_time: StrOrNone2Blank = Field(
        description="结束时间 [原字段 'end_date']",
        examples=[""],
        # - - - - - - - - - -
        default=None,
        validation_alias="end_date",
    )
    state: StrOrNone2Blank = Field(
        description="广告状态",
        examples=["enabled"],
    )
    status: StrOrNone2Blank = Field(
        description="服务状态 [原字段 'serving_status']",
        examples=["CAMPAIGN_STATUS_ENABLED"],
        # - - - - - - - - - -
        validation_alias="serving_status",
    )
    create_time_ts: IntOrNone2Zero = Field(
        description="创建时间 (UTC毫秒时间戳) [原字段 'creation_date']",
        examples=[1749892734147],
        # - - - - - - - - - -
        validation_alias="creation_date",
    )
    update_time_ts: IntOrNone2Zero = Field(
        description="更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']",
        examples=[1791884107102],
        # - - - - - - - - - -
        validation_alias="last_updated_date",
    )


class SpCampaigns(ResponseV1Token):
    """SP 广告活动列表"""

    data: list[SpCampaign] = Field(
        description="SP 广告活动列表",
        examples=[
            [
                {
                    "profile_id": 90000000000003,
                    "portfolio_id": 80000000000012,
                    "campaign_id": 70000000000010,
                    "campaign_name": "AA-000AAA-AAAI",
                    "campaign_type": "sponsoredProducts",
                    "targeting_type": "manual",
                    "premium_bid_adjustment": 0,
                    "daily_budget": 6.0,
                    "last_over_budget_at": "2026-10-12 22:17:35",
                    "bidding": '{"strategy": "manual", "adjustments": [{"predicate": "placementRestOfSearch", "percentage": 50}, {"predicate": "placementTop", "percentage": 80}]}',
                    "start_time": "2019-11-05 00:00:00",
                    "end_time": "",
                    "state": "enabled",
                    "status": "CAMPAIGN_STATUS_ENABLED",
                    "create_time_ts": 1572927171000,
                    "update_time_ts": 1791674172950,
                },
            ],
        ],
    )


# . SP Ad Groups
class SpAdGroup(BaseModel):
    """SP 广告组"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000004],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000128],
    )
    ad_group_id: int = Field(
        description="广告组ID",
        examples=[600000000066],
    )
    ad_group_name: str = Field(
        description="广告组名称 [原字段 'name']",
        examples=["AA 000 000广告组广合"],
        # - - - - - - - - - -
        validation_alias="name",
    )
    default_bid: float = Field(
        description="默认竞价",
        examples=[1.13],
    )
    state: StrOrNone2Blank = Field(
        description="广告组状态",
        examples=["enabled"],
    )
    status: StrOrNone2Blank = Field(
        description="服务状态 [原字段 'serving_status']",
        examples=["CAMPAIGN_PAUSED"],
        # - - - - - - - - - -
        validation_alias="serving_status",
    )
    create_time_ts: IntOrNone2Zero = Field(
        description="创建时间 (UTC毫秒时间戳) [原字段 'creation_date']",
        examples=[1667273890695],
        # - - - - - - - - - -
        validation_alias="creation_date",
    )
    update_time_ts: IntOrNone2Zero = Field(
        description="更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']",
        examples=[1667273890695],
        # - - - - - - - - - -
        validation_alias="last_updated_date",
    )


class SpAdGroups(ResponseV1Token):
    """SP 广告组列表"""

    data: list[SpAdGroup] = Field(
        description="SP 广告组列表",
        examples=[
            [
                {
                    "profile_id": 90000000000004,
                    "campaign_id": 700000000000128,
                    "ad_group_id": 600000000066,
                    "ad_group_name": "AA 000 000广告组广合",
                    "default_bid": 1.13,
                    "state": "enabled",
                    "status": "CAMPAIGN_PAUSED",
                    "create_time_ts": 1667273890695,
                    "update_time_ts": 1667273890695,
                },
            ],
        ],
    )


# . SP Ads
class SpProductVideoDetail(BaseModel):
    """SP 商品广告视频详情"""

    asset_id: str = Field(
        description="视频素材ID",
        examples=["amzn1.assetlibrary.asset1.a0000000aa0a0aa0a0aa00000000a0ac"],
    )
    asset_version: str = Field(
        description="广告指定的视频素材版本",
        examples=["version_v2"],
    )
    headline: str = Field(
        description="视频标题",
        examples=["Aaa Aaaaaab"],
    )
    description: str = Field(
        description="视频描述",
        examples=["Aaaaaaa aaa aaaaaa aa aaaaa aaaaaaa aac."],
    )
    name: StrOrNone2Blank = Field(
        description="本地视频素材名称，未匹配素材时为空字符串",
        examples=[""],
    )
    url: StrOrNone2Blank = Field(
        description="本地视频素材地址，未匹配素材时为空字符串",
        examples=[""],
    )


class SpProduct(BaseModel):
    """SP 广告商品"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000004],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[7000000000264],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000026],
    )
    ad_id: int = Field(
        description="商品广告ID",
        examples=[50000000002],
    )
    asin: StrOrNone2Blank = Field(
        description="商品ASIN",
        examples=["A00A0AAAA4"],
    )
    msku: str = Field(
        description="亚马逊SKU [原字段 'sku']",
        examples=["000aaAA 000CY"],
        # - - - - - - - - - -
        validation_alias="sku",
    )
    video_details: list[SpProductVideoDetail] = Field(
        description="商品广告视频详情",
        examples=[
            [
                {
                    "asset_id": "amzn1.assetlibrary.asset1.a0000000aa0a0aa0a0aa00000000a0ac",
                    "asset_version": "version_v2",
                    "headline": "Aaa Aaaaaab",
                    "description": "Aaaaaaa aaa aaaaaa aa aaaaa aaaaaaa aac.",
                    "name": "",
                    "url": "",
                }
            ]
        ],
    )
    state: StrOrNone2Blank = Field(
        description="广告状态",
        examples=["enabled"],
    )
    status: StrOrNone2Blank = Field(
        description="服务状态 [原字段 'serving_status']",
        examples=["CAMPAIGN_PAUSED"],
        # - - - - - - - - - -
        validation_alias="serving_status",
    )
    create_time_ts: IntOrNone2Zero = Field(
        description="创建时间 (UTC毫秒时间戳) [原字段 'creation_date']",
        examples=[1599466635000],
        # - - - - - - - - - -
        validation_alias="creation_date",
    )
    update_time_ts: IntOrNone2Zero = Field(
        description="更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']",
        examples=[1599466635000],
        # - - - - - - - - - -
        validation_alias="last_updated_date",
    )


class SpProducts(ResponseV1Token):
    """SP 广告商品列表"""

    data: list[SpProduct] = Field(
        description="SP 广告商品列表",
        examples=[
            [
                {
                    "profile_id": 90000000000004,
                    "campaign_id": 7000000000264,
                    "ad_group_id": 600000000000026,
                    "ad_id": 50000000002,
                    "asin": "A00A0AAAA4",
                    "msku": "000aaAA 000CY",
                    "video_details": [
                        {
                            "asset_id": "amzn1.assetlibrary.asset1.a0000000aa0a0aa0a0aa00000000a0ac",
                            "asset_version": "version_v2",
                            "headline": "Aaa Aaaaaab",
                            "description": "Aaaaaaa aaa aaaaaa aa aaaaa aaaaaaa aac.",
                            "name": "",
                            "url": "",
                        },
                    ],
                    "state": "enabled",
                    "status": "CAMPAIGN_PAUSED",
                    "create_time_ts": 1599466635000,
                    "update_time_ts": 1599466635000,
                },
            ],
        ],
    )


# . SP Keywords
class SpKeyword(BaseModel):
    """SP 关键词投放投放"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000004],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000097],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[60000000000058],
    )
    keyword_id: int = Field(
        description="关键词ID",
        examples=[4000000008],
    )
    keyword_text: StrOrNone2Blank = Field(
        description="关键词文本",
        examples=["aaaa 0000 aaf"],
    )
    match_type: StrOrNone2Blank = Field(
        description="关键词匹配类型",
        examples=["phrase"],
    )
    bid: FloatOrNone2Zero = Field(
        description="竞价",
        examples=[0.5],
    )
    state: StrOrNone2Blank = Field(
        description="广告状态",
        examples=["enabled"],
    )
    status: StrOrNone2Blank = Field(
        description="服务状态 [原字段 'serving_status']",
        examples=["CAMPAIGN_PAUSED"],
        # - - - - - - - - - -
        validation_alias="serving_status",
    )
    create_time_ts: IntOrNone2Zero = Field(
        description="创建时间 (UTC毫秒时间戳) [原字段 'creation_date']",
        examples=[1583837811000],
        # - - - - - - - - - -
        validation_alias="creation_date",
    )
    update_time_ts: IntOrNone2Zero = Field(
        description="更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']",
        examples=[1583837811000],
        # - - - - - - - - - -
        validation_alias="last_updated_date",
    )


class SpKeywords(ResponseV1Token):
    """SP 手动关键词投放列表"""

    data: list[SpKeyword] = Field(
        description="SP 手动关键词投放列表",
        examples=[
            [
                {
                    "profile_id": 90000000000004,
                    "campaign_id": 700000000000097,
                    "ad_group_id": 60000000000058,
                    "keyword_id": 4000000008,
                    "keyword_text": "aaaa 0000 aaf",
                    "match_type": "phrase",
                    "bid": 0.5,
                    "state": "enabled",
                    "status": "CAMPAIGN_PAUSED",
                    "create_time_ts": 1583837811000,
                    "update_time_ts": 1583837811000,
                },
            ],
        ],
    )


# . SP Targets
class SpTarget(BaseModel):
    """SP 自动投放/手动商品投放"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000004],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000111],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[60000000000255],
    )
    target_id: int = Field(
        description="自动投放/手动商品投放ID",
        examples=[300000000003],
    )
    expression_type: str = Field(
        description="自动/手动投放类型",
        examples=["auto"],
    )
    expression: StrOrNone2Blank = Field(
        description="自动投放/手动商品投放表达式 (JSON 字符串)",
        examples=['[{"type": "queryHighRelMatches"}]'],
    )
    expression_resolved: StrOrNone2Blank = Field(
        description="自动投放/手动商品投放表达式表达式解析 (JSON 字符串) [原字段 'resolved_expression']",
        examples=['[{"type": "queryHighRelMatches"}]'],
        # - - - - - - - - - -
        validation_alias="resolved_expression",
    )
    bid: FloatOrNone2Zero = Field(
        description="竞价",
        examples=[0.45],
    )
    state: StrOrNone2Blank = Field(
        description="广告状态",
        examples=["enabled"],
    )
    status: StrOrNone2Blank = Field(
        description="服务状态 [原字段 'serving_status']",
        examples=["CAMPAIGN_PAUSED"],
        # - - - - - - - - - -
        validation_alias="serving_status",
    )
    create_time_ts: IntOrNone2Zero = Field(
        description="创建时间 (UTC毫秒时间戳) [原字段 'creation_date']",
        examples=[1590133144000],
        # - - - - - - - - - -
        validation_alias="creation_date",
    )
    update_time_ts: IntOrNone2Zero = Field(
        description="更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']",
        examples=[1599470603000],
        # - - - - - - - - - -
        validation_alias="last_updated_date",
    )


class SpTargets(ResponseV1Token):
    """SP 自动投放/手动商品投放列表"""

    data: list[SpTarget] = Field(
        description="SP 自动投放/手动商品投放列表",
        examples=[
            [
                {
                    "profile_id": 90000000000004,
                    "campaign_id": 700000000000111,
                    "ad_group_id": 60000000000255,
                    "target_id": 300000000003,
                    "expression_type": "auto",
                    "expression": '[{"type": "queryHighRelMatches"}]',
                    "expression_resolved": '[{"type": "queryHighRelMatches"}]',
                    "bid": 0.45,
                    "state": "enabled",
                    "status": "CAMPAIGN_PAUSED",
                    "create_time_ts": 1590133144000,
                    "update_time_ts": 1599470603000,
                },
            ],
        ],
    )


# . Sp Negative Keywords
class SpNegativeKeyword(BaseModel):
    """SP 否定手动关键词投放"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000004],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[70000000000079],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[0],
    )
    negative_keyword_id: int = Field(
        description="否定关键词ID [原字段 'target_id']",
        examples=[400000000000001],
        # - - - - - - - - - -
        validation_alias="target_id",
    )
    negative_keyword_text: str = Field(
        description="否定关键词文本 [原字段 'negative_text']",
        examples=["aa 0000  aag"],
        # - - - - - - - - - -
        validation_alias="negative_text",
    )
    negative_keyword_match_type: str = Field(
        description="否定匹配方式 [原字段 'negative_match_type']",
        examples=["negativePhrase"],
        # - - - - - - - - - -
        validation_alias="negative_match_type",
    )
    state: StrOrNone2Blank = Field(
        description="广告状态",
        examples=["enabled"],
    )
    status: StrOrNone2Blank = Field(
        description="服务状态 [原字段 'serving_status']",
        examples=["CAMPAIGN_PAUSED"],
        # - - - - - - - - - -
        validation_alias="serving_status",
    )
    create_time_ts: IntOrNone2Zero = Field(
        description="创建时间 (UTC毫秒时间戳) [原字段 'creation_date']",
        examples=[1530580497000],
        # - - - - - - - - - -
        validation_alias="creation_date",
    )
    update_time_ts: IntOrNone2Zero = Field(
        description="更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']",
        examples=[1530580497000],
        # - - - - - - - - - -
        validation_alias="last_updated_date",
    )


class SpNegativeKeywords(ResponseV1Token):
    """SP 否定手动关键词投放列表"""

    data: list[SpNegativeKeyword] = Field(
        description="SP 否定手动关键词投放列表",
        examples=[
            [
                {
                    "profile_id": 90000000000004,
                    "campaign_id": 70000000000079,
                    "ad_group_id": 0,
                    "negative_keyword_id": 400000000000001,
                    "negative_keyword_text": "aa 0000  aag",
                    "negative_keyword_match_type": "negativePhrase",
                    "state": "enabled",
                    "status": "CAMPAIGN_PAUSED",
                    "create_time_ts": 1530580497000,
                    "update_time_ts": 1530580497000,
                },
            ],
        ],
    )


# . SP Negative Targets
class SpNegativeTarget(BaseModel):
    """SP 否定自动投放/手动商品投放"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000004],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000087],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000031],
    )
    negative_target_id: int = Field(
        description="否定目标ID [原字段 'target_id']",
        examples=[30000000000002],
        # - - - - - - - - - -
        validation_alias="target_id",
    )
    negative_target_text: StrOrNone2Blank = Field(
        description="否定目标文本 [原字段 'negative_text']",
        examples=["Aaaaaab"],
        # - - - - - - - - - -
        validation_alias="negative_text",
    )
    negative_target_match_type: str = Field(
        description="否定目标类型 [原字段 'negative_type']",
        examples=["negativeBrand"],
        # - - - - - - - - - -
        validation_alias="negative_type",
    )
    state: StrOrNone2Blank = Field(
        description="广告状态",
        examples=["enabled"],
    )
    status: StrOrNone2Blank = Field(
        description="服务状态 [原字段 'serving_status']",
        examples=["CAMPAIGN_PAUSED"],
        # - - - - - - - - - -
        validation_alias="serving_status",
    )
    create_time_ts: IntOrNone2Zero = Field(
        description="创建时间 (UTC毫秒时间戳) [原字段 'creation_date']",
        examples=[1573797409000],
        # - - - - - - - - - -
        validation_alias="creation_date",
    )
    update_time_ts: IntOrNone2Zero = Field(
        description="更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']",
        examples=[1573797409000],
        # - - - - - - - - - -
        validation_alias="last_updated_date",
    )


class SpNegativeTargets(ResponseV1Token):
    """SP 否定自动投放/手动商品投放列表"""

    data: list[SpNegativeTarget] = Field(
        description="SP 否定自动投放/手动商品投放列表",
        examples=[
            [
                {
                    "profile_id": 90000000000004,
                    "campaign_id": 700000000000087,
                    "ad_group_id": 600000000000031,
                    "negative_target_id": 30000000000002,
                    "negative_target_text": "Aaaaaab",
                    "negative_target_match_type": "negativeBrand",
                    "state": "enabled",
                    "status": "CAMPAIGN_PAUSED",
                    "create_time_ts": 1573797409000,
                    "update_time_ts": 1573797409000,
                },
            ],
        ],
    )


# 基础数据 - Sponsored Brands - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# . SB Campaigns
class SbCampaign(BaseModel):
    """SB 广告活动"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000006],
    )
    portfolio_id: IntOrNone2Zero = Field(
        description="广告组合ID",
        examples=[800000000000005],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[7000000000280],
    )
    campaign_name: str = Field(
        description="广告活动名称 [原字段 'name']",
        examples=["000 0A0A 广告示示广-告铺"],
        # - - - - - - - - - -
        validation_alias="name",
    )
    creative_type: str = Field(
        description="广告创意类型",
        examples=["COLLECTION"],
    )
    budget: float = Field(
        description="广告预算",
        examples=[1.0],
    )
    budget_type: str = Field(
        description="广告预算类型",
        examples=["daily"],
    )
    last_over_budget_at: str | None = Field(
        description="时间字符串，格式为 YYYY-MM-DD HH:MM:SS，可为 None [原字段 'lastOverBudgetAt']",
        examples=["2026-10-12 22:17:35"],
        # - - - - - - - - - -
        validation_alias="lastOverBudgetAt",
    )
    bid_multiplier: FloatOrNone2Zero = Field(
        description="自定义竞价调整",
        examples=[0.0],
    )
    bid_optimization: IntOrNone2Zero = Field(
        description="是否使用自动竞价 (0: 否, 1: 是)",
        examples=[1],
    )
    start_time: StrOrNone2Blank = Field(
        description="开始时间 [原字段 'start_date']",
        examples=["2022-11-17 00:00:00"],
        # - - - - - - - - - -
        validation_alias="start_date",
    )
    end_time: StrOrNone2Blank = Field(
        description="结束时间 [原字段 'end_date']",
        examples=[""],
        # - - - - - - - - - -
        default=None,
        validation_alias="end_date",
    )
    state: StrOrNone2Blank = Field(
        description="广告状态",
        examples=["enabled"],
    )
    status: StrOrNone2Blank = Field(
        description="服务状态 [原字段 'serving_status']",
        examples=["CAMPAIGN_STATUS_ENABLED"],
        # - - - - - - - - - -
        validation_alias="serving_status",
    )


class SbCampaigns(ResponseV1Token):
    """SB 广告活动列表"""

    data: list[SbCampaign] = Field(
        description="SB 广告活动列表",
        examples=[
            [
                {
                    "profile_id": 90000000000006,
                    "portfolio_id": 800000000000005,
                    "campaign_id": 7000000000280,
                    "campaign_name": "000 0A0A 广告示示广-告铺",
                    "creative_type": "COLLECTION",
                    "budget": 1.0,
                    "budget_type": "daily",
                    "last_over_budget_at": "2026-10-12 22:17:35",
                    "bid_multiplier": 0.0,
                    "bid_optimization": 1,
                    "start_time": "2022-11-17 00:00:00",
                    "end_time": "",
                    "state": "enabled",
                    "status": "CAMPAIGN_STATUS_ENABLED",
                },
            ],
        ],
    )


# . SB Ad Groups
class SbAdGroup(BaseModel):
    """SB 广告组"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000004],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000112],
    )
    ad_group_id: int = Field(
        description="广告组ID",
        examples=[60000000000208],
    )
    ad_group_name: str = Field(
        description="广告组名称 [原字段 'name']",
        examples=["000 000广告组-广甲"],
        # - - - - - - - - - -
        validation_alias="name",
    )
    state: StrOrNone2Blank = Field(
        description="广告组状态",
        examples=["enabled"],
    )
    status: StrOrNone2Blank = Field(
        description="服务状态 [原字段 'serving_status']",
        examples=["CAMPAIGN_PAUSED"],
        # - - - - - - - - - -
        validation_alias="serving_status",
    )
    create_time_ts: IntOrNone2Zero = Field(
        description="创建时间 (UTC毫秒时间戳) [原字段 'creation_date']",
        examples=[1670754552292],
        # - - - - - - - - - -
        validation_alias="creation_date",
    )
    update_time_ts: IntOrNone2Zero = Field(
        description="更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']",
        examples=[1670754552292],
        # - - - - - - - - - -
        validation_alias="last_updated_date",
    )


class SbAdGroups(ResponseV1Token):
    """SB 广告组列表"""

    data: list[SbAdGroup] = Field(
        description="SB 广告组列表",
        examples=[
            [
                {
                    "profile_id": 90000000000004,
                    "campaign_id": 700000000000112,
                    "ad_group_id": 60000000000208,
                    "ad_group_name": "000 000广告组-广甲",
                    "state": "enabled",
                    "status": "CAMPAIGN_PAUSED",
                    "create_time_ts": 1670754552292,
                    "update_time_ts": 1670754552292,
                },
            ],
        ],
    )


# . SB Creatives
class SbCreativeCustomImage(BaseModel):
    """SB 广告创意图片配置"""

    image_asset_id: str = Field(
        description="图片素材ID [原字段 'assetId']",
        examples=[
            "amzn1.assetlibrary.asset1.aa0000a0aa0a000a000aa000a0a001u6:version_v1"
        ],
        # - - - - - - - - - -
        validation_alias="assetId",
    )
    image_url: str = Field(
        description="图片链接 [原字段 'url']",
        examples=[
            "https://a.aaaaa-aaaaaa.aaa/aaaaaa/A/aa-aa-aa0000aa-a000/000a0aaa-00aa-0000-0a00-0a0a00000aa0.afw"
        ],
        # - - - - - - - - - -
        validation_alias="url",
    )


class SbCreativeSubpage(BaseModel):
    """SB 广告创意子页面配置"""

    asin: StrOrNone2Blank = Field(
        description="子页面ASIN [原字段 'asin']",
        examples=["A0000AAADB"],
        # - - - - - - - - - -
        default=None,
        validation_alias="asin",
    )
    page_title: StrOrNone2Blank = Field(
        description="子页面标题 [原字段 'pageTitle']",
        examples=["aaa RT"],
        # - - - - - - - - - -
        default=None,
        validation_alias="pageTitle",
    )
    page_url: str = Field(
        description="子页面URL [原字段 'url']",
        examples=[
            "https://aaa.aaaaaa.aaa/aaaaaa/aaaa/A0AA0000-00AA-0A0A-A00A-0A000AAA0883"
        ],
        # - - - - - - - - - -
        validation_alias="url",
    )


class SbCreativeConfig(BaseModel):
    """SB 广告创意设置"""

    creative_type: str = Field(
        description="广告创意类型 [原字段 'type']",
        examples=["PRODUCT_COLLECTION"],
        # - - - - - - - - - -
        validation_alias="type",
    )
    creative_status: str = Field(
        description="广告创意状态 [原字段 'creativeStatus']",
        examples=["REJECTED_BY_MODERATION"],
        # - - - - - - - - - -
        validation_alias="creativeStatus",
    )
    creative_version: int = Field(
        description="广告创意版本 [原字段 'creativeVersion']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="creativeVersion",
    )
    asins: list[str] | None = Field(
        description="广告创意 ASIN 列表",
        examples=[["A00AAAA0F5"]],
        # - - - - - - - - - -
        default=None,
    )
    asin_excluded: list[str] | None = Field(
        description="广告创意排除 ASIN 列表 [原字段 'asinExclusions']",
        examples=[["A0A0A0AAJN"]],
        # - - - - - - - - - -
        default=None,
        validation_alias="asinExclusions",
    )
    consent_to_translate: bool = Field(
        description="是否同意翻译 [原字段 'consentToTranslate']",
        examples=[False],
        # - - - - - - - - - -
        default=False,
        validation_alias="consentToTranslate",
    )
    brand_name: StrOrNone2Blank = Field(
        description="品牌名称 [原字段 'brandName']",
        examples=["AaaaAaaal"],
        # - - - - - - - - - -
        default=None,
        validation_alias="brandName",
    )
    brand_logo_asset_id: StrOrNone2Blank = Field(
        description="品牌Logo素材ID [原字段 'brandLogoAssetID']",
        examples=[
            "amzn1.assetlibrary.asset1.0000000a00a0000000000a000a0a0167:version_v1"
        ],
        # - - - - - - - - - -
        default=None,
        validation_alias="brandLogoAssetID",
    )
    brand_logo_url: StrOrNone2Blank = Field(
        description="品牌Logo链接 [原字段 'brandLogoUrl']",
        examples=[
            "https://a.aaaaa-aaaaaa.aaa/aaaaaa/A/aa-aa-aa0000aa-a000/aa0a0a00-0a00-0aaa-0aa0-a0000000a0a0.afx"
        ],
        # - - - - - - - - - -
        default=None,
        validation_alias="brandLogoUrl",
    )
    headline: StrOrNone2Blank = Field(
        description="头条",
        examples=["AaaaAaaaa 示示示示示示示示示示示示、示示示示示示示示店丙"],
        # - - - - - - - - - -
        default=None,
    )
    headlines: list[str] | None = Field(
        description="头条列表",
        examples=[["000AA Aaa Aaaaaaaaaa 000/000+ Aaaaa (Aaaaa/Aaaabf)"]],
        # - - - - - - - - - -
        default=None,
    )
    headline_original: StrOrNone2Blank = Field(
        description="原始头条 [原字段 'originalHeadline']",
        examples=["示示00示示示示示示示示示色账！"],
        # - - - - - - - - - -
        default=None,
        validation_alias="originalHeadline",
    )
    headlines_original: list[str] | None = Field(
        description="原始头条列表 [原字段 'originalHeadlines']",
        examples=[["000AA Aaa Aaaaaaaaaa 000/000+ Aaaaa (Aaaaa/Aaaabf)"]],
        # - - - - - - - - - -
        default=None,
        validation_alias="originalHeadlines",
    )
    custom_image_asset_id: StrOrNone2Blank = Field(
        description="图片素材ID [原字段 'customImageAssetId']",
        examples=[
            "amzn1.assetlibrary.asset1.0aa0a0000000a00aaa00aa0a000a012g:version_v1"
        ],
        # - - - - - - - - - -
        default=None,
        validation_alias="customImageAssetId",
    )
    custom_image_url: StrOrNone2Blank = Field(
        description="图片链接 [原字段 'customImageUrl']",
        examples=[
            "https://a.aaaaa-aaaaaa.aaa/aaaaaa/A/aa-aa-aa0000aa-a000/aa0a000a-000a-0aaa-00aa-0a00aaa00a0a.aga"
        ],
        # - - - - - - - - - -
        default=None,
        validation_alias="customImageUrl",
    )
    custom_images: list[SbCreativeCustomImage] | None = Field(
        description="图片素材列表 [原字段 'customImages']",
        examples=[
            [
                {
                    "image_asset_id": "amzn1.assetlibrary.asset1.aa0000a0aa0a000a000aa000a0a001u6:version_v1",
                    "image_url": "https://a.aaaaa-aaaaaa.aaa/aaaaaa/A/aa-aa-aa0000aa-a000/000a0aaa-00aa-0000-0a00-0a0a00000aa0.afw",
                }
            ]
        ],
        # - - - - - - - - - -
        default=None,
        validation_alias="customImages",
    )
    optimize_properties: list[str] | None = Field(
        description="优化属性列表 [原字段 'creativePropertiesToOptimize']",
        examples=[["HEADLINE"]],
        # - - - - - - - - - -
        default=None,
        validation_alias="creativePropertiesToOptimize",
    )
    video_asset_ids: list[str] | None = Field(
        description="视频素材ID列表 [原字段 'videoAssetIds']",
        examples=[["aaaa0.aaaa.aaaaa0.0aaa00a0-000a-00aa-a0a0-0a00a0000053"]],
        # - - - - - - - - - -
        default=None,
        validation_alias="videoAssetIds",
    )
    video_original_asset_ids: list[str] | None = Field(
        description="原始素材ID列表 [原字段 'originalVideoAssetIds']",
        examples=[["aaaa0.aaaa.aaaaa0.0aaa00a0-000a-00aa-a0a0-0a00a0000053"]],
        # - - - - - - - - - -
        default=None,
        validation_alias="originalVideoAssetIds",
    )
    collection_type: StrOrNone2Blank = Field(
        description="商品集类型 [原字段 'collectionType']",
        examples=["THEMED"],
        # - - - - - - - - - -
        default=None,
        validation_alias="collectionType",
    )
    subpages: list[SbCreativeSubpage] | None = Field(
        description="子页面列表",
        examples=[
            [
                {
                    "asin": "A0000AAADB",
                    "page_title": "aaa RT",
                    "page_url": "https://aaa.aaaaaa.aaa/aaaaaa/aaaa/A0AA0000-00AA-0A0A-A00A-0A000AAA0883",
                }
            ]
        ],
        # - - - - - - - - - -
        default=None,
    )
    title: StrOrNone2Blank = Field(
        description="广告标题",
        examples=["000AA AA & AAA - 0000+ Aaaaao"],
        # - - - - - - - - - -
        default=None,
    )


class SbCreativeLandingPage(BaseModel):
    """SB 广告创意着陆页"""

    page_type: str = Field(
        description="着陆页类型 [原字段 'pageType']",
        examples=["PRODUCT_LIST"],
        # - - - - - - - - - -
        validation_alias="pageType",
    )
    page_url: StrOrNone2Blank = Field(
        description="着陆页URL [原字段 'url']",
        examples=[
            "https://aaa.aaaaaa.aa.aa/aaaaaa/aaaa/A00A0000-A000-00A0-A000-00AAA00A0BM3"
        ],
        # - - - - - - - - - -
        default=None,
        validation_alias="url",
    )


class SbCreative(BaseModel):
    """SB 广告创意"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[900000000000001],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000000185],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000000172],
    )
    creative_id: int = Field(
        description="广告创意ID [原字段 'ad_creative_id']",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="ad_creative_id",
    )
    creative_name: StrOrNone2Blank = Field(
        description="广告创意名称 [原字段 'name']",
        examples=["广-aaaaaaaaaa000告示示广-49.7"],
        # - - - - - - - - - -
        validation_alias="name",
    )
    creative_type: str = Field(
        description="广告创意类型",
        examples=["PRODUCT_COLLECTION"],
    )
    creative_config: SbCreativeConfig = Field(
        description="广告创意设置 [原字段 'creative']",
        examples=[
            {
                "creative_type": "PRODUCT_COLLECTION",
                "creative_status": "REJECTED_BY_MODERATION",
                "creative_version": 1,
                "asins": ["A00AAAA0F5"],
                "asin_excluded": ["A0A0A0AAJN"],
                "consent_to_translate": False,
                "brand_name": "AaaaAaaal",
                "brand_logo_asset_id": "amzn1.assetlibrary.asset1.0000000a00a0000000000a000a0a0167:version_v1",
                "brand_logo_url": "https://a.aaaaa-aaaaaa.aaa/aaaaaa/A/aa-aa-aa0000aa-a000/aa0a0a00-0a00-0aaa-0aa0-a0000000a0a0.afx",
                "headline": "AaaaAaaaa 示示示示示示示示示示示示、示示示示示示示示店丙",
                "headlines": None,
                "headline_original": None,
                "headlines_original": None,
                "custom_image_asset_id": "amzn1.assetlibrary.asset1.0aa0a0000000a00aaa00aa0a000a012g:version_v1",
                "custom_image_url": "https://a.aaaaa-aaaaaa.aaa/aaaaaa/A/aa-aa-aa0000aa-a000/aa0a000a-000a-0aaa-00aa-0a00aaa00a0a.aga",
                "custom_images": None,
                "optimize_properties": None,
                "video_asset_ids": [
                    "amzn1.assetlibrary.asset1.0000a0000aaa0a00aaa0aaa000aa023s:version_v1"
                ],
                "video_original_asset_ids": [
                    "amzn1.assetlibrary.asset1.0000a0000aaa0a00aaa0aaa000aa023s:version_v1"
                ],
                "collection_type": "THEMED",
                "subpages": [
                    {
                        "asin": "A0000AAADB",
                        "page_title": "aaa RT",
                        "page_url": "https://aaa.aaaaaa.aaa/aaaaaa/aaaa/A0AA0000-00AA-0A0A-A00A-0A000AAA0883",
                    }
                ],
                "title": "000AA AA & AAA - 0000+ Aaaaao",
            }
        ],
        # - - - - - - - - - -
        validation_alias="creative",
    )
    video_creatives: list[Any] = Field(
        description="视频创意列表",
        examples=[
            [
                {
                    "creative_version": "3",
                    "creative_status": "PUBLISHED",
                    "creative_type": "VIDEO",
                    "videos": [
                        {
                            "asset_id": "amzn1.assetlibrary.asset1.0000a0000aaa0a00aaa0aaa000aa023s:version_v1",
                            "versions": [],
                        }
                    ],
                }
            ]
        ],
    )
    landing_page: SbCreativeLandingPage | None = Field(
        description="广告创意着陆页",
        examples=[
            {
                "page_type": "PRODUCT_LIST",
                "page_url": "https://aaa.aaaaaa.aa.aa/aaaaaa/aaaa/A00A0000-A000-00A0-A000-00AAA00A0BM3",
            }
        ],
        # - - - - - - - - - -
        default=None,
    )
    asins: list[str] | None = Field(
        description="广告创意 ASIN 列表 [原字段 'asin']",
        examples=[["A00AAAA0F5"]],
        # - - - - - - - - - -
        default=None,
        validation_alias="asin",
    )
    state: StrOrNone2Blank = Field(
        description="广告状态",
        examples=["archived"],
    )
    status: StrOrNone2Blank = Field(
        description="服务状态 [原字段 'serving_status']",
        examples=["CAMPAIGN_ARCHIVED"],
        # - - - - - - - - - -
        validation_alias="serving_status",
    )
    create_time_ts: IntOrNone2Zero = Field(
        description="创建时间 (UTC毫秒时间戳) [原字段 'creation_date']",
        examples=[1663141705429],
        # - - - - - - - - - -
        validation_alias="creation_date",
    )
    update_time_ts: IntOrNone2Zero = Field(
        description="更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']",
        examples=[1724621774670],
        # - - - - - - - - - -
        validation_alias="last_updated_date",
    )

    @field_validator("video_creatives", mode="before")
    @classmethod
    def _validate_video_creatives(cls, value: object) -> object:
        """将显式null转换为空列表，保留其他输入供列表外层校验。

        Args:
            value (object): 字段校验前的原始输入；字段缺失仍由必填约束处理。

        Returns:
            object: null对应空列表；其他输入保持原样。
        """
        return [] if value is None else value


class SbCreatives(ResponseV1Token):
    """SB 广告创意列表"""

    data: list[SbCreative] = Field(
        description="SB 广告创意列表",
        examples=[
            [
                {
                    "profile_id": 90000000000007,
                    "campaign_id": 700000000000170,
                    "ad_group_id": 600000000000278,
                    "creative_id": 500000000000004,
                    "creative_name": "广告 示示 - 00.0.0004",
                    "creative_type": "VIDEO",
                    "creative_config": {
                        "creative_type": "VIDEO",
                        "creative_status": "PUBLISHED",
                        "creative_version": 1,
                        "asins": ["A0AAA0AA6O"],
                        "asin_excluded": ["A0A0A0AAJN"],
                        "consent_to_translate": False,
                        "brand_name": None,
                        "brand_logo_asset_id": None,
                        "brand_logo_url": None,
                        "headline": None,
                        "headlines": None,
                        "headline_original": None,
                        "headlines_original": None,
                        "custom_image_asset_id": None,
                        "custom_image_url": None,
                        "custom_images": None,
                        "optimize_properties": None,
                        "video_asset_ids": [
                            "amzn1.assetlibrary.asset1.0000a0000aaa0a00aaa0aaa000aa023s:version_v1"
                        ],
                        "video_original_asset_ids": [
                            "amzn1.assetlibrary.asset1.0000a0000aaa0a00aaa0aaa000aa023s:version_v1"
                        ],
                        "collection_type": "THEMED",
                        "subpages": [
                            {
                                "asin": "A0000AAADB",
                                "page_title": "aaa RT",
                                "page_url": "https://aaa.aaaaaa.aaa/aaaaaa/aaaa/A0AA0000-00AA-0A0A-A00A-0A000AAA0883",
                            }
                        ],
                        "title": "000AA AA & AAA - 0000+ Aaaaao",
                    },
                    "video_creatives": [
                        {
                            "creative_version": "3",
                            "creative_status": "PUBLISHED",
                            "creative_type": "VIDEO",
                            "videos": [
                                {
                                    "asset_id": "amzn1.assetlibrary.asset1.0000a0000aaa0a00aaa0aaa000aa023s:version_v1",
                                    "versions": [],
                                }
                            ],
                        }
                    ],
                    "landing_page": {
                        "page_type": "DETAIL_PAGE",
                        "page_url": "https://aaa.aaaaaa.aa/aa/A0AAA0AA0M",
                    },
                    "asins": ["A0AAA0AA6O"],
                    "state": "enabled",
                    "status": "CAMPAIGN_PAUSED",
                    "create_time_ts": 1758692404896,
                    "update_time_ts": 1781581969786,
                }
            ]
        ],
    )
# . SB Keywords
class SbKeyword(BaseModel):
    """SB 广告投放目标"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000006],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000090],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000028],
    )
    ad_type: str = Field(
        description="广告类型 [原字段 'ads_type']",
        examples=["SB"],
        # - - - - - - - - - -
        validation_alias="ads_type",
    )
    targeting_type: str = Field(
        description="投放目标类型",
        examples=["keyword"],
    )
    keyword_id: int = Field(
        description="关键词ID",
        examples=[400000000020],
    )
    keyword_text: StrOrNone2Blank = Field(
        description="关键词文本",
        examples=["+aaaaa +000ab"],
    )
    match_type: StrOrNone2Blank = Field(
        description="关键词匹配类型",
        examples=["broad"],
    )
    bid: FloatOrNone2Zero = Field(
        description="竞价 [原字段 'keyword_bid']",
        examples=[0.8],
        # - - - - - - - - - -
        validation_alias="keyword_bid",
    )
    state: StrOrNone2Blank = Field(
        description="广告状态 [原字段 'keyword_state']",
        examples=["paused"],
        # - - - - - - - - - -
        validation_alias="keyword_state",
    )


class SbKeywords(ResponseV1Token):
    """SB 关键词投放列表"""

    data: list[SbKeyword] = Field(
        description="SB 关键词投放列表",
        examples=[
            [
                {
                    "profile_id": 90000000000006,
                    "campaign_id": 700000000000090,
                    "ad_group_id": 600000000000028,
                    "ad_type": "SB",
                    "targeting_type": "keyword",
                    "keyword_id": 400000000020,
                    "keyword_text": "+aaaaa +000ab",
                    "match_type": "broad",
                    "bid": 0.8,
                    "state": "paused",
                },
            ],
        ],
    )


# . SB Targets
class SbTarget(BaseModel):
    """SB 目标商品投放"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000006],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000000039],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000000041],
    )
    ad_type: str = Field(
        description="广告类型 [原字段 'ads_type']",
        examples=["SB"],
        # - - - - - - - - - -
        validation_alias="ads_type",
    )
    targeting_type: str = Field(
        description="投放目标类型",
        examples=["producttarget"],
    )
    target_id: int = Field(
        description="目标商品广告ID",
        examples=[300000000000000003],
    )
    expression: str = Field(
        description="目标定位表达式 (JSON 字符串)",
        examples=['[{"type": "asinSameAs", "value": "A00AA0AAFG"}]'],
    )
    expression_resolved: StrOrNone2Blank = Field(
        description="目标定位解析表达式 (JSON 字符串) [原字段 'resolved_expression']",
        examples=['[{"type": "asinSameAs", "value": "A00AA0AAFG"}]'],
        # - - - - - - - - - -
        validation_alias="resolved_expression",
    )
    bid: FloatOrNone2Zero = Field(
        description="竞价 [原字段 'target_bid']",
        examples=[1.0],
        # - - - - - - - - - -
        validation_alias="target_bid",
    )
    state: StrOrNone2Blank = Field(
        description="广告状态 [原字段 'target_state']",
        examples=["paused"],
        # - - - - - - - - - -
        validation_alias="target_state",
    )


class SbTargets(ResponseV1Token):
    """SB 目标商品投放列表"""

    data: list[SbTarget] = Field(
        description="SB 目标商品投放列表",
        examples=[
            [
                {
                    "profile_id": 90000000000006,
                    "campaign_id": 700000000000000039,
                    "ad_group_id": 600000000000000041,
                    "ad_type": "SB",
                    "targeting_type": "producttarget",
                    "target_id": 300000000000000003,
                    "expression": '[{"type": "asinSameAs", "value": "A00AA0AAFG"}]',
                    "expression_resolved": '[{"type": "asinSameAs", "value": "A00AA0AAFG"}]',
                    "bid": 1.0,
                    "state": "paused",
                },
            ],
        ],
    )


# . SB Negative Keywords
class SbNegativeKeyword(BaseModel):
    """SB 否定关键词投放"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000004],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000128],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[60000000000285],
    )
    negative_keyword_id: int = Field(
        description="否定关键词ID [原字段 'keyword_id']",
        examples=[40000000000006],
        # - - - - - - - - - -
        validation_alias="keyword_id",
    )
    negative_keyword_text: str = Field(
        description="否定关键词文本 [原字段 'keyword_text']",
        examples=["aaaaa 000 ag"],
        # - - - - - - - - - -
        validation_alias="keyword_text",
    )
    negative_keyword_match_type: str = Field(
        description="否定匹配方式 [原字段 'match_type']",
        examples=["negativeExact"],
        # - - - - - - - - - -
        validation_alias="match_type",
    )
    state: StrOrNone2Blank = Field(
        description="广告状态",
        examples=["enabled"],
    )
    status: StrOrNone2Blank = Field(
        description="服务状态 [原字段 'serving_status']",
        examples=[""],
        # - - - - - - - - - -
        validation_alias="serving_status",
    )
    create_time_ts: IntOrNone2Zero = Field(
        description="创建时间 (UTC毫秒时间戳) [原字段 'creation_date']",
        examples=[1743039447981],
        # - - - - - - - - - -
        validation_alias="creation_date",
    )
    update_time_ts: IntOrNone2Zero = Field(
        description="更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']",
        examples=[1743039448036],
        # - - - - - - - - - -
        validation_alias="last_updated_date",
    )


class SbNegativeKeywords(ResponseV1Token):
    """SB 否定关键词投放列表"""

    data: list[SbNegativeKeyword] = Field(
        description="SB 否定关键词投放列表",
        examples=[
            [
                {
                    "profile_id": 90000000000004,
                    "campaign_id": 700000000000128,
                    "ad_group_id": 60000000000285,
                    "negative_keyword_id": 40000000000006,
                    "negative_keyword_text": "aaaaa 000 ag",
                    "negative_keyword_match_type": "negativeExact",
                    "state": "enabled",
                    "status": "",
                    "create_time_ts": 1743039447981,
                    "update_time_ts": 1743039448036,
                },
            ],
        ],
    )


# . SB Negative Targets
class SbNegativeTarget(BaseModel):
    """SB 否定目标商品投放"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[900000000000001],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000000038],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000000037],
    )
    negative_target_id: int = Field(
        description="否定目标ID [原字段 'target_id']",
        examples=[300000000000000001],
        # - - - - - - - - - -
        validation_alias="target_id",
    )
    negative_expression: str = Field(
        description="否定定位表达式 (JSON 字符串) [原字段 'expression']",
        examples=['[{"type": "asinSameAs", "value": "A000AAA0A3"}]'],
        # - - - - - - - - - -
        validation_alias="expression",
    )
    negative_expression_resolved: str = Field(
        description="否定定位解析表达式 (JSON 字符串) [原字段 'resolved_expression']",
        examples=['[{"type": "asinSameAs", "value": "A000AAA0A3"}]'],
        # - - - - - - - - - -
        validation_alias="resolved_expression",
    )
    negative_expression_type: StrOrNone2Blank = Field(
        description="否定定位类型 [原字段 'expression_type']",
        examples=[""],
        # - - - - - - - - - -
        validation_alias="expression_type",
    )
    state: StrOrNone2Blank = Field(
        description="广告状态",
        examples=["archived"],
    )
    status: StrOrNone2Blank = Field(
        description="服务状态 [原字段 'serving_status']",
        examples=[""],
        # - - - - - - - - - -
        validation_alias="serving_status",
    )
    create_time_ts: IntOrNone2Zero = Field(
        description="创建时间 (UTC毫秒时间戳) [原字段 'creation_date']",
        examples=[1598667375000],
        # - - - - - - - - - -
        validation_alias="creation_date",
    )
    update_time_ts: IntOrNone2Zero = Field(
        description="更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']",
        examples=[1761061319939],
        # - - - - - - - - - -
        validation_alias="last_updated_date",
    )


class SbNegativeTargets(ResponseV1Token):
    """SB 否定目标商品投放列表"""

    data: list[SbNegativeTarget] = Field(
        description="SB 否定目标商品投放列表",
        examples=[
            [
                {
                    "profile_id": 900000000000001,
                    "campaign_id": 700000000000000038,
                    "ad_group_id": 600000000000000037,
                    "negative_target_id": 300000000000000001,
                    "negative_expression": '[{"type": "asinSameAs", "value": "A000AAA0A3"}]',
                    "negative_expression_resolved": '[{"type": "asinSameAs", "value": "A000AAA0A3"}]',
                    "negative_expression_type": "",
                    "state": "archived",
                    "status": "",
                    "create_time_ts": 1598667375000,
                    "update_time_ts": 1761061319939,
                },
            ],
        ],
    )


# 基础数据 - Sponsored Display - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# . SD Campaigns
class SdCampaign(BaseModel):
    """SD 广告活动"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000007],
    )
    portfolio_id: IntOrNone2Zero = Field(
        description="广告组合ID",
        examples=[0],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[7000000000202],
    )
    campaign_name: str = Field(
        description="广告活动名称 [原字段 'name']",
        examples=["00-广告角"],
        # - - - - - - - - - -
        validation_alias="name",
    )
    tactic: str = Field(
        description="投放类型",
        examples=["T00020"],
    )
    bid_type: str = Field(
        description="竞价类型 [原字段 'cost_type']",
        examples=["cpc"],
        # - - - - - - - - - -
        validation_alias="cost_type",
    )
    budget: float = Field(
        description="每日预算",
        examples=[14.0],
    )
    budget_type: str = Field(
        description="预算类型",
        examples=["daily"],
    )
    last_over_budget_at: str | None = Field(
        description="时间字符串，格式为 YYYY-MM-DD HH:MM:SS，可为 None [原字段 'lastOverBudgetAt']",
        examples=["2026-10-12 22:17:35"],
        # - - - - - - - - - -
        validation_alias="lastOverBudgetAt",
    )
    start_time: StrOrNone2Blank = Field(
        description="开始时间 [原字段 'start_date']",
        examples=["2020-09-29 00:00:00"],
        # - - - - - - - - - -
        validation_alias="start_date",
    )
    end_time: StrOrNone2Blank = Field(
        description="结束时间 [原字段 'end_date']",
        examples=[""],
        # - - - - - - - - - -
        default=None,
        validation_alias="end_date",
    )
    state: StrOrNone2Blank = Field(
        description="广告状态",
        examples=["paused"],
    )
    status: StrOrNone2Blank = Field(
        description="服务状态 [原字段 'serving_status']",
        examples=["CAMPAIGN_PAUSED"],
        # - - - - - - - - - -
        validation_alias="serving_status",
    )
    create_time_ts: IntOrNone2Zero = Field(
        description="创建时间 (UTC毫秒时间戳) [原字段 'creation_date']",
        examples=[1601345109000],
        # - - - - - - - - - -
        validation_alias="creation_date",
    )
    update_time_ts: IntOrNone2Zero = Field(
        description="更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']",
        examples=[1792105230609],
        # - - - - - - - - - -
        validation_alias="last_updated_date",
    )


class SdCampaigns(ResponseV1Token):
    """SD 广告活动列表"""

    data: list[SdCampaign] = Field(
        description="SD 广告活动列表",
        examples=[
            [
                {
                    "profile_id": 90000000000007,
                    "portfolio_id": 0,
                    "campaign_id": 7000000000202,
                    "campaign_name": "00-广告角",
                    "tactic": "T00020",
                    "bid_type": "cpc",
                    "budget": 14.0,
                    "budget_type": "daily",
                    "last_over_budget_at": "2026-10-12 22:17:35",
                    "start_time": "2020-09-29 00:00:00",
                    "end_time": "",
                    "state": "paused",
                    "status": "CAMPAIGN_PAUSED",
                    "create_time_ts": 1601345109000,
                    "update_time_ts": 1792105230609,
                },
            ],
        ],
    )


# . SD Ad Groups
class SdAdGroup(BaseModel):
    """SD 广告组"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000006],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[70000000000077],
    )
    ad_group_id: int = Field(
        description="广告组ID",
        examples=[60000000000072],
    )
    ad_group_name: str = Field(
        description="广告组名称 [原字段 'name']",
        examples=["aa-00-广名"],
        # - - - - - - - - - -
        validation_alias="name",
    )
    default_bid: float = Field(
        description="默认竞价",
        examples=[0.6],
    )
    bid_optimization: str = Field(
        description="竞价优化方式",
        examples=["clicks"],
    )
    state: StrOrNone2Blank = Field(
        description="广告组状态",
        examples=["enabled"],
    )
    status: StrOrNone2Blank = Field(
        description="服务状态 [原字段 'serving_status']",
        examples=["CAMPAIGN_PAUSED"],
        # - - - - - - - - - -
        validation_alias="serving_status",
    )
    create_time_ts: IntOrNone2Zero = Field(
        description="创建时间 (UTC毫秒时间戳) [原字段 'creation_date']",
        examples=[1599816989000],
        # - - - - - - - - - -
        validation_alias="creation_date",
    )
    update_time_ts: IntOrNone2Zero = Field(
        description="更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']",
        examples=[1599816989000],
        # - - - - - - - - - -
        validation_alias="last_updated_date",
    )


class SdAdGroups(ResponseV1Token):
    """SD 广告组列表"""

    data: list[SdAdGroup] = Field(
        description="SD 广告组列表",
        examples=[
            [
                {
                    "profile_id": 90000000000006,
                    "campaign_id": 70000000000077,
                    "ad_group_id": 60000000000072,
                    "ad_group_name": "aa-00-广名",
                    "default_bid": 0.6,
                    "bid_optimization": "clicks",
                    "state": "enabled",
                    "status": "CAMPAIGN_PAUSED",
                    "create_time_ts": 1599816989000,
                    "update_time_ts": 1599816989000,
                },
            ],
        ],
    )


# . SD Products
class SdProduct(BaseModel):
    """SD 商品投放"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000006],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000168],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000108],
    )
    ad_id: int = Field(
        description="商品广告ID",
        examples=[5000000000005],
    )
    asin: StrOrNone2Blank = Field(
        description="商品ASIN",
        examples=["A00AAAA0AL"],
    )
    msku: str = Field(
        description="亚马逊SKU [原字段 'sku']",
        examples=["000aa*2X"],
        # - - - - - - - - - -
        validation_alias="sku",
    )
    state: StrOrNone2Blank = Field(
        description="广告状态",
        examples=["paused"],
    )
    status: StrOrNone2Blank = Field(
        description="服务状态 [原字段 'serving_status']",
        examples=["AD_PAUSED"],
        # - - - - - - - - - -
        validation_alias="serving_status",
    )
    create_time_ts: IntOrNone2Zero = Field(
        description="创建时间 (UTC毫秒时间戳) [原字段 'creation_date']",
        examples=[1600853070000],
        # - - - - - - - - - -
        validation_alias="creation_date",
    )
    update_time_ts: IntOrNone2Zero = Field(
        description="更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']",
        examples=[1696439612959],
        # - - - - - - - - - -
        validation_alias="last_updated_date",
    )


class SdProducts(ResponseV1Token):
    """SD 商品投放列表"""

    data: list[SdProduct] = Field(
        description="SD 商品投放列表",
        examples=[
            [
                {
                    "profile_id": 90000000000006,
                    "campaign_id": 700000000000168,
                    "ad_group_id": 600000000000108,
                    "ad_id": 5000000000005,
                    "asin": "A00AAAA0AL",
                    "msku": "000aa*2X",
                    "state": "paused",
                    "status": "AD_PAUSED",
                    "create_time_ts": 1600853070000,
                    "update_time_ts": 1696439612959,
                },
            ],
        ],
    )


# . SD Targets
class SdTarget(BaseModel):
    """SD 目标商品投放"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000007],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000033],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000106],
    )
    target_id: int = Field(
        description="目标商品广告ID",
        examples=[300000000015],
    )
    expression_type: str = Field(
        description="目标定位类型",
        examples=["manual"],
    )
    expression: str = Field(
        description="目标定位表达式 (JSON 字符串)",
        examples=['[{"type": "asinSameAs", "value": "A00AAAAABI"}]'],
    )
    expression_resolved: str = Field(
        description="目标定位解析表达式 (JSON 字符串) [原字段 'resolved_expression']",
        examples=['[{"type": "asinSameAs", "value": "A00AAAAABI"}]'],
        # - - - - - - - - - -
        validation_alias="resolved_expression",
    )
    bid: FloatOrNone2Zero = Field(
        description="竞价",
        examples=[0.3],
    )
    state: StrOrNone2Blank = Field(
        description="广告状态",
        examples=["enabled"],
    )
    status: StrOrNone2Blank = Field(
        description="服务状态 [原字段 'serving_status']",
        examples=["CAMPAIGN_PAUSED"],
        # - - - - - - - - - -
        validation_alias="serving_status",
    )
    create_time_ts: IntOrNone2Zero = Field(
        description="创建时间 (UTC毫秒时间戳) [原字段 'creation_date']",
        examples=[1601344253000],
        # - - - - - - - - - -
        validation_alias="creation_date",
    )
    update_time_ts: IntOrNone2Zero = Field(
        description="更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']",
        examples=[1601344253000],
        # - - - - - - - - - -
        validation_alias="last_updated_date",
    )


class SdTargets(ResponseV1Token):
    """SD 目标商品投放列表"""

    data: list[SdTarget] = Field(
        description="SD 目标商品投放列表",
        examples=[
            [
                {
                    "profile_id": 90000000000007,
                    "campaign_id": 700000000000033,
                    "ad_group_id": 600000000000106,
                    "target_id": 300000000015,
                    "expression_type": "manual",
                    "expression": '[{"type": "asinSameAs", "value": "A00AAAAABI"}]',
                    "expression_resolved": '[{"type": "asinSameAs", "value": "A00AAAAABI"}]',
                    "bid": 0.3,
                    "state": "enabled",
                    "status": "CAMPAIGN_PAUSED",
                    "create_time_ts": 1601344253000,
                    "update_time_ts": 1601344253000,
                },
            ],
        ],
    )


# . SD Negative Targets
class SdNegativeTarget(BaseModel):
    """SD 否定目标商品投放"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[900000000000001],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[70000000000159],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000057],
    )
    negative_target_id: int = Field(
        description="否定目标ID [原字段 'target_id']",
        examples=[30000000000020],
        # - - - - - - - - - -
        validation_alias="target_id",
    )
    negative_expression: str = Field(
        description="否定定位表达式 (JSON 字符串) [原字段 'expression']",
        examples=['[{"type": "asinSameAs", "value": "A00AA0AAFV"}]'],
        # - - - - - - - - - -
        validation_alias="expression",
    )
    negative_expression_resolved: str = Field(
        description="否定定位解析表达式 (JSON 字符串) [原字段 'resolved_expression']",
        examples=['[{"type": "asinSameAs", "value": "A00AA0AAFV"}]'],
        # - - - - - - - - - -
        validation_alias="resolved_expression",
    )
    negative_expression_type: StrOrNone2Blank = Field(
        description="否定定位类型 [原字段 'expression_type']",
        examples=["manual"],
        # - - - - - - - - - -
        validation_alias="expression_type",
    )
    state: StrOrNone2Blank = Field(
        description="广告状态",
        examples=["enabled"],
    )
    status: StrOrNone2Blank = Field(
        description="服务状态 [原字段 'serving_status']",
        examples=["CAMPAIGN_PAUSED"],
        # - - - - - - - - - -
        validation_alias="serving_status",
    )
    create_time_ts: IntOrNone2Zero = Field(
        description="创建时间 (UTC毫秒时间戳) [原字段 'creation_date']",
        examples=[1659405193284],
        # - - - - - - - - - -
        validation_alias="creation_date",
    )
    update_time_ts: IntOrNone2Zero = Field(
        description="更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']",
        examples=[1659405193284],
        # - - - - - - - - - -
        validation_alias="last_updated_date",
    )


class SdNegativeTargets(ResponseV1Token):
    """SD 否定目标商品投放列表"""

    data: list[SdNegativeTarget] = Field(
        description="SD 否定目标商品投放列表",
        examples=[
            [
                {
                    "profile_id": 900000000000001,
                    "campaign_id": 70000000000159,
                    "ad_group_id": 600000000000057,
                    "negative_target_id": 30000000000020,
                    "negative_expression": '[{"type": "asinSameAs", "value": "A00AA0AAFV"}]',
                    "negative_expression_resolved": '[{"type": "asinSameAs", "value": "A00AA0AAFV"}]',
                    "negative_expression_type": "manual",
                    "state": "enabled",
                    "status": "CAMPAIGN_PAUSED",
                    "create_time_ts": 1659405193284,
                    "update_time_ts": 1659405193284,
                },
            ],
        ],
    )


# 报告 -------------------------------------------------------------------------------------------------------------------------
# 报告 - Sponsored Products - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# . SP Campaign Reports
class SpCampaignReport(BaseModel):
    """SP 广告活动报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000007],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[70000000000204],
    )
    targeting_type: StrOrNone2Blank = Field(
        description="投放目标类型",
        examples=[""],
    )
    cost: float = Field(
        description="广告花费",
        examples=[1.5],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[177],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[1],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[1],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[1],
    )
    direct_units: int = Field(
        description="直接广告成交商品件数 [原字段 'same_units']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="same_units",
    )
    sales: float = Field(
        description="广告销售额",
        examples=[16.66],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[16.66],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SpCampaignReports(ResponseV1Token):
    """SP 广告活动报告列表"""

    data: list[SpCampaignReport] = Field(
        description="SP 广告活动报告列表",
        examples=[
            [
                {
                    "profile_id": 90000000000007,
                    "campaign_id": 70000000000204,
                    "targeting_type": "",
                    "cost": 1.5,
                    "impressions": 177,
                    "clicks": 1,
                    "orders": 1,
                    "direct_orders": 1,
                    "units": 1,
                    "direct_units": 1,
                    "sales": 16.66,
                    "direct_sales": 16.66,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SP Campaign Hour Data
class SpCampaignHour(BaseModel):
    """SP 广告活动小时数据"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000007],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[70000000000204],
    )
    cost: float = Field(
        description="广告花费",
        examples=[1.5],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[1],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[1],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[1],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[1],
    )
    direct_units: int = Field(
        description="直接广告成交商品件数 [原字段 'same_units']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="same_units",
    )
    sales: float = Field(
        description="广告销售额",
        examples=[16.66],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[16.66],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    ctr: FloatOrNone2Zero = Field(
        description="点击率 - Click Through Rate (总点击次数 / 总展示次数)",
        examples=[0.0833],
    )
    cvr: FloatOrNone2Zero = Field(
        description="转化率 - Conversion Rate (广告订单数 / 总点击次数)",
        examples=[1.0],
    )
    cpc: FloatOrNone2Zero = Field(
        description="平均点击花费 - Cost Per Click (广告花费 / 总点击次数)",
        examples=[1.5],
    )
    cpa: FloatOrNone2Zero = Field(
        description="平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)",
        examples=[1.5],
    )
    acos: FloatOrNone2Zero = Field(
        description="广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)",
        examples=[0.09],
    )
    roas: FloatOrNone2Zero = Field(
        description="广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)",
        examples=[11.11],
    )
    hour: int = Field(
        description="数据所属小时 (0-23)",
        examples=[0],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SpCampaignHourData(ResponseV1):
    """SP 广告活动小时数据列表"""

    data: list[SpCampaignHour] = Field(
        description="SP 广告活动小时数据列表",
        examples=[
            [
                {
                    "profile_id": 90000000000004,
                    "campaign_id": 70000000000006,
                    "cost": 1.5,
                    "impressions": 12,
                    "clicks": 1,
                    "orders": 1,
                    "direct_orders": 1,
                    "units": 1,
                    "direct_units": 1,
                    "sales": 16.66,
                    "direct_sales": 16.66,
                    "ctr": 0.0833,
                    "cvr": 1.0,
                    "cpc": 1.5,
                    "cpa": 1.5,
                    "acos": 0.09,
                    "roas": 11.11,
                    "hour": 20,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SP Placement Reports
class SpCampaignReport(BaseModel):
    """SP 广告活动投放位置报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000007],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000083],
    )
    placement: str = Field(
        description="广告投放位置 [原字段 'placement_type']",
        examples=["OTHER ON-AMAZON"],
        # - - - - - - - - - -
        validation_alias="placement_type",
    )
    cost: float = Field(
        description="广告花费",
        examples=[1.35],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[24],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[1],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[1],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[1],
    )
    direct_units: int = Field(
        description="直接广告成交商品件数 [原字段 'same_units']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="same_units",
    )
    sales: float = Field(
        description="广告销售额",
        examples=[19.77],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[19.77],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SpPlacementReports(ResponseV1Token):
    """SP 广告活动投放位置报告列表"""

    data: list[SpCampaignReport] = Field(
        description="SP 广告活动投放位置报告列表",
        examples=[
            [
                {
                    "profile_id": 90000000000004,
                    "campaign_id": 700000000000008,
                    "placement": "OTHER ON-AMAZON",
                    "cost": 1.35,
                    "impressions": 19,
                    "clicks": 1,
                    "orders": 1,
                    "direct_orders": 1,
                    "units": 1,
                    "direct_units": 1,
                    "sales": 19.77,
                    "direct_sales": 19.77,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SP Placement Hour Data
class SpPlacementHour(BaseModel):
    """SP 广告活动投放位置小时数据"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000007],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[70000000000204],
    )
    placement: str = Field(
        description="广告投放位置",
        examples=["Other on-Amazon"],
    )
    cost: float = Field(
        description="广告花费",
        examples=[1.5],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[1],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[1],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[1],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[1],
    )
    direct_units: int = Field(
        description="直接广告成交商品件数 [原字段 'same_units']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="same_units",
    )
    sales: float = Field(
        description="广告销售额",
        examples=[16.66],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[16.66],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    ctr: FloatOrNone2Zero = Field(
        description="点击率 - Click Through Rate (总点击次数 / 总展示次数)",
        examples=[0.2],
    )
    cvr: FloatOrNone2Zero = Field(
        description="转化率 - Conversion Rate (广告订单数 / 总点击次数)",
        examples=[1.0],
    )
    cpc: FloatOrNone2Zero = Field(
        description="平均点击花费 - Cost Per Click (广告花费 / 总点击次数)",
        examples=[1.5],
    )
    cpa: FloatOrNone2Zero = Field(
        description="平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)",
        examples=[1.5],
    )
    acos: FloatOrNone2Zero = Field(
        description="广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)",
        examples=[0.09],
    )
    roas: FloatOrNone2Zero = Field(
        description="广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)",
        examples=[11.11],
    )
    hour: int = Field(
        description="数据所属小时 (0-23)",
        examples=[0],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SpPlacementHourData(ResponseV1):
    """SP 广告活动投放位置小时数据列表"""

    data: list[SpPlacementHour] = Field(
        description="SP 广告活动投放位置小时数据列表",
        examples=[
            [
                {
                    "profile_id": 90000000000004,
                    "campaign_id": 70000000000006,
                    "placement": "Other on-Amazon",
                    "cost": 1.5,
                    "impressions": 5,
                    "clicks": 1,
                    "orders": 1,
                    "direct_orders": 1,
                    "units": 1,
                    "direct_units": 1,
                    "sales": 16.66,
                    "direct_sales": 16.66,
                    "ctr": 0.2,
                    "cvr": 1.0,
                    "cpc": 1.5,
                    "cpa": 1.5,
                    "acos": 0.09,
                    "roas": 11.11,
                    "hour": 20,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SP Ad Group Reports
class SpAdGroupReport(BaseModel):
    """SP 广告组报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000007],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000083],
    )
    ad_group_id: int = Field(
        description="广告组ID",
        examples=[60000000000319],
    )
    cost: float = Field(
        description="广告花费",
        examples=[2.64],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[36],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[2],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[2],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[2],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[2],
    )
    direct_units: int = Field(
        description="直接广告成交商品件数 [原字段 'same_units']",
        examples=[2],
        # - - - - - - - - - -
        validation_alias="same_units",
    )
    sales: float = Field(
        description="广告销售额",
        examples=[33.32],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[33.32],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SpAdGroupReports(ResponseV1Token):
    """SP 广告组报告列表"""

    data: list[SpAdGroupReport] = Field(
        description="SP 广告组报告列表",
        examples=[
            [
                {
                    "profile_id": 90000000000004,
                    "campaign_id": 70000000000011,
                    "ad_group_id": 600000000000001,
                    "cost": 2.64,
                    "impressions": 1106,
                    "clicks": 2,
                    "orders": 2,
                    "direct_orders": 2,
                    "units": 2,
                    "direct_units": 2,
                    "sales": 33.32,
                    "direct_sales": 33.32,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SP Ad Group Hour Data
class SpAdGroupHour(BaseModel):
    """SP 广告组小时数据"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000007],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[70000000000204],
    )
    ad_group_id: int = Field(
        description="广告组ID [原字段 'group_id']",
        examples=[600000000000150],
        # - - - - - - - - - -
        validation_alias="group_id",
    )
    cost: float = Field(
        description="广告花费",
        examples=[1.5],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[1],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[1],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[1],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[1],
    )
    direct_units: int = Field(
        description="直接广告成交商品件数 [原字段 'same_units']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="same_units",
    )
    sales: float = Field(
        description="广告销售额",
        examples=[16.66],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[16.66],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    ctr: FloatOrNone2Zero = Field(
        description="点击率 - Click Through Rate (总点击次数 / 总展示次数)",
        examples=[0.0833],
    )
    cvr: FloatOrNone2Zero = Field(
        description="转化率 - Conversion Rate (广告订单数 / 总点击次数)",
        examples=[1.0],
    )
    cpc: FloatOrNone2Zero = Field(
        description="平均点击花费 - Cost Per Click (广告花费 / 总点击次数)",
        examples=[1.5],
    )
    cpa: FloatOrNone2Zero = Field(
        description="平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)",
        examples=[1.5],
    )
    acos: FloatOrNone2Zero = Field(
        description="广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)",
        examples=[0.09],
    )
    roas: FloatOrNone2Zero = Field(
        description="广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)",
        examples=[11.11],
    )
    hour: int = Field(
        description="数据所属小时 (0-23)",
        examples=[0],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SpAdGroupHourData(ResponseV1):
    """SP 广告组小时数据列表"""

    data: list[SpAdGroupHour] = Field(
        description="SP 广告组小时数据列表",
        examples=[
            [
                {
                    "profile_id": 90000000000004,
                    "campaign_id": 70000000000006,
                    "ad_group_id": 600000000000002,
                    "cost": 1.5,
                    "impressions": 12,
                    "clicks": 1,
                    "orders": 1,
                    "direct_orders": 1,
                    "units": 1,
                    "direct_units": 1,
                    "sales": 16.66,
                    "direct_sales": 16.66,
                    "ctr": 0.0833,
                    "cvr": 1.0,
                    "cpc": 1.5,
                    "cpa": 1.5,
                    "acos": 0.09,
                    "roas": 11.11,
                    "hour": 20,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SP Product Reports
class SpProductReport(BaseModel):
    """SP 商品投放报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000007],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[70000000000305],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000013],
    )
    ad_id: int = Field(
        description="商品广告ID",
        examples=[500000000000003],
    )
    asin: str = Field(
        description="商品ASIN",
        examples=["A0AAAA0A7X"],
    )
    msku: str = Field(
        description="亚马逊SKU [原字段 'sku']",
        examples=["AA-000*3M"],
        # - - - - - - - - - -
        validation_alias="sku",
    )
    cost: float = Field(
        description="广告花费",
        examples=[2.64],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[1106],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[2],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[2],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[2],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[2],
    )
    direct_units: int = Field(
        description="直接广告成交商品件数 [原字段 'same_units']",
        examples=[2],
        # - - - - - - - - - -
        validation_alias="same_units",
    )
    sales: float = Field(
        description="广告销售额",
        examples=[33.32],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[33.32],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SpProductReports(ResponseV1Token):
    """SP 商品投放报告列表"""

    data: list[SpProductReport] = Field(
        description="SP 商品投放报告列表",
        examples=[
            [
                {
                    "profile_id": 90000000000007,
                    "campaign_id": 70000000000305,
                    "ad_group_id": 600000000000013,
                    "ad_id": 500000000000003,
                    "asin": "A0AAAA0A7X",
                    "msku": "AA-000*3M",
                    "cost": 2.64,
                    "impressions": 1106,
                    "clicks": 2,
                    "orders": 2,
                    "direct_orders": 2,
                    "units": 2,
                    "direct_units": 2,
                    "sales": 33.32,
                    "direct_sales": 33.32,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# , SP Product Hour Data
class SpProductHour(BaseModel):
    """SP 商品投放小时数据"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000007],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[70000000000204],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID [原字段 'group_id']",
        examples=[600000000000150],
        # - - - - - - - - - -
        validation_alias="group_id",
    )
    ad_id: int = Field(
        description="商品广告ID",
        examples=[500000000000005],
    )
    asin: str = Field(
        description="商品ASIN",
        examples=["A0AAAA0A7X"],
    )
    msku: str = Field(
        description="亚马逊SKU",
        examples=["AA-000*3M"],
    )
    cost: float = Field(
        description="广告花费",
        examples=[1.5],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[11],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[1],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[1],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[1],
    )
    direct_units: int = Field(
        description="直接广告成交商品件数 [原字段 'same_units']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="same_units",
    )
    sales: float = Field(
        description="广告销售额",
        examples=[16.66],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[16.66],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    ctr: FloatOrNone2Zero = Field(
        description="点击率 - Click Through Rate (总点击次数 / 总展示次数)",
        examples=[0.0833],
    )
    cvr: FloatOrNone2Zero = Field(
        description="转化率 - Conversion Rate (广告订单数 / 总点击次数)",
        examples=[1.0],
    )
    cpc: FloatOrNone2Zero = Field(
        description="平均点击花费 - Cost Per Click (广告花费 / 总点击次数)",
        examples=[1.5],
    )
    cpa: FloatOrNone2Zero = Field(
        description="平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)",
        examples=[1.5],
    )
    acos: FloatOrNone2Zero = Field(
        description="广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)",
        examples=[0.09],
    )
    roas: FloatOrNone2Zero = Field(
        description="广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)",
        examples=[11.11],
    )
    hour: int = Field(
        description="数据所属小时 (0-23)",
        examples=[8],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SpProductHourData(ResponseV1):
    """SP 商品投放小时数据列表"""

    data: list[SpProductHour] = Field(
        description="SP 商品投放小时数据列表",
        examples=[
            [
                {
                    "profile_id": 90000000000004,
                    "campaign_id": 70000000000006,
                    "ad_group_id": 600000000000002,
                    "ad_id": 500000000000002,
                    "asin": "A0AAAA0A0F",
                    "msku": "AA-000*0C",
                    "cost": 1.5,
                    "impressions": 12,
                    "clicks": 1,
                    "orders": 1,
                    "direct_orders": 1,
                    "units": 1,
                    "direct_units": 1,
                    "sales": 16.66,
                    "direct_sales": 16.66,
                    "ctr": 0.0833,
                    "cvr": 1.0,
                    "cpc": 1.5,
                    "cpa": 1.5,
                    "acos": 0.09,
                    "roas": 11.11,
                    "hour": 20,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SP Keyword Reports
class SpKeywordReport(BaseModel):
    """SP 手动关键词投放报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000007],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000083],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[60000000000319],
    )
    keyword_id: int = Field(
        description="关键词ID",
        examples=[4000000000012],
    )
    keyword_text: StrOrNone2Blank = Field(
        description="关键词文本",
        examples=["aa 000cb"],
    )
    match_type: StrOrNone2Blank = Field(
        description="关键词匹配类型",
        examples=["EXACT"],
    )
    cost: float = Field(
        description="广告花费",
        examples=[0.0],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[4],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[0],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[0],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[0],
    )
    direct_units: int = Field(
        description="直接广告成交商品件数 [原字段 'same_units']",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="same_units",
    )
    sales: float = Field(
        description="广告销售额",
        examples=[0.0],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[0.0],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SpKeywordReports(ResponseV1Token):
    """SP 手动关键词投放报告列表"""

    data: list[SpKeywordReport] = Field(
        description="SP 手动关键词投放报告列表",
        examples=[
            [
                {
                    "profile_id": 90000000000007,
                    "campaign_id": 700000000000083,
                    "ad_group_id": 60000000000319,
                    "keyword_id": 4000000000012,
                    "keyword_text": "aa 000cb",
                    "match_type": "EXACT",
                    "cost": 0.0,
                    "impressions": 4,
                    "clicks": 0,
                    "orders": 0,
                    "direct_orders": 0,
                    "units": 0,
                    "direct_units": 0,
                    "sales": 0.0,
                    "direct_sales": 0.0,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SP Keyword Hour Data
class SpKeywordHour(BaseModel):
    """SP 手动关键词投放小时数据"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000007],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[70000000000204],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID [原字段 'group_id']",
        examples=[600000000000150],
        # - - - - - - - - - -
        validation_alias="group_id",
    )
    ad_id: int = Field(
        description="商品广告ID",
        examples=[500000000000005],
    )
    keyword_id: int = Field(
        description="关键词ID [原字段 'targeting_id']",
        examples=[40000000000050],
        # - - - - - - - - - -
        validation_alias="targeting_id",
    )
    keyword_text: StrOrNone2Blank = Field(
        description="关键词文本 [原字段 'targeting']",
        examples=["000 aaaaj"],
        # - - - - - - - - - -
        validation_alias="targeting",
    )
    match_type: StrOrNone2Blank = Field(
        description="关键词匹配类型",
        examples=["BROAD"],
    )
    asin: str = Field(
        description="商品ASIN",
        examples=["A0AAAA0A7X"],
    )
    msku: str = Field(
        description="亚马逊SKU",
        examples=["AA-000*3M"],
    )
    cost: float = Field(
        description="广告花费",
        examples=[1.5],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[8],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[1],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[1],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[1],
    )
    direct_units: int = Field(
        description="直接广告成交商品件数 [原字段 'same_units']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="same_units",
    )
    sales: float = Field(
        description="广告销售额",
        examples=[16.66],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[16.66],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    ctr: FloatOrNone2Zero = Field(
        description="点击率 - Click Through Rate (总点击次数 / 总展示次数)",
        examples=[0.0833],
    )
    cvr: FloatOrNone2Zero = Field(
        description="转化率 - Conversion Rate (广告订单数 / 总点击次数)",
        examples=[1.0],
    )
    cpc: FloatOrNone2Zero = Field(
        description="平均点击花费 - Cost Per Click (广告花费 / 总点击次数)",
        examples=[1.5],
    )
    cpa: FloatOrNone2Zero = Field(
        description="平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)",
        examples=[1.5],
    )
    acos: FloatOrNone2Zero = Field(
        description="广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)",
        examples=[0.09],
    )
    roas: FloatOrNone2Zero = Field(
        description="广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)",
        examples=[11.11],
    )
    hour: int = Field(
        description="数据所属小时 (0-23)",
        examples=[7],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SpKeywordHourData(ResponseV1):
    """SP 手动关键词投放小时数据列表"""

    data: list[SpKeywordHour] = Field(
        description="SP 手动关键词投放小时数据列表",
        examples=[
            [
                {
                    "profile_id": 90000000000004,
                    "campaign_id": 70000000000006,
                    "ad_group_id": 600000000000002,
                    "ad_id": 500000000000002,
                    "keyword_id": 40000000000006,
                    "keyword_text": "000 aaaac",
                    "match_type": "BROAD",
                    "asin": "A0AAAA0A0F",
                    "msku": "AA-000*0C",
                    "cost": 1.5,
                    "impressions": 12,
                    "clicks": 1,
                    "orders": 1,
                    "direct_orders": 1,
                    "units": 1,
                    "direct_units": 1,
                    "sales": 16.66,
                    "direct_sales": 16.66,
                    "ctr": 0.0833,
                    "cvr": 1.0,
                    "cpc": 1.5,
                    "cpa": 1.5,
                    "acos": 0.09,
                    "roas": 11.11,
                    "hour": 20,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SP Target Reports
class SpTargetReport(BaseModel):
    """SP 自动投放/手动商品投放报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000007],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000227],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000287],
    )
    target_id: int = Field(
        description="自动投放/手动商品投放ID",
        examples=[3000000000027],
    )
    expression_type: StrOrNone2Blank = Field(
        description="投放匹配类型 [原字段 'targeting_type']",
        examples=["TARGETING_EXPRESSION"],
        # - - - - - - - - - -
        validation_alias="targeting_type",
    )
    expression: StrOrNone2Blank = Field(
        description="自动投放/手动商品投放表达式 (JSON 字符串)",
        examples=[
            '"[{\\"type\\": \\"asinExpandedFrom\\", \\"value\\": \\"0000000001\\"}]"'
        ],
        # - - - - - - - - - -
        validation_alias="targeting_expression",
    )
    cost: float = Field(
        description="广告花费",
        examples=[0.0],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[2],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[0],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[0],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[0],
    )
    direct_units: int = Field(
        description="直接广告成交商品件数 [原字段 'same_units']",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="same_units",
    )
    sales: float = Field(
        description="广告销售额",
        examples=[0.0],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[0.0],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SpTargetReports(ResponseV1Token):
    """SP 自动投放/手动商品投放报告列表"""

    data: list[SpTargetReport] = Field(
        description="SP 自动投放/手动商品投放报告列表",
        examples=[
            [
                {
                    "profile_id": 90000000000007,
                    "campaign_id": 700000000000227,
                    "ad_group_id": 600000000000287,
                    "target_id": 3000000000027,
                    "expression_type": "TARGETING_EXPRESSION",
                    "expression": '"[{\\"type\\": \\"asinExpandedFrom\\", \\"value\\": \\"0000000001\\"}]"',
                    "cost": 0.0,
                    "impressions": 2,
                    "clicks": 0,
                    "orders": 0,
                    "direct_orders": 0,
                    "units": 0,
                    "direct_units": 0,
                    "sales": 0.0,
                    "direct_sales": 0.0,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SP Target Hour Data
class SpTargetHour(BaseModel):
    """SP投放小时数据"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000007],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[70000000000204],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID [原字段 'group_id']",
        examples=[600000000000150],
        # - - - - - - - - - -
        validation_alias="group_id",
    )
    ad_id: int = Field(
        description="商品广告ID",
        examples=[500000000000005],
    )
    target_id: int = Field(
        description="投放ID [原字段 'targeting_id']",
        examples=[40000000000050],
        # - - - - - - - - - -
        validation_alias="targeting_id",
    )
    target_text: StrOrNone2Blank = Field(
        description="投放文本 [原字段 'targeting']",
        examples=["000 aaaaj"],
        # - - - - - - - - - -
        validation_alias="targeting",
    )
    target_type: StrOrNone2Blank = Field(
        description="投放匹配类型 [原字段 'match_type']",
        examples=["BROAD"],
        # - - - - - - - - - -
        validation_alias="match_type",
    )
    asin: str = Field(
        description="商品ASIN",
        examples=["A0AAAA0A7X"],
    )
    msku: str = Field(
        description="亚马逊SKU",
        examples=["AA-000*3M"],
    )
    cost: float = Field(
        description="广告花费",
        examples=[1.5],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[13],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[1],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[1],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[1],
    )
    direct_units: int = Field(
        description="直接广告成交商品件数 [原字段 'same_units']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="same_units",
    )
    sales: float = Field(
        description="广告销售额",
        examples=[16.66],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[16.66],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    ctr: FloatOrNone2Zero = Field(
        description="点击率 - Click Through Rate (总点击次数 / 总展示次数)",
        examples=[0.0833],
    )
    cvr: FloatOrNone2Zero = Field(
        description="转化率 - Conversion Rate (广告订单数 / 总点击次数)",
        examples=[1.0],
    )
    cpc: FloatOrNone2Zero = Field(
        description="平均点击花费 - Cost Per Click (广告花费 / 总点击次数)",
        examples=[1.5],
    )
    cpa: FloatOrNone2Zero = Field(
        description="平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)",
        examples=[1.5],
    )
    acos: FloatOrNone2Zero = Field(
        description="广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)",
        examples=[0.09],
    )
    roas: FloatOrNone2Zero = Field(
        description="广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)",
        examples=[11.11],
    )
    hour: int = Field(
        description="数据所属小时 (0-23)",
        examples=[19],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SpTargetHourData(ResponseV1):
    """SP投放小时数据列表"""

    data: list[SpTargetHour] = Field(
        description="SP投放小时数据列表",
        examples=[
            [
                {
                    "profile_id": 90000000000004,
                    "campaign_id": 70000000000006,
                    "ad_group_id": 600000000000002,
                    "ad_id": 500000000000002,
                    "target_id": 40000000000006,
                    "target_text": "000 aaaac",
                    "target_type": "BROAD",
                    "asin": "A0AAAA0A0F",
                    "msku": "AA-000*0C",
                    "cost": 1.5,
                    "impressions": 12,
                    "clicks": 1,
                    "orders": 1,
                    "direct_orders": 1,
                    "units": 1,
                    "direct_units": 1,
                    "sales": 16.66,
                    "direct_sales": 16.66,
                    "ctr": 0.0833,
                    "cvr": 1.0,
                    "cpc": 1.5,
                    "cpa": 1.5,
                    "acos": 0.09,
                    "roas": 11.11,
                    "hour": 20,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SP Query Keyword Reports
class SpQueryBaseReport(BaseModel):
    """SP 用户搜索词基础报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000007],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000215],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000183],
    )
    query_text: str = Field(
        description="用户使用搜索词 [原字段 'query']",
        examples=["aa 008"],
        # - - - - - - - - - -
        validation_alias="query",
    )
    cost: float = Field(
        description="广告花费",
        examples=[1.35],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[1],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[1],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[1],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[1],
    )
    direct_units: int = Field(
        description="直接广告成交商品件数 [原字段 'same_units']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="same_units",
    )
    sales: float = Field(
        description="广告销售额",
        examples=[19.77],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[19.77],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SpKeywordQueryReport(SpQueryBaseReport):
    """SP 手动关键词的用户搜索词报告"""

    keyword_id: int = Field(
        description="关键词ID [原字段 'target_id']",
        examples=[400000000000003],
        # - - - - - - - - - -
        validation_alias="target_id",
    )
    keyword_text: StrOrNone2Blank = Field(
        description="关键词文本 [原字段 'target_text']",
        examples=["aa 0043"],
        # - - - - - - - - - -
        validation_alias="target_text",
    )
    match_type: StrOrNone2Blank = Field(
        description="关键词匹配类型",
        examples=["BROAD"],
    )


class SpKeywordQueryReports(ResponseV1Token):
    """SP 手动关键词的用户搜索词报告列表"""

    data: list[SpKeywordQueryReport] = Field(
        description="SP 手动关键词的用户搜索词报告列表",
        examples=[
            [
                {
                    "profile_id": 90000000000007,
                    "campaign_id": 700000000000215,
                    "ad_group_id": 600000000000183,
                    "query_text": "aa 008",
                    "cost": 1.35,
                    "impressions": 1,
                    "clicks": 1,
                    "orders": 1,
                    "direct_orders": 1,
                    "units": 1,
                    "direct_units": 1,
                    "sales": 19.77,
                    "direct_sales": 19.77,
                    "report_date": "2026-10-01",
                    "keyword_id": 400000000000003,
                    "keyword_text": "aa 0043",
                    "match_type": "BROAD",
                }
            ]
        ],
    )


# . SP Query Target Reports
class SpTargetQueryReport(SpQueryBaseReport):
    """SP 自动投放/手动商品投的用户搜索词报告"""

    target_id: int = Field(
        description="自动投放/手动商品投放ID",
        examples=[30000000000034],
    )
    expression: StrOrNone2Blank = Field(
        description="自动投放/手动商品投放表达式 (JSON 字符串) [原字段 'target_text']",
        examples=['"[{\\"type\\": \\"queryBroadRelMatches\\"}]"'],
        # - - - - - - - - - -
        validation_alias="target_text",
    )
    match_type: StrOrNone2Blank = Field(
        description="投放匹配类型",
        examples=[""],
    )


class SpTargetQueryReports(ResponseV1Token):
    """SP 自动投放/手动商品投的用户搜索词报告列表"""

    data: list[SpTargetQueryReport] = Field(
        description="SP 自动投放/手动商品投的用户搜索词报告列表",
        examples=[
            [
                {
                    "profile_id": 90000000000004,
                    "campaign_id": 700000000000007,
                    "ad_group_id": 600000000000003,
                    "query_text": "000 aaaaaaa aab",
                    "cost": 1.6,
                    "impressions": 2,
                    "clicks": 1,
                    "orders": 1,
                    "direct_orders": 1,
                    "units": 1,
                    "direct_units": 1,
                    "sales": 16.66,
                    "direct_sales": 16.66,
                    "report_date": "2026-10-01",
                    "target_id": 30000000000004,
                    "expression": '"[{\\"type\\": \\"keywordGroupSameAs\\", \\"value\\": \\"category\\"}]"',
                    "match_type": "",
                }
            ]
        ],
    )


# 报告 - Sponsored Brands - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# . SB Campaign Reports
class SbCampaignReport(BaseModel):
    """SB 广告活动报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[900000000000002],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[70000000000373],
    )
    cost: float = Field(
        description="广告花费",
        examples=[10.98],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[187],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[2],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[1],
    )
    direct_orders: int = Field(
        description='直接广告订单数 [原字段 "same_orders"]',
        examples=[1],
        validation_alias="same_orders",
    )
    new_to_brand_orders: int = Field(
        description="品牌新买家广告订单数",
        examples=[1],
    )
    new_to_brand_order_pct: FloatOrNone2Zero = Field(
        description='品牌新买家订单占比 [原字段 "new_to_brand_order_percentage"] (品牌新买家广告订单数 / 广告订单数 x 100%)',
        examples=[100.0],
        validation_alias="new_to_brand_order_percentage",
    )
    new_to_brand_order_rate: FloatOrNone2Zero = Field(
        description="品牌新买家订单转化率 (品牌新买家广告订单数 / 总点击次数 x 100%)",
        examples=[0.0],
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[1],
    )
    direct_units: IntOrNone2Zero = Field(
        description='直接广告成交商品件数 [原字段 "same_units"]',
        examples=[0],
        validation_alias="same_units",
    )
    new_to_brand_units: int = Field(
        description="品牌新买家成交商品件数",
        examples=[1],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[38.99],
    )
    direct_sales: float = Field(
        description='直接广告销售额 [原字段 "same_sales"]',
        examples=[38.99],
        validation_alias="same_sales",
    )
    new_to_brand_sales: float = Field(
        description="品牌新买家销售额",
        examples=[38.99],
    )
    vtr: FloatOrNone2Zero = Field(
        description="广告可见率 - View Through Rate (可见展示次数 / 总展示次数 x 100%)",
        examples=[0.0],
    )
    vctr: FloatOrNone2Zero = Field(
        description="广告可见点击率 - View Click Through Rate (总点击次数 / 可见展示次数 x 100%)",
        examples=[0.0],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )
    # fmt: on


class SbCampaignReports(ResponseV1Token):
    """SB 广告活动报告列表"""

    data: list[SbCampaignReport] = Field(
        description="SB广告活动日报数据",
        examples=[
            [
                {
                    "profile_id": 900000000000001,
                    "campaign_id": 700000000000001,
                    "cost": 5.24,
                    "impressions": 126,
                    "clicks": 2,
                    "orders": 1,
                    "direct_orders": 1,
                    "new_to_brand_orders": 1,
                    "new_to_brand_order_pct": 100.0,
                    "new_to_brand_order_rate": 0.0,
                    "units": 1,
                    "direct_units": 0,
                    "new_to_brand_units": 1,
                    "sales": 38.99,
                    "direct_sales": 38.99,
                    "new_to_brand_sales": 38.99,
                    "vtr": 0.0,
                    "vctr": 0.0,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SB Campaign Hour Data
class SbCampaignHour(BaseModel):
    """SB 广告活动小时数据"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[900000000000002],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[70000000000376],
    )
    cost: float = Field(
        description="广告花费",
        examples=[4.28],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[6],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[1],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[0],
    )
    direct_orders: int = Field(
        description='直接广告订单数 [原字段 "same_orders"]',
        examples=[0],
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[0],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[0.0],
    )
    direct_sales: float = Field(
        description='直接广告销售额 [原字段 "same_sales"]',
        examples=[0.0],
        validation_alias="same_sales",
    )
    ctr: FloatOrNone2Zero = Field(
        description="点击率 - Click Through Rate (总点击次数 / 总展示次数)",
        examples=[0.0149],
    )
    cvr: FloatOrNone2Zero = Field(
        description="转化率 - Conversion Rate (广告订单数 / 总点击次数)",
        examples=[0.0],
    )
    cpc: FloatOrNone2Zero = Field(
        description="平均点击花费 - Cost Per Click (广告花费 / 总点击次数)",
        examples=[4.28],
    )
    cpa: FloatOrNone2Zero = Field(
        description="平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)",
        examples=[0.0],
    )
    acos: FloatOrNone2Zero = Field(
        description="广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)",
        examples=[0.0],
    )
    roas: FloatOrNone2Zero = Field(
        description="广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)",
        examples=[0.0],
    )
    hour: int = Field(
        description="数据所属小时 (0-23)",
        examples=[1],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SbCampaignHourData(ResponseV1):
    """SB 广告活动小时数据列表"""

    data: list[SbCampaignHour] = Field(
        description="SB广告活动小时数据数据",
        examples=[
            [
                {
                    "profile_id": 900000000000001,
                    "campaign_id": 70000000000014,
                    "cost": 4.28,
                    "impressions": 67,
                    "clicks": 1,
                    "orders": 0,
                    "direct_orders": 0,
                    "units": 0,
                    "sales": 0.0,
                    "direct_sales": 0.0,
                    "ctr": 0.0149,
                    "cvr": 0.0,
                    "cpc": 4.28,
                    "cpa": 0.0,
                    "acos": 0.0,
                    "roas": 0.0,
                    "hour": 6,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SB Campaign Placement Reports
class SbPlacementReprot(BaseModel):
    """SB 广告活动投放位置报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[900000000000002],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000155],
    )
    placement: str = Field(
        description='广告投放位置 [原字段 "placement_type"]',
        examples=["Other on-Amazon"],
        validation_alias="placement_type",
    )
    creative_type: str = Field(
        description="广告创意类型；官方已作废，具体类型应查询SB广告创意的creative.type",
        examples=["all"],
    )
    cost: float = Field(
        description="广告花费",
        examples=[2.94],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[47],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[1],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[0],
    )
    new_to_brand_orders: IntOrNone2Zero = Field(
        description="品牌新买家广告订单数",
        examples=[0],
    )
    new_to_brand_order_pct: FloatOrNone2Zero = Field(
        description='品牌新买家订单占比 [原字段 "new_to_brand_order_percentage"] (品牌新买家广告订单数 / 广告订单数 x 100%)',
        examples=[0.0],
        validation_alias="new_to_brand_order_percentage",
    )
    new_to_brand_order_rate: FloatOrNone2Zero = Field(
        description="品牌新买家订单转化率 (品牌新买家广告订单数 / 总点击次数 x 100%)",
        examples=[0.0],
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[0],
    )
    direct_units: IntOrNone2Zero = Field(
        description='直接广告成交商品件数 [原字段 "same_units"]',
        examples=[0],
        validation_alias="same_units",
    )
    new_to_brand_units: int = Field(
        description="品牌新买家成交商品件数",
        examples=[0],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[0.0],
    )
    new_to_brand_sales: float = Field(
        description="品牌新买家销售额",
        examples=[0.0],
    )
    brand_searches: IntOrNone2Zero = Field(
        description='品牌搜索次数 [原字段 "branded_searches"]',
        examples=[0],
        validation_alias="branded_searches",
    )
    video_25pct_views: IntOrNone2Zero = Field(
        description='视频广告播放25%次数 [原字段 "videofirstquartileviews"]',
        examples=[0],
        validation_alias="videofirstquartileviews",
    )
    video_50pct_views: IntOrNone2Zero = Field(
        description='视频广告播放50%次数 [原字段 "videomidpointviews"]',
        examples=[0],
        validation_alias="videomidpointviews",
    )
    video_75pct_views: IntOrNone2Zero = Field(
        description='视频广告播放75%次数 [原字段 "videothirdquartileviews"]',
        examples=[0],
        validation_alias="videothirdquartileviews",
    )
    video_5sec_views: IntOrNone2Zero = Field(
        description='视频广告播放5秒次数 [原字段 "video5secondviews"]',
        examples=[0],
        validation_alias="video5secondviews",
    )
    video_5sec_view_rate: FloatOrNone2Zero = Field(
        description='视频广告播放5秒观看率 [原字段 "video5secondviewrate"]',
        examples=[0.0],
        validation_alias="video5secondviewrate",
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )
    # fmt: on


class SbPlacementReports(ResponseV1Token):
    """SB 广告活动投放位置报告列表"""

    data: list[SbPlacementReprot] = Field(
        description="SB广告活动广告位日报数据",
        examples=[
            [
                {
                    "profile_id": 900000000000002,
                    "campaign_id": 700000000000155,
                    "placement": "Other on-Amazon",
                    "creative_type": "all",
                    "cost": 2.94,
                    "impressions": 47,
                    "clicks": 1,
                    "orders": 0,
                    "new_to_brand_orders": 0,
                    "new_to_brand_order_pct": 0.0,
                    "new_to_brand_order_rate": 0.0,
                    "units": 0,
                    "direct_units": 0,
                    "new_to_brand_units": 0,
                    "sales": 0.0,
                    "new_to_brand_sales": 0.0,
                    "brand_searches": 0,
                    "video_25pct_views": 0,
                    "video_50pct_views": 0,
                    "video_75pct_views": 0,
                    "video_5sec_views": 0,
                    "video_5sec_view_rate": 0.0,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SB Campaign Placement Hour Data
class SbPlacementHour(BaseModel):
    """SB 广告活动投放位置小时数据"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[900000000000002],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[70000000000376],
    )
    placement: str = Field(
        description="广告投放位置",
        examples=["Other on-Amazon"],
    )
    cost: float = Field(
        description="广告花费",
        examples=[4.28],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[4],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[1],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[0],
    )
    direct_orders: int = Field(
        description='直接广告订单数 [原字段 "same_orders"]',
        examples=[0],
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[0],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[0.0],
    )
    direct_sales: float = Field(
        description='直接广告销售额 [原字段 "same_sales"]',
        examples=[0.0],
        validation_alias="same_sales",
    )
    ctr: FloatOrNone2Zero = Field(
        description="点击率 - Click Through Rate (总点击次数 / 总展示次数)",
        examples=[0.1111],
    )
    cvr: FloatOrNone2Zero = Field(
        description="转化率 - Conversion Rate (广告订单数 / 总点击次数)",
        examples=[0.0],
    )
    cpc: FloatOrNone2Zero = Field(
        description="平均点击花费 - Cost Per Click (广告花费 / 总点击次数)",
        examples=[4.28],
    )
    cpa: FloatOrNone2Zero = Field(
        description="平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)",
        examples=[0.0],
    )
    acos: FloatOrNone2Zero = Field(
        description="广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)",
        examples=[0.0],
    )
    roas: FloatOrNone2Zero = Field(
        description="广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)",
        examples=[0.0],
    )
    hour: int = Field(
        description="数据所属小时 (0-23)",
        examples=[1],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SbPlacementHourData(ResponseV1):
    """SB 广告活动投放位置小时数据列表"""

    data: list[SbPlacementHour] = Field(
        description="SB广告位小时数据数据",
        examples=[
            [
                {
                    "profile_id": 900000000000001,
                    "campaign_id": 70000000000014,
                    "placement": "Top of Search on-Amazon",
                    "cost": 4.28,
                    "impressions": 9,
                    "clicks": 1,
                    "orders": 0,
                    "direct_orders": 0,
                    "units": 0,
                    "sales": 0.0,
                    "direct_sales": 0.0,
                    "ctr": 0.1111,
                    "cvr": 0.0,
                    "cpc": 4.28,
                    "cpa": 0.0,
                    "acos": 0.0,
                    "roas": 0.0,
                    "hour": 6,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SB Ad Group Reports
class SbAdGroupReport(BaseModel):
    """SB 广告组报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[900000000000002],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000007],
    )
    ad_group_id: int = Field(
        description="广告组ID",
        examples=[600000000000233],
    )
    cost: float = Field(
        description="广告花费",
        examples=[3.28],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[7],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[3],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[1],
    )
    direct_orders: int = Field(
        description='直接广告订单数 [原字段 "same_orders"]',
        examples=[1],
        validation_alias="same_orders",
    )
    new_to_brand_orders: int = Field(
        description="品牌新买家广告订单数",
        examples=[1],
    )
    new_to_brand_order_pct: FloatOrNone2Zero = Field(
        description='品牌新买家订单占比 [原字段 "new_to_brand_order_percentage"] (品牌新买家广告订单数 / 广告订单数 x 100%)',
        examples=[100.0],
        validation_alias="new_to_brand_order_percentage",
    )
    new_to_brand_order_rate: FloatOrNone2Zero = Field(
        description="品牌新买家订单转化率 (品牌新买家广告订单数 / 总点击次数 x 100%)",
        examples=[0.0],
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[1],
    )
    direct_units: IntOrNone2Zero = Field(
        description='直接广告成交商品件数 [原字段 "same_units"]',
        examples=[0],
        validation_alias="same_units",
    )
    new_to_brand_units: int = Field(
        description="品牌新买家成交商品件数",
        examples=[1],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[38.99],
    )
    direct_sales: float = Field(
        description='直接广告销售额 [原字段 "same_sales"]',
        examples=[38.99],
        validation_alias="same_sales",
    )
    new_to_brand_sales: float = Field(
        description="品牌新买家销售额",
        examples=[38.99],
    )
    vtr: FloatOrNone2Zero = Field(
        description="广告可见率 - View Through Rate (可见展示次数 / 总展示次数 x 100%)",
        examples=[0.0],
    )
    vctr: FloatOrNone2Zero = Field(
        description="广告可见点击率 - View Click Through Rate (总点击次数 / 可见展示次数 x 100%)",
        examples=[0.0],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )
    # fmt: on


class SbAdGroupReports(ResponseV1Token):
    """SB 广告组报告列表"""

    data: list[SbAdGroupReport] = Field(
        description="SB广告组日报数据",
        examples=[
            [
                {
                    "profile_id": 900000000000001,
                    "campaign_id": 700000000000001,
                    "ad_group_id": 600000000000011,
                    "cost": 5.24,
                    "impressions": 126,
                    "clicks": 2,
                    "orders": 1,
                    "direct_orders": 1,
                    "new_to_brand_orders": 1,
                    "new_to_brand_order_pct": 100.0,
                    "new_to_brand_order_rate": 0.0,
                    "units": 1,
                    "direct_units": 0,
                    "new_to_brand_units": 1,
                    "sales": 38.99,
                    "direct_sales": 38.99,
                    "new_to_brand_sales": 38.99,
                    "vtr": 0.0,
                    "vctr": 0.0,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SB Ad Group Hour Data
class SbAdGroupHour(BaseModel):
    """SB 广告组小时数据"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[900000000000002],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[70000000000376],
    )
    ad_group_id: int = Field(
        description='广告组ID [原字段 "group_id"]',
        examples=[600000000000239],
        validation_alias="group_id",
    )
    cost: float = Field(
        description="广告花费",
        examples=[4.28],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[6],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[1],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[0],
    )
    direct_orders: int = Field(
        description='直接广告订单数 [原字段 "same_orders"]',
        examples=[0],
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[0],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[0.0],
    )
    direct_sales: float = Field(
        description='直接广告销售额 [原字段 "same_sales"]',
        examples=[0.0],
        validation_alias="same_sales",
    )
    ctr: FloatOrNone2Zero = Field(
        description="点击率 - Click Through Rate (总点击次数 / 总展示次数)",
        examples=[0.0149],
    )
    cvr: FloatOrNone2Zero = Field(
        description="转化率 - Conversion Rate (广告订单数 / 总点击次数)",
        examples=[0.0],
    )
    cpc: FloatOrNone2Zero = Field(
        description="平均点击花费 - Cost Per Click (广告花费 / 总点击次数)",
        examples=[4.28],
    )
    cpa: FloatOrNone2Zero = Field(
        description="平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)",
        examples=[0.0],
    )
    acos: FloatOrNone2Zero = Field(
        description="广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)",
        examples=[0.0],
    )
    roas: FloatOrNone2Zero = Field(
        description="广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)",
        examples=[0.0],
    )
    hour: int = Field(
        description="数据所属小时 (0-23)",
        examples=[1],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SbAdGroupHourData(ResponseV1):
    """SB 广告组小时数据列表"""

    data: list[SbAdGroupHour] = Field(
        description="SB广告组小时数据数据",
        examples=[
            [
                {
                    "profile_id": 900000000000001,
                    "campaign_id": 70000000000014,
                    "ad_group_id": 600000000000007,
                    "cost": 4.28,
                    "impressions": 67,
                    "clicks": 1,
                    "orders": 0,
                    "direct_orders": 0,
                    "units": 0,
                    "sales": 0.0,
                    "direct_sales": 0.0,
                    "ctr": 0.0149,
                    "cvr": 0.0,
                    "cpc": 4.28,
                    "cpa": 0.0,
                    "acos": 0.0,
                    "roas": 0.0,
                    "hour": 6,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SB Creative Reports
class SbCreativeReport(BaseModel):
    """SB 广告创意报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[900000000000002],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000007],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000233],
    )
    creative_id: int = Field(
        description='广告创意ID [原字段 "ad_creative_id"]',
        examples=[500000000000010],
        validation_alias="ad_creative_id",
    )
    cost: float = Field(
        description="广告花费",
        examples=[3.28],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[7],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[3],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[1],
    )
    direct_orders: int = Field(
        description='直接广告订单数 [原字段 "same_orders"]',
        examples=[1],
        validation_alias="same_orders",
    )
    new_to_brand_orders: int = Field(
        description="品牌新买家广告订单数",
        examples=[1],
    )
    new_to_brand_order_pct: FloatOrNone2Zero = Field(
        description='品牌新买家订单占比 [原字段 "new_to_brand_order_percentage"] (品牌新买家广告订单数 / 广告订单数 x 100%)',
        examples=[100.0],
        validation_alias="new_to_brand_order_percentage",
    )
    new_to_brand_order_rate: FloatOrNone2Zero = Field(
        description="品牌新买家订单转化率 (品牌新买家广告订单数 / 总点击次数 x 100%)",
        examples=[50.0],
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[1],
    )
    direct_units: IntOrNone2Zero = Field(
        description='直接广告成交商品件数 [原字段 "same_units"]',
        examples=[1],
        validation_alias="same_units",
    )
    new_to_brand_units: int = Field(
        description="品牌新买家成交商品件数",
        examples=[1],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[38.99],
    )
    direct_sales: float = Field(
        description='直接广告销售额 [原字段 "same_sales"]',
        examples=[38.99],
        validation_alias="same_sales",
    )
    new_to_brand_sales: float = Field(
        description="品牌新买家销售额",
        examples=[38.99],
    )
    vtr: FloatOrNone2Zero = Field(
        description="广告可见率 - View Through Rate (可见展示次数 / 总展示次数 x 100%)",
        examples=[100.0],
    )
    vctr: FloatOrNone2Zero = Field(
        description="广告可见点击率 - View Click Through Rate (总点击次数 / 可见展示次数 x 100%)",
        examples=[2.13],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )
    # fmt: on


class SbCreativeReports(ResponseV1Token):
    """SB 广告创意报告列表"""

    data: list[SbCreativeReport] = Field(
        description="SB广告创意日报数据",
        examples=[
            [
                {
                    "profile_id": 900000000000001,
                    "campaign_id": 700000000000001,
                    "ad_group_id": 600000000000011,
                    "creative_id": 500000000000001,
                    "cost": 5.24,
                    "impressions": 127,
                    "clicks": 2,
                    "orders": 1,
                    "direct_orders": 1,
                    "new_to_brand_orders": 1,
                    "new_to_brand_order_pct": 100.0,
                    "new_to_brand_order_rate": 50.0,
                    "units": 1,
                    "direct_units": 1,
                    "new_to_brand_units": 1,
                    "sales": 38.99,
                    "direct_sales": 38.99,
                    "new_to_brand_sales": 38.99,
                    "vtr": 22.83,
                    "vctr": 6.9,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SB Keyword Reports
class SbKeywordReport(BaseModel):
    """SB 关键词投放报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[900000000000002],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000155],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000283],
    )
    keyword_id: int = Field(
        description="关键词ID",
        examples=[4000000000032],
    )
    creative_type: str = Field(
        description="广告创意类型；官方已作废，具体类型应查询SB广告创意的creative.type",
        examples=["all"],
    )
    cost: float = Field(
        description="广告花费",
        examples=[2.05],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[2],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[1],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[0],
    )
    direct_orders: int = Field(
        description='直接广告订单数 [原字段 "same_orders"]',
        examples=[0],
        validation_alias="same_orders",
    )
    new_to_brand_orders: int = Field(
        description="品牌新买家广告订单数",
        examples=[0],
    )
    new_to_brand_order_pct: FloatOrNone2Zero = Field(
        description='品牌新买家订单占比 [原字段 "new_to_brand_order_percentage"] (品牌新买家广告订单数 / 广告订单数 x 100%)',
        examples=[0.0],
        validation_alias="new_to_brand_order_percentage",
    )
    new_to_brand_order_rate: FloatOrNone2Zero = Field(
        description="品牌新买家订单转化率 (品牌新买家广告订单数 / 总点击次数 x 100%)",
        examples=[0.0],
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[0],
    )
    direct_units: IntOrNone2Zero = Field(
        description='直接广告成交商品件数 [原字段 "same_units"]',
        examples=[0],
        validation_alias="same_units",
    )
    new_to_brand_units: int = Field(
        description="品牌新买家成交商品件数",
        examples=[0],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[0.0],
    )
    direct_sales: float = Field(
        description='直接广告销售额 [原字段 "same_sales"]',
        examples=[0.0],
        validation_alias="same_sales",
    )
    new_to_brand_sales: float = Field(
        description="品牌新买家销售额",
        examples=[0.0],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )
    # fmt: on


class SbKeywordReports(ResponseV1Token):
    """SB 关键词投放报告列表"""

    data: list[SbKeywordReport] = Field(
        description="SB关键词投放日报数据",
        examples=[
            [
                {
                    "profile_id": 90000000000005,
                    "campaign_id": 70000000000013,
                    "ad_group_id": 600000000000005,
                    "keyword_id": 400000000003,
                    "creative_type": "all",
                    "cost": 2.05,
                    "impressions": 91,
                    "clicks": 1,
                    "orders": 0,
                    "direct_orders": 0,
                    "new_to_brand_orders": 0,
                    "new_to_brand_order_pct": 0.0,
                    "new_to_brand_order_rate": 0.0,
                    "units": 0,
                    "direct_units": 0,
                    "new_to_brand_units": 0,
                    "sales": 0.0,
                    "direct_sales": 0.0,
                    "new_to_brand_sales": 0.0,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SB Keyword Query Reports
class SbKeywordQueryReport(BaseModel):
    """SB 关键词的用户搜索词报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[900000000000002],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[70000000000376],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000239],
    )
    query_text: str = Field(
        description='用户使用搜索词 [原字段 "query"]',
        examples=["aaa aaaaaaaaaa aaa aa aaaaaaaq"],
        validation_alias="query",
    )
    cost: float = Field(
        description="广告花费",
        examples=[4.28],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[9],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[1],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[1],
    )
    direct_orders: IntOrNone2Zero = Field(
        description='直接广告订单数 [原字段 "same_orders"]',
        examples=[0],
        validation_alias="same_orders",
    )
    new_to_brand_orders: IntOrNone2Zero = Field(
        description="品牌新买家广告订单数",
        examples=[0],
    )
    new_to_brand_order_pct: FloatOrNone2Zero = Field(
        description='品牌新买家订单占比 [原字段 "new_to_brand_order_percentage"] (品牌新买家广告订单数 / 广告订单数 x 100%)',
        examples=[0.0],
        validation_alias="new_to_brand_order_percentage",
    )
    new_to_brand_order_rate: FloatOrNone2Zero = Field(
        description="品牌新买家订单转化率 (品牌新买家广告订单数 / 总点击次数 x 100%)",
        examples=[0.0],
    )
    new_to_brand_units: IntOrNone2Zero = Field(
        description="品牌新买家成交商品件数",
        examples=[0],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[38.99],
    )
    direct_sales: FloatOrNone2Zero = Field(
        description='直接广告销售额 [原字段 "same_sales"]',
        examples=[0.0],
        validation_alias="same_sales",
    )
    new_to_brand_sales: FloatOrNone2Zero = Field(
        description="品牌新买家销售额",
        examples=[0.0],
    )
    video_25pct_views: IntOrNone2Zero = Field(
        description='视频广告播放25%次数 [原字段 "video_first_quartile_views"]',
        examples=[0],
        validation_alias="video_first_quartile_views",
    )
    video_50pct_views: IntOrNone2Zero = Field(
        description='视频广告播放50%次数 [原字段 "video_midpoint_views"]',
        examples=[0],
        validation_alias="video_midpoint_views",
    )
    video_75pct_views: IntOrNone2Zero = Field(
        description='视频广告播放75%次数 [原字段 "video_third_quartile_views"]',
        examples=[0],
        validation_alias="video_third_quartile_views",
    )
    video_100pct_views: IntOrNone2Zero = Field(
        description='视频广告播放100%次数 [原字段 "video_complete_views"]',
        examples=[0],
        validation_alias="video_complete_views",
    )
    video_5sec_views: IntOrNone2Zero = Field(
        description='视频广告播放5秒次数 [原字段 "video_5_second_views"]',
        examples=[0],
        validation_alias="video_5_second_views",
    )
    video_5sec_view_rate: FloatOrNone2Zero = Field(
        description='视频广告播放5秒观看率 [原字段 "video_5_second_view_rate"]',
        examples=[0.0],
        validation_alias="video_5_second_view_rate",
    )
    video_unmutes: IntOrNone2Zero = Field(
        description='视频广告静音取消次数 [原字段 "video_unmutes"]',
        examples=[0],
        validation_alias="video_unmutes",
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )
    keyword_id: int = Field(
        description='关键词ID [原字段 "target_id"]',
        examples=[40000000000059],
        validation_alias="target_id",
    )
    keyword_text: StrOrNone2Blank = Field(
        description='关键词文本 [原字段 "target_text"]',
        examples=["aaa aaaaaaaaa aaa aa aaaaacc"],
        validation_alias="target_text",
    )
    match_type: StrOrNone2Blank = Field(
        description="关键词匹配类型",
        examples=["exact"],
    )
    # fmt: on


class SbKeywordQueryReports(ResponseV1Token):
    """SB 关键词的用户搜索词报告列表"""

    data: list[SbKeywordQueryReport] = Field(
        description="SB关键词用户搜索词日报数据",
        examples=[
            [
                {
                    "profile_id": 90000000000005,
                    "campaign_id": 70000000000012,
                    "ad_group_id": 600000000000009,
                    "query_text": "aaaaa aa-000a aaaaaaa aaa aa-000a aaaa-aaaaaaaaaaaaa a示a aaaac",
                    "cost": 1.67,
                    "impressions": 1,
                    "clicks": 1,
                    "orders": 1,
                    "direct_orders": 0,
                    "new_to_brand_orders": 0,
                    "new_to_brand_order_pct": 0.0,
                    "new_to_brand_order_rate": 0.0,
                    "new_to_brand_units": 0,
                    "sales": 28.54,
                    "direct_sales": 0.0,
                    "new_to_brand_sales": 0.0,
                    "video_25pct_views": 0,
                    "video_50pct_views": 0,
                    "video_75pct_views": 0,
                    "video_100pct_views": 0,
                    "video_5sec_views": 0,
                    "video_5sec_view_rate": 0.0,
                    "video_unmutes": 0,
                    "report_date": "2026-10-01",
                    "keyword_id": 40000000000005,
                    "keyword_text": "aaaaa aaaaaaaaaaaaaaa 003",
                    "match_type": "phrase",
                }
            ]
        ],
    )


# . SB Keyword Placement Reports
class SbKeywordPlacementReport(BaseModel):
    """SB 关键词投放位置报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[9000000000000005],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000198],
    )
    keyword_id: int = Field(
        description="关键词ID",
        examples=[40000000000116],
    )
    keyword_text: StrOrNone2Blank = Field(
        description="关键词文本",
        examples=["+aa +aaaa +0009"],
    )
    match_type: StrOrNone2Blank = Field(
        description="关键词匹配类型",
        examples=["broad"],
    )
    placement_type: int = Field(
        description="广告位类型 (1: Other Placements, 2: Other on-Amazon, 3: Top of Search)",
        examples=[2],
    )
    creative_type: str = Field(
        description="广告创意类型",
        examples=["all"],
    )
    cost: float = Field(
        description="广告花费",
        examples=[0.0],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[2],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[0],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[0],
    )
    new_to_brand_orders: IntOrNone2Zero = Field(
        description="品牌新买家广告订单数",
        examples=[0],
    )
    new_to_brand_order_pct: FloatOrNone2Zero = Field(
        description='品牌新买家订单占比 [原字段 "new_to_brand_order_percentage"] (品牌新买家广告订单数 / 广告订单数 x 100%)',
        examples=[0.0],
        validation_alias="new_to_brand_order_percentage",
    )
    new_to_brand_order_rate: FloatOrNone2Zero = Field(
        description="品牌新买家订单转化率 (品牌新买家广告订单数 / 总点击次数 x 100%)",
        examples=[0.0],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[0.0],
    )
    new_to_brand_sales: FloatOrNone2Zero = Field(
        description="品牌新买家销售额",
        examples=[0.0],
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[0],
    )
    direct_units: IntOrNone2Zero = Field(
        description='直接广告成交商品件数 [原字段 "same_units"]',
        examples=[0],
        validation_alias="same_units",
    )
    new_to_brand_units: IntOrNone2Zero = Field(
        description="品牌新买家成交商品件数",
        examples=[0],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SbKeywordPlacementReports(ResponseV1Token):
    """SB 关键词投放位置报告列表"""

    data: list[SbKeywordPlacementReport] = Field(
        description="SB关键词广告位日报数据",
        examples=[
            [
                {
                    "profile_id": 9000000000000005,
                    "campaign_id": 700000000000198,
                    "keyword_id": 40000000000116,
                    "keyword_text": "+aa +aaaa +0009",
                    "match_type": "broad",
                    "placement_type": 2,
                    "creative_type": "all",
                    "cost": 0.0,
                    "impressions": 2,
                    "clicks": 0,
                    "orders": 0,
                    "new_to_brand_orders": 0,
                    "new_to_brand_order_pct": 0.0,
                    "new_to_brand_order_rate": 0.0,
                    "sales": 0.0,
                    "new_to_brand_sales": 0.0,
                    "units": 0,
                    "direct_units": 0,
                    "new_to_brand_units": 0,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SB Target Reports
class SbTargetReport(BaseModel):
    """SB 目标商品投放报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[9000000000000005],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000187],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000286],
    )
    target_id: int = Field(
        description="目标商品广告ID",
        examples=[30000000000034],
    )
    creative_type: str = Field(
        description="广告创意类型；官方已作废，具体类型应查询SB广告创意的creative.type",
        examples=["all"],
    )
    cost: float = Field(
        description="广告花费",
        examples=[0.78],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[11],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[1],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[1],
    )
    direct_orders: int = Field(
        description='直接广告订单数 [原字段 "same_orders"]',
        examples=[1],
        validation_alias="same_orders",
    )
    new_to_brand_orders: int = Field(
        description="品牌新买家广告订单数",
        examples=[1],
    )
    new_to_brand_order_pct: FloatOrNone2Zero = Field(
        description='品牌新买家订单占比 [原字段 "new_to_brand_order_percentage"] (品牌新买家广告订单数 / 广告订单数 x 100%)',
        examples=[100.0],
        validation_alias="new_to_brand_order_percentage",
    )
    new_to_brand_order_rate: FloatOrNone2Zero = Field(
        description="品牌新买家订单转化率 (品牌新买家广告订单数 / 总点击次数 x 100%)",
        examples=[100.0],
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[1],
    )
    direct_units: IntOrNone2Zero = Field(
        description='直接广告成交商品件数 [原字段 "same_units"]',
        examples=[1],
        validation_alias="same_units",
    )
    new_to_brand_units: int = Field(
        description="品牌新买家成交商品件数",
        examples=[1],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[22.89],
    )
    direct_sales: float = Field(
        description='直接广告销售额 [原字段 "same_sales"]',
        examples=[22.89],
        validation_alias="same_sales",
    )
    new_to_brand_sales: float = Field(
        description="品牌新买家销售额",
        examples=[22.89],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )
    # fmt: on


class SbTargetReports(ResponseV1Token):
    """SB 目标商品投放报告列表"""

    data: list[SbTargetReport] = Field(
        description="SB商品投放日报数据",
        examples=[
            [
                {
                    "profile_id": 9000000000000003,
                    "campaign_id": 700000000000004,
                    "ad_group_id": 600000000000008,
                    "target_id": 30000000000005,
                    "creative_type": "all",
                    "cost": 0.78,
                    "impressions": 2,
                    "clicks": 1,
                    "orders": 1,
                    "direct_orders": 1,
                    "new_to_brand_orders": 1,
                    "new_to_brand_order_pct": 100.0,
                    "new_to_brand_order_rate": 100.0,
                    "units": 1,
                    "direct_units": 1,
                    "new_to_brand_units": 1,
                    "sales": 22.89,
                    "direct_sales": 22.89,
                    "new_to_brand_sales": 22.89,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SB Target Query Reports
class SbTargetQueryReport(BaseModel):
    """SB 目标商品投放的用户搜索词报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[9000000000000001],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[70000000000004],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000002],
    )
    query_text: str = Field(
        description='用户使用搜索词 [原字段 "query"]',
        examples=["aaaaaaaaaaaaaaa aaaal"],
        validation_alias="query",
    )
    cost: float = Field(
        description="广告花费",
        examples=[6.23],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[188],
    )
    viewable_impressions: IntOrNone2Zero = Field(
        description="可见展示次数",
        examples=[82],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[7],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[1],
    )
    view_orders: IntOrNone2Zero = Field(
        description="浏览后归因订单数",
        examples=[1],
    )
    click_order_units: IntOrNone2Zero = Field(
        description='点击归因成交商品件数 [原字段 "units_ordered"]',
        examples=[0],
        validation_alias="units_ordered",
    )
    view_order_units: IntOrNone2Zero = Field(
        description='浏览后归因成交商品件数 [原字段 "view_units_ordered"]',
        examples=[1],
        validation_alias="view_units_ordered",
    )
    sales: float = Field(
        description="广告销售额",
        examples=[37.55],
    )
    view_sales: FloatOrNone2Zero = Field(
        description="浏览后归因销售额",
        examples=[37.55],
    )
    video_25pct_views: IntOrNone2Zero = Field(
        description='视频广告播放25%次数 [原字段 "video_first_quartile_views"]',
        examples=[0],
        validation_alias="video_first_quartile_views",
    )
    video_50pct_views: IntOrNone2Zero = Field(
        description='视频广告播放50%次数 [原字段 "video_midpoint_views"]',
        examples=[0],
        validation_alias="video_midpoint_views",
    )
    video_75pct_views: IntOrNone2Zero = Field(
        description='视频广告播放75%次数 [原字段 "video_third_quartile_views"]',
        examples=[0],
        validation_alias="video_third_quartile_views",
    )
    video_100pct_views: IntOrNone2Zero = Field(
        description='视频广告播放100%次数 [原字段 "video_complete_views"]',
        examples=[0],
        validation_alias="video_complete_views",
    )
    video_5sec_views: IntOrNone2Zero = Field(
        description='视频广告播放5秒次数 [原字段 "video_5_second_views"]',
        examples=[0],
        validation_alias="video_5_second_views",
    )
    video_5sec_view_rate: FloatOrNone2Zero = Field(
        description='视频广告播放5秒观看率 [原字段 "video_5_second_view_rate"]',
        examples=[0.0],
        validation_alias="video_5_second_view_rate",
    )
    video_unmutes: IntOrNone2Zero = Field(
        description='视频广告静音取消次数 [原字段 "video_unmutes"]',
        examples=[0],
        validation_alias="video_unmutes",
    )
    add_to_cart_times: IntOrNone2Zero = Field(
        description='加入购物车次数 [原字段 "add_to_list"]',
        examples=[0],
        validation_alias="add_to_list",
    )
    click_add_to_cart_times: IntOrNone2Zero = Field(
        description='通过点击加入购物次数 [原字段 "add_to_list_from_clicks"]',
        examples=[0],
        validation_alias="add_to_list_from_clicks",
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )
    target_id: int = Field(
        description="目标商品投放ID",
        examples=[300000000000004],
    )
    target_text: StrOrNone2Blank = Field(
        description="目标商品投放文本",
        examples=[""],
    )
    is_asin_target: int = Field(
        description='是否为 ASIN 商品投放 (1: 是, 0: 否) [原字段 "is_asin"]',
        examples=[0],
        validation_alias="is_asin",
    )
    # fmt: on


class SbTargetQueryReports(ResponseV1Token):
    """SB 目标商品投放的用户搜索词报告列表"""

    data: list[SbTargetQueryReport] = Field(
        description="SB商品投放用户搜索词日报数据",
        examples=[
            [
                {
                    "profile_id": 9000000000000001,
                    "campaign_id": 70000000000004,
                    "ad_group_id": 600000000000002,
                    "query_text": "aaaaaaaaaaaaaaa aaaal",
                    "cost": 6.23,
                    "impressions": 188,
                    "viewable_impressions": 82,
                    "clicks": 7,
                    "orders": 1,
                    "view_orders": 1,
                    "click_order_units": 0,
                    "view_order_units": 1,
                    "sales": 37.55,
                    "view_sales": 37.55,
                    "video_25pct_views": 0,
                    "video_50pct_views": 0,
                    "video_75pct_views": 0,
                    "video_100pct_views": 0,
                    "video_5sec_views": 0,
                    "video_5sec_view_rate": 0.0,
                    "video_unmutes": 0,
                    "add_to_cart_times": 0,
                    "click_add_to_cart_times": 0,
                    "report_date": "2026-10-01",
                    "target_id": 300000000000004,
                    "target_text": "",
                    "is_asin_target": 0,
                }
            ]
        ],
    )


# . SB Targeting Hour Data
class SbTargetingHour(BaseModel):
    """SB 目标关键词或商品投放小时数据"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[900000000000002],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[70000000000384],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description='广告组ID [原字段 "group_id"]',
        examples=[600000000000243],
        validation_alias="group_id",
    )
    targeting_id: int = Field(
        description="目标定位ID (keyword_id 或 target_id)",
        examples=[400000000000030],
    )
    targeting_text: StrOrNone2Blank = Field(
        description='目标定位文本 [原字段 "targeting"]',
        examples=["00aa aaa aaaaaaaaaa aaaaa aaa aaabo"],
        validation_alias="targeting",
    )
    cost: float = Field(
        description="广告花费",
        examples=[4.28],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[1],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[1],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[1],
    )
    direct_orders: int = Field(
        description='直接广告订单数 [原字段 "same_orders"]',
        examples=[1],
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[1],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[34.89],
    )
    direct_sales: float = Field(
        description='直接广告销售额 [原字段 "same_sales"]',
        examples=[34.89],
        validation_alias="same_sales",
    )
    ctr: FloatOrNone2Zero = Field(
        description="点击率 - Click Through Rate (总点击次数 / 总展示次数)",
        examples=[0.25],
    )
    cvr: FloatOrNone2Zero = Field(
        description="转化率 - Conversion Rate (广告订单数 / 总点击次数)",
        examples=[0.5],
    )
    cpc: FloatOrNone2Zero = Field(
        description="平均点击花费 - Cost Per Click (广告花费 / 总点击次数)",
        examples=[4.28],
    )
    cpa: FloatOrNone2Zero = Field(
        description="平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)",
        examples=[3.3],
    )
    acos: FloatOrNone2Zero = Field(
        description="广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)",
        examples=[0.0946],
    )
    roas: FloatOrNone2Zero = Field(
        description="广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)",
        examples=[10.57],
    )
    hour: int = Field(
        description="数据所属小时 (0-23)",
        examples=[4],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SbTargetingHourData(ResponseV1):
    """SB 目标关键词或商品投放小时数据列表"""

    data: list[SbTargetingHour] = Field(
        description="SB投放小时数据数据",
        examples=[
            [
                {
                    "profile_id": 9000000000000003,
                    "campaign_id": 700000000000004,
                    "ad_group_id": 600000000000008,
                    "targeting_id": 300000000000002,
                    "targeting_text": 'asin="A00AAAAA0C"',
                    "cost": 3.3,
                    "impressions": 4,
                    "clicks": 2,
                    "orders": 1,
                    "direct_orders": 1,
                    "units": 1,
                    "sales": 34.89,
                    "direct_sales": 34.89,
                    "ctr": 0.5,
                    "cvr": 0.5,
                    "cpc": 1.65,
                    "cpa": 3.3,
                    "acos": 0.0946,
                    "roas": 10.57,
                    "hour": 9,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SB ASIN Attribution Reports
class SbAsinAttributionReport(BaseModel):
    """SB 广告商品归因报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[900000000000002],
    )
    campaign_id: IntOrNone2Zero = Field(
        description="广告活动ID",
        examples=[700000000000040],
    )
    campaign_name: StrOrNone2Blank = Field(
        description="广告活动名称",
        examples=["00AA-0A0A-A0AAA00AAA-AA-AAL"],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000315],
    )
    ad_group_name: StrOrNone2Blank = Field(
        description="广告组名称",
        examples=["00AA-0A0A-A0AAA00AAA-AA-AAA-AG"],
    )
    attribution_type: str = Field(
        description="归因类型",
        examples=["Promoted"],
    )
    asin: str = Field(
        description="商品ASIN",
        examples=["A0AAA00AHF"],
    )
    orders_14d: int = Field(
        description='广告14天订单数 [原字段 "orders14d"]',
        examples=[1],
        validation_alias="orders14d",
    )
    new_to_brand_orders_14d: int = Field(
        description='品牌新买家14天订单数 [原字段 "new_to_brand_purchases14d"]',
        examples=[1],
        validation_alias="new_to_brand_purchases14d",
    )
    new_to_brand_order_pct_14d: FloatOrNone2Zero = Field(
        description='品牌新买家订单占比14天 [原字段 "new_to_brand_purchases_percentage14d"] (品牌新买家14天订单数 / 广告14天订单数 x 100%)',
        examples=[100.0],
        validation_alias="new_to_brand_purchases_percentage14d",
    )
    units_14d: int = Field(
        description='广告14天成交商品件数 [原字段 "units_sold14d"]',
        examples=[1],
        validation_alias="units_sold14d",
    )
    new_to_brand_units_14d: int = Field(
        description='品牌新买家14天成交商品件数 [原字段 "new_to_brand_units_sold14d"]',
        examples=[1],
        validation_alias="new_to_brand_units_sold14d",
    )
    new_to_brand_units_pct_14d: FloatOrNone2Zero = Field(
        description='品牌新买家成交商品件数占比14天 [原字段 "new_to_brand_units_sold_percentage14d"] (品牌新买家14天成交商品件数 / 广告14天成交商品件数 x 100%)',
        examples=[100.0],
        validation_alias="new_to_brand_units_sold_percentage14d",
    )
    sales_14d: float = Field(
        description="广告14天销售",
        examples=[38.99],
        validation_alias="sales14d",
    )
    new_to_brand_sales_14d: float = Field(
        description='品牌新买家14天销售额 [原字段 "new_to_brand_sales14d"]',
        examples=[38.99],
        validation_alias="new_to_brand_sales14d",
    )
    new_to_brand_sales_pct_14d: FloatOrNone2Zero = Field(
        description='品牌新买家销售额占比14天 [原字段 "new_to_brand_sales_percentage14d"] (品牌新买家14天销售额 / 广告14天销售 x 100%)',
        examples=[100.0],
        validation_alias="new_to_brand_sales_percentage14d",
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )
    # fmt: on


class SbAsinAttributionReports(ResponseV1Token):
    """SB 广告商品归因报告列表"""

    data: list[SbAsinAttributionReport] = Field(
        description="SB已购买商品归因日报数据",
        examples=[
            [
                {
                    "profile_id": 900000000000002,
                    "campaign_id": 700000000000040,
                    "campaign_name": "00AA-0A0A-A0AAA00AAA-AA-AAL",
                    "ad_group_id": 600000000000315,
                    "ad_group_name": "00AA-0A0A-A0AAA00AAA-AA-AAA-AG",
                    "attribution_type": "Promoted",
                    "asin": "A0AAA00AHF",
                    "orders_14d": 1,
                    "new_to_brand_orders_14d": 1,
                    "new_to_brand_order_pct_14d": 100.0,
                    "units_14d": 1,
                    "new_to_brand_units_14d": 1,
                    "new_to_brand_units_pct_14d": 100.0,
                    "sales_14d": 38.99,
                    "new_to_brand_sales_14d": 38.99,
                    "new_to_brand_sales_pct_14d": 100.0,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SB Cost Allocation Reports
class SbCostAllocationReport(BaseModel):
    """SB 广告费用分摊报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[900000000000002],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000043],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000194],
    )
    department_id: IntOrNone2Zero = Field(
        description="部门ID",
        examples=[200000000000000001],
    )
    allocation_rule_id: StrOrNone2Blank = Field(
        description='设置分摊的事务ID, 用于追踪具体的分摊规则 (UUID) [原字段 "transaction_uuid"]',
        examples=[""],
        validation_alias="transaction_uuid",
    )
    allocation_asin_id: str = Field(
        description='分摊产品的MD5值 (ad_group_id, asin, sku) [原字段 "divide_asin_md5"]',
        examples=["00a0aa0000aa000a0aa0a0a0a00a0003"],
        validation_alias="divide_asin_md5",
    )
    allocation_ratio: float = Field(
        description='分摊比率 (0.0 - 1.0) [原字段 "percent"]',
        examples=[0.3333],
        validation_alias="percent",
    )
    asin: str = Field(
        description="商品ASIN",
        examples=["A0AA0AA0HE"],
    )
    msku: str = Field(
        description='商品SKU [原字段 "sku"]',
        examples=["000-0-AAA-AA-00AA-0A0A-AA-ACW"],
        validation_alias="sku",
    )
    costs: float = Field(
        description='分摊后的广告花费 [原字段 "spends"]',
        examples=[0.355],
        validation_alias="spends",
    )
    impressions: float = Field(
        description="分摊后的展示次数",
        examples=[0.3333],
    )
    clicks: float = Field(
        description="分摊后的点击次数",
        examples=[0.25],
    )
    orders: float = Field(
        description="分摊后的广告订单数",
        examples=[0.2],
    )
    direct_orders: float = Field(
        description='分摊后的直接广告订单数 [原字段 "same_orders"]',
        examples=[0.2],
        validation_alias="same_orders",
    )
    units: float = Field(
        description='分摊后的广告成交商品件数 [原字段 "units_sold"]',
        examples=[0.2],
        validation_alias="units_sold",
    )
    direct_units: float = Field(
        description='分摊后的直接广告成交商品件数 [原字段 "same_units_sold"]',
        examples=[0.2],
        validation_alias="same_units_sold",
    )
    sales: float = Field(
        description="分摊后的广告销售额",
        examples=[7.798],
    )
    direct_sales: float = Field(
        description='分摊后的直接广告销售额 [原字段 "same_sales"]',
        examples=[7.798],
        validation_alias="same_sales",
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SbCostAllocationReports(ResponseV1Token):
    """SB 广告费用分摊报告"""

    data: list[SbCostAllocationReport] = Field(
        description="SB广告费用分摊日报数据",
        examples=[
            [
                {
                    "profile_id": 900000000000001,
                    "campaign_id": 700000000000001,
                    "ad_group_id": 600000000000011,
                    "department_id": 200000000000000001,
                    "allocation_rule_id": "",
                    "allocation_asin_id": "0aa00a000a00a000aa000aa0a000a0a1",
                    "allocation_ratio": 0.2,
                    "asin": "A0AA0AA0AD",
                    "msku": "000-0-AAA-AA-00AA-0A0A-AA-AAA-AA1",
                    "costs": 1.048,
                    "impressions": 25.2,
                    "clicks": 0.4,
                    "orders": 0.2,
                    "direct_orders": 0.2,
                    "units": 0.2,
                    "direct_units": 0.2,
                    "sales": 7.798,
                    "direct_sales": 7.798,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# 报告 - Sponsored Display - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# . SD Campaign Reports
class SdCampaignReport(BaseModel):
    """SD 广告活动报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000009],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000032],
    )
    tactic: str = Field(
        description="投放策略",
        examples=["T00030"],
    )
    cost: float = Field(
        description="广告花费",
        examples=[11.13],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[320],
    )
    viewable_impressions: int = Field(
        description="可见展示次数 [原字段 'view_impressions']",
        examples=[96],
        # - - - - - - - - - -
        validation_alias="view_impressions",
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[30],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[0],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: IntOrNone2Zero = Field(
        description="广告成交商品件数",
        examples=[0],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[0.0],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[0.0],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    new_to_brand_orders_14d: IntOrNone2Zero = Field(
        description="品牌新客14天订单数",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="attributed_orders_new_to_brand_14d",
    )
    new_to_brand_units_14d: IntOrNone2Zero = Field(
        description="品牌新客14天商品件数",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="attributed_units_ordered_new_to_brand_14d",
    )
    new_to_brand_sales_14d: FloatOrNone2Zero = Field(
        description="品牌新客14天销售额",
        examples=[0.0],
        # - - - - - - - - - -
        validation_alias="attributed_sales_new_to_brand_14d",
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SdCampaignReports(ResponseV1Token):
    """SD 广告活动报告列表"""

    data: list[SdCampaignReport] = Field(
        description="SD 广告活动报告数据",
        examples=[
            [
                {
                    "profile_id": 9000000000000005,
                    "campaign_id": 700000000000293,
                    "tactic": "T00030",
                    "cost": 11.13,
                    "impressions": 3250,
                    "viewable_impressions": 96,
                    "clicks": 30,
                    "orders": 0,
                    "direct_orders": 0,
                    "units": 0,
                    "sales": 0.0,
                    "direct_sales": 0.0,
                    "new_to_brand_orders_14d": 0,
                    "new_to_brand_units_14d": 0,
                    "new_to_brand_sales_14d": 0.0,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SD Campaign Hour Data
class SdCampaignHour(BaseModel):
    """SD 广告活动小时数据"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000009],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000032],
    )
    cost: float = Field(
        description="广告花费",
        examples=[0.22],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[1],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[2],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[0],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[0],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[0.0],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[0.0],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    ctr: FloatOrNone2Zero = Field(
        description="点击率 - Click Through Rate (总点击次数 / 总展示次数)",
        examples=[0.0077],
    )
    cvr: FloatOrNone2Zero = Field(
        description="转化率 - Conversion Rate (广告订单数 / 总点击次数)",
        examples=[0.0],
    )
    cpc: FloatOrNone2Zero = Field(
        description="平均点击花费 - Cost Per Click (广告花费 / 总点击次数)",
        examples=[0.11],
    )
    cpa: FloatOrNone2Zero = Field(
        description="平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)",
        examples=[0.0],
    )
    acos: FloatOrNone2Zero = Field(
        description="广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)",
        examples=[0.0],
    )
    roas: FloatOrNone2Zero = Field(
        description="广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)",
        examples=[0.0],
    )
    hour: int = Field(
        description="数据所属小时 (0-23)",
        examples=[0],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SdCampaignHourData(ResponseV1):
    """SD 广告活动小时数据列表"""

    data: list[SdCampaignHour] = Field(
        description="SD 广告活动小时数据数据",
        examples=[
            [
                {
                    "profile_id": 9000000000000005,
                    "campaign_id": 700000000000293,
                    "cost": 0.22,
                    "impressions": 259,
                    "clicks": 2,
                    "orders": 0,
                    "direct_orders": 0,
                    "units": 0,
                    "sales": 0.0,
                    "direct_sales": 0.0,
                    "ctr": 0.0077,
                    "cvr": 0.0,
                    "cpc": 0.11,
                    "cpa": 0.0,
                    "acos": 0.0,
                    "roas": 0.0,
                    "hour": 0,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SD Ad Group Reports
class SdAdGroupReport(BaseModel):
    """SD 广告组报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000009],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000032],
    )
    ad_group_id: int = Field(
        description="广告组ID",
        examples=[600000000000216],
    )
    tactic: str = Field(
        description="投放策略",
        examples=["T00030"],
    )
    cost: float = Field(
        description="广告花费",
        examples=[11.13],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[320],
    )
    viewable_impressions: int = Field(
        description="可见展示次数 [原字段 'view_impressions']",
        examples=[96],
        # - - - - - - - - - -
        validation_alias="view_impressions",
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[30],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[0],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: IntOrNone2Zero = Field(
        description="广告成交商品件数",
        examples=[0],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[0.0],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[0.0],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    new_to_brand_orders_14d: IntOrNone2Zero = Field(
        description="品牌新客14天订单数",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="attributed_orders_new_to_brand_14d",
    )
    new_to_brand_units_14d: IntOrNone2Zero = Field(
        description="品牌新客14天商品件数",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="attributed_units_ordered_new_to_brand_14d",
    )
    new_to_brand_sales_14d: FloatOrNone2Zero = Field(
        description="品牌新客14天销售额",
        examples=[0.0],
        # - - - - - - - - - -
        validation_alias="attributed_sales_new_to_brand_14d",
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SdAdGroupReports(ResponseV1Token):
    """SD 广告组报告列表"""

    data: list[SdAdGroupReport] = Field(
        description="SD 广告组报告数据",
        examples=[
            [
                {
                    "profile_id": 9000000000000005,
                    "campaign_id": 700000000000293,
                    "ad_group_id": 600000000000338,
                    "tactic": "T00030",
                    "cost": 11.13,
                    "impressions": 3250,
                    "viewable_impressions": 96,
                    "clicks": 30,
                    "orders": 0,
                    "direct_orders": 0,
                    "units": 0,
                    "sales": 0.0,
                    "direct_sales": 0.0,
                    "new_to_brand_orders_14d": 0,
                    "new_to_brand_units_14d": 0,
                    "new_to_brand_sales_14d": 0.0,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SD Ad Group Hour Data
class SdAdGroupHour(BaseModel):
    """SD 广告组小时数据"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000009],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000032],
    )
    ad_group_id: int = Field(
        description="广告组ID [原字段 'group_id']",
        examples=[600000000000216],
        # - - - - - - - - - -
        validation_alias="group_id",
    )
    cost: float = Field(
        description="广告花费",
        examples=[0.22],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[1],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[2],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[0],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[0],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[0.0],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[0.0],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    ctr: FloatOrNone2Zero = Field(
        description="点击率 - Click Through Rate (总点击次数 / 总展示次数)",
        examples=[0.0077],
    )
    cvr: FloatOrNone2Zero = Field(
        description="转化率 - Conversion Rate (广告订单数 / 总点击次数)",
        examples=[0.0],
    )
    cpc: FloatOrNone2Zero = Field(
        description="平均点击花费 - Cost Per Click (广告花费 / 总点击次数)",
        examples=[0.11],
    )
    cpa: FloatOrNone2Zero = Field(
        description="平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)",
        examples=[0.0],
    )
    acos: FloatOrNone2Zero = Field(
        description="广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)",
        examples=[0.0],
    )
    roas: FloatOrNone2Zero = Field(
        description="广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)",
        examples=[0.0],
    )
    hour: int = Field(
        description="数据所属小时 (0-23)",
        examples=[0],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SdAdGroupHourData(ResponseV1):
    """SD 广告组小时数据列表"""

    data: list[SdAdGroupHour] = Field(
        description="SD 广告组小时数据数据",
        examples=[
            [
                {
                    "profile_id": 9000000000000005,
                    "campaign_id": 700000000000293,
                    "ad_group_id": 600000000000338,
                    "cost": 0.22,
                    "impressions": 259,
                    "clicks": 2,
                    "orders": 0,
                    "direct_orders": 0,
                    "units": 0,
                    "sales": 0.0,
                    "direct_sales": 0.0,
                    "ctr": 0.0077,
                    "cvr": 0.0,
                    "cpc": 0.11,
                    "cpa": 0.0,
                    "acos": 0.0,
                    "roas": 0.0,
                    "hour": 0,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SD Product Reports
class SdProductReport(BaseModel):
    """SD 商品投放报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000009],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000175],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000306],
    )
    ad_id: int = Field(
        description="商品广告ID",
        examples=[500000000000215],
    )
    tactic: str = Field(
        description="投放策略",
        examples=["T00030"],
    )
    asin: str = Field(
        description="商品ASIN",
        examples=["A0AA0AA0HF"],
    )
    msku: str = Field(
        description="亚马逊SKU [原字段 'sku']",
        examples=["000-AA-000-AD-M"],
        # - - - - - - - - - -
        validation_alias="sku",
    )
    cost: float = Field(
        description="广告花费",
        examples=[0.99],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[1],
    )
    viewable_impressions: int = Field(
        description="可见展示次数 [原字段 'view_impressions']",
        examples=[9],
        # - - - - - - - - - -
        validation_alias="view_impressions",
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[2],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[0],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: IntOrNone2Zero = Field(
        description="广告成交商品件数",
        examples=[0],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[0.0],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[0.0],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    new_to_brand_orders_14d: IntOrNone2Zero = Field(
        description="品牌新客14天订单数",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="attributed_orders_new_to_brand_14d",
    )
    new_to_brand_units_14d: IntOrNone2Zero = Field(
        description="品牌新客14天商品件数",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="attributed_units_ordered_new_to_brand_14d",
    )
    new_to_brand_sales_14d: FloatOrNone2Zero = Field(
        description="品牌新客14天销售额",
        examples=[0.0],
        # - - - - - - - - - -
        validation_alias="attributed_sales_new_to_brand_14d",
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SdProductReports(ResponseV1Token):
    """SD 商品投放报告列表"""

    data: list[SdProductReport] = Field(
        description="SD 商品投放报告数据",
        examples=[
            [
                {
                    "profile_id": 9000000000000005,
                    "campaign_id": 700000000000293,
                    "ad_group_id": 600000000000338,
                    "ad_id": 500000000000223,
                    "tactic": "T00030",
                    "asin": "A0A00AAAIT",
                    "msku": "000-00-AA-00AA-0A-BI",
                    "cost": 0.99,
                    "impressions": 325,
                    "viewable_impressions": 9,
                    "clicks": 2,
                    "orders": 0,
                    "direct_orders": 0,
                    "units": 0,
                    "sales": 0.0,
                    "direct_sales": 0.0,
                    "new_to_brand_orders_14d": 0,
                    "new_to_brand_units_14d": 0,
                    "new_to_brand_sales_14d": 0.0,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SD Product Hour Data
class SpdProductHour(BaseModel):
    """SD 商品投放小时数据"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000009],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000032],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID [原字段 'group_id']",
        examples=[600000000000216],
        # - - - - - - - - - -
        validation_alias="group_id",
    )
    ad_id: int = Field(
        description="商品广告ID",
        examples=[500000000000488],
    )
    asin: str = Field(
        description="商品ASIN",
        examples=["A0AAAAAAT0"],
    )
    msku: str = Field(
        description="亚马逊SKU",
        examples=["000-AA-000-0D-K"],
    )
    cost: float = Field(
        description="广告花费",
        examples=[0.36],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[2],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[3],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[0],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[0],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[0.0],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[0.0],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    ctr: FloatOrNone2Zero = Field(
        description="点击率 - Click Through Rate (总点击次数 / 总展示次数)",
        examples=[0.0189],
    )
    cvr: FloatOrNone2Zero = Field(
        description="转化率 - Conversion Rate (广告订单数 / 总点击次数)",
        examples=[0.0],
    )
    cpc: FloatOrNone2Zero = Field(
        description="平均点击花费 - Cost Per Click (广告花费 / 总点击次数)",
        examples=[0.12],
    )
    cpa: FloatOrNone2Zero = Field(
        description="平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)",
        examples=[0.0],
    )
    acos: FloatOrNone2Zero = Field(
        description="广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)",
        examples=[0.0],
    )
    roas: FloatOrNone2Zero = Field(
        description="广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)",
        examples=[0.0],
    )
    hour: int = Field(
        description="数据所属小时 (0-23)",
        examples=[19],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SdProductHourData(ResponseV1):
    """SD 商品投放小时数据列表"""

    data: list[SpdProductHour] = Field(
        description="SD 商品投放小时数据数据",
        examples=[
            [
                {
                    "profile_id": 9000000000000005,
                    "campaign_id": 700000000000293,
                    "ad_group_id": 600000000000338,
                    "ad_id": 500000000000468,
                    "asin": "A00AAAAA6N",
                    "msku": "000-00-AA-00AA-0A0A-0BB",
                    "cost": 0.36,
                    "impressions": 159,
                    "clicks": 3,
                    "orders": 0,
                    "direct_orders": 0,
                    "units": 0,
                    "sales": 0.0,
                    "direct_sales": 0.0,
                    "ctr": 0.0189,
                    "cvr": 0.0,
                    "cpc": 0.12,
                    "cpa": 0.0,
                    "acos": 0.0,
                    "roas": 0.0,
                    "hour": 2,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SD Target Reports
class SdTargetReport(BaseModel):
    """SD 目标商品投放报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000009],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000032],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000216],
    )
    target_id: int = Field(
        description="目标商品广告ID",
        examples=[300000000000011],
    )
    target_text: StrOrNone2Blank = Field(
        description="目标商品文本 [原字段 'targeting_expression']",
        examples=["views=(exact-product lookback=30)"],
        # - - - - - - - - - -
        validation_alias="targeting_expression",
    )
    expression_type: StrOrNone2Blank = Field(
        description="目标定位类型 [原字段 'targeting_type']",
        examples=[""],
        # - - - - - - - - - -
        validation_alias="targeting_type",
    )
    expression: StrOrNone2Blank = Field(
        description="目标定位表达式 (JSON 字符串) [原字段 'targeting_text']",
        examples=[
            '"[{\\"type\\": \\"views\\", \\"value\\": [{\\"type\\": \\"exactProduct\\"}, {\\"type\\": \\"lookback\\", \\"value\\": \\"30\\"}]}]"'
        ],
        # - - - - - - - - - -
        validation_alias="targeting_text",
    )
    tactic: str = Field(
        description="投放策略",
        examples=["T00030"],
    )
    cost: float = Field(
        description="广告花费",
        examples=[0.94],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[104],
    )
    viewable_impressions: int = Field(
        description="可见展示次数 [原字段 'view_impressions']",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="view_impressions",
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[2],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[0],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: IntOrNone2Zero = Field(
        description="广告成交商品件数",
        examples=[0],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[0.0],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[0.0],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    new_to_brand_orders_14d: IntOrNone2Zero = Field(
        description="品牌新客14天订单数",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="attributed_orders_new_to_brand_14d",
    )
    new_to_brand_units_14d: IntOrNone2Zero = Field(
        description="品牌新客14天商品件数",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="attributed_units_ordered_new_to_brand_14d",
    )
    new_to_brand_sales_14d: FloatOrNone2Zero = Field(
        description="品牌新客14天销售额",
        examples=[0.0],
        # - - - - - - - - - -
        validation_alias="attributed_sales_new_to_brand_14d",
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SdTargetReports(ResponseV1Token):
    """SD 目标商品投放报告列表"""

    data: list[SdTargetReport] = Field(
        description="SD 目标商品投放报告数据",
        examples=[
            [
                {
                    "profile_id": 90000000000009,
                    "campaign_id": 700000000000175,
                    "ad_group_id": 600000000000306,
                    "target_id": 300000000000020,
                    "target_text": "purchases=(exact-product lookback=365)",
                    "expression_type": "",
                    "expression": '"[{\\"type\\": \\"purchases\\", \\"value\\": [{\\"type\\": \\"exactProduct\\"}, {\\"type\\": \\"lookback\\", \\"value\\": \\"365\\"}]}]"',
                    "tactic": "T00030",
                    "cost": 0.94,
                    "impressions": 101,
                    "viewable_impressions": 0,
                    "clicks": 2,
                    "orders": 0,
                    "direct_orders": 0,
                    "units": 0,
                    "sales": 0.0,
                    "direct_sales": 0.0,
                    "new_to_brand_orders_14d": 0,
                    "new_to_brand_units_14d": 0,
                    "new_to_brand_sales_14d": 0.0,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SD Target Hour Data
class SdTargetHour(BaseModel):
    """SD 目标商品投放小时数据"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[90000000000009],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000032],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID [原字段 'group_id']",
        examples=[600000000000216],
        # - - - - - - - - - -
        validation_alias="group_id",
    )
    ad_id: int = Field(
        description="商品广告ID",
        examples=[500000000000542],
    )
    target_id: int = Field(
        description="目标商品广告ID [原字段 'targeting_id']",
        examples=[300000000000011],
        # - - - - - - - - - -
        validation_alias="targeting_id",
    )
    target_text: StrOrNone2Blank = Field(
        description="目标定位文本 [原字段 'targeting']",
        examples=["views=(exact-product lookback=30)"],
        # - - - - - - - - - -
        validation_alias="targeting",
    )
    asin: str = Field(
        description="商品ASIN",
        examples=["A0A0A00A7N"],
    )
    msku: str = Field(
        description="亚马逊SKU",
        examples=["000-AA-000-0D-Q"],
    )
    cost: float = Field(
        description="广告花费",
        examples=[0.1],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[1],
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[1],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[0],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[0],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[0.0],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[0.0],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    ctr: FloatOrNone2Zero = Field(
        description="点击率 - Click Through Rate (总点击次数 / 总展示次数)",
        examples=[0.125],
    )
    cvr: FloatOrNone2Zero = Field(
        description="转化率 - Conversion Rate (广告订单数 / 总点击次数)",
        examples=[0.0],
    )
    cpc: FloatOrNone2Zero = Field(
        description="平均点击花费 - Cost Per Click (广告花费 / 总点击次数)",
        examples=[0.1],
    )
    cpa: FloatOrNone2Zero = Field(
        description="平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)",
        examples=[0.0],
    )
    acos: FloatOrNone2Zero = Field(
        description="广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)",
        examples=[0.0],
    )
    roas: FloatOrNone2Zero = Field(
        description="广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)",
        examples=[0.0],
    )
    hour: int = Field(
        description="数据所属小时 (0-23)",
        examples=[6],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SdTargetHourData(ResponseV1):
    """SD 目标商品投放小时数据列表"""

    data: list[SdTargetHour] = Field(
        description="SD 目标商品投放小时数据数据",
        examples=[
            [
                {
                    "profile_id": 9000000000000005,
                    "campaign_id": 700000000000293,
                    "ad_group_id": 600000000000338,
                    "ad_id": 500000000000534,
                    "target_id": 30000000000050,
                    "target_text": "views=(similar-product lookback=90)",
                    "asin": "A000AA0ACR",
                    "msku": "000-00-AA-AAAA-00AA-0A-AW",
                    "cost": 0.1,
                    "impressions": 8,
                    "clicks": 1,
                    "orders": 0,
                    "direct_orders": 0,
                    "units": 0,
                    "sales": 0.0,
                    "direct_sales": 0.0,
                    "ctr": 0.125,
                    "cvr": 0.0,
                    "cpc": 0.1,
                    "cpa": 0.0,
                    "acos": 0.0,
                    "roas": 0.0,
                    "hour": 2,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# . SD Matched Target Reports
class SdMatchedTargetReport(BaseModel):
    """SD 匹配的目标商品投放报告"""

    profile_id: int = Field(
        description="亚马逊店铺ID (广告帐号ID)",
        examples=[9000000000000005],
    )
    campaign_id: int = Field(
        description="广告活动ID",
        examples=[700000000000293],
    )
    ad_group_id: IntOrNone2Zero = Field(
        description="广告组ID",
        examples=[600000000000338],
    )
    target_id: int = Field(
        description="目标商品广告ID",
        examples=[300000000000009],
    )
    expression: str = Field(
        description="目标定位表达式 (JSON 字符串) [原字段 'target_text']",
        examples=[
            '"[{\\"type\\": \\"views\\", \\"value\\": [{\\"type\\": \\"exactProduct\\"}, {\\"type\\": \\"lookback\\", \\"value\\": \\"30\\"}]}]"'
        ],
        # - - - - - - - - - -
        validation_alias="target_text",
    )
    matched_target: str = Field(
        description="匹配的目标商品 (ASIN)",
        examples=["A00AAAAAAV"],
    )
    currency_code: StrOrNone2Blank = Field(
        description="货币代码 [原字段 'currency']",
        examples=[""],
        # - - - - - - - - - -
        validation_alias="currency",
    )
    cost: float = Field(
        description="广告花费",
        examples=[1.98],
    )
    impressions: int = Field(
        description="总展示次数",
        examples=[2],
    )
    viewable_impressions: int = Field(
        description="可见展示次数 [原字段 'view_impressions']",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="view_impressions",
    )
    clicks: int = Field(
        description="总点击次数",
        examples=[1],
    )
    orders: int = Field(
        description="广告订单数",
        examples=[0],
    )
    direct_orders: int = Field(
        description="直接广告订单数 [原字段 'same_orders']",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="same_orders",
    )
    new_to_brand_orders: int = Field(
        description="品牌新买家广告订单数",
        examples=[0],
    )
    units: int = Field(
        description="广告成交商品件数",
        examples=[0],
    )
    new_to_brand_units: int = Field(
        description="品牌新买家成交商品件数",
        examples=[0],
    )
    sales: float = Field(
        description="广告销售额",
        examples=[0.0],
    )
    direct_sales: float = Field(
        description="直接广告销售额 [原字段 'same_sales']",
        examples=[0.0],
        # - - - - - - - - - -
        validation_alias="same_sales",
    )
    new_to_brand_sales: float = Field(
        description="品牌新买家销售额",
        examples=[0.0],
    )
    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )


class SdMatchedTargetReports(ResponseV1Token):
    """SD 匹配的目标商品投放报告列表"""

    data: list[SdMatchedTargetReport] = Field(
        description="SD 匹配的目标商品投放报告数据",
        examples=[
            [
                {
                    "profile_id": 9000000000000005,
                    "campaign_id": 700000000000293,
                    "ad_group_id": 600000000000338,
                    "target_id": 300000000000009,
                    "expression": '"[{\\"type\\": \\"views\\", \\"value\\": [{\\"type\\": \\"exactProduct\\"}, {\\"type\\": \\"lookback\\", \\"value\\": \\"30\\"}]}]"',
                    "matched_target": "A00AAAAAAV",
                    "currency_code": "",
                    "cost": 1.98,
                    "impressions": 2,
                    "viewable_impressions": 0,
                    "clicks": 1,
                    "orders": 0,
                    "direct_orders": 0,
                    "new_to_brand_orders": 0,
                    "units": 0,
                    "new_to_brand_units": 0,
                    "sales": 0.0,
                    "direct_sales": 0.0,
                    "new_to_brand_sales": 0.0,
                    "report_date": "2026-10-01",
                }
            ]
        ],
    )


# 报告 - Demand-Side Platform - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# . DSP Reports
class DspReport(BaseModel):
    """DSP 报告"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告主ID
    advertiser_id: int
    # 广告主名称
    advertiser_name: str
    # 订单ID
    order_id: str
    # 订单名称
    order_name: str
    # 订单开始时间
    order_start_date: str
    # 订单结束时间
    order_end_date: str
    # 预算 [原字段 'order_budget']
    budget: float = Field(validation_alias="order_budget")
    # 广告花费 [原字段 'spends']
    costs: float = Field(validation_alias="spends")
    # 总展示次数
    impressions: int
    # 可见展示次数
    viewable_impressions: int
    # 总点击次数
    clicks: int
    # 商品详情页浏览次数 [原字段 'dpv']
    page_views: int = Field(validation_alias="dpv")
    # 加购次数 [原字段 'total_add_to_cart']
    add_to_cart_count: int = Field(validation_alias="total_add_to_cart")
    # 订单数
    orders: int
    # 销量 [原字段 'ad_units']
    units: int = Field(validation_alias="ad_units")
    # 销售额
    sales: float
    # 币种 [原字段 'order_currency']
    currency_code: str = Field(validation_alias="order_currency")


class DspReports(ResponseV1):
    """DSP 报告列表"""

    data: list[DspReport]


# 报表下载 ----------------------------------------------------------------------------------------------------------------------
# . Download ABA Report
class AbaReportUrl(BaseModel):
    """ABA 报告下载链接"""

    # 国家代码 [原字段 'country']
    country_code: str = Field(validation_alias="country")
    # 报告周期
    report_period: str
    # 报告开始日期 [原字段 'data_start_time']
    start_date: str = Field(validation_alias="data_start_time")
    # 下载链接
    url: str


class DownloadAbaReport(ResponseV1):
    """下载 ABA 报告信息"""

    data: AbaReportUrl


# 操作日志 ----------------------------------------------------------------------------------------------------------------------
class AdsOperation(BaseModel):
    """广告操作"""

    # 操作编码
    code: str
    # 操作值
    value: StrOrNone2Blank


class AdsOperationLog(BaseModel):
    """广告操作日志"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告活动名称
    campaign_name: str
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 广告组名称
    ad_group_name: StrOrNone2Blank
    # 广告对象ID [原字段 'object_id']
    ad_object_id: IntOrNone2Zero = Field(validation_alias="object_id")
    # 广告对象名称 [原字段 'object_name']
    ad_object_name: StrOrNone2Blank = Field(validation_alias="object_name")
    # 广告类型 [原字段 'sponsored_type']
    ad_type: str = Field(validation_alias="sponsored_type")
    # 操作用户ID [原字段 'user_id']
    operator_id: IntOrNone2Zero = Field(validation_alias="user_id")
    # 操作用户名称 [原字段 'user_name']
    operator_name: StrOrNone2Blank = Field(validation_alias="user_name")
    # 操作对象 [原字段 'operate_type']
    operation_target: StrOrNone2Blank = Field(validation_alias="operate_type")
    # 操作类型 [原字段 'change_type']
    operation_type: StrOrNone2Blank = Field(validation_alias="change_type")
    # 操作来源 [原字段 'function_name']
    operation_source: StrOrNone2Blank = Field(validation_alias="function_name")
    # 操作时间 [原字段 'operate_time']
    operation_time: str = Field(validation_alias="operate_time")
    # 操作前列表 [原字段 'operate_before']
    before: list[AdsOperation] = Field(validation_alias="operate_before")
    # 操作后列表 [原字段 'operate_after']
    after: list[AdsOperation] = Field(validation_alias="operate_after")


class AdsOperationLogs(ResponseV1):
    """广告操作日志"""

    data: list[AdsOperationLog]
