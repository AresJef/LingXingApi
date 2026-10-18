"""Public utils behavior contracts: fixed synthetic inputs, no credentials or network."""

import asyncio
from copy import deepcopy
import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN, ROUND_HALF_UP, localcontext
import hashlib
import math
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest
from Crypto.Cipher import AES
from cytimes import Pydt

from lingxingapi import utils


@pytest.mark.parametrize("text,expected", [
    ("", "D41D8CD98F00B204E9800998ECF8427E"),
    ("abc", "900150983CD24FB0D6963F7D28E17F72"),
    ("中文", "A7BAC2239FCDCB3A067903D8077C4A07"),
    ("a\nb", "8CDEB44417F3C26826595D5820CF5700"),
])
def test_md5_known_digests(text, expected):
    assert utils.md5_encrypt(text) == expected


@pytest.mark.parametrize("name,args,error", [
    ("md5_encrypt", (None,), AttributeError),
    ("md5_encrypt", ("\ud800",), UnicodeEncodeError),
    ("pkc5_pad", (None,), TypeError),
    ("pkc5_pad", ("\ud800",), UnicodeEncodeError),
])
def test_crypto_native_errors(name, args, error):
    with pytest.raises(error):
        getattr(utils, name)(*args)


@pytest.mark.parametrize("text,count", [
    ("", 16), ("a", 15), ("a" * 15, 1), ("a" * 16, 16),
    ("a" * 31, 1), ("a" * 32, 16), ("中", 15), ("🙂", 15),
])
def test_padding_character_length_contract(text, count):
    result = utils.pkc5_pad(text)
    assert type(result) is bytes
    assert result == text.encode("utf-8") + bytes([count]) * count


SIGN_PARAMS = {
    "zero": 0, "tuple": (2, {"z": 2, "a": 1}), "empty_tuple": (),
    "special": " +/", "skip_none": None, "skip_blank": "", "empty_list": [],
    "empty_dict": {}, "d": {"z": "中文", "a": [1, None, True]},
    "b": False, "access_token": "synthetic",
}
# Independent golden inputs: explicit canonical text, hashlib + AES + standard
# Base64/quote_plus, computed before editing utils. No SDK helper generated these.
SIGN_CANONICAL = (
    'access_token=synthetic&b=False&d={"a":[1,null,true],"z":"中文"}'
    '&empty_dict={}&empty_list=[]&empty_tuple=[]&special= +/'
    '&tuple=[2,{"a":1,"z":2}]&zero=0'
)


@pytest.mark.parametrize("key_size,expected", [
    (16, "Mo0JCf7MefH%2FjPUZ6hl%2BoQtY8EtHEZ6iG38pWBD7%2F2Q0a84Lju002hD2qPq7hESU"),
    (24, "datelUt5xwca%2B8i4bMLNegOrE1bDCdNU48qEDKlTgigBK30KCHQwW9WXfBl7Viw6"),
    (32, "Yjh%2FBVxZwJmR%2BWn9eGtYEaXRKmhrJdEyjF2oaDPB4nUDGOCE4WZuaZiRx4%2BKqYlg"),
])
def test_sign_golden_order_and_no_mutation(key_size, expected):
    params = deepcopy(SIGN_PARAMS)
    before = deepcopy(params)
    cipher = AES.new(b"0" * key_size, AES.MODE_ECB)
    assert utils.generate_sign(params, cipher) == expected
    reversed_params = dict(reversed(list(params.items())))
    reversed_params["d"] = {"a": [1, None, True], "z": "中文"}
    assert utils.generate_sign(reversed_params, cipher) == expected
    assert params == before
    assert reversed_params == before


