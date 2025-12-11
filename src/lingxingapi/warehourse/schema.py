# -*- coding: utf-8 -*-
from typing import Any
from pydantic import BaseModel, Field, field_validator
from lingxingapi.base import schema as base_schema
from lingxingapi.base.schema import ResponseV1, FlattenDataList
from lingxingapi.fields import IntOrNone2Zero, FloatOrNone2Zero


# 仓库 - 仓库设置 ----------------------------------------------------------------------------------------------------------------
# . Warehouse
class Warehouse(BaseModel):
    """仓库信息"""

    # 仓库ID [原字段 'wid']
    warehouse_id: int = Field(validation_alias="wid")
    # 仓库类型 [原字段 'type']
    # (1: 本地仓, 3: 海外仓, 4: 亚马逊平台仓, 6: AWD仓)
    warehouse_type: int = Field(validation_alias="type")
    # 仓库名称 [原字段 'name']
    warehouse_name: str = Field(validation_alias="name")
    # 仓库国家代码 [原字段 'country_code']
    warehouse_country_code: str = Field(validation_alias="country_code")
    # 仓库服务商ID (仅仓库类型为3时有值) [原字段 'wp_id']
    provider_id: int = Field(validation_alias="wp_id")
    # 仓库服务商名称 (仅仓库类型为3时有值) [原字段 'wp_name']
    provider_name: str = Field(validation_alias="wp_name")
    # 第三方仓库名称 [原字段 't_warehouse_name']
    third_party_warehouse_name: str = Field(validation_alias="t_warehouse_name")
    # 第三方仓库代码 [原字段 't_warehouse_code']
    third_party_warehouse_code: str = Field(validation_alias="t_warehouse_code")
    # 第三方仓库所在地理位置 [原字段 't_country_area_name']
    thrid_party_warehouse_location: str = Field(validation_alias="t_country_area_name")
    # 第三方仓库状态 (1: 启用, 0: 停用) [原字段 't_status']
    thrid_party_warehouse_status: IntOrNone2Zero = Field(validation_alias="t_status")
    # 是否已删除 (0: 否, 1: 是) [原字段 'is_delete']
    deleted: int = Field(validation_alias="is_delete")


class Warehouses(ResponseV1):
    """仓库信息列表"""

    data: list[Warehouse]


# . Warehouse Bin
class WarehouseBinItem(BaseModel):
    """仓库货架(仓位)货物信息"""

    # 领星店铺ID [原字段 'store_id']
    sid: int = Field(validation_alias="store_id")
    # 领星店铺名称
    seller_name: str
    # 领星本地商品SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 商品FNSKU
    fnsku: str
    # 领星商品ID
    product_id: int
    # 领星商品名称
    product_name: str


class WarehouseBin(BaseModel):
    """仓库货架(仓位)信息"""

    # 仓库ID [原字段 'wid']
    warehouse_id: int = Field(validation_alias="wid")
    # 仓库名称 [原字段 'Ware_house_name']
    warehouse_name: str = Field(validation_alias="Ware_house_name")
    # 仓库货架(仓位)ID [原字段 'id']
    bin_id: int = Field(validation_alias="id")
    # 仓库货架(仓位)名称 [原字段 'storage_bin']
    bin_name: str = Field(validation_alias="storage_bin")
    # 仓库货架(仓位)类型 (5: 可用, 6: 次品) [原字段 'type']
    bin_type: IntOrNone2Zero = Field(validation_alias="type")
    # 仓库货架(仓位)状态 (0: 停用, 1: 启用) [原字段 'status']
    bin_status: IntOrNone2Zero = Field(validation_alias="status")
    # 仓库货架(仓位)货物列表 [原字段 'sku_fnsku']
    skus: list[WarehouseBinItem] = Field(validation_alias="sku_fnsku")


class WarehouseBins(ResponseV1):
    """仓库货架(仓位)货物信息列表"""

    data: list[WarehouseBin]


# 仓库 - 库存&流水 ---------------------------------------------------------------------------------------------------------------
# . FBA Inventory
class FbaInventoryFulfillableLocal(BaseModel):
    """FBA库存多国店铺本地可售库存信息"""

    # fmt: off
    # 店铺名称 [原字段 'name']
    seller_name: str = Field(validation_alias="name")
    # 店铺本地可售数量 [原字段 'quantity_for_local_fulfillment']
    afn_fulfillable_local: int = Field(validation_alias="quantity_for_local_fulfillment")
    # fmt: on


