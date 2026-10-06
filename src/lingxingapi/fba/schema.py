# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field, field_validator, model_validator
from lingxingapi import errors
from lingxingapi.base.schema import ResponseV1, ResponseV2, FlattenDataRecords
from lingxingapi.fields import FloatOrNone2Zero, StrOrNone2Blank


# Share ------------------------------------------------------------------------------------------------------------------------
class BaseItem(BaseModel):
    """基础商品信息"""

    # 亚马逊ASIN
    asin: StrOrNone2Blank
    # 父ASIN [原字段 'parent_asin']
    parent_asin: StrOrNone2Blank = Field(validation_alias="parentAsin")
    # 亚马逊SKU
    msku: StrOrNone2Blank
    # 领星本地SKU [原字段 'sku']
    lsku: StrOrNone2Blank = Field(validation_alias="sku")
    # 亚马逊FNSKU
    fnsku: StrOrNone2Blank
    # 领星本地商品名称 [原字段 'productName']
    product_name: StrOrNone2Blank = Field(validation_alias="productName")
    # 商品标题
    title: StrOrNone2Blank
    # 商品略缩图
    thumbnail_url: StrOrNone2Blank = Field(validation_alias="url")


# FBA - FBA货件 (STA) ----------------------------------------------------------------------------------------------------------
# . STA Plans
class StaPlanShipment(BaseModel):
    """亚马逊STA计划货件"""

    # 货件ID
    shipment_id: str = Field(validation_alias="shipmentId")
    # 货件确认ID
    shipment_confirmation_id: str = Field(validation_alias="shipmentConfirmationId")
    # 货件状态 [原字段 'status']
    shipment_status: str = Field("", validation_alias="status")
    # 取件ID
    pick_up_id: StrOrNone2Blank = Field(validation_alias="pickUpId")
    # 运单号
    freight_bill_number: StrOrNone2Blank = Field(validation_alias="freightBillNumber")


class StaItem(BaseItem):
    """亚马逊STA计划货件商品"""

    # 预处理方 [原字段 'prepOwner']
    prep_owner: StrOrNone2Blank = Field(validation_alias="prepOwner")
    # 标签处理方 [原字段 'labelOwner']
    label_owner: StrOrNone2Blank = Field(validation_alias="labelOwner")
    # 有效日期 [原字段 'expiration']
    expiration_date: StrOrNone2Blank = Field(validation_alias="expiration")


class StaPlanItem(StaItem):
    """亚马逊STA计划货件商品"""

    # 货件申报数量 [原字段 'quantity']
    item_qty: int = Field(validation_alias="quantity")


class StaPlan(BaseModel):
    """亚马逊STA计划"""

    # 领星店铺ID
    sid: int
    # STA计划ID [原字段 'inboundPlanId']
    inbound_plan_id: str = Field(validation_alias="inboundPlanId")
    # STA计划名称 [原字段 'planName']
    plan_name: str = Field(validation_alias="planName")
    # 计划状态
    status: str
    # 分仓类型 (1: 先装箱再分仓, 2: 先分仓再装箱)
    position_type: str = Field(validation_alias="positionType")
    # 创建时间 [原字段 'gmtCreate']
    create_time: str = Field(validation_alias="gmtCreate")
    # 计划创建时间 [原字段 'planCreateTime']
    plan_create_time: str = Field(validation_alias="planCreateTime")
    # 更新时间 [原字段 'gmtModified']
    update_time: str = Field(validation_alias="gmtModified")
    # 计划更新时间 [原字段 'planUpdateTime']
    plan_update_time: str = Field(validation_alias="planUpdateTime")
    # 货件列表 [原字段 'shipmentList']
    shipments: list[StaPlanShipment] = Field(validation_alias="shipmentList")
    # 计划商品列表 [原字段 'inboundPlanItemList']
    items: list[StaPlanItem] = Field(validation_alias="inboundPlanItemList")


class StaPlans(ResponseV2, FlattenDataRecords):
    """亚马逊STA计划列表"""

    data: list[StaPlan]


# . STA Plan Detail
class StaPlanAddress(BaseModel):
    """亚马逊STA计划发货地址"""

    # 国家代码 [原字段 'countryCode']
    country_code: str = Field(validation_alias="countryCode")
    # 国家名称 [原字段 'countryName']
    country: str = Field(validation_alias="countryName")
    # 州或省代码 [原字段 'stateOrProvinceCode']
    state: str = Field(validation_alias="stateOrProvinceCode")
    # 城市
    city: str
    # 发货地址行1 [原字段 'addressLine1']
    address_line1: str = Field(validation_alias="addressLine1")
    # 发货地址行2 [原字段 'addressLine2']
    address_line2: StrOrNone2Blank = Field(validation_alias="addressLine2")
    # 邮政编码 [原字段 'postalCode']
    postcode: str = Field(validation_alias="postalCode")
    # 发货人姓名 [原字段 'shipperName']
    shipper_name: str = Field(validation_alias="shipperName")
    # 电子邮件 [原字段 'email']
    email: str = Field(validation_alias="email")
    # 电话号码 [原字段 'phoneNumber']
    phone: str = Field(validation_alias="phoneNumber")


