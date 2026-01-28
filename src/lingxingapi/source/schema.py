# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from lingxingapi.base.schema import ResponseV1, FlattenDataList
from lingxingapi.fields import IntOrNone2Zero, FloatOrNone2Zero, StrOrNone2Blank


# 订单数据 -----------------------------------------------------------------------------------------------------------------------
# . Orders
class Order(BaseModel):
    """亚马逊源订单"""

    # fmt: off
    # 领星店铺ID
    sid: int
    # 亚马逊订单编号
    amazon_order_id: str
    # 卖家提供的订单编号
    merchant_order_id: str
    # 配送方式 ("Amazon" [AFN] 或 "Merchant" [MFN])
    fulfillment_channel: str
    # 销售渠道 (如: "Amazon.com")
    sales_channel: str
    # 销售子渠道 (CBA/WBA) [原字段 'order_channel']
    sales_sub_channel: str = Field(validation_alias="order_channel")
    # 订单配送服务级别 [原字段 'ship_service_level']
    shipment_service: str = Field(validation_alias="ship_service_level")
    # 是否为B2B订单 [原字段 'is_business_order']
    is_b2b_order: str = Field(validation_alias="is_business_order")
    # 订单状态
    order_status: str
    # 订单商品状态 [原字段 'item_status']
    order_item_status: str = Field(validation_alias="item_status")
    # 领星产品ID [原字段 'pid']
    product_id: int = Field(validation_alias="pid")
    # 领星产品名称 [原字段 'local_name']
    product_name: str = Field(validation_alias="local_name")
    # 商品ASIN
    asin: str
    # 亚马逊SKU [原字段 'sku']
    msku: str = Field(validation_alias="sku")
    # 本地SKU [原字段 'local_sku']
    lsku: str = Field(validation_alias="local_sku")
    # 商品标题 [原字段 'product_name']
    title: str = Field(validation_alias="product_name")
    # ASIN链接 [原字段 'url']
    asin_url: str = Field(validation_alias="url")
    # 商品促销标识 [原字段 'promotion_ids']
    promotion_labels: str = Field(validation_alias="promotion_ids")
    # 订单商品总数量 [原字段 'quantity']
    order_qty: int = Field(validation_alias="quantity")
    # 商品销售金额 [原字段 'item_price']
    sales_amt: FloatOrNone2Zero = Field(validation_alias="item_price")
    # 商品销售金额税费 [原字段 'item_tax']
    sales_tax_amt: FloatOrNone2Zero = Field(validation_alias="item_tax")
    # 买家支付运费金额 [原字段 'shipping_price']
    shipping_credits_amt: FloatOrNone2Zero = Field(validation_alias="shipping_price")
    # 买家支付运费税费 [原字段 'shipping_tax']
    shipping_credits_tax_amt: FloatOrNone2Zero = Field(validation_alias="shipping_tax")
    # 买家支付礼品包装费金额 [原字段 'gift_wrap_price']
    giftwrap_credits_amt: FloatOrNone2Zero = Field(validation_alias="gift_wrap_price")
    # 买家支付礼品包装费税费 [原字段 'gift_wrap_tax']
    giftwrap_credits_tax_amt: FloatOrNone2Zero = Field(validation_alias="gift_wrap_tax")
    # 卖家商品促销折扣金额 [原字段 'item_promotion_discount']
    promotion_discount_amt: FloatOrNone2Zero = Field(validation_alias="item_promotion_discount")
    # 卖家商品运费折扣金额 [原字段 'ship_promotion_discount']
    shipping_discount_amt: FloatOrNone2Zero = Field(validation_alias="ship_promotion_discount")
    # 货币代码 [原字段 'currency']
    currency_code: str = Field(validation_alias="currency")
    # 买家国家代码 [原字段 'ship_country']
    buyer_country_code: str = Field(validation_alias="ship_country")
    # 买家州/省 [原字段 'ship_state']
    buyer_state: str = Field(validation_alias="ship_state")
    # 买家城市 [原字段 'ship_city']
    buyer_city: str = Field(validation_alias="ship_city")
    # 买家邮编 [原字段 'ship_postal_code']
    buyer_postcode: str = Field(validation_alias="ship_postal_code")
    # 订单购买时间 (UTC时间) [原字段 'purchase_date']
    purchase_time_utc: str = Field(validation_alias="purchase_date")
    # 订单购买时间 (本地时间) [原字段 'purchase_date_local']
    purchase_time_loc: str = Field(validation_alias="purchase_date_local")
    # 订单购买日期 (本地日期) [原字段 'purchase_date_locale']
    purchase_date_loc: str = Field(validation_alias="purchase_date_locale")
    # 订单发货时间 (本地时间) [原字段 'shipment_date']
    shipment_time_loc: str = Field(validation_alias="shipment_date")
    # 订单更新时间 (时间戳) [原字段 'last_updated_time']
    update_time_ts: int = Field(validation_alias="last_updated_time")
    # fmt: on


class Orders(ResponseV1):
    """亚马逊所有类型(FBA & FBM)的源订单列表"""

    data: list[Order]


