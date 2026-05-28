# -*- coding: utf-8 -*-

# fmt: off
# 销售 - Listing ----------------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/Sale/Listing
LISTINGS: str = "/erp/sc/data/mws/listing"
# https://apidoc.lingxing.com/#/docs/Sale/UpdatePrincipal
EDIT_LISTING_OPERATORS: str = "/listing/listing/open/api/asin/updatePrincipal"
# https://apidoc.lingxing.com/#/docs/Sale/pricingSubmit
EDIT_LISTING_PRICES: str = "/erp/sc/listing/ProductPricing/pricingSubmit"
# https://apidoc.lingxing.com/#/docs/Sale/Productlink
PAIR_LISTING_PRODUCTS: str = "/erp/sc/storage/product/link"
# https://apidoc.lingxing.com/#/docs/Sale/UnlinkListing
UNPAIR_LISTING_PRODUCTS: str = "/basicOpen/listingManage/unLinkListingPairs"
# https://apidoc.lingxing.com/#/docs/Sale/globalTagPageList
LISTING_GLOBAL_TAGS: str = "/basicOpen/globalTag/listing/page/list"
# https://apidoc.lingxing.com/#/docs/Sale/globalTagAddTag
CREATE_LISTING_GLOBAL_TAG: str = "/basicOpen/globalTag/listing/addTag"
# https://apidoc.lingxing.com/#/docs/Sale/globalTagRemoveTag
REMOVE_LISTING_GLOBAL_TAG: str = "/basicOpen/globalTag/listing/removeTag"
# https://apidoc.lingxing.com/#/docs/Sale/queryListingRelationTagList
LISTING_TAGS: str = "/basicOpen/listingManage/queryListingRelationTagList"
# https://apidoc.lingxing.com/#/docs/Sale/AddGoodsTag
SET_LISTING_TAG: str = "/basicOpen/listingManage/bindListingAndTag"
# https://apidoc.lingxing.com/#/docs/Sale/DeleteGoodsTag
UNSET_LISTING_TAG: str = "/basicOpen/listingManage/removeListingAndTag"
# https://apidoc.lingxing.com/#/docs/Sale/GetPrices
LISTING_FBA_FEES: str = "/listing/listing/open/api/listing/getPrices"
# https://apidoc.lingxing.com/#/docs/Sale/UpdateFbmInventory
EDIT_LISTING_FBMS: str = "/basicOpen/FbmManagement/modifyFbmInventory"
# https://apidoc.lingxing.com/#/docs/Sale/listingOperateLogPageList
LISTING_OPERATION_LOGS: str = "/basicOpen/listingManage/listingOperateLog/pageList"

# 销售 - 刊登管理 ----------------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/Sale/PublishManageCategoryRoot
AMAZON_ROOT_CATEGORIES: str = "/basicOpen/openapi/publish/manage/categoryRoot"
# https://apidoc.lingxing.com/#/docs/Sale/PublishManageCategoryChildren
AMAZON_CHILD_CATEGORIES: str = "/basicOpen/openapi/publish/manage/categoryChildren"

# 销售 - 平台订单 ----------------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/Sale/Orderlists
ORDERS: str = "/erp/sc/data/mws/orders"
# https://apidoc.lingxing.com/#/docs/Sale/OrderDetail
ORDER_DETAILS: str = "/erp/sc/data/mws/orderDetail"
# https://apidoc.lingxing.com/#/docs/Sale/ScOrderSetRemark
EDIT_ORDER_NOTE: str = "/basicOpen/platformOrder/scOrder/setRemark"
# https://apidoc.lingxing.com/#/docs/Sale/afterSaleList
AFTER_SALES_ORDERS: str = "/erp/sc/routing/amzod/order/afterSaleList"
# https://apidoc.lingxing.com/#/docs/Sale/MCFOrderList
MCF_ORDERS: str = "/order/amzod/api/orderList"
# https://apidoc.lingxing.com/#/docs/Sale/ProductInformation
MCF_ORDER_DETAILS: str = "/order/amzod/api/orderDetails/productInformation"
# https://apidoc.lingxing.com/#/docs/Sale/LogisticsInformation
MCF_ORDER_LOGISTICS: str = "/order/amzod/api/orderDetails/logisticsInformation"
# https://apidoc.lingxing.com/#/docs/Sale/ReturnInfomation
MCF_AFTER_SALES_ORDERS: str = "/order/amzod/api/orderDetails/returnInformation"
# https://apidoc.lingxing.com/#/docs/Sale/MutilChannelTransactionDetail
MCF_ORDER_TRANSACTION: str = "/basicOpen/openapi/salesOrder/multi-channel/list/transaction"

# 销售 - 自发货管理 --------------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/Sale/FBMOrderList
FBM_ORDERS: str = "/erp/sc/routing/order/Order/getOrderList"
# https://apidoc.lingxing.com/#/docs/Sale/FBMOrderDetail
FBM_ORDER_DETAIL: str = "/erp/sc/routing/order/Order/getOrderDetail"

# 销售 - 促销管理 ----------------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/Sale/promotionalActivitiesCouponList
PROMOTION_COUPONS: str = "/basicOpen/promotionalActivities/coupon/list"
# https://apidoc.lingxing.com/#/docs/Sale/promotionalActivitiesSecKillList
PROMOTION_DEALS: str = "/basicOpen/promotionalActivities/secKill/list"
# https://apidoc.lingxing.com/#/docs/Sale/promotionalActivitiesManageList
PROMOTION_ACTIVITIES: str = "/basicOpen/promotionalActivities/manage/list"
# https://apidoc.lingxing.com/#/docs/Sale/promotionalActivitiesVipDiscountList
PROMOTION_DISCOUNTS: str = "/basicOpen/promotionalActivities/vipDiscount/list"
# https://apidoc.lingxing.com/#/docs/Sale/promotionListingList
PROMOTION_ON_LISTINGS: str = "/basicOpen/promotion/listingList"
