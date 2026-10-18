"""当前seller轻量集合；纯离线，旧20条文档样例不代表本轮采集。"""
from __future__ import annotations
from pathlib import Path
from lingxingapi.ads.schema import AdProfiles
from response_contract import validate_response
from sample_collection import load_collection, same_data


def test_current_seller_reference_segments_and_stability():
    manifest, records, responses = load_collection(Path(__file__).with_name("fixtures") / "ads/basic/common/ad_profiles-manifest.json", "ads.AdProfiles")
    assert len(records) == manifest["planned_requests"] == 4
    assert set(records) == {"reference-direct", "offset-first", "offset-second", "reference-end"}
    for label, raw in responses.items():
        parsed = validate_response(raw, AdProfiles)
        assert parsed.response_count == len(raw["data"]) == records[label]["request"]["length"]
        assert parsed.total_count == raw["total"]
        assert records[label]["request"]["type"] == "seller"
        assert set(records[label]["request"]) == {"type", "offset", "length"}
        for wire, row in zip(raw["data"], parsed.data, strict=True):
            assert type(wire["sid"]) is str and wire["sid"].isdecimal() and len(wire["sid"]) in {4, 5}
            assert row.sid == int(wire["sid"])
            assert type(wire["profile_id"]) is str and wire["profile_id"].isdecimal() and len(wire["profile_id"]) in {14, 15}
            assert row.profile_id == int(wire["profile_id"])
            assert wire["name"] == row.seller_name == "广告账号名"
            assert row.profile_type == wire["type"] and row.profile_status == wire["status"]
    assert same_data(responses["offset-first"]["data"] + responses["offset-second"]["data"], responses["reference-direct"]["data"])
    assert same_data(responses["reference-direct"]["data"], responses["reference-end"]["data"])
    assert manifest["checks"]["offset_concat"]["status"] == manifest["checks"]["baseline_stability"]["status"] == "proved"
    assert len({row["profile_id"] for row in responses["reference-direct"]["data"]}) == 4
    # 完整data比较在原始数据与脱敏结果上分别验证，来源由SHA关联。