# . FBA Orders
class FbaOrder(BaseModel):
    """亚马逊FBA源订单"""

    # fmt: off
    # 亚马逊订单编号
    amazon_order_id: str
    # 亚马逊订单商品编号
    amazon_order_item_id: str
    # 配送方式 (AFN 或 MFN)
    fulfillment_channel: str
    # 亚马逊货件编号
    shipment_id: str
    # 亚马逊货件商品编号
    shipment_item_id: str
    # 订单配送服务级别 [原字段 'ship_service_level']
    shipment_service: str = Field(validation_alias="ship_service_level")
    # 承运商代码 [原字段 'carrier']
    shipment_carrier: str = Field(validation_alias="carrier")
    # 追踪单号
    tracking_number: str
    # 亚马逊SKU [原字段 'sku']
    msku: str = Field(validation_alias="sku")
    # 商品标题 [原字段 'product_name']
    title: str = Field(validation_alias="product_name")
    # 发货商品数量 [原字段 'quantity_shipped']
    shipped_qty: int = Field(validation_alias="quantity_shipped")
    # 商品销售金额 [原字段 'item_price']
    sales_amt: FloatOrNone2Zero = Field(validation_alias="item_price")
    # 商品销售金额税费 [原字段 'item_tax']
    sales_tax_amt: FloatOrNone2Zero = Field(validation_alias="item_tax")
    # 买家支付运费金额 [原字段 'shipping_price']
    shipping_credits_amt: FloatOrNone2Zero = Field(validation_alias="shipping_price")
    # 买家支付运费税费 [原字段 'shipping_tax']
    shipping_credits_tax_amt: FloatOrNone2Zero = Field(validation_alias="shipping_tax")
    # 买家支付礼品包装费金额 [原字段 'gift_wrap_price']
    giftwrap_credits_amt: FloatOrNone2Zero = Field(validation_alias="gift_wrap_price")
    # 买家支付礼品包装费税费 [原字段 'gift_wrap_tax']
    giftwrap_credits_tax_amt: FloatOrNone2Zero = Field(validation_alias="gift_wrap_tax")
    # 卖家商品促销折扣金额 [原字段 'item_promotion_discount']
    promotion_discount_amt: FloatOrNone2Zero = Field(validation_alias="item_promotion_discount")
    # 卖家商品运费折扣金额 [原字段 'ship_promotion_discount']
    shipping_discount_amt: FloatOrNone2Zero = Field(validation_alias="ship_promotion_discount")
    # 亚马逊积分抵付款金额 (日本站) [原字段 'points_granted']
    points_discount_amt: FloatOrNone2Zero = Field(validation_alias="points_granted")
    # 货币代码 [原字段 'currency']
    currency_code: str = Field(validation_alias="currency")
    # 买家国家代码 [原字段 'ship_country']
    buyer_country_code: str = Field(validation_alias="ship_country")
    # 买家州/省 [原字段 'ship_state']
    buyer_state: str = Field(validation_alias="ship_state")
    # 买家城市 [原字段 'ship_city']
    buyer_city: str = Field(validation_alias="ship_city")
    # 买家地址 [原字段 'ship_address_1']
    buyer_address: str = Field(validation_alias="ship_address_1")
    # 买家邮编 [原字段 'ship_postal_code']
    buyer_postcode: str = Field(validation_alias="ship_postal_code")
    # 买家名称
    buyer_name: str
    # 买家邮箱
    buyer_email: str
    # 买家电话 [原字段 'buyer_phone_number']
    buyer_phone: str = Field(validation_alias="buyer_phone_number")
    # 收件人名称
    recipient_name: str
    # 订单购买时间 (UTC时间) [原字段 'purchase_date']
    purchase_time_utc: str = Field(validation_alias="purchase_date")
    # 订单支付时间 (UTC时间) [原字段 'payments_date']
    payments_time_utc: str = Field(validation_alias="payments_date")
    # 订单发货时间 (UTC时间) [原字段 'shipment_date']
    shipment_time_utc: str = Field(validation_alias="shipment_date")
    # 预计送达时间 (UTC时间) [原字段 'estimated_arrival_date']
    estimated_arrival_time_utc: str = Field(validation_alias="estimated_arrival_date")
    # 报告数据时间 (UTC时间) [原字段 'reporting_date']
    report_time_utc: str = Field(validation_alias="reporting_date")
    # fmt: on


class FbaOrders(ResponseV1):
    """亚马逊FBA订单列表"""

    data: list[FbaOrder]


# . FBA Replacement Orders
class FbaReplacementOrder(BaseModel):
    """亚马逊FBA换货源订单"""

    # fmt: off
    # 领星店铺ID
    sid: int
    # 订单唯一哈希值 (不是唯一键)
    order_hash: str
    # 原始亚马逊订单编号 [原字段 'original_amazon_order_id']
    amazon_order_id: str = Field(validation_alias="original_amazon_order_id")
    # 原始亚马逊配送中心代码 [原字段 'original_fulfillment_center_id']
    fulfillment_center_id: str = Field(validation_alias="original_fulfillment_center_id")
    # 换货商品ASIN
    asin: str
    # 换货亚马逊SKU [原字段 'seller_sku']
    msku: str = Field(validation_alias="seller_sku")
    # 换货亚马逊订单编号
    replacement_amazon_order_id: str
    # 换货亚马逊配送中心代码 [原字段 'fulfillment_center_id']
    replacement_fulfillment_center_id: str = Field(validation_alias="fulfillment_center_id")
    # 换货数量 [原字段 'quantity']
    replacement_qty: int = Field(validation_alias="quantity")
    # 换货原因代码
    replacement_reason_code: int
    # 换货原因描述 [原字段 'replacement_reason_msg']
    replacement_reason_desc: str = Field(validation_alias="replacement_reason_msg")
    # 换货时间 (UTC时间) [原字段 'shipment_date']
    replacement_time_utc: str = Field(validation_alias="shipment_date")
    # 数据同步时间 (时间戳) [原字段 'sync_time']
    sync_time_ts: int = Field(validation_alias="sync_time")
    # fmt: on


class FbaReplacementOrders(ResponseV1):
    """亚马逊FBA换货源订单列表"""

    data: list[FbaReplacementOrder]


# . FBA Return Orders
class ReturnOrderTag(BaseModel):
    """亚马逊FBA退货源订单标签"""

    # 标签名称
    tag_name: str
    # 标签颜色
    tag_color: str


class FbaReturnOrder(BaseModel):
    """亚马逊FBA退货源订单"""

    # 领星店铺ID
    sid: int
    # 亚马逊订单编号 [原字段 'order_id']
    amazon_order_id: str = Field(validation_alias="order_id")
    # 亚马逊配送中心代码
    fulfillment_center_id: str
    # 退货商品ASIN
    asin: str
    # 退货亚马逊SKU [原字段 'sku']
    msku: str = Field(validation_alias="sku")
    # 退货领星本地SKU [原字段 'local_sku']
    lsku: str = Field(validation_alias="local_sku")
    # 退货亚马逊FNSKU
    fnsku: str
    # 退货商品标题 [原字段 'product_name']
    title: str = Field(validation_alias="product_name")
    # 退货商品数量 [原字段 'quantity']
    return_qty: int = Field(validation_alias="quantity")
    # 退货状态 [原字段 'status']
    return_status: str = Field(validation_alias="status")
    # 退货原因 [原字段 'reason']
    return_reason: str = Field(validation_alias="reason")
    # 退货备注 [原字段 'remark']
    return_note: str = Field(validation_alias="remark")
    # 退货处置结果 [原字段 'detailed_disposition']
    disposition: str = Field(validation_alias="detailed_disposition")
    # LNP编码号 [原字段 'license_plate_number']
    lpn_number: str = Field(validation_alias="license_plate_number")
    # 买家评论
    customer_comments: str
    # 订单购买时间 (UTC时间) [原字段 'purchase_date']
    purchase_time_utc: str = Field(validation_alias="purchase_date")
    # 订单购买日期 (本地日期) [原字段 'purchase_date_locale']
    purchase_date_loc: str = Field(validation_alias="purchase_date_locale")
    # 退货时间 (UTC时间) [原字段 'return_date']
    return_time_utc: str = Field(validation_alias="return_date")
    # 退货日期 (本地日期) [原字段 'return_date_locale']
    return_date_loc: str = Field(validation_alias="return_date_locale")
    # 数据最后修改时间 (北京时间) [原字段 'gmt_modified']
    update_time_cnt: str = Field(validation_alias="gmt_modified")
    # 退货标签 [原字段 'tag']
    tags: list[ReturnOrderTag] = Field(validation_alias="tag")


