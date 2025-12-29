# -*- coding: utf-8 -*-c
import datetime
from typing import Literal
from lingxingapi import errors
from lingxingapi.base.api import BaseAPI
from lingxingapi.ads import param, route, schema

# Type Aliases ---------------------------------------------------------------------------------------------------------
AD_PROFILE_TYPE = Literal["dsp", "seller", "vendor"]
AD_STATE = Literal["enabled", "paused", "archived"]
AD_TYPE = Literal["SP", "SB", "SD"]
AD_SB_TYPE = Literal["SB", "SBV", "ALL"]
AD_OPERATION_TARGET = Literal[
    "campaigns",
    "adGroups",
    "productAds",
    "keywords",
    "negativeKeywords",
    "targets",
    "negativeTargets",
    "profiles",
]
LOG_SOURCE = Literal["amazon", "erp", "all"]


# API ------------------------------------------------------------------------------------------------------------------
class AdsAPI(BaseAPI):
    """领星API `广告数据` 接口

    ## Notice
    请勿直接实例化此类
    """

    # 公共 API --------------------------------------------------------------------------------------
    # 基础数据 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    async def AdProfiles(
        self,
        profile_type: AD_PROFILE_TYPE = "seller",
        *,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.AdProfiles:
        """查询广告账号

        ## Docs
        - 新广告 - 基础数据: [查询广告账号列表](https://apidoc.lingxing.com/#/docs/newAd/baseData/dspAccountList)

        :param account_type `<'str'>`: 广告账号类型, 默认 `"seller"`, 可选值:

            - `"dsp"` (DSP账号)
            - `"seller"` (卖家账号)
            - `"vendor"` (供应商账号)

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 20)
        :returns `<'AdProfiles'>`: 返回查询到的广告帐号结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 领星店铺ID
                    "sid": 1,
                    # 领星店铺名称 [原字段 'name']
                    "seller_name": "UK-Store",
                    # 店铺国家代码
                    "country_code": "UK",
                    # 店铺货币代码
                    "currency_code": "GBP",
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 439*************
                    # 广告帐号类型 [原字段 'type']
                    "profile_type": "seller",
                    # 广告帐号状态 [原字段 'status']
                    # (-1: 删除, 0: 停用, 1: 正常, 2: 异常)
                    "profile_status": 1,
                },
                ...
            ],
        }
        ```
        """
        url = route.AD_PROFILES
        # 解析并验证参数
        args = {
            "profile_type": profile_type,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdProfiles.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.AdProfiles.model_validate(data)

    async def Portfolios(
        self,
        sid: int,
        profile_id: int,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.Portfolios:
        """查询广告组合

        ## Docs
        - 新广告 - 基础数据: [广告组合](https://apidoc.lingxing.com/#/docs/newAd/baseData/portfolios)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param state `<'str/None'>`: 广告状态, 默认 `None` (查询所有状态), 可选值:

            - `"enabled"` (启用)
            - `"paused"` (暂停)
            - `"archived"` (归档)

        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'Portfolios'>`: 返回查询到的广告组合结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告组合ID
                    "portfolio_id": 180************,
                    # 广告组合名称
                    "portfolio_name": "Zero",
                    # 广告预算 (JSON 字符串)
                    "budget": '{"policy": "noCap", "currencyCode": "USD"}'
                    # 当前是否在预算范围内 (0: 超出预算, 1: 在预算内)
                    "in_budget": 0,
                    # 广告状态
                    "state": "enabled",
                    # 服务状态 [原字段 'serving_status']
                    "status": "PORTFOLIO_OUT_OF_BUDGET",
                    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                    "create_time_ts": 1739410536715,
                    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                    "update_time_ts": 1745401171459,
                },
                ...
            ],
            # 分页游标
            "next_token": "Mjc5MDM3NjkxNDM4ODU4",
        }
        ```
        """
        url = route.PORTFOLIOS
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "state": state,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdEntities.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.Portfolios.model_validate(data)

    # . 基础数据 - Sponsored Products
    async def SpCampaigns(
        self,
        sid: int,
        profile_id: int,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpCampaigns:
        """查询 SP 广告活动

        ## Docs
        - 新广告 - 基础数据: [SP广告活动](https://apidoc.lingxing.com/#/docs/newAd/baseData/spCampaigns)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param state `<'str/None'>`: 广告状态, 默认 `None` (查询所有状态), 可选值:

            - `"enabled"` (启用)
            - `"paused"` (暂停)
            - `"archived"` (归档)

        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SpCampaigns'>`: 返回查询到的 SP 广告活动结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告组合ID
                    "portfolio_id": 0,
                    # 广告活动ID
                    "campaign_id": 467************,
                    # 广告活动名称 [原字段 'name']
                    "campaign_name": "I13FHH",
                    # 广告活动类型
                    "campaign_type": "sponsoredProducts",
                    # 投放类型
                    "targeting_type": "manual",
                    # 溢价报价调整 (0: 不调整, 1: 调整)
                    "premium_bid_adjustment": 1,
                    # 每日预算
                    "daily_budget": 80.0,
                    # 竞价策略 (JSON 字符串)
                    "bidding": '{"strategy": "manual", "adjustments": [{"predicate": "placementRestOfSearch", "percentage": 50}]}',
                    # 开始时间 [原字段 'start_date']
                    "start_time": "2025-01-17 00:00:00",
                    # 结束时间 [原字段 'end_date']
                    "end_time": "",
                    # 广告状态
                    "state": "enabled",
                    # 服务状态 [原字段 'serving_status']
                    "status": "CAMPAIGN_STATUS_ENABLED",
                    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                    "create_time_ts": 1737172532791,
                    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                    "update_time_ts": 1755674682189,
                },
                ...
            ],
            # 分页游标
            "next_token": "MTczMjQxNDQ=",
        }
        ```
        """
        url = route.SP_CAMPAIGNS
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "state": state,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdEntities.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SpCampaigns.model_validate(data)

    async def SpAdGroups(
        self,
        sid: int,
        profile_id: int,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpAdGroups:
        """查询 SP 广告组

        ## Docs
        - 新广告 - 基础数据: [SP广告组](https://apidoc.lingxing.com/#/docs/newAd/baseData/spAdGroups)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param state `<'str/None'>`: 广告状态, 默认 `None` (查询所有状态), 可选值:

            - `"enabled"` (启用)
            - `"paused"` (暂停)
            - `"archived"` (归档)

        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SpAdGroups'>`: 返回查询到的 SP 广告组结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 458************,
                    # 广告组ID
                    "ad_group_id": 287************,
                    # 广告组名称 [原字段 'name']
                    "ad_group_name": "广告组 - 2/3/2025 23:57:34.612",
                    # 默认竞价
                    "default_bid": 1.0,
                    # 广告状态
                    "state": "enabled",
                    # 服务状态 [原字段 'serving_status']
                    "status": "CAMPAIGN_PAUSED",
                    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                    "create_time_ts": 1738598311353,
                    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                    "update_time_ts": 1738598311403,
                },
                ...
            ],
            # 分页游标
            "next_token": "Mjg3ODAwODc1NDAxOTkw",
        }
        ```
        """
        url = route.SP_AD_GROUPS
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "state": state,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdEntities.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SpAdGroups.model_validate(data)

    async def SpProducts(
        self,
        sid: int,
        profile_id: int,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpProducts:
        """查询 SP 商品投放

        ## Docs
        - 新广告 - 基础数据: [SP广告商品](https://apidoc.lingxing.com/#/docs/newAd/baseData/spProductAds)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param state `<'str/None'>`: 广告状态, 默认 `None` (查询所有状态), 可选值:

            - `"enabled"` (启用)
            - `"paused"` (暂停)
            - `"archived"` (归档)

        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SpProducts'>`: 返回查询到的 SP 商品投放结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 431************,
                    # 广告组ID
                    "ad_group_id": 364************,
                    # 商品广告ID
                    "ad_id": 560************,
                    # 商品ASIN
                    "asin": "B0D*******",
                    # 亚马逊SKU [原字段 'sku']
                    "msku": "SKU********",
                    # 广告状态
                    "state": "enabled",
                    # 服务状态 [原字段 'serving_status']
                    "status": "PORTFOLIO_OUT_OF_BUDGET",
                    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                    "create_time_ts": 1743694871939,
                    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                    "update_time_ts": 1743694872065,
                },
                ...
            ],
            # 分页游标
            "next_token": "Mjg3ODAwODc1NDAxOTkw",
        }
        ```
        """
        url = route.SP_PRODUCTS
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "state": state,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdEntities.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SpProducts.model_validate(data)

    async def SpKeywords(
        self,
        sid: int,
        profile_id: int,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpKeywords:
        """查询 SP 关键词投放

        ## Docs
        - 新广告 - 基础数据: [SP关键词](https://apidoc.lingxing.com/#/docs/newAd/baseData/spKeywords)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param state `<'str/None'>`: 广告状态, 默认 `None` (查询所有状态), 可选值:

            - `"enabled"` (启用)
            - `"paused"` (暂停)
            - `"archived"` (归档)

        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SpKeywords'>`: 返回查询到的 SP 关键词投放结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 378************,
                    # 广告组ID
                    "ad_group_id": 376************,
                    # 关键词ID
                    "keyword_id": 281************,
                    # 关键词文本
                    "keyword_text": "color",
                    # 关键词匹配类型
                    "match_type": "broad",
                    # 竞价
                    "bid": 2.0,
                    # 广告状态
                    "state": "enabled",
                    # 服务状态 [原字段 'serving_status']
                    "status": "CAMPAIGN_PAUSED",
                    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                    "create_time_ts": 1741705542679,
                    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                    "update_time_ts": 1741706022758,
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SP_KEYWORDS
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "state": state,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdEntities.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SpKeywords.model_validate(data)

    async def SpTargets(
        self,
        sid: int,
        profile_id: int,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpTargets:
        """查询 SP 目标商品投放

        ## Docs
        - 新广告 - 基础数据: [SP商品定位](https://apidoc.lingxing.com/#/docs/newAd/baseData/spTargets)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param state `<'str/None'>`: 广告状态, 默认 `None` (查询所有状态), 可选值:

            - `"enabled"` (启用)
            - `"paused"` (暂停)
            - `"archived"` (归档)

        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SpTargets'>`: 返回查询到的 SP 目标商品投放结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 327************,
                    # 广告组ID
                    "ad_group_id": 442************,
                    # 目标商品广告ID
                    "target_id": 562************,
                    # 目标定位表达式类型
                    "expression_type": "manual",
                    # 目标定位表达式 (JSON 字符串)
                    "expression": '[{"type": "asinSameAs", "value": "B00*******"}]',
                    # 目标定位解析表达式 (JSON 字符串) [原字段 'resolved_expression']
                    "expression_resolved": '[{"type": "asinSameAs", "value": "B00*******"}]',
                    # 竞价
                    "bid": 2.0,
                    # 广告状态
                    "state": "paused",
                    # 服务状态 [原字段 'serving_status']
                    "status": "CAMPAIGN_PAUSED",
                    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                    "create_time_ts": 1747815913398,
                    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                    "update_time_ts": 1747816012556,
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SP_TARGETS
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "state": state,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdEntities.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SpTargets.model_validate(data)

    async def SpNegativeKeywords(
        self,
        sid: int,
        profile_id: int,
        *,
        champaign_id: int | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpNegativeKeywords:
        """查询 SP 否定关键词投放

        ## Docs
        - 新广告 - 基础数据: [SP否定投放(keyword)](https://apidoc.lingxing.com/#/docs/newAd/baseData/spNegativeTargetsOrKeywords)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param champaign_id `<'int/None'>`: 广告活动ID, 参数来源 `SpCampaigns.campaign_id`, 默认 `None` (查询所有活动)

        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SpNegativeKeywords'>`: 返回查询到的 SP 否定投放结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 397************,
                    # 广告组ID
                    "ad_group_id": 0,
                    # 否定关键词文本 [原字段 'negative_text']
                    "keyword_text": "inexpensive",
                    # 否定匹配方式 [原字段 'negative_match_type']
                    "match_type": "negativePhrase",
                    # 广告状态
                    "state": "enabled",
                    # 服务状态 [原字段 'serving_status']
                    "status": "PORTFOLIO_OUT_OF_BUDGET",
                    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                    "create_time_ts": 1744989374515,
                    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                    "update_time_ts": 1744989374649,
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SP_NEGATIVE_TARGETING
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "targeting_type": "keyword",
            "champaign_id": champaign_id,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.SpNegativeTargeting.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SpNegativeKeywords.model_validate(data)

    async def SpNegativeTargets(
        self,
        sid: int,
        profile_id: int,
        *,
        champaign_id: int | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpNegativeTargets:
        """查询 SP 否定目标商品投放

        ## Docs
        - 新广告 - 基础数据: [SP否定投放(target)](https://apidoc.lingxing.com/#/docs/newAd/baseData/spNegativeTargetsOrKeywords)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param champaign_id `<'int/None'>`: 广告活动ID, 参数来源 `SpCampaigns.campaign_id`, 默认 `None` (查询所有活动)

        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SpNegativeTargets'>`: 返回查询到的 SP 否定目标商品投放结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 397************,
                    # 广告组ID
                    "ad_group_id": 335************,
                    # 否定目标类型 [原字段 'negative_type']
                    "target_type": "negativeAsin",
                    # 否定目标文本 [原字段 'negative_text']
                    "target_text": "B0C*******",
                    # 广告状态
                    "state": "enabled",
                    # 服务状态 [原字段 'serving_status']
                    "status": "PORTFOLIO_OUT_OF_BUDGET",
                    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                    "create_time_ts": 1744989374515,
                    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                    "update_time_ts": 1744989374649,
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SP_NEGATIVE_TARGETING
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "targeting_type": "target",
            "champaign_id": champaign_id,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.SpNegativeTargeting.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SpNegativeTargets.model_validate(data)

    # . 基础数据 - Sponsored Brands
    async def SbCampaigns(
        self,
        sid: int,
        profile_id: int,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbCampaigns:
        """查询 SB 广告活动

        ## Docs
        - 新广告 - 基础数据: [SB广告活动](https://apidoc.lingxing.com/#/docs/newAd/baseData/hsaCampaigns)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param state `<'str/None'>`: 广告状态, 默认 `None` (查询所有状态), 可选值:

            - `"enabled"` (启用)
            - `"paused"` (暂停)
            - `"archived"` (归档)

        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SbCampaigns'>`: 返回查询到的 SB 广告活动结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告组合ID
                    "portfolio_id": 0,
                    # 广告活动ID
                    "campaign_id": 560************,
                    # 广告活动名称 [原字段 'name']
                    "campaign_name": "SBV-TR9ZFH",
                    # 广告预算
                    "budget": 10.0,
                    # 广告预算类型
                    "budget_type": "daily",
                    # 自定义竞价调整
                    "bid_multiplier": 0.0,
                    # 是否使用自动竞价 (0: 否, 1: 是)
                    "bid_optimization": 0,
                    # 广告着陆页 (JSON 字符串)
                    "landing_page": '{"url": "https://www.amazon.de/dp/B07*******", "pageType": "detailPage"}',
                    # 广告创意结构 (JSON 字符串)
                    "creative": '{"type": "video", "asins": ["B07*******"], "videoMediaIds": ["amzn1.adex.media1.d9cd46ae-1a24-4ffe-b29f-74d7e131e16d"]}',
                    # 广告创意类型
                    "creative_type": "COLLECTION",
                    # 开始时间 [原字段 'start_date']
                    "start_time": "2025-05-05 00:00:00",
                    # 结束时间 [原字段 'end_date']
                    "end_time": "",
                    # 广告状态
                    "state": "paused",
                    # 服务状态 [原字段 'serving_status']
                    "status": "CAMPAIGN_PAUSED",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SB_CAMPAIGNS
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "state": state,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdEntities.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SbCampaigns.model_validate(data)

    async def SbAdGroups(
        self,
        sid: int,
        profile_id: int,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbAdGroups:
        """查询 SB 广告组

        ## Docs
        - 新广告 - 基础数据: [SB广告组](https://apidoc.lingxing.com/#/docs/newAd/baseData/hsaAdGroups)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param state `<'str/None'>`: 广告状态, 默认 `None` (查询所有状态), 可选值:

            - `"enabled"` (启用)
            - `"paused"` (暂停)
            - `"archived"` (归档)

        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SbAdGroups'>`: 返回查询到的 SB 广告组结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 476************,
                    # 广告组ID
                    "ad_group_id": 297************,
                    # 广告组名称 [原字段 'name']
                    "ad_group_name": "广告组 - 4/19/2025 17:56:43.450",
                    # 广告组状态
                    "state": "enabled",
                    # 服务状态 [原字段 'serving_status']
                    "status": "AD_GROUP_STATUS_ENABLED",
                    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                    "create_time_ts": 1745056819692,
                    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                    "update_time_ts": 1745056819692,
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SB_AD_GROUPS
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "state": state,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdEntities.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SbAdGroups.model_validate(data)

    async def SbCreatives(
        self,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbCreatives:
        """查询 SB 广告创意

        ## Docs
        - 新广告 - 基础数据: [SB广告创意](https://apidoc.lingxing.com/#/docs/newAd/baseData/sbAdHasProductAds)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SbCreatives'>`: 返回查询到的 SB 广告创意结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 378************,
                    # 广告组ID
                    "ad_group_id": 454************,
                    # 广告创意ID [原字段 'ad_creative_id']
                    "creative_id": 283************,
                    # 广告创意名称 [原字段 'name']
                    "creative_name": "商品集 广告 - 4/19/2025 17:56:42.987",
                    # 广告创意 ASIN 列表 [原字段 'asin']
                    "asins": ["B0D*******"],
                    # 广告状态
                    "state": "enabled",
                    # 服务状态 [原字段 'serving_status']
                    "status": "AD_STATUS_LIVE",
                    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                    "create_time_ts": 1745056822757,
                    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                    "update_time_ts": 1752331081315,
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SB_CREATIVES
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdEntities.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SbCreatives.model_validate(data)

    async def SbKeywords(
        self,
        sid: int,
        profile_id: int,
        ad_type: AD_SB_TYPE = "ALL",
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbKeywords:
        """查询 SB 关键词投放

        ## Docs
        - 新广告 - 基础数据: [SB广告的投放(keyword)](https://apidoc.lingxing.com/#/docs/newAd/baseData/sbTargeting)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param ad_type `<'str'>`: SB 广告类型, 默认 `"ALL"`, 可选值:

            - `"SB"` (SB 广告)
            - `"SBV"` (SB 视频广告)
            - `"ALL"` (所有 SB 广告类型)

        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SbKeywords'>`: 返回查询到的 SB 关键词投放结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 369************,
                    # 广告组ID
                    "ad_group_id": 450************,
                    # 广告类型 [原字段 'ads_type']
                    "ad_type": "SB",
                    # 投放目标类型
                    "targeting_type": "keyword",
                    # 关键词ID
                    "keyword_id": 281************,
                    # 关键词文本
                    "keyword_text": "+color",
                    # 关键词匹配类型
                    "match_type": "broad",
                    # 竞价 [原字段 'keyword_bid']
                    "bid": 1.1,
                    # 广告状态 [原字段 'keyword_state']
                    "state": "enabled",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SB_TARGETING
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "ad_type": ad_type,
            "targeting_type": "keyword",
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.SbTargeting.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SbKeywords.model_validate(data)

    async def SbTargets(
        self,
        sid: int,
        profile_id: int,
        ad_type: AD_SB_TYPE = "ALL",
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbTargets:
        """查询 SB 目标商品投放

        ## Docs
        - 新广告 - 基础数据: [SB广告的投放](https://apidoc.lingxing.com/#/docs/newAd/baseData/sbTargeting)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param ad_type `<'str'>`: SB 广告类型, 默认 `"ALL"`, 可选值:

            - `"SB"` (SB 广告)
            - `"SBV"` (SB 视频广告)
            - `"ALL"` (所有 SB 广告类型)

        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SbTargets'>`: 返回查询到的 SB 目标商品投放结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 369************,
                    # 广告组ID
                    "ad_group_id": 450************,
                    # 广告类型 [原字段 'ads_type']
                    "ad_type": "SB",
                    # 投放目标类型
                    "targeting_type": "producttarget",
                    # 目标商品广告ID
                    "target_id": 285************,
                    # 目标定位表达式 (JSON 字符串)
                    "expression": '[{"type": "asinSameAs", "value": "B0B*******"}]',
                    # 目标定位解析表达式 (JSON 字符串) [原字段 'resolved_expression']
                    "expression_resolved": '[{"type": "asinSameAs", "value": "B0B*******"}]',
                    # 竞价 [原字段 'target_bid']
                    "bid": 1.0,
                    # 广告状态 [原字段 'target_state']
                    "state": "enabled",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SB_TARGETING
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "ad_type": ad_type,
            "targeting_type": "product",
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.SbTargeting.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SbTargets.model_validate(data)

    async def SbNegativeKeywords(
        self,
        sid: int,
        profile_id: int,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbNegativeKeywords:
        """查询 SB 否定关键词投放

        ## Docs
        - 新广告 - 基础数据: [SB否定关键词](https://apidoc.lingxing.com/#/docs/newAd/baseData/hsaNegativeKeywords)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param state `<'str/None'>`: 广告状态, 默认 `None` (查询所有状态), 可选值:

            - `"enabled"` (启用)
            - `"paused"` (暂停)
            - `"archived"` (归档)

        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SbNegativeKeywords'>`: 返回查询到的 SB 否定关键词投放结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 517************,
                    # 广告组ID
                    "ad_group_id": 434************,
                    # 否定关键词ID
                    "keyword_id": 562************,
                    # 否定关键词文本
                    "keyword_text": "cheap",
                    # 否定关键词匹配类型
                    "match_type": "negativePhrase",
                    # 广告状态
                    "state": "enabled",
                    # 服务状态 [原字段 'serving_status']
                    "status": "",
                    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                    "create_time_ts": 1741601265137,
                    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                    "update_time_ts": 1741601265144,
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SB_NEGATIVE_KEYWORDS
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "state": state,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdEntities.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SbNegativeKeywords.model_validate(data)

    async def SbNegativeTargets(
        self,
        sid: int,
        profile_id: int,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbNegativeTargets:
        """查询 SB 否定目标商品投放

        ## Docs
        - 新广告 - 基础数据: [SB否定商品投放](https://apidoc.lingxing.com/#/docs/newAd/baseData/hsaNegativeTargets)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param state `<'str/None'>`: 广告状态, 默认 `None` (查询所有状态), 可选值:

            - `"enabled"` (启用)
            - `"paused"` (暂停)
            - `"archived"` (归档)

        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SbNegativeTargets'>`: 返回查询到的 SB 否定目标商品投放结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 517************,
                    # 广告组ID
                    "ad_group_id": 434************,
                    # 否定目标商品广告ID
                    "target_id": 562************,
                    # 否定目标定位类型
                    "expression_type": "manual",
                    # 否定目标定位表达式 (JSON 字符串)
                    "expression": '[{"type": "asinSameAs", "value": "B00*******"}]',
                    # 否定目标定位解析表达式 (JSON 字符串) [原字段 'resolved_expression']
                    "expression_resolved": '[{"type": "asinSameAs", "value": "B00*******"}]',
                    # 广告状态
                    "state": "enabled",
                    # 服务状态 [原字段 'serving_status']
                    "status": "",
                    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                    "create_time_ts": 1741601265137,
                    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                    "update_time_ts": 1741601265144,
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SB_NEGATIVE_TARGETS
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "state": state,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdEntities.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SbNegativeTargets.model_validate(data)

    # . 基础数据 - Sponsored Display
    async def SdCampaigns(
        self,
        sid: int,
        profile_id: int,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SdCampaigns:
        """查询 SD 广告活动

        ## Docs
        - 新广告 - 基础数据: [SD广告活动](https://apidoc.lingxing.com/#/docs/newAd/baseData/sdCampaigns)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param state `<'str/None'>`: 广告状态, 默认 `None` (查询所有状态), 可选值:

            - `"enabled"` (启用)
            - `"paused"` (暂停)
            - `"archived"` (归档)

        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SdCampaigns'>`: 返回查询到的 SD 广告活动结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告组合ID
                    "portfolio_id": 0,
                    # 广告活动ID
                    "campaign_id": 303************,
                    # 广告活动名称 [原字段 'name']
                    "campaign_name": "SD-TEST",
                    # 投放类型
                    "tactic": "T00030",
                    # 竞价类型 [原字段 'cost_type']
                    "bid_type": "cpc",
                    # 每日预算
                    "budget": 3.0,
                    # 预算类型
                    "budget_type": "daily",
                    # 开始时间 [原字段 'start_date']
                    "start_time": "2025-07-11 00:00:00",
                    # 结束时间 [原字段 'end_date']
                    "end_time": "",
                    # 广告状态
                    "state": "paused",
                    # 服务状态 [原字段 'serving_status']
                    "status": "CAMPAIGN_PAUSED",
                    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                    "create_time_ts": 1752293593320,
                    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date
                    "update_time_ts": 1752761805148,
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SD_CAMPAIGNS
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "state": state,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdEntities.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SdCampaigns.model_validate(data)

    async def SdAdGroups(
        self,
        sid: int,
        profile_id: int,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SdAdGroups:
        """查询 SD 广告组

        ## Docs
        - 新广告 - 基础数据: [SD广告组](https://apidoc.lingxing.com/#/docs/newAd/baseData/sdAdGroups)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param state `<'str/None'>`: 广告状态, 默认 `None` (查询所有状态), 可选值:

            - `"enabled"` (启用)
            - `"paused"` (暂停)
            - `"archived"` (归档)

        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SdAdGroups'>`: 返回查询到的 SD 广告组结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 414************,
                    # 广告组ID
                    "ad_group_id": 301************,
                    # 广告组名称 [原字段 'name']
                    "ad_group_name": "广告组 - 3/11/2025 15:00:48.627",
                    # 默认竞价
                    "default_bid": 0.02,
                    # 竞价优化方式
                    "bid_optimization": "clicks",
                    # 广告组状态
                    "state": "paused",
                    # 服务状态 [原字段 'serving_status']
                    "status": "CAMPAIGN_PAUSED",
                    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                    "create_time_ts": 1741677037099,
                    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                    "update_time_ts": 1747663132380,
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SD_AD_GROUPS
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "state": state,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdEntities.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SdAdGroups.model_validate(data)

    async def SdProducts(
        self,
        sid: int,
        profile_id: int,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SdProducts:
        """查询 SD 商品投放

        ## Docs
        - 新广告 - 基础数据: [SD广告商品](https://apidoc.lingxing.com/#/docs/newAd/baseData/sdProductAds)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param state `<'str/None'>`: 广告状态, 默认 `None` (查询所有状态), 可选值:

            - `"enabled"` (启用)
            - `"paused"` (暂停)
            - `"archived"` (归档)

        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SdProducts'>`: 返回查询到的 SD 商品投放结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 303************,
                    # 广告组ID
                    "ad_group_id": 429************,
                    # 商品广告ID
                    "ad_id": 556************,
                    # 商品ASIN
                    "asin": "B0D*******",
                    # 亚马逊SKU [原字段 'sku']
                    "msku": "SKU********",
                    # 广告状态
                    "state": "enabled",
                    # 服务状态 [原字段 'serving_status']
                    "status": "CAMPAIGN_PAUSED",
                    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                    "create_time_ts": 1752293594049,
                    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                    "update_time_ts": 1752294110214,
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SD_PRODUCTS
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "state": state,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdEntities.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SdProducts.model_validate(data)

    async def SdTargets(
        self,
        sid: int,
        profile_id: int,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SdTargets:
        """查询 SD 目标商品投放

        ## Docs
        - 新广告 - 基础数据: [SD商品定位](https://apidoc.lingxing.com/#/docs/newAd/baseData/sdTargets)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param state `<'str/None'>`: 广告状态, 默认 `None` (查询所有状态), 可选值:

            - `"enabled"` (启用)
            - `"paused"` (暂停)
            - `"archived"` (归档)

        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SdTargets'>`: 返回查询到的 SD 目标商品投放结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 536************,
                    # 广告组ID
                    "ad_group_id": 385************,
                    # 目标商品广告ID
                    "target_id": 560************,
                    # 目标定位类型
                    "expression_type": "manual",
                    # 目标定位表达式 (JSON 字符串)
                    "expression": '[{"type": "asinSameAs", "value": "B0C*******"}]',
                    # 目标定位解析表达式 (JSON 字符串) [原字段 'resolved_expression']
                    "expression_resolved": '[{"type": "asinSameAs", "value": "B0C*******"}]',
                    # 竞价
                    "bid": 1.0,
                    # 广告状态
                    "state": "enabled",
                    # 服务状态 [原字段 'serving_status']
                    "status": "CAMPAIGN_PAUSED",
                    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                    "create_time_ts": 1738163058574,
                    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                    "update_time_ts": 1738163058579,
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SD_TARGETS
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "state": state,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdEntities.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SdTargets.model_validate(data)

    async def SdNegativeTargets(
        self,
        sid: int,
        profile_id: int,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SdNegativeTargets:
        """查询 SD 否定目标商品投放

        ## Docs
        - 新广告 - 基础数据: [SD否定商品定位](https://apidoc.lingxing.com/#/docs/newAd/baseData/sdNegativeTargets)

        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param state `<'str/None'>`: 广告状态, 默认 `None` (查询所有状态), 可选值:

            - `"enabled"` (启用)
            - `"paused"` (暂停)
            - `"archived"` (归档)

        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SdNegativeTargets'>`: 返回查询到的 SD 否定目标商品投放结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 536************,
                    # 广告组ID
                    "ad_group_id": 385************,
                    # 否定目标商品广告ID
                    "target_id": 560************,
                    # 否定目标定位类型
                    "expression_type": "manual",
                    # 否定目标定位表达式 (JSON 字符串)
                    "expression": '[{"type": "asinSameAs", "value": "B0C*******"}]',
                    # 否定目标定位解析表达式 (JSON 字符串) [原字段 'resolved_expression']
                    "expression_resolved": '[{"type": "asinSameAs", "value": "B0C*******"}]',
                    # 广告状态
                    "state": "enabled",
                    # 服务状态 [原字段 'serving_status']
                    "status": "CAMPAIGN_PAUSED",
                    # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                    "create_time_ts": 1738163058574,
                    # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                    "update_time_ts": 1738163058579,
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SD_NEGATIVE_TARGETS
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "state": state,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdEntities.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SdNegativeTargets.model_validate(data)

    # 报告 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # . 报告 - Sponsored Products
    async def SpCampaignReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpCampaignReports:
        """查询 SP 广告活动报告

        ## Docs
        - 新广告 - 报告: [SP广告活动报表](https://apidoc.lingxing.com/#/docs/newAd/report/spCampaignReports)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SpCampaignReports'>`: 返回查询到的 SP 广告活动报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 541************,
                    # 投放目标类型
                    "targeting_type": "",
                    # 广告花费
                    "cost": 41.6,
                    # 总展示次数
                    "impressions": 1569,
                    # 总点击次数
                    "clicks": 14,
                    # 广告订单数
                    "orders": 7,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 7,
                    # 广告成交商品件数
                    "units": 7,
                    # 直接广告成交商品件数 [原字段 'same_units']
                    "direct_units": 7,
                    # 广告销售额
                    "sales": 181.23,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 181.23,
                    # 报告日期
                    "report_date": "2025-08-23",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SP_CAMPAIGN_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SpCampaignReports.model_validate(data)

    async def SpCampaignHourData(
        self,
        report_date: str | datetime.date | datetime.datetime,
        campaign_id: int,
    ) -> schema.SpCampaignHourData:
        """查询 SP 广告活动小时数据

        ## Docs
        - 新广告 - 报告: [SP广告活动小时数据](https://apidoc.lingxing.com/#/docs/newAd/report/spCampaignHourData)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param campaign_id `<'int'>`: 广告活动ID, 参数来源 `SpCampaign.campaign_id`
        :returns `<'SpCampaignHourData'>`: 返回查询到的 SP 广告活动小时数据结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 287************,
                    # 广告花费
                    "cost": 1.48,
                    # 总展示次数
                    "impressions": 14,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 广告成交商品件数
                    "units": 1,
                    # 直接广告成交商品件数 [原字段 'same_units']
                    "direct_units": 1,
                    # 广告销售额
                    "sales": 35.0,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 35.0,
                    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                    "ctr": 0.0714,
                    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                    "cvr": 1.0,
                    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                    "cpc": 1.48,
                    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                    "cpa": 1.48,
                    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                    "acos": 0.0423,
                    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                    "roas": 23.65,
                    # 数据所属小时 (0-23)
                    "hour": 0,
                    # 报告日期
                    "report_date": "2025-08-25",
                },
                ...
            ],
        }
        ```
        """
        url = route.SP_CAMPAIGN_HOUR_DATA
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "campaign_id": campaign_id,
        }
        try:
            p = param.AdHourData.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SpCampaignHourData.model_validate(data)

    async def SpPlacementReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpPlacementReports:
        """查询 SP 广告活动投放位置报告

        ## Docs
        - 新广告 - 报告: [SP广告位报告](https://apidoc.lingxing.com/#/docs/newAd/report/campaignPlacementReports)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SpPlacementReports'>`: 返回查询到的 SP 广告活动投放位置报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 548************,
                    # 广告投放位置 [原字段 'placement_type']
                    "placement": "OTHER ON-AMAZON",
                    # 广告花费
                    "cost": 38.4,
                    # 总展示次数
                    "impressions": 1213,
                    # 总点击次数
                    "clicks": 12,
                    # 广告订单数
                    "orders": 6,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 6,
                    # 广告成交商品件数
                    "units": 6,
                    # 直接广告成交商品件数 [原字段 'same_units']
                    "direct_units": 6,
                    # 广告销售额
                    "sales": 155.34,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 155.34,
                    # 报告日期
                    "report_date": "2025-08-23",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SP_PLACEMENT_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SpPlacementReports.model_validate(data)

    async def SpPlacementHourData(
        self,
        report_date: str | datetime.date | datetime.datetime,
        campaign_id: int,
    ) -> schema.SpPlacementHourData:
        """查询 SP 广告活动投放位置小时数据

        ## Docs
        - 新广告 - 报告: [SP广告位小时数据](https://apidoc.lingxing.com/#/docs/newAd/report/spAdPlacementHourData)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param campaign_id `<'int'>`: 广告活动ID, 参数来源 `SpCampaign.campaign_id`
        :returns `<'SpPlacementHourData'>`: 返回查询到的 SP 广告活动投放位置小时数据结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 287************,
                    # 广告投放位置
                    "placement": "Other on-Amazon",
                    # 广告花费
                    "cost": 1.48,
                    # 总展示次数
                    "impressions": 14,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 广告成交商品件数
                    "units": 1,
                    # 直接广告成交商品件数 [原字段 'same_units']
                    "direct_units": 1,
                    # 广告销售额
                    "sales": 35.0,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 35.0,
                    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                    "ctr": 0.0714,
                    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                    "cvr": 1.0,
                    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                    "cpc": 1.48,
                    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                    "cpa": 1.48,
                    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                    "acos": 0.0423,
                    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                    "roas": 23.65,
                    # 数据所属小时 (0-23)
                    "hour": 0,
                    # 报告日期
                    "report_date": "2025-08-25",
                },
                ...
            ],
        }
        ```
        """
        url = route.SP_PLACEMENT_HOUR_DATA
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "campaign_id": campaign_id,
        }
        try:
            p = param.AdHourData.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SpPlacementHourData.model_validate(data)

    async def SpAdGroupReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpAdGroupReports:
        """查询 SP 广告组报告

        ## Docs
        - 新广告 - 报告: [SP广告组报表](https://apidoc.lingxing.com/#/docs/newAd/report/spAdGroupReports)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SpAdGroupReports'>`: 返回查询到的 SP 广告组报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 548************,
                    # 广告组ID
                    "ad_group_id": 511************,
                    # 广告花费
                    "cost": 41.6,
                    # 总展示次数
                    "impressions": 1569,
                    # 总点击次数
                    "clicks": 14,
                    # 广告订单数
                    "orders": 7,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 7,
                    # 广告成交商品件数
                    "units": 7,
                    # 直接广告成交商品件数 [原字段 'same_units']
                    "direct_units": 7,
                    # 广告销售额
                    "sales": 181.23,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 181.23,
                    # 报告日期
                    "report_date": "2025-08-23",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SP_AD_GROUP_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SpAdGroupReports.model_validate(data)

    async def SpAdGroupHourData(
        self,
        report_date: str | datetime.date | datetime.datetime,
        campaign_id: int,
    ) -> schema.SpAdGroupHourData:
        """查询 SP 广告组小时数据

        ## Docs
        - 新广告 - 报告: [SP广告组小时数据](https://apidoc.lingxing.com/#/docs/newAd/report/spAdGroupHourData)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param campaign_id `<'int'>`: 广告活动ID, 参数来源 `SpCampaign.campaign_id`
        :returns `<'SpAdGroupHourData'>`: 返回查询到的 SP 广告组小时数据结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 287************,
                    # 广告组ID [原字段 'group_id']
                    "ad_group_id": 367************,
                    # 广告花费
                    "cost": 1.48,
                    # 总展示次数
                    "impressions": 14,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 广告成交商品件数
                    "units": 1,
                    # 直接广告成交商品件数 [原字段 'same_units']
                    "direct_units": 1,
                    # 广告销售额
                    "sales": 35.0,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 35.0,
                    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                    "ctr": 0.0714,
                    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                    "cvr": 1.0,
                    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                    "cpc": 1.48,
                    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                    "cpa": 1.48,
                    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                    "acos": 0.0423,
                    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                    "roas": 23.65,
                    # 数据所属小时 (0-23)
                    "hour": 0,
                    # 报告日期
                    "report_date": "2025-08-25",
                },
                ...
            ],
        }
        ```
        """
        url = route.SP_AD_GROUP_HOUR_DATA
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "campaign_id": campaign_id,
        }
        try:
            p = param.AdHourData.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SpAdGroupHourData.model_validate(data)

    async def SpProductReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpProductReports:
        """查询 SP 商品投放报告

        ## Docs
        - 新广告 - 报告: [SP广告商品报表](https://apidoc.lingxing.com/#/docs/newAd/report/spProductAdReports)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SpProductReports'>`: 返回查询到的 SP 商品投放报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 512************,
                    # 广告组ID
                    "ad_group_id": 367************,
                    # 商品广告ID
                    "ad_id": 537************,
                    # 商品ASIN
                    "asin": "B0D*******",
                    # 亚马逊SKU [原字段 'sku']
                    "msku": "SKU*********",
                    # 广告花费
                    "cost": 18.7,
                    # 总展示次数
                    "impressions": 1102,
                    # 总点击次数
                    "clicks": 8,
                    # 广告订单数
                    "orders": 5,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 5,
                    # 广告成交商品件数
                    "units": 5,
                    # 直接广告成交商品件数 [原字段 'same_units']
                    "direct_units": 5,
                    # 广告销售额
                    "sales": 149.4,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 149.4,
                    # 报告日期
                    "report_date": "2025-08-23",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SP_PRODUCT_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SpProductReports.model_validate(data)

    async def SpProductHourData(
        self,
        report_date: str | datetime.date | datetime.datetime,
        campaign_id: int,
    ) -> schema.SpProductHourData:
        """查询 SP 商品投放小时数据

        ## Docs
        - 新广告 - 报告: [SP广告小时数据(ad)](https://apidoc.lingxing.com/#/docs/newAd/report/spTargetHourData)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param campaign_id `<'int'>`: 广告活动ID, 参数来源 `SpCampaign.campaign_id`
        :returns `<'SpProductHourData'>`: 返回查询到的 SP 商品投放小时数据结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 494************,
                    # 广告组ID [原字段 'group_id']
                    "ad_group_id": 340************,
                    # 商品广告ID
                    "ad_id": 282************,
                    # 商品ASIN
                    "asin": "B0F*******",
                    # 亚马逊SKU
                    "msku": "SKU*********",
                    # 广告花费
                    "cost": 77.96,
                    # 总展示次数
                    "impressions": 369,
                    # 总点击次数
                    "clicks": 13,
                    # 广告订单数
                    "orders": 3,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 3,
                    # 广告成交商品件数
                    "units": 3,
                    # 直接广告成交商品件数 [原字段 'same_units']
                    "direct_units": 3,
                    # 广告销售额
                    "sales": 119.67,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 119.67,
                    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                    "ctr": 0.0352,
                    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                    "cvr": 0.2308,
                    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                    "cpc": 6.0,
                    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                    "cpa": 25.99,
                    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                    "acos": 0.6515,
                    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                    "roas": 1.54,
                    # 数据所属小时 (0-23)
                    "hour": 18,
                    # 报告日期
                    "report_date": "2025-08-25",
                },
                ...
            ],
        }
        ```
        """
        url = route.SP_PRODUCT_KEYWORD_HOUR_DATA
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "campaign_id": campaign_id,
            "agg_dimension": "ad",
        }
        try:
            p = param.AdHourData.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SpProductHourData.model_validate(data)

    async def SpKeywordReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpKeywordReports:
        """查询 SP 关键词投放报告

        ## Docs
        - 新广告 - 报告: [SP关键词报表](https://apidoc.lingxing.com/#/docs/newAd/report/spKeywordReports)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SpKeywordReports'>`: 返回查询到的 SP 关键词投放报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 512************,
                    # 广告组ID
                    "ad_group_id": 367************,
                    # 关键词ID
                    "keyword_id": 557************,
                    # 关键词文本
                    "keyword_text": "color",
                    # 关键词匹配类型
                    "match_type": "BROAD",
                    # 广告花费
                    "cost": 5.1,
                    # 总展示次数
                    "impressions": 167,
                    # 总点击次数
                    "clicks": 2,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 广告成交商品件数
                    "units": 1,
                    # 直接广告成交商品件数 [原字段 'same_units']
                    "direct_units": 1,
                    # 广告销售额
                    "sales": 29.88,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 29.88,
                    # 报告日期
                    "report_date": "2025-08-23",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SP_KEYWORD_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SpKeywordReports.model_validate(data)

    async def SpKeywordHourData(
        self,
        report_date: str | datetime.date | datetime.datetime,
        campaign_id: int,
    ) -> schema.SpKeywordHourData:
        """查询 SP 关键词投放小时数据

        ## Docs
        - 新广告 - 报告: [SP广告小时数据(both_ad_target)](https://apidoc.lingxing.com/#/docs/newAd/report/spTargetHourData)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param campaign_id `<'int'>`: 广告活动ID, 参数来源 `SpCampaign.campaign_id`
        :returns `<'SpKeywordHourData'>`: 返回查询到的 SP 关键词投放小时数据结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 494************,
                    # 广告组ID [原字段 'group_id']
                    "ad_group_id": 340************,
                    # 商品广告ID
                    "ad_id": 282************,
                    # 关键词ID [原字段 'targeting_id']
                    "keyword_id": 557************,
                    # 关键词文本 [原字段 'targeting']
                    "keyword_text": "color",
                    # 关键词匹配类型
                    "match_type": "BROAD",
                    # 商品ASIN
                    "asin": "B0F*******",
                    # 亚马逊SKU
                    "msku": "SKU*********",
                    # 广告花费
                    "cost": 77.96,
                    # 总展示次数
                    "impressions": 369,
                    # 总点击次数
                    "clicks": 13,
                    # 广告订单数
                    "orders": 3,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 3,
                    # 广告成交商品件数
                    "units": 3,
                    # 直接广告成交商品件数 [原字段 'same_units']
                    "direct_units": 3,
                    # 广告销售额
                    "sales": 119.67,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 119.67,
                    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                    "ctr": 0.0352,
                    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                    "cvr": 0.2308,
                    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                    "cpc": 6.0,
                    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                    "cpa": 25.99,
                    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                    "acos": 0.6515,
                    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                    "roas": 1.54,
                    # 数据所属小时 (0-23)
                    "hour": 18,
                    # 报告日期
                    "report_date": "2025-08-25",
                },
                ...
            ],
        }
        ```
        """
        url = route.SP_PRODUCT_KEYWORD_HOUR_DATA
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "campaign_id": campaign_id,
            "agg_dimension": "both_ad_target",
        }
        try:
            p = param.AdHourData.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SpKeywordHourData.model_validate(data)

    async def SpTargetReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpTargetReports:
        """查询 SP 目标商品投放报告

        ## Docs
        - 新广告 - 报告: [SP商品定位报表](https://apidoc.lingxing.com/#/docs/newAd/report/spTargetReports)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SpTargetReports'>`: 返回查询到的 SP 目标商品投放报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 363************,
                    # 广告组ID
                    "ad_group_id": 353************,
                    # 目标商品广告ID
                    "target_id": 529************,
                    # 目标定位表达式类型 [原字段 'targeting_type']
                    "expression_type": "TARGETING_EXPRESSION",
                    # 目标定位表达式 (JSON 字符串) [原字段 'targeting_expression']
                    "expression": '"[{\\"type\\": \\"asinSameAs\\", \\"value\\": \\"B06*******\\"}]"',
                    # 广告花费
                    "cost": 4.8,
                    # 总展示次数
                    "impressions": 157,
                    # 总点击次数
                    "clicks": 2,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 广告成交商品件数
                    "units": 1,
                    # 直接广告成交商品件数 [原字段 'same_units']
                    "direct_units": 1,
                    # 广告销售额
                    "sales": 39.89,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 39.89,
                    # 报告日期
                    "report_date": "2025-08-23",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SP_TARGET_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SpTargetReports.model_validate(data)

    async def SpTargetHourData(
        self,
        report_date: str | datetime.date | datetime.datetime,
        campaign_id: int,
    ) -> schema.SpTargetHourData:
        """查询 SP 目标商品投放小时数据

        ## Docs
        - 新广告 - 报告: [SP投放小时数据(both_ad_target)](https://apidoc.lingxing.com/#/docs/newAd/report/spTargetHourData)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param campaign_id `<'int'>`: 广告活动ID, 参数来源 `SpCampaign.campaign_id`
        :returns `<'SpTargetHourData'>`: 返回查询到的 SP 目标商品投放小时数据结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 442************,
                    # 广告组ID [原字段 'group_id']
                    "ad_group_id": 297************,
                    # 商品广告ID
                    "ad_id": 401************,
                    # 目标商品广告ID [原字段 'targeting_id']
                    "target_id": 297************,
                    # 目标商品文本 [原字段 'targeting']
                    "target_text": 'asin="B01*******"',
                    # 目标匹配类型 [原字段 'match_type']
                    "target_type": "TARGETING_EXPRESSION",
                    # 商品ASIN
                    "asin": "B0F*******",
                    # 亚马逊SKU
                    "msku": "SKU*********",
                    # 广告花费
                    "cost": 2.4,
                    # 广告花费
                    "impressions": 28,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 广告成交商品件数
                    "units": 1,
                    # 直接广告成交商品件数 [原字段 'same_units']
                    "direct_units": 1,
                    # 广告销售额
                    "sales": 39.89,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 39.89,
                    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                    "ctr": 0.0357,
                    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                    "cvr": 1.0,
                    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                    "cpc": 2.4,
                    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                    "cpa": 2.4,
                    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                    "acos": 0.0602,
                    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                    "roas": 16.62,
                    # 数据所属小时 (0-23)
                    "hour": 20,
                    # 报告日期
                    "report_date": "2025-08-25",
                },
                ...
            ],
        }
        ```
        """
        url = route.SP_TARGET_HOUR_DATA
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "campaign_id": campaign_id,
            "agg_dimension": "both_ad_target",
        }
        try:
            p = param.AdHourData.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SpTargetHourData.model_validate(data)

    async def SpQueryWordReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpQueryWordReports:
        """查询 SP 用户搜索词报告

        ## Docs
        - 新广告 - 报告: [SP用户搜索词报表](https://apidoc.lingxing.com/#/docs/newAd/report/queryWordReports)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SpQueryWordReports'>`: 返回查询到的 SP 用户搜索词报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 336************,
                    # 广告组ID
                    "ad_group_id": 351************,
                    # 关键词ID [原字段 'target_id']
                    "keyword_id": 508************,
                    # 关键词文本 [原字段 'target_text']
                    "keyword_text": "canon ts3120 ink cartridges",
                    # 用户使用搜索词 [原字段 'query']
                    "query_text": "canon pixma ts3120 color ink cartridges",
                    # 关键词匹配类型
                    "match_type": "BROAD",
                    # 广告花费
                    "cost": 2.55,
                    # 总展示次数
                    "impressions": 2,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 广告成交商品件数
                    "units": 1,
                    # 直接广告成交商品件数 [原字段 'same_units']
                    "direct_units": 1,
                    # 广告销售额
                    "sales": 29.88,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 29.88,
                    # 报告日期
                    "report_date": "2025-08-23",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SP_QUERY_WORD_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SpQueryWordReports.model_validate(data)

    # . 报告 - Sponsored Brands
    async def SbCampaignReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbCampaignReports:
        """查询 SB 广告活动报告

        ## Docs
        - 新广告 - 报告: [SB广告活动报表](https://apidoc.lingxing.com/#/docs/newAd/report/hsaCampaignReports)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SbCampaignReports'>`: 返回查询到的 SB 广告活动报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 372************,
                    # 广告花费
                    "cost": 39.62,
                    # 总展示次数
                    "impressions": 1694,
                    # 总点击次数
                    "clicks": 34,
                    # 广告订单数
                    "orders": 11,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 11,
                    # 品牌新买家广告订单数
                    "new_to_brand_orders": 10,
                    # 品牌新买家订单占比 [原字段 'new_to_brand_order_percentage']
                    # (品牌新买家广告订单数 / 广告订单数 x 100%)
                    "new_to_brand_order_pct": 90.91,
                    # 品牌新买家订单转化率
                    # (品牌新买家广告订单数 / 总点击次数 x 100%)
                    "new_to_brand_order_rate": 29.41,
                    # 广告成交商品件数
                    "units": 12,
                    # 直接广告成交商品件数 [原字段 'same_units']
                    "direct_units": 12,
                    # 品牌新买家成交商品件数
                    "new_to_brand_units": 11,
                    # 广告销售额
                    "sales": 430.8,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 430.8,
                    # 品牌新买家销售额
                    "new_to_brand_sales": 394.9,
                    # 广告可见率 - View Through Rate
                    # (可见展示次数 / 总展示次数 x 100%)
                    "vtr": 27.98,
                    # 广告可见点击率 - View Click Through Rate
                    # (总点击次数 / 可见展示次数 x 100%)
                    "vctr": 7.17,
                    # 报告日期
                    "report_date": "2025-08-23",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SB_CAMPAIGN_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SbCampaignReports.model_validate(data)

    async def SbCampaignHourData(
        self,
        report_date: str | datetime.date | datetime.datetime,
        campaign_id: int,
    ) -> schema.SbCampaignHourData:
        """查询 SB 广告活动小时数据

        ## Docs
        - 新广告 - 报告: [SB广告活动小时数据](https://apidoc.lingxing.com/#/docs/newAd/report/sbCampaignHourData)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param campaign_id `<'int'>`: 广告活动ID, 参数来源 `SbCampaign.campaign_id`
        :returns `<'SbCampaignHourData'>`: 返回查询到的 SB 广告活动小时数据结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 442************,
                    # 广告花费
                    "cost": 2.4,
                    # 广告花费
                    "impressions": 28,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 广告成交商品件数
                    "units": 1,
                    # 广告销售额
                    "sales": 39.89,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 39.89,
                    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                    "ctr": 0.0357,
                    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                    "cvr": 1.0,
                    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                    "cpc": 2.4,
                    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                    "cpa": 2.4,
                    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                    "acos": 0.0602,
                    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                    "roas": 16.62,
                    # 数据所属小时 (0-23)
                    "hour": 20,
                    # 报告日期
                    "report_date": "2025-08-25",
                },
                ...
            ],
        }
        ```
        """
        url = route.SB_CAMPAIGN_HOUR_DATA
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "campaign_id": campaign_id,
        }
        try:
            p = param.AdHourData.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SbCampaignHourData.model_validate(data)

    async def SbPlacementReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbPlacementReports:
        """查询 SB 广告活动投放位置报告

        ## Docs
        - 新广告 - 报告: [SB广告活动-广告位报告](https://apidoc.lingxing.com/#/docs/newAd/report/hsaCampaignPlacementReports)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SbPlacementReports'>`: 返回查询到的 SB 广告活动投放位置报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 451************,
                    # 广告投放位置 [原字段 'placement_type']
                    "placement": "Top of Search on-Amazon",
                    # 广告创意类型
                    "creative_type": "all",
                    # 广告花费
                    "cost": 4.87,
                    # 总展示次数
                    "impressions": 112,
                    # 总点击次数
                    "clicks": 5,
                    # 广告订单数
                    "orders": 4,
                    # 品牌新买家广告订单数
                    "new_to_brand_orders": 3,
                    # 品牌新买家订单占比 [原字段 'new_to_brand_order_percentage']
                    # (品牌新买家广告订单数 / 广告订单数 x 100%)
                    "new_to_brand_order_pct": 75.0,
                    # 品牌新买家订单转化率
                    # (品牌新买家广告订单数 / 总点击次数 x 100%)
                    "new_to_brand_order_rate": 60.0,
                    # 广告成交商品件数
                    "units": 4,
                    # 直接广告成交商品件数 [原字段 'same_units']
                    "direct_units": 4,
                    # 品牌新买家成交商品件数
                    "new_to_brand_units": 3,
                    # 广告销售额
                    "sales": 159.56,
                    # 品牌新买家销售额
                    "new_to_brand_sales": 119.67,
                    # 报告日期
                    "report_date": "2025-08-23",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SB_PLACEMENT_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SbPlacementReports.model_validate(data)

    async def SbPlacementHourData(
        self,
        report_date: str | datetime.date | datetime.datetime,
        campaign_id: int,
    ) -> schema.SbPlacementHourData:
        """查询 SB 广告活动投放位置小时数据

        ## Docs
        - 新广告 - 报告: [SB广告位小时数据](https://apidoc.lingxing.com/#/docs/newAd/report/sbAdPlacementHourData)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param campaign_id `<'int'>`: 广告活动ID, 参数来源 `SbCampaign.campaign_id`
        :returns `<'SbPlacementHourData'>`: 返回查询到的 SB 广告活动投放位置小时数据结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 442************,
                    # 广告投放位置
                    placement: "Other on-Amazon",
                    # 广告花费
                    "cost": 2.4,
                    # 广告花费
                    "impressions": 28,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 广告成交商品件数
                    "units": 1,
                    # 广告销售额
                    "sales": 39.89,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 39.89,
                    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                    "ctr": 0.0357,
                    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                    "cvr": 1.0,
                    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                    "cpc": 2.4,
                    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                    "cpa": 2.4,
                    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                    "acos": 0.0602,
                    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                    "roas": 16.62,
                    # 数据所属小时 (0-23)
                    "hour": 20,
                    # 报告日期
                    "report_date": "2025-08-25",
                },
                ...
            ],
        }
        ```
        """
        url = route.SB_PLACEMENT_HOUR_DATA
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "campaign_id": campaign_id,
        }
        try:
            p = param.AdHourData.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SbPlacementHourData.model_validate(data)

    async def SbAdGroupReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbAdGroupReports:
        """查询 SB 广告组报告

        ## Docs
        - 新广告 - 报告: [SB广告组报表](https://apidoc.lingxing.com/#/docs/newAd/report/hsaAdGroupReports)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SbAdGroupReports'>`: 返回查询到的 SB 广告组报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 536************,
                    # 广告组ID
                    "ad_group_id": 445************,
                    # 广告花费
                    "cost": 12.88,
                    # 总展示次数
                    "impressions": 805,
                    # 总点击次数
                    "clicks": 17,
                    # 广告订单数
                    "orders": 4,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 4,
                    # 品牌新买家广告订单数
                    "new_to_brand_orders": 4,
                    # 品牌新买家订单占比 [原字段 'new_to_brand_order_percentage']
                    # (品牌新买家广告订单数 / 广告订单数 x 100%)
                    "new_to_brand_order_pct": 100.0,
                    # 品牌新买家订单转化率
                    # (品牌新买家广告订单数 / 总点击次数 x 100%)
                    "new_to_brand_order_rate": 23.53,
                    # 广告成交商品件数
                    "units": 5,
                    # 直接广告成交商品件数 [原字段 'same_units']
                    "direct_units": 5,
                    # 品牌新买家成交商品件数
                    "new_to_brand_units": 5,
                    # 广告销售额
                    "sales": 149.4,
                    # 直接广告销售额 [原字段 'same_sales']
                    "new_to_brand_sales": 149.4,
                    # 广告可见率 - View Through Rate
                    # (可见展示次数 / 总展示次数 x 100%)
                    "vtr": 20.87,
                    # 广告可见点击率 - View Click Through Rate
                    # (总点击次数 / 可见展示次数 x 100%)
                    "vctr": 10.12,
                    # 报告日期
                    "report_date": "2025-08-23",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SB_AD_GROUP_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SbAdGroupReports.model_validate(data)

    async def SbAdGroupHourData(
        self,
        report_date: str | datetime.date | datetime.datetime,
        campaign_id: int,
    ) -> schema.SbAdGroupHourData:
        """查询 SB 广告组小时数据

        ## Docs
        - 新广告 - 报告: [SB广告组小时数据](https://apidoc.lingxing.com/#/docs/newAd/report/sbAdGroupHourData)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param campaign_id `<'int'>`: 广告活动ID, 参数来源 `SbCampaign.campaign_id`
        :returns `<'SbAdGroupHourData'>`: 返回查询到的 SB 广告组小时数据结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 442************,
                    # 广告组ID [原字段 'group_id']
                    "ad_group_id": 329************,
                    # 广告花费
                    "cost": 2.4,
                    # 广告花费
                    "impressions": 28,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 广告成交商品件数
                    "units": 1,
                    # 广告销售额
                    "sales": 39.89,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 39.89,
                    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                    "ctr": 0.0357,
                    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                    "cvr": 1.0,
                    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                    "cpc": 2.4,
                    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                    "cpa": 2.4,
                    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                    "acos": 0.0602,
                    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                    "roas": 16.62,
                    # 数据所属小时 (0-23)
                    "hour": 20,
                    # 报告日期
                    "report_date": "2025-08-25",
                },
                ...
            ],
        }
        ```
        """
        url = route.SB_AD_GROUP_HOUR_DATA
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "campaign_id": campaign_id,
        }
        try:
            p = param.AdHourData.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SbAdGroupHourData.model_validate(data)

    async def SbCreativeReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbCreativeReports:
        """查询 SB 广告创意报告

        ## Docs
        - 新广告 - 报告: [SB广告创意报告](https://apidoc.lingxing.com/#/docs/newAd/report/listHsaProductAdReport)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SbCreativeReports'>`: 返回查询到的 SB 广告创意报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 451************,
                    # 广告组ID
                    "ad_group_id": 329************,
                    # 广告创意ID [原字段 'ad_creative_id']
                    "creative_id": 442************,
                    # 广告花费
                    "cost": 7.06,
                    # 总展示次数
                    "impressions": 1335,
                    # 总点击次数
                    "clicks": 7,
                    # 广告订单数
                    "orders": 5,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 5,
                    # 品牌新买家广告订单数
                    "new_to_brand_orders": 5,
                    # 品牌新买家订单占比 [原字段 'new_to_brand_order_percentage']
                    # (品牌新买家广告订单数 / 广告订单数 x 100%)
                    "new_to_brand_order_pct": 100.0,
                    # 品牌新买家订单转化率
                    # (品牌新买家广告订单数 / 总点击次数 x 100%)
                    "new_to_brand_order_rate": 71.43,
                    # 广告成交商品件数
                    "units": 6,
                    # 直接广告成交商品件数 [原字段 'same_units']
                    "direct_units": 6,
                    # 品牌新买家成交商品件数
                    "new_to_brand_units": 6,
                    # 广告销售额
                    "sales": 239.34,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 239.34,
                    # 品牌新买家销售额
                    "new_to_brand_sales": 239.34,
                    # 广告可见率 - View Through Rate
                    # (可见展示次数 / 总展示次数 x 100%)
                    "vtr": 13.86,
                    # 广告可见点击率 - View Click Through Rate
                    # (总点击次数 / 可见展示次数 x 100%)
                    "vctr": 3.78,
                    # 报告日期
                    "report_date": "2025-08-24",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SB_CREATIVE_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SbCreativeReports.model_validate(data)

    async def SbKeywordReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbKeywordReports:
        """查询 SB 关键词投放报告

        ## Docs
        - 新广告 - 报告: [SB广告的投放报告(keyword)](https://apidoc.lingxing.com/#/docs/newAd/report/listHsaTargetingReport)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SbKeywordReports'>`: 返回查询到的 SB 关键词投放报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 404************,
                    # 广告组ID
                    "ad_group_id": 328************,
                    # 关键词ID
                    "keyword_id": 562************,
                    # 广告创意类型
                    "creative_type": "all",
                    # 广告花费
                    "cost": 1.49,
                    # 总展示次数
                    "impressions": 5,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 品牌新买家广告订单数
                    "new_to_brand_orders": 1,
                    # 品牌新买家订单占比 [原字段 'new_to_brand_order_percentage']
                    # (品牌新买家广告订单数 / 广告订单数 x 100%)
                    "new_to_brand_order_pct": 100.0,
                    # 品牌新买家订单转化率
                    # (品牌新买家广告订单数 / 总点击次数 x 100%)
                    "new_to_brand_order_rate": 100.0,
                    # 广告成交商品件数
                    "units": 1,
                    # 直接广告成交商品件数 [原字段 'same_units']
                    "direct_units": 1,
                    # 品牌新买家成交商品件数
                    "new_to_brand_units": 1,
                    # 广告销售额
                    "sales": 35.0,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 35.0,
                    # 品牌新买家销售额
                    "new_to_brand_sales": 35.0,
                    # 报告日期
                    "report_date": "2025-08-23",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SB_TARGETING_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "ad_type": "ALL",
            "targeting_type": "keyword",
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.SbTargetingReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SbKeywordReports.model_validate(data)

    async def SbTargetReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbTargetReports:
        """查询 SB 目标商品投放报告

        ## Docs
        - 新广告 - 报告: [SB广告的投放报告(product)](https://apidoc.lingxing.com/#/docs/newAd/report/listHsaTargetingReport)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SbTargetReports'>`: 返回查询到的 SB 目标商品投放报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 404************,
                    # 广告组ID
                    "ad_group_id": 328************,
                    # 目标商品广告ID
                    "target_id": 562************,
                    # 广告创意类型
                    "creative_type": "all",
                    # 广告花费
                    "cost": 1.49,
                    # 总展示次数
                    "impressions": 5,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 品牌新买家广告订单数
                    "new_to_brand_orders": 1,
                    # 品牌新买家订单占比 [原字段 'new_to_brand_order_percentage']
                    # (品牌新买家广告订单数 / 广告订单数 x 100%)
                    "new_to_brand_order_pct": 100.0,
                    # 品牌新买家订单转化率
                    # (品牌新买家广告订单数 / 总点击次数 x 100%)
                    "new_to_brand_order_rate": 100.0,
                    # 广告成交商品件数
                    "units": 1,
                    # 直接广告成交商品件数 [原字段 'same_units']
                    "direct_units": 1,
                    # 品牌新买家成交商品件数
                    "new_to_brand_units": 1,
                    # 广告销售额
                    "sales": 35.0,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 35.0,
                    # 品牌新买家销售额
                    "new_to_brand_sales": 35.0,
                    # 报告日期
                    "report_date": "2025-08-23",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SB_TARGETING_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "ad_type": "ALL",
            "targeting_type": "product",
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.SbTargetingReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SbTargetReports.model_validate(data)

    async def SbTargetingHourData(
        self,
        report_date: str | datetime.date | datetime.datetime,
        campaign_id: int,
    ) -> schema.SbTargetingHourData:
        """查询 SB 目标关键词或商品投放小时数据

        ## Docs
        - 新广告 - 报告: [SB投放小时数据](https://apidoc.lingxing.com/#/docs/newAd/report/sbTargetHourData)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param campaign_id `<'int'>`: 广告活动ID, 参数来源 `SbCampaign.campaign_id`
        :returns `<'SbTargetingHourData'>`: 返回查询到的 SB 目标关键词或商品投放小时数据结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 439************,
                    # 广告组ID [原字段 'group_id']
                    "ad_group_id": 325************,
                    # 目标定位ID (keyword_id 或 target_id)
                    "targeting_id": 341************,
                    # 目标定位文本 [原字段 'targeting']
                    "targeting_text": "+pixma",
                    # 广告花费
                    "cost": 1.45,
                    # 总展示次数
                    "impressions": 0,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 广告成交商品件数
                    "units": 2,
                    # 广告销售额
                    "sales": 59.76,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 59.76,
                    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                    "ctr": 0.0,
                    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                    "cvr": 1.0,
                    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                    "cpc": 1.45,
                    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                    "cpa": 1.45,
                    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                    "acos": 0.0243,
                    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                    "roas": 41.21,
                    # 数据所属小时 (0-23)
                    "hour": 18,
                    # 报告日期
                    "report_date": "2025-08-25",
                },
                ...
            ],
        }
        ```
        """
        url = route.SB_TARGETING_HOUR_DATA
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "campaign_id": campaign_id,
            "agg_dimension": "target",
        }
        try:
            p = param.AdHourData.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SbTargetingHourData.model_validate(data)

    async def SbQueryWordReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbQueryWordReports:
        """查询 SB 用户搜索词报告

        ## Docs
        - 新广告 - 报告: [SB用户搜索词报表](https://apidoc.lingxing.com/#/docs/newAd/report/hsaQueryWordReports)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SbQueryWordReports'>`: 返回查询到的 SB 用户搜索词报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 451************,
                    # 广告组ID
                    "ad_group_id": 329************,
                    # 关键词ID [原字段 'target_id']
                    "keyword_id": 431************,
                    # 关键词文本 [原字段 'target_text']
                    "keyword_text": "+hp +envy +5660 +ink",
                    # 用户使用搜索词 [原字段 'query']
                    "query_text": "hp envy 5660 ink",
                    # 关键词匹配类型
                    "match_type": "broad",
                    # 广告花费
                    "cost": 0.62,
                    # 总展示次数
                    "impressions": 3,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 广告销售额
                    "sales": 39.89,
                    # 视频广告播放25%次数 [原字段 'video_first_quartile_views']
                    "video_25pct_views": 0,
                    # 视频广告播放50%次数 [原字段 'video_midpoint_views']
                    "video_50pct_views": 0,
                    # 视频广告播放75%次数 [原字段 'video_third_quartile_views']
                    "video_75pct_views": 0,
                    # 视频广告播放100%次数 [原字段 'video_complete_views']
                    "video_100pct_views": 0,
                    # 视频广告播放5秒次数 [原字段 'video_5_second_views']
                    "video_5sec_views": 0,
                    # 视频广告播放5秒观看率 [原字段 'video_5_second_view_rate']
                    "video_5sec_view_rate": 0.0,
                    # 视频广告静音取消次数 [原字段 'video_unmutes']
                    "video_unmutes": 0,
                    # 报告日期
                    "report_date": "2025-08-24",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SB_QUERY_WORD_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "targeting_type": "keyword",
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.SbQueryWordReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SbQueryWordReports.model_validate(data)

    async def SbAsinAttributionReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbAsinAttributionReports:
        """查询 SB 目标商品归因报告

        ## Docs
        - 新广告 - 报告: [SB广告归因于广告的购买报告](https://apidoc.lingxing.com/#/docs/newAd/report/hsaPurchasedAsinReports)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SbAsinAttributionReports'>`: 返回查询到的 SB 目标商品归因报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 372************,
                    # 广告活动名称
                    "campaign_name": "SB-GEXG",
                    # 广告组ID
                    "ad_group_id": 391************,
                    # 广告组名称
                    "ad_group_name": "广告组 - 5/4/2025 00:39:02.466",
                    # 归因类型
                    "attribution_type": "Promoted",
                    # 商品ASIN
                    "asin": "B0F*******",
                    # 广告14天订单数 [原字段 'orders14d']
                    "orders_14d": 12,
                    # 品牌新买家14天订单数 [原字段 'new_to_brand_purchases14d']
                    "new_to_brand_orders_14d": 12,
                    # 品牌新买家订单占比14天 [原字段 'new_to_brand_purchases_percentage14d']
                    # (品牌新买家14天订单数 / 广告14天订单数 x 100%)
                    "new_to_brand_order_pct_14d": 100.0,
                    # 广告14天成交商品件数 [原字段 'units_sold14d']
                    "units_14d": 12,
                    # 品牌新买家14天成交商品件数 [原字段 'new_to_brand_units_sold14d']
                    "new_to_brand_units_14d": 12,
                    # 品牌新买家成交商品件数占比14天 [原字段 'new_to_brand_units_sold_percentage14d']
                    # (品牌新买家14天成交商品件数 / 广告14天成交商品件数 x 100%)
                    "new_to_brand_units_pct_14d": 100.0,
                    # 广告14天销售
                    "sales_14d": 430.8,
                    # 品牌新买家14天销售额 [原字段 'new_to_brand_sales14d']
                    "new_to_brand_sales_14d": 430.8,
                    # 品牌新买家销售额占比14天 [原字段 'new_to_brand_sales_percentage14d']
                    # (品牌新买家14天销售额 / 广告14天销售 x 100%)
                    "new_to_brand_sales_pct_14d": 100.0,
                    # 报告日期
                    "report_date": "2025-08-24",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SB_ASIN_ATTRIBUTION_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SbAsinAttributionReports.model_validate(data)

    async def SbCostAllocationReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbCostAllocationReports:
        """查询 SB 广告费用分摊报告

        ## Docs
        - 新广告 - 报告: [SB分摊](https://apidoc.lingxing.com/#/docs/newAd/baseData/newadsbDivideAsinReports)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SbCostAllocationReports'>`: 返回查询到的 SB 广告费用分摊报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 536************,
                    # 广告组ID
                    "ad_group_id": 328************,
                    # 部门ID
                    "department_id": 901***************,
                    # 设置分摊的事务ID, 用于追踪具体的分摊规则 (UUID) [原字段 'transaction_uuid']
                    "allocation_rule_id": "",
                    # 分摊产品的MD5值 (ad_group_id, asin, sku) [原字段 'divide_asin_md5']
                    "allocation_asin_id": "9647c9e*************************",
                    # 分摊比率 (0.0 - 1.0) [原字段 'percent']
                    "allocation_ratio": 0.5,
                    # 商品ASIN
                    "asin": "B0D*******",
                    # 商品SKU [原字段 'sku']
                    "msku": "SKU*********",
                    # 分摊后的广告花费 [原字段 'spends']
                    "costs": 13.395,
                    # 分摊后的展示次数
                    "impressions": 834.5,
                    # 分摊后的点击次数
                    "clicks": 5.5,
                    # 分摊后的广告订单数
                    "orders": 1.5,
                    # 分摊后的直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1.5,
                    # 分摊后的广告成交商品件数 [原字段 'units_sold']
                    "units": 1.5,
                    # 分摊后的直接广告成交商品件数 [原字段 'same_units_sold']
                    "direct_units": 1.5,
                    # 分摊后的广告销售额
                    "sales": 89.835,
                    # 分摊后的直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 89.835,
                    # 报告日期
                    "report_date": "2025-08-25",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SB_COST_ALLOCATION_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "profile_id": profile_id,
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SbCostAllocationReports.model_validate(data)

    # . 报告 - Sponsored Display
    async def SdCampaignReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SdCampaignReports:
        """查询 SD 广告活动报告

        ## Docs
        - 新广告 - 报告: [SD广告活动报表](https://apidoc.lingxing.com/#/docs/newAd/report/sdCampaignReports)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SdCampaignReports'>`: 返回查询到的 SD 广告活动报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 289************,
                    # 投放策略
                    "tactic": "T00030",
                    # 广告花费
                    "cost": 2.87,
                    # 总展示次数
                    "impressions": 405,
                    # 可见展示次数 [原字段 'view_impressions']
                    "viewable_impressions": 0,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 广告成交商品件数
                    "units": 1,
                    # 广告销售额
                    "sales": 29.98,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 29.98,
                    # 报告日期
                    "report_date": "2025-06-28",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SD_CAMPAIGN_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SdCampaignReports.model_validate(data)

    async def SdCampaignHourData(
        self,
        report_date: str | datetime.date | datetime.datetime,
        campaign_id: int,
    ) -> schema.SdCampaignHourData:
        """查询 SD 广告活动小时数据

        ## Docs
        - 新广告 - 报告: [SD广告活动小时数据](https://apidoc.lingxing.com/#/docs/newAd/report/sdCampaignHourData)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param campaign_id `<'int'>`: 广告活动ID, 参数来源 `SdCampaign.campaign_id`
        :returns `<'SdCampaignHourData'>`: 返回查询到的 SD 广告活动小时数据结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 439************,
                    # 广告花费
                    "cost": 1.45,
                    # 总展示次数
                    "impressions": 0,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 广告成交商品件数
                    "units": 2,
                    # 广告销售额
                    "sales": 59.76,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 59.76,
                    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                    "ctr": 0.0,
                    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                    "cvr": 1.0,
                    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                    "cpc": 1.45,
                    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                    "cpa": 1.45,
                    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                    "acos": 0.0243,
                    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                    "roas": 41.21,
                    # 数据所属小时 (0-23)
                    "hour": 18,
                    # 报告日期
                    "report_date": "2025-08-25",
                },
                ...
            ],
        }
        ```
        """
        url = route.SD_CAMPAIGN_HOUR_DATA
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "campaign_id": campaign_id,
        }
        try:
            p = param.AdHourData.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SdCampaignHourData.model_validate(data)

    async def SdAdGroupReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SdAdGroupReports:
        """查询 SD 广告组报告

        ## Docs
        - 新广告 - 报告: [SD广告组报表](https://apidoc.lingxing.com/#/docs/newAd/report/sdAdGroupReports)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SdAdGroupReports'>`: 返回查询到的 SD 广告组报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 289************,
                    # 广告组ID
                    "ad_group_id": 551************,
                    # 投放策略
                    "tactic": "T00030",
                    # 广告花费
                    "cost": 2.87,
                    # 总展示次数
                    "impressions": 405,
                    # 可见展示次数 [原字段 'view_impressions']
                    "viewable_impressions": 0,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 广告成交商品件数
                    "units": 1,
                    # 广告销售额
                    "sales": 29.98,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 29.98,
                    # 报告日期
                    "report_date": "2025-06-28",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SD_AD_GROUP_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SdAdGroupReports.model_validate(data)

    async def SdAdGroupHourData(
        self,
        report_date: str | datetime.date | datetime.datetime,
        campaign_id: int,
    ) -> schema.SdAdGroupHourData:
        """查询 SD 广告组小时数据

        ## Docs
        - 新广告 - 报告: [SD广告组小时数据](https://apidoc.lingxing.com/#/docs/newAd/report/sdAdGroupHourData)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param campaign_id `<'int'>`: 广告活动ID, 参数来源 `SdCampaign.campaign_id`
        :returns `<'SdAdGroupHourData'>`: 返回查询到的 SD 广告组小时数据结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 439************,
                    # 广告组ID [原字段 'group_id']
                    "ad_group_id": 325************,
                    # 广告花费
                    "cost": 1.45,
                    # 总展示次数
                    "impressions": 0,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 广告成交商品件数
                    "units": 2,
                    # 广告销售额
                    "sales": 59.76,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 59.76,
                    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                    "ctr": 0.0,
                    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                    "cvr": 1.0,
                    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                    "cpc": 1.45,
                    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                    "cpa": 1.45,
                    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                    "acos": 0.0243,
                    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                    "roas": 41.21,
                    # 数据所属小时 (0-23)
                    "hour": 18,
                    # 报告日期
                    "report_date": "2025-08-25",
                },
                ...
            ],
        }
        ```
        """
        url = route.SD_AD_GROUP_HOUR_DATA
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "campaign_id": campaign_id,
        }
        try:
            p = param.AdHourData.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SdAdGroupHourData.model_validate(data)

    async def SdProductReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SdProductReports:
        """查询 SD 商品广告报告

        ## Docs
        - 新广告 - 报告: [SD广告商品报表](https://apidoc.lingxing.com/#/docs/newAd/report/sdProductAdReports)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SdProductReports'>`: 返回查询到的 SD 商品广告报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 289************,
                    # 广告组ID
                    "ad_group_id": 551************,
                    # 商品广告ID
                    "ad_id": 364************,
                    # 投放策略
                    "tactic": "T00030",
                    # 商品ASIN
                    "asin": "B0D*******",
                    # 亚马逊SKU [原字段 'sku']
                    "msku": "SKU********",
                    # 广告花费
                    "cost": 2.87,
                    # 总展示次数
                    "impressions": 405,
                    # 可见展示次数 [原字段 'view_impressions']
                    "viewable_impressions": 0,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 广告成交商品件数
                    "units": 1,
                    # 广告销售额
                    "sales": 29.98,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 29.98,
                    # 报告日期
                    "report_date": "2025-06-28",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SD_PRODUCT_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SdProductReports.model_validate(data)

    async def SdProductHourData(
        self,
        report_date: str | datetime.date | datetime.datetime,
        campaign_id: int,
    ) -> schema.SdProductHourData:
        """查询 SD 商品广告小时数据

        ## Docs
        - 新广告 - 报告: [SD广告小时数据(ad)](https://apidoc.lingxing.com/#/docs/newAd/report/sdAdvertiseHourData)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param campaign_id `<'int'>`: 广告活动ID, 参数来源 `SdCampaign.campaign_id`
        :returns `<'SdProductHourData'>`: 返回查询到的 SD 商品广告小时数据结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 439************,
                    # 广告组ID [原字段 'group_id']
                    "ad_group_id": 325************,
                    # 商品广告ID
                    "ad_id": 364************,
                    # 商品ASIN
                    "asin": "B0X*******
                    # 亚马逊SKU
                    "msku": "SKU********",
                    # 广告花费
                    "cost": 1.45,
                    # 总展示次数
                    "impressions": 0,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 广告成交商品件数
                    "units": 2,
                    # 广告销售额
                    "sales": 59.76,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 59.76,
                    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                    "ctr": 0.0,
                    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                    "cvr": 1.0,
                    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                    "cpc": 1.45,
                    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                    "cpa": 1.45,
                    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                    "acos": 0.0243,
                    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                    "roas": 41.21,
                    # 数据所属小时 (0-23)
                    "hour": 18,
                    # 报告日期
                    "report_date": "2025-08-25",
                },
                ...
            ],
        }
        ```
        """
        url = route.SD_PRODUCT_HOUR_DATA
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "campaign_id": campaign_id,
            "agg_dimension": "ad",
        }
        try:
            p = param.AdHourData.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SdProductHourData.model_validate(data)

    async def SdTargetReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SdTargetReports:
        """查询 SD 目标商品投放报告

        ## Docs
        - 新广告 - 报告: [SD商品定位报表](https://apidoc.lingxing.com/#/docs/newAd/report/sdTargetReports)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SdTargetReports'>`: 返回查询到的 SD 目标商品投放报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 289************,
                    # 广告组ID
                    "ad_group_id": 551************,
                    # 目标商品广告ID
                    "target_id": 542************,
                    # 目标商品文本 [原字段 'targeting_expression']
                    "target_text": 'asin="B0F*******"',
                    # 目标定位类型 [原字段 'targeting_type']
                    "expression_type": "",
                    # 目标定位表达式 (JSON 字符串) [原字段 'targeting_text']
                    "expression": '"[{\\"type\\": \\"asinSameAs\\", \\"value\\": \\"B0F*******\\"}]"',
                    # 投放策略
                    "tactic": "T00030",
                    # 广告花费
                    "cost": 2.87,
                    # 总展示次数
                    "impressions": 144,
                    # 可见展示次数 [原字段 'view_impressions']
                    "viewable_impressions": 0,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 广告成交商品件数
                    "units": 1,
                    # 广告销售额
                    "sales": 29.98,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 29.98,
                    # 报告日期
                    "report_date": "2025-06-28",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SD_TARGET_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SdTargetReports.model_validate(data)

    async def SdTargetHourData(
        self,
        report_date: str | datetime.date | datetime.datetime,
        campaign_id: int,
    ) -> schema.SdTargetHourData:
        """查询 SD 目标商品投放小时数据

        ## Docs
        - 新广告 - 报告: [SD投放小时数据(both_ad_target)](https://apidoc.lingxing.com/#/docs/newAd/report/sdTargetHourData)

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param campaign_id `<'int'>`: 广告活动ID, 参数来源 `SdCampaign.campaign_id`
        :returns `<'SdTargetHourData'>`: 返回查询到的 SD 目标商品投放小时数据结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 439************,
                    # 广告组ID [原字段 'group_id']
                    "ad_group_id": 325************,
                    # 商品广告ID
                    "ad_id": 364************,
                    # 目标商品广告ID [原字段 'targeting_id']
                    "target_id": 542************,
                    # 目标定位文本 [原字段 'targeting']
                    "target_text": 'asin="B0F*******"',
                    # 商品ASIN
                    "asin": "B0X*******
                    # 亚马逊SKU
                    "msku": "SKU********",
                    # 广告花费
                    "cost": 1.45,
                    # 总展示次数
                    "impressions": 0,
                    # 总点击次数
                    "clicks": 1,
                    # 广告订单数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 广告成交商品件数
                    "units": 2,
                    # 广告销售额
                    "sales": 59.76,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 59.76,
                    # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                    "ctr": 0.0,
                    # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                    "cvr": 1.0,
                    # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                    "cpc": 1.45,
                    # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                    "cpa": 1.45,
                    # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                    "acos": 0.0243,
                    # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                    "roas": 41.21,
                    # 数据所属小时 (0-23)
                    "hour": 18,
                    # 报告日期
                    "report_date": "2025-08-25",
                },
                ...
            ],
        }
        ```
        """
        url = route.SD_TARGET_HOUR_DATA
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "campaign_id": campaign_id,
            "agg_dimension": "both_ad_target",
        }
        try:
            p = param.AdHourData.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SdTargetHourData.model_validate(data)

    async def SdMatchedTargetReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SdMatchedTargetReports:
        """查询 SD 匹配的目标商品投放报告

        ## Docs
        - 新广告 - 报告: [SD匹配的目标报表](https://apidoc.lingxing.com/#/docs/newAd/report/sdMatchTargetReports)

        ## Notice
        此报告展示 SD 广告在哪些 ASIN 的 Listing 页面展示井被点击过, 但不同于`'目标商品投放报告'`,
        这份报告只统计显示到 Listing 页面并有点击的数据, 不包括显示到其他位置的和在 Lisitng 贡面有显示但无点击的数据

        :param report_date `<'str/date/datetime'>`: 报告日期
        :param sid `<'int'>`: 领星店铺ID
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param next_token `<'str/None'>`: 分页游标, 上次分页结果中的 `next_token`,
            第一分页无需填写, 当 next_token 和 offset 同时传入时以 next_token 为主, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'SdMatchedTargetReports'>`: 返回查询到的 SD 匹配的目标商品投放报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告活动ID
                    "campaign_id": 289************,
                    # 广告组ID
                    "ad_group_id": 551************,
                    # 目标商品广告ID
                    "target_id": 542************,
                    # 目标定位表达式 (JSON 字符串) [原字段 'target_text']
                    "expression": '"[{\\"type\\": \\"asinSameAs\\", \\"value\\": \\"B0F*******\\"}]"',
                    # 匹配的目标商品 (ASIN)
                    "matched_target": "B0F*******",
                    # 货币代码 [原字段 'currency']
                    "currency_code": "",
                    # 广告花费
                    "cost": 2.87,
                    # 广告花费
                    "impressions": 141,
                    # 可见展示次数 [原字段 'view_impressions']
                    "viewable_impressions": 0,
                    # 总点击次数
                    "clicks": 1,
                    # 总点击次数
                    "orders": 1,
                    # 直接广告订单数 [原字段 'same_orders']
                    "direct_orders": 1,
                    # 品牌新买家广告订单数
                    "new_to_brand_orders": 0,
                    # 广告成交商品件数
                    "units": 1,
                    # 品牌新买家成交商品件数
                    "new_to_brand_units": 0,
                    # 广告销售额
                    "sales": 29.98,
                    # 直接广告销售额 [原字段 'same_sales']
                    "direct_sales": 29.98,
                    # 品牌新买家销售额
                    "new_to_brand_sales": 0.0,
                    # 报告日期
                    "report_date": "2025-06-28",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.SD_MATCHED_TARGET_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "show_detail": 0,
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SdMatchedTargetReports.model_validate(data)

    # . 报告 - Demand-Side Platform (DSP)
    async def DspReports(
        self,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        profile_id: int,
        *,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.DspReports:
        """查询 DSP 报告

        ## Docs
        - 新广告 - 报告: [查询DSP报告列表-订单](https://apidoc.lingxing.com/#/docs/newAd/report/dspReportOrderList)

        :param start_date `<'str/date/datetime'>`: 报告开始日期
        :param end_date `<'str/date/datetime'>`: 报告结束日期
        :param profile_id `<'int'>`: 亚马逊店铺ID (广告帐号ID), 参数来源 `AdsProfiles.profile_id`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 20)
        :returns `<'DspReports'>`: 返回查询到的 DSP 报告结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 亚马逊店铺ID (广告帐号ID)
                    "profile_id": 494************,
                    # 广告主ID
                    "advertiser_id": 214************,
                    # 广告主名称
                    "advertiser_name": "Seller",
                    # 订单ID
                    "order_id": 584************,
                    # 订单名称
                    "order_name": "Link-In",
                    # 订单开始时间
                    "order_start_date": "2022-09-13 00:00:00",
                    # 订单结束时间
                    "order_end_date": "2023-01-01 00:00:00",
                    # 预算 [原字段 'order_budget']
                    "budget": 2715.00,
                    # 广告花费 [原字段 'spends']
                    "costs": 26.88,
                    # 总展示次数
                    "impressions": 4053,
                    # 可见展示次数
                    "viewable_impressions": 2176,
                    # 总点击次数
                    "clicks": 31,
                    # 商品详情页浏览次数 [原字段 'dpv']
                    "page_views": 51,
                    # 加购次数 [原字段 'total_add_to_cart']
                    "add_to_cart_count": 22,
                    # 订单数
                    "orders": 10,
                    # 成交商品件数 [原字段 'ad_units']
                    "units": 11,
                    # 销售额
                    "sales": 330.59,
                    # 货币代码 [原字段 'order_currency']
                    "currency_code": "USD",
                },
                ...
            ],
            # 分页游标
            "next_token": "MjgxNTExNTQ0MTc4ODM1",
        }
        ```
        """
        url = route.DSP_REPORTS
        # 解析并验证参数
        args = {
            "start_date": start_date,
            "end_date": end_date,
            "profile_id": profile_id,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.DspReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.DspReports.model_validate(data)

    # 报表下载 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    async def DownloadAbaReport(
        self,
        country: str,
        start_date: str | datetime.date | datetime.datetime,
    ) -> schema.DownloadAbaReport:
        """生成亚马逊 ABA 搜索词报告的下载连接 (周纬度)

        ## Docs
        - 新广告 - 报表下载: [ABA搜索词报告-按周维度](https://apidoc.lingxing.com/#/docs/newAd/reportDownload/abaReport)

        ## Notice
        - 下载的 ABA 报告为 zip 压缩包 (无后缀), 内包含同名 json 文件 (无后缀)
        - 压缩包内的 json 报告文件普遍很大, 建议使用流式读数据内容

        :param country `<'str'>`: 国家代码
        :param start_date `<'str/date/datetime'>`: 报告开始日期, 会自动调整为周日,
            下载的报告会包含此日期到当前为止所有的 ABA 数据, 一般数据量很大
        :returns `<'DownloadAbaReport'>`: 返回生成的 ABA 报告下载连接
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "操作成功",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 1,
            # 总数据量
            "total_count": 1,
            # 响应数据
            "data": {
                # 国家代码 [原字段 'country']
                "country_code": "US",
                # 报告周期
                "report_period": "WEEK",
                # 报告开始日期 [原字段 'data_start_time']
                "start_date": "2025-08-03",
                # 下载链接
                "url": "https://dg-reportserviceprd-1254213275.cos.ap-guangzhou.myqcloud.com/****",
            },
        }
        ```
        """
        url = route.DOWNLOAD_ABA_REPORT
        # 解析并验证参数
        args = {
            "country": country,
            "start_date": start_date,
        }
        try:
            p = param.DownloadAbaReport.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.DownloadAbaReport.model_validate(data)

    # 操作日志 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    async def AdsOperationLogs(
        self,
        sid: int,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        ad_type: AD_TYPE,
        operation_target: AD_OPERATION_TARGET,
        *,
        log_source: LOG_SOURCE = "all",
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.AdsOperationLogs:
        """查询广告操作日志

        ## Docs
        - 新广告: [操作日志(新）](https://apidoc.lingxing.com/#/docs/newAd/apiLogStandard)

        :param sid `<'int'>`: 领星店铺ID
        :param start_date `<'str/date/datetime'>`: 操作日志开始日期, 日期间隔不能超过1个月
        :param end_date `<'str/date/datetime'>`: 操作日志结束日期, 日期间隔不能超过1个月
        :param ad_type `<'str'>`: 广告类型, 可选值: `"SP"`, `"SB"`, `"SD"`
        :param operation_target `<'str'>`: 操作对象, 可选值:

            - `"campaigns"` (广告活动)
            - `"adGroups"` (广告组)
            - `"productAds"` (广告)
            - `"keywords"` (关键词)
            - `"negativeKeywords"` (否定关键词)
            - `"targets"` (商品投放)
            - `"negativeTargets"` (否定商品投放)
            - `"profiles"` (预算设置)

        :param log_source `<'str'>`: 日志来源, 默认值 `"all"`, 可选值:

            - `"erp"` (仅领星ERP的广告调整日志)
            - `"amazon"` (仅亚马逊后台的广告调整日志)
            - `"all"` (全部)

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'AdsOperationLogs'>`: 返回查询到的广告操作日志结果
        ```python
        {
            # 亚马逊店铺ID (广告帐号ID)
            "profile_id": 494************,
            # 广告活动ID
            "campaign_id": 326************,
            # 广告活动名称
            "campaign_name": "V9IP",
            # 广告组ID
            "ad_group_id": 314************,
            # 广告组名称
            "ad_group_name": "广告组 - 8/10/2025 00:44:01.141",
            # 广告对象ID [原字段 'object_id']
            "ad_object_id": 314************,
            # 广告对象名称 [原字段 'object_name']
            "ad_object_name": "广告组 - 8/10/2025 00:44:01.141",
            # 广告类型 [原字段 'sponsored_type']
            "ad_type": "sp",
            # 操作用户ID [原字段 'user_id']
            "operator_id": 0,
            # 操作用户名称 [原字段 'user_name']
            "operator_name": "亚马逊日志",
            # 操作对象 [原字段 'operate_type']
            "operation_target": "adGroups",
            # 操作类型 [原字段 'change_type']
            "operation_type": "create",
            # 操作来源 [原字段 'function_name']
            "operation_source": "history",
            # 操作时间 [原字段 'operate_time']
            "operation_time": "2025-08-09 09:59:08",
            # 操作前列表 [原字段 'operate_before']
            "before": [
                {
                    # 操作编码
                    "code": "STATUS",
                    # 操作值
                    "value": "null",
                },
                ...
            ],
            # 操作后列表 [原字段 'operate_after']
            "after": [
                {
                    # 操作编码
                    "code": "STATUS",
                    # 操作值
                    "value": "CREATED"
                },
                ...
            ],
        }
        ```
        """
        url = route.ADS_OPERATION_LOGS
        # 解析并验证参数
        args = {
            "sid": sid,
            "start_date": start_date,
            "end_date": end_date,
            "ad_type": ad_type,
            "operation_target": operation_target,
            "log_source": log_source,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdsOperationLogs.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.AdsOperationLogs.model_validate(data)