class FbaInventoryItem(BaseModel):
    """FBA库存产品信息"""

    # fmt: off
    # 仓库名称 [原字段 'wname']
    warehouse_name: str = Field(validation_alias="wname")
    # 领星店铺ID [sid + msku 唯一键]
    sid: int
    # 商品ASIN
    asin: str
    # 亚马逊SKU 
    msku: str
    # 领星本地SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 亚马逊FNSKU
    fnsku: str
    # 领星商品名称
    product_name: str
    # 商品类型ID
    category_id: int
    # 商品类型名称
    category_name: str
    # 商品品牌ID
    brand_id: int
    # 商品品牌名称
    brand_name: str
    # 商品图片链接 [原字段 'product_image']
    image_url: str = Field(validation_alias="product_image")
    # 商品配送方式 (如: "FBA" 或 "FBM") [原字段 'fulfillment_channel_name']
    fulfillment_channel: str = Field(validation_alias="fulfillment_channel_name")
    # 库存共享类型 [原字段 'share_type']
    # (0: 库存不共享, 1: 库存北美共享, 2: 库存欧洲共享)
    stock_share_type: int = Field(validation_alias="share_type")
    # FBA 多国店铺本地可售库存信息列表 [原字段 'afn_fulfillable_quantity_multi']
    afn_fulfillable_local: list[FbaInventoryFulfillableLocal] = Field(validation_alias="afn_fulfillable_quantity_multi")
    # FBA 总可售库存数量 [原字段 'total_fulfillable_quantity']
    # afn_fulfillable + afn_reserved_fc_processing + afn_reserved_fc_transfers
    afn_fulfillable_total: int = Field(validation_alias="total_fulfillable_quantity")
    # FBA 可售库存数量 [原字段 'afn_fulfillable_quantity']
    afn_fulfillable: int = Field(validation_alias="afn_fulfillable_quantity")
    # FBA 在库待调仓的库存数量 [原字段 'reserved_fc_processing']
    afn_reserved_fc_processing: int = Field(validation_alias="reserved_fc_processing")
    # FBA 在库调仓中的库存数量 [原字段 'reserved_fc_transfers']
    afn_reserved_fc_transfers: int = Field(validation_alias="reserved_fc_transfers")
    # FBA 在库待发货的库存数量 [原字段 'reserved_customerorders']
    afn_reserved_customer_order: int = Field(validation_alias="reserved_customerorders")
    # FBA 在库不可售的库存数量 [原字段 'afn_unsellable_quantity']
    afn_unsellable: int = Field(validation_alias="afn_unsellable_quantity")
    # FBA 实际发货在途的数量 [原字段 'afn_erp_real_shipped_quantity']
    afn_actual_shipped: int = Field(validation_alias="afn_erp_real_shipped_quantity")
    # FBA 发货在途的库存数量 [原字段 'afn_inbound_shipped_quantity']
    afn_inbound_shipped: int = Field(validation_alias="afn_inbound_shipped_quantity")
    # FBA 发货计划入库的库存数量 [原字段 'afn_inbound_working_quantity']
    afn_inbound_working: int = Field(validation_alias="afn_inbound_working_quantity")
    # FBA 发货入库接收中的库存数量 [原字段 'afn_inbound_receiving_quantity']
    afn_inbound_receiving: int = Field(validation_alias="afn_inbound_receiving_quantity")
    # FBA 调查中的库存数量 [原字段 'afn_researching_quantity']
    afn_researching: int = Field(validation_alias="afn_researching_quantity")
    # 库龄0-30天的库存数量 [原字段 'inv_age_0_to_30_days']
    age_0_to_30_days: int = Field(validation_alias="inv_age_0_to_30_days")
    # 库龄31-60天的库存数量 [原字段 'inv_age_31_to_60_days']
    age_31_to_60_days: int = Field(validation_alias="inv_age_31_to_60_days")
    # 库龄61-90天的库存数量 [原字段 'inv_age_61_to_90_days']
    age_61_to_90_days: int = Field(validation_alias="inv_age_61_to_90_days")
    # 库龄0-90天的库存数量 [原字段 'inv_age_0_to_90_days']
    age_0_to_90_days: int = Field(validation_alias="inv_age_0_to_90_days")
    # 库龄91-180天的库存数量 [原字段 'inv_age_91_to_180_days']
    age_91_to_180_days: int = Field(validation_alias="inv_age_91_to_180_days")
    # 库龄181-270天的库存数量 [原字段 'inv_age_181_to_270_days']
    age_181_to_270_days: int = Field(validation_alias="inv_age_181_to_270_days")
    # 库龄271-330天的库存数量 [原字段 'inv_age_271_to_330_days']
    age_271_to_330_days: int = Field(validation_alias="inv_age_271_to_330_days")
    # 库龄271-365天的库存数量 [原字段 'inv_age_271_to_365_days']
    age_271_to_365_days: int = Field(validation_alias="inv_age_271_to_365_days")
    # 库龄331-365天的库存数量 [原字段 'inv_age_331_to_365_days']
    age_331_to_365_days: int = Field(validation_alias="inv_age_331_to_365_days")
    # 库龄365天以上的库存数量 [原字段 'inv_age_365_plus_days']
    age_365_plus_days: int = Field(validation_alias="inv_age_365_plus_days")
    # 库存售出率 (过去 90 天销量除以平均可售库存) [原字段 'sell_through']
    sell_through_rate: float = Field(validation_alias="sell_through")
    # 历史供货天数 (取短期&长期更大值)
    historical_days_of_supply: float
    # 历史短期供货天数 [原字段 'short_term_historical_days_of_supply']
    historical_st_days_of_supply: float = Field(validation_alias="short_term_historical_days_of_supply")
    # 历史长期供货天数 [原字段 'long_term_historical_days_of_supply']
    historical_lt_days_of_supply: float = Field(validation_alias="long_term_historical_days_of_supply")
    # 库存成本金额 [原字段 'cost']
    inventory_cost_amt: float = Field(validation_alias="cost")
    # 库存货值金额 [原字段 'stock_cost_total']
    inventory_value_amt: float = Field(validation_alias="stock_cost_total")
    # 亚马逊预测的库存健康状态 [原字段 'fba_inventory_level_health_status']
    inventory_health_status: str = Field(validation_alias="fba_inventory_level_health_status")
    # 亚马逊低库存水平费收费情况 [原字段 'low_inventory_level_fee_applied']
    inventory_low_level_fee_status: str = Field(validation_alias="low_inventory_level_fee_applied")
    # 亚马逊预测的从今天起30天内产生的仓储费 [原字段 'estimated_storage_cost_next_month']
    estimated_30d_storage_fee: float = Field(validation_alias="estimated_storage_cost_next_month")
    # 亚马逊预估的冗余商品数量 [原字段 'estimated_excess_quantity']
    estimated_excess_qty: float = Field(validation_alias="estimated_excess_quantity")
    # 亚马逊建议的最低库存量 [原字段 'fba_minimum_inventory_level']
    recommended_minimum_qty: float = Field(validation_alias="fba_minimum_inventory_level")
    # 亚马逊建议的操作 [原字段 'recommended_action']
    recommended_action: str
    # fmt: on


class FbaInventory(ResponseV1, FlattenDataList):
    """FBA库存信息"""

    data: list[FbaInventoryItem]


# . FBA Inventory Detail
class FbaInventoryDetailFulfillableLocal(BaseModel):
    """FBA库存多国店铺本地可售库存信息"""

    # fmt: off
    # 领星店铺ID
    sid: int
    # 店铺名称 [原字段 'name']
    seller_name: str = Field(validation_alias="name")
    # 店铺本地可售数量 [原字段 'quantity_for_local_fulfillment']
    afn_fulfillable_local: int = Field(validation_alias="quantity_for_local_fulfillment")
    # fmt: on


