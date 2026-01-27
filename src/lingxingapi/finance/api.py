# -*- coding: utf-8 -*-c
import datetime
from typing import Literal
from lingxingapi import errors
from lingxingapi.base.api import BaseAPI
from lingxingapi.finance import param, route, schema

# Type Aliases ---------------------------------------------------------------------------------------------------------
TRANSACTION_SEARCH_FIELD = Literal[
    "transaction_id",
    "transaction_number",
    "amazon_order_id",
    "settlement_id",
]
SETTLEMENT_SEARCH_FIELD = Literal[
    "settlement_id",
    "settlement_number",
]
LEDGER_EVENT_TYPE = Literal[
    "Shipments",
    "CustomerReturns",
    "WhseTransfers",
    "Receipts",
    "VendorReturns",
    "Adjustments",
]
LEDGER_DISPOSITION = Literal[
    "SELLABLE",
    "UNSELLABLE",
    "ALL",
]
ADS_TYPE = Literal["SP", "SB", "SBV", "SD"]
ADS_INVOICE_SEARCH_FIELD = Literal[
    "invoice_id",
    "msku",
    "asin",
    "campaign_name",
]
ADS_CAMPAIGN_INVOICE_SEARCH_FIELD = Literal[
    "item",
    "campaign_name",
]
RECEIVABLE_SORT_FIELD = Literal[
    "opening_balance",
    "income",
    "refund",
    "spend",
    "other",
]
INCOME_STATEMENT_TRANSACTION_STATUS = Literal[
    "Disbursed",
    "Deferred",
    "DisbursedAndSettled",
    "All",
]


