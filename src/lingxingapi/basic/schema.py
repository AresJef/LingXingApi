# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field, field_validator
from lingxingapi.fields import IntOrNone2Zero
from lingxingapi.base.schema import ResponseV1, ResponseResult


# 基础数据 -----------------------------------------------------------------------------------------------------------------------
# . Marketplaces
class Marketplace(BaseModel):
    """亚马逊站点."""

    mid: int = Field(
        description="领星站点ID [唯一标识]",
        examples=[1],
    )
    region: str = Field(
        description="站点区域",
        examples=["NA"],
    )
    region_aws: str = Field(
        description="站点亚马逊仓库所属区域 [原字段 'aws_region']",
        examples=["NA"],
        # - - - - - - - - - -
        validation_alias="aws_region",
    )
    country: str = Field(
        description="站点国家 (中文)",
        examples=["美国"],
    )
    country_code: str = Field(
        description="站点国家代码 [原字段 'code']",
        examples=["US"],
        # - - - - - - - - - -
        validation_alias="code",
    )
    marketplace_id: str = Field(
        description="亚马逊市场ID",
        examples=["ATVPDKIKX0DER"],
    )

class Marketplaces(ResponseV1):
    """亚马逊站点查询结果."""

    data: list[Marketplace]


# . States
class State(BaseModel):
    """国家的省/州."""

    country_code: str = Field(
        description="国家代码",
        examples=["US"],
    )
    state: str = Field(
        description="省/州名称 [原字段 'state_or_province_name']",
        examples=["AL-Alabama"],
        # - - - - - - - - - -
        validation_alias="state_or_province_name",
    )
    state_code: str = Field(
        description="省/州代码 [原字段 'code']",
        examples=["AL"],
        # - - - - - - - - - -
        validation_alias="code",
    )


class States(ResponseV1):
    """国家的省/州查询结果."""

    data: list[State]


# . Sellers
class Seller(BaseModel):
    """领星店铺."""

    mid: int = Field(
        description="领星站点ID (Marketplace.mid)",
        examples=[4],
    )
    sid: int = Field(
        description="领星店铺ID [唯一标识]",
        examples=[10000],
    )
    seller_id: str = Field(
        description="亚马逊卖家ID",
        examples=["AW900000000QD"],
    )
    seller_name: str = Field(
        description="领星店铺名称 (含国家信息) [原字段 'name']",
        examples=["名称店铺"],
        # - - - - - - - - - -
        validation_alias="name",
    )
    account_id: int = Field(
        description="领星店铺帐号ID [原字段 'seller_account_id']",
        examples=[1000],
        # - - - - - - - - - -
        validation_alias="seller_account_id",
    )
    account_name: str = Field(
        description="领星店铺帐号名称",
        examples=["店铺账号名称"],
    )
    marketplace_id: str = Field(
        description="亚马逊市场ID (Marketplace.marketplace_id)",
        examples=["A1F83G8C2ARO7P"],
    )
    region: str = Field(
        description="店铺区域",
        examples=["EU"],
    )
    country: str = Field(
        description="店铺国家 (中文)",
        examples=["英国"],
    )
    status: int = Field(
        description="店铺状态 (0: 停止同步, 1: 正常, 2: 授权异常, 3: 欠费停服)",
        examples=[2],
    )
    ads_authorized: int = Field(
        description="店铺是否授权广告 (0: 否, 1: 是) [原字段 'has_ads_setting']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="has_ads_setting",
    )


class Sellers(ResponseV1):
    """领星店铺查询结果."""

    data: list[Seller]


# . Concept Sellers
class ConceptSeller(BaseModel):
    """领星概念店铺."""

    cmid: int = Field(
        description="领星概念站点ID [原字段 'mid']",
        examples=[1000000],
        # - - - - - - - - - -
        validation_alias="mid",
    )
    csid: int = Field(
        description="领星概念店铺ID [唯一标识, 原字段 'id']",
        examples=[100000000000000000],
        # - - - - - - - - - -
        validation_alias="id",
    )
    seller_id: str = Field(
        description="亚马逊卖家ID",
        examples=["A20000000000T"],
    )
    seller_name: str = Field(
        description="领星概念店铺名称 (含区域信息) [原字段 'name']",
        examples=["概念店铺名称"],
        # - - - - - - - - - -
        validation_alias="name",
    )
    account_id: int = Field(
        description="领星概念店铺账号ID [原字段 'seller_account_id']",
        examples=[1000],
        # - - - - - - - - - -
        validation_alias="seller_account_id",
    )
    account_name: str = Field(
        description="领星概念店铺帐号名称 [原字段 'seller_account_name']",
        examples=["概念店铺账号"],
        # - - - - - - - - - -
        validation_alias="seller_account_name",
    )
    region: str = Field(
        description="概念店铺区域",
        examples=["NA"],
    )
    country: str = Field(
        description="概念店铺国家, 如: \"北美共享\", \"欧洲共享\"",
        examples=["北美共享"],
    )
    status: int = Field(
        description="概念店铺状态 (1: 启用, 2: 停用)",
        examples=[1],
    )


