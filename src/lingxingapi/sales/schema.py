# -*- coding: utf-8 -*-
from typing import Any
from pydantic import BaseModel, Field, field_validator
from lingxingapi.base import schema as base_schema
from lingxingapi.base.schema import ResponseV1, ResponseResult, FlattenDataRecords
from lingxingapi.fields import IntOrNone2Zero, FloatOrNone2Zero, StrOrNone2Blank


# 销售 - Listing ----------------------------------------------------------------------------------------------------------------
# . Listing
class ListingSubcategory(BaseModel):
    """商品小类排名."""

    # 商品所属小类目 [原字段 'category']
    subcategory: str = Field(validation_alias="category")
    # 商品小类目排名 [原字段 'rank']
    subcategory_rank: int = Field(validation_alias="rank")


class ListingDimension(BaseModel):
    """商品尺寸和重量.

    - 长度单位: ""(未知), "inches", "inch", "centimeter", "yard", "veron", "foot"
    - 重量单位: ""(未知), "pounds", "kg", "ounce", "gram", "carat"
    """

    # 商品高度
    item_height: FloatOrNone2Zero
    # 商品高度单位 [原字段 'item_height_units_type']
    item_height_unit: str = Field(validation_alias="item_height_units_type")
    # 商品长度
    item_length: FloatOrNone2Zero
    # 商品长度单位 [原字段 'item_length_units_type']
    item_length_unit: str = Field(validation_alias="item_length_units_type")
    # 商品宽度
    item_width: FloatOrNone2Zero
    # 商品宽度单位 [原字段 'item_width_units_type']
    item_width_unit: str = Field(validation_alias="item_width_units_type")
    # 商品重量
    item_weight: FloatOrNone2Zero
    # 商品重量单位 [原字段 'item_weight_units_type']
    item_weight_unit: str = Field(validation_alias="item_weight_units_type")
    # 商品包装高度
    package_height: FloatOrNone2Zero
    # 商品包装高度单位 [原字段 'package_height_units_type']
    package_height_unit: str = Field(validation_alias="package_height_units_type")
    # 商品包装长度
    package_length: FloatOrNone2Zero
    # 商品包装长度单位 [原字段 'package_length_units_type']
    package_length_unit: str = Field(validation_alias="package_length_units_type")
    # 商品包装宽度
    package_width: FloatOrNone2Zero
    # 商品包装宽度单位 [原字段 'package_width_units_type']
    package_width_unit: str = Field(validation_alias="package_width_units_type")
    # 商品包装重量
    package_weight: FloatOrNone2Zero
    # 商品包装重量单位 [原字段 'package_weight_units_type']
    package_weight_unit: str = Field(validation_alias="package_weight_units_type")


class ListingOperator(BaseModel):
    """商品负责人."""

    # 负责人的领星帐号ID (Account.user_id) [原字段 'principal_uid']
    user_id: int = Field(validation_alias="principal_uid")
    # 负责人的领星帐号显示姓名 (Account.display_name) [原字段 'principal_name']
    user_name: str = Field(validation_alias="principal_name")


class ListingTagInfo(BaseModel):
    """商品标签信息."""

    # 领星标签ID (ListingGlobalTag.tag_id) [原字段 'globalTagId']
    tag_id: str = Field(validation_alias="globalTagId")
    # 领星标签名称 (ListingGlobalTag.tag_name) [原字段 'tagName']
    tag_name: str = Field(validation_alias="tagName")
    # 领星标签颜色 (如: "#FF0000") [原字段 'color']
    tag_color: str = Field(validation_alias="color")


class Listing(BaseModel):
    """商品 Listing 信息."""

    # fmt: off
    # 领星店铺ID (Seller.sid) [sid + msku 唯一标识]
    sid: int
    # 商品国家 (中文) [原字段 'marketplace']
    country: str = Field(validation_alias="marketplace")
    # 商品ASIN码 (Amazon Standard Identification Number)
    asin: str
    # 商品父ASIN码 (变体商品的主ASIN, 无变体则与 asin 相同)
    parent_asin: str
    # 亚马逊商品SKU [原字段 'seller_sku']
    msku: str = Field(validation_alias="seller_sku")
    # 领星本地商品SKU [原字段 'local_sku']
    lsku: str = Field(validation_alias="local_sku")
    # 亚马逊FBA自生成的商品编号
    fnsku: str
    # 领星本地商品名称 [原字段 'local_name']
    product_name: str = Field(validation_alias="local_name")
    # 品牌名称 [原字段 'brand_name']
    brand: str = Field(validation_alias="seller_brand")
    # 商品标题 [原字段 'item_name']
    title: str = Field(validation_alias="item_name")
    # 商品略缩图链接 [原字段 'small_image_url']
    thumbnail_url: str = Field(validation_alias="small_image_url")
    # 产品类型 (1: 普通产品, 2: 多属性产品) [原字段 'store_type']
    product_type: int = Field(validation_alias="store_type")
    # 商品价格的货币代码
    currency_code: str
    # 商品标准价 (不包含促销, 运费, 积分) [原字段 'price']
    standard_price: FloatOrNone2Zero = Field(validation_alias="price")
    # 商品优惠价 [原字段 'listing_price']
    sale_price: FloatOrNone2Zero = Field(validation_alias="listing_price")
    # 商品运费
    shipping: FloatOrNone2Zero
    # 商品积分 (适用于日本站点)
    points: FloatOrNone2Zero
    # 商品到手价 (包含促销, 运费, 积分)
    landed_price: FloatOrNone2Zero
    # 商品昨天的总销售额 [原字段 'yesterday_amount']
    sales_amt_1d: FloatOrNone2Zero = Field(validation_alias="yesterday_amount")
    # 商品7天的总销售额 [原字段 'seven_amount']
    sales_amt_7d: FloatOrNone2Zero = Field(validation_alias="seven_amount")
    # 商品14天的总销售额 [原字段 'fourteen_amount']
    sales_amt_14d: FloatOrNone2Zero = Field(validation_alias="fourteen_amount")
    # 商品30天的总销售额 [原字段 'thirty_amount']
    sales_amt_30d: FloatOrNone2Zero = Field(validation_alias="thirty_amount")
    # 商品昨天的总销量 [原字段 'yesterday_volume']
    sales_qty_1d: IntOrNone2Zero = Field(validation_alias="yesterday_volume")
    # 商品7天的总销量 [原字段 'total_volume']
    sales_qty_7d: IntOrNone2Zero = Field(validation_alias="total_volume")
    # 商品14天的总销量 [原字段 'fourteen_volume']
    sales_qty_14d: IntOrNone2Zero = Field(validation_alias="fourteen_volume")
    # 商品30天的总销量 [原字段 'thirty_volume']
    sales_qty_30d: IntOrNone2Zero = Field(validation_alias="thirty_volume")
    # 商品7天的日均销量 [原字段 'average_seven_volume']
    sales_avg_qty_7d: FloatOrNone2Zero = Field(validation_alias="average_seven_volume")
    # 商品14天的日均销量 [原字段 'average_fourteen_volume']
    sales_avg_qty_14d: FloatOrNone2Zero = Field(validation_alias="average_fourteen_volume")
    # 商品30天的日均销量 [原字段 'average_thirty_volume']
    sales_avg_qty_30d: FloatOrNone2Zero = Field(validation_alias="average_thirty_volume")
    # 商品所属主类目 [原字段 'seller_category_new']
    category: list[str] = Field(validation_alias="seller_category_new")
    # 商品主类目排名 [原字段 'seller_rank']
    category_rank: int = Field(validation_alias="seller_rank")
    # 商品小类和排名列表 [原字段 'small_rank']
    subcategories: list[ListingSubcategory] = Field(validation_alias="small_rank")
    # 商品评价数量 [原字段 'review_num']
    review_count: int = Field(validation_alias="review_num")
    # 商品评价星级 [原字段 'last_star']
    review_stars: FloatOrNone2Zero = Field(validation_alias="last_star")
    # 商品配送方式 (如: "FBA" 或 "FBM") [原字段 'fulfillment_channel_type']
    fulfillment_channel: str = Field(validation_alias="fulfillment_channel_type")
    # FBM 可售库存数量 [原字段 'quantity']
    mfn_fulfillable: int = Field(validation_alias="quantity")
    # FBA 在库可售的库存数量 [原字段 'afn_fulfillable_quantity']
    afn_fulfillable: int = Field(validation_alias="afn_fulfillable_quantity")
    # FBA 在库不可售的库存数量 [原字段 'afn_unsellable_quantity']
    afn_unsellable: int = Field(validation_alias="afn_unsellable_quantity")
    # FBA 在库待调仓的库存数量 [原字段 'reserved_fc_processing']
    afn_reserved_fc_processing: int = Field(validation_alias="reserved_fc_processing")
    # FBA 在库调仓中的库存数量 [原字段 'reserved_fc_transfers']
    afn_reserved_fc_transfers: int = Field(validation_alias="reserved_fc_transfers")
    # FBA 在库待发货的库存数量 [原字段 'reserved_customerorders']
    afn_reserved_customer_order: int = Field(validation_alias="reserved_customerorders")
    # FBA 发货计划入库的库存数量 [原字段 'afn_inbound_working_quantity']
    afn_inbound_working: int = Field(validation_alias="afn_inbound_working_quantity")
    # FBA 发货在途的库存数量 [原字段 'afn_inbound_shipped_quantity']
    afn_inbound_shipped: int = Field(validation_alias="afn_inbound_shipped_quantity")
    # FBA 发货入库接收中的库存数量 [原字段 'afn_inbound_receiving_quantity']
    afn_inbound_receiving: int = Field(validation_alias="afn_inbound_receiving_quantity")
    # 商品状态 (0: 停售, 1: 在售)
    status: int
    # 商品是否已删除 (0: 未删除, 1: 已删除) [原字段 'is_delete']
    deleted: int = Field(validation_alias="is_delete")
    # 商品创建时间 (时区时间) [原字段 'open_date_display']
    create_time: str = Field(validation_alias="open_date_display")
    # 商品开售日期 (如: "2023-06-23") [原字段 'on_sale_time']
    on_sale_date: str = Field(validation_alias="on_sale_time")
    # 商品首次下单日期 (如: "2023-06-23") [原字段 'first_order_time']
    first_order_date: str = Field(validation_alias="first_order_time")
    # 亚马逊更新时间 (UTC时间) [原字段 'listing_update_date']
    update_time_utc: str = Field(validation_alias="listing_update_date")
    # 领星配对时间 (北京时间) [原字段 'pair_update_time']
    pair_time_cnt: str = Field(validation_alias="pair_update_time")
    # 商品尺寸和重量 [原字段 'dimension_info']
    dimensions: list[ListingDimension] = Field(validation_alias="dimension_info")
    # 商品负责人 [原字段 'principal_info']
    operators: list[ListingOperator] = Field(validation_alias="principal_info")
    # 商品标签信息 [原字段 'global_tags']
    tags: list[ListingTagInfo] = Field(validation_alias="global_tags")
    # fmt: on


