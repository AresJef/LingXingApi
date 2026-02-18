# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field, field_validator
from lingxingapi.base import schema as base_schema
from lingxingapi.base.schema import ResponseV1, ResponseResult, FlattenDataList


# 采购 --------------------------------------------------------------------------------------------------------------------------
# . Supplier
class Supplier(BaseModel):
    """产品供应商"""

    # 供应商ID
    supplier_id: int
    # 供应商名称
    supplier_name: str
    # 供应商编码
    supplier_code: str
    # 供应商是否已删除 (0: 否, 1: 是)
    deleted: int = Field(validation_alias="is_delete")
    # 供应商等级 [原字段 'level_text']
    supplier_level: str = Field(validation_alias="level_text")
    # 供应商员工人数等级 [原字段 'employees']
    # (1: 少于50, 2: 50-150, 3: 150-500, 4: 500-1000, 5: 1000+)
    employees_level: int = Field(validation_alias="employees")
    # 供应商员工人数描述 [原字段 'employees_text']
    employees_desc: str = Field(validation_alias="employees_text")
    # 供应商网址 [原字段 'url']
    website_url: str = Field(validation_alias="url")
    # 供应商联系人姓名
    contact_person: str
    # 供应商联系电话 [原字段 'contact_number']
    phone: str = Field(validation_alias="contact_number")
    # 供应商联系邮箱
    email: str
    # 供应商联系QQ
    qq: str
    # 供应商传真
    fax: str
    # 供应商地址 [原字段 'address_full']
    address: str = Field(validation_alias="address_full")
    # 供应商开户银行 [原字段 'open_bank']
    bank: str = Field(validation_alias="open_bank")
    # 供应商银行账号户名 [原字段 'account_name']
    bank_account_name: str = Field(validation_alias="account_name")
    # 供应商银行账号卡好 [原字段 'bank_account_number']
    bank_account_number: str = Field(validation_alias="bank_card_number")
    # 供应商备注 [原字段 'remark']
    note: str = Field(validation_alias="remark")
    # 采购跟进人员ID列表 [原字段 'purchaser']
    purchase_staff_ids: list[int] = Field(validation_alias="purchaser")
    # 采购合同名称 [原字段 'pc_name']
    purchase_contract: str = Field(validation_alias="pc_name")
    # 采购支付方式 [原字段 'payment_method_text']
    payment_method: str = Field(validation_alias="payment_method_text")
    # 采购结算方式 [原字段 'settlement_method_text']
    settlement_method: str = Field(validation_alias="settlement_method_text")
    # 采购结算描述 [原字段 'settlement_description']
    settlement_desc: str = Field(validation_alias="settlement_description")

    @field_validator("purchase_staff_ids", mode="before")
    @classmethod
    def _validate_purchase_staff_ids(cls, v) -> list[int]:
        """验证采购跟进人员ID列表"""
        if not v:
            return []
        if not isinstance(v, str):
            raise ValueError("采购跟进人员ID purchase_staff_ids 必须是字符串")
        return [int(x) for x in v.split(",")]


class Suppliers(ResponseV1):
    """产品供应商列表"""

    data: list[Supplier]


# . Edit Supplier
class EditSupplier(BaseModel):
    """编辑产品供应商结果"""

    # 编辑结果
    supplier_id: int = Field(validation_alias="erp_supplier_id")


class EditSupplierResult(ResponseResult):
    """编辑产品供应商结果"""

    data: EditSupplier


# . Purchaser
class Purchaser(BaseModel):
    """采购方主体"""

    # 采购方主体ID
    purchaser_id: int
    # 采购方主体名称 [原字段 'name']
    purhcaser_name: str = Field(validation_alias="name")
    # 采购方主体联系人 [原字段 'contacter']
    contact_person: str = Field(validation_alias="contacter")
    # 采购方主体联系电话 [原字段 'contact_phone']
    phone: str = Field(validation_alias="contact_phone")
    # 采购方主体联系邮箱
    email: str
    # 采购方主体地址
    address: str


class Purchasers(ResponseV1, FlattenDataList):
    """采购方主体列表"""

    data: list[Purchaser]


# . Purchase Plan
class PurchasePlanFile(BaseModel):
    """采购计划文件"""

    # 文件名称 [原字段 'name']
    file_name: str = Field(validation_alias="name")
    # 文件链接 [原字段 'url']
    file_url: str = Field(validation_alias="url")


