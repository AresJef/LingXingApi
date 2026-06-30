# -*- coding: utf-8 -*-

# fmt: off
# 基础数据 ----------------------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/newAd/baseData/dspAccountList
AD_PROFILES: str = "/basicOpen/baseData/account/list"
# https://apidoc.lingxing.com/#/docs/newAd/baseData/portfolios
PORTFOLIOS: str = "/pb/openapi/newad/portfolios"

# . 基础数据 - Sponsored Products
# https://apidoc.lingxing.com/#/docs/newAd/baseData/spCampaigns
SP_CAMPAIGNS: str = "/pb/openapi/newad/spCampaigns"
# https://apidoc.lingxing.com/#/docs/newAd/baseData/spAdGroups
SP_AD_GROUPS: str = "/pb/openapi/newad/spAdGroups"
# https://apidoc.lingxing.com/#/docs/newAd/baseData/spProductAds
SP_PRODUCTS: str = "/pb/openapi/newad/spProductAds"
# https://apidoc.lingxing.com/#/docs/newAd/baseData/spKeywords
SP_KEYWORDS: str = "/pb/openapi/newad/spKeywords"
# https://apidoc.lingxing.com/#/docs/newAd/baseData/spTargets
SP_TARGETS: str = "/pb/openapi/newad/spTargets"
# https://apidoc.lingxing.com/#/docs/newAd/baseData/spNegativeTargetsOrKeywords
SP_NEGATIVE_TARGETING: str = "/pb/openapi/newad/spNegativeTargetsOrKeywords"

# . 基础数据 - Sponsored Brands
# https://apidoc.lingxing.com/#/docs/newAd/baseData/hsaCampaigns
SB_CAMPAIGNS: str = "/pb/openapi/newad/hsaCampaigns"
# https://apidoc.lingxing.com/#/docs/newAd/baseData/hsaAdGroups
SB_AD_GROUPS: str = "/pb/openapi/newad/hsaAdGroups"
# https://apidoc.lingxing.com/#/docs/newAd/baseData/sbAdHasProductAds
SB_CREATIVES: str = "/pb/openapi/newad/hsaProductAds"
# https://apidoc.lingxing.com/#/docs/newAd/baseData/sbTargeting
SB_TARGETING: str = "/pb/openapi/newad/sbTargeting"
# https://apidoc.lingxing.com/#/docs/newAd/baseData/hsaNegativeKeywords
SB_NEGATIVE_KEYWORDS: str = "/pb/openapi/newad/hsaNegativeKeywords"
# https://apidoc.lingxing.com/#/docs/newAd/baseData/hsaNegativeTargets
SB_NEGATIVE_TARGETS: str = "/pb/openapi/newad/hsaNegativeTargets"

# . 基础数据 - Sponsored Display
# https://apidoc.lingxing.com/#/docs/newAd/baseData/sdCampaigns
SD_CAMPAIGNS: str = "/pb/openapi/newad/sdCampaigns"
# https://apidoc.lingxing.com/#/docs/newAd/baseData/sdAdGroups
SD_AD_GROUPS: str = "/pb/openapi/newad/sdAdGroups"
# https://apidoc.lingxing.com/#/docs/newAd/baseData/sdProductAds
SD_PRODUCTS: str = "/pb/openapi/newad/sdProductAds"
# https://apidoc.lingxing.com/#/docs/newAd/baseData/sdTargets
SD_TARGETS: str = "/pb/openapi/newad/sdTargets"
# https://apidoc.lingxing.com/#/docs/newAd/baseData/sdNegativeTargets
SD_NEGATIVE_TARGETS: str = "/pb/openapi/newad/sdNegativeTargets"

# 报告 -------------------------------------------------------------------------------------------------------------------------
# . 报告 - Sponsored Products
# https://apidoc.lingxing.com/#/docs/newAd/report/spCampaignReports
SP_CAMPAIGN_REPORTS: str = "/pb/openapi/newad/spCampaignReports"
# https://apidoc.lingxing.com/#/docs/newAd/report/spCampaignHourData
SP_CAMPAIGN_HOUR_DATA: str = "/pb/openapi/newad/spCampaignHourData"
# https://apidoc.lingxing.com/#/docs/newAd/report/campaignPlacementReports
SP_PLACEMENT_REPORTS: str = "/pb/openapi/newad/campaignPlacementReports"
# https://apidoc.lingxing.com/#/docs/newAd/report/spAdPlacementHourData
SP_PLACEMENT_HOUR_DATA: str = "/pb/openapi/newad/spAdPlacementHourData"
# https://apidoc.lingxing.com/#/docs/newAd/report/spAdGroupReports
SP_AD_GROUP_REPORTS: str = "/pb/openapi/newad/spAdGroupReports"
# https://apidoc.lingxing.com/#/docs/newAd/report/spAdGroupHourData
SP_AD_GROUP_HOUR_DATA: str = "/pb/openapi/newad/spAdGroupHourData"
# https://apidoc.lingxing.com/#/docs/newAd/report/spProductAdReports
SP_PRODUCT_REPORTS: str = "/pb/openapi/newad/spProductAdReports"
# https://apidoc.lingxing.com/#/docs/newAd/report/spAdvertiseHourData
SP_PRODUCT_KEYWORD_HOUR_DATA: str = "/pb/openapi/newad/spAdvertiseHourData"
# https://apidoc.lingxing.com/#/docs/newAd/report/spKeywordReports
SP_KEYWORD_REPORTS: str = "/pb/openapi/newad/spKeywordReports"
# https://apidoc.lingxing.com/#/docs/newAd/report/spTargetReports
SP_TARGET_REPORTS: str = "/pb/openapi/newad/spTargetReports"
# https://apidoc.lingxing.com/#/docs/newAd/report/spTargetHourData
SP_TARGET_HOUR_DATA: str = "/pb/openapi/newad/spTargetHourData"
# https://apidoc.lingxing.com/#/docs/newAd/report/queryWordReports
SP_QUERY_REPORTS: str = "/pb/openapi/newad/queryWordReports"

