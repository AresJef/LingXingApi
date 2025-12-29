# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from lingxingapi.base import schema as base_schema
from lingxingapi.base.schema import ResponseV1, ResponseResult, FlattenDataList
from lingxingapi.fields import IntOrNone2Zero, FloatOrNone2Zero, StrOrNone2Blank


# 产品 --------------------------------------------------------------------------------------------------------------------------
# . Products
class ProductQuotePriceTier(BaseModel):
    """领星本地产品供应商报价定价梯度"""

    # 最小订购量 (MOQ)
    moq: int
    # 报价 (不含税) [原字段 'price']
    price_excl_tax: float = Field(validation_alias="price")
    # 报价 (含税)
    price_with_tax: float


class ProductQuotePricing(BaseModel):
    """领星本地产品供应商报价定价信息"""

    # 报价货币代码 [原字段 'currency']
    currency_code: str = Field(validation_alias="currency")
    # 报价货币符号
    currency_icon: str
    # 报价是否含税 (0: 否, 1: 是) [原字段 'is_tax']
    is_tax_inclusive: int = Field(validation_alias="is_tax")
    # 报价税率 (百分比)
    tax_rate: float
    # 报价梯度 [原字段 'step_prices']
    price_tiers: list[ProductQuotePriceTier] = Field(validation_alias="step_prices")


class ProductSupplierQuote(BaseModel):
    """领星本地产品供应商报价信息"""

    # 领星本地产品ID
    product_id: int
    # 供应商ID
    supplier_id: int
    # 供应商名称
    supplier_name: str
    # 供应商编码
    supplier_code: str
    # 供应商等级 [原字段 'level_text']
    supplier_level: str = Field("", validation_alias="level_text")
    # 供应商员工数 [原字段 'employees_text']
    supplier_employees: str = Field("", validation_alias="employees_text")
    # 供应商产品链接 [原字段 'supplier_product_url']
    supplier_product_urls: list[str] = Field(validation_alias="supplier_product_url")
    # 供应商备注 [原字段 'remark']
    supplier_note: str = Field("", validation_alias="remark")
    # 是否是首选供应商 (0: 否, 1: 是) [原字段 'is_primary']
    is_primary_supplier: int = Field(validation_alias="is_primary")
    # 报价ID [原字段 'psq_id']
    quote_id: int = Field(validation_alias="psq_id")
    # 报价货币符号 [原字段 'cg_currency_icon']
    quote_currency_icon: str = Field(validation_alias="cg_currency_icon")
    # 报价单价 [原字段 'cg_price']
    quote_price: float = Field(validation_alias="cg_price")
    # 报价交期 (单位: 天) [原字段 'quote_cg_delivery']
    quote_delivery_time: int = Field(validation_alias="quote_cg_delivery")
    # 报价备注 [原字段 'quote_remark']
    quote_note: str = Field(validation_alias="quote_remark")
    # 报价列表 [原字段 'quotes']
    quotes: list[ProductQuotePricing]


class Product(BaseModel):
    """领星本地产品"""

    # fmt: off
    # 领星本地SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 领星本地SKU识别码
    sku_identifier: str
    # 领星本地产品ID [原字段 'id']
    product_id: int = Field(validation_alias="id")
    # 领星本地产品名称
    product_name: str
    # 领星本地产品分类ID [原字段 'cid']
    category_id: int = Field(validation_alias="cid")
    # 领星本地产品分类名称
    category_name: str
    # 领星本地产品品牌ID
    brand_id: int = Field(validation_alias="bid")
    # 领星本地产品品牌名称
    brand_name: str
    # 产品图片链接 [原字段 'pic_url']
    image_url: str = Field(validation_alias="pic_url")
    # 是否为组合产品 (0: 否, 1: 是) [原字段 'is_combo']
    is_bundled: int = Field(validation_alias="is_combo")
    # 产品是否被启用 (0: 未启用, 1: 已启用) [原字段 'open_status']
    is_enabled: int = Field(validation_alias="open_status")
    # 产品状态 (0: 停售, 1: 在售, 2: 开发中, 3: 清仓) [原字段 'status']
    status: int
    # 产品状态描述 [原字段 'status_text']
    status_desc: str = Field(validation_alias="status_text")
    # 创建时间 (UTC秒时间戳) [原字段 'create_time']
    create_time_ts: int = Field(validation_alias="create_time")
    # 更新时间 (UTC秒时间戳) [原字段 'update_time']
    update_time_ts: int = Field(validation_alias="update_time")
    # 产品开发者用户ID (Account.user_id) [原字段 'product_developer_uid']
    product_developer_id: int = Field(validation_alias="product_developer_uid")
    # 产品开发者姓名 (Account.display_name) [原字段 'product_developer']
    product_developer_name: str = Field(validation_alias="product_developer")
    # 产品采购人用户ID (Account.user_id) [原字段 'cg_opt_uid']
    purchase_staff_id: int = Field(validation_alias="cg_opt_uid")
    # 产品采购人姓名 (Account.display_name) [原字段 'cg_opt_username']
    purchase_staff_name: str = Field(validation_alias="cg_opt_username")
    # 采购交期 (单位: 天) [原字段 'cg_delivery']
    purchase_delivery_time: int = Field(validation_alias="cg_delivery")
    # 采购运输成本 [原字段 'cg_transport_costs']
    purchase_transport_costs: float = Field(validation_alias="cg_transport_costs")
    # 采购成本 [原字段 'cg_price']
    purchase_price: float = Field(validation_alias="cg_price")
    # 采购备注 [原字段 'purchase_remark']
    purchase_note: str = Field(validation_alias="purchase_remark")
    # 供应商报价信息列表 [原字段 'supplier_quote']
    supplier_quotes: list[ProductSupplierQuote] = Field(validation_alias="supplier_quote")
    # 多属性产品ID [原字段 'ps_id']
    spu_id: int = Field(validation_alias="ps_id")
    # 多属性产品名称 [原字段 'spu']
    spu_name: str = Field(validation_alias="spu")
    # 产品属性列表 [原字段 'attribute']
    attributes: list[base_schema.SpuProductAttribute] = Field(validation_alias="attribute")
    # 产品标签列表 [原字段 'global_tags']
    tags: list[base_schema.TagInfo] = Field(validation_alias="global_tags")
    # 自定义字段
    custom_fields: list[base_schema.CustomField]
    # fmt: on


