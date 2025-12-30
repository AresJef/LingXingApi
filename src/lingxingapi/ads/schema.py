# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from lingxingapi.base.schema import ResponseV1, ResponseV1Token
from lingxingapi.fields import IntOrNone2Zero, FloatOrNone2Zero, StrOrNone2Blank


# 基础数据 ----------------------------------------------------------------------------------------------------------------------
# . Ads Profiles
class AdProfile(BaseModel):
    """广告帐号"""

    # 领星店铺ID
    sid: IntOrNone2Zero
    # 领星店铺名称 [原字段 'name']
    seller_name: str = Field(validation_alias="name")
    # 店铺国家代码
    country_code: str
    # 店铺货币代码
    currency_code: str
    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告帐号类型 [原字段 'type']
    profile_type: str = Field(validation_alias="type")
    # 广告帐号状态 [原字段 'status']
    # (-1: 删除, 0: 停用, 1: 正常, 2: 异常)
    profile_status: int = Field(validation_alias="status")


class AdProfiles(ResponseV1):
    """广告帐号列表"""

    data: list[AdProfile]


# . Portfolios
class Portfolio(BaseModel):
    """广告组合"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告组合ID
    portfolio_id: int
    # 广告组合名称 [原字段 'name']
    portfolio_name: str = Field(validation_alias="name")
    # 广告预算 (JSON 字符串)
    budget: StrOrNone2Blank
    # 当前是否在预算范围内 (0: 超出预算, 1: 在预算内)
    in_budget: int
    # 广告状态
    state: StrOrNone2Blank
    # 服务状态 [原字段 'serving_status']
    status: StrOrNone2Blank = Field(validation_alias="serving_status")
    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
    create_time_ts: IntOrNone2Zero = Field(validation_alias="creation_date")
    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
    update_time_ts: IntOrNone2Zero = Field(validation_alias="last_updated_date")


class Portfolios(ResponseV1Token):
    """广告组合列表"""

    data: list[Portfolio]


# 基础数据 - Sponsored Products - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# . SP Campaigns
class SpCampaign(BaseModel):
    """SP 广告活动"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告组合ID
    portfolio_id: IntOrNone2Zero
    # 广告活动ID
    campaign_id: int
    # 广告活动名称 [原字段 'name']
    campaign_name: str = Field(validation_alias="name")
    # 广告活动类型
    campaign_type: str
    # 投放类型
    targeting_type: str
    # 溢价报价调整 (0: 不调整, 1: 调整)
    premium_bid_adjustment: int
    # 每日预算
    daily_budget: float
    # 竞价策略 (JSON 字符串)
    bidding: StrOrNone2Blank
    # 开始时间 [原字段 'start_date']
    start_time: StrOrNone2Blank = Field(validation_alias="start_date")
    # 结束时间 [原字段 'end_date']
    end_time: StrOrNone2Blank = Field(None, validation_alias="end_date")
    # 广告状态
    state: StrOrNone2Blank
    # 服务状态 [原字段 'serving_status']
    status: StrOrNone2Blank = Field(validation_alias="serving_status")
    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
    create_time_ts: IntOrNone2Zero = Field(validation_alias="creation_date")
    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
    update_time_ts: IntOrNone2Zero = Field(validation_alias="last_updated_date")


class SpCampaigns(ResponseV1Token):
    """SP 广告活动列表"""

    data: list[SpCampaign]


# . SP Ad Groups
class SpAdGroup(BaseModel):
    """SP 广告组"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: int
    # 广告组名称 [原字段 'name']
    ad_group_name: str = Field(validation_alias="name")
    # 默认竞价
    default_bid: float
    # 广告组状态
    state: StrOrNone2Blank
    # 服务状态 [原字段 'serving_status']
    status: StrOrNone2Blank = Field(validation_alias="serving_status")
    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
    create_time_ts: IntOrNone2Zero = Field(validation_alias="creation_date")
    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
    update_time_ts: IntOrNone2Zero = Field(validation_alias="last_updated_date")


class SpAdGroups(ResponseV1Token):
    """SP 广告组列表"""

    data: list[SpAdGroup]


# . SP Ads
class SpProduct(BaseModel):
    """SP 商品投放"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 商品广告ID
    ad_id: int
    # 商品ASIN
    asin: StrOrNone2Blank
    # 亚马逊SKU [原字段 'sku']
    msku: str = Field(validation_alias="sku")
    # 广告状态
    state: StrOrNone2Blank
    # 服务状态 [原字段 'serving_status']
    status: StrOrNone2Blank = Field(validation_alias="serving_status")
    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
    create_time_ts: IntOrNone2Zero = Field(validation_alias="creation_date")
    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
    update_time_ts: IntOrNone2Zero = Field(validation_alias="last_updated_date")


class SpProducts(ResponseV1Token):
    """SP 商品投放列表"""

    data: list[SpProduct]


# . SP Keywords
class SpKeyword(BaseModel):
    """SP 关键词投放"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 关键词ID
    keyword_id: int
    # 关键词文本
    keyword_text: str
    # 关键词匹配类型
    match_type: str
    # 竞价
    bid: FloatOrNone2Zero
    # 广告状态
    state: StrOrNone2Blank
    # 服务状态 [原字段 'serving_status']
    status: StrOrNone2Blank = Field(validation_alias="serving_status")
    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
    create_time_ts: IntOrNone2Zero = Field(validation_alias="creation_date")
    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
    update_time_ts: IntOrNone2Zero = Field(validation_alias="last_updated_date")


class SpKeywords(ResponseV1Token):
    """SP 关键词投放列表"""

    data: list[SpKeyword]


# . SP Targets
class SpTarget(BaseModel):
    """SP 目标商品投放"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 目标商品广告ID
    target_id: int
    # 目标定位表达式类型
    expression_type: str
    # 目标定位表达式 (JSON 字符串)
    expression: StrOrNone2Blank
    # 目标定位解析表达式 (JSON 字符串) [原字段 'resolved_expression']
    expression_resolved: StrOrNone2Blank = Field(validation_alias="resolved_expression")
    # 竞价
    bid: FloatOrNone2Zero
    # 广告状态
    state: StrOrNone2Blank
    # 服务状态 [原字段 'serving_status']
    status: StrOrNone2Blank = Field(validation_alias="serving_status")
    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
    create_time_ts: IntOrNone2Zero = Field(validation_alias="creation_date")
    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
    update_time_ts: IntOrNone2Zero = Field(validation_alias="last_updated_date")


class SpTargets(ResponseV1Token):
    """SP 目标商品投放列表"""

    data: list[SpTarget]


