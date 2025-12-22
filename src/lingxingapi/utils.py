# -*- coding: utf-8 -*-c
import asyncio
import datetime
from typing import Any
from decimal import Decimal
from time import time as _unix_time
from hashlib import md5 as _hashlib_md5
from base64 import b64encode as _b64encode
from urllib.parse import quote_plus as _urllib_quote
from cytimes import Pydt
from Crypto.Cipher import AES
from Crypto.Cipher._mode_ecb import EcbMode
from orjson import dumps as _orjson_dumps, OPT_SORT_KEYS


# Constants ------------------------------------------------------------------------------------------------------------
BLOCK_SIZE: int = AES.block_size
DEFAULT_DATE: datetime.date = datetime.date(1970, 1, 1)


# Cryptography ---------------------------------------------------------------------------------------------------------
def md5_encrypt(text: str) -> str:
    """对字符串进行 MD5 加密

    :param text `<'str'>`: 要加密的字符串
    :returns `<'str'>`: 返回加密后大写的十六进制字符串
    """
    return _hashlib_md5(text.encode("utf-8")).hexdigest().upper()


def pkc5_pad(text: str) -> str:
    """对字符串进行 PKCS#5 填充

    :param text `<'str'>`: 要填充的字符串
    :returns `<'bytes'>`: 返回填充后的字节串 (utf-8编码)
    """
    length: int = len(text)
    text += (BLOCK_SIZE - length % BLOCK_SIZE) * chr(BLOCK_SIZE - length % BLOCK_SIZE)
    return text.encode("utf-8")


def generate_sign(params: dict, app_cipher: EcbMode) -> str:
    """根据参数生成请求签名

    :param params `<'dict'>`: 请求参数字典, 包含公共参数和业务参数
    :param app_cipher `<'EcbMode'>`: 基于 appId 创建 AES-ECB 加密器
    :returns `<'str'>`: 返回生成的签名字符串, 用于请求验证

    ## 签名步骤
    1. 按ASCII排序 params, 并过滤 None 或空字符串
    2. 将参数转换为字符串格式, 如 `key=value` 的形式.
       若参数值为字典或列表, 则使用 `orjson.dumps` 序列化为 JSON 字符串
    3. 将所有参数字符串连接成一个以 `&` 分隔的字符串
    4. 对连接后的字符串使用 `hashlib.md5` 计算 MD5 值, 并转换为大写十六进制字符串
    5. 使用 AES-ECB 模式加密 MD5 字符串, 使用 PKCS#5 填充
    6. 对加密结果进行 Base64 编码, 并进行 URL 安全的编码
    """
    # 1–3: 对参数进行排序, 并转换为字符串
    items: list = []
    for key in sorted(params.keys()):
        val = params[key]
        if val is None or val == "":
            continue
        if isinstance(val, (dict, list, tuple)):
            val = _orjson_dumps(val, option=OPT_SORT_KEYS).decode("utf-8")
        items.append("%s=%s" % (key, val))
    canonical: str = "&".join(items)

    # 4: 使用 hashlib.md5 计算字符串的 MD5 值, 并转换为大写十六进制字符串
    md5hex: str = md5_encrypt(canonical)

    # 5: AES-ECB加密, 使用 PKCS#5 填充
    encrypt: bytes = app_cipher.encrypt(pkc5_pad(md5hex))

    # 6: 使用 base64 编码, 并进行 URL 安全的编码
    return _urllib_quote(_b64encode(encrypt).decode("utf-8"), safe="")