class Products(ResponseV1):
    """领星本地产品列表"""

    data: list[Product]


# . Product Detail
class ProductBundleItem(BaseModel):
    """领星本地产品组合信息"""

    # 领星本地SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 领星本地产品ID
    product_id: int
    # 产品数量 [原字段 'quantity']
    product_qty: int = Field(validation_alias="quantity")


class ProductImage(BaseModel):
    """领星本地产品图片信息"""

    # 图片链接 [原字段 'pic_url']
    image_url: str = Field(validation_alias="pic_url")
    # 是否为主图 (0: 否, 1: 是)
    is_primary: int


class ProductCustomsDeclaration(BaseModel):
    """领星本地产品报关信息"""

    # fmt: off
    # 报关申报品名 (出口国) [原字段 'customs_export_name']
    export_name: str = Field("", validation_alias="customs_export_name")
    # 报关申报HS编码 (出口国) [原字段 'customs_declaration_hs_code']
    export_hs_code: str = Field("", validation_alias="customs_declaration_hs_code")
    # 报关申报品名 (进口国) [原字段 'customs_import_name']
    import_name: str = Field("", validation_alias="customs_import_name")
    # 报关申报单价 (进口国) [原字段 'customs_import_price']
    import_price: float = Field(validation_alias="customs_import_price")
    # 报关申报单价货币代码 (进口国) [原字段 'customs_import_price_currency']
    currency_code: str = Field(validation_alias="customs_import_price_currency")
    # 报关申报单价货币符号 (进口国) [原字段 'customs_import_price_currency_icon']
    currency_icon: str = Field("", validation_alias="customs_import_price_currency_icon")
    # 报关申报产品单位 [原字段 'customs_declaration_unit']
    unit: str = Field(validation_alias="customs_declaration_unit")
    # 报关申报产品规格 [原字段 'customs_declaration_spec']
    specification: str = Field(validation_alias="customs_declaration_spec")
    # 报关申报产品原产地 [原字段 'customs_declaration_origin_produce']
    country_of_origin: str = Field(validation_alias="customs_declaration_origin_produce")
    # 报关申报内陆来源 [原字段 'customs_declaration_inlands_source']
    source_from_inland: str = Field(validation_alias="customs_declaration_inlands_source")
    # 报关申报免税 [原字段 'customs_declaration_exempt']
    exemption: str = Field(validation_alias="customs_declaration_exempt")
    # 其他申报要素 [原字段 'other_declare_element']
    other_details: str = Field("", validation_alias="other_declare_element")
    # fmt: on


class ProductCustomsClearance(BaseModel):
    """领星本地产品清关信息"""

    # fmt: off
    # 清关内部编码 [原字段 'customs_clearance_internal_code']
    internal_code: str = Field(validation_alias="customs_clearance_internal_code")
    # 清关产品材质 [原字段 'customs_clearance_material']
    material: str = Field(validation_alias="customs_clearance_material")
    # 清关产品用途 [原字段 'customs_clearance_usage']
    usage: str = Field(validation_alias="customs_clearance_usage")
    # 清关是否享受优惠 [原字段 'customs_clearance_preferential']
    # (0: 未设置, 1: 不享惠, 2: 享惠, 3: 不确定)
    preferential: int = Field(validation_alias="customs_clearance_preferential")
    # 清关是否享受优惠描述 [原字段 'customs_clearance_preferential_text']
    preferential_desc: str = Field("", validation_alias="customs_clearance_preferential_text")
    # 清关品牌类型 [原字段 'customs_clearance_brand_type']
    # (0: 未设置, 1: 无品牌, 2: 境内品牌[自主], 3: 境内品牌[收购], 4: 境外品牌[贴牌], 5: 境外品牌[其他])
    brand_type: int = Field(validation_alias="customs_clearance_brand_type")
    # 清关品牌类型描述 [原字段 'customs_clearance_brand_type_text']
    brand_type_desc: str = Field("", validation_alias="customs_clearance_brand_type_text")
    # 清关产品型号 [原字段 'customs_clearance_product_pattern']
    model: str = Field(validation_alias="customs_clearance_product_pattern")
    # 清关产品图片链接 [原字段 'customs_clearance_pic_url']
    image_url: str = Field(validation_alias="customs_clearance_pic_url")
    # 配货备注 [原字段 'allocation_remark']
    allocation_note: StrOrNone2Blank = Field(validation_alias="allocation_remark")
    # 织造类型 (0: 未设置, 1: 针织, 2: 梭织) [原字段 'weaving_mode']
    fabric_type: int = Field(validation_alias="weaving_mode")
    # 织造类型描述 [原字段 'weaving_mode_text']
    fabric_type_desc: str = Field("", validation_alias="weaving_mode_text")
    # 清关申报单价货币代码 [原字段 'customs_clearance_price_currency']
    clearance_currency_code: str = Field(validation_alias="customs_clearance_price_currency")
    # 清关申报单价货币符号 [原字段 'customs_clearance_price_currency_icon']
    clearance_currency_icon: str = Field("", validation_alias="customs_clearance_price_currency_icon")
    # 清关申报单价 [原字段 'customs_clearance_price']
    clearance_price: float = Field(validation_alias="customs_clearance_price")
    # 清关税率 [原字段 'customs_clearance_tax_rate']
    clearance_tax_rate: float = Field(validation_alias="customs_clearance_tax_rate")
    # 清关HS编码 [原字段 'customs_clearance_hs_code']
    clearance_hs_code: str = Field(validation_alias="customs_clearance_hs_code")
    # 清关备注 [原字段 'customs_clearance_remark']
    clearance_note: StrOrNone2Blank = Field(validation_alias="customs_clearance_remark")
    # fmt: on