@pytest.mark.parametrize("params,canonical", [
    ({}, ""), ({"omit": None, "empty": ""}, ""),
    ({"n": float("nan"), "p": float("inf"), "m": -float("inf")}, "m=-inf&n=nan&p=inf"),
    ({"nested": [float("nan"), float("inf")]}, 'nested=[null,null]'),
    ({"decimal": Decimal("1.20")}, "decimal=1.20"),
    ({2: "second", 1: "first"}, "1=first&2=second"),
])
def test_sign_exact_cipher_input_and_call_count(params, canonical):
    cipher = Mock()
    cipher.encrypt.return_value = b"\xfb\xff"
    assert utils.generate_sign(params, cipher) == "%2B%2F8%3D"
    digest = hashlib.md5(canonical.encode("utf-8")).hexdigest().upper().encode("ascii")
    cipher.encrypt.assert_called_once_with(digest + b"\x10" * 16)


@pytest.mark.parametrize("params,message", [
    ({"nested": [Decimal("1")]}, "Type is not JSON serializable: decimal.Decimal"),
    ({"nested": {1: "x"}}, "Dict key must be str"),
    ({"a": 1, 2: "x"}, "'<' not supported between instances of 'int' and 'str'"),
])
def test_sign_unsupported_serialization(params, message):
    cipher = Mock()
    with pytest.raises(TypeError) as caught:
        utils.generate_sign(params, cipher)
    assert str(caught.value) == message
    cipher.encrypt.assert_not_called()


def test_sign_cipher_failure_propagates():
    error = RuntimeError("synthetic cipher failure")
    cipher = Mock(encrypt=Mock(side_effect=error))
    with pytest.raises(RuntimeError) as caught:
        utils.generate_sign({"x": 1}, cipher)
    assert caught.value is error


@pytest.mark.parametrize("value,expected", [(1, 1), (1.9, 1), (-1.9, -1), (0.9, 0)])
def test_now_ts_truncates_wall_clock(monkeypatch, value, expected):
    clock = Mock(return_value=value)
    monkeypatch.setattr(utils, "_unix_time", clock)
    assert utils.now_ts() == expected
    assert utils.now_ts() == expected
    assert clock.call_count == 2


class Text(str):
    pass


class Integer(int):
    pass


@pytest.mark.parametrize("name,value,expected", [
    ("validate_str", "", ""), ("validate_str", "  a  ", "  a  "),
    ("validate_str", Text("a"), Text("a")),
    ("validate_non_empty_str", " \t中文\u3000", "中文"),
    ("validate_non_empty_str", Text(" a "), "a"),
    ("validate_int", -1, -1), ("validate_int", 0, 0),
    ("validate_int", True, True), ("validate_int", Integer(3), Integer(3)),
    ("validate_unsigned_int", 0, 0), ("validate_unsigned_int", False, False),
    ("validate_unsigned_int", True, True), ("validate_unsigned_int", Integer(3), Integer(3)),
])
def test_string_integer_scalar_success(name, value, expected):
    result = getattr(utils, name)(value, "value")
    assert result == expected and type(result) is type(expected)
    if name != "validate_non_empty_str":
        assert result is value


@pytest.mark.parametrize("name,value,message", [
    ("validate_str", None, "value 参数必须是 str 类型, 而非 <class 'NoneType'>."),
    ("validate_str", b"a", "value 参数必须是 str 类型, 而非 <class 'bytes'>."),
    ("validate_non_empty_str", 1, "value 参数必须是 str 类型, 而非 <class 'int'>."),
    ("validate_non_empty_str", "", "value 参数必须为非空字符串."),
    ("validate_non_empty_str", " \t\u3000", "value 参数必须为非空字符串."),
    ("validate_int", 1.0, "value 参数必须是 int 类型, 而非 <class 'float'>."),
    ("validate_int", "1", "value 参数必须是 int 类型, 而非 <class 'str'>."),
    ("validate_unsigned_int", -1, "value 参数必须为非负整数, 而非 -1."),
    ("validate_unsigned_int", None, "value 参数必须是 int 类型, 而非 <class 'NoneType'>."),
])
def test_string_integer_scalar_errors(name, value, message):
    with pytest.raises(ValueError) as caught:
        getattr(utils, name)(value, "value")
    assert str(caught.value) == message
    assert caught.value.__cause__ is None and caught.value.__context__ is None


