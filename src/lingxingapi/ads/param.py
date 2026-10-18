# -*- coding: utf-8 -*-
from __future__ import annotations

import datetime
from typing import Optional
from pydantic import ValidationInfo, Field, field_serializer, field_validator, model_validator
from lingxingapi import utils
from lingxingapi.base.param import Parameter, PageOffestAndLength
from lingxingapi.fields import NonEmptyStr, CountryCode, NonNegativeInt


# 基础数据 ----------------------------------------------------------------------------------------------------------------------
# . Ads Profiles
class AdProfiles(PageOffestAndLength):
    """查询广告账号参数。

    账号类型在模型中必填；SDK 方法默认传入 "seller"。

    Args:
        profile_type (str): 广告账号类型，去除首尾空白后必须非空；请求别名为 type。
        offset (int | None): 分页偏移量，默认 None；None 不输出到请求字典，0 保留。
        length (int | None): 分页长度，默认 None；None 不输出到请求字典，0 保留。

    Raises:
        pydantic.ValidationError: 账号类型缺失或不符合非空字符串规则，或分页参数
            无法按现有规则解析为非负整数。

    Examples:
        查询 seller 类型广告账号，从第0条开始返回最多20条记录。

        >>> AdProfiles(profile_type="seller", offset=0, length=20).model_dump_params()
        {'length': 20, 'offset': 0, 'type': 'seller'}
        >>> AdProfiles.model_validate_params({"type": "seller"})
        {'type': 'seller'}
    """

    profile_type: NonEmptyStr = Field(
        description="广告账号类型",
        examples=["seller"],
        # - - - - - - - - - -
        alias="type",
    )


