# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field, field_validator
from lingxingapi.base.schema import ResponseV1, ResponseV1TraceId, FlattenDataRecords
from lingxingapi.fields import IntOrNone2Zero, FloatOrNone2Zero, StrOrNone2Blank


# 用户自定义费用管理 --------------------------------------------------------------------------------------------------------------
# . User Fee Types
class UserFeeType(BaseModel):
    """用户自定义费用类型"""

    # 序号 [原字段 'sort']
    seq: int = Field(validation_alias="sort")
    # 费用类型ID [原字段 'id']
    fee_type_id: int = Field(validation_alias="id")
    # 费用类型名称 [原字段 'name']
    fee_type_name: str = Field(validation_alias="name")
    # 备用ID
    fpoft_id: str


class UserFeeTypes(ResponseV1):
    """用户自定义费用类型列表"""

    data: list[UserFeeType]


# 亚马逊交易数据 -----------------------------------------------------------------------------------------------------------------
# . Transactions
class Transaction(BaseModel):
    """亚马逊交易明细"""

    # 唯一键 [原字段 'uniqueKey']
    # 交易明细唯一标识, 当 event_type 为 'serviceFeeEventList' 时, uid 会变动
    # 但当交易明细 settlement_status 为 'Closed' 状态时 uid 不会变化
    # 建议拉取数据时, 把这个类型的数据作单独的删除与写入操作
    uid: str = Field(validation_alias="uniqueKey")
    # 领星店铺ID
    sid: int
    # 亚马逊卖家ID [原字段 'sellerId']
    seller_id: str = Field(validation_alias="sellerId")
    # 领星店铺名称 [原字段 'storeName']
    seller_name: str = Field(validation_alias="storeName")
    # 国家代码 [原字段 'countryCode']
    country_code: str = Field(validation_alias="countryCode")
    # 市场名称 [原字段 'marketplaceName']
    marketplace: str = Field(validation_alias="marketplaceName")
    # 账单类型 [原字段 'accountType']
    account_type: str = Field(validation_alias="accountType")
    # 事件组ID [原字段 'financialEventGroupId']
    financial_event_group_id: str = Field(validation_alias="financialEventGroupId")
    # 事件类型 [原字段 'eventType']
    event_type: str = Field(validation_alias="eventType")
    # 交易编号 [原字段 'fid']
    transaction_number: str = Field(validation_alias="fid")
    # 交易类型 [原字段 'type']
    transaction_type: str = Field(validation_alias="type")
    # 结算ID [原字段 'settlementId']
    settlement_id: IntOrNone2Zero = Field(validation_alias="settlementId")
    # 处理状态 [原字段 'processingStatus']
    # (Open: 未结算, Closed: 已结算, Reconciled: 已对账)
    settlement_status: str = Field(validation_alias="processingStatus")
    # 资金转账状态 [原字段 'fundTransferStatus']
    # (Succeeded: 已转账, Processing: 转账中, Failed: 失败, Unknown: 未知)
    transfer_status: str = Field(validation_alias="fundTransferStatus")
    # 数量 [原字段 'quantity']
    transaction_qty: int = Field(validation_alias="quantity")
    # 金额 [原字段 'currencyAmount']
    transaction_amt: float = Field(validation_alias="currencyAmount")
    # 币种 [原字段 'currencyCode']
    currency_code: str = Field(validation_alias="currencyCode")
    # 交易发生时间 (UTC时间) [原字段 'postedDate']
    transaction_time_utc: str = Field(validation_alias="postedDate")
    # 交易发生时间 (本地时间) [原字段 'postedDateLocale']
    transaction_time_loc: str = Field(validation_alias="postedDateLocale")
    # 数据创建时间 (中国时间) [原字段 'gmtCreate']
    create_time_cnt: str = Field(validation_alias="gmtCreate")
    # 数据更新时间 (中国时间) [原字段 'gmtModified']
    update_time_cnt: str = Field(validation_alias="gmtModified")
    # 亚马逊订单编号 [原字段 'amazonOrderId']
    amazon_order_id: StrOrNone2Blank = Field(validation_alias="amazonOrderId")
    # 商家订单ID [原字段 'merchantOrderId']
    merchant_order_id: StrOrNone2Blank = Field(validation_alias="merchantOrderId")
    # 卖家提供的订单编号 [原字段 'sellerOrderId']
    seller_order_id: StrOrNone2Blank = Field(validation_alias="sellerOrderId")
    # 亚马逊订单ID [原字段 'orderId']
    order_id: StrOrNone2Blank = Field(validation_alias="orderId")
    # 亚马逊订单商品ID [原字段 'orderItemId']
    order_item_id: IntOrNone2Zero = Field(validation_alias="orderItemId")
    # 配送渠道 [原字段 'fulfillment']
    fulfillment_channel: str = Field(validation_alias="fulfillment")
    # 亚马逊SKU [原字段 'sellerSku']
    msku: StrOrNone2Blank = Field(validation_alias="sellerSku")
    # 领星本地SKU [原字段 'localSku']
    lsku: StrOrNone2Blank = Field(validation_alias="localSku")
    # FNSKU [原字段 'fnsku']
    fnsku: StrOrNone2Blank = Field(validation_alias="fnsku")
    # 领星本地商品名称 [原字段 'localName']
    product_name: StrOrNone2Blank = Field(validation_alias="localName")
    # 费用类型 [原字段 'feeType']
    fee_type: str = Field(validation_alias="feeType")
    # 费用描述 [原字段 'feeDescription']
    fee_desc: str = Field(validation_alias="feeDescription")
    # 费用原因 [原字段 'feeReason']
    fee_reason: str = Field(validation_alias="feeReason")
    # 促销ID [原字段 'promotionId']
    promotion_id: str = Field(validation_alias="promotionId")
    # 活动ID [原字段 'dealId']
    deal_id: str = Field(validation_alias="dealId")
    # 活动描述 [原字段 'dealDescription']
    deal_desc: str = Field(validation_alias="dealDescription")
    # 优惠券ID [原字段 'couponId']
    coupon_id: str = Field(validation_alias="couponId")
    # 优惠券描述 [原字段 'sellerCouponDescription']
    coupon_desc: str = Field(validation_alias="sellerCouponDescription")
    # 优惠券兑换次数 [原字段 'clipOrRedemptionCount']
    coupon_redemption_count: int = Field(validation_alias="clipOrRedemptionCount")
    # 发票ID [原字段 'invoiceId']
    invoice_id: str = Field(validation_alias="invoiceId")
    # 支付事件ID [原字段 'paymentEventId']
    payment_event_id: str = Field(validation_alias="paymentEventId")
    # 注册ID [原字段 'enrollmentId']
    enrollment_id: str = Field(validation_alias="enrollmentId")
    # 债务恢复类型 [原字段 'debtRecoveryType']
    debt_recovery_type: str = Field(validation_alias="debtRecoveryType")
    # 移除货件项ID [原字段 'removalShipmentItemId']
    removal_shipment_item_id: str = Field(validation_alias="removalShipmentItemId")
    # 调整事件ID [原字段 'adjustmentEventId']
    adjustment_event_id: str = Field(validation_alias="adjustmentEventId")
    # 安全索赔ID [原字段 'safeTClaimId']
    safe_t_claim_id: str = Field(validation_alias="safeTClaimId")
    # 安全索赔原因代码 [原字段 'reasonCode']
    saft_t_claim_reason: str = Field(validation_alias="reasonCode")


class Transactions(ResponseV1, FlattenDataRecords):
    """亚马逊交易明细列表"""

    data: list[Transaction]


# . Settlements
class SettlementIncome(BaseModel):
    """亚马逊结算收入明细"""

    # 销售 [原字段 'product']
    product_sales: float = Field(validation_alias="product")
    # 运费 [原字段 'freight']
    shipping_credits: float = Field(validation_alias="freight")
    # 包装 [原字段 'packing']
    giftwrap_credits: float = Field(validation_alias="packing")
    # 其他
    other: float
    # 税费
    tax: float
    # 总收入 [原字段 'sale']
    total_income: float = Field(validation_alias="sale")


class SettlementRefund(BaseModel):
    """亚马逊结算退费明细"""

    # 销售退费
    sales_refunds: float = Field(validation_alias="saleRefund")
    # 其他退费
    other_refunds: float = Field(validation_alias="feeRefund")
    # 税费退费
    tax_refunds: float = Field(validation_alias="tax")
    # 总退费
    total_refunds: float = Field(validation_alias="refund")


class SettlementExpense(BaseModel):
    """亚马逊结算支出明细"""

    # 亚马逊费用 [原字段 'amazon']
    amazon_fees: float = Field(validation_alias="amazon")
    # 库存费用 [原字段 'storage']
    inventory_fees: float = Field(validation_alias="storage")
    # 广告费用 [原字段 'ad']
    cost_of_advertising: float = Field(validation_alias="ad")
    # 促销费用 [原字段 'promotion']
    promotion_rebates: float = Field(validation_alias="promotion")
    # 其他费用 [原字段 'other']
    other_fees: float = Field(validation_alias="other")
    # 总支出 [原字段 'pay']
    total_expense: float = Field(validation_alias="pay")


class SettlementTransfer(BaseModel):
    """亚马逊结算转账明细"""

    # 初期余额 [原字段 'beginningBalanceCurrencyAmount']
    opening_balance: float = Field(validation_alias="beginningBalanceCurrencyAmount")
    # 本期应收 [原字段 'originalTotalCurrencyAmount']
    receivable: float = Field(validation_alias="originalTotalCurrencyAmount")
    # 信用卡扣款 [原字段 'creditCardDeduction']
    credit_card_deduction: float = Field(validation_alias="creditCardDeduction")
    # 上期预留金余额 [原字段 'previousReserveAmount']
    prior_reserve_balance: float = Field(validation_alias="previousReserveAmount")
    # 本期预留金余额 [原字段 'currentReserveAmount']
    current_reserve_balance: float = Field(validation_alias="currentReserveAmount")
    # 本期结算 [原字段 'convertedTotalCurrencyAmount']
    settlement: float = Field(validation_alias="convertedTotalCurrencyAmount")