class ProductOperator(BaseModel):
    """领星本地产品负责人信息"""

    # 负责人帐号ID (Account.user_id) [原字段 'permission_uid']
    user_id: int = Field(validation_alias="permission_uid")
    # 负责人姓名 (Account.display_name) [原字段 'permission_user_name']
    user_name: str = Field(validation_alias="permission_user_name")


class ProductDetail(BaseModel):
    """领星本地产品详情"""

    # fmt: off
    # 领星本地SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 领星本地SKU识别码
    sku_identifier: str
    # 领星本地产品ID [原字段 'id']
    product_id: int = Field(validation_alias="id")
    # 领星本地产品名称
    product_name: str
    # 领星本地产品分类ID [原字段 'cid']
    category_id: int = Field(validation_alias="cid")
    # 领星本地产品分类名称
    category_name: str
    # 领星本地产品品牌ID
    brand_id: int = Field(validation_alias="bid")
    # 领星本地产品品牌名称
    brand_name: str
    # 产品图片链接 [原字段 'pic_url']
    image_url: str = Field(validation_alias="pic_url")
    # 是否为组合产品 (0: 否, 1: 是) [原字段 'is_combo']
    is_bundled: int = Field(validation_alias="is_combo")
    # 组合产品所包含的单品列表 [原字段 'combo_product_list']
    bundle_items: list[ProductBundleItem] = Field(validation_alias="combo_product_list")
    # 产品状态 (0: 停售, 1: 在售, 2: 开发中, 3: 清仓) [原字段 'status']
    status: int
    # 产品型号 [原字段 'model']
    product_model: str = Field(validation_alias="model")
    # 产品单位 [原字段 'unit']
    product_unit: str = Field(validation_alias="unit")
    # 产品描述 [原字段 'description']
    product_description: str = Field(validation_alias="description")
    # 产品图片列表 [原字段 'picture_list']
    product_images: list[ProductImage] = Field(validation_alias="picture_list")
    # 产品特殊属性列表 (1: 含电, 2: 纯电, 3: 液体, 4: 粉末, 5: 膏体, 6: 带磁) [原字段 'special_attr']
    product_special_attrs: list[int] = Field(validation_alias="special_attr")
    # 产品开发者用户ID (Account.user_id) [原字段 'product_developer_uid']
    product_developer_id: int = Field(validation_alias="product_developer_uid")
    # 产品开发者姓名 (Account.display_name) [原字段 'product_developer']
    product_developer_name: str = Field(validation_alias="product_developer")
    # 产品采购人姓名 (Account.display_name) [原字段 'cg_opt_username']
    purchase_staff_name: str = Field(validation_alias="cg_opt_username")
    # 采购交期 (单位: 天) [原字段 'cg_delivery']
    purchase_delivery_time: int = Field(validation_alias="cg_delivery")
    # 采购价格货币代码 [原字段 'currency']
    purchase_currency_code: str = Field(validation_alias="currency")
    # 采购价格 [原字段 'cg_price']
    purchase_price: float = Field(validation_alias="cg_price")
    # 采购备注 [原字段 'purchase_remark']
    purchase_note: str = Field(validation_alias="purchase_remark")
    # 采购产品材质 [原字段 'cg_product_material']
    product_material: str = Field(validation_alias="cg_product_material")
    # 采购产品总重 (单位: G) [原字段 'cg_product_gross_weight']
    product_gross_weight: FloatOrNone2Zero = Field(validation_alias="cg_product_gross_weight")
    # 采购产品净重 (单位: G) [原字段 'cg_product_net_weight']
    product_net_weight: FloatOrNone2Zero = Field(validation_alias="cg_product_net_weight")
    # 采购产品长度 (单位: CM) [原字段 'cg_product_length']
    product_length: FloatOrNone2Zero = Field(validation_alias="cg_product_length")
    # 采购产品宽度 (单位: CM) [原字段 'cg_product_width']
    product_width: FloatOrNone2Zero = Field(validation_alias="cg_product_width")
    # 采购产品高度 (单位: CM) [原字段 'cg_product_height']
    product_height: FloatOrNone2Zero = Field(validation_alias="cg_product_height")
    # 采购包装长度 (单位: CM) [原字段 'cg_package_length']
    package_length: FloatOrNone2Zero = Field(validation_alias="cg_package_length")
    # 采购包装宽度 (单位: CM) [原字段 'cg_package_width']
    package_width: FloatOrNone2Zero = Field(validation_alias="cg_package_width")
    # 采购包装高度 (单位: CM) [原字段 'cg_package_height']
    package_height: FloatOrNone2Zero = Field(validation_alias="cg_package_height")
    # 采购外箱重量 (单位: KG) [原字段 'cg_box_weight']
    box_weight: FloatOrNone2Zero = Field(validation_alias="cg_box_weight")
    # 采购外箱长度 (单位: CM) [原字段 'cg_box_length']
    box_length: FloatOrNone2Zero = Field(validation_alias="cg_box_length")
    # 采购外箱宽度 (单位: CM) [原字段 'cg_box_width']
    box_width : FloatOrNone2Zero = Field(validation_alias="cg_box_width")
    # 采购外箱高度 (单位: CM) [原字段 'cg_box_height']
    box_height: FloatOrNone2Zero = Field(validation_alias="cg_box_height")
    # 采购外箱数量 [原字段 'cg_box_pcs']
    box_qty: IntOrNone2Zero = Field(validation_alias="cg_box_pcs")
    # 供应商报价信息列表 [原字段 'supplier_quote']
    supplier_quotes: list[ProductSupplierQuote] = Field(validation_alias="supplier_quote")
    # 报关申报品名 (出口国) [原字段 'bg_customs_export_name']
    customs_export_name: str = Field(validation_alias="bg_customs_export_name")
    # 报关申报HS编码 (出口国) [原字段 'bg_export_hs_code']
    customs_export_hs_code: str = Field(validation_alias="bg_export_hs_code")
    # 报关申报品名 (进口国) [原字段 'bg_customs_import_name']
    customs_import_name: str = Field(validation_alias="bg_customs_import_name")
    # 报关申报单价 (进口国) [原字段 'bg_customs_import_price']
    customs_import_price: FloatOrNone2Zero = Field(validation_alias="bg_customs_import_price")
    # 报关申报HS编码 (进口国) [原字段 'bg_import_hs_code']
    customs_import_hs_code: str = Field(validation_alias="bg_import_hs_code")
    # 报关信息 [原字段 'declaration']
    customs_declaration: ProductCustomsDeclaration = Field(validation_alias="declaration")
    # 清关信息 [原字段 'clearance']
    customs_clearance: ProductCustomsClearance = Field(validation_alias="clearance")
    # 负责人列表 [原字段 'permission_user_info']
    operators: list[ProductOperator] = Field(validation_alias="permission_user_info")
    # 产品标签列表 [原字段 'global_tags']
    tags: list[base_schema.TagInfo] = Field(validation_alias="global_tags")
    # 产品附件ID [原字段 'attachment_id']
    attachment_ids: list[str] = Field(validation_alias="attachment_id")
    # 自定义字段
    custom_fields: list[base_schema.CustomField]