@pytest.mark.parametrize("name,value,expected", [
    ("validate_array_of_str", "", [""]),
    ("validate_array_of_str", ("", "  a  ", "a"), ["", "  a  ", "a"]),
    ("validate_array_of_non_empty_str", " a ", ["a"]),
    ("validate_array_of_non_empty_str", [], []),
    ("validate_array_of_non_empty_str", (), []),
    ("validate_array_of_non_empty_str", [" a ", "a"], ["a", "a"]),
    ("validate_array_of_int", False, [False]),
    ("validate_array_of_int", [-1, 0, True, 0], [-1, 0, True, 0]),
    ("validate_array_of_int", (Integer(1),), [Integer(1)]),
    ("validate_array_of_unsigned_int", 0, [0]),
    ("validate_array_of_unsigned_int", (False, 0, 1, 0), [False, 0, 1, 0]),
])
def test_array_success_preserves_input_types_order_duplicates(name, value, expected):
    before = deepcopy(value)
    result = getattr(utils, name)(value, "value")
    assert type(result) is list and result == expected
    assert [type(x) for x in result] == [type(x) for x in expected]
    assert value == before and result is not value


@pytest.mark.parametrize("name", [
    "validate_array_of_str", "validate_array_of_int", "validate_array_of_unsigned_int",
    "validate_array_of_float", "validate_array_of_unsigned_float",
])
@pytest.mark.parametrize("value", [[], ()])
def test_empty_arrays_rejected(name, value):
    with pytest.raises(ValueError) as caught:
        getattr(utils, name)(value, "value")
    assert str(caught.value) == "value 参数不能为空."


@pytest.mark.parametrize("name,value,kind", [
    ("validate_array_of_str", {"a"}, "set"),
    ("validate_array_of_non_empty_str", None, "NoneType"),
    ("validate_array_of_int", "1", "str"),
    ("validate_array_of_unsigned_int", 1.0, "float"),
    ("validate_array_of_float", 1, "int"),
    ("validate_array_of_float", "1", "str"),
    ("validate_array_of_unsigned_float", Decimal("1"), "Decimal"),
    ("validate_array_of_unsigned_float", 0, "int"),
    ("validate_array_of_unsigned_float", False, "bool"),
    ("validate_array_of_unsigned_float", "0", "str"),
])
def test_array_scalar_restrictions(name, value, kind):
    with pytest.raises(ValueError) as caught:
        getattr(utils, name)(value, "value")
    assert str(caught.value) == f"value 参数必须是列表或元组类型, 而非 <class '{kind if kind != 'Decimal' else 'decimal.Decimal'}'>."


@pytest.mark.parametrize("name,valid,bad,message", [
    ("validate_array_of_str", "a", 1, "value 参数中的元素必须是 str 类型, 而非 <class 'int'>."),
    ("validate_array_of_non_empty_str", "a", " ", "value 参数中的元素必须为非空字符串."),
    ("validate_array_of_int", 1, 1.0, "value 参数中的元素必须是 int 类型, 而非 <class 'float'>."),
    ("validate_array_of_unsigned_int", 1, -1, "value 参数中的元素必须为非负整数, 而非 -1."),
    ("validate_array_of_float", 1.0, None, "value 参数中的元素必须是 float 类型, 而非 <class 'NoneType'>."),
    ("validate_array_of_unsigned_float", 1.0, -1, "value 参数中的元素必须为非负浮点数, 而非 -1.0."),
])
@pytest.mark.parametrize("position", [0, 1, 2])
def test_array_first_error_and_no_mutation(name, valid, bad, message, position):
    value = [valid, valid, valid]
    value[position] = bad
    before = deepcopy(value)
    with pytest.raises(ValueError) as caught:
        getattr(utils, name)(value, "value")
    assert str(caught.value) == message and value == before


