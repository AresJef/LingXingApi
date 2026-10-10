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
    """计算字符串的 UTF-8 MD5 摘要。

    Args:
        text: 要计算摘要的字符串。

    Returns:
        str: 大写的 32 位十六进制摘要。

    Raises:
        UnicodeEncodeError: text 无法编码为 UTF-8。

    Examples:
        >>> md5_encrypt("abc")
        '900150983CD24FB0D6963F7D28E17F72'
    """
    return _hashlib_md5(text.encode("utf-8")).hexdigest().upper()


def pkc5_pad(text: str) -> bytes:
    """按字符串字符数填充到 16 的倍数，再编码为 UTF-8 字节串。

    填充长度按 len(text) 而非 UTF-8 字节长度计算；非 ASCII 输出不保证
    字节数为 16 的倍数。签名流程传入 ASCII MD5 摘要，整块输入仍补一整块。

    Args:
        text: 要填充的字符串。

    Returns:
        bytes: 添加填充字符后编码为 UTF-8 的结果。

    Raises:
        UnicodeEncodeError: text 无法编码为 UTF-8。

    Examples:
        >>> pkc5_pad("").hex()
        '10101010101010101010101010101010'
    """
    length: int = len(text)
    padding_len: int = BLOCK_SIZE - length % BLOCK_SIZE
    text += padding_len * chr(padding_len)
    return text.encode("utf-8")


