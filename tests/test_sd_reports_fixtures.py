"""SD九项正式完整报告的fixture契约；历史单实体补样保留原始覆盖范围。"""

from __future__ import annotations

import asyncio
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from lingxingapi.ads import schema
from lingxingapi.ads.api import AdsAPI
from sample_collection import load_collection, same_data
from sd_reports_contract import validate_sd_report_response
from test_sd_reports_requests import DAILY, HOURLY

DIRECTORY = Path(__file__).with_name("fixtures") / "ads/reports/sd"
PREFIXES = {
    "SdCampaignReports": "sd_campaign_reports",
    "SdCampaignHourData": "sd_campaign_hour_data",
    "SdAdGroupReports": "sd_ad_group_reports",
    "SdAdGroupHourData": "sd_ad_group_hour_data",
    "SdProductReports": "sd_product_reports",
    "SdProductHourData": "sd_product_hour_data",
    "SdTargetReports": "sd_target_reports",
    "SdTargetHourData": "sd_target_hour_data",
    "SdMatchedTargetReports": "sd_matched_target_reports",
}
DAILY_COMPLETE = tuple(item for item in DAILY if item[0] in PREFIXES)


def collection(method):
    return load_collection(
        DIRECTORY / (PREFIXES[method] + "-manifest.json"), "ads." + method
    )


def same_hour_rows(left, right):
    def canonical(row):
        return json.dumps(row, sort_keys=True, ensure_ascii=True, allow_nan=False)

    return Counter(map(canonical, left)) == Counter(map(canonical, right))


@pytest.mark.parametrize("method,url,fixed", DAILY_COMPLETE)
def test_complete_daily_identifiers_two_distinct_pages_cursor_priority_and_dates(
    method, url, fixed
):
    manifest, records, responses = collection(method)
    before = deepcopy((manifest, records, responses))
    assert len(records) == manifest["planned_requests"] == 13
    assert manifest["not_run"] == [] and manifest["diagnostics"] == []
    assert all(check["status"] == "proved" for check in manifest["checks"].values())
    for label, raw in responses.items():
        parsed = validate_sd_report_response(raw, getattr(schema, method))
        assert (
            parsed.response_count == len(raw["data"])
            and parsed.total_count == raw["total"]
        )
        request = records[label]["request"]
        assert request["show_detail"] == 0
        assert all(row["report_date"] == request["report_date"] for row in raw["data"])
        if "profile_id" in request:
            assert all(
                row["profile_id"] == request["profile_id"] for row in raw["data"]
            )
        if method != "SdMatchedTargetReports":
            for row, output in zip(raw["data"], parsed.data, strict=True):
                for wire, name, kind in (
                    (
                        "attributed_orders_new_to_brand_14d",
                        "new_to_brand_orders_14d",
                        int,
                    ),
                    (
                        "attributed_units_ordered_new_to_brand_14d",
                        "new_to_brand_units_14d",
                        int,
                    ),
                    (
                        "attributed_sales_new_to_brand_14d",
                        "new_to_brand_sales_14d",
                        float,
                    ),
                ):
                    assert type(row[wire]) is kind and row[wire] == 0
                    assert (
                        type(getattr(output, name)) is kind
                        and getattr(output, name) == row[wire]
                    )
    for account in ("A", "B"):
        rows = responses[f"account-{account}-profile-only"]["data"]
        assert rows
        assert same_data(rows, responses[f"account-{account}-sid-only"]["data"])
        assert same_data(rows, responses[f"account-{account}-both"]["data"])
    assert not same_data(
        responses["account-A-profile-only"]["data"],
        responses["account-B-profile-only"]["data"],
    )
    assert manifest["checks"]["cross_identifier_priority"]["observed"] == "profile_id"
    for account, other in (("A", "B"), ("B", "A")):
        assert same_data(
            responses[f"account-{account}-sid-{other}-profile"]["data"],
            responses[f"account-{other}-profile-only"]["data"],
        )
    relation = manifest["relationships"]
    reference = responses[relation["reference"]]["data"]
    assert len(reference) == 2 and not same_data(reference[:1], reference[1:])
    assert same_data(reference, responses[relation["end_reference"]]["data"])
    for key in ("offset_pages", "token_pages"):
        assert all(len(responses[label]["data"]) == 1 for label in relation[key])
        assert same_data(
            [row for label in relation[key] for row in responses[label]["data"]],
            reference,
        )
    assert same_data(
        responses[relation["token_control"]]["data"],
        responses[relation["token_conflict"]]["data"],
    )
    assert (manifest, records, responses) == before