# . Sp Negative Keywords
class SpNegativeKeyword(BaseModel):
    """SP 否定投放目标或关键词"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 否定关键词文本 [原字段 'negative_text']
    keyword_text: str = Field(validation_alias="negative_text")
    # 否定匹配方式 [原字段 'negative_match_type']
    match_type: str = Field(validation_alias="negative_match_type")
    # 广告状态
    state: StrOrNone2Blank
    # 服务状态 [原字段 'serving_status']
    status: StrOrNone2Blank = Field(validation_alias="serving_status")
    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
    create_time_ts: IntOrNone2Zero = Field(validation_alias="creation_date")
    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
    update_time_ts: IntOrNone2Zero = Field(validation_alias="last_updated_date")


class SpNegativeKeywords(ResponseV1Token):
    """SP 否定关键词投放列表"""

    data: list[SpNegativeKeyword]


# . SP Negative Targets
class SpNegativeTarget(BaseModel):
    """SP 否定投放目标或关键词"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 否定目标类型 [原字段 'negative_type']
    target_type: str = Field(validation_alias="negative_type")
    # 否定目标文本 [原字段 'negative_text']
    target_text: StrOrNone2Blank = Field(validation_alias="negative_text")
    # 广告状态
    state: StrOrNone2Blank
    # 服务状态 [原字段 'serving_status']
    status: StrOrNone2Blank = Field(validation_alias="serving_status")
    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
    create_time_ts: IntOrNone2Zero = Field(validation_alias="creation_date")
    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
    update_time_ts: IntOrNone2Zero = Field(validation_alias="last_updated_date")


class SpNegativeTargets(ResponseV1Token):
    """SP 否定目标商品投放列表"""

    data: list[SpNegativeTarget]


# 基础数据 - Sponsored Brands - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# . SB Campaigns
class SbCampaign(BaseModel):
    """SB 广告活动"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告组合ID
    portfolio_id: IntOrNone2Zero
    # 广告活动ID
    campaign_id: int
    # 广告活动名称 [原字段 'name']
    campaign_name: str = Field(validation_alias="name")
    # 广告预算
    budget: float
    # 广告预算类型
    budget_type: str
    # 自定义竞价调整
    bid_multiplier: FloatOrNone2Zero
    # 是否使用自动竞价 (0: 否, 1: 是)
    bid_optimization: IntOrNone2Zero
    # 广告着陆页 (JSON 字符串)
    landing_page: StrOrNone2Blank
    # 广告创意结构 (JSON 字符串)
    creative: StrOrNone2Blank
    # 广告创意类型
    creative_type: StrOrNone2Blank
    # 开始时间 [原字段 'start_date']
    start_time: StrOrNone2Blank = Field(validation_alias="start_date")
    # 结束时间 [原字段 'end_date']
    end_time: StrOrNone2Blank = Field(None, validation_alias="end_date")
    # 广告状态
    state: StrOrNone2Blank
    # 服务状态 [原字段 'serving_status']
    status: StrOrNone2Blank = Field(validation_alias="serving_status")


class SbCampaigns(ResponseV1Token):
    """SB 广告活动列表"""

    data: list[SbCampaign]


# . SB Ad Groups
class SbAdGroup(BaseModel):
    """SB 广告组"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: int
    # 广告组名称 [原字段 'name']
    ad_group_name: str = Field(validation_alias="name")
    # 广告组状态
    state: StrOrNone2Blank
    # 服务状态 [原字段 'serving_status']
    status: StrOrNone2Blank = Field(validation_alias="serving_status")
    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
    create_time_ts: IntOrNone2Zero = Field(validation_alias="creation_date")
    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
    update_time_ts: IntOrNone2Zero = Field(validation_alias="last_updated_date")


class SbAdGroups(ResponseV1Token):
    """SB 广告组列表"""

    data: list[SbAdGroup]


# . SB Creatives
class SbCreative(BaseModel):
    """SB 广告创意"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 广告创意ID [原字段 'ad_creative_id']
    creative_id: int = Field(validation_alias="ad_creative_id")
    # 广告创意名称 [原字段 'name']
    creative_name: StrOrNone2Blank = Field(validation_alias="name")
    # 广告创意 ASIN 列表 [原字段 'asin']
    asins: list[str] = Field(validation_alias="asin")
    # 广告状态
    state: StrOrNone2Blank
    # 服务状态 [原字段 'serving_status']
    status: StrOrNone2Blank = Field(validation_alias="serving_status")
    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
    create_time_ts: IntOrNone2Zero = Field(validation_alias="creation_date")
    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
    update_time_ts: IntOrNone2Zero = Field(validation_alias="last_updated_date")


class SbCreatives(ResponseV1Token):
    """SB 广告创意列表"""

    data: list[SbCreative]


# . SB Keywords
class SbKeyword(BaseModel):
    """SB 广告投放目标"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 广告类型 [原字段 'ads_type']
    ad_type: str = Field(validation_alias="ads_type")
    # 投放目标类型
    targeting_type: str
    # 关键词ID
    keyword_id: int
    # 关键词文本
    keyword_text: str
    # 关键词匹配类型
    match_type: str
    # 竞价 [原字段 'keyword_bid']
    bid: FloatOrNone2Zero = Field(validation_alias="keyword_bid")
    # 广告状态 [原字段 'keyword_state']
    state: StrOrNone2Blank = Field(validation_alias="keyword_state")


class SbKeywords(ResponseV1Token):
    """SB 关键词投放列表"""

    data: list[SbKeyword]


# . SB Targets
class SbTarget(BaseModel):
    """SB 目标商品投放"""

    # fmt: off
    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 广告类型 [原字段 'ads_type']
    ad_type: str = Field(validation_alias="ads_type")
    # 投放目标类型 
    targeting_type: str
    # 目标商品广告ID
    target_id: int 
    # 目标定位表达式 (JSON 字符串)
    expression: str
    # 目标定位解析表达式 (JSON 字符串) [原字段 'resolved_expression']
    expression_resolved: str = Field(validation_alias="resolved_expression")
    # 竞价 [原字段 'target_bid']
    bid: FloatOrNone2Zero = Field(validation_alias="target_bid")
    # 广告状态 [原字段 'target_state']
    state: StrOrNone2Blank = Field(validation_alias="target_state")
    # fmt: on


class SbTargets(ResponseV1Token):
    """SB 目标商品投放列表"""

    data: list[SbTarget]