class StaPlanDetail(BaseModel):
    """亚马逊STA计划详情"""

    # STA计划ID [原字段 'inboundPlanId']
    inbound_plan_id: str = Field(validation_alias="inboundPlanId")
    # 计划名称 [原字段 'planName']
    plan_name: str = Field(validation_alias="planName")
    # 计划状态
    status: str
    # 分仓类型 (1: 先装箱再分仓, 2: 先分仓再装箱)
    position_type: str = Field(validation_alias="positionType")
    # 创建时间 [原字段 'gmtCreate']
    create_time: str = Field(validation_alias="gmtCreate")
    # 计划创建时间 [原字段 'planCreateTime']
    plan_create_time: str = Field(validation_alias="planCreateTime")
    # 更新时间 [原字段 'gmtModified']
    update_time: str = Field(validation_alias="gmtModified")
    # 计划更新时间 [原字段 'planUpdateTime']
    plan_update_time: str = Field(validation_alias="planUpdateTime")
    # 货件列表 [原字段 'shipmentList']
    shipments: list[StaPlanShipment] = Field(validation_alias="shipmentList")
    # 发货地址 [原字段 'addressVO']
    shipment_address: StaPlanAddress = Field(validation_alias="addressVO")
    # 计划商品列表 [原字段 'productList']
    items: list[StaPlanItem] = Field(validation_alias="productList")


class StaPlanDetailData(ResponseV2):

    data: StaPlanDetail


# . Packing Groups
class PackingGroup(BaseModel):
    """亚马逊STA包装组"""

    # 包装组ID [原字段 'packingGroupId']
    packing_group_id: str = Field(validation_alias="packingGroupId")
    # 包装组商品列表 [原字段 'packingGroupItemList']
    items: list[StaPlanItem] = Field(validation_alias="packingGroupItemList")


class PackingGroups(ResponseV2):
    """亚马逊STA包装组"""

    data: list[PackingGroup]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @model_validator(mode="before")
    def _flatten_data(cls, data: dict) -> dict:
        try:
            inner: dict = data.pop("data", {})
            data["data"] = inner.get("packingGroupList", [])
        except Exception:
            raise errors.ResponseDataError(cls.__name__, data=data)
        return data


# . Packing Group Boxes
class PackingGroupBoxItem(StaItem):
    """亚马逊STA包装组装箱商品"""

    # 箱内商品总数量 [原字段 'quantityInBox']
    item_qty: int = Field(validation_alias="quantityInBox")


class PackingGroupBoxItem(BaseModel):
    """亚马逊STA庄庄组装箱商品"""

    # 包裹ID [原字段 'packageId']
    package_id: StrOrNone2Blank = Field(validation_alias="packageId")
    # 箱子顺序号 [原字段 'localBoxId']
    box_seq: int = Field(validation_alias="localBoxId")
    # 亚马逊箱子ID [原字段 'boxId']
    box_id: StrOrNone2Blank = Field(validation_alias="boxId")
    # 箱子名称 [原字段 'boxName']
    box_name: str = Field(validation_alias="boxName")
    # 箱内商品总数量 [原字段 'total']
    box_item_qty: int = Field(validation_alias="total")
    # 箱子重量
    weight: float
    # 重量单位 [原字段 'weightUnit']
    weight_unit: str = Field(validation_alias="weightUnit")
    # 箱子长度
    length: float
    # 箱子宽度
    width: float
    # 箱子高度
    height: float
    # 箱子尺寸单位 [原字段 'lengthUnit']
    dimension_unit: str = Field(validation_alias="lengthUnit")
    # 箱内商品列表 [原字段 'productList']
    items: list[PackingGroupBoxItem] = Field(validation_alias="productList")


class PackingGroupBox(BaseModel):
    """亚马逊STA庄庄组装箱"""

    # 包装组ID [原字段 'packingGroupId']
    packing_group_id: str = Field(validation_alias="packingGroupId")
    # 装箱列表 [原字段 'shipmentPackingList']
    boxes: list[PackingGroupBoxItem] = Field(validation_alias="shipmentPackingList")


class PackingGroupBoxes(ResponseV2):
    """亚马逊STA庄庄组装箱"""

    data: list[PackingGroupBox]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @model_validator(mode="before")
    def _flatten_data(cls, data: dict) -> dict:
        try:
            inner: dict = data.pop("data", {})
            data["data"] = inner.get("packingGroupList", [])
        except Exception:
            raise errors.ResponseDataError(cls.__name__, data=data)
        return data