def generate_sign(params: dict[str, object], app_cipher: EcbMode) -> str:
    """按领星请求协议生成签名，不修改参数字典。

    先按 Python 键顺序排序，仅跳过 None 或等于空串的值。dict/list/tuple
    由 orjson 按嵌套字典键排序序列化，其余值按字符串格式化；False、零和
    空容器均保留。随后连接 key=value、计算大写 MD5、填充、AES-ECB 加密、
    Base64 编码，再以 quote_plus(safe="") 编码。每次调用重新生成签名。

    Args:
        params: 含公共参数和业务参数的字典；SDK 使用字符串键。
        app_cipher: 基于 appId 创建的 AES-ECB 加密器。

    Returns:
        str: URL 编码后的请求签名。

    Raises:
        TypeError: 键无法排序或嵌套值不能由 orjson 序列化。
        ValueError: 加密器拒绝输入。

    Examples:
        >>> cipher = AES.new(b"0" * 16, AES.MODE_ECB)
        >>> isinstance(generate_sign({"value": 0}, cipher), str)
        True
    """
    # 1–3: 对参数进行排序, 并转换为字符串
    items: list[str] = []
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
    """尝试建立 TCP 连接，判断指定端点是否可达。

    timeout 只限制连接阶段；成功后关闭 writer 并等待关闭，该等待没有超时。
    wait_closed() 的普通异常被忽略，close() 的异常与任务取消原样传播。
    端点 TCP 可达不保证 DNS 查询或 HTTP 请求成功。

    Args:
        host: 目标主机或 IP，默认 119.29.29.29。
        port: 目标 TCP 端口，默认 53。
        timeout: 连接阶段的超时秒数，默认 3.0。

    Returns:
        bool: 连接成功返回 True；连接 OSError 或超时返回 False。

    Raises:
        asyncio.CancelledError: 连接或关闭等待期间任务被取消。
        Exception: writer.close() 抛出的异常，或其他未捕获错误。

    Examples:
        使用模拟连接演示，避免访问外部端点。
        >>> from unittest.mock import AsyncMock, Mock, patch
        >>> writer = Mock(wait_closed=AsyncMock())
        >>> with patch("asyncio.open_connection", AsyncMock(return_value=(None, writer))):
        ...     asyncio.run(check_internet_tcp())
        True
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
    """取得墙上时钟的 Unix 时间戳，按 int 截断到秒。

    Returns:
        int: 当前 Unix 秒数，不是单调时钟值。

    Examples:
        >>> isinstance(now_ts(), int)
        True
    """
    return int(_unix_time())


# Validator ------------------------------------------------------------------------------------------------------------
def validate_str(param: object, param_name: str, *, is_item: bool = False) -> str:
    """校验字符串并返回原值，允许空串及空白。

    Args:
        param: 待校验的原始值；接受 str 及其子类。
        param_name: 用于构建错误信息的参数名称。
        is_item: 为 True 时使用数组元素的错误描述；默认 False，不改变有效结果。

    Returns:
        str: 原字符串，不裁剪空白或转换类型。

    Raises:
        ValueError: param 不是字符串。

    Examples:
        >>> validate_str("  a  ", "value")
        '  a  '
        >>> validate_str(None, "value", is_item=True)
        Traceback (most recent call last):
            ...
        ValueError: value 参数中的元素必须是 str 类型, 而非 <class 'NoneType'>.
    """
    if not isinstance(param, str):
        if is_item:
            err_msg = "%s 参数中的元素必须是 str 类型, 而非 %s."
        else:
            err_msg = "%s 参数必须是 str 类型, 而非 %s."
        raise ValueError(err_msg % (param_name, type(param)))
    return param


def validate_array_of_str(
    array: object,
    param_name: str,
) -> list[str]:
    """将字符串或非空 list/tuple 校验为字符串列表。

    Args:
        array: 单个字符串或字符串 list/tuple；元素可为空串。
        param_name: 用于构建错误信息的参数名称。

    Returns:
        list[str]: 新列表，保留空白、顺序和重复项，不修改输入。

    Raises:
        ValueError: 输入类型不符、容器为空，或元素不是字符串。

    Examples:
        >>> validate_array_of_str(("", " a "), "value")
        ['', ' a ']
    """
    if not isinstance(array, (list, tuple)):
        if not isinstance(array, str):
            err_msg = "%s 参数必须是列表或元组类型, 而非 %s."
            raise ValueError(err_msg % (param_name, type(array)))
        array = [array]
    elif not array:
        raise ValueError("%s 参数不能为空." % param_name)

    return [validate_str(i, param_name, is_item=True) for i in array]


def validate_non_empty_str(
    param: object,
    param_name: str,
    *,
    is_item: bool = False,
) -> str:
    """裁剪字符串两端的空白，并拒绝裁剪后的空串。

    Args:
        param: 待校验的原始值；接受 str 及其子类。
        param_name: 用于构建错误信息的参数名称。
        is_item: 为 True 时使用数组元素的错误描述；默认 False，不改变有效结果。

    Returns:
        str: strip() 后的非空字符串。

    Raises:
        ValueError: param 不是字符串或裁剪后为空。

    Examples:
        >>> validate_non_empty_str("  a  ", "value")
        'a'
        >>> validate_non_empty_str(None, "value", is_item=True)
        Traceback (most recent call last):
            ...
        ValueError: value 参数中的元素必须是 str 类型, 而非 <class 'NoneType'>.
    """
    if not isinstance(param, str):
        if is_item:
            err_msg = "%s 参数中的元素必须是 str 类型, 而非 %s."
        else:
            err_msg = "%s 参数必须是 str 类型, 而非 %s."
        raise ValueError(err_msg % (param_name, type(param)))
    if not (param := param.strip()):
        if is_item:
            err_msg = "%s 参数中的元素必须为非空字符串."
        else:
            err_msg = "%s 参数必须为非空字符串."
        raise ValueError(err_msg % param_name)
    return param


def validate_array_of_non_empty_str(
    array: object,
    param_name: str,
) -> list[str]:
    """将字符串或 list/tuple 的元素裁剪并校验为非空字符串。

    Args:
        array: 单个字符串或字符串 list/tuple；允许空容器。
        param_name: 用于构建错误信息的参数名称。

    Returns:
        list[str]: 裁剪后的新列表，保留顺序和重复项；空容器返回 []。

    Raises:
        ValueError: 输入类型不符，或元素不是字符串、裁剪后为空。

    Examples:
        >>> validate_array_of_non_empty_str([" a ", "a"], "value")
        ['a', 'a']
        >>> validate_array_of_non_empty_str([], "value")
        []
    """
    if not isinstance(array, (list, tuple)):
        if not isinstance(array, str):
            err_msg = "%s 参数必须是列表或元组类型, 而非 %s."
            raise ValueError(err_msg % (param_name, type(array)))
        array = [array]

    return [validate_non_empty_str(i, param_name, is_item=True) for i in array]


def validate_int(param: object, param_name: str, *, is_item: bool = False) -> int:
    """校验 Python 整数并返回原值，允许 bool、零和负数。

    Args:
        param: 待校验的原始值；接受 int 及其子类。
        param_name: 用于构建错误信息的参数名称。
        is_item: 为 True 时使用数组元素的错误描述；默认 False，不改变有效结果。

    Returns:
        int: 原整数对象，不将 bool 转为 0/1。

    Raises:
        ValueError: param 不是 int 或其子类。

    Examples:
        >>> validate_int(True, "value")
        True
        >>> validate_int(None, "value", is_item=True)
        Traceback (most recent call last):
            ...
        ValueError: value 参数中的元素必须是 int 类型, 而非 <class 'NoneType'>.
    """
    if not isinstance(param, int):
        if is_item:
            err_msg = "%s 参数中的元素必须是 int 类型, 而非 %s."
        else:
            err_msg = "%s 参数必须是 int 类型, 而非 %s."
        raise ValueError(err_msg % (param_name, type(param)))
    return param


def validate_array_of_int(
    array: object,
    param_name: str,
) -> list[int]:
    """将整数或非空 list/tuple 校验为整数列表。

    Args:
        array: 单个 int 或整数 list/tuple；允许 bool、零和负数。
        param_name: 用于构建错误信息的参数名称。

    Returns:
        list[int]: 新列表，保留元素的类型、顺序和重复项。

    Raises:
        ValueError: 输入类型不符、容器为空，或元素不是 int。

    Examples:
        >>> validate_array_of_int((-1, False, 0), "value")
        [-1, False, 0]
    """
    if not isinstance(array, (list, tuple)):
        if not isinstance(array, int):
            raise ValueError(
                "%s 参数必须是列表或元组类型, 而非 %s." % (param_name, type(array))
            )
        array = [array]
    elif not array:
        raise ValueError("%s 参数不能为空." % param_name)

    return [validate_int(i, param_name, is_item=True) for i in array]


def validate_unsigned_int(
    param: object,
    param_name: str,
    *,
    is_item: bool = False,
) -> int:
    """校验非负整数，允许零和 bool。

    Args:
        param: 待校验的原始值；接受非负 int 及其子类。
        param_name: 用于构建错误信息的参数名称。
        is_item: 为 True 时使用数组元素的错误描述；默认 False，不改变有效结果。

    Returns:
        int: 原整数对象，不进行数值转换。

    Raises:
        ValueError: param 不是 int 或为负数；错误包含失败类型或负数值。

    Examples:
        >>> validate_unsigned_int(0, "value")
        0
        >>> validate_unsigned_int(-1, "value")
        Traceback (most recent call last):
            ...
        ValueError: value 参数必须为非负整数, 而非 -1.
        >>> validate_unsigned_int(-1, "value", is_item=True)
        Traceback (most recent call last):
            ...
        ValueError: value 参数中的元素必须为非负整数, 而非 -1.
    """
    if not isinstance(param, int):
        if is_item:
            err_msg = "%s 参数中的元素必须是 int 类型, 而非 %s."
        else:
            err_msg = "%s 参数必须是 int 类型, 而非 %s."
        raise ValueError(err_msg % (param_name, type(param)))
    if param < 0:
        if is_item:
            err_msg = "%s 参数中的元素必须为非负整数, 而非 %s."
        else:
            err_msg = "%s 参数必须为非负整数, 而非 %s."
        raise ValueError(err_msg % (param_name, param))
    return param


def validate_array_of_unsigned_int(
    array: object,
    param_name: str,
) -> list[int]:
    """将非负整数或非空 list/tuple 校验为整数列表。

    Args:
        array: 单个非负 int 或其 list/tuple；允许零和 bool。
        param_name: 用于构建错误信息的参数名称。

    Returns:
        list[int]: 新列表，保留元素类型、顺序和重复项，不修改输入。

    Raises:
        ValueError: 输入类型不符、容器为空，或元素不是非负 int。
            负数错误描述为非负整数，并包含首个失败元素的值。

    Examples:
        >>> validate_array_of_unsigned_int((0, False, 2, 2), "value")
        [0, False, 2, 2]
        >>> validate_array_of_unsigned_int([0, -1], "value")
        Traceback (most recent call last):
            ...
        ValueError: value 参数中的元素必须为非负整数, 而非 -1.
    """
    if not isinstance(array, (list, tuple)):
        if not isinstance(array, int):
            raise ValueError(
                "%s 参数必须是列表或元组类型, 而非 %s." % (param_name, type(array))
            )
        array = [array]
    elif not array:
        raise ValueError("%s 参数不能为空." % param_name)

    return [validate_unsigned_int(i, param_name, is_item=True) for i in array]


def validate_float(param: Any, param_name: str, *, is_item: bool = False) -> float:
    """返回已有 float，或尝试用 float() 转换原始值。

    Args:
        param: 可交给 float() 的原始值，包括字符串、整数和转换钩子对象。
        param_name: 用于构建错误信息的参数名称。
        is_item: 为 True 时使用数组元素的错误描述；默认 False，不改变有效结果。

    Returns:
        float: 已有 float 的原值或转换结果；允许 NaN、正负无穷及负零。

    Raises:
        ValueError: float() 转换抛出 Exception，原异常显式保留为 cause。

    Examples:
        >>> validate_float("1.25", "value")
        1.25
        >>> validate_float(None, "value", is_item=True)
        Traceback (most recent call last):
            ...
        ValueError: value 参数中的元素必须是 float 类型, 而非 <class 'NoneType'>.
    """
    if not isinstance(param, float):
        try:
            param = float(param)
        except Exception as err:
            if is_item:
                err_msg = "%s 参数中的元素必须是 float 类型, 而非 %s."
            else:
                err_msg = "%s 参数必须是 float 类型, 而非 %s."
            raise ValueError(err_msg % (param_name, type(param))) from err
    return param


def validate_array_of_float(
    array: object,
    param_name: str,
) -> list[float]:
    """将 float 或非空 list/tuple 转换为浮点数列表。

    Args:
        array: 标量必须是 float；list/tuple 的元素可逐项经 float() 转换。
            单独的整数或数字字符串不被接受。
        param_name: 用于构建错误信息的参数名称。

    Returns:
        list[float]: 新列表，保留顺序和重复项，允许非有限数，不修改输入。

    Raises:
        ValueError: 输入类型不符、容器为空，或某个元素转换失败。
            转换异常显式保留为 cause，按输入顺序在首个错误处停止。

    Examples:
        >>> validate_array_of_float([1, "1.25"], "value")
        [1.0, 1.25]
    """
    if not isinstance(array, (list, tuple)):
        if not isinstance(array, float):
            raise ValueError(
                "%s 参数必须是列表或元组类型, 而非 %s." % (param_name, type(array))
            )
        array = [array]
    elif not array:
        raise ValueError("%s 参数不能为空." % param_name)

    return [validate_float(i, param_name, is_item=True) for i in array]


def validate_unsigned_float(
    param: Any,
    param_name: str,
    *,
    is_item: bool = False,
) -> float:
    """用 float() 转换原始值，并按 < 0 比较拒绝负值。

    判断针对转换后的 float；零、负零和转换为 0.0 的 False 均可通过。
    NaN 和正无穷按比较规则通过，负无穷被拒绝。

    Args:
        param: 可交给 float() 的原始值，包括数字字符串、bool 和转换钩子对象。
        param_name: 用于构建错误信息的参数名称。
        is_item: 为 True 时使用数组元素的错误描述；默认 False，不改变有效结果。

    Returns:
        float: 已有 float 的原值或转换结果，保留负零；允许 NaN 和正无穷。

    Raises:
        ValueError: float() 转换抛出 Exception，或转换后的值小于零。
            转换异常显式保留为 cause，回溯显示原异常及本层 ValueError；
            负值错误包含转换后的失败值。

    Examples:
        >>> validate_unsigned_float(True, "value")
        1.0
        >>> [validate_unsigned_float(v, "value") for v in ("0", -0.0, False)]
        [0.0, -0.0, 0.0]
        >>> validate_unsigned_float(-1, "value")
        Traceback (most recent call last):
            ...
        ValueError: value 参数必须为非负浮点数, 而非 -1.0.
        >>> validate_unsigned_float(None, "value", is_item=True)
        Traceback (most recent call last):
            ...
        ValueError: value 参数中的元素必须是 float 类型, 而非 <class 'NoneType'>.
    """
    if not isinstance(param, float):
        try:
            param = float(param)
        except Exception as err:
            if is_item:
                err_msg = "%s 参数中的元素必须是 float 类型, 而非 %s."
            else:
                err_msg = "%s 参数必须是 float 类型, 而非 %s."
            raise ValueError(err_msg % (param_name, type(param))) from err
    if param < 0:
        if is_item:
            err_msg = "%s 参数中的元素必须为非负浮点数, 而非 %s."
        else:
            err_msg = "%s 参数必须为非负浮点数, 而非 %s."
        raise ValueError(err_msg % (param_name, param))
    return param


def validate_array_of_unsigned_float(
    array: object,
    param_name: str,
) -> list[float]:
    """逐项转换浮点数并拒绝负数元素，允许零和负零。

    Args:
        array: 标量必须是 float；非空 list/tuple 的元素可经 float() 转换。
            容器内允许零、负零和 False（转换为 0.0）；NaN、正无穷按比较规则通过。
        param_name: 用于构建错误信息的参数名称。

    Returns:
        list[float]: 新列表，保留顺序和重复项，不修改输入。

    Raises:
        ValueError: 输入类型不符、容器为空、元素转换失败或小于零。
            按输入顺序在首个错误处停止，负数错误包含转换后的失败值。
            转换异常显式保留为 cause，回溯显示原异常及本层 ValueError。

    Examples:
        >>> validate_array_of_unsigned_float([1, "1.25"], "value")
        [1.0, 1.25]
        >>> validate_array_of_unsigned_float([0, -0.0, False], "value")
        [0.0, -0.0, 0.0]
        >>> validate_array_of_unsigned_float([1, -1], "value")
        Traceback (most recent call last):
            ...
        ValueError: value 参数中的元素必须为非负浮点数, 而非 -1.0.
    """
    if not isinstance(array, (list, tuple)):
        if not isinstance(array, float):
            raise ValueError(
                "%s 参数必须是列表或元组类型, 而非 %s." % (param_name, type(array))
            )
        array = [array]
    elif not array:
        raise ValueError("%s 参数不能为空." % param_name)

    return [validate_unsigned_float(i, param_name, is_item=True) for i in array]


def validate_datetime(
    dt: str | datetime.date | datetime.datetime | None,
    support_none: bool,
    param_name: str,
) -> Pydt:
    """按 Pydt.parse 的默认行为解析日期，不另加日历或时区规则。

    缺省日期分量使用 DEFAULT_DATE（1970-01-01）；解析器可能归一化字符串
    中的超范围分量。返回 Pydt，具体年月或日期字符串由调用者格式化。

    Args:
        dt: 日期字符串、date/datetime 对象或 None。
        support_none: 为 False 时提前拒绝 None；为 True 时仅将 None 交给
            解析器，不构造当前日期，也不保证 None 可以解析成功。
        param_name: 用于构建错误信息的参数名称。

    Returns:
        Pydt: 解析结果；时区处理沿用第三方解析器默认行为。

    Raises:
        ValueError: 不允许 None，或解析失败；解析异常保留为 cause。

    Examples:
        >>> validate_datetime("2026-09", False, "date").strftime("%Y-%m-%d")
        '2026-09-01'
    """
    if not support_none and dt is None:
        raise ValueError("%s 参数不能为 None." % param_name)
    try:
        return Pydt.parse(dt, default=DEFAULT_DATE)
    except Exception as err:
        raise ValueError(
            "%s 参数值 %r 无法被解析为日期对象." % (param_name, dt)
        ) from err


def validate_exchange_rate(rate: object, param_name: str) -> Decimal:
    """解析有限正汇率，并按当前 Decimal context 量化到十位小数。

    float 及其他非 str/Decimal 对象先转为字符串，再构造 Decimal。
    量化使用当前精度、舍入和 traps，可能设置 context flags；极小正数可
    量化为零，关闭异常 trap 时也可能得到特殊值，不保证结果始终为正。

    Args:
        rate: 原始汇率，常见输入为 str、int、float 或 Decimal。
        param_name: 用于构建错误信息的参数名称。

    Returns:
        Decimal: 当前 context 下的量化结果，正常有限结果的指数为 -10。

    Raises:
        ValueError: 转换失败、输入非有限或小于或等于零。
            转换异常保留为 cause。
        decimal.DecimalException: 量化触发的 context 异常（如 InvalidOperation）
            原样传播，不包装为 ValueError。

    Examples:
        >>> str(validate_exchange_rate("1.25", "rate"))
        '1.2500000000'
    """
    if isinstance(rate, str):
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
        raise ValueError("%s 参数值必须为正数, 而非 %s." % (param_name, rate))

    return rate.quantize(Decimal("0.0000000000"))  # 保留10位小数