class Listings(ResponseV1):
    """商品Listing."""

    data: list[Listing]


# . Edit Listing Result [Generic]
class EditListing(BaseModel):
    """更新商品 Listing 的结果."""

    # 总更新个数
    total: IntOrNone2Zero
    # 更新成功个数 [原字段 'success_num']
    success: IntOrNone2Zero = Field(validation_alias="success")
    # 更新失败个数 [原字段 'failure_num']
    failure: IntOrNone2Zero = Field(validation_alias="error")


class EditListingResult(ResponseResult):
    """更新商品 Listing 的结果."""

    data: EditListing


# . Edit Listing Price
class EditListingPriceFailureDetail(BaseModel):
    """更新商品价格失败的详情."""

    # 领星店铺ID (Seller.sid)
    sid: int
    # 商品ASIN码 (Listing.asin)
    asin: str
    # 亚马逊卖家SKU (Listing.msku)
    msku: str
    # 错误信息 [原字段 'msg']
    message: str = Field(validation_alias="msg")


class EditListingPrice(BaseModel):
    """更新商品价格的结果."""

    # fmt: off
    # 更新成功个数 [原字段 'success_num']
    success: IntOrNone2Zero = Field(validation_alias="success_num")
    # 更新失败个数 [原字段 'failure_num']
    failure: IntOrNone2Zero = Field(validation_alias="failure_num")
    # 更新失败的详情
    failure_detail: list[EditListingPriceFailureDetail]
    # fmt: on

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("failure_detail", mode="before")
    def _validate_failure_detail(cls, v):
        if v is None:
            return []
        return [EditListingPriceFailureDetail.model_validate(i) for i in v]


class EditListingPricesResult(ResponseResult):
    """更新商品价格的结果."""

    data: EditListingPrice


# . Listing Global Tag
class ListingGlobalTag(BaseModel):
    """商品 Listing 标签."""

    # 领星标签ID [原字段 'global_tag_id']
    tag_id: str = Field(validation_alias="global_tag_id")
    # 领星标签名称
    tag_name: str
    # 标签类型 [原字段 'type']
    tag_type: str = Field(validation_alias="type")
    # 标签的关联对象 [原字段 'tag_object']
    tag_attachment: str = Field(validation_alias="tag_object")
    # 标签当前关联对象的总数量 [原字段 'relation_count']
    tag_attachment_count: int = Field(validation_alias="relation_count")
    # 标签最初创建者 (Account.display_name) [原字段 'create_by_name']
    created_by: StrOrNone2Blank = Field(validation_alias="create_by_name")
    # 标签创建时间 (北京时间) [原字段 'create_by']
    create_time: str = Field(validation_alias="create_by")
    # 标签最后编辑者 (Account.display_name) [原字段 'modify_by_name']
    modified_by: StrOrNone2Blank = Field(validation_alias="modify_by_name")
    # 标签修改时间 (北京时间) [原字段 'modify_by']
    modify_time: str = Field(validation_alias="modify_by")


class ListingGlobalTags(ResponseV1):
    """商品 Listing 标签列表."""

    data: list[ListingGlobalTag]


# . Listing Tag
class ListingTag(BaseModel):
    """商品 Listing 关联标签."""

    # 领星店铺ID (Seller.sid)
    sid: int
    # 亚马逊卖家SKU (Listing.msku) [原字段 'relation_id']
    msku: str = Field(validation_alias="relation_id")
    # 标签信息列表 [原字段 'tag_infos']
    tags: list[base_schema.TagInfo] = Field(validation_alias="tag_infos")


class ListingTags(ResponseV1):
    """商品 Listing 关联标签列表."""

    data: list[ListingTag]


# . Listing FBA Fee
class ListingFbaFee(BaseModel):
    """商品 Listing 的 FBA 费用."""

    # 领星店铺ID (Seller.sid)
    sid: int
    # 亚马逊卖家SKU (Listing.msku)
    msku: str
    # 预估FBA费用
    fba_fee: FloatOrNone2Zero
    # 预估FBA费用货币代码 [原字段 'fba_fee_currency_code']
    currency_code: str = Field(validation_alias="fba_fee_currency_code")


class ListingFbaFees(ResponseV1):
    """商品 Listing 的 FBA 费用列表."""

    data: list[ListingFbaFee]


# . Edit Listing FBM Inventory
class EditListingFbmFailureDetail(BaseModel):
    """更新商品 FBM 库存失败的详情."""

    # 领星店铺ID (Seller.sid) [原字段 'storeId']
    sid: int = Field(validation_alias="storeId")
    # 商品ASIN码 (Listing.asin)
    asin: str
    # 亚马逊卖家SKU (Listing.msku)
    msku: str
    # 错误信息 [原字段 'msg']
    message: str = Field(validation_alias="msg")


class EditListingFbm(BaseModel):
    """更新商品 FBM 库存的结果."""

    # fmt: off
    # 更新成功个数 [原字段 'successNum']
    success: int = Field(validation_alias="successNum")
    # 更新失败个数 [原字段 'failureNum']
    failure: int = Field(validation_alias="failureNum")
    # 更新失败的详情 [原字段 'failureDetail']
    failure_detail: list[EditListingFbmFailureDetail] = Field(validation_alias="failureDetail")
    # fmt: on


class EditListingFbmsResult(ResponseResult):
    """更新商品 FBM 库存的结果."""

    data: EditListingFbm


# . Listing Operation Log
class ListingOperationLog(BaseModel):
    # 领星店铺ID (Seller.sid)
    sid: int
    # 操作用户名称 (Account.display_name) [原字段 'operate_user']
    operator: str = Field(validation_alias="operate_user")
    # 操作类型 [原字段 'operate_type']
    operation_type: int = Field(validation_alias="operate_type")
    # 操作类型说明 [原字段 'operate_type_text']
    operation_type_desc: str = Field(validation_alias="operate_type_text")
    # 操作时间 (北京时间) [原字段 'operate_time']
    operation_time: str = Field(validation_alias="operate_time")
    # 操作详情 [原字段 'operate_detail']
    operation_detail: str = Field(validation_alias="operate_detail")


class ListingOperationLogs(ResponseV1):
    """商品 Listing 操作日志."""

    data: list[ListingOperationLog]


# 销售 - 平台订单 ----------------------------------------------------------------------------------------------------------------
# . Order
class OrderItem(BaseModel):
    """平台的订单商品."""

    # 商品ASIN (Listing.asin)
    asin: str
    # 亚马逊卖家SKU (Listing.msku) [原字段 'seller_sku']
    msku: str = Field(validation_alias="seller_sku")
    # 领星本地SKU (Listing.lsku) [原字段 'local_sku']
    lsku: str = Field(validation_alias="local_sku")
    # 领星本地商品名 (Listing.product_name) [原字段 'local_name']
    product_name: str = Field(validation_alias="local_name")
    # 订购数量 [原字段 'quantity_ordered']
    order_qty: int = Field(validation_alias="quantity_ordered")
    # 订单状态
    order_status: str


class Order(BaseModel):
    """平台订单."""

    # fmt: off
    # 领星店铺ID (Seller.sid)
    sid: int
    # 领星店铺名称 (Seller.name)
    seller_name: str
    # 亚马逊订单ID
    amazon_order_id: str
    # 销售渠道 (如: "Amazon.com")
    sales_channel: str
    # 配送方式 ("AFN" 或 "MFN")
    fulfillment_channel: str
    # 物流追踪号码
    tracking_number: str
    # 订单状态
    order_status: str
    # 是否为退货订单 (0: 否, 1: 是)
    is_return_order: int
    # 退货订单的状态 (0: 未退货, 1: 退货中, 2: 完成退货/退款, 3: 被标记为领星本地的退货订单) [原字段 'is_return']
    return_order_status: int = Field(validation_alias="is_return", description="退货订单的状态")
    # 是否为换货订单 (0: 否, 1: 是)
    is_replacement_order: int
    # 换货订单的状态 (0: 未换货, 1: 完成换货) [原字段 'is_replaced_order']
    replacement_order_status: int = Field(validation_alias="is_replaced_order")
    # 是否为多渠道配送订单 (0: 否, 1: 是) [2023年后的多渠道订单数据均不在此接口返回]
    is_mcf_order: int
    # 是否被标记为领星本地的推广订单 (0: 否, 1: 是) [原字段 'is_assessed']
    is_promotion_tagged: int = Field(validation_alias="is_assessed")
    # 订单金额的货币代码 [原字段 'order_total_currency_code']
    order_currency_code: str = Field(validation_alias="order_total_currency_code")
    # 订单总金额 [原字段 'order_total_amount']
    order_amt: FloatOrNone2Zero = Field(validation_alias="order_total_amount")
    # 退款金额 [原字段 'refund_amount']
    refund_amt: FloatOrNone2Zero = Field(validation_alias="refund_amount")
    # 买家名字
    buyer_name: str
    # 买家电子邮箱
    buyer_email: str
    # 买家电话号码 [原字段 'phone']
    buyer_phone: str = Field(validation_alias="phone")
    # 买家地址 [原字段 'address']
    buyer_address: str = Field(validation_alias="address")
    # 买家邮政编码 [原字段 'postal_code']
    buyer_postcode: str = Field(validation_alias="postal_code")
    # 订购时间 (时区时间, 如: '2025-07-07T19:39:47Z') [原字段 'purchase_date']
    purchase_time: str = Field(validation_alias="purchase_date")
    # 订购时间 (UTC时间) [原字段 'purchase_date_local_utc']
    purchase_time_utc: str = Field(validation_alias="purchase_date_local_utc")
    # 订购时间 (站点时间) [原字段 'purchase_date_local']
    purchase_time_loc: str = Field(validation_alias="purchase_date_local")
    # 发货时间 (时区时间, 如: '2025-07-08T02:17:27+00:00') [原字段 'shipment_date']
    shipment_time: str = Field(validation_alias="shipment_date")
    # 发货时间 (UTC时间) [原字段 'shipment_date_utc']
    shipment_time_utc: str = Field(validation_alias="shipment_date_utc")
    # 发货时间 (站点时间) [原字段 'shipment_date_local']
    shipment_time_loc: str = Field(validation_alias="shipment_date_local")
    # 最早发货时间 (时区时间, 如: '2025-07-08T06:59:59Z') [原字段 'earliest_ship_date']
    earliest_ship_time: str = Field(validation_alias="earliest_ship_date")
    # 最早发货时间 (UTC时间) [原字段 'earliest_ship_date_utc']
    earliest_ship_time_utc: str = Field(validation_alias="earliest_ship_date_utc")
    # 付款确认时间 (时区时间, 如: '2025-07-15T17:14:53Z') [原字段 'posted_date_utc']
    posted_time: str = Field(validation_alias="posted_date_utc")
    # 付款确认时间 (UTC时间) [原字段 'posted_date']
    posted_time_utc: str = Field(validation_alias="posted_date")
    # 亚马逊订单更新时间 (UTC时间) [原字段 'last_update_date_utc']
    update_time_utc: str = Field(validation_alias="last_update_date_utc")
    # 亚马逊订单更新时间 (站点时间) [原字段 'last_update_date']
    update_time_loc: str = Field(validation_alias="last_update_date")
    # 领星订单更新时间 (北京时间) [原字段 'gmt_modified']
    modify_time_cnt: str = Field(validation_alias="gmt_modified")
    # 领星订单更新时间 (UTC时间) [原字段 'gmt_modified_utc']
    modify_time_utc: str = Field(validation_alias="gmt_modified_utc")
    # 订单中的商品列表 [原字段 'item_list']
    items: list[OrderItem] = Field(validation_alias="item_list")
    # fmt: on