# . Placement Options
class PlacementOptionExpirationOffsetRules(BaseModel):
    """亚马逊FBA货件计划分仓选项过期时间规则"""

    # 时区过渡
    transitions: list
    # 时区过渡规则 [原字段 'transitionRules']
    transition_rules: list = Field(validation_alias="transitionRules")
    # 时区是否固定偏移 [原字段 'fixedOffset']
    fixed_offset: bool = Field(validation_alias="fixedOffset")


class PlacementOptionExpirationOffset(BaseModel):
    """亚马逊FBA货件计划分仓选项过期时间偏移"""

    # 时区ID [原字段 'id']
    timezone_id: str = Field(validation_alias="id")
    # 时区偏移秒数 [原字段 'totalSeconds']
    seconds: int = Field(validation_alias="totalSeconds")
    # 时区规则
    rules: PlacementOptionExpirationOffsetRules


class PlacementOptionExpiration(BaseModel):
    """亚马逊FBA货件计划分仓选项过期时间"""

    # 年份值
    year: int
    # 月份值 [原字段 'monthValue']
    month: int = Field(validation_alias="monthValue")
    # 天数值 [原字段 'dayOfMonth']
    day: int = Field(validation_alias="dayOfMonth")
    # 小时值
    hour: int
    # 分钟值
    minute: int
    # 秒值
    second: int
    # 纳秒值
    nano: int
    # 年内日序 [原字段 'dayOfYear']
    day_of_year: int = Field(validation_alias="dayOfYear")
    # 月份名称 [原字段 'month']
    month_name: str = Field(validation_alias="month")
    # 星期名称 [原字段 'dayOfWeek']
    weekday_name: str = Field(validation_alias="dayOfWeek")
    # 时区偏移 [原字段 'offset']
    offset: PlacementOptionExpirationOffset = Field(validation_alias="offset")


class PlacementOptionFee(BaseModel):
    """亚马逊FBA货件计划分仓选项费用"""

    # 费用项目 [原字段 'target']
    # (如: Placement Services, Fulfillment Fee Discount)
    charge: str = Field(validation_alias="target")
    # 费用类型 (如: FEE, DISCOUNT)
    type: str
    # 费用金额 [原字段 'amount']
    fee_amt: float = Field(validation_alias="amount")
    # 费用币种代码 [原字段 'code']
    currency_code: str = Field(validation_alias="code")


class PlacementOptionShipmentAddress(BaseModel):
    """亚马逊FBA货件详情发货地址"""

    # 国家代码 [原字段: 'countryCode']
    country_code: StrOrNone2Blank = Field(validation_alias="countryCode")
    # 州或省代码 [原字段 'stateOrProvinceCode']
    state: StrOrNone2Blank = Field(validation_alias="stateOrProvinceCode")
    # 城市
    city: StrOrNone2Blank
    # 地址行1 [原字段 'addressLine1']
    address_line1: StrOrNone2Blank = Field(validation_alias="addressLine1")
    # 地址行2 [原字段 'addressLine2']
    address_line2: StrOrNone2Blank = Field(validation_alias="addressLine2")
    # 地址名称 [原字段 'addressName']
    address_name: StrOrNone2Blank = Field(validation_alias="name")
    # 邮政编码 [原字段 'postalCode']
    postcode: StrOrNone2Blank = Field(validation_alias="postalCode")
    # 公司名称 [原字段 'companyName']
    company_name: StrOrNone2Blank = Field(validation_alias="companyName")
    # 电子邮箱
    email: StrOrNone2Blank
    # 电话号码 [原字段 'phoneNumber']
    phone: StrOrNone2Blank = Field(validation_alias="phoneNumber")


class PlacementOptionItem(BaseItem):
    """亚马逊FBA货件计划分仓选项货件商品"""

    # 货件申报数量 [原字段 'quantity']
    item_qty: int = Field(validation_alias="quantity")


class PlacementOptionShipment(BaseModel):
    """亚马逊FBA货件计划分仓选项货件"""

    # 货件ID [原字段 'shipmentId']
    shipment_id: str = Field(validation_alias="shipmentId")
    # 货件名称 [原字段 'shipmentName']
    shipment_name: str = Field(validation_alias="shipmentName")
    # 亚马逊配送中心编码 [原字段 'wareHouseId']
    fulfillment_center_id: str = Field(validation_alias="wareHouseId")
    # 入库区域 (中文) [原字段 'postalCodeMark']
    inbound_region: StrOrNone2Blank = Field(validation_alias="postalCodeMark")
    # 收货地址 [原字段 'address']
    ship_to_address: PlacementOptionShipmentAddress = Field(validation_alias="address")
    # 不同货件商品数 [原字段 'itemCount']
    item_count: int = Field(validation_alias="itemCount")
    # 货件商品申报总数量 [原字段 'quantity']
    items_qty: int = Field(validation_alias="quantity")
    # 货件商品列表 [原字段 'itemList']
    items: list[PlacementOptionItem] = Field(validation_alias="itemList")