# . SB Negative Keywords
class SbNegativeKeyword(BaseModel):
    """SB 否定关键词投放"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 否定关键词ID
    keyword_id: int
    # 否定关键词文本
    keyword_text: str
    # 否定关键词匹配类型
    match_type: str
    # 广告状态
    state: StrOrNone2Blank
    # 服务状态 [原字段 'serving_status']
    status: StrOrNone2Blank = Field(validation_alias="serving_status")
    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
    create_time_ts: IntOrNone2Zero = Field(validation_alias="creation_date")
    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
    update_time_ts: IntOrNone2Zero = Field(validation_alias="last_updated_date")


class SbNegativeKeywords(ResponseV1Token):
    """SB 否定关键词投放列表"""

    data: list[SbNegativeKeyword]


# . SB Negative Targets
class SbNegativeTarget(BaseModel):
    """SB 否定目标商品投放"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 否定目标商品广告ID
    target_id: int
    # 否定目标定位类型
    expression_type: str
    # 否定目标定位表达式 (JSON 字符串)
    expression: str
    # 否定目标定位解析表达式 (JSON 字符串) [原字段 'resolved_expression']
    expression_resolved: str = Field(validation_alias="resolved_expression")
    # 广告状态
    state: StrOrNone2Blank
    # 服务状态 [原字段 'serving_status']
    status: StrOrNone2Blank = Field(validation_alias="serving_status")
    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
    create_time_ts: IntOrNone2Zero = Field(validation_alias="creation_date")
    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
    update_time_ts: IntOrNone2Zero = Field(validation_alias="last_updated_date")


class SbNegativeTargets(ResponseV1Token):
    """SB 否定目标商品投放列表"""

    data: list[SbNegativeTarget]


# 基础数据 - Sponsored Display - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# . SD Campaigns
class SdCampaign(BaseModel):
    """SD 广告活动"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告组合ID
    portfolio_id: IntOrNone2Zero
    # 广告活动ID
    campaign_id: int
    # 广告活动名称 [原字段 'name']
    campaign_name: str = Field(validation_alias="name")
    # 投放类型
    tactic: str
    # 竞价类型 [原字段 'cost_type']
    bid_type: str = Field(validation_alias="cost_type")
    # 每日预算
    budget: float
    # 预算类型
    budget_type: str
    # 开始时间 [原字段 'start_date']
    start_time: StrOrNone2Blank = Field(validation_alias="start_date")
    # 结束时间 [原字段 'end_date']
    end_time: StrOrNone2Blank = Field(None, validation_alias="end_date")
    # 广告状态
    state: StrOrNone2Blank
    # 服务状态 [原字段 'serving_status']
    status: StrOrNone2Blank = Field(validation_alias="serving_status")
    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
    create_time_ts: IntOrNone2Zero = Field(validation_alias="creation_date")
    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date
    update_time_ts: IntOrNone2Zero = Field(validation_alias="last_updated_date")


class SdCampaigns(ResponseV1Token):
    """SD 广告活动列表"""

    data: list[SdCampaign]


# . SD Ad Groups
class SdAdGroup(BaseModel):
    """SD 广告组"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: int
    # 广告组名称 [原字段 'name']
    ad_group_name: str = Field(validation_alias="name")
    # 默认竞价
    default_bid: float
    # 竞价优化方式
    bid_optimization: str
    # 广告组状态
    state: StrOrNone2Blank
    # 服务状态 [原字段 'serving_status']
    status: StrOrNone2Blank = Field(validation_alias="serving_status")
    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
    create_time_ts: IntOrNone2Zero = Field(validation_alias="creation_date")
    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
    update_time_ts: IntOrNone2Zero = Field(validation_alias="last_updated_date")


class SdAdGroups(ResponseV1Token):
    """SD 广告组列表"""

    data: list[SdAdGroup]


# . SD Products
class SdProduct(BaseModel):
    """SD 商品投放"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 商品广告ID
    ad_id: int
    # 商品ASIN
    asin: str
    # 亚马逊SKU [原字段 'sku']
    msku: str = Field(validation_alias="sku")
    # 广告状态
    state: StrOrNone2Blank
    # 服务状态 [原字段 'serving_status']
    status: StrOrNone2Blank = Field(validation_alias="serving_status")
    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
    create_time_ts: IntOrNone2Zero = Field(validation_alias="creation_date")
    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
    update_time_ts: IntOrNone2Zero = Field(validation_alias="last_updated_date")


class SdProducts(ResponseV1Token):
    """SD 商品投放列表"""

    data: list[SdProduct]


# . SD Targets
class SdTarget(BaseModel):
    """SD 目标商品投放"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 目标商品广告ID
    target_id: int
    # 目标定位类型
    expression_type: str
    # 目标定位表达式 (JSON 字符串)
    expression: str
    # 目标定位解析表达式 (JSON 字符串) [原字段 'resolved_expression']
    expression_resolved: str = Field(validation_alias="resolved_expression")
    # 竞价
    bid: float
    # 广告状态
    state: StrOrNone2Blank
    # 服务状态 [原字段 'serving_status']
    status: StrOrNone2Blank = Field(validation_alias="serving_status")
    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
    create_time_ts: IntOrNone2Zero = Field(validation_alias="creation_date")
    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
    update_time_ts: IntOrNone2Zero = Field(validation_alias="last_updated_date")


class SdTargets(ResponseV1Token):
    """SD 目标商品投放列表"""

    data: list[SdTarget]


# . SD Negative Targets
class SdNegativeTarget(BaseModel):
    """SD 否定目标商品投放"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 否定目标商品广告ID
    target_id: int
    # 否定目标定位类型
    expression_type: str
    # 否定目标定位表达式 (JSON 字符串)
    expression: str
    # 否定目标定位解析表达式 (JSON 字符串) [原字段 'resolved_expression']
    expression_resolved: str = Field(validation_alias="resolved_expression")
    # 广告状态
    state: StrOrNone2Blank
    # 服务状态 [原字段 'serving_status']
    status: StrOrNone2Blank = Field(validation_alias="serving_status")
    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
    create_time_ts: IntOrNone2Zero = Field(validation_alias="creation_date")
    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
    update_time_ts: IntOrNone2Zero = Field(validation_alias="last_updated_date")


class SdNegativeTargets(ResponseV1Token):
    """SD 否定目标商品投放列表"""

    data: list[SdNegativeTarget]


# 报告 -------------------------------------------------------------------------------------------------------------------------
# 报告 - Sponsored Products - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# . SP Campaign Reports
class SpCampaignReport(BaseModel):
    """SP 广告活动报告"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 投放目标类型
    targeting_type: StrOrNone2Blank
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 直接广告成交商品件数 [原字段 'same_units']
    direct_units: int = Field(validation_alias="same_units")
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 报告日期
    report_date: str


class SpCampaignReports(ResponseV1Token):
    """SP 广告活动报告列表"""

    data: list[SpCampaignReport]


# . SP Campaign Hour Data
class SpCampaignHour(BaseModel):
    """SP 广告活动小时数据"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 直接广告成交商品件数 [原字段 'same_units']
    direct_units: int = Field(validation_alias="same_units")
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
    ctr: FloatOrNone2Zero
    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
    cvr: FloatOrNone2Zero
    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
    cpc: FloatOrNone2Zero
    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
    cpa: FloatOrNone2Zero
    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
    acos: FloatOrNone2Zero
    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
    roas: FloatOrNone2Zero
    # 数据所属小时 (0-23)
    hour: int
    # 报告日期
    report_date: str


class SpCampaignHourData(ResponseV1):
    """SP 广告活动小时数据列表"""

    data: list[SpCampaignHour]


# . SP Placement Reports
class SpCampaignReport(BaseModel):
    """SP 广告活动投放位置报告"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告投放位置 [原字段 'placement_type']
    placement: str = Field(validation_alias="placement_type")
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 直接广告成交商品件数 [原字段 'same_units']
    direct_units: int = Field(validation_alias="same_units")
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 报告日期
    report_date: str