# Network --------------------------------------------------------------------------------------------------------------
async def check_internet_tcp(
    host: str = "119.29.29.29",
    port: int = 53,
    timeout: float = 3.0,
) -> bool:
    """Check basic network reachability by opening a TCP connection to a DNS endpoint `<'bool'>`.

    This function attempts to establish a TCP socket connection to `host:port`
    (by default, a public DNS resolver on port 53). If the TCP handshake succeeds
    within `timeout`, the function closes the connection and returns `True`.
    Otherwise (timeout or OS-level network error), it returns `False`.

    **Important**
    - This checks **TCP connectivity** to a specific endpoint, not general “internet
      availability”.
    - Many DNS resolvers primarily serve queries over **UDP/53**; some networks may
      block TCP/53, or block direct access to public resolvers, while internet access
      still works through other resolvers or via DoH/DoT.
    - A `True` result indicates the target endpoint is reachable over TCP, not that
      DNS queries succeed or that HTTP(S) is reachable.

    :param host `<'str'>`: Target host/IP to connect to. Defaults to `'119.29.29.29'`.
    :param port `<'int'>`: Target TCP port. Defaults to `'53'`.
    :param timeout `<'float'>`: Maximum time in seconds to wait for the connection
        attempt. Defaults to `3.0`.
    :return `<'bool'>`: `True` if a TCP connection to `host:port` is established
        within `timeout`, otherwise `False`.
    """
    try:
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=timeout
        )
    except (OSError, asyncio.TimeoutError):
        return False
    else:
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass
        return True


# Date & Time ----------------------------------------------------------------------------------------------------------
def now_ts() -> int:
    """获取当前 Unix 时间戳 (秒)

    :returns `<'int'>`: 返回当前 Unix 时间戳, 单位为秒
    """
    return int(_unix_time())


# Validator ------------------------------------------------------------------------------------------------------------
def validate_str(param: str | Any, param_name: str) -> str:
    """验证参数是否为字符串

    :param param `<'str'>`: 要验证的参数
    :param param_name `<'str'>`: 参数名称, 用于构建错误信息
    :returns `<'str'>`: 返回验证后的字符串
    """
    if not isinstance(param, str):
        raise ValueError("%s 参数必须是 str 类型, 而非 %s." % (param_name, type(param)))
    return param


def validate_array_of_str(
    array: str | list | tuple | Any,
    param_name: str,
) -> list[str]:
    """验证参数是否为字符串列表或元组

    :param array `<'str/list/tuple'>`: 要验证的参数
    :param param_name `<'str'>`: 参数名称, 用于构建错误信息
    :returns `<'list[str]'>`: 返回验证后的字符串列表
    """
    if not isinstance(array, (list, tuple)):
        if not isinstance(array, str):
            raise ValueError(
                "%s 参数必须是列表或元组类型, 而非 %s." % (param_name, type(array))
            )
        array = [array]
    elif not array:
        raise ValueError("%s 参数不能为空." % param_name)
    res: list = []
    for i in array:
        if not isinstance(i, str):
            raise ValueError(
                "%s 参数中的元素必须是 str 类型, 而非 %s." % (param_name, type(i))
            )
        res.append(i)
    return res


def validate_non_empty_str(param: str | Any, param_name: str) -> str:
    """验证参数是否为非空字符串

    :param param `<'str'>`: 要验证的参数
    :param param_name `<'str'>`: 参数名称, 用于构建错误信息
    :returns `<'str'>`: 返回验证后的非空字符串
    """
    if not isinstance(param, str):
        raise ValueError("%s 参数必须是 str 类型, 而非 %s." % (param_name, type(param)))
    if not (param := param.strip()):
        raise ValueError("%s 参数必须为非空字符串." % param_name)
    return param


def validate_array_of_non_empty_str(
    array: str | list | tuple | Any,
    param_name: str,
) -> list[str]:
    """验证参数是否为非空字符串列表或元组

    :param array `<'str/list/tuple'>`: 要验证的参数
    :param param_name `<'str'>`: 参数名称, 用于构建错误信息
    :returns `<'list[str]'>`: 返回验证后的非空字符串列表
    """
    if not isinstance(array, (list, tuple)):
        if not isinstance(array, str):
            raise ValueError(
                "%s 参数必须是列表或元组类型, 而非 %s." % (param_name, type(array))
            )
        array = [array]
    res: list = []
    for i in array:
        if not isinstance(i, str):
            raise ValueError(
                "%s 参数中的元素必须是 str 类型, 而非 %s." % (param_name, type(i))
            )
        if not (i := i.strip()):
            raise ValueError("%s 参数中的元素必须为非空字符串." % param_name)
        res.append(i)
    return res