class PlacementOption(BaseModel):
    """亚马逊FBA货件计划分仓选项"""

    # fmt: off
    # 货件分仓方案ID [原字段 'placementOptionId']
    placement_option_id: str = Field(validation_alias="placementOptionId")
    # 货件分仓状态 [原字段 'placementStatus']
    placement_status: str = Field(validation_alias="placementStatus")
    # 货件分仓过期时间 [原字段 'expiration']
    expiration: PlacementOptionExpiration
    # 总费用 [原字段 'feeCount']
    fee_amt: float = Field(validation_alias="feeCount")
    # 费用列表 [原字段 'fees']
    fees: list[PlacementOptionFee] = Field(validation_alias="fees")
    # 货件列表 [原字段 'shipmentInformationList']
    shipments: list[PlacementOptionShipment] = Field(validation_alias="shipmentInformationList")
    # fmt: on


class PlacementOptions(ResponseV2):
    """亚马逊FBA货件计划数据"""

    data: list[PlacementOption]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @model_validator(mode="before")
    def _flatten_data(cls, data: dict) -> dict:
        try:
            inner: dict = data.pop("data", {})
            data["data"] = inner.get("placementOptionList", [])
        except Exception:
            raise errors.ResponseDataError(cls.__name__, data=data)
        return data


# . Placement Option Boxes
class PlacementOptionShipmentBoxItem(BaseItem):
    """亚马逊FBA货件计划分仓选项装箱商品"""

    # 箱内商品总数量 [原字段 'quantityInBox']
    item_qty: int = Field(validation_alias="quantityInBox")


class PlacementOptionShipmentBox(BaseModel):
    """亚马逊FBA货件计划分仓选项装箱"""

    # 箱子名称 [原字段 'boxName']
    box_name: str = Field(validation_alias="boxName")
    # 箱子重量
    weight: float
    # 重量单位 [原字段 'weightUnit']
    weight_unit: str = Field(validation_alias="weightUnit")
    # 箱子长度
    length: float
    # 箱子宽度
    width: float
    # 箱子高度
    height: float
    # 箱子尺寸单位 [原字段 'lengthUnit']
    dimension_unit: str = Field(validation_alias="lengthUnit")
    # 箱子总数量 [原字段 'total']
    box_qty: int = Field(validation_alias="total")
    # 箱内商品列表 [原字段 'productList']
    items: list[PlacementOptionShipmentBoxItem] = Field(validation_alias="productList")


class PlacementOptionShipmentBoxes(BaseModel):
    """亚马逊FBA货件计划分仓选项装箱"""

    # fmt: off
    # 货件ID [原字段 'shipmentId']
    shipment_id: str = Field(validation_alias="shipmentId")
    # 货件重量
    weight: FloatOrNone2Zero
    # 货件重量单位 [原字段 'weightUnit']
    weight_unit: StrOrNone2Blank = Field(validation_alias="weightUnit")
    # 货件体积
    volume: FloatOrNone2Zero
    # 货件体积单位 [原字段 'volumeUnit']
    volume_unit: StrOrNone2Blank = Field(validation_alias="volumeUnit")
    # 装箱列表 [原字段 'shipmentPackingList']
    boxes: list[PlacementOptionShipmentBox] = Field(validation_alias="shipmentPackingList")
    # fmt: on

    @field_validator("boxes", mode="before")
    def _validate_boxes(cls, v):
        return [] if v is None else v


class PlacementOptionShipmentsBoxes(BaseModel):
    """亚马逊FBA货件计划分仓选项装箱信息"""

    # fmt: off
    # 货件分仓方案ID [原字段 'placementOptionId']
    placement_option_id: str = Field(validation_alias="placementOptionId")
    # 货件分仓状态 [原字段 'placementStatus']
    placement_status: str = Field(validation_alias="placementStatus")
    # 货件装箱列表 [原字段 'shipmentInformationList']
    shipments: list[PlacementOptionShipmentBoxes] = Field(validation_alias="shipmentInformationList")
    # fmt: on


class PlacementOptionBoxes(ResponseV2):
    """亚马逊FBA货件计划分仓选项装箱数据"""

    data: list[PlacementOptionShipmentsBoxes]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @model_validator(mode="before")
    def _flatten_data(cls, data: dict) -> dict:
        try:
            inner: dict = data.pop("data", {})
            data["data"] = inner.get("placementOptionList", [])
        except Exception:
            raise errors.ResponseDataError(cls.__name__, data=data)
        return data


# . Shipments
class ShipmentAddress(BaseModel):
    """亚马逊FBA货件发货地址"""

    # 国家代码
    country_code: str
    # 州或省 [原字段 'state_or_province_code']
    state: str = Field(validation_alias="state_or_province_code")
    # 城市
    city: str
    # 地址区域 [原字段 'region']
    district: str = Field(validation_alias="region")
    # 地址行1
    address_line1: str
    # 地址行2
    address_line2: str
    # 地址名称 [原字段 'name']
    address_name: str = Field(validation_alias="name")
    # 邮政编码 [原字段 'postal_code']
    postcode: str = Field(validation_alias="postal_code")
    # 门牌号 [原字段 'doorplate']
    door_plate: str = Field("", validation_alias="doorplate")
    # 电话号码
    phone: str = ""