class SpPlacementReports(ResponseV1Token):
    """SP 广告活动投放位置报告列表"""

    data: list[SpCampaignReport]


# . SP Placement Hour Data
class SpPlacementHour(BaseModel):
    """SP 广告活动投放位置小时数据"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告投放位置
    placement: str
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 直接广告成交商品件数 [原字段 'same_units']
    direct_units: int = Field(validation_alias="same_units")
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
    ctr: FloatOrNone2Zero
    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
    cvr: FloatOrNone2Zero
    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
    cpc: FloatOrNone2Zero
    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
    cpa: FloatOrNone2Zero
    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
    acos: FloatOrNone2Zero
    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
    roas: FloatOrNone2Zero
    # 数据所属小时 (0-23)
    hour: int
    # 报告日期
    report_date: str


class SpPlacementHourData(ResponseV1):
    """SP 广告活动投放位置小时数据列表"""

    data: list[SpPlacementHour]


# . SP Ad Group Reports
class SpAdGroupReport(BaseModel):
    """SP 广告组报告"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: int
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 直接广告成交商品件数 [原字段 'same_units']
    direct_units: int = Field(validation_alias="same_units")
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 报告日期
    report_date: str


class SpAdGroupReports(ResponseV1Token):
    """SP 广告组报告列表"""

    data: list[SpAdGroupReport]


# . SP Ad Group Hour Data
class SpAdGroupHour(BaseModel):
    """SP 广告组小时数据"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID [原字段 'group_id']
    ad_group_id: int = Field(validation_alias="group_id")
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 直接广告成交商品件数 [原字段 'same_units']
    direct_units: int = Field(validation_alias="same_units")
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
    ctr: FloatOrNone2Zero
    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
    cvr: FloatOrNone2Zero
    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
    cpc: FloatOrNone2Zero
    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
    cpa: FloatOrNone2Zero
    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
    acos: FloatOrNone2Zero
    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
    roas: FloatOrNone2Zero
    # 数据所属小时 (0-23)
    hour: int
    # 报告日期
    report_date: str


class SpAdGroupHourData(ResponseV1):
    """SP 广告组小时数据列表"""

    data: list[SpAdGroupHour]


# . SP Product Reports
class SpProductReport(BaseModel):
    """SP 商品投放报告"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 商品广告ID
    ad_id: int
    # 商品ASIN
    asin: str
    # 亚马逊SKU [原字段 'sku']
    msku: str = Field(validation_alias="sku")
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 直接广告成交商品件数 [原字段 'same_units']
    direct_units: int = Field(validation_alias="same_units")
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 报告日期
    report_date: str


class SpProductReports(ResponseV1Token):
    """SP 商品投放报告列表"""

    data: list[SpProductReport]


# , SP Product Hour Data
class SpProductHour(BaseModel):
    """SP 商品投放小时数据"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID [原字段 'group_id']
    ad_group_id: IntOrNone2Zero = Field(validation_alias="group_id")
    # 商品广告ID
    ad_id: int
    # 商品ASIN
    asin: str
    # 亚马逊SKU
    msku: str
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 直接广告成交商品件数 [原字段 'same_units']
    direct_units: int = Field(validation_alias="same_units")
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
    ctr: FloatOrNone2Zero
    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
    cvr: FloatOrNone2Zero
    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
    cpc: FloatOrNone2Zero
    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
    cpa: FloatOrNone2Zero
    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
    acos: FloatOrNone2Zero
    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
    roas: FloatOrNone2Zero
    # 数据所属小时 (0-23)
    hour: int
    # 报告日期
    report_date: str


class SpProductHourData(ResponseV1):
    """SP 商品投放小时数据列表"""

    data: list[SpProductHour]


# . SP Keyword Reports
class SpKeywordReport(BaseModel):
    """SP 关键词投放报告"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 关键词ID
    keyword_id: int
    # 关键词文本
    keyword_text: str
    # 关键词匹配类型
    match_type: str
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 直接广告成交商品件数 [原字段 'same_units']
    direct_units: int = Field(validation_alias="same_units")
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 报告日期
    report_date: str


class SpKeywordReports(ResponseV1Token):
    """SP 关键词投放报告列表"""

    data: list[SpKeywordReport]


# . SP Keyword Hour Data
class SpKeywordHour(BaseModel):
    """SP 关键词投放小时数据"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID [原字段 'group_id']
    ad_group_id: IntOrNone2Zero = Field(validation_alias="group_id")
    # 商品广告ID
    ad_id: int
    # 关键词ID [原字段 'targeting_id']
    keyword_id: int = Field(validation_alias="targeting_id")
    # 关键词文本 [原字段 'targeting']
    keyword_text: str = Field(validation_alias="targeting")
    # 关键词匹配类型
    match_type: str
    # 商品ASIN
    asin: str
    # 亚马逊SKU
    msku: str
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 直接广告成交商品件数 [原字段 'same_units']
    direct_units: int = Field(validation_alias="same_units")
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
    ctr: FloatOrNone2Zero
    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
    cvr: FloatOrNone2Zero
    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
    cpc: FloatOrNone2Zero
    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
    cpa: FloatOrNone2Zero
    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
    acos: FloatOrNone2Zero
    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
    roas: FloatOrNone2Zero
    # 数据所属小时 (0-23)
    hour: int
    # 报告日期
    report_date: str


class SpKeywordHourData(ResponseV1):
    """SP 关键词投放小时数据列表"""

    data: list[SpKeywordHour]


# . SP Target Reports
class SpTargetReport(BaseModel):
    """SP 目标商品投放报告"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 目标商品广告ID
    target_id: int
    # 目标定位表达式类型 [原字段 'targeting_type']
    expression_type: StrOrNone2Blank = Field(validation_alias="targeting_type")
    # 目标定位表达式 (JSON 字符串) [原字段 'targeting_expression']
    expression: str = Field(validation_alias="targeting_expression")
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 直接广告成交商品件数 [原字段 'same_units']
    direct_units: int = Field(validation_alias="same_units")
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 报告日期
    report_date: str


class SpTargetReports(ResponseV1Token):
    """SP 目标商品投放报告列表"""

    data: list[SpTargetReport]