class FbaInventoryDetailItem(BaseModel):

    # fmt: off
    # 仓库名称 [原字段 'name']
    warehouse_name: str = Field(validation_alias="name")
    # 领星店铺ID (共享库存时为0)
    sid: int
    # 商品ASIN
    asin: str
    # 亚马逊SKU [原字段 'seller_sku']
    msku: str = Field(validation_alias="seller_sku")
    # 领星本地SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 亚马逊FNSKU
    fnsku: str
    # 领星商品名称 
    product_name: str
    # 商品类型ID [原字段 'cid']
    category_id: int = Field(validation_alias="cid")
    # 商品类型名称 [原字段 'category_text']
    category_name: str = Field(validation_alias="category_text")
    # 商品品牌ID [原字段 'bid']
    brand_id: int = Field(validation_alias="bid")
    # 商品品牌名称 [原字段 'product_brand_text']
    brand_name: str = Field(validation_alias="product_brand_text")
    # 商品略缩图链接 [原字段 'small_image_url']
    thumbnail_url: str = Field(validation_alias="small_image_url")
    # 商品配送方式 (如: "AMAZON_NA")
    fulfillment_channel: str
    # 库存共享类型 [原字段 'share_type']
    # (0: 库存不共享, 1: 库存北美共享, 2: 库存欧洲共享)
    stock_share_type: int = Field(validation_alias="share_type")
    # 库存总数量 [原字段 'total']
    stock_total: int = Field(validation_alias="total")
    # 库存总货值金额 [原字段 'total_price']
    stock_total_amt: float = Field(validation_alias="total_price")
    # 库存总可售数量 [原字段 'available_total']
    stock_total_fulfillable: int = Field(validation_alias="available_total")
    # 库存总可售货值金额 [原字段 'available_total_price']
    stock_total_fulfillable_amt: float = Field(validation_alias="available_total_price")
    # FBA 多国店铺本地可售库存信息列表 [原字段 'fba_storage_quantity_list']
    afn_fulfillable_local: list[FbaInventoryDetailFulfillableLocal] = Field(validation_alias="fba_storage_quantity_list")
    # FBA 总可售库存数量 [原字段 'total_fulfillable_quantity']
    # afn_fulfillable + afn_reserved_fc_processing + afn_reserved_fc_transfers
    afn_fulfillable_total: int = Field(validation_alias="total_fulfillable_quantity")
    # FBA 可售库存数量 [原字段 'afn_fulfillable_quantity']
    afn_fulfillable: int = Field(validation_alias="afn_fulfillable_quantity")
    # FBA 可售库存货值金额 [原字段 'afn_fulfillable_quantity_price']
    afn_fulfillable_amt: float = Field(validation_alias="afn_fulfillable_quantity_price")
    # FBA 在库待调仓的库存数量 [原字段 'reserved_fc_processing']
    afn_reserved_fc_processing: int = Field(validation_alias="reserved_fc_processing")
    # FBA 在库待调仓的库存货值金额 [原字段 'reserved_fc_processing_price']
    afn_reserved_fc_processing_amt: float = Field(validation_alias="reserved_fc_processing_price")
    # FBA 在库调仓中的库存数量 [原字段 'reserved_fc_transfers']
    afn_reserved_fc_transfers: int = Field(validation_alias="reserved_fc_transfers")
    # FBA 在库调仓中的库存货值金额 [原字段 'reserved_fc_transfers_price']
    afn_reserved_fc_transfers_amt: float = Field(validation_alias="reserved_fc_transfers_price")
    # FBA 在库待发货的库存数量 [原字段 'reserved_customerorders']
    afn_reserved_customer_order: int = Field(validation_alias="reserved_customerorders")
    # FBA 在库待发货的库存货值金额 [原字段 'reserved_customerorders_price']
    afn_reserved_customer_order_amt: float = Field(validation_alias="reserved_customerorders_price")
    # FBA 在库不可售的库存数量 [原字段 'afn_unsellable_quantity']
    afn_unsellable: int = Field(validation_alias="afn_unsellable_quantity")
    # FBA 在库不可售的库存货值金额 [原字段 'afn_unsellable_quantity_price']
    afn_unsellable_amt: float = Field(validation_alias="afn_unsellable_quantity_price")
    # FBA 实际发货在途的数量 [原字段 'stock_up_num']
    afn_actual_shipped: int = Field(validation_alias="stock_up_num")
    # FBA 实际发货在途的货值金额 [原字段 'stock_up_num_price']
    afn_actual_shipped_amt: float = Field(validation_alias="stock_up_num_price")
    # FBA 发货在途的库存数量 [原字段 'afn_inbound_shipped_quantity']
    afn_inbound_shipped: int = Field(validation_alias="afn_inbound_shipped_quantity")
    # FBA 发货在途的库存货值金额 [原字段 'afn_inbound_shipped_quantity_price']
    afn_inbound_shipped_amt: float = Field(validation_alias="afn_inbound_shipped_quantity_price")
    # FBA 发货计划入库的库存数量 [原字段 'afn_inbound_working_quantity']
    afn_inbound_working: int = Field(validation_alias="afn_inbound_working_quantity")
    # FBA 发货计划入库的库存货值金额 [原字段 'afn_inbound_working_quantity_price']
    afn_inbound_working_amt: float = Field(validation_alias="afn_inbound_working_quantity_price")
    # FBA 发货入库接收中的库存数量 [原字段 'afn_inbound_receiving_quantity']
    afn_inbound_receiving: int = Field(validation_alias="afn_inbound_receiving_quantity")
    # FBA 发货入库接收中的库存货值金额 [原字段 'afn_inbound_receiving_quantity_price']
    afn_inbound_receiving_amt: float = Field(validation_alias="afn_inbound_receiving_quantity_price")
    # FBA 调查中的库存数量 [原字段 'afn_researching_quantity']
    afn_researching: int = Field(validation_alias="afn_researching_quantity")
    # FBA 调查中的库存货值金额 [原字段 'afn_researching_quantity_price']
    afn_researching_amt: float = Field(validation_alias="afn_researching_quantity_price")
    # FBM 可售库存数量 [原字段 'quantity']
    mfn_fulfillable: int = Field(validation_alias="quantity")
    # FBM 可售库存货值金额 [原字段 'quantity_price']
    mfn_fulfillable_amt: float = Field(validation_alias="quantity_price")
    # 库龄0-30天的库存数量 [原字段 'inv_age_0_to_30_days']
    age_0_to_30_days: int = Field(validation_alias="inv_age_0_to_30_days")
    # 库龄0-30天的库存货值金额 [原字段 'inv_age_0_to_30_price']
    age_0_to_30_days_amt: float = Field(validation_alias="inv_age_0_to_30_price")
    # 库龄31-60天的库存数量 [原字段 'inv_age_31_to_60_days']
    age_31_to_60_days: int = Field(validation_alias="inv_age_31_to_60_days")
    # 库龄31-60天的库存货值金额 [原字段 'inv_age_31_to_60_price']
    age_31_to_60_days_amt: float = Field(validation_alias="inv_age_31_to_60_price")
    # 库龄61-90天的库存数量 [原字段 'inv_age_61_to_90_days']
    age_61_to_90_days: int = Field(validation_alias="inv_age_61_to_90_days")
    # 库龄61-90天的库存货值金额 [原字段 'inv_age_61_to_90_price']
    age_61_to_90_days_amt: float = Field(validation_alias="inv_age_61_to_90_price")
    # 库龄0-90天的库存数量 [原字段 'inv_age_0_to_90_days']
    age_0_to_90_days: int = Field(validation_alias="inv_age_0_to_90_days")
    # 库龄0-90天的库存货值金额 [原字段 'inv_age_0_to_90_price']
    age_0_to_90_days_amt: float = Field(validation_alias="inv_age_0_to_90_price")
    # 库龄91-180天的库存数量 [原字段 'inv_age_91_to_180_days']
    age_91_to_180_days: int = Field(validation_alias="inv_age_91_to_180_days")
    # 库龄91-180天的库存货值金额 [原字段 'inv_age_91_to_180_price']
    age_91_to_180_days_amt: float = Field(validation_alias="inv_age_91_to_180_price")
    # 库龄181-270天的库存数量 [原字段 'inv_age_181_to_270_days']
    age_181_to_270_days: int = Field(validation_alias="inv_age_181_to_270_days")
    # 库龄181-270天的库存货值金额 [原字段 'inv_age_181_to_270_price']
    age_181_to_270_days_amt: float = Field(validation_alias="inv_age_181_to_270_price")
    # 库龄271-330天的库存数量 [原字段 'inv_age_271_to_330_days']
    age_271_to_330_days: int = Field(validation_alias="inv_age_271_to_330_days")
    # 库龄271-330天的库存货值金额 [原字段 'inv_age_271_to_330_price']
    age_271_to_330_days_amt: float = Field(validation_alias="inv_age_271_to_330_price")
    # 库龄271-365天的库存数量 [原字段 'inv_age_271_to_365_days']
    age_271_to_365_days: int = Field(validation_alias="inv_age_271_to_365_days")
    # 库龄271-365天的库存货值金额 [原字段 'inv_age_271_to_365_price']
    age_271_to_365_days_amt: float = Field(validation_alias="inv_age_271_to_365_price")
    # 库龄331-365天的库存数量 [原字段 'inv_age_331_to_365_days']
    age_331_to_365_days: int = Field(validation_alias="inv_age_331_to_365_days")
    # 库龄331-365天的库存货值金额 [原字段 'inv_age_331_to_365_price']
    age_331_to_365_days_amt: float = Field(validation_alias="inv_age_331_to_365_price")
    # 库龄365天以上的库存数量 [原字段 'inv_age_365_plus_days']
    age_365_plus_days: int = Field(validation_alias="inv_age_365_plus_days")
    # 库龄365天以上的库存货值金额 [原字段 'inv_age_365_plus_price']
    age_365_plus_days_amt: float = Field(validation_alias="inv_age_365_plus_price")
    # 库存售出率 (过去 90 天销量除以平均可售库存) [原字段 'sell_through']
    sell_through_rate: float = Field(validation_alias="sell_through")
    # 历史供货天数 (取短期&长期更大值)
    historical_days_of_supply: float
    # 历史供货天数货值金额 [原字段 'historical_days_of_supply_price']
    historical_days_of_supply_amt: float = Field(validation_alias="historical_days_of_supply_price")
    # 亚马逊预测的库存健康状态 [原字段 'fba_inventory_level_health_status']
    inventory_health_status: str = Field(validation_alias="fba_inventory_level_health_status")
    # 亚马逊低库存水平费收费情况 [原字段 'low_inventory_level_fee_applied']
    inventory_low_level_fee_status: str = Field(validation_alias="low_inventory_level_fee_applied")
    # 亚马逊预测的从今天起30天内产生的仓储费 [原字段 'estimated_storage_cost_next_month']
    estimated_30d_storage_fee: float = Field(validation_alias="estimated_storage_cost_next_month")
    # 亚马逊预估的冗余商品数量 [原字段 'estimated_excess_quantity']
    estimated_excess_qty: float = Field(validation_alias="estimated_excess_quantity")
    # 亚马逊建议的最低库存量 [原字段 'fba_minimum_inventory_level']
    recommended_minimum_qty: float = Field(validation_alias="fba_minimum_inventory_level")
    # 亚马逊建议的操作 [原字段 'recommended_action']
    recommended_action: str
    # fmt: on

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("afn_fulfillable_local", mode="before")
    @classmethod
    def _validate_afn_fulfillable_local(cls, v) -> list | Any:
        """验证 FBA 多国店铺本地可售库存信息"""
        return [] if v is None else v