class ShipmentTrackingNumber(BaseModel):
    """亚马逊FBA货件追踪号码"""

    # 包裹ID
    box_id: str
    # 追踪号码
    tracking_number: str


class ShipmentItem(BaseModel):
    """亚马逊FBA货件商品"""

    # 唯一键
    id: int
    # 亚马逊SKU
    msku: str
    # 领星本地SKU [原字段 'sku']
    lsku: str = Field(validation_alias="sku")
    # 亚马逊FNSKU
    fnsku: str
    # 预处理说明
    prep_instruction: str
    # 预处理方
    prep_owner: str
    # 预处理明细
    prep_details: str
    # 标签处理方 [原字段 'prep_labelowner']
    label_owner: str = Field(validation_alias="prep_labelowner")
    # 有效日期 [原字段 'expiration']
    expiration_date: str = Field(validation_alias="expiration")
    # 生产日期
    release_date: str
    # 初始货件申报数量 [原字段 'init_quantity_shipped']
    init_item_qty: int = Field(validation_alias="init_quantity_shipped")
    # 当前货件申报数量 [原字段 'quantity_shipped']
    curr_item_qty: int = Field(validation_alias="quantity_shipped")
    # 箱内商品数量 [原字段 'quantity_in_case']
    box_item_qty: int = Field(validation_alias="quantity_in_case")
    # 已发货数量 [原字段 'quantity_shipped_local']
    shipped_qty: int = Field(validation_alias="quantity_shipped_local")
    # 亚马逊配送中心已接收的商品数量 [原字段 'quantity_received']
    received_qty: int = Field(validation_alias="quantity_received")
    # 库存明细ID [原字段 'ware_house_storage_id']
    warehouse_storage_id: int = Field(validation_alias="ware_house_storage_id")
    # 发货计划单号列表 [原字段 'shipment_plan_list']
    shipment_plan_numbers: list = Field(validation_alias="shipment_plan_list")


class Shipment(BaseModel):
    """亚马逊FBA货件"""

    # fmt: off
    # 唯一键
    id: int
    # 领星店铺ID
    sid: int
    # 领星店铺名称 [原字段 'seller']
    seller_name: str = Field(validation_alias="seller")
    # FBA货件ID
    shipment_id: str
    # FBA货件名称
    shipment_name: str
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
    shipment_status: str
    # 货件事否已完成 [原字段 'is_closed']
    # 有绑定, 按签发差异判断: 1. 发货量>签收量='进行中'; 2. 发货量<=签收量='已完成'
    # 无绑定, 用货件状态判断: DELETED, CANCELED, CLOSED为已完成, 其他为进行中
    # 额外情况: 当货件状态进入CLOSED, CANCELLED, DELETED 之后90天, 自动变为'已完成'
    shipment_closed: int = Field(validation_alias="is_closed")
    # 承运方式名称 [原字段 'alpha_name']
    transport_name: str = Field(validation_alias="alpha_name")
    # 承运方式编码 [原字段 'alpha_code']
    transport_code: str = Field(validation_alias="alpha_code")
    # 运输类型
    shipping_mode: str
    # 运输解决方案
    shipping_solution: str
    # 是否同步亚马逊后台 [原字段 'is_synchronous']
    is_synchronized: int = Field(validation_alias="is_synchronous")
    # 是否上传包装箱信息 [原字段 'is_uploaded_box']
    is_box_info_uploaded: int = Field(validation_alias="is_uploaded_box")
    # 货件创建人ID [原字段 'uid']
    creator_id: int = Field(validation_alias="uid")
    # 货件创建人名称 [原字段 'username']
    creator_name: str = Field(validation_alias="username")
    # 货件数据创建时间 [原字段 'gmt_create']
    create_time: str = Field(validation_alias="gmt_create")
    # 货件数据更新时间 [原字段 'gmt_modified']
    update_time: str = Field(validation_alias="gmt_modified")
    # 货件数据同步时间
    sync_time: str
    # 货件创建时间
    working_time: str
    # 承运人已取件时间
    shipped_time: str
    # 货件到达亚马逊配送中心后, 开始接收时间
    receiving_time: str
    # 货件到达亚马逊配送中心后, 完成接收时间
    closed_time: str
    # 是否为STA货件 (0: 否, 1: 是) 
    is_sta: int 
    # STA计划名称
    sta_plan_name: str
    # STA计划ID
    sta_inbound_plan_id: str
    # STA货件ID
    sta_shipment_id: str 
    # STA发货日期 [原字段 'sta_shipment_date']
    sta_shipping_date: str = Field(validation_alias="sta_shipment_date")
    # STA送达开始时间
    sta_delivery_start_date: str
    # STA送达结束时间
    sta_delivery_end_date: str
    # 提货单号 (BOL)
    bill_of_lading_number: str
    # 跟踪编号 (PRO) [原字段 'freight_bill_number']
    freight_pro_number: str = Field(validation_alias="freight_bill_number")
    # 亚马逊关联编码 [原字段 'reference_id']
    amazon_reference_id: str = Field(validation_alias="reference_id")
    # 亚马逊配送中心编码 [原字段 'destination_fulfillment_center_id']
    fulfillment_center_id: str = Field(validation_alias="destination_fulfillment_center_id")
    # 发货地址
    ship_from_address: ShipmentAddress
    # 收货地址
    ship_to_address: ShipmentAddress
    # 追踪号码列表 [原字段 'tracking_number_list']
    tracking_numbers: list[ShipmentTrackingNumber] = Field(validation_alias="tracking_number_list")
    # 货件商品列表 [原字段 'item_list']
    items: list[ShipmentItem] = Field(validation_alias="item_list")
    # fmt: on