class FbaReturnOrders(ResponseV1):
    """亚马逊FBA退货源订单列表"""

    data: list[FbaReturnOrder]


# . FBA Shipments
class FbaShipment(BaseModel):
    """亚马逊FBA发货订单"""

    # fmt: off
    # 领星店铺ID
    sid: int
    # 亚马逊订单编号
    amazon_order_id: str
    # 亚马逊订单商品编号
    amazon_order_item_id: str
    # 商家订单编号
    merchant_order_id: str
    # 商家订单商品编号
    merchant_order_item_id: str
    # 销售渠道 (如: "amazon.com")
    sales_channel: str
    # 配送方式 (AFN 或 MFN)
    fulfillment_channel: str
    # 亚马逊配送中心代码
    fulfillment_center_id: str
    # 亚马逊货件编号
    shipment_id: str
    # 亚马逊货件商品编号
    shipment_item_id: str
    # 订单配送服务级别 [原字段 'ship_service_level']
    shipment_service: str = Field(validation_alias="ship_service_level")
    # 承运商代码 [原字段 'carrier']
    shipment_carrier: str = Field(validation_alias="carrier")
    # 追踪单号
    tracking_number: str
    # 亚马逊SKU
    msku: str
    # 领星本地SKU [原字段 'local_sku']
    lsku: str = Field(validation_alias="local_sku")
    # 领星产品名称 [原字段 'local_name']
    product_name: str = Field(validation_alias="local_name")
    # 商品标题 [原字段 'product_name']
    title: str = Field(validation_alias="product_name")
    # 发货商品数量 [原字段 'quantity_shipped']
    shipped_qty: int = Field(validation_alias="quantity_shipped")
    # 商品销售金额 [原字段 'item_price']
    sales_amt: FloatOrNone2Zero = Field(validation_alias="item_price")
    # 商品销售金额税费 [原字段 'item_tax']
    sales_tax_amt: FloatOrNone2Zero = Field(validation_alias="item_tax")
    # 买家支付运费金额 [原字段 'shipping_price']
    shipping_credits_amt: FloatOrNone2Zero = Field(validation_alias="shipping_price")
    # 买家支付运费税费 [原字段 'shipping_tax']
    shipping_credits_tax_amt: FloatOrNone2Zero = Field(validation_alias="shipping_tax")
    # 买家支付礼品包装费金额 [原字段 'gift_wrap_price']
    giftwrap_credits_amt: FloatOrNone2Zero = Field(validation_alias="gift_wrap_price")
    # 买家支付礼品包装费税费 [原字段 'gift_wrap_tax']
    giftwrap_credits_tax_amt: FloatOrNone2Zero = Field(validation_alias="gift_wrap_tax")
    # 卖家商品促销折扣金额 [原字段 'item_promotion_discount']
    promotion_discount_amt: FloatOrNone2Zero = Field(validation_alias="item_promotion_discount")
    # 卖家商品运费折扣金额 [原字段 'ship_promotion_discount']
    shipping_discount_amt: FloatOrNone2Zero = Field(validation_alias="ship_promotion_discount")
    # 亚马逊积分抵付款金额 (日本站) [原字段 'points_granted']
    points_discount_amt: FloatOrNone2Zero = Field(validation_alias="points_granted")
    # 货币代码 [原字段 'currency']
    currency_code: str = Field(validation_alias="currency")
    # 买家国家代码 [原字段 'ship_country']
    buyer_country_code: str = Field(validation_alias="ship_country")
    # 买家州/省 [原字段 'ship_state']
    buyer_state: str = Field(validation_alias="ship_state")
    # 买家城市 [原字段 'ship_city']
    buyer_city: str = Field(validation_alias="ship_city")
    # 买家地址1 [原字段 'ship_address_1']
    buyer_address1: str = Field(validation_alias="ship_address_1")
    # 买家地址2 [原字段 'ship_address_2']
    buyer_address2: str = Field(validation_alias="ship_address_2")
    # 买家地址3 [原字段 'ship_address_3']
    buyer_address3: str = Field(validation_alias="ship_address_3")
    # 买家邮编 [原字段 'ship_postal_code']
    buyer_postcode: str = Field(validation_alias="ship_postal_code")
    # 买家名称
    buyer_name: str
    # 买家邮箱
    buyer_email: str
    # 买家电话 [原字段 'buyer_phone_number']
    buyer_phone: str = Field(validation_alias="buyer_phone_number")
    # 收件人名称
    recipient_name: str
    # 账单国家代码 [原字段 'bill_country']
    billing_country_code: str = Field(validation_alias="bill_country")
    # 账单州/省 [原字段 'bill_state']
    billing_state: str = Field(validation_alias="bill_state")
    # 账单城市 [原字段 'bill_city']
    billing_city: str = Field(validation_alias="bill_city")
    # 账单地址1 [原字段 'bill_address_1']
    billing_address1: str = Field(validation_alias="bill_address_1")
    # 账单地址2 [原字段 'bill_address_2']
    billing_address2: str = Field(validation_alias="bill_address_2")
    # 账单地址3 [原字段 'bill_address_3']
    billing_address3: str = Field(validation_alias="bill_address_3")
    # 账单邮编 [原字段 'bill_postal_code']
    billing_postcode: str = Field(validation_alias="bill_postal_code")
    # 订单购买时间 (UTC时间) [原字段 'purchase_date']
    purchase_time_utc: str = Field(validation_alias="purchase_date")
    # 订单购买日期 (本地时间) [原字段 'purchase_date_locale']
    purchase_time_loc: str = Field(validation_alias="purchase_date_locale")
    # 订单付款时间 (UTC时间) [原字段 'payments_date']
    payments_time_utc: str = Field(validation_alias="payments_date")
    # 订单付款时间 (本地时间) [原字段 'payments_date_locale']
    payments_time_loc: str = Field(validation_alias="payments_date_locale")
    # 订单发货时间 (UTC时间) [原字段 'shipment_date']
    shipment_time_utc: str = Field(validation_alias="shipment_date")
    # 订单发货时间 (本地时间) [原字段 'shipment_date_locale']
    shipment_time_loc: str = Field(validation_alias="shipment_date_locale")
    # 预计送达时间 (UTC时间) [原字段 'estimated_arrival_date']
    estimated_arrival_time_utc: str = Field(validation_alias="estimated_arrival_date")
    # 预计送达日期 (本地日期) [原字段 'estimated_arrival_date_locale']
    estimated_arrival_date_loc: str = Field(validation_alias="estimated_arrival_date_locale")
    # 报告数据时间 (UTC时间) [原字段 'reporting_date']
    report_time_utc: str = Field(validation_alias="reporting_date")
    # 报告数据时间 (本地时间) [原字段 'reporting_date_locale']
    report_time_loc: str = Field(validation_alias="reporting_date_locale")
    # fmt: on