class Floatable:
    def __float__(self):
        return 1.25


class BrokenFloat:
    def __float__(self):
        raise RuntimeError("synthetic conversion failure")


@pytest.mark.parametrize("name", ["validate_float", "validate_unsigned_float"])
@pytest.mark.parametrize("value", [1.25, 1, True, "1.25", b"1.25", Decimal("1.25"), Floatable()])
def test_float_conversion_success(name, value):
    result = getattr(utils, name)(value, "value")
    assert type(result) is float
    assert result == (1.0 if value is True or type(value) is int else 1.25)
    if isinstance(value, float):
        assert result is value


@pytest.mark.parametrize("name", ["validate_array_of_float", "validate_array_of_unsigned_float"])
def test_float_array_conversion_and_scalar_asymmetry(name):
    value = [1, "1.25", True, b"1.25", Decimal("1.25"), Floatable()]
    result = getattr(utils, name)(value, "value")
    assert result == [1.0, 1.25, 1.0, 1.25, 1.25, 1.25]
    assert all(type(x) is float for x in result)
    assert type(value[0]) is int and isinstance(value[4], Decimal)
    assert getattr(utils, name)(1.25, "value") == [1.25]


@pytest.mark.parametrize("name,is_array", [
    ("validate_float", False), ("validate_unsigned_float", False),
    ("validate_array_of_float", True), ("validate_array_of_unsigned_float", True),
])
@pytest.mark.parametrize("value", [None, "bad", BrokenFloat()])
def test_float_conversion_error_chain(name, is_array, value):
    with pytest.raises(ValueError) as caught:
        getattr(utils, name)([value] if is_array else value, "value")
    error = caught.value
    kind = repr(type(value))
    fragment = "参数中的元素" if is_array else "参数"
    assert str(error) == f"value {fragment}必须是 float 类型, 而非 {kind}."
    original = error.__context__
    assert type(original) is (RuntimeError if isinstance(value, BrokenFloat) else TypeError if value is None else ValueError)
    # Explicit `from err` keeps both traceback layers for every float conversion.
    assert error.__cause__ is original and error.__suppress_context__ is True


@pytest.mark.parametrize("name,is_array", [
    ("validate_float", False), ("validate_array_of_float", True),
    ("validate_unsigned_float", False), ("validate_array_of_unsigned_float", True),
])
@pytest.mark.parametrize("value", [float("nan"), float("inf")])
def test_nonfinite_positive_float_contract(name, is_array, value):
    result = getattr(utils, name)([value] if is_array else value, "value")
    if is_array:
        result = result[0]
    assert math.isnan(result) if math.isnan(value) else result == value


@pytest.mark.parametrize("is_item", [False, True])
@pytest.mark.parametrize("value", [-1.0, -float("inf")])
def test_unsigned_float_rejections(value, is_item):
    with pytest.raises(ValueError) as caught:
        utils.validate_unsigned_float(value, "value", is_item=is_item)
    fragment = "参数中的元素" if is_item else "参数"
    assert str(caught.value) == f"value {fragment}必须为非负浮点数, 而非 {float(value)}."
    assert caught.value.__cause__ is None and caught.value.__context__ is None


@pytest.mark.parametrize("is_item", [False, True])
@pytest.mark.parametrize("value,sign", [
    (0, 1), (0.0, 1), (-0.0, -1), (False, 1),
    ("0", 1), ("-0", -1), (b"0", 1), (Decimal("0"), 1),
])
def test_unsigned_float_scalar_accepts_zero(value, sign, is_item):
    result = utils.validate_unsigned_float(value, "value", is_item=is_item)
    assert type(result) is float and result == 0.0
    assert math.copysign(1, result) == sign
    if isinstance(value, float):
        assert result is value


