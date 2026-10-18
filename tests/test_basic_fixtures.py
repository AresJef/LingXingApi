"""四项只读Basic真实fixture、完整契约与当前API文档示例。"""
from copy import deepcopy
from datetime import date
from pathlib import Path

from lingxingapi.basic import schema
from lingxingapi.basic.api import BasicAPI
from response_contract import ContractError, load_json_bytes, validate_response
from documentation_contract import validate_documentation, validate_field_examples

FIXTURES = Path(__file__).with_name("fixtures") / "basic"


def _fixture(stem, model):
    path = FIXTURES / (stem + ".json")
    if path.is_symlink() or not path.is_file():
        raise ContractError("input_error", [f"{model.__name__} fixture不存在或不是普通文件：{path}"])
    fixture = load_json_bytes(path.read_bytes())
    if type(fixture) is not dict or fixture.get("source") not in {"live", "local_raw"}:
        raise ContractError("input_error", [f"{model.__name__} fixture缺少实际样本包装身份"])
    if fixture.get("endpoint") != "basic." + model.__name__:
        raise ContractError("input_error", [f"{model.__name__} fixture接口身份不符"])
    raw = fixture.get("response")
    before = deepcopy(raw)
    parsed = validate_response(raw, model)
    assert raw == before
    assert parsed.response_count == len(raw["data"]) == len(parsed.data)
    return raw, parsed


def test_sellers_fixture_contract():
    raw, parsed = _fixture("sellers", schema.Sellers)
    for wire, seller in zip(raw["data"], parsed.data, strict=True):
        assert seller.seller_name == wire["name"]
        assert seller.account_id == wire["seller_account_id"] and type(seller.account_id) is int
        assert seller.ads_authorized == wire["has_ads_setting"] and type(seller.ads_authorized) is int
    validate_documentation(BasicAPI.Sellers, schema.Sellers)


def test_concept_sellers_fixture_contract():
    raw, parsed = _fixture("concept_sellers", schema.ConceptSellers)
    for wire, seller in zip(raw["data"], parsed.data, strict=True):
        assert seller.cmid == wire["mid"] and type(seller.cmid) is int
        assert seller.csid == wire["id"] and type(seller.csid) is int
        assert seller.seller_name == wire["name"]
        assert seller.account_id == wire["seller_account_id"] and type(seller.account_id) is int
        assert seller.account_name == wire["seller_account_name"]
    validate_documentation(BasicAPI.ConceptSellers, schema.ConceptSellers)


def test_accounts_fixture_contract():
    raw, parsed = _fixture("accounts", schema.Accounts)
    for wire, account in zip(raw["data"], parsed.data, strict=True):
        assert account.parent_id == wire["zid"] and type(account.parent_id) is int
        assert account.user_id == wire["uid"] and type(account.user_id) is int
        assert account.display_name == wire["realname"]
        assert account.phone == wire["mobile"]
        assert account.login_count == wire["login_num"] and type(account.login_count) is int
        assert account.sellers == wire["seller"] and type(account.sellers) is str
    assert {account.role for account in parsed.data} == {"", "运营"}
    assert validate_field_examples(schema.Account)["role"] == "运营"
    shown = validate_documentation(BasicAPI.Accounts, schema.Accounts)
    assert shown["data"][0]["role"] == "运营" and shown["data"][0]["login_count"] == 0


def test_exchange_rates_fixture_contract():
    raw, parsed = _fixture("exchange_rates", schema.ExchangeRates)
    for wire, rate in zip(raw["data"], parsed.data, strict=True):
        expected = wire["date"] + "-01" if len(wire["date"]) == 7 else wire["date"]
        assert rate.date == date.fromisoformat(expected).isoformat()
        assert rate.currency == wire["name"] and rate.currency_code == wire["code"]
        assert rate.currency_icon == wire["icon"]
        assert type(rate.boc_rate) is float and rate.boc_rate == float(wire["rate_org"])
        assert type(rate.user_rate) is float and rate.user_rate == float(wire["my_rate"])
        assert rate.update_time == wire["update_time"]
    assert validate_field_examples(schema.ExchangeRate)["update_time"]
    shown = validate_documentation(BasicAPI.ExchangeRates, schema.ExchangeRates)
    assert shown["data"][0]["update_time"]