class FbaShipments(ResponseV1):
    """亚马逊FBA发货订单列表"""

    data: list[FbaShipment]


# . FBM Return Orders
class FbmReturnOrder(BaseModel):
    """亚马逊FBM退货源订单"""

    # fmt: off
    # 领星店铺ID
    sid: int
    # 领星店铺名称
    seller_name: str
    # 国家 (站点)
    country: str
    # 订单唯一哈希值 (不是唯一键)
    order_hash: str
    # 亚马逊订单编号 [原字段 'order_id']
    amazon_order_id: str = Field(validation_alias="order_id")
    # 商品ASIN
    asin: str
    # 亚马逊SKU [原字段 'seller_sku']
    msku: str = Field(validation_alias="seller_sku")
    # 领星本地SKU [原字段 'local_sku']
    lsku: str = Field(validation_alias="local_sku")
    # 领星产品名称 [原字段 'local_name']
    product_name: str = Field(validation_alias="local_name")
    # 品牌名称 [原字段 'brand_title']
    brand: str = Field(validation_alias="brand_title")
    # 商品标题 [原字段 'item_name']
    title: str = Field(validation_alias="item_name")
    # 商品类目 [原字段 'category_title_path']
    category: str = Field(validation_alias="category_title_path")
    # 商品 ASIN 链接
    asin_url: str
    # 商品图片链接 [原字段 'pic_url']
    image_url: str = Field(validation_alias="pic_url")
    # 货币代码
    currency_code: str
    # 订单商品销售金额 [原字段 'order_amount']
    order_amt: float = Field(validation_alias="order_amount")
    # 订单商品退款金额 [原字段 'refunded_amount']
    refund_amt: float = Field(validation_alias="refunded_amount")
    # 订单商品数量 [原字段 'order_quantity']
    order_qty: int = Field(validation_alias="order_quantity")
    # 退货商品数量 [原字段 'return_quantity']
    return_qty: int = Field(validation_alias="return_quantity")
    # 退货状态
    return_status: str
    # 退货类型
    return_type: str
    # 退货原因
    return_reason: str
    # 退货解决方案 [原字段 'resolution']
    return_resolution: str = Field(validation_alias="resolution")
    # 退货备注 [原字段 'remark']
    return_note: str = Field(validation_alias="remark")
    # 退货RMA编号 [原字段 'rma_id']
    rma_number: str = Field(validation_alias="rma_id")
    # 退货RMA提供者 [原字段 'rma_id_provider']
    rma_provider: str = Field(validation_alias="rma_id_provider")
    # 退货承运商 [原字段 'return_carrier']
    carrier: str = Field(validation_alias="return_carrier")
    # 退货追踪单号 [原字段 'tracking_id']
    tracking_number: str = Field(validation_alias="tracking_id")
    # 发票编号
    invoice_number: str
    # 物流标签类型
    label_type: str
    # 物流标签费用
    label_cost: float
    # 物流标签费用支付方
    label_payer: str
    # 是否为Prime订单 (N: No, Y: Yes)
    is_prime: str
    # 是否在退货政策内 (N: No, Y: Yes) [原字段 'in_policy']
    is_within_policy: str = Field(validation_alias="in_policy")
    # 是否是A-to-Z索赔订单 (N: No, Y: Yes) [原字段 'a_to_z_claim']
    is_a_to_z_claim: str = Field(validation_alias="a_to_z_claim")
    # Safe-T索赔ID
    safet_claim_id: str
    # Safe-T索赔原因 [原字段 'safet_action_reason']
    safet_claim_reason: str = Field(validation_alias="safet_action_reason")
    # Safe-T索赔状态
    safet_claim_state: str
    # Safe-T索赔赔付金额 [原字段 'safet_claim_reimbursement_amount']
    safet_claim_reimbursement_amt: FloatOrNone2Zero = Field(validation_alias="safet_claim_reimbursement_amount")
    # Safe-T索赔时间 [原字段 'safet_claim_creation_time']
    safet_claim_time: str = Field(validation_alias="safet_claim_creation_time")
    # 购买日期
    order_date: str
    # 退货日期 
    return_date: str
    # 退货送达日期
    return_delivery_date: str
    # 数据同步时间 (时间戳) [原字段 'sync_time']
    sync_time_ts: int = Field(validation_alias="sync_time")
    # 退货标签 [原字段 'tag_type_ids']
    tags: list[ReturnOrderTag] = Field(validation_alias="tag_type_ids")
    # fmt: on


class FbmReturnOrders(ResponseV1):
    """亚马逊FBM退货源订单列表"""

    data: list[FbmReturnOrder]