@pytest.mark.parametrize("value,sign", [
    (0.0, 1), (-0.0, -1), ([0], 1), ([-0.0], -1), ([False], 1),
    (["0"], 1), (["-0"], -1), ([b"0"], 1), ([Decimal("0")], 1), ((0,), 1),
])
def test_unsigned_float_array_accepts_zero(value, sign):
    before = deepcopy(value)
    result = utils.validate_array_of_unsigned_float(value, "value")
    assert type(result) is list and result == [0.0]
    assert type(result[0]) is float and math.copysign(1, result[0]) == sign
    assert value == before and result is not value


@pytest.mark.parametrize("value", [-1, "-1", -float("inf")])
def test_unsigned_float_array_rejects_negative(value):
    with pytest.raises(ValueError) as caught:
        utils.validate_array_of_unsigned_float([value], "value")
    assert str(caught.value) == f"value 参数中的元素必须为非负浮点数, 而非 {float(value)}."
    assert caught.value.__cause__ is None and caught.value.__context__ is None


def test_unsigned_float_array_zero_keeps_order_duplicates_and_input():
    value = [False, -0.0, "0", 1, 0, "0"]
    before = deepcopy(value)
    result = utils.validate_array_of_unsigned_float(value, "value")
    assert result == [0.0, -0.0, 0.0, 1.0, 0.0, 0.0]
    assert all(type(item) is float for item in result)
    assert math.copysign(1, result[1]) == -1
    assert value == before and [type(item) for item in value] == [type(item) for item in before]


@pytest.mark.parametrize("negative_first", [True, False])
def test_unsigned_float_array_stops_at_first_failure(negative_first):
    broken = BrokenFloat()
    value = [-1, broken] if negative_first else [broken, -1]
    before = list(value)
    with pytest.raises(ValueError) as caught:
        utils.validate_array_of_unsigned_float(value, "value")
    error = caught.value
    if negative_first:
        assert str(error) == "value 参数中的元素必须为非负浮点数, 而非 -1.0."
        assert error.__cause__ is None and error.__context__ is None
    else:
        assert str(error) == f"value 参数中的元素必须是 float 类型, 而非 {type(broken)!r}."
        assert type(error.__cause__) is RuntimeError
        assert str(error.__cause__) == "synthetic conversion failure"
    assert value == before


def test_signed_float_negative_zero_and_negative_values():
    result = utils.validate_float(-0.0, "value")
    assert math.copysign(1, result) == -1
    assert utils.validate_array_of_float([-0.0, -1, False], "value") == [-0.0, -1.0, 0.0]


@pytest.mark.parametrize("value,expected", [
    ("2026", datetime.datetime(2026, 1, 1)),
    ("2026-09", datetime.datetime(2026, 9, 1)),
    ("2026-02-30", datetime.datetime(2026, 2, 28)),
    ("2026-99-99", datetime.datetime(2026, 4, 9)),
    ("09-15", datetime.datetime(1970, 9, 15)),
    ("2026-09-15T03:04:05+08:00", datetime.datetime(2026, 9, 15, 3, 4, 5)),
    (datetime.date(2026, 9, 15), datetime.datetime(2026, 9, 15)),
    (datetime.datetime(2026, 9, 15, 3, 4, 5), datetime.datetime(2026, 9, 15, 3, 4, 5)),
    (Pydt(2026, 9, 15), datetime.datetime(2026, 9, 15)),
    (datetime.datetime(2026, 9, 15, tzinfo=datetime.timezone.utc), datetime.datetime(2026, 9, 15, tzinfo=datetime.timezone.utc)),
    (datetime.datetime(2026, 9, 15, tzinfo=datetime.timezone(datetime.timedelta(hours=8))),
     datetime.datetime(2026, 9, 15, tzinfo=datetime.timezone(datetime.timedelta(hours=8)))),
])
def test_datetime_defaults_fields_and_timezone(value, expected):
    result = utils.validate_datetime(value, False, "value")
    assert type(result) is Pydt and result == expected and result.tzinfo == expected.tzinfo
    assert utils.DEFAULT_DATE == datetime.date(1970, 1, 1)