# . SP Target Hour Data
class SpTargetHour(BaseModel):
    """SP 目标商品投放小时数据"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID [原字段 'group_id']
    ad_group_id: IntOrNone2Zero = Field(validation_alias="group_id")
    # 商品广告ID
    ad_id: int
    # 目标商品广告ID [原字段 'targeting_id']
    target_id: int = Field(validation_alias="targeting_id")
    # 目标商品文本 [原字段 'targeting']
    target_text: str = Field(validation_alias="targeting")
    # 目标匹配类型 [原字段 'match_type']
    target_type: str = Field(validation_alias="match_type")
    # 商品ASIN
    asin: str
    # 亚马逊SKU
    msku: str
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 直接广告成交商品件数 [原字段 'same_units']
    direct_units: int = Field(validation_alias="same_units")
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
    ctr: FloatOrNone2Zero
    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
    cvr: FloatOrNone2Zero
    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
    cpc: FloatOrNone2Zero
    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
    cpa: FloatOrNone2Zero
    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
    acos: FloatOrNone2Zero
    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
    roas: FloatOrNone2Zero
    # 数据所属小时 (0-23)
    hour: int
    # 报告日期
    report_date: str


class SpTargetHourData(ResponseV1):
    """SP 目标商品投放小时数据列表"""

    data: list[SpTargetHour]


# . SP Query Word Reports
class SpQueryWordReport(BaseModel):
    """SP 用户搜索词报告"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 关键词ID [原字段 'target_id']
    keyword_id: int = Field(validation_alias="target_id")
    # 关键词文本 [原字段 'target_text']
    keyword_text: str = Field(validation_alias="target_text")
    # 用户使用搜索词 [原字段 'query']
    query_text: str = Field(validation_alias="query")
    # 关键词匹配类型
    match_type: str
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 直接广告成交商品件数 [原字段 'same_units']
    direct_units: int = Field(validation_alias="same_units")
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 报告日期
    report_date: str


class SpQueryWordReports(ResponseV1Token):
    """SP 用户搜索词报告列表"""

    data: list[SpQueryWordReport]


# 报告 - Sponsored Brands - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# . SB Campaign Reports
class SbCampaignReport(BaseModel):
    """SB 广告活动报告"""

    # fmt: off
    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 品牌新买家广告订单数
    new_to_brand_orders: int
    # 品牌新买家订单占比 [原字段 'new_to_brand_order_percentage']
    # (品牌新买家广告订单数 / 广告订单数 x 100%)
    new_to_brand_order_pct: float = Field(validation_alias="new_to_brand_order_percentage")
    # 品牌新买家订单转化率 
    # (品牌新买家广告订单数 / 总点击次数 x 100%)
    new_to_brand_order_rate: float
    # 广告成交商品件数
    units: int
    # 直接广告成交商品件数 [原字段 'same_units']
    direct_units: int = Field(validation_alias="same_units")
    # 品牌新买家成交商品件数
    new_to_brand_units: int
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 品牌新买家销售额
    new_to_brand_sales: float
    # 广告可见率 - View Through Rate 
    # (可见展示次数 / 总展示次数 x 100%)
    vtr: float
    # 广告可见点击率 - View Click Through Rate 
    # (总点击次数 / 可见展示次数 x 100%)
    vctr: float
    # 报告日期
    report_date: str
    # fmt: on


class SbCampaignReports(ResponseV1Token):
    """SB 广告活动报告列表"""

    data: list[SbCampaignReport]


# . SB Campaign Hour Data
class SbCampaignHour(BaseModel):
    """SB 广告活动小时数据"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
    ctr: FloatOrNone2Zero
    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
    cvr: FloatOrNone2Zero
    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
    cpc: FloatOrNone2Zero
    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
    cpa: FloatOrNone2Zero
    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
    acos: FloatOrNone2Zero
    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
    roas: FloatOrNone2Zero
    # 数据所属小时 (0-23)
    hour: int
    # 报告日期
    report_date: str


class SbCampaignHourData(ResponseV1):
    """SB 广告活动小时数据列表"""

    data: list[SbCampaignHour]


# . SB Campaign Placement Reports
class SbPlacementReprot(BaseModel):
    """SB 广告活动投放位置报告"""

    # fmt: off
    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告投放位置 [原字段 'placement_type']
    placement: str = Field(validation_alias="placement_type")
    # 广告创意类型
    creative_type: str
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 品牌新买家广告订单数
    new_to_brand_orders: int
    # 品牌新买家订单占比 [原字段 'new_to_brand_order_percentage']
    # (品牌新买家广告订单数 / 广告订单数 x 100%)
    new_to_brand_order_pct: float = Field(validation_alias="new_to_brand_order_percentage")
    # 品牌新买家订单转化率
    # (品牌新买家广告订单数 / 总点击次数 x 100%)
    new_to_brand_order_rate: float
    # 广告成交商品件数
    units: int
    # 直接广告成交商品件数 [原字段 'same_units']
    direct_units: int = Field(validation_alias="same_units")
    # 品牌新买家成交商品件数
    new_to_brand_units: int
    # 广告销售额
    sales: float
    # 品牌新买家销售额
    new_to_brand_sales: float
    # 报告日期
    report_date: str
    # fmt: on


class SbPlacementReports(ResponseV1Token):
    """SB 广告活动投放位置报告列表"""

    data: list[SbPlacementReprot]


# . SB Campaign Placement Hour Data
class SbPlacementHour(BaseModel):
    """SB 广告活动投放位置小时数据"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告投放位置
    placement: str
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
    ctr: FloatOrNone2Zero
    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
    cvr: FloatOrNone2Zero
    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
    cpc: FloatOrNone2Zero
    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
    cpa: FloatOrNone2Zero
    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
    acos: FloatOrNone2Zero
    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
    roas: FloatOrNone2Zero
    # 数据所属小时 (0-23)
    hour: int
    # 报告日期
    report_date: str


class SbPlacementHourData(ResponseV1):
    """SB 广告活动投放位置小时数据列表"""

    data: list[SbPlacementHour]


# . SB Ad Group Reports
class SbAdGroupReport(BaseModel):
    """SB 广告组报告"""

    # fmt: off
    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: int
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 品牌新买家广告订单数
    new_to_brand_orders: int
    # 品牌新买家订单占比 [原字段 'new_to_brand_order_percentage']
    # (品牌新买家广告订单数 / 广告订单数 x 100%)
    new_to_brand_order_pct: float = Field(validation_alias="new_to_brand_order_percentage")
    # 品牌新买家订单转化率
    # (品牌新买家广告订单数 / 总点击次数 x 100%)
    new_to_brand_order_rate: float
    # 广告成交商品件数
    units: int
    # 直接广告成交商品件数 [原字段 'same_units']
    direct_units: int = Field(validation_alias="same_units")
    # 品牌新买家成交商品件数
    new_to_brand_units: int
    # 广告销售额
    sales: float
    # 品牌新买家销售额
    new_to_brand_sales: float
    # 广告可见率 - View Through Rate
    # (可见展示次数 / 总展示次数 x 100%)
    vtr: float
    # 广告可见点击率 - View Click Through Rate
    # (总点击次数 / 可见展示次数 x 100%)
    vctr: float
    # 报告日期
    report_date: str
    # fmt: on