class Settlement(BaseModel):
    """亚马逊结算汇总"""

    # fmt: off
    # 领星店铺ID
    sid: int
    # 亚马逊卖家ID [原字段 'sellerId']
    seller_id: str = Field(validation_alias="sellerId")
    # 领星店铺名称 [原字段 'storeName']
    seller_name: str = Field(validation_alias="storeName")
    # 国家代码 [原字段 'countryCode']
    country_code: str = Field(validation_alias="countryCode")
    # 追踪编号 [原字段 'traceId']
    trace_number: str = Field(validation_alias="traceId")
    # 结算ID [原字段 'settlementId']
    settlement_id: IntOrNone2Zero = Field(validation_alias="settlementId")
    # 结算编号 [原字段 'id']
    settlement_number: str = Field(validation_alias="id")
    # 结算备注 [原字段 'comment']
    settlement_note: StrOrNone2Blank = Field(validation_alias="comment")
    # 结算状态 [原字段 'processingStatus']
    # (Open: 未结算, Closed: 已结算, Reconciled: 已对账)
    settlement_status: str = Field(validation_alias="processingStatus")
    # 资金转账状态 [原字段 'fundTransferStatus']
    # (Succeeded: 已转账, Processing: 转账中, Failed: 失败, Unknown: 未知)
    transfer_status: str = Field(validation_alias="fundTransferStatus")
    # 账单类型 [原字段 'accountType']
    account_type: str = Field(validation_alias="accountType")
    # 原始结算货币代码 [原字段 'originalTotalCurrencyCode']
    settlement_currency_code: str = Field(validation_alias="originalTotalCurrencyCode")
    # 原始结算金额 [原字段 'originalTotalCurrencyAmount']
    settlement_amt: float = Field(validation_alias="originalTotalCurrencyAmount")
    # 转账货币代码 [原字段 'convertedTotalCurrencyCode']
    transfer_currency_code: str = Field(validation_alias="convertedTotalCurrencyCode")
    # 转账金额 [原字段 'convertedTotalCurrencyAmount']
    transfer_amt: float = Field(validation_alias="convertedTotalCurrencyAmount")
    # 转账折算结算金额 [原字段 'convertedTotalCurrencyAmountToOrigin']
    transfer_to_settlement_amt: float = Field(validation_alias="convertedTotalCurrencyAmountToOrigin")
    # 结算事件组ID [原字段 'financialEventGroupId']
    settlement_event_group_id: str = Field(validation_alias="financialEventGroupId")
    # 结算事件金额 [原字段 'financialEventsAmount']
    settlement_events_amt: float = Field(validation_alias="financialEventsAmount")
    # 对账结果 [原字段 'reconciliationResult']
    reconciliation_result: str = Field(validation_alias="reconciliationResult")
    # 汇款比率 [原字段 'remittanceRate']
    remittance_rate: float = Field(validation_alias="remittanceRate")
    # 银行帐号信息 [原字段 'accountInfo']
    banck_account_info: StrOrNone2Blank = Field(validation_alias="accountInfo")
    # 银行帐号尾号 [原字段 'accountTail']
    bank_account_last_digits: StrOrNone2Blank = Field(validation_alias="accountTail")
    # 收入 [原字段 'sale']
    income: SettlementIncome = Field(validation_alias="sale")
    # 退费
    refund: SettlementRefund
    # 支出 [原字段 'pay']
    expense: SettlementExpense = Field(validation_alias="pay")
    # 转账
    transfer: SettlementTransfer = Field(validation_alias="transfer")
    # 结算开始时间 (本地时间) [原字段 'financialEventGroupStartLocale']
    settlement_start_time_loc: str = Field(validation_alias="financialEventGroupStartLocale")
    # 结算结束时间 (本地时间) [原字段 'financialEventGroupEndLocale']
    settlement_end_time_loc: str = Field(validation_alias="financialEventGroupEndLocale")
    # 资金转账时间 (本地时间) [原字段 'fundTransferDateLocale']
    transfer_time_loc: str = Field(validation_alias="fundTransferDateLocale")
    # 资金转账时间 (UTC时间) [原字段 'fundTransferDate']
    transfer_time_utc: str = Field(validation_alias="fundTransferDate")
    # fmt: on


class Settlements(ResponseV1, FlattenDataRecords):
    """亚马逊结算汇总列表"""

    data: list[Settlement]


# . Settlement Variances
class ShipmentSettlement(BaseModel):
    """亚马逊发货与结算差异"""

    # fmt: off
    # 领星店铺ID
    sid: int
    # 亚马逊卖家ID [原字段 'sellerId']
    seller_id: str = Field(validation_alias="sellerId")
    # 领星店铺名称 [原字段 'sellerName']
    seller_name: str = Field(validation_alias="sellerName")
    # 国家代码 [原字段 'countryCode']
    country_code: str = Field(validation_alias="countryCode")
    # 亚马逊订单编号 [原字段 'amazonOrderId']
    amazon_order_id: str = Field(validation_alias="amazonOrderId")
    # 卖家提供的订单编号 [原字段 'merchantOrderId']
    merchant_order_id: str = Field(validation_alias="merchantOrderId")
    # 亚马逊货件编号 [原字段 'shipmentId']
    shipment_id: str = Field(validation_alias="shipmentId")
    # 亚马逊货件商品编号 [原字段 'shipmentItemId']
    shipment_item_id: str = Field(validation_alias="shipmentItemId")
    # 销售渠道 [原字段 'salesChannel']
    sales_channel: str = Field(validation_alias="salesChannel")
    # 配送方式 [原字段 'fulfillment']
    fulfillment_channel: str = Field(validation_alias="fulfillment")
    # 亚马逊配送中心代码 [原字段 'fulfillmentCenterId']
    fulfillment_center_id: str = Field(validation_alias="fulfillmentCenterId")
    # 物流模式 [原字段 'logisitcsMode']
    logistics_mode: str = Field(validation_alias="logisitcsMode")
    # 物流跟踪号 [原字段 'trackingNumber']
    tracking_number: str = Field(validation_alias="trackingNumber")
    # 结算ID [原字段 'settlementId']
    settlement_id: IntOrNone2Zero = Field(validation_alias="settlementId")
    # 处理状态 [原字段 'processingStatus']
    # (Open: 未结算, Closed: 已结算, Reconciled: 已对账)
    settlement_status: StrOrNone2Blank = Field(validation_alias="processingStatus")
    # 资金转账状态 [原字段 'fundTransferStatus']
    # (Succeeded: 已转账, Processing: 转账中, Failed: 失败, Unknown: 未知)
    transfer_status: StrOrNone2Blank = Field(validation_alias="fundTransferStatus")
    # 发货与结算时间差异 [原字段 'daysBetweenShipAndFiance']
    settlement_lag: str = Field(validation_alias="daysBetweenShipAndFiance")
    # 亚马逊SKU
    msku: str
    # 领星本地SKU [原字段 'localSku']
    lsku: StrOrNone2Blank = Field(validation_alias="localSku")
    # 领星本地商品名称 [原字段 'localName']
    product_name: StrOrNone2Blank = Field(validation_alias="localName")
    # 领星本地品牌名称 [原字段 'brandName']
    brand_name: StrOrNone2Blank = Field(validation_alias="brandName")
    # 领星本地分类名称 [原字段 'categoryName']
    category_name: StrOrNone2Blank = Field(validation_alias="categoryName")
    # 商品开发负责人名称 [原字段 'productDeveloper']
    developer_name: StrOrNone2Blank = Field(validation_alias="productDeveloper")
    # 商品负责人名称 (逗号分隔) [原字段 'listing']
    operator_names: StrOrNone2Blank = Field(validation_alias="listing")
    # 订单商品总数量 [原字段 'quantity']
    order_qty: int = Field(validation_alias="quantity")
    # 商品销售金额 [原字段 'itemPrice']
    sales_amt: FloatOrNone2Zero = Field(validation_alias="itemPrice")
    # 商品销售金额税费 [原字段 'itemTax']
    sales_tax_amt: FloatOrNone2Zero = Field(validation_alias="itemTax")
    # 买家支付运费金额 [原字段 'shippingPrice']
    shipping_credits_amt: FloatOrNone2Zero = Field(validation_alias="shippingPrice")
    # 买家支付运费税费 [原字段 'shippingTax']
    shipping_credits_tax_amt: FloatOrNone2Zero = Field(validation_alias="shippingTax")
    # 买家支付礼品包装费金额 [原字段 'giftWrapPrice']
    giftwrap_credits_amt: FloatOrNone2Zero = Field(validation_alias="giftWrapPrice")
    # 买家支付礼品包装费税费 [原字段 'giftWrapTax']
    giftwrap_credits_tax_amt: FloatOrNone2Zero = Field(validation_alias="giftWrapTax")
    # 卖家商品促销折扣金额 [原字段 'itemPromotionDiscount']
    promotion_discount_amt: FloatOrNone2Zero = Field(validation_alias="itemPromotionDiscount")
    # 卖家商品运费折扣金额 [原字段 'shipPromotionDiscount']
    shipping_discount_amt: FloatOrNone2Zero = Field(validation_alias="shipPromotionDiscount")
    # 货币代码 [原字段 'currencyCode']
    currency_code: str = Field(validation_alias="currencyCode")
    # 买家国家 [原字段 'saleCountryName']
    buyer_country: StrOrNone2Blank = Field(validation_alias="saleCountryName")
    # 买家城市 [原字段 'shipCity']
    buyer_city: str = Field(validation_alias="shipCity")
    # 买家区域 [原字段 'region']
    buyer_district: str = Field(validation_alias="region")
    # 买家邮编 [原字段 'shipPostalCode']
    buyer_postcode: str = Field(validation_alias="shipPostalCode")
    # 订单购买时间 (本地时间) [原字段 'purchaseDateLocale']
    purchase_time_loc: StrOrNone2Blank = Field(validation_alias="purchaseDateLocale")
    # 订单发货时间 (本地时间) [原字段 'shipmentsDateLocale']
    shipment_time_loc: StrOrNone2Blank = Field(validation_alias="shipmentsDateLocale")
    # 订单付款时间 (本地时间) [原字段 'paymentsDateLocale']
    payment_time_loc: StrOrNone2Blank = Field(validation_alias="paymentsDateLocale")
    # 订单结算时间 (本地时间) [原字段 'financePostedDateLocale']
    settlement_time_loc: StrOrNone2Blank = Field(validation_alias="financePostedDateLocale")
    # 资金转账时间 (本地时间) [原字段 'fundTransferDateLocale']
    transfer_time_loc: StrOrNone2Blank = Field(validation_alias="fundTransferDateLocale")
    # 数据更新时间 (中国时间) [原字段 'gmtModified']
    update_time_cnt: str = Field(validation_alias="gmtModified")
    # fmt: on