class ProductDetails(ResponseV1):
    """领星本地产品详情列表"""

    data: list[ProductDetail]


# . Edit Product
class EditProduct(BaseModel):
    """领星本地产品编辑结果"""

    # 领星本地产品SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 领星本地SKU识别码
    sku_identifier: str
    # 领星本地产品ID
    product_id: int


class EditProductResult(ResponseResult):
    """领星本地产品编辑结果"""

    data: EditProduct


# . SPU Products
class SpuProduct(BaseModel):
    """领星本地SPU多属性产品"""

    # 领星SPU多属性产品ID [原字段 'ps_id']
    spu_id: int = Field(validation_alias="ps_id")
    # 领星SPU多属性产品编码
    spu: str
    # 领星SPU多属性产品名称
    spu_name: str
    # 领星本地产品分类ID [原字段 'cid']
    category_id: int = Field(validation_alias="cid")
    # 领星本地产品品牌ID [原字段 'bid']
    brand_id: int = Field(validation_alias="bid")
    # 产品型号 [原字段 'model']
    product_model: str = Field(validation_alias="model")
    # 产品开发者用户ID (Account.user_id) [原字段 'developer_uid']
    product_developer_id: int = Field(validation_alias="developer_uid")
    # 产品采购人用户ID (Account.user_id) [原字段 'cg_uid']
    purchase_staff_id: int = Field(validation_alias="cg_uid")
    # 采购交期 (单位: 天) [原字段 'cg_delivery']
    purchase_delivery_time: int = Field(validation_alias="cg_delivery")
    # 采购成本 [原字段 'cg_price']
    purchase_price: float = Field(validation_alias="cg_price")
    # 采购备注 [原字段 'purchase_remark']
    purchase_note: str = Field(validation_alias="purchase_remark")
    # 创建人用户ID (Account.user_id) [原字段 'create_uid']
    create_user_id: int = Field(validation_alias="create_uid")
    # 创建时间 (北京时间)
    create_time: str
    # 产品状态 (0: 停售, 1: 在售, 2: 开发中, 3: 清仓)
    status: int


class SpuProducts(ResponseV1):
    """领星本地SPU多属性产品列表"""

    data: list[SpuProduct]


# . SPU Product Detail
class SpuProductOperator(BaseModel):
    """领星SPU多属性产品负责人信息"""

    # 负责人帐号ID (Account.user_id) [原字段 'permission_uid']
    user_id: int = Field(validation_alias="id")
    # 负责人姓名 (Account.display_name) [原字段 'permission_user_name']
    user_name: str = Field(validation_alias="realname")