class Shipments(ResponseV1):
    """亚马逊FBA货件列表"""

    data: list[Shipment]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @model_validator(mode="before")
    def _flatten_data(cls, data: dict) -> dict:
        try:
            inner: dict = data.pop("data", {})
            data["data"] = inner.get("list", [])
        except Exception:
            raise errors.ResponseDataError(cls.__name__, data=data)
        return data


# . Shipment Details
class ShipmentDetailAddress(BaseModel):
    """亚马逊FBA货件详情发货地址"""

    # 国家代码 [原字段: 'countryCode']
    country_code: StrOrNone2Blank = Field(validation_alias="countryCode")
    # 国家
    country: StrOrNone2Blank
    # 州或省代码 [原字段 'stateOrProvinceCode']
    state: StrOrNone2Blank = Field(validation_alias="stateOrProvinceCode")
    # 城市
    city: StrOrNone2Blank
    # 地址行1 [原字段 'addressLine1']
    address_line1: StrOrNone2Blank = Field(validation_alias="addressLine1")
    # 地址行2 [原字段 'addressLine2']
    address_line2: StrOrNone2Blank = Field(validation_alias="addressLine2")
    # 地址名称 [原字段 'addressName']
    address_name: StrOrNone2Blank = Field(validation_alias="addressName")
    # 邮政编码 [原字段 'postalCode']
    postcode: StrOrNone2Blank = Field(validation_alias="postalCode")
    # 电子邮箱
    email: StrOrNone2Blank
    # 电话号码 [原字段 'phoneNumber']
    phone: StrOrNone2Blank = Field(validation_alias="phoneNumber")


class ShipmentDetailTrackingNumber(BaseModel):
    """亚马逊FBA货件追踪号码"""

    # 包裹ID [原字段 'boxId']
    box_id: str = Field(validation_alias="boxId")
    # 追踪号码 [原字段 'trackingNumber']
    tracking_number: str = Field(validation_alias="trackingNumber")


class ShipmentDetail(BaseModel):
    """亚马逊FBA货件详情"""

    # fmt: off
    # 领星店铺ID
    sid: int
    # 货件ID [原字段 'shipmentId']
    shipment_id: str = Field(validation_alias="shipmentId")
    # 货件名称 [原字段 'shipmentName']
    shipment_name: str = Field(validation_alias="shipmentName")
    # 货件确认ID [原字段 'shipmentConfirmationId']
    shipment_confirmation_id: str = Field(validation_alias="shipmentConfirmationId")
    # 货件状态 [原字段 'status']
    shipment_status: str = Field(validation_alias="status")
    # 承运方式编码 [原字段 'alphaCode']
    transport_code: str = Field(validation_alias="alphaCode")
    # 运输类型 [原字段 'shippingMode']
    shipping_mode: str = Field(validation_alias="shippingMode")
    # 运输解决方案 [原字段 'shippingSolution']
    shipping_solution: str = Field(validation_alias="shippingSolution")
    # STA发货日期 [原字段 'shipingTime']
    shipping_date: StrOrNone2Blank = Field(validation_alias="shipingTime")
    # STA送达开始时间 [原字段 'startDate']
    delivery_start_date: StrOrNone2Blank = Field(validation_alias="startDate")
    # STA送达结束时间 [原字段 'endDate']
    delivery_end_date: StrOrNone2Blank = Field(validation_alias="endDate")
    # 提货单号 (BOL) [原字段 'pickUpId']
    bill_of_lading_number: StrOrNone2Blank = Field(validation_alias="pickUpId")
    # 亚马逊关联编码 [原字段 'amazonReferenceId']
    amazon_reference_id: str = Field(validation_alias="amazonReferenceId")
    # 亚马逊配送中心编码 [原字段 'warehouseId']
    fulfillment_center_id: str = Field(validation_alias="warehouseId")
    # 入库区域 (中文) [原字段 'inboundRegion']
    inbound_region: str = Field(validation_alias="inboundRegion")
    # 发货地址 [原字段 'sendAddress']
    ship_from_address: ShipmentDetailAddress = Field(validation_alias="sendAddress")
    # 收货地址 [原字段 'shippingAddress']
    ship_to_address: ShipmentDetailAddress = Field(validation_alias="shippingAddress")
    # 追踪号码 [原字段 'trackingNumber']
    tracking_number: StrOrNone2Blank = Field(validation_alias="trackingNumber")
    # 追踪号码列表 [原字段 'trackingNumberList']
    tracking_numbers: list[ShipmentDetailTrackingNumber] = Field(validation_alias="trackingNumberList")
    # 货件商品数量 [原字段 'itemCount']
    item_count: int = Field(validation_alias="itemCount")
    # 货件商品列表 [原字段 'itemList']
    items: list[StaPlanItem] = Field(validation_alias="itemList")
    # fmt: on