class ShipmentSettlements(ResponseV1TraceId, FlattenDataRecords):
    """亚马逊发货与结算差异列表"""

    data: list[ShipmentSettlement]


# . Receivables
class Receivable(BaseModel):
    """亚马逊应收账款"""

    # 领星店铺ID
    sid: int
    # 领星店铺名称 [原字段 'storeName']
    seller_name: str = Field(validation_alias="storeName")
    # 国家 (中文)
    country: str
    # 国家代码 [原字段 'countryCode']
    country_code: str = Field(validation_alias="countryCode")
    # 对账状态 (0: 未对账, 1: 已对账)
    archive_status: int = Field(validation_alias="archiveStatus")
    # 对账状态描述
    archive_status_desc: str = Field(validation_alias="archiveStatusName")
    # 应收款备注 [原字段 'remark']
    note: StrOrNone2Blank = Field(validation_alias="remark")
    # 初期余额 [原字段 'beginningBalanceCurrencyAmount']
    opening_balance: float = Field(validation_alias="beginningBalanceCurrencyAmount")
    # 收入金额 [原字段 'incomeAmount']
    income: float = Field(validation_alias="incomeAmount")
    # 退费金额 [原字段 'refundAmount']
    refund: float = Field(validation_alias="refundAmount")
    # 支出金额 [原字段 'spendAmount']
    expense: float = Field(validation_alias="spendAmount")
    # 其他金额
    other: float
    # 其他: 信用卡扣款金额 [原字段 'card']
    other_credit_card_deduction: float = Field(validation_alias="card")
    # 其他: 其他子项金额 [原字段 'otherItem']
    other_item: float = Field(validation_alias="otherItem")
    # 转账成功金额 [原字段 'convertedSuccessAmount']
    transfer_success: float = Field(validation_alias="convertedSuccessAmount")
    # 转账到账金额 [原字段 'receivedAmount']
    transfer_received: float = Field(validation_alias="receivedAmount")
    # 转账失败金额 [原字段 'convertedFailedAmount']
    transfer_failed: float = Field(validation_alias="convertedFailedAmount")
    # 期末余额 [原字段 'endingBalance']
    ending_balance: float = Field(validation_alias="endingBalance")
    # 币种代码 [原字段 'currencyCode']
    currency_code: str = Field(validation_alias="currencyCode")
    # 币种符号 [原字段 'currencyIcon']
    currency_icon: str = Field(validation_alias="currencyIcon")
    # 结算日期 (格式: YYYY-MM) [原字段 'settlementDate']
    settlement_date: str = Field(validation_alias="settlementDate")


class Receivables(ResponseV1):
    """亚马逊应收账款列表"""

    data: list[Receivable]


# 亚马逊库存数据 -----------------------------------------------------------------------------------------------------------------
# . Ledger Details
class LedgerDetailItem(BaseModel):
    """亚马逊库存明细台账"""

    # 同uid_idx共同构成唯一索引 [原字段 'uniqueMd5']
    uid: str = Field(validation_alias="uniqueMd5")
    # 同uid共同构成唯一索引 [原字段 'uniqueMd5Idx']
    uid_idx: int = Field(validation_alias="uniqueMd5Idx")
    # 货物关联ID [原字段 'referenceId']
    reference_id: str = Field(validation_alias="referenceId")
    # 亚马逊卖家ID [原字段 'sellerId']
    seller_id: str = Field(validation_alias="sellerId")
    # 亚马逊ASIN
    asin: str
    # 亚马逊SKU
    msku: str
    # 亚马逊FNSKU
    fnsku: str
    # 商品标题
    title: str
    # 事件类型编码 [原字段 'eventType']
    event_type_code: str = Field(validation_alias="eventType")
    # 事件类型 [原字段 'eventTypeDesc']
    event_type: str = Field(validation_alias="eventTypeDesc")
    # 事件原因 [原字段 'reason']
    event_reason: str = Field(validation_alias="reason")
    # 事件发生日期 [原字段 'date']
    event_date: str = Field(validation_alias="date")
    # 国家代码 (库存位置) [原字段 'location']
    country_code: str = Field(validation_alias="location")
    # 亚马逊配送中心代码 [原字段 'fulfillmentCenter']
    fulfillment_center_id: str = Field(validation_alias="fulfillmentCenter")
    # 库存处置结果编码 [原字段 'disposition']
    disposition_code: str = Field(validation_alias="disposition")
    # 库存处置结果 [原字段 'dispositionDesc']
    disposition: str = Field(validation_alias="dispositionDesc")
    # 数量 [原字段 'quantity']
    qty: int = Field(validation_alias="quantity")


class LedgerDetail(ResponseV1TraceId, FlattenDataRecords):
    """亚马逊库存明细台账列表"""

    data: list[LedgerDetailItem]


# . Ledger Summary
class LedgerSummaryItem(BaseModel):
    """亚马逊库存汇总台账"""

    # 同uid_idx共同构成唯一索引 [原字段 'uniqueMd5']
    uid: str = Field(validation_alias="uniqueMd5")
    # 同uid共同构成唯一索引 [原字段 'uniqueMd5Idx']
    uid_idx: int = Field(validation_alias="uniqueMd5Idx")
    # 亚马逊卖家ID [原字段 'sellerId']
    seller_id: str = Field(validation_alias="sellerId")
    # 亚马逊ASIN
    asin: str
    # 亚马逊SKU
    msku: str
    # 亚马逊FNSKU
    fnsku: str
    # 商品标题
    title: str
    # 汇总月份/日期 [原字段 'date']
    # (月维度: '2024-01', 日维度: '2024-01-01')
    summary_date: str = Field(validation_alias="date")
    # 国家代码 (库存位置) [原字段 'location']
    country_code: str = Field(validation_alias="location")
    # 库存处置结果编码 [原字段 'disposition']
    disposition_code: str = Field(validation_alias="disposition")
    # 库存处置结果 [原字段 'dispositionDesc']
    disposition: str = Field(validation_alias="dispositionDesc")
    # 初期库存 [原字段 'startingWarehouseBalance']
    opening_balance: int = Field(validation_alias="startingWarehouseBalance")
    # 调拨变动 [原字段 'warehouseTransferInOrOut']
    transfer_net: int = Field(validation_alias="warehouseTransferInOrOut")
    # 调拨在途 [原字段 'inTransitBetweenWarehouses']
    transfer_in_transit: int = Field(validation_alias="inTransitBetweenWarehouses")
    # 签收入库 [原字段 'receipts']
    received: int = Field(validation_alias="receipts")
    # 销售出库 [原字段 'customerShipments']
    customer_shipment: int = Field(validation_alias="customerShipments")
    # 销售退货 [原字段 'customerReturns']
    customer_returned: int = Field(validation_alias="customerReturns")
    # 卖家移除 [原字段 'vendorReturns']
    seller_removal: int = Field(validation_alias="vendorReturns")
    # 丢失报损 [原字段 'lost']
    lost_events: int = Field(validation_alias="lost")
    # 盘盈找回 [原字段 'found']
    found_events: int = Field(validation_alias="found")
    # 受损调整 [原字段 'damaged']
    damaged_events: int = Field(validation_alias="damaged")
    # 处置报废 [原字段 'disposed']
    disposed_events: int = Field(validation_alias="disposed")
    # 其他事件变动 [原字段 'otherEvents']
    other_events: int = Field(validation_alias="otherEvents")
    # 未知事件变动 [原字段 'unKnownEvents']
    unknown_events: int = Field(validation_alias="unKnownEvents")
    # 期末库存 [原字段 'endingWareHouseBalance']
    closing_balance: int = Field(validation_alias="endingWareHouseBalance")


class LedgerSummary(ResponseV1TraceId, FlattenDataRecords):
    """亚马逊库存汇总台账列表"""

    data: list[LedgerSummaryItem]