class SpuProductPurchaseInfo(BaseModel):
    """领星SPU多属性产品采购信息"""

    # fmt: off
    # 产品采购人用户ID (Account.user_id) [原字段 'cg_uid']
    purchase_staff_id: int = Field(validation_alias="cg_uid")
    # 产品采购人姓名 (Account.display_name) [原字段 'cg_user']
    purchase_staff_name: str = Field(validation_alias="cg_user")
    # 采购交期 (单位: 天) [原字段 'cg_delivery']
    purchase_delivery_time: int = Field(validation_alias="cg_delivery")
    # 采购价格 [原字段 'cg_price']
    purchase_price: float = Field(validation_alias="cg_price")
    # 采购备注 [原字段 'purchase_remark']
    purchase_note: str = Field(validation_alias="purchase_remark")
    # 采购产品材质 [原字段 'cg_product_material']
    product_material: str = Field(validation_alias="cg_product_material")
    # 采购产品公制总重 [原字段 'cg_product_gross_weight']
    product_gross_weight_metric: FloatOrNone2Zero = Field(validation_alias="cg_product_gross_weight")
    # 采购产品公制总重单位 [原字段 'cg_product_gross_weight_unit']
    product_gross_weight_metric_unit: str = Field(validation_alias="cg_product_gross_weight_unit")
    # 采购产品英制总重 [原字段 'cg_product_gross_weight_in']
    product_gross_weight_imperial: FloatOrNone2Zero = Field(validation_alias="cg_product_gross_weight_in")
    # 采购产品总重英制单位 [原字段 'cg_product_gross_weight_in_unit']
    product_gross_weight_imperial_unit: str = Field(validation_alias="cg_product_gross_weight_in_unit")
    # 采购产品公制净重 [原字段 'cg_product_net_weight']
    product_net_weight_metric: FloatOrNone2Zero = Field(validation_alias="cg_product_net_weight")
    # 采购产品公制净重单位 [原字段 'cg_product_net_weight_unit']
    product_net_weight_metric_unit: str = Field(validation_alias="cg_product_net_weight_unit")
    # 采购产品英制净重 [原字段 'cg_product_net_weight_in']
    product_net_weight_imperial: FloatOrNone2Zero = Field(validation_alias="cg_product_net_weight_in")
    # 采购产品净重英制单位 [原字段 'cg_product_net_weight_in_unit']
    product_net_weight_imperial_unit: str = Field(validation_alias="cg_product_net_weight_in_unit")
    # 采购产品公制长度 [原字段 'cg_product_length']
    product_length_metric: FloatOrNone2Zero = Field(validation_alias="cg_product_length")
    # 采购产品英制长度 [原字段 'cg_product_length_in']
    product_length_imperial: FloatOrNone2Zero = Field(validation_alias="cg_product_length_in")
    # 采购产品公制宽度 [原字段 'cg_product_width']
    product_width_metric: FloatOrNone2Zero = Field(validation_alias="cg_product_width")
    # 采购产品英制宽度 [原字段 'cg_product_width_in']
    product_width_imperial: FloatOrNone2Zero = Field(validation_alias="cg_product_width_in")
    # 采购产品公制高度 [原字段 'cg_product_height']
    product_height_metric: FloatOrNone2Zero = Field(validation_alias="cg_product_height")
    # 采购产品英制高度 [原字段 'cg_product_height_in']
    product_height_imperial: FloatOrNone2Zero = Field(validation_alias="cg_product_height_in")
    # 采购包装公制长度 [原字段 'cg_package_length']
    package_length_metric: FloatOrNone2Zero = Field(validation_alias="cg_package_length")
    # 采购包装英制长度 [原字段 'cg_package_length_in']
    package_length_imperial: FloatOrNone2Zero = Field(validation_alias="cg_package_length_in")
    # 采购包装公制宽度 [原字段 'cg_package_width']
    package_width_metric: FloatOrNone2Zero = Field(validation_alias="cg_package_width")
    # 采购包装英制宽度 [原字段 'cg_package_width_in']
    package_width_imperial: FloatOrNone2Zero = Field(validation_alias="cg_package_width_in")
    # 采购包装公制高度 [原字段 'cg_package_height']
    package_height_metric: FloatOrNone2Zero = Field(validation_alias="cg_package_height")
    # 采购包装英制高度 [原字段 'cg_package_height_in']
    package_height_imperial: FloatOrNone2Zero = Field(validation_alias="cg_package_height_in")
    # 采购外箱公制重量 [原字段 'cg_box_weight']
    box_weight_metric: FloatOrNone2Zero = Field(validation_alias="cg_box_weight")
    # 采购外箱公制重量单位 [原字段 'cg_box_weight_unit']
    box_weight_metric_unit: str = Field(validation_alias="cg_box_weight_unit")
    # 采购外箱英制重量 [原字段 'cg_box_weight_in']
    box_weight_imperial: FloatOrNone2Zero = Field(validation_alias="cg_box_weight_in")
    # 采购外箱英制重量单位 [原字段 'cg_box_weight_in_unit']
    box_weight_imperial_unit: str = Field(validation_alias="cg_box_weight_in_unit")
    # 采购外箱公制长度 [原字段 'cg_box_length']
    box_length_metric: FloatOrNone2Zero = Field(validation_alias="cg_box_length")
    # 采购外箱英制长度 [原字段 'cg_box_length_in']
    box_length_imperial: FloatOrNone2Zero = Field(validation_alias="cg_box_length_in")
    # 采购外箱公制宽度 [原字段 'cg_box_width']
    box_width_metric : FloatOrNone2Zero = Field(validation_alias="cg_box_width")
    # 采购外箱英制宽度 [原字段 'cg_box_width_in']
    box_width_imperial: FloatOrNone2Zero = Field(validation_alias="cg_box_width_in")
    # 采购外箱公制高度 [原字段 'cg_box_height']
    box_height_metric: FloatOrNone2Zero = Field(validation_alias="cg_box_height")
    # 采购外箱英制高度 [原字段 'cg_box_height_in']
    box_height_imperial: FloatOrNone2Zero = Field(validation_alias="cg_box_height_in")
    # 采购外箱数量 [原字段 'cg_box_pcs']
    box_qty: IntOrNone2Zero = Field(validation_alias="cg_box_pcs")
    # fmt: on


class SpuProductSpecialAttr(BaseModel):
    """领星本地SPU多属性产品特殊属性"""

    # 特殊属性ID [原字段 'id']
    special_attr_id: int = Field(validation_alias="id")
    # 特殊属性值 [原字段 'value']
    special_attr_value: str = Field(validation_alias="value")


class SpuProductCustomsBaseInfo(BaseModel):
    """领星本地SPU多属性产品信息"""

    # 产品特殊属性 [原字段 'special_attr']
    special_attrs: list[SpuProductSpecialAttr] = Field(validation_alias="special_attr")
    # 报关申报HS编码 (出口国) [原字段 'bg_export_hs_code']
    customs_export_hs_code: str = Field(validation_alias="bg_export_hs_code")


class SpuProductCustomsInfo(BaseModel):
    """领星本地产品海关申报信息"""

    # fmt: off
    # 基础产品信息 [原字段 'base']
    base_info: SpuProductCustomsBaseInfo = Field(validation_alias="base")
    # 海关报关信息
    declaration: ProductCustomsDeclaration
    # 海关清关信息
    clearance: ProductCustomsClearance
    # fmt: on


