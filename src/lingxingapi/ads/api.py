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
        """查询广告账号列表。

        ## Docs
        领星接口文档: 新广告 - 基础数据.[查询广告账号列表](https://apidoc.lingxing.com/#/docs/newAd/baseData/dspAccountList)

        Args:
            profile_type (AD_PROFILE_TYPE): 广告账号类型，默认 "seller"；类型提示列出 "dsp"、"seller"、"vendor"。
            offset (int | None): 分页偏移量，默认 None；为 None 时SDK省略请求体中的 offset。
            length (int | None): 分页长度，默认 None；为 None 时SDK省略请求体中的 length。

        Returns:
            ads.schema.AdProfiles: 广告账号的分页查询结果。

        Examples:
            查询 seller 第一页并查看返回数据。

            .. code-block:: python

                result = await client.ads.AdProfiles(profile_type="seller", offset=0, length=20)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": 'success',
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": '00000000000000000000000000000000.0000000000031',
                    # 响应时间
                    "response_time": '2001-05-07 06:36:00',
                    # 响应数据量
                    "response_count": 20,
                    # 总数据量
                    "total_count": 240,
                    # 响应数据
                    "data": [
                        {
                            # 领星店铺ID
                            "sid": 10105,
                            # 领星店铺名称 [原字段 'name']
                            "seller_name": '广告账号名',
                            # 店铺国家代码
                            "country_code": 'NL',
                            # 店铺货币代码
                            "currency_code": 'EUR',
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 90000000000001,
                            # 广告帐号类型 [原字段 'type']
                            "profile_type": 'seller',
                            # 广告帐号状态 [原字段 'status']
                            # (-1: 删除, 0: 停用, 1: 正常, 2: 异常)
                            "profile_status": 1,
                        },
                        ...
                    ],
                }
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
        sid: int | None = None,
        profile_id: int | None = None,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.Portfolios:
        """查询广告组合。

        ## Docs
        领星接口文档: 新广告 - 基础数据.[广告组合](https://apidoc.lingxing.com/#/docs/newAd/baseData/portfolios)

        Args:
            sid (int | None): 领星店铺ID，默认 None。sid 与 profile_id 至少提供一项；同时提供时，以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            state (str | None): 广告组合状态，可传 enabled、paused、archived；默认 None，不输出该请求参数。查询结果可能为空。
            next_token (str | None): 上一页返回的分页游标，默认 None；与 offset 同时提供时按游标定位。
            offset (int | None): 按记录数计算的非负分页偏移量，默认 None；None 省略请求键，0 保留。
            length (int | None): 非负分页长度，默认 None；None 省略请求键，由服务端决定默认分页长度。

        Returns:
            ads.schema.Portfolios: 查询到的广告组合及当前页游标、总数量。

        Examples:
            指定广告账号、状态和分页范围查询广告组合并查看返回数据。

            .. code-block:: python

                result = await client.ads.Portfolios(profile_id=90000000000003, state="enabled", offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    'code': 0,
                    # 提示信息
                    'message': '操作成功',
                    # 错误信息
                    'errors': [],
                    # 请求ID
                    'request_id': '00000000-0000-0000-0000-000000000010',
                    # 响应时间
                    'response_time': '2001-05-07 06:21:00',
                    # 响应数据量
                    'response_count': 2,
                    # 总数据量
                    'total_count': 56,
                    # 响应数据
                    'data': [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            'profile_id': 90000000000003,
                            # 广告组合ID
                            'portfolio_id': 800000000004,
                            # 广告组合名称
                            'portfolio_name': 'A000000AAA-000 0A0A 组',
                            # 广告预算 (JSON 字符串)
                            'budget': '{"amount": 1.0, "policy": "dateRange", "startDate": "20260313", "currencyCode": "GBP"}',
                            # 当前是否在预算范围内 (0: 超出预算, 1: 在预算内)
                            'in_budget': 0,
                            # 广告状态
                            'state': 'enabled',
                            # 服务状态 [原字段 'serving_status']
                            'status': 'PORTFOLIO_OUT_OF_BUDGET',
                            # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                            'create_time_ts': 1755676941815,
                            # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                            'update_time_ts': 1773498441693,
                        },
                        ...,
                    ],
                    # 分页游标
                    'next_token': 'MTAwMDAwMDAwMDAwMDE=',
                }
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
        sid: int | None = None,
        profile_id: int | None = None,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpCampaigns:
        """查询 SP 广告活动。

        ## Docs
        领星接口文档: 新广告 - 基础数据.[SP广告活动](https://apidoc.lingxing.com/#/docs/newAd/baseData/spCampaigns)

        Args:
            sid (int | None): 领星店铺ID，默认 None。sid 与 profile_id 至少提供一项；同时提供时，以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            state (str | None): 广告活动状态，可传 enabled（启用）、paused（暂停）、archived（归档）；默认 None，省略请求参数并查询所有状态。
            next_token (str | None): 上一页返回的分页游标，默认 None，首次查询无需提供；与 offset 同时提供时按游标定位。
            offset (int | None): 按记录数计算的非负分页偏移量，默认 None；None 省略请求键，由服务端采用默认值 0，显式传入 0 时保留。
            length (int | None): 非负分页长度，默认 None；None 省略请求键，由服务端采用默认值 15。

        Returns:
            ads.schema.SpCampaigns: 查询到的 SP 广告活动及当前页游标、总数量；返回记录不包含 tags 字段。

        Examples:
            指定广告账号、状态和分页范围查询 SP 广告活动并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpCampaigns(profile_id=90000000000003, state="enabled", offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    'code': 0,
                    # 提示信息
                    'message': '操作成功',
                    # 错误信息
                    'errors': [],
                    # 请求ID
                    'request_id': '00000000-0000-0000-0000-00000000001c',
                    # 响应时间
                    'response_time': '2001-05-07 06:21:00',
                    # 响应数据量
                    'response_count': 2,
                    # 总数据量
                    'total_count': 259,
                    # 响应数据
                    'data': [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            'profile_id': 90000000000003,
                            # 广告组合ID
                            'portfolio_id': 80000000000012,
                            # 广告活动ID
                            'campaign_id': 70000000000010,
                            # 广告活动名称 [原字段 'name']
                            'campaign_name': 'AA-000AAA-AAAI',
                            # 广告活动类型
                            'campaign_type': 'sponsoredProducts',
                            # 投放类型
                            'targeting_type': 'manual',
                            # 溢价报价调整 (0: 不调整, 1: 调整)
                            'premium_bid_adjustment': 0,
                            # 每日预算
                            'daily_budget': 6.0,
                            # 时间字符串，格式为 YYYY-MM-DD HH:MM:SS，可为 None [原字段 'lastOverBudgetAt']
                            'last_over_budget_at': '2026-10-12 22:17:35',
                            # 竞价策略 (JSON 字符串)
                            'bidding': '{"strategy": "manual", "adjustments": [{"predicate": "placementRestOfSearch", "percentage": 50}, {"predicate": "placementTop", "percentage": 80}]}',
                            # 开始时间 [原字段 'start_date']
                            'start_time': '2019-11-05 00:00:00',
                            # 结束时间 [原字段 'end_date']
                            'end_time': '',
                            # 广告状态
                            'state': 'enabled',
                            # 服务状态 [原字段 'serving_status']
                            'status': 'CAMPAIGN_STATUS_ENABLED',
                            # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                            'create_time_ts': 1572927171000,
                            # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                            'update_time_ts': 1791674172950,
                        },
                        ...,
                    ],
                    # 分页游标
                    'next_token': 'MTAwMDA2',
                }
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
        sid: int | None = None,
        profile_id: int | None = None,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpAdGroups:
        """查询 SP 广告组。

        ## Docs
        领星接口文档: 新广告 - 基础数据.[SP广告组](https://apidoc.lingxing.com/#/docs/newAd/baseData/spAdGroups)

        Args:
            sid (int | None): 领星店铺ID，默认 None。sid 与 profile_id 至少提供一项；同时提供时，以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            state (str | None): 广告状态，可传 enabled（启用）、paused（暂停）、archived（归档）；默认 None，省略请求参数并查询所有状态。
            next_token (str | None): 上一页返回的分页游标，默认 None，首次查询无需提供；与 offset 同时提供时按游标定位。
            offset (int | None): 按记录数计算的非负分页偏移量，默认 None；None 省略请求键，由服务端采用默认值 0，显式传入 0 时保留。
            length (int | None): 非负分页长度，默认 None；None 省略请求键，由服务端采用默认值 15。

        Returns:
            ads.schema.SpAdGroups: 查询到的 SP 广告组及当前页游标、总数量。

        Examples:
            指定广告账号和分页范围查询并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpAdGroups(profile_id=90000000000004, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    'code': 0,
                    # 提示信息
                    'message': '操作成功',
                    # 错误信息
                    'errors': [],
                    # 请求ID
                    'request_id': '00000000-0000-0000-0000-000000000046',
                    # 响应时间
                    'response_time': '2001-05-07 06:36:00',
                    # 响应数据量
                    'response_count': 2,
                    # 总数据量
                    'total_count': 542,
                    # 响应数据
                    'data': [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            'profile_id': 90000000000004,
                            # 广告活动ID
                            'campaign_id': 700000000000128,
                            # 广告组ID
                            'ad_group_id': 600000000066,
                            # 广告组名称 [原字段 'name']
                            'ad_group_name': 'AA 000 000广告组广合',
                            # 默认竞价
                            'default_bid': 1.13,
                            # 广告组状态
                            'state': 'enabled',
                            # 服务状态 [原字段 'serving_status']
                            'status': 'CAMPAIGN_PAUSED',
                            # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                            'create_time_ts': 1667273890695,
                            # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                            'update_time_ts': 1667273890695,
                        },
                        ...,
                    ],
                    # 分页游标
                    'next_token': 'MTAwMDAwMDAwMDIx',
                }
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
        sid: int | None = None,
        profile_id: int | None = None,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpProducts:
        """查询 SP 广告商品。

        ## Docs
        领星接口文档: 新广告 - 基础数据.[SP广告商品](https://apidoc.lingxing.com/#/docs/newAd/baseData/spProductAds)

        Args:
            sid (int | None): 领星店铺ID，默认 None。sid 与 profile_id 至少提供一项；同时提供时，以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            state (str | None): 广告状态，可传 enabled（启用）、paused（暂停）、archived（归档）；默认 None，省略请求参数并查询所有状态。
            next_token (str | None): 上一页返回的分页游标，默认 None，首次查询无需提供；与 offset 同时提供时按游标定位。
            offset (int | None): 按记录数计算的非负分页偏移量，默认 None；None 省略请求键，由服务端采用默认值 0，显式传入 0 时保留。
            length (int | None): 非负分页长度，默认 None；None 省略请求键，由服务端采用默认值 15。

        Returns:
            ads.schema.SpProducts: 查询到的 SP 广告商品及视频详情及当前页游标、总数量。

        Examples:
            指定广告账号和分页范围查询并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpProducts(profile_id=90000000000004, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    'code': 0,
                    # 提示信息
                    'message': '操作成功',
                    # 错误信息
                    'errors': [],
                    # 请求ID
                    'request_id': '00000000-0000-0000-0000-000000000017',
                    # 响应时间
                    'response_time': '2001-05-07 06:50:00',
                    # 响应数据量
                    'response_count': 2,
                    # 总数据量
                    'total_count': 1157,
                    # 响应数据
                    'data': [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            'profile_id': 90000000000004,
                            # 广告活动ID
                            'campaign_id': 7000000000264,
                            # 广告组ID
                            'ad_group_id': 600000000000026,
                            # 商品广告ID
                            'ad_id': 50000000002,
                            # 商品ASIN
                            'asin': 'A00A0AAAA4',
                            # 亚马逊SKU [原字段 'sku']
                            'msku': '000aaAA 000CY',
                            # 商品广告视频详情
                            'video_details': [
                                {
                                    # 视频素材ID
                                    'asset_id': 'amzn1.assetlibrary.asset1.a0000000aa0a0aa0a0aa00000000a0ac',
                                    # 广告指定的视频素材版本
                                    'asset_version': 'version_v2',
                                    # 视频标题
                                    'headline': 'Aaa Aaaaaab',
                                    # 视频描述
                                    'description': 'Aaaaaaa aaa aaaaaa aa aaaaa aaaaaaa aac.',
                                    # 本地视频素材名称，未匹配素材时为空字符串
                                    'name': '',
                                    # 本地视频素材地址，未匹配素材时为空字符串
                                    'url': '',
                                },
                                ...,
                            ],
                            # 广告状态
                            'state': 'enabled',
                            # 服务状态 [原字段 'serving_status']
                            'status': 'CAMPAIGN_PAUSED',
                            # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                            'create_time_ts': 1599466635000,
                            # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                            'update_time_ts': 1599466635000,
                        },
                        ...,
                    ],
                    # 分页游标
                    'next_token': 'MTAwMDAwMDAwMDI1',
                }
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
        sid: int | None = None,
        profile_id: int | None = None,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpKeywords:
        """查询 SP 关键词。

        ## Docs
        领星接口文档: 新广告 - 基础数据.[SP关键词](https://apidoc.lingxing.com/#/docs/newAd/baseData/spKeywords)

        Args:
            sid (int | None): 领星店铺ID，默认 None。sid 与 profile_id 至少提供一项；同时提供时，以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            state (str | None): 广告状态，可传 enabled（启用）、paused（暂停）、archived（归档）；默认 None，省略请求参数并查询所有状态。
            next_token (str | None): 上一页返回的分页游标，默认 None，首次查询无需提供；与 offset 同时提供时按游标定位。
            offset (int | None): 按记录数计算的非负分页偏移量，默认 None；None 省略请求键，由服务端采用默认值 0，显式传入 0 时保留。
            length (int | None): 非负分页长度，默认 None；None 省略请求键，由服务端采用默认值 15。

        Returns:
            ads.schema.SpKeywords: 查询到的 SP 手动关键词投放及当前页游标、总数量。

        Examples:
            指定广告账号和分页范围查询并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpKeywords(profile_id=90000000000004, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    'code': 0,
                    # 提示信息
                    'message': '操作成功',
                    # 错误信息
                    'errors': [],
                    # 请求ID
                    'request_id': '00000000-0000-0000-0000-000000000053',
                    # 响应时间
                    'response_time': '2001-05-07 07:04:00',
                    # 响应数据量
                    'response_count': 2,
                    # 总数据量
                    'total_count': 16923,
                    # 响应数据
                    'data': [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            'profile_id': 90000000000004,
                            # 广告活动ID
                            'campaign_id': 700000000000097,
                            # 广告组ID
                            'ad_group_id': 60000000000058,
                            # 关键词ID
                            'keyword_id': 4000000008,
                            # 关键词文本
                            'keyword_text': 'aaaa 0000 aaf',
                            # 关键词匹配类型
                            'match_type': 'phrase',
                            # 竞价
                            'bid': 0.5,
                            # 广告状态
                            'state': 'enabled',
                            # 服务状态 [原字段 'serving_status']
                            'status': 'CAMPAIGN_PAUSED',
                            # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                            'create_time_ts': 1583837811000,
                            # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                            'update_time_ts': 1583837811000,
                        },
                        ...,
                    ],
                    # 分页游标
                    'next_token': 'MTAwMDAwMDAzNg==',
                }
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
        sid: int | None = None,
        profile_id: int | None = None,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpTargets:
        """查询 SP 商品定位。

        ## Docs
        领星接口文档: 新广告 - 基础数据.[SP商品定位](https://apidoc.lingxing.com/#/docs/newAd/baseData/spTargets)

        Args:
            sid (int | None): 领星店铺ID，默认 None。sid 与 profile_id 至少提供一项；同时提供时，以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            state (str | None): 广告状态，可传 enabled（启用）、paused（暂停）、archived（归档）；默认 None，省略请求参数并查询所有状态。
            next_token (str | None): 上一页返回的分页游标，默认 None，首次查询无需提供；与 offset 同时提供时按游标定位。
            offset (int | None): 按记录数计算的非负分页偏移量，默认 None；None 省略请求键，由服务端采用默认值 0，显式传入 0 时保留。
            length (int | None): 非负分页长度，默认 None；None 省略请求键，由服务端采用默认值 15。

        Returns:
            ads.schema.SpTargets: 查询到的 SP 自动投放/手动商品投放及当前页游标、总数量。

        Examples:
            指定广告账号和分页范围查询并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpTargets(profile_id=90000000000004, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    'code': 0,
                    # 提示信息
                    'message': '操作成功',
                    # 错误信息
                    'errors': [],
                    # 请求ID
                    'request_id': '00000000-0000-0000-0000-00000000005d',
                    # 响应时间
                    'response_time': '2001-05-07 07:16:00',
                    # 响应数据量
                    'response_count': 2,
                    # 总数据量
                    'total_count': 1510,
                    # 响应数据
                    'data': [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            'profile_id': 90000000000004,
                            # 广告活动ID
                            'campaign_id': 700000000000111,
                            # 广告组ID
                            'ad_group_id': 60000000000255,
                            # 自动投放/手动商品投放ID
                            'target_id': 300000000003,
                            # 自动/手动投放类型
                            'expression_type': 'auto',
                            # 自动投放/手动商品投放表达式 (JSON 字符串)
                            'expression': '[{"type": "queryHighRelMatches"}]',
                            # 自动投放/手动商品投放表达式表达式解析 (JSON 字符串) [原字段 'resolved_expression']
                            'expression_resolved': '[{"type": "queryHighRelMatches"}]',
                            # 竞价
                            'bid': 0.45,
                            # 广告状态
                            'state': 'enabled',
                            # 服务状态 [原字段 'serving_status']
                            'status': 'CAMPAIGN_PAUSED',
                            # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                            'create_time_ts': 1590133144000,
                            # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                            'update_time_ts': 1599470603000,
                        },
                        ...,
                    ],
                    # 分页游标
                    'next_token': 'MTAwMDAwMDAwMDE4',
                }
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
        sid: int | None = None,
        profile_id: int | None = None,
        *,
        campaign_id: int | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpNegativeKeywords:
        """查询 SP 否定关键词。

        ## Docs
        领星接口文档: 新广告 - 基础数据.[SP否定投放](https://apidoc.lingxing.com/#/docs/newAd/baseData/spNegativeTargetsOrKeywords)

        Args:
            sid (int | None): 领星店铺ID，默认 None。sid 与 profile_id 至少提供一项；同时提供时，以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            campaign_id (int | None): 广告活动ID，来源为 SpCampaigns 返回记录的 campaign_id，默认 None；None 省略请求键并查询所有活动。
            next_token (str | None): 上一页返回的分页游标，默认 None，首次查询无需提供；与 offset 同时提供时按游标定位。
            offset (int | None): 按记录数计算的非负分页偏移量，默认 None；None 省略请求键，由服务端采用默认值 0，显式传入 0 时保留。
            length (int | None): 非负分页长度，默认 None；None 省略请求键，由服务端采用默认值 15。

        Returns:
            ads.schema.SpNegativeKeywords: 查询到的 SP 否定关键词及当前页游标、总数量。返回记录不包含 negative_type 字段。

        Examples:
            指定广告账号和分页范围查询并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpNegativeKeywords(profile_id=90000000000004, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    'code': 0,
                    # 提示信息
                    'message': '操作成功',
                    # 错误信息
                    'errors': [],
                    # 请求ID
                    'request_id': '00000000-0000-0000-0000-00000000001f',
                    # 响应时间
                    'response_time': '2001-05-07 07:29:00',
                    # 响应数据量
                    'response_count': 2,
                    # 总数据量
                    'total_count': 576,
                    # 响应数据
                    'data': [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            'profile_id': 90000000000004,
                            # 广告活动ID
                            'campaign_id': 70000000000079,
                            # 广告组ID
                            'ad_group_id': 0,
                            # 否定关键词ID [原字段 'target_id']
                            'negative_keyword_id': 400000000000001,
                            # 否定关键词文本 [原字段 'negative_text']
                            'negative_keyword_text': 'aa 0000  aag',
                            # 否定匹配方式 [原字段 'negative_match_type']
                            'negative_keyword_match_type': 'negativePhrase',
                            # 广告状态
                            'state': 'enabled',
                            # 服务状态 [原字段 'serving_status']
                            'status': 'CAMPAIGN_PAUSED',
                            # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                            'create_time_ts': 1530580497000,
                            # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                            'update_time_ts': 1530580497000,
                        },
                        ...,
                    ],
                    # 分页游标
                    'next_token': 'MTAwMDAxNg==',
                }
        """
        url = route.SP_NEGATIVE_TARGETING
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "target_type": "keyword",
            "campaign_id": campaign_id,
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
        sid: int | None = None,
        profile_id: int | None = None,
        *,
        campaign_id: int | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpNegativeTargets:
        """查询 SP 否定目标。

        ## Docs
        领星接口文档: 新广告 - 基础数据.[SP否定投放](https://apidoc.lingxing.com/#/docs/newAd/baseData/spNegativeTargetsOrKeywords)

        Args:
            sid (int | None): 领星店铺ID，默认 None。sid 与 profile_id 至少提供一项；同时提供时，以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            campaign_id (int | None): 广告活动ID，来源为 SpCampaigns 返回记录的 campaign_id，默认 None；None 省略请求键并查询所有活动。
            next_token (str | None): 上一页返回的分页游标，默认 None，首次查询无需提供；与 offset 同时提供时按游标定位。
            offset (int | None): 按记录数计算的非负分页偏移量，默认 None；None 省略请求键，由服务端采用默认值 0，显式传入 0 时保留。
            length (int | None): 非负分页长度，默认 None；None 省略请求键，由服务端采用默认值 15。

        Returns:
            ads.schema.SpNegativeTargets: 查询到的 SP 否定目标及当前页游标、总数量。返回记录不包含 negative_match_type 字段。

        Examples:
            指定广告账号和分页范围查询并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpNegativeTargets(profile_id=90000000000004, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    'code': 0,
                    # 提示信息
                    'message': '操作成功',
                    # 错误信息
                    'errors': [],
                    # 请求ID
                    'request_id': '00000000-0000-0000-0000-00000000005b',
                    # 响应时间
                    'response_time': '2001-05-07 07:40:00',
                    # 响应数据量
                    'response_count': 2,
                    # 总数据量
                    'total_count': 988,
                    # 响应数据
                    'data': [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            'profile_id': 90000000000004,
                            # 广告活动ID
                            'campaign_id': 700000000000087,
                            # 广告组ID
                            'ad_group_id': 600000000000031,
                            # 否定目标ID [原字段 'target_id']
                            'negative_target_id': 30000000000002,
                            # 否定目标文本 [原字段 'negative_text']
                            'negative_target_text': 'Aaaaaab',
                            # 否定目标类型 [原字段 'negative_type']
                            'negative_target_match_type': 'negativeBrand',
                            # 广告状态
                            'state': 'enabled',
                            # 服务状态 [原字段 'serving_status']
                            'status': 'CAMPAIGN_PAUSED',
                            # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                            'create_time_ts': 1573797409000,
                            # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                            'update_time_ts': 1573797409000,
                        },
                        ...,
                    ],
                    # 分页游标
                    'next_token': 'MTAwMDMz',
                }
        """
        url = route.SP_NEGATIVE_TARGETING
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "target_type": "target",
            "campaign_id": campaign_id,
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
        sid: int | None = None,
        profile_id: int | None = None,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbCampaigns:
        """查询SB 广告活动。

        ## Docs
        领星接口文档: [新广告 - 基础数据 - SB广告活动](https://apidoc.lingxing.com/new/api-docs/newAd/baseData/hsaCampaigns/)

        Args:
            sid (int | None): 领星店铺ID，默认 None。sid 与 profile_id 至少提供一项；同时提供时，以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            state (str | None): enabled、paused或archived；默认None，省略并查询所有状态。
            next_token (str | None): 上次响应的分页游标；默认None；同时传offset时以游标定位。
            offset (int | None): 非负记录偏移量，默认None，由服务端采用0；显式0保留。
            length (int | None): 非负分页长度，默认None，由服务端采用15。

        Returns:
            ads.schema.SbCampaigns: SB 广告活动及当前页游标、总数量。

        Examples:
            指定广告账号和分页范围查询并查看公开字段。

            .. code-block:: python

                result = await client.ads.SbCampaigns(profile_id=90000000000006, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码，0表示成功
                    'code': 0,
                    # 消息提示
                    'message': '操作成功',
                    # 错误明细
                    'errors': [
                    ],
                    # 请求链路ID
                    'request_id': '00000000-0000-0000-0000-00000000004d',
                    # 响应时间
                    'response_time': '2001-05-07 07:50:00',
                    # 当前页数量
                    'response_count': 2,
                    # 总数量
                    'total_count': 37,
                    # 响应数据
                    'data': [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            'profile_id': 90000000000006,
                            # 广告组合ID
                            'portfolio_id': 800000000000005,
                            # 广告活动ID
                            'campaign_id': 7000000000280,
                            # 广告活动名称 [原字段 'name']
                            'campaign_name': '000 0A0A 广告示示广-告铺',
                            # 广告创意类型
                            'creative_type': 'COLLECTION',
                            # 广告预算
                            'budget': 1.0,
                            # 广告预算类型
                            'budget_type': 'daily',
                            # 时间字符串，格式为 YYYY-MM-DD HH:MM:SS，可为 None [原字段 'lastOverBudgetAt']
                            'last_over_budget_at': '2026-10-12 22:17:35',
                            # 自定义竞价调整
                            'bid_multiplier': 0.0,
                            # 是否使用自动竞价 (0: 否, 1: 是)
                            'bid_optimization': 1,
                            # 开始时间 [原字段 'start_date']
                            'start_time': '2022-11-17 00:00:00',
                            # 结束时间 [原字段 'end_date']
                            'end_time': '',
                            # 广告状态
                            'state': 'enabled',
                            # 服务状态 [原字段 'serving_status']
                            'status': 'CAMPAIGN_STATUS_ENABLED',
                        },
                        ...,
                    ],
                    # 分页游标
                    'next_token': 'MTAwMDAwMDAwMDAwMzc=',
                }
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
        sid: int | None = None,
        profile_id: int | None = None,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbAdGroups:
        """查询 SB 广告组。

        ## Docs
        领星接口文档: [新广告 - 基础数据 - SB 广告组](https://apidoc.lingxing.com/new/api-docs/newAd/baseData/hsaAdGroups/)

        Args:
            sid (int | None): 领星店铺ID，默认 None。sid 与 profile_id 至少提供一项；同时提供时，以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            state (str | None): enabled、paused或archived；默认None，省略并查询所有状态。
            next_token (str | None): 上次响应的分页游标；默认None；同时传offset时以游标定位。
            offset (int | None): 非负记录偏移量，默认None，由服务端采用0；显式0保留。
            length (int | None): 非负分页长度，默认None，由服务端采用15。

        Returns:
            ads.schema.SbAdGroups: SB 广告组及当前页游标、总数量。

        Examples:
            指定广告账号和分页范围查询并查看公开字段。

            .. code-block:: python

                result = await client.ads.SbAdGroups(profile_id=90000000000004, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {'code': 0,
                 # 消息提示
                 'message': '操作成功',
                 # 错误明细
                 'errors': [],
                 # 请求链路ID
                 'request_id': '00000000-0000-0000-0000-000000000002',
                 # 响应时间
                 'response_time': '2001-05-07 07:50:00',
                 # 当前页数量
                 'response_count': 2,
                 # 总数量
                 'total_count': 37,
                 # 响应数据
                 'data': [{'profile_id': 90000000000004,
                           # 广告活动ID
                           'campaign_id': 700000000000112,
                           # 广告组ID
                           'ad_group_id': 60000000000208,
                           # 广告组名称 [原字段 'name']
                           'ad_group_name': '000 000广告组-广甲',
                           # 广告状态
                           'state': 'enabled',
                           # 服务状态 [原字段 'serving_status']
                           'status': 'CAMPAIGN_PAUSED',
                           # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                           'create_time_ts': 1670754552292,
                           # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                           'update_time_ts': 1670754552292},
                          ...],
                 # 分页游标
                 'next_token': 'MTAwMDAwMDAwMDAwMzA='}
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
        sid: int | None = None,
        profile_id: int | None = None,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbCreatives:
        """查询 SB 广告创意。

        ## Docs
        领星接口文档: [新广告 - 基础数据 - SB广告创意](https://apidoc.lingxing.com/new/api-docs/newAd/baseData/sbAdHasProductAds/)

        Args:
            sid (int | None): 领星店铺ID，默认 None。sid 与 profile_id 至少提供一项；同时提供时，以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            next_token (str | None): 上次响应的分页游标；默认None；同时传offset时以游标定位。
            offset (int | None): 非负记录偏移量，默认None，由服务端采用0；显式0保留。
            length (int | None): 非负分页长度，默认None，由服务端采用15。

        Returns:
            ads.schema.SbCreatives: 广告创意、创意配置、着陆页、视频创意列表，以及当前页游标、总数量。

        使用 offset/length 或 next_token 分页时，返回结果可能出现重复或遗漏；
        分段查询结果不保证与单次查询一致，去重也不能保证恢复完整数据。

        Examples:
            指定广告账号和分页范围查询并查看公开字段。

            .. code-block:: python

                result = await client.ads.SbCreatives(profile_id=90000000000007, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码，0表示成功
                    "code": 0,
                    # 消息提示
                    "message": "操作成功",
                    # 错误明细
                    "errors": [],
                    # 请求链路ID
                    "request_id": "00000000-0000-0000-0000-00000000002d",
                    # 响应时间
                    "response_time": "2001-05-07 08:20:00",
                    # 当前页数量
                    "response_count": 2,
                    # 总数量
                    "total_count": 258,
                    # 响应数据
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 90000000000007,
                            # 广告活动ID
                            "campaign_id": 700000000000170,
                            # 广告组ID
                            "ad_group_id": 600000000000278,
                            # 广告创意ID [原字段 'ad_creative_id']
                            "creative_id": 500000000000004,
                            # 广告创意名称 [原字段 'name']
                            "creative_name": "广告 示示 - 00.0.0004",
                            # 广告创意类型
                            "creative_type": "VIDEO",
                            # 广告创意设置 [原字段 'creative']
                            "creative_config": {
                                # 广告创意类型
                                "creative_type": "VIDEO",
                                # 广告创意状态 [原字段 'creativeStatus']
                                "creative_status": "PUBLISHED",
                                # 广告创意版本 [原字段 'creativeVersion']
                                "creative_version": 1,
                                # 广告创意 ASIN 列表 [原字段 'asin']
                                "asins": ["A0AAA0AA6O"],
                                # 广告创意排除 ASIN 列表 [原字段 'asinExclusions']
                                "asin_excluded": ["A0A0A0AAJN", ...],
                                # 是否同意翻译 [原字段 'consentToTranslate']
                                "consent_to_translate": False,
                                # 品牌名称 [原字段 'brandName']
                                "brand_name": None,
                                # 品牌Logo素材ID [原字段 'brandLogoAssetID']
                                "brand_logo_asset_id": None,
                                # 品牌Logo链接 [原字段 'brandLogoUrl']
                                "brand_logo_url": None,
                                # 头条
                                "headline": None,
                                # 头条列表
                                "headlines": None,
                                # 原始头条 [原字段 'originalHeadline']
                                "headline_original": None,
                                # 原始头条列表 [原字段 'originalHeadlines']
                                "headlines_original": None,
                                # 图片素材ID [原字段 'customImageAssetId']
                                "custom_image_asset_id": None,
                                # 图片链接 [原字段 'customImageUrl']
                                "custom_image_url": None,
                                # 图片素材列表 [原字段 'customImages']
                                "custom_images": None,
                                # 优化属性列表 [原字段 'creativePropertiesToOptimize']
                                "optimize_properties": None,
                                # 视频素材ID列表 [原字段 'videoAssetIds']
                                "video_asset_ids": [
                                    "amzn1.assetlibrary.asset1.0000a0000aaa0a00aaa0aaa000aa023s:version_v1",
                                ],
                                # 原始素材ID列表 [原字段 'originalVideoAssetIds']
                                "video_original_asset_ids": [
                                    "amzn1.assetlibrary.asset1.0000a0000aaa0a00aaa0aaa000aa023s:version_v1",
                                ],
                                # 商品集类型 [原字段 'collectionType']
                                "collection_type": "THEMED",
                                # 子页面列表
                                "subpages": [
                                    {
                                        "asin": "A0000AAADB",
                                        "page_title": "aaa RT",
                                        "page_url": "https://aaa.aaaaaa.aaa/aaaaaa/aaaa/A0AA0000-00AA-0A0A-A00A-0A000AAA0883",
                                    },
                                    ...,
                                ],
                                # 广告标题
                                "title": "000AA AA & AAA - 0000+ Aaaaao",
                            },
                            # 视频创意列表
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
                                },
                                ...,
                            ],
                            # 广告创意着陆页
                            "landing_page": {
                                # 着陆页类型 [原字段 'pageType']
                                "page_type": "DETAIL_PAGE",
                                # 着陆页URL [原字段 'url']
                                "page_url": "https://aaa.aaaaaa.aa/aa/A0AAA0AA0M",
                            },
                            # 广告创意 ASIN 列表 [原字段 'asin']
                            "asins": ["A0AAA0AA6O"],
                            # 广告状态
                            "state": "enabled",
                            # 服务状态 [原字段 'serving_status']
                            "status": "CAMPAIGN_PAUSED",
                            # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                            "create_time_ts": 1758692404896,
                            # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                            "update_time_ts": 1781581969786,
                        },
                        ...,
                    ],
                    # 分页游标
                    "next_token": "MTAwMDI1",
                }
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
        sid: int | None = None,
        profile_id: int | None = None,
        ad_type: AD_SB_TYPE = "ALL",
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbKeywords:
        """查询SB 关键词投放。

        ## Docs
        领星接口文档: [新广告 - 基础数据 - SB广告的投放](https://apidoc.lingxing.com/new/api-docs/newAd/baseData/sbTargeting/)

        Args:
            sid (int | None): 领星店铺ID，默认 None。sid 与 profile_id 至少提供一项；同时提供时，以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            ad_type (str): 广告类型，SB、SBV或ALL；默认ALL。只查询关键词投放。
            next_token (str | None): 上次响应的分页游标；默认None；同时传offset时以游标定位。
            offset (int | None): 非负记录偏移量，默认None，由服务端采用0；显式0保留。
            length (int | None): 非负分页长度，默认None，由服务端采用15。

        Returns:
            ads.schema.SbKeywords: SB 关键词投放及当前页游标、总数量。

        Examples:
            指定广告账号和分页范围查询并查看公开字段。

            .. code-block:: python

                result = await client.ads.SbKeywords(profile_id=90000000000006, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码，0表示成功
                    'code': 0,
                    # 消息提示
                    'message': '操作成功',
                    # 错误明细
                    'errors': [
                    ],
                    # 请求链路ID
                    'request_id': '00000000-0000-0000-0000-000000000011',
                    # 响应时间
                    'response_time': '2001-05-07 08:18:00',
                    # 当前页数量
                    'response_count': 2,
                    # 总数量
                    'total_count': 3804,
                    # 响应数据
                    'data': [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            'profile_id': 90000000000006,
                            # 广告活动ID
                            'campaign_id': 700000000000090,
                            # 广告组ID
                            'ad_group_id': 600000000000028,
                            # 广告类型 [原字段 'ads_type']
                            'ad_type': 'SB',
                            # 投放目标类型
                            'targeting_type': 'keyword',
                            # 关键词ID
                            'keyword_id': 400000000020,
                            # 关键词文本
                            'keyword_text': '+aaaaa +000ab',
                            # 关键词匹配类型
                            'match_type': 'broad',
                            # 竞价 [原字段 'keyword_bid']
                            'bid': 0.8,
                            # 广告状态 [原字段 'keyword_state']
                            'state': 'paused',
                        },
                        ...,
                    ],
                    # 分页游标
                    'next_token': 'MTAwMDAwMDAwMDAxOQ==',
                }
        """
        url = route.SB_TARGETING
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "ad_type": ad_type,
            "target_type": "keyword",
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
        sid: int | None = None,
        profile_id: int | None = None,
        ad_type: AD_SB_TYPE = "ALL",
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbTargets:
        """查询SB 目标商品投放。

        ## Docs
        领星接口文档: [新广告 - 基础数据 - SB广告的投放](https://apidoc.lingxing.com/new/api-docs/newAd/baseData/sbTargeting/)

        Args:
            sid (int | None): 领星店铺ID，默认 None。sid 与 profile_id 至少提供一项；同时提供时，以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            ad_type (str): 广告类型，SB、SBV或ALL；默认ALL。只查询商品投放。
            next_token (str | None): 上次响应的分页游标；默认None；同时传offset时以游标定位。
            offset (int | None): 非负记录偏移量，默认None，由服务端采用0；显式0保留。
            length (int | None): 非负分页长度，默认None，由服务端采用15。

        Returns:
            ads.schema.SbTargets: SB 目标商品投放及当前页游标、总数量。

        Examples:
            指定广告账号和分页范围查询并查看公开字段。

            .. code-block:: python

                result = await client.ads.SbTargets(profile_id=90000000000006, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码，0表示成功
                    'code': 0,
                    # 消息提示
                    'message': '操作成功',
                    # 错误明细
                    'errors': [
                    ],
                    # 请求链路ID
                    'request_id': '00000000-0000-0000-0000-00000000005b',
                    # 响应时间
                    'response_time': '2001-05-07 08:31:00',
                    # 当前页数量
                    'response_count': 2,
                    # 总数量
                    'total_count': 11,
                    # 响应数据
                    'data': [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            'profile_id': 90000000000006,
                            # 广告活动ID
                            'campaign_id': 700000000000000039,
                            # 广告组ID
                            'ad_group_id': 600000000000000041,
                            # 广告类型 [原字段 'ads_type']
                            'ad_type': 'SB',
                            # 投放目标类型
                            'targeting_type': 'producttarget',
                            # 目标商品广告ID
                            'target_id': 300000000000000003,
                            # 目标定位表达式 (JSON 字符串)
                            'expression': '[{"type": "asinSameAs", "value": "A00AA0AAFG"}]',
                            # 目标定位解析表达式 (JSON 字符串) [原字段 'resolved_expression']
                            'expression_resolved': '[{"type": "asinSameAs", "value": "A00AA0AAFG"}]',
                            # 竞价 [原字段 'target_bid']
                            'bid': 1.0,
                            # 广告状态 [原字段 'target_state']
                            'state': 'paused',
                        },
                        ...,
                    ],
                    # 分页游标
                    'next_token': 'MTAwMDAwMDAwMDAwMDAwMDA5',
                }
        """
        url = route.SB_TARGETING
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "ad_type": ad_type,
            "target_type": "product",
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
        sid: int | None = None,
        profile_id: int | None = None,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbNegativeKeywords:
        """查询 SB 否定关键词投放。

        ## Docs
        领星接口文档: [新广告 - 基础数据 - SB 否定关键词投放](https://apidoc.lingxing.com/new/api-docs/newAd/baseData/hsaNegativeKeywords/)

        Args:
            sid (int | None): 领星店铺ID，默认 None。sid 与 profile_id 至少提供一项；同时提供时，以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            state (str | None): enabled、paused或archived；默认None，省略并查询所有状态。
            next_token (str | None): 上次响应的分页游标；默认None；同时传offset时以游标定位。
            offset (int | None): 非负记录偏移量，默认None，由服务端采用0；显式0保留。
            length (int | None): 非负分页长度，默认None，由服务端采用15。

        Returns:
            ads.schema.SbNegativeKeywords: SB 否定关键词投放及当前页游标、总数量。

        Examples:
            指定广告账号和分页范围查询并查看公开字段。

            .. code-block:: python

                result = await client.ads.SbNegativeKeywords(profile_id=90000000000004, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {'code': 0,
                 # 消息提示
                 'message': '操作成功',
                 # 错误明细
                 'errors': [],
                 # 请求链路ID
                 'request_id': '00000000-0000-0000-0000-000000000019',
                 # 响应时间
                 'response_time': '2001-05-07 08:04:00',
                 # 当前页数量
                 'response_count': 2,
                 # 总数量
                 'total_count': 128,
                 # 响应数据
                 'data': [{'profile_id': 90000000000004,
                           # 广告活动ID
                           'campaign_id': 700000000000128,
                           # 广告组ID
                           'ad_group_id': 60000000000285,
                           # 否定关键词ID [原字段 'keyword_id']
                           'negative_keyword_id': 40000000000006,
                           # 否定关键词文本 [原字段 'keyword_text']
                           'negative_keyword_text': 'aaaaa 000 ag',
                           # 否定匹配方式 [原字段 'match_type']
                           'negative_keyword_match_type': 'negativeExact',
                           # 广告状态
                           'state': 'enabled',
                           # 服务状态 [原字段 'serving_status']
                           'status': '',
                           # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                           'create_time_ts': 1743039447981,
                           # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                           'update_time_ts': 1743039448036},
                          ...],
                 # 分页游标
                 'next_token': 'MTAwMDAwMDAwMDAwMjA='}
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
        sid: int | None = None,
        profile_id: int | None = None,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbNegativeTargets:
        """查询 SB 否定目标商品投放。

        ## Docs
        领星接口文档: [新广告 - 基础数据 - SB否定商品投放](https://apidoc.lingxing.com/new/api-docs/newAd/baseData/hsaNegativeTargets/)

        Args:
            sid (int | None): 领星店铺ID，默认 None。sid 与 profile_id 至少提供一项；同时提供时，以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            state (str | None): enabled、paused或archived；默认None，省略并查询所有状态。
            next_token (str | None): 上次响应的分页游标；默认None；同时传offset时以游标定位。
            offset (int | None): 非负记录偏移量，默认None，由服务端采用0；显式0保留。
            length (int | None): 非负分页长度，默认None，由服务端采用15。

        Returns:
            ads.schema.SbNegativeTargets: SB否定目标商品投放及当前页游标、总数量。

        Examples:
            指定广告账号和分页范围查询并查看公开字段。

            .. code-block:: python

                result = await client.ads.SbNegativeTargets(profile_id=900000000000001, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码，0表示成功
                    'code': 0,
                    # 消息提示
                    'message': '操作成功',
                    # 错误明细
                    'errors': [
                    ],
                    # 请求链路ID
                    'request_id': '00000000-0000-0000-0000-00000000007e',
                    # 响应时间
                    'response_time': '2001-05-07 08:18:00',
                    # 当前页数量
                    'response_count': 2,
                    # 总数量
                    'total_count': 34,
                    # 响应数据
                    'data': [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            'profile_id': 900000000000001,
                            # 广告活动ID
                            'campaign_id': 700000000000000038,
                            # 广告组ID
                            'ad_group_id': 600000000000000037,
                            # 否定目标ID [原字段 'target_id']
                            'negative_target_id': 300000000000000001,
                            # 否定定位表达式 (JSON 字符串) [原字段 'expression']
                            'negative_expression': '[{"type": "asinSameAs", "value": "A000AAA0A3"}]',
                            # 否定定位解析表达式 (JSON 字符串) [原字段 'resolved_expression']
                            'negative_expression_resolved': '[{"type": "asinSameAs", "value": "A000AAA0A3"}]',
                            # 否定定位类型 [原字段 'expression_type']
                            'negative_expression_type': '',
                            # 广告状态
                            'state': 'archived',
                            # 服务状态 [原字段 'serving_status']
                            'status': '',
                            # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                            'create_time_ts': 1598667375000,
                            # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                            'update_time_ts': 1761061319939,
                        },
                        ...,
                    ],
                    # 分页游标
                    'next_token': 'MTAwMDAwMDAwMDAwMDAwMDA4',
                }
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
        sid: int | None = None,
        profile_id: int | None = None,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SdCampaigns:
        """查询SD广告活动。

        ## Docs
        领星接口文档: 新广告 - 基础数据.[SD广告活动](https://apidoc.lingxing.com/new/api-docs/newAd/baseData/sdCampaigns/)

        Args:
            sid (int | None): 领星店铺ID，默认 None；与 profile_id 至少提供一项，同时提供时以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            state (str | None): 广告状态，可传 enabled（启用）、paused（暂停）、archived（归档）；默认 None，省略请求参数并查询所有状态。
            next_token (str | None): 上一页返回的分页游标，默认 None，首次查询无需提供；与 offset 同时提供时按游标定位。
            offset (int | None): 按记录数计算的非负分页偏移量，默认 None；None 省略请求键，由服务端采用默认值0，显式0保留。
            length (int | None): 非负分页长度，默认 None；None 省略请求键，由服务端采用默认值15。

        Returns:
            ads.schema.SdCampaigns: 查询到的SD广告活动及当前页游标、总数量。

        Examples:
            指定广告账号和分页范围查询并查看返回数据。

            .. code-block:: python

                result = await client.ads.SdCampaigns(profile_id=90000000000007, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    'code': 0,
                    'message': 'success',
                    'errors': [],
                    'request_id': '00000000-0000-0000-0000-0000000001af',
                    'response_time': '2001-05-07 09:48:00',
                    'response_count': 2,
                    'total_count': 2,
                    'data': [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            'profile_id': 90000000000007,
                            # 广告组合ID
                            'portfolio_id': 0,
                            # 广告活动ID
                            'campaign_id': 7000000000202,
                            # 广告活动名称 [原字段 'name']
                            'campaign_name': '00-广告角',
                            # 投放类型
                            'tactic': 'T00020',
                            # 竞价类型 [原字段 'cost_type']
                            'bid_type': 'cpc',
                            # 每日预算
                            'budget': 14.0,
                            # 预算类型
                            'budget_type': 'daily',
                            # 时间字符串，格式为 YYYY-MM-DD HH:MM:SS，可为 None [原字段 'lastOverBudgetAt']
                            'last_over_budget_at': '2026-10-12 22:17:35',
                            # 开始时间 [原字段 'start_date']
                            'start_time': '2020-09-29 00:00:00',
                            # 结束时间 [原字段 'end_date']
                            'end_time': '',
                            # 广告状态
                            'state': 'paused',
                            # 服务状态 [原字段 'serving_status']
                            'status': 'CAMPAIGN_PAUSED',
                            # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                            'create_time_ts': 1601345109000,
                            # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                            'update_time_ts': 1792105230609,
                        },
                        ...,
                    ],
                    'next_token': 'MTAwMDAwMDAwMDAwMjM=',
                }
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
        sid: int | None = None,
        profile_id: int | None = None,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SdAdGroups:
        """查询SD广告组。

        ## Docs
        领星接口文档: 新广告 - 基础数据.[SD广告组](https://apidoc.lingxing.com/new/api-docs/newAd/baseData/sdAdGroups/)

        Args:
            sid (int | None): 领星店铺ID，默认 None；与 profile_id 至少提供一项，同时提供时以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            state (str | None): 广告状态，可传 enabled（启用）、paused（暂停）、archived（归档）；默认 None，省略请求参数并查询所有状态。
            next_token (str | None): 上一页返回的分页游标，默认 None，首次查询无需提供；与 offset 同时提供时按游标定位。
            offset (int | None): 按记录数计算的非负分页偏移量，默认 None；None 省略请求键，由服务端采用默认值0，显式0保留。
            length (int | None): 非负分页长度，默认 None；None 省略请求键，由服务端采用默认值15。

        Returns:
            ads.schema.SdAdGroups: 查询到的SD广告组及当前页游标、总数量。

        Examples:
            指定广告账号和分页范围查询并查看返回数据。

            .. code-block:: python

                result = await client.ads.SdAdGroups(profile_id=90000000000006, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    'code': 0,
                    'message': 'success',
                    'errors': [],
                    'request_id': '00000000-0000-0000-0000-0000000000a9',
                    'response_time': '2001-05-07 10:02:00',
                    'response_count': 2,
                    'total_count': 2,
                    'data': [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            'profile_id': 90000000000006,
                            # 广告活动ID
                            'campaign_id': 70000000000077,
                            # 广告组ID
                            'ad_group_id': 60000000000072,
                            # 广告组名称 [原字段 'name']
                            'ad_group_name': 'aa-00-广名',
                            # 默认竞价
                            'default_bid': 0.6,
                            # 竞价优化方式
                            'bid_optimization': 'clicks',
                            # 广告组状态
                            'state': 'enabled',
                            # 服务状态 [原字段 'serving_status']
                            'status': 'CAMPAIGN_PAUSED',
                            # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                            'create_time_ts': 1599816989000,
                            # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                            'update_time_ts': 1599816989000,
                        },
                        ...,
                    ],
                    # 下一页游标
                    'next_token': 'MTAwMDAwMDAwMDAwMzQ=',
                }
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
        sid: int | None = None,
        profile_id: int | None = None,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SdProducts:
        """查询SD商品投放。

        ## Docs
        领星接口文档: 新广告 - 基础数据.[SD商品投放](https://apidoc.lingxing.com/new/api-docs/newAd/baseData/sdProductAds/)

        Args:
            sid (int | None): 领星店铺ID，默认 None；与 profile_id 至少提供一项，同时提供时以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            state (str | None): 广告状态，可传 enabled（启用）、paused（暂停）、archived（归档）；默认 None，省略请求参数并查询所有状态。
            next_token (str | None): 上一页返回的分页游标，默认 None，首次查询无需提供；与 offset 同时提供时按游标定位。
            offset (int | None): 按记录数计算的非负分页偏移量，默认 None；None 省略请求键，由服务端采用默认值0，显式0保留。
            length (int | None): 非负分页长度，默认 None；None 省略请求键，由服务端采用默认值15。

        Returns:
            ads.schema.SdProducts: 查询到的SD商品投放及当前页游标、总数量。

        Examples:
            指定广告账号和分页范围查询并查看返回数据。

            .. code-block:: python

                result = await client.ads.SdProducts(profile_id=90000000000006, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    'code': 0,
                    'message': 'success',
                    'errors': [],
                    'request_id': '00000000-0000-0000-0000-000000000013',
                    'response_time': '2001-05-07 10:15:00',
                    'response_count': 2,
                    'total_count': 2,
                    'data': [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            'profile_id': 90000000000006,
                            # 广告活动ID
                            'campaign_id': 700000000000168,
                            # 广告组ID
                            'ad_group_id': 600000000000108,
                            # 商品广告ID
                            'ad_id': 5000000000005,
                            # 商品ASIN
                            'asin': 'A00AAAA0AL',
                            # 亚马逊SKU [原字段 'sku']
                            'msku': '000aa*2X',
                            # 广告状态
                            'state': 'paused',
                            # 服务状态 [原字段 'serving_status']
                            'status': 'AD_PAUSED',
                            # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                            'create_time_ts': 1600853070000,
                            # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                            'update_time_ts': 1696439612959,
                        },
                        ...,
                    ],
                    # 下一页游标
                    'next_token': 'MTAwMDAwMDAwMDAzNg==',
                }
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
        sid: int | None = None,
        profile_id: int | None = None,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SdTargets:
        """查询SD目标商品投放。

        ## Docs
        领星接口文档: 新广告 - 基础数据.[SD目标商品投放](https://apidoc.lingxing.com/new/api-docs/newAd/baseData/sdTargets/)

        Args:
            sid (int | None): 领星店铺ID，默认 None；与 profile_id 至少提供一项，同时提供时以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            state (str | None): 广告状态，可传 enabled（启用）、paused（暂停）、archived（归档）；默认 None，省略请求参数并查询所有状态。
            next_token (str | None): 上一页返回的分页游标，默认 None，首次查询无需提供；与 offset 同时提供时按游标定位。
            offset (int | None): 按记录数计算的非负分页偏移量，默认 None；None 省略请求键，由服务端采用默认值0，显式0保留。
            length (int | None): 非负分页长度，默认 None；None 省略请求键，由服务端采用默认值15。

        Returns:
            ads.schema.SdTargets: 查询到的SD目标商品投放及当前页游标、总数量。

        Examples:
            指定广告账号和分页范围查询并查看返回数据。

            .. code-block:: python

                result = await client.ads.SdTargets(profile_id=90000000000007, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    'code': 0,
                    'message': 'success',
                    'errors': [],
                    'request_id': '00000000-0000-0000-0000-000000000146',
                    'response_time': '2001-05-07 10:28:00',
                    'response_count': 2,
                    'total_count': 2,
                    'data': [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            'profile_id': 90000000000007,
                            # 广告活动ID
                            'campaign_id': 700000000000033,
                            # 广告组ID
                            'ad_group_id': 600000000000106,
                            # 目标商品广告ID
                            'target_id': 300000000015,
                            # 目标定位类型
                            'expression_type': 'manual',
                            # 目标定位表达式 (JSON 字符串)
                            'expression': '[{"type": "asinSameAs", "value": "A00AAAAABI"}]',
                            # 目标定位解析表达式 (JSON 字符串) [原字段 'resolved_expression']
                            'expression_resolved': '[{"type": "asinSameAs", "value": "A00AAAAABI"}]',
                            # 竞价
                            'bid': 0.3,
                            # 广告状态
                            'state': 'enabled',
                            # 服务状态 [原字段 'serving_status']
                            'status': 'CAMPAIGN_PAUSED',
                            # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                            'create_time_ts': 1601344253000,
                            # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                            'update_time_ts': 1601344253000,
                        },
                        ...,
                    ],
                    'next_token': 'MTAwMDAwMDAwMDgx',
                }
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
        sid: int | None = None,
        profile_id: int | None = None,
        *,
        state: AD_STATE | None = None,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SdNegativeTargets:
        """查询SD否定目标商品投放。

        ## Docs
        领星接口文档: 新广告 - 基础数据.[SD否定目标商品投放](https://apidoc.lingxing.com/new/api-docs/newAd/baseData/sdNegativeTargets/)

        Args:
            sid (int | None): 领星店铺ID，默认 None；与 profile_id 至少提供一项，同时提供时以 profile_id 指定的广告账号为准。
            profile_id (int | None): 广告账号ID，来源为 AdProfiles 返回记录的 profile_id，默认 None；None 不输出到请求字典。
            state (str | None): 广告状态，可传 enabled（启用）、paused（暂停）、archived（归档）；默认 None，省略请求参数并查询所有状态。
            next_token (str | None): 上一页返回的分页游标，默认 None，首次查询无需提供；与 offset 同时提供时按游标定位。
            offset (int | None): 按记录数计算的非负分页偏移量，默认 None；None 省略请求键，由服务端采用默认值0，显式0保留。
            length (int | None): 非负分页长度，默认 None；None 省略请求键，由服务端采用默认值15。

        Returns:
            ads.schema.SdNegativeTargets: 查询到的SD否定目标商品投放及当前页游标、总数量。

        Examples:
            指定广告账号和分页范围查询并查看返回数据。

            .. code-block:: python

                result = await client.ads.SdNegativeTargets(profile_id=900000000000001, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    'code': 0,
                    'message': 'success',
                    'errors': [],
                    'request_id': '00000000-0000-0000-0000-000000000052',
                    'response_time': '2001-05-07 10:42:00',
                    'response_count': 2,
                    'total_count': 2,
                    'data': [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            'profile_id': 900000000000001,
                            # 广告活动ID
                            'campaign_id': 70000000000159,
                            # 广告组ID
                            'ad_group_id': 600000000000057,
                            # 否定目标ID [原字段 'target_id']
                            'negative_target_id': 30000000000020,
                            # 否定定位表达式 (JSON 字符串) [原字段 'expression']
                            'negative_expression': '[{"type": "asinSameAs", "value": "A00AA0AAFV"}]',
                            # 否定定位解析表达式 (JSON 字符串) [原字段 'resolved_expression']
                            'negative_expression_resolved': '[{"type": "asinSameAs", "value": "A00AA0AAFV"}]',
                            # 否定定位类型 [原字段 'expression_type']
                            'negative_expression_type': 'manual',
                            # 广告状态
                            'state': 'enabled',
                            # 服务状态 [原字段 'serving_status']
                            'status': 'CAMPAIGN_PAUSED',
                            # 创建时间 (UTC毫秒时间戳) [原字段 'creation_date']
                            'create_time_ts': 1659405193284,
                            # 更新时间 (UTC毫秒时间戳) [原字段 'last_updated_date']
                            'update_time_ts': 1659405193284,
                        },
                        ...,
                    ],
                    # 下一页游标
                    'next_token': 'MTAwMDAwMDAwMDAwMDIz',
                }
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
        """查询SP广告活动日报。

        ## Docs
        领星接口文档: 新广告 - 报告.[SP广告活动日报](https://apidoc.lingxing.com/new/api-docs/newAd/report/spCampaignReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，按传入日期的年月日查询，建议提供完整YYYY-MM-DD。
            sid (int): 领星店铺ID；与profile_id至少提供一项，使用profile_id查询时可显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id；使用sid查询时可显式传None。
            next_token (str | None): 上一页返回的游标，默认None；与offset同时提供时按游标定位。
            offset (int | None): 非负记录偏移量，默认None并省略，由接口采用0；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，由接口采用15；显式0保留。

        Returns:
            ads.schema.SpCampaignReports: 返回默认归因范围的日报指标，不提供完整归因期开关。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpCampaignReports(report_date="2026-10-01", sid=None, profile_id=90000000000007, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "操作成功",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-00000000014c",
                    # 响应时间
                    "response_time": "2001-05-07 10:44:00",
                    # 响应数据量
                    "response_count": 2,
                    # 总数据量
                    "total_count": 33,
                    # SP 广告活动报告列表
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 90000000000007,
                            # 广告活动ID
                            "campaign_id": 70000000000204,
                            # 投放目标类型
                            "targeting_type": "",
                            # 广告花费
                            "cost": 1.5,
                            # 总展示次数
                            "impressions": 177,
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
                            "sales": 16.66,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 16.66,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                    # 分页游标
                    "next_token": "MTAwMDAwMDAwMDAwMTk=",
                }
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
        """查询SP广告活动小时数据。

        ## Docs
        领星接口文档: 新广告 - 报告.[SP广告活动小时数据](https://apidoc.lingxing.com/new/api-docs/newAd/report/spCampaignHourData/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，按传入日期的年月日查询，建议提供完整YYYY-MM-DD。接口支持最近60天。
            campaign_id (int): 广告活动ID，可取同日日报或SpCampaigns返回的campaign_id。

        Returns:
            ads.schema.SpCampaignHourData: 按小时返回，不提供分页参数。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpCampaignHourData(campaign_id=70000000000006, report_date="2026-10-01")
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "操作成功",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-00000000008d",
                    # 响应时间
                    "response_time": "2001-05-07 12:21:00",
                    # 响应数据量
                    "response_count": 21,
                    # 总数据量
                    "total_count": 21,
                    # SP 广告活动小时数据列表
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 90000000000004,
                            # 广告活动ID
                            "campaign_id": 70000000000006,
                            # 广告花费
                            "cost": 1.5,
                            # 总展示次数
                            "impressions": 12,
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
                            "sales": 16.66,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 16.66,
                            # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                            "ctr": 0.0833,
                            # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                            "cvr": 1.0,
                            # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                            "cpc": 1.5,
                            # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                            "cpa": 1.5,
                            # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                            "acos": 0.09,
                            # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                            "roas": 11.11,
                            # 数据所属小时 (0-23)
                            "hour": 20,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                }
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
        """查询SP广告位日报。

        ## Docs
        领星接口文档: 新广告 - 报告.[SP广告位日报](https://apidoc.lingxing.com/new/api-docs/newAd/report/campaignPlacementReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，按传入日期的年月日查询，建议提供完整YYYY-MM-DD。
            sid (int): 领星店铺ID；与profile_id至少提供一项，使用profile_id查询时可显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id；使用sid查询时可显式传None。
            next_token (str | None): 上一页返回的游标，默认None；与offset同时提供时按游标定位。
            offset (int | None): 非负记录偏移量，默认None并省略，由接口采用0；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，由接口采用15；显式0保留。

        Returns:
            ads.schema.SpPlacementReports: 返回默认归因范围的日报指标，不提供完整归因期开关。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpPlacementReports(report_date="2026-10-01", sid=None, profile_id=90000000000004, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "操作成功",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-000000000101",
                    # 响应时间
                    "response_time": "2001-05-07 10:56:00",
                    # 响应数据量
                    "response_count": 2,
                    # 总数据量
                    "total_count": 75,
                    # SP 广告活动投放位置报告列表
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 90000000000004,
                            # 广告活动ID
                            "campaign_id": 700000000000008,
                            # 广告投放位置 [原字段 'placement_type']
                            "placement": "OTHER ON-AMAZON",
                            # 广告花费
                            "cost": 1.35,
                            # 总展示次数
                            "impressions": 19,
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
                            "sales": 19.77,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 19.77,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                    # 分页游标
                    "next_token": "MDAwYTAwYWEwYWEwMDBhMDBhYTBhMDBhYTAwYTAwMDU=",
                }
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
        """查询SP广告位小时数据。

        ## Docs
        领星接口文档: 新广告 - 报告.[SP广告位小时数据](https://apidoc.lingxing.com/new/api-docs/newAd/report/spAdPlacementHourData/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，按传入日期的年月日查询，建议提供完整YYYY-MM-DD。接口支持最近60天。
            campaign_id (int): 广告活动ID，可取同日日报或SpCampaigns返回的campaign_id。

        Returns:
            ads.schema.SpPlacementHourData: 按小时返回，不提供分页参数。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpPlacementHourData(campaign_id=70000000000006, report_date="2026-10-01")
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "操作成功",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-0000000000c7",
                    # 响应时间
                    "response_time": "2001-05-07 12:23:00",
                    # 响应数据量
                    "response_count": 50,
                    # 总数据量
                    "total_count": 50,
                    # SP 广告活动投放位置小时数据列表
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 90000000000004,
                            # 广告活动ID
                            "campaign_id": 70000000000006,
                            # 广告投放位置
                            "placement": "Other on-Amazon",
                            # 广告花费
                            "cost": 1.5,
                            # 总展示次数
                            "impressions": 5,
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
                            "sales": 16.66,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 16.66,
                            # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                            "ctr": 0.2,
                            # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                            "cvr": 1.0,
                            # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                            "cpc": 1.5,
                            # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                            "cpa": 1.5,
                            # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                            "acos": 0.09,
                            # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                            "roas": 11.11,
                            # 数据所属小时 (0-23)
                            "hour": 20,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                }
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
        """查询SP广告组日报。

        ## Docs
        领星接口文档: 新广告 - 报告.[SP广告组日报](https://apidoc.lingxing.com/new/api-docs/newAd/report/spAdGroupReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，按传入日期的年月日查询，建议提供完整YYYY-MM-DD。
            sid (int): 领星店铺ID；与profile_id至少提供一项，使用profile_id查询时可显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id；使用sid查询时可显式传None。
            next_token (str | None): 上一页返回的游标，默认None；与offset同时提供时按游标定位。
            offset (int | None): 非负记录偏移量，默认None并省略，由接口采用0；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，由接口采用15；显式0保留。

        Returns:
            ads.schema.SpAdGroupReports: 返回默认归因范围的日报指标，不提供完整归因期开关。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpAdGroupReports(report_date="2026-10-01", sid=None, profile_id=90000000000004, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "操作成功",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-00000000004f",
                    # 响应时间
                    "response_time": "2001-05-07 11:08:00",
                    # 响应数据量
                    "response_count": 2,
                    # 总数据量
                    "total_count": 33,
                    # SP 广告组报告列表
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 90000000000004,
                            # 广告活动ID
                            "campaign_id": 70000000000011,
                            # 广告组ID
                            "ad_group_id": 600000000000001,
                            # 广告花费
                            "cost": 2.64,
                            # 总展示次数
                            "impressions": 1106,
                            # 总点击次数
                            "clicks": 2,
                            # 广告订单数
                            "orders": 2,
                            # 直接广告订单数 [原字段 'same_orders']
                            "direct_orders": 2,
                            # 广告成交商品件数
                            "units": 2,
                            # 直接广告成交商品件数 [原字段 'same_units']
                            "direct_units": 2,
                            # 广告销售额
                            "sales": 33.32,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 33.32,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                    # 分页游标
                    "next_token": "MTAwMDAwMDAwMDAwMjM=",
                }
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
        """查询SP广告组小时数据。

        ## Docs
        领星接口文档: 新广告 - 报告.[SP广告组小时数据](https://apidoc.lingxing.com/new/api-docs/newAd/report/spAdGroupHourData/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，按传入日期的年月日查询，建议提供完整YYYY-MM-DD。接口支持最近60天。
            campaign_id (int): 广告活动ID，可取同日日报或SpCampaigns返回的campaign_id。

        Returns:
            ads.schema.SpAdGroupHourData: 按小时返回，不提供分页参数。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpAdGroupHourData(campaign_id=70000000000006, report_date="2026-10-01")
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "操作成功",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-000000000177",
                    # 响应时间
                    "response_time": "2001-05-07 12:25:00",
                    # 响应数据量
                    "response_count": 21,
                    # 总数据量
                    "total_count": 21,
                    # SP 广告组小时数据列表
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 90000000000004,
                            # 广告活动ID
                            "campaign_id": 70000000000006,
                            # 广告组ID [原字段 'group_id']
                            "ad_group_id": 600000000000002,
                            # 广告花费
                            "cost": 1.5,
                            # 总展示次数
                            "impressions": 12,
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
                            "sales": 16.66,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 16.66,
                            # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                            "ctr": 0.0833,
                            # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                            "cvr": 1.0,
                            # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                            "cpc": 1.5,
                            # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                            "cpa": 1.5,
                            # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                            "acos": 0.09,
                            # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                            "roas": 11.11,
                            # 数据所属小时 (0-23)
                            "hour": 20,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                }
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
        """查询SP广告商品日报。

        ## Docs
        领星接口文档: 新广告 - 报告.[SP广告商品日报](https://apidoc.lingxing.com/new/api-docs/newAd/report/spProductAdReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，按传入日期的年月日查询，建议提供完整YYYY-MM-DD。
            sid (int): 领星店铺ID；与profile_id至少提供一项，使用profile_id查询时可显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id；使用sid查询时可显式传None。
            next_token (str | None): 上一页返回的游标，默认None；与offset同时提供时按游标定位。
            offset (int | None): 非负记录偏移量，默认None并省略，由接口采用0；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，由接口采用15；显式0保留。

        Returns:
            ads.schema.SpProductReports: 返回默认归因范围的日报指标，不提供完整归因期开关。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpProductReports(report_date="2026-10-01", sid=None, profile_id=90000000000007, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "操作成功",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-0000000000ea",
                    # 响应时间
                    "response_time": "2001-05-07 11:20:00",
                    # 响应数据量
                    "response_count": 2,
                    # 总数据量
                    "total_count": 33,
                    # SP 商品投放报告列表
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 90000000000007,
                            # 广告活动ID
                            "campaign_id": 70000000000305,
                            # 广告组ID
                            "ad_group_id": 600000000000013,
                            # 商品广告ID
                            "ad_id": 500000000000003,
                            # 商品ASIN
                            "asin": "A0AAAA0A7X",
                            # 亚马逊SKU [原字段 'sku']
                            "msku": "AA-000*3M",
                            # 广告花费
                            "cost": 2.64,
                            # 总展示次数
                            "impressions": 1106,
                            # 总点击次数
                            "clicks": 2,
                            # 广告订单数
                            "orders": 2,
                            # 直接广告订单数 [原字段 'same_orders']
                            "direct_orders": 2,
                            # 广告成交商品件数
                            "units": 2,
                            # 直接广告成交商品件数 [原字段 'same_units']
                            "direct_units": 2,
                            # 广告销售额
                            "sales": 33.32,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 33.32,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                    # 分页游标
                    "next_token": "MTAwMDAwMDAwMDAwMDA3",
                }
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
        """查询SP广告商品小时数据。

        ## Docs
        领星接口文档: 新广告 - 报告.[SP广告商品小时数据](https://apidoc.lingxing.com/new/api-docs/newAd/report/spAdvertiseHourData/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，按传入日期的年月日查询，建议提供完整YYYY-MM-DD。接口支持最近60天。
            campaign_id (int): 广告活动ID，可取同日日报或SpCampaigns返回的campaign_id。

        Returns:
            ads.schema.SpProductHourData: 按广告维度返回，不提供分页参数。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpProductHourData(campaign_id=70000000000006, report_date="2026-10-01")
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "操作成功",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-00000000005f",
                    # 响应时间
                    "response_time": "2001-05-07 12:27:00",
                    # 响应数据量
                    "response_count": 21,
                    # 总数据量
                    "total_count": 21,
                    # SP 商品投放小时数据列表
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 90000000000004,
                            # 广告活动ID
                            "campaign_id": 70000000000006,
                            # 广告组ID [原字段 'group_id']
                            "ad_group_id": 600000000000002,
                            # 商品广告ID
                            "ad_id": 500000000000002,
                            # 商品ASIN
                            "asin": "A0AAAA0A0F",
                            # 亚马逊SKU
                            "msku": "AA-000*0C",
                            # 广告花费
                            "cost": 1.5,
                            # 总展示次数
                            "impressions": 12,
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
                            "sales": 16.66,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 16.66,
                            # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                            "ctr": 0.0833,
                            # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                            "cvr": 1.0,
                            # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                            "cpc": 1.5,
                            # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                            "cpa": 1.5,
                            # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                            "acos": 0.09,
                            # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                            "roas": 11.11,
                            # 数据所属小时 (0-23)
                            "hour": 20,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                }
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
        """查询SP关键词日报。

        ## Docs
        领星接口文档: 新广告 - 报告.[SP关键词日报](https://apidoc.lingxing.com/new/api-docs/newAd/report/spKeywordReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，按传入日期的年月日查询，建议提供完整YYYY-MM-DD。
            sid (int): 领星店铺ID；与profile_id至少提供一项，使用profile_id查询时可显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id；使用sid查询时可显式传None。
            next_token (str | None): 上一页返回的游标，默认None；与offset同时提供时按游标定位。
            offset (int | None): 非负记录偏移量，默认None并省略，由接口采用0；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，由接口采用15；显式0保留。

        Returns:
            ads.schema.SpKeywordReports: 返回默认归因范围的日报指标，不提供完整归因期开关。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpKeywordReports(report_date="2026-10-01", sid=None, profile_id=90000000000007, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "操作成功",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-000000000066",
                    # 响应时间
                    "response_time": "2001-05-07 11:32:00",
                    # 响应数据量
                    "response_count": 2,
                    # 总数据量
                    "total_count": 180,
                    # SP 手动关键词投放报告列表
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 90000000000007,
                            # 广告活动ID
                            "campaign_id": 700000000000083,
                            # 广告组ID
                            "ad_group_id": 60000000000319,
                            # 关键词ID
                            "keyword_id": 4000000000012,
                            # 关键词文本
                            "keyword_text": "aa 000cb",
                            # 关键词匹配类型
                            "match_type": "EXACT",
                            # 广告花费
                            "cost": 0.0,
                            # 总展示次数
                            "impressions": 4,
                            # 总点击次数
                            "clicks": 0,
                            # 广告订单数
                            "orders": 0,
                            # 直接广告订单数 [原字段 'same_orders']
                            "direct_orders": 0,
                            # 广告成交商品件数
                            "units": 0,
                            # 直接广告成交商品件数 [原字段 'same_units']
                            "direct_units": 0,
                            # 广告销售额
                            "sales": 0.0,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 0.0,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                    # 分页游标
                    "next_token": "MTAwMDAwMDAwMDAxMQ==",
                }
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
        """查询SP关键词投放小时数据。

        ## Docs
        领星接口文档: 新广告 - 报告.[SP关键词投放小时数据](https://apidoc.lingxing.com/new/api-docs/newAd/report/spAdvertiseHourData/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，按传入日期的年月日查询，建议提供完整YYYY-MM-DD。接口支持最近60天。
            campaign_id (int): 广告活动ID，可取同日日报或SpCampaigns返回的campaign_id。

        Returns:
            ads.schema.SpKeywordHourData: 按广告及投放维度返回，不提供分页参数。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpKeywordHourData(campaign_id=70000000000006, report_date="2026-10-01")
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "操作成功",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-000000000096",
                    # 响应时间
                    "response_time": "2001-05-07 12:30:00",
                    # 响应数据量
                    "response_count": 21,
                    # 总数据量
                    "total_count": 21,
                    # SP 手动关键词投放小时数据列表
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 90000000000004,
                            # 广告活动ID
                            "campaign_id": 70000000000006,
                            # 广告组ID [原字段 'group_id']
                            "ad_group_id": 600000000000002,
                            # 商品广告ID
                            "ad_id": 500000000000002,
                            # 关键词ID [原字段 'targeting_id']
                            "keyword_id": 40000000000006,
                            # 关键词文本 [原字段 'targeting']
                            "keyword_text": "000 aaaac",
                            # 关键词匹配类型
                            "match_type": "BROAD",
                            # 商品ASIN
                            "asin": "A0AAAA0A0F",
                            # 亚马逊SKU
                            "msku": "AA-000*0C",
                            # 广告花费
                            "cost": 1.5,
                            # 总展示次数
                            "impressions": 12,
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
                            "sales": 16.66,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 16.66,
                            # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                            "ctr": 0.0833,
                            # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                            "cvr": 1.0,
                            # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                            "cpc": 1.5,
                            # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                            "cpa": 1.5,
                            # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                            "acos": 0.09,
                            # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                            "roas": 11.11,
                            # 数据所属小时 (0-23)
                            "hour": 20,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                }
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

    async def SpKeywordQueryReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpKeywordQueryReports:
        """查询SP关键词用户搜索词日报。

        ## Docs
        领星接口文档: 新广告 - 报告.[SP关键词用户搜索词日报](https://apidoc.lingxing.com/new/api-docs/newAd/report/queryWordReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，按传入日期的年月日查询，建议提供完整YYYY-MM-DD。
            sid (int): 领星店铺ID；与profile_id至少提供一项，使用profile_id查询时可显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id；使用sid查询时可显式传None。
            next_token (str | None): 上一页返回的游标，默认None；与offset同时提供时按游标定位。
            offset (int | None): 非负记录偏移量，默认None并省略，由接口采用0；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，由接口采用15；显式0保留。

        Returns:
            ads.schema.SpKeywordQueryReports: 返回默认归因范围的日报指标，不提供完整归因期开关。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpKeywordQueryReports(report_date="2026-10-01", sid=None, profile_id=90000000000007, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "操作成功",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-00000000009b",
                    # 响应时间
                    "response_time": "2001-05-07 11:44:00",
                    # 响应数据量
                    "response_count": 2,
                    # 总数据量
                    "total_count": 22,
                    # SP 手动关键词的用户搜索词报告列表
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 90000000000007,
                            # 广告活动ID
                            "campaign_id": 700000000000215,
                            # 广告组ID
                            "ad_group_id": 600000000000183,
                            # 用户使用搜索词 [原字段 'query']
                            "query_text": "aa 008",
                            # 广告花费
                            "cost": 1.35,
                            # 总展示次数
                            "impressions": 1,
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
                            "sales": 19.77,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 19.77,
                            # 报告日期
                            "report_date": "2026-10-01",
                            # 关键词ID [原字段 'target_id']
                            "keyword_id": 400000000000003,
                            # 关键词文本 [原字段 'target_text']
                            "keyword_text": "aa 0043",
                            # 关键词匹配类型
                            "match_type": "BROAD",
                        },
                        ...,
                    ],
                    # 分页游标
                    "next_token": "MDAwYWEwMDAwYTBhMGEwMDBhYWEwMDAwMDAwMGEwMmY=",
                }
        """
        url = route.SP_QUERY_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "show_detail": 0,
            "target_type": "keyword",
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.SpQueryReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SpKeywordQueryReports.model_validate(data)

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
        """查询SP商品投放日报。

        ## Docs
        领星接口文档: 新广告 - 报告.[SP商品投放日报](https://apidoc.lingxing.com/new/api-docs/newAd/report/spTargetReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，按传入日期的年月日查询，建议提供完整YYYY-MM-DD。
            sid (int): 领星店铺ID；与profile_id至少提供一项，使用profile_id查询时可显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id；使用sid查询时可显式传None。
            next_token (str | None): 上一页返回的游标，默认None；与offset同时提供时按游标定位。
            offset (int | None): 非负记录偏移量，默认None并省略，由接口采用0；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，由接口采用15；显式0保留。

        Returns:
            ads.schema.SpTargetReports: 返回默认归因范围的日报指标，不提供完整归因期开关。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpTargetReports(report_date="2026-10-01", sid=None, profile_id=90000000000007, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "操作成功",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-00000000009d",
                    # 响应时间
                    "response_time": "2001-05-07 11:56:00",
                    # 响应数据量
                    "response_count": 2,
                    # 总数据量
                    "total_count": 41,
                    # SP 自动投放/手动商品投放报告列表
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 90000000000007,
                            # 广告活动ID
                            "campaign_id": 700000000000227,
                            # 广告组ID
                            "ad_group_id": 600000000000287,
                            # 自动投放/手动商品投放ID
                            "target_id": 3000000000027,
                            # 投放匹配类型 [原字段 'targeting_type']
                            "expression_type": "TARGETING_EXPRESSION",
                            # 自动投放/手动商品投放表达式 (JSON 字符串)
                            "expression": "\\"[{\\\\\\"type\\\\\\": \\\\\\"asinExpandedFrom\\\\\\", \\\\\\"value\\\\\\": \\\\\\"0000000001\\\\\\"}]\\"",
                            # 广告花费
                            "cost": 0.0,
                            # 总展示次数
                            "impressions": 2,
                            # 总点击次数
                            "clicks": 0,
                            # 广告订单数
                            "orders": 0,
                            # 直接广告订单数 [原字段 'same_orders']
                            "direct_orders": 0,
                            # 广告成交商品件数
                            "units": 0,
                            # 直接广告成交商品件数 [原字段 'same_units']
                            "direct_units": 0,
                            # 广告销售额
                            "sales": 0.0,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 0.0,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                    # 分页游标
                    "next_token": "MTAwMDAwMDAwMDAyMQ==",
                }
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
        """查询SP投放小时数据。

        ## Docs
        领星接口文档: 新广告 - 报告.[SP投放小时数据](https://apidoc.lingxing.com/new/api-docs/newAd/report/spTargetHourData/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，按传入日期的年月日查询，建议提供完整YYYY-MM-DD。投放小时接口允许当天至向前第61天（含两端）。
            campaign_id (int): 广告活动ID，可取同日日报或SpCampaigns返回的campaign_id。

        Returns:
            ads.schema.SpTargetHourData: 按广告及投放维度返回，不提供分页参数。结果可包含关键词投放，未在本地按投放类型筛选。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpTargetHourData(campaign_id=70000000000006, report_date="2026-10-01")
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "操作成功",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-000000000072",
                    # 响应时间
                    "response_time": "2001-05-07 12:32:00",
                    # 响应数据量
                    "response_count": 21,
                    # 总数据量
                    "total_count": 21,
                    # SP投放小时数据列表
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 90000000000004,
                            # 广告活动ID
                            "campaign_id": 70000000000006,
                            # 广告组ID [原字段 'group_id']
                            "ad_group_id": 600000000000002,
                            # 商品广告ID
                            "ad_id": 500000000000002,
                            # 投放ID [原字段 'targeting_id']
                            "target_id": 40000000000006,
                            # 投放文本 [原字段 'targeting']
                            "target_text": "000 aaaac",
                            # 投放匹配类型 [原字段 'match_type']
                            "target_type": "BROAD",
                            # 商品ASIN
                            "asin": "A0AAAA0A0F",
                            # 亚马逊SKU
                            "msku": "AA-000*0C",
                            # 广告花费
                            "cost": 1.5,
                            # 总展示次数
                            "impressions": 12,
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
                            "sales": 16.66,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 16.66,
                            # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                            "ctr": 0.0833,
                            # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                            "cvr": 1.0,
                            # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                            "cpc": 1.5,
                            # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                            "cpa": 1.5,
                            # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                            "acos": 0.09,
                            # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                            "roas": 11.11,
                            # 数据所属小时 (0-23)
                            "hour": 20,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                }
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

    async def SpTargetQueryReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpTargetQueryReports:
        """查询SP商品投放及关键词组用户搜索词日报。

        ## Docs
        领星接口文档: 新广告 - 报告.[SP商品投放及关键词组用户搜索词日报](https://apidoc.lingxing.com/new/api-docs/newAd/report/queryWordReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，按传入日期的年月日查询，建议提供完整YYYY-MM-DD。
            sid (int): 领星店铺ID；与profile_id至少提供一项，使用profile_id查询时可显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id；使用sid查询时可显式传None。
            next_token (str | None): 上一页返回的游标，默认None；与offset同时提供时按游标定位。
            offset (int | None): 非负记录偏移量，默认None并省略，由接口采用0；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，由接口采用15；显式0保留。

        Returns:
            ads.schema.SpTargetQueryReports: 返回默认归因范围的日报指标，不提供完整归因期开关。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SpTargetQueryReports(report_date="2026-10-01", sid=None, profile_id=90000000000004, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "操作成功",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-000000000116",
                    # 响应时间
                    "response_time": "2001-05-07 12:08:00",
                    # 响应数据量
                    "response_count": 2,
                    # 总数据量
                    "total_count": 8,
                    # SP 自动投放/手动商品投的用户搜索词报告列表
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 90000000000004,
                            # 广告活动ID
                            "campaign_id": 700000000000007,
                            # 广告组ID
                            "ad_group_id": 600000000000003,
                            # 用户使用搜索词 [原字段 'query']
                            "query_text": "000 aaaaaaa aab",
                            # 广告花费
                            "cost": 1.6,
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
                            "sales": 16.66,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 16.66,
                            # 报告日期
                            "report_date": "2026-10-01",
                            # 自动投放/手动商品投放ID
                            "target_id": 30000000000004,
                            # 自动投放/手动商品投放表达式 (JSON 字符串) [原字段 'target_text']
                            "expression": "\\"[{\\\\\\"type\\\\\\": \\\\\\"keywordGroupSameAs\\\\\\", \\\\\\"value\\\\\\": \\\\\\"category\\\\\\"}]\\"",
                            # 投放匹配类型
                            "match_type": "",
                        },
                        ...,
                    ],
                    # 分页游标
                    "next_token": "MGEwMDAwMDBhMGFhMGEwMDAwMDAwMDAwYWEwYTAwMDE=",
                }
        """
        url = route.SP_QUERY_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "show_detail": 0,
            "target_type": "target",
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.SpQueryReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SpTargetQueryReports.model_validate(data)

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
        """查询SB广告活动日报。

        ## Docs
        领星接口文档: 新广告 - 报告.[SB广告活动日报](https://apidoc.lingxing.com/new/api-docs/newAd/report/hsaCampaignReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议提供完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            sid (int): 领星店铺ID，与profile_id至少提供一项；按profile_id查询时显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id。按sid查询时显式传None。
            next_token (str | None): 上一页返回的游标，默认None并省略。与offset同时提供时优先使用游标。
            offset (int | None): 非负记录偏移量，默认None并省略；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，接口默认15；显式0保留。

        Returns:
            ads.schema.SbCampaignReports: data集合仅展示首项，数量字段保留完整返回值。两账号标识同时提供时按profile_id定位。

        Raises:
            errors.InvalidParametersError: 请求参数不符合既有校验规则。
            errors.RequestError: 请求失败或服务端返回接口错误。
            pydantic.ValidationError: 返回内容不符合响应模型。

        Examples:
            查询报告并查看model_dump()返回的数据。

            .. code-block:: python

                result = await client.ads.SbCampaignReports(report_date="2026-10-01", sid=None, profile_id=900000000000001, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    "code": 0,
                    "message": "操作成功",
                    "errors": [],
                    "request_id": "00000000-0000-0000-0000-0000000000b1",
                    "response_time": "2001-05-07 12:41:00",
                    "response_count": 2,
                    "total_count": 5,
                    "data": [
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
                        },
                        ...,
                    ],
                    "next_token": "MTAwMDAwMDAwMDAwMDEw",
                }
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
        """查询SB广告活动小时数据。

        ## Docs
        领星接口文档: 新广告 - 报告.[SB广告活动小时数据](https://apidoc.lingxing.com/new/api-docs/newAd/report/sbCampaignHourData/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议提供完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            campaign_id (int): 广告活动ID；此方法只查询单个活动。接口支持最近60天。

        Returns:
            ads.schema.SbCampaignHourData: data集合仅展示首项，数量字段保留完整返回值。按小时返回，不提供分页参数。

        Raises:
            errors.InvalidParametersError: 请求参数不符合既有校验规则。
            errors.RequestError: 请求失败或服务端返回接口错误。
            pydantic.ValidationError: 返回内容不符合响应模型。

        Examples:
            查询报告并查看model_dump()返回的数据。

            .. code-block:: python

                result = await client.ads.SbCampaignHourData(report_date="2026-10-01", campaign_id=70000000000014)
                print(result.model_dump())

            .. code-block:: python

                {
                    "code": 0,
                    "message": "操作成功",
                    "errors": [],
                    "request_id": "00000000-0000-0000-0000-000000000159",
                    "response_time": "2001-05-07 14:17:00",
                    "response_count": 2,
                    "total_count": 2,
                    "data": [
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
                        },
                        ...,
                    ],
                }
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
        """查询SB广告活动广告位日报。

        ## Docs
        领星接口文档: 新广告 - 报告.[SB广告活动广告位日报](https://apidoc.lingxing.com/new/api-docs/newAd/report/hsaCampaignPlacementReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议提供完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            sid (int): 领星店铺ID，与profile_id至少提供一项；按profile_id查询时显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id。按sid查询时显式传None。
            next_token (str | None): 上一页返回的游标，默认None并省略。与offset同时提供时优先使用游标。
            offset (int | None): 非负记录偏移量，默认None并省略；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，接口默认15；显式0保留。

        Returns:
            ads.schema.SbPlacementReports: data集合仅展示首项，数量字段保留完整返回值。creative_type已被官方标为作废，创意类型应查询SB广告创意数据。两账号标识同时提供时按profile_id定位。

        Raises:
            errors.InvalidParametersError: 请求参数不符合既有校验规则。
            errors.RequestError: 请求失败或服务端返回接口错误。
            pydantic.ValidationError: 返回内容不符合响应模型。

        Examples:
            查询报告并查看model_dump()返回的数据。

            .. code-block:: python

                result = await client.ads.SbPlacementReports(report_date="2026-10-01", sid=None, profile_id=900000000000002, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    "code": 0,
                    "message": "操作成功",
                    "errors": [],
                    "request_id": "00000000-0000-0000-0000-000000000161",
                    "response_time": "2001-05-07 12:56:00",
                    "response_count": 2,
                    "total_count": 12,
                    "data": [
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
                        },
                        ...,
                    ],
                    "next_token": "MGFhMGFhMDBhYWEwMDAwYWEwMDAwYTAwYWEwMDAwMWM=",
                }
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
        """查询SB广告位小时数据。

        ## Docs
        领星接口文档: 新广告 - 报告.[SB广告位小时数据](https://apidoc.lingxing.com/new/api-docs/newAd/report/sbAdPlacementHourData/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议提供完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            campaign_id (int): 广告活动ID；此方法只查询单个活动。接口支持最近60天。

        Returns:
            ads.schema.SbPlacementHourData: data集合仅展示首项，数量字段保留完整返回值。按小时返回，不提供分页参数。

        Raises:
            errors.InvalidParametersError: 请求参数不符合既有校验规则。
            errors.RequestError: 请求失败或服务端返回接口错误。
            pydantic.ValidationError: 返回内容不符合响应模型。

        Examples:
            查询报告并查看model_dump()返回的数据。

            .. code-block:: python

                result = await client.ads.SbPlacementHourData(report_date="2026-10-01", campaign_id=70000000000014)
                print(result.model_dump())

            .. code-block:: python

                {
                    "code": 0,
                    "message": "操作成功",
                    "errors": [],
                    "request_id": "00000000-0000-0000-0000-00000000000f",
                    "response_time": "2001-05-07 14:20:00",
                    "response_count": 2,
                    "total_count": 2,
                    "data": [
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
                        },
                        ...,
                    ],
                }
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
        """查询SB广告组日报。

        ## Docs
        领星接口文档: 新广告 - 报告.[SB广告组日报](https://apidoc.lingxing.com/new/api-docs/newAd/report/hsaAdGroupReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议提供完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            sid (int): 领星店铺ID，与profile_id至少提供一项；按profile_id查询时显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id。按sid查询时显式传None。
            next_token (str | None): 上一页返回的游标，默认None并省略。与offset同时提供时优先使用游标。
            offset (int | None): 非负记录偏移量，默认None并省略；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，接口默认15；显式0保留。

        Returns:
            ads.schema.SbAdGroupReports: data集合仅展示首项，数量字段保留完整返回值。两账号标识同时提供时按profile_id定位。

        Raises:
            errors.InvalidParametersError: 请求参数不符合既有校验规则。
            errors.RequestError: 请求失败或服务端返回接口错误。
            pydantic.ValidationError: 返回内容不符合响应模型。

        Examples:
            查询报告并查看model_dump()返回的数据。

            .. code-block:: python

                result = await client.ads.SbAdGroupReports(report_date="2026-10-01", sid=None, profile_id=900000000000001, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    "code": 0,
                    "message": "操作成功",
                    "errors": [],
                    "request_id": "00000000-0000-0000-0000-000000000151",
                    "response_time": "2001-05-07 13:11:00",
                    "response_count": 2,
                    "total_count": 6,
                    "data": [
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
                        },
                        ...,
                    ],
                    "next_token": "MTAwMDAwMDIw",
                }
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
        """查询SB广告组小时数据。

        ## Docs
        领星接口文档: 新广告 - 报告.[SB广告组小时数据](https://apidoc.lingxing.com/new/api-docs/newAd/report/sbAdGroupHourData/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议提供完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            campaign_id (int): 广告活动ID；此方法只查询单个活动。接口支持最近60天。

        Returns:
            ads.schema.SbAdGroupHourData: data集合仅展示首项，数量字段保留完整返回值。按小时返回，不提供分页参数。

        Raises:
            errors.InvalidParametersError: 请求参数不符合既有校验规则。
            errors.RequestError: 请求失败或服务端返回接口错误。
            pydantic.ValidationError: 返回内容不符合响应模型。

        Examples:
            查询报告并查看model_dump()返回的数据。

            .. code-block:: python

                result = await client.ads.SbAdGroupHourData(report_date="2026-10-01", campaign_id=70000000000014)
                print(result.model_dump())

            .. code-block:: python

                {
                    "code": 0,
                    "message": "操作成功",
                    "errors": [],
                    "request_id": "00000000-0000-0000-0000-000000000163",
                    "response_time": "2001-05-07 14:23:00",
                    "response_count": 2,
                    "total_count": 2,
                    "data": [
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
                        },
                        ...,
                    ],
                }
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
        """查询SB广告创意日报。

        ## Docs
        领星接口文档: 新广告 - 报告.[SB广告创意日报](https://apidoc.lingxing.com/new/api-docs/newAd/report/listHsaProductAdReport/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议提供完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            sid (int): 领星店铺ID，与profile_id至少提供一项；按profile_id查询时显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id。按sid查询时显式传None。
            next_token (str | None): 上一页返回的游标，默认None并省略。与offset同时提供时优先使用游标。
            offset (int | None): 非负记录偏移量，默认None并省略；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，接口默认15；显式0保留。

        Returns:
            ads.schema.SbCreativeReports: data集合仅展示首项，数量字段保留完整返回值。两账号标识同时提供时按profile_id定位。

        Raises:
            errors.InvalidParametersError: 请求参数不符合既有校验规则。
            errors.RequestError: 请求失败或服务端返回接口错误。
            pydantic.ValidationError: 返回内容不符合响应模型。

        Examples:
            查询报告并查看model_dump()返回的数据。

            .. code-block:: python

                result = await client.ads.SbCreativeReports(report_date="2026-10-01", sid=None, profile_id=900000000000001, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    "code": 0,
                    "message": "操作成功",
                    "errors": [],
                    "request_id": "00000000-0000-0000-0000-0000000000c2",
                    "response_time": "2001-05-07 13:26:00",
                    "response_count": 2,
                    "total_count": 6,
                    "data": [
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
                        },
                        ...,
                    ],
                    "next_token": "MTAwMDAwMDE3",
                }
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
        """查询SB关键词投放日报。

        ## Docs
        领星接口文档: 新广告 - 报告.[SB关键词投放日报](https://apidoc.lingxing.com/new/api-docs/newAd/report/listHsaTargetingReport/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议提供完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            sid (int): 领星店铺ID，与profile_id至少提供一项；按profile_id查询时显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id。按sid查询时显式传None。
            next_token (str | None): 上一页返回的游标，默认None并省略。与offset同时提供时优先使用游标。
            offset (int | None): 非负记录偏移量，默认None并省略；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，接口默认10；显式0保留。

        Returns:
            ads.schema.SbKeywordReports: data集合仅展示首项，数量字段保留完整返回值。creative_type已被官方标为作废，创意类型应查询SB广告创意数据。两账号标识同时提供时按profile_id定位。

        Raises:
            errors.InvalidParametersError: 请求参数不符合既有校验规则。
            errors.RequestError: 请求失败或服务端返回接口错误。
            pydantic.ValidationError: 返回内容不符合响应模型。

        Examples:
            查询报告并查看model_dump()返回的数据。

            .. code-block:: python

                result = await client.ads.SbKeywordReports(report_date="2026-10-01", sid=None, profile_id=90000000000005, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    "code": 0,
                    "message": "操作成功",
                    "errors": [],
                    "request_id": "00000000-0000-0000-0000-00000000015a",
                    "response_time": "2001-05-07 13:39:00",
                    "response_count": 2,
                    "total_count": 100,
                    "data": [
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
                        },
                        ...,
                    ],
                    "next_token": "MTAwMDAwMDAwMDAzOQ==",
                }
        """
        url = route.SB_TARGETING_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "ad_type": "ALL",
            "target_type": "keyword",
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

    async def SbKeywordQueryReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbKeywordQueryReports:
        """查询SB关键词用户搜索词日报。

        ## Docs
        领星接口文档: 新广告 - 报告.[SB关键词用户搜索词日报](https://apidoc.lingxing.com/new/api-docs/newAd/report/hsaQueryWordReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议提供完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            sid (int): 领星店铺ID，与profile_id至少提供一项；按profile_id查询时显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id。按sid查询时显式传None。
            next_token (str | None): 上一页返回的游标，默认None并省略。与offset二选一；官方请求字段为nextToken。
            offset (int | None): 非负记录偏移量，默认None并省略；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，接口默认15；显式0保留。

        Returns:
            ads.schema.SbKeywordQueryReports: data集合仅展示首项，数量字段保留完整返回值。两账号标识同时提供时按profile_id定位。

        Raises:
            errors.InvalidParametersError: 请求参数不符合既有校验规则。
            errors.RequestError: 请求失败或服务端返回接口错误。
            pydantic.ValidationError: 返回内容不符合响应模型。

        Examples:
            查询报告并查看model_dump()返回的数据。

            .. code-block:: python

                result = await client.ads.SbKeywordQueryReports(report_date="2026-10-01", sid=None, profile_id=90000000000005, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    "code": 0,
                    "message": "操作成功",
                    "errors": [],
                    "request_id": "00000000-0000-0000-0000-00000000007a",
                    "response_time": "2001-05-07 13:45:00",
                    "response_count": 2,
                    "total_count": 6,
                    "data": [
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
                        },
                        ...,
                    ],
                    "next_token": "MDAwYWFhMGFhMGEwYTAwMDAwMGFhYWEwMDBhYTBhZTE=",
                }
        """
        url = route.SB_QUERY_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "target_type": "keyword",
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.SbQueryReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SbKeywordQueryReports.model_validate(data)

    async def SbKeywordPlacementReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbKeywordPlacementReports:
        """查询SB关键词广告位日报。

        ## Docs
        领星接口文档: 新广告 - 报告.[SB关键词广告位日报](https://apidoc.lingxing.com/new/api-docs/newAd/report/listHsaKeywordPlacementReport/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议提供完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            sid (int): 领星店铺ID，与profile_id至少提供一项；按profile_id查询时显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id。按sid查询时显式传None。
            next_token (str | None): 上一页返回的游标，默认None并省略。建议与offset分别使用。
            offset (int | None): 非负记录偏移量，默认None并省略；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，接口默认15；显式0保留。

        Returns:
            ads.schema.SbKeywordPlacementReports: data集合仅展示首项，数量字段保留完整返回值。

        Raises:
            errors.InvalidParametersError: 请求参数不符合既有校验规则。
            errors.RequestError: 请求失败或服务端返回接口错误。
            pydantic.ValidationError: 返回内容不符合响应模型。

        Examples:
            查询报告并查看model_dump()返回的数据。

            .. code-block:: python

                result = await client.ads.SbKeywordPlacementReports(report_date="2026-10-01", sid=None, profile_id=9000000000000005, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    "code": 0,
                    "message": "操作成功",
                    "errors": [],
                    "request_id": "00000000-0000-0000-0000-000000000158",
                    "response_time": "2001-05-07 14:27:00",
                    "response_count": 2,
                    "total_count": 21,
                    "data": [
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
                        },
                        ...,
                    ],
                    "next_token": "MTAwMDAwMDAwMDAwMDE3",
                }
        """
        url = route.SB_KEYWORD_PLACEMENT_REPORTS
        # 解析并验证参数
        args = {
            "sid": sid,
            "profile_id": profile_id,
            "sponsored_type": "ALL",
            "target_type": "keyword",
            "report_date": report_date,
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
        return schema.SbKeywordPlacementReports.model_validate(data)

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
        """查询SB商品投放日报。

        ## Docs
        领星接口文档: 新广告 - 报告.[SB商品投放日报](https://apidoc.lingxing.com/new/api-docs/newAd/report/listHsaTargetingReport/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议提供完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            sid (int): 领星店铺ID，与profile_id至少提供一项；按profile_id查询时显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id。按sid查询时显式传None。
            next_token (str | None): 上一页返回的游标，默认None并省略。建议与offset分别使用。
            offset (int | None): 非负记录偏移量，默认None并省略；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，接口默认10；显式0保留。

        Returns:
            ads.schema.SbTargetReports: data集合仅展示首项，数量字段保留完整返回值。creative_type已被官方标为作废，创意类型应查询SB广告创意数据。

        Raises:
            errors.InvalidParametersError: 请求参数不符合既有校验规则。
            errors.RequestError: 请求失败或服务端返回接口错误。
            pydantic.ValidationError: 返回内容不符合响应模型。

        Examples:
            查询报告并查看model_dump()返回的数据。

            .. code-block:: python

                result = await client.ads.SbTargetReports(report_date="2026-10-01", sid=None, profile_id=9000000000000003, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    "code": 0,
                    "message": "操作成功",
                    "errors": [],
                    "request_id": "00000000-0000-0000-0000-000000000093",
                    "response_time": "2001-05-07 14:40:00",
                    "response_count": 2,
                    "total_count": 14,
                    "data": [
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
                        },
                        ...,
                    ],
                    "next_token": "MTAwMDAwMDAwMDAwNTE=",
                }
        """
        url = route.SB_TARGETING_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "ad_type": "ALL",
            "target_type": "product",
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

    async def SbTargetQueryReports(
        self,
        report_date: str | datetime.date | datetime.datetime,
        sid: int,
        profile_id: int,
        *,
        next_token: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SbTargetQueryReports:
        """查询SB商品投放用户搜索词日报。

        ## Docs
        领星接口文档: 新广告 - 报告.[SB商品投放用户搜索词日报](https://apidoc.lingxing.com/new/api-docs/newAd/report/hsaQueryWordReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议提供完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            sid (int): 领星店铺ID，与profile_id至少提供一项；按profile_id查询时显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id。按sid查询时显式传None。
            next_token (str | None): 上一页返回的游标，默认None并省略。与offset二选一；官方请求字段为nextToken。
            offset (int | None): 非负记录偏移量，默认None并省略；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，接口默认15；显式0保留。

        Returns:
            ads.schema.SbTargetQueryReports: data集合展示一条完整记录，数量字段保留完整返回值。

        Raises:
            errors.InvalidParametersError: 请求参数不符合既有校验规则。
            errors.RequestError: 请求失败或服务端返回接口错误。
            pydantic.ValidationError: 返回内容不符合响应模型。

        Examples:
            查询报告并查看model_dump()返回的数据。

            .. code-block:: python

                result = await client.ads.SbTargetQueryReports(report_date="2026-10-01", sid=None, profile_id=9000000000000001, offset=4, length=200)
                print(result.model_dump())

            .. code-block:: python

                {
                    "code": 0,
                    "message": "操作成功",
                    "errors": [],
                    "request_id": "00000000-0000-0000-0000-00000000000c",
                    "response_time": "2001-05-07 13:57:00",
                    "response_count": 18,
                    "total_count": 22,
                    "data": [
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
                        },
                        ...,
                    ],
                    "next_token": "YTAwYTBhYWEwMGEwYWEwMDAwMDAwMGFhYWEwMGEwNDk=",
                }
        """
        url = route.SB_QUERY_REPORTS
        # 解析并验证参数
        args = {
            "report_date": report_date,
            "sid": sid,
            "profile_id": profile_id,
            "target_type": "target",
            "next_token": next_token,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.SbQueryReports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body=p.model_dump_params(), headers={"X-API-VERSION": "2"}
        )
        return schema.SbTargetQueryReports.model_validate(data)

    async def SbTargetingHourData(
        self,
        report_date: str | datetime.date | datetime.datetime,
        campaign_id: int,
    ) -> schema.SbTargetingHourData:
        """查询SB投放小时数据。

        ## Docs
        领星接口文档: 新广告 - 报告.[SB投放小时数据](https://apidoc.lingxing.com/new/api-docs/newAd/report/sbTargetHourData/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议提供完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            campaign_id (int): 广告活动ID；此方法只查询单个活动。接口支持最近60天。

        Returns:
            ads.schema.SbTargetingHourData: data集合仅展示首项，数量字段保留完整返回值。按小时返回，不提供分页参数。聚合维度固定为target；SDK不按关键词或商品投放类型进行本地筛选。

        Raises:
            errors.InvalidParametersError: 请求参数不符合既有校验规则。
            errors.RequestError: 请求失败或服务端返回接口错误。
            pydantic.ValidationError: 返回内容不符合响应模型。

        Examples:
            查询报告并查看model_dump()返回的数据。

            .. code-block:: python

                result = await client.ads.SbTargetingHourData(report_date="2026-10-01", campaign_id=700000000000004)
                print(result.model_dump())

            .. code-block:: python

                {
                    "code": 0,
                    "message": "操作成功",
                    "errors": [],
                    "request_id": "00000000-0000-0000-0000-000000000100",
                    "response_time": "2001-05-07 14:24:00",
                    "response_count": 150,
                    "total_count": 150,
                    "data": [
                        {
                            "profile_id": 9000000000000003,
                            "campaign_id": 700000000000004,
                            "ad_group_id": 600000000000008,
                            "targeting_id": 300000000000002,
                            "targeting_text": "asin=\\"A00AAAAA0C\\"",
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
                        },
                        ...,
                    ],
                }
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
        """查询SB已购买商品归因日报。

        ## Docs
        领星接口文档: 新广告 - 报告.[SB已购买商品归因日报](https://apidoc.lingxing.com/new/api-docs/newAd/report/hsaPurchasedAsinReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议提供完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            sid (int): 领星店铺ID，与profile_id至少提供一项；按profile_id查询时显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id。按sid查询时显式传None。
            next_token (str | None): 上一页返回的游标，默认None并省略。与offset同时提供时优先使用游标。
            offset (int | None): 非负记录偏移量，默认None并省略；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，接口默认15；显式0保留。

        Returns:
            ads.schema.SbAsinAttributionReports: data集合仅展示首项，数量字段保留完整返回值。返回14天归因指标；非SB2活动的空ID沿用模型既有转换规则。两账号标识同时提供时按profile_id定位。

        Raises:
            errors.InvalidParametersError: 请求参数不符合既有校验规则。
            errors.RequestError: 请求失败或服务端返回接口错误。
            pydantic.ValidationError: 返回内容不符合响应模型。

        Examples:
            查询报告并查看model_dump()返回的数据。

            .. code-block:: python

                result = await client.ads.SbAsinAttributionReports(report_date="2026-10-01", sid=None, profile_id=900000000000002, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    "code": 0,
                    "message": "操作成功",
                    "errors": [],
                    "request_id": "00000000-0000-0000-0000-000000000033",
                    "response_time": "2001-05-07 14:10:00",
                    "response_count": 1,
                    "total_count": 1,
                    "data": [
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
                        },
                    ],
                    "next_token": "MTAwMDAwMzY=",
                }
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
        """查询SB广告费用分摊日报。

        ## Docs
        领星接口文档: 新广告 - 报告.[SB广告费用分摊日报](https://apidoc.lingxing.com/new/api-docs/newAd/baseData/newadsbDivideAsinReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议提供完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id。
            next_token (str | None): 上一页返回的游标，默认None并省略。与offset同时提供时优先使用游标。
            offset (int | None): 非负记录偏移量，默认None并省略；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，接口默认15；显式0保留。

        Returns:
            ads.schema.SbCostAllocationReports: data集合仅展示首项，数量字段保留完整返回值。

        Raises:
            errors.InvalidParametersError: 请求参数不符合既有校验规则。
            errors.RequestError: 请求失败或服务端返回接口错误。
            pydantic.ValidationError: 返回内容不符合响应模型。

        Examples:
            查询报告并查看model_dump()返回的数据。

            .. code-block:: python

                result = await client.ads.SbCostAllocationReports(report_date="2026-10-01", profile_id=900000000000001, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    "code": 0,
                    "message": "操作成功",
                    "errors": [],
                    "request_id": "00000000-0000-0000-0000-0000000000bc",
                    "response_time": "2001-05-07 14:04:00",
                    "response_count": 2,
                    "total_count": 261,
                    "data": [
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
                        },
                        ...,
                    ],
                    "next_token": "MTAwMDAwMDMx",
                }
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
        """查询SD广告活动报表。

        ## Docs
        领星接口文档: 新广告 - 报告.[SD广告活动报表](https://apidoc.lingxing.com/new/api-docs/newAd/report/sdCampaignReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议使用完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            sid (int): 领星店铺ID，与profile_id至少提供一项；按profile_id查询时显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id；按sid查询时显式传None。
            next_token (str | None): 上一页返回的分页游标，默认None并省略；同时提供offset时两项均发送。
            offset (int | None): 非负分页偏移量，默认None并省略，接口默认0；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，接口默认15；显式0保留。

        Returns:
            ads.schema.SdCampaignReports: 返回SD广告活动报表的默认归因数据。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SdCampaignReports(report_date="2026-10-01", sid=None, profile_id=9000000000000005, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "success",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-000000000056",
                    # 响应时间
                    "response_time": "2001-05-07 14:56:00",
                    # 响应数据量
                    "response_count": 2,
                    # 总数据量
                    "total_count": 2,
                    # 响应数据
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 9000000000000005,
                            # 广告活动ID
                            "campaign_id": 700000000000293,
                            # 投放策略
                            "tactic": "T00030",
                            # 广告花费
                            "cost": 11.13,
                            # 总展示次数
                            "impressions": 3250,
                            # 可见展示次数 [原字段 'view_impressions']
                            "viewable_impressions": 96,
                            # 总点击次数
                            "clicks": 30,
                            # 广告订单数
                            "orders": 0,
                            # 直接广告订单数 [原字段 'same_orders']
                            "direct_orders": 0,
                            # 广告成交商品件数
                            "units": 0,
                            # 广告销售额
                            "sales": 0.0,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 0.0,
                            # 品牌新客14天订单数
                            "new_to_brand_orders_14d": 0,
                            # 品牌新客14天商品件数
                            "new_to_brand_units_14d": 0,
                            # 品牌新客14天销售额
                            "new_to_brand_sales_14d": 0.0,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                    # 分页游标
                    "next_token": "MjgxNTExNTQ0MTc4ODM1",
                }
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
        """查询SD广告活动小时数据。

        ## Docs
        领星接口文档: 新广告 - 报告.[SD广告活动小时数据](https://apidoc.lingxing.com/new/api-docs/newAd/report/sdCampaignHourData/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议使用完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。接口仅支持最近60天。
            campaign_id (int): 单个广告活动ID，来源为SdCampaign.campaign_id。

        Returns:
            ads.schema.SdCampaignHourData: 返回SD广告活动小时数据。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SdCampaignHourData(report_date="2026-10-01", campaign_id=700000000000293)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "success",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-00000000005c",
                    # 响应时间
                    "response_time": "2001-05-07 15:08:00",
                    # 响应数据量
                    "response_count": 2,
                    # 总数据量
                    "total_count": 2,
                    # 响应数据
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 9000000000000005,
                            # 广告活动ID
                            "campaign_id": 700000000000293,
                            # 广告花费
                            "cost": 0.22,
                            # 总展示次数
                            "impressions": 259,
                            # 总点击次数
                            "clicks": 2,
                            # 广告订单数
                            "orders": 0,
                            # 直接广告订单数 [原字段 'same_orders']
                            "direct_orders": 0,
                            # 广告成交商品件数
                            "units": 0,
                            # 广告销售额
                            "sales": 0.0,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 0.0,
                            # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                            "ctr": 0.0077,
                            # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                            "cvr": 0.0,
                            # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                            "cpc": 0.11,
                            # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                            "cpa": 0.0,
                            # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                            "acos": 0.0,
                            # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                            "roas": 0.0,
                            # 数据所属小时 (0-23)
                            "hour": 0,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                }
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
        """查询SD广告组报表。

        ## Docs
        领星接口文档: 新广告 - 报告.[SD广告组报表](https://apidoc.lingxing.com/new/api-docs/newAd/report/sdAdGroupReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议使用完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            sid (int): 领星店铺ID，与profile_id至少提供一项；按profile_id查询时显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id；按sid查询时显式传None。
            next_token (str | None): 上一页返回的分页游标，默认None并省略；同时提供offset时两项均发送。
            offset (int | None): 非负分页偏移量，默认None并省略，接口默认0；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，接口默认15；显式0保留。

        Returns:
            ads.schema.SdAdGroupReports: 返回SD广告组报表的默认归因数据。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SdAdGroupReports(report_date="2026-10-01", sid=None, profile_id=9000000000000005, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "success",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-000000000170",
                    # 响应时间
                    "response_time": "2001-05-07 15:11:00",
                    # 响应数据量
                    "response_count": 2,
                    # 总数据量
                    "total_count": 2,
                    # 响应数据
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 9000000000000005,
                            # 广告活动ID
                            "campaign_id": 700000000000293,
                            # 广告组ID
                            "ad_group_id": 600000000000338,
                            # 投放策略
                            "tactic": "T00030",
                            # 广告花费
                            "cost": 11.13,
                            # 总展示次数
                            "impressions": 3250,
                            # 可见展示次数 [原字段 'view_impressions']
                            "viewable_impressions": 96,
                            # 总点击次数
                            "clicks": 30,
                            # 广告订单数
                            "orders": 0,
                            # 直接广告订单数 [原字段 'same_orders']
                            "direct_orders": 0,
                            # 广告成交商品件数
                            "units": 0,
                            # 广告销售额
                            "sales": 0.0,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 0.0,
                            # 品牌新客14天订单数
                            "new_to_brand_orders_14d": 0,
                            # 品牌新客14天商品件数
                            "new_to_brand_units_14d": 0,
                            # 品牌新客14天销售额
                            "new_to_brand_sales_14d": 0.0,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                    # 分页游标
                    "next_token": "MjgxNTExNTQ0MTc4ODM1",
                }
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
        """查询SD广告组小时数据。

        ## Docs
        领星接口文档: 新广告 - 报告.[SD广告组小时数据](https://apidoc.lingxing.com/new/api-docs/newAd/report/sdAdGroupHourData/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议使用完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。接口仅支持最近60天。
            campaign_id (int): 单个广告活动ID，来源为SdCampaign.campaign_id。

        Returns:
            ads.schema.SdAdGroupHourData: 返回SD广告组小时数据。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SdAdGroupHourData(report_date="2026-10-01", campaign_id=700000000000293)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "success",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-00000000003c",
                    # 响应时间
                    "response_time": "2001-05-07 15:24:00",
                    # 响应数据量
                    "response_count": 2,
                    # 总数据量
                    "total_count": 2,
                    # 响应数据
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 9000000000000005,
                            # 广告活动ID
                            "campaign_id": 700000000000293,
                            # 广告组ID [原字段 'group_id']
                            "ad_group_id": 600000000000338,
                            # 广告花费
                            "cost": 0.22,
                            # 总展示次数
                            "impressions": 259,
                            # 总点击次数
                            "clicks": 2,
                            # 广告订单数
                            "orders": 0,
                            # 直接广告订单数 [原字段 'same_orders']
                            "direct_orders": 0,
                            # 广告成交商品件数
                            "units": 0,
                            # 广告销售额
                            "sales": 0.0,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 0.0,
                            # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                            "ctr": 0.0077,
                            # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                            "cvr": 0.0,
                            # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                            "cpc": 0.11,
                            # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                            "cpa": 0.0,
                            # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                            "acos": 0.0,
                            # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                            "roas": 0.0,
                            # 数据所属小时 (0-23)
                            "hour": 0,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                }
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
        """查询SD广告商品报表。

        ## Docs
        领星接口文档: 新广告 - 报告.[SD广告商品报表](https://apidoc.lingxing.com/new/api-docs/newAd/report/sdProductAdReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议使用完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            sid (int): 领星店铺ID，与profile_id至少提供一项；按profile_id查询时显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id；按sid查询时显式传None。
            next_token (str | None): 上一页返回的分页游标，默认None并省略；同时提供offset时两项均发送。
            offset (int | None): 非负分页偏移量，默认None并省略，接口默认0；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，接口默认15；显式0保留。

        Returns:
            ads.schema.SdProductReports: 返回SD广告商品报表的默认归因数据。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SdProductReports(report_date="2026-10-01", sid=None, profile_id=9000000000000005, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "success",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-00000000018d",
                    # 响应时间
                    "response_time": "2001-05-07 15:26:00",
                    # 响应数据量
                    "response_count": 2,
                    # 总数据量
                    "total_count": 2,
                    # 响应数据
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 9000000000000005,
                            # 广告活动ID
                            "campaign_id": 700000000000293,
                            # 广告组ID
                            "ad_group_id": 600000000000338,
                            # 商品广告ID
                            "ad_id": 500000000000223,
                            # 投放策略
                            "tactic": "T00030",
                            # 商品ASIN
                            "asin": "A0A00AAAIT",
                            # 亚马逊SKU [原字段 'sku']
                            "msku": "000-00-AA-00AA-0A-BI",
                            # 广告花费
                            "cost": 0.99,
                            # 总展示次数
                            "impressions": 325,
                            # 可见展示次数 [原字段 'view_impressions']
                            "viewable_impressions": 9,
                            # 总点击次数
                            "clicks": 2,
                            # 广告订单数
                            "orders": 0,
                            # 直接广告订单数 [原字段 'same_orders']
                            "direct_orders": 0,
                            # 广告成交商品件数
                            "units": 0,
                            # 广告销售额
                            "sales": 0.0,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 0.0,
                            # 品牌新客14天订单数
                            "new_to_brand_orders_14d": 0,
                            # 品牌新客14天商品件数
                            "new_to_brand_units_14d": 0,
                            # 品牌新客14天销售额
                            "new_to_brand_sales_14d": 0.0,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                    # 分页游标
                    "next_token": "MjgxNTExNTQ0MTc4ODM1",
                }
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
        """查询SD广告小时数据。

        ## Docs
        领星接口文档: 新广告 - 报告.[SD广告小时数据](https://apidoc.lingxing.com/new/api-docs/newAd/report/sdAdvertiseHourData/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议使用完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。接口仅支持最近60天。
            campaign_id (int): 单个广告活动ID，来源为SdCampaign.campaign_id；固定按广告维度聚合。

        Returns:
            ads.schema.SdProductHourData: 返回SD广告小时数据。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SdProductHourData(report_date="2026-10-01", campaign_id=700000000000293)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "success",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-0000000000c6",
                    # 响应时间
                    "response_time": "2001-05-07 15:39:00",
                    # 响应数据量
                    "response_count": 2,
                    # 总数据量
                    "total_count": 2,
                    # 响应数据
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 9000000000000005,
                            # 广告活动ID
                            "campaign_id": 700000000000293,
                            # 广告组ID [原字段 'group_id']
                            "ad_group_id": 600000000000338,
                            # 商品广告ID
                            "ad_id": 500000000000468,
                            # 商品ASIN
                            "asin": "A00AAAAA6N",
                            # 亚马逊SKU
                            "msku": "000-00-AA-00AA-0A0A-0BB",
                            # 广告花费
                            "cost": 0.36,
                            # 总展示次数
                            "impressions": 159,
                            # 总点击次数
                            "clicks": 3,
                            # 广告订单数
                            "orders": 0,
                            # 直接广告订单数 [原字段 'same_orders']
                            "direct_orders": 0,
                            # 广告成交商品件数
                            "units": 0,
                            # 广告销售额
                            "sales": 0.0,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 0.0,
                            # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                            "ctr": 0.0189,
                            # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                            "cvr": 0.0,
                            # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                            "cpc": 0.12,
                            # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                            "cpa": 0.0,
                            # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                            "acos": 0.0,
                            # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                            "roas": 0.0,
                            # 数据所属小时 (0-23)
                            "hour": 2,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                }
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
        """查询SD商品定位报表。

        ## Docs
        领星接口文档: 新广告 - 报告.[SD商品定位报表](https://apidoc.lingxing.com/new/api-docs/newAd/report/sdTargetReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议使用完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            sid (int): 领星店铺ID，与profile_id至少提供一项；按profile_id查询时显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id；按sid查询时显式传None。
            next_token (str | None): 上一页返回的分页游标，默认None并省略；同时提供offset时两项均发送。
            offset (int | None): 非负分页偏移量，默认None并省略，接口默认0；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，接口默认15；显式0保留。

        Returns:
            ads.schema.SdTargetReports: 返回SD商品定位报表的默认归因数据。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SdTargetReports(report_date="2026-10-01", sid=None, profile_id=90000000000009, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "success",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-00000000019b",
                    # 响应时间
                    "response_time": "2001-05-07 15:41:00",
                    # 响应数据量
                    "response_count": 2,
                    # 总数据量
                    "total_count": 2,
                    # 响应数据
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 90000000000009,
                            # 广告活动ID
                            "campaign_id": 700000000000175,
                            # 广告组ID
                            "ad_group_id": 600000000000306,
                            # 目标商品广告ID
                            "target_id": 300000000000020,
                            # 目标商品文本 [原字段 'targeting_expression']
                            "target_text": "purchases=(exact-product lookback=365)",
                            # 目标定位类型 [原字段 'targeting_type']
                            "expression_type": "",
                            # 目标定位表达式 (JSON 字符串) [原字段 'targeting_text']
                            "expression": "\\"[{\\\\\\"type\\\\\\": \\\\\\"purchases\\\\\\", \\\\\\"value\\\\\\": [{\\\\\\"type\\\\\\": \\\\\\"exactProduct\\\\\\"}, {\\\\\\"type\\\\\\": \\\\\\"lookback\\\\\\", \\\\\\"value\\\\\\": \\\\\\"365\\\\\\"}]}]\\"",
                            # 投放策略
                            "tactic": "T00030",
                            # 广告花费
                            "cost": 0.94,
                            # 总展示次数
                            "impressions": 101,
                            # 可见展示次数 [原字段 'view_impressions']
                            "viewable_impressions": 0,
                            # 总点击次数
                            "clicks": 2,
                            # 广告订单数
                            "orders": 0,
                            # 直接广告订单数 [原字段 'same_orders']
                            "direct_orders": 0,
                            # 广告成交商品件数
                            "units": 0,
                            # 广告销售额
                            "sales": 0.0,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 0.0,
                            # 品牌新客14天订单数
                            "new_to_brand_orders_14d": 0,
                            # 品牌新客14天商品件数
                            "new_to_brand_units_14d": 0,
                            # 品牌新客14天销售额
                            "new_to_brand_sales_14d": 0.0,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                    # 分页游标
                    "next_token": "MjgxNTExNTQ0MTc4ODM1",
                }
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
        """查询SD投放小时数据。

        ## Docs
        领星接口文档: 新广告 - 报告.[SD投放小时数据](https://apidoc.lingxing.com/new/api-docs/newAd/report/sdTargetHourData/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议使用完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。接口仅支持最近60天。
            campaign_id (int): 单个广告活动ID，来源为SdCampaign.campaign_id；固定按广告与投放组合维度聚合。

        Returns:
            ads.schema.SdTargetHourData: 返回SD投放小时数据。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SdTargetHourData(report_date="2026-10-01", campaign_id=700000000000293)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "success",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-000000000165",
                    # 响应时间
                    "response_time": "2001-05-07 15:54:00",
                    # 响应数据量
                    "response_count": 2,
                    # 总数据量
                    "total_count": 2,
                    # 响应数据
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 9000000000000005,
                            # 广告活动ID
                            "campaign_id": 700000000000293,
                            # 广告组ID [原字段 'group_id']
                            "ad_group_id": 600000000000338,
                            # 商品广告ID
                            "ad_id": 500000000000534,
                            # 目标商品广告ID [原字段 'targeting_id']
                            "target_id": 30000000000050,
                            # 目标定位文本 [原字段 'targeting']
                            "target_text": "views=(similar-product lookback=90)",
                            # 商品ASIN
                            "asin": "A000AA0ACR",
                            # 亚马逊SKU
                            "msku": "000-00-AA-AAAA-00AA-0A-AW",
                            # 广告花费
                            "cost": 0.1,
                            # 总展示次数
                            "impressions": 8,
                            # 总点击次数
                            "clicks": 1,
                            # 广告订单数
                            "orders": 0,
                            # 直接广告订单数 [原字段 'same_orders']
                            "direct_orders": 0,
                            # 广告成交商品件数
                            "units": 0,
                            # 广告销售额
                            "sales": 0.0,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 0.0,
                            # 点击率 - Click Through Rate (总点击次数 / 总展示次数)
                            "ctr": 0.125,
                            # 转化率 - Conversion Rate (广告订单数 / 总点击次数)
                            "cvr": 0.0,
                            # 平均点击花费 - Cost Per Click (广告花费 / 总点击次数)
                            "cpc": 0.1,
                            # 平均订单花费 - Cost Per Acquisition (广告花费 / 广告订单数)
                            "cpa": 0.0,
                            # 广告花费占比 - Ad Cost of Sales (广告花费 / 广告销售额)
                            "acos": 0.0,
                            # 广告投入回报 - Return On Ad Spend (广告销售额 / 广告花费)
                            "roas": 0.0,
                            # 数据所属小时 (0-23)
                            "hour": 2,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                }
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
        """查询SD匹配的目标报表。

        ## Docs
        领星接口文档: 新广告 - 报告.[SD匹配的目标报表](https://apidoc.lingxing.com/new/api-docs/newAd/report/sdMatchTargetReports/)

        Args:
            report_date (str | datetime.date | datetime.datetime): 报告日期，建议使用完整YYYY-MM-DD；按输入日期的年月日查询，不额外换算时区。
            sid (int): 领星店铺ID，与profile_id至少提供一项；按profile_id查询时显式传None。
            profile_id (int): 广告账号ID，来源为AdProfiles.profile_id；按sid查询时显式传None。
            next_token (str | None): 上一页返回的分页游标，默认None并省略；同时提供offset时两项均发送。
            offset (int | None): 非负分页偏移量，默认None并省略，接口默认0；显式0保留。
            length (int | None): 非负分页长度，默认None并省略，接口默认15；显式0保留。

        Returns:
            ads.schema.SdMatchedTargetReports: 返回在ASIN商品详情页展示且发生点击的匹配目标默认归因数据。

        Examples:
            查询报告并查看返回数据。

            .. code-block:: python

                result = await client.ads.SdMatchedTargetReports(report_date="2026-10-01", sid=None, profile_id=9000000000000005, offset=0, length=2)
                print(result.model_dump())

            .. code-block:: python

                {
                    # 状态码
                    "code": 0,
                    # 提示信息
                    "message": "success",
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": "00000000-0000-0000-0000-0000000000cb",
                    # 响应时间
                    "response_time": "2001-05-07 15:57:00",
                    # 响应数据量
                    "response_count": 2,
                    # 总数据量
                    "total_count": 2,
                    # 响应数据
                    "data": [
                        {
                            # 亚马逊店铺ID (广告帐号ID)
                            "profile_id": 9000000000000005,
                            # 广告活动ID
                            "campaign_id": 700000000000293,
                            # 广告组ID
                            "ad_group_id": 600000000000338,
                            # 目标商品广告ID
                            "target_id": 300000000000009,
                            # 目标定位表达式 (JSON 字符串) [原字段 'target_text']
                            "expression": "\\"[{\\\\\\"type\\\\\\": \\\\\\"views\\\\\\", \\\\\\"value\\\\\\": [{\\\\\\"type\\\\\\": \\\\\\"exactProduct\\\\\\"}, {\\\\\\"type\\\\\\": \\\\\\"lookback\\\\\\", \\\\\\"value\\\\\\": \\\\\\"30\\\\\\"}]}]\\"",
                            # 匹配的目标商品 (ASIN)
                            "matched_target": "A00AAAAAAV",
                            # 货币代码 [原字段 'currency']
                            "currency_code": "",
                            # 广告花费
                            "cost": 1.98,
                            # 总展示次数
                            "impressions": 2,
                            # 可见展示次数 [原字段 'view_impressions']
                            "viewable_impressions": 0,
                            # 总点击次数
                            "clicks": 1,
                            # 广告订单数
                            "orders": 0,
                            # 直接广告订单数 [原字段 'same_orders']
                            "direct_orders": 0,
                            # 品牌新买家广告订单数
                            "new_to_brand_orders": 0,
                            # 广告成交商品件数
                            "units": 0,
                            # 品牌新买家成交商品件数
                            "new_to_brand_units": 0,
                            # 广告销售额
                            "sales": 0.0,
                            # 直接广告销售额 [原字段 'same_sales']
                            "direct_sales": 0.0,
                            # 品牌新买家销售额
                            "new_to_brand_sales": 0.0,
                            # 报告日期
                            "report_date": "2026-10-01",
                        },
                        ...,
                    ],
                    # 分页游标
                    "next_token": "MjgxNTExNTQ0MTc4ODM1",
                }
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