# . Ledger Valuation
class LedgerValuationItem(BaseModel):
    """亚马逊库存价值台账"""

    # 唯一键 [原字段 'unique_key']
    uid: str = Field(validation_alias="unique_key")
    # 库存动作类型编码 [原字段 'business_type']
    transaction_type_code: str = Field(validation_alias="business_type")
    # 库存动作类型 [原字段 'business_type_desc']
    transaction_type: str = Field(validation_alias="business_type_desc")
    # 库存动作单号 [原字段 'business_number']
    transaction_number: str = Field(validation_alias="business_number")
    # 库存动作原因 [原字段 'reason']
    transaction_reason: str = Field(validation_alias="reason")
    # 源头单据号 (中文逗号分割) [原字段 'origin_account']
    source_numbers: str = Field(validation_alias="origin_account")
    # 领星店铺名称 [原字段 'shop_name']
    seller_name: str = Field(validation_alias="shop_name")
    # 仓库名称 [原字段 'wh_name']
    warehouse_name: str = Field(validation_alias="wh_name")
    # 亚马逊SKU
    msku: str
    # 领星本地SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 结存数量 [原字段 'balance_quantity']
    balance_qty: int = Field(validation_alias="balance_quantity")
    # 采购单价 [原字段 'balance_purchase_unit_price']
    purchase_unit_cost: float = Field(validation_alias="balance_purchase_unit_price")
    # 采购金额 [原字段 'balance_purchase_amount']
    purchase_total_cost: float = Field(validation_alias="balance_purchase_amount")
    # 物流单价 [原字段 'balance_logistics_unit_price']
    logistics_unit_cost: float = Field(validation_alias="balance_logistics_unit_price")
    # 物流金额 [原字段 'balance_logistics_amount']
    logistics_total_cost: float = Field(validation_alias="balance_logistics_amount")
    # 其他单价 [原字段 'balance_other_unit_price']
    other_unit_cost: float = Field(validation_alias="balance_other_unit_price")
    # 其他金额 [原字段 'balance_other_amount']
    other_total_cost: float = Field(validation_alias="balance_other_amount")
    # 成本来源 [原字段 'cost_source']
    cost_source: str = Field(validation_alias="cost_source")
    # 库存处置 [原字段 'disposition_type']
    disposition: str = Field(validation_alias="disposition_type")
    # 源头数据时间
    source_data_time: str
    # 库存动作日期 [原字段 'stream_date']
    transaction_date: str = Field(validation_alias="stream_date")
    # 数据版本
    data_version: str


class LedgerValuation(ResponseV1TraceId, FlattenDataRecords):
    """亚马逊库存价值台账列表"""

    data: list[LedgerValuationItem]


# 亚马逊广告数据 -----------------------------------------------------------------------------------------------------------------
# . Ads Invoices
class AdsInvoices(BaseModel):
    """亚马逊广告发票"""

    # 领星店铺ID
    sid: int
    # 领星店铺名称 [原字段 'store_name']
    seller_name: str = Field(validation_alias="store_name")
    # 国家 (中文)
    country: str
    # 广告发票ID
    invoice_id: str
    # 广告发票状态 [原字段 'status']
    invoice_status: str = Field(validation_alias="status")
    # 付款方式
    payment_method: str
    # 广告花费 [原字段 'cost_amount']
    cost_amt: float = Field(validation_alias="cost_amount")
    # 税费 [原字段 'tax_amount']
    tax_amt: float = Field(validation_alias="tax_amount")
    # 分摊费用 [原字段 'other_allocation_fee']
    # 总发票金额中扣除的其他费或税费，按此发票的花费占比分摊
    allocation_amt: float = Field(validation_alias="other_allocation_fee")
    # 广告发票总金额 [原字段 'amount']
    invoice_amt: float = Field(validation_alias="amount")
    # 账单周期开始日期 [原字段 'from_date']
    billing_start_date: str = Field(validation_alias="from_date")
    # 账单周期结束日期 [原字段 'to_date']
    billing_end_date: str = Field(validation_alias="to_date")
    # 广告发票开具日期
    invoice_date: str


class AdsInvoices(ResponseV1):
    """亚马逊广告发票列表"""

    data: list[AdsInvoices]


# . Ads Invoice Detail
class AdsInvoiceDetailData(BaseModel):
    """亚马逊广告发票明细数据"""

    # 广告发票ID
    invoice_id: str
    # 付款方式
    payment_method: str
    # 广告发票总金额 [原字段 'amount']
    invoice_amt: float = Field(validation_alias="amount")
    # 币种代码
    currency_code: str
    # 币种图标
    currency_icon: str
    # 账单地址 [原字段 'address']
    billing_address: StrOrNone2Blank = Field(validation_alias="address")
    # 账单周期开始日期 [原字段 'from_date']
    billing_start_date: str = Field(validation_alias="from_date")
    # 账单周期结束日期 [原字段 'to_date']
    billing_end_date: str = Field(validation_alias="to_date")
    # 广告发票开具日期
    invoice_date: str


class AdsInvoiceDetail(ResponseV1):
    """亚马逊广告发票明细"""

    data: AdsInvoiceDetailData


# . Ads Campaign Invoices
class AdsCampaignInvoice(BaseModel):
    """亚马逊广告活动发票明细"""

    # 广告活动ID
    campaign_id: str
    # 广告活动名称
    campaign_name: str
    # 广告数据来源 [原字段 'origin']
    source: str = Field(validation_alias="origin")
    # 广告商品
    items: list[str]
    # 广告类型 [原字段 'ads_type']
    ad_type: str = Field(validation_alias="ads_type")
    # 计价方式
    price_type: str
    # 广告事件次数 [原字段 'cost_event_count']
    event_count: int = Field(validation_alias="cost_event_count")
    # 广告事件单次花费 [原字段 'cost_per_unit']
    cost_per_event: float = Field(validation_alias="cost_per_unit")
    # 广告总花费 [原字段 'cost_amount']
    cost_amt: float = Field(validation_alias="cost_amount")
    # 分摊费用 [原字段 'other_allocation_fee']
    allocation_amt: float = Field(validation_alias="other_allocation_fee")
    # 币种图标 [原字段 'currency_icon']
    currency_icon: str = Field(validation_alias="currency_icon")


class AdsCampaignInvoices(ResponseV1):
    """亚马逊广告活动发票明细列表"""

    data: list[AdsCampaignInvoice]


# 亚马逊损益报告 -----------------------------------------------------------------------------------------------------------------
# . Income Statement
class UserOtherFee(BaseModel):
    """用户自定义其他费用"""

    # 费用金额
    fee_id: int
    # 费用名称
    fee_name: str
    # 费用金额
    fee_amt: float