class FbaInventoryDetails(ResponseV1):
    """FBA库存明细信息"""

    data: list[FbaInventoryDetailItem]


# . AWD Inventory
class AwdInventoryItem(BaseModel):
    """AWD库存产品信息"""

    # fmt: off
    # 仓库名称 [原字段 'wname']
    warehouse_name: str = Field(validation_alias="wname")
    # 领星站点ID
    mid: int
    # 国家 [原字段 'nation']
    country: str = Field(validation_alias="nation")
    # 领星店铺ID
    sid: int
    # 领星店铺名称
    seller_name: str
    # 商品父ASIN
    parent_asin: str
    # 商品ASIN
    asin: str
    # 商品ASIN链接
    asin_url: str
    # 亚马逊SKU [原字段 'seller_sku']
    msku: str = Field(validation_alias="seller_sku")
    # 领星本地SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 亚马逊FNSKU
    fnsku: str
    # 多属性SPU产品编码
    spu: str
    # 多属性SPU产品名称
    spu_name: str
    # 领星产品ID
    product_id: int
    # 领星商品名称
    product_name: str
    # 商品类型ID [原字段 'cid']
    category_id: int = Field(validation_alias="cid")
    # 商品类型名称 [原字段 'category_text']
    category_name: str = Field(validation_alias="category_text")
    # 商品类型1级名称
    category_level1: str
    # 商品类型2级名称
    category_level2: str
    # 商品类型3级名称
    category_level3: str
    # 商品类型列表 [原字段 'category_Arr']
    categories: list = Field(validation_alias="category_Arr")
    # 商品品牌ID [原字段 'bid']
    brand_id: int = Field(validation_alias="bid")
    # 商品品牌名称 [原字段 'product_brand_text']
    brand_name: str = Field(validation_alias="product_brand_text")
    # 产品图片链接 [原字段 'pic_url']
    image_url: str = Field(validation_alias="pic_url")
    # 产品略缩图链接 [原字段 'small_image_url']
    thumbnail_url: str = Field(validation_alias="small_image_url")
    # 产品负责人列表 [原字段 'asin_principal_list']
    operators: list = Field(validation_alias="asin_principal_list")
    # 商品属性列表 [原字段 'attribute']
    attributes: list[base_schema.SpuProductAttribute] = Field(validation_alias="attribute")
    # AWD 总库存数量 [原字段 'total_onhand_quantity']
    awd_total: int = Field(validation_alias="total_onhand_quantity")
    # AWD 总库存货值金额 [原字段 'total_onhand_quantity_price']
    awd_total_amt: float = Field(validation_alias="total_onhand_quantity_price")
    # AWD 可分发库存数量 [原字段 'available_distributable_quantity']
    awd_distributable: int = Field(validation_alias="available_distributable_quantity")
    # AWD 可分发库存货值金额 [原字段 'available_distributable_quantity_price']
    awd_distributable_amt: float = Field(validation_alias="available_distributable_quantity_price")
    # AWD 在途分发至FBA数量 [原字段 'awd_to_fba_quantity_shipped']
    awd_distributing: int = Field(validation_alias="awd_to_fba_quantity_shipped")
    # AWD 在途分发至FBA货值金额 [原字段 'awd_to_fba_quantity_shipped_price']
    awd_distributing_amt: float = Field(validation_alias="awd_to_fba_quantity_shipped_price")
    # AWD 在库待分发数量 [原字段 'reserved_distributable_quantity']
    awd_reserved_distributes: int = Field(validation_alias="reserved_distributable_quantity")
    # AWD 在库待分发货值金额 [原字段 'reserved_distributable_quantity_price']
    awd_reserved_distributes_amt: float = Field(validation_alias="reserved_distributable_quantity_price")
    # AWD 实际发货在途的数量 [原字段 'awd_actual_quantity_shipped']
    awd_actual_shipped: int = Field(validation_alias="awd_actual_quantity_shipped")
    # AWD 实际发货在途的货值金额 [原字段 'awd_actual_quantity_shipped_price']
    awd_actual_shipped_amt: float = Field(validation_alias="awd_actual_quantity_shipped_price")
    # AWD 发货在途的库存数量 [原字段 'awd_quantity_shipped']
    awd_inbound_shipped: int = Field(validation_alias="awd_quantity_shipped")
    # AWD 发货在途的库存货值金额 [原字段 'awd_quantity_shipped_price']
    awd_inbound_shipped_amt: float = Field(validation_alias="awd_quantity_shipped_price")
    # fmt: on