class SpuProductAuxiliaryMaterial(BaseModel):
    """领星本地产品关联辅料"""

    # 辅料ID
    aux_id: int
    # 辅料SKU
    aux_sku: str
    # 辅料名称
    aux_name: str
    # 辅料备注 [原字段 'remark']
    aux_note: str = Field(validation_alias="remark")
    # 辅料配比数量 [原字段 'aux_qty']
    aux_ratio_qty: int = Field(validation_alias="aux_qty")
    # 产品配比数据 [原字段 'sku_qty']
    sku_ratio_qty: int = Field(validation_alias="sku_qty")
    # 辅料采购数量 [原字段 'quantity']
    purchase_qty: int = Field(validation_alias="quantity")
    # 辅料采购价格 [原字段 'cg_price']
    purchase_price: float = Field(validation_alias="cg_price")


class SpuProductDetailItemImage(BaseModel):
    """领星本地SPU多属性产品详情项图片"""

    # 图片ID [原字段 'pp_id']
    image_id: int = Field(validation_alias="pp_id")
    # 图片名称 [原字段 'pic_name']
    image_name: str = Field(validation_alias="pic_name")
    # 图片链接 [原字段 'pic_url']
    image_url: str = Field(validation_alias="pic_url")
    # 图片大小 (单位: Byte) [原字段 'pic_space']
    image_size: int = Field(validation_alias="pic_space")
    # 图片宽度 (单位: PX) [原字段 'pic_size_w']
    image_width: int = Field(validation_alias="pic_size_w")
    # 图片高度 (单位: PX) [原字段 'pic_size_h']
    image_height: int = Field(validation_alias="pic_size_h")
    # 图片类型 [原字段 'pic_type']
    image_type: int = Field(validation_alias="pic_type")
    # 是否为主图 (0: 否, 1: 是)
    is_primary: int
    # 领星本地产品ID
    product_id: int


class SpuProductDetailItemAttribute(BaseModel):
    """领星本地SPU多属性产品详情项属性"""

    # 属性ID [原字段 'pa_id']
    attr_id: int = Field(validation_alias="pa_id")
    # 属性值ID [原字段 'pai_id']
    attr_value_id: str = Field(validation_alias="pai_id")
    # 属性值名称 [原字段 'pai_name']
    attr_value_name: str = Field(validation_alias="pai_name")


class SpuProductDetailItem(BaseModel):
    """领星本地SPU多属性产品详情项"""

    # fmt: off
    # 领星本地SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 领星本地产品ID
    product_id: int
    # 领星本地产品名称 
    product_name: str
    # 产品图片链接 [原字段 'pic_url']
    image_url: str = Field(validation_alias="pic_url")
    # 产品图片列表 [原字段 'pic_list']
    images: list[SpuProductDetailItemImage] = Field(validation_alias="pic_list")
    # 产品属性列表 [原字段 'attribute']
    attributes: list[SpuProductDetailItemAttribute] = Field(validation_alias="attribute")
    # fmt: on


class SpuProductDetail(BaseModel):
    """领星本地SPU多属性产品详情"""

    # fmt: off
    # 领星SPU多属性产品ID [原字段 'ps_id']
    spu_id: int = Field(validation_alias="ps_id")
    # 领星SPU多属性产品编码
    spu: str
    # 领星SPU多属性产品名称
    spu_name: str
    # 领星本地产品分类ID [原字段 'cid']
    category_id: int = Field(validation_alias="cid")
    # 领星本地产品分类名称
    category_name: str
    # 领星本地产品品牌ID [原字段 'bid']
    brand_id: int = Field(validation_alias="bid")
    # 领星本地产品品牌名称
    brand_name: str
    # 产品图片链接 [原字段 'pic_url']
    image_url: str = Field(validation_alias="pic_url")
    # 产品状态 (0: 停售, 1: 在售, 2: 开发中, 3: 清仓) [原字段 'status']
    status: int
    # 产品状态描述 [原字段 'status_text']
    status_desc: str = Field(validation_alias="status_text")
    # 产品型号 [原字段 'model']
    product_model: str = Field(validation_alias="model")
    # 产品单位 [原字段 'unit']
    product_unit: str = Field(validation_alias="unit")
    # 产品描述 [原字段 'description']
    product_description: str = Field(validation_alias="description")
    # 创建者用户ID (Account.user_id) [原字段 'create_uid']
    product_creator_id: int = Field(validation_alias="create_uid")
    # 创建者姓名 (Account.display_name) [原字段 'create_user']
    product_creator_name: str = Field(validation_alias="create_user")
    # 产品开发者用户ID (Account.user_id) [原字段 'developer_uid']
    product_developer_id: int = Field(validation_alias="developer_uid")
    # 产品开发者姓名 (Account.display_name) [原字段 'developer']
    product_developer_name: str = Field(validation_alias="developer")
    # 产品负责人用户ID列表 (Account.user_id) [原字段 'product_duty_uids']
    operator_ids: list[int] = Field(validation_alias="product_duty_uids")
    # 产品负责人用户信息列表 [原字段 'product_duty_users']
    operators: list[SpuProductOperator] = Field(validation_alias="product_duty_users")
    # 产品采购信息
    purchase_info: SpuProductPurchaseInfo
    # 海关申报信息 [原字段 'logistics']
    customs_info: SpuProductCustomsInfo = Field(validation_alias="logistics")
    # 关联辅料列表 [原字段 'aux_relation_list']
    auxiliary_materials: list[SpuProductAuxiliaryMaterial] = Field(validation_alias="aux_relation_list")
    # 标准产品列表 [原字段 'sku_list']
    items: list[SpuProductDetailItem] = Field(validation_alias="sku_list")
    # 附件信息列表 [原字段 'attachmentFiles']
    attachments: list[base_schema.AttachmentFile] = Field(validation_alias="attachmentFiles")
    # fmt: on