# . 报告 - Sponsored Brands
# https://apidoc.lingxing.com/#/docs/newAd/report/hsaCampaignReports
SB_CAMPAIGN_REPORTS: str = "/pb/openapi/newad/hsaCampaignReports"
# https://apidoc.lingxing.com/#/docs/newAd/report/sbCampaignHourData
SB_CAMPAIGN_HOUR_DATA: str = "/pb/openapi/newad/sbCampaignHourData"
# https://apidoc.lingxing.com/#/docs/newAd/report/hsaCampaignPlacementReports
SB_PLACEMENT_REPORTS: str = "/pb/openapi/newad/hsaCampaignPlacementReports"
# https://apidoc.lingxing.com/#/docs/newAd/report/sbAdPlacementHourData
SB_PLACEMENT_HOUR_DATA: str = "/pb/openapi/newad/sbAdPlacementHourData"
# https://apidoc.lingxing.com/#/docs/newAd/report/hsaAdGroupReports
SB_AD_GROUP_REPORTS: str = "/pb/openapi/newad/hsaAdGroupReports"
# https://apidoc.lingxing.com/#/docs/newAd/report/sbAdGroupHourData
SB_AD_GROUP_HOUR_DATA: str = "/pb/openapi/newad/sbAdGroupHourData"
# https://apidoc.lingxing.com/#/docs/newAd/report/listHsaProductAdReport
SB_CREATIVE_REPORTS: str = "/pb/openapi/newad/listHsaProductAdReport"
# https://apidoc.lingxing.com/#/docs/newAd/report/listHsaTargetingReport
SB_TARGETING_REPORTS: str = "/pb/openapi/newad/listHsaTargetingReport"
# https://apidoc.lingxing.com/#/docs/newAd/report/hsaQueryWordReports
SB_QUERY_REPORTS: str = "/pb/openapi/newad/hsaQueryWordReports"
# https://apidoc.lingxing.com/#/docs/newAd/report/sbTargetHourData
SB_TARGETING_HOUR_DATA: str = "/pb/openapi/newad/sbTargetHourData"
# https://apidoc.lingxing.com/#/docs/newAd/report/listHsaKeywordPlacementReport
SB_KEYWORD_PLACEMENT_REPORTS: str = "/pb/openapi/newad/listHsaKeywordPlacementReport"
# https://apidoc.lingxing.com/#/docs/newAd/report/hsaPurchasedAsinReports
SB_ASIN_ATTRIBUTION_REPORTS: str = "/pb/openapi/newad/hsaPurchasedAsinReports"
# https://apidoc.lingxing.com/#/docs/newAd/baseData/newadsbDivideAsinReports
SB_COST_ALLOCATION_REPORTS: str = "/pb/openapi/newad/sbDivideAsinReports"

# . 报告 - Sponsored Display
# https://apidoc.lingxing.com/#/docs/newAd/report/sdCampaignReports
SD_CAMPAIGN_REPORTS: str = "/pb/openapi/newad/sdCampaignReports"
# https://apidoc.lingxing.com/#/docs/newAd/report/sdCampaignHourData
SD_CAMPAIGN_HOUR_DATA: str = "/pb/openapi/newad/sdCampaignHourData"
# https://apidoc.lingxing.com/#/docs/newAd/report/sdAdGroupReports
SD_AD_GROUP_REPORTS: str = "/pb/openapi/newad/sdAdGroupReports"
# https://apidoc.lingxing.com/#/docs/newAd/report/sdAdGroupHourData
SD_AD_GROUP_HOUR_DATA: str = "/pb/openapi/newad/sdAdGroupHourData"
# https://apidoc.lingxing.com/#/docs/newAd/report/sdProductAdReports
SD_PRODUCT_REPORTS: str = "/pb/openapi/newad/sdProductAdReports"
# https://apidoc.lingxing.com/#/docs/newAd/report/sdAdvertiseHourData
SD_PRODUCT_HOUR_DATA: str = "/pb/openapi/newad/sdAdvertiseHourData"
# https://apidoc.lingxing.com/#/docs/newAd/report/sdTargetReports
SD_TARGET_REPORTS: str = "/pb/openapi/newad/sdTargetReports"
# https://apidoc.lingxing.com/#/docs/newAd/report/sdTargetHourData
SD_TARGET_HOUR_DATA: str = "/pb/openapi/newad/sdTargetHourData"
# https://apidoc.lingxing.com/#/docs/newAd/report/sdMatchTargetReports
SD_MATCHED_TARGET_REPORTS: str = "/pb/openapi/newad/sdMatchTargetReports"

# . 报告 - Demand-Side Platform (DSP)
# https://apidoc.lingxing.com/#/docs/newAd/report/dspReportOrderList
DSP_REPORTS: str = "/basicOpen/dspReport/order/list"


# 报表下载 ----------------------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/newAd/reportDownload/abaReport
DOWNLOAD_ABA_REPORT: str = "/pb/openapi/newad/abaReport"

# 操作日志 ----------------------------------------------------------------------------------------------------------------------
# https://apidoc.lingxing.com/#/docs/newAd/apiLogStandard
ADS_OPERATION_LOGS: str = "/pb/openapi/newad/apiLogStandard"