# API ------------------------------------------------------------------------------------------------------------------
class FinanceAPI(BaseAPI):
    """领星API `财务数据` 接口

    ## Notice
    请勿直接实例化此类
    """

    # 公共 API --------------------------------------------------------------------------------------
    # . 用户自定义费用管理 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    async def UserFeeTypes(self) -> schema.UserFeeTypes:
        """查询用户自定义费用类型

        ## Docs
        - 财务: [查询费用类型列表](https://apidoc.lingxing.com/#/docs/Finance/feeManagementType)

        :returns `<'UserFeeTypes'>`: 查询到的用户自定义费用类型结果
        ```
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
                    # 序号 [原字段 'sort']
                    "seq": 0,
                    # 费用类型ID [原字段 'id']
                    "fee_type_id": 1045768,
                    # 费用类型名称 [原字段 'name']
                    "fee_type_name": "系统测试费用类型1",
                    # 备用ID
                    "fpoft_id": "304611409499395584",
                },
                ...
            ],
        }
        ```
        """
        url = route.USER_FEE_TYPES
        # 发送请求
        data = await self._request_with_sign("POST", url)
        return schema.UserFeeTypes.model_validate(data)

    # . 亚马逊交易数据 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    async def Transactions(
        self,
        transaction_start_date: str | datetime.date | datetime.datetime | None = None,
        transaction_end_date: str | datetime.date | datetime.datetime | None = None,
        update_start_time: str | datetime.date | datetime.datetime | None = None,
        update_end_time: str | datetime.date | datetime.datetime | None = None,
        *,
        mids: int | list[int] | None = None,
        sids: int | list[int] | None = None,
        event_types: str | list[str] | None = None,
        transaction_type: str | None = None,
        search_field: TRANSACTION_SEARCH_FIELD | None = None,
        search_value: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.Transactions:
        """查询亚马逊交易明细

        ## Docs
        - 财务: [查询结算中心-交易明细](https://apidoc.lingxing.com/#/docs/Finance/settlementTransactionList)

        ## Notice
        - 交易明细唯一标识, 当 event_type 为 'serviceFeeEventList' 时, uid 会变动
        - 但当交易明细 settlement_status 为 'Closed' 状态时 uid 不会变化
        - 建议拉取数据时, 把这个类型的数据作单独的删除与写入操作

        :param transaction_start_date `<'str/date/datetime/None'>`: 交易开始日期 (本地时间),
            双闭区间, 间隔不超过7天, 默认 `None` (交易或更新日期必须指定一个)
        :param transaction_end_date `<'str/date/datetime/None'>`: 交易结束日期 (本地时间),
            双闭区间, 间隔不超过7天, 默认 `None` (交易或更新日期必须指定一个)
        :param update_start_time `<'str/date/datetime/None'>`: 数据更新开始时间 (中国时间),
            间隔不超过7天, 默认 `None` (交易或更新日期必须指定一个)
        :param update_end_time `<'str/date/datetime/None'>`: 数据更新结束时间 (中国时间),
            间隔不超过7天, 默认 `None` (交易或更新日期必须指定一个)
        :param mids `<'int/list[int]/None'>`: 领星站点ID或ID列表 (Seller.mid), 默认 `None` (不筛选)
        :param sids `<'int/list[int]/None'>`: 领星店铺ID或ID列表 (Seller.sid), 默认 `None` (不筛选)
        :param event_types `<'str/list[str]/None'>`: 事件类型或类型列表, 默认 `None` (不筛选)
        :param transaction_type `<'str/None'>`: 交易类型, 默认 `None` (不筛选)
        :param search_field `<'str/None'>`: 搜索字段, 默认 `None` (不筛选), 可选值:

            - 'transaction_id': 交易ID
            - 'transaction_number': 交易编号
            - 'amazon_order_id': 亚马逊订单ID
            - 'settlement_id': 结算ID

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值 10000, 默认 `None` (使用: 20)
        :returns `<'Transactions'>`: 查询到的亚马逊交易明细结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 唯一键 [原字段 'uniqueKey']
                    "uid": "AV94ZBO************",
                    # 领星店铺ID
                    "sid": 1,
                    # 亚马逊卖家ID [原字段 'sellerId']
                    "seller_id": "AV9**********",
                    # 领星店铺名称 [原字段 'storeName']
                    "seller_name": "Store-DE",
                    # 国家代码 [原字段 'countryCode']
                    "country_code": "DE",
                    # 市场名称 [原字段 'marketplaceName']
                    "marketplace": "Amazon.de",
                    # 账单类型 [原字段 'accountType']
                    "account_type": "Standard",
                    # 事件组ID [原字段 'financialEventGroupId']
                    "financial_event_group_id": "To6lYH1kP6icDvKl4-********",
                    # 事件类型 [原字段 'eventType']
                    "event_type": "Shipment",
                    # 交易编号 [原字段 'fid']
                    "transaction_number": "HIO*********",
                    # 交易类型 [原字段 'type']
                    "transaction_type": "Commission",
                    # 结算ID [原字段 'settlementId']
                    "settlement_id": 0,
                    # 处理状态 [原字段 'processingStatus']
                    # (Open: 未结算, Closed: 已结算, Reconciled: 已对账)
                    "settlement_status": "Open",
                    # 资金转账状态 [原字段 'fundTransferStatus']
                    # (Succeeded: 已转账, Processing: 转账中, Failed: 失败, Unknown: 未知)
                    "transfer_status": "Unknown",
                    # 数量 [原字段 'quantity']
                    "transaction_qty": 1,
                    # 金额 [原字段 'currencyAmount']
                    "transaction_amt": -7.78,
                    # 币种 [原字段 'currencyCode']
                    "currency_code": "EUR",
                    # 交易发生时间 (UTC时间) [原字段 'postedDate']
                    "transaction_time_utc": "2026-01-06T11:17:40Z",
                    # 交易发生时间 (本地时间) [原字段 'postedDateLocale']
                    "transaction_time_loc": "2026-01-06T03:17:40-08:00",
                    # 数据创建时间 (中国时间) [原字段 'gmtCreate']
                    "create_time_cnt": "2026-01-06 23:33:08.238",
                    # 数据更新时间 (中国时间) [原字段 'gmtModified']
                    "update_time_cnt": "2025-09-04 06:19:38.739",
                    # 亚马逊订单编号 [原字段 'amazonOrderId']
                    "amazon_order_id": "303-*******-*******",
                    # 商家订单ID [原字段 'merchantOrderId']
                    "merchant_order_id": "",
                    # 卖家提供的订单编号 [原字段 'sellerOrderId']
                    "seller_order_id": "303-*******-*******",
                    # 亚马逊订单ID [原字段 'orderId']
                    "order_id": "",
                    # 亚马逊订单商品ID [原字段 'orderItemId']
                    "order_item_id": 14955****,
                    # 配送渠道 [原字段 'fulfillment']
                    "fulfillment_channel": "FBA",
                    # 亚马逊SKU [原字段 'sellerSku']
                    "msku": "SKU*******",
                    # 领星本地SKU [原字段 'localSku']
                    "lsku": "LOCAL*******",
                    # 亚马逊FNSKU [原字段 'fnsku']
                    "fnsku": "X000*******",
                    # 领星本地商品名称 [原字段 'localName']
                    "product_name": "JBL",
                    # 费用类型 [原字段 'feeType']
                    "fee_type": "",
                    # 费用描述 [原字段 'feeDescription']
                    "fee_desc": "",
                    # 费用原因 [原字段 'feeReason']
                    "fee_reason": "",
                    # 促销ID [原字段 'promotionId']
                    "promotion_id": "",
                    # 活动ID [原字段 'dealId']
                    "deal_id": "",
                    # 活动描述 [原字段 'dealDescription']
                    "deal_desc": "",
                    # 优惠券ID [原字段 'couponId']
                    "coupon_id": "",
                    # 优惠券描述 [原字段 'sellerCouponDescription']
                    "coupon_desc": "",
                    # 优惠券兑换次数 [原字段 'clipOrRedemptionCount']
                    "coupon_redemption_count": 0,
                    # 发票ID [原字段 'invoiceId']
                    "invoice_id": "",
                    # 支付事件ID [原字段 'paymentEventId']
                    "payment_event_id": "",
                    # 注册ID [原字段 'enrollmentId']
                    "enrollment_id": "",
                    # 债务恢复类型 [原字段 'debtRecoveryType']
                    "debt_recovery_type": "",
                    # 移除货件项ID [原字段 'removalShipmentItemId']
                    "removal_shipment_item_id": "",
                    # 调整事件ID [原字段 'adjustmentEventId']
                    "adjustment_event_id": "",
                    # 安全索赔ID [原字段 'safeTClaimId']
                    "safe_t_claim_id": "",
                    # 安全索赔原因代码 [原字段 'reasonCode']
                    "saft_t_claim_reason": "",
                },
                ...
            ],
        }
        ```
        """
        url = route.TRANSACTIONS
        # 构建参数
        args = {
            "mids": mids,
            "sids": sids,
            "transaction_start_date": transaction_start_date,
            "transaction_end_date": transaction_end_date,
            "update_start_time": update_start_time,
            "update_end_time": update_end_time,
            "event_types": event_types,
            "transaction_type": transaction_type,
            "search_field": search_field,
            "search_value": search_value,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.Transactions.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.Transactions.model_validate(data)

    async def Settlements(
        self,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        date_type: int,
        *,
        mids: int | list[int] | None = None,
        sids: int | list[int] | None = None,
        search_field: SETTLEMENT_SEARCH_FIELD | None = None,
        search_value: str | None = None,
        currency_code: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.Settlements:
        """查询亚马逊结算汇总

        ## Docs
        - 财务: [查询结算中心-结算汇总](https://apidoc.lingxing.com/#/docs/Finance/settlementSummaryList)

        :param start_date `<'str/date/datetime'>`: 日期开始, 间隔不超过90天
        :param end_date `<'str/date/datetime'>`: 日期结束, 间隔不超过90天
        :param date_type `<'int'>`: 日期类型, 可选值:

            - `0`: 结算开始时间 (本地时间)
            - `1`: 结算结束时间 (本地时间)
            - `2`: 资金转账时间 (本地时间)

        :param mids `<'int/list[int]/None'>`: 领星站点ID或ID列表 (Seller.mid), 默认 `None` (不筛选)
        :param sids `<'int/list[int]/None'>`: 领星店铺ID或ID列表 (Seller.sid), 默认 `None` (不筛选)
        :param search_field `<'str/None'>`: 搜索字段, 默认 `None` (不筛选), 可选值:

            - 'settlement_id': 结算ID
            - 'settlement_number': 结算编号

        :param search_value `<'str/None'>`: 搜索值, 默认 `None` (不筛选)
        :param currency_code `<'str/None'>`: 结算金额目标转换货币代码, 默认 `None` (保持原结算货币)
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 20)
        :returns `<'Settlements'>`: 查询到的亚马逊结算汇总结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "",
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
                    # 亚马逊卖家ID [原字段 'sellerId']
                    "seller_id": "ARHK*********",
                    # 领星店铺名称 [原字段 'storeName'
                    "seller_name": "Store-SE",
                    # 国家代码 [原字段 'countryCode']
                    "country_code": "SE",
                    # 追踪编号 [原字段 'traceId']
                    "trace_number": "139V**********",
                    # 结算ID [原字段 'settlementId']
                    "settlement_id": 2301*******,
                    # 结算编号 [原字段 'id']
                    "settlement_number": "8RC4********",
                    # 结算备注 [原字段 'comment']
                    "settlement_note": "",
                    # 处理状态 [原字段 'processingStatus']
                    # (Open: 未结算, Closed: 已结算, Reconciled: 已对账)
                    "settlement_status": "Closed",
                    # 资金转账状态 [原字段 'fundTransferStatus']
                    # (Succeeded: 已转账, Processing: 转账中, Failed: 失败, Unknown: 未知)
                    "transfer_status": "Succeeded",
                    # 账单类型 [原字段 'accountType']
                    "account_type": "Standard",
                    # 原始结算货币代码 [原字段 'originalTotalCurrencyCode']
                    "settlement_currency_code": "SEK",
                    # 原始结算金额 [原字段 'originalTotalCurrencyAmount']
                    "settlement_amt": 120.62,
                    # 转账货币代码 [原字段 'convertedTotalCurrencyCode']
                    "transfer_currency_code": "EUR",
                    # 转账金额 [原字段 'convertedTotalCurrencyAmount']
                    "transfer_amt": 10.77,
                    # 转账折算结算金额 [原字段 'convertedTotalCurrencyAmountToOrigin']
                    "transfer_to_settlement_amt": 122.91,
                    # 结算事件组ID [原字段 'financialEventGroupId']
                    "settlement_event_group_id": "O9rWlJ*********",
                    # 结算事件金额 [原字段 'financialEventsAmount']
                    "settlement_events_amt": 120.62,
                    # 对账结果 [原字段 'reconciliationResult']
                    "reconciliation_result": "未对账",
                    # 汇款比率 [原字段 'remittanceRate']
                    "remittance_rate": 0.607263,
                    # 银行帐号信息 [原字段 'accountInfo']
                    "banck_account_info": "",
                    # 银行帐号尾号 [原字段 'accountTail']
                    "bank_account_last_digits": "025",
                    # 收入 [原字段 'sale']
                    "income": {
                        # 销售 [原字段 'product']
                        "product_sales": 202.4,
                        # 运费 [原字段 'freight']
                        "shipping_credits": 14.02,
                        # 包装 [原字段 'packing']
                        "giftwrap_credits": 0.0,
                        # 其他
                        "other": -14.02,
                        # 税费
                        "tax": 0.0,
                        # 总收入 [原字段 'sale']
                        "total_income": 202.4,
                    },
                    # 退费
                    "refund": {
                        # 销售退费
                        "sales_refunds": 0.0,
                        # 其他退费
                        "other_refunds": 0.0,
                        # 税费退费
                        "tax_refunds": 0.0,
                        # 总退费
                        "total_refunds": 0.0,
                    },
                    # 支出 [原字段 'pay']
                    "expense": {
                        # 亚马逊费用 [原字段 'amazon']
                        "amazon_fees": -81.78,
                        # 库存费用 [原字段 'storage']
                        "inventory_fees": 0.0,
                        # 广告费用 [原字段 'ad']
                        "cost_of_advertising": 0.0,
                        # 促销费用 [原字段 'promotion']
                        "promotion_rebates": 0.0,
                        # 其他费用 [原字段 'other']
                        "other_fees": 0.0,
                        # 总支出 [原字段 'pay']
                        "total_expense": -81.78,
                    },
                    # 转账
                    "transfer": {
                        # 初期余额 [原字段 'beginningBalanceCurrencyAmount']
                        "opening_balance": 0.0,
                        # 本期应收 [原字段 'originalTotalCurrencyAmount']
                        "receivable": 120.62,
                        # 信用卡扣款 [原字段 'creditCardDeduction']
                        "credit_card_deduction": 0.0,
                        # 上期预留金余额 [原字段 'previousReserveAmount']
                        "prior_reserve_balance": 0.0,
                        # 本期预留金余额 [原字段 'currentReserveAmount']
                        "current_reserve_balance": 0.0,
                        # 本期结算 [原字段 'convertedTotalCurrencyAmount']
                        "settlement": 120.62,
                    },
                    # 结算开始时间 (本地时间) [原字段 'financialEventGroupStartLocale']
                    "settlement_start_time_loc": "2024-10-16T21:33:44+02:00",
                    # 结算结束时间 (本地时间) [原字段 'financialEventGroupEndLocale']
                    "settlement_end_time_loc": "2025-09-03T21:33:45+02:00",
                    # 资金转账时间 (本地时间) [原字段 'fundTransferDateLocale']
                    "transfer_time_loc": "2025-09-03T21:33:45+02:00",
                    # 资金转账时间 (UTC时间) [原字段 'fundTransferDate']
                    "transfer_time_utc": "2025-09-03T19:33:45Z",
                },
                ...
            ]
        }
        ```
        """
        url = route.SETTLEMENTS
        # 构建参数
        args = {
            "start_date": start_date,
            "end_date": end_date,
            "date_type": date_type,
            "mids": mids,
            "sids": sids,
            "search_field": search_field,
            "search_value": search_value,
            "currency_code": currency_code,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.Settlements.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.Settlements.model_validate(data)

    async def ShipmentSettlements(
        self,
        sids: int | list[int],
        seller_ids: str | list[str],
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        date_type: int,
        *,
        mskus: str | list[str] | None = None,
        lskus: str | list[str] | None = None,
        product_names: str | list[str] | None = None,
        amazon_order_ids: str | list[str] | None = None,
        shipment_ids: str | list[str] | None = None,
        tracking_numbers: str | list[str] | None = None,
        country_codes: str | list[str] | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.ShipmentSettlements:
        """查询亚马逊发货结算信息

        ## Docs
        - 财务: [查询发货结算报告](https://apidoc.lingxing.com/#/docs/Finance/SettlementReport)

        :param sids `<'int/list[int]'>`: 领星店铺ID或ID列表 (Seller.sid)
        :param seller_ids `<'str/list[str]'>`: 亚马逊卖家ID或列表 (Seller.seller_id)
        :param start_date `<'str/date/datetime'>`: 统计开始日期, 双闭区间
        :param end_date `<'str/date/datetime'>`: 统计结束日期, 双闭区间
        :param date_type `<'int'>`: 日期类型, 可选值:

            - `1`: 下单时间 (本地时间)
            - `2`: 付款时间 (本地时间)
            - `3`: 发货时间 (本地时间)
            - `4`: 结算时间 (本地时间)
            - `5`: 转账时间 (本地时间)
            - `6`: 更新时间 (中国时间)

        :param mskus `<'str/list[str]/None'>`: 亚马逊SKU或列表, 默认 `None` (不筛选)
        :param lskus `<'str/list[str]/None'>`: 领星本地SKU或列表, 默认 `None` (不筛选)
        :param product_names `<'str/list[str]/None'>`: 领星本地商品名称或列表, 默认 `None` (不筛选)
        :param amazon_order_ids `<'str/list[str]/None'>`: 亚马逊订单ID或列表, 默认 `None` (不筛选)
        :param shipment_ids `<'str/list[str]/None'>`: 亚马逊发货ID或列表, 默认 `None` (不筛选)
        :param tracking_numbers `<'str/list[str]/None'>`: 亚马逊追踪编号或列表, 默认 `None` (不筛选)
        :param country_codes `<'str/list[str]/None'>`: 国家代码或列表, 默认 `None` (不筛选)
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值 1000, 默认 `None` (使用: 20)
        :returns `<'ShipmentSettlements'>`: 查询到的亚马逊发货结算信息结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "",
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
                    # 亚马逊卖家ID [原字段 'sellerId']
                    "seller_id": "A1IJ**********",
                    # 领星店铺名称 [原字段 'sellerName']
                    "seller_name": "Store-US",
                    # 国家代码 [原字段 'countryCode']
                    "country_code": "US",
                    # 亚马逊订单编号 [原字段 'amazonOrderId']
                    "amazon_order_id": "114-*******-*******",
                    # 卖家提供的订单编号 [原字段 'merchantOrderId']
                    "merchant_order_id": "",
                    # 亚马逊货件编号 [原字段 'shipmentId']
                    "shipment_id": "Bx4******",
                    # 亚马逊货件商品编号 [原字段 'shipmentItemId']
                    "shipment_item_id": "DDhy*********",
                    # 销售渠道 [原字段 'salesChannel']
                    "sales_channel": "amazon.com",
                    # 配送方式 [原字段 'fulfillment']
                    "fulfillment_channel": "FBA",
                    # 亚马逊配送中心代码 [原字段 'fulfillmentCenterId']
                    "fulfillment_center_id": "ORF3",
                    # 物流模式 [原字段 'logisitcsMode']
                    "logistics_mode": "USPS",
                    # 物流跟踪号 [原字段 'trackingNumber']
                    "tracking_number": "93612*****************",
                    # 结算ID [原字段 'settlementId']
                    "settlement_id": 0,
                    # 处理状态 [原字段 'processingStatus']
                    # (Open: 未结算, Closed: 已结算, Reconciled: 已对账)
                    "settlement_status": "",
                    # 资金转账状态 [原字段 'fundTransferStatus']
                    # (Succeeded: 已转账, Processing: 转账中, Failed: 失败, Unknown: 未知)
                    "transfer_status": "",
                    # 发货与结算时间差异 [原字段 'daysBetweenShipAndFiance']
                    "settlement_lag": "00天00小时00分",
                    # 亚马逊SKU
                    "msku": "SKU********",
                    # 领星本地SKU [原字段 'localSku']
                    "lsku": "LOCAL********",
                    # 领星本地商品名称 [原字段 'localName']
                    "product_name": "JBL",
                    # 领星本地品牌名称 [原字段 'brandName']
                    "brand_name": "",
                    # 领星本地分类名称 [原字段 'categoryName']
                    "category_name": "",
                    # 商品开发负责人名称 [原字段 'productDeveloper']
                    "developer_name": "",
                    # 商品负责人名称 (逗号分隔) [原字段 'listing']
                    "operator_names": "白小白",
                    # 订单商品总数量 [原字段 'quantity']
                    "order_qty": 1,
                    # 商品销售金额 [原字段 'itemPrice']
                    "sales_amt": 38.89,
                    # 商品销售金额税费 [原字段 'itemTax']
                    "sales_tax_amt": 2.72,
                    # 买家支付运费金额 [原字段 'shippingPrice']
                    "shipping_credits_amt": 0.0,
                    # 买家支付运费税费 [原字段 'shippingTax']
                    "shipping_credits_tax_amt": 0.0,
                    # 买家支付礼品包装费金额 [原字段 'giftWrapPrice']
                    "giftwrap_credits_amt": 0.0,
                    # 买家支付礼品包装费税费 [原字段 'giftWrapTax']
                    "giftwrap_credits_tax_amt": 0.0,
                    # 卖家商品促销折扣金额 [原字段 'itemPromotionDiscount']
                    "promotion_discount_amt": 0.0,
                    # 卖家商品运费折扣金额 [原字段 'shipPromotionDiscount']
                    "shipping_discount_amt": 0.0,
                    # 货币代码 [原字段 'currencyCode']
                    "currency_code": "USD",
                    # 买家国家 [原字段 'saleCountryName']
                    "buyer_country": "美国",
                    # 买家城市 [原字段 'shipCity']
                    "buyer_city": "DALTON",
                    # 买家区域 [原字段 'region']
                    "buyer_district": "GA",
                    # 买家邮编 [原字段 'shipPostalCode']
                    "buyer_postcode": "30721-7330",
                    # 订单购买时间 (本地时间) [原字段 'purchaseDateLocale']
                    "purchase_time_loc": "2025-09-03 14:18:46",
                    # 订单发货时间 (本地时间) [原字段 'shipmentsDateLocale']
                    "shipment_time_loc": "2025-09-03 21:42:31",
                    # 订单付款时间 (本地时间) [原字段 'paymentsDateLocale']
                    "payment_time_loc": "2025-09-03 21:42:31",
                    # 订单结算时间 (本地时间) [原字段 'financePostedDateLocale']
                    "settlement_time_loc": "",
                    # 资金转账时间 (本地时间) [原字段 'fundTransferDateLocale']
                    "transfer_time_loc": "",
                    # 数据更新时间 (中国时间) [原字段 'gmtModified']
                    "update_time_cnt": "2025-09-05 07:38:11",
                },
                ...
            ]
        }
        ```
        """
        url = route.SHIPMENT_SETTLEMENT
        # 构建参数
        args = {
            "sids": sids,
            "seller_ids": seller_ids,
            "start_date": start_date,
            "end_date": end_date,
            "date_type": date_type,
            "mskus": mskus,
            "lskus": lskus,
            "product_names": product_names,
            "amazon_order_ids": amazon_order_ids,
            "shipment_ids": shipment_ids,
            "tracking_numbers": tracking_numbers,
            "country_codes": country_codes,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.ShipmentSettlement.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.ShipmentSettlements.model_validate(data)

    async def Receivables(
        self,
        settlement_date: str | datetime.date | datetime.datetime,
        *,
        mids: int | list[int] | None = None,
        sids: int | list[int] | None = None,
        archive_status: int | None = None,
        received_state: int | None = None,
        sort_field: RECEIVABLE_SORT_FIELD | None = None,
        sort_type: int | None = None,
        currency_code: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.Receivables:
        """查询亚马逊应收账款

        ## Docs
        - 财务: [应收报告-列表查询](https://apidoc.lingxing.com/#/docs/Finance/receivableReportList)

        :param settlement_date `<'str/date/datetime'>`: 结算日期
        :param mids `<'int/list[int]/None'>`: 领星站点ID或ID列表 (Seller.mid), 默认 `None` (不筛选)
        :param sids `<'int/list[int]/None'>`: 领星店铺ID或ID列表 (Seller.sid), 默认 `None` (不筛选)
        :param archive_status `<'int/None'>`: 归档状态, 默认 `None` (不筛选), 可选值:

            - `0`: 未归档
            - `1`: 已归档

        :param received_state `<'int/None'>`: 收款状态, 默认 `None` (不筛选), 可选值:

            - `0`: 未收款
            - `1`: 已收款

        :param sort_field `<'str/None'>`: 排序字段, 默认 `None` (不排序), 可选值:

            - `'opening_balance'`: 期初余额
            - `'income'`: 收入
            - `'refund'`: 退款
            - `'spend'`: 支出
            - `'other'`: 其他

        :param sort_type `<'int/None'>`: 排序方式, 默认 `None` (不排序), 可选值:

            - `0`: 升序
            - `1`: 降序

        :param currency_code `<'str/None'>`: 结算金额目标转换货币代码, 默认 `None` (保持原结算货币)
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 20)
        :returns `<'Receivables'>`: 查询到的亚马逊应收账款结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "",
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
                    # 领星店铺名称 [原字段 'storeName']
                    "seller_name": "Store-CA",
                    # 国家 (中文)
                    "country": "加拿大",
                    # 国家代码 [原字段 'countryCode']
                    "country_code": "CA",
                    # 对账状态 (0: 未对账, 1: 已对账)
                    "archive_status": 0,
                    # 对账状态描述
                    "archive_status_desc": "未对账",
                    # 应收款备注 [原字段 'remark']
                    "note": "",
                    # 初期余额 [原字段 'beginningBalanceCurrencyAmount']
                    "opening_balance": 1940.57,
                    # 收入金额 [原字段 'incomeAmount']
                    "income": 74958.81,
                    # 退费金额 [原字段 'refundAmount']
                    "refund": -2671.66,
                    # 支出金额 [原字段 'spendAmount']
                    "expense": -22988.99,
                    # 其他金额
                    "other": 0.0,
                    # 其他: 信用卡扣款金额 [原字段 'card']
                    "other_credit_card_deduction": 0.0,
                    # 其他: 其他子项金额 [原字段 'otherItem']
                    "other_item": 0.0,
                    # 转账成功金额 [原字段 'convertedSuccessAmount']
                    "transfer_success": 51612.15,
                    # 转账到账金额 [原字段 'receivedAmount']
                    "transfer_received": 0.0,
                    # 转账失败金额 [原字段 'convertedFailedAmount']
                    "transfer_failed": 0.0,
                    # 期末余额 [原字段 'endingBalance']
                    "ending_balance": -373.42,
                    # 币种代码 [原字段 'currencyCode']
                    "currency_code": "CAD",
                    # 币种符号 [原字段 'currencyIcon']
                    "currency_icon": "CA$",
                    # 结算日期 (格式: YYYY-MM) [原字段 'settlementDate']
                    "settlement_date": "2025-08",
                },
                ...
            ]
        }
        ```
        """
        url = route.RECEIVABLES
        # 构建参数
        args = {
            "settlement_date": settlement_date,
            "mids": mids,
            "sids": sids,
            "archive_status": archive_status,
            "received_state": received_state,
            "sort_field": sort_field,
            "sort_type": sort_type,
            "currency_code": currency_code,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.Receivables.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.Receivables.model_validate(data)

    # . 亚马逊库存数据 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    async def LedgerDetail(
        self,
        seller_ids: str | list[str],
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        *,
        asins: str | list[str] | None = None,
        mskus: str | list[str] | None = None,
        fnskus: str | list[str] | None = None,
        country_codes: str | list[str] | None = None,
        event_types: LEDGER_EVENT_TYPE | list[LEDGER_EVENT_TYPE] | None = None,
        reference_id: int | None = None,
        disposition: LEDGER_DISPOSITION | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.LedgerDetail:
        """查询亚马逊库存明细台账

        ## Docs
        - 财务: [查询库存分类账detail数据](https://apidoc.lingxing.com/#/docs/Finance/centerOdsDetailQuery)

        :param seller_ids `<'str/list[str]'>`: 亚马逊卖家ID或列表 (Seller.seller_id)
        :param start_date `<'str/date/datetime'>`: 统计开始日期, 闭合区间
        :param end_date `<'str/date/datetime'>`: 统计结束日期, 闭合区间
        :param asins `<'str/list[str]/None'>`: 亚马逊ASIN或列表, 默认 `None` (不筛选)
        :param mskus `<'str/list[str]/None'>`: 亚马逊SKU或列表, 默认 `None` (不筛选)
        :param fnskus `<'str/list[str]/None'>`: 亚马逊FNSKU或列表, 默认 `None` (不筛选)
        :param country_codes `<'str/list[str]/None'>`: 国家代码(库存位置)或列表, 默认 `None` (不筛选)
        :param event_types `<'str/list[str]/None'>`: 事件类型或类型列表, 默认 `None` (不筛选), 可选值:

            - `'Shipments'`
            - `'CustomerReturns'`
            - `'WhseTransfers'`
            - `'Receipts'`
            - `'VendorReturns'`
            - `'Adjustments'`

        :param reference_id `<'int/None'>`: 货物关联ID, 支持模糊查询, 默认 `None` (不筛选)
        :param disposition `<'int/None'>`: 库存处置结果, 默认 `None` (不筛选), 可选值:

            - `'SELLABLE'`
            - `'UNSELLABLE'`
            - `'ALL'`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值 1000, 默认 `None` (使用: 20)
        :returns `<'LedgerDetail'>`: 查询到的亚马逊库存明细台账结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 同uid_idx共同构成唯一索引 [原字段 'uniqueMd5']
                    "uid": "5cdbbb**************",
                    # 同uid共同构成唯一索引 [原字段 'uniqueMd5Idx']
                    "uid_idx": 0,
                    # 货物关联ID [原字段 'referenceId']
                    "reference_id": "",
                    # 亚马逊卖家ID [原字段 'sellerId']
                    "seller_id": "A1IJ**********",
                    # 亚马逊ASIN
                    "asin": "B0D*******",
                    # 亚马逊SKU
                    "msku": "SKU*******",
                    # 亚马逊FNSKU
                    "fnsku": "X00*******",
                    # 商品标题
                    "title": "Product Title",
                    # 事件类型编码 [原字段 'eventType']
                    "event_type_code": "01",
                    # 事件类型 [原字段 'eventTypeDesc']
                    "event_type": "Shipments",
                    # 事件原因 [原字段 'reason']
                    "event_reason": "",
                    # 事件发生日期 [原字段 'date
                    "event_date": "2025-09-04",
                    # 国家代码 (库存位置)
                    "country_code": "US",
                    # 亚马逊配送中心代码 [原字段 'fulfillmentCenter']
                    "fulfillment_center_id": "RIC2",
                    # 库存处置结果编码 [原字段 'disposition']
                    "disposition_code": "01",
                    # 库存处置结果 [原字段 'dispositionDesc']
                    "disposition": "SELLABLE",
                    # 数量 [原字段 'quantity']
                    "qty": -1,
                },
                ...
            ]
        }
        ```
        """
        url = route.LEDGER_DETAIL
        # 构建参数
        args = {
            "seller_ids": seller_ids,
            "start_date": start_date,
            "end_date": end_date,
            "asins": asins,
            "mskus": mskus,
            "fnskus": fnskus,
            "country_codes": country_codes,
            "event_types": event_types,
            "reference_id": reference_id,
            "disposition": disposition,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.LedgerDetail.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.LedgerDetail.model_validate(data)

    async def LedgerSummary(
        self,
        seller_ids: str | list[str],
        query_dimension: int,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        *,
        asins: str | list[str] | None = None,
        mskus: str | list[str] | None = None,
        fnskus: str | list[str] | None = None,
        country_codes: str | list[str] | None = None,
        disposition: LEDGER_DISPOSITION | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.LedgerSummary:
        """查询亚马逊库存汇总台账

        ## Docs
        - 财务: [查询库存分类账summary数据](https://apidoc.lingxing.com/#/docs/Finance/summaryQuery)

        :param seller_ids `<'str/list[str]'>`: 亚马逊卖家ID或列表 (Seller.seller_id)
        :param query_dimension `<'int'>`: 查询维度, 可选值:

            - `1`: 月维度
            - `2`: 日维度

        :param start_date `<'str/date/datetime'>`: 统计开始日期, 闭合区间
        :param end_date `<'str/date/datetime'>`: 统计结束日期, 闭合区间
        :param asins `<'str/list[str]/None'>`: 亚马逊ASIN或列表, 默认 `None` (不筛选)
        :param mskus `<'str/list[str]/None'>`: 亚马逊SKU或列表, 默认 `None` (不筛选)
        :param fnskus `<'str/list[str]/None'>`: 亚马逊FNSKU或列表, 默认 `None` (不筛选)
        :param country_codes `<'str/list[str]/None'>`: 国家代码(库存位置)或列表, 默认 `None` (不筛选)
        :param disposition `<'int/None'>`: 库存处置结果, 默认 `None` (不筛选), 可选值:

            - `'SELLABLE'`
            - `'UNSELLABLE'`
            - `'ALL'`

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值 1000, 默认 `None` (使用: 20)
        :returns `<'LedgerSummary'>`: 查询到的亚马逊库存汇总台账结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 同uid_idx共同构成唯一索引 [原字段 'uniqueMd5']
                    "uid": "1c227d2****************",
                    # 同uid共同构成唯一索引 [原字段 'uniqueMd5Idx']
                    "uid_idx": 0,
                    # 亚马逊卖家ID [原字段 'sellerId']
                    "seller_id": "A1IJI*********",
                    # 亚马逊ASIN
                    "asin": "B0D*******",
                    # 亚马逊SKU
                    "msku": "SKU*******",
                    # 亚马逊FNSKU
                    "fnsku": "X00*******",
                    # 商品标题
                    "title": "Product Title",
                    # 汇总月份/日期 [原字段 'date']
                    # (月维度: '2024-01', 日维度: '2024-01-01')
                    "summary_date": "2025-08",
                    # 国家代码 (库存位置)
                    "country_code": "US",
                    # 库存处置结果编码 [原字段 'disposition']
                    "disposition_code": "01",
                    # 库存处置结果 [原字段 'dispositionDesc']
                    "disposition": "SELLABLE",
                    # 初期库存 [原字段 'startingWarehouseBalance']
                    "opening_balance": 676,
                    # 调拨变动 [原字段 'warehouseTransferInOrOut']
                    "transfer_net": -209,
                    # 调拨在途 [原字段 'inTransitBetweenWarehouses']
                    "transfer_in_transit": 210,
                    # 签收入库 [原字段 'receipts']
                    "received": 700,
                    # 销售出库 [原字段 'customerShipments']
                    "customer_shipment": -566,
                    # 销售退货 [原字段 'customerReturns']
                    "customer_returned": 4,
                    # 卖家移除 [原字段 'vendorReturns']
                    "seller_removal": 0,
                    # 丢失报损 [原字段 'lost']
                    "lost_events": -1,
                    # 盘盈找回 [原字段 'found'
                    "found_events": 1,
                    # 受损调整 [原字段 'damaged']
                    "damaged_events": 0,
                    # 处置报废 [原字段 'disposed']
                    "disposed_events": 0,
                    # 其他事件变动 [原字段 'otherEvents']
                    "other_events": 0,
                    # 未知事件变动 [原字段 'unKnownEvents']
                    "unknown_events": 0,
                    # 期末库存 [原字段 'endingWareHouseBalance']
                    "closing_balance": 605,
                },
                ...
            ]
        }
        ```
        """
        url = route.LEDGER_SUMMARY
        # 构建参数
        args = {
            "seller_ids": seller_ids,
            "query_dimension": query_dimension,
            "start_date": start_date,
            "end_date": end_date,
            "asins": asins,
            "mskus": mskus,
            "fnskus": fnskus,
            "country_codes": country_codes,
            "disposition": disposition,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.LedgerSummary.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.LedgerSummary.model_validate(data)

    async def LedgerValuation(
        self,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        date_type: int,
        *,
        transaction_types: int | list[int] | None = None,
        transaction_numbers: str | list[str] | None = None,
        source_numbers: str | list[str] | None = None,
        warehouse_names: str | list[str] | None = None,
        seller_names: str | list[str] | None = None,
        mskus: str | list[str] | None = None,
        lskus: str | list[str] | None = None,
        dispositions: int | list[int] | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.LedgerValuation:
        """查询亚马逊库存价值台账

        ## Docs
        - 财务: [查询FBA成本计价流水](https://apidoc.lingxing.com/#/docs/Finance/CostStream)

        :param start_date `<'str/date/datetime'>`: 查询开始日期
        :param end_date `<'str/date/datetime'>`: 查询结束日期
        :param date_type `<'int'>`: 日期类型, 可选值:

            - `1`: 库存动作日期
            - `2`: 结算日期 (仅销售, 退货场景会存在结算日期, 其他库存动作结算日期为空)

        :param transaction_types `<'int/list[int]/None'>`: 库存动作类型或列表, 默认 `None` (不筛选), 可选值:

            - `1`: 期初库存-FBA上月结存
            - `10`: 调拨入库-FBA补货入库
            - `11`: 调拨入库-FBA途损补回
            - `12`: 调拨入库-FBA超签入库
            - `13`: 调拨入库-FBA超签入库 (Close后)
            - `14`: 调拨入库-FBA补货入库 (无发货单)
            - `20`: 调拨入库-FBA调仓入库
            - `35`: 调拨入库-FBA发货在途入库
            - `25`: 盘点入库-FBA盘点入库
            - `30`: FBA退货-FBA无源单销售退货
            - `31`: FBA退货-FBA有源单销售退货
            - `200`: 销售出库-FBA补发货销售
            - `201`: 销售出库-FBA多渠道销售订单
            - `202`: 销售出库-FBA亚马逊销售订单
            - `205`: 其他出库-FBA补货出库
            - `220`: 盘点出库-FBA盘点出库
            - `15`: 调拨出库-FBA调仓出库
            - `215`: 调拨出库-FBA移除
            - `225`: 调拨出库-FBA发货在途出库
            - `226`: 调拨出库-FBA发货途损
            - `227`: 调拨出库-后补发货单在途出库
            - `5`: 调整单- FBA对账差异入库调整
            - `210`: 调整单-FBA对账差异出库调整
            - `400`: 调整单-尾差调整
            - `420`: 调整单-负库存数量调整
            - `405`: 调整单-期初成本录入

        :param transaction_numbers `<'str/list[str]/None'>`: 库存动作单号或列表, 默认 `None` (不筛选)
        :param source_numbers `<'str/list[str]/None'>`: 源头单据号或列表, 默认 `None` (不筛选)
        :param warehouse_names `<'str/list[str]/None'>`: 仓库名称或列表, 默认 `None` (不筛选)
        :param seller_names `<'str/list[str]/None'>`: 领星店铺名称或列表, 默认 `None` (不筛选)
        :param mskus `<'str/list[str]/None'>`: 亚马逊SKU或列表, 默认 `None` (不筛选)
        :param lskus `<'str/list[str]/None'>`: 领星本地SKU或列表, 默认 `None` (不筛选)
        :param dispositions `<'int/list[int]/None'>`: 库存处置结果或列表, 默认 `None` (不筛选), 可选值:

            - `1`: 可用在途
            - `2`: 可用
            - `3`: 次品

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 200)
        :returns `<'LedgerValuation'>`: 查询到的亚马逊库存价值台账结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    "uid": "e1a1e****************",
                    "transaction_type_code": "1",
                    "transaction_type": "期初库存-FBA上月结存",
                    "transaction_number": "",
                    "transaction_reason": "",
                    "source_numbers": "2025-05无源单入库，业务编号：FBA15K96M3KT，流水编号：20250500B0039T",
                    "seller_name": "STORE-UK",
                    "warehouse_name": "STORE-UK英国仓",
                    "msku": "SKU*******",
                    "lsku": "LOCAL*******",
                    "balance_qty": 211,
                    "purchase_unit_cost": 98.4179,
                    "purchase_total_cost": 20766.18,
                    "logistics_unit_cost": 0.0,
                    "logistics_total_cost": 0.0,
                    "other_unit_cost": 0.0,
                    "other_total_cost": 0.0,
                    "cost_source": "上月结存",
                    "disposition": "可用",
                    "source_data_time": "2025-09-10 00:14:30",
                    "transaction_date": "2025-08-01",
                    "data_version": "1757433678235",
                },
                ...
            ]
        }
        ```
        """
        url = route.LEDGER_VALUATION
        # 构建参数
        args = {
            "start_date": start_date,
            "end_date": end_date,
            "date_type": date_type,
            "transaction_types": transaction_types,
            "transaction_numbers": transaction_numbers,
            "source_numbers": source_numbers,
            "warehouse_names": warehouse_names,
            "seller_names": seller_names,
            "mskus": mskus,
            "lskus": lskus,
            "dispositions": dispositions,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.LedgerValuation.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.LedgerValuation.model_validate(data)

    # . 亚马逊广告数据 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    async def AdsInvoices(
        self,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        *,
        ads_type: ADS_TYPE | None = None,
        mids: int | list[int] | None = None,
        sids: int | list[int] | None = None,
        search_field: ADS_INVOICE_SEARCH_FIELD | None = None,
        search_value: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.AdsInvoices:
        """查询亚马逊广告发票信息

        ## Docs
        - 财务: [查询广告发票列表](https://apidoc.lingxing.com/#/docs/Finance/InvoiceList)

        :param start_date `<'str/date/datetime'>`: 开具发票的开始日期, 参数来源: `AdsInvoice.invoice_date`
        :param end_date `<'str/date/datetime'>`: 开具发票的结束日期, 参数来源: `AdsInvoice.invoice_date`
        :param ads_type `<'int/None'>`: 广告类型, 默认 `None` (不筛选), 可选值:

            - `'SP'`: 赞助产品广告 (Sponsored Products)
            - `'SB'`: 赞助品牌广告 (Sponsored Brands)
            - `'SBV'`: 赞助品牌视频广告 (Sponsored Brands Video)
            - `'SD'`: 赞助展示广告 (Sponsored Display)

        :param mids `<'int/list[int]/None'>`: 领星站点ID或ID列表 (Seller.mid), 默认 `None` (不筛选)
        :param sids `<'int/list[int]/None'>`: 领星店铺ID或ID列表 (Seller.sid), 默认 `None` (不筛选)
        :param search_field `<'str/None'>`: 搜索字段, 默认 `None` (不筛选), 可选值:

            - `'invoice_id'`: 广告发票编号
            - `'msku'`: 广告发票关联的亚马逊SKU
            - `'asin'`: 广告发票关联的商品ASIN
            - `'campaign_name'`: 广告发票关联的广告活动名称

        :param search_value `<'str/None'>`: 搜索值, 默认 `None` (不筛选), 与 `search_field` 配合使用
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 20)
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "",
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
                    # 领星店铺名称 [原字段 'store_name']
                    "seller_name": "Store-DE",
                    # 国家 (中文)
                    "country": "德国",
                    # 广告发票ID
                    "invoice_id": "239**********",
                    # 广告发票状态 [原字段 'status']
                    "invoice_status": "PAID_IN_FULL",
                    # 付款方式
                    "payment_method": "UNIFIED_BILLING",
                    # 广告花费 [原字段 'cost_amount']
                    "ads_cost_amt": 504.75,
                    # 税费 [原字段 'tax_amount']
                    "tax_amt": 0.0,
                    # 分摊费用 [原字段 'other_allocation_fee']
                    # 总发票金额中扣除的其他费或税费，按此发票的花费占比分摊
                    "allocation_amt": -0.35,
                    # 广告发票总金额 [原字段 'amount']
                    "invoice_amt": 504.4,
                    # 账单周期开始日期 [原字段 'from_date']
                    "billing_start_date": "2025-06-06",
                    # 账单周期结束日期 [原字段 'to_date']
                    "billing_end_date": "2025-06-13",
                    # 广告发票开具日期
                    "invoice_date": "2025-06-12",
                },
                ...
            ]
        }
        ```
        """
        url = route.ADS_INVOICES
        # 构建参数
        args = {
            "start_date": start_date,
            "end_date": end_date,
            "ads_type": ads_type,
            "mids": mids,
            "sids": sids,
            "search_field": search_field,
            "search_value": search_value,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdsInvoices.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.AdsInvoices.model_validate(data)

    async def AdsInvoiceDetail(
        self,
        sid: int,
        invoice_id: str,
    ) -> schema.AdsInvoiceDetail:
        """查询亚马逊广告发票详情

        ## Docs
        - 财务: [查询广告发票基本信息](https://apidoc.lingxing.com/#/docs/Finance/InvoiceDetail)

        :param sid `<'int'>`: 领星店铺ID (Seller.sid)
        :param invoice_id `<'str'>`: 广告发票ID (AdsInvoice.invoice_id)
        :returns `<'AdsInvoiceDetail'>`: 查询到的亚马逊广告发票详情结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 1,
            # 总数据量
            "total_count": 1,
            # 响应数据
            "data": {
                # 广告发票ID
                "invoice_id": "2962*********",
                # 付款方式
                "payment_method": "UNIFIED_BILLING",
                # 广告发票总金额 [原字段 'amount']
                "invoice_amt": 512.77,
                # 币种代码
                "currency_code": "GBP",
                # 币种图标
                "currency_icon": "￡",
                # 账单地址 [原字段 'address']
                "billing_address": "",
                # 账单周期开始日期 [原字段 'from_date']
                "billing_start_date": "2025-09-09",
                # 账单周期结束日期 [原字段 'to_date']
                "billing_end_date": "2025-09-10",
                # 广告发票开具日期
                "invoice_date": "2025-09-10",
            },
        }
        ```
        """
        url = route.ADS_INVOICE_DETAIL
        # 构建参数
        args = {
            "sid": sid,
            "invoice_id": invoice_id,
        }
        try:
            p = param.AdsInvoiceDetail.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.AdsInvoiceDetail.model_validate(data)

    async def AdsCampaignInvoices(
        self,
        sid: int,
        invoice_id: str,
        *,
        ads_type: ADS_TYPE | None = None,
        search_field: ADS_CAMPAIGN_INVOICE_SEARCH_FIELD | None = None,
        search_value: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.AdsCampaignInvoices:
        """查询亚马逊广告活动发票明细

        ## Docs
        - 财务: [查询广告发票活动列表](https://apidoc.lingxing.com/#/docs/Finance/InvoiceCampaignList)

        :param sid `<'int'>`: 领星店铺ID (Seller.sid)
        :param invoice_id `<'str'>`: 广告发票ID (AdsInvoice.invoice_id)
        :param ads_type `<'int/None'>`: 广告类型, 默认 `None` (不筛选), 可选值:

            - `'SP'`: 赞助产品广告 (Sponsored Products)
            - `'SB'`: 赞助品牌广告 (Sponsored Brands)
            - `'SBV'`: 赞助品牌视频广告 (Sponsored Brands Video)
            - `'SD'`: 赞助展示广告 (Sponsored Display)

        :param search_field `<'str/None'>`: 搜索字段, 默认 `None` (不筛选), 可选值:

            - `'item'`: 广告发票关联的商品, 如: 亚马逊SKU(SP/SD) 或 ASIN(SB/SBV)
            - `'campaign_name'`: 广告发票关联的广告活动名称

        :param search_value `<'str/None'>`: 搜索值, 默认 `None` (不筛选), 与 `search_field` 配合使用
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 20)
        :returns `<'AdsCampaignInvoices'>`: 查询到的亚马逊广告活动发票明细结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 广告活动ID
                    "campaign_id": "8537**********",
                    # 广告活动名称
                    "campaign_name": "商品推广",
                    # 广告数据来源 [原字段 'origin']
                    "source": "业务报告",
                    # 广告商品
                    "items": ["SKU********"],
                    # 广告类型 [原字段 'ads_type']
                    "ad_type": "SPONSORED PRODUCTS",
                    # 计价方式
                    "price_type": "CPC",
                    # 广告事件次数 [原字段 'cost_event_count']
                    "event_count": 1,
                    # 广告事件单次花费 [原字段 'cost_per_unit']
                    "cost_per_event": 0.41,
                    # 广告总花费 [原字段 'cost_amount']
                    "cost_amt": 0.41,
                    # 分摊费用 [原字段 'other_allocation_fee']
                    "allocation_amt": 0.0,
                    # 币种图标 [原字段 'currency_icon']
                    "currency_icon": "€",
                },
                ...
            ]
        }
        ```
        """
        url = route.ADS_CAMPAIGN_INVOICES
        # 构建参数
        args = {
            "sid": sid,
            "invoice_id": invoice_id,
            "ads_type": ads_type,
            "search_field": search_field,
            "search_value": search_value,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AdsCampaignInvoices.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.AdsCampaignInvoices.model_validate(data)

    # . 亚马逊损益报告 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    async def IncomeStatementSellers(
        self,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        *,
        query_dimension: int | None = None,
        mids: int | list[int] | None = None,
        sids: int | list[int] | None = None,
        transaction_status: INCOME_STATEMENT_TRANSACTION_STATUS | None = None,
        summarize: int | None = None,
        currency_code: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.IncomeStatementSellers:
        """查询损益报告-店铺维度

        ## Docs
        - 财务: [查询利润报表-店铺](https://apidoc.lingxing.com/#/docs/Finance/bdSeller)

        :param start_date `<'str/date/datetime'>`: 统计开始日期, 闭合区间
        :param end_date `<'str/date/datetime'>`: 统计结束日期, 闭合区间
        :param query_dimension `<'int/None'>`: 查询维度, 默认 `None` (使用: 0), 可选值:

            - `0`: 天维度, 开始和结束时间跨度不能超过31天
            - `1`: 月维度, 开始和结束时间跨度不能超过1个月

        :param mids `<'int/list[int]/None'>`: 领星站点ID或ID列表 (Seller.mid), 默认 `None` (不筛选)
        :param sids `<'int/list[int]/None'>`: 领星店铺ID或ID列表 (Seller.sid), 默认 `None` (不筛选)
        :param transaction_status `<'int/None'>`: 交易状态, 默认 `None` (使用: 'Disbursed'), 可选值:

            - `'Deferred'`: 订单未进入Transaction报告, 无法回款
            - `'Disbursed'`: 订单已进入Transaction报告, 可以回款
            - `'DisbursedAndSettled'`: 可以回款和预结算订单
            - `'All'`: 所有状态

        :param summarize `<'int/None'>`: 是否返回汇总数据, 默认 `None` (使用: 0), 可选值:

            - `0`: 返回原始数据
            - `1`: 返回汇总数据

        :param currency_code `<'str/None'>`: 结算金额目标转换货币代码, 默认 `None` (保持原结算货币)
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值 10000, 默认 `None` (使用: 15)
        :returns `<'IncomeStatementSellers'>`: 查询到的损益报告-店铺维度结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 币种代码 [原字段 'currencyCode']
                    "currency_code": "USD",
                    # 币种图标 [原字段 'currencyIcon']
                    "currency_icon": "$",
                    # 收入 - 总收入金额 [原字段 'grossProfitIncome']
                    "total_income": 221568.35,
                    # 收入 - 总销售金额 [原字段 'totalSalesAmount']
                    "product_sales": 235906.05,
                    # 收入 - 总销售数量 [原字段 'totalSalesQuantity']
                    "product_sales_qty": 6715,
                    # 收入 - 总销售退费 [原字段 'totalSalesRefunds']
                    "product_sales_refunds": -11807.03,
                    # 收入 - FBA销售金额 [原字段 'fbaSaleAmount']
                    "fba_product_sales": 235906.05,
                    # 收入 - FBA销售数量 [原字段 'fbaSalesQuantity']
                    "fba_product_sales_qty": 6715,
                    # 收入 - FBA销售退费 [原字段 'fbaSalesRefunds']
                    "fba_product_sales_refunds": -11807.03,
                    # 收入 - FBM销售金额 [原字段 'fbmSaleAmount']
                    "fbm_product_sales": 0.0,
                    # 收入 - FBM销售数量 [原字段 'fbmSalesQuantity']
                    "fbm_product_sales_qty": 0,
                    # 收入 - FBM销售退费 [原字段 'fbmSalesRefunds']
                    "fbm_product_sales_refunds": 0.0,
                    # 收入 - FBA库存赔付/补偿金额 [原字段 'fbaInventoryCredit']
                    "fba_inventory_credits": 3483.66,
                    # 收入 - FBA库存赔付/补偿数量 [原字段 'fbaInventoryCreditQuantity']
                    "fba_inventory_credit_qty": 169,
                    # 收入 - FBA清算收益金额 [原字段 'fbaLiquidationProceeds']
                    "fba_liquidation_proceeds": 0.0,
                    # 收入 - FBA清算收益调整金额 [原字段 'fbaLiquidationProceedsAdjustments']
                    "fba_liquidation_proceeds_adj": 0.0,
                    # 收入 - 配送运费收入金额 (买家支出) [原字段 'shippingCredits']
                    "shipping_credits": 6595.82,
                    # 收入 - 配送运费退款金额 (买家收入) [原字段 'shippingCreditRefunds']
                    "shipping_credit_refunds": -354.16,
                    # 收入 - 礼品包装费收入金额 (买家支出) [原字段 'giftWrapCredits']
                    "giftwrap_credits": 0.0,
                    # 收入 - 礼品包装费退款金额 (买家收入) [原字段 'giftWrapCreditRefunds']
                    "giftwrap_credit_refunds": 0.0,
                    # 收入 - 促销折扣金额 (卖家支出) [原字段 'promotionalRebates']
                    "promotional_rebates": -12777.02,
                    # 收入 - 促销折扣退款金额 (卖家收入) [原字段 'promotionalRebateRefunds']
                    "promotional_rebate_refunds": 521.03,
                    # 收入 - A-to-Z 保障/索赔金额 [原字段 'guaranteeClaims']
                    "a2z_guarantee_claims": 0.0,
                    # 收入 - 拒付金额 (拒付造成的让利（发生时为负数）) [原字段 'chargebacks']
                    "chargebacks": 0.0,
                    # 收入 - 亚马逊运费补偿金额 [原字段 'amazonShippingReimbursement']
                    "amazon_shipping_reimbursement": 0.0,
                    # 收入 - 亚马逊安全运输计划补偿金额 [原字段 'safeTReimbursement']
                    "safe_t_reimbursement": 0.0,
                    # 收入 - 其他补偿/赔付金额 [原字段 'reimbursements']
                    "other_reimbursement": 0.0,
                    # 收入 - 积分发放金额 (日本站) [原字段 'costOfPoIntegersGranted']
                    "points_granted": 0.0,
                    # 收入 - 积分退还金额 (日本站) [原字段 'costOfPoIntegersReturned']
                    "points_returned": 0.0,
                    # 收入 - 积分调整金额 (日本站) [原字段 'pointsAdjusted']
                    "points_adjusted": 0.0,
                    # 收入 - 货到付款金额 (COD) [原字段 'cashOnDelivery']
                    "cash_on_delivery": 0.0,
                    # 收入 - VAT进项税费金额 [原字段 'sharedComminglingVatIncome']
                    "commingling_vat_income": 0.0,
                    # 收入 - NetCo混合网络交易金额 [原字段 'netcoTransaction']
                    "netco_transaction": 0.0,
                    # 收入 - TDS 194-O净额 (印度站) [原字段 'tdsSection194ONet']
                    "tds_section_194o_net": 0.0,
                    # 收入 - 收回/冲回金额
                    "clawbacks": 0.0,
                    # 收入 - 其他收入金额 [原字段 'otherInAmount']
                    "other_income": 0.0,
                    # 支出 - FBA销售佣金 (Referral Fee) [原字段 'platformFee']
                    "fba_selling_fees": -19936.57,
                    # 支出 - FBA销售佣金退款金额 [原字段 'sellingFeeRefunds']
                    "fba_selling_fee_refunds": 1095.17,
                    # 支出 - FBA交易费用 [原字段 'totalFbaDeliveryFee']
                    # (fba_fulfillment_fees 到 fba_transaction_return_fees_alloc 之间所有费用)
                    "fba_transaction_fees": -23814.6,
                    # 支付 - FBA配送费用 (Fulfillment Fee) [原字段 'fbaDeliveryFee']
                    "fba_fulfillment_fees": -23769.11,
                    # 支出 - FBA多渠道配送费用 (Multi-Channel) [原字段 'mcFbaDeliveryFee']
                    "fba_mcf_fulfillment_fees": -45.49,
                    # 支出 - FBA多渠道配送费用 (分摊) [原字段 'sharedMcFbaFulfillmentFees']
                    "fba_mcf_fulfillment_fees_alloc": 0.0,
                    # 支出 - FBA多渠道配送数量 (Multi-Channel) [原字段 'mcFbaFulfillmentFeesQuantity']
                    "fba_mcf_fulfillment_qty": 7,
                    # 支出 - FBA客户退货处理费用 (分摊) [原字段 'sharedFbaCustomerReturnFee']
                    "fba_customer_return_fees_alloc": 0.0,
                    # 支出 - FBA交易退货处理费用 (分摊) [原字段 'sharedFbaTransactionCustomerReturnFee']
                    "fba_transaction_return_fees_alloc": 0.0,
                    # 支出 - FBA总配送费用退款金额 [原字段 'fbaTransactionFeeRefunds']
                    "fba_transaction_fee_refunds": 120.94,
                    # 支出 - 其他交易费用 [原字段 'otherTransactionFees']
                    "other_transaction_fees": 0.0,
                    # 支出 - 其他交易费用退款金额 [原字段 'otherTransactionFeeRefunds']
                    "other_transaction_fee_refunds": 0.0,
                    # 支出 - FBA仓储和入库服务总费用 [原字段 'totalStorageFee']
                    # ('fba_storage_fees' 到 'other_fba_inventory_fees_alloc' 之间的所有费用)
                    "fba_inventory_and_inbound_services_fees": -484.25,
                    # 支出 - FBA仓储费用 [原字段 'fbaStorageFee']
                    "fba_storage_fees": -151.64,
                    # 支出 - FBA仓储费用计提金额 [原字段 'fbaStorageFeeAccrual']
                    "fba_storage_fees_accr": 0.0,
                    # 支出 - FBA仓储费用计提调整金额 [原字段 'fbaStorageFeeAccrualDifference']
                    "fba_storage_fees_accr_adj": 0.0,
                    # 支出 - FBA仓储费用 (分摊) [原字段 'sharedFbaStorageFee']
                    "fba_storage_fees_alloc": 0.01,
                    # 支出 - FBA长期仓储费用 [原字段 'longTermStorageFee']
                    "fba_lt_storage_fees": 0.0,
                    # 支出 - FBA长期仓储费用计提金额 [原字段 'longTermStorageFeeAccrual']
                    "fba_lt_storage_fees_accr": 0.0,
                    # 支出 - FBA长期仓储费用计提调整金额 [原字段 'longTermStorageFeeAccrualDifference']
                    "fba_lt_storage_fees_accr_adj": 0.0,
                    # 支出 - FBA长期仓储费用 (分摊) [原字段 'sharedLongTermStorageFee']
                    "fba_lt_storage_fees_alloc": 0.0,
                    # 支出 - FBA仓储超储费用 (分摊) [原字段 'sharedFbaOverageFee']
                    "fba_overage_fees_alloc": 0.0,
                    # 支出 - FBA仓储续期费用 (分摊) [原字段 'sharedStorageRenewalBilling']
                    "fba_storage_renewal_fees_alloc": 0.0,
                    # 支出 - FBA仓鼠销毁费用 (分摊) [原字段 'sharedFbaDisposalFee']
                    "fba_disposal_fees_alloc": -2.08,
                    # 支出 - FBA仓储销毁数量 [原字段 'disposalQuantity']
                    "fba_disposal_qty": 0,
                    # 支出 - FBA仓储移除费用 (分摊) [原字段 'sharedFbaRemovalFee']
                    "fba_removal_fees_alloc": -330.54,
                    # 支出 - FBA仓储移除数量 [原字段 'removalQuantity']
                    "fba_removal_qty": 315,
                    # 支出 - FBA入库运输计划费用 (分摊) [原字段 'sharedFbaInboundTransportationProgramFee']
                    "fba_inbound_transportation_program_fees_alloc": 0.0,
                    # 支出 - FBA入库缺陷费用 (分摊) [原字段 'sharedFbaInboundDefectFee']
                    "fba_inbound_defect_fees_alloc": 0.0,
                    # 支出 - FBA国际入库费用 (分摊) [原字段 'sharedFbaIntegerernationalInboundFee']
                    "fba_international_inbound_fees_alloc": 0.0,
                    # 支出 - FBA合作承运商(入库)运费 (分摊) [原字段 'sharedAmazonPartneredCarrierShipmentFee']
                    "fba_partnered_carrier_shipment_fees_alloc": 0.0,
                    # 支出 - FBA人工处理费用 (分摊) [原字段 'sharedManualProcessingFee']
                    "fba_manual_processing_fees_alloc": 0.0,
                    # 支出 - AWD仓储费用 (分摊) [原字段 'sharedAwdStorageFee']
                    "awd_storage_fees_alloc": 0.0,
                    # 支出 - AWD处理费用 (分摊) [原字段 'sharedAwdProcessingFee']
                    "awd_processing_fees_alloc": 0.0,
                    # 支出 - AWD运输费用 (分摊) [原字段 'sharedAwdTransportationFee']
                    "awd_transportation_fees_alloc": 0.0,
                    # 支出 - AWD卫星仓储费用 (分摊) [原字段 'sharedStarStorageFee']
                    "awd_satellite_storage_fees_alloc": 0.0,
                    # 支出 - FBA库存费用调整金额 (分摊) [原字段 'sharedItemFeeAdjustment']
                    "fba_inventory_fees_adj_alloc": 0.0,
                    # 支出 - FBA其他库存费用 (分摊) [原字段 'sharedOtherFbaInventoryFees']
                    "other_fba_inventory_fees_alloc": 0.0,
                    # 支出 - 运输标签花费金额 [原字段 'shippingLabelPurchases']
                    "shipping_label_purchases": 0.0,
                    # 支出 - FBA贴标费用 (分摊) [原字段 'sharedLabelingFee']
                    "fba_labeling_fees_alloc": 0.0,
                    # 支出 - FBA塑封袋费用 (分摊) [原字段 'sharedPolybaggingFee']
                    "fba_polybagging_fees_alloc": 0.0,
                    # 支出 - FBA气泡膜费用 (分摊) [原字段 'sharedBubblewrapFee']
                    "fba_bubblewrap_fees_alloc": 0.0,
                    # 支出 - FBA封箱胶带费用 (分摊) [原字段 'sharedTapingFee']
                    "fba_taping_fees_alloc": 0.0,
                    # 支出 - FBM邮寄资费 (分摊) [原字段 'sharedMfnPostageFee']
                    "mfn_postage_fees_alloc": 0.0,
                    # 支出 - 运输标签退款金额 [原字段 'shippingLabelRefunds']
                    "shipping_label_refunds": 0.0,
                    # 支出 - 承运商运输标签花费调整金额 [原字段 'sharedCarrierShippingLabelAdjustments']
                    "carrier_shipping_label_adj": 0.0,
                    # 支出 - 总推广费用 (Service Fee) [原字段 'promotionFee']
                    # (subscription_fees_alloc 到 early_reviewer_program_fees_alloc 之间的所有费用)
                    "promotion_fees": -679.97,
                    # 支出 - 订阅服务费 (分摊) [原字段 'sharedSubscriptionFee']
                    "subscription_fees_alloc": -39.99,
                    # 支出 - 优惠券费用 (分摊) [原字段 'sharedCouponFee']
                    "coupon_fees_alloc": -239.98,
                    # 支出 - 秒杀费用 (分摊) [原字段 'sharedLdFee']
                    "deal_fees_alloc": 0.0,
                    # 支出 - Vine费用 (分摊) [原字段 'sharedVineFee']
                    "vine_fees_alloc": -400.0,
                    # 支出 - 早期评论人计划费用 (分摊) [原字段 'sharedEarlyReviewerProgramFee']
                    "early_reviewer_program_fees_alloc": 0.0,
                    # 支出 - FBA入库便利费用 (Service Fee/分摊) [原字段 'sharedFbaInboundConvenienceFee']
                    "fba_inbound_convenience_fees_alloc": 0.0,
                    # 支出 - 其他亚马逊服务费用 (分摊) [原字段 'totalPlatformOtherFee']
                    "other_service_fees_alloc": -1733.33,
                    # 支出 - 亚马逊退款管理费用 [原字段 'refundAdministrationFees']
                    "refund_administration_fees": -219.15,
                    # 支出 - 总费用退款金额 [totalFeeRefunds]
                    # (fba_selling_fee_refunds + fba_transaction_fee_refunds + refund_administration_fees)
                    "total_fee_refunds": 996.96,
                    # 支出 - 其他费用调整金额
                    "adjustments": -163.14,
                    # 支出 - 广告总花费 (Cost of Advertising) [原字段 'totalAdsCost']
                    # (ads_sp_cost + ads_sb_cost + ads_sbv_cost + ads_sd_cost + ads_cost_alloc +
                    #  ads_amazon_live_cost_alloc + ads_creator_connections_cost_alloc +
                    #  ads_sponsored_tv_cost_alloc + ads_retail_ad_service_alloc)
                    "ads_cost": -27743.22,
                    # 支出 - 广告总销售金额 [原字段 'totalAdsSales']
                    "ads_sales": 142803.87,
                    # 支出 - 广告总销售数量 [原字段 'totalAdsSalesQuantity']
                    "ads_sales_qty": 3333,
                    # 支出 - SP广告花费 (Sponsored Products) [原字段 'adsSpCost']
                    "ads_sp_cost": -22291.36,
                    # 支出 - SP广告销售金额 [原字段 'adsSpSales']
                    "ads_sp_sales": 97531.25,
                    # 支出 - SP广告销售数量 [原字段 'adsSpSalesQuantity']
                    "ads_sp_sales_qty": 2305,
                    # 支出 - SB广告花费 (Sponsored Brands) [原字段 'adsSbCost']
                    "ads_sb_cost": -5451.86,
                    # 支出 - SB广告销售金额 [原字段 'sharedAdsSbSales']
                    "ads_sb_sales": 25464.72,
                    # 支出 - SB广告销售数量 [原字段 'sharedAdsSbSalesQuantity']
                    "ads_sb_sales_qty": 552,
                    # 支出 - SBV广告花费 (Sponsored Brands Video) [原字段 'adsSbvCost']
                    "ads_sbv_cost": 0.0,
                    # 支出 - SBV广告销售金额 [原字段 'sharedAdsSbvSales']
                    "ads_sbv_sales": 19807.9,
                    # 支出 - SBV广告销售数量 [原字段 'sharedAdsSbvSalesQuantity']
                    "ads_sbv_sales_qty": 476,
                    # 支出 - SD广告花费 (Sponsored Display) [原字段 'adsSdCost']
                    "ads_sd_cost": 0.0,
                    # 支出 - SD广告销售金额 [原字段 'adsSdSales']
                    "ads_sd_sales": 0.0,
                    # 支出 - SD广告销售数量 [原字段 'adsSdSalesQuantity']
                    "ads_sd_sales_qty": 0,
                    # 支出 - 广告分摊费用 [原字段 'sharedCostOfAdvertising']
                    "ads_cost_alloc": 0.0,
                    # 支出 - Live广告花费 (分摊) [原字段 'sharedAdsAlCost']
                    "ads_amazon_live_cost_alloc": 0.0,
                    # 支出 - 内容创作者计划花费 (分摊) [原字段 'sharedAdsCcCost']
                    "ads_creator_connections_cost_alloc": 0.0,
                    # 支出 - TV广告花费 (分摊) [原字段 'sharedAdsSspaotCost']
                    "ads_sponsored_tv_cost_alloc": 0.0,
                    # 支出 - 零售商赞助广告花费 (分摊) [原字段 'sharedAdsSarCost']
                    "ads_retail_ad_service_alloc": 0.0,
                    # 支出 - 广告总退款金额 (Refund for Advertiser) [原字段 'refundForAdvertiser']
                    "ads_cost_refunds": 0.0,
                    # 支出 - 清算服务费 (分摊) [原字段 'sharedLiquidationsFees']
                    "liquidation_service_fees_alloc": 0.0,
                    # 支出 - 应收账款扣减 (分摊) [原字段 'sharedReceivablesDeductions']
                    "receivables_deductions_alloc": 0.0,
                    # 支出 - 亚马逊运费调整 (分摊) [原字段 'sharedAmazonShippingChargeAdjustments']
                    "amazon_shipping_charge_adj_alloc": 0.0,
                    # 支出 - VAT销项税费金额 [原字段 'sharedComminglingVatExpenses']
                    "commingling_vat_expenses": 0.0,
                    # 支出 - 其他支出费用 [原字段 'others']
                    "other_expenses": 0.0,
                    # 支出 - 用户自定义推广总费用 [原字段 'customOrderFee']
                    "user_promotion_fees": 0.0,
                    # (user_promotion_principal + user_promotion_commission)
                    # 支出 - 用户自定义推广费用本金 [原字段 'customOrderFeePrincipal']
                    "user_promotion_principal": 0.0,
                    # 支出 - 用户自定义推广佣金费用 [原字段 'customOrderFeeCommission']
                    "user_promotion_commission": 0.0,
                    # 支出 - 用户自定义其他费用 [原字段 'otherFeeStr']
                    "user_other_fees": [],
                    # 税费 - 总税费 [grossProfitTax]
                    "total_tax": 0.0,
                    # 税费 - 总销税收金额 [原字段 'totalSalesTax']
                    # ('product_tax_collected' 到 'tcs_cgst_collected' 之间的所有税费)
                    "sales_tax_collected": 15036.42,
                    # 税费 - 商品销售税收金额 [原字段 'taxCollectedProduct']
                    "product_tax_collected": 15006.18,
                    # 税费 - 配送运费税收金额 [原字段 'taxCollectedShipping']
                    "shipping_tax_collected": 18.58,
                    # 税费 - 礼品包装税收金额 [原字段 'taxCollectedGiftWrap']
                    "giftwrap_tax_collected": 0.0,
                    # 税费 - 促销折扣税收金额 [原字段 'taxCollectedDiscount']
                    "promotional_rebate_tax_collected": 0.0,
                    # 税费 - VAT/GST税收金额 [原字段 'taxCollected']
                    "vat_gst_tax_collected": 11.66,
                    # 税费 - TCS IGST税收金额 (印度站) [原字段 'tcsIgstCollected']
                    "tcs_igst_collected": 0.0,
                    # 税费 - TCS SGST税收金额 (印度站) [原字段 'tcsSgstCollected']
                    "tcs_sgst_collected": 0.0,
                    # 税费 - TCS CGST税收金额 (印度站) [原字段 'tcsCgstCollected']
                    "tcs_cgst_collected": 0.0,
                    # 税费 - 总销售税代扣金额 [原字段 'salesTaxWithheld']
                    "sales_tax_withheld": -15036.42,
                    # 税费 - 总销售税费退款 [salesTaxRefund]
                    # ('product_tax_refunded' 到 'tcs_cgst_refunded' 之间的所有税费退款)
                    "sales_tax_refunded": -784.31,
                    # 税费 - 商品销售税费退款金额 [原字段 'taxRefundedProduct']
                    "product_tax_refunded": -783.0,
                    # 税费 - 配送运费税费退款金额 [原字段 'taxRefundedShipping']
                    "shipping_tax_refunded": -1.31,
                    # 税费 - 礼品包装税费退款金额 [原字段 'taxRefundedGiftWrap']
                    "giftwrap_tax_refunded": 0.0,
                    # 税费 - 促销折扣税费退款金额 [原字段 'taxRefundedDiscount']
                    "promotional_rebate_tax_refunded": 0.0,
                    # 税费 - VAT/GST税费退款金额 [原字段 'taxRefunded']
                    "vat_gst_tax_refunded": 0.0,
                    # 税费 - TCS IGST税费退款金额 (印度站) [原字段 'tcsIgstRefunded']
                    "tcs_igst_refunded": 0.0,
                    # 税费 - TCS SGST税费退款金额 (印度站) [原字段 'tcsSgstRefunded']
                    "tcs_sgst_refunded": 0.0,
                    # 税费 - TCS CGST税费退款金额 (印度站) [原字段 'tcsCgstRefunded']
                    "tcs_cgst_refunded": 0.0,
                    # 税费 - 总退款税代扣金额 [原字段 'refundTaxWithheld']
                    "refund_tax_withheld": 784.31,
                    # 税费 - 其他税费调整 (分摊) [原字段 'sharedTaxAdjustment']
                    "other_tax_adj_alloc": 0.0,
                    # 成本 - 总退款数量 [原字段 'refundsQuantity']
                    "total_refunds_qty": 329,
                    # 成本 - 总退款率 [原字段 'refundsRate']
                    # (total_refund_qty / (fba&fbm_product_sales_qty + fba_mcf_fulfillment_qty + fba_reshipment_qty))
                    "total_refunds_rate": 0.0486,
                    # 成本 - FBA退货数量 [原字段 'fbaReturnsQuantity']
                    "fba_returns_qty": 363,
                    # 成本 - FBA退货可售数量 [原字段 'fbaReturnsSaleableQuantity']
                    "fba_returns_saleable_qty": 12,
                    # 成本 - FBA退货不可售数量 [原字段 'fbaReturnsUnsaleableQuantity']
                    "fba_returns_unsaleable_qty": 351,
                    # 成本 - FBA退货率 [原字段 'fbaReturnsQuantityRate']
                    # (fba_returns_qty / (fba_product_sales_qty + fba_mcf_fulfillment_qty))
                    "fba_returns_rate": 0.054,
                    # 成本 - 总补发/换货数量 [原字段 'totalReshipQuantity']
                    "total_reshipment_qty": 50,
                    # 成本 - FBA补发/换货数量 [原字段 'reshipFbaProductSalesQuantity']
                    "fba_reshipment_qty": 47,
                    # 成本 - FBA换货退回数量 [原字段 'reshipFbaProductSaleRefundsQuantity']
                    "fba_reshipment_returned_qty": 3,
                    # 成本 - FBM补发/换货数量 [原字段 'reshipFbmProductSalesQuantity']
                    "fbm_reshipment_qty": 0,
                    # 成本 - FBM换货退回数量 [原字段 'reshipFbmProductSaleRefundsQuantity']
                    "fbm_reshipment_returned_qty": 0,
                    # 成本 - 总成本数量 [原字段 'cgQuantity']
                    # (fba&fbm_product_sales_qty + fba_mcf_fulfillment_qty + fba&fbm_reshipment_qty - fba_returns_saleable_qty)
                    "cost_of_goods_qty": -6757,
                    # 成本 - 重成本数量绝对值 [原字段 'cgAbsQuantity']
                    "cost_of_goods_abs_qty": 6780,
                    # 成本 - 总成本金额 (COGS) [原字段 'totalCost']
                    # (purchase_cost + logistics_cost + other_costs)
                    "cost_of_goods": -100790.7,
                    # 成本 - 总成本占比 [原字段 'proportionOfTotalCost']
                    "cost_of_goods_ratio": 0.4272,
                    # 成本 - 总采购成本 (COGS) [原字段 'cgPriceTotal']
                    "purchase_cost": -100790.7,
                    # 成本 - 总采购绝对成本 [原字段 'cgPriceAbsTotal']
                    "purchase_abs_cost": 100890.7,
                    # 成本 - 单品成本 [原字段 'cgUnitPrice']
                    "purchase_unit_cost": 14.93,
                    # 成本 - 采购成本占比 [原字段 'proportionOfCg']
                    "purchase_cost_ratio": 0.4272,
                    # 成本 - 是否有成本明细 [原字段 'hasCgPriceDetail']
                    "has_purchase_cost_detail": 1,
                    # 成本 - 总物流费用 [原字段 'cgTransportCostsTotal']
                    "logistics_cost": 0.0,
                    # 成本 - 物流单品费用 [原字段 'cgTransportUnitCosts']
                    "logistics_unit_cost": 0.0,
                    # 成本 - 物流费用占比 [原字段 'proportionOfCgTransport']
                    "logistics_cost_ratio": 0.0,
                    # 成本 - 是否有物流费用明细 [原字段 'hasCgTransportCostsDetail']
                    "has_logistics_cost_detail": 1,
                    # 成本 - 其他费用总金额 [原字段 'cgOtherCostsTotal']
                    "other_costs": 0.0,
                    # 成本 - 其他费用单品金额 [原字段 'cgOtherUnitCosts']
                    "other_unit_cost": 0.0,
                    # 成本 - 其他费用占比 [原字段 'proportionOfCgOtherCosts']
                    "other_cost_ratio": 0.0,
                    # 成本 - 是否有其他费用明细 [原字段 'hasCgOtherCostsDetail']
                    "has_other_cost_detail": 0,
                    # 利润 - 毛利润 [原字段 'grossProfit']
                    "gross_profit": 47219.53,
                    # 利润 - 毛利率 [原字段 'grossRate']
                    "gross_profit_margin": 0.2131,
                    # 利润 - 投资回报率 (ROI)
                    "roi": 0.2693,
                    # 交易状态 [原字段 'transactionStatusCode']
                    "transaction_status": "Disbursed",
                    # 交易状态描述 [原字段 'transactionStatus']
                    "transaction_status_desc": "已发放",
                    # 延迟结算状态 [原字段 'deferredSubStatusCode']
                    "deferred_settlement_status": "Disbursed",
                    # 延迟结算状态描述 [原字段 'deferredSubStatus']
                    "deferred_settlement_status_desc": "",
                    # 延迟结算总金额 [原字段 'deferredSettlementAmount']
                    "deferred_settlement": 186019.17,
                    # 结算小计 [原字段 'settlementSubtotal']
                    "settlement_subtotal": 186019.17,
                    # 报告时间 (本地时间) [原字段 'postedDateDayLocale']
                    "report_time_loc": "",
                    # 报告开始时间 (本地时间) [原字段 'minPostedDateDayLocale']
                    "report_start_time_loc": "",
                    # 报告结束时间 (本地时间) [原字段 'maxPostedDateDayLocale']
                    "report_end_time_loc": "",
                    # 报告日期 (本地时间) [原字段 'postedDateLocale']
                    "report_date_loc": "2025-08",
                    # 领星店铺ID
                    "sid": 1,
                    # 领星店铺名称 [原字段 'storeName']
                    "seller_name": "Store-US",
                    # 国家 (中文)
                    "country": "美国",
                    # 国家代码 [原字段 'countryCode']
                    "country_code": "US",
                    # 店铺负责人名称 (逗号隔开) [原字段 'sellerPrincipalRealname']
                    "operator_names": "白小白,黑小黑",
                },
                ...
            ]
        }
        ```
        """
        url = route.INCOME_STATEMENT_SELLERS
        # 构建参数
        args = {
            "start_date": start_date,
            "end_date": end_date,
            "mids": mids,
            "sids": sids,
            "query_dimension": query_dimension,
            "transaction_status": transaction_status,
            "summarize": summarize,
            "currency_code": currency_code,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.IncomeStatementSellers.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.IncomeStatementSellers.model_validate(data)

    async def IncomeStatementAsins(
        self,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        *,
        query_dimension: int | None = None,
        mids: int | list[int] | None = None,
        sids: int | list[int] | None = None,
        transaction_status: INCOME_STATEMENT_TRANSACTION_STATUS | None = None,
        summarize: int | None = None,
        currency_code: str | None = None,
        search_value: str | list[str] | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.IncomeStatementAsins:
        """查询损益报告-ASIN维度

        ## Docs
        - 财务: [查询利润报表-ASIN](https://apidoc.lingxing.com/#/docs/Finance/bdASIN)

        :param start_date `<'str/date/datetime'>`: 统计开始日期, 闭合区间
        :param end_date `<'str/date/datetime'>`: 统计结束日期, 闭合区间
        :param query_dimension `<'int/None'>`: 查询维度, 默认 `None` (使用: 0), 可选值:

            - `0`: 天维度, 开始和结束时间跨度不能超过31天
            - `1`: 月维度, 开始和结束时间跨度不能超过1个月

        :param mids `<'int/list[int]/None'>`: 领星站点ID或ID列表 (Seller.mid), 默认 `None` (不筛选)
        :param sids `<'int/list[int]/None'>`: 领星店铺ID或ID列表 (Seller.sid), 默认 `None` (不筛选)
        :param transaction_status `<'int/None'>`: 交易状态, 默认 `None` (使用: 'Disbursed'), 可选值:

            - `'Deferred'`: 订单未进入Transaction报告, 无法回款
            - `'Disbursed'`: 订单已进入Transaction报告, 可以回款
            - `'DisbursedAndSettled'`: 可以回款和预结算订单
            - `'All'`: 所有状态

        :param summarize `<'int/None'>`: 是否返回汇总数据, 默认 `None` (使用: 0), 可选值:

            - `0`: 返回原始数据
            - `1`: 返回汇总数据

        :param currency_code `<'str/None'>`: 结算金额目标转换货币代码, 默认 `None` (保持原结算货币)
        :param search_value `<'str/list[str]/None'>`: 搜索值, 默认 `None` (不筛选), 可传入单个ASIN或ASIN列表
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值 10000, 默认 `None` (使用: 15)
        :returns `<'IncomeStatementAsins'>`: 查询到的损益报告-ASIN维度结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 币种代码 [原字段 'currencyCode']
                    "currency_code": "USD",
                    # 币种图标 [原字段 'currencyIcon']
                    "currency_icon": "$",
                    # 收入 - 总收入金额 [原字段 'grossProfitIncome']
                    "total_income": 221568.35,
                    # 收入 - 总销售金额 [原字段 'totalSalesAmount']
                    "product_sales": 235906.05,
                    # 收入 - 总销售数量 [原字段 'totalSalesQuantity']
                    "product_sales_qty": 6715,
                    # 收入 - 总销售退费 [原字段 'totalSalesRefunds']
                    "product_sales_refunds": -11807.03,
                    # 收入 - FBA销售金额 [原字段 'fbaSaleAmount']
                    "fba_product_sales": 235906.05,
                    # 收入 - FBA销售数量 [原字段 'fbaSalesQuantity']
                    "fba_product_sales_qty": 6715,
                    # 收入 - FBA销售退费 [原字段 'fbaSalesRefunds']
                    "fba_product_sales_refunds": -11807.03,
                    # 收入 - FBM销售金额 [原字段 'fbmSaleAmount']
                    "fbm_product_sales": 0.0,
                    # 收入 - FBM销售数量 [原字段 'fbmSalesQuantity']
                    "fbm_product_sales_qty": 0,
                    # 收入 - FBM销售退费 [原字段 'fbmSalesRefunds']
                    "fbm_product_sales_refunds": 0.0,
                    # 收入 - FBA库存赔付/补偿金额 [原字段 'fbaInventoryCredit']
                    "fba_inventory_credits": 3483.66,
                    # 收入 - FBA库存赔付/补偿数量 [原字段 'fbaInventoryCreditQuantity']
                    "fba_inventory_credit_qty": 169,
                    # 收入 - FBA清算收益金额 [原字段 'fbaLiquidationProceeds']
                    "fba_liquidation_proceeds": 0.0,
                    # 收入 - FBA清算收益调整金额 [原字段 'fbaLiquidationProceedsAdjustments']
                    "fba_liquidation_proceeds_adj": 0.0,
                    # 收入 - 配送运费收入金额 (买家支出) [原字段 'shippingCredits']
                    "shipping_credits": 6595.82,
                    # 收入 - 配送运费退款金额 (买家收入) [原字段 'shippingCreditRefunds']
                    "shipping_credit_refunds": -354.16,
                    # 收入 - 礼品包装费收入金额 (买家支出) [原字段 'giftWrapCredits']
                    "giftwrap_credits": 0.0,
                    # 收入 - 礼品包装费退款金额 (买家收入) [原字段 'giftWrapCreditRefunds']
                    "giftwrap_credit_refunds": 0.0,
                    # 收入 - 促销折扣金额 (卖家支出) [原字段 'promotionalRebates']
                    "promotional_rebates": -12777.02,
                    # 收入 - 促销折扣退款金额 (卖家收入) [原字段 'promotionalRebateRefunds']
                    "promotional_rebate_refunds": 521.03,
                    # 收入 - A-to-Z 保障/索赔金额 [原字段 'guaranteeClaims']
                    "a2z_guarantee_claims": 0.0,
                    # 收入 - 拒付金额 (拒付造成的让利（发生时为负数）) [原字段 'chargebacks']
                    "chargebacks": 0.0,
                    # 收入 - 亚马逊运费补偿金额 [原字段 'amazonShippingReimbursement']
                    "amazon_shipping_reimbursement": 0.0,
                    # 收入 - 亚马逊安全运输计划补偿金额 [原字段 'safeTReimbursement']
                    "safe_t_reimbursement": 0.0,
                    # 收入 - 其他补偿/赔付金额 [原字段 'reimbursements']
                    "other_reimbursement": 0.0,
                    # 收入 - 积分发放金额 (日本站) [原字段 'costOfPoIntegersGranted']
                    "points_granted": 0.0,
                    # 收入 - 积分退还金额 (日本站) [原字段 'costOfPoIntegersReturned']
                    "points_returned": 0.0,
                    # 收入 - 积分调整金额 (日本站) [原字段 'pointsAdjusted']
                    "points_adjusted": 0.0,
                    # 收入 - 货到付款金额 (COD) [原字段 'cashOnDelivery']
                    "cash_on_delivery": 0.0,
                    # 收入 - VAT进项税费金额 [原字段 'sharedComminglingVatIncome']
                    "commingling_vat_income": 0.0,
                    # 收入 - NetCo混合网络交易金额 [原字段 'netcoTransaction']
                    "netco_transaction": 0.0,
                    # 收入 - TDS 194-O净额 (印度站) [原字段 'tdsSection194ONet']
                    "tds_section_194o_net": 0.0,
                    # 收入 - 收回/冲回金额
                    "clawbacks": 0.0,
                    # 收入 - 其他收入金额 [原字段 'otherInAmount']
                    "other_income": 0.0,
                    # 支出 - FBA销售佣金 (Referral Fee) [原字段 'platformFee']
                    "fba_selling_fees": -19936.57,
                    # 支出 - FBA销售佣金退款金额 [原字段 'sellingFeeRefunds']
                    "fba_selling_fee_refunds": 1095.17,
                    # 支出 - FBA交易费用 [原字段 'totalFbaDeliveryFee']
                    # (fba_fulfillment_fees 到 fba_transaction_return_fees_alloc 之间所有费用)
                    "fba_transaction_fees": -23814.6,
                    # 支付 - FBA配送费用 (Fulfillment Fee) [原字段 'fbaDeliveryFee']
                    "fba_fulfillment_fees": -23769.11,
                    # 支出 - FBA多渠道配送费用 (Multi-Channel) [原字段 'mcFbaDeliveryFee']
                    "fba_mcf_fulfillment_fees": -45.49,
                    # 支出 - FBA多渠道配送费用 (分摊) [原字段 'sharedMcFbaFulfillmentFees']
                    "fba_mcf_fulfillment_fees_alloc": 0.0,
                    # 支出 - FBA多渠道配送数量 (Multi-Channel) [原字段 'mcFbaFulfillmentFeesQuantity']
                    "fba_mcf_fulfillment_qty": 7,
                    # 支出 - FBA客户退货处理费用 (分摊) [原字段 'sharedFbaCustomerReturnFee']
                    "fba_customer_return_fees_alloc": 0.0,
                    # 支出 - FBA交易退货处理费用 (分摊) [原字段 'sharedFbaTransactionCustomerReturnFee']
                    "fba_transaction_return_fees_alloc": 0.0,
                    # 支出 - FBA总配送费用退款金额 [原字段 'fbaTransactionFeeRefunds']
                    "fba_transaction_fee_refunds": 120.94,
                    # 支出 - 其他交易费用 [原字段 'otherTransactionFees']
                    "other_transaction_fees": 0.0,
                    # 支出 - 其他交易费用退款金额 [原字段 'otherTransactionFeeRefunds']
                    "other_transaction_fee_refunds": 0.0,
                    # 支出 - FBA仓储和入库服务总费用 [原字段 'totalStorageFee']
                    # ('fba_storage_fees' 到 'other_fba_inventory_fees_alloc' 之间的所有费用)
                    "fba_inventory_and_inbound_services_fees": -484.25,
                    # 支出 - FBA仓储费用 [原字段 'fbaStorageFee']
                    "fba_storage_fees": -151.64,
                    # 支出 - FBA仓储费用计提金额 [原字段 'fbaStorageFeeAccrual']
                    "fba_storage_fees_accr": 0.0,
                    # 支出 - FBA仓储费用计提调整金额 [原字段 'fbaStorageFeeAccrualDifference']
                    "fba_storage_fees_accr_adj": 0.0,
                    # 支出 - FBA仓储费用 (分摊) [原字段 'sharedFbaStorageFee']
                    "fba_storage_fees_alloc": 0.01,
                    # 支出 - FBA长期仓储费用 [原字段 'longTermStorageFee']
                    "fba_lt_storage_fees": 0.0,
                    # 支出 - FBA长期仓储费用计提金额 [原字段 'longTermStorageFeeAccrual']
                    "fba_lt_storage_fees_accr": 0.0,
                    # 支出 - FBA长期仓储费用计提调整金额 [原字段 'longTermStorageFeeAccrualDifference']
                    "fba_lt_storage_fees_accr_adj": 0.0,
                    # 支出 - FBA长期仓储费用 (分摊) [原字段 'sharedLongTermStorageFee']
                    "fba_lt_storage_fees_alloc": 0.0,
                    # 支出 - FBA仓储超储费用 (分摊) [原字段 'sharedFbaOverageFee']
                    "fba_overage_fees_alloc": 0.0,
                    # 支出 - FBA仓储续期费用 (分摊) [原字段 'sharedStorageRenewalBilling']
                    "fba_storage_renewal_fees_alloc": 0.0,
                    # 支出 - FBA仓鼠销毁费用 (分摊) [原字段 'sharedFbaDisposalFee']
                    "fba_disposal_fees_alloc": -2.08,
                    # 支出 - FBA仓储销毁数量 [原字段 'disposalQuantity']
                    "fba_disposal_qty": 0,
                    # 支出 - FBA仓储移除费用 (分摊) [原字段 'sharedFbaRemovalFee']
                    "fba_removal_fees_alloc": -330.54,
                    # 支出 - FBA仓储移除数量 [原字段 'removalQuantity']
                    "fba_removal_qty": 315,
                    # 支出 - FBA入库运输计划费用 (分摊) [原字段 'sharedFbaInboundTransportationProgramFee']
                    "fba_inbound_transportation_program_fees_alloc": 0.0,
                    # 支出 - FBA入库缺陷费用 (分摊) [原字段 'sharedFbaInboundDefectFee']
                    "fba_inbound_defect_fees_alloc": 0.0,
                    # 支出 - FBA国际入库费用 (分摊) [原字段 'sharedFbaIntegerernationalInboundFee']
                    "fba_international_inbound_fees_alloc": 0.0,
                    # 支出 - FBA合作承运商(入库)运费 (分摊) [原字段 'sharedAmazonPartneredCarrierShipmentFee']
                    "fba_partnered_carrier_shipment_fees_alloc": 0.0,
                    # 支出 - FBA人工处理费用 (分摊) [原字段 'sharedManualProcessingFee']
                    "fba_manual_processing_fees_alloc": 0.0,
                    # 支出 - AWD仓储费用 (分摊) [原字段 'sharedAwdStorageFee']
                    "awd_storage_fees_alloc": 0.0,
                    # 支出 - AWD处理费用 (分摊) [原字段 'sharedAwdProcessingFee']
                    "awd_processing_fees_alloc": 0.0,
                    # 支出 - AWD运输费用 (分摊) [原字段 'sharedAwdTransportationFee']
                    "awd_transportation_fees_alloc": 0.0,
                    # 支出 - AWD卫星仓储费用 (分摊) [原字段 'sharedStarStorageFee']
                    "awd_satellite_storage_fees_alloc": 0.0,
                    # 支出 - FBA库存费用调整金额 (分摊) [原字段 'sharedItemFeeAdjustment']
                    "fba_inventory_fees_adj_alloc": 0.0,
                    # 支出 - FBA其他库存费用 (分摊) [原字段 'sharedOtherFbaInventoryFees']
                    "other_fba_inventory_fees_alloc": 0.0,
                    # 支出 - 运输标签花费金额 [原字段 'shippingLabelPurchases']
                    "shipping_label_purchases": 0.0,
                    # 支出 - FBA贴标费用 (分摊) [原字段 'sharedLabelingFee']
                    "fba_labeling_fees_alloc": 0.0,
                    # 支出 - FBA塑封袋费用 (分摊) [原字段 'sharedPolybaggingFee']
                    "fba_polybagging_fees_alloc": 0.0,
                    # 支出 - FBA气泡膜费用 (分摊) [原字段 'sharedBubblewrapFee']
                    "fba_bubblewrap_fees_alloc": 0.0,
                    # 支出 - FBA封箱胶带费用 (分摊) [原字段 'sharedTapingFee']
                    "fba_taping_fees_alloc": 0.0,
                    # 支出 - FBM邮寄资费 (分摊) [原字段 'sharedMfnPostageFee']
                    "mfn_postage_fees_alloc": 0.0,
                    # 支出 - 运输标签退款金额 [原字段 'shippingLabelRefunds']
                    "shipping_label_refunds": 0.0,
                    # 支出 - 承运商运输标签花费调整金额 [原字段 'sharedCarrierShippingLabelAdjustments']
                    "carrier_shipping_label_adj": 0.0,
                    # 支出 - 总推广费用 (Service Fee) [原字段 'promotionFee']
                    # (subscription_fees_alloc 到 early_reviewer_program_fees_alloc 之间的所有费用)
                    "promotion_fees": -679.97,
                    # 支出 - 订阅服务费 (分摊) [原字段 'sharedSubscriptionFee']
                    "subscription_fees_alloc": -39.99,
                    # 支出 - 优惠券费用 (分摊) [原字段 'sharedCouponFee']
                    "coupon_fees_alloc": -239.98,
                    # 支出 - 秒杀费用 (分摊) [原字段 'sharedLdFee']
                    "deal_fees_alloc": 0.0,
                    # 支出 - Vine费用 (分摊) [原字段 'sharedVineFee']
                    "vine_fees_alloc": -400.0,
                    # 支出 - 早期评论人计划费用 (分摊) [原字段 'sharedEarlyReviewerProgramFee']
                    "early_reviewer_program_fees_alloc": 0.0,
                    # 支出 - FBA入库便利费用 (Service Fee/分摊) [原字段 'sharedFbaInboundConvenienceFee']
                    "fba_inbound_convenience_fees_alloc": 0.0,
                    # 支出 - 其他亚马逊服务费用 (分摊) [原字段 'totalPlatformOtherFee']
                    "other_service_fees_alloc": -1733.33,
                    # 支出 - 亚马逊退款管理费用 [原字段 'refundAdministrationFees']
                    "refund_administration_fees": -219.15,
                    # 支出 - 总费用退款金额 [totalFeeRefunds]
                    # (fba_selling_fee_refunds + fba_transaction_fee_refunds + refund_administration_fees)
                    "total_fee_refunds": 996.96,
                    # 支出 - 其他费用调整金额
                    "adjustments": -163.14,
                    # 支出 - 广告总花费 (Cost of Advertising) [原字段 'totalAdsCost']
                    # (ads_sp_cost + ads_sb_cost + ads_sbv_cost + ads_sd_cost + ads_cost_alloc +
                    #  ads_amazon_live_cost_alloc + ads_creator_connections_cost_alloc +
                    #  ads_sponsored_tv_cost_alloc + ads_retail_ad_service_alloc)
                    "ads_cost": -27743.22,
                    # 支出 - 广告总销售金额 [原字段 'totalAdsSales']
                    "ads_sales": 142803.87,
                    # 支出 - 广告总销售数量 [原字段 'totalAdsSalesQuantity']
                    "ads_sales_qty": 3333,
                    # 支出 - SP广告花费 (Sponsored Products) [原字段 'adsSpCost']
                    "ads_sp_cost": -22291.36,
                    # 支出 - SP广告销售金额 [原字段 'adsSpSales']
                    "ads_sp_sales": 97531.25,
                    # 支出 - SP广告销售数量 [原字段 'adsSpSalesQuantity']
                    "ads_sp_sales_qty": 2305,
                    # 支出 - SB广告花费 (Sponsored Brands) [原字段 'adsSbCost']
                    "ads_sb_cost": -5451.86,
                    # 支出 - SB广告销售金额 [原字段 'sharedAdsSbSales']
                    "ads_sb_sales": 25464.72,
                    # 支出 - SB广告销售数量 [原字段 'sharedAdsSbSalesQuantity']
                    "ads_sb_sales_qty": 552,
                    # 支出 - SBV广告花费 (Sponsored Brands Video) [原字段 'adsSbvCost']
                    "ads_sbv_cost": 0.0,
                    # 支出 - SBV广告销售金额 [原字段 'sharedAdsSbvSales']
                    "ads_sbv_sales": 19807.9,
                    # 支出 - SBV广告销售数量 [原字段 'sharedAdsSbvSalesQuantity']
                    "ads_sbv_sales_qty": 476,
                    # 支出 - SD广告花费 (Sponsored Display) [原字段 'adsSdCost']
                    "ads_sd_cost": 0.0,
                    # 支出 - SD广告销售金额 [原字段 'adsSdSales']
                    "ads_sd_sales": 0.0,
                    # 支出 - SD广告销售数量 [原字段 'adsSdSalesQuantity']
                    "ads_sd_sales_qty": 0,
                    # 支出 - 广告分摊费用 [原字段 'sharedCostOfAdvertising']
                    "ads_cost_alloc": 0.0,
                    # 支出 - Live广告花费 (分摊) [原字段 'sharedAdsAlCost']
                    "ads_amazon_live_cost_alloc": 0.0,
                    # 支出 - 内容创作者计划花费 (分摊) [原字段 'sharedAdsCcCost']
                    "ads_creator_connections_cost_alloc": 0.0,
                    # 支出 - TV广告花费 (分摊) [原字段 'sharedAdsSspaotCost']
                    "ads_sponsored_tv_cost_alloc": 0.0,
                    # 支出 - 零售商赞助广告花费 (分摊) [原字段 'sharedAdsSarCost']
                    "ads_retail_ad_service_alloc": 0.0,
                    # 支出 - 广告总退款金额 (Refund for Advertiser) [原字段 'refundForAdvertiser']
                    "ads_cost_refunds": 0.0,
                    # 支出 - 清算服务费 (分摊) [原字段 'sharedLiquidationsFees']
                    "liquidation_service_fees_alloc": 0.0,
                    # 支出 - 应收账款扣减 (分摊) [原字段 'sharedReceivablesDeductions']
                    "receivables_deductions_alloc": 0.0,
                    # 支出 - 亚马逊运费调整 (分摊) [原字段 'sharedAmazonShippingChargeAdjustments']
                    "amazon_shipping_charge_adj_alloc": 0.0,
                    # 支出 - VAT销项税费金额 [原字段 'sharedComminglingVatExpenses']
                    "commingling_vat_expenses": 0.0,
                    # 支出 - 其他支出费用 [原字段 'others']
                    "other_expenses": 0.0,
                    # 支出 - 用户自定义推广总费用 [原字段 'customOrderFee']
                    "user_promotion_fees": 0.0,
                    # (user_promotion_principal + user_promotion_commission)
                    # 支出 - 用户自定义推广费用本金 [原字段 'customOrderFeePrincipal']
                    "user_promotion_principal": 0.0,
                    # 支出 - 用户自定义推广佣金费用 [原字段 'customOrderFeeCommission']
                    "user_promotion_commission": 0.0,
                    # 支出 - 用户自定义其他费用 [原字段 'otherFeeStr']
                    "user_other_fees": [],
                    # 税费 - 总税费 [grossProfitTax]
                    "total_tax": 0.0,
                    # 税费 - 总销税收金额 [原字段 'totalSalesTax']
                    # ('product_tax_collected' 到 'tcs_cgst_collected' 之间的所有税费)
                    "sales_tax_collected": 15036.42,
                    # 税费 - 商品销售税收金额 [原字段 'taxCollectedProduct']
                    "product_tax_collected": 15006.18,
                    # 税费 - 配送运费税收金额 [原字段 'taxCollectedShipping']
                    "shipping_tax_collected": 18.58,
                    # 税费 - 礼品包装税收金额 [原字段 'taxCollectedGiftWrap']
                    "giftwrap_tax_collected": 0.0,
                    # 税费 - 促销折扣税收金额 [原字段 'taxCollectedDiscount']
                    "promotional_rebate_tax_collected": 0.0,
                    # 税费 - VAT/GST税收金额 [原字段 'taxCollected']
                    "vat_gst_tax_collected": 11.66,
                    # 税费 - TCS IGST税收金额 (印度站) [原字段 'tcsIgstCollected']
                    "tcs_igst_collected": 0.0,
                    # 税费 - TCS SGST税收金额 (印度站) [原字段 'tcsSgstCollected']
                    "tcs_sgst_collected": 0.0,
                    # 税费 - TCS CGST税收金额 (印度站) [原字段 'tcsCgstCollected']
                    "tcs_cgst_collected": 0.0,
                    # 税费 - 总销售税代扣金额 [原字段 'salesTaxWithheld']
                    "sales_tax_withheld": -15036.42,
                    # 税费 - 总销售税费退款 [salesTaxRefund]
                    # ('product_tax_refunded' 到 'tcs_cgst_refunded' 之间的所有税费退款)
                    "sales_tax_refunded": -784.31,
                    # 税费 - 商品销售税费退款金额 [原字段 'taxRefundedProduct']
                    "product_tax_refunded": -783.0,
                    # 税费 - 配送运费税费退款金额 [原字段 'taxRefundedShipping']
                    "shipping_tax_refunded": -1.31,
                    # 税费 - 礼品包装税费退款金额 [原字段 'taxRefundedGiftWrap']
                    "giftwrap_tax_refunded": 0.0,
                    # 税费 - 促销折扣税费退款金额 [原字段 'taxRefundedDiscount']
                    "promotional_rebate_tax_refunded": 0.0,
                    # 税费 - VAT/GST税费退款金额 [原字段 'taxRefunded']
                    "vat_gst_tax_refunded": 0.0,
                    # 税费 - TCS IGST税费退款金额 (印度站) [原字段 'tcsIgstRefunded']
                    "tcs_igst_refunded": 0.0,
                    # 税费 - TCS SGST税费退款金额 (印度站) [原字段 'tcsSgstRefunded']
                    "tcs_sgst_refunded": 0.0,
                    # 税费 - TCS CGST税费退款金额 (印度站) [原字段 'tcsCgstRefunded']
                    "tcs_cgst_refunded": 0.0,
                    # 税费 - 总退款税代扣金额 [原字段 'refundTaxWithheld']
                    "refund_tax_withheld": 784.31,
                    # 税费 - 其他税费调整 (分摊) [原字段 'sharedTaxAdjustment']
                    "other_tax_adj_alloc": 0.0,
                    # 成本 - 总退款数量 [原字段 'refundsQuantity']
                    "total_refunds_qty": 329,
                    # 成本 - 总退款率 [原字段 'refundsRate']
                    # (total_refund_qty / (fba&fbm_product_sales_qty + fba_mcf_fulfillment_qty + fba_reshipment_qty))
                    "total_refunds_rate": 0.0486,
                    # 成本 - FBA退货数量 [原字段 'fbaReturnsQuantity']
                    "fba_returns_qty": 363,
                    # 成本 - FBA退货可售数量 [原字段 'fbaReturnsSaleableQuantity']
                    "fba_returns_saleable_qty": 12,
                    # 成本 - FBA退货不可售数量 [原字段 'fbaReturnsUnsaleableQuantity']
                    "fba_returns_unsaleable_qty": 351,
                    # 成本 - FBA退货率 [原字段 'fbaReturnsQuantityRate']
                    # (fba_returns_qty / (fba_product_sales_qty + fba_mcf_fulfillment_qty))
                    "fba_returns_rate": 0.054,
                    # 成本 - 总补发/换货数量 [原字段 'totalReshipQuantity']
                    "total_reshipment_qty": 50,
                    # 成本 - FBA补发/换货数量 [原字段 'reshipFbaProductSalesQuantity']
                    "fba_reshipment_qty": 47,
                    # 成本 - FBA换货退回数量 [原字段 'reshipFbaProductSaleRefundsQuantity']
                    "fba_reshipment_returned_qty": 3,
                    # 成本 - FBM补发/换货数量 [原字段 'reshipFbmProductSalesQuantity']
                    "fbm_reshipment_qty": 0,
                    # 成本 - FBM换货退回数量 [原字段 'reshipFbmProductSaleRefundsQuantity']
                    "fbm_reshipment_returned_qty": 0,
                    # 成本 - 总成本数量 [原字段 'cgQuantity']
                    # (fba&fbm_product_sales_qty + fba_mcf_fulfillment_qty + fba&fbm_reshipment_qty - fba_returns_saleable_qty)
                    "cost_of_goods_qty": -6757,
                    # 成本 - 重成本数量绝对值 [原字段 'cgAbsQuantity']
                    "cost_of_goods_abs_qty": 6780,
                    # 成本 - 总成本金额 (COGS) [原字段 'totalCost']
                    # (purchase_cost + logistics_cost + other_costs)
                    "cost_of_goods": -100790.7,
                    # 成本 - 总成本占比 [原字段 'proportionOfTotalCost']
                    "cost_of_goods_ratio": 0.4272,
                    # 成本 - 总采购成本 (COGS) [原字段 'cgPriceTotal']
                    "purchase_cost": -100790.7,
                    # 成本 - 总采购绝对成本 [原字段 'cgPriceAbsTotal']
                    "purchase_abs_cost": 100890.7,
                    # 成本 - 单品成本 [原字段 'cgUnitPrice']
                    "purchase_unit_cost": 14.93,
                    # 成本 - 采购成本占比 [原字段 'proportionOfCg']
                    "purchase_cost_ratio": 0.4272,
                    # 成本 - 是否有成本明细 [原字段 'hasCgPriceDetail']
                    "has_purchase_cost_detail": 1,
                    # 成本 - 总物流费用 [原字段 'cgTransportCostsTotal']
                    "logistics_cost": 0.0,
                    # 成本 - 物流单品费用 [原字段 'cgTransportUnitCosts']
                    "logistics_unit_cost": 0.0,
                    # 成本 - 物流费用占比 [原字段 'proportionOfCgTransport']
                    "logistics_cost_ratio": 0.0,
                    # 成本 - 是否有物流费用明细 [原字段 'hasCgTransportCostsDetail']
                    "has_logistics_cost_detail": 1,
                    # 成本 - 其他费用总金额 [原字段 'cgOtherCostsTotal']
                    "other_costs": 0.0,
                    # 成本 - 其他费用单品金额 [原字段 'cgOtherUnitCosts']
                    "other_unit_cost": 0.0,
                    # 成本 - 其他费用占比 [原字段 'proportionOfCgOtherCosts']
                    "other_cost_ratio": 0.0,
                    # 成本 - 是否有其他费用明细 [原字段 'hasCgOtherCostsDetail']
                    "has_other_cost_detail": 0,
                    # 利润 - 毛利润 [原字段 'grossProfit']
                    "gross_profit": 47219.53,
                    # 利润 - 毛利率 [原字段 'grossRate']
                    "gross_profit_margin": 0.2131,
                    # 利润 - 投资回报率 (ROI)
                    "roi": 0.2693,
                    # 交易状态 [原字段 'transactionStatusCode']
                    "transaction_status": "Disbursed",
                    # 交易状态描述 [原字段 'transactionStatus']
                    "transaction_status_desc": "已发放",
                    # 延迟结算状态 [原字段 'deferredSubStatusCode']
                    "deferred_settlement_status": "Disbursed",
                    # 延迟结算状态描述 [原字段 'deferredSubStatus']
                    "deferred_settlement_status_desc": "",
                    # 延迟结算总金额 [原字段 'deferredSettlementAmount']
                    "deferred_settlement": 186019.17,
                    # 结算小计 [原字段 'settlementSubtotal']
                    "settlement_subtotal": 186019.17,
                    # 报告时间 (本地时间) [原字段 'postedDateDayLocale']
                    "report_time_loc": "",
                    # 报告开始时间 (本地时间) [原字段 'minPostedDateDayLocale']
                    "report_start_time_loc": "",
                    # 报告结束时间 (本地时间) [原字段 'maxPostedDateDayLocale']
                    "report_end_time_loc": "",
                    # 报告日期 (本地时间) [原字段 'postedDateLocale']
                    "report_date_loc": "2025-08",
                    # 记录ID (非业务唯一键)
                    "id": "65545075457********",
                    # 领星店铺ID
                    "sid": 1,
                    # 国家代码 [原字段 'countryCode']
                    "country_code": "US",
                    # ASIN关联领星店铺ID列表
                    "sids": [1],
                    # ASIN关联领星店铺名称列表 [原字段 'storeName']
                    "seller_names": ["Store-US"],
                    # ASIN关联国家列表 (中文) [原字段 'country']
                    "countries": ["美国"],
                    # 商品ASIN
                    "asin": "B07*******",
                    # 商品父ASIN [原字段 'parentAsin']
                    "parent_asin": "B07*******",
                    # 领星本地SKU [原字段 'localSku']
                    "lsku": "LOCAL********",
                    # 领星本地商品名称 [原字段 'localName']
                    "product_name": "JBL",
                    # 产品型号 [原字段 'model']
                    "product_model": "KX6702",
                    # 领星本地产品分类名称 [原字段 'categoryName']
                    "category_name": "",
                    # 领星本地产品品牌名称 [原字段 'brandName']
                    "brand_name": "",
                    # 标题 [原字段 'itemName']
                    "title": "Product Title",
                    # 商品略缩图链接 [原字段 'smallImageUrl']
                    "thumbnail_url": "https://m.media-amazon.com/images/****.jpg",
                    # ASIN开发人名称 [原字段 'productDeveloperRealname']
                    "developer_name": "",
                    # ASIN负责人名称 (逗号隔开) [原字段 'principalRealname']
                    "operator_names": "白小白,黑小黑",
                    # 商品标签IDs (逗号隔开) [原字段 'listingTagIds']
                    "tag_ids": "907476839534375430, 907476656619287314, 907476656619287354",
                },
                ...
            ]
        }
        ```
        """
        url = route.INCOME_STATEMENT_ASINS
        # 构建参数
        args = {
            "start_date": start_date,
            "end_date": end_date,
            "mids": mids,
            "sids": sids,
            "query_dimension": query_dimension,
            "transaction_status": transaction_status,
            "summarize": summarize,
            "currency_code": currency_code,
            "search_field": None if search_value is None else "asin",
            "search_value": search_value,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.IncomeStatement.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.IncomeStatementAsins.model_validate(data)

    async def IncomeStatementParentAsins(
        self,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        *,
        query_dimension: int | None = None,
        mids: int | list[int] | None = None,
        sids: int | list[int] | None = None,
        transaction_status: INCOME_STATEMENT_TRANSACTION_STATUS | None = None,
        summarize: int | None = None,
        currency_code: str | None = None,
        search_value: str | list[str] | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.IncomeStatementAsins:
        """查询损益报告-父ASIN维度

        ## Docs
        - 财务: [查询利润报表-父ASIN](https://apidoc.lingxing.com/#/docs/Finance/bdParentASIN)

        :param start_date `<'str/date/datetime'>`: 统计开始日期, 闭合区间
        :param end_date `<'str/date/datetime'>`: 统计结束日期, 闭合区间
        :param query_dimension `<'int/None'>`: 查询维度, 默认 `None` (使用: 0), 可选值:

            - `0`: 天维度, 开始和结束时间跨度不能超过31天
            - `1`: 月维度, 开始和结束时间跨度不能超过1个月

        :param mids `<'int/list[int]/None'>`: 领星站点ID或ID列表 (Seller.mid), 默认 `None` (不筛选)
        :param sids `<'int/list[int]/None'>`: 领星店铺ID或ID列表 (Seller.sid), 默认 `None` (不筛选)
        :param transaction_status `<'int/None'>`: 交易状态, 默认 `None` (使用: 'Disbursed'), 可选值:

            - `'Deferred'`: 订单未进入Transaction报告, 无法回款
            - `'Disbursed'`: 订单已进入Transaction报告, 可以回款
            - `'DisbursedAndSettled'`: 可以回款和预结算订单
            - `'All'`: 所有状态

        :param summarize `<'int/None'>`: 是否返回汇总数据, 默认 `None` (使用: 0), 可选值:

            - `0`: 返回原始数据
            - `1`: 返回汇总数据

        :param currency_code `<'str/None'>`: 结算金额目标转换货币代码, 默认 `None` (保持原结算货币)
        :param search_value `<'str/list[str]/None'>`: 搜索值, 默认 `None` (不筛选), 可传入单个父ASIN或父ASIN列表
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值 10000, 默认 `None` (使用: 15)
        :return `<'IncomeStatementAsins'>`: 查询到的损益报告-父ASIN维度结果
        """
        url = route.INCOME_STATEMENT_PARENT_ASINS
        # 构建参数
        args = {
            "start_date": start_date,
            "end_date": end_date,
            "mids": mids,
            "sids": sids,
            "query_dimension": query_dimension,
            "transaction_status": transaction_status,
            "summarize": summarize,
            "currency_code": currency_code,
            "search_field": None if search_value is None else "parent_asin",
            "search_value": search_value,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.IncomeStatement.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.IncomeStatementAsins.model_validate(data)

    async def IncomeStatementMskus(
        self,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        *,
        query_dimension: int | None = None,
        mids: int | list[int] | None = None,
        sids: int | list[int] | None = None,
        transaction_status: INCOME_STATEMENT_TRANSACTION_STATUS | None = None,
        summarize: int | None = None,
        currency_code: str | None = None,
        search_value: str | list[str] | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.IncomeStatementMskus:
        """查询损益报告-亚马逊SKU维度

        ## Docs
        - 财务: [查询利润报表-MSKU](https://apidoc.lingxing.com/#/docs/Finance/bdMSKU)

        :param start_date `<'str/date/datetime'>`: 统计开始日期, 闭合区间
        :param end_date `<'str/date/datetime'>`: 统计结束日期, 闭合区间
        :param query_dimension `<'int/None'>`: 查询维度, 默认 `None` (使用: 0), 可选值:

            - `0`: 天维度, 开始和结束时间跨度不能超过31天
            - `1`: 月维度, 开始和结束时间跨度不能超过1个月

        :param mids `<'int/list[int]/None'>`: 领星站点ID或ID列表 (Seller.mid), 默认 `None` (不筛选)
        :param sids `<'int/list[int]/None'>`: 领星店铺ID或ID列表 (Seller.sid), 默认 `None` (不筛选)
        :param transaction_status `<'int/None'>`: 交易状态, 默认 `None` (使用: 'Disbursed'), 可选值:

            - `'Deferred'`: 订单未进入Transaction报告, 无法回款
            - `'Disbursed'`: 订单已进入Transaction报告, 可以回款
            - `'DisbursedAndSettled'`: 可以回款和预结算订单
            - `'All'`: 所有状态

        :param summarize `<'int/None'>`: 是否返回汇总数据, 默认 `None` (使用: 0), 可选值:

            - `0`: 返回原始数据
            - `1`: 返回汇总数据

        :param currency_code `<'str/None'>`: 结算金额目标转换货币代码, 默认 `None` (保持原结算货币)
        :param search_value `<'str/list[str]/None'>`: 搜索值, 默认 `None` (不筛选), 可传入单个亚马逊SKU或SKU列表
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值 10000, 默认 `None` (使用: 15)
        :returns `<'IncomeStatementMskus'>`: 查询到的损益报告-亚马逊SKU维度结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 币种代码 [原字段 'currencyCode']
                    "currency_code": "USD",
                    # 币种图标 [原字段 'currencyIcon']
                    "currency_icon": "$",
                    # 收入 - 总收入金额 [原字段 'grossProfitIncome']
                    "total_income": 221568.35,
                    # 收入 - 总销售金额 [原字段 'totalSalesAmount']
                    "product_sales": 235906.05,
                    # 收入 - 总销售数量 [原字段 'totalSalesQuantity']
                    "product_sales_qty": 6715,
                    # 收入 - 总销售退费 [原字段 'totalSalesRefunds']
                    "product_sales_refunds": -11807.03,
                    # 收入 - FBA销售金额 [原字段 'fbaSaleAmount']
                    "fba_product_sales": 235906.05,
                    # 收入 - FBA销售数量 [原字段 'fbaSalesQuantity']
                    "fba_product_sales_qty": 6715,
                    # 收入 - FBA销售退费 [原字段 'fbaSalesRefunds']
                    "fba_product_sales_refunds": -11807.03,
                    # 收入 - FBM销售金额 [原字段 'fbmSaleAmount']
                    "fbm_product_sales": 0.0,
                    # 收入 - FBM销售数量 [原字段 'fbmSalesQuantity']
                    "fbm_product_sales_qty": 0,
                    # 收入 - FBM销售退费 [原字段 'fbmSalesRefunds']
                    "fbm_product_sales_refunds": 0.0,
                    # 收入 - FBA库存赔付/补偿金额 [原字段 'fbaInventoryCredit']
                    "fba_inventory_credits": 3483.66,
                    # 收入 - FBA库存赔付/补偿数量 [原字段 'fbaInventoryCreditQuantity']
                    "fba_inventory_credit_qty": 169,
                    # 收入 - FBA清算收益金额 [原字段 'fbaLiquidationProceeds']
                    "fba_liquidation_proceeds": 0.0,
                    # 收入 - FBA清算收益调整金额 [原字段 'fbaLiquidationProceedsAdjustments']
                    "fba_liquidation_proceeds_adj": 0.0,
                    # 收入 - 配送运费收入金额 (买家支出) [原字段 'shippingCredits']
                    "shipping_credits": 6595.82,
                    # 收入 - 配送运费退款金额 (买家收入) [原字段 'shippingCreditRefunds']
                    "shipping_credit_refunds": -354.16,
                    # 收入 - 礼品包装费收入金额 (买家支出) [原字段 'giftWrapCredits']
                    "giftwrap_credits": 0.0,
                    # 收入 - 礼品包装费退款金额 (买家收入) [原字段 'giftWrapCreditRefunds']
                    "giftwrap_credit_refunds": 0.0,
                    # 收入 - 促销折扣金额 (卖家支出) [原字段 'promotionalRebates']
                    "promotional_rebates": -12777.02,
                    # 收入 - 促销折扣退款金额 (卖家收入) [原字段 'promotionalRebateRefunds']
                    "promotional_rebate_refunds": 521.03,
                    # 收入 - A-to-Z 保障/索赔金额 [原字段 'guaranteeClaims']
                    "a2z_guarantee_claims": 0.0,
                    # 收入 - 拒付金额 (拒付造成的让利（发生时为负数）) [原字段 'chargebacks']
                    "chargebacks": 0.0,
                    # 收入 - 亚马逊运费补偿金额 [原字段 'amazonShippingReimbursement']
                    "amazon_shipping_reimbursement": 0.0,
                    # 收入 - 亚马逊安全运输计划补偿金额 [原字段 'safeTReimbursement']
                    "safe_t_reimbursement": 0.0,
                    # 收入 - 其他补偿/赔付金额 [原字段 'reimbursements']
                    "other_reimbursement": 0.0,
                    # 收入 - 积分发放金额 (日本站) [原字段 'costOfPoIntegersGranted']
                    "points_granted": 0.0,
                    # 收入 - 积分退还金额 (日本站) [原字段 'costOfPoIntegersReturned']
                    "points_returned": 0.0,
                    # 收入 - 积分调整金额 (日本站) [原字段 'pointsAdjusted']
                    "points_adjusted": 0.0,
                    # 收入 - 货到付款金额 (COD) [原字段 'cashOnDelivery']
                    "cash_on_delivery": 0.0,
                    # 收入 - VAT进项税费金额 [原字段 'sharedComminglingVatIncome']
                    "commingling_vat_income": 0.0,
                    # 收入 - NetCo混合网络交易金额 [原字段 'netcoTransaction']
                    "netco_transaction": 0.0,
                    # 收入 - TDS 194-O净额 (印度站) [原字段 'tdsSection194ONet']
                    "tds_section_194o_net": 0.0,
                    # 收入 - 收回/冲回金额
                    "clawbacks": 0.0,
                    # 收入 - 其他收入金额 [原字段 'otherInAmount']
                    "other_income": 0.0,
                    # 支出 - FBA销售佣金 (Referral Fee) [原字段 'platformFee']
                    "fba_selling_fees": -19936.57,
                    # 支出 - FBA销售佣金退款金额 [原字段 'sellingFeeRefunds']
                    "fba_selling_fee_refunds": 1095.17,
                    # 支出 - FBA交易费用 [原字段 'totalFbaDeliveryFee']
                    # (fba_fulfillment_fees 到 fba_transaction_return_fees_alloc 之间所有费用)
                    "fba_transaction_fees": -23814.6,
                    # 支付 - FBA配送费用 (Fulfillment Fee) [原字段 'fbaDeliveryFee']
                    "fba_fulfillment_fees": -23769.11,
                    # 支出 - FBA多渠道配送费用 (Multi-Channel) [原字段 'mcFbaDeliveryFee']
                    "fba_mcf_fulfillment_fees": -45.49,
                    # 支出 - FBA多渠道配送费用 (分摊) [原字段 'sharedMcFbaFulfillmentFees']
                    "fba_mcf_fulfillment_fees_alloc": 0.0,
                    # 支出 - FBA多渠道配送数量 (Multi-Channel) [原字段 'mcFbaFulfillmentFeesQuantity']
                    "fba_mcf_fulfillment_qty": 7,
                    # 支出 - FBA客户退货处理费用 (分摊) [原字段 'sharedFbaCustomerReturnFee']
                    "fba_customer_return_fees_alloc": 0.0,
                    # 支出 - FBA交易退货处理费用 (分摊) [原字段 'sharedFbaTransactionCustomerReturnFee']
                    "fba_transaction_return_fees_alloc": 0.0,
                    # 支出 - FBA总配送费用退款金额 [原字段 'fbaTransactionFeeRefunds']
                    "fba_transaction_fee_refunds": 120.94,
                    # 支出 - 其他交易费用 [原字段 'otherTransactionFees']
                    "other_transaction_fees": 0.0,
                    # 支出 - 其他交易费用退款金额 [原字段 'otherTransactionFeeRefunds']
                    "other_transaction_fee_refunds": 0.0,
                    # 支出 - FBA仓储和入库服务总费用 [原字段 'totalStorageFee']
                    # ('fba_storage_fees' 到 'other_fba_inventory_fees_alloc' 之间的所有费用)
                    "fba_inventory_and_inbound_services_fees": -484.25,
                    # 支出 - FBA仓储费用 [原字段 'fbaStorageFee']
                    "fba_storage_fees": -151.64,
                    # 支出 - FBA仓储费用计提金额 [原字段 'fbaStorageFeeAccrual']
                    "fba_storage_fees_accr": 0.0,
                    # 支出 - FBA仓储费用计提调整金额 [原字段 'fbaStorageFeeAccrualDifference']
                    "fba_storage_fees_accr_adj": 0.0,
                    # 支出 - FBA仓储费用 (分摊) [原字段 'sharedFbaStorageFee']
                    "fba_storage_fees_alloc": 0.01,
                    # 支出 - FBA长期仓储费用 [原字段 'longTermStorageFee']
                    "fba_lt_storage_fees": 0.0,
                    # 支出 - FBA长期仓储费用计提金额 [原字段 'longTermStorageFeeAccrual']
                    "fba_lt_storage_fees_accr": 0.0,
                    # 支出 - FBA长期仓储费用计提调整金额 [原字段 'longTermStorageFeeAccrualDifference']
                    "fba_lt_storage_fees_accr_adj": 0.0,
                    # 支出 - FBA长期仓储费用 (分摊) [原字段 'sharedLongTermStorageFee']
                    "fba_lt_storage_fees_alloc": 0.0,
                    # 支出 - FBA仓储超储费用 (分摊) [原字段 'sharedFbaOverageFee']
                    "fba_overage_fees_alloc": 0.0,
                    # 支出 - FBA仓储续期费用 (分摊) [原字段 'sharedStorageRenewalBilling']
                    "fba_storage_renewal_fees_alloc": 0.0,
                    # 支出 - FBA仓鼠销毁费用 (分摊) [原字段 'sharedFbaDisposalFee']
                    "fba_disposal_fees_alloc": -2.08,
                    # 支出 - FBA仓储销毁数量 [原字段 'disposalQuantity']
                    "fba_disposal_qty": 0,
                    # 支出 - FBA仓储移除费用 (分摊) [原字段 'sharedFbaRemovalFee']
                    "fba_removal_fees_alloc": -330.54,
                    # 支出 - FBA仓储移除数量 [原字段 'removalQuantity']
                    "fba_removal_qty": 315,
                    # 支出 - FBA入库运输计划费用 (分摊) [原字段 'sharedFbaInboundTransportationProgramFee']
                    "fba_inbound_transportation_program_fees_alloc": 0.0,
                    # 支出 - FBA入库缺陷费用 (分摊) [原字段 'sharedFbaInboundDefectFee']
                    "fba_inbound_defect_fees_alloc": 0.0,
                    # 支出 - FBA国际入库费用 (分摊) [原字段 'sharedFbaIntegerernationalInboundFee']
                    "fba_international_inbound_fees_alloc": 0.0,
                    # 支出 - FBA合作承运商(入库)运费 (分摊) [原字段 'sharedAmazonPartneredCarrierShipmentFee']
                    "fba_partnered_carrier_shipment_fees_alloc": 0.0,
                    # 支出 - FBA人工处理费用 (分摊) [原字段 'sharedManualProcessingFee']
                    "fba_manual_processing_fees_alloc": 0.0,
                    # 支出 - AWD仓储费用 (分摊) [原字段 'sharedAwdStorageFee']
                    "awd_storage_fees_alloc": 0.0,
                    # 支出 - AWD处理费用 (分摊) [原字段 'sharedAwdProcessingFee']
                    "awd_processing_fees_alloc": 0.0,
                    # 支出 - AWD运输费用 (分摊) [原字段 'sharedAwdTransportationFee']
                    "awd_transportation_fees_alloc": 0.0,
                    # 支出 - AWD卫星仓储费用 (分摊) [原字段 'sharedStarStorageFee']
                    "awd_satellite_storage_fees_alloc": 0.0,
                    # 支出 - FBA库存费用调整金额 (分摊) [原字段 'sharedItemFeeAdjustment']
                    "fba_inventory_fees_adj_alloc": 0.0,
                    # 支出 - FBA其他库存费用 (分摊) [原字段 'sharedOtherFbaInventoryFees']
                    "other_fba_inventory_fees_alloc": 0.0,
                    # 支出 - 运输标签花费金额 [原字段 'shippingLabelPurchases']
                    "shipping_label_purchases": 0.0,
                    # 支出 - FBA贴标费用 (分摊) [原字段 'sharedLabelingFee']
                    "fba_labeling_fees_alloc": 0.0,
                    # 支出 - FBA塑封袋费用 (分摊) [原字段 'sharedPolybaggingFee']
                    "fba_polybagging_fees_alloc": 0.0,
                    # 支出 - FBA气泡膜费用 (分摊) [原字段 'sharedBubblewrapFee']
                    "fba_bubblewrap_fees_alloc": 0.0,
                    # 支出 - FBA封箱胶带费用 (分摊) [原字段 'sharedTapingFee']
                    "fba_taping_fees_alloc": 0.0,
                    # 支出 - FBM邮寄资费 (分摊) [原字段 'sharedMfnPostageFee']
                    "mfn_postage_fees_alloc": 0.0,
                    # 支出 - 运输标签退款金额 [原字段 'shippingLabelRefunds']
                    "shipping_label_refunds": 0.0,
                    # 支出 - 承运商运输标签花费调整金额 [原字段 'sharedCarrierShippingLabelAdjustments']
                    "carrier_shipping_label_adj": 0.0,
                    # 支出 - 总推广费用 (Service Fee) [原字段 'promotionFee']
                    # (subscription_fees_alloc 到 early_reviewer_program_fees_alloc 之间的所有费用)
                    "promotion_fees": -679.97,
                    # 支出 - 订阅服务费 (分摊) [原字段 'sharedSubscriptionFee']
                    "subscription_fees_alloc": -39.99,
                    # 支出 - 优惠券费用 (分摊) [原字段 'sharedCouponFee']
                    "coupon_fees_alloc": -239.98,
                    # 支出 - 秒杀费用 (分摊) [原字段 'sharedLdFee']
                    "deal_fees_alloc": 0.0,
                    # 支出 - Vine费用 (分摊) [原字段 'sharedVineFee']
                    "vine_fees_alloc": -400.0,
                    # 支出 - 早期评论人计划费用 (分摊) [原字段 'sharedEarlyReviewerProgramFee']
                    "early_reviewer_program_fees_alloc": 0.0,
                    # 支出 - FBA入库便利费用 (Service Fee/分摊) [原字段 'sharedFbaInboundConvenienceFee']
                    "fba_inbound_convenience_fees_alloc": 0.0,
                    # 支出 - 其他亚马逊服务费用 (分摊) [原字段 'totalPlatformOtherFee']
                    "other_service_fees_alloc": -1733.33,
                    # 支出 - 亚马逊退款管理费用 [原字段 'refundAdministrationFees']
                    "refund_administration_fees": -219.15,
                    # 支出 - 总费用退款金额 [totalFeeRefunds]
                    # (fba_selling_fee_refunds + fba_transaction_fee_refunds + refund_administration_fees)
                    "total_fee_refunds": 996.96,
                    # 支出 - 其他费用调整金额
                    "adjustments": -163.14,
                    # 支出 - 广告总花费 (Cost of Advertising) [原字段 'totalAdsCost']
                    # (ads_sp_cost + ads_sb_cost + ads_sbv_cost + ads_sd_cost + ads_cost_alloc +
                    #  ads_amazon_live_cost_alloc + ads_creator_connections_cost_alloc +
                    #  ads_sponsored_tv_cost_alloc + ads_retail_ad_service_alloc)
                    "ads_cost": -27743.22,
                    # 支出 - 广告总销售金额 [原字段 'totalAdsSales']
                    "ads_sales": 142803.87,
                    # 支出 - 广告总销售数量 [原字段 'totalAdsSalesQuantity']
                    "ads_sales_qty": 3333,
                    # 支出 - SP广告花费 (Sponsored Products) [原字段 'adsSpCost']
                    "ads_sp_cost": -22291.36,
                    # 支出 - SP广告销售金额 [原字段 'adsSpSales']
                    "ads_sp_sales": 97531.25,
                    # 支出 - SP广告销售数量 [原字段 'adsSpSalesQuantity']
                    "ads_sp_sales_qty": 2305,
                    # 支出 - SB广告花费 (Sponsored Brands) [原字段 'adsSbCost']
                    "ads_sb_cost": -5451.86,
                    # 支出 - SB广告销售金额 [原字段 'sharedAdsSbSales']
                    "ads_sb_sales": 25464.72,
                    # 支出 - SB广告销售数量 [原字段 'sharedAdsSbSalesQuantity']
                    "ads_sb_sales_qty": 552,
                    # 支出 - SBV广告花费 (Sponsored Brands Video) [原字段 'adsSbvCost']
                    "ads_sbv_cost": 0.0,
                    # 支出 - SBV广告销售金额 [原字段 'sharedAdsSbvSales']
                    "ads_sbv_sales": 19807.9,
                    # 支出 - SBV广告销售数量 [原字段 'sharedAdsSbvSalesQuantity']
                    "ads_sbv_sales_qty": 476,
                    # 支出 - SD广告花费 (Sponsored Display) [原字段 'adsSdCost']
                    "ads_sd_cost": 0.0,
                    # 支出 - SD广告销售金额 [原字段 'adsSdSales']
                    "ads_sd_sales": 0.0,
                    # 支出 - SD广告销售数量 [原字段 'adsSdSalesQuantity']
                    "ads_sd_sales_qty": 0,
                    # 支出 - 广告分摊费用 [原字段 'sharedCostOfAdvertising']
                    "ads_cost_alloc": 0.0,
                    # 支出 - Live广告花费 (分摊) [原字段 'sharedAdsAlCost']
                    "ads_amazon_live_cost_alloc": 0.0,
                    # 支出 - 内容创作者计划花费 (分摊) [原字段 'sharedAdsCcCost']
                    "ads_creator_connections_cost_alloc": 0.0,
                    # 支出 - TV广告花费 (分摊) [原字段 'sharedAdsSspaotCost']
                    "ads_sponsored_tv_cost_alloc": 0.0,
                    # 支出 - 零售商赞助广告花费 (分摊) [原字段 'sharedAdsSarCost']
                    "ads_retail_ad_service_alloc": 0.0,
                    # 支出 - 广告总退款金额 (Refund for Advertiser) [原字段 'refundForAdvertiser']
                    "ads_cost_refunds": 0.0,
                    # 支出 - 清算服务费 (分摊) [原字段 'sharedLiquidationsFees']
                    "liquidation_service_fees_alloc": 0.0,
                    # 支出 - 应收账款扣减 (分摊) [原字段 'sharedReceivablesDeductions']
                    "receivables_deductions_alloc": 0.0,
                    # 支出 - 亚马逊运费调整 (分摊) [原字段 'sharedAmazonShippingChargeAdjustments']
                    "amazon_shipping_charge_adj_alloc": 0.0,
                    # 支出 - VAT销项税费金额 [原字段 'sharedComminglingVatExpenses']
                    "commingling_vat_expenses": 0.0,
                    # 支出 - 其他支出费用 [原字段 'others']
                    "other_expenses": 0.0,
                    # 支出 - 用户自定义推广总费用 [原字段 'customOrderFee']
                    "user_promotion_fees": 0.0,
                    # (user_promotion_principal + user_promotion_commission)
                    # 支出 - 用户自定义推广费用本金 [原字段 'customOrderFeePrincipal']
                    "user_promotion_principal": 0.0,
                    # 支出 - 用户自定义推广佣金费用 [原字段 'customOrderFeeCommission']
                    "user_promotion_commission": 0.0,
                    # 支出 - 用户自定义其他费用 [原字段 'otherFeeStr']
                    "user_other_fees": [],
                    # 税费 - 总税费 [grossProfitTax]
                    "total_tax": 0.0,
                    # 税费 - 总销税收金额 [原字段 'totalSalesTax']
                    # ('product_tax_collected' 到 'tcs_cgst_collected' 之间的所有税费)
                    "sales_tax_collected": 15036.42,
                    # 税费 - 商品销售税收金额 [原字段 'taxCollectedProduct']
                    "product_tax_collected": 15006.18,
                    # 税费 - 配送运费税收金额 [原字段 'taxCollectedShipping']
                    "shipping_tax_collected": 18.58,
                    # 税费 - 礼品包装税收金额 [原字段 'taxCollectedGiftWrap']
                    "giftwrap_tax_collected": 0.0,
                    # 税费 - 促销折扣税收金额 [原字段 'taxCollectedDiscount']
                    "promotional_rebate_tax_collected": 0.0,
                    # 税费 - VAT/GST税收金额 [原字段 'taxCollected']
                    "vat_gst_tax_collected": 11.66,
                    # 税费 - TCS IGST税收金额 (印度站) [原字段 'tcsIgstCollected']
                    "tcs_igst_collected": 0.0,
                    # 税费 - TCS SGST税收金额 (印度站) [原字段 'tcsSgstCollected']
                    "tcs_sgst_collected": 0.0,
                    # 税费 - TCS CGST税收金额 (印度站) [原字段 'tcsCgstCollected']
                    "tcs_cgst_collected": 0.0,
                    # 税费 - 总销售税代扣金额 [原字段 'salesTaxWithheld']
                    "sales_tax_withheld": -15036.42,
                    # 税费 - 总销售税费退款 [salesTaxRefund]
                    # ('product_tax_refunded' 到 'tcs_cgst_refunded' 之间的所有税费退款)
                    "sales_tax_refunded": -784.31,
                    # 税费 - 商品销售税费退款金额 [原字段 'taxRefundedProduct']
                    "product_tax_refunded": -783.0,
                    # 税费 - 配送运费税费退款金额 [原字段 'taxRefundedShipping']
                    "shipping_tax_refunded": -1.31,
                    # 税费 - 礼品包装税费退款金额 [原字段 'taxRefundedGiftWrap']
                    "giftwrap_tax_refunded": 0.0,
                    # 税费 - 促销折扣税费退款金额 [原字段 'taxRefundedDiscount']
                    "promotional_rebate_tax_refunded": 0.0,
                    # 税费 - VAT/GST税费退款金额 [原字段 'taxRefunded']
                    "vat_gst_tax_refunded": 0.0,
                    # 税费 - TCS IGST税费退款金额 (印度站) [原字段 'tcsIgstRefunded']
                    "tcs_igst_refunded": 0.0,
                    # 税费 - TCS SGST税费退款金额 (印度站) [原字段 'tcsSgstRefunded']
                    "tcs_sgst_refunded": 0.0,
                    # 税费 - TCS CGST税费退款金额 (印度站) [原字段 'tcsCgstRefunded']
                    "tcs_cgst_refunded": 0.0,
                    # 税费 - 总退款税代扣金额 [原字段 'refundTaxWithheld']
                    "refund_tax_withheld": 784.31,
                    # 税费 - 其他税费调整 (分摊) [原字段 'sharedTaxAdjustment']
                    "other_tax_adj_alloc": 0.0,
                    # 成本 - 总退款数量 [原字段 'refundsQuantity']
                    "total_refunds_qty": 329,
                    # 成本 - 总退款率 [原字段 'refundsRate']
                    # (total_refund_qty / (fba&fbm_product_sales_qty + fba_mcf_fulfillment_qty + fba_reshipment_qty))
                    "total_refunds_rate": 0.0486,
                    # 成本 - FBA退货数量 [原字段 'fbaReturnsQuantity']
                    "fba_returns_qty": 363,
                    # 成本 - FBA退货可售数量 [原字段 'fbaReturnsSaleableQuantity']
                    "fba_returns_saleable_qty": 12,
                    # 成本 - FBA退货不可售数量 [原字段 'fbaReturnsUnsaleableQuantity']
                    "fba_returns_unsaleable_qty": 351,
                    # 成本 - FBA退货率 [原字段 'fbaReturnsQuantityRate']
                    # (fba_returns_qty / (fba_product_sales_qty + fba_mcf_fulfillment_qty))
                    "fba_returns_rate": 0.054,
                    # 成本 - 总补发/换货数量 [原字段 'totalReshipQuantity']
                    "total_reshipment_qty": 50,
                    # 成本 - FBA补发/换货数量 [原字段 'reshipFbaProductSalesQuantity']
                    "fba_reshipment_qty": 47,
                    # 成本 - FBA换货退回数量 [原字段 'reshipFbaProductSaleRefundsQuantity']
                    "fba_reshipment_returned_qty": 3,
                    # 成本 - FBM补发/换货数量 [原字段 'reshipFbmProductSalesQuantity']
                    "fbm_reshipment_qty": 0,
                    # 成本 - FBM换货退回数量 [原字段 'reshipFbmProductSaleRefundsQuantity']
                    "fbm_reshipment_returned_qty": 0,
                    # 成本 - 总成本数量 [原字段 'cgQuantity']
                    # (fba&fbm_product_sales_qty + fba_mcf_fulfillment_qty + fba&fbm_reshipment_qty - fba_returns_saleable_qty)
                    "cost_of_goods_qty": -6757,
                    # 成本 - 重成本数量绝对值 [原字段 'cgAbsQuantity']
                    "cost_of_goods_abs_qty": 6780,
                    # 成本 - 总成本金额 (COGS) [原字段 'totalCost']
                    # (purchase_cost + logistics_cost + other_costs)
                    "cost_of_goods": -100790.7,
                    # 成本 - 总成本占比 [原字段 'proportionOfTotalCost']
                    "cost_of_goods_ratio": 0.4272,
                    # 成本 - 总采购成本 (COGS) [原字段 'cgPriceTotal']
                    "purchase_cost": -100790.7,
                    # 成本 - 总采购绝对成本 [原字段 'cgPriceAbsTotal']
                    "purchase_abs_cost": 100890.7,
                    # 成本 - 单品成本 [原字段 'cgUnitPrice']
                    "purchase_unit_cost": 14.93,
                    # 成本 - 采购成本占比 [原字段 'proportionOfCg']
                    "purchase_cost_ratio": 0.4272,
                    # 成本 - 是否有成本明细 [原字段 'hasCgPriceDetail']
                    "has_purchase_cost_detail": 1,
                    # 成本 - 总物流费用 [原字段 'cgTransportCostsTotal']
                    "logistics_cost": 0.0,
                    # 成本 - 物流单品费用 [原字段 'cgTransportUnitCosts']
                    "logistics_unit_cost": 0.0,
                    # 成本 - 物流费用占比 [原字段 'proportionOfCgTransport']
                    "logistics_cost_ratio": 0.0,
                    # 成本 - 是否有物流费用明细 [原字段 'hasCgTransportCostsDetail']
                    "has_logistics_cost_detail": 1,
                    # 成本 - 其他费用总金额 [原字段 'cgOtherCostsTotal']
                    "other_costs": 0.0,
                    # 成本 - 其他费用单品金额 [原字段 'cgOtherUnitCosts']
                    "other_unit_cost": 0.0,
                    # 成本 - 其他费用占比 [原字段 'proportionOfCgOtherCosts']
                    "other_cost_ratio": 0.0,
                    # 成本 - 是否有其他费用明细 [原字段 'hasCgOtherCostsDetail']
                    "has_other_cost_detail": 0,
                    # 利润 - 毛利润 [原字段 'grossProfit']
                    "gross_profit": 47219.53,
                    # 利润 - 毛利率 [原字段 'grossRate']
                    "gross_profit_margin": 0.2131,
                    # 利润 - 投资回报率 (ROI)
                    "roi": 0.2693,
                    # 交易状态 [原字段 'transactionStatusCode']
                    "transaction_status": "Disbursed",
                    # 交易状态描述 [原字段 'transactionStatus']
                    "transaction_status_desc": "已发放",
                    # 延迟结算状态 [原字段 'deferredSubStatusCode']
                    "deferred_settlement_status": "Disbursed",
                    # 延迟结算状态描述 [原字段 'deferredSubStatus']
                    "deferred_settlement_status_desc": "",
                    # 延迟结算总金额 [原字段 'deferredSettlementAmount']
                    "deferred_settlement": 186019.17,
                    # 结算小计 [原字段 'settlementSubtotal']
                    "settlement_subtotal": 186019.17,
                    # 报告时间 (本地时间) [原字段 'postedDateDayLocale']
                    "report_time_loc": "",
                    # 报告开始时间 (本地时间) [原字段 'minPostedDateDayLocale']
                    "report_start_time_loc": "",
                    # 报告结束时间 (本地时间) [原字段 'maxPostedDateDayLocale']
                    "report_end_time_loc": "",
                    # 报告日期 (本地时间) [原字段 'postedDateLocale']
                    "report_date_loc": "2025-08",
                    # 记录ID (非业务唯一键)
                    "id": "65545075457********",
                    # 领星店铺ID
                    "sid": 1,
                    # 领星店铺名称 [原字段 'storeName']
                    "seller_name": "Store-US",
                    # 国家 (中文)
                    "country": "美国",
                    # 国家代码 [原字段 'countryCode']
                    "country_code": "US",
                    # 商品ASIN
                    "asin": "B07*******",
                    # 商品父ASIN [原字段 'parentAsin']
                    "parent_asin": "B08*******",
                    # 关联的ASIN列表 [原字段 'asins']
                    "asins": ["B07*******", "B08*******"],
                    # 亚马逊SKU
                    "msku": "SKU********",
                    # 领星本地SKU [原字段 'localSku']
                    "lsku": "LOCAL********",
                    # 领星本地商品名称 [原字段 'localName']
                    "product_name": "JBL",
                    # 产品型号 [原字段 'model']
                    "product_model": "KX6702",
                    # 领星本地产品分类名称 [原字段 'categoryName']
                    "category_name": "",
                    # 领星本地产品品牌名称 [原字段 'brandName']
                    "brand_name": "",
                    # 标题 [原字段 'itemName']
                    "title": "Product Title",
                    # 商品略缩图链接 [原字段 'smallImageUrl']
                    "thumbnail_url": "https://m.media-amazon.com/images/****.jpg",
                    # ASIN开发人名称 [原字段 'productDeveloperRealname']
                    "developer_name": "",
                    # ASIN负责人名称 (逗号隔开) [原字段 'principalRealname']
                    "operator_names": "白小白,黑小黑",
                    # 商品标签IDs (逗号隔开) [原字段 'listingTagIds']
                    "tag_ids": "907476839534375430, 907476656619287314, 907476656619287354",
                },
                ...
            ]
        }
        ```
        """
        url = route.INCOME_STATEMENT_MSKUS
        # 构建参数
        args = {
            "start_date": start_date,
            "end_date": end_date,
            "mids": mids,
            "sids": sids,
            "query_dimension": query_dimension,
            "transaction_status": transaction_status,
            "summarize": summarize,
            "currency_code": currency_code,
            "search_field": None if search_value is None else "seller_sku",
            "search_value": search_value,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.IncomeStatement.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.IncomeStatementMskus.model_validate(data)

    async def IncomeStatementLskus(
        self,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        *,
        query_dimension: int | None = None,
        mids: int | list[int] | None = None,
        sids: int | list[int] | None = None,
        transaction_status: INCOME_STATEMENT_TRANSACTION_STATUS | None = None,
        summarize: int | None = None,
        currency_code: str | None = None,
        search_value: str | list[str] | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.IncomeStatementLskus:
        """查询损益报告-领星本地SKU维度

        ## Docs
        - 财务: [查询利润报表-SKU](https://apidoc.lingxing.com/#/docs/Finance/bdSKU)

        :param start_date `<'str/date/datetime'>`: 统计开始日期, 闭合区间
        :param end_date `<'str/date/datetime'>`: 统计结束日期, 闭合区间
        :param query_dimension `<'int/None'>`: 查询维度, 默认 `None` (使用: 0), 可选值:

            - `0`: 天维度, 开始和结束时间跨度不能超过31天
            - `1`: 月维度, 开始和结束时间跨度不能超过1个月

        :param mids `<'int/list[int]/None'>`: 领星站点ID或ID列表 (Seller.mid), 默认 `None` (不筛选)
        :param sids `<'int/list[int]/None'>`: 领星店铺ID或ID列表 (Seller.sid), 默认 `None` (不筛选)
        :param transaction_status `<'int/None'>`: 交易状态, 默认 `None` (使用: 'Disbursed'), 可选值:

            - `'Deferred'`: 订单未进入Transaction报告, 无法回款
            - `'Disbursed'`: 订单已进入Transaction报告, 可以回款
            - `'DisbursedAndSettled'`: 可以回款和预结算订单
            - `'All'`: 所有状态

        :param summarize `<'int/None'>`: 是否返回汇总数据, 默认 `None` (使用: 0), 可选值:

            - `0`: 返回原始数据
            - `1`: 返回汇总数据

        :param currency_code `<'str/None'>`: 结算金额目标转换货币代码, 默认 `None` (保持原结算货币)
        :param search_value `<'str/list[str]/None'>`: 搜索值, 默认 `None` (不筛选), 可传入单个领星本地SKU或SKU列表
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值 10000, 默认 `None` (使用: 15)
        :returns `<'IncomeStatementLskus'>`: 查询到的损益报告-领星本地SKU维度结果
        """
        url = route.INCOME_STATEMENT_LSKUS
        # 构建参数
        args = {
            "start_date": start_date,
            "end_date": end_date,
            "mids": mids,
            "sids": sids,
            "query_dimension": query_dimension,
            "transaction_status": transaction_status,
            "summarize": summarize,
            "currency_code": currency_code,
            "search_field": None if search_value is None else "local_sku",
            "search_value": search_value,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.IncomeStatement.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.IncomeStatementLskus.model_validate(data)
