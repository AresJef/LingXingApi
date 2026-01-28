# -*- coding: utf-8 -*-c
import datetime
from typing import Literal
from lingxingapi import errors
from lingxingapi.base.api import BaseAPI
from lingxingapi.source import param, route, schema

# Type Aliases ---------------------------------------------------------------------------------------------------------
ORDER_DATE_TYPE = Literal["update_date", "request_date"]
SEARCH_FIELD = Literal["asin", "msku", "fnsku", "title", "transaction_item_id"]
REPORT_REGION = Literal["NA", "EU", "FE"]


# API ------------------------------------------------------------------------------------------------------------------
class SourceAPI(BaseAPI):
    """领星API `亚马逊源数据` 接口

    ## Notice
    请勿直接实例化此类
    """

    # 公共 API --------------------------------------------------------------------------------------
    # 订单数据 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    async def Orders(
        self,
        sid: int,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        *,
        date_type: int | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.Orders:
        """查询亚马逊所有类型(FBA & FBM)的源订单

        ## Docs
        - 亚马逊源表数据: [查询亚马逊源报表-所有订单](https://apidoc.lingxing.com/#/docs/SourceData/AllOrders)
        - 对应亚马逊 'All Orders Report By Last Update' 源报告

        :param sid `<'int'>`: 领星店铺ID
        :param start_date `<'str/date/datetime'>`: 查询开始日期
        :param end_date `<'str/date/datetime'>`: 查询结束日期
        :param date_type `<'int/None'>`: 日期类型, 默认 `None` (使用: 1)

            - `1`: 下单日期
            - `2`: 亚马逊订单更新时间

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 1000)
        :returns `<'Orders'>`: 返回查询到的亚马逊所有类型(FBA & FBM)的源订单结果
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
                    # 亚马逊订单编号
                    "amazon_order_id": "113-*******-*******",
                    # 卖家提供的订单编号
                    "merchant_order_id": "113-*******-*******",
                    # 配送方式 ("Amazon" [AFN] 或 "Merchant" [MFN])
                    "fulfillment_channel": "Amazon",
                    # 销售渠道 (如: "Amazon.com")
                    "sales_channel": "Amazon.com",
                    # 销售子渠道 (CBA/WBA) [原字段 'order_channel']
                    "sales_sub_channel": "",
                    # 订单配送服务级别 [原字段 'ship_service_level']
                    "shipment_service": "Expedited",
                    # 是否为B2B订单 [原字段 'is_business_order']
                    "is_b2b_order": "false",
                    # 订单状态
                    "order_status": "Shipped",
                    # 订单商品状态 [原字段 'item_status']
                    "order_item_status": "Shipped",
                    # 领星产品ID [原字段 'pid']
                    "product_id": 2*****,
                    # 领星产品名称 [原字段 'local_name']
                    "product_name": "Apple",
                    # 商品ASIN
                    "asin": "B0D*******",
                    # 亚马逊SKU [原字段 'sku']
                    "msku": "SKU*********",
                    # 本地SKU [原字段 'local_sku']
                    "lsku": "LOCAL********",
                    # 商品标题 [原字段 'product_name']
                    "title": "Product Title",
                    # ASIN链接 [原字段 'url']
                    "asin_url": "",
                    # 商品促销标识 [原字段 'promotion_ids']
                    "promotion_labels": "",
                    # 订单商品总数量 [原字段 'quantity']
                    "order_qty": 1,
                    # 商品销售金额 [原字段 'item_price']
                    "sales_amt": 27.98,
                    # 商品销售金额税费 [原字段 'item_tax']
                    "sales_tax_amt": 2.31,
                    # 买家支付运费金额 [原字段 'shipping_price']
                    "shipping_credits_amt": 0.33,
                    # 买家支付运费税费 [原字段 'shipping_tax']
                    "shipping_credits_tax_amt": 0.0,
                    # 买家支付礼品包装费金额 [原字段 'gift_wrap_price']
                    "giftwrap_credits_amt": 0.0,
                    # 买家支付礼品包装费税费 [原字段 'gift_wrap_tax']
                    "giftwrap_credits_tax_amt": 0.0,
                    # 卖家商品促销折扣金额 [原字段 'item_promotion_discount']
                    "promotion_discount_amt": 0.0,
                    # 卖家商品运费折扣金额 [原字段 'ship_promotion_discount']
                    "shipping_discount_amt": 0.33,
                    # 货币代码 [原字段 'currency']
                    "currency_code": "USD",
                    # 买家国家代码 [原字段 'ship_country']
                    "buyer_country_code": "US",
                    # 买家州/省 [原字段 'ship_state']
                    "buyer_state": "TX",
                    # 买家城市 [原字段 'ship_city']
                    "buyer_city": "ROWLETT",
                    # 买家邮编 [原字段 'ship_postal_code']
                    "buyer_postcode": "75088-8321",
                    # 订单购买时间 (UTC时间) [原字段 'purchase_date']
                    "purchase_time_utc": "2025-08-23T18:54:00+00:00",
                    # 订单购买时间 (本地时间) [原字段 'purchase_date_local']
                    "purchase_time_loc": "2025-08-23 11:54:00",
                    # 订单购买日期 (本地日期) [原字段 'purchase_date_locale']
                    "purchase_date_loc": "2025-08-23",
                    # 订单发货时间 (本地时间) [原字段 'shipment_date']
                    "shipment_time_loc": "2025-08-23T23:48:09-07:00",
                    # 订单更新时间 (时间戳) [原字段 'last_updated_time']
                    "update_time_ts": 1756248908,
                },
                ...
            ],
        }
        ```
        """
        url = route.ORDERS
        # 解析并验证参数
        args = {
            "sid": sid,
            "start_date": start_date,
            "end_date": end_date,
            "date_type": date_type,
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

    async def FbaOrders(
        self,
        sid: int,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        *,
        date_type: int | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.FbaOrders:
        """查询亚马逊FBA源订单

        ## Docs
        - 亚马逊源表数据: [查询亚马逊源报表-FBA订单](https://apidoc.lingxing.com/#/docs/SourceData/FbaOrders)
        - 对应亚马逊 'Amazon-Fulfilled Shipments Report' 源报告

        :param sid `<'int'>`: 领星店铺ID
        :param start_date `<'str/date/datetime'>`: 查询开始日期
        :param end_date `<'str/date/datetime'>`: 查询结束日期
        :param date_type `<'int/None'>`: 日期类型, 默认 `None` (使用: 1)

            - `1`: 下单日期
            - `2`: 配送日期

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 1000)
        :returns `<'FbaOrders'>`: 返回查询到的亚马逊FBA源订单结果
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
                    # 亚马逊订单编号
                    "amazon_order_id": "114-*******-*******",
                    # 亚马逊订单商品编号
                    "amazon_order_item_id": "1367***********",
                    # 配送方式 (AFN 或 MFN)
                    "fulfillment_channel": "AFN",
                    # 亚马逊货件编号
                    "shipment_id": "Bqy******",
                    # 亚马逊货件商品编号
                    "shipment_item_id": "DLXY*********",
                    # 订单配送服务级别 [原字段 'ship_service_level']
                    "shipment_service": "Expedited",
                    # 承运商代码 [原字段 'carrier']
                    "shipment_carrier": "AMZN_US",
                    # 追踪单号
                    "tracking_number": "TBA************",
                    # 亚马逊SKU [原字段 'sku']
                    "msku": "SKU*********",
                    # 商品标题 [原字段 'product_name']
                    "title": "Product Title",
                    # 发货商品数量 [原字段 'quantity_shipped']
                    "shipped_qty": 1,
                    # 商品销售金额 [原字段 'item_price']
                    "sales_amt": 34.98,
                    # 商品销售金额税费 [原字段 'item_tax']
                    "sales_tax_amt": 2.54,
                    # 买家支付运费金额 [原字段 'shipping_price']
                    "shipping_credits_amt": 0.0,
                    # 买家支付运费税费 [原字段 'shipping_tax']
                    "shipping_credits_tax_amt": 0.0,
                    # 买家支付礼品包装费金额 [原字段 'gift_wrap_price']
                    "giftwrap_credits_amt": 0.0,
                    # 买家支付礼品包装费税费 [原字段 'gift_wrap_tax']
                    "giftwrap_credits_tax_amt": 0.0,
                    # 卖家商品促销折扣金额 [原字段 'item_promotion_discount']
                    "promotion_discount_amt": 0.0,
                    # 卖家商品运费折扣金额 [原字段 'ship_promotion_discount']
                    "shipping_discount_amt": 0.0,
                    # 亚马逊积分抵付款金额 (日本站) [原字段 'points_granted']
                    "points_discount_amt": 0.0,
                    # 货币代码 [原字段 'currency']
                    "currency_code": "USD",
                    # 买家国家代码 [原字段 'ship_country']
                    "buyer_country_code": "US",
                    # 买家州/省 [原字段 'ship_state']
                    "buyer_state": "NC",
                    # 买家城市 [原字段 'ship_city']
                    "buyer_city": "RALEIGH",
                    # 买家地址 [原字段 'ship_address_1']
                    "buyer_address": "",
                    # 买家邮编 [原字段 'ship_postal_code']
                    "buyer_postcode": "27614-9689",
                    # 买家名称
                    "buyer_name": "",
                    # 买家邮箱
                    "buyer_email": "****@marketplace.amazon.com",
                    # 买家电话 [原字段 'buyer_phone_number']
                    "buyer_phone": "",
                    # 收件人名称
                    "recipient_name": "",
                    # 订单购买时间 (UTC时间) [原字段 'purchase_date']
                    "purchase_time_utc": "2025-08-17T12:39:08+00:00",
                    # 订单支付时间 (UTC时间) [原字段 'payments_date']
                    "payments_time_utc": "2025-08-18T09:09:35+00:00",
                    # 订单发货时间 (UTC时间) [原字段 'shipment_date']
                    "shipment_time_utc": "2025-08-18T08:11:52+00:00",
                    # 预计送达时间 (UTC时间) [原字段 'estimated_arrival_date']
                    "estimated_arrival_time_utc": "2025-08-19T03:00:00+00:00",
                    # 报告数据时间 (UTC时间) [原字段 'reporting_date']
                    "report_time_utc": "2025-08-18T09:12:04+00:00",
                },
                ...
            ],
        }
        ```
        """
        url = route.FBA_ORDERS
        # 解析并验证参数
        args = {
            "sid": sid,
            "start_date": start_date,
            "end_date": end_date,
            "date_type": date_type,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.Orders.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.FbaOrders.model_validate(data)

    async def FbaReplacementOrders(
        self,
        sid: int,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        *,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.FbaReplacementOrders:
        """查询亚马逊FBA换货源订单

        ## Docs
        - 亚马逊源表数据: [查询亚马逊源报表-FBA换货订单](https://apidoc.lingxing.com/#/docs/SourceData/fbaExchangeOrderList)
        - 对应亚马逊 'Replacements Report' 源报告

        :param sid `<'int'>`: 领星店铺ID
        :param start_date `<'str/date/datetime'>`: 查询开始日期
        :param end_date `<'str/date/datetime'>`: 查询结束日期
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 1000)
        :returns `<'FbaReplacementOrders'>`: 返回查询到的亚马逊FBA换货订单结果
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
                    "sid": 9857,
                    # 订单唯一哈希值 (不是唯一键)
                    "order_hash": "26f96f**************************",
                    # 原始亚马逊订单编号 [原字段 'original_amazon_order_id']
                    "amazon_order_id": "113-*******-*******",
                    # 原始亚马逊配送中心代码 [原字段 'original_fulfillment_center_id']
                    "fulfillment_center_id": "SBD6",
                    # 换货商品ASIN
                    "asin": "B0D*******",
                    # 换货商品SKU [原字段 'seller_sku']
                    "msku": "SKU*********",
                    # 换货亚马逊订单编号
                    "replacement_amazon_order_id": "113-*******-*******",
                    # 换货亚马逊配送中心代码 [原字段 'fulfillment_center_id']
                    "replacement_fulfillment_center_id": "SBD6",
                    # 换货数量 [原字段 'quantity']
                    "replacement_qty": 1,
                    # 换货原因代码
                    "replacement_reason_code": 2,
                    # 换货原因描述 [原字段 'replacement_reason_msg']
                    "replacement_reason_desc": "Defective(存在缺陷)",
                    # 换货时间 (UTC时间) [原字段 'shipment_date']
                    "replacement_time_utc": "2025-08-25 17:00:00",
                    # 数据同步时间 (时间戳) [原字段 'sync_time']
                    "sync_time_ts": -210424147,
                },
                ...
            ],
        }
        ```
        """
        url = route.FBA_REPLACEMENT_ORDERS
        # 解析并验证参数
        args = {
            "sid": sid,
            "start_date": start_date,
            "end_date": end_date,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.Orders.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.FbaReplacementOrders.model_validate(data)

    async def FbaReturnOrders(
        self,
        sid: int,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        *,
        date_type: int | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.FbaReturnOrders:
        """查询亚马逊FBA退货源订单

        ## Docs
        - 亚马逊源表数据: [查询亚马逊源报表-FBA退货订单](https://apidoc.lingxing.com/#/docs/SourceData/RefundOrders)
        - 对应亚马逊 'FBA Customer Returns' 源报告

        :param sid `<'int'>`: 领星店铺ID
        :param start_date `<'str/date/datetime'>`: 查询开始日期
        :param end_date `<'str/date/datetime'>`: 查询结束日期
        :param date_type `<'int/None'>`: 日期类型, 默认 `None` (使用: 1)

            - `1`: 退货日期 (站点时间)
            - `2`: 更新日期 (北京时间)

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 1000)
        :returns `<'FbaReturnOrders'>`: 返回查询到的亚马逊FBA退货源订单结果
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
                    "sid": 9857,
                    # 亚马逊订单编号 [原字段 'order_id']
                    "amazon_order_id": "113-*******-*******",
                    # 亚马逊配送中心代码
                    "fulfillment_center_id": "PCW1",
                    # 退货商品ASIN
                    "asin": "B0D*******",
                    # 退货亚马逊SKU [原字段 'sku']
                    "msku": "SKU*********",
                    # 退货领星本地SKU [原字段 'local_sku']
                    "lsku": "LOCAL********",
                    # 退货亚马逊FNSKU
                    "fnsku": "X00*******",
                    # 退货商品标题 [原字段 'product_name']
                    "title": "Product Title",
                    # 退货商品数量 [原字段 'quantity']
                    "return_qty": 1,
                    # 退货状态 [原字段 'status']
                    "return_status": "Unit returned to inventory",
                    # 退货原因 [原字段 'reason']
                    "return_reason": "UNDELIVERABLE_UNKNOWN",
                    # 退货备注 [原字段 'remark']
                    "return_note": "",
                    # 退货处置结果 [原字段 'detailed_disposition']
                    "disposition": "SELLABLE",
                    # LNP编码号 [原字段 'license_plate_number']
                    "lpn_number": "LPN***********",
                    # 买家评论
                    "customer_comments": "",
                    # 订单购买时间 (UTC时间) [原字段 'purchase_date']
                    "purchase_time_utc": "2025-07-09T21:54:01Z",
                    # 订单购买日期 (本地日期) [原字段 'purchase_date_locale']
                    "purchase_date_loc": "2025-07-09",
                    # 退货时间 (UTC时间) [原字段 'return_date']
                    "return_time_utc": "2025-08-07T01:57:29+01:00",
                    # 退货日期 (本地日期) [原字段 'return_date_locale']
                    "return_date_loc": "2025-08-06",
                    # 数据最后修改时间 (北京时间) [原字段 'gmt_modified']
                    "update_time_cnt": "2025-08-07 13:04:59",
                    # 退货标签 [原字段 'tag']
                    "tags": [
                        {
                            # 标签名称
                            "tag_name": "尺码问题",
                            # 标签颜色
                            "tag_color": "#FF0000",
                        },
                        ...
                    ],
                },
                ...
            ],
        }
        ```
        """
        url = route.FBA_RETURN_ORDERS
        # 解析并验证参数
        args = {
            "sid": sid,
            "start_date": start_date,
            "end_date": end_date,
            "date_type": date_type,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.Orders.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.FbaReturnOrders.model_validate(data)

    async def FbaShipments(
        self,
        sid: int,
        start_time: str | datetime.date | datetime.datetime,
        end_time: str | datetime.date | datetime.datetime,
        *,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.FbaShipments:
        """查询亚马逊FBA发货源订单

        ## Docs
        - 亚马逊源表数据: [查询亚马逊源报表—Amazon Fulfilled Shipments v1](https://apidoc.lingxing.com/#/docs/SourceData/v1getAmazonFulfilledShipmentsList)
        - 对应亚马逊 'Amazon Fulfilled Shipments' 源报告

        :param sid `<'int'>`: 领星店铺ID
        :param start_time `<'str/date/datetime'>`: 查询发货开始时间 `shipment_time_loc`
        :param end_time `<'str/date/datetime'>`: 查询发货结束时间 `shipment_time_loc`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 1000)
        :returns `<'FbaShipments'>`: 返回查询到的亚马逊FBA发货源订单结果
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
                    # 亚马逊订单编号
                    "amazon_order_id": "114-*******-*******",
                    # 亚马逊订单商品编号
                    "amazon_order_item_id": "1373***********",
                    # 商家订单编号
                    "merchant_order_id": "",
                    # 商家订单商品编号
                    "merchant_order_item_id": "",
                    # 销售渠道 (如: "amazon.com")
                    "sales_channel": "amazon.com",
                    # 配送方式 (AFN 或 MFN)
                    "fulfillment_channel": "AFN",
                    # 亚马逊配送中心代码
                    "fulfillment_center_id": "AFW1",
                    # 亚马逊货件编号
                    "shipment_id": "BB3******",
                    # 亚马逊货件商品编号
                    "shipment_item_id": "D0k**********",
                    # 订单配送服务级别 [原字段 'ship_service_level']
                    "shipment_service": "Expedited",
                    # 承运商代码 [原字段 'carrier']
                    "shipment_carrier": "AMZN_US",
                    # 追踪单号
                    "tracking_number": "TBA3***********",
                    # 亚马逊SKU
                    "msku": "SKU*********",
                    # 领星本地SKU [原字段 'local_sku']
                    "lsku": "LOCAL********",
                    # 领星产品名称 [原字段 'local_name']
                    "product_name": "JBL",
                    # 商品标题 [原字段 'product_name']
                    "title": "Product Title",
                    # 发货商品数量 [原字段 'quantity_shipped']
                    "shipped_qty": 1,
                    # 商品销售金额 [原字段 'item_price']
                    "sales_amt": 27.98,
                    # 商品销售金额税费 [原字段 'item_tax']
                    "sales_tax_amt": 1.89,
                    # 买家支付运费金额 [原字段 'shipping_price']
                    "shipping_credits_amt": 0.0,
                    # 买家支付运费税费 [原字段 'shipping_tax']
                    "shipping_credits_tax_amt": 0.0,
                    # 买家支付礼品包装费金额 [原字段 'gift_wrap_price']
                    "giftwrap_credits_amt": 0.0,
                    # 买家支付礼品包装费税费 [原字段 'gift_wrap_tax']
                    "giftwrap_credits_tax_amt": 0.0,
                    # 卖家商品促销折扣金额 [原字段 'item_promotion_discount']
                    "promotion_discount_amt": 0.0,
                    # 卖家商品运费折扣金额 [原字段 'ship_promotion_discount']
                    "shipping_discount_amt": 0.0,
                    # 亚马逊积分抵付款金额 (日本站) [原字段 'points_granted']
                    "points_discount_amt": 0.0,
                    # 货币代码 [原字段 'currency']
                    "currency_code": "USD",
                    # 买家国家代码 [原字段 'ship_country']
                    "buyer_country_code": "US",
                    # 买家州/省 [原字段 'ship_state']
                    "buyer_state": "TX",
                    # 买家城市 [原字段 'ship_city']
                    "buyer_city": "KENDALIA",
                    # 买家地址1 [原字段 'ship_address_1']
                    "buyer_address1": "",
                    # 买家地址2 [原字段 'ship_address_2']
                    "buyer_address2": "",
                    # 买家地址3 [原字段 'ship_address_3']
                    "buyer_address3": "",
                    # 买家邮编 [原字段 'ship_postal_code']
                    "buyer_postcode": "78027-1803",
                    # 买家名称
                    "buyer_name": "",
                    # 买家邮箱
                    "buyer_email": "b589v2l553nyyh2@marketplace.amazon.com",
                    # 买家电话 [原字段 'buyer_phone_number']
                    "buyer_phone": "",
                    # 收件人名称
                    "recipient_name": "",
                    # 账单国家代码 [原字段 'bill_country']
                    "billing_country_code": "",
                    # 账单州/省 [原字段 'bill_state']
                    "billing_state": "",
                    # 账单城市 [原字段 'bill_city']
                    "billing_city": "",
                    # 账单地址1 [原字段 'bill_address_1']
                    "billing_address1": "",
                    # 账单地址2 [原字段 'bill_address_2']
                    "billing_address2": "",
                    # 账单地址3 [原字段 'bill_address_3']
                    "billing_address3": "",
                    # 账单邮编 [原字段 'bill_postal_code']
                    "billing_postcode": "",
                    # 订单购买时间 (UTC时间) [原字段 'purchase_date']
                    "purchase_time_utc": "2025-08-25T18:21:12+00:00",
                    # 订单购买日期 (本地时间) [原字段 'purchase_date_locale']
                    "purchase_time_loc": "2025-08-25T11:21:12-07:00",
                    # 订单付款时间 (UTC时间) [原字段 'payments_date']
                    "payments_time_utc": "2025-08-26T04:20:05+00:00",
                    # 订单付款时间 (本地时间) [原字段 'payments_date_locale']
                    "payments_time_loc": "2025-08-25T21:20:05-07:00",
                    # 订单发货时间 (UTC时间) [原字段 'shipment_date']
                    "shipment_time_utc": "2025-08-26T04:20:05+00:00",
                    # 订单发货时间 (本地时间) [原字段 'shipment_date_locale']
                    "shipment_time_loc": "2025-08-25T21:20:05-07:00",
                    # 预计送达时间 (UTC时间) [原字段 'estimated_arrival_date']
                    "estimated_arrival_time_utc": "2025-08-27T03:00:00+00:00",
                    # 预计送达日期 (本地日期) [原字段 'estimated_arrival_date_locale']
                    "estimated_arrival_date_loc": "2025-08-26",
                    # 报告数据时间 (UTC时间) [原字段 'reporting_date']
                    "report_time_utc": "2025-08-26T07:20:13+00:00",
                    # 报告数据时间 (本地时间) [原字段 'reporting_date_locale']
                    "report_time_loc": "2025-08-26T00:20:13-07:00",
                },
                ...
            ],
        }
        ```
        """
        url = route.FBA_SHIPMENTS_V1
        # 解析并验证参数
        args = {
            "sid": sid,
            "start_time": start_time,
            "end_time": end_time,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.FbaShipments.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.FbaShipments.model_validate(data)

    async def FbmReturnOrders(
        self,
        sid: int,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        *,
        date_type: int | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.FbmReturnOrders:
        """查询亚马逊FBM退货源订单

        ## Docs
        - 亚马逊源表数据: [查询亚马逊源报表-FBM退货订单](https://apidoc.lingxing.com/#/docs/SourceData/fbmReturnOrderList)
        - 对应亚马逊 'Returns Report' 源报告

        :param sid `<'int'>`: 领星店铺ID
        :param start_date `<'str/date/datetime'>`: 查询开始日期
        :param end_date `<'str/date/datetime'>`: 查询结束日期
        :param date_type `<'int/None'>`: 日期类型, 默认 `None` (使用: 1)

            - `1`: 退货日期
            - `2`: 下单日期

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 1000)
        :returns `<'FbmReturnOrders'>`: 返回查询到的亚马逊FBM退货源订单结果
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
                    # 领星店铺名称
                    "seller_name": "Store-UK",
                    # 国家 (中文)
                    "country": "英国",
                    # 订单唯一哈希值 (不是唯一键)
                    "order_hash": "ae6ab186************************",
                    # 亚马逊订单编号 [原字段 'order_id']
                    "amazon_order_id": "205-*******-*******",
                    # 商品ASIN
                    "asin": "B0C*******",
                    # 亚马逊SKU [原字段 'seller_sku']
                    "msku": "SKU*********",
                    # 领星本地SKU [原字段 'local_sku']
                    "lsku": "LOCAL********",
                    # 领星产品名称 [原字段 'local_name']
                    "product_name": "JBL",
                    # 品牌名称 [原字段 'brand_title']
                    "brand": "FastTech",
                    # 商品标题 [原字段 'item_name']
                    "title": "Product Title",
                    # 商品类目 [原字段 'category_title_path']
                    "category": "",
                    # 商品 ASIN 链接
                    "asin_url": "https://www.amazon.co.uk/dp/B0C*******",
                    # 商品图片链接 [原字段 'pic_url']
                    "image_url": "https://image.distributetop.com/****.jpg",
                    # 货币代码
                    "currency_code": "",
                    # 订单商品销售金额 [原字段 'order_amount']
                    "order_amt": 35.57,
                    # 订单商品退款金额 [原字段 'refunded_amount']
                    "refund_amt": 0.0,
                    # 订单商品数量 [原字段 'order_quantity']
                    "order_qty": 1,
                    # 退货商品数量 [原字段 'return_quantity']
                    "return_qty": 1,
                    # 退货状态
                    "return_status": "Approved",
                    # 退货类型
                    "return_type": "C-Returns",
                    # 退货原因
                    "return_reason": "CR-NO_REASON_GIVEN(客户退货-未提供原因)",
                    # 退货解决方案 [原字段 'resolution']
                    "return_resolution": "StandardRefund",
                    # 退货备注 [原字段 'remark']
                    "return_note": "",
                    # 退货RMA编号 [原字段 'rma_id']
                    "rma_number": "DdVn6hR1RRMA",
                    # 退货RMA提供者 [原字段 'rma_id_provider']
                    "rma_provider": "",
                    # 退货承运商 [原字段 'return_carrier']
                    "carrier": "",
                    # 退货追踪单号 [原字段 'tracking_id']
                    "tracking_number": "",
                    # 发票编号
                    "invoice_number": "",
                    # 物流标签类型
                    "label_type": "AmazonUnPaidLabel",
                    # 物流标签费用
                    "label_cost": 0.0,
                    # 物流标签费用支付方
                    "label_payer": "Customer",
                    # 是否为Prime订单 (N: No, Y: Yes)
                    "is_prime": "N",
                    # 是否在退货政策内 (N: No, Y: Yes) [原字段 'in_policy']
                    "is_within_policy": "Y",
                    # 是否是A-to-Z索赔订单 (N: No, Y: Yes) [原字段 'a_to_z_claim']
                    "is_a_to_z_claim": "N",
                    # Safe-T索赔ID
                    "safet_claim_id": "",
                    # Safe-T索赔原因 [原字段 'safet_action_reason']
                    "safet_claim_reason": "",
                    # Safe-T索赔状态
                    "safet_claim_state": "",
                    # Safe-T索赔赔付金额 [原字段 'safet_claim_reimbursement_amount']
                    "safet_claim_reimbursement_amt": 0.0,
                    # Safe-T索赔时间 [原字段 'safet_claim_creation_time']
                    "safet_claim_time": "",
                    # 购买日期
                    "order_date": "2024-07-27",
                    # 退货日期
                    "return_date": "2024-08-12",
                    # 退货送达日期
                    "return_delivery_date": "2024-08-14",
                    # 数据同步时间 (时间戳) [原字段 'sync_time']
                    "sync_time_ts": 0,
                    # 退货标签 [原字段 'tag_type_ids']
                    "tags": [
                        {
                            # 标签名称
                            "tag_name": "尺码问题",
                            # 标签颜色
                            "tag_color": "#FF0000",
                        },
                        ...
                    ],
                },
                ...
            ],
        }
        ```
        """
        url = route.FBM_RETURN_ORDERS
        # 解析并验证参数
        args = {
            "sid": sid,
            "start_date": start_date,
            "end_date": end_date,
            "date_type": date_type,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.Orders.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.FbmReturnOrders.model_validate(data)

    # FBA 库存数据 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    async def FbaRemovalOrders(
        self,
        sid: int,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        *,
        date_type: ORDER_DATE_TYPE = "update_date",
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.FbaRemovalOrders:
        """查询亚马逊FBA移除订单

        ## Docs
        - 亚马逊源表数据: [查询亚马逊源报表-移除订单(新）](https://apidoc.lingxing.com/#/docs/SourceData/RemovalOrderListNew)
        - 对应亚马逊 'Fulfillment-Removal Order Detail' 源报告

        ## Notice
        - 报告为 seller_id 维度, 请求会返回 sid 对应 seller_id 下所有移除订单数据
        - 同一个 seller_id 授权的店铺任取一个 sid 请求报告数据即可

        :param sid `<'int'>`: 领星店铺ID
        :param start_date `<'str/date/datetime'>`: 查询开始日期
        :param end_date `<'str/date/datetime'>`: 查询结束日期
        :param date_type `<'str/None'>`: 日期类型, 默认 `"update_date"`

            - `'update_date'`: 数据更新日期
            - `'request_date'`: 移除请求日期

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 1000)
        :returns `<'FbaRemovalOrders'>`: 返回查询到的亚马逊FBA移除订单结果
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
                    # 亚马逊卖家ID
                    "seller_id": "AVI**********",
                    # 站点区域
                    "region": "na",
                    # 站点国家代码
                    "country_code": "US",
                    # 移除订单编号 [原字段 'order_id']
                    "removal_order_id": "IJW*******",
                    # 移除订单类型 (Return 或 Disposal) [原字段 'order_type']
                    "removal_order_type": "Return",
                    # 移除订单状态 [原字段 'order_status']
                    "removal_order_status": "Completed",
                    # 亚马逊SKU [原字段 'sku']
                    "msku": "SKU*********",
                    # 领星本地SKU [原字段 'local_sku']
                    "lsku": "LOCAL********",
                    # 亚马逊FNSKU
                    "fnsku": "X00*******",
                    # 领星产品名称 [原字段 'local_name']
                    "product_name": "JBL",
                    # 库存处置结果
                    "disposition": "Unsellable",
                    # 移除商品请求数量 [原字段 'requested_quantity']
                    "requested_qty": 5,
                    # 取消移除商品数量 [原字段 'cancelled_quantity']
                    "cancelled_qty": 0,
                    # 移除处理中商品数量 [原字段 'in_process_quantity']
                    "processing_qty": 0,
                    # 已处置商品数量 [原字段 'disposed_quantity']
                    "disposed_qty": 0,
                    # 已发货商品数量 [原字段 'shipped_quantity']
                    "shipped_qty": 5,
                    # 移除商品费用
                    "removal_fee": 5.2,
                    # 货币代码 [原字段 'currency']
                    "currency_code": "USD",
                    # 收件地址 [原字段 'address_detail']
                    "ship_to_address": "Y10062,85756,7480 E Sycamore Park Blvd Tucson,AZ,美国",
                    # 移除请求时间 [原字段 'request_date']
                    "request_time": "2025-07-28T12:39:45-03:00",
                    # 数据更新时间 [原字段 'last_updated_date']
                    "update_time": "2025-08-11T20:31:38-03:00",
                },
                ...
            ]
        }
        ```
        """
        url = route.FBA_REMOVAL_ORDERS
        # 解析并验证参数
        args = {
            "sid": sid,
            "start_date": start_date,
            "end_date": end_date,
            "date_type": date_type,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.FbaRemovalOrders.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.FbaRemovalOrders.model_validate(data)

    async def FbaRemovalShipments(
        self,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        *,
        sid: int | None = None,
        seller_id: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.FbaRemovalShipments:
        """查询亚马逊FBA移除货件

        ## Docs
        - 亚马逊源表数据: [查询亚马逊源报表-移除货件(新）](https://apidoc.lingxing.com/#/docs/SourceData/RemovalShipmentList)
        - 对应亚马逊 'Fulfillment-Removal Shipment Detail' 源报告

        ## Notice
        - 参数 sid 和 seller_id 为可选参数, 若不传入, 则返回所有授权 seller_id 下的移除货件数据
        - 报告为 seller_id 维度, 若按 sid 请求则返回对应 seller_id 下所有移除货件数据
        - 同一个 seller_id 授权的店铺任取一个 sid 请求报告数据即可

        :param start_date `<'str/date/datetime'>`: 查询开始日期
        :param end_date `<'str/date/datetime'>`: 查询结束日期
        :param sid `<'int/None'>`: 领星店铺ID, 默认 `None`
        :param seller_id `<'str/None'>`: 亚马逊卖家ID, 默认 `None`
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 1000)
        :returns `<'FbaRemovalShipments'>`: 返回查询到的亚马逊FBA移除货件结果
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
            data: [
                {
                    # 领星站点ID
                    "mid": 1,
                    # 领星店铺ID
                    "sid": 1,
                    # 站点国家 (中文) [原字段 'marketplace']
                    "country": "美国",
                    # 亚马逊卖家ID
                    "seller_id": "AVI**********",
                    # 领星店铺帐号名称
                    "seller_account_name": "Store-NA",
                    # 店铺信息列表 [原字段 'seller_name']
                    "sellers": [
                        {
                            # 领星站点ID
                            "mid": 1,
                            # 领星店铺ID
                            "sid": 1,
                            # 领星店铺名称 [原字段 'name']
                            "seller_name": "Store-NA-US",
                            # 站点国家 (中文) [原字段 'marketplace']
                            "country": "美国"
                        },
                        ...
                    ],
                    # 移除业务标识 (唯一移除货件行) [原字段 'uuid_new']
                    "uuid": "a644f4d*************************",
                    # 移除业务标识序号 [原字段 'uuid_num_new']
                    "uuid_seq": 1,
                    # 移除货件ID [原字段 'order_id']
                    "removal_shipment_id": "nIU*******",
                    # 移除货件类型 [原字段 'removal_order_type']
                    "removal_shipment_type": "Return",
                    # 亚马逊SKU [原字段 'sku']
                    "msku": "SKU*********",
                    # 亚马逊FNSKU
                    "fnsku": "X00*******",
                    # 商品信息列表 [原字段 'local_info']
                    "products": [
                        {
                            # 领星本地SKU [原字段 'local_sku']
                            "lsku": "LOCAL********",
                            # 领星产品名称 [原字段 'local_name']
                            "product_name": "JBL",
                        },
                        ...
                    ],
                    # 库存处置结果
                    "disposition": "Unsellable",
                    # 已发货商品数量 [原字段 'shipped_quantity']
                    "shipped_qty": 1,
                    # 货件成运商
                    "carrier": "UPS_GR_PL",
                    # 货件追踪单号
                    "tracking_number": "1ZA8**************",
                    # 移除货件的仓库入库单号 [原字段 'overseas_removal_order_no']
                    "warehouse_inbound_number": "OWR25**********",
                    # 移除货件收货地址 [原字段 'delivery_info']
                    "ship_to_address": {
                        # 国家代码 [原字段 'ship_country']
                        "country_code": "US",
                        # 州/省 [原字段 'ship_state']
                        "state": "AZ",
                        # 城市 [原字段 'ship_city']
                        "city": "Tucson",
                        # 县/郡
                        "county": "",
                        # 区/镇
                        "district": "",
                        # 详细地址
                        "address": "Y10062,85756,7480 E Sycamore Park Blvd,Tucson,AZ,US 美国",
                        # 地址行1
                        "address_line1": "7480 E Sycamore Park Blvd",
                        # 地址行2
                        "address_line2": "",
                        # 地址行3
                        "address_line3": "",
                        # 邮编 [原字段 'ship_postal_code']
                        "postcode": "85756",
                        # 收件人名称
                        "name": "Y10062",
                        # 收件人电话
                        "phone": "",
                    },
                    # 移除请求时间 [原字段 'request_date']
                    "request_time": "2025-07-08T07:36:15-07:00",
                    # 移除发货时间 [原字段 'shipment_date']
                    "shipment_time": "2025-08-06T09:27:38-07:00",
                    # 移除发货时间 (时间戳) [原字段 'shipment_date_timestamp']
                    "shipment_time_ts": 1754497658,
                },
                ...
            ],
        }
        ```
        """
        url = route.FBA_REMOVAL_SHIPMENTS
        # 解析并验证参数
        args = {
            "start_date": start_date,
            "end_date": end_date,
            "sid": sid,
            "seller_id": seller_id,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.FbaRemovalShipments.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.FbaRemovalShipments.model_validate(data)

    async def FbaInventory(
        self,
        sid: int,
        *,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.FbaInventory:
        """查询亚马逊FBA库存源数据

        ## Docs
        - 亚马逊源表数据: [查询亚马逊源报表-FBA库存](https://apidoc.lingxing.com/#/docs/SourceData/ManageInventory)
        - 对应亚马逊 'FBA Manage Inventory' 源报告

        :param sid `<'int'>`: 领星店铺ID
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 1000)
        :returns `<'FbaInventory'>`: 返回查询到的亚马逊FBA库存结果
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
            data: [
                {
                    # 商品ASIN
                    "asin": "B0D*******",
                    # 亚马逊SKU [原字段 'sku']
                    "msku": "SKU*********",
                    # 亚马逊FNSKU
                    "fnsku": "X00*******",
                    # 商品标题 [原字段 'product_name']
                    "title": "Product Title",
                    # 商品状态
                    "condition": "New",
                    # 商品单位标准价格 [原字段 'your_price']
                    "standard_price": 39.99,
                    # 商品单位到手价格
                    "landed_price": 39.99,
                    # 商品单位体积 [原字段 'per_unit_volume']
                    "item_volume": 0.02,
                    # 商品单位采购成本 [原字段 'cg_price']
                    "cost_of_goods": 0.0,
                    # 是否是FBM配送 (Yes, No)
                    "mfn_listing_exists": "No",
                    # FBM可售库存数量 [原字段 'mfn_fulfillable_quantity']
                    "mfn_fulfillable_qty": 0,
                    # 是否是FBA配送 (Yes, No)
                    "afn_listing_exists": "Yes",
                    # FBA在库库存数量 [原字段 'afn_warehouse_quantity']
                    # (afn_fulfillable_qty + afn_unsellable_qty + afn_reserved_qty)
                    "afn_warehouse": 1602,
                    # FBA可售库存数量 [原字段 'afn_fulfillable_quantity']
                    "afn_fulfillable_qty": 1598,
                    # FBA不可售库存数量 [原字段 'afn_unsellable_quantity']
                    "afn_unsellable_qty": 0,
                    # FBA预留库存数量 [原字段 'afn_reserved_quantity']
                    "afn_reserved_qty": 2,
                    # FBA总库存数量 [原字段 'afn_total_quantity']
                    # (afn_warehouse_qty + afn_inbound_working&shipped&receiving_qty)
                    "afn_total_qty": 1602,
                    # FBA 发货计划入库的库存数量 [原字段 'afn_inbound_working_quantity']
                    "afn_inbound_working_qty": 0,
                    # FBA 发货在途的库存数量 [原字段 'afn_inbound_shipped_quantity']
                    "afn_inbound_shipped_qty": 0,
                    # FBA 发货入库接收中的库存数量 [原字段 'afn_inbound_receiving_quantity']
                    "afn_inbound_receiving_qty": 0,
                    # 库存更新时间 (北京时间) [原字段 'gmt_modified']
                    "update_time": "2025-09-03 03:17:48",
                },
                ...
            ],
        }
        ```
        """
        url = route.FBA_INVENTORY
        # 解析并验证参数
        args = {
            "sid": sid,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.Seller.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.FbaInventory.model_validate(data)

    async def FbaReservedInventory(
        self,
        sid: int,
        *,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.FbaReservedInventory:
        """查询亚马逊FBA预留库存源数据

        ## Docs
        - 亚马逊源表数据: [查询亚马逊源报表-预留库存](https://apidoc.lingxing.com/#/docs/SourceData/ReservedInventory)
        - 对应亚马逊 'FBA Reserved Inventory Report' 源报告

        :param sid `<'int'>`: 领星店铺ID
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 1000)
        :returns `<'FbaReservedInventory'>`: 返回查询到的亚马逊FBA可售库存结果
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
            data: [
                {
                    # 商品ASIN
                    "asin": "B0D*******",
                    # 亚马逊SKU [原字段 'sku']
                    "msku": "SKU*********",
                    # 亚马逊FNSKU
                    "fnsku": "X00*******",
                    # 商品标题 [原字段 'product_name']
                    "title": "Product Title",
                    # FBA 预留库存总数量 [原字段 'reserved_qty']
                    # (afn_reserved_fc_processing&fc_transfer_qty&customer_order_qty)
                    "afn_reserved_qty": 1184,
                    # FBA 在库待调仓的库存数量 [原字段 'reserved_fc_processing']
                    "afn_reserved_fc_processing_qty": 1020,
                    # FBA 在库调仓中的库存数量 [原字段 'reserved_fc_transfers']
                    "afn_reserved_fc_transfers_qty": 37,
                    # FBA 在库待发货的库存数量 [原字段 'reserved_customerorders']
                    "afn_reserved_customer_order_qty": 127,
                    # 库存更新时间 (北京时间) [原字段 'gmt_modified']
                    "update_time": "2025-09-03 06:22:12",
                },
                ...
            ],
        }
        ```
        """
        url = route.FBA_RESERVED_INVENTORY
        # 解析并验证参数
        args = {
            "sid": sid,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.Seller.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.FbaReservedInventory.model_validate(data)

    async def FbaInventoryHealth(
        self,
        sid: int,
        *,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.FbaInventoryHealth:
        """查询亚马逊FBA库存健康源数据

        ## Docs
        - 亚马逊源表数据: [查询亚马逊源报表—库龄表](https://apidoc.lingxing.com/#/docs/SourceData/getFbaAgeList)
        - 对应亚马逊 'Manage Inventory Health' 源报告

        :param sid `<'int'>`: 领星店铺ID
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 1000)
        :returns `<'FbaInventoryHealth'>`: 返回查询到的亚马逊FBA库健康结果
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
            data: [
                {
                    # 领星店铺ID
                    "sid": 1,
                    # 站点国家 [原字段 'marketplace']
                    "country": "US",
                    # 商品ASIN
                    "asin": "B0F*******",
                    # 亚马逊SKU [原字段 'sku']
                    "msku": "SKU*********",
                    # 亚马逊FNSKU
                    "fnsku": "X00*******",
                    # 商品标题 [原字段 'product_name']
                    "title": "Product Title",
                    # 商品状态
                    "condition": "New",
                    # 商品类目 [原字段 'product_group']
                    "category": "gl_office_product",
                    # 商品类目排名 [原字段 'sales_rank']
                    "category_rank": 10659,
                    # 商品仓储类型
                    "storage_type": "Other",
                    # 商品总仓储使用量 (排除待移除商品仓储使用量)
                    "storage_volume": 27.058595,
                    # 商品单位体积
                    "item_volume": 0.026245,
                    # 体积单位 [原字段 'volume_unit_measurement']
                    "volume_unit": "cubic feet",
                    # 可售库存数量 [原字段 'available']
                    "afn_fulfillable_qty": 1031,
                    # 待移除库存数量 [原字段 'pending_removal_quantity']
                    "afn_pending_removal_qty": 0,
                    # FBA 总发货库存数量 [原字段 'inbound_quantity']
                    # (inbound_working + inbound_shipped + inbound_received)
                    "afn_inbound_total_qty": 0,
                    # FBA 发货计划入库的库存数量 [原字段 'inbound_working']
                    "afn_inbound_working_qty": 0,
                    # FBA 发货在途的库存数量 [原字段 'inbound_shipped']
                    "afn_inbound_shipped_qty": 0,
                    # FBA 发货入库接收中的库存数量 [原字段 'inbound_received']
                    "afn_inbound_receiving_qty": 0,
                    # 库龄0-30天的库存数量 [原字段 'inv_age_0_to_30_days']
                    "age_0_to_30_days_qty": 0,
                    # 库龄31-60天的库存数量 [原字段 'inv_age_31_to_60_days']
                    "age_31_to_60_days_qty": 2,
                    # 库龄61-90天的库存数量 [原字段 'inv_age_61_to_90_days']
                    "age_61_to_90_days_qty": 1,
                    # 库龄0-90天的库存数量 [原字段 'inv_age_0_to_90_days']
                    "age_0_to_90_days_qty": 3,
                    # 库龄91-180天的库存数量 [原字段 'inv_age_91_to_180_days']
                    "age_91_to_180_days_qty": 1109,
                    # 库龄181-270天的库存数量 [原字段 'inv_age_181_to_270_days']
                    "age_181_to_270_days_qty": 0,
                    # 库龄181-330天的库存数量 [原字段 'inv_age_181_to_330_days']
                    "age_181_to_330_days_qty": 0,
                    # 库龄271-330天的库存数量 [原字段 'inv_age_271_to_330_days_quantity']
                    "age_271_to_330_days_qty": 0,
                    # 库龄271-365天的库存数量 [原字段 'inv_age_271_to_365_days']
                    "age_271_to_365_days_qty": 0,
                    # 库龄331-365天的库存数量 [原字段 'inv_age_331_to_365_days']
                    "age_331_to_365_days_qty": 0,
                    # 库龄365天以上的库存数量 [原字段 'inv_age_365_plus_days']
                    "age_365_plus_days_qty": 0,
                    # 库龄180天以上收取长期仓储费的库存数量 [原字段 'qty_to_be_charged_ltsf_6_mo']
                    "ltsf_180_plus_days_qty": 0,
                    # 库龄180天以上预估收取长期仓储费的金额 [原字段 'projected_ltsf_6_mo']
                    "estimated_ltsf_180_plus_fee": 0.0,
                    # 库龄365天以上收取长期仓储费的库存数量 [原字段 'qty_to_be_charged_ltsf_12_mo']
                    "ltsf_365_plus_days_qty": 0,
                    # 库龄365天以上预估收取长期仓储费的金额 [原字段 'projected_ltsf_12_mo']
                    "estimated_ltsf_365_plus_fee": 0.0,
                    # 预估截至下一收费日期 (每月15日) 长期仓储费金额 [原字段 'estimated_ltsf_next_charge']
                    "estimated_ltsf_next_charge_fee": 0.0,
                    # 是否免除低库存费 (Yes, No) [原字段 'exempted_from_low_inventory_level_fee']
                    "is_lilf_exempted": "Yes",
                    # 当前周是否收取低库存费 (Yes, No) [原字段 'low_Inventory_Level_fee_applied_in_current_week']
                    "is_lilf_applied_in_current_week": "No",
                    # 是否免除低库存成本覆盖费 (Yes, No) [原字段 'exempted_from_low_inventory_cost_coverage_fee']
                    "is_licc_exempted": "Yes",
                    # 当前周是否收取低库存成本覆盖费 (Yes, No) [原字段 'low_inventory_cost_coverage_fee_applied_in_current_week']
                    "is_licc_applied_in_current_week": "No",
                    # 预估往后30天内的仓储费金额 (月度仓储 + 长期仓储 + 低库存 + 库存成本覆盖) [原字段 'estimated_storage_cost_next_month']
                    "estimated_30_days_storage_fee": 20.4,
                    # 货币代码 [原字段 'currency']
                    "currency_code": "USD",
                    # 商品标准价 (不包含促销, 运费, 积分) [原字段 'your_price']
                    "standard_price": 39.89,
                    # 商品优惠价 [原字段 'sales_price']
                    "sale_price": 0.0,
                    # 商品促销价 [原字段 'featuredoffer_price']
                    "offer_price": 39.89,
                    # 商品最低价 (含运费) [原字段 'lowest_price_new_plus_shipping']
                    "lowest_price": 35.9,
                    # 商品最低二手价 (含运费) [原字段 'lowest_price_used']
                    "lowest_used_price": 0.0,
                    # 最近7天发货销售额 [原字段 'sales_shipped_last_7_days']
                    "shipped_7d_amt": 9796.72,
                    # 最近30天发货销售额 [原字段 'sales_shipped_last_30_days']
                    "shipped_30d_amt": 16675.3,
                    # 最近60天发货销售额 [原字段 'sales_shipped_last_60_days']
                    "shipped_60d_amt": 25892.12,
                    # 最近90天发货销售额 [原字段 'sales_shipped_last_90_days']
                    "shipped_90d_amt": 30838.75,
                    # 最近7天发货数量 [原字段 'units_shipped_t7']
                    "shipped_7d_qty": 272,
                    # 最近30天发货数量 [原字段 'units_shipped_t30']
                    "shipped_30d_qty": 454,
                    # 最近60天发货数量 [原字段 'units_shipped_t60']
                    "shipped_60d_qty": 690,
                    # 最近90天发货数量 [原字段 'units_shipped_t90']
                    "shipped_90d_qty": 816,
                    # 库存售出率 (过去 90 天销量除以平均可售库存) [原字段 'sell_through']
                    "sell_through_rate": 0.49,
                    # 历史连续至少6个月无销售库存 [原字段 'no_sale_last_6_months']
                    "historical_no_sale_6m": 0,
                    # 历史供货天数 (取短期&长期更大值)
                    "historical_days_of_supply": 195.7,
                    # 历史短期供货天数 [原字段 'short_term_historical_days_of_supply']
                    "historical_st_days_of_supply": 108.0,
                    # 历史长期供货天数 [原字段 'long_term_historical_days_of_supply']
                    "historical_lt_days_of_supply": 195.7,
                    # 预估可供货天数 [原字段 'days_of_supply']
                    "estimated_days_of_supply": 175,
                    # 基于过去30天数据预估可供货周数 [原字段 'weeks_of_cover_t30']
                    "estimated_weeks_of_cover_30d": 9,
                    # 基于过去90天数据预估可供货周数 [原字段 'weeks_of_cover_t90']
                    "estimated_weeks_of_cover_90d": 16,
                    # 预估冗余库存数量 [原字段 'estimated_excess_quantity']
                    "estimated_excess": 0,
                    # 库存健康状态 [原字段 'fba_inventory_level_health_status']
                    "inventory_health_status": "Healthy",
                    # 库存预警信息 [原字段 'alert']
                    "inventory_alert": "Low traffic",
                    # 推荐安全库存水平 [原字段 'healthy_inventory_level']
                    "recommended_healthy_qty": 0,
                    # 推荐最低库存水平 [原字段 'fba_minimum_inventory_level']
                    "recommended_minimum_qty": 372,
                    # 推荐移除库存数量 [原字段 'recommended_removal_quantity']
                    "recommended_removal_qty": 0,
                    # 推荐促销价格
                    "recommended_sales_price": 0.0,
                    # 推荐促销天数 [原字段 'recommended_sale_duration_days']
                    "recommended_sales_days": 0,
                    # 推荐操作
                    "recommended_action": "NoRestockExcessActionRequired",
                    # 预计推荐操作节省仓储费用 [原字段 'estimated_cost_savings_of_recommended_actions']
                    "estimated_savings_of_recommended_actions": 0.0,
                    # 数据日期 [原字段 'snapshot_date']
                    "report_date": "2025-09-02",
                },
                ...
            ],
        }
        ```
        """
        url = route.FBA_INVENTORY_HEALTH
        # 解析并验证参数
        args = {
            "sid": sid,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.Seller.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.FbaInventoryHealth.model_validate(data)

    async def FbaInventoryAdjustments(
        self,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        *,
        sids: int | list[int] | None = None,
        search_field: SEARCH_FIELD | None = None,
        search_value: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.FbaInventoryAdjustments:
        """查询亚马逊FBA库存调整源数据

        ## Docs
        - 亚马逊源表数据: [查询亚马逊源报表-盘存记录](https://apidoc.lingxing.com/#/docs/SourceData/AdjustmentList)

        :param start_date `<'str/date/datetime'>`: 查询开始日期
        :param end_date `<'str/date/datetime'>`: 查询结束日期
        :param sids `<'int/list[int]/None'>`: 领星店铺ID或ID列表, 默认 `None` (所有店铺)
        :param search_field `<'str/None'>`: 搜索字段, 默认 `None` (不搜索), 可选值:

            - `'asin'`: 按 ASIN 搜索
            - `'msku'`: 按亚马逊 SKU 搜索
            - `'fnsku'`: 按亚马逊 FNSKU 搜索
            - `'title'`: 按商品标题搜索
            - `'transaction_item_id'`: 按调整交易ID搜索

        :param search_value `<'str/None'>`: 搜索值, 默认 `None` (search_field 有值时必填)
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值 10000, 默认 `None` (使用: 20)
        :returns `<'FbaInventoryAdjustments'>`: 返回查询到的亚马逊FBA库存调整结果
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
            data: []
        }
        ```
        """
        url = route.FBA_INVENTORY_ADJUSTMENTS
        # 解析并验证参数
        args = {
            "start_date": start_date,
            "end_date": end_date,
            "sids": sids,
            "search_field": search_field,
            "search_value": search_value,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.FbaInventoryAdjustments.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.FbaInventoryAdjustments.model_validate(data)

    # 报告导出 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    async def ExportReportTask(
        self,
        seller_id: str,
        marketplace_ids: str | list[str],
        region: REPORT_REGION,
        report_type: str,
        start_time: str | datetime.date | datetime.datetime | None = None,
        end_time: str | datetime.date | datetime.datetime | None = None,
    ) -> schema.ExportReportTask:
        """创建报告导出任务

        ## Docs
        - 亚马逊源表数据: [报告导出 - 创建导出任务](https://apidoc.lingxing.com/#/docs/Statistics/reportCreateReportExportTask)

        :param seller_id `<'str'>`: 亚马逊卖家ID, 参数来源: `Seller.seller_id`
        :param marketplace_ids `<'str/list[str]'>`: 亚马逊站点ID或ID列表, 参数来源: `Seller.marketplace_id`
        :param region `<'str'>`: 亚马逊站点区域, 参数来源: `Seller.region`, 可选值:

            - `'NA'`: 北美站点
            - `'EU'`: 欧洲站点
            - `'FE'`: 远东站点

        :param report_type `<'str'>`: 报告类型, 可选值请参考亚马逊官方: [Report Type Values](https://apidoc.lingxing.com/#/docs/Statistics/reportTypeList)
        :param start_time `<'str/date/datetime/None'>`: 报告数据开始时间, 默认 `None`
        :param end_time `<'str/date/datetime/None'>`: 报告数据结束时间, 默认 `None`
        :returns `<'ExportReportTask'>`: 返回创建的报告导出任务结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "2273ee319fe84b539b6269bb664c22fb.208.17569687977541427",
            # 响应时间
            "response_time": "2025-09-04 14:53:17",
            # 响应数据量
            "response_count": 1,
            # 总数据量
            "total_count": 1,
            # 响应数据
            "data": {
                # 报告导出任务ID
                "task_id": "620358fe-ca1e-4241-b2ef-c3f1e3aae5e6"
            },
        }
        ```
        """
        url = route.EXPORT_REPORT_TASK
        # 解析并验证参数
        args = {
            "seller_id": seller_id,
            "marketplace_ids": marketplace_ids,
            "region": region,
            "report_type": report_type,
            "start_time": start_time,
            "end_time": end_time,
        }
        try:
            p = param.ExportReportTask.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.ExportReportTask.model_validate(data)

    async def ExportReportResult(
        self,
        seller_id: str,
        task_id: str,
        region: REPORT_REGION,
    ) -> schema.ExportReportResult:
        """查询报告导出结果

        ## Docs
        - 亚马逊源表数据: [报告导出-查询导出任务结果](https://apidoc.lingxing.com/#/docs/Statistics/reportQueryReportExportTask)

        :param seller_id `<'str'>`: 亚马逊卖家ID, 参数来源: `Seller.seller_id`
        :param task_id `<'str'>`: 报告导出任务ID, 参数来源: `ExportReportTask.task_id`
        :param region `<'str'>`: 亚马逊站点区域, 参数来源: `Seller.region`, 可选值:

            - `'NA'`: 北美站点
            - `'EU'`: 欧洲站点
            - `'FE'`: 远东站点

        :returns `<'ExportReportResult'>`: 返回查询的报告导出结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "2273ee319fe84b539b6269bb664c22fb.208.17569687977541427",
            # 响应时间
            "response_time": "2025-09-04 14:53:17",
            # 响应数据量
            "response_count": 1,
            # 总数据量
            "total_count": 1,
            # 响应数据
            "data": {
                # 报告文件ID
                "report_document_id": "",
                # 报告生成进度状态
                "progress_status": "",
                # 报告压缩算法
                "compression_algorithm": "",
                # 报告下载链接
                "url": "",
            },
        }
        ```
        """
        url = route.EXPORT_REPORT_RESULT
        # 解析并验证参数
        args = {
            "seller_id": seller_id,
            "task_id": task_id,
            "region": region,
        }
        try:
            p = param.ExportReportResult.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.ExportReportResult.model_validate(data)

    async def ExportReportRefresh(
        self,
        seller_id: str,
        report_document_id: str,
        region: REPORT_REGION,
    ) -> schema.ExportReportRefresh:
        """报告导出结果续期

        ## Docs
        - 亚马逊源表数据: [报告导出 - 报告下载链接续期](https://apidoc.lingxing.com/#/docs/Statistics/AmazonReportExportTask)

        :param seller_id `<'str'>`: 亚马逊卖家ID, 参数来源: `Seller.seller_id`
        :param report_document_id `<'str'>`: 报告文件ID, 参数来源: `ExportReportResult.report_document_id`
        :param region `<'str'>`: 亚马逊站点区域, 参数来源: `Seller.region`, 可选值:

            - `'NA'`: 北美站点
            - `'EU'`: 欧洲站点
            - `'FE'`: 远东站点

        :returns `<'ExportReportRefresh'>`: 返回报告下载链接续期结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "success",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "2273ee319fe84b539b6269bb664c22fb.208.17569687977541427",
            # 响应时间
            "response_time": "2025-09-04 14:53:17",
            # 响应数据量
            "response_count": 1,
            # 总数据量
            "total_count": 1,
            # 响应数据
            "data": {
                # 报告文件ID
                "report_document_id": ""
                # 报告下载链接
                "url": "",
            },
        }
        ```
        """
        url = route.EXPORT_REPORT_REFRESH
        # 解析并验证参数
        args = {
            "seller_id": seller_id,
            "report_document_id": report_document_id,
            "region": region,
        }
        try:
            p = param.ExportReportRefresh.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.ExportReportRefresh.model_validate(data)