def validate_int(param: int | Any, param_name: str) -> int:
    """验证参数是否为整数

    :param param `<'int'>`: 要验证的参数
    :param param_name `<'str'>`: 参数名称, 用于构建错误信息
    :returns `<'int'>`: 返回验证后的整数
    """
    if not isinstance(param, int):
        raise ValueError("%s 参数必须是 int 类型, 而非 %s." % (param_name, type(param)))
    return param


def validate_array_of_int(
    array: int | list | tuple | Any,
    param_name: str,
) -> list[int]:
    """验证参数是否为整数列表或元组

    :param array `<'int/list/tuple'>`: 要验证的参数
    :param param_name `<'str'>`: 参数名称, 用于构建错误信息
    :returns `<'list[int]'>`: 返回验证后的整数列表
    """
    if not isinstance(array, (list, tuple)):
        if not isinstance(array, int):
            raise ValueError(
                "%s 参数必须是列表或元组类型, 而非 %s." % (param_name, type(array))
            )
        array = [array]
    elif not array:
        raise ValueError("%s 参数不能为空." % param_name)
    res: list = []
    for i in array:
        if not isinstance(i, int):
            raise ValueError(
                "%s 参数中的元素必须是 int 类型, 而非 %s." % (param_name, type(i))
            )
        res.append(i)
    return res


def validate_unsigned_int(param: int | Any, param_name: str) -> int:
    """验证参数是否为正整数

    :param param `<'int'>`: 要验证的参数
    :param param_name `<'str'>`: 参数名称, 用于构建错误信息
    :returns `<'int'>`: 返回验证后的正整数
    """
    if not isinstance(param, int):
        raise ValueError("%s 参数必须是 int 类型, 而非 %s." % (param_name, type(param)))
    if param < 0:
        raise ValueError("%s 参数必须为正整数, 而非 %s." % (param_name, param))
    return param


def validate_array_of_unsigned_int(
    array: int | list | tuple | Any,
    param_name: str,
) -> list[int]:
    """验证参数是否为正整数列表或元组

    :param array `<'int/list/tuple'>`: 要验证的参数
    :param param_name `<'str'>`: 参数名称, 用于构建错误信息
    :returns `<'list[int]'>`: 返回验证后的正整数列表
    """
    if not isinstance(array, (list, tuple)):
        if not isinstance(array, int):
            raise ValueError(
                "%s 参数必须是列表或元组类型, 而非 %s." % (param_name, type(array))
            )
        array = [array]
    elif not array:
        raise ValueError("%s 参数不能为空." % param_name)
    res: list = []
    for i in array:
        if not isinstance(i, int):
            raise ValueError(
                "%s 参数中的元素必须是 int 类型, 而非 %s." % (param_name, type(i))
            )
        if i < 0:
            raise ValueError("%s 参数中的元素必须为正整数." % param_name)
        res.append(i)
    return res


def validate_float(param: float | Any, param_name: str) -> float:
    """验证参数是否为浮点数

    :param param `<'float'>`: 要验证的参数
    :param param_name `<'str'>`: 参数名称, 用于构建错误信息
    :returns `<'float'>`: 返回验证后的浮点数
    """
    if not isinstance(param, float):
        try:
            param = float(param)
        except Exception:
            raise ValueError(
                "%s 参数必须是 float 类型, 而非 %s." % (param_name, type(param))
            )
    return param


def validate_array_of_float(
    array: float | list | tuple | Any,
    param_name: str,
) -> list[float]:
    """验证参数是否为浮点数列表或元组

    :param array `<'float/list/tuple'>`: 要验证的参数
    :param param_name `<'str'>`: 参数名称, 用于构建错误信息
    :returns `<'list[float]'>`: 返回验证后的浮点数列表
    """
    if not isinstance(array, (list, tuple)):
        if not isinstance(array, float):
            raise ValueError(
                "%s 参数必须是列表或元组类型, 而非 %s." % (param_name, type(array))
            )
        array = [array]
    elif not array:
        raise ValueError("%s 参数不能为空." % param_name)
    res: list = []
    for i in array:
        if not isinstance(i, float):
            try:
                i = float(i)
            except Exception:
                raise ValueError(
                    "%s 参数中的元素必须是 float 类型, 而非 %s." % (param_name, type(i))
                )
        res.append(i)
    return res