@pytest.mark.parametrize("method,url,fixed", DAILY_COMPLETE)
def test_complete_daily_replays_the_existing_sdk_and_actual_cursor_source(
    method, url, fixed
):
    _, records, responses = collection(method)
    for label, record in records.items():
        request = deepcopy(record["request"])
        if record["next_token_from"] is not None:
            token = responses[record["next_token_from"]]["next_token"]
            assert type(token) is str and token
            request["next_token"] = token
        kwargs = {
            name: value for name, value in request.items() if name != "show_detail"
        }
        kwargs = {
            "sid": kwargs.get("sid"),
            "profile_id": kwargs.get("profile_id"),
            **kwargs,
        }
        signed = AsyncMock(return_value=responses[label])
        parsed = asyncio.run(
            getattr(AdsAPI, method)(
                SimpleNamespace(_request_with_sign=signed), **kwargs
            )
        )
        signed.assert_awaited_once_with(
            "POST", url, body=request, headers={"X-API-VERSION": "2"}
        )
        assert isinstance(parsed, getattr(schema, method))


@pytest.mark.parametrize("method,url,fixed", HOURLY)
def test_hourly_complete_rows_source_membership_multiset_and_null_token_unchanged(
    method, url, fixed
):
    manifest, records, responses = collection(method)
    before = deepcopy((manifest, records, responses))
    assert (
        len(records) == manifest["planned_requests"] == 3 and manifest["not_run"] == []
    )
    assert all(check["status"] == "proved" for check in manifest["checks"].values())
    assert (
        manifest["checks"]["baseline_stability"]["comparison"]
        == "complete_rows_multiset"
    )
    sources = {source["label"]: source for source in manifest["campaign_sources"]}
    _, _, campaigns = collection("SdCampaignReports")
    assert set(sources) == {"campaign-A", "campaign-B"}
    for label, raw in responses.items():
        assert "next_token" in raw and raw["next_token"] is None
        parsed = validate_sd_report_response(raw, getattr(schema, method))
        assert parsed.response_count == len(raw["data"]) > 0
        assert "next_token" not in parsed.model_dump()
        request = records[label]["request"]
        assert records[label]["next_token_from"] is None
        source = sources["campaign-A" if label == "reference-end" else label]
        assert source["campaign_id"] == request["campaign_id"]
        assert source["report_date"] == request["report_date"]
        account = source["label"].removeprefix("campaign-")
        campaign = campaigns[f"account-{account}-profile-only"]["data"][
            source["row_index"]
        ]
        assert all(
            source[key] == campaign[key]
            for key in ("profile_id", "campaign_id", "report_date")
        )
        assert all(
            row["report_date"] == request["report_date"]
            and row["campaign_id"] == request["campaign_id"]
            and row["profile_id"] == source["profile_id"]
            and 0 <= row["hour"] <= 23
            for row in raw["data"]
        )
        kwargs = {name: value for name, value in request.items() if name not in fixed}
        assert all(request[key] == value for key, value in fixed.items())
        signed = AsyncMock(return_value=raw)
        asyncio.run(
            getattr(AdsAPI, method)(
                SimpleNamespace(_request_with_sign=signed), **kwargs
            )
        )
        signed.assert_awaited_once_with("POST", url, body=request, headers={"X-API-VERSION": "2"})
    assert same_hour_rows(
        responses["campaign-A"]["data"], responses["reference-end"]["data"]
    )
    assert manifest["checks"]["baseline_stability"]["ordered_data_equal"] is same_data(
        responses["campaign-A"]["data"], responses["reference-end"]["data"]
    )
    assert (manifest, records, responses) == before