class ConceptSellers(ResponseV1):
    """领星概念店铺查询结果."""

    data: list[ConceptSeller]


# . Rename Sellers
class RenameSellersFailureDetail(BaseModel):
    """批量修改店铺名称失败的详情."""

    sid: int = Field(
        description="领星店铺ID (Seller.sid)",
        examples=[0],
    )
    name: str = Field(
        description="新店铺名称",
        examples=["TEST"],
    )
    message: str = Field(
        description="失败信息 [原字段 'error']",
        examples=["店铺记录不存在"],
        # - - - - - - - - - -
        validation_alias="error",
    )


class RenameSellers(BaseModel):
    """批量修改店铺名称的结果."""

    success: IntOrNone2Zero = Field(
        description="修改成功数量 [原字段 'success_num']",
        examples=[1],
        # - - - - - - - - - -
        validation_alias="success_num",
    )
    failure: IntOrNone2Zero = Field(
        description="修改失败数量 [原字段 'failure_num']",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="failure_num",
    )
    failure_detail: list[RenameSellersFailureDetail] = Field(
        description="修改失败详情",
        examples=[[]],
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("failure_detail", mode="before")
    def _validate_failure_detail(cls, v):
        if v is None:
            return []
        return [RenameSellersFailureDetail.model_validate(i) for i in v]


class RenameSellersResult(ResponseResult):
    """批量修改店铺名称的响应结果."""

    data: RenameSellers


# . Accounts
class Account(BaseModel):
    """领星账号."""

    parent_id: int = Field(
        description="领星账号所从属的ID (如主帐号ID) [原字段 'zid']",
        examples=[10000000],
        # - - - - - - - - - -
        validation_alias="zid",
    )
    user_id: int = Field(
        description="领星帐号ID [唯一标识] [原字段 'uid']",
        examples=[10000000],
        # - - - - - - - - - -
        validation_alias="uid",
    )
    is_master: int = Field(
        description="是否为主账号 (0: 否, 1: 是)",
        examples=[1],
    )
    role: str = Field(
        description="帐号角色",
        examples=[""],
    )
    display_name: str = Field(
        description="领星帐号显示的姓名 [原字段 'realname']",
        examples=["用户名称"],
        # - - - - - - - - - -
        validation_alias="realname",
    )
    username: str = Field(
        description="领星帐号登陆用户名",
        examples=["sample_user"],
    )
    email: str = Field(
        description="领星帐号电子邮箱",
        examples=["user@example.invalid"],
    )
    phone: str = Field(
        description="领星帐号电话号码 [原字段 'mobile']",
        examples=["13800000000"],
        # - - - - - - - - - -
        validation_alias="mobile",
    )
    create_time: str = Field(
        description="领星帐号创建时间 (北京时间)",
        examples=["2001-05-07 05:14"],
    )
    last_login_time: str = Field(
        description="领星帐号最后登录时间 (北京时间)",
        examples=["-"],
    )
    last_login_ip: str = Field(
        description="领星帐号最后登录IP",
        examples=[""],
    )
    login_count: int = Field(
        description="领星帐号登录次数 [原字段 'login_num']",
        examples=[0],
        # - - - - - - - - - -
        validation_alias="login_num",
    )
    status: int = Field(
        description="领星帐号状态 (0: 禁用, 1: 正常)",
        examples=[1],
    )
    sellers: str = Field(
        description="关联的领星店铺名称, 逗号分隔 [原字段 'seller']",
        examples=["示例店铺1,示例店铺2,示例店铺3"],
        # - - - - - - - - - -
        validation_alias="seller",
    )


class Accounts(ResponseV1):
    """领星账号查询结果."""

    data: list[Account]


# . Exchange Rates
class ExchangeRate(BaseModel):
    """货币汇率."""

    date: str = Field(
        description="汇率日期 (格式: YYYY-MM-DD)",
        examples=["2026-09-01"],
    )
    currency: str = Field(
        description="货币名称 (中文) [原字段 'name']",
        examples=["人民币"],
        # - - - - - - - - - -
        validation_alias="name",
    )
    currency_code: str = Field(
        description="货币代码 [原字段 'code']",
        examples=["CNY"],
        # - - - - - - - - - -
        validation_alias="code",
    )
    currency_icon: str = Field(
        description="货币符号 [原字段 'icon']",
        examples=["￥"],
        # - - - - - - - - - -
        validation_alias="icon",
    )
    boc_rate: float = Field(
        description="中国银行官方汇率 (对比人民币, 如: 7.1541) [原字段 'rate_org']",
        examples=[1.0],
        # - - - - - - - - - -
        validation_alias="rate_org",
    )
    user_rate: float = Field(
        description="用户汇率 (对比人民币, 如: 7.2008000000) [原字段 'my_rate']",
        examples=[7.0],
        # - - - - - - - - - -
        validation_alias="my_rate",
    )
    update_time: str = Field(
        description="用户汇率修改时间 (北京时间)",
        examples=[""],
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("date", mode="after")
    @classmethod
    def _validate_date(cls, v: str) -> str:
        return v + "-01"


class ExchangeRates(ResponseV1):
    """货币汇率查询结果."""

    data: list[ExchangeRate]