# FBA 库存数据 -------------------------------------------------------------------------------------------------------------------
# . FBA Removal Orders
class FbaRemovalOrder(BaseModel):
    """亚马逊FBA移除订单"""

    # 领星店铺ID
    sid: int
    # 亚马逊卖家ID
    seller_id: str
    # 站点区域
    region: str
    # 站点国家代码
    country_code: str
    # 移除订单编号 [原字段 'order_id']
    removal_order_id: str = Field(validation_alias="order_id")
    # 移除订单类型 (Return 或 Disposal) [原字段 'order_type']
    removal_order_type: str = Field(validation_alias="order_type")
    # 移除订单状态 [原字段 'order_status']
    removal_order_status: str = Field(validation_alias="order_status")
    # 亚马逊SKU [原字段 'sku']
    msku: str = Field(validation_alias="sku")
    # 领星本地SKU [原字段 'local_sku']
    lsku: str = Field(validation_alias="local_sku")
    # 亚马逊FNSKU
    fnsku: str
    # 领星产品名称 [原字段 'local_name']
    product_name: str = Field(validation_alias="local_name")
    # 库存处置结果
    disposition: str
    # 移除商品请求数量 [原字段 'requested_quantity']
    requested_qty: int = Field(validation_alias="requested_quantity")
    # 取消移除商品数量 [原字段 'cancelled_quantity']
    cancelled_qty: int = Field(validation_alias="cancelled_quantity")
    # 移除处理中商品数量 [原字段 'in_process_quantity']
    processing_qty: int = Field(validation_alias="in_process_quantity")
    # 已处置商品数量 [原字段 'disposed_quantity']
    disposed_qty: int = Field(validation_alias="disposed_quantity")
    # 已发货商品数量 [原字段 'shipped_quantity']
    shipped_qty: int = Field(validation_alias="shipped_quantity")
    # 移除商品费用
    removal_fee: float
    # 货币代码 [原字段 'currency']
    currency_code: str = Field(validation_alias="currency")
    # 收件地址 [原字段 'address_detail']
    ship_to_address: str = Field(validation_alias="address_detail")
    # 移除请求时间 [原字段 'request_date']
    request_time: str = Field(validation_alias="request_date")
    # 数据更新时间 [原字段 'last_updated_date']
    update_time: str = Field(validation_alias="last_updated_date")


class FbaRemovalOrders(ResponseV1):
    """亚马逊FBA移除订单列表"""

    data: list[FbaRemovalOrder]


# . FBA  Removal Shipments
class FbaRemovalShipmentSeller(BaseModel):
    """亚马逊FBA移除货件店铺信息"""

    # 领星站点ID
    mid: int
    # 领星店铺ID
    sid: int
    # 领星店铺名称 [原字段 'name']
    seller_name: str = Field(validation_alias="name")
    # 站点国家 (中文) [原字段 'marketplace']
    country: str = Field(validation_alias="marketplace")


class FbaRemovalShipmentProduct(BaseModel):
    """亚马逊FBA移除货件商品信息"""

    # 领星本地SKU [原字段 'local_sku']
    lsku: str = Field(validation_alias="local_sku")
    # 领星产品名称 [原字段 'local_name']
    product_name: str = Field(validation_alias="local_name")


class FbaRemovalShipmentShipToAddress(BaseModel):
    """亚马逊FBA移除货件收件地址"""

    # 国家代码 [原字段 'ship_country']
    country_code: str = Field(validation_alias="ship_country")
    # 州/省 [原字段 'ship_state']
    state: str = Field(validation_alias="ship_state")
    # 城市 [原字段 'ship_city']
    city: str = Field(validation_alias="ship_city")
    # 县/郡
    county: str
    # 区/镇
    district: str
    # 详细地址
    address: str
    # 地址行1
    address_line1: str
    # 地址行2
    address_line2: str
    # 地址行3
    address_line3: str
    # 邮编 [原字段 'ship_postal_code']
    postcode: str = Field(validation_alias="ship_postal_code")
    # 收件人名称
    name: str
    # 收件人电话
    phone: str


class FbaRemovalShipment(BaseModel):
    """亚马逊FBA移除货件"""

    # fmt: off
    # 领星站点ID
    mid: int
    # 领星店铺ID
    sid: int
    # 站点国家 (中文) [原字段 'marketplace']
    country: str = Field(validation_alias="marketplace")
    # 亚马逊卖家ID
    seller_id: str
    # 领星店铺帐号名称
    seller_account_name: str
    # 店铺信息列表 [原字段 'seller_name']
    sellers: list[FbaRemovalShipmentSeller] = Field(validation_alias="seller_name")
    # 移除业务标识 (唯一移除货件行) [原字段 'uuid_new']
    uuid: str = Field(validation_alias="uuid_new")
    # 移除业务标识序号 [原字段 'uuid_num_new']
    uuid_seq: int = Field(validation_alias="uuid_num_new")
    # 移除货件ID [原字段 'order_id']
    removal_shipment_id: str = Field(validation_alias="order_id")
    # 移除货件类型 [原字段 'removal_order_type']
    removal_shipment_type: str = Field(validation_alias="removal_order_type")
    # 亚马逊SKU [原字段 'sku']
    msku: str = Field(validation_alias="sku")
    # 亚马逊FNSKU
    fnsku: str
    # 商品信息列表 [原字段 'local_info']
    products: list[FbaRemovalShipmentProduct] = Field(validation_alias="local_info")
    # 库存处置结果
    disposition: str
    # 已发货商品数量 [原字段 'shipped_quantity']
    shipped_qty: int = Field(validation_alias="shipped_quantity")
    # 货件成运商
    carrier: str
    # 货件追踪单号
    tracking_number: str
    # 移除货件的仓库入库单号 [原字段 'overseas_removal_order_no']
    warehouse_inbound_number: str = Field(validation_alias="overseas_removal_order_no")
    # 移除货件收货地址 [原字段 'delivery_info']
    ship_to_address: FbaRemovalShipmentShipToAddress = Field(validation_alias="delivery_info")
    # 移除请求时间 [原字段 'request_date']
    request_time: str = Field(validation_alias="request_date")
    # 移除发货时间 [原字段 'shipment_date']
    shipment_time: str = Field(validation_alias="shipment_date")
    # 移除发货时间 (时间戳) [原字段 'shipment_date_timestamp']
    shipment_time_ts: int = Field(validation_alias="shipment_date_timestamp")
    # fmt: on


class FbaRemovalShipments(ResponseV1):
    """亚马逊FBA移除货件列表"""

    data: list[FbaRemovalShipment]