class AwdInventory(ResponseV1, FlattenDataList):
    """AWD库存信息"""

    data: list[AwdInventoryItem]


# . Seller Inventory
class OverseasInventoryInfo(BaseModel):
    """海外仓第三方库存信息"""

    # 产品可售库存数量 [原字段 'qty_sellable']
    fulfillable_qty: IntOrNone2Zero = Field(0, validation_alias="qty_sellable")
    # 产品待上架库存数量 [原字段 'qty_pending']
    pending_qty: IntOrNone2Zero = Field(0, validation_alias="qty_pending")
    # 产品预留库存数量 [原字段 'qty_reserved']
    reserved_qty: IntOrNone2Zero = Field(0, validation_alias="qty_reserved")
    # 产品调拨在途数量 [原字段 'qty_onway']
    transit_qty: IntOrNone2Zero = Field(0, validation_alias="qty_onway")
    # 外箱可售数量 [原字段 'box_qty_sellable']
    box_fulfillable_qty: IntOrNone2Zero = Field(0, validation_alias="box_qty_sellable")
    # 外箱待上架数量 [原字段 'box_qty_pending']
    box_pending_qty: IntOrNone2Zero = Field(0, validation_alias="box_qty_pending")
    # 外箱预留数量 [原字段 'box_qty_reserved']
    box_reserved_qty: IntOrNone2Zero = Field(0, validation_alias="box_qty_reserved")
    # 外箱调拨在途数量 [原字段 'box_qty_onway']
    box_transit_qty: IntOrNone2Zero = Field(0, validation_alias="box_qty_onway")


class SellerInventoryItemAge(BaseModel):
    """卖家(本地/海外)仓库库存产品库龄信息"""

    # 库龄信息 [原字段 'name']
    age: str = Field(validation_alias="name")
    # 库龄数量
    qty: int


