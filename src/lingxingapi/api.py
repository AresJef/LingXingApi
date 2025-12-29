# -*- coding: utf-8 -*-c
from Crypto.Cipher import AES
from aiohttp import ClientTimeout
from lingxingapi import errors
from lingxingapi.base import schema
from lingxingapi.base.api import BaseAPI
from lingxingapi.basic.api import BasicAPI
from lingxingapi.sales.api import SalesAPI
from lingxingapi.fba.api import FbaAPI
from lingxingapi.product.api import ProductAPI
from lingxingapi.purchase.api import PurchaseAPI
from lingxingapi.warehourse.api import WarehouseAPI
from lingxingapi.ads.api import AdsAPI
from lingxingapi.finance.api import FinanceAPI
from lingxingapi.tools.api import ToolsAPI
from lingxingapi.source.api import SourceAPI


# API ------------------------------------------------------------------------------------------------------------------
class API(BaseAPI):
    """领星 API 客户端, 用于与领星开放平台进行交互

    ## Docs
    * 授权
        - AccessToken: [获取 access-token和refresh-token](https://apidoc.lingxing.com/#/docs/Authorization/GetToken)
        - RefreshToken: [续约接口令牌](https://apidoc.lingxing.com/#/docs/Authorization/RefreshToken)
    * 基础数据: basic
    * 销售数据: sales
    * 产品数据: product
    """

    def __init__(
        self,
        app_id: str,
        app_secret: str,
        timeout: int | float = 60,
        ignore_timeout: bool = False,
        ignore_timeout_wait: int | float = 1,
        ignore_timeout_retry: int = 10,
        ignore_api_limit: bool = False,
        ignore_api_limit_wait: int | float = 1,
        ignore_api_limit_retry: int = 10,
        ignore_internal_server_error: bool = False,
        ignore_internal_server_error_wait: int | float = 1,
        ignore_internal_server_error_retry: int = 10,
        ignore_internet_connection: bool = False,
        ignore_internet_connection_wait: int | float = 10,
        ignore_internet_connection_retry: int = 10,
        echo_retry_warnings: bool = True,
    ) -> None:
        """初始化领星 API 客户端

        :param app_id `<'str'>`: 应用ID, 用于鉴权

        :param app_secret `<'str'>`: 应用密钥, 用于鉴权

        :param timeout `<'int/float'>`: 请求超时 (单位: 秒), 默认为 60

        :param ignore_timeout `<'bool'>`: 是否忽略请求超时错误, 默认为 `False`,

            - 如果设置为 `True`, 则在请求超时时不会抛出异常, 而是会等待
              `ignore_timeout_wait` 秒后重试请求, 重试次数不超过 `ignore_timeout_retry`
            - 如果设置为 `False`, 则在请求超时时会抛出 `ApiTimeoutError` 异常

        :param ignore_timeout_wait `<'int/float'>`: 忽略请求超时时的等待时间 (单位: 秒),
            默认为 `1` 秒, 仅在 `ignore_timeout` 为 `True` 时生效

        :param ignore_timeout_retry `<'int'>`: 忽略请求超时时的最大重试次数,
            默认为 `10`, 仅在 `ignore_timeout` 为 `True` 时生效, 若设置为 `-1` 则表示无限重试

        :param ignore_api_limit `<'bool'>`: 是否忽略 API 限流错误, 默认为 `False`,

            - 如果设置为 `True`, 则在遇到限流错误时不会抛出异常, 而是会等待
              `ignore_api_limit_wait` 秒后重试请求, 重试次数不超过 `ignore_api_limit_retry`
            - 如果设置为 `False`, 则在遇到限流错误时会抛出 `ApiLimitError` 异常

        :param ignore_api_limit_wait `<'int/float'>`: 忽略 API 限流错误时的等待时间 (单位: 秒),
            默认为 `1` 秒, 仅在 `ignore_api_limit` 为 `True` 时生效

        :param ignore_api_limit_retry `<'int'>`: 忽略 API 限流错误时的最大重试次数,
            默认为 `10`, 仅在 `ignore_api_limit` 为 `True` 时生效, 若设置为 `-1` 则表示无限重试

        :param ignore_internal_server_error `<'bool'>`: 是否忽略服务器内部错误 (500错误码, 仅限 Internal Server Error 类型), 默认为 `False`,

            - 如果设置为 `True`, 则在遇到服务器内部错误时不会抛出异常, 而是会等待
              `ignore_internal_server_error_wait` 秒后重试请求, 重试次数不超过 `ignore_internal_server_error_retry`
            - 如果设置为 `False`, 则在遇到服务器内部错误时会抛出 `InternalServerError` 异常

        :param ignore_internal_server_error_wait `<'int/float'>`: 忽略服务器内部错误时的等待时间 (单位: 秒),
            默认为 `1` 秒, 仅在 `ignore_internal_server_error` 为 `True` 时生效

        :param ignore_internal_server_error_retry `<'int'>`: 忽略服务器内部错误时的最大重试次数,
            默认为 `10`, 仅在 `ignore_internal_server_error` 为 `True` 时生效, 若设置为 `-1` 则表示无限重试

        :param ignore_internet_connection `<'bool'>`: 是否忽略无法链接互联网的错误, 默认为 `False`,

            - 如果设置为 `True`, 则在无法链接互联网时不会抛出异常, 而是会等待
              `ignore_internet_connection_wait` 秒后重试请求, 重试次数不超过 `ignore_internet_connection_retry`
            - 如果设置为 `False`, 则在无法链接互联网时会抛出 `InternetConnectionError` 异常

        :param ignore_internet_connection_wait `<'int/float'>`: 忽略无法链接互联网时的等待时间 (单位: 秒),
            默认为 `10` 秒, 仅在 `ignore_internet_connection` 为 `True` 时生效

        :param ignore_internet_connection_retry `<'int'>`: 忽略无法链接互联网时的最大重试次数,
            默认为 `10`, 仅在 `ignore_internet_connection` 为 `True` 时生效, 若设置为 `-1` 则表示无限重试

        :param echo_retry_warnings `<'bool'>`: 是否在重试请求时打印警告信息, 默认为 `True`
        """
        # 验证参数
        # . API 凭证
        app_cipher = AES.new(app_id.encode("utf-8"), AES.MODE_ECB)
        # . HTTP 会话
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            raise errors.ApiSettingsError(
                "请求超时必须为正整数或浮点数, 而非 %r" % (timeout,)
            )
        timeout: ClientTimeout = ClientTimeout(total=timeout)
        # 错误处理
        # . 请求超时
        ignore_timeout: bool = bool(ignore_timeout)
        if not isinstance(ignore_timeout_wait, (float, int)) or ignore_timeout_wait < 0:
            raise errors.ApiSettingsError(
                "忽略请求超时时的等待时间必须为非负整数或浮点数, 而非 %r"
                % (ignore_timeout_wait,)
            )
        ignore_timeout_wait: float = float(ignore_timeout_wait)
        if not isinstance(ignore_timeout_retry, int) or ignore_timeout_retry < -1:
            raise errors.ApiSettingsError(
                "忽略请求超时时的最大重试次数必须为正整数或 -1, 而非 %r"
                % (ignore_timeout_retry,)
            )
        ignore_timeout_retry: int = ignore_timeout_retry
        # . API 限流
        ignore_api_limit: bool = bool(ignore_api_limit)
        if (
            not isinstance(ignore_api_limit_wait, (float, int))
            or ignore_api_limit_wait < 0
        ):
            raise errors.ApiSettingsError(
                "忽略 API 限流时的等待时间必须为非负整数或浮点数, 而非 %r"
                % (ignore_api_limit_wait,)
            )
        ignore_api_limit_wait: float = float(ignore_api_limit_wait)
        if not isinstance(ignore_api_limit_retry, int) or ignore_api_limit_retry < -1:
            raise errors.ApiSettingsError(
                "忽略 API 限流时的最大重试次数必须为正整数或 -1, 而非 %r"
                % (ignore_api_limit_retry,)
            )
        ignore_api_limit_retry: int = ignore_api_limit_retry
        # . 服务器内部错误 (500错误码, 仅限 Internal Server Error 类型)
        ignore_internal_server_error: bool = bool(ignore_internal_server_error)
        if (
            not isinstance(ignore_internal_server_error_wait, (float, int))
            or ignore_internal_server_error_wait < 0
        ):
            raise errors.ApiSettingsError(
                "忽略服务器内部错误时的等待时间必须为非负整数或浮点数, 而非 %r"
                % (ignore_internal_server_error_wait,)
            )
        ignore_internal_server_error_wait: float = float(
            ignore_internal_server_error_wait
        )
        if (
            not isinstance(ignore_internal_server_error_retry, int)
            or ignore_internal_server_error_retry < -1
        ):
            raise errors.ApiSettingsError(
                "忽略服务器内部错误时的最大重试次数必须为正整数或 -1, 而非 %r"
                % (ignore_internal_server_error_retry,)
            )
        ignore_internal_server_error_retry: int = ignore_internal_server_error_retry
        # . 无法链接互联网
        ignore_internet_connection: bool = bool(ignore_internet_connection)
        if (
            not isinstance(ignore_internet_connection_wait, (float, int))
            or ignore_internet_connection_wait < 0
        ):
            raise errors.ApiSettingsError(
                "忽略无法链接互联网时的等待时间必须为非负整数或浮点数, 而非 %r"
                % (ignore_internet_connection_wait,)
            )
        ignore_internet_connection_wait: float = float(ignore_internet_connection_wait)
        if (
            not isinstance(ignore_internet_connection_retry, int)
            or ignore_internet_connection_retry < -1
        ):
            raise errors.ApiSettingsError(
                "忽略无法链接互联网时的最大重试次数必须为正整数或 -1, 而非 %r"
                % (ignore_internet_connection_retry,)
            )
        ignore_internet_connection_retry: int = ignore_internet_connection_retry
        # 初始化
        kwargs = {
            "app_id": app_id,
            "app_secret": app_secret,
            "app_cipher": app_cipher,
            "timeout": timeout,
            "ignore_timeout": ignore_timeout,
            "ignore_timeout_wait": ignore_timeout_wait,
            "ignore_timeout_retry": ignore_timeout_retry,
            "ignore_api_limit": ignore_api_limit,
            "ignore_api_limit_wait": ignore_api_limit_wait,
            "ignore_api_limit_retry": ignore_api_limit_retry,
            "ignore_internal_server_error": ignore_internal_server_error,
            "ignore_internal_server_error_wait": ignore_internal_server_error_wait,
            "ignore_internal_server_error_retry": ignore_internal_server_error_retry,
            "ignore_internet_connection": ignore_internet_connection,
            "ignore_internet_connection_wait": ignore_internet_connection_wait,
            "ignore_internet_connection_retry": ignore_internet_connection_retry,
            "echo_retry_warnings": bool(echo_retry_warnings),
        }
        super().__init__(**kwargs)
        self._basic: BasicAPI = BasicAPI(**kwargs)
        self._sales: SalesAPI = SalesAPI(**kwargs)
        self._fba: FbaAPI = FbaAPI(**kwargs)
        self._product: ProductAPI = ProductAPI(**kwargs)
        self._purchase: PurchaseAPI = PurchaseAPI(**kwargs)
        self._warehouse: WarehouseAPI = WarehouseAPI(**kwargs)
        self._ads: AdsAPI = AdsAPI(**kwargs)
        self._finance: FinanceAPI = FinanceAPI(**kwargs)
        self._tools: ToolsAPI = ToolsAPI(**kwargs)
        self._source: SourceAPI = SourceAPI(**kwargs)

    # 公共 API --------------------------------------------------------------------------------------
    # . 授权
    async def AccessToken(self) -> schema.Token:
        """获取领星 API 的访问令牌

        ## Docs
        - 授权: [获取 access-token和refresh-token](https://apidoc.lingxing.com/#/docs/Authorization/GetToken)

        :returns `<'Token'>`: 返回接口的访问令牌
        ```python
        {
            # 接口的访问令牌
            "access_token": "your_access_token",
            # 用于续约 access_token 的更新令牌
            "refresh_token": "your_refresh_token",
            # 访问令牌的有效时间 (单位: 秒)
            "expires_in": 3600
        }
        ```
        """
        return await self._AccessToken()

    async def RefreshToken(self, refresh_token: str) -> schema.Token:
        """基于 refresh_token 刷新领星 API 的访问令牌

        ## Docs
        - 授权: [续约接口令牌](https://apidoc.lingxing.com/#/docs/Authorization/RefreshToken)

        :param refresh_token `<'str'>`: 用于续约 refresh_token 的令牌
        :returns `<'Token'>`: 返回接口的访问令牌
        ```python
        {
            # 接口的访问令牌
            "access_token": "your_access_token",
            # 用于续约 access_token 的更新令牌
            "refresh_token": "your_refresh_token",
            # 访问令牌的有效时间 (单位: 秒)
            "expires_in": 3600
        }
        ```
        """
        return await self._RefreshToken(refresh_token)

    # . 基础数据
    @property
    def basic(self) -> BasicAPI:
        """领星API `基础数据` 接口 `<'BasicAPI'>`

        ## Docs
        * 基础数据
            - Marketplaces: [查询亚马逊市场列表](https://apidoc.lingxing.com/#/docs/BasicData/AllMarketplace)
            - States: [查询亚马逊国家下地区列表](https://apidoc.lingxing.com/#/docs/BasicData/WorldStateLists)
            - Sellers: [查询亚马逊店铺列表](https://apidoc.lingxing.com/#/docs/BasicData/SellerLists)
            - ConceptSellers: [查询亚马逊概念店铺列表](https://apidoc.lingxing.com/#/docs/BasicData/ConceptSellerLists)
            - RenameSellers: [批量修改店铺名称](https://apidoc.lingxing.com/#/docs/BasicData/SellerBatchRename)
            - Accounts: [查询ERP用户信息列表](https://apidoc.lingxing.com/#/docs/BasicData/AccoutLists)
            - ExchangeRates: [查询汇率](https://apidoc.lingxing.com/#/docs/BasicData/Currency)
            - UpdateExchangeRate: [修改我的汇率](https://apidoc.lingxing.com/#/docs/BasicData/ExchangeRateUpdate)
        """
        return self._basic

    # . 销售数据
    @property
    def sales(self) -> SalesAPI:
        """领星API `销售数据` 接口 `<'SalesAPI'>`

        ## Docs
        * 销售 - Listing
            - Listings: [查询亚马逊Listing](https://apidoc.lingxing.com/#/docs/Sale/Listing)
            - EditListingOperators: [批量分配Listing负责人](https://apidoc.lingxing.com/#/docs/Sale/UpdatePrincipal)
            - EditListingPrices: [批量修改Listing价格](https://apidoc.lingxing.com/#/docs/Sale/pricingSubmit)
            - PairListingProducts: [批量添加/编辑Listing配对](https://apidoc.lingxing.com/#/docs/Sale/Productlink)
            - UnpairListingProducts: [解除Listing配对](https://apidoc.lingxing.com/#/docs/Sale/UnlinkListing)
            - ListingGlobalTags: [查询Listing标签列表](https://apidoc.lingxing.com/#/docs/Sale/globalTagPageList)
            - CreateListingGlobalTag: [添加Listing标签](https://apidoc.lingxing.com/#/docs/Sale/globalTagAddTag)
            - RemoveListingGlobalTag: [删除Listing标签](https://apidoc.lingxing.com/#/docs/Sale/globalTagRemoveTag)
            - ListingTags: [查询Listing标记标签列表](https://apidoc.lingxing.com/#/docs/Sale/queryListingRelationTagList)
            - SetListingTag: [Listing新增商品标签](https://apidoc.lingxing.com/#/docs/Sale/AddGoodsTag)
            - UnsetListingTag: [Listing删除商品标签](https://apidoc.lingxing.com/#/docs/Sale/DeleteGoodsTag)
            - ListingFbaFees: [批量获取Listing费用](https://apidoc.lingxing.com/#/docs/Sale/GetPrices)
            - EditListingFbms: [修改FBM库存&处理时间](https://apidoc.lingxing.com/#/docs/Sale/UpdateFbmInventory)
            - ListingOperationLogs: [查询Listing操作日志列表](https://apidoc.lingxing.com/#/docs/Sale/listingOperateLogPageList)

        * 销售 - 平台订单
            - Orders: [查询亚马逊订单列表](https://apidoc.lingxing.com/#/docs/Sale/Orderlists)
            - OrderDetails: [查询亚马逊订单详情](https://apidoc.lingxing.com/#/docs/Sale/OrderDetail)
            - EditOrderNote: [SC订单-设置订单备注](https://apidoc.lingxing.com/#/docs/Sale/ScOrderSetRemark)
            - AfterSalesOrders: [查询售后订单列表](https://apidoc.lingxing.com/#/docs/Sale/afterSaleList)
            - McfOrders: [查询亚马逊多渠道订单列表-v2](https://apidoc.lingxing.com/#/docs/Sale/OrderMCFOrders)
            - McfOrderDetails: [查询亚马逊多渠道订单详情-商品信息](https://apidoc.lingxing.com/#/docs/Sale/ProductInformation)
            - McfOrderLogistics: [查询亚马逊多渠道订单详情-物流信息](https://apidoc.lingxing.com/#/docs/Sale/LogisticsInformation)
            - McfAfterSalesOrders: [查询亚马逊多渠道订单详情-退货换货信息](https://apidoc.lingxing.com/#/docs/Sale/ReturnInfomation)
            - McfOrderTransaction: [多渠道订单-交易明细](https://apidoc.lingxing.com/#/docs/Sale/MutilChannelTransactionDetail)

        * 销售 - 自发货管理
            - FbmOrders: [查询亚马逊自发货订单列表](https://apidoc.lingxing.com/#/docs/Sale/FBMOrderList)
            - FbmOrderDetail: [查询亚马逊自发货订单详情](https://apidoc.lingxing.com/#/docs/Sale/FBMOrderDetail)

        * 销售 - 促销管理
            - PromotionCoupons: [查询促销活动列表-优惠券](https://apidoc.lingxing.com/#/docs/Sale/promotionalActivitiesCouponList)
            - PromotionDeals: [查询促销活动列表-秒杀](https://apidoc.lingxing.com/#/docs/Sale/promotionalActivitiesSecKillList)
            - PromotionActivities: [查询促销活动列表-管理促销](https://apidoc.lingxing.com/#/docs/Sale/promotionalActivitiesManageList)
            - PromotionDiscounts: [查询促销活动列表-会员折扣](https://apidoc.lingxing.com/#/docs/Sale/promotionalActivitiesVipDiscountList)
            - PromotionOnListings: [查询商品折扣列表](https://apidoc.lingxing.com/#/docs/Sale/promotionListingList)
        """
        return self._sales

    # . FBA数据
    @property
    def fba(self) -> FbaAPI:
        """领星API `FBA数据` 接口 `<'FbaAPI'>`

        ## Docs
        * FBA - FBA货件 (STA)
            - StaPlans: [查询STA任务列表](https://apidoc.lingxing.com/#/docs/FBA/QuerySTATaskList)
            - StaPlanDetail: [查询STA任务详情](https://apidoc.lingxing.com/#/docs/FBA/StaTaskDetail)
            - PackingGroups: [查询包装组](https://apidoc.lingxing.com/#/docs/FBA/ListPackingGroupItems)
            - PackingGroupBoxes: [查询STA任务包装组装箱信息](https://apidoc.lingxing.com/#/docs/FBA/QuerySTATaskBoxInformation)
            - PlacementOptions: [查询货件方案](https://apidoc.lingxing.com/#/docs/FBA/ShipmentPreView)
            - PlacementOptionBoxes: [查询货件方案的装箱信息](https://apidoc.lingxing.com/#/docs/FBA/getInboundPackingBoxInfo)
            - Shipments: [查询货件列表](https://apidoc.lingxing.com/#/docs/FBA/FBAShipmentList)
            - ShipmentDetails: [查询货件详情](https://apidoc.lingxing.com/#/docs/FBA/ShipmentDetailList)
            - ShipmentBoxes: [查询货件装箱信息](https://apidoc.lingxing.com/#/docs/FBA/ListShipmentBoxes)
            - ShipmentTransports: [查询承运方式](https://apidoc.lingxing.com/#/docs/FBA/GetTransportList)
            - ShipmentReceiptRecords: [查询FBA到货接收明细](https://apidoc.lingxing.com/#/docs/FBA/FBAReceivedInventory)
            - ShipmentDeliveryAddress: [地址簿-配送地址详情](https://apidoc.lingxing.com/#/docs/FBA/ShoppingAddress)
            - ShipFromAddresses: [地址簿-发货地址列表](https://apidoc.lingxing.com/#/docs/FBA/ShipFromAddressList)
        """
        return self._fba

    # . 产品数据
    @property
    def product(self) -> ProductAPI:
        """领星API `产品数据` 接口 `<'ProductAPI'>`

        ## Docs
        * 产品
            - Products: [查询本地产品列表](https://apidoc.lingxing.com/#/docs/Product/ProductLists)
            - ProductDetails: [批量查询本地产品详情](https://apidoc.lingxing.com/#/docs/Product/batchGetProductInfo)
            - EnableProducts: [产品启用、禁用](https://apidoc.lingxing.com/#/docs/Product/productOperateBatch)
            - DisableProducts: [产品启用、禁用](https://apidoc.lingxing.com/#/docs/Product/productOperateBatch)
            - EditProduct: [添加/编辑本地产品](https://apidoc.lingxing.com/#/docs/Product/SetProduct)
            - SpuProducts: [查询多属性产品列表](https://apidoc.lingxing.com/#/docs/Product/spuList)
            - SpuProductDetail: [查询多属性产品详情](https://apidoc.lingxing.com/#/docs/Product/spuInfo)
            - EditSpuProduct: [添加/编辑多属性产品](https://apidoc.lingxing.com/#/docs/Product/spuSet)
            - BundleProducts: [查询捆绑产品关系列表](https://apidoc.lingxing.com/#/docs/Product/bundledProductList)
            - EditBundleProduct: [添加/编辑捆绑产品](https://apidoc.lingxing.com/#/docs/Product/SetBundled)
            - AuxiliaryMaterials: [查询产品辅料列表](https://apidoc.lingxing.com/#/docs/Product/productAuxList)
            - EditAuxiliaryMaterial: [添加/编辑辅料](https://apidoc.lingxing.com/#/docs/Product/setAux)
            - ProductCodes: [获取UPC编码列表](https://apidoc.lingxing.com/#/docs/Product/UpcList)
            - CreateProductCode: [创建UPC编码](https://apidoc.lingxing.com/#/docs/Product/AddCommodityCode)
            - ProductGlobalTags: [查询产品标签](https://apidoc.lingxing.com/#/docs/Product/GetProductTag)
            - CreateProductGlobalTag: [创建产品标签](https://apidoc.lingxing.com/#/docs/Product/CreateProductTag)
            - SetProductTag: [标记产品标签](https://apidoc.lingxing.com/#/docs/Product/SetProductTag)
            - UnsetProductTag: [删除产品标签](https://apidoc.lingxing.com/#/docs/Product/DelProductTag)
            - ProductGlobalAttributes: [查询产品属性列表](https://apidoc.lingxing.com/#/docs/Product/attributeList)
            - EditProductGlobalAttribute: [添加/编辑产品属性](https://apidoc.lingxing.com/#/docs/Product/attributeSet)
            - ProductBrands: [查询产品品牌列表](https://apidoc.lingxing.com/#/docs/Product/productBrandList)
            - EditProductBrands: [添加/编辑产品品牌](https://apidoc.lingxing.com/#/docs/Product/SetBrand)
            - ProductCategories: [查询产品分类列表](https://apidoc.lingxing.com/#/docs/Product/Category)
            - EditProductCategories: [添加/编辑产品分类](https://apidoc.lingxing.com/#/docs/Product/SetCategory)
        """
        return self._product

    # . 采购数据
    @property
    def purchase(self) -> PurchaseAPI:
        """领星API `采购数据` 接口 `<'PurchaseAPI'>`

        ## Docs
        * 采购
            - Suppliers: [查询供应商列表](https://apidoc.lingxing.com/#/docs/Purchase/Supplier)
            - EditSupplier: [添加/修改供应商](https://apidoc.lingxing.com/#/docs/Purchase/SupplierEdit)
            - Purchasers: [查询采购方列表](https://apidoc.lingxing.com/#/docs/Purchase/Purchaser)
            - PurchasePlans: [查询采购计划列表](https://apidoc.lingxing.com/#/docs/Purchase/getPurchasePlans)
        """
        return self._purchase

    # . 仓库数据
    @property
    def warehouse(self) -> WarehouseAPI:
        """领星API `仓库数据` 接口 `<'WarehouseAPI'>`

        ## Docs
        * 仓库 - 仓库设置
            - Warehouses: [查询仓库列表](https://apidoc.lingxing.com/#/docs/Warehouse/WarehouseLists)
            - WarehouseBins: [查询本地仓位列表](https://apidoc.lingxing.com/#/docs/Warehouse/warehouseBin)

        * 仓库 - 库存&流水
            - FbaInventory: [查询FBA库存列表](https://apidoc.lingxing.com/#/docs/Warehouse/FBAStock)
            - FbaInventoryDetails: [查询FBA库存列表-v2](https://apidoc.lingxing.com/#/docs/Warehouse/FBAStockDetail)
            - AwdInventory: [查询AWD库存列表](https://apidoc.lingxing.com/#/docs/Warehouse/AwdWarehouseDetail)
            - SellerInventory: [查询仓库库存明细](https://apidoc.lingxing.com/#/docs/Warehouse/InventoryDetails)
            - SellerInventoryBins: [查询仓位库存明细](https://apidoc.lingxing.com/#/docs/Warehouse/inventoryBinDetails)
            - SellerInventoryBatches: [查询批次明细](https://apidoc.lingxing.com/#/docs/Warehouse/GetBatchDetailList)
            - SellerInventoryRecords: [查询批次流水](https://apidoc.lingxing.com/#/docs/Warehouse/GetBatchStatementList)
            - SellerInventoryOperations: [查询库存流水(新)](https://apidoc.lingxing.com/#/docs/Warehouse/WarehouseStatementNew)
            - SellerInventoryBinRecords: [查询仓位流水](https://apidoc.lingxing.com/#/docs/Warehouse/wareHouseBinStatement)
        """
        return self._warehouse

    # . 广告数据
    @property
    def ads(self) -> AdsAPI:
        """领星API `广告数据` 接口 `<'AdsAPI'>`

        ## Docs
        * 新广告 - 基础数据
            - AdProfiles: [查询广告账号列表](https://apidoc.lingxing.com/#/docs/newAd/baseData/dspAccountList)
            - Portfolios: [广告组合](https://apidoc.lingxing.com/#/docs/newAd/baseData/portfolios)
            - SpCampaigns: [SP广告活动](https://apidoc.lingxing.com/#/docs/newAd/baseData/spCampaigns)
            - SpAdGroups: [SP广告组](https://apidoc.lingxing.com/#/docs/newAd/baseData/spAdGroups)
            - SpProducts: [SP广告商品](https://apidoc.lingxing.com/#/docs/newAd/baseData/spProductAds)
            - SpKeywords: [SP关键词](https://apidoc.lingxing.com/#/docs/newAd/baseData/spKeywords)
            - SpTargets: [SP商品定位](https://apidoc.lingxing.com/#/docs/newAd/baseData/spTargets)
            - SpNegativeKeywords: [SP否定投放(keyword)](https://apidoc.lingxing.com/#/docs/newAd/baseData/spNegativeTargetsOrKeywords)
            - SpNegativeTargets: [SP否定投放(target)](https://apidoc.lingxing.com/#/docs/newAd/baseData/spNegativeTargetsOrKeywords)
            - SbCampaigns: [SB广告活动](https://apidoc.lingxing.com/#/docs/newAd/baseData/hsaCampaigns)
            - SbAdGroups: [SB广告组](https://apidoc.lingxing.com/#/docs/newAd/baseData/hsaAdGroups)
            - SbCreatives: [SB广告创意](https://apidoc.lingxing.com/#/docs/newAd/baseData/sbAdHasProductAds)
            - SbKeywords: [SB广告的投放(keyword)](https://apidoc.lingxing.com/#/docs/newAd/baseData/sbTargeting)
            - SbTargets: [SB广告的投放](https://apidoc.lingxing.com/#/docs/newAd/baseData/sbTargeting)
            - SbNegativeKeywords: [SB否定关键词](https://apidoc.lingxing.com/#/docs/newAd/baseData/hsaNegativeKeywords)
            - SbNegativeTargets: [SB否定商品投放](https://apidoc.lingxing.com/#/docs/newAd/baseData/hsaNegativeTargets)
            - SdCampaigns: [SD广告活动](https://apidoc.lingxing.com/#/docs/newAd/baseData/sdCampaigns)
            - SdAdGroups: [SD广告组](https://apidoc.lingxing.com/#/docs/newAd/baseData/sdAdGroups)
            - SdProducts: [SD广告商品](https://apidoc.lingxing.com/#/docs/newAd/baseData/sdProductAds)
            - SdTargets: [SD商品定位](https://apidoc.lingxing.com/#/docs/newAd/baseData/sdTargets)
            - SdNegativeTargets: [SD否定商品定位](https://apidoc.lingxing.com/#/docs/newAd/baseData/sdNegativeTargets)

        * 新广告 - 报告
            - SpCampaignReports: [SP广告活动报表](https://apidoc.lingxing.com/#/docs/newAd/report/spCampaignReports)
            - SpCampaignHourData: [SP广告活动小时数据](https://apidoc.lingxing.com/#/docs/newAd/report/spCampaignHourData)
            - SpPlacementReports: [SP广告位报告](https://apidoc.lingxing.com/#/docs/newAd/report/campaignPlacementReports)
            - SpPlacementHourData: [SP广告位小时数据](https://apidoc.lingxing.com/#/docs/newAd/report/spAdPlacementHourData)
            - SpAdGroupReports: [SP广告组报表](https://apidoc.lingxing.com/#/docs/newAd/report/spAdGroupReports)
            - SpAdGroupHourData: [SP广告组小时数据](https://apidoc.lingxing.com/#/docs/newAd/report/spAdGroupHourData)
            - SpProductReports: [SP广告商品报表](https://apidoc.lingxing.com/#/docs/newAd/report/spProductAdReports)
            - SpProductHourData: [SP广告小时数据(ad)](https://apidoc.lingxing.com/#/docs/newAd/report/spTargetHourData)
            - SpKeywordReports: [SP关键词报表](https://apidoc.lingxing.com/#/docs/newAd/report/spKeywordReports)
            - SpKeywordHourData: [SP广告小时数据(both_ad_target)](https://apidoc.lingxing.com/#/docs/newAd/report/spTargetHourData)
            - SpTargetReports: [SP商品定位报表](https://apidoc.lingxing.com/#/docs/newAd/report/spTargetReports)
            - SpTargetHourData: [SP投放小时数据(both_ad_target)](https://apidoc.lingxing.com/#/docs/newAd/report/spTargetHourData)
            - SpQueryWordReports: [SP用户搜索词报表](https://apidoc.lingxing.com/#/docs/newAd/report/queryWordReports)
            - SbCampaignReports: [SB广告活动报表](https://apidoc.lingxing.com/#/docs/newAd/report/hsaCampaignReports)
            - SbCampaignHourData: [SB广告活动小时数据](https://apidoc.lingxing.com/#/docs/newAd/report/sbCampaignHourData)
            - SbPlacementReports: [SB广告活动-广告位报告](https://apidoc.lingxing.com/#/docs/newAd/report/hsaCampaignPlacementReports)
            - SbPlacementHourData: [SB广告位小时数据](https://apidoc.lingxing.com/#/docs/newAd/report/sbAdPlacementHourData)
            - SbAdGroupReports: [SB广告组报表](https://apidoc.lingxing.com/#/docs/newAd/report/hsaAdGroupReports)
            - SbAdGroupHourData: [SB广告组小时数据](https://apidoc.lingxing.com/#/docs/newAd/report/sbAdGroupHourData)
            - SbCreativeReports: [SB广告创意报告](https://apidoc.lingxing.com/#/docs/newAd/report/listHsaProductAdReport)
            - SbKeywordReports: [SB广告的投放报告(keyword)](https://apidoc.lingxing.com/#/docs/newAd/report/listHsaTargetingReport)
            - SbTargetReports: [SB广告的投放报告(product)](https://apidoc.lingxing.com/#/docs/newAd/report/listHsaTargetingReport)
            - SbTargetingHourData: [SB投放小时数据](https://apidoc.lingxing.com/#/docs/newAd/report/sbTargetHourData)
            - SbQueryWordReports: [SB用户搜索词报表](https://apidoc.lingxing.com/#/docs/newAd/report/hsaQueryWordReports)
            - SbAsinAttributionReports: [SB广告归因于广告的购买报告](https://apidoc.lingxing.com/#/docs/newAd/report/hsaPurchasedAsinReports)
            - SbCostAllocationReports: [SB分摊](https://apidoc.lingxing.com/#/docs/newAd/baseData/newadsbDivideAsinReports)
            - SdCampaignReports: [SD广告活动报表](https://apidoc.lingxing.com/#/docs/newAd/report/sdCampaignReports)
            - SdCampaignHourData: [SD广告活动小时数据](https://apidoc.lingxing.com/#/docs/newAd/report/sdCampaignHourData)
            - SdAdGroupReports: [SD广告组报表](https://apidoc.lingxing.com/#/docs/newAd/report/sdAdGroupReports)
            - SdAdGroupHourData: [SD广告组小时数据](https://apidoc.lingxing.com/#/docs/newAd/report/sdAdGroupHourData)
            - SdProductReports: [SD广告商品报表](https://apidoc.lingxing.com/#/docs/newAd/report/sdProductAdReports)
            - SdProductHourData: [SD广告小时数据(ad)](https://apidoc.lingxing.com/#/docs/newAd/report/sdAdvertiseHourData)
            - SdTargetReports: [SD商品定位报表](https://apidoc.lingxing.com/#/docs/newAd/report/sdTargetReports)
            - SdTargetHourData: [SD投放小时数据(both_ad_target)](https://apidoc.lingxing.com/#/docs/newAd/report/sdTargetHourData)
            - SdMatchedTargetReports: [SD匹配的目标报表](https://apidoc.lingxing.com/#/docs/newAd/report/sdMatchTargetReports)
            - DspReports: [查询DSP报告列表-订单](https://apidoc.lingxing.com/#/docs/newAd/report/dspReportOrderList)

        * 新广告 - 报表下载
            - DownloadAbaReport: [ABA搜索词报告-按周维度](https://apidoc.lingxing.com/#/docs/newAd/reportDownload/abaReport)

        * 新广告
            - AdsOperationLogs: [操作日志(新）](https://apidoc.lingxing.com/#/docs/newAd/apiLogStandard)
        """
        return self._ads

    # . 财务数据
    @property
    def finance(self) -> FinanceAPI:
        """领星API `财务数据` 接口 `<'FinanceAPI'>`

        ## Docs
        * 财务
            - UserFeeTypes: [查询费用类型列表](https://apidoc.lingxing.com/#/docs/Finance/feeManagementType)
            - Transactions: [查询结算中心-交易明细](https://apidoc.lingxing.com/#/docs/Finance/settlementTransactionList)
            - Settlements: [查询结算中心-结算汇总](https://apidoc.lingxing.com/#/docs/Finance/settlementSummaryList)
            - ShipmentSettlements: [查询发货结算报告](https://apidoc.lingxing.com/#/docs/Finance/SettlementReport)
            - Receivables: [应收报告-列表查询](https://apidoc.lingxing.com/#/docs/Finance/receivableReportList)
            - LedgerDetail: [查询库存分类账detail数据](https://apidoc.lingxing.com/#/docs/Finance/centerOdsDetailQuery)
            - LedgerSummary: [查询库存分类账summary数据](https://apidoc.lingxing.com/#/docs/Finance/summaryQuery)
            - LedgerValuation: [查询FBA成本计价流水](https://apidoc.lingxing.com/#/docs/Finance/CostStream)
            - AdsInvoices: [查询广告发票列表](https://apidoc.lingxing.com/#/docs/Finance/InvoiceList)
            - AdsInvoiceDetail: [查询广告发票基本信息](https://apidoc.lingxing.com/#/docs/Finance/InvoiceDetail)
            - AdsCampaignInvoices: [查询广告发票活动列表](https://apidoc.lingxing.com/#/docs/Finance/InvoiceCampaignList)
            - IncomeStatementSellers: [查询利润报表-店铺](https://apidoc.lingxing.com/#/docs/Finance/bdSeller)
            - IncomeStatementAsins: [查询利润报表-ASIN](https://apidoc.lingxing.com/#/docs/Finance/bdASIN)
            - IncomeStatementParentAsins: [查询利润报表-父ASIN](https://apidoc.lingxing.com/#/docs/Finance/bdParentASIN)
            - IncomeStatementMskus: [查询利润报表-MSKU](https://apidoc.lingxing.com/#/docs/Finance/bdMSKU)
            - IncomeStatementLskus: [查询利润报表-SKU](https://apidoc.lingxing.com/#/docs/Finance/bdSKU)
        """
        return self._finance

    # . 工具数据
    @property
    def tools(self) -> ToolsAPI:
        """领星API `工具数据` 接口 `<'ToolsAPI'>`

        ## Docs
        * 工具
            - MonitorKeywords: [关键词列表](https://apidoc.lingxing.com/#/docs/Tools/GetKeywordList)
            - MonitorAsins: [查询竞品监控列表](https://apidoc.lingxing.com/#/docs/Tools/CompetitiveMonitorList)
        """
        return self._tools

    # . 亚马逊源数据
    @property
    def source(self) -> SourceAPI:
        """领星API `亚马逊源数据` 接口 `<'SourceAPI'>`

        ## Docs
        * 订单数据
            - Orders: [查询亚马逊源报表-所有订单](https://apidoc.lingxing.com/#/docs/SourceData/AllOrders)
            - FbaOrders: [查询亚马逊源报表-FBA订单](https://apidoc.lingxing.com/#/docs/SourceData/FbaOrders)
            - FbaReplacementOrders: [查询亚马逊源报表-FBA换货订单](https://apidoc.lingxing.com/#/docs/SourceData/fbaExchangeOrderList)
            - FbaReturnOrders: [查询亚马逊源报表-FBA退货订单](https://apidoc.lingxing.com/#/docs/SourceData/RefundOrders)
            - FbaShipments: [查询亚马逊源报表—Amazon Fulfilled Shipments](https://apidoc.lingxing.com/#/docs/SourceData/getAmazonFulfilledShipmentsList)
            - FbmReturnOrders: [查询亚马逊源报表-FBM退货订单](https://apidoc.lingxing.com/#/docs/SourceData/fbmReturnOrderList)
            - FbaRemovalOrders: [查询亚马逊源报表-移除订单(新）](https://apidoc.lingxing.com/#/docs/SourceData/RemovalOrderListNew)
            - FbaRemovalShipments: [查询亚马逊源报表-移除货件(新）](https://apidoc.lingxing.com/#/docs/SourceData/RemovalShipmentList)
            - FbaInventory: [查询亚马逊源报表-FBA库存](https://apidoc.lingxing.com/#/docs/SourceData/ManageInventory)
            - FbaReservedInventory: [查询亚马逊源报表-预留库存](https://apidoc.lingxing.com/#/docs/SourceData/ReservedInventory)
            - FbaInventoryHealth: [查询亚马逊源报表—库龄表](https://apidoc.lingxing.com/#/docs/SourceData/getFbaAgeList)
            - FbaInventoryAdjustments: [查询亚马逊源报表-盘存记录](https://apidoc.lingxing.com/#/docs/SourceData/AdjustmentList)
            - ExportReportTask: [报告导出 - 创建导出任务](https://apidoc.lingxing.com/#/docs/Statistics/reportCreateReportExportTask)
            - ExportReportResult: [报告导出-查询导出任务结果](https://apidoc.lingxing.com/#/docs/Statistics/reportQueryReportExportTask)
            - ExportReportRefresh: [报告导出 - 报告下载链接续期](https://apidoc.lingxing.com/#/docs/Statistics/AmazonReportExportTask)
        """
        return self._source
