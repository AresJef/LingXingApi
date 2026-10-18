"""已发布采集集合的离线读取与整行比较；不导入tools或读取raw/pass。"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from response_contract import load_json_bytes


def same_data(left, right):
    return json.dumps(left, sort_keys=True, ensure_ascii=True, allow_nan=False) == json.dumps(right, sort_keys=True, ensure_ascii=True, allow_nan=False)


def load_collection(path: Path, endpoint: str):
    root = path.parent
    manifest = load_json_bytes(path.read_bytes())
    assert manifest["source"] == "local_raw" and manifest["endpoint"] == endpoint
    assert manifest["format"] == "ads-fixtures-v3"
    records, responses = {}, {}
    for record in manifest["samples"]:
        assert record["label"] not in records and record["http_status"] == 200
        path = root / record["fixture"]
        assert not path.is_symlink() and path.resolve().is_relative_to(root.resolve())
        data = path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == record["sha256"]
        fixture = load_json_bytes(data)
        assert fixture["source"] == "local_raw" and fixture["endpoint"] == endpoint
        records[record["label"]], responses[record["label"]] = record, fixture["response"]
    return manifest, records, responses
