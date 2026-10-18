"""正式 raw 契约入口；main 的受控 pytest 调用也执行这一项。"""

from response_contract import ContractError, load_json_bytes, validate_fixture, validate_response, validate_rename_sellers_response
from lingxingapi.basic.schema import RenameSellersResult
from lingxingapi.base.schema import ResponseResult
from edit_exchange_rate_contract import validate_edit_exchange_rate_response
from sp_entities_contract import MODELS as SP_ENTITY_MODELS, validate_sp_entity_response
from sb_entities_contract import MODELS as SB_ENTITY_MODELS, validate_sb_entity_response
from sd_entities_contract import MODELS as SD_ENTITY_MODELS, validate_sd_entity_response
from sp_reports_contract import HOURLY_MODELS, validate_sp_report_response
from sb_reports_contract import MODELS as SB_REPORT_CHECK_MODELS, validate_sb_report_response
from sd_reports_contract import MODELS as SD_REPORT_CHECK_MODELS, validate_sd_report_response
from ads_operation_logs_contract import validate_operation_logs_response


def test_api_contract(contract_case):
    if contract_case.get("error"):
        raise ContractError("input_error", [contract_case["error"]])
    if contract_case.get("fixture"):
        validate_fixture(contract_case["fixture"])
    else:
        raw = load_json_bytes(contract_case["snapshot"])
        if contract_case.get("endpoint") == "basic.EditExchangeRate":
            if contract_case["schema"] is not ResponseResult:
                raise ContractError("input_error", ["EditExchangeRate的登记Schema不符"])
            validate_edit_exchange_rate_response(raw, scenario=contract_case.get("scenario"))
        elif contract_case["schema"] is RenameSellersResult:
            validate_rename_sellers_response(raw, scenario=contract_case.get("scenario"))
        elif contract_case.get("endpoint") == "ads.Portfolios":
            from lingxingapi.ads.schema import Portfolios
            from portfolios_contract import validate_portfolios_response
            if contract_case["schema"] is not Portfolios:
                raise ContractError("input_error", ["Portfolios的登记Schema不符"])
            validate_portfolios_response(raw, scenario=contract_case.get("scenario"))
        elif contract_case.get("endpoint") == "ads.SpCampaigns":
            from lingxingapi.ads.schema import SpCampaigns
            from sp_campaigns_contract import validate_sp_campaigns_response
            if contract_case["schema"] is not SpCampaigns:
                raise ContractError("input_error", ["SpCampaigns的登记Schema不符"])
            validate_sp_campaigns_response(raw, scenario=contract_case.get("scenario"))
        elif contract_case.get("endpoint") == "ads.AdsOperationLogs":
            validate_operation_logs_response(raw, contract_case["schema"], scenario=contract_case.get("scenario"))
        elif contract_case.get("endpoint") in SP_ENTITY_MODELS:
            if contract_case["schema"] is not SP_ENTITY_MODELS[contract_case["endpoint"]]:
                raise ContractError("input_error", ["SP 实体的登记Schema不符"])
            validate_sp_entity_response(raw, contract_case["schema"], scenario=contract_case.get("scenario"))
        elif contract_case.get("endpoint") in SB_ENTITY_MODELS:
            if contract_case["schema"] is not SB_ENTITY_MODELS[contract_case["endpoint"]]:
                raise ContractError("input_error", ["SB 的登记Schema不符"])
            validate_sb_entity_response(raw, contract_case["schema"], scenario=contract_case.get("scenario"))
        elif contract_case.get("endpoint") in SD_ENTITY_MODELS:
            if contract_case["schema"] is not SD_ENTITY_MODELS[contract_case["endpoint"]]:
                raise ContractError('input_error', ['SD接口与Schema不符'])
            validate_sd_entity_response(raw, contract_case["schema"], scenario=contract_case.get("scenario"))
        elif contract_case.get("endpoint") in SD_REPORT_CHECK_MODELS:
            if contract_case["schema"] is not SD_REPORT_CHECK_MODELS[contract_case["endpoint"]]:
                raise ContractError("input_error", ["SD报告的登记Schema不符"])
            validate_sd_report_response(raw, contract_case["schema"])
        elif contract_case.get("endpoint") in SB_REPORT_CHECK_MODELS:
            if contract_case["schema"] is not SB_REPORT_CHECK_MODELS[contract_case["endpoint"]]:
                raise ContractError("input_error", ["SB报告的登记Schema不符"])
            validate_sb_report_response(raw, contract_case["schema"])
        elif contract_case["schema"] in HOURLY_MODELS:
            validate_sp_report_response(raw, contract_case["schema"])
        else:
            validate_response(raw, contract_case["schema"])