class SbAdGroupReports(ResponseV1Token):
    """SB 广告组报告列表"""

    data: list[SbAdGroupReport]


# . SB Ad Group Hour Data
class SbAdGroupHour(BaseModel):
    """SB 广告组小时数据"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID [原字段 'group_id']
    ad_group_id: int = Field(validation_alias="group_id")
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
    ctr: FloatOrNone2Zero
    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
    cvr: FloatOrNone2Zero
    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
    cpc: FloatOrNone2Zero
    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
    cpa: FloatOrNone2Zero
    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
    acos: FloatOrNone2Zero
    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
    roas: FloatOrNone2Zero
    # 数据所属小时 (0-23)
    hour: int
    # 报告日期
    report_date: str

    {
        "profile_id": 494383675863017,
        "campaign_id": 404109386867496,
        "ad_group_id": 328051704994534,
        "cost": 1.42,
        "impressions": 76,
        "clicks": 1,
        "orders": 1,
        "direct_orders": 1,
        "units": 1,
        "sales": 35.0,
        "direct_sales": 35.0,
        "ctr": 0.0132,
        "cvr": 1.0,
        "cpc": 1.42,
        "cpa": 1.42,
        "acos": 0.0406,
        "roas": 24.65,
        "hour": 21,
        "report_date": "2025-08-25",
    }


class SbAdGroupHourData(ResponseV1):
    """SB 广告组小时数据列表"""

    data: list[SbAdGroupHour]


# . SB Creative Reports
class SbCreativeReport(BaseModel):
    """SB 广告创意报告"""

    # fmt: off
    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 广告创意ID [原字段 'ad_creative_id']
    creative_id: int = Field(validation_alias="ad_creative_id")
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 品牌新买家广告订单数
    new_to_brand_orders: int
    # 品牌新买家订单占比 [原字段 'new_to_brand_order_percentage']
    # (品牌新买家广告订单数 / 广告订单数 x 100%)
    new_to_brand_order_pct: float = Field(validation_alias="new_to_brand_order_percentage")
    # 品牌新买家订单转化率
    # (品牌新买家广告订单数 / 总点击次数 x 100%)
    new_to_brand_order_rate: float
    # 广告成交商品件数
    units: int
    # 直接广告成交商品件数 [原字段 'same_units']
    direct_units: int = Field(validation_alias="same_units")
    # 品牌新买家成交商品件数
    new_to_brand_units: int
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 品牌新买家销售额
    new_to_brand_sales: float
    # 广告可见率 - View Through Rate
    # (可见展示次数 / 总展示次数 x 100%)
    vtr: float
    # 广告可见点击率 - View Click Through Rate
    # (总点击次数 / 可见展示次数 x 100%)
    vctr: float
    # 报告日期
    report_date: str
    # fmt: on


class SbCreativeReports(ResponseV1Token):
    """SB 广告创意报告列表"""

    data: list[SbCreativeReport]


# . SB Keyword Reports
class SbKeywordReport(BaseModel):
    """SB 关键词投放报告"""

    # fmt: off
    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 关键词ID
    keyword_id: int
    # 广告创意类型
    creative_type: str
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 品牌新买家广告订单数
    new_to_brand_orders: int
    # 品牌新买家订单占比 [原字段 'new_to_brand_order_percentage']
    # (品牌新买家广告订单数 / 广告订单数 x 100%)
    new_to_brand_order_pct: float = Field(validation_alias="new_to_brand_order_percentage")
    # 品牌新买家订单转化率
    # (品牌新买家广告订单数 / 总点击次数 x 100%)
    new_to_brand_order_rate: float
    # 广告成交商品件数
    units: int
    # 直接广告成交商品件数 [原字段 'same_units']
    direct_units: int = Field(validation_alias="same_units")
    # 品牌新买家成交商品件数
    new_to_brand_units: int
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 品牌新买家销售额
    new_to_brand_sales: float
    # 报告日期
    report_date: str
    # fmt: on


class SbKeywordReports(ResponseV1Token):
    """SB 关键词投放报告列表"""

    data: list[SbKeywordReport]


# . SB Target Reports
class SbTargetReport(BaseModel):
    """SB 目标商品投放报告"""

    # fmt: off
    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 目标商品广告ID
    target_id: int
    # 广告创意类型
    creative_type: str
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 品牌新买家广告订单数
    new_to_brand_orders: int
    # 品牌新买家订单占比 [原字段 'new_to_brand_order_percentage']
    # (品牌新买家广告订单数 / 广告订单数 x 100%)
    new_to_brand_order_pct: float = Field(validation_alias="new_to_brand_order_percentage")
    # 品牌新买家订单转化率
    # (品牌新买家广告订单数 / 总点击次数 x 100%)
    new_to_brand_order_rate: float
    # 广告成交商品件数
    units: int
    # 直接广告成交商品件数 [原字段 'same_units']
    direct_units: int = Field(validation_alias="same_units")
    # 品牌新买家成交商品件数
    new_to_brand_units: int
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 品牌新买家销售额
    new_to_brand_sales: float
    # 报告日期
    report_date: str
    # fmt: on


class SbTargetReports(ResponseV1Token):
    """SB 目标商品投放报告列表"""

    data: list[SbTargetReport]


# . SB Targeting Hour Data
class SbTargetingHour(BaseModel):
    """SB 目标关键词或商品投放小时数据"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID [原字段 'group_id']
    ad_group_id: IntOrNone2Zero = Field(validation_alias="group_id")
    # 目标定位ID (keyword_id 或 target_id)
    targeting_id: int
    # 目标定位文本 [原字段 'targeting']
    targeting_text: str = Field(validation_alias="targeting")
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
    ctr: FloatOrNone2Zero
    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
    cvr: FloatOrNone2Zero
    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
    cpc: FloatOrNone2Zero
    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
    cpa: FloatOrNone2Zero
    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
    acos: FloatOrNone2Zero
    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
    roas: FloatOrNone2Zero
    # 数据所属小时 (0-23)
    hour: int
    # 报告日期
    report_date: str


class SbTargetingHourData(ResponseV1):
    """SB 目标关键词或商品投放小时数据列表"""

    data: list[SbTargetingHour]