class SellerInventoryItem(BaseModel):
    """卖家(本地/海外)仓库库存产品信息"""

    # fmt: off
    # 仓库ID [原字段 'wid']
    warehouse_id: int = Field(validation_alias="wid")
    # 领星店铺ID [原字段 'seller_id']
    sid: int = Field(validation_alias="seller_id")
    # 领星本地商品SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 亚马逊FNSKU
    fnsku: str
    # 领星商品ID
    product_id: int
    # 产品总库存数量 [原字段 'product_total']
    total_qty: int = Field(validation_alias="product_total")
    # 产品库存可售数量 [原字段 'product_valid_num']
    fulfillable_qty: int = Field(validation_alias="product_valid_num")
    # 产品库存可售预留数量 [原字段 'good_lock_num']
    fulfillable_reserved_qty: int = Field(validation_alias="good_lock_num")
    # 产品库存次品数量 [原字段 'product_bad_num']
    unsellable_qty: int = Field(validation_alias="product_bad_num")
    # 产品库存不可售预留数量 [原字段 'bad_lock_num']
    unsellable_reserved_qty: int = Field(validation_alias="bad_lock_num")
    # 产品库存加工计划单品的预留数量 [原字段 'product_lock_num']
    process_reserved_qty: int = Field(validation_alias="product_lock_num")
    # 产品库存待质检数量 [原字段 'product_qc_num']
    pending_qc_qty: int = Field(validation_alias="product_qc_num")
    # 产品待到货数量 [原字段 'quantity_receive']
    pending_arrival_qty: int = Field(validation_alias="quantity_receive")
    # 产品调拨在途数量 [原字段 'product_onway']
    transit_qty: int = Field(validation_alias="product_onway")
    # 产品调拨在途头程费用 [原字段 'transit_head_cost']
    transit_first_leg_fee: float = Field(validation_alias="transit_head_cost")
    # 外箱可售数量 [原字段 'available_inventory_box_qty']
    box_fulfillable_qty: int = Field(validation_alias="available_inventory_box_qty")
    # 第三方海外仓库存信息 [原字段 'third_inventory']
    overseas_inventory: OverseasInventoryInfo = Field(validation_alias="third_inventory")
    # 库存单价成本 [原字段 'stock_cost']
    stock_item_cost_amt: FloatOrNone2Zero = Field(validation_alias="stock_cost")
    # 库存总成本金额 [原字段 'stock_cost_total']
    stock_total_cost_amt: FloatOrNone2Zero = Field(validation_alias="stock_cost_total")
    # 平均库龄 [原字段 'average_age']
    age_avg_days: int = Field(validation_alias="average_age")
    # 库龄列表 [原字段 'stock_age_list']
    ages: list[SellerInventoryItemAge] = Field(validation_alias="stock_age_list")
    # fmt: on

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("overseas_inventory", mode="before")
    @classmethod
    def _validate_overseas_inventory(cls, v) -> dict:
        return {} if not v else v


class SellerInventory(ResponseV1):
    """卖家(本地/海外)仓库库存信息"""

    data: list[SellerInventoryItem]


# . Seller Inventory Bin
class SellerInventoryBinItem(BaseModel):
    """查询卖家(本地/海外)仓库库存货架(仓位)信息"""

    # fmt: off
    # 仓库ID [原字段 'wid']
    warehouse_id: int = Field(validation_alias="wid")
    # 仓库名称 [原字段 'wh_name']
    warehouse_name: str = Field(validation_alias="wh_name")
    # 仓库货架ID [原字段 'whb_id']
    bin_id: int = Field(validation_alias="whb_id")
    # 仓库货架名称 [原字段 'whb_name']
    bin_name: str = Field(validation_alias="whb_name")
    # 仓库货架类型 [原字段 'whb_type']
    bin_type: int = Field(validation_alias="whb_type")
    # 仓库货架类型描述 [原字段 'whb_type_name']
    bin_type_desc: str = Field(validation_alias="whb_type_name")
    # 领星店铺ID [原字段 'store_id']
    sid: int = Field(validation_alias="store_id")
    # 亚马逊SKU
    msku: str
    # 领星本地商品SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 亚马逊FNSKU
    fnsku: str
    # 领星商品ID
    product_id: int
    # 领星商品名称
    product_name: str
    # 产品总库存数量 [原字段 'total']
    total_qty: int = Field(validation_alias="total")
    # 产品库存可售数量 [原字段 'validNum']
    fulfillable_qty: int = Field(validation_alias="validNum")
    # 产品库存预留数量 [原字段 'lockNum']
    reserved_qty: int = Field(validation_alias="lockNum")
    # 第三方海外仓库存信息 [原字段 'third_inventory']
    overseas_inventory: OverseasInventoryInfo = Field(validation_alias="third_inventory")
    # fmt: on

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("overseas_inventory", mode="before")
    @classmethod
    def _validate_overseas_inventory(cls, v) -> dict:
        return {} if not v else v


class SellerInventoryBins(ResponseV1):
    """卖家(本地/海外)仓库库存货架(仓位)信息"""

    data: list[SellerInventoryBinItem]


# . Seller Inventory Batch
class SellerInventoryBatch(BaseModel):
    """卖家(本地/海外)仓库出入库批次信息"""

    # 仓库ID [原字段 'wid']
    warehouse_id: int = Field(validation_alias="wid")
    # 仓库名称 [原字段 'wh_name']
    warehouse_name: str = Field(validation_alias="wh_name")
    # 批次号 [原字段 'batch_no']
    batch_number: str = Field(validation_alias="batch_no")
    # 源头批次号 [原字段 'source_batch_no']
    source_batch_numbers: list[str] = Field(validation_alias="source_batch_no")
    # 出入库单号 [原字段 'order_sn']
    transaction_number: str = Field(validation_alias="order_sn")
    # 出入库类型 [原字段 'type']
    transaction_type: int = Field(validation_alias="type")
    # 出入库类型描述 [原字段 'type_name']
    transaction_type_desc: str = Field(validation_alias="type_name")
    # 领星店铺ID [原字段 'store_id']
    sid: int = Field(validation_alias="store_id")
    # 领星店铺名称 [原字段 'store_name']
    seller_name: str = Field(validation_alias="store_name")
    # 亚马逊SKU
    msku: str
    # 领星本地商品SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 亚马逊FNSKU
    fnsku: str
    # 领星商品ID
    product_id: int
    # 领星商品名称
    product_name: str
    # 批次总数 [原字段 'total']
    total_qty: int = Field(validation_alias="total")
    # 批次在库结存 [原字段 'balance_num']
    ending_balance_qty: int = Field(validation_alias="balance_num")
    # 批次在途结存 [原字段 'transit_balance_num']
    transit_balance_qty: int = Field(validation_alias="transit_balance_num")
    # 批次可售在途 [原字段 'good_transit_num']
    transit_fulfillable_qty: int = Field(validation_alias="good_transit_num")
    # 批次不可售在途 [原字段 'bad_transit_num']
    transit_unsellable_qty: int = Field(validation_alias="bad_transit_num")
    # 批次可售数量 [原字段 'good_num']
    fulfillable_qty: int = Field(validation_alias="good_num")
    # 批次不可售数量 [原字段 'bad_num']
    unsellable_qty: int = Field(validation_alias="bad_num")
    # 批次待质检数量 [原字段 'qc_num']
    pending_qc_qty: int = Field(validation_alias="qc_num")
    # 批次货物成本 [原字段 'stock_cost']
    cost_amt: float = Field(validation_alias="stock_cost")
    # 批次头程费用 [原字段 'head_stock_cost']
    first_leg_fee: float = Field(validation_alias="head_stock_cost")
    # 批次出入库费用 [原字段 'fee']
    transaction_fee: float = Field(validation_alias="fee")
    # 批次总货值 [原字段 'amount']
    value_amt: float = Field(validation_alias="amount")
    # 采购计划单号列表 [原字段 'plan_sn']
    purchase_plan_numbers: list[str] = Field(validation_alias="plan_sn")
    # 采购单号列表 [原字段 'purchase_order_sns']
    purchase_numbers: list[str] = Field(validation_alias="purchase_order_sns")
    # 收货单号列表 [原字段 'delivery_order_sns']
    receiving_numbers: list[str] = Field(validation_alias="delivery_order_sns")
    # 供应商ID列表
    supplier_ids: list[int]
    # 供应商名称列表
    supplier_names: list[str]
    # 批次创建时间 (北京时间)
    batch_time: str
    # 采购时间 (北京时间) [原字段 'purchase_in_time']
    purchase_time: str = Field(validation_alias="purchase_in_time")
    # 更新时间 (北京时间)
    update_time: str