class Orders(ResponseV1):
    """平台订单列表."""

    data: list[Order]


# . Order Detail Item
class OrderDetailItem(BaseModel):
    """平台订单详情中的商品.

    ## 与领星前台对比缺失字段
    - 站外推广费的'佣金', 此字段在前台订单详情中显示并会比计入毛利率, 但在此接口中未返回.

    ## 与领星前台对比无效字段
    - 在前台订单详情中会显示 '平台支出->其他', 但在此接口返回的 'other_amount'
      字段中为空字符串.
    """

    # fmt: off
    # 领星店铺ID
    sid: int
    # 领星本地商品ID
    product_id: int
    # 领星订单详情ID [原字段 'id']
    order_id: int = Field(validation_alias="id")
    # 亚马逊订单商品编码 [订单下唯一键, 但亚马逊返回值可能会发生变更]
    order_item_id: str
    # 商品ASIN
    asin: str
    # 亚马逊卖家SKU [原字段 'seller_sku']
    msku: str = Field(validation_alias="seller_sku")
    # 领星本地商品SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 领星本地商品名称
    product_name: str
    # 商品 ASIN 链接
    asin_url: str
    # 商品图片链接 [原字段 'pic_url']
    image_url: str = Field(validation_alias="pic_url")
    # 商品标题
    title: str
    # 订单商品总数量 [原字段 'quantity_ordered']
    order_qty: int = Field(validation_alias="quantity_ordered")
    # 订单已发货数量 [原字段 'quantity_shipped']
    shipped_qty: int = Field(validation_alias="quantity_shipped")
    # 商品促销标识 [原字段 'promotion_ids']
    promotion_labels: list[str] = Field(validation_alias="promotion_ids")
    # 商品价格标识 (如: "Business Price") [原字段 'price_designation']
    price_label: str = Field(validation_alias="price_designation")
    # 商品销售单价 [原字段 'unit_price_amount']
    item_price: FloatOrNone2Zero = Field(validation_alias="unit_price_amount")
    # 商品销售金额 [原字段 'item_price_amount']
    sales_amt: FloatOrNone2Zero = Field(validation_alias="item_price_amount")
    # 商品销售金额税费 [原字段 'item_tax_amount']
    sales_tax_amt: FloatOrNone2Zero = Field(validation_alias="item_tax_amount")
    # 商品销售实收金额 [原字段 'sales_price_amount']
    sales_received_amt: FloatOrNone2Zero = Field(validation_alias="sales_price_amount")
    # 买家支付运费金额 [原字段 'shipping_price_amount']
    shipping_credits_amt: FloatOrNone2Zero = Field(validation_alias="shipping_price_amount")
    # 买家支付运费税费 [原字段 'shipping_tax_amount']
    shipping_credits_tax_amt: FloatOrNone2Zero = Field(validation_alias="shipping_tax_amount")
    # 买家支付礼品包装费金额 [原字段 'gift_wrap_price_amount']
    giftwrap_credits_amt: FloatOrNone2Zero = Field(validation_alias="gift_wrap_price_amount")
    # 买家支付礼品包装费税费 [原字段 'gift_wrap_tax_amount']
    giftwrap_credits_tax_amt: FloatOrNone2Zero = Field(validation_alias="gift_wrap_tax_amount")
    # 买家支付货到付款服务费金额 (Cash On Delivery) [原字段 'cod_fee_amount']
    cod_service_credits_amt: FloatOrNone2Zero = Field(validation_alias="cod_fee_amount")
    # 卖家商品促销折扣金额 [原字段 'promotion_discount_amount']
    promotion_discount_amt: FloatOrNone2Zero = Field(validation_alias="promotion_discount_amount")
    # 卖家商品促销折扣税费 [原字段 'promotion_discount_tax_amount']
    promotion_discount_tax_amt: FloatOrNone2Zero = Field(validation_alias="promotion_discount_tax_amount")
    # 卖家商品运费折扣金额 [原字段 'shipping_discount_amount']
    shipping_discount_amt: FloatOrNone2Zero = Field(validation_alias="shipping_discount_amount")
    # 卖家商品运费折扣税费 [原字段 'shipping_discount_tax_amount']
    shipping_discount_tax_amt: FloatOrNone2Zero = Field(validation_alias="shipping_discount_tax_amount")
    # 亚马逊积分抵付款金额 (日本站) [原字段 'points_monetary_value_amount']
    points_discount_amt: FloatOrNone2Zero = Field(validation_alias="points_monetary_value_amount")
    # 卖家货到付款服务费折扣金额 (Cash On Delivery) [原字段 'cod_fee_discount_amount']
    cod_service_discount_amt: FloatOrNone2Zero= Field(validation_alias="cod_fee_discount_amount")
    # 卖家总折扣金额 [原字段 'promotion_amount']
    total_discount_amt: FloatOrNone2Zero = Field(validation_alias="promotion_amount")
    # 卖家总代扣税费 [原字段 'tax_amount']
    withheld_tax_amt: FloatOrNone2Zero = Field(validation_alias="tax_amount")
    # 卖家总代扣税费是否为预估值 (0: 否, 1: 是) [原字段 'item_tax_amount_estimated']
    withheld_tax_amt_estimated: int = Field(validation_alias="item_tax_amount_estimated")
    # 亚马逊FBA配送费用 [原字段 'fba_shipment_amount']
    fulfillment_fee: FloatOrNone2Zero = Field(validation_alias="fba_shipment_amount")
    # 亚马逊FBA配送费用是否为预估值 (0: 否, 1: 是) [原字段 'fba_shipment_amount_estimated']
    fulfillment_fee_estimated: int = Field(validation_alias="fba_shipment_amount_estimated")
    # 亚马逊销售佣金 [原字段 'commission_amount']
    referral_fee: FloatOrNone2Zero = Field(validation_alias="commission_amount")
    # 亚马逊销售佣金是否为预估值 (0: 否, 1: 是) [原字段 'commission_amount_estimated']
    referral_fee_estimated: int = Field(validation_alias="commission_amount_estimated")
    # 亚马逊收取的其他费用 (如: Amazon Exlusives Program) [原字段 'other_amount']
    other_fee: FloatOrNone2Zero = Field(validation_alias="other_amount")  
    # 用户自定义推广费用名称 (如: 推广费) [原字段 'fee_name']
    user_promotion_type: str = Field(validation_alias="fee_name")
    # 用户自定义推广费用货币代码 [原字段 'fee_currency']
    user_promotion_currency_code: str = Field(validation_alias="fee_currency")
    # 用户自定义推广费用货币符号 [原字段 'fee_icon']
    user_promotion_currency_icon: str = Field(validation_alias="fee_icon")
    # 用户自定义推广费用本金 (原币种) [原字段 'fee_cost']
    user_promotion_currency_fee: FloatOrNone2Zero = Field(validation_alias="fee_cost")
    # 用户自定义推广费用本金 (店铺币种) [原字段 'fee_cost_amount']
    user_promotion_fee: FloatOrNone2Zero = Field(validation_alias="fee_cost_amount")
    # 商品采购头程费用金额 [原字段 'cg_transport_costs']
    cost_of_logistics_amt: FloatOrNone2Zero = Field(validation_alias="cg_transport_costs")
    # 商品采购成本金额 [原字段 'cg_price']
    cost_of_goods_amt: FloatOrNone2Zero = Field(validation_alias="cg_price")
    # 商品毛利润金额 [原字段 'profit']
    profit_amt: FloatOrNone2Zero = Field(validation_alias="profit")
    # 商品状况（卖家提供）[原字段 'condition_note']
    item_condition: str = Field(validation_alias="condition_note")
    # 商品状况ID (卖家提供) [原字段 'condition_id']
    item_condition_id: str = Field(validation_alias="condition_id")
    # 商品子状况ID (卖家提供) [原字段 'condition_subtype_id']
    item_condition_sub_id: str = Field(validation_alias="condition_subtype_id")
    # 礼品包装级别（买家提供) [原字段 'gift_wrap_level']
    giftwrap_level: str = Field(validation_alias="gift_wrap_level")
    # 礼品包装信息（买家提供）[原字段 'gift_message_text']
    giftwap_message: str = Field(validation_alias="gift_message_text")
    # 计划交货开始时间 [原字段 'scheduled_delivery_start_date']
    scheduled_delivery_start_time: str = Field(validation_alias="scheduled_delivery_start_date")
    # 计划交货结束时间 [原字段 'scheduled_delivery_end_date']
    scheduled_delivery_end_time: str = Field(validation_alias="scheduled_delivery_end_date")
    # 商品自定义JSON数据
    customized_json: str
    # fmt: on


