# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import ValidationInfo, Field, field_validator
from lingxingapi import utils
from lingxingapi.base.param import Parameter, PageOffestAndLength
from lingxingapi.fields import NonEmptyStr, CountryCode, NonNegativeInt


# 基础数据 ----------------------------------------------------------------------------------------------------------------------
# . Ads Profiles
class AdProfiles(PageOffestAndLength):
    """查询广告账号参数"""

    profile_type: NonEmptyStr = Field(alias="type")


# . Ads Entities (Portfolios, Campaigns, etc.)
class AdEntities(PageOffestAndLength):
    """查询广告组合参数"""

    # 领星店铺ID
    sid: Optional[NonNegativeInt] = None
    # 亚马逊店铺ID [广告帐号ID] (AdsProfiles.profile_id)
    profile_id: NonNegativeInt
    # 广告组合状态 ("enabled", "paused", "archived" | 默认所有)
    state: Optional[NonEmptyStr] = None
    # 分页游标, 上次分页结果中的next_token
    next_token: Optional[NonEmptyStr] = None


# . SP Negative Targets
class SpNegativeTargeting(AdEntities):
    """查询 SP 否定投放参数"""

    # 否定投放类型 ("keyword", "target")
    target_type: NonEmptyStr
    # 广告活动ID
    campaign_id: Optional[NonNegativeInt] = None


# . SB Targets
class SbTargeting(AdEntities):
    """查询 SP 广告投放目标参数"""

    # SB广告类型 ('SB', 'SBV', 'ALL')
    ad_type: NonEmptyStr = Field(alias="ads_type")
    # 投放目标类型 ('keyword', 'product', 'ALL')
    target_type: NonEmptyStr = Field(alias="targeting_type")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("target_type", mode="before")
    @classmethod
    def _validate_target_type(cls, v: str) -> str:
        return "producttarget" if v == "product" else v


# 报告 -------------------------------------------------------------------------------------------------------------------------
# . Ad Reports
class AdReports(AdEntities):
    """查询广告报告参数"""

    # 报告日期
    report_date: str
    # 是否展示完整归因期信息 (0: 否, 1: 是 | 默认: 0)
    show_detail: Optional[NonNegativeInt] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("report_date", mode="before")
    @classmethod
    def _validate_report_date(cls, v: str) -> str:
        dt = utils.validate_datetime(v, False, "广告报告日期")
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)


# . Ad Hour Reports
class AdHourData(Parameter):
    """查询广告的小时报告参数"""

    # 报告日期 (只能查询最近60天内的数据)
    report_date: str
    # 广告活动ID
    campaign_id: NonNegativeInt
    # 聚合纬度
    agg_dimension: Optional[NonEmptyStr] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("report_date", mode="before")
    @classmethod
    def _validate_report_date(cls, v: str) -> str:
        dt = utils.validate_datetime(v, False, "广告报告日期")
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)


# . SP Query Reports
class SpQueryReports(AdReports):
    """查询 SP 用户搜索词报告参数"""

    # 投放目标类型 ('keyword', 'product')
    target_type: NonEmptyStr


# . SB Target Reports
class SbTargetingReports(AdReports):
    """查询 SB 广告投放目标报告参数"""

    # SB广告类型 ('SB', 'SBV', 'ALL' - 当前只支持'ALL')
    ad_type: NonEmptyStr = Field(alias="sponsored_type")
    # 投放目标类型 ('keyword', 'product', 'ALL')
    target_type: NonEmptyStr

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("target_type", mode="before")
    @classmethod
    def _validate_target_type(cls, v: str) -> str:
        return "producttarget" if v == "product" else v


# . SB Query Reports
class SbQueryReports(AdReports):
    """查询 SB 用户搜索词报告参数"""

    # 投放目标类型 ('keyword', 'product' - 当前只支持'keyword')
    target_type: NonEmptyStr


# . DSP Reports
class DspReports(PageOffestAndLength):
    """查询 DSP 报告参数"""

    # 开始日期, 双闭区间, 时间间隔最长不超过90天
    start_date: str
    # 结束日期, 双闭区间, 时间间隔最长不超过90天
    end_date: str
    # 亚马逊店铺ID [广告帐号ID] (AdsProfiles.profile_id)
    profile_id: NonNegativeInt

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v: str, info: ValidationInfo) -> str:
        dt = utils.validate_datetime(v, False, "DSP报告日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)


# 报表下载 ----------------------------------------------------------------------------------------------------------------------
# . Download ABA Report
class DownloadAbaReport(Parameter):
    """查询 Amazon ABA 报表下载参数"""

    # 国家代码
    country_code: CountryCode = Field(alias="country")
    # 开始日期, 报表开始日期, 自动会调整为当周周日
    start_date: str = Field(alias="data_start_time")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("start_date", mode="before")
    @classmethod
    def _validate_start_date(cls, v: str) -> str:
        dt = utils.validate_datetime(v, False, "ABA报表开始日期").to_sunday()
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)


# 操作日志 ----------------------------------------------------------------------------------------------------------------------
# . Ads Operation Logs
class AdsOperationLogs(PageOffestAndLength):
    """查询广告操作日志参数"""

    # 领星店铺ID
    sid: NonNegativeInt
    # 开始日期, 日期间隔不能超过1个月
    start_date: str
    # 结束日期, 日期间隔不能超过1个月
    end_date: str
    # 广告类型 ('sp', 'sb', 'sd')
    ad_type: str = Field(alias="sponsored_type")
    # 操作对象
    # - campaigns 广告活动
    # - adGroups 广告组
    # - productAds 广告
    # - keywords 关键词
    # - negativeKeywords 否定关键词
    # - targets 商品投放
    # - negativeTargets 否定商品投放
    # - profiles 预算设置
    operation_target: NonEmptyStr = Field(alias="operate_type")
    # 日志来源
    log_source: NonEmptyStr

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v: str, info: ValidationInfo) -> str:
        dt = utils.validate_datetime(v, False, "广告操作日志日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)

    @field_validator("ad_type", mode="before")
    @classmethod
    def _validate_ad_type(cls, v) -> str:
        if not isinstance(v, str):
            raise ValueError("广告类型必须是字符串")
        return v.lower()