class IncomeStatement(BaseModel):
    """损益报告-项目维度"""

    # fmt: off
    # 币种代码 [原字段 'currencyCode']
    currency_code: str = Field(validation_alias="currencyCode")
    # 币种图标 [原字段 'currencyIcon']
    currency_icon: str = Field(validation_alias="currencyIcon")
    # 收入 - 总收入金额 [原字段 'grossProfitIncome']
    total_income: FloatOrNone2Zero = Field(validation_alias="grossProfitIncome")
    # 收入 - 总销售金额 [原字段 'totalSalesAmount']
    product_sales: float = Field(validation_alias="totalSalesAmount")
    # 收入 - 总销售数量 [原字段 'totalSalesQuantity']
    product_sales_qty: int = Field(validation_alias="totalSalesQuantity")
    # 收入 - 总销售退费 [原字段 'totalSalesRefunds']
    product_sales_refunds: float = Field(validation_alias="totalSalesRefunds")
    # 收入 - FBA销售金额 [原字段 'fbaSaleAmount']
    fba_product_sales: float = Field(validation_alias="fbaSaleAmount")
    # 收入 - FBA销售数量 [原字段 'fbaSalesQuantity']
    fba_product_sales_qty: int = Field(validation_alias="fbaSalesQuantity")
    # 收入 - FBA销售退费 [原字段 'fbaSalesRefunds']
    fba_product_sales_refunds: float = Field(validation_alias="fbaSalesRefunds")
    # 收入 - FBM销售金额 [原字段 'fbmSaleAmount']
    fbm_product_sales: float = Field(validation_alias="fbmSaleAmount")
    # 收入 - FBM销售数量 [原字段 'fbmSalesQuantity']
    fbm_product_sales_qty: int = Field(validation_alias="fbmSalesQuantity")
    # 收入 - FBM销售退费 [原字段 'fbmSalesRefunds']
    fbm_product_sales_refunds: float = Field(validation_alias="fbmSalesRefunds")
    # 收入 - FBA库存赔付/补偿金额 [原字段 'fbaInventoryCredit']
    fba_inventory_credits: float = Field(validation_alias="fbaInventoryCredit")
    # 收入 - FBA库存赔付/补偿数量 [原字段 'fbaInventoryCreditQuantity']
    fba_inventory_credit_qty: int = Field(validation_alias="fbaInventoryCreditQuantity")
    # 收入 - FBA清算收益金额 [原字段 'fbaLiquidationProceeds']
    fba_liquidation_proceeds: float = Field(validation_alias="fbaLiquidationProceeds")
    # 收入 - FBA清算收益调整金额 [原字段 'fbaLiquidationProceedsAdjustments']
    fba_liquidation_proceeds_adj: float = Field(validation_alias="fbaLiquidationProceedsAdjustments")
    # 收入 - 配送运费收入金额 (买家支出) [原字段 'shippingCredits']
    shipping_credits: float = Field(validation_alias="shippingCredits")
    # 收入 - 配送运费退款金额 (买家收入) [原字段 'shippingCreditRefunds']
    shipping_credit_refunds: float = Field(validation_alias="shippingCreditRefunds")
    # 收入 - 礼品包装费收入金额 (买家支出) [原字段 'giftWrapCredits']
    giftwrap_credits: float = Field(validation_alias="giftWrapCredits")
    # 收入 - 礼品包装费退款金额 (买家收入) [原字段 'giftWrapCreditRefunds']
    giftwrap_credit_refunds: float = Field(validation_alias="giftWrapCreditRefunds")
    # 收入 - 促销折扣金额 (卖家支出) [原字段 'promotionalRebates']
    promotional_rebates: float = Field(validation_alias="promotionalRebates")
    # 收入 - 促销折扣退款金额 (卖家收入) [原字段 'promotionalRebateRefunds']
    promotional_rebate_refunds: float = Field(validation_alias="promotionalRebateRefunds")
    # 收入 - A-to-Z 保障/索赔金额 [原字段 'guaranteeClaims']
    a2z_guarantee_claims: float = Field(validation_alias="guaranteeClaims")
    # 收入 - 拒付金额 (拒付造成的让利（发生时为负数）)
    chargebacks: float
    # 收入 - 亚马逊运费补偿金额 [原字段 'amazonShippingReimbursement']
    amazon_shipping_reimbursement: float = Field(validation_alias="amazonShippingReimbursement")
    # 收入 - 亚马逊安全运输计划补偿金额 [原字段 'safeTReimbursement']
    safe_t_reimbursement: float = Field(validation_alias="safeTReimbursement")
    # 收入 - 其他补偿/赔付金额 [原字段 'reimbursements']
    other_reimbursement: float = Field(validation_alias="reimbursements")
    # 收入 - 积分发放金额 (日本站) [原字段 'costOfPoIntegersGranted']
    points_granted: float = Field(validation_alias="costOfPoIntegersGranted")
    # 收入 - 积分退还金额 (日本站) [原字段 'costOfPoIntegersReturned']
    points_returned: float = Field(validation_alias="costOfPoIntegersReturned")
    # 收入 - 积分调整金额 (日本站) [原字段 'pointsAdjusted']
    points_adjusted: float = Field(validation_alias="pointsAdjusted")
    # 收入 - 货到付款金额 (COD) [原字段 'cashOnDelivery']
    cash_on_delivery: float = Field(validation_alias="cashOnDelivery")
    # 收入 - VAT进项税费金额 [原字段 'sharedComminglingVatIncome']
    commingling_vat_income: float = Field(validation_alias="sharedComminglingVatIncome")
    # 收入 - NetCo混合网络交易金额 [原字段 'netcoTransaction']
    netco_transaction: float = Field(validation_alias="netcoTransaction")
    # 收入 - TDS 194-O净额 (印度站) [原字段 'tdsSection194ONet']
    tds_section_194o_net: float = Field(validation_alias="tdsSection194ONet")
    # 收入 - 收回/冲回金额
    clawbacks: float
    # 收入 - 其他收入金额 [原字段 'otherInAmount']
    other_income: float = Field(validation_alias="otherInAmount")
    # 支出 - FBA销售佣金 (Referral Fee) [原字段 'platformFee']
    fba_selling_fees: float = Field(validation_alias="platformFee")
    # 支出 - FBA销售佣金退款金额 [原字段 'sellingFeeRefunds']
    fba_selling_fee_refunds: float = Field(validation_alias="sellingFeeRefunds")
    # 支出 - FBA交易费用 [原字段 'totalFbaDeliveryFee'] 
    # (fba_fulfillment_fees 到 fba_transaction_return_fees_alloc 之间所有费用)
    fba_transaction_fees: float = Field(validation_alias="totalFbaDeliveryFee")
    # 支出 - FBA配送费用 (Fulfillment Fee) [原字段 'fbaDeliveryFee']
    fba_fulfillment_fees: float = Field(validation_alias="fbaDeliveryFee")
    # 支出 - FBA多渠道配送费用 (Multi-Channel) [原字段 'mcFbaDeliveryFee']
    fba_mcf_fulfillment_fees: float = Field(validation_alias="mcFbaDeliveryFee")
    # 支出 - FBA多渠道配送费用 (分摊) [原字段 'sharedMcFbaFulfillmentFees']
    fba_mcf_fulfillment_fees_alloc: FloatOrNone2Zero = Field(0.0, validation_alias="sharedMcFbaFulfillmentFees")
    # 支出 - FBA多渠道配送数量 (Multi-Channel) [原字段 'mcFbaFulfillmentFeesQuantity']
    fba_mcf_fulfillment_qty: int = Field(validation_alias="mcFbaFulfillmentFeesQuantity")
    # 支出 - FBA客户退货处理费用 (分摊) [原字段 'sharedFbaCustomerReturnFee']
    fba_customer_return_fees_alloc: float = Field(validation_alias="sharedFbaCustomerReturnFee")
    # 支出 - FBA交易退货处理费用 (分摊) [原字段 'sharedFbaTransactionCustomerReturnFee']
    fba_transaction_return_fees_alloc: float = Field(validation_alias="sharedFbaTransactionCustomerReturnFee")
    # 支出 - FBA总配送费用退款金额 [原字段 'fbaTransactionFeeRefunds']
    fba_transaction_fee_refunds: float = Field(validation_alias="fbaTransactionFeeRefunds")
    # 支出 - 其他交易费用 [原字段 'otherTransactionFees']
    other_transaction_fees: float = Field(validation_alias="otherTransactionFees")
    # 支出 - 其他交易费用退款金额 [原字段 'otherTransactionFeeRefunds']
    other_transaction_fee_refunds: float = Field(validation_alias="otherTransactionFeeRefunds")
    # 支出 - FBA仓储和入库服务总费用 [原字段 'totalStorageFee']
    fba_inventory_and_inbound_services_fees: float = Field(validation_alias="totalStorageFee")
    # ('fba_storage_fees' 到 'other_fba_inventory_fees_alloc' 之间的所有费用)
    # 支出 - FBA仓储费用 [原字段 'fbaStorageFee']
    fba_storage_fees: float = Field(validation_alias="fbaStorageFee")
    # 支出 - FBA仓储费用计提金额 [原字段 'fbaStorageFeeAccrual']
    fba_storage_fees_accr: float = Field(validation_alias="fbaStorageFeeAccrual")
    # 支出 - FBA仓储费用计提调整金额 [原字段 'fbaStorageFeeAccrualDifference']
    fba_storage_fees_accr_adj: float = Field(validation_alias="fbaStorageFeeAccrualDifference")
    # 支出 - FBA仓储费用 (分摊) [原字段 'sharedFbaStorageFee']
    fba_storage_fees_alloc: float = Field(validation_alias="sharedFbaStorageFee")
    # 支出 - FBA长期仓储费用 [原字段 'longTermStorageFee']
    fba_lt_storage_fees: float = Field(validation_alias="longTermStorageFee")
    # 支出 - FBA长期仓储费用计提金额 [原字段 'longTermStorageFeeAccrual']
    fba_lt_storage_fees_accr: float = Field(validation_alias="longTermStorageFeeAccrual")
    # 支出 - FBA长期仓储费用计提调整金额 [原字段 'longTermStorageFeeAccrualDifference']
    fba_lt_storage_fees_accr_adj: float = Field(validation_alias="longTermStorageFeeAccrualDifference")
    # 支出 - FBA长期仓储费用 (分摊) [原字段 'sharedLongTermStorageFee']
    fba_lt_storage_fees_alloc: float = Field(validation_alias="sharedLongTermStorageFee")
    # 支出 - FBA仓储超储费用 (分摊) [原字段 'sharedFbaOverageFee']
    fba_overage_fees_alloc: float = Field(validation_alias="sharedFbaOverageFee")
    # 支出 - FBA仓储续期费用 (分摊) [原字段 'sharedStorageRenewalBilling']
    fba_storage_renewal_fees_alloc: float = Field(validation_alias="sharedStorageRenewalBilling")
    # 支出 - FBA仓鼠销毁费用 (分摊) [原字段 'sharedFbaDisposalFee']
    fba_disposal_fees_alloc: float = Field(validation_alias="sharedFbaDisposalFee")
    # 支出 - FBA仓储销毁数量 [原字段 'disposalQuantity']
    fba_disposal_qty: int = Field(validation_alias="disposalQuantity")
    # 支出 - FBA仓储移除费用 (分摊) [原字段 'sharedFbaRemovalFee']
    fba_removal_fees_alloc: float = Field(validation_alias="sharedFbaRemovalFee")
    # 支出 - FBA仓储移除数量 [原字段 'removalQuantity']
    fba_removal_qty: int = Field(validation_alias="removalQuantity")
    # 支出 - FBA入库运输计划费用 (分摊) [原字段 'sharedFbaInboundTransportationProgramFee']
    fba_inbound_transportation_program_fees_alloc: float = Field(validation_alias="sharedFbaInboundTransportationProgramFee")
    # 支出 - FBA入库缺陷费用 (分摊) [原字段 'sharedFbaInboundDefectFee']
    fba_inbound_defect_fees_alloc: float = Field(validation_alias="sharedFbaInboundDefectFee")
    # 支出 - FBA国际入库费用 (分摊) [原字段 'sharedFbaIntegerernationalInboundFee']
    fba_international_inbound_fees_alloc: float = Field(validation_alias="sharedFbaIntegerernationalInboundFee")
    # 支出 - FBA合作承运商(入库)运费 (分摊) [原字段 'sharedAmazonPartneredCarrierShipmentFee']
    fba_partnered_carrier_shipment_fees_alloc: float = Field(validation_alias="sharedAmazonPartneredCarrierShipmentFee")
    # 支出 - FBA人工处理费用 (分摊) [原字段 'sharedManualProcessingFee']
    fba_manual_processing_fees_alloc: float = Field(validation_alias="sharedManualProcessingFee")
    # 支出 - AWD仓储费用 (分摊) [原字段 'sharedAwdStorageFee']
    awd_storage_fees_alloc: float = Field(validation_alias="sharedAwdStorageFee")
    # 支出 - AWD处理费用 (分摊) [原字段 'sharedAwdProcessingFee']
    awd_processing_fees_alloc: float = Field(validation_alias="sharedAwdProcessingFee")
    # 支出 - AWD运输费用 (分摊) [原字段 'sharedAwdTransportationFee']
    awd_transportation_fees_alloc: float = Field(validation_alias="sharedAwdTransportationFee")
    # 支出 - AWD卫星仓储费用 (分摊) [原字段 'sharedStarStorageFee']
    awd_satellite_storage_fees_alloc: float = Field(validation_alias="sharedStarStorageFee")
    # 支出 - FBA库存费用调整金额 (分摊) [原字段 'sharedItemFeeAdjustment'] 
    fba_inventory_fees_adj_alloc: float = Field(validation_alias="sharedItemFeeAdjustment")
    # 支出 - FBA其他库存费用 (分摊) [原字段 'sharedOtherFbaInventoryFees']
    other_fba_inventory_fees_alloc: float = Field(validation_alias="sharedOtherFbaInventoryFees")
    # 支出 - 运输标签花费金额 [原字段 'shippingLabelPurchases']
    shipping_label_purchases: float = Field(validation_alias="shippingLabelPurchases")
    # 支出 - FBA贴标费用 (分摊) [原字段 'sharedLabelingFee']
    fba_labeling_fees_alloc: float = Field(validation_alias="sharedLabelingFee")
    # 支出 - FBA塑封袋费用 (分摊) [原字段 'sharedPolybaggingFee']
    fba_polybagging_fees_alloc: float = Field(validation_alias="sharedPolybaggingFee")
    # 支出 - FBA气泡膜费用 (分摊) [原字段 'sharedBubblewrapFee']
    fba_bubblewrap_fees_alloc: float = Field(validation_alias="sharedBubblewrapFee")
    # 支出 - FBA封箱胶带费用 (分摊) [原字段 'sharedTapingFee']
    fba_taping_fees_alloc: float = Field(validation_alias="sharedTapingFee")
    # 支出 - FBM邮寄资费 (分摊) [原字段 'sharedMfnPostageFee']
    mfn_postage_fees_alloc: float = Field(validation_alias="sharedMfnPostageFee")
    # 支出 - 运输标签退款金额 [原字段 'shippingLabelRefunds']
    shipping_label_refunds: float = Field(validation_alias="shippingLabelRefunds")
    # 支出 - 承运商运输标签花费调整金额 [原字段 'sharedCarrierShippingLabelAdjustments']
    carrier_shipping_label_adj: float = Field(validation_alias="sharedCarrierShippingLabelAdjustments")
    # 支出 - 总推广费用 (Service Fee) [原字段 'promotionFee']
    # (subscription_fees_alloc 到 early_reviewer_program_fees_alloc 之间的所有费用)
    promotion_fees: float = Field(validation_alias="promotionFee")
    # 支出 - 订阅服务费 (分摊) [原字段 'sharedSubscriptionFee']
    subscription_fees_alloc: float = Field(validation_alias="sharedSubscriptionFee")
    # 支出 - 优惠券费用 (分摊) [原字段 'sharedCouponFee']
    coupon_fees_alloc: float = Field(validation_alias="sharedCouponFee")
    # 支出 - 秒杀费用 (分摊) [原字段 'sharedLdFee']
    deal_fees_alloc: float = Field(validation_alias="sharedLdFee")
    # 支出 - Vine费用 (分摊) [原字段 'sharedVineFee']
    vine_fees_alloc: float = Field(validation_alias="sharedVineFee")
    # 支出 - 早期评论人计划费用 (分摊) [原字段 'sharedEarlyReviewerProgramFee']
    early_reviewer_program_fees_alloc: float = Field(validation_alias="sharedEarlyReviewerProgramFee")
    # 支出 - FBA入库便利费用 (Service Fee/分摊) [原字段 'sharedFbaInboundConvenienceFee']
    fba_inbound_convenience_fees_alloc: float = Field(validation_alias="sharedFbaInboundConvenienceFee")
    # 支出 - 其他亚马逊服务费用 (分摊) [原字段 'sharedOtherServiceFees']
    other_service_fees_alloc: float = Field(validation_alias="sharedOtherServiceFees")
    # 支出 - 亚马逊退款管理费用 [原字段 'refundAdministrationFees']
    refund_administration_fees: float = Field(validation_alias="refundAdministrationFees")
    # 支出 - 总费用退款金额 [totalFeeRefunds]
    # (fba_selling_fee_refunds + fba_transaction_fee_refunds + refund_administration_fees)
    total_fee_refunds: float = Field(validation_alias="totalFeeRefunds")
    # 支出 - 其他费用调整金额
    adjustments: float
    # 支出 - 广告总花费 (Cost of Advertising) [原字段 'totalAdsCost']
    # (ads_sp_cost + ads_sb_cost + ads_sbv_cost + ads_sd_cost + ads_cost_alloc + 
    #  ads_amazon_live_cost_alloc + ads_creator_connections_cost_alloc + 
    #  ads_sponsored_tv_cost_alloc + ads_retail_ad_service_alloc)
    ads_cost: float = Field(validation_alias="totalAdsCost")
    # 支出 - 广告总销售金额 [原字段 'totalAdsSales']
    ads_sales: float = Field(validation_alias="totalAdsSales")
    # 支出 - 广告总销售数量 [原字段 'totalAdsSalesQuantity']
    ads_sales_qty: int = Field(validation_alias="totalAdsSalesQuantity")
    # 支出 - SP广告花费 (Sponsored Products) [原字段 'adsSpCost']
    ads_sp_cost: float = Field(validation_alias="adsSpCost")
    # 支出 - SP广告销售金额 [原字段 'adsSpSales']
    ads_sp_sales: float = Field(validation_alias="adsSpSales")
    # 支出 - SP广告销售数量 [原字段 'adsSpSalesQuantity']
    ads_sp_sales_qty: int = Field(validation_alias="adsSpSalesQuantity")
    # 支出 - SB广告花费 (Sponsored Brands) [原字段 'adsSbCost']
    ads_sb_cost: float = Field(validation_alias="adsSbCost")
    # 支出 - SB广告销售金额 [原字段 'sharedAdsSbSales']
    ads_sb_sales: float = Field(validation_alias="sharedAdsSbSales")
    # 支出 - SB广告销售数量 [原字段 'sharedAdsSbSalesQuantity']
    ads_sb_sales_qty: int = Field(validation_alias="sharedAdsSbSalesQuantity")
    # 支出 - SBV广告花费 (Sponsored Brands Video) [原字段 'adsSbvCost']
    ads_sbv_cost: float = Field(validation_alias="adsSbvCost")
    # 支出 - SBV广告销售金额 [原字段 'sharedAdsSbvSales']
    ads_sbv_sales: float = Field(validation_alias="sharedAdsSbvSales")
    # 支出 - SBV广告销售数量 [原字段 'sharedAdsSbvSalesQuantity']
    ads_sbv_sales_qty: int = Field(validation_alias="sharedAdsSbvSalesQuantity")
    # 支出 - SD广告花费 (Sponsored Display) [原字段 'adsSdCost']
    ads_sd_cost: float = Field(validation_alias="adsSdCost")
    # 支出 - SD广告销售金额 [原字段 'adsSdSales']
    ads_sd_sales: float = Field(validation_alias="adsSdSales")
    # 支出 - SD广告销售数量 [原字段 'adsSdSalesQuantity']
    ads_sd_sales_qty: int = Field(validation_alias="adsSdSalesQuantity")
    # 支出 - 广告分摊费用 [原字段 'sharedCostOfAdvertising']
    ads_cost_alloc: float = Field(validation_alias="sharedCostOfAdvertising")
    # 支出 - Live广告花费 (分摊) [原字段 'sharedAdsAlCost']
    ads_amazon_live_cost_alloc: FloatOrNone2Zero = Field(validation_alias="sharedAdsAlCost")
    # 支出 - 内容创作者计划花费 (分摊) [原字段 'sharedAdsCcCost']
    ads_creator_connections_cost_alloc: FloatOrNone2Zero = Field(validation_alias="sharedAdsCcCost")
    # 支出 - TV广告花费 (分摊) [原字段 'sharedAdsSspaotCost']
    ads_sponsored_tv_cost_alloc: FloatOrNone2Zero = Field(validation_alias="sharedAdsSspaotCost")
    # 支出 - 零售商赞助广告花费 (分摊) [原字段 'sharedAdsSarCost']
    ads_retail_ad_service_alloc: FloatOrNone2Zero = Field(validation_alias="sharedAdsSarCost")
    # 支出 - 广告总退款金额 (Refund for Advertiser) [原字段 'refundForAdvertiser']
    ads_cost_refunds: float = Field(validation_alias="refundForAdvertiser")
    # 支出 - 清算服务费 (分摊) [原字段 'sharedLiquidationsFees']
    liquidation_service_fees_alloc: float = Field(validation_alias="sharedLiquidationsFees")
    # 支出 - 应收账款扣减 (分摊) [原字段 'sharedReceivablesDeductions']
    receivables_deductions_alloc: float = Field(validation_alias="sharedReceivablesDeductions")
    # 支出 - 亚马逊运费调整 (分摊) [原字段 'sharedAmazonShippingChargeAdjustments']
    amazon_shipping_charge_adj_alloc: float = Field(validation_alias="sharedAmazonShippingChargeAdjustments")
    # 支出 - VAT销项税费金额 [原字段 'sharedComminglingVatExpenses']
    commingling_vat_expenses: float = Field(validation_alias="sharedComminglingVatExpenses")
    # 支出 - 其他支出费用 [原字段 'others']
    other_expenses: float = Field(validation_alias="others")
    # 支出 - 用户自定义推广总费用 [原字段 'customOrderFee']
    user_promotion_fees: float = Field(validation_alias="customOrderFee")
    # (user_promotion_principal + user_promotion_commission)
    # 支出 - 用户自定义推广费用本金 [原字段 'customOrderFeePrincipal']
    user_promotion_principal: float = Field(validation_alias="customOrderFeePrincipal")
    # 支出 - 用户自定义推广佣金费用 [原字段 'customOrderFeeCommission']
    user_promotion_commission: float = Field(validation_alias="customOrderFeeCommission")
    # 支出 - 用户自定义其他费用 [原字段 'otherFeeStr']
    user_other_fees: list[UserOtherFee] = Field(validation_alias="otherFeeStr")
    # 税费 - 总税费 [grossProfitTax]
    total_tax: FloatOrNone2Zero = Field(validation_alias="grossProfitTax")
    # 税费 - 总销税收金额 [原字段 'totalSalesTax']
    # ('product_tax_collected' 到 'tcs_cgst_collected' 之间的所有税费)
    sales_tax_collected: float = Field(validation_alias="totalSalesTax")
    # 税费 - 商品销售税收金额 [原字段 'taxCollectedProduct']
    product_tax_collected: float = Field(validation_alias="taxCollectedProduct")
    # 税费 - 配送运费税收金额 [原字段 'taxCollectedShipping']
    shipping_tax_collected: float = Field(validation_alias="taxCollectedShipping")
    # 税费 - 礼品包装税收金额 [原字段 'taxCollectedGiftWrap']
    giftwrap_tax_collected: float = Field(validation_alias="taxCollectedGiftWrap")
    # 税费 - 促销折扣税收金额 [原字段 'taxCollectedDiscount']
    promotional_rebate_tax_collected: float = Field(validation_alias="taxCollectedDiscount")
    # 税费 - VAT/GST税收金额 [原字段 'taxCollected']
    vat_gst_tax_collected: float = Field(validation_alias="taxCollected")
    # 税费 - TCS IGST税收金额 (印度站) [原字段 'tcsIgstCollected']
    tcs_igst_collected: float = Field(validation_alias="tcsIgstCollected")
    # 税费 - TCS SGST税收金额 (印度站) [原字段 'tcsSgstCollected']
    tcs_sgst_collected: float = Field(validation_alias="tcsSgstCollected")
    # 税费 - TCS CGST税收金额 (印度站) [原字段 'tcsCgstCollected']
    tcs_cgst_collected: float = Field(validation_alias="tcsCgstCollected")
    # 税费 - 总销售税代扣金额 [原字段 'salesTaxWithheld']
    sales_tax_withheld: float = Field(validation_alias="salesTaxWithheld")
    # 税费 - 总销售税费退款 [salesTaxRefund]
    sales_tax_refunded: float = Field(validation_alias="salesTaxRefund")
    # ('product_tax_refunded' 到 'sales_tax_withheld_refunded' 之间的所有税费退款)
    # 税费 - 商品销售税费退款金额 [原字段 'taxRefundedProduct']
    product_tax_refunded: float = Field(validation_alias="taxRefundedProduct")
    # 税费 - 配送运费税费退款金额 [原字段 'taxRefundedShipping']
    shipping_tax_refunded: float = Field(validation_alias="taxRefundedShipping")
    # 税费 - 礼品包装税费退款金额 [原字段 'taxRefundedGiftWrap']
    giftwrap_tax_refunded: float = Field(validation_alias="taxRefundedGiftWrap")
    # 税费 - 促销折扣税费退款金额 [原字段 'taxRefundedDiscount']
    promotional_rebate_tax_refunded: float = Field(validation_alias="taxRefundedDiscount")
    # 税费 - VAT/GST税费退款金额 [原字段 'taxRefunded']
    vat_gst_tax_refunded: float = Field(validation_alias="taxRefunded")
    # 税费 - TCS IGST税费退款金额 (印度站) [原字段 'tcsIgstRefunded']
    tcs_igst_refunded: float = Field(validation_alias="tcsIgstRefunded")
    # 税费 - TCS SGST税费退款金额 (印度站) [原字段 'tcsSgstRefunded']
    tcs_sgst_refunded: float = Field(validation_alias="tcsSgstRefunded")
    # 税费 - TCS CGST税费退款金额 (印度站) [原字段 'tcsCgstRefunded']
    tcs_cgst_refunded: float = Field(validation_alias="tcsCgstRefunded")
    # 税费 - 总退款税代扣金额 [原字段 'refundTaxWithheld']
    refund_tax_withheld: float = Field(validation_alias="refundTaxWithheld")
    # 税费 - 其他税费调整 (分摊) [原字段 'sharedTaxAdjustment']
    other_tax_adj_alloc: float = Field(validation_alias="sharedTaxAdjustment")
    # 成本 - 总退款数量 [原字段 'refundsQuantity']
    total_refunds_qty: int = Field(validation_alias="refundsQuantity")
    # 成本 - 总退款率 [原字段 'refundsRate']
    # (total_refund_qty / (fba&fbm_product_sales_qty + fba_mcf_fulfillment_qty + fba_reshipment_qty))
    total_refunds_rate: float = Field(validation_alias="refundsRate")
    # 成本 - FBA退货数量 [原字段 'fbaReturnsQuantity']
    fba_returns_qty: int = Field(validation_alias="fbaReturnsQuantity")
    # 成本 - FBA退货可售数量 [原字段 'fbaReturnsSaleableQuantity']
    fba_returns_saleable_qty: int = Field(validation_alias="fbaReturnsSaleableQuantity")
    # 成本 - FBA退货不可售数量 [原字段 'fbaReturnsUnsaleableQuantity']
    fba_returns_unsaleable_qty: int = Field(validation_alias="fbaReturnsUnsaleableQuantity")
    # 成本 - FBA退货率 [原字段 'fbaReturnsQuantityRate']
    # (fba_returns_qty / (fba_product_sales_qty + fba_mcf_fulfillment_qty))
    fba_returns_rate: float = Field(validation_alias="fbaReturnsQuantityRate")
    # 成本 - 总补发/换货数量 [原字段 'totalReshipQuantity']
    total_reshipment_qty: int = Field(validation_alias="totalReshipQuantity")
    # 成本 - FBA补发/换货数量 [原字段 'reshipFbaProductSalesQuantity']
    fba_reshipment_qty: int = Field(validation_alias="reshipFbaProductSalesQuantity")
    # 成本 - FBA换货退回数量 [原字段 'reshipFbaProductSaleRefundsQuantity']
    fba_reshipment_returned_qty: int = Field(validation_alias="reshipFbaProductSaleRefundsQuantity")
    # 成本 - FBM补发/换货数量 [原字段 'reshipFbmProductSalesQuantity']
    fbm_reshipment_qty: int = Field(validation_alias="reshipFbmProductSalesQuantity")
    # 成本 - FBM换货退回数量 [原字段 'reshipFbmProductSaleRefundsQuantity']
    fbm_reshipment_returned_qty: int = Field(validation_alias="reshipFbmProductSaleRefundsQuantity")
    # 成本 - 总成本数量 [原字段 'cgQuantity']
    # (fba&fbm_product_sales_qty + fba_mcf_fulfillment_qty + fba&fbm_reshipment_qty - fba_returns_saleable_qty)
    cost_of_goods_qty: IntOrNone2Zero = Field(validation_alias="cgQuantity")
    # 成本 - 重成本数量绝对值 [原字段 'cgAbsQuantity']
    cost_of_goods_abs_qty: int = Field(validation_alias="cgAbsQuantity")
    # 成本 - 总成本金额 (COGS) [原字段 'totalCost']
    # (purchase_cost + logistics_cost + other_costs)
    cost_of_goods: float = Field(validation_alias="totalCost")
    # 成本 - 总成本占比 [原字段 'proportionOfTotalCost']
    cost_of_goods_ratio: float = Field(validation_alias="proportionOfTotalCost")
    # 成本 - 总采购成本 (COGS) [原字段 'cgPriceTotal']
    purchase_cost: float = Field(validation_alias="cgPriceTotal")
    # 成本 - 总采购绝对成本 [原字段 'cgPriceAbsTotal']
    purchase_abs_cost: float = Field(validation_alias="cgPriceAbsTotal")
    # 成本 - 单品成本 [原字段 'cgUnitPrice']
    purchase_unit_cost: float = Field(validation_alias="cgUnitPrice")
    # 成本 - 采购成本占比 [原字段 'proportionOfCg']
    purchase_cost_ratio: float = Field(validation_alias="proportionOfCg")
    # 成本 - 是否有成本明细 [原字段 'hasCgPriceDetail']
    has_purchase_cost_detail: int = Field(validation_alias="hasCgPriceDetail")
    # 成本 - 总物流费用 [原字段 'cgTransportCostsTotal']
    logistics_cost: float = Field(validation_alias="cgTransportCostsTotal")
    # 成本 - 物流单品费用 [原字段 'cgTransportUnitCosts']
    logistics_unit_cost: float = Field(validation_alias="cgTransportUnitCosts")
    # 成本 - 物流费用占比 [原字段 'proportionOfCgTransport']
    logistics_cost_ratio: float = Field(validation_alias="proportionOfCgTransport")
    # 成本 - 是否有物流费用明细 [原字段 'hasCgTransportCostsDetail']
    has_logistics_cost_detail: int = Field(validation_alias="hasCgTransportCostsDetail")
    # 成本 - 其他费用总金额 [原字段 'cgOtherCostsTotal']
    other_costs: float = Field(validation_alias="cgOtherCostsTotal")
    # 成本 - 其他费用单品金额 [原字段 'cgOtherUnitCosts']
    other_unit_cost: float = Field(validation_alias="cgOtherUnitCosts")
    # 成本 - 其他费用占比 [原字段 'proportionOfCgOtherCosts']
    other_cost_ratio: float = Field(validation_alias="proportionOfCgOtherCosts")
    # 成本 - 是否有其他费用明细 [原字段 'hasCgOtherCostsDetail']
    has_other_cost_detail: int = Field(validation_alias="hasCgOtherCostsDetail")
    # 利润 - 毛利润 [原字段 'grossProfit']
    gross_profit: float = Field(validation_alias="grossProfit")
    # 利润 - 毛利率 [原字段 'grossRate']
    gross_profit_margin: float = Field(validation_alias="grossRate")
    # 利润 - 投资回报率 (ROI)
    roi: float
    # 交易状态 [原字段 'transactionStatusCode']
    transaction_status: str = Field(validation_alias="transactionStatusCode")
    # 交易状态描述 [原字段 'transactionStatus']
    transaction_status_desc: str = Field(validation_alias="transactionStatus")
    # 延迟结算状态 [原字段 'deferredSubStatusCode']
    deferred_settlement_status: str = Field(validation_alias="deferredSubStatusCode")
    # 延迟结算状态描述 [原字段 'deferredSubStatus']
    deferred_settlement_status_desc: str = Field(validation_alias="deferredSubStatus")
    # 延迟结算总金额 [原字段 'deferredSettlementAmount']
    deferred_settlement: float = Field(0.0, validation_alias="deferredSettlementAmount")
    # 结算小计 [原字段 'settlementSubtotal']
    settlement_subtotal: float = Field(0.0, validation_alias="settlementSubtotal")
    # 报告时间 (本地时间) [原字段 'postedDateDayLocale']
    report_time_loc: StrOrNone2Blank = Field(validation_alias="postedDateDayLocale")
    # 报告开始时间 (本地时间) [原字段 'minPostedDateDayLocale']
    report_start_time_loc: StrOrNone2Blank = Field(validation_alias="minPostedDateDayLocale")
    # 报告结束时间 (本地时间) [原字段 'maxPostedDateDayLocale']
    report_end_time_loc: StrOrNone2Blank = Field(validation_alias="maxPostedDateDayLocale")
    # 报告日期 (本地时间) [原字段 'postedDateLocale']
    report_date_loc: str = Field(validation_alias="postedDateLocale")
    # fmt: on

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("user_other_fees", mode="before")
    @classmethod
    def _validate_user_other_fees(cls, v):
        if v is None:
            return []
        return [UserOtherFee.model_validate(i) for i in v]


