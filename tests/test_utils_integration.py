"""Offline callers and BaseAPI contracts for utils; all transports are synthetic."""

import asyncio
from contextlib import asynccontextmanager
from copy import deepcopy
from decimal import Decimal
from json import dumps
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest
from Crypto.Cipher import AES
from aiohttp import ClientTimeout
from pydantic import ValidationError

from lingxingapi import errors, utils
from lingxingapi.ads import param as ads
from lingxingapi.basic import param as basic
from lingxingapi.base.api import BaseAPI
from lingxingapi.fba import param as fba
from lingxingapi.finance import param as finance
from lingxingapi.product import param as product
from lingxingapi.sales import param as sales
from lingxingapi.tools import param as tools
from lingxingapi.warehourse import param as warehouse


@pytest.mark.parametrize(
    "model,value,expected",
    [
        (basic.ExchangeRate, {"date": "2026"}, {"date": "2026-01"}),
        (
            basic.EditExchangeRate,
            {"date": "2026-09", "currency_code": "USD", "user_rate": Decimal("1.25")},
            {"date": "2026-09", "code": "USD", "my_rate": "1.2500000000"},
        ),
        (
            sales.Listings,
            {
                "sids": [0, False, 2, 2],
                "search_value": [" a ", "a"],
                "update_start_time": "2026-09-15T03:04:05+08:00",
            },
            {
                "sid": "0,False,2,2",
                "search_value": ["a", "a"],
                "listing_update_start_time": "2026-09-15 03:04:05",
            },
        ),
        (
            sales.Listings,
            {"sids": 0, "search_value": [], "update_start_time": None},
            {"sid": "0", "search_value": []},
        ),
        (
            warehouse.WarehouseBins,
            {"warehouse_ids": (0, False, 3), "bin_ids": [4, 4]},
            {"wid": "0,False,3", "bin_id": "4,4"},
        ),
        (
            product.EnableDisableProducts,
            {"status": "Enable", "lsku_ids": [0, False, 2]},
            {"batch_status": "Enable", "product_ids": [0, False, 2]},
        ),
        (
            product.Products,
            {"lskus": [" a ", "a"], "sku_identifiers": ["", " b "]},
            {"sku_list": ["a", "a"], "sku_identifier": ["", " b "]},
        ),
        (
            finance.FinanceShare,
            {"mids": [0, False, 2], "sids": 3},
            {"countryCodes": [0, False, 2], "sids": [3]},
        ),
        (
            finance.Settlements,
            {"start_date": "2026-09", "end_date": "2026-09-15", "date_type": 0},
            {"startDate": "2026-09-01", "endDate": "2026-09-15", "dateType": 0},
        ),
        (
            finance.ShipmentSettlement,
            {
                "seller_ids": [" a ", "a"],
                "start_date": "2026-09",
                "end_date": "2026-09-15",
                "date_type": "01",
            },
            {
                "amazonSellerIds": ["a", "a"],
                "filterBeginDate": "2026-09-01",
                "filterEndDate": "2026-09-15",
                "timeType": "01",
            },
        ),
        (
            fba.StaPlans,
            {
                "start_date": "2026-09",
                "end_date": "2026-09-15",
                "date_type": 1,
                "sids": [0, False, 2],
                "statuses": [],
            },
            {
                "dateBegin": "2026-09-01",
                "dateEnd": "2026-09-15",
                "dateType": 1,
                "sids": [0, False, 2],
                "statusList": [],
                "page": 1,
                "length": 200,
            },
        ),
        (
            ads.AdReports,
            {"profile_id": 2, "report_date": "2026-09-15T03:04:05"},
            {"profile_id": 2, "report_date": "2026-09-15"},
        ),
        (
            tools.MonitorKeywords,
            {"start_date": "2026-09", "end_date": None},
            {"start_date": "2026-09-01"},
        ),
        (
            tools.MonitorAsins,
            {"start_time": "2026-09-15T03:04:05", "monitor_levels": [0, False, 1]},
            {"start_time": "2026-09-15 03:04:05", "levels": [0, False, 1]},
        ),
        (
            sales.PromotionOnListings,
            {"site_date": "2026-09", "product_status": [-1, False, 1]},
            {"site_date": "2026-09-01", "product_status": [-1, False, 1]},
        ),
    ],
)
def test_actual_parameter_models_keep_wire_values(model, value, expected):
    before = deepcopy(value)
    result = model.model_validate_params(value)
    assert result == expected and value == before
    # bool == 0 alone would miss a compatibility regression.
    for key, expected_value in expected.items():
        if isinstance(expected_value, list):
            assert [type(x) for x in result[key]] == [type(x) for x in expected_value]


@pytest.mark.parametrize(
    "model,value",
    [
        (basic.ExchangeRate, {"date": None}),
        (sales.Listings, {"sids": []}),
        (warehouse.WarehouseBins, {"warehouse_ids": [-1]}),
        (product.EnableDisableProducts, {"status": "Enable", "lsku_ids": ["1"]}),
        (finance.FinanceShare, {"mids": []}),
        (ads.AdReports, {"profile_id": 2, "report_date": "bad"}),
    ],
)
def test_actual_parameter_models_still_reject_invalid_values(model, value):
    with pytest.raises(ValidationError):
        model.model_validate_params(value)


@pytest.mark.parametrize("position", [0, 1, 2])
def test_actual_integer_array_error_keeps_nonnegative_wording(position):
    ids = [0, False, 2]
    ids[position] = -1
    before = list(ids)
    with pytest.raises(ValidationError) as caught:
        warehouse.WarehouseBins.model_validate_params({"warehouse_ids": ids})
    original = caught.value.errors(include_url=False)[0]["ctx"]["error"]
    assert str(original) == "仓库ID warehouse_ids 参数中的元素必须为非负整数, 而非 -1."
    assert original.__cause__ is None and ids == before