class PurchasePlan(BaseModel):
    """采购计划"""

    # fmt: off
    # 采购计划ID [原字段 'group_id']
    plan_id: int = Field(validation_alias="group_id")
    # 采购计划单号 [原字段 'plan_sn']
    plan_number: str = Field(validation_alias="plan_sn")
    # 采购计划批次号 [原字段 'ppg_sn']
    plan_batch_number: str = Field(validation_alias="ppg_sn")
    # 采购产品领星店铺ID
    sid: int
    # 采购产品的店铺名称
    seller_name: str
    # 采购产品销售国家 [原字段 'marketplace']
    country: str = Field(validation_alias="marketplace")
    # 亚马逊SKU列表 [原字段 'msku']
    mskus: list[str] = Field(validation_alias="msku")
    # 领星本地产品ID [原字段 'product_id']
    lsku_id: int = Field(validation_alias="product_id")
    # 本地产品SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 亚马逊FNSKU
    fnsku: str
    # 多属性产品编码
    spu: str
    # 多属性产品名称
    spu_name: str
    # 本地产品名称
    product_name: str
    # 多属性产品属性列表 [原字段 'attribute']
    attributes: list[base_schema.SpuProductAttribute] = Field(validation_alias="attribute")
    # 是否是捆绑产品 [原字段 'is_combo']
    is_bundled: int = Field(validation_alias="is_combo")
    # 是否是辅料 [原字段 'is_aux']
    is_auxiliary_material: int = Field(validation_alias="is_aux")
    # 产品图片链接 [原字段 'pic_url']
    image_url: str = Field(validation_alias="pic_url")
    # 采购产品备注 [原字段 'remark']
    product_note: str = Field(validation_alias="remark")
    # 采购数量 [原字段 'quantity_plan']
    purchase_qty: int = Field(validation_alias="quantity_plan")
    # 采购箱子数量 [原字段 'cg_box_pcs']
    pruchase_box_qty: int = Field(validation_alias="cg_box_pcs")
    # 供应商ID
    supplier_id: int
    # 供应商名称
    supplier_name: str
    # 仓库ID [原字段 'wid']
    warehouse_id: int = Field(validation_alias="wid")
    # 仓库名称
    warehouse_name: str
    # 采购方主体ID
    purchaser_id: int
    # 采购方主体名称
    purchaser_name: str
    # 期望到货日期 [原字段 'expect_arrive_time']
    expect_arrive_date: str = Field(validation_alias="expect_arrive_time")
    # 采购计划备注 [原字段 'plan_remark']
    purchase_note: str = Field(validation_alias="plan_remark")
    # 采购文件 [原字段 'file']
    purchase_files: list[PurchasePlanFile] = Field(validation_alias="file")
    # 是否已关联加工计划 [原字段 'is_related_process_plan']
    has_process_plan: int = Field(validation_alias="is_related_process_plan")
    # 采购计划状态 (2: 待采购, -2: 已完成, 121: 待审批, 122: 已驳回, -3或124: 已作废)
    status: int
    # 采购计划状态描述 [原字段 'status_text']
    status_desc: str = Field(validation_alias="status_text")
    # 创建人ID [原字段 'creator_uid']
    creator_id: int = Field(validation_alias="creator_uid")
    # 创建人姓名 [原字段 'creator_real_name']
    creator_name: str = Field(validation_alias="creator_real_name")
    # 采购跟进人员ID [原字段 'cg_uid']
    purchase_staff_id: int = Field(validation_alias="cg_uid")
    # 采购跟进人员姓名 [原字段 'cg_opt_username']
    purchase_staff_name: str = Field(validation_alias="cg_opt_username")
    # 采购单负责人ID列表 [原字段 'perm_uid']
    responsible_staff_ids: list[int] = Field(default_factory=list, validation_alias="perm_uid")
    # 审计人员ID列表 [原字段 'audit_uids']
    audit_staff_ids: list[int] = Field(validation_alias="audit_uids")
    # 采购计划创建时间 (北京时间)
    create_time: str 
    # 采购计划更新时间 (北京时间)
    update_time: str
    # fmt: on


class PurchasePlans(ResponseV1):
    """采购计划列表"""

    data: list[PurchasePlan]
