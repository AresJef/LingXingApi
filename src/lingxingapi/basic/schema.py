# -*- coding: utf-8 -*-
from __future__ import annotations

from cytimes import parse as _parse
from pydantic import BaseModel, Field, field_validator
from lingxingapi import utils
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
        examples=['NA'],
    )
    region_aws: str = Field(
        description="站点亚马逊仓库所属区域 [原字段 'aws_region']",
        examples=['NA'],
        # - - - - - - - - - -
        validation_alias="aws_region",
    )
    country: str = Field(
        description="站点国家 (中文)",
        examples=['美国'],
    )
    country_code: str = Field(
        description="站点国家代码 [原字段 'code']",
        examples=['US'],
        # - - - - - - - - - -
        validation_alias="code",
    )
    marketplace_id: str = Field(
        description="亚马逊市场ID",
        examples=['ATVPDKIKX0DER'],
    )

class Marketplaces(ResponseV1):
    """亚马逊站点查询结果."""

    data: list[Marketplace]


# . States
class State(BaseModel):
    """国家的省/州."""

    country_code: str = Field(
        description="国家代码",
        examples=['US'],
    )
    state: str = Field(
        description="省/州名称 [原字段 'state_or_province_name']",
        examples=['AL-Alabama'],
        # - - - - - - - - - -
        validation_alias="state_or_province_name",
    )
    state_code: str = Field(
        description="省/州代码 [原字段 'code']",
        examples=['AL'],
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
        examples=[10041],
    )
    seller_id: str = Field(
        description="亚马逊卖家ID",
        examples=['AA0AAAA00A0CN'],
    )
    seller_name: str = Field(
        description="领星店铺名称 (含国家信息) [原字段 'name']",
        examples=['000-名称店-IH'],
        # - - - - - - - - - -
        validation_alias="name",
    )
    account_id: int = Field(
        description="领星店铺帐号ID [原字段 'seller_account_id']",
        examples=[3035],
        # - - - - - - - - - -
        validation_alias="seller_account_id",
    )
    account_name: str = Field(
        description="领星店铺帐号名称",
        examples=['000-BU'],
    )
    marketplace_id: str = Field(
        description="亚马逊市场ID (Marketplace.marketplace_id)",
        examples=['A1F83G8C2ARO7P'],
    )
    region: str = Field(
        description="店铺区域",
        examples=['EU'],
    )
    country: str = Field(
        description="店铺国家 (中文)",
        examples=['英国'],
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
        examples=[200000000000000001],
        # - - - - - - - - - -
        validation_alias="id",
    )
    seller_id: str = Field(
        description="亚马逊卖家ID",
        examples=['A00A0AA0000AAT'],
    )
    seller_name: str = Field(
        description="领星概念店铺名称 (含区域信息) [原字段 'name']",
        examples=['000-AA-DE'],
        # - - - - - - - - - -
        validation_alias="name",
    )
    account_id: int = Field(
        description="领星概念店铺账号ID [原字段 'seller_account_id']",
        examples=[3001],
        # - - - - - - - - - -
        validation_alias="seller_account_id",
    )
    account_name: str = Field(
        description="领星概念店铺帐号名称 [原字段 'seller_account_name']",
        examples=['000-AO'],
        # - - - - - - - - - -
        validation_alias="seller_account_name",
    )
    region: str = Field(
        description="概念店铺区域",
        examples=['NA'],
    )
    country: str = Field(
        description="概念店铺国家, 如: \"北美共享\", \"欧洲共享\"",
        examples=['北美共享'],
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
        examples=['TEST'],
    )
    message: str = Field(
        description="失败信息 [原字段 'error']",
        examples=['店铺记录不存在'],
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
        examples=[[{'sid': 0, 'name': 'TEST', 'message': '店铺记录不存在'}]],
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("failure_detail", mode="before")
    def _validate_failure_detail(cls, v: object) -> list[RenameSellersFailureDetail]:
        """将原始失败详情逐项解析为模型列表。

        Args:
            v: 未经字段校验的原始值；None 转为空列表，其余值按迭代协议处理。

        Returns:
            list[RenameSellersFailureDetail]: 保持原迭代顺序的失败详情列表；
                空可迭代值返回空列表。

        Raises:
            TypeError: 原始值不支持迭代。
            pydantic.ValidationError: 任一元素无法解析为失败详情模型。
        """
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
        examples=[50000001],
        # - - - - - - - - - -
        validation_alias="zid",
    )
    user_id: int = Field(
        description="领星帐号ID [唯一标识] [原字段 'uid']",
        examples=[40000001],
        # - - - - - - - - - -
        validation_alias="uid",
    )
    is_master: int = Field(
        description="是否为主账号 (0: 否, 1: 是)",
        examples=[1],
    )
    role: str = Field(
        description="帐号角色",
        examples=['运营'],
    )
    display_name: str = Field(
        description="领星帐号显示的姓名 [原字段 'realname']",
        examples=['用户名店告'],
        # - - - - - - - - - -
        validation_alias="realname",
    )
    username: str = Field(
        description="领星帐号登陆用户名",
        examples=['a.0000AAaaaa1F'],
    )
    email: str = Field(
        description="领星帐号电子邮箱",
        examples=['aaaaaad@xxxxxxxx.test'],
    )
    phone: str = Field(
        description="领星帐号电话号码 [原字段 'mobile']",
        examples=['00000000002'],
        # - - - - - - - - - -
        validation_alias="mobile",
    )
    create_time: str = Field(
        description="领星帐号创建时间 (北京时间)",
        examples=['2001-05-07 05:15'],
    )
    last_login_time: str = Field(
        description="领星帐号最后登录时间 (北京时间)",
        examples=['-'],
    )
    last_login_ip: str = Field(
        description="领星帐号最后登录IP",
        examples=[''],
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
        examples=['000-AA-GQ,aaaa-288,000-AA-GO,000-名称-店铺名-称店铺-JE,000-AA-色丁,000-AA-GK,000-AA-IF,000-AA-AA-BV,Aaaa角己,000-AA名称-店铺名、称店铺-KG,000-名称-IK,000-名称-JC,Aaaaaaaaaaaa-LB,000-名称店-铺名称-KF,000-AA-广店,000-名称店铺名-称店铺-KE,000-AA-EP,000-AA-EK,000-AA-EG,000-AA-EJ,000-AA-EH,000-AA-EL,000-AA-EN,000-AA-EO,000-AA-EM,000-AA-EF,000-AA-HR,000-AA-BE,000-AA-BB,000-AA名称-店铺名-JD,000-名称店铺名-称店铺-KC,000-AP,000-AH,000-AC,000-AF,000-AD,000-AL,000-AN,000-名称店-铺名称-KD,000-AO,000-AA-EV,000-AM,000-AA-EU,000-AB,000-AA-EY,000-AA-CL,000-AA-EX,000-AA-CJ,000-AA-GI,000-BQ,名称店铺-00000000000000-LH,000-BL,000-AA-GN,000-BG,000-AA-GL,000-BJ,000-BH,000-BM,000-BO,000-BP,000-BN,000-BF,000-AA-CZ,000-AA-CX,000-AA-DD,000-AA-DB,000-AA-DH,000-CH,000-BY,000-BS,000-BW,000-BT,000-CD,000-CF,000-CG,000-CE,000-BR,000-AA-CW,000-AA-CR,000-AA-CN,000-AA-CQ,000-AA-CO,000-AA-CS,000-AA-CU,000-AA-CV,aaaaa-aaa-aalf,000-AA-CT,000-AA-CM,Aaaaaaaaa 角辛,000-AA-GH,000-AA-GF,000-AA-BA,000-AA-AV,000-AA-AR,000-AA-AU,000-AA-AS,000-AA-AW,000-AA-AY,000-AA-AZ,000-AA-AX,000-AA-AQ,000-DS,000-DO,000-DJ,000-DM,000-DK,000-DP,000-DR,000-DQ,000-DI,000-HP,AaaaaAks,000-HI,Aaaaaaaaa 角庚,000-HD,000-HG,000-HE,000-HL,000-HN,000-HO,000-HM,000-HC,000-AA-HS,000-AA-FG,000-BZ,000-AA-FE,000-AA-名称-IM,000-AA-JB,000-AA-IY,000-AA-IZ,aaaaaaaaale,aaaaa-aaa-lg,000-AA-EE,000-AA-EA,000-AA-DV,Aaaaaaa角戊,000-AA-DY,000-AA-DW,000-AA-EB,000-AA-ED,000-AA-EC,000-AA-DU,000-AA-GE,000-AA-GC,000-AA-GB,aaaa-289,000-AA-FY,000-AA-FZ,000-BK,AaaaaAaaaaaa-la,000-AA-FD,000-AA-FC,000-AA-DZ,000-DN,000-名称店-IH,000-AG,000-AA-AA-名色角,000-HH,000-BX,000-AA-FK,000-GW,000-AA-FH,000-JX,000-AA-FI,000-JT,000-JV,000-JU,000-JY,000-KA,000-JZ,000-JS,000-JW,000-JM,000-JG,000-JK,000-JH,000-JN,000-JP,000-JO,000-AA-FS,000-JF,000-AA-FO,000-AA名称店-铺名称 店铺名-JR,000-JL,000-AA-FP,000-AA-FB,000-AA-EZ,000-AA-FX,000-AA-FV,000-IS,000-AA-DF,000-AA-HJ,000-AA-CB,000-AA-ES,000-AA-EQ,Aaaaaa-aaaaa-akz,000-名称-店铺名-IL,000-HB,000-GX,000-GS,000-GV,000-AA-名称店-DT,000-GT,000-名称-II,000-GY,000-HA,000-GZ,000-GR,000-IX,000-IT,000-IO,000-IR,000-AA-IC,000-IP,000-AA-FN,000-AA-HY,000-IU,000-AA-AK,000-AA-HU,000-IW,000-AA-AI,000-AA-HX,000-IV,000-AA-HV,000-IN,000-AA-HZ,000-AA-IB,000-AA-IA,000-AA-HT,000-Aaaaaci,000-示店店,000-AA名称店-铺名称，店铺名-IE,000-名称-IJ,000-AA名称店-KR,000-AA名称店-KN,000-AA名称店-KJ,000-AA名称店-KL,000-AA名称店-KK,000-AA名称店-KO,000-AA名称店-KQ,000-AA名称店-KP,000-AA名称店-KI,000-AA名称店-KM,000-AA-FL,Aaaaaa-aaaaa-aaky,000-AA-CA,AAAAAKX,000-AA-FU,000-AA-FT'],
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
        examples=['2026-09-01'],
    )
    currency: str = Field(
        description="货币名称 (中文) [原字段 'name']",
        examples=['人民币'],
        # - - - - - - - - - -
        validation_alias="name",
    )
    currency_code: str = Field(
        description="货币代码 [原字段 'code']",
        examples=['CNY'],
        # - - - - - - - - - -
        validation_alias="code",
    )
    currency_icon: str = Field(
        description="货币符号 [原字段 'icon']",
        examples=['￥'],
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
        examples=[1.0000000013],
        # - - - - - - - - - -
        validation_alias="my_rate",
    )
    update_time: str = Field(
        description="用户汇率修改时间 (北京时间)",
        examples=['2001-05-07 05:55:00'],
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("date", mode="after")
    @classmethod
    def _validate_date(cls, v: str) -> str:
        """解析汇率日期并输出 YYYY-MM-DD 字符串。

        缺省分量使用 DEFAULT_DATE（1970-01-01）；月份输入补1日，完整日期
        保留实际日。沿用cytimes的宽松解析，不另加严格日历校验。

        Args:
            v: 已通过字段字符串校验的日期文本。

        Returns:
            str: 解析结果格式化得到的日期，仍为字符串。

        Raises:
            ValueError: 解析失败；模型校验时由Pydantic转换为ValidationError。
        """
        return _parse(v, default=utils.DEFAULT_DATE).strftime("%Y-%m-%d")


class ExchangeRates(ResponseV1):
    """货币汇率查询结果."""

    data: list[ExchangeRate]
