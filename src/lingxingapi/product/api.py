# -*- coding: utf-8 -*-c
import datetime
from typing import Literal
from lingxingapi import utils, errors
from lingxingapi.base.api import BaseAPI
from lingxingapi.base import param as base_param
from lingxingapi.base import schema as base_schema
from lingxingapi.product import param, route, schema

# Type Aliases ---------------------------------------------------------------------------------------------------------
PRODUCT_CODE_TYPE = Literal["UPC", "EAN", "ISBN"]


# API ------------------------------------------------------------------------------------------------------------------
class ProductAPI(BaseAPI):
    """领星API `产品数据` 接口

    ## Notice
    请勿直接实例化此类
    """

    async def Products(
        self,
        *,
        lskus: str | list[str] | None = None,
        sku_identifiers: str | list[str] | None = None,
        update_start_time: str | int | datetime.date | datetime.datetime | None = None,
        update_end_time: str | int | datetime.date | datetime.datetime | None = None,
        create_start_time: str | int | datetime.date | datetime.datetime | None = None,
        create_end_time: str | int | datetime.date | datetime.datetime | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.Products:
        """查询领星本地产品列表

        ## Docs
        - 产品: [查询本地产品列表](https://apidoc.lingxing.com/#/docs/Product/ProductLists)

        :param lskus `<'str/list'>`: 领星本地SKU或SKU列表, 默认 `None` (查询所有SKU)
        :param sku_identifiers `<'str/list'>`: 领星本地SKU识别码或识别码列表, 默认 `None` (查询所有SKU识别码)
        :param update_start_time `<'str/int/date/datetime'>`: 产品更新开始时间, 左闭右开, 默认 `None`
        :param update_end_time `<'str/int/date/datetime'>`: 产品更新结束时间, 左闭右开, 默认 `None`
        :param create_start_time `<'str/int/date/datetime'>`: 产品创建开始时间, 左闭右开, 默认 `None`
        :param create_end_time `<'str/int/date/datetime'>`: 产品创建结束时间, 左闭右开, 默认 `None`
        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 最大值1000, 默认 `None` (使用: 1000)
        :returns `<'Products'>`: 返回查询到的领星本地产品列表
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
                    # 领星本地SKU [原字段 'sku']
                    "lsku": "LOCAL********",
                    # 领星本地SKU识别码
                    "sku_identifier": "S/N1234567890",
                    # 领星本地产品ID [原字段 'id']
                    "product_id": 1,
                    # 领星本地产品名称
                    "product_name": "P*********",
                    # 领星本地产品分类ID [原字段 'cid']
                    "category_id": 1,
                    # 领星本地产品分类名称
                    "category_name": "香薰机",
                    # 领星本地产品品牌ID
                    "brand_id": 1,
                    # 领星本地产品品牌名称
                    "brand_name": "BestTech",
                    # 产品图片链接 [原字段 'pic_url']
                    "image_url": "https://image.distributetop.com/****.jpeg",
                    # 是否为组合产品 (0: 否, 1: 是) [原字段 'is_combo']
                    "is_bundled": 0,
                    # 产品是否被启用 (0: 未启用, 1: 已启用) [原字段 'open_status']
                    "is_enabled": 1,
                    # 产品状态 (0: 停售, 1: 在售, 2: 开发中, 3: 清仓) [原字段 'status']
                    "status": 1,
                    # 产品状态描述 [原字段 'status_text']
                    "status_desc": "在售",
                    # 创建时间 (UTC秒时间戳) [原字段 'create_time']
                    "create_time_ts": 1753330296,
                    # 更新时间 (UTC秒时间戳) [原字段 'update_time']
                    "update_time_ts": 1753330796,
                    # 产品开发者用户ID (Account.user_id) [原字段 'product_developer_uid']
                    "product_developer_id": 10******,
                    # 产品开发者姓名 (Account.display_name) [原字段 'product_developer']
                    "product_developer_name": "超级管理员",
                    # 产品采购人用户ID (Account.user_id) [原字段 'cg_opt_uid']
                    "purchase_staff_id": 10******,
                    # 产品采购人姓名 (Account.display_name) [原字段 'cg_opt_username']
                    "purchase_staff_name": "超级管理员",
                    # 采购交期 (单位: 天) [原字段 'cg_delivery']
                    "purchase_delivery_time": 14,
                    # 采购运输成本 [原字段 'cg_transport_costs']
                    "purchase_shipping_costs": 0.0,
                    # 采购成本 [原字段 'cg_price']
                    "purchase_price": 100.0,
                    # 采购备注 [原字段 'purchase_remark']
                    "purchase_note": "",
                    # 供应商报价信息列表 [原字段 'supplier_quote']
                    "supplier_quotes": [
                        {
                            # 领星本地产品ID
                            "product_id": 4*****,
                            # 供应商ID
                            "supplier_id": 6***,
                            # 供应商名称
                            "supplier_name": "遵*****",
                            # 供应商编码
                            "supplier_code": "SU*****",
                            # 供应商等级 [原字段 'level_text']
                            "supplier_level": "",
                            # 供应商员工数 [原字段 'employees_text']
                            "supplier_employees": "",
                            # 供应商产品链接 [原字段 'supplier_product_url']
                            "supplier_product_urls": [],
                            # 供应商备注 [原字段 'remark']
                            "supplier_note": "",
                            # 是否是首选供应商 (0: 否, 1: 是) [原字段 'is_primary']
                            "is_primary_supplier": 1,
                            # 报价ID [原字段 'psq_id']
                            "quote_id": 21****************,
                            # 报价货币符号 [原字段 'cg_currency_icon']
                            "quote_currency_icon": "￥",
                            # 报价单价 [原字段 'cg_price']
                            "quote_price": 100.0,
                            # 报价交期 (单位: 天) [原字段 'quote_cg_delivery']
                            "quote_delivery_time": 14,
                            # 报价备注 [原字段 'quote_remark']
                            "quote_note": "",
                            # 报价列表 [原字段 'quotes']
                            "quotes": [
                                {
                                    # 报价货币代码 [原字段 'currency']
                                    "currency_code": "CNY",
                                    # 报价货币符号
                                    "currency_icon": "￥",
                                    # 报价是否含税 (0: 否, 1: 是) [原字段 'is_tax']
                                    "is_tax_inclusive": 1,
                                    # 报价税率 (百分比)
                                    "tax_rate": 5.0,
                                    # 报价梯度 [原字段 'step_prices']
                                    "price_tiers": [
                                        {
                                            # 最小订购量
                                            "moq": 100,
                                            # 报价 (不含税) [原字段 'price']
                                            "price_excl_tax": 100.0,
                                            # 报价 (含税)
                                            "price_with_tax": 105.0,
                                        },
                                        ...
                                    ],
                                },
                                ...
                            ],
                        },
                        ...
                    ],
                    # 多属性产品ID [原字段 'ps_id']
                    "spu_id": 1,
                    # 多属性产品名称 [原字段 'spu']
                    "spu_name": "香薰机",
                    # 产品属性列表 [原字段 'attribute']
                    "attributes": [
                        {
                            # 产品属性ID
                            "attr_id": 1,
                            # 产品属性名称
                            "attr_name": "颜色",
                            # 产品属性值
                            "attr_value": "红色",
                        },
                        ...
                    ],
                    # 产品标签列表 [原字段 'global_tags']
                    "tags": [
                        {
                            # 领星标签ID (GlobalTag.tag_id) [原字段 'global_tag_id']
                            "tag_id": "9*****************",
                            # 领星标签名称 (GlobalTag.tag_name) [原字段 'tag_name']
                            "tag_name": "重点款",
                            # 领星标签颜色 (如: "#FF0000") [原字段 'color']
                            "tag_color": "#3BB84C",
                        },
                        ...
                    ],
                    # 自定义字段
                    "custom_fields": [
                        {
                            # 自定义字段ID
                            "field_id": "20************",
                            # 自定义字段名称
                            "field_name": "字段名",
                            # 自定义字段值
                            "field_value": "字段值",
                        },
                        ...
                    ],
                },
                ...
            ],
        }
        ```
        """
        url = route.PRODUCTS
        # 解析并验证参数
        args = {
            "lskus": lskus,
            "sku_identifiers": sku_identifiers,
            "update_start_time": update_start_time,
            "update_end_time": update_end_time,
            "create_start_time": create_start_time,
            "create_end_time": create_end_time,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.Products.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.Products.model_validate(data)

    async def ProductDetails(
        self,
        *,
        lskus: str | list[str] | None = None,
        sku_identifiers: str | list[str] | None = None,
        product_ids: int | list[int] | None = None,
    ) -> schema.ProductDetails:
        """批量查询领星本地产品详情

        ## Docs
        - 产品: [批量查询本地产品详情](https://apidoc.lingxing.com/#/docs/Product/batchGetProductInfo)

        :param lskus `<'str/list'>`: 领星本地SKU或SKU列表,
            默认 `None` (三码选一必填), 参数来源 `Product.lsku`
        :param sku_identifiers `<'str/list'>`: 领星本地SKU识别码或识别码列表,
            默认 `None` (三码选一必填), 参数来源 `Product.sku_identifier`
        :param product_ids `<'int/list'>`: 领星本地产品ID或产品ID列表,
            默认 `None` (三码选一必填), 参数来源 `Product.product_id`
        :returns `<'ProductDetails'>`: 返回查询到的领星本地产品详情列表
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
                    # 领星本地SKU [原字段 'sku']
                    "lsku": "SKU********",
                    # 领星本地SKU识别码
                    "sku_identifier": "S/N1234567890",
                    # 领星本地产品ID [原字段 'id']
                    "product_id": 1,
                    # 领星本地产品名称
                    "product_name": "P*********",
                    # 领星本地产品分类ID [原字段 'cid']
                    "category_id": 1,
                    # 领星本地产品分类名称
                    "category_name": "香薰机",
                    # 领星本地产品品牌ID
                    "brand_id": 1,
                    # 领星本地产品品牌名称
                    "brand_name": "BestTech",
                    # 产品图片链接 [原字段 'pic_url']
                    "image_url": "https://image.distributetop.com/****.jpeg",
                    # 是否为组合产品 (0: 否, 1: 是) [原字段 'is_combo']
                    "is_bundled": 0,
                    # 组合产品所包含的单品列表 [原字段 'combo_product_list']
                    "bundle_items": [
                        {
                            # 领星本地SKU [原字段 'sku']
                            "lsku": "SKU********",
                            # 领星本地产品ID
                            "product_id": 1,
                            # 产品数量 [原字段 'quantity']
                            "product_qty": 100,
                        },
                        ...
                    ],
                    # 产品状态 (0: 停售, 1: 在售, 2: 开发中, 3: 清仓) [原字段 'status']
                    "status": 1,
                    # 产品型号 [原字段 'model']
                    "product_model": "AO-1234",
                    # 产品单位 [原字段 'unit']
                    "product_unit": "套",
                    # 产品描述 [原字段 'description']
                    "product_description": "<p>AO-1234</p>",
                    # 产品图片列表 [原字段 'picture_list']
                    "product_images": [
                        {
                            # 图片链接 [原字段 'pic_url']
                            "image_url": "https://image.distributetop.com/****.jpeg",
                            # 是否为主图 (0: 否, 1: 是)
                            "is_primary": 1,
                        },
                        ...
                    ],
                    # 产品特殊属性列表 [原字段 'special_attr']
                    # (1: 含电, 2: 纯电, 3: 液体, 4: 粉末, 5: 膏体, 6: 带磁)
                    "product_special_attrs": [3],
                    # 产品开发者用户ID (Account.user_id) [原字段 'product_developer_uid']
                    "product_developer_id": 1,
                    # 产品开发者姓名 (Account.display_name) [原字段 'product_developer']
                    "product_developer_name": "超级管理员",
                    # 产品采购人姓名 (Account.display_name) [原字段 'cg_opt_username']
                    "purchase_staff_name": "超级管理员",
                    # 采购交期 (单位: 天) [原字段 'cg_delivery']
                    "purchase_delivery_time": 14,
                    # 采购价格货币代码 [原字段 'currency']
                    "purchase_currency_code": "USD",
                    # 采购价格 [原字段 'cg_price']
                    "purchase_price": 100.0,
                    # 采购备注 [原字段 'purchase_remark']
                    "purchase_note": "",
                    # 采购产品材质 [原字段 'cg_product_material']
                    "product_material": "塑料",
                    # 采购产品总重 (单位: G) [原字段 'cg_product_gross_weight']
                    "product_gross_weight": 18.0,
                    # 采购产品净重 (单位: G) [原字段 'cg_product_net_weight']
                    "product_net_weight": 180.0,
                    # 采购产品长度 (单位: CM) [原字段 'cg_product_length']
                    "product_length": 7.5,
                    # 采购产品宽度 (单位: CM) [原字段 'cg_product_width']
                    "product_width": 7.5,
                    # 采购产品高度 (单位: CM) [原字段 'cg_product_height']
                    "product_height": 7.0,
                    # 采购包装长度 (单位: CM) [原字段 'cg_package_length']
                    "package_length": 7.5,
                    # 采购包装宽度 (单位: CM) [原字段 'cg_package_width']
                    "package_width": 7.5,
                    # 采购包装高度 (单位: CM) [原字段 'cg_package_height']
                    "package_height": 7.0,
                    # 采购外箱重量 (单位: KG) [原字段 'cg_box_weight']
                    "box_weight": 18.0,
                    # 采购外箱长度 (单位: CM) [原字段 'cg_box_length']
                    "box_length": 50.0,
                    # 采购外箱宽度 (单位: CM) [原字段 'cg_box_width']
                    "box_width": 50.0,
                    # 采购外箱高度 (单位: CM) [原字段 'cg_box_height']
                    "box_height": 50.0,
                    # 采购外箱数量 [原字段 'cg_box_pcs']
                    "box_qty": 1,
                    # 供应商报价信息列表 [原字段 'supplier_quote']
                    "supplier_quotes": [
                        {
                            # 领星本地产品ID
                            "product_id": 4*****,
                            # 供应商ID
                            "supplier_id": 6***,
                            # 供应商名称
                            "supplier_name": "遵*****",
                            # 供应商编码
                            "supplier_code": "SU*****",
                            # 供应商等级 [原字段 'level_text']
                            "supplier_level": "",
                            # 供应商员工数 [原字段 'employees_text']
                            "supplier_employees": "",
                            # 供应商产品链接 [原字段 'supplier_product_url']
                            "supplier_product_urls": [],
                            # 供应商备注 [原字段 'remark']
                            "supplier_note": "",
                            # 是否是首选供应商 (0: 否, 1: 是) [原字段 'is_primary']
                            "is_primary_supplier": 1,
                            # 报价ID [原字段 'psq_id']
                            "quote_id": 21****************,
                            # 报价货币符号 [原字段 'cg_currency_icon']
                            "quote_currency_icon": "￥",
                            # 报价单价 [原字段 'cg_price']
                            "quote_price": 100.0,
                            # 报价交期 (单位: 天) [原字段 'quote_cg_delivery']
                            "quote_delivery_time": 14,
                            # 报价备注 [原字段 'quote_remark']
                            "quote_note": "",
                            # 报价列表 [原字段 'quotes']
                            "quotes": [
                                {
                                    # 报价货币代码 [原字段 'currency']
                                    "currency_code": "CNY",
                                    # 报价货币符号
                                    "currency_icon": "￥",
                                    # 报价是否含税 (0: 否, 1: 是) [原字段 'is_tax']
                                    "is_tax_inclusive": 1,
                                    # 报价税率 (百分比)
                                    "tax_rate": 5.0,
                                    # 报价梯度 [原字段 'step_prices']
                                    "price_tiers": [
                                        {
                                            # 最小订购量
                                            "moq": 100,
                                            # 报价 (不含税) [原字段 'price']
                                            "price_excl_tax": 100.0,
                                            # 报价 (含税)
                                            "price_with_tax": 105.0,
                                        },
                                        ...
                                    ],
                                },
                                ...
                            ],
                        },
                        ...
                    ],
                    # 报关申报品名 (出口国) [原字段 'bg_customs_export_name']
                    "customs_export_name": "香薰机",
                    # 报关申报HS编码 (出口国) [原字段 'bg_export_hs_code']
                    "customs_export_hs_code": "8*********",
                    # 报关申报品名 (进口国) [原字段 'bg_customs_import_name']
                    "customs_import_name": "Essential oil diffuser",
                    # 报关申报单价 (进口国) [原字段 'bg_customs_import_price']
                    "customs_import_price": 1.2,
                    # 报关申报HS编码 (进口国) [原字段 'bg_import_hs_code']
                    "customs_import_hs_code": "",
                    # 报关信息 [原字段 'declaration']
                    "customs_declaration": {
                        # 报关申报品名 (出口国) [原字段 'customs_export_name']
                        "export_name": "",
                        # 报关申报HS编码 (出口国) [原字段 'customs_declaration_hs_code']
                        "export_hs_code": "",
                        # 报关申报品名 (进口国) [原字段 'customs_import_name']
                        "import_name": "",
                        # 报关申报单价 (进口国) [原字段 'customs_import_price']
                        "import_price": 1.2,
                        # 报关申报单价货币代码 (进口国) [原字段 'customs_import_price_currency']
                        "currency_code": "USD",
                        # 报关申报单价货币符号 (进口国) [原字段 'customs_import_price_currency_icon']
                        "currency_icon": "",
                        # 报关申报产品单位 [原字段 'customs_declaration_unit']
                        "unit": "套",
                        # 报关申报产品规格 [原字段 'customs_declaration_spec']
                        "specification": "香薰机",
                        # 报关申报产品原产地 [原字段 'customs_declaration_origin_produce']
                        "country_of_origin": "中国",
                        # 报关申报内陆来源 [原字段 'customs_declaration_inlands_source']
                        "source_from_inland": "中国",
                        # 报关申报免税 [原字段 'customs_declaration_exempt']
                        "exemption": "",
                        # 其他申报要素 [原字段 'other_declare_element']
                        "other_details": "",
                    },
                    "customs_clearance": {
                        # 清关内部编码 [原字段 'customs_clearance_internal_code']
                        "internal_code": "",
                        # 清关产品材质 [原字段 'customs_clearance_material']
                        "material": "",
                        # 清关产品用途 [原字段 'customs_clearance_usage']
                        "usage": "",
                        # 清关是否享受优惠 [原字段 'customs_clearance_preferential']
                        # (0: 未设置, 1: 不享惠, 2: 享惠, 3: 不确定)
                        "preferential": 2,
                        # 清关是否享受优惠描述 [原字段 'customs_clearance_preferential_text']
                        "preferential_desc": "",
                        # 清关品牌类型 [原字段 'customs_clearance_brand_type']
                        # (0: 未设置, 1: 无品牌, 2: 境内品牌[自主], 3: 境内品牌[收购], 4: 境外品牌[贴牌], 5: 境外品牌[其他])
                        "brand_type": 2,
                        # 清关品牌类型描述 [原字段 'customs_clearance_brand_type_text']
                        "brand_type_desc": "",
                        # 清关产品型号 [原字段 'customs_clearance_product_pattern']
                        "model": "香薰机",
                        # 清关产品图片链接 [原字段 'customs_clearance_pic_url']
                        "image_url": "https://image.umaicloud.com/****.jpg",
                        # 配货备注 [原字段 'allocation_remark']
                        "allocation_note": "",
                        # 织造类型 (0: 未设置, 1: 针织, 2: 梭织) [原字段 'weaving_mode']
                        "fabric_type": 0,
                        # 织造类型描述 [原字段 'weaving_mode_text']
                        "fabric_type_desc": "",
                        # 清关申报单价货币代码 [原字段 'customs_clearance_price_currency']
                        "clearance_currency_code": "CNY",
                        # 清关申报单价货币符号 [原字段 'customs_clearance_price_currency_icon']
                        "clearance_currency_icon": "",
                        # 清关申报单价 [原字段 'customs_clearance_price']
                        "clearance_price": 8.4,
                        # 清关税率 [原字段 'customs_clearance_tax_rate']
                        "clearance_tax_rate": 0.0,
                        # 清关HS编码 [原字段 'customs_clearance_hs_code']
                        "clearance_hs_code": "8*********",
                        # 清关备注 [原字段 'customs_clearance_remark']
                        "clearance_note": "",
                    },
                    "operators": [
                        {
                            # 负责人帐号ID (Account.user_id) [原字段 'permission_uid']
                            "user_id": 1,
                            # 负责人姓名 (Account.display_name) [原字段 'permission_user_name']
                            "user_name": "超级管理员",
                        },
                        ...
                    ],
                    # 产品标签列表 [原字段 'global_tags']
                    "tags": [
                        {
                            # 领星标签ID (GlobalTag.tag_id) [原字段 'global_tag_id']
                            "tag_id": "9*****************",
                            # 领星标签名称 (GlobalTag.tag_name) [原字段 'tag_name']
                            "tag_name": "重点款",
                            # 领星标签颜色 (如: "#FF0000") [原字段 'color']
                            "tag_color": "#3BB84C",
                        },
                        ...
                    ],
                    # 产品附件ID [原字段 'attachment_id']
                    "attachment_ids": [],
                    # 自定义字段
                    "custom_fields": [
                        {
                            # 自定义字段ID
                            "field_id": "20************",
                            # 自定义字段名称
                            "field_name": "字段名",
                            # 自定义字段值
                            "field_value": "字段值",
                        },
                        ...
                    ],
                },
                ...
            ]
        ```
        """
        url = route.PRODUCT_DETAILS
        # 解析并验证参数
        args = {
            "lskus": lskus,
            "sku_identifiers": sku_identifiers,
            "product_ids": product_ids,
        }
        try:
            p = param.ProductDetails.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.ProductDetails.model_validate(data)

    async def EnableProducts(self, *product_ids: int) -> base_schema.ResponseResult:
        """批量启用领星本地产品

        ## Docs
        - 产品: [产品启用、禁用](https://apidoc.lingxing.com/#/docs/Product/productOperateBatch)

        :param *product_ids `<'int'>`: 领星本地产品ID, 参数来源 `Product.product_id`
        :returns `<'ResponseResult'>`: 返回启用产品结果
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
            "data": None
        }
        ```
        """
        url = route.ENABLE_DISABLE_PRODUCTS
        # 解析并验证参数
        try:
            ids = utils.validate_array_of_unsigned_int(
                product_ids, "领星本地产品ID product_ids"
            )
        except Exception as err:
            raise errors.InvalidParametersError(
                err, url, {"product_ids": product_ids}
            ) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body={"batch_status": "Enable", "product_ids": ids}
        )
        return base_schema.ResponseResult.model_validate(data)

    async def DisableProducts(self, *product_ids: int) -> base_schema.ResponseResult:
        """批量禁用领星本地产品

        ## Docs
        - 产品: [产品启用、禁用](https://apidoc.lingxing.com/#/docs/Product/productOperateBatch)

        :param *product_ids `<'int'>`: 领星本地产品ID, 参数来源 `Product.product_id`
        :returns `<'ResponseResult'>`: 返回禁用产品结果
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
            "data": None
        }
        ```
        """
        url = route.ENABLE_DISABLE_PRODUCTS
        # 解析并验证参数
        try:
            ids = utils.validate_array_of_unsigned_int(
                product_ids, "领星本地产品ID product_ids"
            )
        except Exception as err:
            raise errors.InvalidParametersError(
                err, url, {"product_ids": product_ids}
            ) from err

        # 发送请求
        data = await self._request_with_sign(
            "POST", url, body={"batch_status": "Disable", "product_ids": ids}
        )
        return base_schema.ResponseResult.model_validate(data)

    async def EditProduct(
        self,
        lsku: str,
        product_name: str,
        *,
        sku_identifier: str | None = None,
        category_id: int | None = None,
        category_name: str | None = None,
        brand_id: int | None = None,
        brand_name: str | None = None,
        product_model: str | None = None,
        product_unit: str | None = None,
        product_description: str | None = None,
        product_images: dict | list[dict] | None = None,
        product_special_attrs: int | list[int] | None = None,
        status: int | None = None,
        bundle_items: dict | list[dict] | None = None,
        auto_bundle_purchase_price: int | None = None,
        product_creator_id: int | None = None,
        product_developer_id: int | None = None,
        product_developer_name: str | None = None,
        purchase_staff_id: int | None = None,
        purchase_staff_name: str | None = None,
        purchase_delivery_time: int | None = None,
        purchase_price: int | float | None = None,
        purchase_note: str | None = None,
        product_material: str | None = None,
        product_gross_weight: int | float | None = None,
        product_net_weight: int | float | None = None,
        product_length: int | float | None = None,
        product_width: int | float | None = None,
        product_height: int | float | None = None,
        package_length: int | float | None = None,
        package_width: int | float | None = None,
        package_height: int | float | None = None,
        box_weight: int | float | None = None,
        box_length: int | float | None = None,
        box_width: int | float | None = None,
        box_height: int | float | None = None,
        box_qty: int | None = None,
        supplier_quotes: dict | list[dict] | None = None,
        customs_export_name: str | None = None,
        customs_export_hs_code: str | None = None,
        customs_import_name: str | None = None,
        customs_import_price: int | float | None = None,
        customs_import_currency_code: str | None = None,
        customs_declaration: dict | None = None,
        customs_clearance: dict | None = None,
        operator_ids: int | list[int] | None = None,
        operator_update_mode: int | None = None,
    ) -> schema.EditProductResult:
        """添加/编辑本地产品

        ## Docs
        - 产品: [添加/编辑本地产品](https://apidoc.lingxing.com/#/docs/Product/SetProduct)

        ## Notice
        - 默认参数 `None` 表示留空或不修改, 只有传入的对应参数才会被更新
        - 这点不同于 `EditSpuProduct` 方法, 其默认参数 `None` 表示重置设置,
          所有没有传入的参数都将被重置为默认值

        :param lsku `<'str'>`: 领星本地SKU, 参数来源 `Product.lsku`
        :param product_name `<'str'>`: 领星本地产品名称, 参数来源 `Product.product_name`
        :param sku_identifier `<'str'>`: 领星本地SKU识别码,
            默认 `None` (留空或不修改), 不支持清除设置
        :param category_id `<'int'>`: 领星本地产品分类ID (当ID与名称同时存在时, ID优先),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param category_name `<'str'>`: 领星本地产品分类名称,
            默认 `None` (留空或不修改)
        :param brand_id `<'int'>`: 领星本地产品品牌ID (当ID与名称同时存在时, ID优先),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param brand_name `<'str'>`: 领星本地产品品牌名称,
            默认 `None` (留空或不修改)
        :param product_model `<'str'>`: 产品型号,
            默认 `None` (留空或不修改), 传入空字符串清除设置
        :param product_unit `<'str'>`: 产品单位,
            默认 `None` (留空或不修改), 传入空字符串清除设置
        :param product_description `<'str'>`: 产品描述,
            默认 `None` (留空或不修改), 传入空字符串清除设置
        :param product_images `<'dict/list[dict]'>`: 产品图片列表,
            默认 `None` (留空或不修改), 传入空列表清除设置

            - 每个字典必须包含 `image_url` 和 `is_primary` 字段:
            - 必填字段 `image_url` 图片链接, 必须为 str 类型
            - 必填字段 `is_primary` 是否为主图, 必须为 int 类型 (0: 否, 1: 是)

        :param product_special_attrs `<'int/list[int]'>`: 产品特殊属性
            (1: 含电, 2: 纯电, 3: 液体, 4: 粉末, 5: 膏体, 6: 带磁),
            默认 `None` (留空或不修改), 传入空列表清除设置
        :param status `<'int'>`: 产品状态 (0: 停售, 1: 在售, 2: 开发中, 3: 清仓),
            默认 `None` (默认1或不修改)
        :param bundle_items `<'dict/list[dict]'>`: 组合产品所包含的单品列表,
            默认 `None` (留空或不修改), 传入空列表清除设置

            - 每个字典必须包含 `lsku` 和 `product_qty` 字段:
            - 必填字段 `lsku` 领星本地SKU, 必须为 str 类型
            - 必填字段 `product_qty` 子产品数量, 必须为 int 类型

        :param auto_bundle_purchase_price `<'int'>`: 是否自动计算组合产品采购价格
            (0: 手动, 1: 自动 | 选择自动后, 组合产品采购价格为所包含单品成本的总计),
            默认 `None` (默认0或不修改)
        :param product_creator_id `<'int'>`: 产品创建人ID,
            默认 `None` (默认API账号ID或不修改)
        :param product_developer_id `<'int'>`: 产品开发者用户ID (当ID与名称同时存在时, ID优先),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param product_developer_name `<'str'>`: 产品开发者姓名,
            默认 `None` (留空或不修改), 传入空字符串清除设置
        :param purchase_staff_id `<'int'>`: 产品采购人用户ID (当ID与名称同时存在时, ID优先),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param purchase_staff_name `<'str'>`: 产品采购人姓名,
            默认 `None` (留空或不修改), 传入空字符串清除设置
        :param purchase_delivery_time `<'int'>`: 采购交期 (单位: 天),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param purchase_price `<'int/float'>`: 采购价格,
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param purchase_note `<'str'>`: 采购备注,
            默认 `None` (留空或不修改), 传入空字符串清除设置
        :param product_material `<'str'>`: 采购产品材质,
            默认 `None` (留空或不修改), 传入空字符串清除设置
        :param product_gross_weight `<'int/float'>`: 采购产品总重 (单位: G),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param product_net_weight `<'int/float'>`: 采购产品净重 (单位: G),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param product_length `<'int/float'>`: 采购产品长度 (单位: CM),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param product_width `<'int/float'> : 采购产品宽度 (单位: CM),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param product_height `<'int/float'>`: 采购产品高度 (单位: CM),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param package_length `<'int/float'>`: 采购包装长度 (单位: CM),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param package_width `<'int/float'>`: 采购包装宽度 (单位: CM),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param package_height `<'int/float'>`: 采购包装高度 (单位: CM),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param box_weight `<'int/float'>`: 采购外箱重量 (单位: KG),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param box_length `<'int/float'>`: 采购外箱长度 (单位: CM),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param box_width `<'int/float'>`: 采购外箱宽度 (单位: CM),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param box_height `<'int/float'>`: 采购外箱高度 (单位: CM),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param box_qty `<'int'>`: 采购外箱数量,
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param supplier_quotes `<'dict/list[dict]'>`: 供应商报价信息列表,
            默认 `None` (留空或不修改), 传入空列表清除设置

            - 每个字典必须包含 `supplier_id`, `is_primary` 和 `quotes` 字段:
            - 必填字段 `supplier_id` 供应商ID, 必须为 int 类型, 参数来源 `Supplier.supplier_id`
            - 必填字段 `is_primary` 是否为首选供应商, 必须为 int 类型 (0: 否, 1: 是)
            - 必填字段 `quotes` 报价列表, 必须为 list[dict] 类型, 每个字典必须包含以下字段:
                * 必填字段 `quotes.currency_code` 报价货币代码, 必须为 str 类型
                * 必填字段 `quotes.is_tax_inclusive` 报价是否含税, 必须为 int 类型 (0: 否, 1: 是)
                * 必填字段 `quotes.price_tiers` 报价梯度, 必须为 list[dict] 类型, 每个字典必须包含以下字段:
                    - 必填字段 `quotes.price_tiers.moq` 最小订购量, 必须为 int 类型
                    - 必填字段 `quotes.price_tiers.price_with_tax` 报价 (含税), 必须为 int/float 类型
                * 选填字段 `quotes.tax_rate` 报价税率 (百分比), 如 5% 则传 5, 必须为 int/float 类型
            - 选填字段 `quote_note` 报价备注, 必须为 str 类型
            - 选填字段 `product_urls` 供应商产品链接, 必须为 list[str] 类型

        :param customs_export_name `<'str'>`: 报关申报品名 (出口国),
            默认 `None` (留空或不修改), 传入空字符串清除设置
        :param customs_export_hs_code `<'str'>`: 报关申报HS编码 (出口国),
            默认 `None` (留空或不修改), 传入空字符串清除设置
        :param customs_import_name `<'str'>`: 报关申报品名 (进口国),
            默认 `None` (留空或不修改), 传入空字符串清除设置
        :param customs_import_price `<'int/float'>`: 报关申报单价 (进口国),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param customs_import_currency_code `<'str'>`: 报关申报单价货币代码 (进口国),
            默认 `None` (留空或不修改), 传入空字符串清除设置
        :param customs_declaration `<'dict'>`: 报关信息,
            默认 `None` (留空或不修改)

            - 字典可选填字段:
            - 选填字段 `unit` 报关申报产品单位, 必须为 str 类型, 传入空字符串清除设置
            - 选填字段 `specification` 报关申报产品规格, 必须为 str 类型, 传入空字符串清除设置
            - 选填字段 `country_of_origin` 报关申报产品原产地, 必须为 str 类型, 传入空字符串清除设置
            - 选填字段 `source_from_inland` 报关申报内陆来源, 必须为 str 类型, 传入空字符串清除设置
            - 选填字段 `exemption` 报关申报免税, 必须为 str 类型, 传入空字符串清除设置

        :param customs_clearance `<'dict'>`: 清关信息,
            默认 `None` (留空或不修改)

            - 字典可选填字段:
            - 选填字段 `internal_code` 清关内部编码, 必须为 str 类型, 传入空字符串清除设置
            - 选填字段 `material` 清关产品材质, 必须为 str 类型, 传入空字符串清除设置
            - 选填字段 `usage` 清关产品用途, 必须为 str 类型, 传入空字符串清除设置
            - 选填字段 `preferential` 清关是否享受优惠, 必须为 int 类型
              (0: 未设置, 1: 不享惠, 2: 享惠, 3: 不确定), 传入 `0` 清除设置
            - 选填字段 `brand_type` 清关品牌类型, 必须为 int 类型,
              (0: 未设置, 1: 无品牌, 2: 境内品牌[自主], 3: 境内品牌[收购], 4: 境外品牌[贴牌], 5: 境外品牌[其他]),
              传入 `0` 清除设置
            - 选填字段 `model` 清关产品型号, 必须为 str 类型, 传入空字符串清除设置
            - 选填字段 `image_url` 清关产品图片链接, 必须为 str 类型, 传入空字符串清除设置
            - 选填字段 `allocation_note` 配货备注, 必须为 str 类型, 传入空字符串清除设置
            - 选填字段 `fabric_type` 织造类型, 必须为 int 类型 (0: 未设置, 1: 针织, 2: 梭织), 传入 `0` 清除设置

        :param operator_ids `<'int/list[int]'>`: 负责人帐号ID列表 (Account.user_id),
            默认 `None` (留空或不修改)
        :param operator_update_mode `<'int'>`: 负责人ID的更新模式 (0: 覆盖, 1: 追加),
            默认 `None` 追加模式
        :returns `<'EditProductResult'>`: 返回编辑产品的结果
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
                # 领星本地产品SKU [原字段 'sku']
                "lsku": "SKU*******",
                # 领星本地产品SKU识别码
                "sku_identifier": "SN*******",
                # 领星本地产品ID
                "product_id": 1,
            },
        }
        ```
        """
        url = route.EDIT_PRODUCT
        # 解析并验证参数
        args = {
            "lsku": lsku,
            "product_name": product_name,
            "sku_identifier": sku_identifier,
            "category_id": category_id,
            "category_name": category_name,
            "brand_id": brand_id,
            "brand_name": brand_name,
            "product_model": product_model,
            "product_unit": product_unit,
            "product_description": product_description,
            "product_images": product_images,
            "product_special_attrs": product_special_attrs,
            "status": status,
            "bundle_items": bundle_items,
            "auto_bundle_purchase_price": auto_bundle_purchase_price,
            "product_creator_id": product_creator_id,
            "product_developer_id": product_developer_id,
            "product_developer_name": product_developer_name,
            "purchase_staff_id": purchase_staff_id,
            "purchase_staff_name": purchase_staff_name,
            "purchase_delivery_time": purchase_delivery_time,
            "purchase_price": purchase_price,
            "purchase_note": purchase_note,
            "product_material": product_material,
            "product_gross_weight": product_gross_weight,
            "product_net_weight": product_net_weight,
            "product_length": product_length,
            "product_width": product_width,
            "product_height": product_height,
            "package_length": package_length,
            "package_width": package_width,
            "package_height": package_height,
            "box_weight": box_weight,
            "box_length": box_length,
            "box_width": box_width,
            "box_height": box_height,
            "box_qty": box_qty,
            "supplier_quotes": supplier_quotes,
            "customs_export_name": customs_export_name,
            "customs_export_hs_code": customs_export_hs_code,
            "customs_import_name": customs_import_name,
            "customs_import_price": customs_import_price,
            "customs_import_currency_code": customs_import_currency_code,
            "customs_declaration": customs_declaration,
            "customs_clearance": customs_clearance,
            "operator_ids": operator_ids,
            "operator_update_mode": operator_update_mode,
        }
        try:
            p = param.EditProduct.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.EditProductResult.model_validate(data)

    async def SpuProducts(
        self,
        *,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.SpuProducts:
        """查询SPU多属性产品

        ## Docs
        - 产品: [查询多属性产品列表](https://apidoc.lingxing.com/#/docs/Product/spuList)

        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 最大值200, 默认 `None` (使用: 20)
        :returns `<'SpuProducts'>`: 返回查询到的SPU多属性产品列表
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
                    # 领星SPU多属性产品ID [原字段 'ps_id']
                    "spu_id": 1,
                    # 领星SPU多属性产品编码
                    "spu": "SPU*******",
                    # 领星SPU多属性产品名称
                    "spu_name": "P*********",
                    # 领星本地产品分类ID [原字段 'cid']
                    "category_id": 0,
                    # 领星本地产品品牌ID [原字段 'bid']
                    "brand_id": 0,
                    # 产品型号 [原字段 'model']
                    "product_model": "香薰机",
                    # 产品开发者用户ID (Account.user_id) [原字段 'developer_uid']
                    "product_developer_id": 10******,
                    # 产品采购人用户ID (Account.user_id) [原字段 'cg_uid']
                    "purchase_staff_id": 10******,
                    # 采购交期 (单位: 天) [原字段 'cg_delivery']
                    "purchase_delivery_time": 14,
                    # 采购成本 [原字段 'cg_price']
                    "purchase_price": 100.0,
                    # 采购备注 [原字段 'purchase_remark']
                    "purchase_note": "采购备注",
                    # 创建人用户ID (Account.user_id) [原字段 'create_uid']
                    "create_user_id": 10******,
                    # 创建时间 (北京时间)
                    "create_time": "2025-07-25 16:12:28",
                    # 产品状态 (0: 停售, 1: 在售, 2: 开发中, 3: 清仓)
                    "status": 1,
                },
                ...
            ],
        }
        ```
        """
        url = route.SPU_PRODUCTS
        # 解析并验证参数
        args = {"offset": offset, "length": length}
        try:
            p = base_param.PageOffestAndLength.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SpuProducts.model_validate(data)

    async def SpuProductDetail(
        self,
        spu_id: int,
        spu: str,
    ) -> schema.SpuProductDetailData:
        """查询SPU多属性产品详情

        ## Docs
        - 产品: [查询多属性产品详情](https://apidoc.lingxing.com/#/docs/Product/spuInfo)

        :param spu_id `<'int'>`: 领星SPU多属性产品ID, 参数来源 `SpuProduct.spu_id`
        :param spu `<'str'>`: 领星SPU多属性产品编码, 参数来源 `SpuProduct.spu`
        :returns `<'SpuProductDetailData'>`: 返回查询到的SPU多属性产品详情
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
                # 领星SPU多属性产品ID [原字段 'ps_id']
                "spu_id": 1,
                # 领星SPU多属性产品编码
                "spu": "SPU*******",
                # 领星SPU多属性产品名称
                "spu_name": "P*********",
                # 领星本地产品分类ID [原字段 'cid']
                "category_id": 0,
                # 领星本地产品分类名称
                "category_name": "",
                # 领星本地产品品牌ID [原字段 'bid']
                "brand_id": 0,
                # 领星本地产品品牌名称
                "brand_name": "",
                # 产品图片链接 [原字段 'pic_url']
                "image_url": "https://image.distributetop.com/****.jpeg",
                # 产品状态 (0: 停售, 1: 在售, 2: 开发中, 3: 清仓) [原字段 'status']
                "status": 1,
                # 产品状态描述 [原字段 'status_text']
                "status_desc": "在售",
                # 产品型号 [原字段 'model']
                "product_model": "AOP-1234",
                # 产品单位 [原字段 'unit']
                "product_unit": "套",
                # 产品描述 [原字段 'description']
                "product_description": "",
                # 创建者用户ID (Account.user_id) [原字段 'create_uid']
                "product_creator_id": 10******,
                # 创建者姓名 (Account.display_name) [原字段 'create_user']
                "product_creator_name": "超级管理员",
                # 产品开发者用户ID (Account.user_id) [原字段 'developer_uid']
                "product_developer_id": 10******,
                # 产品开发者姓名 (Account.display_name) [原字段 'developer']
                "product_developer_name": "超级管理员",
                # 产品负责人用户ID列表 (Account.user_id) [原字段 'product_duty_uids']
                "operator_ids": [10******],
                # 产品负责人用户信息列表 [原字段 'product_duty_users']
                "operators": [{"user_id": 10******, "user_name": "超级管理员"}],
                # 产品采购信息
                "purchase_info": {
                    # 产品采购人用户ID (Account.user_id) [原字段 'cg_uid']
                    "purchase_staff_id": 10******,
                    # 产品采购人姓名 (Account.display_name) [原字段 'cg_user']
                    "purchase_staff_name": "超级管理员",
                    # 采购交期 (单位: 天) [原字段 'cg_delivery']
                    "purchase_delivery_time": 14,
                    # 采购价格 [原字段 'cg_price']
                    "purchase_price": 100.0,
                    # 采购备注 [原字段 'purchase_remark']
                    "purchase_note": "采购备注",
                    # 采购产品材质 [原字段 'cg_product_material']
                    "product_material": "塑料",
                    # 采购产品公制总重 [原字段 'cg_product_gross_weight']
                    "product_gross_weight_metric": 100.0,
                    # 采购产品公制总重单位 [原字段 'cg_product_gross_weight_unit']
                    "product_gross_weight_metric_unit": "g",
                    # 采购产品英制总重 [原字段 'cg_product_gross_weight_in']
                    "product_gross_weight_imperial": 0.22,
                    # 采购产品总重英制单位 [原字段 'cg_product_gross_weight_in_unit']
                    "product_gross_weight_imperial_unit": "lb",
                    # 采购产品公制净重 [原字段 'cg_product_net_weight']
                    "product_net_weight_metric": 100.0,
                    # 采购产品公制净重单位 [原字段 'cg_product_net_weight_unit']
                    "product_net_weight_metric_unit": "g",
                    # 采购产品英制净重 [原字段 'cg_product_net_weight_in']
                    "product_net_weight_imperial": 0.22,
                    # 采购产品净重英制单位 [原字段 'cg_product_net_weight_in_unit']
                    "product_net_weight_imperial_unit": "lb",
                    # 采购产品公制长度 [原字段 'cg_product_length']
                    "product_length_metric": 10.0,
                    # 采购产品英制长度 [原字段 'cg_product_length_in']
                    "product_length_imperial": 3.94,
                    # 采购产品公制宽度 [原字段 'cg_product_width']
                    "product_width_metric": 10.0,
                    # 采购产品英制宽度 [原字段 'cg_product_width_in']
                    "product_width_imperial": 3.94,
                    # 采购产品公制高度 [原字段 'cg_product_height']
                    "product_height_metric": 10.0,
                    # 采购产品英制高度 [原字段 'cg_product_height_in']
                    "product_height_imperial": 3.94,
                    # 采购包装公制长度 [原字段 'cg_package_length']
                    "package_length_metric": 10.0,
                    # 采购包装英制长度 [原字段 'cg_package_length_in']
                    "package_length_imperial": 3.94,
                    # 采购包装公制宽度 [原字段 'cg_package_width']
                    "package_width_metric": 10.0,
                    # 采购包装英制宽度 [原字段 'cg_package_width_in']
                    "package_width_imperial": 3.94,
                    # 采购包装公制高度 [原字段 'cg_package_height']
                    "package_height_metric": 10.0,
                    # 采购包装英制高度 [原字段 'cg_package_height_in']
                    "package_height_imperial": 3.94,
                    # 采购外箱公制重量 [原字段 'cg_box_weight']
                    "box_weight_metric": 100.0,
                    # 采购外箱公制重量单位 [原字段 'cg_box_weight_unit']
                    "box_weight_metric_unit": "kg",
                    # 采购外箱英制重量 [原字段 'cg_box_weight_in']
                    "box_weight_imperial": 220.46,
                    # 采购外箱英制重量单位 [原字段 'cg_box_weight_in_unit']
                    "box_weight_imperial_unit": "lb",
                    # 采购外箱公制长度 [原字段 'cg_box_length']
                    "box_length_metric": 10.0,
                    # 采购外箱英制长度 [原字段 'cg_box_length_in']
                    "box_length_imperial": 3.94,
                    # 采购外箱公制宽度 [原字段 'cg_box_width']
                    "box_width_metric": 10.0,
                    # 采购外箱英制宽度 [原字段 'cg_box_width_in']
                    "box_width_imperial": 3.94,
                    # 采购外箱公制高度 [原字段 'cg_box_height']
                    "box_height_metric": 10.0,
                    # 采购外箱英制高度 [原字段 'cg_box_height_in']
                    "box_height_imperial": 3.94,
                    # 采购外箱数量 [原字段 'cg_box_pcs']
                    "box_qty": 1,
                },
                # 海关申报信息 [原字段 'logistics']
                "customs_info": {
                    # 基础产品信息 [原字段 'base']
                    "base_info": {
                        # 产品特殊属性 [原字段 'special_attr']
                        "special_attrs": [
                            {
                                # 特殊属性ID [原字段 'id']
                                "special_attr_id": 3,
                                # 特殊属性值 [原字段 'value']
                                "special_attr_value": "液体"
                            },
                            ...
                        ],
                        # 报关申报HS编码 (出口国) [原字段 'bg_export_hs_code']
                        "customs_export_hs_code": "84********",
                    },
                    # 海关报关信息
                    "declaration": {
                        # 报关申报品名 (出口国) [原字段 'customs_export_name']
                        "export_name": "香薰机",
                        # 报关申报HS编码 (出口国) [原字段 'customs_declaration_hs_code']
                        "export_hs_code": "84********",
                        # 报关申报品名 (进口国) [原字段 'customs_import_name']
                        "import_name": "Vaper",
                        # 报关申报单价 (进口国) [原字段 'customs_import_price']
                        "import_price": 1.2,
                        # 报关申报单价货币代码 (进口国) [原字段 'customs_import_price_currency']
                        "currency_code": "USD",
                        # 报关申报单价货币符号 (进口国) [原字段 'customs_import_price_currency_icon']
                        "currency_icon": "$",
                        # 报关申报产品单位 [原字段 'customs_declaration_unit']
                        "unit": "套",
                        # 报关申报产品规格 [原字段 'customs_declaration_spec']
                        "specification": "香薰机",
                        # 报关申报产品原产地 [原字段 'customs_declaration_origin_produce']
                        "country_of_origin": "中国",
                        # 报关申报内陆来源 [原字段 'customs_declaration_inlands_source']
                        "source_from_inland": "中国",
                        # 报关申报免税 [原字段 'customs_declaration_exempt']
                        "exemption": "",
                        # 其他申报要素 [原字段 'other_declare_element']
                        "other_details": "",
                    },
                    # 海关清关信息
                    "clearance": {
                        # 清关内部编码 [原字段 'customs_clearance_internal_code']
                        "internal_code": "",
                        # 清关产品材质 [原字段 'customs_clearance_material']
                        "material": "",
                        # 清关产品用途 [原字段 'customs_clearance_usage']
                        "usage": "",
                        # 清关是否享受优惠 [原字段 'customs_clearance_preferential']
                        # (0: 未设置, 1: 不享惠, 2: 享惠, 3: 不确定)
                        "preferential": 2,
                        # 清关是否享受优惠描述 [原字段 'customs_clearance_preferential_text']
                        "preferential_desc": "享惠",
                        # 清关品牌类型 [原字段 'customs_clearance_brand_type']
                        # (0: 未设置, 1: 无品牌, 2: 境内品牌[自主], 3: 境内品牌[收购], 4: 境外品牌[贴牌], 5: 境外品牌[其他])
                        "brand_type": 2,
                        # 清关品牌类型描述 [原字段 'customs_clearance_brand_type_text']
                        "brand_type_desc": "境内自主品牌",
                        # 清关产品型号 [原字段 'customs_clearance_product_pattern']
                        "model": "香薰机",
                        # 清关产品图片链接 [原字段 'customs_clearance_pic_url']
                        "image_url": "https://image.umaicloud.com/****.jpg",
                        # 配货备注 [原字段 'allocation_remark']
                        "allocation_note": "",
                        # 织造类型 (0: 未设置, 1: 针织, 2: 梭织) [原字段 'weaving_mode']
                        "fabric_type": 0,
                        # 织造类型描述 [原字段 'weaving_mode_text']
                        "fabric_type_desc": "",
                        # 清关申报单价货币代码 [原字段 'customs_clearance_price_currency']
                        "clearance_currency_code": "CNY",
                        # 清关申报单价货币符号 [原字段 'customs_clearance_price_currency_icon']
                        "clearance_currency_icon": "￥",
                        # 清关申报单价 [原字段 'customs_clearance_price']
                        "clearance_price": 8.4,
                        # 清关税率 [原字段 'customs_clearance_tax_rate']
                        "clearance_tax_rate": 0.0,
                        # 清关HS编码 [原字段 'customs_clearance_hs_code']
                        "clearance_hs_code": "8*********",
                        # 清关备注 [原字段 'customs_clearance_remark']
                        "clearance_note": "",
                    },
                },
                # 关联辅料列表 [原字段 'aux_relation_list']
                "auxiliary_materials": [
                    {
                        # 辅料ID
                        "aux_id": 4*****,
                        # 辅料SKU
                        "aux_sku": "BOX001",
                        # 辅料名称
                        "aux_name": "包装箱",
                        # 辅料备注 [原字段 'remark']
                        "aux_note": "",
                        # 辅料配比数量 [原字段 'aux_qty']
                        "aux_ratio_qty": 1,
                        # 产品配比数据 [原字段 'sku_qty']
                        "sku_ratio_qty": 1,
                        # 辅料采购数量 [原字段 'quantity']
                        "purchase_qty": 100,
                        # 辅料采购价格 [原字段 'cg_price']
                        "purchase_price": 10.0,
                    }
                ],
                # 标准产品列表 [原字段 'sku_list']
                "items": [
                    {
                        # 领星本地SKU [原字段 'sku']
                        "lsku": "SKU*******",
                        # 领星本地产品ID
                        "product_id": 47****,
                        # 领星本地产品名称
                        "product_name": "P*********",
                        # 产品图片链接 [原字段 'pic_url']
                        "image_url": "https://image.distributetop.com/****.jpeg",
                        # 产品图片列表 [原字段 'pic_list']
                        "images": [
                            {
                                # 图片ID [原字段 'pp_id']
                                "image_id": 21****************,
                                # 图片名称 [原字段 'pic_name']
                                "image_name": "****.jpg",
                                # 图片链接 [原字段 'pic_url']
                                "image_url": "https://image.distributetop.com/***.jpeg",
                                # 图片大小 (单位: Byte) [原字段 'pic_space']
                                "image_size": 208636,
                                # 图片宽度 (单位: PX) [原字段 'pic_size_w']
                                "image_width": 1500,
                                # 图片高度 (单位: PX) [原字段 'pic_size_h']
                                "image_height": 1422,
                                # 图片类型 [原字段 'pic_type']
                                "image_type": 1,
                                # 是否为主图 (0: 否, 1: 是)
                                "is_primary": 1,
                                # 领星本地产品ID
                                "product_id": 47****,
                            },
                            ...
                        ],
                        # 产品属性列表 [原字段 'attribute']
                        "attributes": [
                            {
                                # 属性ID [原字段 'pa_id']
                                "attr_id": 1***,
                                # 属性值ID [原字段 'pai_id']
                                "attr_value_id": "4***",
                                # 属性值名称 [原字段 'pai_name']
                                "attr_value_name": "紫色",
                            },
                            ...
                        ],
                    }
                ],
                # 附件信息列表 [原字段 'attachmentFiles']
                "attachments": [
                    {
                        # 文件ID
                        "file_id": "10************",
                        # 文件名称
                        "file_name": "产品说明书.pdf",
                        # 文件类型 (0: 未知, 1: 图片, 2: 压缩包)
                        "file_type": 0,
                        # 文件链接
                        "file_url": "https://file.lingxing.com/****.pdf",
                    },
                    ...
                ],
            },
        }
        ```
        """
        url = route.SPU_PRODUCT_DETAIL
        # 解析并验证参数
        args = {"spu_id": spu_id, "spu": spu}
        try:
            p = param.SpuProductDetail.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.SpuProductDetailData.model_validate(data)

    async def EditSpuProduct(
        self,
        spu: str,
        spu_name: str,
        items: dict | list[dict],
        *,
        category_id: int | None = None,
        brand_id: int | None = None,
        product_model: str | None = None,
        product_unit: str | None = None,
        product_description: str | None = None,
        status: int | None = None,
        product_creator_id: int | None = None,
        product_developer_id: int | None = None,
        operator_ids: int | list[int] | None = None,
        apply_to_new_skus: int | None = None,
        purchase_info: dict | None = None,
        customs_info: dict | None = None,
    ) -> schema.EditSpuProductResult:
        """添加/编辑SPU多属性产品

        ## Docs
        - 产品: [添加/编辑多属性产品](https://apidoc.lingxing.com/#/docs/Product/spuSet)

        ## Notice
        - 默认参数 `None` 表示重置设置, 所有没有传入的参数都将被重置为默认值
        - 这点不同于 `EditProduct` 方法, 其默认参数 `None` 表示留空或不修改,
          只有传入的对应参数才会被更新

        :param spu `<'str'>`: 领星SPU多属性产品编码, 参数来源 `SpuProduct.spu`
        :param spu_name `<'str'>`: 领星SPU多属性产品名称, 参数来源 `SpuProduct.spu_name`
        :param items `<'dict/list[dict]'>`: 子产品字典或列表, 必填项, 参数为覆盖模式

            - 每个字典必须包含 `lsku` 和 `attributes` 字段, 如:
              `{"lsku": "SKU", "attributes": [{"attr_id": 1, "attr_value_id": "4"}]}`
            - 必填字段 `lsku` 领星本地产品SKU, 必须为 str 类型
            - 必填字段 `attributes` 产品属性列表, 必须为 list[dict] 类型, 每个字典必须包含以下字段:
                * 必填字段 `attributes.attr_id` 属性ID, 必须为 int 类型
                * 必填字段 `attributes.attr_value_id` 属性值ID, 必须为 str 类型

        :param category_id `<'int'>`: 领星本地产品分类ID,
            默认 `None`, 不同于 `EditProduct`, 表示重置设置或默认0
        :param brand_id `<'int'>`: 领星本地产品品牌ID,
            默认 `None`, 不同于 `EditProduct`, 表示重置设置或默认0
        :param product_model `<'str'>`: 产品型号,
            默认 `None`, 不同于 `EditProduct`, 表示重置设置或默认空字符串
        :param product_unit `<'str'>`: 产品单位,
            默认 `None`, 不同于 `EditProduct`, 表示重置设置或默认空字符串
        :param product_description `<'str'>`: 产品描述,
            默认 `None`, 不同于 `EditProduct`, 表示重置设置或默认空字符串
        :param status `<'int'>`: 产品状态 (0: 停售, 1: 在售, 2: 开发中, 3: 清仓),
            默认 `None`, 不同于 `EditProduct`, 表示重置为1或默认1
        :param product_creator_id `<'int'>`: 产品创建人ID,
            默认 `None`, 不同于 `EditProduct`, 表示重置为初始创建人ID
        :param product_developer_id `<'int'>`: 产品开发者ID,
            默认 `None`, 不同于 `EditProduct`, 表示重置设置或默认0
        :param operator_ids `<'int/list[int]'>`: 产品负责人帐号ID列表 (Account.user_id),
            默认 `None`, 不同于 `EditProduct`, 表示重置设置或默认空列表
        :param apply_to_new_skus `<'int'>`: 是否应用SPU多属性产品基础信息至新生成的SKU (0: 否, 1: 是),
            默认 `None` 不应用 (0: 否)
        :param purchase_info `<'dict'>`: 产品采购信息,
            默认 `None`, 不同于 `EditProduct`, 表示重置设置或默认设置

            - 字典可选填字段 (覆盖模式, 缺失字段设置将被重置):
            - 可选字段 `purchase_staff_id` 产品采购人用户ID, 必须为 int 类型, 不传重置为0
            - 可选字段 `purchase_delivery_time` 采购交期 (单位: 天), 必须为 int 类型, 不传重置为0
            - 可选字段 `purchase_note` 采购备注, 必须为 str 类型, 不传重置为空字符串
            - 可选字段 `product_material` 采购产品材质, 必须为 str 类型, 不传重置为空字符串
            - 可选字段 `product_gross_weight` 采购产品总重 (单位: G), 必须为 int/float 类型, 不传重置为0
            - 可选字段 `product_net_weight` 采购产品净重 (单位: G), 必须为 int/float 类型, 不传重置为0
            - 可选字段 `product_length` 采购产品长度 (单位: CM), 必须为 int/float 类型, 不传重置为0
            - 可选字段 `product_width` 采购产品宽度 (单位: CM), 必须为 int/float 类型, 不传重置为0
            - 可选字段 `product_height` 采购产品高度 (单位: CM), 必须为 int/float 类型, 不传重置为0
            - 可选字段 `package_length` 采购包装长度 (单位: CM), 必须为 int/float 类型, 不传重置为0
            - 可选字段 `package_width` 采购包装宽度 (单位: CM), 必须为 int/float 类型, 不传重置为0
            - 可选字段 `package_height` 采购包装高度 (单位: CM), 必须为 int/float 类型, 不传重置为0
            - 可选字段 `box_weight` 采购外箱重量 (单位: KG), 必须为 int/float 类型, 不传重置为0
            - 可选字段 `box_length` 采购外箱长度 (单位: CM), 必须为 int/float 类型, 不传重置为0
            - 可选字段 `box_width` 采购外箱宽度 (单位: CM), 必须为 int/float 类型, 不传重置为0
            - 可选字段 `box_height` 采购外箱高度 (单位: CM), 必须为 int/float 类型, 不传重置为0
            - 可选字段 `box_qty` 采购外箱数量, 必须为 int 类型, 不传重置为0

        :param customs_info `<'dict'>`: 海关申报信息,
            默认 `None`, 不同于 `EditProduct`, 表示重置设置或默认设置

            - 字典可选填字段 (覆盖模式, 缺失字段设置将被重置):
            - 可选字段 `base_info` 基础产品信息, 必须为 dict 类型, 不传重置为默认设置
                * 可选字段 `base_info.customs_export_hs_code` 报关申报HS编码 (出口国),
                  必须为 str 类型, 不传重置为空字符串
                * 可选字段 `base_info.special_attrs` 产品特殊属性列表, 必须为 int/list[int] 类型
                  (1: 含电, 2: 纯电, 3: 液体, 4: 粉末, 5: 膏体, 6: 带磁), 不传清除设置
            - 可选字段 `declaration` 海关报关信息, 必须为 dict 类型, 不传重置为默认设置
                * 可选字段 `declaration.export_name` 报关申报品名 (出口国), 必须为 str 类型, 不传重置为空字符串
                * 可选字段 `declaration.import_name` 报关申报品名 (进口国), 必须为 str 类型, 不传重置为空字符串
                * 可选字段 `declaration.import_price` 报关申报单价 (进口国), 必须为 int/float 类型, 不传重置为0
                * 可选字段 `declaration.currency_code` 报关申报单价货币代码 (进口国), 必须为 str 类型, 不传重置为`"USD"`
                * 可选字段 `declaration.unit` 报关申报产品单位, 必须为 str 类型, 不传重置为空字符串
                * 可选字段 `declaration.specification` 报关申报产品规格, 必须为 str 类型, 不传重置为空字符串
                * 可选字段 `declaration.country_of_origin` 报关申报产品原产地, 必须为 str 类型, 不传重置为空字符串
                * 可选字段 `declaration.source_from_inland` 报关申报内陆来源, 必须为 str 类型, 不传重置为空字符串
                * 可选字段 `declaration.exemption` 报关申报免税, 必须为 str 类型, 不传重置为空字符串
            - 可选字段 `clearance` 海关清关信息, 必须为 dict 类型, 不传重置为默认设置
                * 可选字段 `clearance.internal_code` 清关内部编码, 必须为 str 类型, 不传重置为空字符串
                * 可选字段 `clearance.material` 清关产品材质, 必须为 str 类型, 不传重置为空字符串
                * 可选字段 `clearance.usage` 清关产品用途, 必须为 str 类型, 不传重置为空字符串
                * 可选字段 `clearance.preferential` 清关是否享受优惠, 必须为 int 类型
                  (0: 未设置, 1: 不享惠, 2: 享惠, 3: 不确定), 不传重置为0
                * 可选字段 `clearance.brand_type` 清关品牌类型, 必须为 int 类型
                  (0: 未设置, 1: 无品牌, 2: 境内品牌[自主], 3: 境内品牌[收购],
                  4: 境外品牌[贴牌], 5: 境外品牌[其他]), 不传重置为0
                * 可选字段 `clearance.model` 清关产品型号, 必须为 str 类型, 不传重置为空字符串
                * 可选字段 `clearance.image_url` 清关产品图片链接, 必须为 str 类型, 不传重置为空字符串
                * 可选字段 `clearance.allocation_note` 配货备注, 必须为 str 类型, 不传重置为空字符串
                * 可选字段 `clearance.fabric_type` 织造类型, 必须为 int 类型
                  (0: 未设置, 1: 针织, 2: 梭织), 不传重置为0

        :returns `<'EditSpuProductResult'>`: 返回添加/编辑SPU多属性产品的结果
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
                # 领星SPU多属性产品ID [原字段 'ps_id']
                "spu_id": 1,
                # 领星SPU多属性产品列表 [原字段 'sku_list']
                "items": [
                    {
                        # 领星本地SKU [原字段 'sku']
                        "lsku": "SKU*******",
                        # 领星本地产品ID
                        "product_id": 47****,
                    },
                    ...
                ],
            },
        }
        ```
        """
        url = route.EDIT_SPU_PRODUCT
        # 解析并验证参数
        args = {
            "spu": spu,
            "spu_name": spu_name,
            "items": items,
            "category_id": category_id,
            "brand_id": brand_id,
            "product_model": product_model,
            "product_unit": product_unit,
            "product_description": product_description,
            "status": status,
            "product_creator_id": product_creator_id,
            "product_developer_id": product_developer_id,
            "operator_ids": operator_ids,
            "apply_to_new_skus": apply_to_new_skus,
            "purchase_info": purchase_info,
            "customs_info": customs_info,
        }
        try:
            p = param.EditSpuProduct.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.EditSpuProductResult.model_validate(data)

    async def BundleProducts(
        self,
        *,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.BundleProducts:
        """查询领星本地捆绑产品

        ## Docs
        - 产品: [查询捆绑产品关系列表](https://apidoc.lingxing.com/#/docs/Product/bundledProductList)

        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 最大1000, 默认 `None` (使用: 1000)
        :returns `<'BundleProducts'>`: 返回查询到的捆绑产品列表
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
                    # 捆绑产品ID [原字段 'id']
                    "bundle_id": 4*****,
                    # 捆绑产品SKU [原字段 'sku']
                    "bundle_sku": "BUNDLE-SKU",
                    # 捆绑产品名称 [原字段 'product_name']
                    "bundle_name": "P*********",
                    # 捆绑产品采购价 [原字段 'cg_price']
                    "purchase_price": 100.0,
                    # 捆绑产品状态描述 [原字段 'status_text']
                    "status_desc": "在售",
                    # 捆绑产品列表 [原字段 'bundled_products']
                    "items": [
                        {
                            # 子产品SKU [原字段 'sku']
                            "lsku": "SKU*******",
                            # 领星本地子产品ID [原字段 'productId']
                            "product_id": 4*****,
                            # 子产品捆绑数量 [原字段 'bundledQty']
                            "bundle_qty": 1,
                            # 子产品费用比例
                            "cost_ratio": 0.0,
                        },
                        ...
                    ],
                },
                ...
            ],
        }
        ```
        """
        url = route.BUNDLE_PRODUCTS
        # 解析并验证参数
        args = {"offset": offset, "length": length}
        try:
            p = base_param.PageOffestAndLength.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.BundleProducts.model_validate(data)

    async def EditBundleProduct(
        self,
        bundle_sku: str,
        bundle_name: str,
        *,
        items: dict | list[dict] | None = None,
        category_id: int | None = None,
        category_name: str | None = None,
        brand_id: int | None = None,
        brand_name: str | None = None,
        product_model: str | None = None,
        product_unit: str | None = None,
        product_description: str | None = None,
        product_images: dict | list[dict] | None = None,
        product_creator_id: int | None = None,
        product_developer_id: int | None = None,
        product_developer_name: str | None = None,
        operator_ids: int | list[int] | None = None,
        operator_update_mode: int | None = None,
    ) -> schema.EditBundleProductResult:
        """添加/编辑捆绑产品

        ## Docs
        - 产品: [添加/编辑捆绑产品](https://apidoc.lingxing.com/#/docs/Product/SetBundled)

        ## Notice
        - 默认参数 `None` 表示留空或不修改, 只有传入的对应参数才会被更新
        - 这点不同于 `EditSpuProduct` 方法, 其默认参数 `None` 表示重置设置,
          所有没有传入的参数都将被重置为默认值

        :param bundle_sku `<'str'>`: 捆绑产品SKU (BundleProduct.bundle_sku)
        :param bundle_name `<'str'>`: 捆绑产品名称 (BundleProduct.bundle_name)
        :param items `<'dict/list[dict]'>`: 捆绑产品子产品字典或列表,
            新建捆绑产品时为必填项, 修改捆绑产品时选填 (覆盖模式)

            - 每个字典必须包含 `lsku` 和 `bundle_qty` 字段, 如:
              `{"lsku": "SKU", "bundle_qty": 1}`
            - 必填字段 `lsku` 关联的子产品SKU, 必须为 str 类型
            - 必填字段 `bundle_qty` 关联的子产品捆绑数量, 必须为 int 类型
            - 可选字段 `cost_ratio` 关联的子产品费用占比, 必须为 float 类型,
              用于指定子产品在捆绑产品中的费用占比, 若填写则每项必填, 且总和为`1`

        :param category_id `<'int'>`: 领星本地产品分类ID (当ID与名称同时存在时, ID优先),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param category_name `<'str'>`: 领星本地产品分类名称,
            默认 `None` (留空或不修改)
        :param brand_id `<'int'>`: 领星本地产品品牌ID (当ID与名称同时存在时, ID优先),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param brand_name `<'str'>`: 领星本地产品品牌名称,
            默认 `None` (留空或不修改)
        :param product_model `<'str'>`: 产品型号,
            默认 `None` (留空或不修改), 传入空字符串清除设置
        :param product_unit `<'str'>`: 产品单位,
            默认 `None` (留空或不修改), 传入空字符串清除设置
        :param product_description `<'str'>`: 产品描述,
            默认 `None` (留空或不修改), 传入空字符串清除设置
        :param product_images `<'dict/list[dict]'>`: 产品图片列表,
            默认 `None` (留空或不修改), 传入空列表清除设置

            - 每个字典必须包含 `image_url` 和 `is_primary` 字段:
            - 必填字段 `image_url` 图片链接, 必须为 str 类型
            - 必填字段 `is_primary` 是否为主图, 必须为 int 类型 (0: 否, 1: 是)

        :param product_creator_id `<'int'>`: 产品创建人ID,
            默认 `None` (默认API账号ID或不修改)
        :param product_developer_id `<'int'>`: 产品开发者用户ID (当ID与名称同时存在时, ID优先),
            默认 `None` (默认0或不修改), 传入 `0` 清除设置
        :param product_developer_name `<'str'>`: 产品开发者姓名,
            默认 `None` (留空或不修改), 传入空字符串清除设置
        :param operator_ids `<'int/list[int]'>`: 负责人帐号ID列表 (Account.user_id),
            默认 `None` (留空或不修改), 传入空列表清除设置
        :param operator_update_mode `<'int'>`: 负责人ID的更新模式 (0: 覆盖, 1: 追加),
            默认 `None` 追加模式
        :returns `<'EditBundleProductResult'>`: 返回添加/编辑捆绑产品的结果
        ```python

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
                # 捆绑产品ID [原字段 'product_id']
                "bundle_id": 4*****,
                # 捆绑产品SKU [原字段 'sku']
                "bundle_sku": "BUNDLE-SKU",
                # 捆绑产品SKU识别码
                "sku_identifier": "",
            },
        }
        """
        url = route.EDIT_BUNDLE_PRODUCT
        # 解析并验证参数
        args = {
            "bundle_sku": bundle_sku,
            "bundle_name": bundle_name,
            "items": items,
            "category_id": category_id,
            "category_name": category_name,
            "brand_id": brand_id,
            "brand_name": brand_name,
            "product_model": product_model,
            "product_unit": product_unit,
            "product_description": product_description,
            "product_images": product_images,
            "product_creator_id": product_creator_id,
            "product_developer_id": product_developer_id,
            "product_developer_name": product_developer_name,
            "operator_ids": operator_ids,
            "operator_update_mode": operator_update_mode,
        }
        try:
            p = param.EditBundleProduct.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.EditBundleProductResult.model_validate(data)

    async def AuxiliaryMaterials(
        self,
        *,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.AuxiliaryMaterials:
        """查询产品辅料

        ## Docs
        - 产品: [查询产品辅料列表](https://apidoc.lingxing.com/#/docs/Product/productAuxList)

        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 最大支持 1000, 默认 `None` (使用: 1000)
        :returns `<'AuxiliaryMaterials'>`: 返回查询到的产品辅料列表
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
                    # 辅料分类ID [原字段 'cid']
                    "category_id": 0,
                    # 辅料ID [原字段 'id']
                    "aux_id": 4*****,
                    # 辅料SKU [原字段 'sku']
                    "aux_sku": "MAT*******",
                    # 辅料名称 [原字段 'product_name']
                    "aux_name": "包装箱",
                    # 辅料净重 [原字段 'cg_product_net_weight']
                    "aux_net_weight": 10.0,
                    # 辅料长度 [原字段 'cg_product_length']
                    "aux_length": 100.0,
                    # 辅料宽度 [原字段 'cg_product_width']
                    "aux_width": 100.0,
                    # 辅料高度 [原字段 'cg_product_height']
                    "aux_height": 100.0,
                    # 辅料备注 [原字段 'remark']
                    "aux_note": "",
                    # 辅料采购价格 [原字段 'cg_price']
                    "purchase_price": 10.0,
                    # 辅料关联的产品列表 [原字段 'aux_relation_product']
                    "associates": [
                        {
                            # 领星本地产品SKU [原字段 'sku']
                            "lsku": "SKU*******",
                            # 领星本地产品ID [原字段 'pid']
                            "product_id": 4*****,
                            # 领星本地产品名称
                            "product_name": "P*********",
                            # 产品关联辅料的数量 [原字段 'quantity']
                            "aux_qty": 0,
                            # 辅料配比数量 [原字段 'aux_qty']
                            "aux_ratio_qty": 1,
                            # 产品配比数据 [原字段 'sku_qty']
                            "sku_ratio_qty": 1,
                        }
                    ],
                    # 供应商报价信息列表 [原字段 'supplier_quote']
                    "supplier_quotes": [
                        {
                            # 领星本地产品ID
                            "product_id": 4*****,
                            # 供应商ID
                            "supplier_id": 6***,
                            # 供应商名称
                            "supplier_name": "遵*****",
                            # 供应商编码
                            "supplier_code": "SU*****",
                            # 供应商等级 [原字段 'level_text']
                            "supplier_level": "",
                            # 供应商员工数 [原字段 'employees_text']
                            "supplier_employees": "",
                            # 供应商产品链接 [原字段 'supplier_product_url']
                            "supplier_product_urls": [],
                            # 供应商备注 [原字段 'remark']
                            "supplier_note": "",
                            # 是否是首选供应商 (0: 否, 1: 是) [原字段 'is_primary']
                            "is_primary_supplier": 1,
                            # 报价ID [原字段 'psq_id']
                            "quote_id": 21****************,
                            # 报价货币符号 [原字段 'cg_currency_icon']
                            "quote_currency_icon": "￥",
                            # 报价单价 [原字段 'cg_price']
                            "quote_price": 10.0,
                            # 报价交期 (单位: 天) [原字段 'quote_cg_delivery']
                            "quote_delivery_time": 14,
                            # 报价备注 [原字段 'quote_remark']
                            "quote_note": "",
                            # 报价列表 [原字段 'quotes']
                            "quotes": [
                                {
                                    # 报价货币代码 [原字段 'currency']
                                    "currency_code": "CNY",
                                    # 报价货币符号
                                    "currency_icon": "￥",
                                    # 报价是否含税 (0: 否, 1: 是) [原字段 'is_tax']
                                    "is_tax_inclusive": 1,
                                    # 报价税率 (百分比)
                                    "tax_rate": 5.0,
                                    # 报价梯度 [原字段 'step_prices']
                                    "price_tiers": [
                                        {
                                            # 最小订购量
                                            "moq": 10,
                                            # 报价 (不含税) [原字段 'price']
                                            "price_excl_tax": 10.0,
                                            # 报价 (含税)
                                            "price_with_tax": 10.5,
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
                ...
            ],
        }
        """
        url = route.AUXILIARY_MATERIALS
        # 解析并验证参数
        args = {"offset": offset, "length": length}
        try:
            p = base_param.PageOffestAndLength.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.AuxiliaryMaterials.model_validate(data)

    async def EditAuxiliaryMaterial(
        self,
        aux_sku: str,
        aux_name: str,
        *,
        aux_net_weight: int | float | None = None,
        aux_length: int | float | None = None,
        aux_width: int | float | None = None,
        aux_height: int | float | None = None,
        aux_note: str | None = None,
        purchase_price: int | float | None = None,
        supplier_quotes: dict | list[dict] | None = None,
    ) -> schema.EditAuxiliaryMaterialResult:
        """添加/编辑辅料

        ## Docs
        - 产品: [添加/编辑辅料](https://apidoc.lingxing.com/#/docs/Product/setAux)

        ## Notice
        - 默认参数 `None` 表示重置设置, 所有没有传入的参数都将被重置为默认值
        - 这点不同于 `EditProduct` 方法, 其默认参数 `None` 表示留空或不修改,
          只有传入的对应参数才会被更新

        :param aux_sku `<'str'>`: 辅料SKU (AuxiliaryMaterial.aux_sku)
        :param aux_name `<'str'>`: 辅料名称 (AuxiliaryMaterial.aux_name)
        :param aux_net_weight `<'int/float'>`: 辅料净重 (单位: G),
            默认 `None`, 不同于 `EditProduct`, 表示重置设置或默认0
        :param aux_length `<'int/float'>`: 辅料长度 (单位: CM),
            默认 `None`, 不同于 `EditProduct`, 表示重置设置或默认0
        :param aux_width `<'int/float'>`: 辅料宽度 (单位: CM),
            默认 `None`, 不同于 `EditProduct`, 表示重置设置或默认0
        :param aux_height `<'int/float'>`: 辅料高度 (单位: CM),
            默认 `None`, 不同于 `EditProduct`, 表示重置设置或默认0
        :param aux_note `<'str'>`: 辅料备注,
            默认 `None`, 不同于 `EditProduct`, 表示重置设置或默认空字符串
        :param purchase_price `<'int/float'>`: 辅料采购价格,
            默认 `None`, 不同于 `EditProduct`, 表示重置设置或默认0
        :param supplier_quotes `<'dict/list[dict]'>`: 供应商报价信息列表,
            默认 `None`, 不同于 `EditProduct`, 表示重置设置或默认空

            - 每个字典必须包含 `supplier_id`, `is_primary`, `quotes` 字段:
            - 必填字段 `supplier_id` 供应商ID, 必须为 int 类型 (`Supplier.supplier_id`)
            - 必填字段 `is_primary` 是否是首选供应商, 必须为 int 类型 (0: 否, 1: 是)
            - 必填字段 `quotes` 供应商报价列表, 必须为 dict/list[dict] 类型, 每个字典必须包含以下字段:
                * 必填字段 `quotes.currency_code` 报价货币代码, 必须为 str
                * 必填字段 `quotes.is_tax_inclusive` 报价是否含税, 必须为 int 类型 (0: 否, 1: 是)
                * 必填字段 `quotes.tax_rate` 报价税率, 必须为 float 类型 (百分比, 如 5% 则传 5)
                * 必填字段 `quotes.price_tiers` 报价梯度, 必须为 dict/list[dict] 类型, 每个字典必须包含以下字段:
                    + 必填字段 `quotes.price_tiers.moq` 最小订购量, 必须为 int 类型
                    + 必填字段 `quotes.price_tiers.price_with_tax` 报价 (含税), 必须为 int/float 类型
            - 可选字段 `product_urls` 供应商产品链接列表, 必须为 str/list[str] 类型, 不传重置为空列表
            - 可选字段 `supplier_note` 供应商备注, 必须为 str 类型, 不传重置为空字符串

        :returns `<'EditAuxiliaryMaterialResult'>`: 返回添加/编辑辅料的结果
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
                # 辅料ID [原字段 'product_id']
                "aux_id": 4*****,
                # 辅料SKU [原字段 'sku']
                "aux_sku": "MAT*******",
                # 辅料SKU识别码
                "sku_identifier": "",
            },
        }
        ```
        """
        url = route.EDIT_AUXILIARY_MATERIAL
        # 解析并验证参数
        args = {
            "aux_sku": aux_sku,
            "aux_name": aux_name,
            "aux_net_weight": aux_net_weight,
            "aux_length": aux_length,
            "aux_width": aux_width,
            "aux_height": aux_height,
            "aux_note": aux_note,
            "purchase_price": purchase_price,
            "supplier_quotes": supplier_quotes,
        }
        try:
            p = param.EditAuxiliaryMaterial.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.EditAuxiliaryMaterialResult.model_validate(data)

    async def ProductCodes(
        self,
        *,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.ProductCodes:
        """查询产品编码 (UPC/EAN/ISBN)

        ## Docs
        - 产品: [获取UPC编码列表](https://apidoc.lingxing.com/#/docs/Product/UpcList)

        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 最大值200, 默认 `None` (使用: 20)
        :returns `<'ProductCodes'>`: 返回查询到的产品编码列表
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
                    # 产品编码 ID [原字段 'id']
                    "code_id": 1,
                    # 产品编码 [原字段 'commodity_code']
                    "code": "1234567890123",
                    # 编码类型
                    "code_type": "UPC",
                    # 编码备注 [原字段 'remark']
                    "code_note": "",
                    # 编码状态 (0: 未使用, 1: 已使用) [原字段 'is_used']
                    "status": 0,
                    # 编码状态描述 [原字段 'is_used_desc']
                    "status_desc": "未使用",
                    # 创建人的用户ID (Account_user_id) [原字段 'created_user_id']
                    "create_user_id": 1*******,
                    # 创建时间 (北京时间) [原字段 'gmt_create']
                    "create_time": "2025-07-23 17:46:58",
                    # 使用人的用户ID (Account_user_id)
                    "use_user_id": 1*******,
                    # 使用时间 (北京时间)
                    "use_time": "2025-07-23 18:46:58",
                },
                ...
            ],
        }
        ```
        """
        url = route.PRODUCT_CODES
        # 解析并验证参数
        args = {"offset": offset, "length": length}
        try:
            p = base_param.PageOffestAndLength.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.ProductCodes.model_validate(data)

    async def CreateProductCode(
        self,
        code_type: PRODUCT_CODE_TYPE,
        *codes: str,
    ) -> base_schema.ResponseResult:
        """批量添加产品编码 (UPC/EAN/ISBN)

        ## Docs
        - 产品: [创建UPC编码](https://apidoc.lingxing.com/#/docs/Product/AddCommodityCode)

        :param code_type `<'str'>`: 编码类型, 可选值: `"UPC"`, `"EAN"`, `"ISBN"`
        :param codes `<'str'>`: 一个或多个产品编码
        :returns `<'ResponseResult'>`: 返返回添加产品编码结果
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
            "data": ["1234567890123", ...]
        }
        ```
        """
        url = route.CREATE_PRODUCT_CODE
        # 解析并验证参数
        args = {"code_type": code_type, "codes": codes}
        try:
            p = param.CreateProductCode.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return base_schema.ResponseResult.model_validate(data)

    async def ProductGlobalTags(self) -> schema.ProductGlobalTags:
        """查询产品可设置的全局标签

        ## Docs
        - 产品: [查询产品标签](https://apidoc.lingxing.com/#/docs/Product/GetProductTag)

        :returns `<'ProductGlobalTags'>`: 返回查询到的产品全局标签
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
                    # 全局标签ID [原字段 'label_id']
                    "tag_id": 1,
                    # 全局标签名称 [原字段 'label_name']
                    "tag_name": "新品",
                    # 全局标签创建时间 (UTC毫秒时间戳) [原字段 'gmt_created']
                    "create_time_ts": 1753330280000
                },
                ...
            ],
        }
        """
        url = route.PRODUCT_GLOBAL_TAGS
        # 发送请求
        data = await self._request_with_sign("GET", url)
        return schema.ProductGlobalTags.model_validate(data)

    async def CreateProductGlobalTag(
        self,
        tag_name: str,
    ) -> schema.CreateProductGlobalTagResult:
        """创建产品可设置的全局标签

        ## Docs
        - 产品: [创建产品标签](https://apidoc.lingxing.com/#/docs/Product/CreateProductTag)

        :param tag_name `<'str'>`: 新全局标签名称
        :returns `<'CreateProductGlobalTagResult'>`: 返回创建全局标签的结果
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
                # 全局标签ID [原字段 'label_id']
                "tag_id": 1,
                # 全局标签名称 [原字段 'label_name']
                "tag_name": "新品",
            },
        }
        """
        url = route.CREATE_PRODUCT_GLOBAL_TAG
        # 解析并验证参数
        args = {"tag_name": tag_name}
        try:
            p = param.CreateProductGlobalTag.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.CreateProductGlobalTagResult.model_validate(data)

    async def SetProductTag(
        self,
        mode: int,
        *product_tags: dict,
    ) -> base_schema.ResponseResult:
        """批量给指定产品设置标签

        ## Docs
        - 产品: [标记产品标签](https://apidoc.lingxing.com/#/docs/Product/SetProductTag)

        :param mode `<'int'>`: 设置模式

            - `1`: 追加新的标签
            - `2`: 覆盖现有标签

        :param *product_tags `<'dict'>`: 需要设置对应标签的产品信息

            - 每个字典必须包含 `lsku` 和 `tags` 字段, 如:
              `{"lsku": "SKU12345", "tags": ["新品", "热销"]}`
            - 必填字段 `lsku` 领星本地产品的SKU, 参数来源 `Product.lsku`
            - 必填字段 `tags` 产品标签名称或名称列表, 参数来源 `ProductGlobalTag.tag_name`

        :returns `<'ResponseResult'>`: 返回设置标签的结果
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
            "data": None
        }
        ```
        """
        url = route.SET_PRODUCT_TAG
        # 解析并验证参数
        args = {"mode": mode, "product_tags": product_tags}
        try:
            p = param.SetProductTag.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return base_schema.ResponseResult.model_validate(data)

    async def UnsetProductTag(
        self,
        mode: int,
        *product_tags: dict,
    ) -> base_schema.ResponseResult:
        """批量给指定产品删除标签

        ## Docs
        - 产品: [删除产品标签](https://apidoc.lingxing.com/#/docs/Product/DelProductTag)

        :param mode `<'int'>`: 删除模式

            - `1`: 删除SKU指定的标签
            - `2`: 删除SKU全部的标签, [此模式下, 对应 lsku 的 tags 为 `None` 即可]

        :param *product_tags `<'dict'>`: 需要删除对应标签的产品信息

            - 每个字典必须包含 `lsku` 和 `tags` 字段, 如:
              `{"lsku": "SKU12345", "tags": ["新品", "热销"]}`
            - 必填字段 `lsku` 领星本地产品的SKU, 参数来源 `Product.lsku`
            - 必填字段 `tags` 产品标签名称或名称列表, 参数来源 `ProductGlobalTag.tag_name`

        :returns `<'ResponseResult'>`: 返回删除标签的结果
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
            "data": None
        }
        ```
        """
        url = route.UNSET_PRODUCT_TAG
        # 解析并验证参数
        args = {"mode": mode, "product_tags": product_tags}
        try:
            p = param.UnsetProductTag.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return base_schema.ResponseResult.model_validate(data)

    async def ProductGlobalAttributes(
        self,
        *,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.ProductGlobalAttributes:
        """查询产品可设置的全局属性

        ## Docs
        - 产品: [查询产品属性列表](https://apidoc.lingxing.com/#/docs/Product/attributeList)

        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 最大支持 200, 默认 `None` (使用: 20)
        :returns `<'ProductGlobalAttributes'>`: 返回查询到的产品属性列表
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
                    # 产品属性ID [原字段 'pa_id']
                    "attr_id": 1,
                    # 产品属性名称
                    "attr_name": "香薰机",
                    # 产品属性编码
                    "attr_code": "XXJ",
                    # 产品子属性列表 [原字段 'item_list']
                    "attr_values": [
                        {
                            # 产品属性ID 【原字段 'pa_id'】
                            "attr_id": 1,
                            # 产品属性值ID [原字段 'pai_id']
                            "attr_value_id": 100,
                            # 产品属性值编码 [原字段 'attr_val_code']
                            "attr_value_code": "BLUE",
                            # 产品属性值 [原字段 'attr_value']
                            "attr_value": "蓝色",
                            # 产品属性值创建时间 (北京时间)
                            "create_time": "2024-08-13 14:04:13",
                        },
                        ...
                    ],
                    # 产品属性创建时间 (北京时间)
                    "create_time": "2024-08-13 14:04:13",
                },
                ...
            ],
        }
        ```
        """
        url = route.PRODUCT_GLOBAL_ATTRIBUTES
        # 解析并验证参数
        args = {"offset": offset, "length": length}
        try:
            p = base_param.PageOffestAndLength.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.ProductGlobalAttributes.model_validate(data)

    async def EditProductGlobalAttribute(
        self,
        attr_name: str,
        attr_values: str | dict | list[str | dict],
        *,
        attr_id: int | None = None,
    ) -> base_schema.ResponseResult:
        """添加/编辑产品可设置的全局属性

        ## Docs
        - 产品: [添加/编辑产品属性](https://apidoc.lingxing.com/#/docs/Product/attributeSet)

        ## Notice
        - 1. 接口对属性数据为覆盖式操作，入参属性值会全量覆盖系统里已存在属性内容
        - 2. 属性值有关联SPU的情况下, 不允许对该属性值有编辑、删除操作
        - 3. 如需对已存在属性新增属性值, 入参为: 该属性下已存在属性值 + 新增属性值
        - 4. 如 `attr_id` 与 `attr_value_id` 都不传，视为新增属性

        :param attr_name `<'str'>`: 产品属性名称
        :param attr_values `<'str/dict/list'>`: 产品属性值, 可以是字符串、字典或字符串列表

            - `<'str'>`: 单个属性值
            - `<'dict'>`: 包含 `attr_value` 和 `attr_value_id` 的键值对
            - `<'list'>`: 多个属性值的列表, 子元素可以是字符串或字典

        :param attr_id `<'int'>`: 产品属性ID, 默认 `None` (新增属性)
        :returns `<'ResponseResult'>`: 返回添加/编辑属性结果
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
            "data": None
        }
        ```
        """
        url = route.EDIT_PRODUCT_GLOBAL_ATTRIBUTE
        # 解析并验证参数
        args = {"attr_name": attr_name, "attr_values": attr_values, "attr_id": attr_id}
        try:
            p = param.EditProductGlobalAttribute.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return base_schema.ResponseResult.model_validate(data)

    async def ProductBrands(
        self,
        *,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.ProductBrands:
        """查询产品品牌

        ## Docs
        - 产品: [查询产品品牌列表](https://apidoc.lingxing.com/#/docs/Product/productBrandList)

        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 最大支持 1000, 默认 `None` (使用: 1000)
        :returns `<'ProductBrands'>`: 返回查询到的产品品牌列表
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
                    # 领星本地品牌ID [原字段 'bid']
                    "brand_id": 1,
                    # 品牌名称 [原字段 'title']
                    "brand_name": "FastTech",
                    # 品牌编码
                    "brand_code": "",
                },
                ...
            ],
        }
        ```
        """
        url = route.PRODUCT_BRANDS
        # 解析并验证参数
        args = {"offset": offset, "length": length}
        try:
            p = base_param.PageOffestAndLength.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.ProductBrands.model_validate(data)

    async def EditProductBrands(
        self,
        *brand: str | dict,
    ) -> schema.EditProductBrandsResult:
        """添加/编辑产品品牌

        ## Docs
        - 产品: [添加/编辑产品品牌](https://apidoc.lingxing.com/#/docs/Product/SetBrand)

        :param *brand `<'str/dict'>`: 产品品牌信息, 可以是字符串或字典

            - `<'str'>`: 品牌名称 (新增品牌)
            - `<'dict'>`: 每个字典必须包含 `brand_name` 字段, 如:
              `{'brand_name': '品牌名'}`
            * 必填字段 `brand_name` 品牌名称, 必须是 str 类型,
              参数来源 `ProductBrand.brand_name`
            * 可选字段 `brand_id` 品牌ID, 必须 int 类型, 如果提供则编辑现有品牌,
              否则新增品牌, 参数来源 `ProductBrand.brand_id`
            * 可选字段 `brand_code` 品牌编码, 必须是 str 类型,
              参数来源 `ProductBrand.brand_code`

        :returns `<'EditProductBrandsResult'>`: 返回创建或编辑的产品品牌结果列表
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
            "data": [
                {
                    # 创建/编辑的产品品牌ID [原字段 'id']
                    "brand_id": 1,
                    # 创建/编辑的产品品牌名称 [原字段 'title']
                    "brand_name": "FastTech",
                    # 创建/编辑的产品品牌编码
                    "brand_code": "FT-001",
                },
                ...
            ],
        }
        """
        url = route.EDIT_PRODUCT_BRANDS
        # 解析并验证参数
        args = {"brands": brand}
        try:
            p = param.EditProductBrands.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.EditProductBrandsResult.model_validate(data)

    async def ProductCategories(
        self,
        *category_id: int,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.ProductCategories:
        """查询产品分类

        ## Docs
        - 产品: [查询产品分类列表](https://apidoc.lingxing.com/#/docs/Product/Category)

        :param *category_id `<'int'>`: 产品分类ID列表, 可以传入多个分类ID, 或不传入 (查询所有分类)
        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 最大值 1000, 默认 `None` (使用: 1000)
        :returns `<'ProductCategories'>`: 返回查询到的产品分类列表
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
                    # 领星本地产品分类ID [原字段 'id']
                    "category_id": 1,
                    # 分类名称 [原字段 'title']
                    "category_name": "电子产品",
                    # 分类编码
                    "category_code": "ELEC-001",
                    # 父分类ID [原字段 'parent_cid']
                    "parent_category_id": 0,
                },
                ...
            ],
        }
        """
        url = route.PRODUCT_CATEGORIES
        # 解析并验证参数
        args = {"category_id": category_id, "offset": offset, "length": length}
        try:
            p = param.ProductCategories.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.ProductCategories.model_validate(data)

    async def EditProductCategories(
        self,
        *category: str | dict,
    ) -> schema.EditProductCategoriesResult:
        """添加/编辑产品分类

        ## Docs
        - 产品: [添加/编辑产品分类](https://apidoc.lingxing.com/#/docs/Product/SetCategory)

        :param *category `<'str/dict'>`: 产品品牌信息, 可以是字符串或字典

            - `<'str'>`: 分类名称 (新增分类)
            - `<'dict'>`: 每个字典必须包含 `category_name` 字段, 如:
              `{'category_name': '新分类'}`
            * 必填字段 `category_name` 分类名称, 必须是 str 类型,
              参数来源 `ProductCategory.category_name`
            * 可选字段 `category_id` 分类ID, 必须 int 类型, 如果提供则编辑现有分类,
              否则新增分类, 参数来源 `ProductCategory.category_id`
            * 可选字段 `category_code` 分类编码, 必须是 str 类型,
              参数来源 `ProductCategory.category_code`
            * 可选字段 `parent_category_id` 父分类ID, 必须 int 类型,
              参数来源 `ProductCategory.parent_category_id`

        :returns `<'EditProductCategoriesResult'>`: 返回创建或编辑的产品分类结果列表
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
            "data": [
                {
                    # 创建/编辑的产品分类ID [原字段 'id']
                    "category_id": 1,
                    # 创建/编辑的产品分类名称 [原字段 'title']
                    "category_name": "电子产品",
                    # 创建/编辑的产品分类编码
                    "category_code": "ELEC-001",
                    # 创建/编辑的产品分类父ID [原字段 'parent_cid']
                    "parent_category_id": 0,
                },
                ...
            ],
        }
        """
        url = route.EDIT_PRODUCT_CATEGORIES
        # 解析并验证参数
        args = {"categories": category}
        try:
            p = param.EditProductCategories.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.EditProductCategoriesResult.model_validate(data)