# . Income Statement Sellers
class IncomeStatementSeller(IncomeStatement):
    """损益报告-店铺维度"""

    # 领星店铺ID
    sid: int
    # 领星店铺名称 [原字段 'storeName']
    seller_name: str = Field(validation_alias="storeName")
    # 国家 (中文)
    country: str
    # 国家代码 [原字段 'countryCode']
    country_code: str = Field(validation_alias="countryCode")
    # 店铺负责人名称 (逗号隔开) [原字段 'sellerPrincipalRealname']
    operator_names: StrOrNone2Blank = Field(validation_alias="sellerPrincipalRealname")


class IncomeStatementSellers(ResponseV1, FlattenDataRecords):
    """损益报告-店铺维度列表"""

    data: list[IncomeStatementSeller]


# . Income Statement Asins
class IncomeStatementAsin(IncomeStatement):
    """损益报告-商品维度明细"""

    # 记录ID (非业务唯一键)
    id: str
    # 领星店铺ID
    sid: int
    # 国家代码 [原字段 'countryCode']
    country_code: str = Field(validation_alias="countryCode")
    # ASIN关联领星店铺ID列表
    sids: list[int]
    # ASIN关联领星店铺名称列表 [原字段 'storeName']
    seller_names: list[str] = Field(validation_alias="storeName")
    # ASIN关联国家列表 (中文) [原字段 'country']
    countries: list[str] = Field(validation_alias="country")
    # 商品ASIN
    asin: str
    # 商品父ASIN [原字段 'parentAsin']
    parent_asin: str = Field(validation_alias="parentAsin")
    # 关联的ASIN列表 [原字段 'asins']
    asins: list[str]
    # 领星本地SKU [原字段 'localSku']
    lsku: StrOrNone2Blank = Field(validation_alias="localSku")
    # 领星本地商品名称 [原字段 'localName']
    product_name: StrOrNone2Blank = Field(validation_alias="localName")
    # 产品型号 [原字段 'model']
    product_model: StrOrNone2Blank = Field(validation_alias="model")
    # 领星本地产品分类名称 [原字段 'categoryName']
    category_name: StrOrNone2Blank = Field(validation_alias="categoryName")
    # 领星本地产品品牌名称 [原字段 'brandName']
    brand_name: StrOrNone2Blank = Field(validation_alias="brandName")
    # 标题 [原字段 'itemName']
    title: StrOrNone2Blank = Field(validation_alias="itemName")
    # 商品略缩图链接 [原字段 'smallImageUrl']
    thumbnail_url: StrOrNone2Blank = Field(validation_alias="smallImageUrl")
    # ASIN开发人名称 [原字段 'productDeveloperRealname']
    developer_name: StrOrNone2Blank = Field(validation_alias="productDeveloperRealname")
    # ASIN负责人名称 (逗号隔开) [原字段 'principalRealname']
    operator_names: StrOrNone2Blank = Field(validation_alias="principalRealname")
    # 商品标签IDs (逗号隔开) [原字段 'listingTagIds']
    tag_ids: StrOrNone2Blank = Field(validation_alias="listingTagIds")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("sids", "asins", mode="before")
    @classmethod
    def _validate_sids(cls, v: str) -> list[str]:
        return v.split(",")

    @field_validator("seller_names", "countries", mode="before")
    @classmethod
    def _validate_seller_names(cls, v) -> list[str]:
        return [v] if isinstance(v, str) else v


