# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import ValidationInfo, Field, field_validator
from lingxingapi import utils
from lingxingapi.base.param import Parameter, PageOffestAndLength
from lingxingapi.fields import (
    NonEmptyStr,
    NonNegativeInt,
    NonNegativeFloat,
    StrOrNone2Blank,
)


# 销售 - Listing ----------------------------------------------------------------------------------------------------------------
# . Listings
class Listings(PageOffestAndLength):
    # 领星店铺ID (Seller.sid)
    sids: str = Field(alias="sid")
    # 搜索字段, 可选值为: 'msku', 'lsku', 'asin'
    search_field: Optional[NonEmptyStr] = None
    # 搜索模式 (0: 模糊搜索, 1: 精确搜索) [默认值 1]
    search_mode: Optional[NonNegativeInt] = Field(None, alias="exact_search")
    # 搜索值 (最多支持10个), 根据 search_field 和 search_mode 进行匹配
    search_value: Optional[list] = None
    # 是否已删除 (0: 未删除, 1: 已删除)
    deleted: Optional[NonNegativeInt] = Field(None, alias="is_delete")
    # 是否已完成领星配对 (1: 已配对, 2: 未配对)
    paired: Optional[NonNegativeInt] = Field(None, alias="is_pair")
    # 领星配对更新开始时间, 此参数查询要求 `paired=1`
    pair_start_time: Optional[str] = Field(None, alias="pair_update_start_time")
    # 领星配对更新结束时间, 此参数查询要求 `paired=1`
    pair_end_time: Optional[str] = Field(None, alias="pair_update_end_time")
    # 亚马逊更新开始时间
    update_start_time: Optional[str] = Field(None, alias="listing_update_start_time")
    # 亚马逊更新结束时间
    update_end_time: Optional[str] = Field(None, alias="listing_update_end_time")
    # 产品类型 (1: 普通产品, 2: 多属性产品)
    product_type: Optional[NonNegativeInt] = Field(None, alias="store_type")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("sids", mode="before")
    @classmethod
    def _validate_sids(cls, v) -> str:
        l = utils.validate_array_of_unsigned_int(v, "领星店铺ID sids")
        return ",".join(map(str, l))

    @field_validator("search_field", mode="before")
    @classmethod
    def _validate_search_field(cls, v) -> str | None:
        if v is None:
            return None
        if v == "msku":
            return "seller_sku"
        if v == "lsku":
            return "sku"
        return v

    @field_validator("search_value", mode="before")
    @classmethod
    def _validate_search_value(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_non_empty_str(v, "搜索值 search_value")

    @field_validator(
        "pair_start_time",
        "pair_end_time",
        "update_start_time",
        "update_end_time",
        mode="before",
    )
    @classmethod
    def _validate_update_time(cls, v, info: ValidationInfo) -> str | None:
        if v is None:
            return None
        dt = utils.validate_datetime(v, True, "更新时间 %s" % info.field_name)
        # fmt: off
        return "%04d-%02d-%02d %02d:%02d:%02d" % (
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
        )
        # fmt: on


# . Edit Listing Operators
class EditListingOperator(Parameter):
    # 领星店铺ID (Listing.sid)
    sid: NonNegativeInt
    # 商品ASIN码 (Listing.asin)
    asin: NonEmptyStr
    # 负责人姓名, 最多支持10个负责人, 传入 None 表示清空负责人
    name: Optional[list] = Field(None, alias="principal_name")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("name", mode="before")
    @classmethod
    def _validate_name(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_non_empty_str(v, "负责人名称 name")


class EditListingOperators(Parameter):
    # 修改负责人参数列表
    operators: list = Field(alias="sid_asin_list")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("operators", mode="before")
    @classmethod
    def _validate_operators(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            res = [EditListingOperator.model_validate_params(v)]
        else:
            res = [EditListingOperator.model_validate_params(i) for i in v]
            if len(res) == 0:
                raise ValueError("必须提供至少一个 operator 来修改商品负责人")
        return res


# . Edit Listing Prices
class EditListingPrice(Parameter):
    # 领星店铺ID (Listing.sid)
    sid: NonNegativeInt
    # 亚马逊卖家SKU (Listing.msku)
    msku: NonEmptyStr
    # 商品标准价 (不包含促销, 运费, 积分) (Listing.standard_price)
    standard_price: NonNegativeFloat
    # 商品优惠价 (不包含运费, 积分) (Listing.sale_price)
    sale_price: Optional[NonNegativeFloat]
    # 商品优惠价开始时间, 格式为 "YYYY-MM-DD"
    start_date: Optional[str] = None
    # 商品优惠价结束时间, 格式为 "YYYY-MM-DD"
    end_date: Optional[str] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("end_date", "start_date", mode="before")
    @classmethod
    def _validate_date(cls, v, info: ValidationInfo) -> str | None:
        if v is None:
            return None
        dt = utils.validate_datetime(v, True, "优惠价 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)


class EditListingPrices(Parameter):
    # 修改商品价格参数列表
    prices: list = Field(alias="pricing_params")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("prices", mode="before")
    @classmethod
    def _validate_prices(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            res = [EditListingPrice.model_validate_params(v)]
        else:
            res = [EditListingPrice.model_validate_params(i) for i in v]
            if len(res) == 0:
                raise ValueError("必须提供至少一个 prices 来修改商品价格")
        return res


# . Pair Listing Products
class PairListingProduct(Parameter):
    # 亚马逊卖家SKU (Listing.msku)
    msku: NonEmptyStr
    # 领星本地SKU (Listing.lsku)
    lsku: NonEmptyStr = Field(alias="sku")
    # 是否同步Listing图片 (0 否, 1 是)
    sync_pic: NonNegativeInt = Field(alias="is_sync_pic")
    # 亚马逊卖家ID (Sellers.Seller.seller_id)
    seller_id: Optional[NonEmptyStr] = None
    # 亚马逊市场ID (Sellers.Seller.marketplace_id)
    marketplace_id: Optional[NonEmptyStr] = None


class PairListingProducts(Parameter):
    # 修改商品配对参数列表
    pair_products: list = Field(alias="data")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("pair_products", mode="before")
    @classmethod
    def _validate_pair_products(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            res = [PairListingProduct.model_validate_params(v)]
        else:
            res = [PairListingProduct.model_validate_params(i) for i in v]
            if len(res) == 0:
                raise ValueError("必须提供至少一个 pair_product 来修改领星商品配对")
        return res


# . Unpair Listing Products
class UnpairListingProduct(Parameter):
    # 领星店铺ID (Listing.sid)
    sid: NonNegativeInt = Field(alias="storeId")
    # 亚马逊卖家SKU (Listing.msku)
    msku: NonEmptyStr


class UnpairListingProducts(Parameter):
    # 删除商品配对参数列表
    unpair_products: list = Field(alias="list")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("unpair_products", mode="before")
    @classmethod
    def _validate_unpair_products(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            res = [UnpairListingProduct.model_validate_params(v)]
        else:
            res = [UnpairListingProduct.model_validate_params(i) for i in v]
            if len(res) == 0:
                raise ValueError("必须提供至少一个 product_unpair 来删除领星商品配对")
        return res


# . Listing Global Tags
class ListingGlobalTags(PageOffestAndLength):
    # 搜索类型, 支持 "tag_name"
    search_field: Optional[NonEmptyStr] = None
    # 搜索值, 仅支持字符串作为检索值
    search_value: Optional[NonEmptyStr] = None


# . Create Listing Global Tag
class CreateListingGlobalTag(Parameter):
    # 领星标签名称 (ListingGlobalTag.tag_name)
    tag_name: NonEmptyStr


# . Remove Listing Global Tag
class RemoveListingGlobalTag(Parameter):
    # 领星标签IDs, 最多支持 200 个 (ListingGlobalTag.tag_id)
    tag_ids: list[NonEmptyStr]


# . Listing Tags
class ListingTags(Parameter):
    # 领星店铺ID (Listing.sid)
    sid: NonNegativeInt
    # 亚马逊卖家SKU (Listing.msku)
    msku: NonEmptyStr = Field(alias="relation_id")


class ListingTagsMskus(Parameter):
    # 查询Listing标签参数列表
    mskus: list = Field(alias="bind_detail")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("mskus", mode="before")
    @classmethod
    def _validate_mskus(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            res = [ListingTags.model_validate_params(v)]
        else:
            res = [ListingTags.model_validate_params(i) for i in v]
            if len(res) == 0:
                raise ValueError("必须提供至少一个 msku 来查询 Listing 的关联标签信息")
        return res


# . Edit Listing Tags
class EditListingTag(Parameter):
    # 领星店铺ID (Listing.sid)
    sid: NonNegativeInt
    # 亚马逊卖家SKU (Listing.msku)
    msku: NonEmptyStr = Field(alias="relationId")


class SetListingTag(Parameter):
    # 领星标签ID列表 (ListingTag.tag_id)
    tag_ids: list = Field(alias="tagIds")
    # 亚马逊卖家SKU列表
    mskus: list = Field(alias="bindDetail")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("tag_ids", mode="before")
    @classmethod
    def _validate_tag_ids(cls, v) -> list[str]:
        return utils.validate_array_of_unsigned_int(v, "领星标签ID列表 tag_ids")

    @field_validator("mskus", mode="before")
    @classmethod
    def _validate_mskus(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            res = [EditListingTag.model_validate_params(v)]
        else:
            res = [EditListingTag.model_validate_params(i) for i in v]
            if len(res) == 0:
                raise ValueError("必须提供至少一个 msku 来新增 Listing 标签")
        return res


class UnsetListingTag(Parameter):
    # 领星标签ID列表 (ListingTag.tag_id)
    tag_ids: list = Field(alias="globalTagIds")
    # 亚马逊卖家SKU列表
    mskus: list = Field(alias="bindDetail")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("tag_ids", mode="before")
    @classmethod
    def _validate_tag_ids(cls, v) -> list[str]:
        return utils.validate_array_of_unsigned_int(v, "领星标签ID列表 tag_ids")

    @field_validator("mskus", mode="before")
    @classmethod
    def _validate_mskus(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            res = [EditListingTag.model_validate_params(v)]
        else:
            res = [EditListingTag.model_validate_params(i) for i in v]
            if len(res) == 0:
                raise ValueError("必须提供至少一个 msku 来删除 Listing 标签")
        return res


# . Listing FBA Fees
class ListingFbaFees(Parameter):
    # 领星店铺ID (Listing.sid)
    sid: NonNegativeInt
    # 亚马逊卖家SKU (Listing.msku)
    msku: NonEmptyStr


class ListingFbaFeesMskus(Parameter):
    # 查询预估 FBA 费用参数列表
    mskus: list = Field(alias="data")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("mskus", mode="before")
    @classmethod
    def _validate_mskus(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            res = [ListingFbaFees.model_validate_params(v)]
        else:
            res = [ListingFbaFees.model_validate_params(i) for i in v]
            if len(res) == 0:
                raise ValueError("必须提供至少一个 msku 来查询预估FBA费用")
        return res


# . Edit Listing FBM
class EditListingFbm(Parameter):
    # 领星店铺ID (Listing.sid)
    sid: NonNegativeInt = Field(alias="storeId")
    # 亚马逊卖家SKU (Listing.msku)
    msku: NonEmptyStr
    # FBM库存数量
    qty: NonNegativeInt = Field(alias="fbmInventory")
    # 发货/处理天数
    ship_days: Optional[NonNegativeInt] = Field(None, alias="shipDays")


class EditListingFbms(Parameter):
    # 更新 FBM 库存参数列表
    mskus: list = Field(alias="fbmInventoryList")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("mskus", mode="before")
    @classmethod
    def _validate_mskus(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            res = [EditListingFbm.model_validate_params(v)]
        else:
            res = [EditListingFbm.model_validate_params(i) for i in v]
            if len(res) == 0:
                raise ValueError("必须提供至少一个 msku 来更新 FBM 库存")
        return res


# . Listing Operate Logs
class ListingOperationLogs(PageOffestAndLength):
    # 领星店铺ID (Listing.sid)
    sid: NonNegativeInt
    # 亚马逊卖家SKU (Listing.msku)
    msku: NonEmptyStr
    # 操作用户ID列表 (Account.user_id)
    operator_ids: Optional[list] = Field(None, alias="operate_uid")
    # 操作类型列表 (1: 调价, 2: 调库存, 3: 修改标题, 4: 编辑商品, 5: B2B调价)
    operation_types: Optional[list] = Field(None, alias="operate_type")
    # 操作时间开始, 格式为 "YYYY-MM-DD HH:MM:SS"
    start_time: Optional[str] = Field(None, alias="operate_time_start")
    # 操作时间结束, 格式为 "YYYY-MM-DD HH:MM:SS"
    end_time: Optional[str] = Field(None, alias="operate_time_end")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("operator_ids", mode="before")
    @classmethod
    def _validate_operator_ids(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_non_empty_str(v, "操作用户ID operator_ids")

    @field_validator("operation_types", mode="before")
    @classmethod
    def _validate_operation_types(cls, v) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_unsigned_int(v, "操作类型 operation_types")

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def _validate_time(cls, v, info: ValidationInfo) -> str | None:
        if v is None:
            return None
        dt = utils.validate_datetime(v, True, "操作时间 %s" % info.field_name)
        # fmt: off
        return "%04d-%02d-%02d %02d:%02d:%02d" % (
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
        )
        # fmt: on


# 销售 - 平台订单 ----------------------------------------------------------------------------------------------------------------
# . Orders
class Orders(PageOffestAndLength):
    # 查询开始时间, 格式为 "YYYY-MM-DD HH:MM:SS"
    start_time: str = Field(alias="start_date")
    # 查询结束时间, 格式为 "YYYY-MM-DD HH:MM:SS"
    end_time: str = Field(alias="end_date")
    # 查询时间类型 (1: 订购时间[站点时间], 2: 订单修改时间[北京时间], 3: 平台更新时间[UTC时间], 4: 发货时间[站点时间]) [默认值 1]
    time_type: Optional[NonNegativeInt] = Field(None, alias="date_type")
    # 是否按时间排序 (0: 否, 1: 降序, 2: 升序) [默认值 0]
    time_sort: Optional[NonNegativeInt] = Field(None, alias="sort_desc_by_date_type")
    # 领星店铺ID列表 (Order.sid)
    sids: Optional[list] = Field(None, alias="sid_list")
    # 配送方式 (1: AFN, 2: MFN) (Order.fulfillment_channel)
    fulfillment_channel: Optional[NonNegativeInt] = None
    # 订单状态列表 ("Pending", "Unshipped", "PartiallyShipped", "Shipped", "Canceled") (Order.order_status)
    order_status: Optional[list]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def _validate_time(cls, v, info: ValidationInfo) -> str:
        dt = utils.validate_datetime(v, True, "查询日期 %s" % info.field_name)
        # fmt: off
        return "%04d-%02d-%02d %02d:%02d:%02d" % (
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
        )
        # fmt: on

    @field_validator("sids", mode="before")
    @classmethod
    def _validate_sids(cls, v) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_unsigned_int(v, "领星店铺ID sid")

    @field_validator("order_status", mode="before")
    @classmethod
    def _validate_order_status(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_non_empty_str(v, "订单状态 order_status")


# . Edit Order Note
class EditOrderNote(Parameter):
    # 领星店铺ID (Order.sid)
    sid: NonNegativeInt
    # 亚马逊订单ID (Order.amazon_order_id)
    amazon_order_id: NonEmptyStr = Field(alias="amazonOrderId")
    # 备注内容
    note: StrOrNone2Blank = Field(alias="remark")


# . Order Details
class OrderDetails(Parameter):
    # 亚马逊订单ID列表 (Order.amazon_order_id)
    amazon_order_ids: str = Field(alias="order_id")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("amazon_order_ids", mode="before")
    @classmethod
    def _validate_amazon_order_ids(cls, v) -> str:
        ids = utils.validate_array_of_non_empty_str(
            v, "亚马逊订单ID列表 amazon_order_ids"
        )
        return ",".join(ids)


# . After-Sales Orders
class AfterSalesOrder(PageOffestAndLength):
    # 查询开始日期, 左闭右开, 格式为 "YYYY-MM-DD"
    start_date: str
    # 查询结束日期, 左闭右开, 格式为 "YYYY-MM-DD"
    end_date: str
    # 查询日期类型 (1: 售后时间, 2: 订购时间, 3: 更新时间) [默认值: 1]
    date_type: Optional[NonNegativeInt] = None
    # 售后类型 (1: 退款, 2: 退货, 3: 换货) [默认查询所有类型]
    service_type: Optional[str] = Field(None, alias="after_type")
    # 领星店铺ID列表 (Order.sid)
    sids: Optional[str] = Field(None, alias="sid")
    # 亚马逊订单ID列表, 最多支持 50 个 (Order.amazon_order_id)
    amazon_order_ids: Optional[list] = Field(None, alias="amazon_order_id_list")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v, info: ValidationInfo) -> str:
        dt = utils.validate_datetime(v, True, "查询日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)

    @field_validator("service_type", mode="before")
    @classmethod
    def _validate_service_type(cls, v) -> str | None:
        if v is None:
            return None
        l = utils.validate_array_of_unsigned_int(v, "售后类型 service_type")
        return ",".join(map(str, l))

    @field_validator("sids", mode="before")
    @classmethod
    def _validate_sids(cls, v) -> str | None:
        if v is None:
            return None
        ids = utils.validate_array_of_unsigned_int(v, "店铺ID列表 sids")
        return ",".join(map(str, ids))

    @field_validator("amazon_order_ids", mode="before")
    @classmethod
    def _validate_amazon_order_ids(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_non_empty_str(
            v, "亚马逊订单ID列表 amazon_order_ids"
        )


# . MCF Orders
class McfOrders(Parameter):
    # 领星店铺ID列表 (Order.sid)
    sids: Optional[list] = None
    # 查询开始时间 (不传默认最近6个月)
    start_date: Optional[str] = None
    # 查询结束时间 (不传默认最近6个月)
    end_date: Optional[str] = None
    # 查询时期类型 (1: 订购时间[站点时间], 2: 订单修改时间[北京时间]) [默认值: 1]
    date_type: Optional[NonNegativeInt] = None
    # 分页偏移量
    offset: NonNegativeInt
    # 分页长度 [最大值 1000]
    length: NonNegativeInt

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("sids", mode="before")
    @classmethod
    def _validate_sids(cls, v) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_unsigned_int(v, "领星店铺ID sids")

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v, info: ValidationInfo) -> str | None:
        if v is None:
            return None
        dt = utils.validate_datetime(v, True, "查询日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)


# . MCF Fulfillment Order IDs
class McfFulfillmentOrderId(Parameter):
    # 领星店铺ID (McfOrder.sid)
    sid: NonNegativeInt
    # 多渠道订单配送ID (McfOrder.fulfillment_order_id)
    fulfillment_order_id: NonEmptyStr = Field(alias="seller_fulfillment_order_id")


class McfFulfillmentOrderIds(Parameter):
    # 订单ID参数列表
    fulfillment_order_ids: list = Field(alias="order_info")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("fulfillment_order_ids", mode="before")
    @classmethod
    def _validate_fulfillment_order_ids(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            res = [McfFulfillmentOrderId.model_validate_params(v)]
        else:
            res = [McfFulfillmentOrderId.model_validate_params(i) for i in v]
            if len(res) == 0:
                raise ValueError(
                    "必须提供至少一个 fulfillment_order_id 来查询多渠道配送的商品信息"
                )
        return res


# . MCF Order Transactions
class McfOrderTransaction(Parameter):
    # 领星店铺ID (McfOrder.sid)
    sid: NonNegativeInt
    # 多渠道亚马逊订单ID (McfOrder.amazon_order_id)
    amazon_order_id: NonEmptyStr = Field(alias="amazonOrderId")


# 销售 - 自发货管理 --------------------------------------------------------------------------------------------------------------
# . FBM Orders
class FbmOrders(Parameter):
    # 领星店铺ID列表 (Order.sid)
    sids: str = Field(alias="sid")
    # 订购开始时间, 格式为 "YYYY-MM-DD HH:MM:SS"
    purchase_start_time: Optional[str] = Field(None, alias="start_time")
    # 订购结束时间, 格式为 "YYYY-MM-DD HH:MM:
    purchase_end_time: Optional[str] = Field(None, alias="end_time")
    # 订单状态 (1: 同步中, 2: 已发货, 3: 未付款, 4: 待审核, 5: 待发货, 6: 不发货)
    order_status: Optional[str] = None
    # 分页页码 [默认值 1]
    page: Optional[NonNegativeInt] = None
    # 分页长度 [默认值 100]
    length: Optional[NonNegativeInt] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("sids", mode="before")
    @classmethod
    def _validate_sids(cls, v) -> str:
        l = utils.validate_array_of_unsigned_int(v, "领星店铺ID sids")
        return ",".join(map(str, l))

    @field_validator("purchase_start_time", "purchase_end_time", mode="before")
    @classmethod
    def _validate_time(cls, v, info: ValidationInfo) -> str | None:
        if v is None:
            return None
        dt = utils.validate_datetime(v, True, "订购时间 %s" % info.field_name)
        # fmt: off
        return "%04d-%02d-%02d %02d:%02d:%02d" % (
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
        )
        # fmt: on

    @field_validator("order_status", mode="before")
    @classmethod
    def _validate_order_status(cls, v) -> str | None:
        if v is None:
            return None
        l = utils.validate_array_of_unsigned_int(v, "订单状态 order_status")
        return ",".join(map(str, l))


# . FBM Order Detail
class FbmOrderDetail(Parameter):
    # 自发货订单号 (FbmOrder.order_number)
    order_number: NonEmptyStr


# 销售 - 促销管理 ----------------------------------------------------------------------------------------------------------------
# . Promotions
class Promotions(PageOffestAndLength):
    # 领星店铺ID列表 (Seller.sid)
    sids: Optional[list] = None
    # 优惠券开始日期, 时间间隔长度不超过90天, 格式为 "YYYY-MM-DD"
    start_date: Optional[str] = None
    # 优惠券结束日期, 时间间隔长度不超过90天, 格式为 "YYYY-MM-DD"
    end_date: Optional[str] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("sids", mode="before")
    @classmethod
    def _validate_sids(cls, v) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_unsigned_int(v, "领星店铺ID sids")

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v, info: ValidationInfo) -> str | None:
        if v is None:
            return None
        dt = utils.validate_datetime(v, True, "优惠券日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)


# . Promotion On Listings
class PromotionOnListings(PageOffestAndLength):
    # 站点日期, 格式为 "YYYY-MM-DD"
    site_date: str
    # 促销开始日期, 格式为 "YYYY-MM-DD"
    start_date: Optional[str] = Field(None, alias="start_time")
    # 促销结束日期, 格式为 "YYYY-MM-DD"
    end_date: Optional[str] = Field(None, alias="end_time")
    # 领星店铺ID列表 (Seller.sid)
    sids: Optional[list] = None
    # 促销类型 (1: 优惠券, 2: Deal, 3 活动, 4 价格折扣)
    promotion_type: Optional[list] = Field(None, alias="promotion_category")
    # 促销状态 (0: 其他, 1: 进行中, 2: 已过期, 3: 未开始)
    promotion_status: Optional[list] = Field(None, alias="status")
    # 商品状态 (-1: 已删除, 0: 停售, 1: 在售)
    product_status: Optional[list] = None
    # 是否叠加优惠券 (0: 否, 1: 是)
    is_coupon_stacked: Optional[NonNegativeInt] = Field(None, alias="is_overlay")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("site_date", "start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v, info: ValidationInfo) -> str | None:
        if v is None:
            return None
        dt = utils.validate_datetime(v, True, "促销日期 %s" % info.field_name)
        return "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)

    @field_validator("sids", mode="before")
    @classmethod
    def _validate_sids(cls, v) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_unsigned_int(v, "领星店铺ID sids")

    @field_validator("promotion_type", "promotion_status", mode="before")
    @classmethod
    def _validate_promotion_type(cls, v, info: ValidationInfo) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_unsigned_int(v, "促销 %s" % info.field_name)

    @field_validator("product_status", mode="before")
    @classmethod
    def _validate_product_status(cls, v) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_int(v, "商品状态 product_status")
