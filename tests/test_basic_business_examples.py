"""基础接口业务数值的静态原文投影；不依赖可覆盖 fixtures 或私有 raw。"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from documentation_contract import documentation_example
from lingxingapi.ads.api import AdsAPI
from lingxingapi.ads import schema as ads_schema
from lingxingapi.basic.api import BasicAPI
from lingxingapi.basic import schema as basic_schema


LEDGER = json.loads(Path(__file__).with_name("basic_business_examples_metrics.json").read_bytes())


@pytest.fixture
def redaction_tools_path(monkeypatch):
    """单独运行正式文件时，也明确定位本仓库的脱敏工具。"""
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "tools"))


def canonical(value):
    return json.dumps(value, sort_keys=True, allow_nan=False)


@pytest.mark.parametrize("endpoint,item", LEDGER["methods"].items())
def test_business_numeric_groups_in_api_and_collection_examples_share_real_row(endpoint, item):
    module, name = endpoint.split(".")
    api, schema = (BasicAPI, basic_schema) if module == "basic" else (AdsAPI, ads_schema)
    _, shown = documentation_example(getattr(api, name))
    data = getattr(schema, item["wrapper"]).model_fields["data"].examples[0]
    for surface in (shown["data"], data):
        row = surface[0] if type(surface) is list else surface
        assert canonical({field: row[field] for field in item["business_fields"]}) == canonical(item["row"]["values"])


@pytest.mark.parametrize("key,item", LEDGER["fields"].items())
def test_independent_business_field_examples_have_representative_original_source(key, item):
    schema = basic_schema if item["endpoint"].startswith("basic.") else ads_schema
    field = getattr(schema, item["model"]).model_fields[item["field"]]
    assert canonical(field.examples) == canonical([item["value"]])
    assert len(item["source"]["sha256"]) == 64


def test_business_example_contract_does_not_read_overwritable_raw_or_fixtures(monkeypatch):
    def forbid_read(path):
        raise AssertionError("static business examples cannot read current raw/fixtures")

    monkeypatch.setattr(Path, "read_bytes", forbid_read)
    for endpoint, item in LEDGER["methods"].items():
        test_business_numeric_groups_in_api_and_collection_examples_share_real_row(endpoint, item)
    for key, item in LEDGER["fields"].items():
        test_independent_business_field_examples_have_representative_original_source(key, item)


@pytest.mark.parametrize("endpoint,item", LEDGER["methods"].items())
def test_configured_redaction_preserves_business_wire_values_and_types(endpoint, item, redaction_tools_path):
    import redaction
    from redaction_formats import Formatter

    module, name = endpoint.split(".")
    wire = deepcopy(item["row"]["wire_values"])
    wire.update(profile_id=12345678901234, portfolio_id=23456789012345, name="Synthetic portfolio")
    raw = {"request_id": "ABCDEF12-1234-ABCD-1234-123456789ABC", "data": [wire]}
    formatter = Formatter()
    if name == "Portfolios":
        from portfolios import redaction_documents

        documents = {key: json.loads((Path(__file__).parents[1] / f"tools/redaction/{key}.json").read_bytes()) for key in ("global", "ads")}
        sample = {"sha256": "a" * 64, "request": {"profile_id": wire["profile_id"]}}
        documents = redaction_documents(documents, [raw], [sample], "b" * 64, formatter=formatter)
        rules = redaction.load_rules(module, name + "/" + sample["sha256"], documents=documents)
    else:
        rules = redaction.load_rules(module, "RenameSellers（返回失败）" if name == "RenameSellers" else name)
    original = deepcopy(raw)
    formatter.observe(raw, rules, name)
    clean = redaction.apply_redactions(raw, formatter.compile(raw, rules, name))
    assert raw == original
    for key, value in item["row"]["wire_values"].items():
        assert canonical(clean["data"][0][key]) == canonical(value)
        assert type(clean["data"][0][key]) is type(value)
    assert clean["request_id"] != raw["request_id"]
    if module == "ads":
        assert clean["data"][0]["profile_id"] != wire["profile_id"]


@pytest.mark.parametrize("rate", ["1.0000000000", "7.2400000000", "0.0003000000", "0", None, ""])
def test_exchange_rate_redaction_keeps_real_numeric_strings_including_zero_empty_and_null(rate, redaction_tools_path):
    import redaction
    from redaction_formats import Formatter

    raw = {"data": [{"rate_org": "7.1541", "my_rate": rate, "update_time": "2026-09-02 12:30:45"}]}
    rules = redaction.load_rules("basic", "ExchangeRates")
    formatter = Formatter()
    formatter.observe(raw, rules, "ExchangeRates")
    clean = redaction.apply_redactions(raw, formatter.compile(raw, rules, "ExchangeRates"))
    assert clean["data"][0]["rate_org"] == "7.1541"
    assert clean["data"][0]["my_rate"] == rate and type(clean["data"][0]["my_rate"]) is type(rate)
    assert clean["data"][0]["update_time"] != raw["data"][0]["update_time"]