# . FBA Inventory
class FbaInventoryItem(BaseModel):
    """亚马逊FBA库存"""

    # fmt: off
    # 商品ASIN
    asin: str
    # 亚马逊SKU [原字段 'sku']
    msku: str = Field(validation_alias="sku")
    # 亚马逊FNSKU
    fnsku: str
    # 商品标题 [原字段 'product_name']
    title: str = Field(validation_alias="product_name")
    # 商品状态
    condition: str
    # 商品单位标准价格 [原字段 'your_price']
    standard_price: float = Field(validation_alias="your_price")
    # 商品单位到手价格
    landed_price: float
    # 商品单位体积 [原字段 'per_unit_volume']
    item_volume: float = Field(validation_alias="per_unit_volume")
    # 商品单位采购成本 [原字段 'cg_price']
    cost_of_goods: FloatOrNone2Zero = Field(validation_alias="cg_price")
    # 是否是FBM配送 (Yes, No)
    mfn_listing_exists: str
    # FBM可售库存数量 [原字段 'mfn_fulfillable_quantity']
    mfn_fulfillable_qty: int = Field(validation_alias="mfn_fulfillable_quantity")
    # 是否是FBA配送 (Yes, No)
    afn_listing_exists: str
    # FBA在库库存数量 [原字段 'afn_warehouse_quantity']
    # (afn_fulfillable_qty + afn_unsellable_qty + afn_reserved_qty)
    afn_warehouse_qty: int = Field(validation_alias="afn_warehouse_quantity")
    # FBA可售库存数量 [原字段 'afn_fulfillable_quantity']
    afn_fulfillable_qty: int = Field(validation_alias="afn_fulfillable_quantity")
    # FBA不可售库存数量 [原字段 'afn_unsellable_quantity']
    afn_unsellable_qty: int = Field(validation_alias="afn_unsellable_quantity")
    # FBA预留库存数量 [原字段 'afn_reserved_quantity']
    afn_reserved_qty: int = Field(validation_alias="afn_reserved_quantity")
    # FBA总库存数量 [原字段 'afn_total_quantity']
    # (afn_warehouse_qty + afn_inbound_working&shipped&receiving_qty)
    afn_total_qty: int = Field(validation_alias="afn_total_quantity")
    # FBA 发货计划入库的库存数量 [原字段 'afn_inbound_working_quantity']
    afn_inbound_working_qty: int = Field(validation_alias="afn_inbound_working_quantity")
    # FBA 发货在途的库存数量 [原字段 'afn_inbound_shipped_quantity']
    afn_inbound_shipped_qty: int = Field(validation_alias="afn_inbound_shipped_quantity")
    # FBA 发货入库接收中的库存数量 [原字段 'afn_inbound_receiving_quantity']
    afn_inbound_receiving_qty: int = Field(validation_alias="afn_inbound_receiving_quantity")
    # 库存更新时间 (北京时间) [原字段 'gmt_modified']
    update_time: str = Field(validation_alias="gmt_modified")
    # fmt: on


class FbaInventory(ResponseV1):
    """亚马逊FBA库存列表"""

    data: list[FbaInventoryItem]


# . FBA Reserved Inventory
class FbaReservedInventoryItem(BaseModel):
    """亚马逊FBA预留库存"""

    # fmt: off
    # 商品ASIN
    asin: str
    # 亚马逊SKU [原字段 'sku']
    msku: str = Field(validation_alias="sku")
    # 亚马逊FNSKU
    fnsku: str
    # 商品标题 [原字段 'product_name']
    title: str = Field(validation_alias="product_name")
    # FBA 预留库存总数量 [原字段 'reserved_qty']
    # (afn_reserved_fc_processing&fc_transfer_qty&customer_order_qty)
    afn_reserved_qty: int = Field(validation_alias="reserved_qty")
    # FBA 在库待调仓的库存数量 [原字段 'reserved_fc_processing']
    afn_reserved_fc_processing_qty: int = Field(validation_alias="reserved_fc_processing")
    # FBA 在库调仓中的库存数量 [原字段 'reserved_fc_transfers']
    afn_reserved_fc_transfers_qty: int = Field(validation_alias="reserved_fc_transfers")
    # FBA 在库待发货的库存数量 [原字段 'reserved_customerorders']
    afn_reserved_customer_order_qty: int = Field(validation_alias="reserved_customerorders")
    # 库存更新时间 (北京时间) [原字段 'gmt_modified']
    update_time: str = Field(validation_alias="gmt_modified")
    # fmt: on


class FbaReservedInventory(ResponseV1):
    """亚马逊FBA可售库存列表"""

    data: list[FbaReservedInventoryItem]