# . Ads Entities (Portfolios, Campaigns, etc.)
class AdEntities(PageOffestAndLength):
    """查询广告实体参数，sid 与 profile_id 至少提供一项。

    标识沿用现有非负整数校验，0 保留；同时提供时保留两者，None 在请求字典中省略。

    Args:
        sid (int | None): 领星店铺ID，默认 None。
        profile_id (int | None): 广告账号ID，默认 None；Portfolios 同时提供两个标识时，以 profile_id 指定的广告账号为准。其他接口按各自的账号选择规则处理。
        state (str | None): 广告实体状态，默认 None 并省略请求键，给定字符串去除首尾空白后须非空。
        next_token (str | None): 上一页返回的分页游标，默认 None 并省略请求键；Portfolios 同时提供 offset 时按游标定位。
        offset (int | None): 非负分页偏移量，默认 None 并省略请求键，0 保留。
        length (int | None): 非负分页长度，默认 None 并省略请求键，0 保留。

    Raises:
        pydantic.ValidationError: 两个标识均缺失或为 None，或任一给定值不符合
            现有字段校验规则。

    Examples:
        使用店铺ID或广告账号ID指定查询账号。

        >>> AdEntities.model_validate_params({"sid": 1212})
        {'sid': 1212}
        >>> AdEntities.model_validate_params({"profile_id": 90000000000003})
        {'profile_id': 90000000000003}
        >>> AdEntities.model_validate_params({"sid": 1212, "profile_id": 90000000000003})
        {'profile_id': 90000000000003, 'sid': 1212}
    """

    sid: Optional[NonNegativeInt] = Field(
        description="领星店铺ID",
        examples=[1212],
        # - - - - - - - - - -
        default=None,
    )
    profile_id: Optional[NonNegativeInt] = Field(
        description="广告账号ID (AdProfiles.profile_id)；与 sid 至少提供一项；Portfolios 同时提供两者时，以 profile_id 指定的广告账号为准；其他接口按各自的账号选择规则处理",
        examples=[90000000000003],
        # - - - - - - - - - -
        default=None,
    )
    state: Optional[NonEmptyStr] = Field(
        description='广告实体状态 ("enabled", "paused", "archived")；None 时省略请求参数，由服务端应用默认筛选',
        examples=["enabled"],
        # - - - - - - - - - -
        default=None,
    )
    next_token: Optional[NonEmptyStr] = Field(
        description="分页游标, 上次分页结果中的next_token",
        examples=["MTAwMDAwMDAwMDAwMDE="],
        # - - - - - - - - - -
        default=None,
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @model_validator(mode="after")
    def _validate_identifiers(self) -> AdEntities:
        """在字段校验完成后，要求至少一个标识不是 None。

        Returns:
            AdEntities: 当前模型实例，保留已解析的全部字段。

        Raises:
            ValueError: sid 和 profile_id 均为 None。
        """
        if self.sid is None and self.profile_id is None:
            raise ValueError("sid 和 profile_id 至少提供一个")
        return self


# . SP Negative Targets
class SpNegativeTargeting(AdEntities):
    """查询 SP 否定投放参数。

    sid 与 profile_id 至少提供一项。SpNegativeKeywords 使用 keyword，
    SpNegativeTargets 使用 target；这两个 SDK 方法不提供 state 筛选。

    Args:
        target_type (str): 否定投放类型，去除首尾空白后须非空；两个 SDK 方法分别固定为 keyword、target。
        campaign_id (int | None): 非负广告活动ID，默认 None；None 省略请求参数并查询所有活动，0 保留。

    Raises:
        pydantic.ValidationError: 未提供查询账号，或给定参数不符合非负整数、非空字符串规则。

    Examples:
        按广告账号与活动查询否定关键词。

        >>> SpNegativeTargeting(profile_id=90000000000004, target_type="keyword", campaign_id=70000000000079).model_dump_params()
        {'campaign_id': 70000000000079, 'profile_id': 90000000000004, 'target_type': 'keyword'}
    """

    target_type: NonEmptyStr = Field(
        description='否定投放类型 ("keyword", "target")',
        examples=["keyword"],
    )
    campaign_id: Optional[NonNegativeInt] = Field(
        description="广告活动ID",
        examples=[70000000000079],
        # - - - - - - - - - -
        default=None,
    )


# . SB Targets
class SbTargeting(AdEntities):
    """查询 SB 关键词或商品定位参数。

    Args:
        ad_type (str): 广告类型，SB、SBV或ALL；请求别名为ads_type。
        target_type (str): 投放类型，keyword、product或ALL；仅精确的product
            转换为producttarget，请求别名为targeting_type。
        sid (int | None): 领星店铺ID，与profile_id至少提供一项。
        profile_id (int | None): 广告账号ID。
        state (str | None): 继承的通用字段；两个SB投放查询方法不提供此筛选。
        next_token (str | None): 上页返回的游标，None省略。
        offset (int | None): 非负偏移量，None省略，0保留。
        length (int | None): 非负分页长度，None省略，0保留。

    Raises:
        pydantic.ValidationError: 标识缺失或字段不符合原有非负整数、非空字符串规则。

    字符串沿用去除首尾空白的校验，不增加枚举限制或改变已有转换顺序。
    """

    ad_type: NonEmptyStr = Field(
        description="SB广告类型 [请求字段 'ads_type']",
        examples=["SB"],
        # - - - - - - - - - -
        alias="ads_type",
    )
    target_type: NonEmptyStr = Field(
        description="SB投放类型 [请求字段 'targeting_type']",
        examples=["producttarget"],
        # - - - - - - - - - -
        alias="targeting_type",
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("target_type", mode="before")
    @classmethod
    def _validate_target_type(cls, v: object) -> object:
        """转换Python接口的商品投放名称，其他输入交给字段校验。

        Args:
            v (object): 字段校验前的原始输入，可能不是字符串。

        Returns:
            object: 精确的product字符串变为producttarget；其他值保持原样。
        """
        return "producttarget" if v == "product" else v


# 报告 -------------------------------------------------------------------------------------------------------------------------
# . Ad Reports
class AdReports(AdEntities):
    """查询广告日报参数。

    标识和分页字段沿用AdEntities，具体支持字段以所调用方法为准。
    report_date按既有日期解析器取年月日，不自动换算时区；不检查接口的查询时间范围。
    缺少日的月份字符串补为1日，越界日可能归一化，建议明确提供完整YYYY-MM-DD。

    Args:
        report_date (str | date | datetime): 报告日期，输出为YYYY-MM-DD字符串。
        show_detail (int | None): 完整归因期标记，0为否、1为是；模型默认None并省略，SP日报方法固定传0。

    Raises:
        pydantic.ValidationError: 日期无法解析，账号标识缺失或其他参数不符合已有校验规则。

    Examples:
        使用广告账号查询指定日期的默认归因范围。

        >>> AdReports(profile_id=90000000000001, report_date="2026-10-01", show_detail=0).model_dump_params()
        {'profile_id': 90000000000001, 'report_date': '2026-10-01', 'show_detail': 0}
    """

    report_date: str = Field(
        description="报告日期",
        examples=["2026-10-01"],
    )
    show_detail: Optional[NonNegativeInt] = Field(
        description="是否展示完整归因期信息 (0: 否, 1: 是；接口默认0)",
        examples=[0],
        # - - - - - - - - - -
        default=None,
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("report_date", mode="before")
    @classmethod
    def _validate_report_date(cls, v: object) -> str:
        """按既有解析规则转换报告日期。

        Args:
            v (object): 校验前的日期输入，支持日期字符串及date、datetime对象。

        Returns:
            str: 解析结果的年月日，格式为YYYY-MM-DD；不额外换算时区或检查查询时间范围。

        Raises:
            ValueError: 输入为None或既有日期解析器无法解析输入。

        Examples:
            >>> print(AdReports._validate_report_date("2026-10-01"))
            2026-10-01
        """
        dt = utils.validate_datetime(v, False, "广告报告日期")
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)


# . Ad Hour Reports
class AdHourData(Parameter):
    """查询广告小时数据参数。

    报告日期按既有日期解析器取年月日，不自动换算时区；日期范围和聚合维度由具体接口规定。
    该模型只提供单个campaign_id，不提供批量活动或分页参数。

    Args:
        report_date (str | date | datetime): 报告日期，输出为YYYY-MM-DD；建议提供完整有效日期。
        campaign_id (int): 广告活动ID，沿用非负整数校验，0不会被省略。
        agg_dimension (str | None): 聚合维度，默认None并省略；字符串去除首尾空白后须非空。

    Raises:
        pydantic.ValidationError: 日期无法解析，活动ID或聚合维度不符合已有校验规则。

    Examples:
        查询指定活动的广告及投放小时数据。

        >>> AdHourData(report_date="2026-10-01", campaign_id=70000000000001, agg_dimension="both_ad_target").model_dump_params()
        {'agg_dimension': 'both_ad_target', 'campaign_id': 70000000000001, 'report_date': '2026-10-01'}
    """

    report_date: str = Field(
        description="报告日期；允许的查询时间范围由所调用接口规定",
        examples=["2026-10-01"],
    )
    campaign_id: NonNegativeInt = Field(
        description="广告活动ID",
        examples=[70000000000204],
    )
    agg_dimension: Optional[NonEmptyStr] = Field(
        description="聚合维度",
        examples=["both_ad_target"],
        # - - - - - - - - - -
        default=None,
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("report_date", mode="before")
    @classmethod
    def _validate_report_date(cls, v: object) -> str:
        """按既有解析规则转换报告日期。

        Args:
            v (object): 校验前的日期输入，支持日期字符串及date、datetime对象。

        Returns:
            str: 解析结果的年月日，格式为YYYY-MM-DD；不额外换算时区或检查查询时间范围。

        Raises:
            ValueError: 输入为None或既有日期解析器无法解析输入。

        Examples:
            >>> print(AdHourData._validate_report_date("2026-10-01"))
            2026-10-01
        """
        dt = utils.validate_datetime(v, False, "广告报告日期")
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)


# . SP Query Reports
class SpQueryReports(AdReports):
    """查询SP用户搜索词日报参数。

    日期、标识和分页规则沿用AdReports。SDK关键词与商品投放搜索词方法分别固定target_type。

    Args:
        target_type (str): keyword表示关键词；target表示商品投放或关键词组。去除首尾空白后须非空，模型不额外限制枚举。

    Raises:
        pydantic.ValidationError: 投放类型为空或继承参数不符合已有校验规则。

    Examples:
        查询指定日期的关键词搜索词。

        >>> SpQueryReports(profile_id=90000000000001, report_date="2026-10-01", target_type="keyword").model_dump_params()
        {'profile_id': 90000000000001, 'report_date': '2026-10-01', 'target_type': 'keyword'}
    """

    target_type: NonEmptyStr = Field(
        description="投放目标类型 (keyword: 关键词；target: 商品投放或关键词组)",
        examples=["keyword"],
    )


# . SB Target Reports
class SbTargetingReports(AdReports):
    """查询SB广告投放日报参数。

    日期、账号标识与分页字段继承AdReports；具体接口支持范围以调用方法为准。

    Args:
        ad_type (str): SB广告类型；请求字段sponsored_type，官方当前支持ALL
        target_type (str): SB投放类型；精确product输入序列化为producttarget，keyword和ALL沿用既有校验

    Raises:
        pydantic.ValidationError: 自有字段或继承字段不符合既有校验规则。

    Examples:
        序列化后的请求参数：

        .. code-block:: json

            {
                "length": 2,
                "offset": 0,
                "profile_id": 9000000000000005,
                "report_date": "2026-10-01",
                "sponsored_type": "ALL",
                "target_type": "keyword"
            }
    """

    ad_type: NonEmptyStr = Field(
        description="SB广告类型；请求字段sponsored_type，官方当前支持ALL",
        examples=["ALL"],
        alias="sponsored_type",
    )
    target_type: NonEmptyStr = Field(
        description="SB投放类型；精确product输入序列化为producttarget，keyword和ALL沿用既有校验",
        examples=["keyword"],
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("target_type", mode="before")
    @classmethod
    def _validate_target_type(cls, v: object) -> object:
        """转换Python接口的商品投放名称，其他输入交给字段校验。

        Args:
            v (object): 字段校验前的原始输入，可能不是字符串。

        Returns:
            object: 精确的product字符串变为producttarget；其他值保持原样。
        """
        return "producttarget" if v == "product" else v


# . SB Query Reports
class SbQueryReports(AdReports):
    """查询SB用户搜索词日报参数。

    日期、账号标识与分页字段继承AdReports；具体接口支持范围以调用方法为准。

    Args:
        target_type (str): 搜索词投放类型；keyword表示关键词，target表示商品投放；沿用非空字符串校验，不额外限制枚举

    Raises:
        pydantic.ValidationError: 自有字段或继承字段不符合既有校验规则。

    Examples:
        序列化后的请求参数：

        .. code-block:: json

            {
                "length": 2,
                "offset": 0,
                "profile_id": 900000000000002,
                "report_date": "2026-10-01",
                "target_type": "keyword"
            }
    """

    target_type: NonEmptyStr = Field(
        description="搜索词投放类型；keyword表示关键词，target表示商品投放；沿用非空字符串校验，不额外限制枚举",
        examples=["keyword"],
    )


# . DSP Reports
class DspReports(PageOffestAndLength):
    """查询 DSP 订单日报参数。

    Args:
        start_date (str | date | datetime): 报告开始日期，包含当日，输出为YYYY-MM-DD。
        end_date (str | date | datetime): 报告结束日期，包含当日；接口要求查询间隔不超过90天。
        profile_id (int | None): DSP账户ID，来源为AdProfiles返回的profile_id；沿用非负整数校验，发送为字符串。
            与advertiser_id至少提供一项；同时提供时接口优先使用advertiser_id。
        advertiser_id (int | None): 广告主ID，默认None并省略，发送为非负整数。
        next_token (str | None): 上一页返回的Base64游标，默认None并省略；给定字符串去除首尾空白后须非空。
        offset (int | None): 从0开始的分页偏移量，默认None并省略；接口默认0，显式0保留。
        length (int | None): 分页长度，默认None并省略；接口默认20，显式0保留。

    Raises:
        pydantic.ValidationError: 日期缺失或无法解析、两个标识均为None，或给定的标识、游标和分页字段不符合校验规则。

    Examples:
        使用DSP账户ID查询，账号ID在请求字典中输出为字符串。

        >>> DspReports(start_date="2022-10-05", end_date="2022-12-01", profile_id=90000000000001).model_dump_params()
        {'end_date': '2022-12-01', 'profile_id': '90000000000001', 'start_date': '2022-10-05'}

        也可使用广告主ID，输出请求键按接口协议序列化。

        >>> DspReports(start_date="2022-10-05", end_date="2022-12-01", advertiser_id=80000000000001).model_dump_params()
        {'dsp_advertiser_id': 80000000000001, 'end_date': '2022-12-01', 'start_date': '2022-10-05'}
    """

    start_date: str = Field(
        description="报告开始日期，包含当日，输出为YYYY-MM-DD；接口要求查询间隔不超过90天",
        examples=["2022-10-05"],
    )
    end_date: str = Field(
        description="报告结束日期，包含当日，输出为YYYY-MM-DD；接口要求查询间隔不超过90天",
        examples=["2022-12-01"],
    )
    profile_id: Optional[NonNegativeInt] = Field(
        description="DSP账户ID，来源为AdProfiles.profile_id；与advertiser_id至少提供一项，输入按非负整数校验并发送为字符串；同时提供时接口优先使用advertiser_id",
        examples=[90000000000001],
        # - - - - - - - - - -
        default=None,
    )
    advertiser_id: Optional[NonNegativeInt] = Field(
        description="广告主ID；与profile_id至少提供一项，同时提供时接口优先使用此标识；None省略请求键",
        examples=[80000000000001],
        # - - - - - - - - - -
        serialization_alias="dsp_advertiser_id",
        default=None,
    )
    next_token: Optional[NonEmptyStr] = Field(
        description="上一页最后一条记录ID经Base64编码的分页游标；首次请求可省略，None省略请求键，给定字符串去除首尾空白后须非空",
        examples=["NzAwMDAwMDAwMDAwMDAx"],
        # - - - - - - - - - -
        default=None,
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @model_validator(mode="after")
    def _validate_identifiers(self) -> DspReports:
        """要求至少一个账号或广告主标识不是None。

        Returns:
            DspReports: 当前模型实例，同时保留两个已提供的标识。

        Raises:
            ValueError: profile_id和advertiser_id均为None。
        """
        if self.profile_id is None and self.advertiser_id is None:
            raise ValueError("profile_id和advertiser_id至少提供一项")
        return self

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_serializer("profile_id")
    def _serialize_profile_id(self, v: int | None) -> str | None:
        """将已验证的账号ID按接口要求输出为字符串。

        Args:
            v (int | None): 按既有非负整数规则解析后的账号ID。

        Returns:
            str | None: 账号ID字符串；未提供时返回None，由请求字典省略。
        """
        return None if v is None else str(v)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v: str | datetime.date | datetime.datetime, info: ValidationInfo) -> str:
        """按既有日期解析规则输出DSP报告日期。

        Args:
            v (str | date | datetime): 校验前的日期输入。
            info (ValidationInfo): 正在校验的日期字段，用于错误提示。

        Returns:
            str: YYYY-MM-DD日期文本；不额外校验起止顺序或90天查询间隔。

        Raises:
            ValueError: 输入为None或既有日期解析器无法解析输入。
        """
        dt = utils.validate_datetime(v, False, "DSP报告日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)


# 报表下载 ----------------------------------------------------------------------------------------------------------------------
# . Download ABA Report
class DownloadAbaReport(Parameter):
    """查询指定国家和周起始日期的 ABA 报告下载信息参数。

    Args:
        country_code (str): 两字符国家代码，如US；去除首尾空白，请求别名为country。
        start_date (str | date | datetime): 周报告起始日期，请求别名为data_start_time，输出为YYYY-MM-DD。
            以周日为每周起点，归并到输入日期当天或之前最近的周日；接口仅支持最近45天的周日，模型不额外校验该范围。

    Raises:
        pydantic.ValidationError: 必填参数缺失、国家代码不符合两字符规则，或日期无法解析。

    Examples:
        使用所选日期生成其所在周的请求参数。

        .. code-block:: python

            parameters = DownloadAbaReport(country_code="US", start_date="2026-09-18")
            print(parameters.model_dump_params())
    """

    country_code: CountryCode = Field(
        description="两字符国家代码，去除首尾空白 [请求字段 'country']",
        examples=["US"],
        # - - - - - - - - - -
        alias="country",
    )
    start_date: str = Field(
        description="周报告起始日期（周日），输出为YYYY-MM-DD；输入转换为当天或之前最近的周日，周日保持不变；接口仅支持最近45天 [请求字段 'data_start_time']",
        examples=["2026-10-04"],
        # - - - - - - - - - -
        alias="data_start_time",
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("start_date", mode="before")
    @classmethod
    def _validate_start_date(cls, v: str | datetime.date | datetime.datetime) -> str:
        """按周日为每周起点，将所选日期归并到该周周日并输出年月日。

        Args:
            v (str | date | datetime): 校验前的日期输入。

        Returns:
            str: YYYY-MM-DD日期文本；取输入日期当天或之前最近的周日，不校验最近45天范围。

        Raises:
            ValueError: 输入为None或既有日期解析器无法解析输入。
        """
        dt = utils.validate_datetime(v, False, "ABA报表开始日期")
        # cyTimes的周从周一开始；ABA的周从周日开始。
        if not dt.is_weekday("Sun"):
            dt = dt.to_prev_weekday("Sun")
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)


# 操作日志 ----------------------------------------------------------------------------------------------------------------------
# . Ads Operation Logs
class AdsOperationLogs(PageOffestAndLength):
    """查询广告操作日志参数。

    日期输出为YYYY-MM-DD，接口要求查询间隔不超过一个月；模型不额外校验起止顺序或跨度。
    广告类型转为小写，其余文本去除首尾空白；模型不额外限制广告类型、操作对象或来源的枚举。
    日志来源在本模型中必填，SDK方法默认传入all。分页查询不保证跨页完整性。

    Args:
        sid (int): 领星店铺ID，沿用非负整数校验，与响应中的广告账号profile_id不同。
        start_date (str | date | datetime): 操作日志开始日期，输出为YYYY-MM-DD。
        end_date (str | date | datetime): 操作日志结束日期，输出为YYYY-MM-DD。
        ad_type (str): 广告类型，接口支持SP、SB、SD；转为小写后使用请求别名sponsored_type。
        operation_target (str): 操作对象，使用请求别名operate_type；campaigns广告活动、adGroups广告组、productAds广告、keywords关键词、negativeKeywords否定关键词、targets商品投放、negativeTargets否定商品投放、profiles预算设置。去除首尾空白后须非空。
        log_source (str): 日志来源，all全部、erp仅ERP调整、amazon仅亚马逊后台调整；去除首尾空白后须非空。
        offset (int | None): 从0开始的偏移量，默认None并省略，显式0保留。
        length (int | None): 分页长度，默认None并省略；接口默认15，显式0保留，不额外设置长度上限。

    Raises:
        pydantic.ValidationError: 必填参数缺失、日期无法解析，或参数不符合既有类型及非空、非负校验。

    Examples:
        将日期、广告类型和请求别名序列化。

        >>> AdsOperationLogs(sid=10105, start_date="2026-10-01", end_date="2026-10-16", ad_type="SP", operation_target="campaigns", log_source="all").model_dump_params()
        {'end_date': '2026-10-16', 'log_source': 'all', 'operate_type': 'campaigns', 'sid': 10105, 'sponsored_type': 'sp', 'start_date': '2026-10-01'}
        >>> AdsOperationLogs.model_validate_params({"sid": 10105, "start_date": "2026-10-01", "end_date": "2026-10-16", "sponsored_type": "SP", "operate_type": "campaigns", "log_source": "all", "offset": 0, "length": 4})
        {'end_date': '2026-10-16', 'length': 4, 'log_source': 'all', 'offset': 0, 'operate_type': 'campaigns', 'sid': 10105, 'sponsored_type': 'sp', 'start_date': '2026-10-01'}
    """

    sid: NonNegativeInt = Field(
        description="领星店铺ID",
        examples=[10105],
    )
    start_date: str = Field(
        description="开始日期, 日期间隔不能超过1个月；输出为YYYY-MM-DD，模型不额外校验起止顺序或跨度",
        examples=["2026-10-01"],
    )
    end_date: str = Field(
        description="结束日期, 日期间隔不能超过1个月；输出为YYYY-MM-DD，模型不额外校验起止顺序或跨度",
        examples=["2026-10-16"],
    )
    ad_type: str = Field(
        description="广告类型 ('sp', 'sb', 'sd')；转为小写，模型不额外限制枚举 [请求字段 'sponsored_type']",
        examples=["SP"],
        # - - - - - - - - - -
        alias="sponsored_type",
    )
    operation_target: NonEmptyStr = Field(
        description="操作对象；campaigns广告活动、adGroups广告组、productAds广告、keywords关键词、negativeKeywords否定关键词、targets商品投放、negativeTargets否定商品投放、profiles预算设置；去除首尾空白后须非空，模型不额外限制枚举 [请求字段 'operate_type']",
        examples=["campaigns"],
        # - - - - - - - - - -
        alias="operate_type",
    )
    log_source: NonEmptyStr = Field(
        description="日志来源；all全部、erp仅ERP调整、amazon仅亚马逊后台调整；模型中必填，SDK方法默认all；去除首尾空白后须非空，模型不额外限制枚举",
        examples=["all"],
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v: str, info: ValidationInfo) -> str:
        """按既有日期解析规则输出操作日志日期。

        Args:
            v (str | date | datetime): 校验前的日期输入。
            info (ValidationInfo): 正在校验的日期字段信息，用于错误提示。

        Returns:
            str: 解析结果的年月日，格式为YYYY-MM-DD；不换算时区或校验查询间隔。

        Raises:
            ValueError: 输入为None或既有日期解析器无法解析输入。

        Examples:
            >>> AdsOperationLogs(sid=10105, start_date="2026-10-01 12:30:00", end_date="2026-10-16", ad_type="SP", operation_target="campaigns", log_source="all").start_date
            '2026-10-01'
        """
        dt = utils.validate_datetime(v, False, "广告操作日志日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)

    @field_validator("ad_type", mode="before")
    @classmethod
    def _validate_ad_type(cls, v) -> str:
        """将字符串广告类型转为小写。

        Args:
            v (object): 校验前的广告类型输入。

        Returns:
            str: 输入字符串的小写形式；不额外限制枚举。

        Raises:
            ValueError: 输入不是字符串。

        Examples:
            >>> AdsOperationLogs._validate_ad_type("SP")
            'sp'
        """
        if not isinstance(v, str):
            raise ValueError("广告类型必须是字符串")
        return v.lower()