class OrderDetail(BaseModel):
    """平台订单详情.

    包含订单的所有字段, 以及商品的详细信息.
    """

    # fmt: off
    # 领星店铺ID (Seller.sid)
    sid: int
    # 亚马逊订单ID
    amazon_order_id: str
    # 销售渠道 (如: "Amazon.com")
    sales_channel: str
    # 配送方式 ("AFN" 或 "MFN")
    fulfillment_channel: str
    # 订单类型
    order_type: str
    # 订单状态
    order_status: str
    # 是否为退货订单 (0: 否, 1: 是)
    is_return_order: int
    # 退货订单的状态 (0: 未退货, 1: 退货中, 2: 完成退货/退款, 3: 被标记为领星本地的退货订单) [原字段 'is_return']
    return_order_status: int = Field(validation_alias="is_return")
    # 是否为换货订单 (0: 否, 1: 是)
    is_replacement_order: int
    # 换货订单的状态 (0: 未换货, 1: 完成换货) [原字段 'is_replaced_order']
    replacement_order_status: int = Field(validation_alias="is_replaced_order")
    # 是否为促销折扣订单 (0: 否, 1: 是) [原字段 'is_promotion']
    # 当 OrderDetailItem.promotion_discount_amt > 0 时,
    # 此字段为 1, 其他 discount_amt 不计做 promotioin 类型
    is_promotion_order: int = Field(validation_alias="is_promotion")
    # 是否为B2B订单 (0: 否, 1: 是) [原字段 'is_business_order']
    is_b2b_order: int = Field(validation_alias="is_business_order")
    # 是否为Prime订单 (0: 否, 1: 是) [原字段 'is_prime']
    is_prime_order: int = Field(validation_alias="is_prime")
    # 是否为优先配送订单 (0: 否, 1: 是)
    is_premium_order: int
    # 是否为多渠道配送订单 (0: 否, 1: 是)
    is_mcf_order: int
    # 是否被用户标记为领星本地的推广订单 (0: 否, 1: 是) [原字段 'is_assessed']
    is_user_promotion_order: int = Field(validation_alias="is_assessed")
    # 订单已发货数量 [原字段 'number_of_items_shipped']
    shipped_qty: IntOrNone2Zero = Field(validation_alias="number_of_items_shipped")
    # 订单未发货数量 [原字段 'number_of_items_unshipped']
    unshipped_qty: IntOrNone2Zero = Field(validation_alias="number_of_items_unshipped")
    # 订单金额的货币代码 [原字段 'order_total_currency_code']
    order_currency_code: str = Field(validation_alias="currency")
    # 订单金额的货币图标 [原字段 'icon']
    order_currency_icon: str = Field(validation_alias="icon")
    # 订单销售总金额 [原字段 'order_total_amount']
    order_sales_amt: FloatOrNone2Zero = Field(validation_alias="order_total_amount")
    # 订单金额费用是否含税 (1: 含税, 2: 不含税) [原字段 'taxes_included']
    order_tax_inclusive: int = Field(validation_alias="taxes_included")
    # 订单税务分类 [原字段 'tax_classifications']
    order_tax_class: str = Field(validation_alias="tax_classifications")
    # 订单配送服务级别 [原字段 'ship_service_level']
    shipment_service: str = Field(validation_alias="ship_service_level")
    # 订单配送服务级别类型 [原字段 'shipment_service_level_category']
    shipment_service_category: str = Field(validation_alias="shipment_service_level_category")
    # 采购订单编号 (买家结账时输入)
    purchase_order_number: str
    # 付款方式 ("COD", "CVS", "Other")
    payment_method: str
    # 亚马逊结账 (CBA) 的自定义发货标签 [原字段 'cba_displayable_shipping_label']
    cba_shipping_label: str = Field(validation_alias="cba_displayable_shipping_label")
    # 买家姓名
    buyer_name: str
    # 买家电子邮箱
    buyer_email: str
    # 买家电话号码 [原字段 'phone']
    buyer_phone: str = Field(validation_alias="phone")
    # 买家所在国家 [原字段 'country']
    buyer_country: str = Field(validation_alias="country")
    # 买家所在国家代码 [原字段 'country_code']
    buyer_country_code: str = Field(validation_alias="country_code")
    # 买家所在省/州 [原字段 'state_or_region']
    buyer_state: str = Field(validation_alias="state_or_region")
    # 买家所在城市 [原字段 'city']
    buyer_city: str = Field(validation_alias="city")
    # 买家所在区县 [原字段 'district']
    buyer_district: str = Field(validation_alias="district")
    # 买家地址 [原字段 'address']
    buyer_address: str = Field(validation_alias="address")
    # 买家邮政编码 [原字段 'postal_code']
    buyer_postcode: str = Field(validation_alias="postal_code")
    # 订购时间 (UTC时间) [原字段 'purchase_date_local_utc']
    purchase_time_utc: str = Field(validation_alias="purchase_date_local_utc")
    # 订购时间 (站点时间) [原字段 'purchase_date_local']
    purchase_time_loc: str = Field(validation_alias="purchase_date_local")
    # 发货时间 (站点时间) [原字段 'shipment_date']
    shipment_time_loc: str = Field(validation_alias="shipment_date")
    # 最早发货时间 (UTC时间) [原字段 'earliest_ship_date_utc']
    earliest_ship_time_utc: str = Field(validation_alias="earliest_ship_date_utc")
    # 最早发货时间 (站点时间) [原字段 'earliest_ship_date']
    earliest_ship_time_loc: str = Field(validation_alias="earliest_ship_date")
    # 最晚发货时间 (时区时间) [原字段 'latest_ship_date']
    latest_ship_time: str = Field(validation_alias="latest_ship_date")
    # 付款确认时间 (站点时间) [原字段 'posted_date']
    posted_time_loc: str = Field(validation_alias="posted_date")
    # 亚马逊订单更新时间 (UTC时间) [原字段 'last_update_date_utc']
    update_time_utc: str = Field(validation_alias="last_update_date_utc")
    # 亚马逊订单更新时间 (站点时间) [原字段 'last_update_date']
    update_time_loc: str = Field(validation_alias="last_update_date")
    # 订单中的商品 [原字段 'item_list']
    items: list[OrderDetailItem] = Field(validation_alias="item_list")
    # fmt: on


class OrderDetails(ResponseV1):
    """平台订单详情列表"""

    data: list[OrderDetail]


# . Order After-Sales Order
class AfterSalesOrderRefundDetail(BaseModel):
    """平台订单退款金额的详细信息."""

    # 退款金额类型 (如: "Principal", "ShippingCharge", "Commission")
    type: str
    # 退款金额 (含货币符号) [原字段 'amount']
    amt: str = Field(validation_alias="amount")


class AfterSalesOrderItem(BaseModel):
    """平台售后订单中的商品."""

    # fmt: off
    # 售后订单唯一标, 由多个字段拼接而成 [原字段 'item_identifier']
    uid: str = Field(validation_alias="item_identifier")
    # 售后订单唯一标, 由uid基于md5压缩而成 [原字段 'md5_v2']
    uid_md5: str = Field(validation_alias="md5_v2")
    # 商品ASIN (Listing.asin)
    asin: str
    # 亚马逊卖家SKU (Listing.msku)
    msku: str 
    # 领星本地商品SKU (Listing.lsku) [原字段 'local_sku']
    lsku: str = Field(validation_alias="local_sku")
    # 领星本地商品名称 (Listing.product_name) [原字段 'local_name']
    product_name: str = Field(validation_alias="local_name")
    # 商品 ASIN 链接
    asin_url: str
    # 商品略缩图链接 [原字段 'small_image_url']
    thumbnail_url: str = Field(validation_alias="small_image_url")
    # 商品标题 [原字段 'item_name']
    title: str = Field(validation_alias="item_name")
    # 售后类型 (如: "退款", "退货", "换货") [原字段 'after_type']
    service_type: str = Field(validation_alias="after_type")
    # 售后数量 [原字段 'after_quantity']
    service_qty: int = Field(validation_alias="after_quantity")
    # 售后原因 [原字段 'after_reason']
    service_reason: str = Field(validation_alias="after_reason")
    # 订单退款金额 (含货币符号) [原字段 'refund_amount']
    order_refund_amt: str  = Field(validation_alias="refund_amount")
    # 订单退款金额详情 [原字段 'refund_amount_details']
    order_refund_amt_details: list[AfterSalesOrderRefundDetail] = Field(validation_alias="refund_amount_details")
    # 订单退款成本 (含货币符号) [原字段 'refund_cost']
    order_refund_cost: str = Field(validation_alias="refund_cost")
    # 订单退款成本详情 [原字段 'refund_cost_details']
    order_refund_cost_details: list[AfterSalesOrderRefundDetail] = Field(validation_alias="refund_cost_details")
    # 退货状态, 如 "Approved" [原字段 'return_status']
    order_return_status: str = Field(validation_alias="return_status")
    # 换货订单号
    exchange_order_number: str
    # LPN编码号
    lpn_number: str
    # RMA订单号 [原字段 'rma_order_number']
    rma_number: str = Field(validation_alias="rma_order_number")
    # 运单号
    waybill_number: str
    # 承运商
    carriers: str
    # 买家备注
    buyer_note: str = Field(validation_alias="buyers_note")
    # 库存属性
    inventory_attributes: str
    # 售后时间 (站点时间) [原字段 'service_time']
    service_time_loc: str = Field(validation_alias="after_time")
    # 售后间隔天数 [原字段 'after_interval']
    service_interval_days: str = Field(validation_alias="after_interval")
    # 领星订单更新时间 (北京时间) [原字段 'gmt_modified']
    modify_time_cnt: str = Field(validation_alias="data_update_time")
    # fmt: on


