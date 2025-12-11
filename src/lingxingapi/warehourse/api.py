# -*- coding: utf-8 -*-c
import datetime
from typing import Literal
from lingxingapi import errors
from lingxingapi.base.api import BaseAPI
from lingxingapi.warehourse import param, route, schema

# Type Aliases ---------------------------------------------------------------------------------------------------------
INVENTORY_SEARCH_FIELD = Literal[
    "msku",
    "lsku",
    "fnsku",
    "product_name",
    "asin",
    "parent_asin",
    "spu",
    "spu_name",
]
SELLER_INVENTORY_SEARCH_FIELD = Literal[
    "msku",
    "lsku",
    "fnsku",
    "product_name",
    "transaction_number",
    "batch_number",
    "source_batch_number",
    "purchase_plan_number",
    "purchase_number",
    "receiving_number",
]


# API ------------------------------------------------------------------------------------------------------------------
class WarehouseAPI(BaseAPI):
    """领星API `仓库数据` 接口

    ## Notice
    请勿直接实例化此类
    """

    # 公共 API --------------------------------------------------------------------------------------
    # . 仓库 - 仓库设置
    async def Warehouses(
        self,
        *,
        warehouse_type: int | None = None,
        overseas_warehouse_type: int | None = None,
        deleted: int | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.Warehouses:
        """查询仓库

        ## Docs
        - 仓库 - 仓库设置: [查询仓库列表](https://apidoc.lingxing.com/#/docs/Warehouse/WarehouseLists)

        :param warehouse_type `<'int/None'>`: 仓库类型 (1: 本地仓, 3: 海外仓, 4: 亚马逊平台仓, 6: AWD仓),
            默认 `None` (查询`1: 本地仓`)
        :param overseas_warehouse_type `<'int/None'>`: 海外仓库类型 (1: 无API海外仓, 2: 有API海外仓),
            此参数只在`warehouse_type=3`时生效, 默认 `None` (查询所有海外仓)
        :param deleted `<'int/None'>`: 是否已删除 (0: 未删除, 1: 已删除),
            默认 `None` (查询`0: 未删除`)
        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 默认 `None` (使用: 1000)
        :returns `<'Warehouses'>`: 返回查询到的仓库数据
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
                    # 仓库ID [原字段 'wid']
                    "warehouse_id": 1****,
                    # 仓库类型 [原字段 'type']
                    # (1: 本地仓, 3: 海外仓, 4: 亚马逊平台仓, 6: AWD仓)
                    "warehouse_type": 3,
                    # 仓库名称 [原字段 'name']
                    "warehouse_name": "测试海外仓",
                    # 仓库国家代码 [原字段 'country_code']
                    "warehouse_country_code": "DE",
                    # 仓库服务商ID (仅仓库类型为3时有值) [原字段 'wp_id']
                    "provider_id": 267,
                    # 仓库服务商名称 (仅仓库类型为3时有值) [原字段 'wp_name']
                    "provider_name": "测试服务商",
                    # 第三方仓库名称 [原字段 't_warehouse_name']
                    "third_party_warehouse_name": "DE Warehouse",
                    # 第三方仓库代码 [原字段 't_warehouse_code']
                    "third_party_warehouse_code": "DE0001",
                    # 第三方仓库所在地理位置 [原字段 't_country_area_name']
                    "thrid_party_warehouse_location": "德国",
                    # 第三方仓库状态 (1: 启用, 0: 停用) [原字段 't_status']
                    "thrid_party_warehouse_status": 1,
                    # 是否已删除 (0: 否, 1: 是) [原字段 'is_delete']
                    "deleted": 0,
                },
                ...
            ],
        }
        ```
        """
        url = route.WAREHOUSES
        # 解析并验证参数
        args = {
            "warehouse_type": warehouse_type,
            "overseas_warehouse_type": overseas_warehouse_type,
            "deleted": deleted,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.Warehouses.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.Warehouses.model_validate(data)

    async def WarehouseBins(
        self,
        *,
        warehouse_ids: int | list[int] | None = None,
        bin_ids: int | list[int] | None = None,
        bin_status: int | None = None,
        bin_type: int | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.WarehouseBins:
        """查询仓库货架(仓位)

        ## Docs
        - 仓库 - 仓库设置: [查询本地仓位列表](https://apidoc.lingxing.com/#/docs/Warehouse/warehouseBin)

        :param warehouse_ids `<'int/list[int]/None'>`: 仓库IDs,
            默认 `None` (查询所有仓库)
        :param bin_ids `<'int/list[int]/None'>`: 仓库货架(仓位)IDs,
            默认 `None` (查询所有仓库货架)
        :param bin_status `<'int/None'>`: 仓库货架(仓位)状态 (1: 启用, 0: 停用),
            默认 `None` (查询所有状态)
        :param bin_type `<'int/None'>`: 仓库货架(仓位)类型 (5: 可用, 6: 次品),
            默认 `None` (查询所有类型)
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 20)
        :returns `<'WarehouseBins'>`: 返回查询到的仓库货架(仓位)数据
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
                    # 仓库ID [原字段 'wid']
                    "warehouse_id": 1,
                    # 仓库名称 [原字段 'Ware_house_name']
                    "warehouse_name": "测试仓库",
                    # 仓库货架(仓位)ID [原字段 'id']
                    "bin_id": 1,
                    # 仓库货架(仓位)名称 [原字段 'storage_bin']
                    "bin_name": "A-1-3",
                    # 仓库货架(仓位)类型 (5: 可用, 6: 次品) [原字段 'type']
                    "bin_type": 5,
                    # 仓库货架(仓位)状态 (0: 停用, 1: 启用) [原字段 'status']
                    "bin_status": 1,
                    # 仓库货架(仓位)货物列表 [原字段 'sku_fnsku']
                    "skus": [
                        {
                            # 领星店铺ID [原字段 'store_id']
                            "sid": "1",
                            # 领星店铺名称
                            "seller_name": "测试卖家",
                            # 领星本地商品SKU [原字段 'sku']
                            "lsku": "SKU*******",
                            # 商品FNSKU
                            "fnsku": "X0********",
                            # 领星商品ID
                            "product_id": 1****,
                            # 领星商品名称
                            "product_name": "P********",
                        },
                        ...
                    ],
                },
                ...
            ],
        }
        ```
        """
        url = route.WAREHOUSE_BINS
        # 解析并验证参数
        args = {
            "warehouse_ids": warehouse_ids,
            "bin_ids": bin_ids,
            "bin_status": bin_status,
            "bin_type": bin_type,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.WarehouseBins.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.WarehouseBins.model_validate(data)

    # . 仓库 - 库存&流水
    async def FbaInventory(
        self,
        sids: int | list[int],
        *,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.FbaInventory:
        """查询FBA库存

        ## Docs
        - 仓库 - 库存&流水: [查询FBA库存列表](https://apidoc.lingxing.com/#/docs/Warehouse/FBAStock)

        :param sids `<'int/list[int]'>`: 领星店铺ID
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 15)
        :returns `<'FbaInventory'>`: 返回查询到的FBA库存数据
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
                    # 仓库名称 [原字段 'wname']
                    "warehouse_name": "EU欧洲仓",
                    # 领星店铺ID [sid + msku 唯一键]
                    "sid": 1,
                    # 商品ASIN
                    "asin": "B0********",
                    # 亚马逊SKU
                    "msku": "SKU********",
                    # 领星本地SKU [原字段 'sku']
                    "lsku": "LOCAL*******",
                    # 亚马逊FNSKU
                    "fnsku": "X00*******",
                    # 领星商品名称
                    "product_name": "P********",
                    # 商品类型ID
                    "category_id": 0,
                    # 商品类型名称
                    "category_name": "",
                    # 商品品牌ID
                    "brand_id": 0,
                    # 商品品牌名称
                    "brand_name": "",
                    # 商品图片链接 [原字段 'product_image']
                    "image_url": "https://m.media-amazon.com/****.jpg",
                    # 商品配送方式 (如: "FBA" 或 "FBM") [原字段 'fulfillment_channel_name']
                    "fulfillment_channel": "FBA",
                    # 库存共享类型 [原字段 'share_type']
                    # (0: 库存不共享, 1: 库存北美共享, 2: 库存欧洲共享)
                    "stock_share_type": 2,
                    # FBA 多国店铺本地可售库存信息列表 [原字段 'afn_fulfillable_quantity_multi']
                    "afn_fulfillable_local": [
                        {
                            # 店铺名称 [原字段 'name']
                            "seller_name": "EU-FR",
                            # 店铺本地可售数量 [原字段 'quantity_for_local_fulfillment']
                            "afn_fulfillable_local": 447
                        },
                        ...
                    ],
                    # FBA 总可售库存数量 [原字段 'total_fulfillable_quantity']
                    # afn_fulfillable + afn_reserved_fc_processing + afn_reserved_fc_transfers
                    "afn_fulfillable_total": 447,
                    # FBA 可售库存数量 [原字段 'afn_fulfillable_quantity']
                    "afn_fulfillable": 443,
                    # FBA 在库待调仓的库存数量 [原字段 'reserved_fc_processing']
                    "afn_reserved_fc_processing": 4,
                    # FBA 在库调仓中的库存数量 [原字段 'reserved_fc_transfers']
                    "afn_reserved_fc_transfers": 0,
                    # FBA 在库待发货的库存数量 [原字段 'reserved_customerorders']
                    "afn_reserved_customer_order": 0,
                    # FBA 在库不可售的库存数量 [原字段 'afn_unsellable_quantity']
                    "afn_unsellable": 0,
                    # FBA 实际发货在途的数量 [原字段 'afn_erp_real_shipped_quantity']
                    "afn_actual_shipped": 0,
                    # FBA 发货在途的库存数量 [原字段 'afn_inbound_shipped_quantity']
                    "afn_inbound_shipped": 0,
                    # FBA 发货计划入库的库存数量 [原字段 'afn_inbound_working_quantity']
                    "afn_inbound_working": 0,
                    # FBA 发货入库接收中的库存数量 [原字段 'afn_inbound_receiving_quantity']
                    "afn_inbound_receiving": 0,
                    # FBA 调查中的库存数量 [原字段 'afn_researching_quantity']
                    "afn_researching": 0,
                    # 库龄0-30天的库存数量 [原字段 'inv_age_0_to_30_days']
                    "age_0_to_30_days": 1,
                    # 库龄31-60天的库存数量 [原字段 'inv_age_31_to_60_days']
                    "age_31_to_60_days": 448,
                    # 库龄61-90天的库存数量 [原字段 'inv_age_61_to_90_days']
                    "age_61_to_90_days": 0,
                    # 库龄0-90天的库存数量 [原字段 'inv_age_0_to_90_days']
                    "age_0_to_90_days": 449,
                    # 库龄91-180天的库存数量 [原字段 'inv_age_91_to_180_days']
                    "age_91_to_180_days": 0,
                    # 库龄181-270天的库存数量 [原字段 'inv_age_181_to_270_days']
                    "age_181_to_270_days": 0,
                    # 库龄271-330天的库存数量 [原字段 'inv_age_271_to_330_days']
                    "age_271_to_330_days": 0,
                    # 库龄271-365天的库存数量 [原字段 'inv_age_271_to_365_days']
                    "age_271_to_365_days": 0,
                    # 库龄331-365天的库存数量 [原字段 'inv_age_331_to_365_days']
                    "age_331_to_365_days": 0,
                    # 库龄365天以上的库存数量 [原字段 'inv_age_365_plus_days']
                    "age_365_plus_days": 0,
                    # 库存售出率 (过去 90 天销量除以平均可售库存) [原字段 'sell_through']
                    "sell_through_rate": 1.57,
                    # 历史供货天数 (取短期&长期更大值)
                    "historical_days_of_supply": 491.3,
                    # 历史短期供货天数 [原字段 'short_term_historical_days_of_supply']
                    "historical_st_days_of_supply": 281.3,
                    # 历史长期供货天数 [原字段 'long_term_historical_days_of_supply']
                    "historical_lt_days_of_supply": 491.3,
                    # 库存成本金额 [原字段 'cost']
                    "inventory_cost_amt": 0.0,
                    # 库存货值金额 [原字段 'stock_cost_total']
                    "inventory_value_amt": 0.0,
                    # 亚马逊预测的库存健康状态 [原字段 'fba_inventory_level_health_status']
                    "inventory_health_status": "",
                    # 亚马逊低库存水平费收费情况 [原字段 'low_inventory_level_fee_applied']
                    "inventory_low_level_fee_status": "豁免收取",
                    # 亚马逊预测的从今天起30天内产生的仓储费 [原字段 'estimated_storage_cost_next_month']
                    "estimated_30d_storage_fee": 2.11,
                    # 亚马逊预估的冗余商品数量 [原字段 'estimated_excess_quantity']
                    "estimated_excess_qty": 0.0,
                    # 亚马逊建议的最低库存量 [原字段 'fba_minimum_inventory_level']
                    "recommended_minimum_qty": 58.0,
                    # 亚马逊建议的操作 [原字段 'recommended_action']
                    "recommended_action": "No Excess Inventory",
                },
                ...
            ]
        }
        ```
        """
        url = route.FBA_INVENTORY
        # 解析并验证参数
        args = {
            "sids": sids,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.FbaInventory.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.FbaInventory.model_validate(data)

    async def FbaInventoryDetails(
        self,
        *,
        search_field: INVENTORY_SEARCH_FIELD | None = None,
        search_value: str | None = None,
        category_ids: int | list[int] | None = None,
        brand_ids: int | list[int] | None = None,
        operator_ids: int | list[int] | None = None,
        attr_value_id: int | None = None,
        fulfillment_channel: Literal["FBA", "FBM"] | None = None,
        status: int | None = None,
        exclude_zero_stock: int | None = None,
        exclude_deleted: int | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.FbaInventoryDetails:
        """查询FBA库存详情

        ## Docs
        - 仓库 - 库存&流水: [查询FBA库存列表-v2](https://apidoc.lingxing.com/#/docs/Warehouse/FBAStockDetail)

        :param search_field `<'str/None'>`: 搜索字段, 默认 `None` (不搜索), 可选值:

            - `"msku"` (亚马逊SKU)
            - `"lsku"` (领星本地SKU)
            - `"fnsku"` (亚马逊FNSKU)
            - `"product_name"` (领星商品名称)
            - `"asin"` (商品ASIN)
            - `"parent_asin"` (商品父ASIN)
            - `"spu"` (领星SPU编码)
            - `"spu_name"` (领星SPU名称)

        :param search_value `<'str/None'>`: 搜索内容, 需搭配`search_field`一起使用, 默认 `None` (不搜索)
        :param category_ids `<'int/list[int]/None'>`: 产品分类ID或ID列表, 默认 `None` (不筛选)
        :param brand_ids `<'int/list[int]/None'>`: 产品品牌ID或ID列表, 默认 `None` (不筛选)
        :param operator_ids `<'int/list[int]/None'>`: 产品负责人ID或ID列表, 默认 `None` (不筛选)
        :param attr_value_id `<'int/None'>`: 多属性SPU产品属性值ID, 默认 `None` (不筛选)
        :param fulfillment_channel `<'str/None'>`: 产品配送方式 ("FBA", "FBM"), 默认 `None` (不筛选), 可选值:
        :param status `<'int/None'>`: 产品状态 (0: 停售, 1: 在售), 默认 `None` (不筛选)
        :param exclude_zero_stock `<'int/None'>`: 是否去除零库存 (0: 保留, 1: 去除), 默认 `None` (使用0)
        :param exclude_deleted `<'int/None'>`: 是否去除已删除产品 (0: 保留, 1: 去除), 默认 `None` (使用0)
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值200, 默认 `None` (使用: 20)
        :returns `<'FbaInventoryDetails'>`: 返回查询到的FBA库存详情数据
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
                    # 仓库名称 [原字段 'name']
                    "warehouse_name": "EU欧洲仓",
                    # 领星店铺ID (共享库存时为0)
                    "sid": 0,
                    # 商品ASIN
                    "asin": "B0********",
                    # 亚马逊SKU [原字段 'seller_sku']
                    "msku": "SKU********",
                    # 领星本地SKU [原字段 'sku']
                    "lsku": "LOCAL*******",
                    # 亚马逊FNSKU
                    "fnsku": "X000*******",
                    # 领星商品名称
                    "product_name": "P********",
                    # 商品类型ID [原字段 'cid']
                    "category_id": 0,
                    # 商品类型名称 [原字段 'category_text']
                    "category_name": "",
                    # 商品品牌ID [原字段 'bid']
                    "brand_id": 0,
                    # 商品品牌名称 [原字段 'product_brand_text']
                    "brand_name": "",
                    # 商品略缩图链接 [原字段 'small_image_url']
                    "thumbnail_url": "https://image.distributetop.com/****.jpg",
                    # 商品配送方式
                    "fulfillment_channel": "AMAZON_EU",
                    # 库存共享类型 [原字段 'share_type']
                    # (0: 库存不共享, 1: 库存北美共享, 2: 库存欧洲共享)
                    "stock_share_type": 2,
                    # 库存总数量 [原字段 'total']
                    "stock_total": 472,
                    # 库存总货值金额 [原字段 'total_price']
                    "stock_total_amt": 30977.36,
                    # 库存总可售数量 [原字段 'available_total']
                    "stock_total_fulfillable": 472,
                    # 库存总可售货值金额 [原字段 'available_total_price']
                    "stock_total_fulfillable_amt": 30977.36,
                    # FBA 多国店铺本地可售库存信息列表 [原字段 'fba_storage_quantity_list']
                    "afn_fulfillable_local": [
                        {
                            # 领星店铺ID
                            "sid": 1,
                            # 店铺名称 [原字段 'name']
                            "seller_name": "DE-Store",
                            # 店铺本地可售数量 [原字段 'quantity_for_local_fulfillment']
                            "afn_fulfillable_local": 75
                        },
                        ...
                    ],
                    # afn_fulfillable + afn_reserved_fc_processing + afn_reserved_fc_transfers
                    # FBA 总可售库存数量 [原字段 'total_fulfillable_quantity']
                    "afn_fulfillable_total": 462,
                    # FBA 可售库存数量 [原字段 'afn_fulfillable_quantity']
                    "afn_fulfillable": 161,
                    # FBA 可售库存货值金额 [原字段 'afn_fulfillable_quantity_price']
                    "afn_fulfillable_amt": 10566.43,
                    # FBA 在库待调仓的库存数量 [原字段 'reserved_fc_processing']
                    "afn_reserved_fc_processing": 1,
                    # FBA 在库待调仓的库存货值金额 [原字段 'reserved_fc_processing_price']
                    "afn_reserved_fc_processing_amt": 65.63,
                    # FBA 在库调仓中的库存数量 [原字段 'reserved_fc_transfers']
                    "afn_reserved_fc_transfers": 300,
                    # FBA 在库调仓中的库存货值金额 [原字段 'reserved_fc_transfers_price']
                    "afn_reserved_fc_transfers_amt": 19689.0,
                    # FBA 在库待发货的库存数量 [原字段 'reserved_customerorders']
                    "afn_reserved_customer_order": 10,
                    # FBA 在库待发货的库存货值金额 [原字段 'reserved_customerorders_price']
                    "afn_reserved_customer_order_amt": 656.3,
                    # FBA 在库不可售的库存数量 [原字段 'afn_unsellable_quantity']
                    "afn_unsellable": 2,
                    # FBA 在库不可售的库存货值金额 [原字段 'afn_unsellable_quantity_price']
                    "afn_unsellable_amt": 131.26,
                    # FBA 实际发货在途的数量 [原字段 'stock_up_num']
                    "afn_actual_shipped": 0,
                    # FBA 实际发货在途的货值金额 [原字段 'stock_up_num_price']
                    "afn_actual_shipped_amt": 0.0,
                    # FBA 发货在途的库存数量 [原字段 'afn_inbound_shipped_quantity']
                    "afn_inbound_shipped": 0,
                    # FBA 发货在途的库存货值金额 [原字段 'afn_inbound_shipped_quantity_price']
                    "afn_inbound_shipped_amt": 0.0,
                    # FBA 发货计划入库的库存数量 [原字段 'afn_inbound_working_quantity']
                    "afn_inbound_working": 0,
                    # FBA 发货计划入库的库存货值金额 [原字段 'afn_inbound_working_quantity_price']
                    "afn_inbound_working_amt": 0.0,
                    # FBA 发货入库接收中的库存数量 [原字段 'afn_inbound_receiving_quantity']
                    "afn_inbound_receiving": 0,
                    # FBA 发货入库接收中的库存货值金额 [原字段 'afn_inbound_receiving_quantity_price']
                    "afn_inbound_receiving_amt": 0.0,
                    # FBA 调查中的库存数量 [原字段 'afn_researching_quantity']
                    "afn_researching": 2,
                    # FBA 调查中的库存货值金额 [原字段 'afn_researching_quantity_price']
                    "afn_researching_amt": 131.26,
                    # FBM 可售库存数量 [原字段 'quantity']
                    "mfn_fulfillable": 0,
                    # FBM 可售库存货值金额 [原字段 'quantity_price']
                    "mfn_fulfillable_amt": 0.0,
                    # 库龄0-30天的库存数量 [原字段 'inv_age_0_to_30_days']
                    "age_0_to_30_days": 7,
                    # 库龄0-30天的库存货值金额 [原字段 'inv_age_0_to_30_price']
                    "age_0_to_30_days_amt": 459.41,
                    # 库龄31-60天的库存数量 [原字段 'inv_age_31_to_60_days']
                    "age_31_to_60_days": 280,
                    # 库龄31-60天的库存货值金额 [原字段 'inv_age_31_to_60_price']
                    "age_31_to_60_days_amt": 18376.4,
                    # 库龄61-90天的库存数量 [原字段 'inv_age_61_to_90_days']
                    "age_61_to_90_days": 0,
                    # 库龄61-90天的库存货值金额 [原字段 'inv_age_61_to_90_price']
                    "age_61_to_90_days_amt": 0.0,
                    # 库龄0-90天的库存数量 [原字段 'inv_age_0_to_90_days']
                    "age_0_to_90_days": 287,
                    # 库龄0-90天的库存货值金额 [原字段 'inv_age_0_to_90_price']
                    "age_0_to_90_days_amt": 18835.81,
                    # 库龄91-180天的库存数量 [原字段 'inv_age_91_to_180_days']
                    "age_91_to_180_days": 0,
                    # 库龄91-180天的库存货值金额 [原字段 'inv_age_91_to_180_price']
                    "age_91_to_180_days_amt": 0.0,
                    # 库龄181-270天的库存数量 [原字段 'inv_age_181_to_270_days']
                    "age_181_to_270_days": 0,
                    # 库龄181-270天的库存货值金额 [原字段 'inv_age_181_to_270_price']
                    "age_181_to_270_days_amt": 0.0,
                    # 库龄271-330天的库存数量 [原字段 'inv_age_271_to_330_days']
                    "age_271_to_330_days": 0,
                    # 库龄271-330天的库存货值金额 [原字段 'inv_age_271_to_330_price']
                    "age_271_to_330_days_amt": 0.0,
                    # 库龄271-365天的库存数量 [原字段 'inv_age_271_to_365_days']
                    "age_271_to_365_days": 0,
                    # 库龄271-365天的库存货值金额 [原字段 'inv_age_271_to_365_price']
                    "age_271_to_365_days_amt": 0.0,
                    # 库龄331-365天的库存数量 [原字段 'inv_age_331_to_365_days']
                    "age_331_to_365_days": 0,
                    # 库龄331-365天的库存货值金额 [原字段 'inv_age_331_to_365_price']
                    "age_331_to_365_days_amt": 0.0,
                    # 库龄365天以上的库存数量 [原字段 'inv_age_365_plus_days']
                    "age_365_plus_days": 0,
                    # 库龄365天以上的库存货值金额 [原字段 'inv_age_365_plus_price']
                    "age_365_plus_days_amt": 0.0,
                    # 库存售出率 (过去 90 天销量除以平均可售库存) [原字段 'sell_through']
                    "sell_through_rate": 1.31,
                    # 历史供货天数 (取短期&长期更大值)
                    "historical_days_of_supply": 56.1,
                    # 历史供货天数货值金额 [原字段 'historical_days_of_supply_price']
                    "historical_days_of_supply_amt": "56.10",
                    # 亚马逊预测的库存健康状态 [原字段 'fba_inventory_level_health_status']
                    "inventory_health_status": "",
                    # 亚马逊低库存水平费收费情况 [原字段 'low_inventory_level_fee_applied']
                    "inventory_low_level_fee_status": "本周未收",
                    # 亚马逊预测的从今天起30天内产生的仓储费 [原字段 'estimated_storage_cost_next_month']
                    "estimated_30d_storage_fee": 0.0,
                    # 亚马逊预估的冗余商品数量 [原字段 'estimated_excess_quantity']
                    "estimated_excess_qty": 0.0,
                    # 亚马逊建议的最低库存量 [原字段 'fba_minimum_inventory_level']
                    "recommended_minimum_qty": 258.0,
                    # 亚马逊建议的操作 [原字段 'recommended_action']
                    "recommended_action": "Go to Restock",
                },
                ...
            ],
        }
        ```
        """
        url = route.FBA_INVENTORY_DETAILS
        # 解析并验证参数
        args = {
            "search_field": search_field,
            "search_value": search_value,
            "category_ids": category_ids,
            "brand_ids": brand_ids,
            "attr_value_id": attr_value_id,
            "operator_ids": operator_ids,
            "fulfillment_channel": fulfillment_channel,
            "status": status,
            "exclude_zero_stock": exclude_zero_stock,
            "exclude_deleted": exclude_deleted,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.FbaInventoryDetails.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.FbaInventoryDetails.model_validate(data)

    async def AwdInventory(
        self,
        *,
        search_field: INVENTORY_SEARCH_FIELD | None = None,
        search_value: str | None = None,
        warehouse_ids: int | list[int] | None = None,
        category_ids: int | list[int] | None = None,
        brand_ids: int | list[int] | None = None,
        operator_ids: int | list[int] | None = None,
        attr_value_id: int | None = None,
        status: int | None = None,
        exclude_zero_stock: int | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.AwdInventory:
        """查询AWD库存

        ## Docs
        - 仓库 - 库存&流水: [查询AWD库存列表](https://apidoc.lingxing.com/#/docs/Warehouse/AwdWarehouseDetail)

        :param search_field `<'str/None'>`: 搜索字段, 默认 `None` (不搜索), 可选值:

            - `"msku"` (亚马逊SKU)
            - `"lsku"` (领星本地SKU)
            - `"fnsku"` (亚马逊FNSKU)
            - `"product_name"` (领星商品名称)
            - `"asin"` (商品ASIN)
            - `"parent_asin"` (商品父ASIN)
            - `"spu"` (领星SPU编码)
            - `"spu_name"` (领星SPU名称)

        :param search_value `<'str/None'>`: 搜索内容, 需搭配`search_field`一起使用, 默认 `None` (不搜索)
        :param warehouse_ids `<'int/list[int]/None'>`: 仓库ID或ID列表, 默认 `None` (不筛选)
        :param category_ids `<'int/list[int]/None'>`: 产品分类ID或ID列表, 默认 `None` (不筛选)
        :param brand_ids `<'int/list[int]/None'>`: 产品品牌ID或ID列表, 默认 `None` (不筛选)
        :param operator_ids `<'int/list[int]/None'>`: 产品负责人ID或ID列表, 默认 `None` (不筛选)
        :param attr_value_id `<'int/None'>`: 多属性SPU产品属性值ID, 默认 `None` (不筛选)
        :param status `<'int/None'>`: 产品状态 (0: 停售, 1: 在售), 默认 `None` (不筛选)
        :param exclude_zero_stock `<'int/None'>`: 是否去除零库存 (0: 保留, 1: 去除), 默认 `None` (使用0)
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值200, 默认 `None` (使用: 20)
        :returns `<'AwdInventory'>`: 返回查询到的AWD库存数据
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
                    # 仓库名称 [原字段 'wname']
                    "warehouse_name": "US美国仓(AWD)",
                    # 领星站点ID
                    "mid": 1,
                    # 国家 [原字段 'nation']
                    "country": "美国",
                    # 领星店铺ID
                    "sid": 50,
                    # 领星店铺名称
                    "seller_name": "韧啸-US",
                    # 商品父ASIN
                    "parent_asin": "B0CPT1TVV7",
                    # 商品ASIN
                    "asin": "B0CPT1TVV7",
                    # 商品ASIN链接
                    "asin_url": "https://www.amazon.com/dp/B0CPT1TVV7",
                    # 亚马逊SKU [原字段 'seller_sku']
                    "msku": "HM300-BLACK",
                    # 领星本地SKU [原字段 'sku']
                    "lsku": "",
                    # 亚马逊FNSKU
                    "fnsku": "",
                    # 多属性SPU产品编码
                    "spu": "",
                    # 多属性SPU产品名称
                    "spu_name": "",
                    # 领星产品ID
                    "product_id": 0,
                    # 领星商品名称
                    "product_name": "",
                    # 商品类型ID [原字段 'cid']
                    "category_id": 0,
                    # 商品类型名称 [原字段 'category_text']
                    "category_name": "",
                    # 商品类型1级名称
                    "category_level1": "",
                    # 商品类型2级名称
                    "category_level2": "",
                    # 商品类型3级名称
                    "category_level3": "",
                    # 商品类型列表 [原字段 'category_Arr']
                    "categories": [],
                    # 商品品牌ID [原字段 'bid']
                    "brand_id": 0,
                    # 商品品牌名称 [原字段 'product_brand_text']
                    "brand_name": "",
                    # 产品图片链接 [原字段 'pic_url']
                    "image_url": "",
                    # 产品略缩图链接 [原字段 'small_image_url']
                    "thumbnail_url": "https://m.media-amazon.com/images/I/41yXqZiD0JL._SL75_.jpg",
                    # 产品负责人列表 [原字段 'asin_principal_list']
                    "operators": [],
                    # 商品属性列表 [原字段 'attribute']
                    "attributes": [],
                    # AWD 总库存数量 [原字段 'total_onhand_quantity']
                    "awd_total": 24,
                    # AWD 总库存货值金额 [原字段 'total_onhand_quantity_price']
                    "awd_total_amt": 0.0,
                    # AWD 可分发库存数量 [原字段 'available_distributable_quantity']
                    "awd_distributable": 14,
                    # AWD 可分发库存货值金额 [原字段 'available_distributable_quantity_price']
                    "awd_distributable_amt": 0.0,
                    # AWD 在途分发至FBA数量 [原字段 'awd_to_fba_quantity_shipped']
                    "awd_distributing": 0,
                    # AWD 在途分发至FBA货值金额 [原字段 'awd_to_fba_quantity_shipped_price']
                    "awd_distributing_amt": 0.0,
                    # AWD 在库待分发数量 [原字段 'reserved_distributable_quantity']
                    "awd_reserved_distributes": 10,
                    # AWD 在库待分发货值金额 [原字段 'reserved_distributable_quantity_price']
                    "awd_reserved_distributes_amt": 0.0,
                    # AWD 实际发货在途的数量 [原字段 'awd_actual_quantity_shipped']
                    "awd_actual_shipped": 0,
                    # AWD 实际发货在途的货值金额 [原字段 'awd_actual_quantity_shipped_price']
                    "awd_actual_shipped_amt": 0.0,
                    # AWD 发货在途的库存数量 [原字段 'awd_quantity_shipped']
                    "awd_inbound_shipped": 0,
                    # AWD 发货在途的库存货值金额 [原字段 'awd_quantity_shipped_price']
                    "awd_inbound_shipped_amt": 0.0,
                },
                ...
            ]
        }
        ```
        """
        urls = route.AWD_INVENTORY
        # 解析并验证参数
        args = {
            "search_field": search_field,
            "search_value": search_value,
            "warehouse_ids": warehouse_ids,
            "category_ids": category_ids,
            "brand_ids": brand_ids,
            "operator_ids": operator_ids,
            "attr_value_id": attr_value_id,
            "status": status,
            "exclude_zero_stock": exclude_zero_stock,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.AwdInventory.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, urls, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", urls, body=p.model_dump_params())
        return schema.AwdInventory.model_validate(data)

    async def SellerInventory(
        self,
        *,
        warehouse_ids: int | list[int] | None = None,
        lsku: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SellerInventory:
        """卖家(本地/海外)仓库库存产品信息

        ## Docs
        - 仓库 - 库存&流水: [查询仓库库存明细](https://apidoc.lingxing.com/#/docs/Warehouse/InventoryDetails)

        :param warehouse_ids `<'int/list[int]/None'>`: 仓库ID或ID列表, 默认 `None` (不筛选)
        :param lsku `<'str/None'>`: 领星本地SKU, 默认 `None` (不筛选)
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值800, 默认 `None` (使用: 20)
        :returns `<'SellerInventory'>`: 返回查询到的卖家仓库库存产品信息数据
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
                    # 仓库ID [原字段 'wid']
                    "warehouse_id": 1***,
                    # 领星店铺ID [原字段 'seller_id']
                    "sid": 1,
                    # 领星本地商品SKU [原字段 'sku']
                    "lsku": "LOCAL*******",
                    # 亚马逊FNSKU
                    "fnsku": "X00*******",
                    # 产品总库存数量 [原字段 'product_total']
                    # 领星商品ID
                    "product_id": 2*****,
                    "total_qty": 0,
                    # 产品库存可售数量 [原字段 'product_valid_num']
                    "fulfillable_qty": 0,
                    # 产品库存可售预留数量 [原字段 'good_lock_num']
                    "fulfillable_reserved_qty": 0,
                    # 产品库存次品数量 [原字段 'product_bad_num']
                    "unsellable_qty": 0,
                    # 产品库存不可售预留数量 [原字段 'bad_lock_num']
                    "unsellable_reserved_qty": 0,
                    # 产品库存加工计划单品的预留数量 [原字段 'product_lock_num']
                    "process_reserved_qty": 0,
                    # 产品库存待质检数量 [原字段 'product_qc_num']
                    "pending_qc_qty": 0,
                    # 产品待到货数量 [原字段 'quantity_receive']
                    "pending_arrival_qty": 100,
                    # 产品调拨在途数量 [原字段 'product_onway']
                    "transit_qty": 0,
                    # 产品调拨在途头程成本 [原字段 'transit_head_cost']
                    "transit_first_leg_fee": 0.0,
                    # 外箱可售数量 [原字段 'available_inventory_box_qty']
                    "box_fulfillable_qty": 0,
                    # 第三方海外仓库存信息 [原字段 'third_inventory']
                    "overseas_inventory": {
                        # 产品可售库存数量 [原字段 'qty_sellable']
                        "fulfillable_qty": 0,
                        # 产品待上架库存数量 [原字段 'qty_pending']
                        "pending_qty": 0,
                        # 产品预留库存数量 [原字段 'qty_reserved']
                        "reserved_qty": 0,
                        # 产品调拨在途数量 [原字段 'qty_onway']
                        "transit_qty": 0,
                        # 外箱可售数量 [原字段 'box_qty_sellable']
                        "box_fulfillable_qty": 0,
                        # 外箱待上架数量 [原字段 'box_qty_pending']
                        "box_pending_qty": 0,
                        # 外箱预留数量 [原字段 'box_qty_reserved']
                        "box_reserved_qty": 0,
                        # 外箱调拨在途数量 [原字段 'box_qty_onway']
                        "box_transit_qty": 0,
                    },
                    # 库存单价成本 [原字段 'stock_cost']
                    "stock_item_cost_amt": 0.0,
                    # 库存总成本金额 [原字段 'stock_cost_total']
                    "stock_total_cost_amt": 0.0,
                    # 平均库龄 [原字段 'average_age']
                    "age_avg_days": 0,
                    # 库龄列表 [原字段 'stock_age_list']
                    "ages": [
                        {
                            # 库龄信息 [原字段 'name']
                            "age": "0-15天库龄",
                            # 库龄数量
                            "qty": 0
                        },
                        ...,
                    ],
                },
                ...
            ],
        }
        ```
        """
        url = route.SELLER_INVENTORY
        # 解析并验证参数
        args = {
            "warehouse_ids": warehouse_ids,
            "lsku": lsku,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.SellerInventory.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SellerInventory.model_validate(data)

    async def SellerInventoryBins(
        self,
        *,
        warehouse_ids: int | list[int] | None = None,
        bin_types: int | list[int] | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SellerInventoryBins:
        """查询卖家(本地/海外)仓库库存货架(仓位)信息

        ## Docs
        - 仓库 - 库存&流水: [查询仓位库存明细](https://apidoc.lingxing.com/#/docs/Warehouse/inventoryBinDetails)

        :param warehouse_ids `<'int/list[int]/None'>`: 仓库ID或ID列表, 默认 `None` (不筛选)
        :param bin_types `<'int/list[int]/None'>`: 仓位类型ID或ID列表, 默认 `None` (不筛选), 可选值:

            - `1`: 待检暂存
            - `2`: 可用暂存
            - `3`: 次品暂存
            - `4`: 拣货暂存
            - `5`: 可用
            - `6`: 次品

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值500, 默认 `None` (使用: 20)
        :returns `<'SellerInventoryBin'>`: 返回查询到的卖家仓库库存货架信息数据
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
                    # 仓库ID [原字段 'wid']
                    "warehouse_id": 1****,
                    # 仓库名称 [原字段 'wh_name']
                    "warehouse_name": "US Warehouse",
                    # 仓库货架ID [原字段 'whb_id']
                    "bin_id": 4****,
                    # 仓库货架名称 [原字段 'whb_name']
                    "bin_name": "可用暂存",
                    # 仓库货架类型 [原字段 'whb_type']
                    "bin_type": 2,
                    # 仓库货架类型描述 [原字段 'whb_type_name']
                    "bin_type_desc": "可用暂存",
                    # 领星店铺ID [原字段 'store_id']
                    "sid": 0,
                    # 亚马逊SKU
                    "msku": "",
                    # 领星本地商品SKU [原字段 'sku']
                    "lsku": "P*******",
                    # 亚马逊FNSKU
                    "fnsku": "",
                    # 领星商品ID
                    "product_id": 237229,
                    # 领星商品名称
                    "product_name": "LOCAL*******",
                    # 产品总库存数量 [原字段 'total']
                    "total_qty": 0,
                    # 产品库存可售数量 [原字段 'validNum']
                    "fulfillable_qty": 0,
                    # 产品库存预留数量 [原字段 'lockNum']
                    "reserved_qty": 0,
                    # 第三方海外仓库存信息 [原字段 'third_inventory']
                    "overseas_inventory": {
                        # 产品可售库存数量 [原字段 'qty_sellable']
                        "fulfillable_qty": 0,
                        # 产品待上架库存数量 [原字段 'qty_pending']
                        "pending_qty": 0,
                        # 产品预留库存数量 [原字段 'qty_reserved']
                        "reserved_qty": 0,
                        # 产品调拨在途数量 [原字段 'qty_onway']
                        "transit_qty": 0,
                        # 外箱可售数量 [原字段 'box_qty_sellable']
                        "box_fulfillable_qty": 0,
                        # 外箱待上架数量 [原字段 'box_qty_pending']
                        "box_pending_qty": 0,
                        # 外箱预留数量 [原字段 'box_qty_reserved']
                        "box_reserved_qty": 0,
                        # 外箱调拨在途数量 [原字段 'box_qty_onway']
                        "box_transit_qty": 0,
                    },
                },
                ...
            ],
        }
        ```
        """
        url = route.SELLER_INVENTORY_BINS
        # 解析并验证参数
        args = {
            "warehouse_ids": warehouse_ids,
            "bin_types": bin_types,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.SellerInventoryBins.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SellerInventoryBins.model_validate(data)

    async def SellerInventoryBatches(
        self,
        *,
        search_field: SELLER_INVENTORY_SEARCH_FIELD | None = None,
        search_value: str | None = None,
        warehouse_ids: int | list[int] | None = None,
        transaction_types: int | list[int] | None = None,
        exclude_zero_stock: int | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SellerInventoryBatches:
        """查询卖家(本地/海外)仓库出入库批次明细

        ## Docs
        - 仓库 - 库存&流水: [查询批次明细](https://apidoc.lingxing.com/#/docs/Warehouse/GetBatchDetailList)

        :param search_field `<'str/None'>`: 搜索字段, 默认 `None` (不搜索), 可选值:

            - `"sku"` (亚马逊SKU)
            - `"lsku"` (领星本地SKU)
            - `"fnsku"` (亚马逊FNSKU)
            - `"product_name"` (领星商品名称)
            - `"transaction_number"` (出入库单号)
            - `"batch_number"` (批次号)
            - `"source_batch_number"` (源头批次号)
            - `"purchase_plan_number"` (采购计划单号)
            - `"purchase_number"` (采购单号)
            - `"receiving_number"` (收货单号)

        :param search_value `<'str/None'>`: 搜索内容, 需搭配`search_field`一起使用, 默认 `None` (不搜索)
        :param warehouse_ids `<'int/list[int]/None'>`: 仓库ID或ID列表, 默认 `None` (不筛选)
        :param transaction_types `<'int/list[int]/None'>`: 出入库类型ID或ID列表, 默认 `None` (不筛选), 可选值:

            - `16`: 换标入库
            - `17`: 加工入库
            - `18`: 拆分入库
            - `19`: 其他入库
            - `22`: 采购入库
            - `24`: 调拨入库
            - `23`: 委外入库
            - `25`: 盘盈入库
            - `26`: 退货入库
            - `27`: 移除入库
            - `45`: 赠品入库

        :param exclude_zero_stock `<'int/None'>`: 是否去除零库存 (0: 保留, 1: 去除), 默认 `None` (使用0)
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值400, 默认 `None` (使用: 20)
        :returns `<'SellerInventoryBatches'>`: 返回查询到的卖家仓库出入库批次明细数据
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
                    # 仓库ID [原字段 'wid']
                    "warehouse_id": 1****,
                    # 仓库名称 [原字段 'wh_name']
                    "warehouse_name": "默认仓库",
                    # 批次号 [原字段 'batch_no']
                    "batch_number": "24********-1",
                    # 源头批次号 [原字段 'source_batch_no']
                    "source_batch_numbers": [],
                    # 出入库单号 [原字段 'order_sn']
                    "transaction_number": "IB2********",
                    # 出入库类型 [原字段 'type']
                    "transaction_type": 2202,
                    # 出入库类型描述 [原字段 'type_name']
                    "transaction_type_desc": "采购入库",
                    # 领星店铺ID [原字段 'store_id']
                    "sid": 1,
                    # 领星店铺名称 [原字段 'store_name']
                    "seller_name": "NA店铺",
                    # 亚马逊SKU
                    "msku": "SKU********",
                    # 领星本地商品SKU [原字段 'sku']
                    "lsku": "LOCAL********",
                    # 亚马逊FNSKU
                    "fnsku": "X00*******",
                    # 领星商品ID
                    "product_id": 2*****,
                    # 领星商品名称
                    "product_name": "P********",
                    # 批次总数 [原字段 'total']
                    "total_qty": 300,
                    # 批次在库结存 [原字段 'balance_num']
                    "ending_balance_qty": 300,
                    # 批次在途结存 [原字段 'transit_balance_num']
                    "transit_balance_qty": 0,
                    # 批次可售在途 [原字段 'good_transit_num']
                    "transit_fulfillable_qty": 0,
                    # 批次不可售在途 [原字段 'bad_transit_num']
                    "transit_unsellable_qty": 0,
                    # 批次可售数量 [原字段 'good_num']
                    "fulfillable_qty": 300,
                    # 批次不可售数量 [原字段 'bad_num']
                    "unsellable_qty": 0,
                    # 批次待质检数量 [原字段 'qc_num']
                    "pending_qc_qty": 0,
                    # 批次货物成本 [原字段 'stock_cost']
                    "cost_amt": 7635.0,
                    # 批次头程费用 [原字段 'head_stock_cost']
                    "first_leg_fee": 0.0,
                    # 批次出入库费用 [原字段 'fee']
                    "transaction_fee": 0.0,
                    # 批次总货值 [原字段 'amount']
                    "value_amt": 7635.0,
                    # 采购计划单号列表 [原字段 'plan_sn']
                    "purchase_plan_numbers": ["PP2********", "PP2********"],
                    # 采购单号列表 [原字段 'purchase_order_sns']
                    "purchase_order_numbers": ["PO2********"],
                    # 收货单号列表 [原字段 'delivery_order_sns']
                    "delivery_order_numbers": ["CR2********"],
                    # 供应商ID列表
                    "supplier_ids": [6***],
                    # 供应商名称列表
                    "supplier_names": ["中********"],
                    # 批次创建时间 (北京时间)
                    "batch_time": "2024-11-12 14:06",
                    # 采购时间 (北京时间) [原字段 'purchase_in_time']
                    "purchase_time": "2024-11-12 14:06",
                    # 更新时间 (北京时间)
                    "update_time": "2024-11-12 14:06",
                },
                ...
            ],
        }
        ```
        """
        url = route.SELLER_INVENTORY_BATCHES
        # 解析并验证参数
        args = {
            "search_field": search_field,
            "search_value": search_value,
            "warehouse_ids": warehouse_ids,
            "transaction_types": transaction_types,
            "exclude_zero_stock": exclude_zero_stock,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.SellerInventoryBatches.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SellerInventoryBatches.model_validate(data)

    async def SellerInventoryRecords(
        self,
        *,
        search_field: SELLER_INVENTORY_SEARCH_FIELD | None = None,
        search_value: str | None = None,
        warehouse_ids: int | list[int] | None = None,
        transaction_types: int | list[int] | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SellerInventoryRecords:
        """查询卖家(本地/海外)仓库出入库批次流水

        ## Docs
        - 仓库 - 库存&流水: [查询批次流水](https://apidoc.lingxing.com/#/docs/Warehouse/GetBatchStatementList)

        :param search_field `<'str/None'>`: 搜索字段, 默认 `None` (不搜索), 可选值:

            - `"msku"` (亚马逊SKU)
            - `"lsku"` (领星本地SKU)
            - `"fnsku"` (亚马逊FNSKU)
            - `"product_name"` (领星商品名称)
            - `"transaction_number"` (出入库单号)
            - `"batch_number"` (批次号)
            - `"source_batch_number"` (源头批次号)
            - `"purchase_plan_number"` (采购计划单号)
            - `"purchase_number"` (采购单号)
            - `"receiving_number"` (收货单号)

        :param search_value `<'str/None'>`: 搜索内容, 需搭配`search_field`一起使用, 默认 `None` (不搜索)
        :param warehouse_ids `<'int/list[int]/None'>`: 仓库ID或ID列表, 默认 `None` (不筛选)
        :param transaction_types `<'int/list[int]/None'>`: 出入库类型ID或ID列表, 默认 `None` (不筛选), 可选值:

            - `19`: 其他入库
            - `22`: 采购入库
            - `24`: 调拨入库
            - `23`: 委外入库
            - `25`: 盘盈入库
            - `16`: 换标入库
            - `17`: 加工入库
            - `18`: 拆分入库
            - `47`: VC-PO出库
            - `48`: VC-DF出库
            - `42`: 其他出库
            - `41`: 调拨出库
            - `32`: 委外出库
            - `33`: 盘亏出库
            - `34`: 换标出库
            - `35`: 加工出库
            - `36`: 拆分出库
            - `37`: FBA出库
            - `38`: FBM出库
            - `39`: 退货出库
            - `26`: 退货入库
            - `27`: 移除入库
            - `28`: 采购质检
            - `29`: 委外质检
            - `71`: 采购上架
            - `72`: 委外上架
            - `65`: WFS出库
            - `45`: 赠品入库
            - `46`: 赠品质检入库
            - `73`: 赠品上架
            - `201`: 期初成本调整
            - `202`: 尾差成本调整

        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值400, 默认 `None` (使用: 20)
        :returns `<'SellerInventoryRecords'>`: 返回查询到的卖家仓库出入库批次流水数据
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
                    # 仓库ID [原字段 'wid']
                    "warehouse_id": 1****,
                    # 仓库名称 [原字段 'wh_name']
                    "warehouse_name": "DE Warehouse",
                    # 批次流水号 [原字段 'batch_state_id']
                    "batch_record_number": "25********-1",
                    # 批次号 [原字段 'batch_no']
                    "batch_number": "25********-1",
                    # 源头批次号 [原字段 'source_batch_no']
                    "source_batch_numbers": [],
                    # 出入库单号 [原字段 'order_sn']
                    "transaction_number": "WO10****************",
                    # 源头出入库单号列表 [原字段 'source_order_sn']
                    "source_transaction_numbers": [],
                    # 出入库类型 [原字段 'type']
                    "transaction_type": 3801,
                    # 出入库类型描述 [原字段 'type_name']
                    "transaction_type_desc": "FBM出库",
                    # 领星店铺ID [原字段 'store_id']
                    "sid": 0,
                    # 领星店铺名称 [原字段 'store_name']
                    "seller_name": "",
                    # 亚马逊SKU
                    "msku": "",
                    # 领星本地商品SKU [原字段 'sku']
                    "lsku": "LOCAL********",
                    # 亚马逊FNSKU
                    "fnsku": "",
                    # 领星商品ID
                    "product_id": 23****,
                    # 领星商品名称
                    "product_name": "P********",
                    # 批次流水在库结存 [原字段 'balance_num']
                    "ending_balance_qty": 115,
                    # 批次流水在途结存 [原字段 'transit_balance_num']
                    "transit_balance_qty": 0,
                    # 批次流水可售在途 [原字段 'good_transit_num']
                    "transit_fulfillable_qty": 0,
                    # 批次流水不可售在途 [原字段 'bad_transit_num']
                    "transit_unsellable_qty": 0,
                    # 批次流水可售数量 [原字段 'good_num']
                    "fulfillable_qty": -1,
                    # 批次流水不可售数量 [原字段 'bad_num']
                    "unsellable_qty": 0,
                    # 批次流水待质检数量 [原字段 'qc_num']
                    "pending_qc_qty": 0,
                    # 批次流水货物成本 [原字段 'stock_cost']
                    "cost_amt": 99.8,
                    # 批次流水头程费用 [原字段 'head_stock_cost']
                    "first_leg_fee": 0.0,
                    # 批次流水出入库费用 [原字段 'fee']
                    "transaction_fee": 0.0,
                    # 批次流水总货值 [原字段 'amount']
                    "value_amt": 99.8,
                    # 采购计划单号列表 [原字段 'plan_sn']
                    "purchase_plan_numbers": [],
                    # 采购单号列表 [原字段 'purchase_order_sns']
                    "purchase_numbers": [],
                    # 收货单号列表 [原字段 'delivery_order_sns']
                    "receiving_numbers": [],
                    # 供应商ID列表
                    "supplier_ids": [],
                    # 供应商名称列表
                    "supplier_names": [],
                },
                ...
            ],
        }
        ```
        """
        url = route.SELLER_INVENTORY_RECORDS
        # 解析并验证参数
        args = {
            "search_field": search_field,
            "search_value": search_value,
            "warehouse_ids": warehouse_ids,
            "transaction_types": transaction_types,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.SellerInventoryRecords.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SellerInventoryRecords.model_validate(data)

    async def SellerInventoryOperations(
        self,
        *,
        warehouse_ids: int | list[int] | None = None,
        transaction_types: int | list[int] | None = None,
        transaction_sub_types: int | list[int] | None = None,
        start_date: str | datetime.date | datetime.datetime | None = None,
        end_date: str | datetime.date | datetime.datetime | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SellerInventoryOperations:
        """查询卖家(本地/海外)仓库出入库操作流水

        ## Docs
        - 仓库 - 库存&流水: [查询库存流水(新)](https://apidoc.lingxing.com/#/docs/Warehouse/WarehouseStatementNew)

        :param warehouse_ids `<'int/list[int]/None'>`: 仓库ID或ID列表, 默认 `None` (不筛选)
        :param transaction_types `<'int/list[int]/None'>`: 操作类型ID或ID列表, 默认 `None` (不筛选), 可选值:

            - `19`: 其他入库
            - `22`: 采购入库
            - `24`: 调拨入库
            - `23`: 委外入库
            - `25`: 盘盈入库
            - `15`: FBM退货
            - `16`: 换标入库
            - `17`: 加工入库
            - `18`: 拆分入库
            - `26`: 退货入库
            - `27`: 移除入库
            - `28`: 采购质检
            - `29`: 委外质检
            - `71`: 采购上架
            - `72`: 委外上架
            - `42`: 其他出库
            - `41`: 调拨出库
            - `32`: 委外出库
            - `33`: 盘亏出库
            - `34`: 换标出库
            - `35`: 加工出库
            - `36`: 拆分出库
            - `37`: FBA出库
            - `38`: FBM出库
            - `39`: 退货出库
            - `65`: WFS出库
            - `100`: 锁定流水
            - `51`: 销毁出库

        :param transaction_sub_types `<'int/list[int]/None'>`: 操作子类型ID或ID列表, 默认 `None` (不筛选), 可选值:

            - `1901`: 其他入库 手工其他入库
            - `1902`: 其他入库 用户初始化
            - `1903`: 其他入库 系统初始化
            - `2201`: 采购入库 手工采购入库
            - `2202`: 采购入库 采购单创建入库单
            - `2801`: 采购质检 质检
            - `7101`: 采购上架 PDA上架入库
            - `7201`: 委外上架 PDA委外上架
            - `2401`: 调拨入库 调拨单入在途
            - `2402`: 调拨入库 调拨单收货
            - `2403`: 调拨入库 备货单入在途
            - `2404`: 调拨入库 备货单收货
            - `2405`: 调拨入库 备货单入库结束到货
            - `2301`: 委外入库 委外订单完成加工后入库
            - `2901`: 委外质检 委外订单质检
            - `2501`: 盘盈入库 盘点单入库
            - `2502`: 盘盈入库 数量调整单正向
            - `1501`: FBM退货 退货入库
            - `1502`: FBM退货 退货入库质检
            - `1601`: 换标入库 换标调整入库
            - `1701`: 加工入库 加工单入库
            - `1702`: 加工入库 委外订单加工入库
            - `1801`: 拆分入库 拆分单入库
            - `2601`: 自动退货入库
            - `2602`: 手动退货入库
            - `2701`: 移除入库
            - `4201`: 其他出库 手工其他出库
            - `4101`: 调拨出库 调拨单出库
            - `4102`: 调拨出库 备货单出库
            - `3201`: 委外出库 委外订单完成加工后出库
            - `3301`: 盘亏出库 盘点单出库
            - `3302`: 盘亏出库 数量调整单负向
            - `3401`: 换标出库 换标调整出库
            - `3501`: 加工出库 加工单出库
            - `3502`: 加工出库 委外订单加工出库
            - `3601`: 拆分出库 拆分单出库
            - `3701`: FBA出库 发货单出库
            - `3702`: FBA出库 手工FBA出库
            - `3801`: FBM出库 销售出库单
            - `3901`: 退货出库 手工退货出库
            - `3902`: 退货出库 采购单生成的退货出库单
            - `10001`: 库存锁定-出库
            - `10002`: 库存锁定-调拨
            - `10003`: 库存锁定-调整
            - `10004`: 库存锁定-加工
            - `10005`: 库存锁定-加工计划
            - `10006`: 库存锁定-拆分
            - `10007`: 库存锁定-海外备货
            - `10008`: 库存锁定-发货
            - `10009`: 库存锁定-自发货
            - `10010`: 库存锁定-主动释放
            - `10012`: 库存锁定-发货拣货
            - `10013`: 库存锁定-发货计划
            - `10014`: 库存锁定-WFS库存调整
            - `10011`: 仓位转移和一键上架

        :param start_date `<'str/date/datetime/None'>`: 操作开始日期, 默认 `None` (不筛选)
        :param end_date `<'str/date/datetime/None'>`: 操作结束日期, 默认 `None` (不筛选)
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值400, 默认 `None` (使用: 20)
        :returns `<'SellerInventoryOperations'>`: 返回查询到的卖家仓库出入库操作流水数据
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
                    # 仓库ID [原字段 'wid']
                    "warehouse_id": 1****,
                    # 仓库名称 [原字段 'wh_name']
                    "warehouse_name": "DE Warehouse",
                    # 出入库单号 [原字段 'order_sn']
                    "transaction_number": "WO103***************",
                    # 关联出入库单号 [原字段 'ref_order_sn']
                    "ref_transaction_number": "",
                    # 操作ID [原字段 'statement_id']
                    "transaction_id": "4016**************",
                    # 操作类型 [原字段 'type']
                    "transaction_type": 100,
                    # 操作类型描述 [原字段 'type_text']
                    "transaction_type_desc": "库存调整",
                    # 出入库子类型 [原字段 'sub_type']
                    "transaction_sub_type": "10009",
                    # 出入库子类型描述 [原字段 'sub_type_text']
                    "transaction_sub_type_desc": "库存调整-自发货【配货锁库存】",
                    # 操作备注
                    "transaction_note": "自发货配货锁定",
                    # 操作时间 (北京时间) [原字段 'opt_time']
                    "transaction_time": "2025-08-04 17:26",
                    # 操作人ID [原字段 'opt_uid']
                    "operator_id": 10******,
                    # 操作人名称 [原字段 'opt_real_name']
                    "operator_name": "白小白",
                    # 领星店铺ID [原字段 'seller_id']
                    "sid": 0,
                    # 领星本地商品SKU [原字段 'sku']
                    "lsku": "LOCAL********",
                    # 亚马逊FNSKU
                    "fnsku": "",
                    # 领星商品ID
                    "product_id": 23****,
                    # 领星商品名称
                    "product_name": "P********",
                    # 品牌ID [原字段 'bid']
                    "brand_id": 0,
                    # 品牌名称
                    "brand_name": "",
                    # 操作流水总数 [原字段 'product_total']
                    "total_qty": 0,
                    # 在途流水可售数量 [原字段 'good_transit_num']
                    "transit_fulfillable_qty": 0,
                    # 在途流水可售结存数量 [原字段 'good_transit_balance_num']
                    "transit_fulfillable_balance_qty": 0,
                    # 在途流水不可售数量 [原字段 'bad_transit_num']
                    "transit_unsellable_qty": 0,
                    # 在途流水不可售结存数量 [原字段 'bad_transit_balance_num']
                    "transit_unsellable_balance_qty": 0,
                    # 操作流水可售数量 [原字段 'product_good_num']
                    "fulfillable_qty": -1,
                    # 操作流水可售结存数量 [原字段 'good_balance_num']
                    "fulfillable_balance_qty": 149,
                    # 操作流水可售预留数量 [原字段 'product_lock_good_num']
                    "fulfillable_reserved_qty": 1,
                    # 操作流水可售预留结存数量 [原字段 'good_lock_balance_num']
                    "fulfillable_reserved_balance_qty": 3,
                    # 操作流水不可售数量 [原字段 'product_bad_num']
                    "unsellable_qty": 0,
                    # 操作流水不可售结存数量 [原字段 'bad_balance_num']
                    "unsellable_balance_qty": 0,
                    # 操作流水不可售预留数量 [原字段 'product_lock_bad_num']
                    "unsellable_reserved_qty": 0,
                    # 操作流水不可售预留结存数量 [原字段 'bad_lock_balance_num']
                    "unsellable_reserved_balance_qty": 0,
                    # 操作流水待质检数量 [原字段 'product_qc_num']
                    "pending_qc_qty": 0,
                    # 操作流水质检结存数量 [原字段 'qc_balance_num']
                    "qc_balance_qty": 0,
                    # 操作流水单位采购价格 [原字段 'single_cg_price']
                    "item_purchase_price": 0.0,
                    # 操作流水货物成本 [原字段 'stock_cost']
                    "cost_amt": 0.0,
                    # 操作流水单位货物成本 [原字段 'single_stock_price']
                    "item_cost_amt": 0.0,
                    # 操作流水头程费用 [原字段 'head_stock_cost']
                    "first_leg_fee": 0.0,
                    # 操作流水单位头程费用 [原字段 'head_stock_price']
                    "item_first_leg_fee": 0.0,
                    # 操作流水出入库费用 [原字段 'fee_cost']
                    "transaction_fee": 0.0,
                    # 操作流水单位出入库费用 [原字段 'single_fee_cost']
                    "item_transaction_fee": 0.0,
                    # 操作流水总货值 [原字段 'product_amounts']
                    "value_amt": 0.0,
                },
                ...
            ],
        }
        ```
        """
        url = route.SELLER_INVENTORY_OPERATIONS
        # 解析并验证参数
        args = {
            "warehouse_ids": warehouse_ids,
            "transaction_types": transaction_types,
            "transaction_sub_types": transaction_sub_types,
            "start_date": start_date,
            "end_date": end_date,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.SellerInventoryOperations.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SellerInventoryOperations.model_validate(data)

    async def SellerInventoryBinRecords(
        self,
        *,
        warehouse_ids: int | list[int] | None = None,
        transaction_types: int | list[int] | None = None,
        bin_types: int | list[int] | None = None,
        start_date: str | datetime.date | datetime.datetime | None = None,
        end_date: str | datetime.date | datetime.datetime | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SellerInventoryBinRecords:
        """查询卖家(本地/海外)仓库货架(仓位)出入流水

        ## Docs
        - 仓库 - 库存&流水: [查询仓位流水](https://apidoc.lingxing.com/#/docs/Warehouse/wareHouseBinStatement)

        :param warehouse_ids `<'int/list[int]/None'>`: 仓库ID或ID列表, 默认 `None` (不筛选)
        :param transaction_types `<'int/list[int]/None'>`: 出入库类型ID或ID列表, 默认 `None` (不筛选), 可选值:

            - `16`: 换标入库
            - `17`: 加工入库
            - `18`: 拆分入库
            - `19`: 其他入库
            - `22`: 采购入库
            - `23`: 委外入库
            - `24`: 调拨入库
            - `25`: 盘盈入库
            - `26`: 退货入库
            - `27`: 移除入库
            - `28`: 采购质检
            - `29`: 委外质检
            - `32`: 委外出库
            - `33`: 盘亏出库
            - `34`: 换标出库
            - `35`: 加工出库
            - `36`: 拆分出库
            - `37`: FBA出库
            - `38`: FBM出库
            - `39`: 退货出库
            - `41`: 调拨出库
            - `42`: 其他出库
            - `65`: WFS出库
            - `71`: 采购上架
            - `72`: 委外上架
            - `100`: 库存调整
            - `200`: 成本补录
            - `30001`: 已撤销

        :param bin_types `<'int/list[int]/None'>`: 货架(仓位)类型或列表, 默认 `None` (不筛选), 可选值:

            - `1`: 待检暂存
            - `2`: 可用暂存
            - `3`: 次品暂存
            - `4`: 拣货暂存
            - `5`: 可用
            - `6`: 次品

        :param start_date `<'str/date/datetime/None'>`: 操作开始日期, 默认 `None` (不筛选)
        :param end_date `<'str/date/datetime/None'>`: 操作结束日期, 默认 `None` (不筛选)
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值400, 默认 `None` (使用: 20)
        :returns `<'SellerInventoryBinRecords'>`: 返回查询到的卖家仓库货架(仓位)出入流水数据
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
                    # 仓库ID [原字段 'wid']
                    "warehouse_id": 1****,
                    # 仓库名称 [原字段 'wh_name']
                    "warehouse_name": "默认仓库",
                    # 仓库货架ID [原字段 'whb_id']
                    "bin_id": 3****,
                    # 仓库货架名称 [原字段 'whb_name']
                    "bin_name": "可用暂存",
                    # 仓库货架类型描述 [原字段 'whb_type_name']
                    "bin_type_desc": "可用暂存",
                    # 出入库单号 [原字段 'order_sn']
                    "transaction_number": "QC2********",
                    # 出入库类型 [原字段 'type']
                    "transaction_type": 28,
                    # 出入库类型描述 [原字段 'type_text']
                    "transaction_type_desc": "采购质检",
                    # 出入库备注
                    "transaction_note": "采购单号:PO241029001;收货单号:CR241112001",
                    # 出入库时间 (北京时间) [原字段 'opt_time']
                    "transaction_time": "2024-11-12 14:06",
                    # 出入库数量 [原字段 'num']
                    "transaction_qty": 300,
                    # 操作人ID [原字段 'opt_uid']
                    "operator_id": 10******,
                    # 操作人名称 [原字段 'opt_realname']
                    "operator_name": "白小白",
                    # 领星店铺ID [原字段 'seller_id']
                    "sid": 1,
                    # 领星本地商品SKU [原字段 'sku']
                    "lsku": "LOCAL********",
                    # 亚马逊FNSKU
                    "fnsku": "X00*******",
                    # 领星商品ID
                    "product_id": 2*****,
                    # 领星商品名称
                    "product_name": "P********",
                },
                ...
            ],
        }
        ```
        """
        url = route.SELLER_INVENTORY_BIN_RECORDS
        # 解析并验证参数
        args = {
            "warehouse_ids": warehouse_ids,
            "transaction_types": transaction_types,
            "bin_types": bin_types,
            "start_date": start_date,
            "end_date": end_date,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.SellerInventoryBinRecords.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SellerInventoryBinRecords.model_validate(data)