# . FBA Inventory Health
class FbaInventoryHealthItem(BaseModel):
    """亚马逊FBA库存年龄"""

    # fmt: off
    # 领星店铺ID
    sid: int
    # 站点国家 [原字段 'marketplace']
    country: str = Field(validation_alias="marketplace")
    # 商品ASIN
    asin: str
    # 亚马逊SKU [原字段 'sku']
    msku: str = Field(validation_alias="sku")
    # 亚马逊FNSKU
    fnsku: str
    # 商品标题 [原字段 'product_name']
    title: str = Field(validation_alias="product_name")
    # 商品状态
    condition: str
    # 商品类目 [原字段 'product_group']
    category: str = Field(validation_alias="product_group")
    # 商品类目排名 [原字段 'sales_rank']
    category_rank: IntOrNone2Zero = Field(validation_alias="sales_rank")
    # 商品仓储类型
    storage_type: str
    # 商品总仓储使用量 (排除待移除商品仓储使用量)
    storage_volume: float
    # 商品单位体积
    item_volume: float
    # 体积单位 [原字段 'volume_unit_measurement']
    volume_unit: str = Field(validation_alias="volume_unit_measurement")
    # 可售库存数量 [原字段 'available']
    afn_fulfillable_qty: int = Field(validation_alias="available")
    # 待移除库存数量 [原字段 'pending_removal_quantity']
    afn_pending_removal_qty: int = Field(validation_alias="pending_removal_quantity")
    # FBA 总发货库存数量 [原字段 'inbound_quantity']
    # (inbound_working_qty + inbound_shipped_qty + inbound_received_qty)
    afn_inbound_total_qty: int = Field(validation_alias="inbound_quantity")
    # FBA 发货计划入库的库存数量 [原字段 'inbound_working']
    afn_inbound_working_qty: int = Field(validation_alias="inbound_working")
    # FBA 发货在途的库存数量 [原字段 'inbound_shipped']
    afn_inbound_shipped_qty: int = Field(validation_alias="inbound_shipped")
    # FBA 发货入库接收中的库存数量 [原字段 'inbound_received']
    afn_inbound_receiving_qty: int = Field(validation_alias="inbound_received")
    # 库龄0-30天的库存数量 [原字段 'inv_age_0_to_30_days']
    age_0_to_30_days_qty: int = Field(validation_alias="inv_age_0_to_30_days")
    # 库龄31-60天的库存数量 [原字段 'inv_age_31_to_60_days']
    age_31_to_60_days_qty: int = Field(validation_alias="inv_age_31_to_60_days")
    # 库龄61-90天的库存数量 [原字段 'inv_age_61_to_90_days']
    age_61_to_90_days_qty: int = Field(validation_alias="inv_age_61_to_90_days")
    # 库龄0-90天的库存数量 [原字段 'inv_age_0_to_90_days']
    age_0_to_90_days_qty: int = Field(validation_alias="inv_age_0_to_90_days")
    # 库龄91-180天的库存数量 [原字段 'inv_age_91_to_180_days']
    age_91_to_180_days_qty: int = Field(validation_alias="inv_age_91_to_180_days")
    # 库龄181-270天的库存数量 [原字段 'inv_age_181_to_270_days']
    age_181_to_270_days_qty: int = Field(validation_alias="inv_age_181_to_270_days")
    # 库龄181-330天的库存数量 [原字段 'inv_age_181_to_330_days']
    age_181_to_330_days_qty: int = Field(validation_alias="inv_age_181_to_330_days")
    # 库龄271-330天的库存数量 [原字段 'inv_age_271_to_330_days_quantity']
    age_271_to_330_days_qty: int = Field(validation_alias="inv_age_271_to_330_days_quantity")
    # 库龄271-365天的库存数量 [原字段 'inv_age_271_to_365_days']
    age_271_to_365_days_qty: int = Field(validation_alias="inv_age_271_to_365_days")
    # 库龄331-365天的库存数量 [原字段 'inv_age_331_to_365_days']
    age_331_to_365_days_qty: int = Field(validation_alias="inv_age_331_to_365_days")
    # 库龄365天以上的库存数量 [原字段 'inv_age_365_plus_days']
    age_365_plus_days_qty: int = Field(validation_alias="inv_age_365_plus_days")
    # 库龄180天以上收取长期仓储费的库存数量 [原字段 'qty_to_be_charged_ltsf_6_mo']
    ltsf_180_plus_days_qty: int = Field(validation_alias="qty_to_be_charged_ltsf_6_mo")
    # 库龄180天以上预估收取长期仓储费的金额 [原字段 'projected_ltsf_6_mo']
    estimated_ltsf_180_plus_fee: FloatOrNone2Zero = Field(validation_alias="projected_ltsf_6_mo")
    # 库龄365天以上收取长期仓储费的库存数量 [原字段 'qty_to_be_charged_ltsf_12_mo']
    ltsf_365_plus_days_qty: int = Field(validation_alias="qty_to_be_charged_ltsf_12_mo")
    # 库龄365天以上预估收取长期仓储费的金额 [原字段 'projected_ltsf_12_mo']
    estimated_ltsf_365_plus_fee: FloatOrNone2Zero = Field(validation_alias="projected_ltsf_12_mo")
    # 预估截至下一收费日期 (每月15日) 长期仓储费金额 [原字段 'estimated_ltsf_next_charge']
    estimated_ltsf_next_charge_fee: FloatOrNone2Zero = Field(validation_alias="estimated_ltsf_next_charge")
    # 是否免除低库存费 (Yes, No) [原字段 'exempted_from_low_inventory_level_fee']
    is_lilf_exempted: str = Field(validation_alias="exempted_from_low_inventory_level_fee")
    # 当前周是否收取低库存费 (Yes, No) [原字段 'low_Inventory_Level_fee_applied_in_current_week']
    is_lilf_applied_in_current_week: str = Field(validation_alias="low_Inventory_Level_fee_applied_in_current_week")
    # 是否免除低库存成本覆盖费 (Yes, No) [原字段 'exempted_from_low_inventory_cost_coverage_fee']
    is_licc_exempted: str = Field(validation_alias="exempted_from_low_inventory_cost_coverage_fee")
    # 当前周是否收取低库存成本覆盖费 (Yes, No) [原字段 'low_inventory_cost_coverage_fee_applied_in_current_week']
    is_licc_applied_in_current_week: str = Field(validation_alias="low_inventory_cost_coverage_fee_applied_in_current_week")
    # 预估往后30天内的仓储费金额 (月度仓储 + 长期仓储 + 低库存 + 库存成本覆盖) [原字段 'estimated_storage_cost_next_month']
    estimated_30_days_storage_fee: FloatOrNone2Zero = Field(validation_alias="estimated_storage_cost_next_month")
    # 货币代码 [原字段 'currency']
    currency_code: str = Field(validation_alias="currency")
    # 商品标准价 (不包含促销, 运费, 积分) [原字段 'your_price']
    standard_price: FloatOrNone2Zero = Field(validation_alias="your_price")
    # 商品优惠价 [原字段 'sales_price']
    sale_price: FloatOrNone2Zero = Field(validation_alias="sales_price")
    # 商品促销价 [原字段 'featuredoffer_price']
    offer_price: FloatOrNone2Zero = Field(validation_alias="featuredoffer_price")
    # 商品最低价 (含运费) [原字段 'lowest_price_new_plus_shipping']
    lowest_price: FloatOrNone2Zero = Field(validation_alias="lowest_price_new_plus_shipping")
    # 商品最低二手价 (含运费) [原字段 'lowest_price_used']
    lowest_used_price: FloatOrNone2Zero = Field(validation_alias="lowest_price_used")
    # 最近7天发货销售额 [原字段 'sales_shipped_last_7_days']
    shipped_7d_amt: FloatOrNone2Zero = Field(validation_alias="sales_shipped_last_7_days")
    # 最近30天发货销售额 [原字段 'sales_shipped_last_30_days']
    shipped_30d_amt: FloatOrNone2Zero = Field(validation_alias="sales_shipped_last_30_days")
    # 最近60天发货销售额 [原字段 'sales_shipped_last_60_days']
    shipped_60d_amt: FloatOrNone2Zero = Field(validation_alias="sales_shipped_last_60_days")
    # 最近90天发货销售额 [原字段 'sales_shipped_last_90_days']
    shipped_90d_amt: FloatOrNone2Zero = Field(validation_alias="sales_shipped_last_90_days")
    # 最近7天发货数量 [原字段 'units_shipped_t7']
    shipped_7d_qty: IntOrNone2Zero = Field(validation_alias="units_shipped_t7")
    # 最近30天发货数量 [原字段 'units_shipped_t30']
    shipped_30d_qty: IntOrNone2Zero = Field(validation_alias="units_shipped_t30")
    # 最近60天发货数量 [原字段 'units_shipped_t60']
    shipped_60d_qty: IntOrNone2Zero = Field(validation_alias="units_shipped_t60")
    # 最近90天发货数量 [原字段 'units_shipped_t90'] 
    shipped_90d_qty: IntOrNone2Zero = Field(validation_alias="units_shipped_t90")
    # 库存售出率 (过去 90 天销量除以平均可售库存) [原字段 'sell_through']
    sell_through_rate: FloatOrNone2Zero = Field(validation_alias="sell_through")
    # 历史连续至少6个月无销售库存 [原字段 'no_sale_last_6_months']
    historical_no_sale_6m: IntOrNone2Zero = Field(validation_alias="no_sale_last_6_months")
    # 历史供货天数 (取短期&长期更大值)
    historical_days_of_supply: FloatOrNone2Zero
    # 历史短期供货天数 [原字段 'short_term_historical_days_of_supply']
    historical_st_days_of_supply: FloatOrNone2Zero = Field(validation_alias="short_term_historical_days_of_supply")
    # 历史长期供货天数 [原字段 'long_term_historical_days_of_supply']
    historical_lt_days_of_supply: FloatOrNone2Zero = Field(validation_alias="long_term_historical_days_of_supply")
    # 预估可供货天数 [原字段 'days_of_supply']
    estimated_days_of_supply: IntOrNone2Zero = Field(validation_alias="days_of_supply")
    # 基于过去30天数据预估可供货周数 [原字段 'weeks_of_cover_t30']
    estimated_weeks_of_cover_30d: IntOrNone2Zero = Field(validation_alias="weeks_of_cover_t30")
    # 基于过去90天数据预估可供货周数 [原字段 'weeks_of_cover_t90']
    estimated_weeks_of_cover_90d: IntOrNone2Zero = Field(validation_alias="weeks_of_cover_t90")
    # 预估冗余库存数量 [原字段 'estimated_excess_quantity']
    estimated_excess: IntOrNone2Zero = Field(validation_alias="estimated_excess_quantity")
    # 库存健康状态 [原字段 'fba_inventory_level_health_status']
    inventory_health_status: str = Field(validation_alias="fba_inventory_level_health_status")
    # 库存预警信息 [原字段 'alert']
    inventory_alert: str = Field(validation_alias="alert")
    # 推荐安全库存水平 [原字段 'healthy_inventory_level']
    recommended_healthy_qty: IntOrNone2Zero = Field(validation_alias="healthy_inventory_level")
    # 推荐最低库存水平 [原字段 'fba_minimum_inventory_level']
    recommended_minimum_qty: IntOrNone2Zero = Field(validation_alias="fba_minimum_inventory_level")
    # 推荐移除库存数量 [原字段 'recommended_removal_quantity']
    recommended_removal_qty: IntOrNone2Zero = Field(validation_alias="recommended_removal_quantity")
    # 推荐促销价格
    recommended_sales_price: FloatOrNone2Zero
    # 推荐促销天数 [原字段 'recommended_sale_duration_days']
    recommended_sales_days: IntOrNone2Zero = Field(validation_alias="recommended_sale_duration_days")
    # 推荐操作
    recommended_action: str
    # 预计推荐操作节省仓储费用 [原字段 'estimated_cost_savings_of_recommended_actions']
    estimated_savings_of_recommended_actions: float = Field(validation_alias="estimated_cost_savings_of_recommended_actions")
    # 数据日期 [原字段 'snapshot_date']
    report_date: str = Field(validation_alias="snapshot_date")
    # fmt: on