class ShipmentDetails(ResponseV2):
    """亚马逊FBA货件详情数据"""

    data: list[ShipmentDetail]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @model_validator(mode="before")
    def _flatten_data(cls, data: dict) -> dict:
        try:
            inner: dict = data.pop("data", {})
            data["data"] = inner.get("shipmentList", [])
        except Exception:
            raise errors.ResponseDataError(cls.__name__, data=data)
        return data


# . Shipment Boxes
class ShipmentBoxItem(StaItem):
    """亚马逊FBA货件装箱商品"""

    # 箱内商品总数量 [原字段 'quantityInBox']
    item_qty: int = Field(validation_alias="quantityInBox")


class ShipmentBox(BaseModel):
    """亚马逊FBA货件装箱商品"""

    # 包裹ID [原字段 'packageId']
    package_id: StrOrNone2Blank = Field(validation_alias="packageId")
    # 箱子序列 [原字段 'localBoxId']
    box_seq: int = Field(validation_alias="localBoxId")
    # 亚马逊箱子ID [原字段 'boxId']
    box_id: StrOrNone2Blank = Field(validation_alias="boxId")
    # 箱子名称 [原字段 'boxName']
    box_name: str = Field(validation_alias="boxName")
    # 箱子产品总数量 [原字段 'total']
    box_item_qty: int = Field(validation_alias="total")
    # 箱子重量
    weight: float
    # 重量单位 [原字段 'weightUnit']
    weight_unit: str = Field(validation_alias="weightUnit")
    # 箱子长度
    length: float
    # 箱子宽度
    width: float
    # 箱子高度
    height: float
    # 箱子尺寸单位 [原字段 'lengthUnit']
    dimension_unit: str = Field(validation_alias="lengthUnit")
    # 商品列表 [原字段 'productList']
    items: list[ShipmentBoxItem] = Field(validation_alias="productList")


class ShipmentPallet(BaseModel):
    """亚马逊FBA货件装箱托盘"""

    # 托盘重量
    weight: float
    # 重量单位 [原字段 'weightUnit']
    weight_unit: str = Field(validation_alias="weightUnit")
    # 托盘长度
    length: float
    # 托盘宽度
    width: float
    # 托盘高度
    height: float
    # 托盘尺寸单位 [原字段 'lengthUnit']
    dimension_unit: str = Field(validation_alias="lengthUnit")
    # 托盘数量 [原字段 'quantity']
    pallet_qty: int = Field(validation_alias="quantity")
    # 堆叠方式
    stackability: str


class ShipmentPackings(BaseModel):
    """亚马逊FBA货件装箱商品"""

    # 货件ID [原字段 'shipmentId']
    shipment_id: str = Field(validation_alias="shipmentId")
    # 装箱列表 [原字段 'shipmentPackingList']
    boxes: list[ShipmentBox] = Field(validation_alias="shipmentPackingList")
    # 装箱托盘列表 [原字段 'palletList']
    pallets: list[ShipmentPallet] = Field(validation_alias="palletList")


class ShipmentBoxes(ResponseV2):
    """亚马逊FBA货件装箱数据"""

    data: list[ShipmentPackings]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @model_validator(mode="before")
    def _flatten_data(cls, data: dict) -> dict:
        try:
            inner: dict = data.pop("data", {})
            data["data"] = inner.get("shipmentList", [])
        except Exception:
            raise errors.ResponseDataError(cls.__name__, data=data)
        return data


# . Shipment Transports
class ShipmentTransport(BaseModel):
    """亚马逊FBA货件运输数据"""

    # 承运选项ID [原字段 'transportationOptionId']
    transport_option_id: str = Field(validation_alias="transportationOptionId")
    # 承运方式名称 [原字段 'alphaName']
    transport_name: str = Field(validation_alias="alphaName")
    # 承运方式编码 [原字段 'alphaCode']
    transport_code: str = Field(validation_alias="alphaCode")
    # 运输类型 [原字段 'shippingMode']
    shipping_mode: str = Field(validation_alias="shippingMode")
    # 运输解决方案 [原字段 'shippingSolution']
    shipping_solution: str = Field(validation_alias="shippingSolution")


