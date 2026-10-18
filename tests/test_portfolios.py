"""Portfolios 空场景及正式样本；纯离线，不能用 mock 结果代替线上证明。"""
from __future__ import annotations

from copy import deepcopy
import ast
import base64
import inspect
from pathlib import Path

import pytest

from lingxingapi.ads.schema import Portfolios
from lingxingapi.ads.api import AdsAPI
from portfolios_contract import validate_portfolios_response
from response_contract import ContractError, load_json_bytes, validate_response
from documentation_contract import validate_documentation, documentation_example


def empty_response():
    return {"code": 0, "message": "success", "data": [], "total": 56, "next_token": "",
            "error_details": [], "request_id": "synthetic", "response_time": "2000-01-01 00:00:00"}


def test_explicit_empty_result_checks_outer_schema_and_preserves_data():
    raw = empty_response()
    before = deepcopy(raw)
    parsed = validate_portfolios_response(raw, scenario="empty_expected")
    assert parsed.data == [] and parsed.response_count == 0 and parsed.total_count == 56
    assert raw == before
    for validate in (lambda: validate_response(raw, Portfolios), lambda: validate_portfolios_response(raw)):
        with pytest.raises(ContractError) as caught:
            validate()
        assert caught.value.status == "coverage"


@pytest.mark.parametrize("patch", [
    {"extra": True}, {"code": 100}, {"code": "0"}, {"data": None}, {"data": {}},
    {"data": [{"profile_id": 1}]}, {"error_details": ["failed"]}, {"total": "bad"},
    {"total": []}, {"next_token": []}, {"response_count": 2},
])
def test_empty_result_never_hides_other_differences(patch):
    with pytest.raises(ContractError):
        validate_portfolios_response({**empty_response(), **patch}, scenario="empty_expected")


@pytest.mark.parametrize("key", ["total", "message", "error_details", "request_id", "response_time", "next_token"])
def test_empty_result_missing_outer_fields_still_fails(key):
    raw = empty_response()
    del raw[key]
    with pytest.raises(ContractError):
        validate_portfolios_response(raw, scenario="empty_expected")


@pytest.fixture(scope="module")
def portfolio_dataset():
    from sample_collection import load_collection
    return load_collection(Path(__file__).with_name("fixtures") / "ads/basic/common/portfolios-manifest.json", "ads.Portfolios")


def sequence(raw):
    return [(row["profile_id"], row["portfolio_id"]) for row in raw["data"]]


def test_daily_collection_contains_only_the_fixed_sixteen_scenes(portfolio_dataset):
    manifest, records, responses = portfolio_dataset
    assert len(records) == manifest["planned_requests"] == 16 and manifest["not_run"] == []
    assert set(records) == {"account-A-sid-only", "account-A-profile-only", "account-A-both",
        "account-B-sid-only", "account-B-profile-only", "account-B-both", "account-A-sid-B-profile", "account-B-sid-A-profile",
        "state-paused", "state-archived", "state-omitted", "reference-direct", "offset-second", "token-second",
        "token-priority-conflicting-offset", "reference-end"}
    for label, raw in responses.items():
        before = deepcopy(raw)
        parsed = validate_portfolios_response(raw, scenario=records[label]["scenario"])
        assert raw == before and parsed.response_count == len(raw["data"]) == len(parsed.data)
        assert parsed.total_count == raw["total"] and parsed.errors == raw["error_details"] == []
        for wire, row in zip(raw["data"], parsed.data, strict=True):
            assert row.profile_id == int(wire["profile_id"]) and row.portfolio_id == int(wire["portfolio_id"])
            assert row.portfolio_name == wire["name"] and row.budget == wire["budget"]
            assert row.in_budget == wire["in_budget"] and row.state == wire["state"]
            assert row.status == wire["serving_status"]
            assert row.create_time_ts == wire["creation_date"] and row.update_time_ts == wire["last_updated_date"]
        if raw["next_token"] not in (None, ""):
            decoded = base64.b64decode(raw["next_token"], validate=True).decode("ascii")
            assert len(raw["next_token"]) == 20 and decoded.isdecimal() and len(decoded) in {13, 14}


