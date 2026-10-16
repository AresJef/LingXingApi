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
                    "message": 'success',
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": '00000000-0000-0000-0000-000000000004',
                    # 响应时间
                    "response_time": '2001-05-07 06:11:00',
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
                            "region": 'NA',
                            # 站点亚马逊仓库所属区域 [原字段 'aws_region']
                            "region_aws": 'NA',
                            # 站点国家 (中文)
                            "country": '美国',
                            # 站点国家代码 [原字段 'code']
                            "country_code": 'US',
                            # 亚马逊市场ID
                            "marketplace_id": 'ATVPDKIKX0DER',
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
                    "message": 'success',
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": '00000000-0000-0000-0000-000000000005',
                    # 响应时间
                    "response_time": '2001-05-07 06:12:00',
                    # 响应数据量
                    "response_count": 53,
                    # 总数据量
                    "total_count": 53,
                    # 响应数据
                    "data": [
                        {
                            # 国家代码
                            "country_code": 'US',
                            # 省/州名称 [原字段 'state_or_province_name']
                            "state": 'AL-Alabama',
                            # 省/州代码 [原字段 'code']
                            "state_code": 'AL',
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
                    "message": 'success',
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": '00000000-0000-0000-0000-00000000000A',
                    # 响应时间
                    "response_time": '2001-05-07 06:13:00',
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
                            "sid": 10041,
                            # 亚马逊卖家ID
                            "seller_id": 'AA0AAAA00A0CN',
                            # 领星店铺名称 (含国家信息) [原字段 'name']
                            "seller_name": '000-名称店-IH',
                            # 领星店铺帐号ID [原字段 'seller_account_id']
                            "account_id": 3035,
                            # 领星店铺帐号名称
                            "account_name": '000-BU',
                            # 亚马逊市场ID (Marketplace.marketplace_id)
                            "marketplace_id": 'A1F83G8C2ARO7P',
                            # 店铺区域
                            "region": 'EU',
                            # 店铺国家 (中文)
                            "country": '英国',
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
                    "message": 'success',
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": '00000000-0000-0000-0000-00000000000B',
                    # 响应时间
                    "response_time": '2001-05-07 06:14:00',
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
                            "csid": 200000000000000001,
                            # 亚马逊卖家ID
                            "seller_id": 'A00A0AA0000AAT',
                            # 领星概念店铺名称 (含区域信息)
                            "seller_name": '000-AA-DE',
                            # 领星概念店铺账号ID [原字段 'seller_account_id']
                            "account_id": 3001,
                            # 领星概念店铺帐号名称 [原字段 'seller_account_name']
                            "account_name": '000-AO',
                            # 概念店铺区域
                            "region": 'NA',
                            # 概念店铺国家, 如: "北美共享", "欧洲共享"
                            "country": '北美共享',
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

            .. code-block:: python

                result = await client.basic.RenameSellers({"sid": seller_sid, "name": new_name})
                print(result.model_dump())

            .. code-block:: python

                {
                    "code": 0,  # 状态码
                    "message": 'success',  # 提示信息
                    "errors": [],  # 错误信息
                    "request_id": '00000000-0000-0000-0000-00000000000C',  # 请求ID
                    "response_time": '2001-05-07 06:07:00',  # 响应时间
                    "data": {
                        # 修改成功数量 [原字段 'success_num']
                        'success': 0,
                        # 修改失败数量 [原字段 'failure_num']
                        'failure': 1,
                        # 修改失败详情
                        'failure_detail': [
                            {
                                # 领星店铺ID (Seller.sid)
                                'sid': 0,
                                # 本地视频素材名称，未匹配素材时为空字符串
                                'name': 'TEST',
                                # 失败信息 [原字段 'error']
                                'message': '店铺记录不存在',
                            },
                        ],
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
                    "message": 'success',
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": '00000000-0000-0000-0000-000000000007',
                    # 响应时间
                    "response_time": '2001-05-07 06:15:00',
                    # 响应数据量
                    "response_count": 43,
                    # 总数据量
                    "total_count": 43,
                    # 响应数据
                    "data": [
                        {
                            # 领星账号所从属的ID (如主帐号ID) [原字段 'zid']
                            "parent_id": 50000001,
                            # 领星帐号ID [唯一标识] [原字段 'uid']
                            "user_id": 40000001,
                            # 是否为主账号 (0: 否, 1: 是)
                            "is_master": 1,
                            # 帐号角色
                            "role": '运营',
                            # 领星帐号显示的姓名 [原字段 'realname']
                            "display_name": '用户名店告',
                            # 领星帐号登陆用户名
                            "username": 'a.0000AAaaaa1F',
                            # 领星帐号电子邮箱
                            "email": 'aaaaaad@xxxxxxxx.test',
                            # 领星帐号电话号码 [原字段 'mobile']
                            "phone": '00000000002',
                            # 领星帐号创建时间 (北京时间)
                            "create_time": '2001-05-07 05:15',
                            # 领星帐号最后登录时间 (北京时间)
                            "last_login_time": '-',
                            # 领星帐号最后登录IP
                            "last_login_ip": '',
                            # 领星帐号登录次数 [原字段 'login_num']
                            "login_count": 0,
                            # 领星帐号状态 (0: 禁用, 1: 正常)
                            "status": 1,
                            # 关联的领星店铺名称, 逗号分隔 [原字段 'seller']
                            "sellers": '000-AA-GQ,aaaa-288,000-AA-GO,000-名称-店铺名-称店铺-JE,000-AA-色丁,000-AA-GK,000-AA-IF,000-AA-AA-BV,Aaaa角己,000-AA名称-店铺名、称店铺-KG,000-名称-IK,000-名称-JC,Aaaaaaaaaaaa-LB,000-名称店-铺名称-KF,000-AA-广店,000-名称店铺名-称店铺-KE,000-AA-EP,000-AA-EK,000-AA-EG,000-AA-EJ,000-AA-EH,000-AA-EL,000-AA-EN,000-AA-EO,000-AA-EM,000-AA-EF,000-AA-HR,000-AA-BE,000-AA-BB,000-AA名称-店铺名-JD,000-名称店铺名-称店铺-KC,000-AP,000-AH,000-AC,000-AF,000-AD,000-AL,000-AN,000-名称店-铺名称-KD,000-AO,000-AA-EV,000-AM,000-AA-EU,000-AB,000-AA-EY,000-AA-CL,000-AA-EX,000-AA-CJ,000-AA-GI,000-BQ,名称店铺-00000000000000-LH,000-BL,000-AA-GN,000-BG,000-AA-GL,000-BJ,000-BH,000-BM,000-BO,000-BP,000-BN,000-BF,000-AA-CZ,000-AA-CX,000-AA-DD,000-AA-DB,000-AA-DH,000-CH,000-BY,000-BS,000-BW,000-BT,000-CD,000-CF,000-CG,000-CE,000-BR,000-AA-CW,000-AA-CR,000-AA-CN,000-AA-CQ,000-AA-CO,000-AA-CS,000-AA-CU,000-AA-CV,aaaaa-aaa-aalf,000-AA-CT,000-AA-CM,Aaaaaaaaa 角辛,000-AA-GH,000-AA-GF,000-AA-BA,000-AA-AV,000-AA-AR,000-AA-AU,000-AA-AS,000-AA-AW,000-AA-AY,000-AA-AZ,000-AA-AX,000-AA-AQ,000-DS,000-DO,000-DJ,000-DM,000-DK,000-DP,000-DR,000-DQ,000-DI,000-HP,AaaaaAks,000-HI,Aaaaaaaaa 角庚,000-HD,000-HG,000-HE,000-HL,000-HN,000-HO,000-HM,000-HC,000-AA-HS,000-AA-FG,000-BZ,000-AA-FE,000-AA-名称-IM,000-AA-JB,000-AA-IY,000-AA-IZ,aaaaaaaaale,aaaaa-aaa-lg,000-AA-EE,000-AA-EA,000-AA-DV,Aaaaaaa角戊,000-AA-DY,000-AA-DW,000-AA-EB,000-AA-ED,000-AA-EC,000-AA-DU,000-AA-GE,000-AA-GC,000-AA-GB,aaaa-289,000-AA-FY,000-AA-FZ,000-BK,AaaaaAaaaaaa-la,000-AA-FD,000-AA-FC,000-AA-DZ,000-DN,000-名称店-IH,000-AG,000-AA-AA-名色角,000-HH,000-BX,000-AA-FK,000-GW,000-AA-FH,000-JX,000-AA-FI,000-JT,000-JV,000-JU,000-JY,000-KA,000-JZ,000-JS,000-JW,000-JM,000-JG,000-JK,000-JH,000-JN,000-JP,000-JO,000-AA-FS,000-JF,000-AA-FO,000-AA名称店-铺名称 店铺名-JR,000-JL,000-AA-FP,000-AA-FB,000-AA-EZ,000-AA-FX,000-AA-FV,000-IS,000-AA-DF,000-AA-HJ,000-AA-CB,000-AA-ES,000-AA-EQ,Aaaaaa-aaaaa-akz,000-名称-店铺名-IL,000-HB,000-GX,000-GS,000-GV,000-AA-名称店-DT,000-GT,000-名称-II,000-GY,000-HA,000-GZ,000-GR,000-IX,000-IT,000-IO,000-IR,000-AA-IC,000-IP,000-AA-FN,000-AA-HY,000-IU,000-AA-AK,000-AA-HU,000-IW,000-AA-AI,000-AA-HX,000-IV,000-AA-HV,000-IN,000-AA-HZ,000-AA-IB,000-AA-IA,000-AA-HT,000-Aaaaaci,000-示店店,000-AA名称店-铺名称，店铺名-IE,000-名称-IJ,000-AA名称店-KR,000-AA名称店-KN,000-AA名称店-KJ,000-AA名称店-KL,000-AA名称店-KK,000-AA名称店-KO,000-AA名称店-KQ,000-AA名称店-KP,000-AA名称店-KI,000-AA名称店-KM,000-AA-FL,Aaaaaa-aaaaa-aaky,000-AA-CA,AAAAAKX,000-AA-FU,000-AA-FT',
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
            date (str | datetime.date | datetime.datetime | None): 查询月份；字符串、date 或 datetime 会转换为 YYYY-MM；None 无法通过参数校验。

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
                    "message": 'success',
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": '00000000-0000-0000-0000-000000000006',
                    # 响应时间
                    "response_time": '2001-05-07 06:15:00',
                    # 响应数据量
                    "response_count": 24,
                    # 总数据量
                    "total_count": 24,
                    # 响应数据
                    "data": [
                        {
                            # 汇率日期 (格式: YYYY-MM-DD)
                            "date": '2026-09-01',
                            # 货币名称 (中文) [原字段 'name']
                            "currency": '人民币',
                            # 货币代码 [原字段 'code']
                            "currency_code": 'CNY',
                            # 货币符号 [原字段 'icon']
                            "currency_icon": '￥',
                            # 中国银行官方汇率 (对比人民币) [原字段 'rate_org']
                            "boc_rate": 1.0,
                            # 用户汇率 (对比人民币) [原字段 'my_rate']
                            "user_rate": 1.0000000013,
                            # 用户汇率修改时间 (北京时间)
                            "update_time": '2001-05-07 05:55:00',
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
            errors.InternalServerError: 服务端返回 code=100、message="未知异常"、error_details=["操作失败"] 时，请求层抛出异常，不返回 ResponseResult。

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
                    "message": 'success',
                    # 错误信息
                    "errors": [],
                    # 请求ID
                    "request_id": '00000000000000000000000000000000.0000000000026',
                    # 响应时间
                    "response_time": '2001-05-07 06:09:00',
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
