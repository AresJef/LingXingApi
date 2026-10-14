# -*- coding: utf-8 -*-
from __future__ import annotations

from pydantic import Field, field_validator
from lingxingapi import utils
from lingxingapi.base.param import Parameter
from lingxingapi.fields import (
    NonEmptyStr,
    CountryCode as CountryCodeField,
    CurrencyCode,
    NonNegativeInt,
)


# . Country Code ----------------------------------------------------------------------------------------------------------------
class CountryCode(Parameter):
    """国家代码参数；去除首尾空白后保留原大小写，要求恰好两个字符。"""

    country_code: CountryCodeField = Field(
        description='国家代码, 如: "US", "CA"',
        examples=["US"],
    )


# . Rename Sellers --------------------------------------------------------------------------------------------------------------
class RenameSeller(Parameter):
    """单店改名参数；SID 允许为零，名称去除首尾空白后必须非空。"""

    sid: NonNegativeInt = Field(
        description="领星店铺ID (Seller.sid)",
        examples=[1],
    )
    name: NonEmptyStr = Field(
        description="新的店铺名称",
        examples=["sample-1"],
    )


class RenameSellers(Parameter):
    """将单项或非空 list/tuple 的改名参数归一化为原生字典列表。"""

    renames: list = Field(
        description="修改店铺名称参数列表",
        examples=[[{"name": "sample-1", "sid": 1}]],
        # - - - - - - - - - -
        alias="sid_name_list",
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("renames", mode="before")
    @classmethod
    def _validate_renames(
        cls: type[RenameSellers], v: object
    ) -> list[dict[str, int | str]]:
        """逐项校验改名参数，保持输入顺序并生成请求字典。

        Args:
            v: 单项参数，或由单项参数组成的非空 list/tuple；单项可为字典
                或 RenameSeller 模型。

        Returns:
            list[dict[str, int | str]]: 经 RenameSeller 校验、按请求字段输出的
                字典列表；不增加批量数量上限。

        Raises:
            ValueError: list/tuple 为空。
            pydantic.ValidationError: 任一单项无法通过 RenameSeller 校验。
        """
        if isinstance(v, (list, tuple)):
            if len(v) <= 0:
                raise ValueError("必须提供至少一个 rename 来修改店铺名称")
            res = [RenameSeller.model_validate_params(i) for i in v]
        else:
            res = [RenameSeller.model_validate_params(v)]
        return res


# . Excahnge Rate ---------------------------------------------------------------------------------------------------------------
class ExchangeRate(Parameter):
    """汇率查询参数；按现有解析器提取年月，当前不支持 None。"""

    date: str = Field(
        description='日期, 格式为 "YYYY-MM"',
        examples=["2026-09"],
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("date", mode="before")
    @classmethod
    def _validate_date(cls: type[ExchangeRate], v: object) -> str:
        """沿用日期解析器的默认规则，将日期格式化为年月。

        Args:
            v: 交给 utils.validate_datetime 的原始日期，常见为字符串或
                date/datetime 对象；None 也交由解析器处理，当前会失败。

        Returns:
            str: 格式为 YYYY-MM 的年月字符串。

        Raises:
            ValueError: 原始日期无法解析。
        """
        dt = utils.validate_datetime(v, True, "汇率日期 date")
        return "%04d-%02d" % (dt.year, dt.month)


# . Edit Exchange Rate ----------------------------------------------------------------------------------------------------------
class EditExchangeRate(Parameter):
    """汇率修改参数；日期取年月，汇率按当前 Decimal context 量化后转为字符串。"""

    date: str = Field(
        description='汇率日期, 格式为 "YYYY-MM"',
        examples=["2016-12"],
    )
    currency_code: CurrencyCode = Field(
        description='货币代码, 如 "CNY", "USD", "EUR"',
        examples=["VND"],
        # - - - - - - - - - -
        alias="code",
    )
    user_rate: str = Field(
        description="用户自定义汇率 (对比人民币, 如: 7.2008000000), 最多支持10位小数",
        examples=["0.0003000000"],
        # - - - - - - - - - -
        alias="my_rate",
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("date", mode="before")
    @classmethod
    def _validate_date(cls: type[EditExchangeRate], v: object) -> str:
        """拒绝 None，沿用日期解析器默认规则提取年月。

        Args:
            v: 原始日期，常见为字符串或 date/datetime 对象。

        Returns:
            str: 格式为 YYYY-MM 的年月字符串。

        Raises:
            ValueError: 日期为 None 或无法解析。
        """
        dt = utils.validate_datetime(v, False, "汇率日期 date")
        return "%04d-%02d" % (dt.year, dt.month)

    @field_validator("user_rate", mode="before")
    @classmethod
    def _validate_user_rate(cls: type[EditExchangeRate], v: object) -> str:
        """校验原始汇率，按当前 Decimal context 量化并保留其字符串表示。

        Args:
            v: 原始汇率，常见为 str、int、float 或 Decimal。

        Returns:
            str: 十位小数量化结果的字符串，沿用 Decimal 的指数表示；极小
                正数可能量化为零，关闭异常 trap 时也可能得到特殊值。

        Raises:
            ValueError: 原始汇率无法转换、非有限或小于等于零。
            decimal.DecimalException: 量化触发的 context 异常，原样传播。
        """
        return str(utils.validate_exchange_rate(v, "用户自定义汇率 user_rate"))
