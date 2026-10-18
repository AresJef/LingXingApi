"""真实汇率双场景fixture及现有SDK业务错误边界，严格离线。"""
import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest
from aiohttp import ClientSession
from lingxingapi import API, errors
from lingxingapi.base.schema import ResponseResult
from lingxingapi.basic import route
from response_contract import load_json_bytes
from edit_exchange_rate_contract import validate_edit_exchange_rate_fixture

FIXTURES = Path(__file__).with_name("fixtures")/"basic"


def test_EditExchangeRate_返回成功():
    path = FIXTURES/"edit_exchange_rate_success.json"
    parsed = validate_edit_exchange_rate_fixture(path, scenario="success")
    raw = load_json_bytes(path.read_bytes())["response"]
    assert parsed.code == 0 and parsed.data is None and parsed.errors == []
    assert type(raw["total"]) is int and raw["total"] == 0


def test_EditExchangeRate_返回失败():
    path = FIXTURES/"edit_exchange_rate_failure.json"
    parsed = validate_edit_exchange_rate_fixture(path, scenario="failure")
    raw = load_json_bytes(path.read_bytes())["response"]
    assert parsed.code == raw["code"] == 100 and parsed.message == "未知异常"
    assert parsed.errors == raw["error_details"] == ["操作失败"] and parsed.data is None
    assert parsed.model_dump(mode="json")["code"] == 100


@pytest.mark.parametrize("failure", [False, True])
def test_real_fixture_replay_preserves_public_sdk_success_and_error_boundary(monkeypatch, failure):
    import json
    name = "failure" if failure else "success"
    raw = load_json_bytes((FIXTURES/("edit_exchange_rate_"+name+".json")).read_bytes())["response"]
    payload = json.dumps(raw, ensure_ascii=False).encode()
    calls = []
    @asynccontextmanager
    async def request(session, method, url, **kwargs):
        assert method == "POST" and url == route.EDIT_EXCHANGE_RATE
        assert kwargs["json"] == {"date":"2016-12", "code":"XXX" if failure else "VND", "my_rate":"0.0003000000"}
        calls.append(url)
        yield SimpleNamespace(status=200, reason="unit", read=AsyncMock(return_value=payload))
    monkeypatch.setattr(ClientSession, "request", request)
    parse = Mock(wraps=ResponseResult.model_validate)
    monkeypatch.setattr(ResponseResult, "model_validate", parse)
    async def replay():
        async with API("unitappid1234567", "unit-sdk-private-key") as client:
            client._state.access_token = "unit-sdk-token"
            client._state.session = ClientSession()
            monkeypatch.setattr(client.basic, "_UpdateToken", AsyncMock(side_effect=AssertionError("离线禁止令牌刷新")))
            if failure:
                with pytest.raises(errors.InternalServerError):
                    await client.basic.EditExchangeRate("2016-12", "XXX", "0.0003")
            else:
                result = await client.basic.EditExchangeRate("2016-12", "VND", "0.0003")
                assert result.code == 0 and result.data is None and not hasattr(result, "total")
    asyncio.run(replay())
    assert len(calls) == 1 and parse.call_count == (0 if failure else 1)