class SpuProductDetailData(ResponseV1):
    """领星本地SPU多属性产品详情"""

    data: SpuProductDetail


# . Edit SPU Product
class EditSpuProductItem(BaseModel):
    """领星本地SPU多属性产品编辑结果项"""

    # 领星本地SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 领星本地产品ID
    product_id: int


class EditSpuProduct(BaseModel):
    """领星本地SPU多属性产品编辑结果"""

    # 领星SPU多属性产品ID [原字段 'ps_id']
    spu_id: int = Field(validation_alias="ps_id")
    # 领星SPU多属性产品列表 [原字段 'sku_list']
    items: list[EditSpuProductItem] = Field(validation_alias="sku_list")


class EditSpuProductResult(ResponseResult):
    """领星本地SPU多属性产品编辑结果"""

    data: EditSpuProduct


# . Bundle Product
class BundleProductItem(BaseModel):
    """领星本地产品组合信息"""

    # 子产品SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 领星本地子产品ID [原字段 'productId']
    product_id: int = Field(validation_alias="productId")
    # 子产品捆绑数量 [原字段 'bundledQty']
    bundle_qty: int = Field(validation_alias="bundledQty")
    # 子产品费用比例
    cost_ratio: float


class BundleProduct(BaseModel):
    """领星本地产品组合信息"""

    # fmt: off
    # 捆绑产品ID [原字段 'id']
    bundle_id: int = Field(validation_alias="id")
    # 捆绑产品SKU [原字段 'sku']
    bundle_sku: str = Field(validation_alias="sku")
    # 捆绑产品名称 [原字段 'product_name']
    bundle_name: str = Field(validation_alias="product_name")
    # 捆绑产品采购价 [原字段 'cg_price']
    purchase_price: float = Field(validation_alias="cg_price")
    # 捆绑产品状态描述 [原字段 'status_text']
    status_desc: str = Field(validation_alias="status_text")
    # 捆绑产品列表 [原字段 'bundled_products']
    items: list[BundleProductItem] = Field(validation_alias="bundled_products")
    # fmt: on


class BundleProducts(ResponseV1):
    """领星本地产品组合列表"""

    data: list[BundleProduct]


# . Edit Bundle Product
class EditBundleProduct(BaseModel):
    """领星本地产品组合编辑结果"""

    # 捆绑产品ID [原字段 'product_id']
    bundle_id: int = Field(validation_alias="product_id")
    # 捆绑产品SKU [原字段 'sku']
    bundle_sku: str = Field(validation_alias="sku")
    # 捆绑产品SKU识别码
    sku_identifier: str


class EditBundleProductResult(ResponseResult):
    """领星本地产品组合编辑结果"""

    data: EditBundleProduct


# . Auxiliary Material
class AuxiliaryMaterialAssociate(BaseModel):
    """领星本地产品辅料关联的产品信息"""

    # 领星本地产品SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 领星本地产品ID [原字段 'pid']
    product_id: int = Field(validation_alias="pid")
    # 领星本地产品名称
    product_name: str
    # 产品关联辅料的数量 [原字段 'quantity']
    aux_qty: int = Field(validation_alias="quantity")
    # 辅料配比数量 [原字段 'aux_qty']
    aux_ratio_qty: int = Field(validation_alias="aux_qty")
    # 产品配比数据 [原字段 'sku_qty']
    sku_ratio_qty: int = Field(validation_alias="sku_qty")


class AuxiliaryMaterial(BaseModel):
    """领星本地产品辅料信息"""

    # fmt: off
    # 辅料分类ID [原字段 'cid']
    category_id: int = Field(validation_alias="cid")
    # 辅料ID [原字段 'id']
    aux_id: int = Field(validation_alias="id")
    # 辅料SKU [原字段 'sku']
    aux_sku: str = Field(validation_alias="sku")
    # 辅料名称 [原字段 'product_name']
    aux_name: str = Field(validation_alias="product_name")
    # 辅料净重 [原字段 'cg_product_net_weight']
    aux_net_weight: float = Field(validation_alias="cg_product_net_weight")
    # 辅料长度 [原字段 'cg_product_length']
    aux_length: float = Field(validation_alias="cg_product_length")
    # 辅料宽度 [原字段 'cg_product_width']
    aux_width: float = Field(validation_alias="cg_product_width")
    # 辅料高度 [原字段 'cg_product_height']
    aux_height: float = Field(validation_alias="cg_product_height")
    # 辅料备注 [原字段 'remark']
    aux_note: str = Field(validation_alias="remark")
    # 辅料采购价格 [原字段 'cg_price']
    purchase_price: float = Field(validation_alias="cg_price")
    # 辅料关联的产品列表 [原字段 'aux_relation_product']
    associates: list[AuxiliaryMaterialAssociate] = Field(validation_alias="aux_relation_product")
    # 供应商报价信息列表 [原字段 'supplier_quote']
    supplier_quotes: list[ProductSupplierQuote] = Field(validation_alias="supplier_quote")
    # fmt: on


class AuxiliaryMaterials(ResponseV1):
    """领星本地产品辅料列表"""

    data: list[AuxiliaryMaterial]


# . Edit Auxiliary Material
class EditAuxiliaryMaterial(BaseModel):
    """领星本地产品辅料编辑结果"""

    # 辅料ID [原字段 'product_id']
    aux_id: int = Field(validation_alias="product_id")
    # 辅料SKU [原字段 'sku']
    aux_sku: str = Field(validation_alias="sku")
    # 辅料SKU识别码
    sku_identifier: str