class IncomeStatementAsins(ResponseV1, FlattenDataRecords):
    """损益报告-商品维度列表"""

    data: list[IncomeStatementAsin]


# . Income Statement Mskus
class IncomeStatementMsku(IncomeStatement):
    """损益报告-亚马逊SKU维度明细"""

    # 记录ID (非业务唯一键)
    id: str
    # 领星店铺ID
    sid: int
    # 领星店铺名称 [原字段 'storeName']
    seller_name: str = Field(validation_alias="storeName")
    # 国家 (中文)
    country: str
    # 国家代码 [原字段 'countryCode']
    country_code: str = Field(validation_alias="countryCode")
    # 商品ASIN
    asin: str
    # 商品父ASIN [原字段 'parentAsin']
    parent_asin: str = Field(validation_alias="parentAsin")
    # 亚马逊SKU
    msku: str
    # 领星本地SKU [原字段 'localSku']
    lsku: StrOrNone2Blank = Field(validation_alias="localSku")
    # 领星本地商品名称 [原字段 'localName']
    product_name: StrOrNone2Blank = Field(validation_alias="localName")
    # 产品型号 [原字段 'model']
    product_model: StrOrNone2Blank = Field(validation_alias="model")
    # 领星本地产品分类名称 [原字段 'categoryName']
    category_name: StrOrNone2Blank = Field(validation_alias="categoryName")
    # 领星本地产品品牌名称 [原字段 'brandName']
    brand_name: StrOrNone2Blank = Field(validation_alias="brandName")
    # 标题 [原字段 'itemName']
    title: StrOrNone2Blank = Field(validation_alias="itemName")
    # 商品略缩图链接 [原字段 'smallImageUrl']
    thumbnail_url: StrOrNone2Blank = Field(validation_alias="smallImageUrl")
    # ASIN开发人名称 [原字段 'productDeveloperRealname']
    developer_name: StrOrNone2Blank = Field(validation_alias="productDeveloperRealname")
    # ASIN负责人名称 (逗号隔开) [原字段 'principalRealname']
    operator_names: StrOrNone2Blank = Field(validation_alias="principalRealname")
    # 商品标签IDs (逗号隔开) [原字段 'listingTagIds']
    tag_ids: StrOrNone2Blank = Field(validation_alias="listingTagIds")


