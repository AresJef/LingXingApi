# -*- coding: utf-8 -*-c
import datetime
from decimal import Decimal
from lingxingapi import errors
from lingxingapi.base.api import BaseAPI
from lingxingapi.base import schema as base_schema
from lingxingapi.basic import param, route, schema


# API ------------------------------------------------------------------------------------------------------------------
class BasicAPI(BaseAPI):
    """领星API `基础数据` 接口

    ## Notice
    请勿直接实例化此类
    """

    # 公共 API --------------------------------------------------------------------------------------
    # . 基础数据
    async def Marketplaces(self) -> schema.Marketplaces:
        """查询所有的亚马逊站点信息。

        ## Docs
        领星接口文档: 基础数据.[查询亚马逊市场列表](https://apidoc.lingxing.com/#/docs/BasicData/AllMarketplace)

        Returns:
            basic.schema.Marketplaces: 所有亚马逊站点的查询结果。

        Examples:
            查询亚马逊站点并查看返回数据。

            .. code-block:: python

                result = await client.basic.Marketplaces()
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
                    "request_id": "123B44C1-ECBC-251A-D3F9-E0D49B2DEC85",
                    # 响应时间
                    "response_time": "2001-05-07 05:14:42",
                    # 响应数据量
                    "response_count": 23,
                    # 总数据量
                    "total_count": 23,
                    # 响应数据
                    "data": [
                        {
                            # 领星站点ID [唯一标识]
                            "mid": 1,
                            # 站点区域
                            "region": "NA",
                            # 站点亚马逊仓库所属区域 [原字段 'aws_region']
                            "region_aws": "NA",
                            # 站点国家 (中文)
                            "country": "美国",
                            # 站点国家代码 [原字段 'code']
                            "country_code": "US",
                            # 亚马逊市场ID
                            "marketplace_id": "ATVPDKIKX0DER",
                        },
                        ...
                    ],
                }
        """
        data = await self._request_with_sign("GET", route.MARKETPLACES)
        return schema.Marketplaces.model_validate(data)

    async def States(self, country_code: str) -> schema.States:
        """查询亚马逊指定国家的省/州信息。

        ## Docs
        领星接口文档: 基础数据.[查询亚马逊国家下地区列表](https://apidoc.lingxing.com/#/docs/BasicData/WorldStateLists)

        Args:
            country_code (str): 国家代码，如 "US"。

        Returns:
            basic.schema.States: 指定国家的省/州查询结果。

        Examples:
            查询指定国家的省/州并查看返回数据。

            .. code-block:: python

                result = await client.basic.States(country_code="US")
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
                    "request_id": "123B44C1-ECBC-251A-D3F9-E0D49B2DEC85",
                    # 响应时间
                    "response_time": "2001-05-07 05:14:42",
                    # 响应数据量
                    "response_count": 53,
                    # 总数据量
                    "total_count": 53,
                    # 响应数据
                    "data": [
                        {
                            # 国家代码
                            "country_code": "US",
                            # 省/州名称 [原字段 'state_or_province_name']
                            "state": "AL-Alabama",
                            # 省/州代码 [原字段 'code']
                            "state_code": "AL",
                        },
                        ...
                    ],
                }
        """
        url = route.STATES
        # 解析并验证参数
        args = {"country_code": country_code}
        try:
            p = param.CountryCode.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err
        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.States.model_validate(data)

    async def Sellers(self) -> schema.Sellers:
        """查询已授权到领星 ERP 的全部亚马逊店铺信息。

        ## Docs
        领星接口文档: 基础数据.[查询亚马逊店铺列表](https://apidoc.lingxing.com/#/docs/BasicData/SellerLists)

        Returns:
            basic.schema.Sellers: 领星亚马逊店铺查询结果。

        Examples:
            查询店铺并查看返回数据。

            .. code-block:: python

                result = await client.basic.Sellers()
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
                    "request_id": "123B44C1-ECBC-251A-D3F9-E0D49B2DEC85",
                    # 响应时间
                    "response_time": "2001-05-07 05:14:42",
                    # 响应数据量
                    "response_count": 232,
                    # 总数据量
                    "total_count": 232,
                    # 响应数据
                    "data": [
                        {
                            # 领星站点ID (Marketplace.mid)
                            "mid": 4,
                            # 领星店铺ID [唯一标识]
                            "sid": 10000,
                            # 亚马逊卖家ID
                            "seller_id": "AW900000000QD",
                            # 领星店铺名称 (含国家信息) [原字段 'name']
                            "seller_name": "名称店铺",
                            # 领星店铺帐号ID [原字段 'seller_account_id']
                            "account_id": 1000,
                            # 领星店铺帐号名称
                            "account_name": "店铺账号名称",
                            # 亚马逊市场ID (Marketplace.marketplace_id)
                            "marketplace_id": "A1F83G8C2ARO7P",
                            # 店铺区域
                            "region": "EU",
                            # 店铺国家 (中文)
                            "country": "英国",
                            # 店铺状态 (0: 停止同步, 1: 正常, 2: 授权异常, 3: 欠费停服)
                            "status": 2,
                            # 店铺是否授权广告 (0: 否, 1: 是) [原字段 'has_ads_setting']
                            "ads_authorized": 1,
                        },
                        ...
                    ],
                }
        """
        data = await self._request_with_sign("GET", route.SELLERS)
        return schema.Sellers.model_validate(data)

    async def ConceptSellers(self) -> schema.ConceptSellers:
        """查询全部亚马逊概念店铺信息。

        ## Docs
        领星接口文档: 基础数据.[查询亚马逊概念店铺列表](https://apidoc.lingxing.com/#/docs/BasicData/ConceptSellerLists)

        Returns:
            basic.schema.ConceptSellers: 领星亚马逊概念店铺查询结果。

        Examples:
            查询概念店铺并查看返回数据。

            .. code-block:: python

                result = await client.basic.ConceptSellers()
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
                    "request_id": "123B44C1-ECBC-251A-D3F9-E0D49B2DEC85",
                    # 响应时间
                    "response_time": "2001-05-07 05:14:42",
                    # 响应数据量
                    "response_count": 44,
                    # 总数据量
                    "total_count": 44,
                    # 响应数据
                    "data": [
                        {
                            # 领星概念站点ID [原字段 'mid']
                            "cmid": 1000000,
                            # 领星概念店铺ID [唯一标识, 原字段 'id']
                            "csid": 100000000000000000,
                            # 亚马逊卖家ID
                            "seller_id": "A20000000000T",
                            # 领星概念店铺名称 (含区域信息)
                            "seller_name": "概念店铺名称",
                            # 领星概念店铺账号ID [原字段 'seller_account_id']
                            "account_id": 1000,
                            # 领星概念店铺帐号名称 [原字段 'seller_account_name']
                            "account_name": "概念店铺账号",
                            # 概念店铺区域
                            "region": "NA",
                            # 概念店铺国家, 如: "北美共享", "欧洲共享"
                            "country": "北美共享",
                            # 概念店铺状态 (1: 启用, 2: 停用)
                            "status": 1,
                        },
                        ...
                    ],
                }
        """
        data = await self._request_with_sign("GET", route.CONCEPT_SELLERS)
        return schema.ConceptSellers.model_validate(data)

    async def RenameSellers(self, *rename: dict) -> schema.RenameSellersResult:
        """批量修改领星店铺名称。

        ## Docs
        领星接口文档: 基础数据.[批量修改店铺名称](https://apidoc.lingxing.com/#/docs/BasicData/SellerBatchRename)

        Args:
            *rename (dict): 要修改的店铺字典，接口支持最多10个店铺。
                每项必须包含 sid 和 name。sid 是领星店铺ID，类型为 int，来源为 Seller.sid；
                name 是新店铺名称，类型为 str。

        Returns:
            basic.schema.RenameSellersResult: 批量修改店铺名称的响应结果。

        Examples:
            确认目标店铺与新名称后执行改名并查看返回数据；调用会修改真实店铺名称。
            下方返回值来自已核验的真实成功样本，真实失败明细尚未采集验证。

            .. code-block:: python

                result = await client.basic.RenameSellers({"sid": seller_sid, "name": new_name})
                print(result.model_dump())

            .. code-block:: python

                {
                    "code": 0,  # 状态码
                    "message": "success",  # 提示信息
                    "errors": [],  # 错误信息
                    "request_id": "123B44C1-ECBC-251A-D3F9-E0D49B2DEC85",  # 请求ID
                    "response_time": "2001-05-07 05:14:42",  # 响应时间
                    "data": {  # 响应结果
                        "success": 1,  # 修改成功数量 [原字段 'success_num']
                        "failure": 0,  # 修改失败数量 [原字段 'failure_num']
                        "failure_detail": [],  # 修改失败详情
                    },
                }
        """
        url = route.RENAME_SELLERS
        # 解析并验证参数
        args = {"renames": rename}
        try:
            p = param.RenameSellers.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.RenameSellersResult.model_validate(data)

    async def Accounts(self) -> schema.Accounts:
        """查询全部领星 ERP 账号信息。

        ## Docs
        领星接口文档: 基础数据.[查询ERP用户信息列表](https://apidoc.lingxing.com/#/docs/BasicData/AccoutLists)

        Returns:
            basic.schema.Accounts: 领星 ERP 账号查询结果。

        Examples:
            查询账号并查看返回数据。

            .. code-block:: python

                result = await client.basic.Accounts()
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
                    "request_id": "123B44C1-ECBC-251A-D3F9-E0D49B2DEC85",
                    # 响应时间
                    "response_time": "2001-05-07 05:14:42",
                    # 响应数据量
                    "response_count": 43,
                    # 总数据量
                    "total_count": 43,
                    # 响应数据
                    "data": [
                        {
                            # 领星账号所从属的ID (如主帐号ID) [原字段 'zid']
                            "parent_id": 10000000,
                            # 领星帐号ID [唯一标识] [原字段 'uid']
                            "user_id": 10000000,
                            # 是否为主账号 (0: 否, 1: 是)
                            "is_master": 1,
                            # 帐号角色
                            "role": "",
                            # 领星帐号显示的姓名 [原字段 'realname']
                            "display_name": "用户名称",
                            # 领星帐号登陆用户名
                            "username": "sample_user",
                            # 领星帐号电子邮箱
                            "email": "user@example.invalid",
                            # 领星帐号电话号码 [原字段 'mobile']
                            "phone": "13800000000",
                            # 领星帐号创建时间 (北京时间)
                            "create_time": "2001-05-07 05:14",
                            # 领星帐号最后登录时间 (北京时间)
                            "last_login_time": "-",
                            # 领星帐号最后登录IP
                            "last_login_ip": "",
                            # 领星帐号登录次数 [原字段 'login_num']
                            "login_count": 0,
                            # 领星帐号状态 (0: 禁用, 1: 正常)
                            "status": 1,
                            # 关联的领星店铺名称, 逗号分隔 [原字段 'seller']
                            "sellers": "示例店铺1,示例店铺2,示例店铺3",
                        },
                        ...
                    ],
                }
        """
        data = await self._request_with_sign("GET", route.ACCOUNTS)
        return schema.Accounts.model_validate(data)

    async def ExchangeRates(
        self,
        date: str | datetime.date | datetime.datetime | None = None,
    ) -> schema.ExchangeRates:
        """查询指定月份的汇率信息。

        ## Docs
        领星接口文档: 基础数据.[查询汇率](https://apidoc.lingxing.com/#/docs/BasicData/Currency)

        Args:
            date (str | datetime.date | datetime.datetime | None): 查询月份；字符串、date 或 datetime 会转换为 YYYY-MM，None 当前无法通过参数校验。

        Returns:
            basic.schema.ExchangeRates: 指定月份的货币汇率查询结果。

        Examples:
            查询指定月份汇率并查看返回数据。

            .. code-block:: python

                result = await client.basic.ExchangeRates(date="2026-09")
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
                    "request_id": "123B44C1-ECBC-251A-D3F9-E0D49B2DEC85",
                    # 响应时间
                    "response_time": "2001-05-07 05:14:42",
                    # 响应数据量
                    "response_count": 24,
                    # 总数据量
                    "total_count": 24,
                    # 响应数据
                    "data": [
                        {
                            # 汇率日期 (格式: YYYY-MM-DD)
                            "date": "2026-09-01",
                            # 货币名称 (中文) [原字段 'name']
                            "currency": "人民币",
                            # 货币代码 [原字段 'code']
                            "currency_code": "CNY",
                            # 货币符号 [原字段 'icon']
                            "currency_icon": "￥",
                            # 中国银行官方汇率 (对比人民币) [原字段 'rate_org']
                            "boc_rate": 1.0,
                            # 用户汇率 (对比人民币) [原字段 'my_rate']
                            "user_rate": 7.0,
                            # 用户汇率修改时间 (北京时间)
                            "update_time": "",
                        },
                        ...
                    ],
                }
        """
        url = route.EXCHANGE_RATES
        # 解析并验证参数
        args = {"date": date}
        try:
            p = param.ExchangeRate.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body={"date": p.date})
        return schema.ExchangeRates.model_validate(data)

    async def EditExchangeRate(
        self,
        date: str | datetime.date | datetime.datetime,
        currency_code: str,
        user_rate: str | float | Decimal,
    ) -> base_schema.ResponseResult:
        """修改指定月份、指定币种的用户汇率。

        ## Docs
        领星接口文档: 基础数据.[修改我的汇率](https://apidoc.lingxing.com/#/docs/BasicData/ExchangeRateUpdate)

        Args:
            date (str | datetime.date | datetime.datetime): 修改月份；有效日期字符串（如 "2016-12"、"2016-12-01"）、date 或 datetime 会转换为 YYYY-MM。
            currency_code (str): 三字符货币代码，如 "VND"。
            user_rate (str | float | Decimal): 对比人民币的用户自定义汇率，须为有限正数，按现有参数模型量化至10位小数。

        Returns:
            base.schema.ResponseResult: 业务成功时的汇率修改结果。

        Raises:
            errors.InvalidParametersError: 日期、货币代码或汇率未通过现有参数验证。
            errors.InternalServerError: 已观察到的 code=100、message="未知异常"、error_details=["操作失败"] 会在请求层抛错，不返回 ResponseResult。

        Examples:
            此调用会修改真实汇率，请确认月份、币种和金额后执行；以下仅展示成功返回。

            .. code-block:: python

                result = await client.basic.EditExchangeRate(
                    date="2016-12", currency_code="VND", user_rate="0.0003"
                )
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
                    "request_id": "123B44C1-ECBC-251A-D3F9-E0D49B2DEC85",
                    # 响应时间
                    "response_time": "2001-05-07 05:14:42",
                    # 编辑结果
                    "data": None,
                }
        """
        url = route.EDIT_EXCHANGE_RATE
        # 解析并验证参数
        args = {
            "date": date,
            "currency_code": currency_code,
            "user_rate": user_rate,
        }
        try:
            p = param.EditExchangeRate.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return base_schema.ResponseResult.model_validate(data)