def validate_unsigned_float(param: float | Any, param_name: str) -> float:
    """验证参数是否为正浮点数

    :param param `<'float'>`: 要验证的参数
    :param param_name `<'str'>`: 参数名称, 用于构建错误信息
    :returns `<'float'>`: 返回验证后的正浮点数
    """
    if not isinstance(param, float):
        try:
            param = float(param)
        except Exception:
            raise ValueError(
                "%s 参数必须是 float 类型, 而非 %s." % (param_name, type(param))
            )
    if param <= 0:
        raise ValueError("%s 参数必须为正浮点数, 而非 %s." % (param_name, param))
    return param


def validate_array_of_unsigned_float(
    array: float | list | tuple | Any,
    param_name: str,
) -> list[float]:
    """验证参数是否为正浮点数列表或元组

    :param array `<'float/list/tuple'>`: 要验证的参数
    :param param_name `<'str'>`: 参数名称, 用于构建错误信息
    :returns `<'list[float]'>`: 返回验证后的正浮点数列表
    """
    if not isinstance(array, (list, tuple)):
        if not isinstance(array, float):
            raise ValueError(
                "%s 参数必须是列表或元组类型, 而非 %s." % (param_name, type(array))
            )
        array = [array]
    elif not array:
        raise ValueError("%s 参数不能为空." % param_name)
    res: list = []
    for i in array:
        if not isinstance(i, float):
            try:
                i = float(i)
            except Exception:
                raise ValueError(
                    "%s 参数中的元素必须是 float 类型, 而非 %s." % (param_name, type(i))
                )
        if i <= 0:
            raise ValueError("%s 参数中的元素必须为正浮点数." % param_name)
        res.append(i)
    return res


def validate_datetime(
    dt: str | datetime.date | datetime.datetime | None,
    support_none: bool,
    param_name: str,
) -> Pydt:
    """检验并解析日期字符串或日期对象

    :param dt `<'str/date/datetime'>`: 日期字符串或日期对象

        - 如果是字符串, 必须是有效的日期字符串, 如: `"2025-07"`, `"2025-07-01"`
        - 如果是 `date` 或 `datetime` 对象, 将自动转换为 `YYYY-MM` 格式
        - 如果为 `None`, 则使用当前月份作为参数

    :param support_none `<'bool'>`: 是否支持参数 `dt` 为 `None`
    :param param_name `<'str'>`: 参数名称, 用于构建错误信息
    :returns `<'Pydt'>`: 返回一个 `Pydt` 的 datetime 对象
    """
    if not support_none and dt is None:
        raise ValueError("%s 参数不能为 None." % param_name)
    try:
        return Pydt.parse(dt, default=DEFAULT_DATE)
    except Exception as err:
        raise ValueError(
            "%s 参数值 %r 无法被解析为日期对象." % (param_name, dt)
        ) from err


def validate_exchange_rate(rate: str | float | Decimal, param_name: str) -> Decimal:
    """检验并解析汇率字符串或数字

    :param rate `<'str/float/Decimal'>`: 汇率字符串或数字
    :param param_name `<'str'>`: 参数名称, 用于构建错误信息
    :returns `<'Decimal'>`: 返回一个精确的 Decimal 对象
    """
    if isinstance(rate, float):
        try:
            rate = Decimal(str(rate))
        except Exception as err:
            raise ValueError(
                "%s 参数值 %r 无法被解析为 Decimal 对象." % (param_name, rate)
            ) from err
    elif isinstance(rate, str):
        try:
            rate = Decimal(rate)
        except Exception as err:
            raise ValueError(
                "%s 参数值 %r 无法被解析为 Decimal 对象." % (param_name, rate)
            ) from err
    elif not isinstance(rate, Decimal):
        try:
            rate = Decimal(str(rate))
        except Exception as err:
            raise ValueError(
                "%s 参数值 %r 无法被解析为 Decimal 对象." % (param_name, rate)
            ) from err
    if not rate.is_finite() or rate <= 0:
        raise ValueError("%s 参数值必须为正整数, 而非 %s." % (param_name, rate))
    return rate.quantize(Decimal("0.0000000000"))  # 保留10位小数