class EditAuxiliaryMaterialResult(ResponseResult):
    """领星本地产品辅料编辑结果"""

    data: EditAuxiliaryMaterial


# . Product Codes
class ProductCode(BaseModel):
    # 产品编码 ID [原字段 'id']
    code_id: int = Field(validation_alias="id")
    # 产品编码 [原字段 'commodity_code']
    code: str = Field(validation_alias="commodity_code")
    # 编码类型
    code_type: str
    # 编码备注 [原字段 'remark']
    code_note: str = Field(validation_alias="remark")
    # 编码状态 (0: 未使用, 1: 已使用) [原字段 'is_used']
    status: int = Field(validation_alias="is_used")
    # 编码状态描述 [原字段 'is_used_desc']
    status_desc: str = Field(validation_alias="is_used_desc")
    # 创建人的用户ID (Account.user_id) [原字段 'created_user_id']
    create_user_id: int = Field(validation_alias="created_user_id")
    # 创建时间 (北京时间) [原字段 'gmt_create']
    create_time: str = Field(validation_alias="gmt_create")
    # 使用人的用户ID (Account.user_id)
    use_user_id: int
    # 使用时间 (北京时间)
    use_time: str


class ProductCodes(ResponseV1, FlattenDataList):
    """产品编码 (UPC/EAN/ISBN)"""

    data: list[ProductCode]


# . Product Global Tag
class ProductGlobalTag(BaseModel):
    """领星本地产品全局标签信息"""

    # 全局标签ID [原字段 'label_id']
    tag_id: str = Field(validation_alias="label_id")
    # 全局标签名称 [原字段 'label_name']
    tag_name: str = Field(validation_alias="label_name")
    # 全局标签创建时间 (UTC毫秒时间戳) [原字段 'gmt_created']
    create_time_ts: int = Field(validation_alias="gmt_created")


class ProductGlobalTags(ResponseV1, FlattenDataList):
    """领星本地产品全局标签信息"""

    data: list[ProductGlobalTag]


# . Create Product Global Tag
class CreateProductGlobalTag(BaseModel):
    """创建产品全局标签结果"""

    # 全局标签ID [原字段 'label_id']
    tag_id: str = Field(validation_alias="label_id")
    # 全局标签名称 [原字段 'label_name']
    tag_name: str = Field(validation_alias="label_name")


class CreateProductGlobalTagResult(ResponseResult):
    """创建产品全局标签结果"""

    data: CreateProductGlobalTag


# . Product Global Attributes
class ProductGlobalAttributeValue(BaseModel):
    """领星本地产品全局属性值"""

    # 产品属性ID 【原字段 'pa_id'】
    attr_id: int = Field(validation_alias="pa_id")
    # 产品属性值ID [原字段 'pai_id']
    attr_value_id: int = Field(validation_alias="pai_id")
    # 产品属性值编码 [原字段 'attr_val_code']
    attr_value_code: str = Field(validation_alias="attr_val_code")
    # 产品属性值 [原字段 'attr_value']
    attr_value: str
    # 产品属性值创建时间 (北京时间)
    create_time: str


class ProductGlobalAttribute(BaseModel):
    """领星本地产品全局属性"""

    # 产品属性ID [原字段 'pa_id']
    attr_id: int = Field(validation_alias="pa_id")
    # 产品属性名称
    attr_name: str
    # 产品属性编码
    attr_code: str
    # 产品子属性列表 [原字段 'item_list']
    attr_values: list[ProductGlobalAttributeValue] = Field(validation_alias="item_list")
    # 产品属性创建时间 (北京时间)
    create_time: str


class ProductGlobalAttributes(ResponseV1, FlattenDataList):
    """领星本地产品全局属性"""

    data: list[ProductGlobalAttribute]


# . Product Brand
class ProductBrand(BaseModel):
    """领星本地产品品牌信息"""

    # 领星本地品牌ID [原字段 'bid']
    brand_id: int = Field(validation_alias="bid")
    # 品牌名称 [原字段 'title']
    brand_name: str = Field(validation_alias="title")
    # 品牌编码
    brand_code: str


class ProductBrands(ResponseV1):
    """领星本地产品品牌列表"""

    data: list[ProductBrand]


# . Edit Product Brand
class EditProductBrand(BaseModel):
    """更新产品品牌结果"""

    # 添加/编辑的产品品牌ID [原字段 'id']
    brand_id: int = Field(validation_alias="id")
    # 添加/编辑的产品品牌名称 [原字段 'title']
    brand_name: str = Field(validation_alias="title")
    # 添加/编辑的产品品牌编码
    brand_code: str


class EditProductBrandsResult(ResponseResult):
    """更新产品品牌结果"""

    data: list[EditProductBrand]


# . Product Category
class ProductCategory(BaseModel):
    """领星本地产品分类信息"""

    # 领星本地产品分类ID [原字段 'cid']
    category_id: int = Field(validation_alias="cid")
    # 分类名称 [原字段 'title']
    category_name: str = Field(validation_alias="title")
    # 分类编码
    category_code: str
    # 父分类ID [原字段 'parent_cid']
    parent_category_id: int = Field(validation_alias="parent_cid")


class ProductCategories(ResponseV1):
    """领星本地产品分类列表"""

    data: list[ProductCategory]


# . Edit Product Category
class EditProductCategory(BaseModel):
    """更新产品分类结果"""

    # 添加/编辑的产品分类ID [原字段 'id']
    category_id: int = Field(validation_alias="id")
    # 添加/编辑的产品分类名称 [原字段 'title']
    category_name: str = Field(validation_alias="title")
    # 添加/编辑的产品分类编码
    category_code: str
    # 父分类ID [原字段 'parent_cid']
    parent_category_id: str = Field(validation_alias="parent_cid")


class EditProductCategoriesResult(ResponseResult):
    """更新产品分类结果"""

    data: list[EditProductCategory]