class AfterSalesOrder(BaseModel):
    """平台售后订单"""

    # fmt: off
    # 领星店铺ID (Seller.sid)
    sid: int
    # 领星售后订单自增ID (非唯一键) [原字段 'id']
    after_sales_id: int = Field(validation_alias="id")
    # 亚马逊订单ID (Order.amazon_order_id)
    amazon_order_id: str
    # 关联ID
    correlation_id: int
    # 商品ASIN (Listing.asin)
    asin: str
    # 亚马逊卖家SKU (Listing.msku)
    msku: str
    # 店铺名称+国家 (如: "领星店铺 美国")
    seller_country: str
    # 是否为多渠道配送订单 (0: 默认值, 1: 普通订单, 2: 多渠道订单)
    is_mcf_order: int
    # 送货方式 ("FBA", "FBM")
    delivery_type: str
    # 售后类型 (如: ["退款","退货","换货"]) [原字段 'after_type_tag']
    service_type: list[str] = Field(validation_alias="after_type_tag")
    # 订单销售总金额 [原字段 'order_total_amount_number']
    order_sales_amt: FloatOrNone2Zero = Field(validation_alias="order_total_amount_number")
    # 订单销售总金额的货币符号 (如: "$" 或 "") [原字段 'order_total_amount_currency_code']
    order_sales_currency_icon: str = Field(validation_alias="order_total_amount_currency_code")
    # 订单退款总金额 [原字段 'total_refund_amount_number']
    order_refund_amt: FloatOrNone2Zero = Field(validation_alias="total_refund_amount_number")
    # 订单退款总金额的货币符号 (如: "$" 或 "") [原字段 'total_refund_amount_currency_code']
    order_refund_currency_icon: str = Field(validation_alias="total_refund_amount_currency_code")
    # 订单退款成本 [原字段 'total_refund_cost_number']
    order_refund_cost_amt: FloatOrNone2Zero = Field(validation_alias="total_refund_cost_number")
    # 订单退款成本的货币符号 (如: "$" 或 "") [原字段 'total_refund_cost_currency_code']
    roder_refund_cost_currency_icon: str = Field(validation_alias="total_refund_cost_currency_code")
    # 订购时间 (站点时间) [原字段 'purchase_time']
    purchase_time_loc: str = Field(validation_alias="purchase_time")
    # 售后时间 (站点时间) [原字段 'deal_time']
    # 如同一个订单存在多个售后订单, 需以 items>>service_time_loc 为准
    service_time_loc: str = Field(validation_alias="deal_time")
    # 售后间隔天数 [原字段 'interval_days']
    service_interval_days: int = Field(validation_alias="interval_days")
    # 领星订单更新时间 (北京时间) [原字段 'gmt_modified']
    # 如同一个订单存在多个售后订单, 需以 items>>modify_time_cnt 为准
    modify_time_cnt: str = Field(validation_alias="gmt_modified")
    # 售后订单中的商品列表 [原字段 'item_list']
    items: list[AfterSalesOrderItem] = Field(validation_alias="item_list")
    # fmt: on


class AfterSalesOrders(ResponseV1):
    """平台售后订单列表."""

    data: list[AfterSalesOrder]


# . Order MCF Order
class McfOrderItem(BaseModel):
    """多渠道订单中的商品"""

    # 商品ASIN (Listing.asin)
    asin: str
    # 亚马逊卖家SKU (Listing.msku)
    msku: str
    # 领星本地SKU (Listing.lsku) [原字段 'local_sku']
    lsku: str = Field(validation_alias="local_sku")
    # 亚马逊FBA自生成的商品编号 (Listing.fnsku)
    fnsku: str
    # 领星本地商品名称 (Listing.product_name) [原字段 'local_name']
    product_name: str = Field(validation_alias="local_name")
    # 商品标题 [原字段 'item_name']
    title: str = Field(validation_alias="item_name")
    # 商品略缩图链接 [原字段 'small_image_url']
    thumbnail_url: str = Field(validation_alias="small_image_url")
    # 订单商品总数量 [原字段 'quantity']
    order_qty: int = Field(validation_alias="quantity")


class McfOrder(BaseModel):
    """多渠道订单"""

    # 领星店铺ID (Seller.sid)
    sid: int
    # 领星店铺名称 (Seller.name) [原字段 'store_name']
    seller_name: str = Field(validation_alias="store_name")
    # 订单国家 (中文)
    country: str
    # 多渠道亚马逊订单ID
    amazon_order_id: str
    # 多渠道订单配送ID [原字段 'seller_fulfillment_order_id']
    fulfillment_order_id: str = Field(validation_alias="seller_fulfillment_order_id")
    # 订单状态
    order_status: str
    # 订单备注 [原字段 'remark']
    order_note: str = Field(validation_alias="remark")
    # 买家名称
    buyer_name: str
    # 购买时间 (站点时间) [原字段 'purchase_date_local']
    purchase_time_loc: str = Field(validation_alias="purchase_date_local")
    # 发货时间 (UTC时间) [原字段 'ship_date_utc']
    shipment_time_utc: StrOrNone2Blank = Field(validation_alias="ship_date_utc")
    # 发货时间 (站点时间) [原字段 'ship_date']
    shipment_time_loc: StrOrNone2Blank = Field(validation_alias="ship_date")
    # 订单更新时间 (UTC时间) [原字段 'last_update_time']
    update_time_utc: str = Field(validation_alias="last_update_time")
    # 商品列表 [原字段 'listing_info']
    items: list[McfOrderItem] = Field(validation_alias="listing_info")


class McfOrders(ResponseV1, FlattenDataRecords):
    """多渠道总订单"""

    data: list[McfOrder]


# . Order MCF Order Detail
class McfOrderDetailItem(BaseModel):
    """多渠道订单详情中的商品"""

    # 商品ASIN (Listing.asin)
    asin: str
    # 亚马逊卖家SKU (Listing.msku)
    msku: str
    # 领星本地SKU (Listing.lsku) [原字段 'local_sku']
    lsku: str = Field(validation_alias="local_sku")
    # 亚马逊FBA自生成的商品编号 (Listing.fnsku)
    fnsku: str
    # 领星本地商品名称 (Listing.product_name) [原字段 'local_name']
    product_name: str = Field(validation_alias="local_name")
    # 商品标题 [原字段 'item_name']
    title: str = Field(validation_alias="item_name")
    # 商品略缩图链接 [原字段 'small_image_url']
    thumbnail_url: str = Field(validation_alias="small_image_url")
    # 订单商品总数量 [原字段 'quantity']
    order_qty: int = Field(validation_alias="quantity")
    # 订单商品已发货数量 [原字段 'shipped_quantity']
    shipped_qty: int = Field(validation_alias="shipped_quantity")
    # 订单商品已取消数量 [原字段 'cancelled_quantity']
    cancelled_qty: int = Field(validation_alias="cancelled_quantity")
    # 订单商品不可售数量 [原字段 'unfulfillable_quantity']
    unfulfillable_qty: int = Field(validation_alias="unfulfillable_quantity")


class McfOrderDetail(BaseModel):
    """多渠道订单详情"""

    # 领星店铺ID (Seller.sid)
    sid: int
    # 领星店铺名称 (Seller.name) [原字段 'store_name']
    seller_name: str = Field(validation_alias="store_name")
    # 多渠道亚马逊订单ID
    amazon_order_id: str
    # 多渠道订单配送ID [原字段 'seller_fulfillment_order_id']
    fulfillment_order_id: str = Field(validation_alias="seller_fulfillment_order_id")
    # 销售渠道
    sales_channel: str
    # 订单配送服务级别 [原字段 'speed_category']
    shipment_service: str = Field(validation_alias="speed_category")
    # 订单状态
    order_status: str
    # 订单备注 [原字段 'remark']
    order_note: str = Field(validation_alias="remark")
    # 订单装箱备注 [原字段 'displayable_order_comment']
    order_comment: str = Field(validation_alias="displayable_order_comment")
    # 买家名称
    buyer_name: str
    # 买家电子邮箱
    buyer_email: str
    # 买家电话号码 [原字段 'phone']
    buyer_phone: str = Field(validation_alias="phone")
    # 卖家地址 [原字段 'address_line1']
    buyer_address: str = Field(validation_alias="address_line1")
    # 买家邮政编码 [原字段 'postal_code']
    buyer_postcode: str = Field(validation_alias="postal_code")
    # 购买时间 (站点时间) [原字段 'purchase_date_local']
    purchase_time_loc: str = Field(validation_alias="purchase_date_local")
    # 发货时间 (UTC时间) [原字段 'ship_date_utc']
    shipment_time_utc: StrOrNone2Blank = Field(validation_alias="ship_date_utc")
    # 发货时间 (北京时间) [原字段 'ship_date']
    shipment_time_cnt: StrOrNone2Blank = Field(validation_alias="ship_date")
    # 订单详情列表
    items: list[McfOrderDetailItem] = Field(validation_alias="listing_detail_info")


class McfOrderDetails(ResponseV1):
    """多渠道订单详情列表"""

    data: list[McfOrderDetail]


# . Order MCF Order Logistics
class McfOrderLogisticsTrackingEventAddress(BaseModel):
    """多渠道订单物流追踪事件地址"""

    # 追踪事件地址国家
    country: StrOrNone2Blank = ""
    # 追踪事件地址省/州
    state: StrOrNone2Blank = ""
    # 追踪事件地址城市
    city: StrOrNone2Blank = ""


class McfOrderLogisticsTrackingEvent(BaseModel):
    """多渠道订单物流追踪事件"""

    # fmt: off
    # 追踪事件
    event: StrOrNone2Blank
    # 追踪事件编码 [原字段 'eventCode']
    event_code: StrOrNone2Blank = Field(validation_alias="eventCode")
    # 追踪事件描述 [原字段 'eventDescription']
    event_description: StrOrNone2Blank = Field(validation_alias="eventDescription")
    # 追踪事件时间 (站点时间) [原字段 'eventDate']
    event_time_loc: StrOrNone2Blank = Field(validation_alias="eventDate")
    # 追踪事件地址 [原字段 'eventAddress']
    event_address: McfOrderLogisticsTrackingEventAddress = Field(validation_alias="eventAddress")
    # fmt: on

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("event_address", mode="before")
    @classmethod
    def _validate_event_address(cls, v) -> dict | Any:
        return {} if v is None else v


class McfOrderLogisticsPackageItem(BaseModel):
    """多渠道订单物流包裹中的商品"""

    # 领星店铺ID (Seller.sid)
    sid: int
    # 亚马逊SKU (Listing.msku)
    msku: str
    # 商品标题
    title: str
    # 商品数量 [原字段 'quantity']
    item_qty: int = Field(validation_alias="quantity")
    # 包裹编码
    package_number: str


