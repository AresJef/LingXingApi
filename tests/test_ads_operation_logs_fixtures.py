"""21份真实操作日志fixture；分页失败保留并仅在pytest报告已批准warning。"""

from copy import deepcopy
from pathlib import Path

from sample_collection import load_collection


def test_real_twenty_one_parameter_samples_and_exact_interface_paging_boundary(
    monkeypatch,
):
    # 明确工具依赖，单独执行不借tools/tests收集副作用或继承PYTHONPATH。
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "tools"))
    import ads_operation_logs as logs

    path = (
        Path(__file__).with_name("fixtures")
        / "ads/logs/ads_operation_logs-manifest.json"
    )
    manifest, records, raws = load_collection(path, logs.ENDPOINT)
    before = deepcopy((manifest, records, raws))
    limitations = logs.validate_collection(manifest, raws, public=True, warn=True)
    assert len(records) == 21 and manifest["headers"] == {"X-API-VERSION": "2"}
    assert manifest["validation"]["pagination"] == (
        "accepted_upstream_limit" if limitations else "proved"
    )
    assert manifest["limitations"] == list(limitations)
    assert all(raw["next_token"] is None for raw in raws.values())
    assert all(
        record["scenario"] == ("empty_expected" if not raws[label]["data"] else None)
        for label, record in records.items()
    )
    for raw in raws.values():
        for row in raw["data"]:
            assert row["object_id"] == row["campaign_id"]
            assert row["object_name"] == row["campaign_name"]
            assert "2026-10-01" <= row["operate_time"][:10] <= "2026-10-16"
    assert (manifest, records, raws) == before