class SellerInventoryBatches(ResponseV1):
    """卖家(本地/海外)仓库出入库批次信息"""

    data: list[SellerInventoryBatch]


# . Seller Inventory Record
class SellerInventoryRecord(BaseModel):
    """卖家(本地/海外)仓库出入库流水信息"""

    # 仓库ID [原字段 'wid']
    warehouse_id: int = Field(validation_alias="wid")
    # 仓库名称 [原字段 'wh_name']
    warehouse_name: str = Field(validation_alias="wh_name")
    # 批次流水号 [原字段 'batch_state_id']
    batch_record_number: str = Field(validation_alias="batch_state_id")
    # 批次号 [原字段 'batch_no']
    batch_number: str = Field(validation_alias="batch_no")
    # 源头批次号 [原字段 'source_batch_no']
    source_batch_numbers: list[str] = Field(validation_alias="source_batch_no")
    # 出入库单号 [原字段 'order_sn']
    transaction_number: str = Field(validation_alias="order_sn")
    # 源头出入库单号列表 [原字段 'source_order_sn']
    source_transaction_numbers: list[str] = Field(validation_alias="source_order_sn")
    # 出入库类型 [原字段 'type']
    transaction_type: int = Field(validation_alias="type")
    # 出入库类型描述 [原字段 'type_name']
    transaction_type_desc: str = Field(validation_alias="type_name")
    # 领星店铺ID [原字段 'store_id']
    sid: int = Field(validation_alias="store_id")
    # 领星店铺名称 [原字段 'store_name']
    seller_name: str = Field(validation_alias="store_name")
    # 亚马逊SKU
    msku: str
    # 领星本地商品SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 亚马逊FNSKU
    fnsku: str
    # 领星商品ID
    product_id: int
    # 领星商品名称
    product_name: str
    # 批次流水在库结存 [原字段 'balance_num']
    ending_balance_qty: int = Field(validation_alias="balance_num")
    # 批次流水在途结存 [原字段 'transit_balance_num']
    transit_balance_qty: int = Field(validation_alias="transit_balance_num")
    # 批次流水可售在途 [原字段 'good_transit_num']
    transit_fulfillable_qty: int = Field(validation_alias="good_transit_num")
    # 批次流水不可售在途 [原字段 'bad_transit_num']
    transit_unsellable_qty: int = Field(validation_alias="bad_transit_num")
    # 批次流水可售数量 [原字段 'good_num']
    fulfillable_qty: int = Field(validation_alias="good_num")
    # 批次流水不可售数量 [原字段 'bad_num']
    unsellable_qty: int = Field(validation_alias="bad_num")
    # 批次流水待质检数量 [原字段 'qc_num']
    pending_qc_qty: int = Field(validation_alias="qc_num")
    # 批次流水货物成本 [原字段 'stock_cost']
    cost_amt: float = Field(validation_alias="stock_cost")
    # 批次流水头程费用 [原字段 'head_stock_cost']
    first_leg_fee: float = Field(validation_alias="head_stock_cost")
    # 批次流水出入库费用 [原字段 'fee']
    transaction_fee: float = Field(validation_alias="fee")
    # 批次流水总货值 [原字段 'amount']
    value_amt: float = Field(validation_alias="amount")
    # 采购计划单号列表 [原字段 'plan_sn']
    purchase_plan_numbers: list[str] = Field(validation_alias="plan_sn")
    # 采购单号列表 [原字段 'purchase_order_sns']
    purchase_numbers: list[str] = Field(validation_alias="purchase_order_sns")
    # 收货单号列表 [原字段 'delivery_order_sns']
    receiving_numbers: list[str] = Field(validation_alias="delivery_order_sns")
    # 供应商ID列表
    supplier_ids: list[int]
    # 供应商名称列表
    supplier_names: list[str]


class SellerInventoryRecords(ResponseV1):
    """卖家(本地/海外)仓库出入库流水信息"""

    data: list[SellerInventoryRecord]