class IncomeStatementMskus(ResponseV1, FlattenDataRecords):
    """损益报告-亚马逊SKU维度列表"""

    data: list[IncomeStatementMsku]


# . Income Statement Lskus
class IncomeStatementLsku(IncomeStatement):
    """损益报告-领星本地SKU维度明细"""

    # 记录ID (非业务唯一键)
    id: str
    # 领星店铺ID列表
    sids: list[int]
    # 领星店铺名称列表 [原字段 'storeName']
    seller_names: list[str] = Field(validation_alias="storeName")
    # 国家列表 (中文) [原字段 'country']
    countries: list[str] = Field(validation_alias="country")
    # 国家代码列表 [原字段 'countryCode']
    country_codes: list[str] = Field(validation_alias="countryCode")
    # 关联的ASIN列表 [原字段 'asins']
    asins: list[str] = Field(validation_alias="asins")
    # 领星本地SKU [原字段 'localSku']
    lsku: str = Field(validation_alias="localSku")
    # 领星本地商品ID [原字段 'pid']
    product_id: int = Field(validation_alias="pid")
    # 领星本地商品名称 [原字段 'localName']
    product_name: StrOrNone2Blank = Field(validation_alias="localName")
    # 产品型号 [原字段 'model']
    product_model: StrOrNone2Blank = Field(validation_alias="model")
    # 领星本地产品分类名称 [原字段 'categoryName']
    category_name: StrOrNone2Blank = Field(validation_alias="categoryName")
    # 领星本地产品品牌名称 [原字段 'brandName']
    brand_name: StrOrNone2Blank = Field(validation_alias="brandName")
    # 标题 [原字段 'itemName']
    title: StrOrNone2Blank = Field(validation_alias="itemName")
    # 商品略缩图链接 [原字段 'smallImageUrl']
    thumbnail_url: StrOrNone2Blank = Field(validation_alias="smallImageUrl")
    # ASIN开发人名称 [原字段 'productDeveloperRealname']
    developer_name: StrOrNone2Blank = Field(validation_alias="productDeveloperRealname")
    # ASIN负责人名称 (逗号隔开) [原字段 'principalRealname']
    operator_names: StrOrNone2Blank = Field(validation_alias="principalRealname")
    # 商品标签IDs (逗号隔开) [原字段 'listingTagIds']
    tag_ids: StrOrNone2Blank = Field(validation_alias="listingTagIds")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("sids", "asins", mode="before")
    @classmethod
    def _validate_sids(cls, v: str) -> list[str]:
        return v.split(",")

    @field_validator("seller_names", "countries", "country_codes", mode="before")
    @classmethod
    def _validate_seller_names(cls, v) -> list[str]:
        return [v] if isinstance(v, str) else v


class IncomeStatementLskus(ResponseV1, FlattenDataRecords):
    """损益报告-领星本地SKU维度列表"""

    data: list[IncomeStatementLsku]
