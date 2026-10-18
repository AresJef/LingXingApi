"""批量改名的离线回归：实际参数模型与 API，所有响应均为合成数据。"""

import asyncio
from copy import deepcopy
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from pydantic import ValidationError

from lingxingapi import errors
from lingxingapi.basic import param, route, schema
from lingxingapi.basic.api import BasicAPI


def rename_items(count):
    return [{"sid": number, "name": f"sample-{number}"} for number in range(1, count + 1)]


def rename_response(count):
    return {
        "code": 0,
        "message": "success",
        "error_details": [],
        "request_id": "synthetic-rename-response",
        "response_time": "2026-10-10 00:00:00",
        "data": {"success_num": count, "failure_num": 0, "failure_detail": []},
    }


@pytest.mark.parametrize("container", [list, tuple])
@pytest.mark.parametrize("key", ["renames", "sid_name_list"])
@pytest.mark.parametrize("count", [1, 2, 10])
def test_rename_batch_preserves_wire_fields_order_and_input(container, key, count):
    items = rename_items(count)
    items[0]["name"] = "  sample-1  "
    data = {key: container(items)}
    before = deepcopy(data)
    expected = rename_items(count)

    assert param.RenameSellers.model_validate_params(data) == {"sid_name_list": expected}
    assert data == before


@pytest.mark.parametrize("key", ["renames", "sid_name_list"])
def test_direct_single_rename_dictionary_remains_supported(key):
    item = {"sid": 1, "name": "sample-1"}
    assert param.RenameSellers.model_validate_params({key: item}) == {"sid_name_list": [item]}


@pytest.mark.parametrize("container", [list, tuple])
@pytest.mark.parametrize("key", ["renames", "sid_name_list"])
def test_empty_rename_batch_reports_validation_error(container, key):
    with pytest.raises(ValidationError, match="必须提供至少一个 rename"):
        param.RenameSellers.model_validate_params({key: container()})


@pytest.mark.parametrize(
    "item",
    [
        {},
        {"name": "sample"},
        {"sid": 1},
        {"sid": -1, "name": "sample"},
        {"sid": "invalid", "name": "sample"},
        {"sid": 1.5, "name": "sample"},
        {"sid": 1, "name": ""},
        {"sid": 1, "name": "   "},
        {"sid": 1, "name": None},
        {"sid": 1, "name": 123},
        None,
        "invalid",
    ],
    ids=["empty", "missing-sid", "missing-name", "negative-sid", "invalid-sid",
         "fractional-sid", "empty-name", "blank-name", "null-name", "numeric-name",
         "null-item", "string-item"],
)
def test_invalid_rename_item_is_rejected_before_api_request(item):
    items = [rename_items(1)[0], item]
    before = deepcopy(items)
    with pytest.raises(ValidationError):
        param.RenameSellers.model_validate_params({"renames": items})

    signed = AsyncMock()
    api = SimpleNamespace(_request_with_sign=signed)
    with pytest.raises(errors.InvalidParametersError) as caught:
        asyncio.run(BasicAPI.RenameSellers(api, *items))
    assert isinstance(caught.value.__cause__, ValidationError)
    signed.assert_not_awaited()
    assert items == before


@pytest.mark.parametrize("count", [1, 2, 10])
def test_api_rename_batch_validates_and_sends_exact_synthetic_body(count):
    items = rename_items(count)
    signed = AsyncMock(return_value=rename_response(count))
    api = SimpleNamespace(_request_with_sign=signed)

    result = asyncio.run(BasicAPI.RenameSellers(api, *items))

    signed.assert_awaited_once_with("POST", route.RENAME_SELLERS, body={"sid_name_list": items})
    assert isinstance(result, schema.RenameSellersResult)
    assert result.data.success == count
    assert result.data.failure == 0
    assert result.data.failure_detail == []


def test_api_empty_rename_batch_keeps_validation_cause_and_never_sends():
    signed = AsyncMock()
    api = SimpleNamespace(_request_with_sign=signed)
    with pytest.raises(errors.InvalidParametersError) as caught:
        asyncio.run(BasicAPI.RenameSellers(api))
    assert isinstance(caught.value.__cause__, ValidationError)
    assert "必须提供至少一个 rename" in str(caught.value.__cause__)
    signed.assert_not_awaited()


@pytest.mark.parametrize("container", [list, tuple])
def test_above_documented_limit_keeps_existing_model_behavior(container):
    # 当前模型未实施文档中的 10 项上限；本次只修复未赋值变量，不新增数量规则。
    items = rename_items(11)
    assert param.RenameSellers.model_validate_params({"renames": container(items)}) == {
        "sid_name_list": items,
    }


def test_above_documented_limit_keeps_existing_api_behavior_with_mock():
    # 仅调用模拟传输，确认现状；不向领星发出真实改名请求。
    items = rename_items(11)
    signed = AsyncMock(return_value=rename_response(11))
    api = SimpleNamespace(_request_with_sign=signed)
    result = asyncio.run(BasicAPI.RenameSellers(api, *items))
    signed.assert_awaited_once_with("POST", route.RENAME_SELLERS, body={"sid_name_list": items})
    assert result.data.success == 11