# . Seller Inventory Operation
class SellerInventoryOperation(BaseModel):
    """卖家(本地/海外)仓库出入库操作流水信息"""

    # fmt: off
    # 仓库ID [原字段 'wid']
    warehouse_id: int = Field(validation_alias="wid")
    # 仓库名称 [原字段 'wh_name']
    warehouse_name: str = Field(validation_alias="ware_house_name")
    # 出入库单号 [原字段 'order_sn']
    transaction_number: str = Field(validation_alias="order_sn")
    # 关联出入库单号 [原字段 'ref_order_sn']
    ref_transaction_number: str = Field(validation_alias="ref_order_sn")
    # 操作ID [原字段 'statement_id']
    transaction_id: str = Field(validation_alias="statement_id")
    # 操作类型 [原字段 'type']
    transaction_type: int = Field(validation_alias="type")
    # 操作类型描述 [原字段 'type_text']
    transaction_type_desc: str = Field(validation_alias="type_text")
    # 出入库子类型 [原字段 'sub_type']
    transaction_sub_type: str = Field(validation_alias="sub_type")
    # 出入库子类型描述 [原字段 'sub_type_text']
    transaction_sub_type_desc: str = Field(validation_alias="sub_type_text")
    # 操作备注
    transaction_note: str = Field(validation_alias="remark")
    # 操作时间 (北京时间) [原字段 'opt_time']
    transaction_time: str = Field(validation_alias="opt_time")
    # 操作人ID [原字段 'opt_uid']
    operator_id: int = Field(validation_alias="opt_uid")
    # 操作人名称 [原字段 'opt_real_name']
    operator_name: str = Field(validation_alias="opt_real_name")
    # 领星店铺ID [原字段 'seller_id']
    sid: int = Field(validation_alias="seller_id")
    # 领星本地商品SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 亚马逊FNSKU
    fnsku: str
    # 领星商品ID
    product_id: int
    # 领星商品名称
    product_name: str
    # 品牌ID [原字段 'bid']
    brand_id: int = Field(validation_alias="bid")
    # 品牌名称
    brand_name: str
    # 操作流水总数 [原字段 'product_total']
    total_qty: int = Field(validation_alias="product_total")
    # 在途流水可售数量 [原字段 'good_transit_num']
    transit_fulfillable_qty: int = Field(validation_alias="good_transit_num")
    # 在途流水可售结存数量 [原字段 'good_transit_balance_num']
    transit_fulfillable_balance_qty: int = Field(validation_alias="good_transit_balance_num")
    # 在途流水不可售数量 [原字段 'bad_transit_num']
    transit_unsellable_qty: int = Field(validation_alias="bad_transit_num")
    # 在途流水不可售结存数量 [原字段 'bad_transit_balance_num']
    transit_unsellable_balance_qty: int = Field(validation_alias="bad_transit_balance_num")
    # 操作流水可售数量 [原字段 'product_good_num']
    fulfillable_qty: int = Field(validation_alias="product_good_num")
    # 操作流水可售结存数量 [原字段 'good_balance_num']
    fulfillable_balance_qty: int = Field(validation_alias="good_balance_num")
    # 操作流水可售预留数量 [原字段 'product_lock_good_num']
    fulfillable_reserved_qty: int = Field(validation_alias="product_lock_good_num")
    # 操作流水可售预留结存数量 [原字段 'good_lock_balance_num']
    fulfillable_reserved_balance_qty: int = Field(validation_alias="good_lock_balance_num")
    # 操作流水不可售数量 [原字段 'product_bad_num']
    unsellable_qty: int = Field(validation_alias="product_bad_num")
    # 操作流水不可售结存数量 [原字段 'bad_balance_num']
    unsellable_balance_qty: int = Field(validation_alias="bad_balance_num")
    # 操作流水不可售预留数量 [原字段 'product_lock_bad_num']
    unsellable_reserved_qty: int = Field(validation_alias="product_lock_bad_num")
    # 操作流水不可售预留结存数量 [原字段 'bad_lock_balance_num']
    unsellable_reserved_balance_qty: int = Field(validation_alias="bad_lock_balance_num")
    # 操作流水待质检数量 [原字段 'product_qc_num']
    pending_qc_qty: int = Field(validation_alias="product_qc_num")
    # 操作流水质检结存数量 [原字段 'qc_balance_num']
    qc_balance_qty: int = Field(validation_alias="qc_balance_num")
    # 操作流水单位采购价格 [原字段 'single_cg_price']
    item_purchase_price: FloatOrNone2Zero = Field(validation_alias="single_cg_price")
    # 操作流水货物成本 [原字段 'stock_cost']
    cost_amt: FloatOrNone2Zero = Field(validation_alias="stock_cost")
    # 操作流水单位货物成本 [原字段 'single_stock_price']
    item_cost_amt: FloatOrNone2Zero = Field(validation_alias="single_stock_price")
    # 操作流水头程费用 [原字段 'head_stock_cost']
    first_leg_fee: FloatOrNone2Zero = Field(validation_alias="head_stock_cost")
    # 操作流水单位头程费用 [原字段 'head_stock_price']
    item_first_leg_fee: FloatOrNone2Zero = Field(validation_alias="head_stock_price")
    # 操作流水出入库费用 [原字段 'fee_cost']
    transaction_fee: FloatOrNone2Zero = Field(validation_alias="fee_cost")
    # 操作流水单位出入库费用 [原字段 'single_fee_cost']
    item_transaction_fee: FloatOrNone2Zero = Field(validation_alias="single_fee_cost")
    # 操作流水总货值 [原字段 'product_amounts']
    value_amt: FloatOrNone2Zero = Field(validation_alias="product_amounts")
    # fmt: on


class SellerInventoryOperations(ResponseV1):
    """卖家(本地/海外)仓库出入库操作流水信息"""

    data: list[SellerInventoryOperation]


# . Seller Inventory Bin Record
class SellerInventoryBinRecord(BaseModel):
    """卖家(本地/海外)仓库货架(仓位)出入库流水信息"""

    # 仓库ID [原字段 'wid']
    warehouse_id: int = Field(validation_alias="wid")
    # 仓库名称 [原字段 'wh_name']
    warehouse_name: str = Field(validation_alias="ware_house_name")
    # 仓库货架ID [原字段 'whb_id']
    bin_id: int = Field(validation_alias="whb_id")
    # 仓库货架名称 [原字段 'whb_name']
    bin_name: str = Field(validation_alias="whb_name")
    # 仓库货架类型描述 [原字段 'whb_type_name']
    bin_type_desc: str = Field(validation_alias="whb_type_name")
    # 出入库单号 [原字段 'order_sn']
    transaction_number: str = Field(validation_alias="order_sn")
    # 出入库类型 [原字段 'type']
    transaction_type: int = Field(validation_alias="type")
    # 出入库类型描述 [原字段 'type_text']
    transaction_type_desc: str = Field(validation_alias="type_text")
    # 出入库备注
    transaction_note: str = Field(validation_alias="remark")
    # 出入库时间 (北京时间) [原字段 'opt_time']
    transaction_time: str = Field(validation_alias="opt_time")
    # 出入库数量 [原字段 'num']
    transaction_qty: int = Field(validation_alias="num")
    # 操作人ID [原字段 'opt_uid']
    operator_id: int = Field(validation_alias="opt_uid")
    # 操作人名称 [原字段 'opt_realname']
    operator_name: str = Field(validation_alias="opt_realname")
    # 领星店铺ID [原字段 'seller_id']
    sid: int = Field(validation_alias="seller_id")
    # 领星本地商品SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 亚马逊FNSKU
    fnsku: str
    # 领星商品ID
    product_id: int
    # 领星商品名称
    product_name: str


class SellerInventoryBinRecords(ResponseV1):
    """卖家(本地/海外)仓库货架(仓位)出入库流水信息"""

    data: list[SellerInventoryBinRecord]