def test_target_text_and_double_json_share_six_audiences_and_one_category_namespace():
    _, _, daily = collection("SdTargetReports")
    _, _, hourly = collection("SdTargetHourData")
    text_audiences, json_audiences, categories = set(), set(), set()
    for response in daily.values():
        for row in response["data"]:
            clause = json.loads(json.loads(row["targeting_text"]))[0]
            if clause["type"] == "audience":
                value = clause["value"][0]["value"]
                assert row["targeting_expression"] == f'audience="{value}"'
                json_audiences.add(value)
            else:
                days = "30" if clause["type"] == "views" else "365"
                assert clause["value"] == [
                    {"type": "exactProduct"},
                    {"type": "lookback", "value": days},
                ]
                assert (
                    row["targeting_expression"]
                    == f'{clause["type"]}=(exact-product lookback={days})'
                )
    controls = set()
    for response in hourly.values():
        for row in response["data"]:
            text = row["targeting"]
            if match := re.fullmatch(r'audience="([0-9]+)"', text):
                text_audiences.add(match[1])
            elif match := re.fullmatch(
                r'views=\(category="([0-9]+)" lookback=30\)', text
            ):
                categories.add(match[1])
            else:
                controls.add(text)
    assert text_audiences == {f"10000000000000000{index}" for index in range(1, 7)}
    assert json_audiences == {"100000000000000006"} <= text_audiences
    assert categories == {"10000000001"}
    assert controls == {
        "similar-product",
        *[
            f"views=({kind} lookback={days})"
            for kind in ("exact-product", "similar-product")
            for days in (7, 14, 30, 60, 90)
        ],
    }


def test_matched_target_historical_single_entity_supplement_keeps_its_original_scope():
    path = DIRECTORY / "sd_matched_target_reports-evidence.json"
    fixture = json.loads(path.read_bytes())
    metadata = json.loads(
        path.with_name("sd_matched_target_reports-evidence-source.json").read_bytes()
    )
    assert (
        fixture["source"] == "local_raw"
        and fixture["endpoint"] == "ads.SdMatchedTargetReports"
    )
    assert "samples" not in fixture and "checks" not in fixture
    assert metadata["fixture_sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert (
        metadata["matrix_status"] == "coverage_gap"
        and metadata["normal_matrix_published"] is False
    )
    assert metadata["schema"] == metadata["redaction"] == "passed"
    assert metadata["scope"] == "historical_single_entity_contract_supplement"
    assert metadata["unique_nonempty_accounts"] == 1
    assert set(metadata["missing_coverage"]) == {
        "second_nonempty_account",
        "two_distinct_rows_reference",
        "second_offset_page",
        "second_cursor_page",
        "cursor_priority",
    }
    raw = fixture["response"]
    parsed = validate_sd_report_response(raw, schema.SdMatchedTargetReports)
    assert len(raw["data"]) == parsed.response_count == metadata["rows"] == 1
    assert raw["data"][0]["currency"] is None and parsed.data[0].currency_code == ""
    clause = json.loads(json.loads(raw["data"][0]["target_text"]))
    assert clause == [
        {
            "type": "views",
            "value": [{"type": "exactProduct"}, {"type": "lookback", "value": "30"}],
        }
    ]
    assert re.fullmatch(r"[A-Z0-9]{10}", raw["data"][0]["matched_target"])
    _, _, products = collection("SdProductHourData")
    assert raw["data"][0]["matched_target"] in {
        row["asin"] for response in products.values() for row in response["data"]
    }


def test_matched_normal_matrix_uses_two_accounts_and_preserves_approved_control_strings():
    manifest, records, responses = collection("SdMatchedTargetReports")
    assert len(records) == 13 and manifest["not_run"] == []
    assert all(check["status"] == "proved" for check in manifest["checks"].values())
    assert len(responses["reference-direct"]["data"]) == 2
    assert len(responses["account-B-profile-only"]["data"]) == 1
    _, campaign_records, _ = collection("SdCampaignReports")
    assert (
        records["account-B-profile-only"]["request"]["profile_id"]
        == campaign_records["account-B-profile-only"]["request"]["profile_id"]
    )
    count = Counter()
    for raw in responses.values():
        for row in raw["data"]:
            control = json.loads(json.loads(row["target_text"]))
            count[control[0]["type"]] += 1
            if control[0]["type"] == "similarProduct":
                assert control == [{"type": "similarProduct"}]
            else:
                assert control == [
                    {
                        "type": "views",
                        "value": [
                            {"type": "exactProduct"},
                            {"type": "lookback", "value": "30"},
                        ],
                    }
                ]
    assert count == {"similarProduct": 11, "views": 4}
