# -*- coding: utf-8 -*-c
import datetime
from typing import Literal
from lingxingapi import errors
from lingxingapi.base.api import BaseAPI
from lingxingapi.base import schema as base_schema
from lingxingapi.sales import param, route, schema


# Type Aliases ---------------------------------------------------------------------------------------------------------
SEARCH_FIELD = Literal["asin", "msku", "lsku"]
ORDER_STATUS = Literal[
    "Pending",
    "Shipped",
    "Unshipped",
    "PartiallyShipped",
    "Canceled",
]


# API ------------------------------------------------------------------------------------------------------------------
class SalesAPI(BaseAPI):
    """领星API `销售数据` 接口

    ## Notice
    请勿直接实例化此类
    """

    # 公共 API --------------------------------------------------------------------------------------
    # Listing - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    async def Listings(
        self,
        sids: int | list[int],
        *,
        search_field: SEARCH_FIELD | None = None,
        search_mode: int | None = None,
        search_value: str | list[str] | None = None,
        deleted: int | None = None,
        paired: int | None = None,
        pair_start_time: str | datetime.date | datetime.datetime = None,
        pair_end_time: str | datetime.date | datetime.datetime = None,
        update_start_time: str | datetime.date | datetime.datetime = None,
        update_end_time: str | datetime.date | datetime.datetime = None,
        product_type: int | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.Listings:
        """查询亚马逊的Listing信息

        ## Docs
        - 销售 - Listing: [查询亚马逊Listing](https://apidoc.lingxing.com/#/docs/Sale/Listing)

        :param sids `<'int/list[int]'>`: 领星店铺ID或ID列表, 参数来源: `Seller.sid`
        :param search_field `<'str'>`: 搜索字段, 默认 `None` (不搜索)

            - `"asin"`: 商品ASIN码
            - `"msku"`: 亚马逊卖家SKU
            - `"lsku"`: 领星本地商品SKU

        :param search_mode `<'int'>`: 搜索模式, 默认 `None` (使用: 1)

            - `0`: 模糊搜索
            - `1`: 精确搜索

        :param search_value `<'str/list[str]'>`: 搜索值 (最多支持10个),
            根据 search_field 和 search_mode 进行匹配, 默认 `None` (不搜索)

        :param deleted `<'int'>`: 是否已删除, 默认 `None` (不筛选), 参数来源: `Listing.deleted`

            - `0`: 未删除
            - `1`: 已删除

        :param paired `<'int'>`: 是否已完成领星配对, 默认 `None` (不筛选)

            - `0`: 未配对
            - `1`: 已配对

        :param pair_start_time `<'str/date/datetime'>`: 领星配对更新开始时间,
            默认 `None` (不筛选), 参数来源: `Listing.pair_time_cnt`
        :param pair_end_time `<'str/date/datetime'>`: 领星配对更新结束时间,
            默认 `None` (不筛选), 参数来源: `Listing.pair_time_cnt`
        :param update_start_time `<'str/date/datetime'>`: 亚马逊更新开始时间,
            默认 `None` (不筛选), 参数来源: `Listing.update_time_utc`
        :param update_end_time `<'str/date/datetime'>`: 亚马逊更新结束时间,
            默认 `None` (不筛选), 参数来源: `Listing.update_time_utc`
        :param product_type `<'int'>`: 产品类型, 默认 `None` (不筛选), 参数来源: `Listing.product_type`

            - `1`: 普通产品
            - `2`: 多属性产品

        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 最大支持 1000, 默认 `None` (使用: 1000)
        :returns `<'Listings'>`: 返回查询到的 Listing 信息列表
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
                    # 领星店铺ID (Seller.sid) [sid + msku 唯一标识]
                    "sid": 1,
                    # 商品国家 (中文) [原字段 'marketplace']
                    "country": "德国",
                    # 商品ASIN码 (Amazon Standard Identification Number)
                    "asin": "B0********",
                    # 商品父ASIN码 (变体商品的主ASIN, 无变体则与 asin 相同)
                    "parent_asin": "B0********",
                    # 亚马逊商品SKU [原字段 'seller_sku']
                    "msku": "sk*******",
                    # 领星本地商品SKU [原字段 'local_sku']
                    "lsku": "sk*******",
                    # 亚马逊FBA自生成的商品编号
                    "fnsku": "X00*******",
                    # 领星本地商品名称 [原字段 'local_name']
                    "product_name": "pr*******",
                    # 品牌名称 [原字段 'brand_name']
                    "brand": "Ec*******",
                    # 商品标题 [原字段 'item_name']
                    "title": "Pr*******",
                    # 商品略缩图链接 [原字段 'small_image_url']
                    "thumbnail_url": "https://m.*******.jpg",
                    # 产品类型 (1: 普通产品, 2: 多属性产品) [原字段 'store_type']
                    "product_type": 1,
                    # 商品价格的货币代码
                    "currency_code": "EUR",  # 商品价格的货币代码
                    # 商品标准价 (不包含促销, 运费, 积分) [原字段 'price']
                    "standard_price": 50.99,
                    # 商品优惠价 [原字段 'listing_price']
                    "sale_price": 43.99,
                    # 商品运费
                    "shipping": 0.0,
                    # 商品积分 (适用于日本站点)
                    "points": 0.0,
                    # 商品到手价 (包含促销, 运费, 积分)
                    "landed_price": 43.99,
                    # 商品昨天的总销售额 [原字段 'yesterday_amount']
                    "sales_amt_1d": 660.96,
                    # 商品7天的总销售额 [原字段 'seven_amount']
                    "sales_amt_7d": 2183.26,
                    # 商品7天的总销售额 [原字段 'seven_amount']
                    "sales_amt_14d": 6111.12,
                    # 商品30天的总销售额 [原字段 'thirty_amount']
                    "sales_amt_30d": 15910.32,
                    # 商品昨天的总销量 [原字段 'yesterday_volume']
                    "sales_qty_1d": 15,
                    # 商品7天的总销量 [原字段 'total_volume']
                    "sales_qty_7d": 50,
                    # 商品14天的总销量 [原字段 'fourteen_volume']
                    "sales_qty_14d": 140,
                    # 商品30天的总销量 [原字段 'thirty_volume']
                    "sales_qty_30d": 367,
                    # 商品7天的日均销量 [原字段 'average_seven_volume']
                    "sales_avg_qty_7d": 7.1,
                    # 商品14天的日均销量 [原字段 'average_fourteen_volume']
                    "sales_avg_qty_14d": 10.0,
                    # 商品30天的日均销量 [原字段 'average_thirty_volume']
                    "sales_avg_qty_30d": 12.2,
                    # 商品所属主类目 [原字段 'seller_category_new']
                    "category": ["Computer & Zubehör"],
                    # 商品主类目排名 [原字段 'seller_rank']
                    "category_rank": 5710,
                    # 商品小类和排名列表 [原字段 'small_rank']
                    "subcategories": [
                        {
                            # 商品所属小类目 [原字段 'category']
                            "subcategory": "Tintenpatronen",
                            # 商品小类目排名 [原字段 'rank']
                            "subcategory_rank": 502,
                        },
                        ...
                    ],
                    # 商品评价数量 [原字段 'review_num']
                    "review_count": 100,
                    # 商品评价星级 [原字段 'last_star']
                    "review_stars": 5.0,
                    # 商品配送方式 (如: "FBA" 或 "FBM") [原字段 'fulfillment_channel_type']
                    "fulfillment_channel": "FBA",
                    # FBM 可售库存数量 [原字段 'quantity']
                    "mfn_fulfillable": 0,
                    # FBA 在库可售的库存数量 [原字段 'afn_fulfillable_quantity']
                    "afn_fulfillable": 1026,
                    # FBA 在库不可售的库存数量 [原字段 'afn_unsellable_quantity']
                    "afn_unsellable": 13,
                    # FBA 在库待调仓的库存数量 [原字段 'reserved_fc_processing']
                    "afn_reserved_fc_processing": 8,
                    # FBA 在库调仓中的库存数量 [原字段 'reserved_fc_transfers']
                    "afn_reserved_fc_transfers": 193,
                    # FBA 在库待发货的库存数量 [原字段 'reserved_customerorders']
                    "afn_reserved_customer_order": 26,
                    # FBA 发货计划入库的库存数量 [原字段 'afn_inbound_working_quantity']
                    "afn_inbound_working": 0,
                    # FBA 发货在途的库存数量 [原字段 'afn_inbound_shipped_quantity']
                    "afn_inbound_shipped": 800,
                    # FBA 发货入库接收中的库存数量 [原字段 'afn_inbound_receiving_quantity']
                    "afn_inbound_receiving": 0,
                    # 商品状态 (0: 停售, 1: 在售)
                    "status": 1,
                    # 商品是否已删除 (0: 未删除, 1: 已删除) [原字段 'is_delete']
                    "deleted": 0,
                    # 商品创建时间 (时区时间) [原字段 'open_date_display']
                    "create_time": "2024-07-20 09:44:06 +03:00",
                    # 商品开售日期 (如: "2023-06-23") [原字段 'on_sale_time']
                    "on_sale_date": "2024-07-20",  # 开售日期 [原字段 'on_sale_time']
                    # 商品首次下单日期 (如: "2023-06-23") [原字段 'first_order_time']
                    "first_order_date": "2024-07-26",  # 首次下单日期 [原字段 'first_order_time']
                    # 商品更新时间 (UTC时间) [原字段 'listing_update_date']
                    "update_time_utc": "2025-05-22 16:06:56",
                    # 领星配对时间 (北京时间) [原字段 'pair_update_time']
                    "pair_time_cnt": "2025-03-14 19:03:28",
                    # 商品尺寸和重量 [原字段 'dimension_info']
                    "dimensions": [
                        {
                            # 商品高度
                            "item_height": 1.46,
                            # 商品高度单位 [原字段 'item_height_units_type']
                            "item_height_unit": "inches",
                            # 商品长度
                            "item_length": 4.41,
                            # 商品长度单位 [原字段 'item_length_units_type']
                            "item_length_unit": "inches",
                            # 商品宽度
                            "item_width": 4.8,
                            # 商品宽度单位 [原字段 'item_width_units_type']
                            "item_width_unit": "inches",
                            # 商品重量
                            "item_weight": 0.0,
                            # 商品重量单位 [原字段 'item_weight_units_type']
                            "item_weight_unit": "",
                            # 商品包装高度
                            "package_height": 1.54,
                            # 商品包装高度单位 [原字段 'package_height_units_type']
                            "package_height_unit": "inches",
                            # 商品包装长度
                            "package_length": 6.22,
                            # 商品包装长度单位 [原字段 'package_length_units_type']
                            "package_length_unit": "inches",
                            # 商品包装宽度
                            "package_width": 4.45,
                            # 商品包装宽度单位 [原字段 'package_width_units_type']
                            "package_width_unit": "inches",
                            # 商品包装重量
                            "package_weight": 0.2,
                            # 商品包装重量单位 [原字段 'package_weight_units_type']
                            "package_weight_unit": "pounds",
                        },
                        ...
                    ],
                    # 商品负责人 [原字段 'principal_info']
                    "operators": [
                        {
                            # 负责人的领星帐号ID (Account.user_id) [原字段 'principal_uid']
                            "user_id": 1*******,
                            # 负责人的领星帐号显示姓名 (Account.display_name) [原字段 'principal_name']
                            "user_name": "白小白"
                        },
                        ...
                    ],
                    # 商品标签信息 [原字段 'global_tags']
                    "tags": [
                        {
                            # 领星标签ID (ListingGlobalTag.tag_id) [原字段 'globalTagId']
                            "tag_id": 1000**************,
                            # 领星标签名称 (ListingGlobalTag.tag_name) [原字段 'tagName']
                            "tag_name": "特殊产品",
                            # 领星标签颜色 [原字段 'color']
                            "tag_color": "#4B8BFA"
                        },
                        ...
                    ],
                },
                ...
            ],
        }
        ```
        """
        url = route.LISTINGS
        # 解析并验证参数
        args = {
            "sids": sids,
            "search_field": search_field,
            "search_mode": search_mode,
            "search_value": search_value,
            "deleted": deleted,
            "paired": paired,
            "pair_start_time": pair_start_time,
            "pair_end_time": pair_end_time,
            "update_start_time": update_start_time,
            "update_end_time": update_end_time,
            "product_type": product_type,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.Listings.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.Listings.model_validate(data)

    async def EditListingOperators(
        self,
        *operator: dict,
    ) -> schema.EditListingResult:
        """批量更新Listing的负责人

        ## Docs:
        - 销售 - Listing: [批量分配Listing负责人](https://apidoc.lingxing.com/#/docs/Sale/UpdatePrincipal)

        :params *operator `<'dict'>`: 支持最多200个Listing的负责人分配信息

            - 每个字典必须包含 `sid`, `asin`, `name` 字段, 如:
              `{'sid': 1, 'asin': 'B0XXXXXXXX', 'name': ['白小白']}`
            - 必填字段 `sid` 领星店铺ID, 必须是 int 类型, 参数来源: `Listing.sid`
            - 必填字段 `asin` 商品ASIN码, 必须是 str 类型, 参数来源: `Listing.asin`
            - 可选字段 `name` 负责人名称, 可以是 str 或 list[str] 类型, 最多支持10个负责人,
              若不填写或传入 `None` 则表示清空负责人, 参数来源: `Account.display_name`

        :returns `<'EditListingResult'>`: 返回批量更新的结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [{'index': 0, 'message': '负责人:白小白不存在'}],
            # 请求ID
            "request_id": "44DAC5AE-7D76-9054-2431-0EF7E357CFE5",
            # 响应时间
            "response_time": "2025-08-13 19:23:04",
            # 响应结果
            "data": {
                # 总更新个数
                "total": 2,
                # 更新成功个数 [原字段 'success']
                "success": 1,
                # 更新失败个数 [原字段 'error']
                "failure": 1,
            },
        }
        ```
        """
        url = route.EDIT_LISTING_OPERATORS
        # 解析并验证参数
        args = {"operators": operator}
        try:
            p = param.EditListingOperators.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.EditListingResult.model_validate(data)

    async def EditListingPrices(
        self,
        *price: dict,
    ) -> schema.EditListingPricesResult:
        """批量修改Listing的价格

        ## Docs:
        - 销售 - Listing: [批量修改Listing价格](https://apidoc.lingxing.com/#/docs/Sale/pricingSubmit)

        :params *prices `<'dict'>`: 支持多个Listing的价格修改信息

            - 每个字典必须包含 `sid`, `msku`, `standard_price` 字段, 如:
              `{"sid": 1, "msku": "SKU*******", "standard_price": 42.98}`
            - 必填字段 `sid` 领星店铺ID, 必须是 int 类型, 参数来源: `Listing.sid`
            - 必填字段 `msku` 亚马逊卖家SKU, 必须是 str 类型, 参数来源: `Listing.msku`
            - 必填字段 `standard_price` 商品标准价, 必须是 float 类型, 参数来源: `Listing.standard_price`
            - 可选字段 `sale_price` 商品优惠价, 必须是 float 类型, 参数来源: `Listing.sale_price`
            - 可选字段 `start_date` 商品优惠价开始时间, 必须是 str/date/datetime 类型
            - 可选字段 `end_date` 商品优惠价结束时间, 必须是 str/date/datetime 类型

        :returns `<'EditListingPriceResult'>`: 返回批量修改的结果
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
            # 响应结果
            "data": {
                # 更新成功个数 [原字段 'success_num']
                'success': 1,
                # 更新失败个数 [原字段 'failure_num']
                'failure': 1,
                # 更新失败的详情
                'failure_detail': [
                    {
                        # 领星店铺ID (Seller.sid)
                        'sid': 1,
                        # 商品ASIN码 (Listing.asin)
                        'asin': 'B0********',
                        # 亚马逊卖家SKU (Listing.msku)
                        'msku': 'SKU*******',
                        # 错误信息 [原字段 'msg']
                        'message': '当前调价未完成，请勿重复操作'
                    },
                    ...
                ],
            },
        }
        ```
        """
        url = route.EDIT_LISTING_PRICES
        # 解析并验证参数
        args = {"prices": price}
        try:
            p = param.EditListingPrices.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.EditListingPricesResult.model_validate(data)

    async def PairListingProducts(
        self,
        *pair_product: dict,
    ) -> schema.EditListingResult:
        """批量添加Listing与领星本地SKU的配对关系

        ## Docs:
        - 销售 - Listing: [批量添加/编辑Listing配对](https://apidoc.lingxing.com/#/docs/Sale/Productlink)

        :params *pair_product `<'dict'>`: 支持添加多个Listing与领星本地SKU的配对关系

            - 每个字典必须包含 `msku`, `lsku`, `sync_pic` 字段, 如:
              `{"msku": "SKU*******", "lsku": "LOCAL*******", "sync_pic": 1}`
            - 必填字段 `msku` 亚马逊卖家SKU, 必须是 str 类型, 参数来源: `Listing.msku`
            - 必填字段 `lsku` 领星本地SKU, 必须是 str 类型, 参数来源: `Listing.lsku`
            - 必填字段 `sync_pic` 领星本地SKU是否同步Listing图片, 必须是 int 类型 (0: 否, 1: 是)
            - 可选字段 `seller_id` 亚马逊卖家ID, 必须是 str 类型, 参数来源: `Seller.seller_id`
            - 可选字段 `marketplace_id` 亚马逊市场ID, 必须是 str 类型, 参数来源: `Seller.marketplace_id`

        :returns `<'UpdateListingResult'>`: 返回批量配对的结果
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
            # 响应结果
            "data": {
                # 总更新个数
                "total": 1,
                # 更新成功个数 [原字段 'success']
                "success": 1,
                # 更新失败个数 [原字段 'error']
                "failure": 0,
            },
        }
        ```
        """
        url = route.PAIR_LISTING_PRODUCTS
        # 解析并验证参数
        args = {"pair_products": pair_product}
        try:
            p = param.PairListingProducts.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.EditListingResult.model_validate(data)

    async def UnpairListingProducts(
        self,
        *unpair_product: dict,
    ) -> base_schema.ResponseResult:
        """批量解除Listing与领星本地SKU的配对关系

        ## Docs:
        - 销售 - Listing: [解除Listing配对](https://apidoc.lingxing.com/#/docs/Sale/UnlinkListing)

        :params *unpair_product `<'dict'>`: 支持解除多个Listing与领星本地SKU的配对关系

            - 每个字典必须包含 `sid` 和 `msku` 字段, 如:
              `{“sid”: 1, "msku": "SKU*******"}`
            - 必填字段 `sid` 领星店铺ID, 必须是 int 类型, 参数来源: `Listing.sid`
            - 必填字段 `msku` 亚马逊卖家SKU, 必须是 str 类型, 参数来源: `Listing.msku`

        :returns `<'ResponseResult'>`: 返回批量解除配对的结果
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
            # 响应结果
            "data": None,
        }
        ```
        """
        url = route.UNPAIR_LISTING_PRODUCTS
        # 解析并验证参数
        args = {"unpair_products": unpair_product}
        try:
            p = param.UnpairListingProducts.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return base_schema.ResponseResult.model_validate(data)

    async def ListingGlobalTags(
        self,
        *,
        search_value: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.ListingGlobalTags:
        """查询Listing可标记的全局标签

        ## Docs:
        - 销售 - Listing: [查询Listing标签列表](https://apidoc.lingxing.com/#/docs/Sale/globalTagPageList)

        :param search_value `<'str'>`: 查询的标签名称, 默认 `None` (所有标签),
            参数来源: `ListingGlobalTag.tag_name`
        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 最大支持 200, 默认 `None` (使用: 20)
        :returns `<'ListingGlobalTags'>`: 返回查询到的 Listing 标签信息列表
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
                    # 领星标签ID [原字段 'global_tag_id']
                    'tag_id': '900000000000000000',
                    # 领星标签名称
                    'tag_name': '特殊Listing',
                    # 标签类型 [原字段 'type']
                    'tag_type': '商品标签',
                    # 标签的关联对象 [原字段 'tag_object']
                    'tag_attachment': 'ASIN',
                    # 标签当前关联对象的总数量 [原字段 'relation_count']
                    'tag_attachment_count': 1,
                    # 标签最初创建者 (Account.display_name) [原字段 'create_by_name']
                    'created_by': '白小白',
                    # 标签创建时间 (北京时间) [原字段 'create_by']
                    'create_time': '2023-08-20 09:53:08',
                    # 标签最后编辑者 (Account.display_name) [原字段 'modify_by_name']
                    'modified_by': '白小白',
                    # 标签修改时间 (北京时间) [原字段 'modify_by']
                    'modify_time': '2024-08-20 09:53:08',
                },
                ...
            ],
        }
        ```
        """
        url = route.LISTING_GLOBAL_TAGS
        # 解析并验证参数
        args = {
            "search_value": search_value,
            "search_field": "tag_name" if search_value is not None else None,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.ListingGlobalTags.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.ListingGlobalTags.model_validate(data)

    async def CreateListingGlobalTag(self, tag_name: str) -> base_schema.ResponseResult:
        """创建Listing可设置的全局标签

        ## Docs:
        - 销售 - Listing: [添加Listing标签](https://apidoc.lingxing.com/#/docs/Sale/globalTagAddTag)

        :param tag_name `<'str'>`: 领星标签名称, 如: `"特殊Listing"`
        :returns `<'ResponseResult'>`: 返回添加结果
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
            # 响应结果
            "data": None,
        }
        ```
        """
        url = route.CREATE_LISTING_GLOBAL_TAG
        # 解析并验证参数
        args = {"tag_name": tag_name}
        try:
            p = param.CreateListingGlobalTag.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return base_schema.ResponseResult.model_validate(data)

    async def RemoveListingGlobalTag(self, *tag_id: str) -> base_schema.ResponseResult:
        """删除Listing可设置的全局标签

        ## Docs:
        - 销售 - Listing: [删除Listing标签](https://apidoc.lingxing.com/#/docs/Sale/globalTagRemoveTag)

        :param *tag_id `<'str'>`: 支持最多删除200个标签ID, 参数来源: `ListingGlobalTag.tag_id`
        :returns `<'ResponseResult'>`: 返回删除结果
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
            # 响应结果
            "data": None,
        }
        ```
        """
        url = route.REMOVE_LISTING_GLOBAL_TAG
        # 解析并验证参数
        args = {"tag_ids": tag_id}
        try:
            p = param.RemoveListingGlobalTag.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return base_schema.ResponseResult.model_validate(data)

    async def ListingTags(self, *msku: dict) -> schema.ListingTags:
        """查询指定Listing当前标记的标签

        ## Docs:
        - 销售 - Listing: [查询Listing标记标签列表](https://apidoc.lingxing.com/#/docs/Sale/queryListingRelationTagList)

        :param *msku `<'dict'>`: 支持最多查询100个Listing当前标记的标签

            - 每个字典必须包含 `sid` 和 `msku` 字段, 如:
              `{"sid": 1, "msku": "SKU*******"}`
            - 必填字段 `sid` 领星店铺ID, 必须是 int 类型, 参数来源: `Listing.sid`
            - 必填字段 `msku` 亚马逊卖家SKU, 必须是 str 类型, 参数来源: `Listing.msku`

        :returns `<'ListingTags'>`: 返回批量查询的Listing当前所标记的标签信息列表
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
                    # 领星店铺ID (Seller.sid)
                    "sid": 1,
                    # 亚马逊卖家SKU (Listing.msku) [原字段 'relation_id']
                    "msku": "SKU*******",
                    # 标签信息列表 [原字段 'tag_infos']
                    "tags": [
                        {
                            # 领星标签ID (ListingGlobalTag.tag_id) [原字段 'global_tag_id']
                            "tag_id": "90000*************",
                            # 领星标签名称 (ListingGlobalTag.tag_name) [原字段 'tag_name']
                            "tag_name": "特殊",
                            # 领星标签颜色 [原字段 'color']
                            "tag_color": "#F05B56",
                        },
                        ...
                    ]
                },
                ...
            ],
        }
        ```
        """
        url = route.LISTING_TAGS
        # 解析并验证参数
        args = {"mskus": msku}
        try:
            p = param.ListingTagsMskus.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.ListingTags.model_validate(data)

    async def SetListingTag(
        self,
        tag_ids: str | list[str],
        *msku: dict,
    ) -> base_schema.ResponseResult:
        """批量给指定Listing设置标签

        ## Docs:
        - 销售 - Listing: [Listing新增商品标签](https://apidoc.lingxing.com/#/docs/Sale/AddGoodsTag)

        :param tag_ids `<'str/list[str]'>`: 单个领星标签ID或ID列表, 参数来源: `ListingGlolbalTag.tag_id`
        :param *msku `<'dict'>`: 需要设置对应标签的Listing信息

            - 每个字典必须包含 `sid` 和 `msku` 字段, 如:
              `{"sid": 1, "msku": "SKU*******"}`
            - 必填字段 `sid` 领星店铺ID, 必须是 int 类型, 参数来源: `Listing.sid`
            - 必填字段 `msku` 亚马逊卖家SKU, 必须是 str 类型, 参数来源: `Listing.msku`

        :returns `<'ResponseResult'>`: 返回设置结果
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
            # 响应结果
            "data": None,
        }
        ```
        """
        url = route.SET_LISTING_TAG
        # 解析并验证参数
        args = {"tag_ids": tag_ids, "mskus": msku}
        try:
            p = param.SetListingTag.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return base_schema.ResponseResult.model_validate(data)

    async def UnsetListingTag(
        self,
        tag_ids: str | list[str],
        *msku: dict,
    ) -> base_schema.ResponseResult:
        """批量给指定Listing移除标签

        ## Docs:
        - 销售 - Listing: [Listing删除商品标签](https://apidoc.lingxing.com/#/docs/Sale/DeleteGoodsTag)

        :param tag_ids `<'str/list[str]'>`: 单个领星标签ID或ID列表, 参数来源: `ListingGlolbalTag.tag_id`
        :param *msku `<'dict'>`: 需要移除对应标签的Listing信息

            - 每个字典必须包含 `sid` 和 `msku` 字段, 如:
              `{"sid": 1, "msku": "SKU*******"}`
            - 必填字段 `sid` 领星店铺ID, 必须是 int 类型, 参数来源: `Listing.sid`
            - 必填字段 `msku` 亚马逊卖家SKU, 必须是 str 类型, 参数来源: `Listing.msku`

        :returns `<'ResponseResult'>`: 返回删除结果
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
            # 响应结果
            "data": None,
        }
        ```
        """
        url = route.UNSET_LISTING_TAG
        # 解析并验证参数
        args = {"tag_ids": tag_ids, "mskus": msku}
        try:
            p = param.UnsetListingTag.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return base_schema.ResponseResult.model_validate(data)

    async def ListingFbaFees(self, *msku: dict) -> schema.ListingFbaFees:
        """批量获取Listing的预估FBA费用

        ## Docs:
        - 销售 - Listing: [批量获取Listing费用](https://apidoc.lingxing.com/#/docs/Sale/GetPrices)

        :param *msku `<'dict'>`: 支持最多500个Listing的FBA费用查询

            - 每个字典必须包含 `sid` 和 `msku` 字段, 如:
              `{"sid": 1, "msku": "SKU*******"}`
            - 必填字段 `sid` 领星店铺ID, 必须是 int 类型, 参数来源: `Listing.sid`
            - 必填字段 `msku` 亚马逊卖家SKU, 必须是 str 类型, 参数来源: `Listing.msku`

        :returns `<'ListingFbaFees'>`: 返回批量查询的预估FBA费用信息列表
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
                    # 领星店铺ID (Seller.sid)
                    "sid": 1,
                    # 亚马逊卖家SKU (Listing.msku)
                    "msku": "SKU*******",
                    # 预估FBA费用
                    "fba_fee": 2.39,
                    # 预估FBA费用货币代码 [原字段 'fba_fee_currency_code']
                    "currency_code": "EUR"
                },
                ...
            ],
        }
        ```
        """
        url = route.LISTING_FBA_FEES
        # 解析并验证参数
        args = {"mskus": msku}
        try:
            p = param.ListingFbaFeesMskus.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.ListingFbaFees.model_validate(data)

    async def EditListingFbms(
        self,
        *msku: dict,
    ) -> schema.EditListingFbmsResult:
        """批量修改FBM库存和处理时间

        ## Docs:
        - 销售 - Listing: [修改FBM库存&处理时间](https://apidoc.lingxing.com/#/docs/Sale/UpdateFbmInventory)

        :params *msku `<'dict'>`: 支持最多200个Listing的FBM库存修改

            - 每个字典必须包含 `sid`, `msku`, `qty` 字段, 如:
              `{"sid": 1, "msku": "SKU*******", "qty": 100}`
            - 必填字段 `sid` 领星店铺ID, 必须是 int 类型, 参数来源: `Listing.sid`
            - 必填字段 `msku` 亚马逊卖家SKU, 必须是 str 类型, 参数来源: `Listing.msku`
            - 必填字段 `qty` FBM库存数量, 必须是 int 类型
            - 可填字段 `ship_days` 发货/处理天数, 必须是 int 类型

        :returns `<'EditListingFbmsResult'>`: 返回批量修改FBM库存的结果
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
            # 响应结果
            "data": {
                # 更新成功个数 [原字段 'successNum']
                "success": 1,
                # 更新失败个数 [原字段 'failureNum']
                "failure": 1,
                # 更新失败的详情 [原字段 'failureDetail']
                "failure_detail": [
                    {
                        # 领星店铺ID (Seller.sid) [原字段 'storeId']
                        "sid": 1,
                        # 商品ASIN码 (Listing.asin)
                        "asin": "B0*******",  # 商品ASIN码
                        # 亚马逊卖家SKU (Listing.msku)
                        "msku": "SKU*******",
                        # 错误信息 [原字段 'msg']
                        "message": "FBA类型的Listing不支持修改FBM库存"
                    },
                    ...
                ],
            },
        }
        """
        url = route.EDIT_LISTING_FBMS
        # 解析并验证参数
        args = {"mskus": msku}
        try:
            p = param.EditListingFbms.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.EditListingFbmsResult.model_validate(data)

    async def ListingOperationLogs(
        self,
        sid: int,
        msku: str,
        *,
        operator_ids: str | list[str] | None = None,
        operation_types: int | list[int] | None = None,
        start_time: str | datetime.date | datetime.datetime | None = None,
        end_time: str | datetime.date | datetime.datetime | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.ListingOperationLogs:
        """查询Listing操作日志

        ## Docs:
        - 销售 - Listing: [查询Listing操作日志列表](https://apidoc.lingxing.com/#/docs/Sale/listingOperateLogPageList)

        :param sid `<'int'>`: 领星店铺ID, 参数来源: `Listing.sid`
        :param msku `<'str'>`: 亚马逊卖家SKU, 参数来源: `Listing.msku`
        :param operator_ids `<'str/list[str]'>`: 操作用户ID或ID列表,
            默认 `None` (查询所有用户), 参数来源: `Account.user_id`
        :param operation_types `<'int/list[int]'>`: 操作类型或类型列表, 默认 `None` (查询所有类型)

            - `1`: 调价
            - `2`: 调库存
            - `3`: 修改标题,
            - `4`: 编辑商品
            - `5`: B2B调价

        :param start_time `<'str/date/datetime'>`: 操作开始时间, 默认 `None` (查询所有时间)
        :param end_time `<'str/date/datetime'>`: 操作结束时间, 默认 `None` (查询所有时间)
        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 默认 `None` (使用: 20)
        :returns `<'ListingOperationLogs'>`: 返回查询到的 Listing 操作日志信息
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
                    # 领星店铺ID (Seller.sid)
                    'sid': 9828,
                    # 操作用户名称 [原字段 'operate_user']
                    'operator': '超级管理员',
                    # 操作类型 [原字段 'operate_type']
                    'operation_type': 1,
                    # 操作类型说明 [原字段 'operate_type_text']
                    'operation_type_desc': '调价',
                    # 操作时间 (北京时间) [原字段 'operate_time']
                    'operate_time': '2025-07-14 12:16:21',
                    # 操作详情 [原字段 'operate_detail']
                    'operate_detail': '手动调价: 【价格】€17.99 -> €12.11',
                },
                ...
            ],
        }
        ```
        """
        url = route.LISTING_OPERATION_LOGS
        # 解析并验证参数
        args = {
            "sid": sid,
            "msku": msku,
            "operator_ids": operator_ids,
            "operation_types": operation_types,
            "start_time": start_time,
            "end_time": end_time,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.ListingOperationLogs.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.ListingOperationLogs.model_validate(data)

    # 平台订单 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    async def Orders(
        self,
        start_time: str | datetime.date | datetime.datetime,
        end_time: str | datetime.date | datetime.datetime,
        *,
        time_type: int | None = None,
        time_sort: int | None = None,
        sids: int | list[int] | None = None,
        fulfillment_channel: int | None = None,
        order_status: ORDER_STATUS | list[ORDER_STATUS] | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.Orders:
        """查询亚马逊订单

        ## Docs:
        - 销售 - 平台订单: [查询亚马逊订单列表](https://apidoc.lingxing.com/#/docs/Sale/Orderlists)

        :param start_time `<'str/date/datetime'>`: 查询开始时间
        :param end_time `<'str/date/datetime'>`: 查询结束时间
        :param time_type `<'int'>`: 查询时间类型, 默认 `None` (使用: 1)

            - `1`: 订购站点时间 (Order.purchase_time_loc)
            - `2`: 领星更新北京时间 (Order.modify_time_cnt)
            - `3`: 亚马逊更新UTC时间 (Order.update_time_utc)
            - `4`: 发货站点时间 (Order.shipment_time_loc)

        :param time_sort `<'int'>`: 是否按时间排序, 默认 `None` (使用: 0)

            - `0`: 不排序
            - `1`: 按时间降序
            - `2`: 按时间升序

        :param sids `<'int/list[int]'>`: 领星店铺ID或ID列表,
            默认 `None` (所有店铺), 参数来源: `Order.sid`

        :param fulfillment_channel `<'int'>`: 配送方式,
            默认 `None` (所有方式), 参数来源: `Order.fulfillment_channel`

            - `1`: AFN亚马逊配送
            - `2`: MFN卖家自发货

        :param order_status `<'str/list[str]'>`: 订单状态或状态列表,
            默认 `None` (所有状态), 参数来源: `Order.order_status`

            - `"Pending"` (待处理)
            - `"Shipped"` (已发货)
            - `"Unshipped"` (未发货)
            - `"PartiallyShipped"` (部分发货)
            - `"Canceled"` (已取消)

        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 最大支持 5000, 默认 `None` (使用: 1000)
        :returns `<'Orders'>`: 返回查询到的订单信息列表
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
                    # 领星店铺ID (Seller.sid)
                    "sid": 1,
                    # 领星店铺名称 (Seller.name)
                    "seller_name": "Store****",
                    # 亚马逊订单ID
                    "amazon_order_id": "205-*******-*******",
                    # 销售渠道
                    "sales_channel": "Amazon.co.uk",
                    # 配送方式 ("AFN" 或 "MFN")
                    "fulfillment_channel": "AFN",
                    # 物流追踪号码
                    "tracking_number": "UK3*********",
                    # 订单状态
                    "order_status": "Shipped",
                    # 是否为退货订单 (0: 否, 1: 是)
                    "is_return_order": 0,
                    # 退货订单的状态 [原字段 'is_return']
                    # (0: 未退货, 1: 退货中, 2: 完成退货/退款, 3: 被标记为领星本地的退货订单)
                    "return_order_status": 0,
                    # 是否为换货订单 (0: 否, 1: 是)
                    "is_replacement_order": 0,
                    # 换货订单的状态 [原字段 'is_replaced_order'] (0: 未换货, 1: 完成换货)
                    "replacement_order_status": 0,
                    # 是否为多渠道配送订单 (0: 否, 1: 是)
                    "is_mcf_order": 0,
                    # 是否被标记为领星本地的推广订单 [原字段 'is_assessed'] (0: 否, 1: 是)
                    "is_promotion_tagged": 0,
                    # 订单金额的货币代码 [原字段 'order_total_currency_code']
                    "order_currency_code": "GBP",
                    # 订单总金额 [原字段 'order_total_amount']
                    "order_amt": 28.89,
                    # 退款金额
                    "refund_amt": 0.0,
                    # 买家名字
                    "buyer_name": "",
                    # 买家电子邮箱
                    "buyer_email": "",
                    # 买家电话号码 [原字段 'phone']
                    "buyer_phone": "",
                    # 买家地址 [原字段 'address']
                    "buyer_address": "",
                    # 买家邮政编码 [原字段 'postal_code']
                    "buyer_postcode": "C*** ***",
                    # 订购时间 (时区时间) [原字段 'purchase_date']
                    "purchase_time": "2025-07-07T13:14:58Z",
                    # 订购时间 (UTC时间) [原字段 'purchase_date_local_utc']
                    "purchase_time_utc": "2025-07-07 13:14:58",
                    # 订购时间 (站点时间) [原字段 'purchase_date_local']
                    "purchase_time_loc": "2025-07-07 14:14:58",
                    # 发货时间 (时区时间) [原字段 'shipment_date']
                    "shipment_time": "2025-07-07T16:54:47+00:00",
                    # 发货时间 (UTC时间) [原字段 'shipment_date_utc']
                    "shipment_time_utc": "2025-07-07 16:54:47",
                    # 发货时间 (站点时间) [原字段 'shipment_date_local']
                    "shipment_time_loc": "2025-07-07 17:54:47",
                    # 最早发货时间 (时区时间) [原字段 'earliest_ship_date']
                    "earliest_ship_time": "2025-07-08T22:59:59Z",
                    # 最早发货时间 (UTC时间) [原字段 'earliest_ship_date_utc']
                    "earliest_ship_time_utc": "2025-07-08 22:59:59",
                    # 付款确认时间 (时区时间) [原字段 'posted_date_utc']
                    "posted_time": "2025-07-15T20:45:48Z",
                    # 付款确认时间 (UTC时间) [原字段 'posted_date']
                    "posted_time_utc": "2025-07-15 20:45:48",
                    # 亚马逊订单更新时间 (UTC时间) [原字段 'last_update_date_utc']
                    "update_time_utc": "2025-07-08 02:23:15",
                    # 亚马逊订单更新时间 (站点时间) [原字段 'last_update_date']
                    "update_time_loc": "2025-07-08 03:23:15",
                    # 领星订单更新时间 (北京时间) [原字段 'gmt_modified']
                    "modify_time_cnt": "2025-07-08 10:31:14",
                    # 领星订单更新时间 (UTC时间) [原字段 'gmt_modified_utc']
                    "modify_time_utc": "2025-07-08 02:31:14",
                    # 订单中的商品列表 [原字段 'items_list']
                    "items": [
                        {
                            # 商品ASIN (Listing.asin)
                            "asin": "B0D2D6922Q",
                            # 亚马逊卖家SKU (Listing.msku) [原字段 'seller_sku']
                            "msku": "907-FGB-305XL-1B1C-UK",
                            # 领星本地SKU (Listing.lsku) [原字段 'local_sku']
                            "lsku": "902-CB-305-1B1C-UK",
                            # 领星本地商品名 (Listing.product_name) [原字段 'local_name']
                            "product_name": "HP305-1B1C",
                            # 订购数量 [原字段 'quantity_ordered']
                            "order_qty": 1,
                            # 订单状态
                            "order_status": "Shipped",
                        },
                        ...
                    ],
                },
                ...
            ],
        }
        ```
        """
        url = route.ORDERS
        # 解析并验证参数
        args = {
            "start_time": start_time,
            "end_time": end_time,
            "time_type": time_type,
            "time_sort": time_sort,
            "sids": sids,
            "fulfillment_channel": fulfillment_channel,
            "order_status": order_status,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.Orders.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.Orders.model_validate(data)

    async def OrderDetails(self, *amazon_order_ids: str) -> schema.OrderDetails:
        """查询亚马逊订单详情

        ## Docs:
        - 销售 - 平台订单: [查询亚马逊订单详情](https://apidoc.lingxing.com/#/docs/Sale/OrderDetail)

        :param *amazon_order_ids `<'str'>`: 支持最多查询200个订单详情, 参数来源: `Order.amazon_order_id`
        :returns `<'OrderDetails'>`: 返回查询到的订单详情信息列表
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
                    # 领星店铺ID (Seller.sid)
                    "sid": 1,
                    # 亚马逊订单ID (Order.amazon_order_id)
                    "amazon_order_id": "171-*******-*******",
                    # 销售渠道 (如: "Amazon.com")
                    "sales_channel": "Amazon.es",
                    # 配送方式 ("AFN" 或 "MFN")
                    "fulfillment_channel": "AFN",
                    # 订单类型
                    "order_type": "StandardOrder",
                    # 订单状态
                    "order_status": "Shipped",
                    # 是否为退货订单 (0: 否, 1: 是)
                    "is_return_order": 0,
                    # 退货订单的状态 [原字段 'is_return']
                    # (0: 未退货, 1: 退货中, 2: 完成退货/退款, 3: 被标记为领星本地的退货订单)
                    "return_order_status": 0,
                    # 是否为换货订单 (0: 否, 1: 是)
                    "is_replacement_order": 0,
                    # 换货订单的状态 (0: 未换货, 1: 完成换货) [原字段 'is_replaced_order']
                    "replacement_order_status": 0,
                    # 是否为促销折扣订单 (0: 否, 1: 是) [原字段 'is_promotion']
                    # 当 OrderDetailItem.promotion_discount_amt > 0 时,
                    # 此字段为 1, 其他 discount_amt 不计做 promotioin 类型
                    "is_promotion_order": 0,
                    # 是否为B2B订单 (0: 否, 1: 是) [原字段 'is_business_order']
                    "is_b2b_order": 0,
                    # 是否为Prime订单 (0: 否, 1: 是) [原字段 'is_prime']
                    "is_prime_order": 0,
                    # 是否为优先配送订单 (0: 否, 1: 是)
                    "is_premium_order": 0,
                    # 是否为多渠道配送订单 (0: 否, 1: 是)
                    "is_mcf_order": 0,
                    # 是否被用户标记为领星本地的推广订单 (0: 否, 1: 是) [原字段 'is_assessed']
                    "is_user_promotion_order": 0,
                    # 订单已发货数量 [原字段 'number_of_items_shipped']
                    "shipped_qty": 1,
                    # 订单未发货数量 [原字段 'number_of_items_unshipped']
                    "unshipped_qty": 0,
                    # 订单金额的货币代码 [原字段 'order_total_currency_code']
                    "order_currency_code": "EUR",
                    # 订单金额的货币图标 [原字段 'icon']
                    "order_currency_icon": "€",
                    # 订单销售总金额 [原字段 'order_total_amount']
                    "order_sales_amt": 29.98,
                    # 订单金额费用是否含税 (1: 含税, 2: 不含税) [原字段 'taxes_included']
                    "order_tax_inclusive": 1,
                    # 订单税务分类 [原字段 'tax_classifications']
                    "order_tax_class": "",
                    # 订单配送服务级别 [原字段 'ship_service_level']
                    "shipment_service": "Expedited",
                    # 订单配送服务级别类型 [原字段 'shipment_service_level_category']
                    "shipment_service_category": "Expedited",
                    # 采购订单编号 (买家结账时输入)
                    "purchase_order_number": "",
                    # 付款方式 ("COD", "CVS", "Other")
                    "payment_method": "Other",
                    # 亚马逊结账 (CBA) 的自定义发货标签 [原字段 'cba_displayable_shipping_label']
                    "cba_shipping_label": "",
                    # 买家姓名
                    "buyer_name": "M*****",
                    # 买家电子邮箱
                    "buyer_email": "v********@marketplace.amazon.es",
                    # 买家电话号码 [原字段 'phone']
                    "buyer_phone": "",
                    # 买家所在国家 [原字段 'country']
                    "buyer_country": "ES",
                    # 买家所在国家代码 [原字段 'country_code']
                    "buyer_country_code": "ES",
                    # 买家所在省/州 [原字段 'state_or_region']
                    "buyer_state": "Valencia",
                    # 买家所在城市 [原字段 'city']
                    "buyer_city": "Valencia",
                    # 买家所在区县 [原字段 'district']
                    "buyer_district": "",
                    # 买家地址 [原字段 'address']
                    "buyer_address": "",
                    # 买家邮政编码 [原字段 'postal_code']
                    "buyer_postcode": "46006",
                    # 订购时间 (UTC时间) [原字段 'purchase_date_local_utc']
                    "purchase_time_utc": "2025-06-29 18:32:04",
                    # 订购时间 (站点时间) [原字段 'purchase_date_local']
                    "purchase_time_loc": "2025-06-29 20:32:04",
                    # 发货时间 (站点时间) [原字段 'shipment_date']
                    "shipment_time_loc": "2025-06-30 18:09:36",
                    # 最早发货时间 (UTC时间) [原字段 'earliest_ship_date_utc']
                    "earliest_ship_time_utc": "2025-06-30 21:59:59",
                    # 最早发货时间 (站点时间) [原字段 'earliest_ship_date']
                    "earliest_ship_time_loc": "2025-06-30 23:59:59",
                    # 最晚发货时间 (时区时间) [原字段 'latest_ship_date']
                    "latest_ship_time": "2025-06-30T21:59:59Z",
                    # 付款确认时间 (站点时间) [原字段 'posted_date']
                    "posted_time_loc": "2025-07-08 23:14:12",
                    # 亚马逊订单更新时间 (UTC时间) [原字段 'last_update_date_utc']
                    "update_time_utc": "2025-07-18 13:26:18",
                    # 亚马逊订单更新时间 (站点时间) [原字段 'last_update_date']
                    "update_time_loc": "2025-07-18 15:26:18",
                    # 订单中的商品 [原字段 'item_list']
                    "items": [
                        {
                            # 领星店铺ID (Seller.sid)
                            "sid": 1,
                            # 领星本地商品ID
                            "product_id": 2*****,
                            # 领星订单详情ID [原字段 'id']
                            "order_id": 10**********,
                            # 亚马逊订单商品编码 [订单下唯一键，但亚马逊返回值可能会发生变更]
                            "order_item_id": "5*************",
                            # 商品ASIN
                            "asin": "B0********",
                            # 亚马逊卖家SKU [原字段 'seller_sku']
                            "msku": "SKU********",
                            # 领星本地商品SKU [原字段 'sku']
                            "lsku": "LOCAL-SKU********",
                            # 领星本地商品名称
                            "product_name": "P*******",
                            # 商品 ASIN 链接
                            "asin_url": "https://www.amazon.es/dp/B0********",
                            # 商品图片链接 [原字段 'pic_url']
                            "image_url": "https://m.media-amazon.com/images/I/61******_.jpg",
                            # 商品标题
                            "title": "Product Title",
                            # 订单商品总数量 [原字段 'quantity_ordered']
                            "order_qty": 1,
                            # 订单已发货数量 [原字段 'quantity_shipped']
                            "shipped_qty": 1,
                            # 商品促销标识 [原字段 'promotion_ids']
                            "promotion_labels": [],
                            # 商品价格标识 (如: "Business Price") [原字段 'price_designation']
                            "price_label": "",
                            # 商品销售单价 [原字段 'unit_price_amount']
                            "item_price": 24.78,
                            # 商品销售金额 [原字段 'item_price_amount']
                            "sales_amt": 29.98,
                            # 商品销售金额税费 [原字段 'item_tax_amount']
                            "sales_tax_amt": 5.2,
                            # 商品销售实收金额 [原字段 'sales_price_amount']
                            "sales_received_amt": 29.98,
                            # 买家支付运费金额 [原字段 'shipping_price_amount']
                            "shipping_credits_amt": 0.0,
                            # 买家支付运费税费 [原字段 'shipping_tax_amount']
                            "shipping_credits_tax_amt": 0.0,
                            # 买家支付礼品包装费金额 [原字段 'gift_wrap_price_amount']
                            "giftwrap_credits_amt": 0.0,
                            # 买家支付礼品包装费税费 [原字段 'gift_wrap_tax_amount']
                            "giftwrap_credits_tax_amt": 0.0,
                            # 买家支付货到付款服务费金额 (Cash On Delivery) [原字段 'cod_fee_amount']
                            "cod_service_credits_amt": 0.0,
                            # 卖家商品促销折扣金额 [原字段 'promotion_discount_amount']
                            "promotion_discount_amt": 0.0,
                            # 卖家商品促销折扣税费 [原字段 'promotion_discount_tax_amount']
                            "promotion_discount_tax_amt": 0.0,
                            # 卖家商品运费折扣金额 [原字段 'shipping_discount_amount']
                            "shipping_discount_amt": 0.0,
                            # 卖家商品运费折扣金额 [原字段 'shipping_discount_amount']
                            "shipping_discount_tax_amt": 0.0,
                            # 亚马逊积分抵付款金额 (日本站) [原字段 'points_monetary_value_amount']
                            "points_discount_amt": 0.0,
                            # 卖家货到付款服务费折扣金额 (Cash On Delivery) [原字段 'cod_fee_discount_amount']
                            "cod_service_discount_amt": 0.0,
                            # 卖家总折扣金额 [原字段 'promotion_amount']
                            "total_discount_amt": 0.0,
                            # 卖家总代扣税费 [原字段 'tax_amount']
                            "withheld_tax_amt": -5.2,
                            # 卖家总代扣税费是否为预估值 (0: 否, 1: 是) [原字段 'item_tax_amount_estimated']
                            "withheld_tax_amt_estimated": 0,
                            # 亚马逊FBA配送费用 [原字段 'fba_shipment_amount']
                            "fulfillment_fee": -3.6,
                            # 亚马逊FBA配送费用是否为预估值 (0: 否, 1: 是) [原字段 'fba_shipment_amount_estimated']
                            "fulfillment_fee_estimated": 0,
                            # 亚马逊销售佣金 [原字段 'commission_amount']
                            "referral_fee": -4.5,
                            # 亚马逊销售佣金是否为预估值 (0: 否, 1: 是) [原字段 'commission_amount_estimated']
                            "referral_fee_estimated": 0,
                            # 亚马逊收取的其他费用 (如: Amazon Exlusives Program) [原字段 'other_amount']
                            "other_fee": 0.0,
                            # 用户自定义推广费用名称 (如: 推广费) [原字段 'fee_name']
                            "user_promotion_type": "推广费",
                            # 用户自定义推广费用货币代码 [原字段 'fee_currency']
                            "user_promotion_currency_code": "",
                            # 用户自定义推广费用货币符号 [原字段 'fee_icon']
                            "user_promotion_currency_icon": "",
                            # 用户自定义推广费用本金 (原币种) [原字段 'fee_cost']
                            "user_promotion_currency_fee": 0.0,
                            # 用户自定义推广费用本金 (店铺币种) [原字段 'fee_cost_amount']
                            "user_promotion_fee": 0.0,
                            # 商品采购头程费用金额 [原字段 'cg_transport_costs']
                            "cost_of_logistics_amt": 0.0,
                            # 商品采购成本金额 [原字段 'cg_price']
                            "cost_of_goods_amt": 12.3,
                            # 商品毛利润金额 [原字段 'profit']
                            "profit_amt": 4.29,
                            # 商品状况（卖家提供）[原字段 'condition_note']
                            "item_condition": "",
                            # 商品状况ID (卖家提供) [原字段 'condition_id']
                            "item_condition_id": "",
                            # 商品子状况ID (卖家提供) [原字段 'condition_subtype_id']
                            "item_condition_sub_id": "",
                            # 礼品包装级别（买家提供) [原字段 'gift_wrap_level']
                            "giftwrap_level": "",
                            # 礼品包装信息（买家提供）[原字段 'gift_message_text']
                            "giftwap_message": "",
                            # 计划交货开始时间 [原字段 'scheduled_delivery_start_date']
                            "scheduled_delivery_start_time": "",
                            # 计划交货结束时间 [原字段 'scheduled_delivery_end_date']
                            "scheduled_delivery_end_time": "",
                            # 商品自定义JSON数据
                            "customized_json": "",
                        },
                        ...
                    ],
                },
                ...
            ],
        }
        ```
        """
        url = route.ORDER_DETAILS
        # 解析并验证参数
        args = {"amazon_order_ids": amazon_order_ids}
        try:
            p = param.OrderDetails.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.OrderDetails.model_validate(data)

    async def EditOrderNote(
        self,
        sid: int,
        amazon_order_id: str,
        note: str | None,
    ) -> base_schema.ResponseResult:
        """更新订单备注

        ## Docs
        - 销售 - 平台订单: [SC订单-设置订单备注](https://apidoc.lingxing.com/#/docs/Sale/ScOrderSetRemark)

        :param sid `<'int'>`: 领星店铺ID, 参数来源: `Order.sid`
        :param amazon_order_id `<'str'>`: 亚马逊订单ID, 参数来源: `Order.amazon_order_id`
        :param note `<'str/None'>`: 订单备注内容, 清除备注时传入 `None` 或空字符串
        :returns `<'ResponseResult'>`: 返回更新结果
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
            # 响应结果
            "data": None,
        }
        ```
        """
        url = route.EDIT_ORDER_NOTE
        # 解析并验证参数
        args = {"sid": sid, "amazon_order_id": amazon_order_id, "note": note}
        try:
            p = param.EditOrderNote.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return base_schema.ResponseResult.model_validate(data)

    async def AfterSalesOrders(
        self,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        *,
        date_type: int | None = None,
        service_type: int | list[int] | None = None,
        sids: int | list[int] = None,
        amazon_order_ids: str | list[str] | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.AfterSalesOrders:
        """查询售后订单

        ## Docs:
        - 销售 - 平台订单: [查询售后订单列表](https://apidoc.lingxing.com/#/docs/Sale/afterSaleList)

        :param start_date `<'str/date/datetime'>`: 查询开始日期, 左闭右开
        :param end_date `<'str/date/datetime'>`: 查询结束日期, 左闭右开
        :param date_type `<'int'>`: 查询日期类型, 默认 `None` (使用: 1)

            - `1`: 售后时间 (AfterSalesOrder.service_time_loc)
            - `2`: 订购时间 (AfterSalesOrder.purchase_time_loc)
            - `3`: 更新时间 (AfterSalesOrder.modify_time_cnt)

        :param service_type `<'int/list[int]'>`: 售后类型或类型列表, 默认 `None` (查询所有类型)

            - `1`: 退款
            - `2`: 退货
            - `3`: 换货

        :param sids `<'int/list[int]'>`: 领星店铺ID或ID列表,
            默认 `None` (查询所有店铺), 参数来源: `Order.sid`
        :param amazon_order_ids `<'str/list[str]'>`: 亚马逊订单ID或最多50个ID列表,
            默认 `None` (查询所有订单), 参数来源: `Order.amazon_order_id`
        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 最大值 5000, 默认 `None` (使用: 1000)
        :returns `<'AfterSalesOrders'>`: 返回查询到的售后订单信息列表.
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
                    # 领星店铺ID (Seller.sid)
                    "sid": 1,
                    # 领星售后订单自增ID (非唯一键) [原字段 'id']
                    "after_sales_id": 100*********,
                    # 亚马逊订单ID (Order.amazon_order_id)
                    "amazon_order_id": "111-*******-*******",
                    # 关联ID
                    "correlation_id": 1*********,
                    # 商品ASIN (Listing.asin)
                    "asin": "B0********",
                    # 亚马逊卖家SKU (Listing.msku)
                    "msku": "SKU********",
                    # 店铺名称+国家 (如: "领星店铺 美国")
                    "seller_country": "店铺名 美国",
                    # 是否为多渠道配送订单 (0: 默认值, 1: 普通订单, 2: 多渠道订单)
                    "is_mcf_order": 0,
                    # 送货方式 ("FBA", "FBM")
                    "delivery_type": "FBA",
                    # 售后类型 (如: ["退款","退货","换货"]) [原字段 'after_type_tag']
                    "service_type": ["退款"],
                    # 订单销售总金额 [原字段 'order_total_amount_number']
                    "order_sales_amt": 31.78,
                    # 订单销售总金额的货币符号 (如: "$" 或 "") [原字段 'order_total_amount_currency_code']
                    "order_sales_currency_icon": "$",
                    # 订单退款总金额 [原字段 'total_refund_amount_number']
                    "order_refund_amt": -26.38,
                    # 订单退款总金额的货币符号 (如: "$" 或 "") [原字段 'total_refund_amount_currency_code']
                    "order_refund_currency_icon": "$",
                    # 订单退款成本 [原字段 'total_refund_cost_number']
                    "order_refund_cost_amt": 3.6,
                    # 订单退款成本的货币符号 (如: "$" 或 "") [原字段 'total_refund_cost_currency_code']
                    "roder_refund_cost_currency_icon": "$",
                    # 订购时间 (站点时间) [原字段 'purchase_time']
                    "purchase_time_loc": "2025-07-10 12:34:17",
                    # 如同一个订单存在多个售后订单，需以 items>>service_time_loc 为准
                    # 售后时间 (站点时间) [原字段 'deal_time']
                    "service_time_loc": "2025-07-18 00:00:00",
                    # 售后间隔天数 [原字段 'interval_days']
                    "service_interval_days": 8,
                    # 领星订单更新时间 (北京时间) [原字段 'gmt_modified']
                    # 如同一个订单存在多个售后订单，需以 items>>modify_time_cnt 为准
                    "modify_time_cnt": "2025-07-20 22:36:36",
                    # 售后订单中的商品列表 [原字段 'item_list']
                    "items": [
                        {
                            # 售后订单唯一标, 由多个字段拼接而成 [原字段 'item_identifier']
                            "uid": "12083+********",
                            # 售后订单唯一标, 由uid基于md5压缩而成 [原字段 'md5_v2']
                            "uid_md5": "2c0*****************************",
                            # 商品ASIN (Listing.asin)
                            "asin": "B0********",
                            # 亚马逊卖家SKU (Listing.msku)
                            "msku": "SKU********",
                            # 领星本地商品SKU (Listing.lsku) [原字段 'local_sku']
                            "lsku": "LOCAL********",
                            # 领星本地商品名称 (Listing.product_name) [原字段 'local_name']
                            "product_name": "待补充",
                            # 商品 ASIN 链接
                            "asin_url": "",
                            # 商品略缩图链接 [原字段 'small_image_url']
                            "thumbnail_url": "https://image.distributetop.com/******.jpg",
                            # 商品标题 [原字段 'item_name']
                            "title": "Product Title",
                            # 售后类型 (如: "退款", "退货", "换货") [原字段 'after_type']
                            "service_type": "退款",
                            # 售后数量 [原字段 'after_quantity']
                            "service_qty": 1,
                            # 售后原因 [原字段 'after_reason']
                            "service_reason": "",
                            # 订单退款金额 (含货币符号) [原字段 'refund_amount']
                            "order_refund_amt": "$-26.380",
                            # 订单退款金额详情 [原字段 'refund_amount_details']
                            "order_refund_amt_details": [
                                {"type": "MarketplaceFacilitatorTax-Principal", "amt": "$1.800"},
                                {"type": "Commission", "amt": "$4.500"},
                                {"type": "Principal", "amt": "$-29.980"},
                                {"type": "RefundCommission", "amt": "$-0.900"},
                                {"type": "Tax", "amt": "$-1.800"},
                            ],
                            # 订单退款成本 (含货币符号) [原字段 'refund_cost']
                            "order_refund_cost": "$3.600",
                            # 订单退款成本详情 [原字段 'refund_cost_details']
                            "order_refund_cost_details": [
                                {"type": "Commission", "amt": "$4.500"},
                                {"type": "RefundCommission", "amt": "$-0.900"},
                            ],
                            # 退货状态, 如 "Approved" [原字段 'return_status']
                            "order_return_status": "",
                            # 换货订单号
                            "exchange_order_number": "",
                            # LPN编码号
                            "lpn_number": "",
                            # RMA订单号 [原字段 'rma_order_number']
                            "rma_number": "",
                            # 运单号
                            "waybill_number": "",
                            # 承运商
                            "carriers": "",
                            # 买家备注
                            "buyer_note": "",
                            # 库存属性
                            "inventory_attributes": "",
                            # 售后时间 (站点时间) [原字段 'service_time']
                            "service_time_loc": "2025-07-20 07:13:36",
                            # 售后间隔天数 [原字段 'after_interval']
                            "service_interval_days": "10天",
                            # 领星订单更新时间 (北京时间) [原字段 'gmt_modified']
                            "modify_time_cnt": "2025-07-20 22:36:36",
                        },
                        ...
                    ],
                },
                ...
            ],
        }
        ```
        """
        url = route.AFTER_SALES_ORDERS
        # 解析并验证参数
        args = {
            "start_date": start_date,
            "end_date": end_date,
            "date_type": date_type,
            "service_type": service_type,
            "sids": sids,
            "amazon_order_ids": amazon_order_ids,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AfterSalesOrder.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.AfterSalesOrders.model_validate(data)

    async def McfOrders(
        self,
        *,
        sids: int | list[int] | None = None,
        start_data: str | datetime.date | datetime.datetime | None = None,
        end_data: str | datetime.date | datetime.datetime | None = None,
        date_type: int | None = None,
        offset: int = 0,
        length: int = 10,
    ) -> schema.McfOrders:
        """查询亚马逊多渠道订单

        ## Docs:
        - 销售 - 平台订单: [查询亚马逊多渠道订单列表-v2](https://apidoc.lingxing.com/#/docs/Sale/OrderMCFOrders)

        :param sids `<'int/list[int]'>`: 领星店铺ID或ID列表,
            默认 `None` (查询所有店铺), 参数来源: `Order.sid`
        :param start_data `<'str/date/datetime'>`: 查询开始日期, 左闭右开,
            默认 `None` (查询最近6个月)
        :param end_data `<'str/date/datetime'>`: 查询结束日期, 左闭右开,
            默认 `None` (查询最近6个月)
        :param date_type `<'int'>`: 查询日期类型, 默认 `None` (使用: 1)

            - `1`: 订购时间 (McfOrder.purchase_time_loc)
            - `2`: 订单修改时间 (McfOrder.update_time_utc)

        :param offset `<'int'>`: 分页偏移量, 默认 `0`
        :param length `<'int'>`: 分页长度, 最大值 1000, 默认 `10`
        :returns `<'McfOrders'>`: 返回查询到的多渠道订单信息列表
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
                    # 领星店铺ID (Seller.sid)
                    "sid": 1,
                    # 领星店铺名称 (Seller.name) [原字段 'store_name']
                    "seller_name": "Seller****",
                    # 订单国家 (中文)
                    "country": "德国",
                    # 多渠道亚马逊订单ID
                    "amazon_order_id": "S02-*******-*******",
                    # 多渠道订单配送ID [原字段 'seller_fulfillment_order_id']
                    "fulfillment_order_id": "RE028-*******-*******",
                    # 订单状态
                    "order_status": "Complete",
                    # 订单备注 [原字段 'remark']
                    "order_note": "",
                    # 买家名称
                    "buyer_name": "Al****",
                    # 购买时间 (站点时间) [原字段 'purchase_date_local']
                    "purchase_time_loc": "2025-06-24 06:04:33",
                    # 发货时间 (UTC时间) [原字段 'ship_date_utc']
                    "shipment_time_utc": "2025-06-25T06:43:04Z",
                    # 发货时间 (站点时间) [原字段 'ship_date']
                    "shipment_time_loc": "2025-06-25 08:43:04",
                    # 订单更新时间 (UTC时间) [原字段 'last_update_time']
                    "update_time_utc": "2025-06-25 15:22:32",
                    # 商品列表 [原字段 'listing_info']
                    "items": [
                        {
                            # 商品ASIN (Listing.asin)
                            "asin": "B0********",
                            # 亚马逊卖家SKU (Listing.msku)
                            "msku": "SKU********",
                            # 领星本地SKU (Listing.lsku) [原字段 'local_sku']
                            "lsku": "LOCAL********",
                            # 亚马逊FBA自生成的商品编号 (Listing.fnsku)
                            "fnsku": "X00*******",
                            # 领星本地商品名称 (Listing.product_name) [原字段 'local_name']
                            "product_name": "Pr*******",
                            # 商品标题 [原字段 'item_name']
                            "title": "Product Title",
                            # 商品略缩图链接 [原字段 'small_image_url']
                            "thumbnail_url": "https://image.distributetop.com/****.jpg",
                            # 订单商品总数量 [原字段 'quantity']
                            "order_qty": 1,
                        },
                        ...
                    ],
                },
                ...
            ]
        }
        ```
        """
        url = route.MCF_ORDERS
        # 解析并验证参数
        args = {
            "sids": sids,
            "start_data": start_data,
            "end_data": end_data,
            "date_type": date_type,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.McfOrders.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        # return data
        return schema.McfOrders.model_validate(data)

    async def McfOrderDetails(
        self,
        *fulfillment_order_id: dict,
    ) -> schema.McfOrderDetails:
        """查询亚马逊多渠道订单的商品信息详情

        ## Docs:
        - 销售 - 平台订单: [查询亚马逊多渠道订单详情-商品信息](https://apidoc.lingxing.com/#/docs/Sale/ProductInformation)

        :param *fulfillment_order_id `<'dict'>`: 支持最多查询200个订单详情

            - 每个字典必须包含 `sid` 和 `fulfillment_order_id` 字段, 如:
              `{"sid": 1, "fulfillment_order_id": "RE028-*******-*******"}`
            - 必填字段 `sid` 领星店铺ID, 必须是 int 类型, 参数来源: `McfOrder.sid`
            - 必填字段 `fulfillment_order_id` 多渠道订单配送ID, 必须是 str 类型,
              参数来源: `McfOrder.fulfillment_order_id`

        :returns `<'McfOrderDetails'>`: 返回查询到的多渠道订单详情信息列表
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
                    # 领星店铺ID (Seller.sid)
                    "sid": 1,
                    # 领星店铺名称 (Seller.name) [原字段 'store_name']
                    "seller_name": "Seller****",
                    # 多渠道亚马逊订单ID
                    "amazon_order_id": "S01-*******-*******",
                    # 多渠道订单配送ID [原字段 'seller_fulfillment_order_id']
                    "fulfillment_order_id": "RE-701-*******-*******",
                    # 销售渠道
                    "sales_channel": "",
                    # 订单配送服务级别 [原字段 'speed_category']
                    "shipment_service": "标准配送",
                    # 订单状态
                    "order_status": "Complete",
                    # 订单备注 [原字段 'remark']
                    "order_note": "",
                    # 订单装箱备注 [原字段 'displayable_order_comment']
                    "order_comment": "Thank you for your order",
                    # 买家名称
                    "buyer_name": "De****",
                    # 买家电子邮箱
                    "buyer_email": "",
                    # 买家电话号码 [原字段 'phone']
                    "buyer_phone": "暂停显示",
                    # 卖家地址 [原字段 'address_line1']
                    "buyer_address": "125*******",
                    # 买家邮政编码 [原字段 'postal_code']
                    "buyer_postcode": "T9A 3R9",
                    # 购买时间 (站点时间) [原字段 'purchase_date_local']
                    "purchase_time_loc": "2025-07-17 22:45:30",
                    # 发货时间 (UTC时间) [原字段 'ship_date_utc']
                    "shipment_time_utc": "2025-07-19T22:28:26Z",
                    # 发货时间 (北京时间) [原字段 'ship_date']
                    "shipment_time_cnt": "2025-07-20 06:28:26",
                    # 订单详情列表
                    "items": [
                        {
                            # 商品ASIN (Listing.asin)
                            "asin": "B0********",
                            # 亚马逊卖家SKU (Listing.msku)
                            "msku": "SKU********",
                            # 领星本地SKU (Listing.lsku) [原字段 'local_sku']
                            "lsku": "LOCAL********",
                            # 亚马逊FBA自生成的商品编号 (Listing.fnsku)
                            "fnsku": "X00*******",
                            # 领星本地商品名称 (Listing.product_name) [原字段 'local_name']
                            "product_name": "Pr*******",
                            # 商品标题 [原字段 'item_name']
                            "title": "Product Title",
                            # 商品略缩图链接 [原字段 'small_image_url']
                            "thumbnail_url": "https://image.distributetop.com/****.jpg",
                            # 订单商品总数量 [原字段 'quantity']
                            "order_qty": 1,
                            # 订单商品已发货数量 [原字段 'shipped_quantity']
                            "shipped_qty": 1,
                            # 订单商品已取消数量 [原字段 'cancelled_quantity']
                            "cancelled_qty": 0,
                            # 订单商品不可售数量 [原字段 'unfulfillable_quantity']
                            "unfulfillable_qty": 0,
                        },
                        ...
                    ],
                },
                ...
            ],
        }
        ```
        """
        url = route.MCF_ORDER_DETAILS
        # 解析并验证参数
        args = {"fulfillment_order_ids": fulfillment_order_id}
        try:
            p = param.McfFulfillmentOrderIds.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.McfOrderDetails.model_validate(data)

    async def McfAfterSalesOrders(
        self,
        *fulfillment_order_id: dict,
    ) -> schema.McfAfterSalesOrders:
        """查询亚马逊多渠道订单的退货换货信息详情

        ## Docs:
        - 销售 - 平台订单: [查询亚马逊多渠道订单详情-退货换货信息](https://apidoc.lingxing.com/#/docs/Sale/ReturnInfomation)

        :param *fulfillment_order_id `<'dict'>`: 支持最多查询200个订单详情

            - 每个字典必须包含 `sid` 和 `fulfillment_order_id` 字段, 如:
              `{"sid": 1, "fulfillment_order_id": "RE028-*******-*******"}`
            - 必填字段 `sid` 领星店铺ID, 必须是 int 类型, 参数来源: `McfOrder.sid`
            - 必填字段 `fulfillment_order_id` 多渠道订单配送ID, 必须是 str 类型,
              参数来源: `McfOrder.fulfillment_order_id`

        :returns `<'McfAfterSalesOrders'>`: 返回查询到的多渠道订单售后信息详情列表
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
                    # 领星店铺ID (Seller.sid)
                    "sid": 1,
                    # 领星店铺名称 (Seller.name) [原字段 'store_name']
                    "seller_name": "Seller****",
                    # 多渠道亚马逊订单ID
                    "amazon_order_id": "S01-*******-*******",
                    # 多渠道订单配送ID [原字段 'seller_fulfillment_order_id']
                    "fulfillment_order_id": "RE402-*******-*******",
                    # 销售渠道
                    "sales_channel": "",
                    # 订单配送服务级别 [原字段 'speed_category']
                    "shipment_service": "标准配送",
                    # 订单状态
                    "order_status": "CANCELLED",
                    # 订单备注 [原字段 'remark']
                    "order_note": "备注",
                    # 订单装箱备注 [原字段 'displayable_order_comment']
                    "order_comment": "Thank you for your order",
                    # 买家名称
                    "buyer_name": "B*****",
                    # 买家电子邮箱
                    "buyer_email": "",
                    # 买家电话号码 [原字段 'phone']
                    "buyer_phone": "暂停显示",
                    # 卖家地址 [原字段 'address_line1']
                    "buyer_address": "",
                    # 买家邮政编码 [原字段 'postal_code']
                    "buyer_postcode": "100000",
                    # 购买时间 (站点时间) [原字段 'purchase_date_local']
                    "purchase_time_loc": "2025-06-23 11:16:19",
                    # 发货时间 (UTC时间) [原字段 'ship_date_utc']
                    "shipment_time_utc": "2025-06-23T18:00:17Z",
                    # 发货时间 (北京时间) [原字段 'ship_date']
                    "shipment_time_cnt": "2025-06-24 02:00:17",
                    # 售后服务详情 [原字段 'order_return_replace_tab']
                    "after_sales_service": {
                        "return_items": [
                            {
                                # 领星店铺ID (Seller.sid)
                                "sid": 1,
                                # 商品ASIN (Listing.asin)
                                "asin": "B0*******",
                                # 亚马逊卖家SKU (Listing.msku)
                                "msku": "SKU********",
                                # 领星本地SKU (Listing.lsku) [原字段 'local_sku']
                                "lsku": "LOCAL********",
                                # 领星本地商品名称 (Listing.product_name) [原字段 'name']
                                "product_name": "Pr*******",
                                # 多渠道订单配送ID [原字段 'order_id']
                                "fulfillment_order_id": "RE402-*******-*******",
                                # 退货数量 [原字段 'return_quantity']
                                "return_qty": 1,
                                # 退货状态
                                "return_status": "Unit returned to inventory",
                                # 退货原因
                                "return_reason": "NOT_AS_DESCRIBED",
                                # 退货日期
                                "return_date": "2023-03-01",
                                # LNP编码号 [原字段 'lpn']
                                "lpn_number": "LPN***********",
                                # 买家备注 [原字段 'customer_comments']
                                "buyer_note": "thank you",
                            },
                            ...
                        ],
                        "replacement_items": [
                            {
                                # 亚马逊卖家SKU (Listing.msku)
                                "msku": "SKU********",
                                # 领星本地商品名称 (Listing.product_name) [原字段 'name']
                                "product_name": "Pr*******",
                                # 商品ASIN链接
                                "asin_url": "https://www.amazon.com/dp/B0********",
                                # 换货原因
                                "replacement_reason": "Policy exception/customer error",
                                # 换货时间
                                "replacement_date": "2022-02-10",
                            },
                            ...
                        ],
                    },
                },
                ...
            ],
        }
        ```
        """
        url = route.MCF_AFTER_SALES_ORDERS
        # 解析并验证参数
        args = {"fulfillment_order_ids": fulfillment_order_id}
        try:
            p = param.McfFulfillmentOrderIds.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.McfAfterSalesOrders.model_validate(data)

    async def McfOrderLogistics(
        self,
        *fulfillment_order_id: dict,
    ) -> schema.McfOrderLogisticsData:
        """查询亚马逊多渠道订单的物流信息详情

        ## Docs:
        - 销售 - 平台订单: [查询亚马逊多渠道订单详情-物流信息](https://apidoc.lingxing.com/#/docs/Sale/LogisticsInformation)

        :param *fulfillment_order_id `<'dict'>`: 支持最多查询200个订单详情

            - 每个字典必须包含 `sid` 和 `fulfillment_order_id` 字段, 如:
              `{"sid": 1, "fulfillment_order_id": "RE028-*******-*******"}`
            - 必填字段 `sid` 领星店铺ID, 必须是 int 类型, 参数来源: `McfOrder.sid`
            - 必填字段 `fulfillment_order_id` 多渠道订单配送ID, 必须是 str 类型,
              参数来源: `McfOrder.fulfillment_order_id`

        :returns `<'McfOrderLogisticsData'>`: 返回查询到的多渠道订单物流信息详情列表
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
                    # 领星店铺ID (Seller.sid)
                    "sid": 1,
                    # 领星店铺名称 (Seller.name) [原字段 'store_name']
                    "seller_name": "Store*****",
                    # 多渠道亚马逊订单ID
                    "amazon_order_id": "S02-*******-*******",
                    # 多渠道订单配送ID [原字段 'seller_fulfillment_order_id']
                    "fulfillment_order_id": "RE402-*******-*******",
                    # 销售渠道
                    "sales_channel": "",
                    # 订单配送服务级别 [原字段 'speed_category']
                    "shipment_service": "标准配送",
                    # 订单状态
                    "order_status": "Complete",
                    # 订单备注 [原字段 'remark']
                    "order_note": "",
                    # 订单装箱备注 [原字段 'displayable_order_comment']
                    "order_comment": "Thank you for your order.",
                    # 买家名称
                    "buyer_name": "B*****",
                    # 买家电子邮箱
                    "buyer_email": "",
                    # 买家电话号码 [原字段 'phone']
                    "buyer_phone": "暂停显示",
                    # 卖家地址 [原字段 'address_line1']
                    "buyer_address": "P*****",
                    # 买家邮政编码 [原字段 'postal_code']
                    "buyer_postcode": "00177",
                    # 购买时间 (站点时间) [原字段 'purchase_date_local']
                    "purchase_time_loc": "2025-06-23 11:16:19",
                    # 发货时间 (UTC时间) [原字段 'ship_date_utc']
                    "shipment_time_utc": "2025-06-23T18:00:17Z",
                    # 发货时间 (北京时间) [原字段 'ship_date']
                    "shipment_time_cnt": "2025-06-24 02:00:17",
                    # 物流列表 [原字段 'shipment_info']
                    "shipments": [
                        {
                            # 亚马逊货件编号
                            "amazon_shipment_id": "U********",
                            # 货件状态 [原字段: 'fulfillment_shipment_status']
                            "shipment_status": "SHIPPED",
                            # 预计到货时间 (站点时间) [原字段 'estimated_arrival_datetime']
                            "estimated_arrival_time": "2025-06-24 23:59:59",
                            # 包裹详情信息
                            "packages": [
                                {
                                    # 承运人代码
                                    "carrier_code": "Amazon",
                                    # 包裹追踪码
                                    "tracking_number": "IT**********",
                                    # 包裹编号
                                    "package_number": "288884492",
                                    # 包裹运输状态 [原字段 'current_status']
                                    "package_status": "",
                                    # 包裹发货时间 (UTC时间) [原字段 'ship_date']
                                    "shipment_date_utc": "2025-06-23T18:00:17Z",
                                    # 包裹预计到货时间 (站点时间) [原字段 'estimated_arrival_datetime']
                                    "estimated_arrival_time": "2025-06-24 20:00:00",
                                    # 包裹追踪事件列表
                                    "tracking_events": [
                                        {
                                            # 追踪事件
                                            "event": "配送成功。",
                                            # 追踪事件编码 [原字段 'eventCode']
                                            "event_code": "EVENT_301",
                                            # 追踪事件描述 [原字段 'eventDescription']
                                            "event_description": "Package delivered. ",
                                            # 追踪事件时间 (站点时间) [原字段 'eventDate']
                                            "event_time_loc": "2025-06-24 13:35:46",
                                            # 追踪事件地址 [原字段 'eventAddress']
                                            "event_address": {
                                                # 追踪事件地址国家
                                                "country": "IT",
                                                # 追踪事件地址省/州
                                                "state": "",
                                                # 追踪事件地址城市
                                                "city": "Roma",
                                            },
                                        },
                                        ...
                                    ],
                                    # 包裹内的商品列表 [原字段 'shipItems']
                                    "package_items": [
                                        {
                                            # 领星店铺ID (Seller.sid)
                                            "sid": 1,
                                            # 亚马逊SKU (Listing.msku)
                                            "msku": "SKU********",
                                            # 商品标题
                                            "title": "Product Title",
                                            # 商品数量 [原字段 'quantity']
                                            "item_qty": 1,
                                            # 包裹编码
                                            "package_number": "2********",
                                        },
                                        ...
                                    ],
                                },
                                ...
                            ],
                        },
                        ...
                    ],
                },
                ...
            ],
        }
        ```
        """
        url = route.MCF_ORDER_LOGISTICS
        # 解析并验证参数
        args = {"fulfillment_order_ids": fulfillment_order_id}
        try:
            p = param.McfFulfillmentOrderIds.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.McfOrderLogisticsData.model_validate(data)

    async def McfOrderTransaction(
        self,
        sid: int,
        amazon_order_id: str,
    ) -> schema.McfOrderTransactionData:
        """查询多渠道订单的交易明细

        ## Docs:
        - 销售 - 平台订单: [多渠道订单-交易明细](https://apidoc.lingxing.com/#/docs/Sale/MutilChannelTransactionDetail)

        :param sid `<'int'>`: 领星店铺ID, 必须是 int 类型, 参数来源: `McfOrder.sid`
        :param amazon_order_id `<'str'>`: 多渠道亚马逊订单ID,
            必须是 str 类型, 参数来源: `McfOrder.amazon_order_id`
        :returns `<'McfOrderTransactionData'>`: 返回查询到的多渠道订单交易明细信息
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
            "data": {
                # 多渠道订单总交易金额 (包含货币符号) [原字段 'totalCurrencyAmounts']
                "transaction_amt": "-CA$8.97",
                # 多渠道订单交易事件列表 [原字段 'list']
                "transaction_events": [
                    {
                        # 领星店铺ID (Seller.sid)
                        "sid": 9846,
                        # 亚马逊卖家SKU (Listing.msku) [原字段 'sellerSku']
                        "msku": "SKU*********",
                        # 领星本地SKU (Listing.lsku) [原字段 'sku']
                        "lsku": "LOCAL*********",
                        # 领星本地商品名称 (Listing.product_name) [原字段 'productName']
                        "product_name": "P********",
                        # 结算编号 [原字段 'fid']
                        "transaction_id": "LWC*********
                        # 交易事件类型 [原字段 'eventType']
                        "event_type": "Shipment",
                        # 交易事件商品数量 [原字段 'quantity']
                        "event_qty": 0,
                        # 交易事件货币代码 [原字段 'currencyCode']
                        "event_currency_code": "CAD",
                        # 交易事件货币金额 (含货币符号) [原字段 'totalCurrencyAmount']
                        "event_amt": "CA$-3.64",
                        # 交易事件详情 [原字段 'costDetails']
                        "event_details": [
                            {
                                # 事件类型
                                "type": "FBAPerUnitFulfillmentFee",
                                # 事件金额 (含货币符号) [原字段 'currencyAmount']
                                "amt": "-CA$3.64"
                            },
                            ...
                        ],
                        # 交易付款确认时间 (时区时间) [原字段 'postedDateLocale']
                        "posted_time": "2025-07-17T23:03:11-07:00",
                        # 交易转账时间 (时区时间) [原字段 'fundTransferDateLocale']
                        "fund_transfer_time": "2025-07-18T10:44:28-07:00",
                    },
                    ...
                ],
            },
        }
        ```
        """
        url = route.MCF_ORDER_TRANSACTION
        # 解析并验证参数
        args = {"sid": sid, "amazon_order_id": amazon_order_id}
        try:
            p = param.McfOrderTransaction.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.McfOrderTransactionData.model_validate(data)

    # 自发货管理 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    async def FbmOrders(
        self,
        sids: int | list[int],
        *,
        purchase_start_time: str | datetime.date | datetime.datetime | None = None,
        purchase_end_time: str | datetime.date | datetime.datetime | None = None,
        order_status: int | list[int] | None = None,
        page: int | None = None,
        length: int | None = None,
    ) -> schema.FbmOrders:
        """查询亚马逊自发货订单

        ## Docs:
        - 销售 - 自发货管理: [查询亚马逊自发货订单列表](https://apidoc.lingxing.com/#/docs/Sale/FBMOrderList)

        :param sids `<'int/list[int]'>`: 领星店铺ID或ID列表, 参数来源: `Order.sid`
        :param purchase_start_time `<'str/date/datetime'>`: 订购开始时间, 默认 `None`,
            参数来源: `FbmOrder.purchase_time`
        :param purchase_end_time `<'str/date/datetime'>`: 订购结束时间, 默认 `None`,
            参数来源: `FbmOrder.purchase_time`
        :param order_status `<'int/list[int]'>`: 订单状态或状态列表, 默认 `None` (查询所有状态),

            - `1`: 同步中
            - `2`: 已发货
            - `3`: 未付款
            - `4`: 待审核
            - `5`: 待发货
            - `6`: 不发货

        :param page `<'int'>`: 分页页码, 默认 `None` (使用: 1)
        :param length `<'int'>`: 分页长度, 默认 `None` (使用: 100)
        :returns `<'FbmOrders'>`: 返回查询到的自发货订单信息列表
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
                    # 自发货订单号
                    "order_number": "10****************",
                    # 订单状态 [原字段 'status']
                    # (1: 同步中, 2: 已发货, 3: 未付款, 4: 待审核, 5: 待发货, 6: 不发货)
                    "order_status": "待审核",
                    # 订单类型 [原字段 'order_from']
                    "order_type": "线上订单",
                    # 平台订单ID列表
                    "platform_order_ids": ["028-*******-*******"],
                    # 订单目的地国家代码
                    "country_code": "DE",
                    # 物流类型ID
                    "logistics_type_id": "1",
                    # 物流类型名称 [原字段 'logistics_type_name']
                    "logistics_type": "1",
                    # 物流商ID
                    "logistics_provider_id": "1",
                    # 物流商名称 [原字段 'logistics_provider_name']
                    "logistics_provider": "4PX",
                    # 发货仓库ID [原字段 'wid']
                    "warehouse_id": 1,
                    # 发货仓库名称 [原字段 'warehouse_name']
                    "warehouse": "OW-测试仓库",
                    # 买家备注 [原字段 'customer_comment']
                    "buyer_note": "thank you",
                    # 订购时间
                    "purchase_time": "2024-12-29 18:20:36",
                },
                ...
            ],
        }
        ```
        """
        url = route.FBM_ORDERS
        # 解析并验证参数
        args = {
            "sids": sids,
            "purchase_start_time": purchase_start_time,
            "purchase_end_time": purchase_end_time,
            "order_status": order_status,
            "page": page,
            "length": length,
        }
        try:
            p = param.FbmOrders.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.FbmOrders.model_validate(data)

    async def FbmOrderDetail(self, order_number: int) -> schema.FbmOrderDetailData:
        """查询亚马逊自发货订单详情

        ## Docs:
        - 销售 - 自发货管理: [查询亚马逊自发货订单详情](https://apidoc.lingxing.com/#/docs/Sale/FBMOrderDetail)

        :param order_number `<'int'>`: 自发货订单号, 必须是 int 类型, 参数来源: `FbmOrder.order_number`
        :returns `<'FbmOrderDetailData'>`: 返回查询到的自发货订单
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
            "data": {
                # 领星店铺名称 (Seller.name) [原字段: 'shop_name']
                "seller_name": "Seller****",
                # 自发货订单号
                "order_number": "103***************",
                # 订单状态
                "order_status": "不发货",
                # 订单类型 [原字段 'order_from_name']
                "order_type": "线上订单",
                # 订单平台 [原字段 'platform']
                "order_platform": "AMAZON",
                # 物流类型ID
                "logistics_type_id": "1",
                # 物流类型名称 [原字段 'logistics_type_name']
                "logistics_type": "HH",
                # 物流商ID
                "logistics_provider_id": "1",
                # 物流商名称 [原字段 'logistics_provider_name']
                "logistics_provider": "4PX",
                # 发货仓库ID [原字段 'wid']
                "warehouse_id": 1,
                # 发货仓库名称 [原字段 'warehouse_name']
                "warehouse": "OW-测试仓库",
                # 订单配送服务级别 [原字段 'buyer_choose_express']
                "shipment_service": "Standard",
                # 买家留言
                "buyer_message": "",
                # 买家备注 [原字段 'customer_comment']
                "buyer_note": "",
                # 订购时间
                "purchase_time": "2024-07-07 05:14:22",
                # 物流跟踪码
                "tracking_number": "42**********",
                # 包裹预估重量 [原字段 'logistics_pre_weight']
                "package_est_weight": 100.0,
                # 包裹预估重量单位 [原字段 'logistics_pre_weight_unit']
                "package_est_weight_unit": "g",
                # 包裹预估长度 [原字段 'package_length']
                "package_est_length": 10.0,
                # 包裹预估宽度 [原字段 'package_width']
                "package_est_width": 10.0,
                # 包裹预估高度 [原字段 'package_height']
                "package_est_height": 10.0,
                # 包裹预估尺寸单位 [原字段 'package_unit']
                "package_est_dimension_unit": "cm",
                # 预估物流费用 [原字段 'logistics_pre_price']
                "logistics_est_amt": 1.2,
                # 包裹实际重量 [原字段: 'pkg_real_weight']
                "package_weight": 101.0,
                # 包裹实际重量单位 [原字段: 'pkg_real_weight_unit']
                "package_weight_unit": "g",
                # 包裹实际长度 [原字段: 'pkg_length']
                "package_length": 10.0,
                # 包裹实际宽度 [原字段: 'pkg_width']
                "package_width": 10.0,
                # 包裹实际高度 [原字段: 'pkg_height']
                "package_height": 10.0,
                # 包裹实际尺寸单位 [原字段: 'pkg_size_unit']
                "package_dimension_unit": "cm",
                # 实际物流费用货币代码 [原字段: 'logistics_freight_currency_code']
                "logistics_currency_code": "GBP",
                # 实际物流费用 [原字段: 'logistics_freight']
                "logistics_amt": 1.4,
                # 总客付运费 [原字段 'total_shipping_price']
                "shipping_amt": 1.4,
                # 订单销售金额 [原字段 'order_price_amount']
                "sales_amt": 29.99,
                # 订单毛利润金额 [原字段 'gross_profit_amount']
                "profit_amt": 24.99,
                # 订单商品列表 [原字段: 'order_item']
                "items": [
                    {
                        # 平台订单ID
                        "platform_order_id": "026-*******-*******",
                        # 订单详情的商品单号 [原字段 'order_item_no']
                        "order_item_id": "398***********",
                        # 亚马逊卖家SKU (Listing.msku) [原字段 'MSKU']
                        "msku": "SKU********",
                        # 领星本地SKU (Listing.lsku) [原字段 'sku']
                        "lsku": "LOCAL********",
                        # 领星本地商品名称 (Listing.product_name)
                        "product_name": "P*******",
                        # 商品图片链接 [原字段 'pic_url']
                        "image_url": "https://****.jpg",
                        # 商品单价货币代码
                        "currency_code": "GBP",
                        # 商品单价 [原字段 'item_unit_price']
                        "item_price": 29.99,
                        # 订单商品数量 [原字段 'quality']
                        "order_qty": 1,
                        # 订单备注 [原字段 'customization']
                        "order_note": "",
                        # 附件信息列表 [原字段 'newAttachments']
                        "attachments": [
                            {
                                # 文件ID
                                "file_id": 103***************,
                                # 文件名称
                                "file_name": "lADPBG1Q7eeWX****.jpg",
                                # 文件类型 (0: 未知, 1: 图片, 2: 压缩包)
                                "file_type": 1,
                                # 文件链接
                                "file_url": "",
                            },
                            ...
                        ],
                    },
                    ...
                ],
            },
        }
        ```
        """
        url = route.FBM_ORDER_DETAIL
        # 解析并验证参数
        args = {"order_number": order_number}
        try:
            p = param.FbmOrderDetail.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.FbmOrderDetailData.model_validate(data)

    # 促销管理 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    async def PromotionCoupons(
        self,
        *,
        sids: int | list[int] | None = None,
        start_data: str | datetime.date | datetime.datetime | None = None,
        end_data: str | datetime.date | datetime.datetime | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.PromotionCoupons:
        """查询促销列表 - 优惠券

        ## Docs:
        - 销售 - 促销管理: [查询促销活动列表-优惠券](https://apidoc.lingxing.com/#/docs/Sale/promotionalActivitiesCouponList)

        :param sids `<'int/list[int]'>`: 领星店铺ID或ID列表,
            默认 `None` (查询所有店铺), 参数来源: `Seller.sid`
        :param start_data `<'str/date/datetime'>`:促销开始日期, 默认 `None`
        :param end_data `<'str/date/datetime'>`: 促销结束日期, 默认 `None`
        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 最大值200, 默认 `None` (使用: 20)
        :returns `<'PromotionCoupons'>`: 返回查询到的促销列表
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
                    # 领星店铺ID (Seller.sid)
                    "sid": 1,
                    # 优惠券名称
                    "coupon_name": "5% di sconto su 304 1B",
                    # 优惠券状态 [原字段 'origin_status']
                    "status": "RUNNING",
                    # 优惠券备注 [原字段 'remark']
                    "note": "",
                    # 优惠券折扣百分比 [原字段 'discount']
                    "discount_pct": "5.00%",
                    # 货币符号
                    "currency_icon": "€",
                    # 优惠券预算金额 [原字段 'budget']
                    "budget_amt": "€1000",
                    # 优惠券费用 [原字段 'cost']
                    "coupon_fee": 107.24,
                    # 优惠券领取数量 [原字段 'draw_quantity']
                    "claimed_qty": 177,
                    # 优惠券兑换数量 [原字段 'exchange_quantity']
                    "redeemed_qty": 111,
                    # 优惠券兑换率 [原字段 'exchange_rate']
                    # (redeemed_qty / claimed_qty)
                    "redemption_rate": 62.71,
                    # 优惠券期间的商品销售数量 [原字段 'sales_volume']
                    "sales_qty": 174,
                    # 优惠券期间的商品销售金额 [原字段 'sales_amount']
                    "sales_amt": 3082.17,
                    # 优惠券的开始时间 (站点时间) [原字段 'promotion_start_time']
                    "start_time": "2024-12-09 00:00:00",
                    # 优惠券的结束时间 (站点时间) [原字段 'promotion_end_time']
                    "end_time": "2025-01-08 00:00:00",
                    # 首次同步时间 (站点时间)
                    "first_sync_time": "2025-01-07 01:25:01",
                    # 最后同步时间 (站点时间)
                    "last_sync_time": "2025-01-08 01:22:32",
                },
                ...
            ],
        }
        ```
        """
        url = route.PROMOTION_COUPONS
        # 解析并验证参数
        args = {
            "sids": sids,
            "start_data": start_data,
            "end_data": end_data,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.Promotions.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.PromotionCoupons.model_validate(data)

    async def PromotionDeals(
        self,
        *,
        sids: int | list[int] | None = None,
        start_data: str | datetime.date | datetime.datetime | None = None,
        end_data: str | datetime.date | datetime.datetime | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.PromotionDeals:
        """查询促销列表 - Deal

        ## Docs:
        - 销售 - 促销管理: [查询促销活动列表-秒杀](https://apidoc.lingxing.com/#/docs/Sale/promotionalActivitiesSecKillList)

        :param sids `<'int/list[int]'>`: 领星店铺ID或ID列表,
            默认 `None` (查询所有店铺), 参数来源: `Seller.sid`
        :param start_data `<'str/date/datetime'>`: 促销开始日期, 默认 `None`
        :param end_data `<'str/date/datetime'>`: 促销结束日期, 默认 `None`
        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 最大值200, 默认 `None` (使用: 20)
        :returns `<'PromotionDeals'>`: 返回查询到的促销列表
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
                    # 领星店铺ID (Seller.sid)
                    "sid": 1,
                    # Deal 类型 [原字段 'promotion_type']
                    # (1: Best Deal, 2: Lightning Deal)
                    "deal_type": 2,
                    # Deal 名称 [原字段 'description']
                    "deal_name": "秒杀-2024/11/01 2-34-2-883",
                    # Deal 状态 [原字段 'origin_status']
                    "status": "ENDED",
                    # Deal 备注 [原字段 'remark']
                    "note": "",
                    # Deal 商品标题 [原字段 'name']
                    "product_title": "Product Title",
                    # Deal 商品数量 [原字段 'product_quantity']
                    "product_count": 1,
                    # 货币符号
                    "currency_icon": "$",
                    # Deal 费用 [原字段 'seckill_fee']
                    "deal_fee": 150.0,
                    # 参与 Deal 的商品库存数量 [原字段 'participate_inventory']
                    "deal_qty": 140,
                    # Deal 期间的商品销售数量 [原字段 'sales_volume']
                    "sales_qty": 103,
                    # Deal 期间参促库存的转化率 [原字段 'sold_rate']
                    # (sales_qty / deal_qty * 100)
                    "sales_rate": 73.57,
                    # Deal 期间商品详情页的浏览量 [原字段 'page_view']
                    "page_views": 524,
                    # Deal 期间浏览至购买的转化率 [原字段 'exchange_rate']
                    # (sales_qty / page_views * 100)
                    "conversion_rate": 19.66,
                    # Deal 期间的商品销售金额 [原字段 'sales_amount']
                    "sales_amt": 4529.94,
                    # Deal 开始时间 (站点时间) [原字段 'promotion_start_time']
                    "start_time": "2024-11-14 10:35:00",
                    # Deal 结束时间 (站点时间) [原字段 'promotion_end_time']
                    "end_time": "2024-11-14 22:35:00",
                    # 首次同步时间 (站点时间)
                    "first_sync_time": "2024-11-18 22:04:44",
                    # 最后同步时间 (站点时间)
                    "last_sync_time": "2024-11-18 22:04:44",
                },
                ...
            ],
        }
        ```
        """
        url = route.PROMOTION_DEALS
        # 解析并验证参数
        args = {
            "sids": sids,
            "start_data": start_data,
            "end_data": end_data,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.Promotions.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.PromotionDeals.model_validate(data)

    async def PromotionActivities(
        self,
        *,
        sids: int | list[int] | None = None,
        start_data: str | datetime.date | datetime.datetime | None = None,
        end_data: str | datetime.date | datetime.datetime | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.PromotionActivities:
        """查询促销列表 - 活动

        ## Docs:
        - 销售 - 促销管理: [查询促销活动列表-管理促销](https://apidoc.lingxing.com/#/docs/Sale/promotionalActivitiesManageList)

        :param sids `<'int/list[int]'>`: 领星店铺ID或ID列表,
            默认 `None` (查询所有店铺), 参数来源: `Seller.sid`
        :param start_data `<'str/date/datetime'>`: 促销开始日期, 默认 `None`
        :param end_data `<'str/date/datetime'>`: 促销结束日期, 默认 `None`
        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 最大值200, 默认 `None` (使用: 20)
        :returns `<'PromotionActivities'>`: 返回查询到的促销列表
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
                    # 领星店铺ID (Seller.sid)
                    "sid": 1,
                    # 促销活动类型
                    # (0: 未定义类型, 3: 买一赠一, 4: 购买折扣, 5: 一口价, 8: 社媒促销)
                    "promotion_type": 4,
                    # 促销活动名称 [原字段 'name']
                    "promotion_name": "6%BUY2",
                    # 促销活动状态 [原字段 'origin_status']
                    "status": "ACTIVE",
                    # 促销活动备注 [原字段 'remark']
                    "note": "",
                    # 促销活动优惠码 [原字段 'promotion_code']
                    "code": "不需要",
                    # 促销活动参与条件 [原字段 'participate_condition']
                    "requirement": "At least this quantity of items 2",
                    # 促销活动参与条件数值 [原字段 'participate_condition_num']
                    "requirement_value": 2,
                    # 促销活动优惠内容 [原字段 'buyer_gets']
                    "offer": "Percent off 6",
                    # 促销活动优惠内容数值 [原字段 'buyer_gets_num']
                    "offer_value": 6,
                    # 促销活动需购买商品
                    "purchase_product": "ASIN List",
                    # 促销活动可享受折扣商品
                    "discount_product": "ASIN List",
                    # 促销活动排除商品
                    "exclude_product": "",
                    # 促销活动是否限制兑换量 (0: 否, 1: 是) [原字段 'exchange_limit']
                    "limited": 0,
                    # 货币符号
                    "currency_icon": "€",
                    # 促销活动期间的商品销售数量 [原字段 'sales_volume']
                    "sales_qty": 1278,
                    # 促销活动期间的商品销售金额 [原字段 'sales_amount']
                    "sales_amt": 81222.45,
                    # 促销活动开始时间 (站点时间) [原字段 'promotion_start_time']
                    "start_time": "2025-01-02 13:00:00",
                    # 促销活动结束时间 (站点时间) [原字段 'promotion_end_time']
                    "end_time": "2025-06-30 23:59:00",
                    # 首次同步时间 (站点时间)
                    "first_sync_time": "2025-01-06 23:14:55",
                    # 最后同步时间 (站点时间)
                    "last_sync_time": "2025-01-08 23:54:13",
                },
                ...
            ],
        }
        ```
        """
        url = route.PROMOTION_ACTIVITIES
        # 解析并验证参数
        args = {
            "sids": sids,
            "start_data": start_data,
            "end_data": end_data,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.Promotions.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.PromotionActivities.model_validate(data)

    async def PromotionDiscounts(
        self,
        *,
        sids: int | list[int] | None = None,
        start_data: str | datetime.date | datetime.datetime | None = None,
        end_data: str | datetime.date | datetime.datetime | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.PromotionDiscounts:
        """查询促销列表 - 价格折扣

        ## Docs:
        - 销售 - 促销管理: [查询促销活动列表-会员折扣](https://apidoc.lingxing.com/#/docs/Sale/promotionalActivitiesVipDiscountList)

        :param sids `<'int/list[int]'>`: 领星店铺ID或ID列表,
            默认 `None` (查询所有店铺), 参数来源: `Seller.sid`
        :param start_data `<'str/date/datetime'>`: 促销开始日期, 默认 `None`
        :param end_data `<'str/date/datetime'>`: 促销结束日期, 默认 `None`
        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 最大值200, 默认 `None` (使用: 20)
        :returns `<'PromotionDiscounts'>`: 返回查询到的促销列表
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
                    # 领星店铺ID (Seller.sid)
                    "sid": 1,
                    # 折扣名称 [原字段 'name']
                    "discount_name": "会员专享8月份",
                    # 折扣状态 [原字段 'origin_status']
                    "status": "EXPIRED",
                    # 折扣备注 [原字段 'remark']
                    "note": "",
                    # 货币符号
                    "currency_icon": "€",
                    # 参与折扣的商品数量
                    "product_quantity": 100,
                    # 折扣开始时间 (站点时间) [原字段 'promotion_start_time']
                    "start_time": "2024-07-28 00:00:00",
                    # 折扣结束时间 (站点时间) [原字段 'promotion_end_time']
                    "end_time": "2024-08-26 23:59:00",
                    # 首次同步时间 (站点时间)
                    "first_sync_time": "2024-08-19 21:03:32",
                    # 最后同步时间 (站点时间)
                    "last_sync_time": "2024-10-10 21:15:53",
                    # 更细时间 (站点时间)
                    "update_time": "",
                },
                ...
            ],
        }
        ```
        """
        url = route.PROMOTION_DISCOUNTS
        # 解析并验证参数
        args = {
            "sids": sids,
            "start_data": start_data,
            "end_data": end_data,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.Promotions.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.PromotionDiscounts.model_validate(data)

    async def PromotionOnListings(
        self,
        site_date: str | datetime.date | datetime.datetime,
        *,
        start_data: str | datetime.date | datetime.datetime | None = None,
        end_data: str | datetime.date | datetime.datetime | None = None,
        sids: int | list[int] | None = None,
        promotion_type: int | list[int] | None = None,
        promotion_status: int | list[int] | None = None,
        product_status: int | list[int] | None = None,
        is_coupon_stacked: int | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.PromotionOnListings:
        """查询应用到 Listing 上的促销列表

        ## Docs:
        - 销售 - 促销管理: [查询商品折扣列表](https://apidoc.lingxing.com/#/docs/Sale/promotionListingList)

        :param site_date `<'str/date/datetime'>`: 站点日期, 必须是 str, date 或 datetime 类型
        :param start_data `<'str/date/datetime'>`: 促销开始日期, 默认 `None`
        :param end_data `<'str/date/datetime'>`: 促销结束日期, 默认 `None`
        :param sids `<'int/list[int]'>`: 领星店铺ID或ID列表,
            默认 `None` (查询所有店铺), 参数来源: `Seller.sid`
        :param promotion_type `<'int/list[int]'>`: 促销类型或类型列表, 默认 `None` (查询所有类型)

            - `1`: 优惠券
            - `2`: Deal
            - `3`: 活动
            - `4`: 价格折扣

        :param promotion_status `<'int/list[int]'>`: 促销状态或状态列表, 默认 `None` (查询所有状态)

            - `0`: 其他
            - `1`: 进行中
            - `2`: 已过期
            - `3`: 未开始

        :param product_status `<'int/list[int]'>`: 商品状态或状态列表, 默认 `None` (查询所有状态)

            - `-1`: 已删除
            - `0`: 停售
            - `1`: 在售

        :param is_coupon_stacked `<'int'>`: 是否叠加优惠券 (0: 否, 1: 是), 默认 `None` (查询所有)
        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 最大值200, 默认 `None` (使用: 20)
        :returns `<'PromotionOnListings'>`: 返回查询到的应用到 Listing 上的促销列表
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
                    # 领星店铺ID (Seller.sid)
                    "sid": 1,
                    # 领星店铺名称 (Seller.name) [原字段 'store_name']
                    "seller_name": "Seller****",
                    # 国家 (中文) [原字段 'region_name']
                    "country": "加拿大",
                    # 商品ASIN
                    "asin": "B0********",
                    # 亚马逊卖家SKU (Listing.msku) [原字段 'seller_sku']
                    "msku": "SKU********",
                    # 商品标题 [原字段 'item_name']
                    "title": "Product Title",
                    # 商品链接
                    "asin_url": "https://www.amazon.ca/dp/B0********",
                    # 商品略缩图链接 [原字段 'small_image_url']
                    "thumbnail_url": "https://m.media-amazon.com/images/I/7***.jpg",
                    # 促销活动叠加数量 [原字段 'promotion_combo_num']
                    "promotion_stacks": 2,
                    # 货币符号
                    "currency_icon": "CA$",
                    # 销售价格
                    "sales_price": 54.89,
                    # 销售价格 (美金)
                    "sales_price_usd": 41.14,
                    # 最低折扣价格 [原字段 'discount_price_min']
                    "discount_min_price": 36.58,
                    # 平均折扣金额 [原字段 'avg_deal_price']
                    "discount_avg_amt": 0.0,
                    # 平均折扣百分比 [原字段 'discount_rate_rate']
                    "discount_avg_pct": 83.0,
                    # FBA可售库存 [原字段 'afn_fulfillable_quantity']
                    "afn_fulfillable_qty": 0,
                    # FBM可售库存 [原字段 'quantity']
                    "mfn_fulfillable_qty": 0,
                    # Listing负责人 [原字段 'principal_list']
                    "operators": ["白小白"],
                    # Listing标签 [原字段: 'listing_tags']
                    "tags": [
                        {
                            # 领星标签ID (ListingGlobalTag.tag_id) [原字段 'global_tag_id']
                            "tag_id": "90****************",
                            # 领星标签名称 (ListingGlobalTag.tag_name) [原字段 'tag_name']
                            "tag_name": "特殊",
                            # 领星标签颜色 (如: "#FF0000") [原字段 'color']
                            "tag_color": "#4B8BFA",
                        },
                        ...
                    ],
                    "promotions": [
                        {
                            # 促销ID
                            "promotion_id": "823e7911-8cc5-****-****-************",
                            # 促销名称 [原字段: 'name']
                            "promotion_name": "Promotion",
                            # 促销状态 [原字段 'origin_status']
                            "status": "APPROVED",
                            # 促销状态码 (0: 其他, 1: 进行中, 2: 已过期, 3: 未开始) [原字段 'status']
                            "status_code": 3,
                            # 促销类型 (1: 优惠券, 2: Deal, 3 活动, 4 价格折扣) [原字段 'category']
                            "promotion_type": 2,
                            # 促销类型文本 [原字段 'category_text']
                            "promotion_type_text": "秒杀",
                            # 促销子类型 [原字段 'promotion_type']
                            "promotion_sub_type": 2,
                            # 促销子类型文本 [原字段 'promotion_type_text']
                            "promotion_sub_type_text": "Lightning Deal",
                            # 折扣金额/折扣售价 [原字段 'discount_price']
                            "discount_amt": 46.31,
                            # 折扣百分比/售价百分比 [原字段 'discount_rate']
                            "discount_pct": 83.0,
                            # 促销开始时间 (站点时间) [原字段 'promotion_start_time']
                            "start_time": "2024-10-22 05:30:00",
                            # 促销结束时间 (站点时间) [原字段 'promotion_end_time
                            "end_time": "2024-10-22 17:30:00",
                        },
                        ...
                    ],
                },
                ...
            ],
        }
        ```
        """
        url = route.PROMOTION_ON_LISTINGS
        # 解析并验证参数
        args = {
            "site_date": site_date,
            "start_data": start_data,
            "end_data": end_data,
            "sids": sids,
            "promotion_type": promotion_type,
            "promotion_status": promotion_status,
            "product_status": product_status,
            "is_coupon_stacked": is_coupon_stacked,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.PromotionOnListings.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.PromotionOnListings.model_validate(data)
