# -*- coding: utf-8 -*-c
import datetime
from lingxingapi import errors
from lingxingapi.base.api import BaseAPI
from lingxingapi.base import param as base_param
from lingxingapi.purchase import param, route, schema


# API ------------------------------------------------------------------------------------------------------------------
class PurchaseAPI(BaseAPI):
    """领星API `采购数据` 接口

    ## Notice
    请勿直接实例化此类
    """

    async def Suppliers(
        self,
        *,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.Suppliers:
        """查询产品供应商

        ## Docs
        - 采购: [查询供应商列表](https://apidoc.lingxing.com/#/docs/Purchase/Supplier)

        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 最大值5000, 默认 `None` (使用: 1000)
        :returns `<'Suppliers'>`: 返回查询到的产品供应商列表
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
                    # 供应商ID
                    "supplier_id": 1,
                    # 供应商名称
                    "supplier_name": "遵*******",
                    # 供应商编码
                    "supplier_code": "SU******",
                    # 供应商是否已删除 (0: 否, 1: 是)
                    "deleted": 0,
                    # 供应商等级 [原字段 'level_text']
                    "supplier_level": "★",
                    # 供应商员工人数等级 [原字段 'employees']
                    # (1: 少于50, 2: 50-150, 3: 150-500, 4: 500-1000, 5: 1000+)
                    "employees_level": 1,
                    # 供应商员工人数描述 [原字段 'employees_text']
                    "employees_desc": "少于50人",
                    # 供应商网址 [原字段 'url']
                    "website_url": "https://www.example.com",
                    # 供应商联系人姓名
                    "contact_person": "",
                    # 供应商联系电话 [原字段 'contact_number']
                    "phone": "",
                    # 供应商联系邮箱
                    "email": "",
                    # 供应商联系QQ
                    "qq": "",
                    # 供应商传真
                    "fax": "",
                    # 供应商地址 [原字段 'address_full']
                    "address": "",
                    # 供应商开户银行 [原字段 'open_bank'
                    "bank": "",
                    # 供应商银行账号户名 [原字段 'account_name']
                    "bank_account_name": "",
                    # 供应商银行账号卡好 [原字段 'bank_account_number']
                    "bank_account_number": "",
                    # 供应商备注 [原字段 'remark']
                    "note": "",
                    # 采购跟进人员ID列表 [原字段 'purchaser']
                    "purchase_staff_ids": [1*****],
                    # 采购合同名称 [原字段 'pc_name']
                    "purchase_contract": "",
                    # 采购支付方式 [原字段 'payment_method_text']
                    "payment_method": "",
                    # 采购结算方式 [原字段 'settlement_method_text']
                    "settlement_method": "月结",
                    # 采购结算描述
                    "settlement_desc": "",

                },
                ...
            ],
        }
        ```
        """
        url = route.SUPPLIERS
        # 解析并验证参数
        args = {"offset": offset, "length": length}
        try:
            p = base_param.PageOffestAndLength.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.Suppliers.model_validate(data)

    async def EditSupplier(
        self,
        supplier_name: str,
        supplier_id: int | None = None,
        *,
        supplier_code: str | None = None,
        supplier_level: int | None = None,
        employees_level: int | None = None,
        website_url: str | None = None,
        contact_person: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        qq: str | None = None,
        fax: str | None = None,
        address: str | None = None,
        bank: str | None = None,
        bank_account_name: str | None = None,
        bank_account_number: str | None = None,
        note: str | None = None,
        purchase_staff_ids: int | list[int] | None = None,
        payment_method: int | None = None,
        settlement_method: int | None = None,
        settlement_desc: str | None = None,
    ) -> schema.EditSupplierResult:
        """添加/修改供应商

        ## Docs
        - 采购: [添加/修改供应商](https://apidoc.lingxing.com/#/docs/Purchase/SupplierEdit)

        ## Notice
        - 默认参数 `None` 有些表示留空或不修改, 有些表示重置设置, 具体请参考参数说明

        :param supplier_name `<'str'>`: 供应商名称,
            若是已存在的供应商, 在传入`supplier_id`的情况下, 可以进行修改
        :param supplier_id `<'int/None'>`: 供应商ID,
            默认 `None`, 如果是新建供应商则不需要传入, 若是编辑供应商信息则必填
        :param supplier_code `<'str/None'>`: 供应商编码,
            默认 `None` (系统自动生成), 不支持后续修改
        :param supplier_level `<'int/None'>`: 供应商等级, 支持 1-5 级,
            默认 `None` 表示默认或重置为空
        :param employees_level `<'int/None'>`: 供应商员工数, 支持 1-5 级,
            默认 `None` 表示默认或重置为空

            - `1`: 少于50人
            - `2`: 50-150人
            - `3`: 150-500人
            - `4`: 500-1000人
            - `5`: 1000+人

        :param website_url `<'str/None'>`: 供应商网址,
            默认 `None` 表示留空或不修改, 传入空字符串清除设置
        :param contact_person `<'str/None'>`: 供应商联系人姓名,
            默认 `None` 表示留空或不修改, 传入空字符串清除设置
        :param phone `<'str/None'>`: 供应商联系电话,
            默认 `None` 表示留空或不修改, 传入空字符串清除设置
        :param email `<'str/None'>`: 供应商联系邮箱,
            默认 `None` 表示留空或不修改, 传入空字符串清除设置
        :param qq `<'str/None'>`: 供应商联系QQ,
            默认 `None` 表示留空或不修改, 传入空字符串清除设置
        :param fax `<'str/None'>`: 供应商传真,
            默认 `None` 表示留空或不修改, 传入空字符串清除设置
        :param address `<'str/None'>`: 供应商地址,
            默认 `None` 表示留空或不修改, 传入空字符串清除设置
        :param bank `<'str/None'>`: 供应商开户银行,
            默认 `None` 表示留空或不修改, 不支持清除设置
        :param bank_account_name `<'str/None'>`: 供应商银行账号户名,
            默认 `None` 表示留空或不修改, 不支持清除设置
        :param bank_account_number `<'str/None'>`: 供应商银行账号卡号,
            默认 `None` 表示留空或不修改, 不支持清除设置
        :param note `<'str/None'>`: 供应商备注,
            默认 `None` 表示留空或不修改, 传入空字符串清除设置
        :param purchase_staff_ids `<'int/list[int]/None'>`: 采购跟进人员ID,
            默认 `None` 表示留空或不修改, 不支持清除设置
        :param payment_method `<'int/None'>`: 采购支付方式,
            默认 `None` 表示默认或重置为空

            - `1`: 网银转账
            - `2`: 网上支付

        :param settlement_method `<'int/None'>`: 采购结算方式,
            默认 `None` 表示默认或重置为 `8: 月结`

            - `7`: 现结
            - `8`: 月结

        :param settlement_desc `<'str/None'>`: 采购结算描述,
            默认 `None` 表示留空或不修改, 传入空字符串清除设置
        :returns `<'EditSupplierResult'>`: 返回编辑供应商结果
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
                # 供应商ID [原字段 'erp_supplier_id']
                "supplier_id": 1*****,
            },
        }
        """
        url = route.EDIT_SUPPLIER
        # 解析并验证参数
        args = {
            "supplier_name": supplier_name,
            "supplier_id": supplier_id,
            "supplier_code": supplier_code,
            "supplier_level": supplier_level,
            "employees_level": employees_level,
            "website_url": website_url,
            "contact_person": contact_person,
            "phone": phone,
            "email": email,
            "qq": qq,
            "fax": fax,
            "address": address,
            "bank": bank,
            "bank_account_name": bank_account_name,
            "bank_account_number": bank_account_number,
            "note": note,
            "purchase_staff_ids": purchase_staff_ids,
            "payment_method": payment_method,
            "settlement_method": 8 if settlement_method is None else settlement_method,
            "settlement_desc": settlement_desc,
        }
        try:
            p = param.EditSupplier.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.EditSupplierResult.model_validate(data)

    async def Purchasers(
        self,
        *,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.Purchasers:
        """查询采购方主体

        ## Docs
        - 采购: [查询采购方列表](https://apidoc.lingxing.com/#/docs/Purchase/Purchaser)

        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 最大值1000, 默认 `None` (使用: 500)
        :returns `<'Purchasers'>`: 返回查询到的采购跟进人员列表
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
                    # 采购方主体ID
                    "purchaser_id": 217,
                    # 采购方主体名称 [原字段 'name']
                    "purhcaser_name": "采购公司",
                    # 采购方主体联系人 [原字段 'contacter']
                    "contact_person": "白小白",
                    # 采购方主体联系电话 [原字段 'contact_phone']
                    "phone": "123456789",
                    # 采购方主体联系邮箱
                    "email": "123456789@qq.com",
                    # 采购方主体地址
                    "address": "中国",
                },
                ...
            ],
        }
        ```
        """
        url = route.PURCHASERS
        # 解析并验证参数
        args = {"offset": offset, "length": length}
        try:
            p = base_param.PageOffestAndLength.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.Purchasers.model_validate(data)

    async def PurchasePlans(
        self,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        date_type: int,
        *,
        plan_ids: str | list[str] | None = None,
        status: int | list[int] | None = None,
        is_bundled: int | None = None,
        is_process_plan_linked: int | None = None,
        sids: int | list[int] | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.PurchasePlans:
        """查询采购计划

        ## Docs
        - 采购: [查询采购计划列表](https://apidoc.lingxing.com/#/docs/Purchase/getPurchasePlans)

        :param start_date `<'str/date/datetime'>`: 查询开始日期, 闭区间, 格式为 "YYYY-MM-DD"
        :param end_date `<'str/date/datetime'>`: 查询结束日期, 闭区间, 格式为 "YYYY-MM-DD"
        :param date_type `<'int'>`: 查询日期类型, 可选值:

            - `1`: 创建时间
            - `2`: 预计到货日期
            - `3`: 更新时间

        :param plan_ids `<'str/list[str]/None'>`: 采购计划单号列表, 默认 `None` (查询所有)
        :param status `<'int/list[int]/None'>`: 采购计划状态列表, 默认 `None` (查询所有)

            - `2`: 待采购
            - `-2`: 已完成
            - `121`: 待审批
            - `122`: 已驳回
            - `-3` 或 `124`: 已作废

        :param is_bundled `<'int/None'>`: 是否为捆绑产品 (0: 否, 1: 是), 默认 `None` (查询所有)
        :param is_process_plan_linked `<'int/None'>`: 是否关联加工计划 (0: 否, 1: 是), 默认 `None` (查询所有)
        :param sids `<'int/list[int]/None'>`: 领星店铺ID列表, 默认 `None` (查询所有)
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 最大值500, 默认 `None` (使用: 500)
        :returns `<'PurchasePlans'>`: 返回查询到的采购计划列表
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
                    # 采购计划ID [原字段 'group_id']
                    "plan_id": 4*****,
                    # 采购计划单号 [原字段 'plan_sn']
                    "plan_number": "PP*********",
                    # 采购计划批次号 [原字段 'ppg_sn']
                    "plan_batch_number": "PPG*********",
                    # 采购产品领星店铺ID
                    "sid": 0,
                    # 采购产品的店铺名称
                    "seller_name": "",
                    # 采购产品销售国家 [原字段 'marketplace']
                    "country": "",
                    # 亚马逊SKU列表 [原字段 'msku']
                    "mskus": [],
                    # 领星本地产品ID [原字段 'product_id']
                    "lsku_id": 2*****,
                    # 本地产品SKU [原字段 'sku']
                    "lsku": "SKU********",
                    # 亚马逊FNSKU
                    "fnsku": "",
                    # 多属性产品编码
                    "spu": "SPU********",
                    # 多属性产品名称
                    "spu_name": "P********",
                    # 本地产品名称
                    "product_name": "P********",
                    # 多属性产品属性列表 [原字段 'attribute']
                    "attributes": [
                        {
                            # 属性ID
                            "attr_id": 1***,
                            # 属性名称
                            "attr_name": "属性名",
                            # 属性值
                            "attr_value": "属性值",
                        }
                    ],
                    # 是否是捆绑产品 [原字段 'is_combo']
                    "is_bundled": 0,
                    # 是否是辅料 [原字段 'is_aux']
                    "is_auxiliary_material": 0,
                    # 产品图片链接 [原字段 'pic_url']
                    "image_url": "",
                    # 采购产品备注 [原字段 'remark']
                    "product_note": "产品备注",
                    # 采购数量 [原字段 'quantity_plan']
                    "purchase_qty": 1,
                    # 采购箱子数量 [原字段 'cg_box_pcs']
                    "pruchase_box_qty": 1,
                    # 供应商ID
                    "supplier_id": 0,
                    # 供应商名称
                    "supplier_name": "",
                    # 仓库ID [原字段 'wid']
                    "warehouse_id": 1***,
                    # 仓库名称
                    "warehouse_name": "默认仓库",
                    # 采购方主体ID
                    "purchaser_id": 1**,
                    # 采购方主体名称
                    "purchaser_name": "采购测试公司",
                    # 期望到货日期 [原字段 'expect_arrive_time']
                    "expect_arrive_date": "2025-08-14",
                    # 采购计划备注 [原字段 'plan_remark']
                    "purchase_note": "",
                    # 采购文件 [原字段 'file']
                    "purchase_files": [],
                    # 是否已关联加工计划 [原字段 'is_related_process_plan']
                    "has_process_plan": 0,
                    # 采购计划状态 (2: 待采购, -2: 已完成, 121: 待审批, 122: 已驳回, -3或124: 已作废)
                    "status": 121,
                    # 采购计划状态描述 [原字段 'status_text']
                    "status_desc": "待审批",
                    # 创建人ID [原字段 'creator_uid']
                    "creator_id": 1*******,
                    # 创建人姓名 [原字段 'creator_real_name']
                    "creator_name": "超级管理员",
                    # 采购跟进人员ID [原字段 'cg_uid']
                    "purchase_staff_id": 1*******,
                    # 采购跟进人员姓名 [原字段 'cg_opt_username']
                    "purchase_staff_name": "超级管理员",
                    # 采购单负责人ID列表 [原字段 'perm_uid']
                    "responsible_staff_ids": [1*******],
                    # 审计人员ID列表 [原字段 'audit_uids']
                    "audit_staff_ids": [1*******],
                    # 采购计划创建时间 (北京时间)
                    "create_time": "2025-08-06 16:34:32",
                    # 采购计划更新时间 (北京时间)
                    "update_time": "2025-08-06 16:49:20",
                },
                ...
            ],
        }
        ```
        """
        url = route.PURCHASE_PLANS
        # 解析并验证参数
        args = {
            "start_date": start_date,
            "end_date": end_date,
            "date_type": date_type,
            "plan_ids": plan_ids,
            "status": status,
            "is_bundled": is_bundled,
            "is_process_plan_linked": is_process_plan_linked,
            "sids": sids,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.PurchasePlans.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.PurchasePlans.model_validate(data)
