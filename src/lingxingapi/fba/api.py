# -*- coding: utf-8 -*-c
import datetime
from typing import Literal
from lingxingapi import errors
from lingxingapi.base.api import BaseAPI
from lingxingapi.fba import param, route, schema

# Type Aliases ---------------------------------------------------------------------------------------------------------
STA_STATUS = Literal["ACTIVE", "VOIDED", "SHIPPED", "ERRORED"]
SHIPMENT_STATUS = Literal[
    "WORKING",
    "READY_TO_SHIP",
    "SHIPPED",
    "RECEIVING",
    "CLOSED",
    "CANCELLED",
    "DELETED",
]
ADDRESS_SEARCH_FIELD = Literal["alias_name", "sender_name"]


# API ------------------------------------------------------------------------------------------------------------------
class FbaAPI(BaseAPI):
    """领星API `FBA数据` 接口

    ## Notice
    请勿直接实例化此类
    """

    # 公共 API --------------------------------------------------------------------------------------
    # . FBA货件(STA)
    async def StaPlans(
        self,
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        date_type: int,
        *,
        plan_name: str | None = None,
        shipment_ids: str | list[str] | None = None,
        statuses: STA_STATUS | list[STA_STATUS] | None = None,
        sids: int | list[int] | None = None,
        page: int = 1,
        length: int = 200,
    ) -> schema.StaPlans:
        """查询STA计划

        ## Docs
        - FBA - FBA货件(STA): [查询STA任务列表](https://apidoc.lingxing.com/#/docs/FBA/QuerySTATaskList)

        :param start_date `<'str/date/datetime'>`: 开始日期 (北京时间), 双闭区间
        :param end_date `<'str/date/datetime'>`: 结束日期 (北京时间), 双闭区间
        :param date_type `<'int'>`: 时期类型 (1: 创建日期; 2: 更新日期)
        :param plan_name `<'str'>`: STA计划名称 (模糊搜索), 默认 `None` (不搜索)
        :param shipment_ids `<'str/list[str]'>`: 货件ID或货件单号列表 (精确搜索), 默认 `None` (不搜索)
        :param statuses `<'str/list[str]'>`: STA计划状态列表, 默认 `None` (不筛选),
            可选值: 'ACTIVE', 'VOIDED', 'SHIPPED', 'ERRORED'
        :param sids `<'int/list[int]'>`: 领星店铺ID列表, 默认 `None` (不筛选)
        :param page `<'int'>`: 分页页码, 默认 `1`
        :param length `<'int'>`: 分页大小, 最大值200, 默认 `200`
        :returns `<'StaPlans'>`: 返回查询STA计划的结果
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
                    # STA计划ID [原字段 'inboundPlanId']
                    "inbound_plan_id": "wf1a0e57bc-****-****-****-************",
                    # STA计划名称 [原字段 'planName']
                    "plan_name": "",
                    # 计划状态
                    "status": "ACTIVE",
                    # 分仓类型 (1: 先装箱再分仓, 2: 先分仓再装箱)
                    "position_type": "2",
                    # 创建时间 [原字段 'gmtCreate']
                    "create_time": "2025-08-13 13:58",
                    # 计划创建时间 [原字段 'planCreateTime']
                    "plan_create_time": "2025-08-13 13:58",
                    # 更新时间 [原字段 'gmtModified']
                    "update_time": "2025-08-13 16:46",
                    # 计划更新时间 [原字段 'planUpdateTime']
                    "plan_update_time": "2025-08-13 14:04",
                    # 货件列表 [原字段 'shipmentList']
                    "shipments": [
                        {
                            # 货件列表 [原字段 'shipmentList']
                            "shipment_id": "she2e425f4-****-****-****-************",
                            # 货件确认ID
                            "shipment_confirmation_id": "FBA15*******",
                            # 货件状态
                            "shipment_status": "",
                            # 取件ID
                            "pick_up_id": "",
                            # 运单号
                            "freight_bill_number": "",
                        },
                        ...
                    ],
                    # 计划商品列表 [原字段 'inboundPlanItemList']
                    "items": [
                        {
                            # 亚马逊ASIN
                            "asin": "B0D*******",
                            # 父ASIN [原字段 'parent_asin']
                            "parent_asin": "B0D*******",
                            # 亚马逊SKU
                            "msku": "SKU********",
                            # 领星本地SKU [原字段 'sku']
                            "lsku": "LOCAL********",
                            # 亚马逊FNSKU
                            "fnsku": "X00*******",
                            # 领星本地商品名称 [原字段 'productName']
                            "product_name": "P********",
                            # 商品标题
                            "title": "Product Title",
                            # 商品略缩图
                            "thumbnail_url": "https://m.media-amazon.com/****.jpg",
                            # 预处理方 [原字段 'prepOwner']
                            "prep_owner": "SELLER",
                            # 标签处理方 [原字段 'labelOwner']
                            "label_owner": "SELLER",
                            # 有效日期 [原字段 'expiration']
                            "expiration_date": "",
                            # 货件申报数量 [原字段 'quantity']
                            "item_qty": 500,
                        },
                        ...
                    ],
                },
            ],
        }
        ```
        """
        url = route.STA_PLANS
        # 解析并验证参数
        args = {
            "start_date": start_date,
            "end_date": end_date,
            "date_type": date_type,
            "plan_name": plan_name,
            "shipment_ids": shipment_ids,
            "statuses": statuses,
            "sids": sids,
            "page": page,
            "length": length,
        }
        try:
            p = param.StaPlans.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.StaPlans.model_validate(data)

    async def StaPlanDetail(
        self,
        sid: int,
        inbound_plan_id: str,
    ) -> schema.StaPlanDetailData:
        """查询STA计划详情

        ## Docs
        - FBA - FBA货件(STA): [查询STA任务详情](https://apidoc.lingxing.com/#/docs/FBA/StaTaskDetail)

        :param sid `<'int'>`: 领星店铺ID
        :param inbound_plan_id `<'str'>`: STA计划ID, 参数来源: `StaPlan.inbound_plan_id`
        :returns `<'StaPlanDetailData'>`: 返回查询STA计划详情的结果
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
                # STA计划ID [原字段 'inboundPlanId']
                "inbound_plan_id": "wf7b4fc853-****-****-****-************",
                # 计划名称 [原字段 'planName']
                "plan_name": "",
                # 计划状态
                "status": "ACTIVE",
                # 分仓类型 (1: 先装箱再分仓, 2: 先分仓再装箱)
                "position_type": "2",
                # 创建时间 [原字段 'gmtCreate']
                "create_time": "2025-08-13 09:58",
                # 计划创建时间 [原字段 'planCreateTime']
                "plan_create_time": "2025-08-13 09:15",
                # 更新时间 [原字段 'gmtModified']
                "update_time": "2025-08-13 12:45",
                # 计划更新时间 [原字段 'planUpdateTime']
                "plan_update_time": "2025-08-13 09:18",
                # 货件列表 [原字段 'shipmentList']
                "shipments": [
                    {
                        # 货件列表 [原字段 'shipmentList']
                        "shipment_id": "she2e425f4-****-****-****-************",
                        # 货件确认ID
                        "shipment_confirmation_id": "FBA15*******",
                        # 货件状态
                        "shipment_status": "READY_TO_SHIP",
                        # 取件ID
                        "pick_up_id": "",
                        # 运单号
                        "freight_bill_number": "",
                    },
                    ...
                ],
                # 发货地址 [原字段 'addressVO']
                "shipment_address": {
                    # 国家代码 [原字段 'countryCode']
                    "country_code": "CN",
                    # 国家名称 [原字段 'countryName']
                    "country": "CN",
                    # 州或省 [原字段 'stateOrProvinceCode']
                    "state": "Guangdong",
                    # 城市
                    "city": "Shenzhen",
                    # 发货地址行1 [原字段 'addressLine1']
                    "address_line1": "Address",
                    # 发货地址行2 [原字段 'addressLine2']
                    "address_line2": "",
                    # 邮政编码 [原字段 'postalCode']
                    "postcode": "518000",
                    # 发货人姓名 [原字段 'shipperName']
                    "shipper_name": "白小白",
                    # 电子邮件 [原字段 'email']
                    "email": "baixiaobai@qq.com",
                    # 电话号码 [原字段 'phoneNumber']
                    "phone": "18*********",
                },
                # 计划商品列表 [原字段 'productList']
                "items": [
                    {
                        # 亚马逊ASIN
                        "asin": "B0D*******",
                        # 父ASIN [原字段 'parent_asin']
                        "parent_asin": "B0D*******",
                        # 亚马逊SKU
                        "msku": "SKU********",
                        # 领星本地SKU [原字段 'sku']
                        "lsku": "LOCAL********",
                        # 亚马逊FNSKU
                        "fnsku": "X00*******",
                        # 领星本地商品名称 [原字段 'productName']
                        "product_name": "P********",
                        # 商品标题
                        "title": "Product Title",
                        # 商品略缩图
                        "thumbnail_url": "https://m.media-amazon.com/****.jpg",
                        # 预处理方 [原字段 'prepOwner']
                        "prep_owner": "SELLER",
                        # 标签处理方 [原字段 'labelOwner']
                        "label_owner": "SELLER",
                        # 有效日期 [原字段 'expiration']
                        "expiration_date": "",
                        # 货件申报数量 [原字段 'quantity']
                        "item_qty": 500,
                    },
                    ...
                ],
            },
        }
        ```
        """
        url = route.STA_PLAN_DETAIL
        # 解析并验证参数
        args = {
            "sid": sid,
            "inbound_plan_id": inbound_plan_id,
        }
        try:
            p = param.StaID.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.StaPlanDetailData.model_validate(data)

    async def PackingGroups(
        self,
        sid: int,
        inbound_plan_id: str,
    ) -> schema.PackingGroups:
        """查询STA包装组

        ## Docs
        - FBA - FBA货件(STA): [查询包装组](https://apidoc.lingxing.com/#/docs/FBA/ListPackingGroupItems)

        :param sid `<'int'>`: 领星店铺ID
        :param inbound_plan_id `<'str'>`: STA计划ID, 参数来源: `StaPlan.inbound_plan_id`
        :returns `<'PackingGroups'>`: 返回查询包装组的结果
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
                    # 包装组ID [原字段 'packingGroupId']
                    "packing_group_id": "pg7847440c-****-****-****-************",
                    # 包装组商品列表 [原字段 'packingGroupItemList']
                    "items": [
                        {
                            # 亚马逊ASIN
                            "asin": "B0D*******",
                            # 父ASIN [原字段 'parent_asin']
                            "parent_asin": "B0D*******",
                            # 亚马逊SKU
                            "msku": "SKU********",
                            # 领星本地SKU [原字段 'sku']
                            "lsku": "LOCAL********",
                            # 亚马逊FNSKU
                            "fnsku": "X00*******",
                            # 领星本地商品名称 [原字段 'productName']
                            "product_name": "P********",
                            # 商品标题
                            "title": "Product Title",
                            # 商品略缩图
                            "thumbnail_url": "https://m.media-amazon.com/****.jpg",
                            # 预处理方 [原字段 'prepOwner']
                            "prep_owner": "SELLER",
                            # 标签处理方 [原字段 'labelOwner']
                            "label_owner": "SELLER",
                            # 有效日期 [原字段 'expiration']
                            "expiration_date": "",
                            # 货件申报数量 [原字段 'quantity']
                            "item_qty": 500,
                        },
                        ...
                    ],
                },
                ...
            ],
        }
        ```
        """
        url = route.PACKING_GROUPS
        # 解析并验证参数
        args = {
            "sid": sid,
            "inbound_plan_id": inbound_plan_id,
        }
        try:
            p = param.StaID.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.PackingGroups.model_validate(data)

    async def PackingGroupBoxes(
        self,
        sid: int,
        inbound_plan_id: str,
        packing_group_ids: str | list[str],
    ) -> schema.PackingGroupBoxes:
        """查询STA包装组装箱信息

        ## Docs
        - FBA - FBA货件(STA): [查询STA任务包装组装箱信息](https://apidoc.lingxing.com/#/docs/FBA/QuerySTATaskBoxInformation

        :param sid `<'int'>`: 领星店铺ID
        :param inbound_plan_id `<'str'>`: STA计划ID, 参数来源: `StaPlan.inbound_plan_id`
        :param packing_group_ids `<'str/list[str]'>`: 包装组ID列表, 参数来源: `PackingGroup.packing_group_id`
        :returns `<'PackingGroupBoxes'>`: 返回查询包装组装箱信息的结果
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
                    # 包装组ID [原字段 'packingGroupId']
                    "packing_group_id": "pg2ec98be6-****-****-****-************",
                    # 装箱列表 [原字段 'shipmentPackingList']
                    "boxes": [
                        {
                            # 包裹ID [原字段 'packageId']
                            "package_id": "pkb1170e07-****-****-****-************",
                            # 箱子顺序号 [原字段 'localBoxId']
                            "box_seq": 1,
                            # 亚马逊箱子ID [原字段 'boxId']
                            "box_id": "",
                            # 箱子名称 [原字段 'boxName']
                            "box_name": "P1 - B1",
                            # 箱内商品总数量 [原字段 'total']
                            "box_item_qty": 85,
                            # 箱子重量
                            "weight": 10.2,
                            # 重量单位 [原字段 'weightUnit']
                            "weight_unit": "KG",
                            # 箱子长度
                            "length": 635.0,
                            # 箱子宽度
                            "width": 20.3,
                            # 箱子高度
                            "height": 45.7,
                            # 箱子尺寸单位 [原字段 'lengthUnit']
                            "dimension_unit": "CM",
                            # 箱内商品列表 [原字段 'productList']
                            "items": [
                                {
                                    # 亚马逊ASIN
                                    "asin": "B0D*******",
                                    # 父ASIN [原字段 'parent_asin']
                                    "parent_asin": "B0D*******",
                                    # 亚马逊SKU
                                    "msku": "SKU********",
                                    # 领星本地SKU [原字段 'sku']
                                    "lsku": "LOCAL********",
                                    # 亚马逊FNSKU
                                    "fnsku": "X00*******",
                                    # 领星本地商品名称 [原字段 'productName']
                                    "product_name": "P********",
                                    # 商品标题
                                    "title": "Product Title",
                                    # 商品略缩图
                                    "thumbnail_url": "https://m.media-amazon.com/****.jpg",
                                    # 预处理方 [原字段 'prepOwner']
                                    "prep_owner": "SELLER",
                                    # 标签处理方 [原字段 'labelOwner']
                                    "label_owner": "SELLER",
                                    # 有效日期 [原字段 'expiration']
                                    "expiration_date": "",
                                    # 箱内商品总数量 [原字段 'quantityInBox']
                                    "item_qty": 85,
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
        url = route.PACKING_GROUP_BOXES
        # 解析并验证参数
        args = {
            "sid": sid,
            "inbound_plan_id": inbound_plan_id,
            "packing_group_ids": packing_group_ids,
        }
        try:
            p = param.PackingGroupBoxes.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.PackingGroupBoxes.model_validate(data)

    async def PlacementOptions(
        self,
        sid: int,
        inbound_plan_id: str,
    ) -> schema.PlacementOptions:
        """查询货件分仓方案

        ## Docs
        - FBA - FBA货件(STA): [查询货件方案](https://apidoc.lingxing.com/#/docs/FBA/ShipmentPreView)

        :param sid `<'int'>`: 领星店铺ID
        :param inbound_plan_id `<'str'>`: STA计划ID, 参数来源: `StaPlan.inbound_plan_id`
        :returns `<'PlacementOptions'>`: 返回查询货件分仓方案的结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "操作成功",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "f9e5e291e14c4180a3cf1405b4d24b99.191.17554878107185127",
            # 响应时间
            "response_time": "2025-08-18T11:30:10.826",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 货件分仓方案ID [原字段 'placementOptionId']
                    "placement_option_id": "plda18cf79-****-****-****-************",
                    # 货件分仓状态 [原字段 'placementStatus']
                    "placement_status": "ACCEPTED",
                    # 货件分仓过期时间 [原字段 'expiration']
                    "expiration": {
                        # 年份值
                        "year": 2025,
                        # 月份值 [原字段 'monthValue']
                        "month": 8,
                        # 天数值 [原字段 'dayOfMonth']
                        "day": 18,
                        # 小时值
                        "hour": 2,
                        # 分钟值
                        "minute": 48,
                        # 秒值
                        "second": 58,
                        # 纳秒值
                        "nano": 4000000,
                        # 年内日序 [原字段 'dayOfYear']
                        "day_of_year": 230,
                        # 月份名称 [原字段 'month']
                        "month_name": "AUGUST",
                        # 星期名称 [原字段 'dayOfWeek']
                        "weekday_name": "MONDAY",
                        # 时区偏移 [原字段 'offset']
                        "offset": {
                            # 时区ID [原字段 'id']
                            "timezone_id": "Z",
                            # 时区偏移秒数 [原字段 'totalSeconds']
                            "seconds": 0,
                            # 时区规则
                            "rules": {
                                # 时区过渡
                                "transitions": [],
                                # 时区过渡规则 [原字段 'transitionRules']
                                "transition_rules": [],
                                # 时区是否固定偏移 [原字段 'fixedOffset']
                                "fixed_offset": True,
                            },
                        },
                    },
                    # 总费用 [原字段 'feeCount']
                    "fee_amt": 35.12,
                    # 费用列表 [原字段 'fees']
                    "fees": [
                        {
                            # 费用项目 [原字段 'target']
                            # (如: Placement Services, Fulfillment Fee Discount)
                            "charge": "Placement Services",
                            # 费用类型 (如: FEE, DISCOUNT)
                            "type": "FEE",
                            # 费用金额 [原字段 'amount']
                            "fee_amt": 37.62,
                            # 费用币种代码 [原字段 'code']
                            "currency_code": "USD",
                        },
                        ...
                    ],
                    # 货件列表 [原字段 'shipmentInformationList']
                    "shipments": [
                        {
                            # 货件ID [原字段 'shipmentId']
                            "shipment_id": "sh1483a535-****-****-****-************",
                            # 货件名称 [原字段 'shipmentName']
                            "shipment_name": "GP-LBE1",
                            # 亚马逊配送中心编码 [原字段 'wareHouseId']
                            "fulfillment_center_id": "LBE1",
                            # 入库区域 (中文) [原字段 'postalCodeMark']
                            "inbound_region": "东部",
                            # 收货地址 [原字段 'address']
                            "ship_to_address": {
                                # 国家代码 [原字段: 'countryCode']
                                "country_code": "US",
                                # 州或省代码 [原字段 'stateOrProvinceCode']
                                "state": "PA",
                                # 城市
                                "city": "NEW STANTON",
                                # 地址行1 [原字段 'addressLine1']
                                "address_line1": "165 GLENN FOX RD",
                                # 地址行2 [原字段 'addressLine2']
                                "address_line2": "",
                                # 地址名称 [原字段 'addressName']
                                "address_name": "LBE1",
                                # 邮政编码 [原字段 'postalCode']
                                "postcode": "15672-9703",
                                # 公司名称 [原字段 'companyName']
                                "company_name": "",
                                # 电子邮箱
                                "email": "",
                                # 电话号码 [原字段 'phoneNumber']
                                "phone": "",
                            },
                            # 不同货件商品数 [原字段 'itemCount']
                            "item_count": 2,
                            '# 货件商品申报总数量 [原字段 'quantity']'
                            "items_qty": 209,
                            # 货件商品列表 [原字段 'itemList']
                            "items": [
                                {
                                    # 亚马逊ASIN
                                    "asin": "B0F*******",
                                    # 父ASIN [原字段 'parent_asin']
                                    "parent_asin": "B0F*******",
                                    # 亚马逊SKU
                                    "msku": "SKU********",
                                    # 领星本地SKU [原字段 'sku']
                                    "lsku": "",
                                    # 亚马逊FNSKU
                                    "fnsku": "X00*******",
                                    # 领星本地商品名称 [原字段 'productName']
                                    "product_name": "",
                                    # 商品标题
                                    "title": "Product Title",
                                    # 商品略缩图
                                    "thumbnail_url": "https://m.media-amazon.com/****.jpg",
                                    # 货件申报数量 [原字段 'quantity']
                                    "item_qty": 149,
                                },
                                ...
                            ],
                        }
                    ],
                }
            ],
        }
        ```
        """
        url = route.PLACEMENT_OPTIONS
        # 解析并验证参数
        args = {
            "sid": sid,
            "inbound_plan_id": inbound_plan_id,
        }
        try:
            p = param.StaID.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.PlacementOptions.model_validate(data)

    async def PlacementOptionBoxes(
        self,
        sid: int,
        inbound_plan_id: str,
    ) -> schema.PlacementOptionBoxes:
        """查询货件分仓方案装箱信息

        ## Docs
        - FBA - FBA货件(STA): [查询货件方案的装箱信息](https://apidoc.lingxing.com/#/docs/FBA/getInboundPackingBoxInfo)

        :param sid `<'int'>`: 领星店铺ID
        :param inbound_plan_id `<'str'>`: STA计划ID, 参数来源: `StaPlan.inbound_plan_id`
        :returns `<'PlacementOptionBoxes'>`: 返回查询货件分仓方案装箱信息的结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "操作成功",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "f9e5e291e14c4180a3cf1405b4d24b99.191.17554878107185127",
            # 响应时间
            "response_time": "2025-08-18T11:30:10.826",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 货件分仓方案ID [原字段 'placementOptionId']
                    "placement_option_id": "plda18cf79-****-****-****-************",
                    # 货件分仓状态 [原字段 'placementStatus']
                    "placement_status": "ACCEPTED",
                    # 货件装箱列表 [原字段 'shipmentInformationList']
                    "shipments": [
                        {
                            # 货件ID [原字段 'shipmentId']
                            "shipment_id": "sh1483a535-****-****-****-************",
                            # 货件重量
                            "weight": 118.0,
                            # 货件重量单位 [原字段 'weightUnit']
                            "weight_unit": "LB",
                            # 货件体积
                            "volume": 6.7,
                            # 货件体积单位 [原字段 'volumeUnit']
                            "volume_unit": "FT³",
                            # 装箱列表 [原字段 'shipmentPackingList']
                            "boxes": [
                                {
                                    # 箱子名称 [原字段 'boxName']
                                    "box_name": "P1 - B2",
                                    # 箱子重量
                                    "weight": 22.0,
                                    # 重量单位 [原字段 'weightUnit']
                                    "weight_unit": "LB",
                                    # 箱子长度
                                    "length": 12.0,
                                    # 箱子宽度
                                    "width": 10.0,
                                    # 箱子高度
                                    "height": 16.0,
                                    # 箱子尺寸单位 [原字段 'lengthUnit']
                                    "dimension_unit": "IN",
                                    # 箱子总数量 [原字段 'total']
                                    "box_qty": 1,
                                    # 箱内商品列表 [原字段 'productList']
                                    "items": [
                                        {
                                           # 亚马逊ASIN
                                            "asin": "B0F*******",
                                            # 父ASIN [原字段 'parent_asin']
                                            "parent_asin": "B0F*******",
                                            # 亚马逊SKU
                                            "msku": "SKU********",
                                            # 领星本地SKU [原字段 'sku']
                                            "lsku": "",
                                            # 亚马逊FNSKU
                                            "fnsku": "X00*******",
                                            # 领星本地商品名称 [原字段 'productName']
                                            "product_name": "",
                                            # 商品标题
                                            "title": "Product Title",
                                            # 商品略缩图
                                            "thumbnail_url": "https://m.media-amazon.com/****.jpg",
                                            # 箱内商品总数量 [原字段 'quantityInBox']
                                            "item_qty": 37,
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
        url = route.PLACEMENT_OPTION_BOXES
        # 解析并验证参数
        args = {
            "sid": sid,
            "inbound_plan_id": inbound_plan_id,
        }
        try:
            p = param.StaID.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.PlacementOptionBoxes.model_validate(data)

    async def Shipments(
        self,
        sids: int | list[int],
        start_date: str | datetime.date | datetime.datetime,
        end_date: str | datetime.date | datetime.datetime,
        *,
        sub_start_date: str | datetime.date | datetime.datetime | None = None,
        sub_end_date: str | datetime.date | datetime.datetime | None = None,
        sub_date_type: int | None = None,
        shipment_ids: str | list[str] | None = None,
        shipment_statuses: SHIPMENT_STATUS | list[SHIPMENT_STATUS] | None = None,
        length: int | None = None,
        offset: int | None = None,
    ) -> schema.Shipments:
        """查询STA货件

        ## Docs
        - FBA - FBA货件(STA): [查询货件列表](https://apidoc.lingxing.com/#/docs/FBA/FBAShipmentList)

        :param sids `<'int/list[int]'>`: 领星店铺ID或ID列表
        :param start_date `<'str/date/datetime'>`: 货件创建开始日期, 左闭右开
        :param end_date `<'str/date/datetime'>`: 货件创建结束日期, 左闭右开
        :param sub_start_date `<'str/date/datetime'>`: 子筛选开始日期, 左闭右开, 默认 `None` (不筛选)
        :param sub_end_date `<'str/date/datetime'>`: 子筛选结束日期, 左闭右开, 默认 `None` (不筛选)
        :param sub_date_type `<'int'>`: 子筛选日期类型 (1: 货件修改日期), 默认 `None` (不筛选)
        :param shipment_ids `<'str/list[str]'>`: 货件ID或ID列表, 默认 `None` (不筛选)
        :param shipment_statuses `<'str/list[str]'>`: 货件状态列表, 默认 `None` (不筛选), 可选值:

            - `'WORKING'`: 卖家已创建货件，但尚未发货
            - `'READY_TO_SHIP'`: 卖家完成货件穿件, 可以发货
            - `'SHIPPED'`: 承运人已取件
            - `'RECEIVING'`: 货件已到达亚马逊配送中心，但有部分商品尚未标记为已收到
            - `'CLOSED'`: 货件已到达亚马逊配送中心，且所有商品已标记为已收到
            - `'CANCELLED'`: 卖家在将货件发送至亚马逊配送中心后取消了货件
            - `'DELETED'`: 卖家在将货件发送至亚马逊配送中心前取消了货件

        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 默认 `None` (使用: 1000)
        :returns `<'Shipments'>`: 返回查询FBA货件数据
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
            "data": "data": [
                {
                    # 唯一键 (货件记录ID)
                    "id": 4*****,
                    # 领星店铺ID
                    "sid": 1,
                    # 领星店铺名称 [原字段 'seller']
                    "seller_name": "US-Store",
                    # FBA货件ID
                    "shipment_id": "FBA*********",
                    # FBA货件名称
                    "shipment_name": "SMF3",
                    # 货件状态
                    # 'WORKING': 卖家已创建货件，但尚未发货
                    # 'READY_TO_SHIP': 卖家完成货件穿件, 可以发货
                    # 'SHIPPED': 承运人已取件
                    # 'IN_TRANSIT': 承运人已通知亚马逊配送中心，知晓货件的存在
                    # 'DELIVERED': 承运人已将货件配送至亚马逊配送中心
                    # 'CHECK_IN': 货件已在亚马逊配送中心
                    # 'RECEIVING': 货件已到达亚马逊配送中心，但有部分商品尚未标记为已收到
                    # 'CLOSED': 货件已到达亚马逊配送中心，且所有商品已标记为已收到
                    # 'CANCELLED': 卖家在将货件发送至亚马逊配送中心后取消了货件
                    # 'DELETED': 卖家在将货件发送至亚马逊配送中心前取消了货件
                    # 'ERROR': 货件出错，但其并非亚马逊处理
                    "shipment_status": "READY_TO_SHIP",
                    # 货件事否已完成 [原字段 'is_closed']
                    # 有绑定, 按签发差异判断: 1. 发货量>签收量='进行中'; 2. 发货量<=签收量='已完成'
                    # 无绑定, 用货件状态判断: DELETED, CANCELED, CLOSED为已完成, 其他为进行中
                    # 额外情况: 当货件状态进入CLOSED, CANCELLED, DELETED 之后90天, 自动变为'已完成'
                    "shipment_closed": 0,
                    # 承运方式名称 [原字段 'alpha_name']
                    "transport_name": "Other",
                    # 承运方式编码 [原字段 'alpha_code']
                    "transport_code": "",
                    # 运输类型
                    "shipping_mode": "GROUND_SMALL_PARCEL",
                    # 运输解决方案
                    "shipping_solution": "USE_YOUR_OWN_CARRIER",
                    # 是否同步亚马逊后台 [原字段 'is_synchronous']
                    "is_synchronized": 1,
                    # 是否上传包装箱信息 [原字段 'is_uploaded_box']
                    "is_box_info_uploaded": 1,
                    # 货件创建人ID [原字段 'uid']
                    "creator_id": 0,
                    # 货件创建人名称 [原字段 'username']
                    "creator_name": "",
                    # 货件数据创建时间 [原字段 'gmt_create']
                    "create_time": "2025-08-14 13:04",
                    # 货件数据更新时间 [原字段 'gmt_modified']
                    "update_time": "2025-08-15 12:59",
                    # 货件数据同步时间
                    "sync_time": "2025-08-14 14:07",
                    # 货件创建时间
                    "working_time": "2025-08-14 13:04",
                    # 承运人已取件时间
                    "shipped_time": "",
                    # 货件到达亚马逊配送中心后, 开始接收时间
                    "receiving_time": "",
                    # 货件到达亚马逊配送中心后, 完成接收时间
                    "closed_time": "",
                    # 是否为STA货件 (0: 否, 1: 是)
                    "is_sta": 1,
                    # STA计划名称
                    "sta_plan_name": "",
                    # STA计划ID
                    "sta_inbound_plan_id": "wfea99b20e-****-****-****-************",
                    # STA货件ID
                    "sta_shipment_id": "shc0ba9022-****-****-****-************",
                    # STA发货日期 [原字段 'sta_shipment_date']
                    "sta_shipping_date": "2025-08-18",
                    # STA送达开始时间
                    "sta_delivery_start_date": "2025-08-18",
                    # STA送达结束时间
                    "sta_delivery_end_date": "2025-08-31",
                    # 提货单号 (BOL)
                    "bill_of_lading_number": "",
                    # 跟踪编号 (PRO) [原字段 'freight_bill_number']
                    "freight_pro_number": "",
                    # 亚马逊关联编码 [原字段 'reference_id']
                    "amazon_reference_id": "3FB*****",
                    # 亚马逊配送中心编码 [原字段 'destination_fulfillment_center_id']
                    "fulfillment_center_id": "SMF3",
                    # 发货地址
                    "ship_from_address": {
                        # 国家代码
                        "country_code": "CN",
                        # 州或省 [原字段 'state_or_province_code']
                        "state": "Guangdong",
                        # 城市
                        "city": "Shenzhen",
                        # 地址区域 [原字段 'region']
                        "district": "Huaqiang North",
                        # 地址行1
                        "address_line1": "Fuyong",
                        # 地址行2
                        "address_line2": "",
                        # 地址名称 [原字段 'name']
                        "address_name": "JBL",
                        # 邮政编码 [原字段 'postal_code']
                        "postcode": "518000",
                        # 门牌号 [原字段 'doorplate']
                        "door_plate": "",
                        # 电话号码
                        "phone": "",
                    },
                    # 收货地址
                    "ship_to_address": {
                        # 国家代码
                        "country_code": "US",
                        # 州或省代码 [原字段 'state_or_province_code']
                        "state": "CA",
                        # 城市
                        "city": "Stockton",
                        # 地址区域 [原字段 'region']
                        "address_region": "",
                        # 地址行1
                        "address_line1": "3923 S B ST",
                        # 地址行2
                        "address_line2": "",
                        # 地址名称 [原字段 'name']
                        "address_name": "JBL",
                        # 邮政编码 [原字段 'postal_code']
                        "postcode": "95206-8202",
                        # 门牌号 [原字段 'doorplate']
                        "door_plate": "",
                        # 电话号码
                        "phone": "",
                    },
                    # 追踪号码列表 [原字段 'tracking_number_list']
                    "tracking_numbers": [
                        {
                            # 包裹ID
                            "box_id": "FBA19**************",
                            # 追踪号码
                            "tracking_number": ""
                        },
                        ...
                    ],
                    # 货件商品列表 [原字段 'item_list']
                    "items": [
                        {
                            # 唯一键
                            "id": 2******,
                            # 亚马逊SKU
                            "msku": "SKU********",
                            # 领星本地SKU [原字段 'sku']
                            "lsku": "LOCAL********",
                            # 亚马逊FNSKU
                            "fnsku": "X00*******",
                            # 预处理说明
                            "prep_instruction": "Labeling",
                            # 预处理方
                            "prep_owner": "SELLER",
                            # 预处理明细
                            "prep_details": "",
                            # 标签处理方 [原字段 'prep_labelowner']
                            "label_owner": "SELLER",
                            # 有效日期 [原字段 'expiration']
                            "expiration_date": "",
                            # 生产日期
                            "release_date": "",
                            # 初始货件申报数量 [原字段 'init_quantity_shipped']
                            "init_item_qty": 100,
                            # 当前货件申报数量 [原字段 'quantity_shipped']
                            "curr_item_qty": 100,
                            # 箱内商品数量 [原字段 'quantity_in_case']
                            "box_item_qty": 0,
                            # 已发货数量 [原字段 'quantity_shipped_local']
                            "shipped_qty": 0,
                            # 亚马逊配送中心已接收的商品数量 [原字段 'quantity_received']
                            "received_qty": 0,
                            # 库存明细ID [原字段 'ware_house_storage_id']
                            "warehouse_storage_id": 0,
                            # 发货计划单号列表 [原字段 'shipment_plan_list']
                            "shipment_plan_numbers": [],
                        },
                        ...
                    ],
                },
                ...
            ],
        }
        ```
        """
        url = route.SHIPMENTS
        # 解析并验证参数
        args = {
            "sids": sids,
            "start_date": start_date,
            "end_date": end_date,
            "sub_start_date": sub_start_date,
            "sub_end_date": sub_end_date,
            "sub_date_type": sub_date_type,
            "shipment_ids": shipment_ids,
            "shipment_statuses": shipment_statuses,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.Shipments.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.Shipments.model_validate(data)

    async def ShipmentDetails(
        self,
        sid: int,
        inbound_plan_id: str,
        shipment_ids: str | list[str],
    ) -> schema.ShipmentDetails:
        """查询STA货件详情

        ## Docs
        - FBA - FBA货件(STA): [查询货件详情](https://apidoc.lingxing.com/#/docs/FBA/ShipmentDetailList)

        :param sid `<'int'>`: 领星店铺ID
        :param inbound_plan_id `<'str'>`: STA计划ID, 参数来源: `Shipment.sta_inbound_plan_id`
        :param shipment_ids `<'str/list[str]'>`: 货件ID或ID列表, 参数来源: `Shipment.sta_shipment_id`
        :returns `<'ShipmentDetails'>`: 返回查询STA货件详情的结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "操作成功",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "f9e5e291e14c4180a3cf1405b4d24b99.191.17554878107185127",
            # 响应时间
            "response_time": "2025-08-18T11:30:10.826",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 领星店铺ID
                    "sid": 1,
                    # 货件ID [原字段 'shipmentId']
                    "shipment_id": "sh5d4c8859-****-****-****-************",
                    # 货件名称 [原字段 'shipmentName']
                    "shipment_name": "产品-2箱-CLT2",
                    # 货件确认ID [原字段 'shipmentConfirmationId']
                    "shipment_confirmation_id": "FBA1********",
                    # 货件状态 [原字段 'status']
                    "shipment_status": "READY_TO_SHIP",
                    # 承运方式编码 [原字段 'alphaCode']
                    "transport_code": "",
                    # 运输类型 [原字段 'shippingMode']
                    "shipping_mode": "GROUND_SMALL_PARCEL",
                    # 运输解决方案 [原字段 'shippingSolution']
                    "shipping_solution": "USE_YOUR_OWN_CARRIER",
                    # STA发货日期 [原字段 'shipingTime']
                    "shipping_date": "2025-08-18",
                    # STA送达开始时间 [原字段 'startDate']
                    "delivery_start_date": "2025-08-18",
                    # STA送达结束时间 [原字段 'endDate']
                    "delivery_end_date": "2025-08-31",
                    # 提货单号 (BOL) [原字段 'pickUpId']
                    "bill_of_lading_number": "",
                    # 亚马逊关联编码 [原字段 'amazonReferenceId']
                    "amazon_reference_id": "31A*****",
                    # 亚马逊配送中心编码 [原字段 'warehouseId']
                    "fulfillment_center_id": "CLT2",
                    # 入库区域 (中文) [原字段 'inboundRegion']
                    "inbound_region": "东部",
                    # 发货地址 [原字段 'shippingAddress']
                    "ship_from_address": {
                        # 国家代码 [原字段: 'countryCode']
                        "country_code": "CN",
                        # 国家
                        "country": "中国",
                        # 州或省代码 [原字段 'stateOrProvinceCode']
                        "state": "Guangdong",
                        # 城市
                        "city": "Shenzhen",
                        # 地址行1 [原字段 'addressLine1']
                        "address_line1": "Fuyong",
                        # 地址行2 [原字段 'addressLine2']
                        "address_line2": "",
                        # 地址名称 [原字段 'addressName']
                        "address_name": "JBL",
                        # 邮政编码 [原字段 'postalCode']
                        "postcode": "518000",
                        # 电子邮箱
                        "email": "",
                        # 电话号码 [原字段 'phoneNumber']
                        "phone": "",
                    },
                    # 收货地址 [原字段 'sendAddress']
                    "ship_to_address": {
                        # 国家代码 [原字段: 'countryCode']
                        "country_code": "US",
                        # 国家
                        "country": "美国",
                        # 州或省代码 [原字段 'stateOrProvinceCode']
                        "state": "NC",
                        # 城市
                        "city": "Charlotte",
                        # 地址行1 [原字段 'addressLine1']
                        "address_line1": "10240 Old Dowd Rd",
                        # 地址行2 [原字段 'addressLine2']
                        "address_line2": "",
                        # 地址名称 [原字段 'addressName']
                        "address_name": "Amazon.com Services, Inc.",
                        # 邮政编码 [原字段 'postalCode']
                        "postcode": "28214-8082",
                        # 电子邮箱
                        "email": "",
                        # 电话号码 [原字段 'phoneNumber']
                        "phone": "",
                    },
                    # 追踪号码 [原字段 'trackingNumber']
                    "tracking_number": "",
                    # 追踪号码列表 [原字段 'trackingNumberList']
                    "tracking_numbers": [
                        {
                            # 包裹ID [原字段 'boxId']
                            "box_id": "FBA1905423KBU000002",
                            # 追踪号码 [原字段 'trackingNumber']
                            "tracking_number": ""
                        },
                    ],
                    # 货件商品数量 [原字段 'itemCount']
                    "item_count": 2,
                    # 货件商品列表 [原字段 'itemList']
                    "items": [
                        {
                            # 亚马逊ASIN
                            "asin": "B0D*******",
                            # 父ASIN [原字段 'parent_asin']
                            "parent_asin": "B0D*******",
                            # 亚马逊SKU
                            "msku": "SKU********",
                            # 领星本地SKU [原字段 'sku']
                            "lsku": "LOCAL********",
                            # 亚马逊FNSKU
                            "fnsku": "X00*******",
                            # 领星本地商品名称 [原字段 'productName']
                            "product_name": "P********",
                            # 商品标题
                            "title": "Product Title",
                            # 商品略缩图
                            "thumbnail_url": "https://m.media-amazon.com/****.jpg",
                            # 预处理方 [原字段 'prepOwner']
                            "prep_owner": "SELLER",
                            # 标签处理方 [原字段 'labelOwner']
                            "label_owner": "SELLER",
                            # 有效日期 [原字段 'expiration']
                            "expiration_date": "",
                            # 货件申报数量 [原字段 'quantity']
                            "item_qty": 500,
                        },
                        ...
                    ],
                },
                ...
            ],
        }
        ```
        """
        url = route.SHIPMENT_DETAILS
        # 解析并验证参数
        args = {
            "sid": sid,
            "inbound_plan_id": inbound_plan_id,
            "shipment_ids": shipment_ids,
        }
        try:
            p = param.ShipmentDetails.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.ShipmentDetails.model_validate(data)

    async def ShipmentBoxes(
        self,
        sid: int,
        inbound_plan_id: str,
        shipment_ids: str | list[str],
    ) -> schema.ShipmentBoxes:
        """查询货件装箱信息

        ## Docs
        - FBA - FBA货件(STA): [查询货件装箱信息](https://apidoc.lingxing.com/#/docs/FBA/ListShipmentBoxes)

        :param sid `<'int'>`: 领星店铺ID
        :param inbound_plan_id `<'str'>`: STA计划ID, 参数来源: `StaPlan.inbound_plan_id`
        :param shipment_ids `<'str/list[str]'>`: 货件ID或ID列表, 参数来源: `Shipment.sta_shipment_id`
        :returns `<'ShipmentBoxes'>`: 返回查询货件装箱信息的结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "操作成功",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "f9e5e291e14c4180a3cf1405b4d24b99.191.17554878107185127",
            # 响应时间
            "response_time": "2025-08-18T11:30:10.826",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 货件ID [原字段 'shipmentId']
                    "shipment_id": "sha51eae2f-****-****-****-************",
                    # 装箱列表 [原字段 'shipmentPackingList']
                    "boxes": [
                        {
                            # 包裹ID [原字段 'packageId']
                            "package_id": "pkd0ab9bcc-****-****-****-************",
                            # 箱子序列 [原字段 'localBoxId']
                            "box_seq": 1,
                            # 亚马逊箱子ID [原字段 'boxId']
                            "box_id": "FBA18**************
                            # 箱子名称 [原字段 'boxName']
                            "box_name": "P1 - B1",
                            # 箱子产品总数量 [原字段 'total']
                            "box_item_qty": 40,
                            # 箱子重量
                            "weight": 22.0,
                            # 重量单位 [原字段 'weightUnit']
                            "weight_unit": "LB",
                            # 箱子长度
                            "length": 16.0,
                            # 箱子宽度
                            "width": 10.0,
                            # 箱子高度
                            "height": 18.0,
                            # 箱子尺寸单位 [原字段 'lengthUnit']
                            "dimension_unit": "IN",
                            # 商品列表 [原字段 'productList']
                            "items": [
                                {
                                    # 亚马逊ASIN
                                    "asin": "B0D*******",
                                    # 父ASIN [原字段 'parent_asin']
                                    "parent_asin": "B0D*******",
                                    # 亚马逊SKU
                                    "msku": "SKU********",
                                    # 领星本地SKU [原字段 'sku']
                                    "lsku": "LOCAL********",
                                    # 亚马逊FNSKU
                                    "fnsku": "X00*******",
                                    # 领星本地商品名称 [原字段 'productName']
                                    "product_name": "P********",
                                    # 商品标题
                                    "title": "Product Title",
                                    # 商品略缩图
                                    "thumbnail_url": "https://m.media-amazon.com/****.jpg",
                                    # 预处理方 [原字段 'prepOwner']
                                    "prep_owner": "SELLER",
                                    # 标签处理方 [原字段 'labelOwner']
                                    "label_owner": "SELLER",
                                    # 有效日期 [原字段 'expiration']
                                    "expiration_date": "",
                                    # 箱子商品数量 [原字段 'quantityInBox']
                                    "item_qty": 40,
                                },
                                ...
                            ],
                        },
                        ...
                    ],
                    # 装箱托盘列表 [原字段 'palletList']
                    "pallets": [
                        {
                            # 托盘重量
                            "weight": 220.0,
                            # 重量单位 [原字段 'weightUnit']
                            "weight_unit": "LB",
                            # 托盘长度
                            "length": 160.0,
                            # 托盘宽度
                            "width": 100.0,
                            # 托盘高度
                            "height": 180.0,
                            # 托盘尺寸单位 [原字段 'lengthUnit']
                            "dimension_unit": "IN",
                            # 托盘数量 [原字段 'quantity']
                            "pallet_qty": 1,
                            # 堆叠方式
                            "stackability": "STACKABLE",
                        },
                        ...
                    ],
                },
                ...
            ],
        }
        ```
        """
        url = route.SHIPMENT_BOXES
        # 解析并验证参数
        args = {
            "sid": sid,
            "inbound_plan_id": inbound_plan_id,
            "shipment_ids": shipment_ids,
        }
        try:
            p = param.ShipmentBoxes.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.ShipmentBoxes.model_validate(data)

    async def ShipmentTransports(
        self,
        sid: int,
        inbound_plan_id: str,
        shipment_id: str,
    ) -> schema.ShipmentTransports:
        """查询货件承运方式

        ## Docs
        - FBA - FBA货件(STA): [查询承运方式](https://apidoc.lingxing.com/#/docs/FBA/GetTransportList)

        :param sid `<'int'>`: 领星店铺ID
        :param inbound_plan_id `<'str'>`: STA计划ID, 参数来源: `StaPlan.inbound_plan_id`
        :param shipment_id `<'str'>`: 货件ID, 参数来源: `Shipment.sta_shipment_id`
        :returns `<'ShipmentTransports'>`: 返回查询货件承运方式的结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "操作成功",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "f9e5e291e14c4180a3cf1405b4d24b99.191.17554878107185127",
            # 响应时间
            "response_time": "2025-08-18T11:30:10.826",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 承运选项ID [原字段 'transportationOptionId']
                    "transport_option_id": "to3ea8cf93-****-****-****-************",
                    # 承运方式名称 [原字段 'alphaName']
                    "transport_name": "UPS",
                    # 承运方式编码 [原字段 'alphaCode']
                    "transport_code": "UPSN",
                    # 运输类型 [原字段 'shippingMode']
                    "shipping_mode": "GROUND_SMALL_PARCEL",
                    # 运输解决方案 [原字段 'shippingSolution']
                    "shipping_solution": "AMAZON_PARTNERED_CARRIER",
                },
                ...
            ],
        }
        ```
        """
        url = route.SHIPMENT_TRANSPORTS
        # 解析并验证参数
        args = {
            "sid": sid,
            "inbound_plan_id": inbound_plan_id,
            "shipment_id": shipment_id,
        }
        try:
            p = param.ShipmentTransports.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.ShipmentTransports.model_validate(data)

    async def ShipmentReceiptRecords(
        self,
        sid: int,
        date: str | datetime.date | datetime.datetime,
        *,
        shipment_ids: str | list[str] | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.ShipmentReceiptRecords:
        """查询货件货接收明细

        ## Docs
        - FBA - FBA货件(STA): [查询FBA到货接收明细](https://apidoc.lingxing.com/#/docs/FBA/FBAReceivedInventory)

        :param sid `<'int'>`: 领星店铺ID
        :param date `<'str/date/datetime'>`: 货件接收日期
        :param shipment_ids `<'str/list[str]'>`: 货件ID或ID列表, 默认 `None` (不筛选)
        :param offset `<'int'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int'>`: 分页长度, 默认 `None` (使用: 1000)
        :returns `<'ShipmentReceiptRecords'>`: 返回查询货件接收明细的结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "操作成功",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "f9e5e291e14c4180a3cf1405b4d24b99.191.17554878107185127",
            # 响应时间
            "response_time": "2025-08-20 11:00:54",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": [
                {
                    # 唯一md5索引
                    "uid_md5": "7665b697************************",
                    # 领星店铺ID
                    "sid": 9968,
                    # 亚马逊SKU [原字段 'sku']
                    "msku": "AC-618-305XL 1B1C-EU-X",
                    # 亚马逊FNSKU
                    "fnsku": "X0027O96FF",
                    # 商品标题 [原字段 'product_name']
                    "title": "Product Title",
                    # 货件ID [原字段 'fba_shipment_id']
                    "shipment_id": "FBA15KGYN4HK",
                    # 亚马逊配送中心编码
                    "fulfillment_center_id": "CDG7",
                    # 亚马逊配送中心国家代码 [原字段 'country']
                    "country_code": "FR",
                    # 货件接收数量 [原字段 'quantity']
                    "received_qty": -2,
                    # 货件接收日期 [原字段 'received_date_report']
                    "received_date": "2025-07-21",
                    # 货件接收时间 (UTC) [原字段 'received_date']
                    "received_time_utc": "2025-07-21T00:00:00+00:00",
                    # 货件接收时间 (时间戳) [原字段 'received_date_timestamp']
                    "received_time_ts": 1753027200,
                },
                ...
            ],
        }
        ```
        """
        url = route.SHIPMENT_RECEIPT_RECORDS
        # 解析并验证参数
        args = {
            "sid": sid,
            "date": date,
            "shipment_ids": shipment_ids,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.ShipmentReceiptRecords.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.ShipmentReceiptRecords.model_validate(data)

    async def ShipmentDeliveryAddress(
        self,
        id: int,
    ) -> schema.ShipmentDeliveryAddressData:
        """查询FBA货件收货地址

        ## Docs
        - FBA - FBA货件(STA): [地址簿-配送地址详情](https://apidoc.lingxing.com/#/docs/FBA/ShoppingAddress)

        :param id `<'int'>`: 货件唯一记录ID, 参数来源: `Shipment.id`
        :returns `<'ShipToAddress'>`: 返回查询货件收货地址的结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "操作成功",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "f9e5e291e14c4180a3cf1405b4d24b99.191.17554878107185127",
            # 响应时间
            "response_time": "2025-08-20 11:00:54",
            # 响应数据量
            "response_count": 2,
            # 总数据量
            "total_count": 2,
            # 响应数据
            "data": {
                # 国家名称 [原字段 'ship_to_country']
                "country": "United States of America (USA)",
                # 州或省 [原字段 'ship_to_province_code']
                "state": "TN",
                # 城市 [原字段 'ship_to_city']
                "city": "Memphis",
                # 地址行 [原字段 'ship_to_address']
                "address": "3292 E Holmes Rd",
                # 邮政编码 [原字段 'ship_to_postal_code']
                "postcode": "38118-8102",
                # 收货人名称 [原字段 'ship_to_name']
                "receiver_name": "MEM1",
            },
        }
        ```
        """
        url = route.SHIPMENT_DELIVERY_ADDRESS
        # 解析并验证参数
        args = {"id": id}
        try:
            p = param.ShipmentDeliveryAddress.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.ShipmentDeliveryAddressData.model_validate(data)

    async def ShipFromAddresses(
        self,
        *,
        sids: int | list[int] | None = None,
        search_field: ADDRESS_SEARCH_FIELD | None = None,
        search_value: str | None = None,
        offset: int | None = None,
        length: int | None = None,
    ) -> schema.ShipFromAddresses:
        """查询发货地址

        ## Docs
        - FBA - FBA货件(STA): [地址簿-发货地址列表](https://apidoc.lingxing.com/#/docs/FBA/ShipFromAddressList)

        :param sids `<'int/list/None'>`: 领星店铺ID或ID列表, 默认 `None` (不筛选)
        :param search_field `<'str/None'>`: 搜索字段, 默认 `None` (不筛选), 可选值:

            - `'alias_name'`: 地址别名
            - `'sender_name'`: 发货人名称

        :param search_value `<'str/None'>`: 搜索值, 模糊搜索, 默认 `None` (不筛选)
        :param offset `<'int/None'>`: 分页偏移量, 默认 `None` (使用: 0)
        :param length `<'int/None'>`: 分页长度, 默认 `None` (使用: 20)
        :returns `<'ShipFromAddresses'>`: 返回查询发货地址的结果
        ```python
        {
            # 状态码
            "code": 0,
            # 提示信息
            "message": "操作成功",
            # 错误信息
            "errors": [],
            # 请求ID
            "request_id": "f9e5e291e14c4180a3cf1405b4d24b99.191.17554878107185127",
            # 响应时间
            "response_time": "2025-08-20 11:00:54",
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
                    "seller_name": "UK-Store",
                    # 店铺国家名称 [原字段 'seller_country_name']
                    "seller_country": "英国",
                    # 地址ID [原字段 'id' | 唯一键]
                    "address_id": 1***,
                    # 地址别名 [原字段 'alias_name']
                    "address_alias": "测试发货地址",
                    # 国家代码
                    "country_code": "CN",
                    # 国家名称 [原字段 'country_name']
                    "country": "中国 内地",
                    # 州或省 [原字段 'province']
                    "state": "广东省",
                    # 城市
                    "city": "深圳市",
                    # 区域 [原字段 'region']
                    "district": "福田区",
                    # 地址行1 [原字段 'street_detail1']
                    "address_line1": "",
                    # 地址行2 [原字段 'street_detail2']
                    "address_line2": "",
                    # 邮政编码 [原字段 'zip_code']
                    "postcode": "518000",
                    # 发件人名称 [原字段 'sender_name']
                    "shipper_name": "测试",
                    # 公司名称 [原字段 'company_name']
                    "company_name": "测试",
                    # 电话号码 [原字段 'phone']
                    "phone": "1234567890",
                    # 电子邮箱 [原字段 'email']
                    "email": "test@gmail.com",
                    # 是否为默认地址 [原字段 'is_default']
                    "is_default": 0,
                },
                ...
            ],
        }
        ```
        """
        url = route.SHIP_FROM_ADDRESSES
        # 解析并验证参数
        args = {
            "sids": sids,
            "search_field": search_field,
            "search_value": search_value,
            "offset": offset,
            "length": length,
        }
        try:
            p = param.ShipFromAddresses.model_validate(args)
        except Exception as err:
            raise errors.InvalidParametersError(err, url, args) from err

        # 发送请求
        data = await self._request_with_sign("POST", url, body=p.model_dump_params())
        return schema.ShipFromAddresses.model_validate(data)
