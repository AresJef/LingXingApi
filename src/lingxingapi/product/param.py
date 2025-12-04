# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import ValidationInfo, Field, field_validator
from lingxingapi import utils
from lingxingapi.base.param import Parameter, PageOffestAndLength
from lingxingapi.fields import (
    NonEmptyStr,
    CurrencyCode,
    NonNegativeInt,
    NonNegativeFloat,
)


# 产品 --------------------------------------------------------------------------------------------------------------------------
# . Products
class Products(PageOffestAndLength):
    """产品列表查询参数"""

    # 领星本地SKU列表
    lskus: Optional[list] = Field(None, alias="sku_list")
    # 领星本地SKU识别码
    sku_identifiers: Optional[list] = Field(None, alias="sku_identifier")
    # 产品更新开始时间, 左闭右开 (时间戳, 单位: 秒)
    update_start_time: Optional[int] = Field(None, alias="update_time_start")
    # 产品更新结束时间, 左闭右开 (时间戳, 单位: 秒)
    update_end_time: Optional[int] = Field(None, alias="update_time_end")
    # 产品创建开始时间, 左闭右开 (时间戳, 单位: 秒)
    create_start_time: Optional[int] = Field(None, alias="create_time_start")
    # 产品创建结束时间, 左闭右开 (时间戳, 单位: 秒)
    create_end_time: Optional[int] = Field(None, alias="create_time_end")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("lskus", mode="before")
    @classmethod
    def _validate_lskus(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_non_empty_str(v, "领星本地SKU lskus")

    @field_validator("sku_identifiers", mode="before")
    @classmethod
    def _validate_sku_identifiers(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_str(v, "领星SKU识别码 sku_identifiers")

    @field_validator(
        "update_start_time",
        "update_end_time",
        "create_start_time",
        "create_end_time",
        mode="before",
    )
    @classmethod
    def _validate_time(cls, v: Optional[int], info: ValidationInfo) -> int | None:
        if v is None:
            return None
        dt = utils.validate_datetime(v, False, "产品时间 %s" % info.field_name)
        return int(dt.toseconds())


class EnableDisableProducts(Parameter):
    """批量启用/禁用产品参数"""

    # 产品起停用状态 (1: 启用, 2: 禁用)
    status: str = Field(alias="batch_status")
    # 领星本地产品ID列表 (Product.product_id)
    product_ids: list

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("status", mode="before")
    @classmethod
    def _validate_status(cls, v: str) -> str:
        if v in (1, "Enable", "1"):
            return "Enable"
        if v in (0, "Disable", "0"):
            return "Disable"
        raise ValueError("产品起停用 status 必须为 (0/Disable) 或 (1/Enable)")

    @field_validator("product_ids", mode="before")
    @classmethod
    def _validate_product_ids(cls, v) -> list[int]:
        return utils.validate_array_of_unsigned_int(v, "领星本地产品ID product_ids")


# . Product Details
class ProductDetails(Parameter):
    """产品详情查询参数"""

    # 领星本地SKU列表 (Product.lsku)
    lskus: Optional[list] = Field(None, alias="skus")
    # 领星本地SKU识别码列表 (Product.sku_identifier)
    sku_identifiers: Optional[list] = Field(None, alias="sku_identifiers")
    # 领星本地产品ID列表 (Product.product_id)
    product_ids: Optional[list] = Field(None, alias="productIds")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("lskus", mode="before")
    @classmethod
    def _validate_lskus(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_non_empty_str(v, "领星本地SKU lskus")

    @field_validator("sku_identifiers", mode="before")
    @classmethod
    def _validate_sku_identifiers(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_str(v, "领星SKU识别码 sku_identifiers")

    @field_validator("product_ids", mode="before")
    @classmethod
    def _validate_product_ids(cls, v) -> list[int] | None:
        if v is None:
            return None
        return utils.validate_array_of_unsigned_int(v, "领星本地产品ID product_ids")


# . Edit Product
class EditProductImage(Parameter):
    """编辑产品图片参数"""

    # 图片链接
    image_url: NonEmptyStr = Field(alias="pic_url")
    # 是否为主图 (0: 否, 1: 是)
    is_primary: NonNegativeInt


class EditProductBundleItem(Parameter):
    """编辑产品捆绑参数"""

    # 领星本地子产品SKU
    lsku: NonEmptyStr = Field(alias="sku")
    # 子产品数量
    product_qty: NonNegativeInt = Field(alias="quantity")


class EditProductQuotePriceTeir(Parameter):
    """编辑产品报价定价梯度参数"""

    # fmt: off
    # 最小订购量 (MOQ)
    moq: int = Field(gt=0)
    # 报价 (含税)
    price_with_tax: NonNegativeFloat
    # fmt: on


class EditProductQuotePricing(Parameter):
    """编辑产品报价参数"""

    # fmt: off
    # 报价货币代码 (目前只支持CNY和USD)
    currency_code: CurrencyCode = Field(alias="currency")
    # 报价是否含税 (0: 否, 1: 是)
    is_tax_inclusive: NonNegativeInt = Field(alias="is_tax")
    # 报价税率 (百分比, 如 5% 则传 5)
    tax_rate: NonNegativeFloat = 0
    # 报价梯度 [原字段 'step_prices']
    price_tiers: list = Field(alias="step_prices")
    # fmt: on

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("price_tiers", mode="before")
    @classmethod
    def _validate_price_tiers(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            return [EditProductQuotePriceTeir.model_validate_params(v)]
        else:
            return [EditProductQuotePriceTeir.model_validate_params(i) for i in v]


class EditProductSupplierQuote(Parameter):
    """编辑产品供应商报价参数"""

    # fmt: off
    # 供应商ID (Supplier.supplier_id)
    supplier_id: NonNegativeInt = Field(alias="erp_supplier_id")
    # 是否是首选供应商 (0: 否, 1: 是)
    is_primary: NonNegativeInt
    # 供应商产品链接 (最多20个，没有则传空数组)
    product_urls: Optional[list] = Field(None, alias="supplier_product_url")
    # 报价备注
    quote_note: Optional[str] = Field(None, alias="quote_remark")
    # 报价列表
    quotes: list
    # fmt: on
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("product_urls", mode="before")
    @classmethod
    def _validate_product_urls(cls, v) -> list[str] | None:
        if v is None:
            return None
        return utils.validate_array_of_str(v, "供应商产品链接 product_urls")

    @field_validator("quotes", mode="before")
    @classmethod
    def _validate_quotes(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            return [EditProductQuotePricing.model_validate_params(v)]
        else:
            return [EditProductQuotePricing.model_validate_params(i) for i in v]


class EditCustomsDeclaration(Parameter):
    """编辑产品报关申报参数"""

    # fmt: off
    # 报关申报品名 (出口国)
    export_name: Optional[str] = Field(None, alias="customs_export_name")
    # 报关申报品名 (进口国)
    import_name: Optional[str] = Field(None, alias="customs_import_name")
    # 报关申报单价 (进口国)
    import_price: Optional[NonNegativeFloat] = Field(None, alias="customs_import_price")
    # 报关申报单价货币代码 (进口国)
    currency_code: Optional[str] = Field(None, alias="customs_import_price_currency")
    # 报关申报产品单位
    unit: Optional[str] = Field(None, alias="customs_declaration_unit")
    # 报关申报产品规格 
    specification: Optional[str] = Field(None, alias="customs_declaration_spec")
    # 报关申报产品原产地
    country_of_origin: Optional[str] = Field(None, alias="customs_declaration_origin_produce")
    # 报关申报内陆来源
    source_from_inland: Optional[str] = Field(None, alias="customs_declaration_inlands_source")
    # 报关申报免税
    exemption: Optional[str] = Field(None, alias="customs_declaration_exempt")
    # fmt: on


class EditCustomsClearance(Parameter):
    """编辑产品报关清关参数"""

    # fmt: off
    # 清关内部编码
    internal_code: Optional[str] = Field(None, alias="customs_clearance_internal_code")
    # 清关产品材质
    material: Optional[str] = Field(None, alias="customs_clearance_material")
    # 清关产品用途
    usage: Optional[str] = Field(None, alias="customs_clearance_usage")
    # 清关是否享受优惠 (0: 未设置, 1: 不享惠, 2: 享惠, 3: 不确定)
    preferential: Optional[NonNegativeInt] = Field(None, alias="customs_clearance_preferential")
    # 清关品牌类型 (0: 未设置, 1: 无品牌, 2: 境内品牌[自主], 3: 境内品牌[收购], 4: 境外品牌[贴牌], 5: 境外品牌[其他])
    brand_type: Optional[NonNegativeInt] = Field(None, alias="customs_clearance_brand_type")
    # 清关产品型号
    model: Optional[str] = Field(None, alias="customs_clearance_product_pattern")
    # 清关产品图片链接
    image_url: Optional[str] = Field(None, alias="customs_clearance_pic_url")
    # 配货备注
    allocation_note: Optional[str] = Field(None, alias="allocation_remark")
    # 织造类型 (0: 未设置, 1: 针织, 2: 梭织)
    fabric_type: Optional[NonNegativeInt] = Field(None, alias="weaving_mode")
    # fmt: on


class EditProduct(Parameter):
    """编辑产品参数"""

    # fmt: off
    # 领星本地SKU (Product.lsku)
    lsku: NonEmptyStr = Field(alias="sku")
    # 领星本地产品名称 (Product.product_name)
    product_name: NonEmptyStr
    # 领星本地SKU识别码
    sku_identifier: Optional[str] = None
    # 领星本地产品分类ID (当ID与名称同时存在时, ID优先)
    category_id: Optional[NonNegativeInt] = None
    # 领星本地产品分类名称
    category_name: Optional[str] = Field(None, alias="category")
    # 领星本地产品品牌ID (当ID与名称同时存在时, ID优先)
    brand_id: Optional[NonNegativeInt] = None
    # 领星本地产品品牌名称
    brand_name: Optional[str] = Field(None, alias="brand")
    # 产品型号
    product_model: Optional[str] = Field(None, alias="model")
    # 产品单位 
    product_unit: Optional[str] = Field(None, alias="unit")
    # 产品描述
    product_description: Optional[str] = Field(None, alias="description")
    # 产品图片列表
    product_images: Optional[list] = Field(None, alias="picture_list")
    # 产品特殊属性列表 (1: 含电, 2: 纯电, 3: 液体, 4: 粉末, 5: 膏体, 6: 带磁)
    product_special_attrs: Optional[list] = Field(None, alias="special_attr")
    # 产品状态 (0: 停售, 1: 在售, 2: 开发中, 3: 清仓 | 默认: 1)
    status: Optional[NonNegativeInt] = None
    # 组合产品所包含的单品列表
    bundle_items: Optional[list] = Field(None, alias="group_list")
    # 是否自动计算组合产品采购价格 (0: 手动, 1: 自动 | 选择自动后, 组合产品采购价格为所包含单品成本的总计)
    auto_bundle_purchase_price: Optional[NonNegativeInt] = Field(None, alias="is_related")
    # 产品创建人ID (默认API账号ID)
    product_creator_id: Optional[NonNegativeInt] = Field(None, alias="product_creator_uid")
    # 产品开发者用户ID (当ID与名称同时存在时, ID优先)
    product_developer_id: Optional[NonNegativeInt] = Field(None, alias="product_developer_uid")
    # 产品开发者姓名
    product_developer_name: Optional[str] = Field(None, alias="product_developer")
    # 产品采购人ID (当ID与名称同时存在时, ID优先)
    purchase_staff_id: Optional[NonNegativeInt] = Field(None, alias="cg_opt_uid")
    # 产品采购人姓名
    purchase_staff_name: Optional[str] = Field(None, alias="cg_opt_username")
    # 采购交期 (单位: 天)
    purchase_delivery_time: Optional[NonNegativeInt] = Field(None, alias="cg_delivery")
    # 采购价格
    purchase_price: Optional[NonNegativeFloat] = Field(None, alias="cg_price")
    # 采购备注
    purchase_note: Optional[str] = Field(None, alias="purchase_remark")
    # 采购产品材质
    product_material: Optional[str] = Field(None, alias="cg_product_material")
    # 采购产品总重 (单位: G)
    product_gross_weight: Optional[NonNegativeFloat] = Field(None, alias="cg_product_gross_weight")
    # 采购产品净重 (单位: G)
    product_net_weight: Optional[NonNegativeFloat] = Field(None, alias="cg_product_net_weight")
    # 采购产品长度 (单位: CM)
    product_length: Optional[NonNegativeFloat] = Field(None, alias="cg_product_length")
    # 采购产品宽度 (单位: CM)
    product_width: Optional[NonNegativeFloat] = Field(None, alias="cg_product_width")
    # 采购产品高度 (单位: CM)
    product_height: Optional[NonNegativeFloat] = Field(None, alias="cg_product_height")
    # 采购包装长度 (单位: CM)
    package_length: Optional[NonNegativeFloat] = Field(None, alias="cg_package_length")
    # 采购包装宽度 (单位: CM)
    package_width: Optional[NonNegativeFloat] = Field(None, alias="cg_package_width")
    # 采购包装高度 (单位: CM)
    package_height: Optional[NonNegativeFloat] = Field(None, alias="cg_package_height")
    # 采购外箱重量 (单位: KG)
    box_weight: Optional[NonNegativeFloat] = Field(None, alias="cg_box_weight")
    # 采购外箱长度 (单位: CM)
    box_length: Optional[NonNegativeFloat] = Field(None, alias="cg_box_length")
    # 采购外箱宽度 (单位: CM)
    box_width : Optional[NonNegativeFloat] = Field(None, alias="cg_box_width")
    # 采购外箱高度 (单位: CM)
    box_height: Optional[NonNegativeFloat] = Field(None, alias="cg_box_height")
    # 采购外箱数量
    box_qty: Optional[NonNegativeInt] = Field(None, alias="cg_box_pcs")
    # 供应商报价信息列表 (传空列表则清空产品供应商报价)
    supplier_quotes: Optional[list] = Field(None, alias="supplier_quote")
    # 报关申报品名 (出口国)
    customs_export_name: Optional[str] = Field(None, alias="bg_customs_export_name")
    # 报关申报HS编码 (出口国)
    customs_export_hs_code: Optional[str] = Field(None, alias="bg_export_hs_code")
    # 报关申报品名 (进口国)
    customs_import_name: Optional[str] = Field(None, alias="bg_customs_import_name")
    # 报关申报单价 (进口国)
    customs_import_price: Optional[NonNegativeFloat] = Field(None, alias="bg_customs_import_price")
    # 报关申报单价货币代码 (进口国)
    customs_import_currency_code: Optional[str] = Field(None, alias="currency")
    # 报关信息
    customs_declaration: Optional[dict] = Field(None, alias="declaration")
    # 清关信息
    customs_clearance: Optional[dict] = Field(None, alias="clearance")
    # 产品负责人ID列表
    operator_ids: Optional[list] = Field(None, alias="product_duty_uids")
    # 产品负责人ID的更新模式 (0: 覆盖, 1: 追加 | 默认: 1)
    operator_update_mode: Optional[NonNegativeInt] = Field(None, alias="is_append_product_duty")
    # fmt: on

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("product_images", mode="before")
    @classmethod
    def _validate_product_images(cls, v) -> list[dict] | None:
        if v is None:
            return None
        elif not isinstance(v, (list, tuple)):
            return [EditProductImage.model_validate_params(v)]
        else:
            return [EditProductImage.model_validate_params(i) for i in v]

    @field_validator("product_special_attrs", "operator_ids", mode="before")
    @classmethod
    def _validate_unsigned_int_array(cls, v, info: ValidationInfo) -> list[int] | None:
        if v is None:
            return None
        if not v:
            return []
        return utils.validate_array_of_unsigned_int(v, info.field_name)

    @field_validator("bundle_items", mode="before")
    @classmethod
    def _validate_bundle_items(cls, v) -> list[dict] | None:
        if v is None:
            return None
        elif not isinstance(v, (list, tuple)):
            return [EditProductBundleItem.model_validate_params(v)]
        else:
            return [EditProductBundleItem.model_validate_params(i) for i in v]

    @field_validator("supplier_quotes", mode="before")
    @classmethod
    def _validate_supplier_quotes(cls, v) -> list[dict] | None:
        if v is None:
            return None
        elif not isinstance(v, (list, tuple)):
            return [EditProductSupplierQuote.model_validate_params(v)]
        else:
            return [EditProductSupplierQuote.model_validate_params(i) for i in v]

    @field_validator("customs_declaration", mode="before")
    @classmethod
    def _validate_customs_declaration(cls, v) -> dict | None:
        if v is None:
            return None
        return EditCustomsDeclaration.model_validate_params(v)

    @field_validator("customs_clearance", mode="before")
    @classmethod
    def _validate_customs_clearance(cls, v) -> dict | None:
        if v is None:
            return None
        return EditCustomsClearance.model_validate_params(v)


# . Spu Products
class SpuProductDetail(Parameter):
    """SPU产品详情查询参数"""

    # 领星SPU多属性产品ID (SpuProduct.spu_id)
    spu_id: NonNegativeInt = Field(alias="ps_id")
    # 领星SPU多属性产品编码
    spu: NonEmptyStr


# . Edit Spu Product
class EditSpuProductItemAttribute(Parameter):
    """编辑SPU多属性产品子项属性参数"""

    # 属性ID
    attr_id: NonNegativeInt = Field(alias="pa_id")
    # 属性名称
    attr_value_id: NonNegativeInt = Field(alias="pai_id")


class EditSpuProductItem(Parameter):
    """编辑SPU多属性产品子项参数"""

    # 子产品本地SKU
    lsku: NonEmptyStr = Field(alias="sku")
    # 子产品本地名称
    product_name: Optional[NonEmptyStr] = None
    # 子产品图片列表
    images: Optional[list] = Field(None, alias="picture_list")
    # 子产品属性
    attributes: list = Field(alias="attribute")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("attributes", mode="before")
    @classmethod
    def _validate_attributes(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            return [EditSpuProductItemAttribute.model_validate_params(v)]
        else:
            return [EditSpuProductItemAttribute.model_validate_params(i) for i in v]

    @field_validator("images", mode="before")
    @classmethod
    def _validate_images(cls, v) -> list[dict] | None:
        if v is None:
            return None
        elif not isinstance(v, (list, tuple)):
            return [EditProductImage.model_validate_params(v)]
        else:
            return [EditProductImage.model_validate_params(i) for i in v]


class EditSpuProductPurchaseInfo(Parameter):
    """编辑SPU多属性产品采购信息参数"""

    # fmt: off
    # 产品采购人用户ID (Account.user_id)
    purchase_staff_id: Optional[NonNegativeInt] = Field(None, alias="cg_uid")
    # 采购交期 (单位: 天)
    purchase_delivery_time: Optional[NonNegativeInt] = Field(None, alias="cg_delivery")
    # 采购备注
    purchase_note: Optional[str] = Field(None, alias="purchase_remark")
    # 采购产品材质
    product_material: Optional[str] = Field(None, alias="cg_product_material")
    # 采购产品总重 (单位: G)
    product_gross_weight: Optional[NonNegativeFloat] = Field(None, alias="cg_product_gross_weight")
    # 采购产品净重 (单位: G)
    product_net_weight: Optional[NonNegativeFloat] = Field(None, alias="cg_product_net_weight")
    # 采购产品长度 (单位: CM)
    product_length: Optional[NonNegativeFloat] = Field(None, alias="cg_product_length")
    # 采购产品宽度 (单位: CM)
    product_width: Optional[NonNegativeFloat] = Field(None, alias="cg_product_width")
    # 采购产品高度 (单位: CM)
    product_height: Optional[NonNegativeFloat] = Field(None, alias="cg_product_height")
    # 采购包装长度 (单位: CM)
    package_length: Optional[NonNegativeFloat] = Field(None, alias="cg_package_length")
    # 采购包装宽度 (单位: CM)
    package_width: Optional[NonNegativeFloat] = Field(None, alias="cg_package_width")
    # 采购包装高度 (单位: CM)
    package_height: Optional[NonNegativeFloat] = Field(None, alias="cg_package_height")
    # 采购外箱重量 (单位: KG)
    box_weight: Optional[NonNegativeFloat] = Field(None, alias="cg_box_weight")
    # 采购外箱长度 (单位: CM)
    box_length: Optional[NonNegativeFloat] = Field(None, alias="cg_box_length")
    # 采购外箱宽度 (单位: CM)
    box_width: Optional[NonNegativeFloat] = Field(None, alias="cg_box_width")
    # 采购外箱高度 (单位: CM)
    box_height: Optional[NonNegativeFloat] = Field(None, alias="cg_box_height")
    # 采购外箱数量
    box_qty: Optional[NonNegativeInt] = Field(None, alias="cg_box_pcs")
    # fmt: on


class EditSpuProductCustomsBaseInfo(Parameter):
    """编辑SPU多属性产品报关信息参数"""

    # 报关申报HS编码 (出口国)
    customs_export_hs_code: Optional[str] = Field(None, alias="bg_export_hs_code")
    # 产品特殊属性 (1: 含电, 2: 纯电, 3: 液体, 4: 粉末, 5: 膏体, 6: 带磁)
    special_attrs: Optional[list] = Field(None, alias="special_attr")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("special_attrs", mode="before")
    @classmethod
    def _validate_special_attrs(cls, v) -> list[int] | None:
        if v is None:
            return None
        if not v:
            return []
        return utils.validate_array_of_unsigned_int(v, "产品特殊属性 special_attrs")


class EditSpuProductCustomsInfo(Parameter):
    """编辑SPU多属性产品报关信息参数"""

    # 基础产品信息
    base_info: Optional[dict] = Field(None, alias="base")
    # 海关报关信息
    declaration: Optional[dict] = None
    # 海关清关信息
    clearance: Optional[dict] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("base_info", mode="before")
    @classmethod
    def _validate_base_info(cls, v) -> dict | None:
        if v is None:
            return None
        return EditSpuProductCustomsBaseInfo.model_validate_params(v)

    @field_validator("declaration", mode="before")
    @classmethod
    def _validate_declaration(cls, v) -> dict | None:
        if v is None:
            return None
        return EditCustomsDeclaration.model_validate_params(v)

    @field_validator("clearance", mode="before")
    @classmethod
    def _validate_clearance(cls, v) -> dict | None:
        if v is None:
            return None
        return EditCustomsClearance.model_validate_params(v)


class EditSpuProduct(Parameter):
    """编辑SPU多属性产品参数"""

    # fmt: off
    # 领星SPU多属性产品编码
    spu: NonEmptyStr
    # 领星SPU多属性产品名称
    spu_name: NonEmptyStr
    # 子产品列表
    items: list = Field(alias="sku_list")
    # 领星本地产品分类ID
    category_id: Optional[NonNegativeInt] = Field(None, alias="cid")
    # 领星本地产品品牌ID
    brand_id: Optional[NonNegativeInt] = Field(None, alias="bid")
    # 产品型号
    product_model: Optional[str] = Field(None, alias="model")
    # 产品单位
    product_unit: Optional[str] = Field(None, alias="unit")
    # 产品描述
    product_description: Optional[str] = Field(None, alias="description")
    # 产品状态 (0: 停售, 1: 在售, 2: 开发中, 3: 清仓 | 默认: 1)
    status: Optional[NonNegativeInt] = None
    # 产品创建人ID (默认API账号ID)
    product_creator_id: Optional[NonNegativeInt] = Field(None, alias="create_uid")
    # 产品开发者用户ID
    product_developer_id: Optional[NonNegativeInt] = Field(None, alias="developer_uid")
    # 产品负责人ID列表
    operator_ids: Optional[list] = Field(None, alias="product_duty_uids")
    # 是否应用SPU多属性产品基础信息至新生成的SKU (0: 否, 1: 是)
    apply_to_new_skus: Optional[NonNegativeInt] = Field(None, alias="use_spu_template")
    # 采购信息
    purchase_info: Optional[dict] = None
    # 海关申报信息
    customs_info: Optional[dict] = Field(None, alias="logistics")
    # fmt: on

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("items", mode="before")
    @classmethod
    def _validate_items(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            return [EditSpuProductItem.model_validate_params(v)]
        else:
            return [EditSpuProductItem.model_validate_params(i) for i in v]

    @field_validator("operator_ids", mode="before")
    @classmethod
    def _validate_unsigned_int_array(cls, v, info: ValidationInfo) -> list[int] | None:
        if v is None:
            return None
        if not v:
            return []
        return utils.validate_array_of_unsigned_int(v, info.field_name)

    @field_validator("purchase_info", mode="before")
    @classmethod
    def _validate_purchase_info(cls, v) -> dict | None:
        if v is None:
            return None
        return EditSpuProductPurchaseInfo.model_validate_params(v)

    @field_validator("customs_info", mode="before")
    @classmethod
    def _validate_customs_info(cls, v) -> dict | None:
        if v is None:
            return None
        return EditSpuProductCustomsInfo.model_validate_params(v)


# . Edit Bundle Product
class EditBundleProductItem(Parameter):
    """编辑组合产品子项参数"""

    # 子产品SKU
    lsku: Optional[NonEmptyStr] = Field(None, alias="sku")
    # 子产品捆绑数量
    bundle_qty: Optional[NonNegativeInt] = Field(None, alias="quantity")
    # 子产品费用比例
    cost_ratio: Optional[NonNegativeFloat] = None


class EditBundleProduct(Parameter):
    """编辑组合产品参数"""

    # fmt: off
    # 捆绑产品本地SKU
    bundle_sku: NonEmptyStr = Field(alias="sku")
    # 捆绑产品本地名称
    bundle_name: NonEmptyStr = Field(alias="product_name")
    # 领星本地产品分类ID (当ID与名称同时存在时, ID优先)
    category_id: Optional[NonNegativeInt] = None
    # 领星本地产品分类名称
    category_name: Optional[str] = Field(None, alias="category")
    # 领星本地产品品牌ID (当ID与名称同时存在时, ID优先)
    brand_id: Optional[NonNegativeInt] = None
    # 领星本地产品品牌名称
    brand_name: Optional[str] = Field(None, alias="brand")
    # 产品型号
    product_model: Optional[str] = Field(None, alias="model")
    # 产品单位
    product_unit: Optional[str] = Field(None, alias="unit")
    # 产品描述
    product_description: Optional[str] = Field(None, alias="description")
    # 产品图片列表
    product_images: Optional[list] = Field(None, alias="picture_list")
    # 产品创建人ID (默认API账号ID)
    product_creator_id: Optional[NonNegativeInt] = Field(None, alias="product_creator_uid")
    # 产品开发者用户ID (当ID与名称同时存在时, ID优先)
    product_developer_id: Optional[NonNegativeInt] = Field(None, alias="product_developer_uid")
    # 产品开发者姓名
    product_developer_name: Optional[str] = Field(None, alias="product_developer")
    # 产品负责人ID列表
    operator_ids: Optional[list] = Field(None, alias="product_duty_uids")
    # 产品负责人ID的更新模式 (0: 覆盖, 1: 追加 | 默认: 1)
    operator_update_mode: Optional[NonNegativeInt] = Field(None, alias="is_append_product_duty")
    # 组合产品所包含的单品列表
    items: Optional[list] = Field(None, alias="group_list")
    # fmt: on

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("product_images", mode="before")
    @classmethod
    def _validate_product_images(cls, v) -> list[dict] | None:
        if v is None:
            return None
        elif not isinstance(v, (list, tuple)):
            return [EditProductImage.model_validate_params(v)]
        else:
            return [EditProductImage.model_validate_params(i) for i in v]

    @field_validator("operator_ids", mode="before")
    @classmethod
    def _validate_operator_ids(cls, v, info: ValidationInfo) -> list[int] | None:
        if v is None:
            return None
        if not v:
            return []
        return utils.validate_array_of_unsigned_int(v, info.field_name)

    @field_validator("items", mode="before")
    @classmethod
    def _validate_items(cls, v) -> list[dict] | None:
        if v is None:
            return None
        elif not isinstance(v, (list, tuple)):
            return [EditBundleProductItem.model_validate_params(v)]
        else:
            return [EditBundleProductItem.model_validate_params(i) for i in v]


# . Edit Auxiliary Materials
class EditAuxiliaryMaterial(Parameter):
    """编辑辅助材料参数"""

    # fmt: off
    # 辅料SKU
    aux_sku: NonEmptyStr = Field(alias="sku")
    # 辅料名称
    aux_name: NonEmptyStr = Field(alias="product_name")
    # 辅料净重
    aux_net_weight: Optional[NonNegativeFloat] = Field(None, alias="cg_product_net_weight")
    # 辅料长度
    aux_length: Optional[NonNegativeFloat] = Field(None, alias="cg_product_length")
    # 辅料宽度
    aux_width: Optional[NonNegativeFloat] = Field(None, alias="cg_product_width")
    # 辅料高度
    aux_height: Optional[NonNegativeFloat] = Field(None, alias="cg_product_height")
    # 辅料备注
    aux_note: Optional[str] = Field(None, alias="remark")
    # 辅料采购价格
    purchase_price: Optional[NonNegativeFloat] = Field(None, alias="cg_price")
    # 供应商报价信息列表
    supplier_quotes: Optional[list] = Field(None, alias="supplier_quote")
    # fmt: on

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("supplier_quotes", mode="before")
    @classmethod
    def _validate_supplier_quotes(cls, v) -> list[dict] | None:
        if v is None:
            return None
        elif not isinstance(v, (list, tuple)):
            return [EditProductSupplierQuote.model_validate_params(v)]
        else:
            return [EditProductSupplierQuote.model_validate_params(i) for i in v]


# . Product Codes
class CreateProductCode(Parameter):
    # 编码类型
    code_type: NonEmptyStr
    # 编码列表
    codes: list = Field(alias="commodity_codes")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("codes", mode="before")
    @classmethod
    def _validate_codes(cls, v) -> list[str]:
        return utils.validate_array_of_non_empty_str(v, "UPC编码列表 codes")


# . Product Global Tags
class CreateProductGlobalTag(Parameter):
    """创建产品全局标签参数"""

    # 全局标签名称
    tag_name: NonEmptyStr = Field(alias="label")


# . Product Tags
class MapOfProductAndTags(Parameter):
    """设置产品标签映射参数"""

    # 领星本地产品SKU (Product.lsku)
    lsku: NonEmptyStr = Field(alias="sku")
    # 产品全局标签名称 (ProductGlobalTag.tag_name)
    tags: list = Field(alias="label_list")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("tags", mode="before")
    @classmethod
    def _validate_tags(cls, v) -> list[str]:
        if not v:
            return []
        return utils.validate_array_of_non_empty_str(v, "产品标签列表 tags")


class SetProductTag(Parameter):
    """设置产品全局标签参数"""

    # 设置模式 (1: 追加, 2: 覆盖)
    mode: NonNegativeInt = Field(alias="type")
    # 产品和标签映射列表
    product_tags: list = Field(alias="detail_list")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("product_tags", mode="before")
    @classmethod
    def _validate_product_tags(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            return [MapOfProductAndTags.model_validate_params(v)]
        else:
            return [MapOfProductAndTags.model_validate_params(i) for i in v]


class UnsetProductTag(Parameter):
    """删除产品全局标签参数"""

    # 设置模式 (1: 删除SKU指定的标签, 2: 删除SKU全部的标签)
    mode: NonNegativeInt = Field(alias="type")
    # 产品和标签映射列表
    product_tags: list = Field(alias="detail_list")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("product_tags", mode="before")
    @classmethod
    def _validate_product_tags(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            return [MapOfProductAndTags.model_validate_params(v)]
        else:
            return [MapOfProductAndTags.model_validate_params(i) for i in v]


# . Product Global Attributes
class EditGlobalAttributeValue(Parameter):
    """更新产品全局属性值参数"""

    # 产品属性值
    attr_value: NonEmptyStr
    # 产品属性值ID
    attr_value_id: Optional[NonNegativeInt] = Field(None, alias="pai_id")


class EditProductGlobalAttribute(Parameter):
    """更新产品全局属性参数"""

    # 产品属性ID
    attr_id: Optional[NonNegativeInt] = Field(None, alias="pa_id")
    # 产品属性名称
    attr_name: NonEmptyStr
    # 产品属性值列表
    attr_values: list

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("attr_values", mode="before")
    @classmethod
    def _validate_attr_values(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            v = [v]

        res: list = []
        for i in v:
            if isinstance(i, str):
                i = {"attr_value": i}
            res.append(EditGlobalAttributeValue.model_validate_params(i))
        return res


# . Product Brands
class EditProductBrand(Parameter):
    """更新产品品牌参数"""

    # 领星本地品牌ID
    brand_id: Optional[NonNegativeInt] = Field(None, alias="id")
    # 领星本地品牌名称
    brand_name: NonEmptyStr = Field(alias="title")
    # 领星本地品牌编码
    brand_code: Optional[NonEmptyStr] = None


class EditProductBrands(Parameter):
    """批量更新产品品牌参数"""

    # 领星本地品牌列表
    brands: list = Field(alias="data")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("brands", mode="before")
    @classmethod
    def _validate_brands(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            v = [v]

        res: list = []
        for i in v:
            if isinstance(i, str):
                i = {"title": i}
            res.append(EditProductBrand.model_validate_params(i))
        return res


# . Product Categories
class ProductCategories(PageOffestAndLength):
    """产品分类查询参数"""

    # 领星本地分类ID列表
    category_ids: Optional[list] = Field(None, alias="ids")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("category_ids", mode="before")
    @classmethod
    def _validate_category_ids(cls, v) -> list[int] | None:
        if not v:
            return None
        return utils.validate_array_of_unsigned_int(v, "领星本地分类ID category_ids")


class EditProductCategory(Parameter):
    """更新产品分类参数"""

    # 领星本地产品分类ID
    category_id: Optional[NonNegativeInt] = Field(None, alias="id")
    # 领星本地产品分类名称
    category_name: NonEmptyStr = Field(alias="title")
    # 领星本地产品分类编码
    category_code: str = ""
    # 父分类ID [原字段 'parent_cid']
    parent_category_id: Optional[NonNegativeInt] = Field(None, alias="parent_cid")


class EditProductCategories(Parameter):
    """批量更新产品分类参数"""

    # 领星本地产品分类列表
    categories: list = Field(alias="data")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @field_validator("categories", mode="before")
    @classmethod
    def _validate_categories(cls, v) -> list[dict]:
        if not isinstance(v, (list, tuple)):
            v = [v]

        res: list = []
        for i in v:
            if isinstance(i, str):
                i = {"title": i, "category_code": ""}
            res.append(EditProductCategory.model_validate_params(i))
        return res