class FbaInventoryHealth(ResponseV1, FlattenDataList):
    """亚马逊FBA库存年龄列表"""

    data: list[FbaInventoryHealthItem]


# . FBA Inventory Adjustments
class FbaInventoryAdjustment(BaseModel):
    """亚马逊FBA库存调整"""

    # 领星店铺ID
    sid: int
    # 调整交易ID
    transaction_item_id: str
    # 亚马逊配送中心ID
    fulfillment_center_id: str
    # 亚马逊SKU
    msku: str
    # 亚马逊FNSKU
    fnsku: str
    # 商品标题 [原字段 'item_name']
    titile: str = Field(validation_alias="item_name")
    # 调整数量 [原字段 'quantity']
    adjustment_qty: int = Field(validation_alias="quantity")
    # 调整原因代码
    adjustment_reason: str = Field(validation_alias="reason")
    # 调整原因说明 [原字段 'reason_text']
    adjustment_reason_desc: str = Field(validation_alias="reason_text")
    # 库存处置结果
    disposition: str
    # 报告数据日期
    report_date: str


class FbaInventoryAdjustments(ResponseV1):
    """亚马逊FBA库存调整列表"""

    data: list[FbaInventoryAdjustment]


# 报告导出 -----------------------------------------------------------------------------------------------------------------------
# . Export Report Task
class ExportReportTaskId(BaseModel):
    """导出报告任务ID"""

    # 报告导出任务ID
    task_id: str


class ExportReportTask(ResponseV1):
    """报告导出任务"""

    data: ExportReportTaskId


# . Export Report Result
class ExportReportResultData(BaseModel):
    """报告导出结果数据"""

    # 报告文件ID
    report_document_id: StrOrNone2Blank
    # 报告生成进度状态
    progress_status: StrOrNone2Blank
    # 报告压缩算法
    compression_algorithm: StrOrNone2Blank
    # 报告下载链接
    url: StrOrNone2Blank


class ExportReportResult(ResponseV1):
    """报告导出结果"""

    data: ExportReportResultData


# . Export Report Refresh
class ExportReportRefreshData(BaseModel):
    """报告导出结果续期数据"""

    # 报告文件ID
    report_document_id: str
    # 报告下载链接
    url: str


class ExportReportRefresh(ResponseV1):
    """报告导出结果续期"""

    data: ExportReportRefreshData