class McfOrderLogisticsPackage(BaseModel):
    """多渠道订单物流包裹信息"""

    # fmt: off
    # 承运人代码
    carrier_code: str
    # 包裹追踪码
    tracking_number: str
    # 包裹编号
    package_number: str
    # 包裹运输状态 [原字段 'current_status']
    package_status: StrOrNone2Blank = Field(validation_alias="current_status")
    # 包裹发货时间 (UTC时间) [原字段 'ship_date']
    shipment_date_utc: str = Field(validation_alias="ship_date")
    # 包裹预计到货时间 (站点时间) [原字段 'estimated_arrival_datetime']
    estimated_arrival_time: str = Field(validation_alias="estimated_arrival_datetime")
    # 包裹追踪事件列表
    tracking_events: list[McfOrderLogisticsTrackingEvent]
    # 包裹内的商品列表 [原字段 'shipItems']
    package_items: list[McfOrderLogisticsPackageItem] = Field(validation_alias="shipItems")
    # fmt: on

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("tracking_events", mode="before")
    @classmethod
    def _validate_tracking_events(cls, v) -> list | Any:
        return [] if v is None else v


class McfOrderLogisticsShipment(BaseModel):
    """多渠道订单物流信息详情"""

    # 亚马逊货件编号
    amazon_shipment_id: str
    # 货件状态 [原字段: 'fulfillment_shipment_status']
    # ('CANCELLED_BY_FULFILLER', 'CANCELLED_BY_SELLER', 'PENDING', 'PROCESSED', 'SHIPPED')
    shipment_status: str = Field(validation_alias="fulfillment_shipment_status")
    # 预计到货时间 (站点时间) [原字段 'estimated_arrival_datetime']
    estimated_arrival_time: str = Field(validation_alias="estimated_arrival_datetime")
    # 包裹详情信息
    packages: list[McfOrderLogisticsPackage]


class McfOrderLogistics(BaseModel):
    """多渠道订单物流信息"""

    # fmt: off
    # 领星店铺ID (Seller.sid)
    sid: int
    # 领星店铺名称 (Seller.name) [原字段 'store_name']
    seller_name: str = Field(validation_alias="store_name")
    # 多渠道亚马逊订单ID
    amazon_order_id: str
    # 多渠道订单配送ID [原字段 'seller_fulfillment_order_id']
    fulfillment_order_id: str = Field(validation_alias="seller_fulfillment_order_id")
    # 销售渠道
    sales_channel: str
    # 订单配送服务级别 [原字段 'speed_category']
    shipment_service: str = Field(validation_alias="speed_category")
    # 订单状态
    order_status: str
    # 订单备注 [原字段 'remark']
    order_note: str = Field(validation_alias="remark")
    # 订单装箱备注 [原字段 'displayable_order_comment']
    order_comment: str = Field(validation_alias="displayable_order_comment")
    # 买家名称
    buyer_name: str
    # 买家电子邮箱
    buyer_email: str
    # 买家电话号码 [原字段 'phone']
    buyer_phone: str = Field(validation_alias="phone")
    # 卖家地址 [原字段 'address_line1']
    buyer_address: str = Field(validation_alias="address_line1")
    # 买家邮政编码 [原字段 'postal_code']
    buyer_postcode: str = Field(validation_alias="postal_code")
    # 购买时间 (站点时间) [原字段 'purchase_date_local']
    purchase_time_loc: str = Field(validation_alias="purchase_date_local")
    # 发货时间 (UTC时间) [原字段 'ship_date_utc']
    shipment_time_utc: StrOrNone2Blank = Field(validation_alias="ship_date_utc")
    # 发货时间 (北京时间) [原字段 'ship_date']
    shipment_time_cnt: StrOrNone2Blank = Field(validation_alias="ship_date")
    # 物流列表 [原字段 'shipment_info']
    shipments: list[McfOrderLogisticsShipment] = Field(validation_alias="shipment_info")
    # fmt: on


class McfOrderLogisticsData(ResponseV1):
    """多渠道订单物流信息列表"""

    data: list[McfOrderLogistics]


# . Order MCF After-Sales Order
class McfAfterSalesReturnItem(BaseModel):
    """多渠道售后退货订单中的商品"""

    # 领星店铺ID (Seller.sid)
    sid: int
    # 商品ASIN (Listing.asin)
    asin: str
    # 亚马逊卖家SKU (Listing.msku)
    msku: str
    # 领星本地SKU (Listing.lsku) [原字段 'local_sku']
    lsku: str = Field(validation_alias="local_sku")
    # 领星本地商品名称 (Listing.product_name) [原字段 'name']
    product_name: str = Field(validation_alias="name")
    # 多渠道订单配送ID [原字段 'order_id']
    fulfillment_order_id: str = Field(validation_alias="order_id")
    # 退货数量 [原字段 'return_quantity']
    return_qty: IntOrNone2Zero = Field(validation_alias="return_quantity")
    # 退货状态
    return_status: str
    # 退货原因
    return_reason: str
    # 退货日期
    return_date: str
    # LNP编码号 [原字段 'lpn']
    lpn_number: str = Field(validation_alias="lpn")
    # 买家备注 [原字段 'customer_comments']
    buyer_note: str = Field(validation_alias="customer_comments")


class McfAfterSalesReplacementItem(BaseModel):
    """多渠道售后换货订单中的商品"""

    # 亚马逊卖家SKU (Listing.msku)
    msku: str
    # 领星本地商品名称 (Listing.product_name) [原字段 'name']
    product_name: str = Field(validation_alias="name")
    # 商品ASIN链接
    asin_url: str
    # 换货原因
    replacement_reason: str
    # 换货时间
    replacement_date: str = Field(validation_alias="shipment_date")


class McfAfterSalesService(BaseModel):
    """多渠道售后服务详情"""

    # fmt: off
    # 退货订单 [原字段 'return_tab']
    return_items: list[McfAfterSalesReturnItem] = Field(validation_alias="return_tab")
    # 换货订单 [原字段 'replace_tab']
    replacement_items: list[McfAfterSalesReplacementItem] = Field(validation_alias="replace_tab")
    # fmt: on


class McfAfterSalesOrder(BaseModel):
    """多渠道售后订单"""

    # fmt: off
    # 领星店铺ID (Seller.sid)
    sid: int
    # 领星店铺名称 (Seller.name) [原字段 'store_name']
    seller_name: str = Field(validation_alias="store_name")
    # 多渠道亚马逊订单ID
    amazon_order_id: str
    # 多渠道订单配送ID [原字段 'seller_fulfillment_order_id']
    fulfillment_order_id: str = Field(validation_alias="seller_fulfillment_order_id")
    # 销售渠道
    sales_channel: str
    # 订单配送服务级别 [原字段 'speed_category']
    shipment_service: str = Field(validation_alias="speed_category")
    # 订单状态
    order_status: str
    # 订单备注 [原字段 'remark']
    order_note: str = Field(validation_alias="remark")
    # 订单装箱备注 [原字段 'displayable_order_comment']
    order_comment: str = Field(validation_alias="displayable_order_comment")
    # 买家名称
    buyer_name: str
    # 买家电子邮箱
    buyer_email: str
    # 买家电话号码 [原字段 'phone']
    buyer_phone: str = Field(validation_alias="phone")
    # 卖家地址 [原字段 'address_line1']
    buyer_address: str = Field(validation_alias="address_line1")
    # 买家邮政编码 [原字段 'postal_code']
    buyer_postcode: str = Field(validation_alias="postal_code")
    # 购买时间 (站点时间) [原字段 'purchase_date_local']
    purchase_time_loc: str = Field(validation_alias="purchase_date_local")
    # 发货时间 (UTC时间) [原字段 'ship_date_utc']
    shipment_time_utc: StrOrNone2Blank = Field(validation_alias="ship_date_utc")
    # 发货时间 (北京时间) [原字段 'ship_date']
    shipment_time_cnt: StrOrNone2Blank = Field(validation_alias="ship_date")
    # 售后服务详情 [原字段 'order_return_replace_tab']
    after_sales_service: McfAfterSalesService = Field(validation_alias="order_return_replace_tab")
    # fmt: on


class McfAfterSalesOrders(ResponseV1):
    """多渠道售后订单列表"""

    data: list[McfAfterSalesOrder]


# . Order MCF Order Transaction
class McfOrderTransactionEventDetail(BaseModel):
    """平台订单退款金额的详细信息."""

    # 事件类型 (如: "FBAPerUnitFulfillmentFee", "FBATransportationFee")
    type: str
    # 事件金额 (含货币符号) [原字段 'currencyAmount']
    amt: str = Field(validation_alias="currencyAmount")


class McfOrderTransactionEvent(BaseModel):
    """多渠道订单交易事件"""

    # fmt: off
    # 领星店铺ID (Seller.sid)
    sid: int
    # 亚马逊卖家SKU (Listing.msku) [原字段 'sellerSku']
    msku: StrOrNone2Blank = Field(validation_alias="sellerSku")
    # 领星本地SKU (Listing.lsku) [原字段 'sku']
    lsku: StrOrNone2Blank = Field(validation_alias="sku")
    # 领星本地商品名称 (Listing.product_name) [原字段 'productName']
    product_name: StrOrNone2Blank = Field(validation_alias="productName")
    # 结算编号 [原字段 'fid']
    transaction_id: str = Field(validation_alias="fid")
    # 交易事件类型 [原字段 'eventType']
    event_type: str = Field(validation_alias="eventType")
    # 交易事件商品数量 [原字段 'quantity']
    event_qty: IntOrNone2Zero = Field(validation_alias="quantity")
    # 交易事件货币代码 [原字段 'currencyCode']
    event_currency_code: str = Field(validation_alias="currencyCode")
    # 交易事件货币金额 (含货币符号) [原字段 'totalCurrencyAmount']
    event_amt: str = Field(validation_alias="totalCurrencyAmount")
    # 交易事件详情 [原字段 'costDetails']
    event_details: list[McfOrderTransactionEventDetail] = Field(validation_alias="costDetails")
    # 交易付款确认时间 (时区时间) [原字段 'postedDateLocale']
    posted_time: str = Field(validation_alias="postedDateLocale")
    # 交易转账时间 (时区时间) [原字段 'fundTransferDateLocale']
    fund_transfer_time: str = Field(validation_alias="fundTransferDateLocale")
    # fmt: on


class McfOrderTransaction(BaseModel):
    """多渠道订单交易信息"""

    # fmt: off
    # 多渠道订单总交易金额 (包含货币符号) [原字段 'totalCurrencyAmounts']
    transaction_amt: StrOrNone2Blank = Field(validation_alias="totalCurrencyAmounts")
    # 多渠道订单交易事件列表 [原字段 'list']
    transaction_events: list[McfOrderTransactionEvent] = Field(validation_alias="list")
    # fmt: on


class McfOrderTransactionData(ResponseV1):
    """多渠道订单交易信息列表"""

    data: McfOrderTransaction