@pytest.mark.parametrize("value", ["0", "-1"])
def test_actual_exchange_rate_error_keeps_positive_number_wording(value):
    with pytest.raises(ValidationError) as caught:
        basic.EditExchangeRate.model_validate_params(
            {
                "date": "2026-09",
                "currency_code": "USD",
                "user_rate": value,
            }
        )
    original = caught.value.errors(include_url=False)[0]["ctx"]["error"]
    assert str(original) == f"用户自定义汇率 user_rate 参数值必须为正数, 而非 {value}."
    assert original.__cause__ is None


def make_api(request):
    api = BaseAPI(
        app_id="0" * 16,
        app_secret="synthetic",
        app_cipher=AES.new(b"0" * 16, AES.MODE_ECB),
        timeout=ClientTimeout(total=1),
        ignore_timeout=False,
        ignore_timeout_wait=0,
        ignore_timeout_retry=1,
        ignore_api_limit=False,
        ignore_api_limit_wait=0,
        ignore_api_limit_retry=0,
        ignore_internal_server_error=False,
        ignore_internal_server_error_wait=0,
        ignore_internal_server_error_retry=0,
        ignore_internet_connection=False,
        ignore_internet_connection_wait=0,
        ignore_internet_connection_retry=0,
        max_tcp_connections=1,
        proxy_connector=None,
    )
    api._state.session = SimpleNamespace(closed=False, request=request)
    api._state.access_token = "synthetic-token-0"
    return api


@pytest.mark.parametrize("retry", ["auth", "timeout"])
def test_each_actual_send_rebuilds_timestamp_and_signature(monkeypatch, retry):
    sends = []

    @asynccontextmanager
    async def request(method, url, *, params, json, headers):
        sends.append(deepcopy(params))
        if len(sends) == 1 and retry == "timeout":
            raise TimeoutError("synthetic timeout")
        response = {"code": 2001003} if len(sends) == 1 else {"code": 0, "data": []}
        yield SimpleNamespace(
            status=200, read=AsyncMock(return_value=dumps(response).encode())
        )

    api = make_api(request)

    async def update(**kwargs):
        api._state.access_token = "synthetic-token-1"
        api._state.token_version += 1

    api._UpdateToken = AsyncMock(side_effect=update)
    api._ignore_timeout = retry == "timeout"
    writer = Mock(wait_closed=AsyncMock())
    monkeypatch.setattr(
        asyncio, "open_connection", AsyncMock(return_value=(None, writer))
    )
    times = iter([100, 101])
    monkeypatch.setattr(utils, "_unix_time", lambda: next(times))
    sign = Mock(wraps=utils.generate_sign)
    monkeypatch.setattr(utils, "generate_sign", sign)
    params, body = {"filter": 0}, {"payload": [1]}
    assert asyncio.run(api._request_with_sign("POST", "/synthetic", params, body)) == {
        "code": 0,
        "data": [],
    }
    assert [send["timestamp"] for send in sends] == [100, 101]
    assert sends[0]["sign"] != sends[1]["sign"]
    assert sign.call_count == 2
    expected_token = "synthetic-token-1" if retry == "auth" else "synthetic-token-0"
    assert sends[1]["access_token"] == expected_token
    assert [call.args[0] for call in sign.call_args_list] == [
        {
            "app_key": "0" * 16,
            "access_token": "synthetic-token-0",
            "timestamp": 100,
            "filter": 0,
            "payload": [1],
        },
        {
            "app_key": "0" * 16,
            "access_token": expected_token,
            "timestamp": 101,
            "filter": 0,
            "payload": [1],
        },
    ]
    assert params == {"filter": 0} and body == {"payload": [1]}
    assert api._UpdateToken.await_count == (1 if retry == "auth" else 0)


def test_body_overrides_common_values_only_in_sign_input(monkeypatch):
    sends = []

    @asynccontextmanager
    async def request(method, url, *, params, json, headers):
        sends.append((deepcopy(params), deepcopy(json)))
        yield SimpleNamespace(
            status=200, read=AsyncMock(return_value=b'{"code":0,"data":[]}')
        )

    api = make_api(request)
    monkeypatch.setattr(utils, "_unix_time", lambda: 100)
    sign = Mock(wraps=utils.generate_sign)
    monkeypatch.setattr(utils, "generate_sign", sign)
    body = {"timestamp": "body-time", "access_token": "synthetic-body-token"}
    asyncio.run(api._request_with_sign("POST", "/synthetic", body=body))
    assert sign.call_args.args[0] == {"app_key": "0" * 16, **body}
    assert (
        sends[0][0]["timestamp"] == 100
        and sends[0][0]["access_token"] == "synthetic-token-0"
    )
    assert sends[0][1] == body


@pytest.mark.parametrize(
    "reachable,error_type",
    [(False, errors.InternetConnectionError), (True, errors.ApiTimeoutError)],
)
def test_base_api_network_error_classification_uses_actual_tcp_helper(
    monkeypatch, reachable, error_type
):
    original = TimeoutError("synthetic request timeout")

    @asynccontextmanager
    async def request(*args, **kwargs):
        raise original
        yield

    api = make_api(request)
    writer = Mock(wait_closed=AsyncMock())
    connector = AsyncMock(return_value=(None, writer))
    if not reachable:
        connector.side_effect = OSError("synthetic connection failure")
    monkeypatch.setattr(asyncio, "open_connection", connector)
    with pytest.raises(error_type) as caught:
        asyncio.run(api._request("GET", "/synthetic", {}))
    assert caught.value.__cause__ is original
    connector.assert_awaited_once_with("119.29.29.29", 53)