class ShipmentTransports(ResponseV2):
    """亚马逊FBA货件运输数据"""

    data: list[ShipmentTransport]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @model_validator(mode="before")
    def _flatten_data(cls, data: dict) -> dict:
        try:
            inner: dict = data.pop("data", {})
            data["data"] = inner.get("transportVOList", [])
        except Exception:
            raise errors.ResponseDataError(cls.__name__, data=data)
        return data


# . Shipment Receipt Records
class ShipmentReceiptRecord(BaseModel):
    """亚马逊FBA货件接收记录"""

    # 唯一md5索引
    uid_md5: str = Field(validation_alias="unique_md5")
    # 领星店铺ID
    sid: int
    # 亚马逊SKU [原字段 'sku']
    msku: str = Field(validation_alias="sku")
    # 亚马逊FNSKU
    fnsku: str
    # 商品标题 [原字段 'product_name']
    title: str = Field(validation_alias="product_name")
    # 货件ID [原字段 'fba_shipment_id']
    shipment_id: str = Field(validation_alias="fba_shipment_id")
    # 亚马逊配送中心编码
    fulfillment_center_id: str
    # 亚马逊配送中心国家代码 [原字段 'country']
    country_code: str = Field(validation_alias="country")
    # 货件接收数量 [原字段 'quantity']
    received_qty: int = Field(validation_alias="quantity")
    # 货件接收日期 [原字段 'received_date_report']
    received_date: str = Field(validation_alias="received_date_report")
    # 货件接收时间 (UTC) [原字段 'received_date']
    received_time_utc: str = Field(validation_alias="received_date")
    # 货件接收时间 (时间戳) [原字段 'received_date_timestamp']
    received_time_ts: int = Field(validation_alias="received_date_timestamp")


class ShipmentReceiptRecords(ResponseV1):
    """亚马逊FBA货件接收记录"""

    data: list[ShipmentReceiptRecord]


# . Shipment Delivery Address
class ShipmentDeliveryAddress(BaseModel):
    """亚马逊FBA货件收货地址"""

    # 国家名称 [原字段 'ship_to_country']
    country: str = Field(validation_alias="ship_to_country")
    # 州或省 [原字段 'ship_to_province_code']
    state: str = Field(validation_alias="ship_to_province_code")
    # 城市 [原字段 'ship_to_city']
    city: str = Field(validation_alias="ship_to_city")
    # 地址行 [原字段 'ship_to_address']
    address: str = Field(validation_alias="ship_to_address")
    # 邮政编码 [原字段 'ship_to_postal_code']
    postcode: str = Field(validation_alias="ship_to_postal_code")
    # 收货人名称 [原字段 'ship_to_name']
    receiver_name: str = Field(validation_alias="ship_to_name")


class ShipmentDeliveryAddressData(ResponseV1):
    """亚马逊FBA货件收货地址"""

    data: ShipmentDeliveryAddress


# . Ship From Addresses
class ShipFromAddress(BaseModel):

    # 领星店铺ID
    sid: int
    # 领星店铺名称
    seller_name: str
    # 店铺国家名称 [原字段 'seller_country_name']
    seller_country: str = Field(validation_alias="seller_country_name")
    # 地址ID [原字段 'id' | 唯一键]
    address_id: int = Field(validation_alias="id")
    # 地址别名 [原字段 'alias_name']
    address_alias: str = Field(validation_alias="alias_name")
    # 国家代码
    country_code: str
    # 国家名称 [原字段 'country_name']
    country: str = Field(validation_alias="country_name")
    # 州或省 [原字段 'province']
    state: str = Field(validation_alias="province")
    # 城市
    city: str
    # 区域 [原字段 'region']
    district: str = Field(validation_alias="region")
    # 地址行1 [原字段 'street_detail1']
    address_line1: str = Field(validation_alias="street_detail1")
    # 地址行2 [原字段 'street_detail2']
    address_line2: str = Field(validation_alias="street_detail2")
    # 邮政编码 [原字段 'zip_code']
    postcode: str = Field(validation_alias="zip_code")
    # 发件人名称 [原字段 'sender_name']
    shipper_name: str = Field(validation_alias="sender_name")
    # 公司名称 [原字段 'company_name']
    company_name: str = Field(validation_alias="company_name")
    # 电话号码 [原字段 'phone']
    phone: str
    # 电子邮箱 [原字段 'email']
    email: str
    # 是否为默认地址 [原字段 'is_default']
    is_default: int = Field(validation_alias="is_default")


class ShipFromAddresses(ResponseV1):
    """亚马逊FBA货件发货地址"""

    data: list[ShipFromAddress]