# 销售 - 自发货管理 --------------------------------------------------------------------------------------------------------------
# . FBM Order
class FbmOrder(BaseModel):
    """自发货订单"""

    # 自发货订单号
    order_number: str
    # 订单状态 (1: 同步中, 2: 已发货, 3: 未付款, 4: 待审核, 5: 待发货, 6: 不发货) [原字段 'status']
    order_status: str = Field(validation_alias="status")
    # 订单类型 [原字段 'order_from']
    order_type: str = Field(validation_alias="order_from")
    # 平台订单ID列表
    platform_order_ids: list[str] = Field(validation_alias="platform_list")
    # 订单目的地国家代码
    country_code: str
    # 物流类型ID
    logistics_type_id: str
    # 物流类型名称 [原字段 'logistics_type_name']
    logistics_type: str = Field(validation_alias="logistics_type_name")
    # 物流商ID
    logistics_provider_id: str
    # 物流商名称 [原字段 'logistics_provider_name']
    logistics_provider: str = Field(validation_alias="logistics_provider_name")
    # 发货仓库ID [原字段 'wid']
    warehouse_id: IntOrNone2Zero = Field(validation_alias="wid")
    # 发货仓库名称 [原字段 'warehouse_name']
    warehouse: str = Field(validation_alias="warehouse_name")
    # 买家备注 [原字段 'customer_comment']
    buyer_note: str = Field(validation_alias="customer_comment")
    # 订购时间
    purchase_time: str


class FbmOrders(ResponseV1):
    """自发货订单列表"""

    data: list[FbmOrder]


# . FBM Order Detail
class FbmOrderDetailItem(BaseModel):
    """自发货订单详情中的商品"""

    # fmt: off
    # 平台订单ID
    platform_order_id: str
    # 订单详情的商品单号 [原字段 'order_item_no']
    order_item_id: str = Field(validation_alias="order_item_no")
    # 亚马逊卖家SKU (Listing.msku) [原字段 'MSKU']
    msku: str = Field(validation_alias="MSKU")
    # 领星本地SKU (Listing.lsku) [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 领星本地商品名称 (Listing.product_name)
    product_name: str
    # 商品图片链接 [原字段 'pic_url']
    image_url: str = Field(validation_alias="pic_url")
    # 商品单价货币代码
    currency_code: str
    # 商品单价 [原字段 'item_unit_price']
    item_price: float = Field(validation_alias="item_unit_price")
    # 订单商品数量 [原字段 'quality']
    order_qty: int = Field(validation_alias="quality")
    # 订单备注 [原字段 'customization']
    order_note: str = Field(validation_alias="customization")
    # 附件信息列表 [原字段 'newAttachments']
    attachments: list[base_schema.AttachmentFile] = Field(validation_alias="newAttachments")
    # fmt: on


class FbmOrderDetail(BaseModel):
    """自发货订单详情"""

    # fmt: off
    # 领星店铺名称 (Seller.name) [原字段: 'shop_name']
    seller_name: str = Field(validation_alias="shop_name")
    # 自发货订单号
    order_number: str
    # 订单状态 (1: 同步中, 2: 已发货, 3: 未付款, 4: 待审核, 5: 待发货, 6: 不发货)
    order_status: str
    # 订单类型 [原字段 'order_from_name']
    order_type: str = Field(validation_alias="order_from_name")
    # 订单平台 [原字段 'platform']
    order_platform: str = Field(validation_alias="platform")
    # 物流类型ID
    logistics_type_id: str
    # 物流类型名称 [原字段 'logistics_type_name']
    logistics_type: str = Field(validation_alias="logistics_type_name")
    # 物流商ID
    logistics_provider_id: str
    # 物流商名称 [原字段 'logistics_provider_name']
    logistics_provider: str = Field(validation_alias="logistics_provider_name")
    # 发货仓库ID [原字段 'wid']
    warehouse_id: IntOrNone2Zero = Field(validation_alias="wid")
    # 发货仓库名称 [原字段 'warehouse_name']
    warehouse: str = Field(validation_alias="warehouse_name")
    # 订单配送服务级别 [原字段 'buyer_choose_express']
    shipment_service: str = Field(validation_alias="buyer_choose_express")
    # 买家留言
    buyer_message: str 
    # 买家备注 [原字段 'customer_comment']
    buyer_note: str = Field(validation_alias="customer_comment")
    # 订购时间
    purchase_time: str
    # 物流跟踪码
    tracking_number: str
    # 包裹预估重量 [原字段 'logistics_pre_weight']
    package_est_weight: FloatOrNone2Zero = Field(validation_alias="logistics_pre_weight")
    # 包裹预估重量单位 [原字段 'logistics_pre_weight_unit']
    package_est_weight_unit: str = Field(validation_alias="logistics_pre_weight_unit")
    # 包裹预估长度 [原字段 'package_length']
    package_est_length: FloatOrNone2Zero = Field(validation_alias="package_length")
    # 包裹预估宽度 [原字段 'package_width']
    package_est_width: FloatOrNone2Zero = Field(validation_alias="package_width")
    # 包裹预估高度 [原字段 'package_height']
    package_est_height: FloatOrNone2Zero = Field(validation_alias="package_height")
    # 包裹预估尺寸单位 [原字段 'package_unit']
    package_est_dimension_unit: str = Field(validation_alias="package_unit")
    # 预估物流费用 [原字段 'logistics_pre_price']
    logistics_est_amt: FloatOrNone2Zero = Field(validation_alias="logistics_pre_price")
    # 包裹实际重量 [原字段: 'pkg_real_weight']
    package_weight: FloatOrNone2Zero = Field(validation_alias="pkg_real_weight")
    # 包裹实际重量单位 [原字段: 'pkg_real_weight_unit']
    package_weight_unit: str = Field(validation_alias="pkg_real_weight_unit")
    # 包裹实际长度 [原字段: 'pkg_length']
    package_length: FloatOrNone2Zero = Field(validation_alias="pkg_length")
    # 包裹实际宽度 [原字段: 'pkg_width']
    package_width: FloatOrNone2Zero = Field(validation_alias="pkg_width")
    # 包裹实际高度 [原字段: 'pkg_height']
    package_height: FloatOrNone2Zero = Field(validation_alias="pkg_height")
    # 包裹实际尺寸单位 [原字段: 'pkg_size_unit']
    package_dimension_unit: str = Field(validation_alias="pkg_size_unit")
    # 实际物流费用货币代码 [原字段: 'logistics_freight_currency_code']
    logistics_currency_code: str = Field(validation_alias="logistics_freight_currency_code")
    # 实际物流费用 [原字段: 'logistics_freight']
    logistics_amt: FloatOrNone2Zero = Field(validation_alias="logistics_freight")
    # 总客付运费 [原字段 'total_shipping_price']
    shipping_amt: FloatOrNone2Zero = Field(validation_alias="total_shipping_price")
    # 订单销售金额 [原字段 'order_price_amount']
    sales_amt: FloatOrNone2Zero = Field(validation_alias="order_price_amount")
    # 订单毛利润金额 [原字段 'gross_profit_amount']
    profit_amt: FloatOrNone2Zero = Field(validation_alias="gross_profit_amount")
    # 订单商品列表 [原字段: 'order_item']
    items: list[FbmOrderDetailItem] = Field(validation_alias="order_item")
    # fmt: on


class FbmOrderDetailData(ResponseV1):
    """自发货订单详情列表"""

    data: FbmOrderDetail


# 销售 - 促销管理 ----------------------------------------------------------------------------------------------------------------
# . Promotion Coupon
class PromotionCoupon(BaseModel):
    """促销 - 优惠券"""

    # 领星店铺ID (Seller.sid)
    sid: int
    # 优惠券名称
    coupon_name: str = Field(validation_alias="name")
    # 优惠券状态 [原字段 'origin_status']
    # (ACTIVE, CANCELED, EXPIRED, RUNNING, NEEDS ACTION, EXPIRING SOON, SUBMITTED, FAILED)
    status: str = Field(validation_alias="origin_status")
    # 优惠券备注 [原字段 'remark']
    note: str = Field(validation_alias="remark")
    # 优惠券折扣百分比 [原字段 'discount']
    discount_pct: str = Field(validation_alias="discount")
    # 货币符号
    currency_icon: str
    # 优惠券预算金额 [原字段 'budget']
    budget_amt: str = Field(validation_alias="budget")
    # 优惠券费用 [原字段 'cost']
    coupon_fee: FloatOrNone2Zero = Field(validation_alias="cost")
    # 优惠券领取数量 [原字段 'draw_quantity']
    claimed_qty: IntOrNone2Zero = Field(validation_alias="draw_quantity")
    # 优惠券兑换数量 [原字段 'exchange_quantity']
    redeemed_qty: IntOrNone2Zero = Field(validation_alias="exchange_quantity")
    # 优惠券兑换率 (redeemed_qty / claimed_qty) [原字段 'exchange_rate']
    redemption_rate: FloatOrNone2Zero = Field(validation_alias="exchange_rate")
    # 优惠券期间的商品销售数量 [原字段 'sales_volume']
    sales_qty: IntOrNone2Zero = Field(validation_alias="sales_volume")
    # 优惠券期间的商品销售金额 [原字段 'sales_amount']
    sales_amt: FloatOrNone2Zero = Field(validation_alias="sales_amount")
    # 优惠券的开始时间 (站点时间) [原字段 'promotion_start_time']
    start_time: str = Field(validation_alias="promotion_start_time")
    # 优惠券的结束时间 (站点时间) [原字段 'promotion_end_time']
    end_time: str = Field(validation_alias="promotion_end_time")
    # 首次同步时间 (站点时间)
    first_sync_time: str
    # 最后同步时间 (站点时间)
    last_sync_time: str


class PromotionCoupons(ResponseV1):
    """促销 - 优惠券列表"""

    data: list[PromotionCoupon]