@pytest.mark.parametrize("value,support", [("", False), ("not-a-date", False), (None, False), (None, True)])
def test_datetime_errors_and_none_contract(value, support):
    with pytest.raises(ValueError) as caught:
        utils.validate_datetime(value, support, "value")
    if value is None and not support:
        assert str(caught.value) == "value 参数不能为 None."
        assert caught.value.__cause__ is None
    else:
        assert str(caught.value) == f"value 参数值 {value!r} 无法被解析为日期对象."
        assert caught.value.__cause__ is not None
        assert caught.value.__cause__ is caught.value.__context__


def test_datetime_parser_error_and_arguments(monkeypatch):
    error = RuntimeError("synthetic parser failure")
    parse = Mock(side_effect=error)
    monkeypatch.setattr(utils, "Pydt", SimpleNamespace(parse=parse))
    with pytest.raises(ValueError) as caught:
        utils.validate_datetime("2026-09", True, "value")
    parse.assert_called_once_with("2026-09", default=datetime.date(1970, 1, 1))
    assert caught.value.__cause__ is error


@pytest.mark.parametrize("value,expected", [
    ("1.2", "1.2000000000"), (1.2, "1.2000000000"), (2, "2.0000000000"),
    (Decimal("1.2300"), "1.2300000000"), ("1e-11", "0E-10"),
])
def test_exchange_rate_exact_type_exponent(value, expected):
    with localcontext() as context:
        context.clear_flags()
        result = utils.validate_exchange_rate(value, "value")
        assert type(result) is Decimal and str(result) == expected
        assert result.as_tuple().exponent == -10


@pytest.mark.parametrize("rounding,expected", [(ROUND_HALF_EVEN, "1.0000000000"), (ROUND_HALF_UP, "1.0000000001")])
def test_exchange_rate_uses_current_context_and_sets_flags(rounding, expected):
    with localcontext() as context:
        context.rounding = rounding
        context.clear_flags()
        result = utils.validate_exchange_rate("1.00000000005", "value")
        assert str(result) == expected
        assert sorted(signal.__name__ for signal, set_ in context.flags.items() if set_) == ["Inexact", "Rounded"]


@pytest.mark.parametrize("value", [True, False, None, "bad"])
def test_exchange_rate_conversion_error_cause(value):
    with localcontext():
        with pytest.raises(ValueError) as caught:
            utils.validate_exchange_rate(value, "value")
        assert str(caught.value) == f"value 参数值 {value!r} 无法被解析为 Decimal 对象."
        assert type(caught.value.__cause__) is InvalidOperation


@pytest.mark.parametrize("value", ["0", "-1", "NaN", "sNaN", "Infinity", "-Infinity"])
def test_exchange_rate_nonpositive_nonfinite_rejected(value):
    with localcontext():
        with pytest.raises(ValueError) as caught:
            utils.validate_exchange_rate(value, "value")
        assert str(caught.value) == f"value 参数值必须为正数, 而非 {Decimal(value)}."
        assert caught.value.__cause__ is None


@pytest.mark.parametrize("value,precision", [("1e100", 28), ("123.456", 5)])
def test_exchange_rate_quantize_exception_not_wrapped(value, precision):
    with localcontext() as context:
        context.prec = precision
        context.clear_flags()
        with pytest.raises(InvalidOperation) as caught:
            utils.validate_exchange_rate(value, "value")
        assert caught.value.__cause__ is None
        assert context.flags[InvalidOperation]