def test_real_eight_identifier_scenarios_account_relationships(portfolio_dataset):
    _, records, responses = portfolio_dataset
    for account in ("A", "B"):
        baseline = sequence(responses[f"account-{account}-both"])
        assert baseline and sequence(responses[f"account-{account}-sid-only"]) == sequence(responses[f"account-{account}-profile-only"]) == baseline
        assert set(records[f"account-{account}-sid-only"]["request"]) == {"sid", "state", "offset", "length"}
        assert set(records[f"account-{account}-profile-only"]["request"]) == {"profile_id", "state", "offset", "length"}
    assert sequence(responses["account-A-sid-B-profile"]) == sequence(responses["account-B-both"])
    assert sequence(responses["account-B-sid-A-profile"]) == sequence(responses["account-A-both"])


def test_complete_data_offset_and_token_segments_match_reference(portfolio_dataset):
    from sample_collection import same_data
    manifest, records, responses = portfolio_dataset
    relationships = manifest["relationships"]
    reference = responses[relationships["reference"]]["data"]
    assert len(reference) == 4
    for kind in ("offset", "token"):
        pages = relationships[kind + "_pages"]
        assert all(len(responses[label]["data"]) == 2 for label in pages)
        combined = [row for label in pages for row in responses[label]["data"]]
        assert same_data(combined, reference)
        assert manifest["checks"][kind + "_concat"]["status"] == "proved"
    assert relationships["offset_pages"][0] == relationships["token_pages"][0] == "account-A-profile-only"
    assert records["offset-second"]["request"]["offset"] == 2
    assert records["token-second"]["next_token_from"] == "account-A-profile-only"
    assert "offset" not in records["token-second"]["request"]
    assert records["token-priority-conflicting-offset"]["request"]["offset"] == 0
    assert same_data(responses["token-second"]["data"], responses["token-priority-conflicting-offset"]["data"])
    assert same_data(reference, responses[relationships["end_reference"]]["data"])
    assert manifest["checks"]["baseline_stability"]["status"] == manifest["checks"]["token_priority"]["status"] == "proved"


def test_real_states_preserve_observed_coverage_limits(portfolio_dataset):
    manifest, records, responses = portfolio_dataset
    for state in ("paused", "archived"):
        assert records["state-" + state]["request"]["state"] == state
        assert responses["state-" + state]["data"] == [] and responses["state-" + state]["total"] == 0
        assert manifest["checks"]["state_" + state]["status"] == "no_nonempty_sample"
    assert "state" not in records["state-omitted"]["request"]


def test_portfolios_google_docstring_is_valid_without_latest_fixture_value_equality():
    path = Path(__file__).with_name("fixtures") / "ads/basic/common/portfolios_documentation.json"
    sample = load_json_bytes(path.read_bytes())
    assert sample["source"] == "local_raw" and sample["endpoint"] == "ads.Portfolios"
    validate_portfolios_response(sample["response"])
    doc = inspect.getdoc(AdsAPI.Portfolios)
    assert doc.count(".. code-block:: python") == 2
    assert doc.index("## Docs") < doc.index("Args:") < doc.index("Returns:") < doc.index("Examples:")
    assert "sid 与 profile_id 至少提供一项；同时提供时，以 profile_id 指定的广告账号为准。" in doc
    assert all(word not in doc for word in ("本次", "实测", "采集", "样本"))
    shown = validate_documentation(AdsAPI.Portfolios, Portfolios)
    call, _ = documentation_example(AdsAPI.Portfolios)
    arguments = {item.arg: ast.literal_eval(item.value) for item in call.keywords}
    assert all(row['profile_id'] == arguments['profile_id'] and row['state'] == arguments['state'] for row in shown['data'] if row is not Ellipsis)