# . Promotion Deal
class PromotionDeal(BaseModel):
    """促销 - Deal"""

    # fmt: off
    # 领星店铺ID (Seller.sid)
    sid: int
    # Deal 类型 (1: Best Deal, 2: Lightning Deal) [原字段 'promotion_type']
    deal_type: int = Field(validation_alias="promotion_type")
    # Deal 名称 [原字段 'description']
    deal_name: str = Field(validation_alias="description")
    # Deal 状态 [原字段 'origin_status']
    # (ACTIVE, CANCELED, EXPIRED, APPROVED, SUPPRESSED, DISMISSED, DRAFT ENDED)
    status: str = Field(validation_alias="origin_status")
    # Deal 备注 [原字段 'remark']
    note: str = Field(validation_alias="remark")
    # Deal 商品标题 [原字段 'name']
    product_title: str = Field(validation_alias="name")
    # Deal 商品数量 [原字段 'product_quantity']
    product_count: IntOrNone2Zero = Field(validation_alias="product_quantity")
    # 货币符号
    currency_icon: str
    # Deal 费用 [原字段 'seckill_fee']
    deal_fee: FloatOrNone2Zero = Field(validation_alias="seckill_fee")
    # 参与 Deal 的商品库存数量 [原字段 'participate_inventory']
    deal_qty: IntOrNone2Zero = Field(validation_alias="participate_inventory")
    # Deal 期间的商品销售数量 [原字段 'sales_volume']
    sales_qty: IntOrNone2Zero = Field(validation_alias="sales_volume")
    # Deal 期间参促库存的转化率 (sales_qty / deal_qty * 100) [原字段 'sold_rate']
    sales_rate: FloatOrNone2Zero = Field(validation_alias="sold_rate")
    # Deal 期间商品详情页的浏览量 [原字段 'page_view']
    page_views: IntOrNone2Zero = Field(validation_alias="page_view")
    # Deal 期间浏览至购买的转化率 (sales_qty / page_views * 100) [原字段 'exchange_rate']
    conversion_rate: FloatOrNone2Zero = Field(validation_alias="exchange_rate")
    # Deal 期间的商品销售金额 [原字段 'sales_amount']
    sales_amt: FloatOrNone2Zero = Field(validation_alias="sales_amount")
    # Deal 开始时间 (站点时间) [原字段 'promotion_start_time']
    start_time: str = Field(validation_alias="promotion_start_time")
    # Deal 结束时间 (站点时间) [原字段 'promotion_end_time']
    end_time: str = Field(validation_alias="promotion_end_time")
    # 首次同步时间 (站点时间)
    first_sync_time: str
    # 最后同步时间 (站点时间)
    last_sync_time: str
    # fmt: on


class PromotionDeals(ResponseV1):
    """促销 - Deal 列表"""

    data: list[PromotionDeal]


# . Promotion Activity
class PromotionActivity(BaseModel):
    """促销 - 活动"""

    # fmt: off
    # 领星店铺ID (Seller.sid)
    sid: int
    # 促销活动类型
    # (0: 未定义类型, 3: 买一赠一, 4: 购买折扣, 5: 一口价, 8: 社媒促销)
    promotion_type: int
    # 促销活动名称 [原字段 'name']
    promotion_name: str = Field(validation_alias="name")
    # 促销活动状态 [原字段 'origin_status']
    # (ACTIVE, CANCELED, EXPIRED, PENDING)
    status: str = Field(validation_alias="origin_status")
    # 促销活动备注 [原字段 'remark']
    note: str = Field(validation_alias="remark")
    # 促销活动优惠码 [原字段 'promotion_code']
    code: str = Field(validation_alias="promotion_code")
    # 促销活动参与条件 [原字段 'participate_condition']
    requirement: str = Field(validation_alias="participate_condition")
    # 促销活动参与条件数值 [原字段 'participate_condition_num']
    requirement_value: IntOrNone2Zero = Field(validation_alias="participate_condition_num")
    # 促销活动优惠内容 [原字段 'buyer_gets']
    offer: str = Field(validation_alias="buyer_gets")
    # 促销活动优惠内容数值 [原字段 'buyer_gets_num']
    offer_value: IntOrNone2Zero = Field(validation_alias="buyer_gets_num")
    # 促销活动需购买商品
    purchase_product: str
    # 促销活动可享受折扣商品
    discount_product: str
    # 促销活动排除商品
    exclude_product: str
    # 促销活动是否限制兑换量 (0: 否, 1: 是) [原字段 'exchange_limit']
    limited: int = Field(validation_alias="exchange_limit")
    # 货币符号
    currency_icon: str
    # 促销活动期间的商品销售数量 [原字段 'sales_volume']
    sales_qty: IntOrNone2Zero = Field(validation_alias="sales_volume")
    # 促销活动期间的商品销售金额 [原字段 'sales_amount']
    sales_amt: FloatOrNone2Zero = Field(validation_alias="sales_amount")
    # 促销活动开始时间 (站点时间) [原字段 'promotion_start_time']
    start_time: str = Field(validation_alias="promotion_start_time")
    # 促销活动结束时间 (站点时间) [原字段 'promotion_end_time']
    end_time: str = Field(validation_alias="promotion_end_time")
    # 首次同步时间 (站点时间)
    first_sync_time: str
    # 最后同步时间 (站点时间)
    last_sync_time: str
    # fmt: on


class PromotionActivities(ResponseV1):
    """促销 - 活动列表"""

    data: list[PromotionActivity]


# . Promotion Discount
class PromotionDiscount(BaseModel):
    """促销 - 价格折扣"""

    # 领星店铺ID (Seller.sid)
    sid: int
    # 折扣名称 [原字段 'name']
    discount_name: str = Field(validation_alias="name")
    # 折扣状态 [原字段 'origin_status']
    # (ACTIVE, CANCELED, EXPIRED, AWAITTING, SCHEDULED, NEEDS ATTENTION)
    status: str = Field(validation_alias="origin_status")
    # 折扣备注 [原字段 'remark']
    note: str = Field(validation_alias="remark")
    # 货币符号
    currency_icon: str
    # 参与折扣的商品数量
    product_quantity: IntOrNone2Zero
    # 折扣开始时间 (站点时间) [原字段 'promotion_start_time']
    start_time: str = Field(validation_alias="promotion_start_time")
    # 折扣结束时间 (站点时间) [原字段 'promotion_end_time']
    end_time: str = Field(validation_alias="promotion_end_time")
    # 首次同步时间 (站点时间)
    first_sync_time: str
    # 最后同步时间 (站点时间)
    last_sync_time: str
    # 更细时间 (站点时间)
    update_time: StrOrNone2Blank


class PromotionDiscounts(ResponseV1):
    """促销 - 价格折扣列表"""

    data: list[PromotionDiscount]


# . Promotion On Listing
class PromotionOnListingDetail(BaseModel):
    """促销 - Listing的促销信息详情"""

    # 促销ID
    promotion_id: str
    # 促销名称 [原字段: 'name']
    promotion_name: str = Field(validation_alias="name")
    # 促销状态 [原字段 'origin_status']
    status: str = Field(validation_alias="origin_status")
    # 促销状态码 (0: 其他, 1: 进行中, 2: 已过期, 3: 未开始) [原字段 'status']
    status_code: int = Field(validation_alias="status")
    # 促销类型 (1: 优惠券, 2: Deal, 3 活动, 4 价格折扣) [原字段 'category']
    promotion_type: int = Field(validation_alias="category")
    # 促销类型文本 [原字段 'category_text']
    promotion_type_text: str = Field(validation_alias="category_text")
    # 促销子类型 (0: 未定义类型, 3: 买一赠一, 4: 购买折扣, 5: 一口价, 8: 社媒促销) [原字段 'promotion_type']
    promotion_sub_type: int = Field(validation_alias="promotion_type")
    # 促销子类型文本 [原字段 'promotion_type_text']
    promotion_sub_type_text: str = Field(validation_alias="promotion_type_text")
    # 折扣金额/折扣价格 [原字段 'discount_price']
    discount_amt: FloatOrNone2Zero = Field(validation_alias="discount_price")
    # 折扣百分比/售价百分比 [原字段 'discount_rate']
    discount_pct: FloatOrNone2Zero = Field(validation_alias="discount_rate")
    # 促销开始时间 (站点时间) [原字段 'promotion_start_time']
    start_time: str = Field(validation_alias="promotion_start_time")
    # 促销结束时间 (站点时间) [原字段 'promotion_end_time
    end_time: str = Field(validation_alias="promotion_end_time")


class PromotionOnListing(BaseModel):
    """促销 - Listing的促销信息"""

    # fmt: off
    # 领星店铺ID (Seller.sid)
    sid: int
    # 领星店铺名称 (Seller.name) [原字段 'store_name']
    seller_name: str = Field(validation_alias="store_name")
    # 国家 (中文) [原字段 'region_name']
    country: str = Field(validation_alias="region_name")
    # 商品ASIN
    asin: str
    # 亚马逊卖家SKU (Listing.msku) [原字段 'seller_sku']
    msku: str = Field(validation_alias="seller_sku")
    # 商品标题 [原字段 'item_name']
    title: str = Field(validation_alias="item_name")
    # 商品链接
    asin_url: str
    # 商品略缩图链接 [原字段 'small_image_url']
    thumbnail_url: str = Field(validation_alias="small_image_url")
    # 促销活动叠加数量 [原字段 'promotion_combo_num']
    promotion_stacks: IntOrNone2Zero = Field(validation_alias="promotion_combo_num")
    # 货币符号
    currency_icon: str
    # 销售价格
    sales_price: FloatOrNone2Zero
    # 销售价格 (美金)
    sales_price_usd: FloatOrNone2Zero
    # 最低折扣价格 [原字段 'discount_price_min']
    discount_min_price: FloatOrNone2Zero = Field(validation_alias="discount_price_min")
    # 平均折扣金额 [原字段 'avg_deal_price']
    discount_avg_amt: FloatOrNone2Zero = Field(validation_alias="avg_deal_price")
    # 平均折扣百分比 [原字段 'discount_rate_rate']
    discount_avg_pct: FloatOrNone2Zero = Field(validation_alias="discount_rate_rate")
    # FBA可售库存 [原字段 'afn_fulfillable_quantity']
    afn_fulfillable_qty: IntOrNone2Zero = Field(validation_alias="afn_fulfillable_quantity")
    # FBM可售库存 [原字段 'quantity']
    mfn_fulfillable_qty: IntOrNone2Zero = Field(validation_alias="quantity")
    # Listing负责人 [原字段 'principal_list']
    operators: list[StrOrNone2Blank] = Field(validation_alias="principal_list")
    # Listing标签 [原字段: 'listing_tags']
    tags: list[base_schema.TagInfo] = Field(validation_alias="listing_tags")
    # 促销活动列表 [原字段 'promotion_list']
    promotions: list[PromotionOnListingDetail] = Field(validation_alias="promotion_list")
    # fmt: on


class PromotionOnListings(ResponseV1):
    """促销 - Listing的促销信息列表"""

    data: list[PromotionOnListing]