@pytest.mark.parametrize("phase,exception,expected", [
    ("connect", OSError("synthetic"), False),
    ("connect", asyncio.TimeoutError(), False),
    ("connect", asyncio.CancelledError(), asyncio.CancelledError),
    ("close", RuntimeError("synthetic"), RuntimeError),
    ("wait", RuntimeError("synthetic"), True),
    ("wait", asyncio.CancelledError(), asyncio.CancelledError),
    ("success", None, True),
])
def test_tcp_error_cleanup_and_cancellation(monkeypatch, phase, exception, expected):
    writer = Mock(wait_closed=AsyncMock())
    connector = AsyncMock(return_value=(None, writer))
    if phase == "connect":
        connector.side_effect = exception
    elif phase == "close":
        writer.close.side_effect = exception
    elif phase == "wait":
        writer.wait_closed.side_effect = exception
    monkeypatch.setattr(asyncio, "open_connection", connector)
    if isinstance(expected, type):
        with pytest.raises(expected) as caught:
            asyncio.run(utils.check_internet_tcp("synthetic.invalid", 1234, 1))
        assert caught.value is exception
    else:
        assert asyncio.run(utils.check_internet_tcp("synthetic.invalid", 1234, 1)) is expected
    connector.assert_awaited_once_with("synthetic.invalid", 1234)
    if phase == "connect":
        writer.close.assert_not_called()
        writer.wait_closed.assert_not_awaited()
    else:
        writer.close.assert_called_once_with()
        assert writer.wait_closed.await_count == (0 if phase == "close" else 1)


def test_tcp_connection_timeout_and_unbounded_close_are_distinct(monkeypatch):
    async def scenario():
        wait_started = asyncio.Event()
        release = asyncio.Event()
        async def wait_closed():
            wait_started.set()
            await release.wait()
        writer = Mock(wait_closed=AsyncMock(side_effect=wait_closed))
        monkeypatch.setattr(asyncio, "open_connection", AsyncMock(return_value=(None, writer)))
        # An exact mocked wait_for verifies only the connection is given the
        # configured timeout. Event coordination avoids sleeps and timing races.
        real_wait_for = asyncio.wait_for
        connection_deadline = Mock()
        async def deadline(coro, timeout):
            connection_deadline(timeout=timeout)
            return await coro
        monkeypatch.setattr(asyncio, "wait_for", deadline)
        task = asyncio.create_task(utils.check_internet_tcp(timeout=0.01))
        await real_wait_for(wait_started.wait(), timeout=1)
        assert not task.done()
        connection_deadline.assert_called_once()
        assert connection_deadline.call_args.kwargs == {"timeout": 0.01}
        release.set()
        assert await real_wait_for(task, timeout=1) is True
    asyncio.run(scenario())


FUNCTION_NAMES = (
    "md5_encrypt", "pkc5_pad", "generate_sign", "check_internet_tcp", "now_ts",
    "validate_str", "validate_array_of_str", "validate_non_empty_str",
    "validate_array_of_non_empty_str", "validate_int", "validate_array_of_int",
    "validate_unsigned_int", "validate_array_of_unsigned_int", "validate_float",
    "validate_array_of_float", "validate_unsigned_float", "validate_array_of_unsigned_float",
    "validate_datetime", "validate_exchange_rate",
)


@pytest.mark.parametrize("name", FUNCTION_NAMES)
def test_public_annotations_and_google_sections(name):
    import inspect
    from typing import Any, get_type_hints

    fn = getattr(utils, name)
    hints = get_type_hints(fn)
    signature = inspect.signature(fn)
    assert set(hints) == {*signature.parameters, "return"}
    returns = {
        "md5_encrypt": str, "pkc5_pad": bytes, "generate_sign": str,
        "check_internet_tcp": bool, "now_ts": int, "validate_datetime": Pydt,
        "validate_exchange_rate": Decimal,
    }
    expected_return = returns.get(name, list[str] if "array" in name and "str" in name
                                  else list[int] if "array" in name and "int" in name
                                  else list[float] if "array" in name
                                  else str if "str" in name else int if "int" in name else float)
    assert hints["return"] == expected_return
    assert "Returns:" in fn.__doc__ and "Examples:" in fn.__doc__
    if signature.parameters:
        assert "Args:" in fn.__doc__
        args = fn.__doc__.split("Args:", 1)[1].split("Returns:", 1)[0]
        assert all(f"{parameter}:" in args for parameter in signature.parameters)
    else:
        assert "Args:" not in fn.__doc__
    for hint in hints.values():
        assert not (getattr(hint, "__args__", ()) and Any in hint.__args__)
    if name in ("validate_float", "validate_unsigned_float"):
        assert hints["param"] is Any  # Deliberate dynamic float() boundary.
    elif name.startswith("validate") and name != "validate_datetime":
        assert hints[next(iter(signature.parameters))] is object
    assert inspect.iscoroutinefunction(fn) == (name == "check_internet_tcp")