# . SB Query Word Reports
class SbQueryWordReport(BaseModel):
    """SB 用户搜索词报告"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 关键词ID [原字段 'target_id']
    keyword_id: int = Field(validation_alias="target_id")
    # 关键词文本 [原字段 'target_text']
    keyword_text: str = Field(validation_alias="target_text")
    # 用户使用搜索词 [原字段 'query']
    query_text: str = Field(validation_alias="query")
    # 关键词匹配类型
    match_type: str
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 广告销售额
    sales: float
    # 视频广告播放25%次数 [原字段 'video_first_quartile_views']
    video_25pct_views: int = Field(validation_alias="video_first_quartile_views")
    # 视频广告播放50%次数 [原字段 'video_midpoint_views']
    video_50pct_views: int = Field(validation_alias="video_midpoint_views")
    # 视频广告播放75%次数 [原字段 'video_third_quartile_views']
    video_75pct_views: int = Field(validation_alias="video_third_quartile_views")
    # 视频广告播放100%次数 [原字段 'video_complete_views']
    video_100pct_views: int = Field(validation_alias="video_complete_views")
    # 视频广告播放5秒次数 [原字段 'video_5_second_views']
    video_5sec_views: int = Field(validation_alias="video_5_second_views")
    # 视频广告播放5秒观看率 [原字段 'video_5_second_view_rate']
    video_5sec_view_rate: float = Field(validation_alias="video_5_second_view_rate")
    # 视频广告静音取消次数 [原字段 'video_unmutes']
    video_unmutes: int = Field(validation_alias="video_unmutes")
    # 报告日期
    report_date: str


class SbQueryWordReports(ResponseV1Token):
    """SB 用户搜索词报告列表"""

    data: list[SbQueryWordReport]


# . SB ASIN Attribution Reports
class SbAsinAttributionReport(BaseModel):
    """SB 广告商品归因报告"""

    # fmt: off
    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告活动名称
    campaign_name: str
    # 广告组ID
    ad_group_id: int
    # 广告组名称
    ad_group_name: str
    # 归因类型
    attribution_type: str
    # 商品ASIN
    asin: str
    # 广告14天订单数 [原字段 'orders14d']
    orders_14d: int = Field(validation_alias="orders14d")
    # 品牌新买家14天订单数 [原字段 'new_to_brand_purchases14d']
    new_to_brand_orders_14d: int = Field(validation_alias="new_to_brand_purchases14d")
    # 品牌新买家订单占比14天 [原字段 'new_to_brand_purchases_percentage14d']
    # (品牌新买家14天订单数 / 广告14天订单数 x 100%)
    new_to_brand_order_pct_14d: float = Field(validation_alias="new_to_brand_purchases_percentage14d")
    # 广告14天成交商品件数 [原字段 'units_sold14d']
    units_14d: int = Field(validation_alias="units_sold14d")
    # 品牌新买家14天成交商品件数 [原字段 'new_to_brand_units_sold14d']
    new_to_brand_units_14d: int = Field(validation_alias="new_to_brand_units_sold14d")
    # 品牌新买家成交商品件数占比14天 [原字段 'new_to_brand_units_sold_percentage14d']
    # (品牌新买家14天成交商品件数 / 广告14天成交商品件数 x 100%)
    new_to_brand_units_pct_14d: float = Field(validation_alias="new_to_brand_units_sold_percentage14d")
    # 广告14天销售
    sales_14d: float = Field(validation_alias="sales14d")
    # 品牌新买家14天销售额 [原字段 'new_to_brand_sales14d']
    new_to_brand_sales_14d: float = Field(validation_alias="new_to_brand_sales14d")
    # 品牌新买家销售额占比14天 [原字段 'new_to_brand_sales_percentage14d']
    # (品牌新买家14天销售额 / 广告14天销售 x 100%)
    new_to_brand_sales_pct_14d: float = Field(validation_alias="new_to_brand_sales_percentage14d")
    # 报告日期
    report_date: str
    # fmt: on


class SbAsinAttributionReports(ResponseV1Token):
    """SB 广告商品归因报告列表"""

    data: list[SbAsinAttributionReport]


# . SB Cost Allocation Reports
class SbCostAllocationReport(BaseModel):
    """SB 广告费用分摊报告"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 部门ID
    department_id: IntOrNone2Zero
    # 设置分摊的事务ID, 用于追踪具体的分摊规则 (UUID) [原字段 'transaction_uuid']
    allocation_rule_id: StrOrNone2Blank = Field(validation_alias="transaction_uuid")
    # 分摊产品的MD5值 (ad_group_id, asin, sku) [原字段 'divide_asin_md5']
    allocation_asin_id: str = Field(validation_alias="divide_asin_md5")
    # 分摊比率 (0.0 - 1.0) [原字段 'percent']
    allocation_ratio: float = Field(validation_alias="percent")
    # 商品ASIN
    asin: str
    # 商品SKU [原字段 'sku']
    msku: str = Field(validation_alias="sku")
    # 分摊后的广告花费 [原字段 'spends']
    costs: float = Field(validation_alias="spends")
    # 分摊后的展示次数
    impressions: float
    # 分摊后的点击次数
    clicks: float
    # 分摊后的广告订单数
    orders: float
    # 分摊后的直接广告订单数 [原字段 'same_orders']
    direct_orders: float = Field(validation_alias="same_orders")
    # 分摊后的广告成交商品件数 [原字段 'units_sold']
    units: float = Field(validation_alias="units_sold")
    # 分摊后的直接广告成交商品件数 [原字段 'same_units_sold']
    direct_units: float = Field(validation_alias="same_units_sold")
    # 分摊后的广告销售额
    sales: float
    # 分摊后的直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 报告日期
    report_date: str


class SbCostAllocationReports(ResponseV1Token):
    """SB 广告费用分摊报告"""

    data: list[SbCostAllocationReport]


# 报告 - Sponsored Display - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# . SD Campaign Reports
class SdCampaignReport(BaseModel):
    """SD 广告活动报告"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 投放策略
    tactic: str
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 可见展示次数 [原字段 'view_impressions']
    viewable_impressions: int = Field(validation_alias="view_impressions")
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 报告日期
    report_date: str


class SdCampaignReports(ResponseV1Token):
    """SD 广告活动报告列表"""

    data: list[SdCampaignReport]


# . SD Campaign Hour Data
class SdCampaignHour(BaseModel):
    """SD 广告活动小时数据"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
    ctr: FloatOrNone2Zero
    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
    cvr: FloatOrNone2Zero
    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
    cpc: FloatOrNone2Zero
    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
    cpa: FloatOrNone2Zero
    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
    acos: FloatOrNone2Zero
    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
    roas: FloatOrNone2Zero
    # 数据所属小时 (0-23)
    hour: int
    # 报告日期
    report_date: str


class SdCampaignHourData(ResponseV1):
    """SD 广告活动小时数据列表"""

    data: list[SdCampaignHour]