@pytest.mark.parametrize("name", FUNCTION_NAMES)
def test_google_examples_execute_offline(name, monkeypatch):
    import doctest
    import inspect

    monkeypatch.setattr(utils, "_unix_time", lambda: 100)
    tests = doctest.DocTestFinder().find(getattr(utils, name), name=name, globs=vars(utils))
    assert len(tests) == 1 and tests[0].examples
    runner = doctest.DocTestRunner()
    with localcontext() as context:
        context.prec = 28
        context.rounding = ROUND_HALF_EVEN
        result = runner.run(tests[0])
    assert result.failed == 0 and result.attempted > 0



@pytest.mark.parametrize("timeout", [0, -1])
def test_tcp_nonpositive_timeout_cancels_connect(monkeypatch, timeout):
    connector = AsyncMock(return_value=(None, Mock()))
    monkeypatch.setattr(asyncio, "open_connection", connector)
    assert asyncio.run(utils.check_internet_tcp(timeout=timeout)) is False
    connector.assert_called_once_with("119.29.29.29", 53)
    connector.assert_not_awaited()


def test_exchange_rate_quantize_respects_disabled_trap():
    with localcontext() as context:
        context.traps[InvalidOperation] = False
        context.clear_flags()
        result = utils.validate_exchange_rate("1e100", "value")
        assert result.is_nan() and context.flags[InvalidOperation]


@pytest.mark.parametrize("name", [
    "validate_array_of_str", "validate_array_of_non_empty_str",
    "validate_array_of_int", "validate_array_of_unsigned_int",
    "validate_array_of_float", "validate_array_of_unsigned_float",
])
def test_arrays_reject_generators_without_consuming_them(name):
    value = iter([1, 2])
    with pytest.raises(ValueError):
        getattr(utils, name)(value, "value")
    assert next(value) == 1


def test_array_stops_at_first_conversion_error():
    later = Mock()
    later.__float__ = Mock(return_value=1.0)
    with pytest.raises(ValueError) as caught:
        utils.validate_array_of_float(["bad", later], "value")
    assert str(caught.value) == "value 参数中的元素必须是 float 类型, 而非 <class 'str'>."
    later.__float__.assert_not_called()


@pytest.mark.parametrize("phase", ["connect", "wait"])
def test_tcp_task_cancellation_preserves_cleanup(monkeypatch, phase):
    async def scenario():
        started = asyncio.Event()
        async def pending():
            started.set()
            await asyncio.Event().wait()
        writer = Mock(wait_closed=AsyncMock(side_effect=pending if phase == "wait" else None))
        async def connect(*args):
            if phase == "connect":
                await pending()
            return None, writer
        monkeypatch.setattr(asyncio, "open_connection", connect)
        task = asyncio.create_task(utils.check_internet_tcp(timeout=1))
        await asyncio.wait_for(started.wait(), timeout=1)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await asyncio.wait_for(task, timeout=1)
        assert writer.close.call_count == (0 if phase == "connect" else 1)
        assert writer.wait_closed.await_count == (0 if phase == "connect" else 1)
    asyncio.run(scenario())