# . SD Ad Group Reports
class SdAdGroupReport(BaseModel):
    """SD 广告组报告"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: int
    # 投放策略
    tactic: str
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 可见展示次数 [原字段 'view_impressions']
    viewable_impressions: int = Field(validation_alias="view_impressions")
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 报告日期
    report_date: str


class SdAdGroupReports(ResponseV1Token):
    """SD 广告组报告列表"""

    data: list[SdAdGroupReport]


# . SD Ad Group Hour Data
class SdAdGroupHour(BaseModel):
    """SD 广告组小时数据"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID [原字段 'group_id']
    ad_group_id: int = Field(validation_alias="group_id")
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
    ctr: FloatOrNone2Zero
    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
    cvr: FloatOrNone2Zero
    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
    cpc: FloatOrNone2Zero
    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
    cpa: FloatOrNone2Zero
    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
    acos: FloatOrNone2Zero
    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
    roas: FloatOrNone2Zero
    # 数据所属小时 (0-23)
    hour: int
    # 报告日期
    report_date: str


class SdAdGroupHourData(ResponseV1):
    """SD 广告组小时数据列表"""

    data: list[SdAdGroupHour]


# . SD Product Reports
class SdProductReport(BaseModel):
    """SD 商品投放报告"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 商品广告ID
    ad_id: int
    # 投放策略
    tactic: str
    # 商品ASIN
    asin: str
    # 亚马逊SKU [原字段 'sku']
    msku: str = Field(validation_alias="sku")
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 可见展示次数 [原字段 'view_impressions']
    viewable_impressions: int = Field(validation_alias="view_impressions")
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 报告日期
    report_date: str


class SdProductReports(ResponseV1Token):
    """SD 商品投放报告列表"""

    data: list[SdProductReport]


# . SD Product Hour Data
class SpdProductHour(BaseModel):
    """SD 商品投放小时数据"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID [原字段 'group_id']
    ad_group_id: IntOrNone2Zero = Field(validation_alias="group_id")
    # 商品广告ID
    ad_id: int
    # 商品ASIN
    asin: str
    # 亚马逊SKU
    msku: str
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
    ctr: FloatOrNone2Zero
    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
    cvr: FloatOrNone2Zero
    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
    cpc: FloatOrNone2Zero
    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
    cpa: FloatOrNone2Zero
    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
    acos: FloatOrNone2Zero
    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
    roas: FloatOrNone2Zero
    # 数据所属小时 (0-23)
    hour: int
    # 报告日期
    report_date: str


class SdProductHourData(ResponseV1):
    """SD 商品投放小时数据列表"""

    data: list[SpdProductHour]


# . SD Target Reports
class SdTargetReport(BaseModel):
    """SD 目标商品投放报告"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 目标商品广告ID
    target_id: int
    # 目标商品文本 [原字段 'targeting_expression']
    target_text: str = Field(validation_alias="targeting_expression")
    # 目标定位类型 [原字段 'targeting_type']
    expression_type: StrOrNone2Blank = Field(validation_alias="targeting_type")
    # 目标定位表达式 (JSON 字符串) [原字段 'targeting_text']
    expression: str = Field(validation_alias="targeting_text")
    # 投放策略
    tactic: str
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 可见展示次数 [原字段 'view_impressions']
    viewable_impressions: int = Field(validation_alias="view_impressions")
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 报告日期
    report_date: str


class SdTargetReports(ResponseV1Token):
    """SD 目标商品投放报告列表"""

    data: list[SdTargetReport]


# . SD Target Hour Data
class SdTargetHour(BaseModel):
    """SD 目标商品投放小时数据"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID [原字段 'group_id']
    ad_group_id: IntOrNone2Zero = Field(validation_alias="group_id")
    # 商品广告ID
    ad_id: int
    # 目标商品广告ID [原字段 'targeting_id']
    target_id: int = Field(validation_alias="targeting_id")
    # 目标定位文本 [原字段 'targeting']
    target_text: str = Field(validation_alias="targeting")
    # 商品ASIN
    asin: str
    # 亚马逊SKU
    msku: str
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 广告成交商品件数
    units: int
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
    ctr: FloatOrNone2Zero
    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
    cvr: FloatOrNone2Zero
    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
    cpc: FloatOrNone2Zero
    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
    cpa: FloatOrNone2Zero
    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
    acos: FloatOrNone2Zero
    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
    roas: FloatOrNone2Zero
    # 数据所属小时 (0-23)
    hour: int
    # 报告日期
    report_date: str


class SdTargetHourData(ResponseV1):
    """SD 目标商品投放小时数据列表"""

    data: list[SdTargetHour]


# . SD Matched Target Reports
class SdMatchedTargetReport(BaseModel):
    """SD 匹配的目标商品投放报告"""

    # 亚马逊店铺ID (广告帐号ID)
    profile_id: int
    # 广告活动ID
    campaign_id: int
    # 广告组ID
    ad_group_id: IntOrNone2Zero
    # 目标商品广告ID
    target_id: int
    # 目标定位表达式 (JSON 字符串) [原字段 'target_text']
    expression: str = Field(validation_alias="target_text")
    # 匹配的目标商品 (ASIN)
    matched_target: str
    # 货币代码 [原字段 'currency']
    currency_code: StrOrNone2Blank = Field(validation_alias="currency")
    # 广告花费
    cost: float
    # 总展示次数
    impressions: int
    # 可见展示次数 [原字段 'view_impressions']
    viewable_impressions: int = Field(validation_alias="view_impressions")
    # 总点击次数
    clicks: int
    # 广告订单数
    orders: int
    # 直接广告订单数 [原字段 'same_orders']
    direct_orders: int = Field(validation_alias="same_orders")
    # 品牌新买家广告订单数
    new_to_brand_orders: int
    # 广告成交商品件数
    units: int
    # 品牌新买家成交商品件数
    new_to_brand_units: int
    # 广告销售额
    sales: float
    # 直接广告销售额 [原字段 'same_sales']
    direct_sales: float = Field(validation_alias="same_sales")
    # 品牌新买家销售额
    new_to_brand_sales: float
    # 报告日期
    report_date: str


class SdMatchedTargetReports(ResponseV1Token):
    """SD 匹配的目标商品投放报告列表"""

    data: list[SdMatchedTargetReport]


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
    value: str


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
    operator_id: int = Field(validation_alias="user_id")
    # 操作用户名称 [原字段 'user_name']
    operator_name: str = Field(validation_alias="user_name")
    # 操作对象 [原字段 'operate_type']
    operation_target: str = Field(validation_alias="operate_type")
    # 操作类型 [原字段 'change_type']
    operation_type: str = Field(validation_alias="change_type")
    # 操作来源 [原字段 'function_name']
    operation_source: str = Field(validation_alias="function_name")
    # 操作时间 [原字段 'operate_time']
    operation_time: str = Field(validation_alias="operate_time")
    # 操作前列表 [原字段 'operate_before']
    before: list[AdsOperation] = Field(validation_alias="operate_before")
    # 操作后列表 [原字段 'operate_after']
    after: list[AdsOperation] = Field(validation_alias="operate_after")


class AdsOperationLogs(ResponseV1):
    """广告操作日志"""

    data: list[AdsOperationLog]
