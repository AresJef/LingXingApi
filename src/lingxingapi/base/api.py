# -*- coding: utf-8 -*-c
from typing import Literal
from typing_extensions import Self
from warnings import warn as _warn
from asyncio import sleep as _aio_sleep
from orjson import loads as _orjson_loads
from Crypto.Cipher._mode_ecb import EcbMode
from aiohttp import (
    TCPConnector,
    ClientSession,
    ClientConnectorError,
    ClientTimeout,
    ServerDisconnectedError,
)
from lingxingapi import utils, errors
from lingxingapi.base import route, schema

# Type Aliases ---------------------------------------------------------------------------------------------------------
REQUEST_METHOD = Literal["GET", "POST", "PUT", "DELETE"]


# API ------------------------------------------------------------------------------------------------------------------
class BaseAPI:
    """领星 API 基础类, 提供公共方法和属性, 用于子类继承

    ## Notice
    请勿直接实例化此类
    """

    # HTTP 会话
    _session: ClientSession = None
    # Token 令牌
    _access_token: str = None
    _refresh_token: str = None

    def __init__(
        self,
        app_id: str,
        app_secret: str,
        app_cipher: EcbMode,
        timeout: int | float,
        ignore_timeout: bool,
        ignore_timeout_wait: int | float,
        ignore_timeout_retry: int,
        ignore_api_limit: bool,
        ignore_api_limit_wait: int | float,
        ignore_api_limit_retry: int,
        ignore_internal_server_error: bool,
        ignore_internal_server_error_wait: int | float,
        ignore_internal_server_error_retry: int,
        ignore_internet_connection: bool,
        ignore_internet_connection_wait: int | float,
        ignore_internet_connection_retry: int,
        echo_retry_warnings: bool = True,
    ) -> None:
        """领星 API 基础类, 提供公共方法和属性供子类继承使用

        ## Notice
        请勿直接实例化此类

        :param app_id `<'str'>`: 应用ID, 用于鉴权

        :param app_secret `<'str'>`: 应用密钥, 用于鉴权

        :param app_cipher `<'EcbMode'>`: 基于 appId 创建的 AES-ECB 加密器

        :param timeout `<'int/float'>`: 请求超时 (单位: 秒)

        :param ignore_timeout `<'bool'>`: 是否忽略请求超时错误

            - 如果设置为 `True`, 则在遇到请求超时错误时不会抛出异常, 而是会等待
              `ignore_timeout_wait` 秒后重试请求, 重试次数不超过 `ignore_timeout_retry`
            - 如果设置为 `False`, 则在遇到请求超时错误时直接抛出 `ApiTimeoutError` 异常

        :param ignore_timeout_wait `<'int/float'>`: 忽略请求超时错误时的等待时间 (单位: 秒),
            仅在 `ignore_timeout` 为 `True` 时生效

        :param ignore_timeout_retry `<'int'>`: 忽略请求超时错误时的最大重试次数,
            仅在 `ignore_timeout` 为 `True` 时生效, 若设置为 `-1` 则表示无限重试

        :param ignore_api_limit `<'bool'>`: 是否忽略 API 限流错误

            - 如果设置为 `True`, 则在遇到限流错误时不会抛出异常, 而是会等待
              `ignore_api_limit_wait` 秒后重试请求, 重试次数不超过 `ignore_api_limit_retry`
            - 如果设置为 `False`, 则在遇到限流错误时直接抛出 `ApiLimitError` 异常

        :param ignore_api_limit_wait `<'int/float'>`: 忽略 API 限流错误时的等待时间 (单位: 秒),
            仅在 `ignore_api_limit` 为 `True` 时生效

        :param ignore_api_limit_retry `<'int'>`: 忽略 API 限流错误时的最大重试次数,
            仅在 `ignore_api_limit` 为 `True` 时生效, 若设置为 `-1` 则表示无限重试

        :param ignore_internal_server_error `<'bool'>`: 是否忽略服务器内部错误 (500错误码, 仅限 Internal Server Error 类型)

            - 如果设置为 `True`, 则在遇到服务器内部错误时不会抛出异常, 而是会等待
              `ignore_internal_server_error_wait` 秒后重试请求, 重试次数不超过 `ignore_internal_server_error_retry`
            - 如果设置为 `False`, 则在遇到服务器内部错误时直接抛出 `InternalServerError` 异常

        :param ignore_internal_server_error_wait `<'int/float'>`: 忽略服务器内部错误时的等待时间 (单位: 秒),
            仅在 `ignore_internal_server_error` 为 `True` 时生效

        :param ignore_internal_server_error_retry `<'int'>`: 忽略服务器内部错误时的最大重试次数,
            仅在 `ignore_internal_server_error` 为 `True` 时生效, 若设置为 `-1` 则表示无限重试

        :param ignore_internet_connection `<'bool'>`: 是否忽略无法链接互联网错误

            - 如果设置为 `True`, 则在遇到无法链接互联网错误时不会抛出异常, 而是会等待
              `ignore_internet_connection_wait` 秒后重试请求, 重试次数不超过 `ignore_internet_connection_retry`
            - 如果设置为 `False`, 则在遇到无法链接互联网错误时直接抛出 `InternetConnectionError` 异常

        :param ignore_internet_connection_wait `<'int/float'>`: 忽略无法链接互联网错误时的等待时间 (单位: 秒),
            仅在 `ignore_internet_connection` 为 `True` 时生效

        :param ignore_internet_connection_retry `<'int'>`: 忽略无法链接互联网错误时的最大重试次数,
            仅在 `ignore_internet_connection` 为 `True` 时生效, 若设置为 `-1` 则表示无限重试

        :param echo_retry_warnings `<'bool'>`: 是否在重试请求时打印警告信息, 默认为 `True`
        """
        # API 凭证
        self._app_id: str = app_id
        self._app_secret: str = app_secret
        self._app_cipher: EcbMode = app_cipher
        # HTTP 会话
        self._timeout: ClientTimeout = timeout
        # 错误处理
        # . 请求超时
        self._ignore_timeout: bool = ignore_timeout
        self._ignore_timeout_wait: float = ignore_timeout_wait
        self._ignore_timeout_retry: int = ignore_timeout_retry
        self._infinite_timeout_retry: bool = ignore_timeout_retry == -1
        # . API 限流
        self._ignore_api_limit: bool = ignore_api_limit
        self._ignore_api_limit_wait: float = ignore_api_limit_wait
        self._ignore_api_limit_retry: int = ignore_api_limit_retry
        self._infinite_retry: bool = ignore_api_limit_retry == -1
        # . 服务器内部错误 (500错误码, 仅限 Internal Server Error 类型)
        self._ignore_internal_server_error: bool = ignore_internal_server_error
        self._ignore_internal_server_error_wait: float = (
            ignore_internal_server_error_wait
        )
        self._ignore_internal_server_error_retry: int = (
            ignore_internal_server_error_retry
        )
        self._infinite_internal_server_error_retry: bool = (
            ignore_internal_server_error_retry == -1
        )
        # . 无法链接互联网
        self._ignore_internet_connection: bool = ignore_internet_connection
        self._ignore_internet_connection_wait: float = ignore_internet_connection_wait
        self._ignore_internet_connection_retry: int = ignore_internet_connection_retry
        self._infinite_internet_connection_retry: bool = (
            ignore_internet_connection_retry == -1
        )
        # . 重试警告
        self._echo_retry_warnings: bool = echo_retry_warnings

    async def __aenter__(self) -> Self:
        """进入 API 客户端异步上下文管理器

        :returns `<'API'>`: 返回 API 客户端实例
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """退出 API 客户端异步上下文管理器, 并关闭 HTTP 会话"""
        await self.close()

    async def close(self) -> None:
        """关闭 API 客户端的 HTTP 会话"""
        if BaseAPI._session is not None:
            await BaseAPI._session.close()
            BaseAPI._session = None

    # 公共 API --------------------------------------------------------------------------------------
    # . Token 令牌
    async def _AccessToken(self) -> schema.Token:
        """(Internal) 获取领星 API 的访问令牌

        ## Docs
        - 授权: [获取 access-token和refresh-token](https://apidoc.lingxing.com/#/docs/Authorization/GetToken)

        :returns `<'Token'>`: 返回接口的访问令牌
        ```python
        {
            # 接口的访问令牌
            "access_token": "your_access_token",
            # 用于续约 access_token 的更新令牌
            "refresh_token": "your_refresh_token",
            # 访问令牌的有效时间 (单位: 秒)
            "expires_in": 3600
        }
        ```
        """
        data = await self._request(
            "POST",
            route.AUTH_GET_TOKEN,
            {"appId": self._app_id, "appSecret": self._app_secret},
            extract_data=True,
        )
        res = schema.Token.model_validate(data)
        BaseAPI._access_token = res.access_token
        BaseAPI._refresh_token = res.refresh_token
        return res

    async def _RefreshToken(self, refresh_token: str) -> schema.Token:
        """(Internal) 基于 refresh_token 刷新领星 API 的访问令牌

        ## Docs
        - 授权: [续约接口令牌](https://apidoc.lingxing.com/#/docs/Authorization/RefreshToken)

        :param refresh_token `<'str'>`: 用于续约 refresh_token 的令牌
        :returns `<'Token'>`: 返回接口的访问令牌
        ```python
        {
            # 接口的访问令牌
            "access_token": "your_access_token",
            # 用于续约 access_token 的更新令牌
            "refresh_token": "your_refresh_token",
            # 访问令牌的有效时间 (单位: 秒)
            "expires_in": 3600
        }
        ```
        """
        data = await self._request(
            "POST",
            route.AUTH_REFRESH_TOKEN,
            {"appId": self._app_id, "refreshToken": str(refresh_token)},
            extract_data=True,
        )
        res = schema.Token.model_validate(data)
        BaseAPI._access_token = res.access_token
        BaseAPI._refresh_token = res.refresh_token
        return res

    async def _UpdateToken(self) -> None:
        """(internal) 获取或刷新 access_token, 如果缓存了 refresh_token,
        则优先基于 refresh_token 进行刷新
        """
        # 如果存在 refresh token, 则使用它刷新 access token
        if BaseAPI._refresh_token is not None:
            try:
                await self._RefreshToken(BaseAPI._refresh_token)
                return None
            except errors.TokenError:
                pass
        # 如果不存在 refresh token, 则重新获取 access token
        await self._AccessToken()

    # 核心 HTTP 逻辑 ---------------------------------------------------------------------------------
    async def _request(
        self,
        method: REQUEST_METHOD,
        url: str,
        params: dict,
        body: dict | None = None,
        headers: dict | None = None,
        extract_data: bool = False,
    ) -> dict | list:
        """(internal) 发送基础 HTTP 请求, 并对状态码与业务响应数据进行校验

        :param method `<'str'>`: HTTP 请求方法, 如: `"GET"`, `"POST"`, `"PUT"`, `"DELETE"`
        :param url `<'str'>`: 业务请求路径, 如: `"/api/auth-server/oauth/access-token"`
        :param params `<'dict'>`: 必填公共参数, 包含 (`app_key`, `access_token`, `timestamp`, `sign`)
        :param body `<'dict/None'>`: 可选业务请求参数, 用于 POST/PUT 请求, 默认 `None`
        :param headers `<'dict/None'>`: 可选请求头, 如: `{"X-API-VERSION": "2"}`, 默认 `None`
        :param extract_data `<'bool'>`: 是否提取响应数据中的 `data` 字段并直接返回, 默认为 `False`
        :returns `<'list/dict'>`: 返回解析并验证后响应数据
        """
        # 确保 HTTP 会话可用
        if BaseAPI._session is None or BaseAPI._session.closed:
            BaseAPI._session = ClientSession(
                route.API_SERVER,
                headers={"Content-Type": "application/json"},
                timeout=self._timeout,
                connector=TCPConnector(limit=100),
            )

        # 发送请求
        retry_count = 0
        while True:
            try:
                async with BaseAPI._session.request(
                    method,
                    url,
                    params=params,
                    json=body,
                    headers=headers,
                ) as res:
                    # . 检查响应状态码
                    if res.status != 200:
                        raise errors.ServerError(
                            "领星API服务器响应错误", url, res.reason, res.status
                        )
                    # . 解析并验证响应数据
                    return self._handle_response_data(
                        url, await res.read(), extract_data
                    )
            # fmt: off
            # . 请求限流错误处理
            except errors.ApiLimitError as err:
                if (
                        self._ignore_api_limit 
                        and (self._infinite_retry or retry_count < self._ignore_api_limit_retry)
                ):
                    retry_count += 1
                    if self._echo_retry_warnings:
                        _warn("请求被限流, 等待 %.2f 秒后重试(%d)..." % (self._ignore_api_limit_wait, retry_count))
                    await _aio_sleep(self._ignore_api_limit_wait)
                    continue
                if params is not None:
                    err.add_note("请求参数: %r" % params)
                if body is not None:
                    err.add_note("请求实体: %r" % body)
                if retry_count > 0:
                    err.add_note("请求重试: %d" % retry_count)
                raise err
            # . 服务器内部错误处理
            except errors.InternalServerError as err:
                if (
                        self._ignore_internal_server_error 
                        and (self._infinite_internal_server_error_retry or retry_count < self._ignore_internal_server_error_retry)
                ):
                    retry_count += 1
                    if self._echo_retry_warnings:
                        _warn("服务器内部错误, 等待 %.2f 秒后重试(%d)..." % (self._ignore_internal_server_error_wait, retry_count))
                    await _aio_sleep(self._ignore_internal_server_error_wait)
                    continue
                if params is not None:
                    err.add_note("请求参数: %r" % params)
                if body is not None:
                    err.add_note("请求实体: %r" % body)
                if retry_count > 0:
                    err.add_note("请求重试: %d" % retry_count)
                raise err
            # . 网络相关错误处理
            except (TimeoutError, ServerDisconnectedError) as err:
                # 无法链接互联网
                if not await utils.check_internet_tcp():
                    if (
                        self._ignore_internet_connection 
                        and (self._infinite_internet_connection_retry or retry_count < self._ignore_internet_connection_retry)
                    ):
                        retry_count += 1
                        if self._echo_retry_warnings:
                            _warn("无法链接互联网, 等待 %.2f 秒后重试(%d)..." % (self._ignore_internet_connection_wait, retry_count))
                        await _aio_sleep(self._ignore_internet_connection_wait)
                        continue
                    exc = errors.InternetConnectionError("无法链接互联网, 请检查网络连接", url, str(err))
                    if params is not None:
                        exc.add_note("请求参数: %r" % params)
                    if body is not None:
                        exc.add_note("请求实体: %r" % body)
                    if retry_count > 0:
                        exc.add_note("请求重试: %d" % retry_count)
                    raise exc from err
                # 请求超时
                if (
                        self._ignore_timeout 
                        and (self._infinite_timeout_retry or retry_count < self._ignore_timeout_retry)
                ):
                    retry_count += 1
                    if self._echo_retry_warnings:
                        _warn("请求超时, 等待 %.2f 秒后重试(%d)..." % (self._ignore_timeout_wait, retry_count))
                    await _aio_sleep(self._ignore_timeout_wait)
                    continue
                exc = errors.ApiTimeoutError("领星 API 请求超时", url, str(err))
                if params is not None:
                    exc.add_note("请求参数: %r" % params)
                if body is not None:
                    exc.add_note("请求实体: %r" % body)
                if retry_count > 0:
                    exc.add_note("请求重试: %d" % retry_count)
                exc.add_note("超时时间: %s" % self._timeout)
                raise exc from err
            # . 服务器无响应处理
            except ClientConnectorError as err:
                # 无法链接互联网
                if not await utils.check_internet_tcp():
                    if (
                        self._ignore_internet_connection 
                        and (self._infinite_internet_connection_retry or retry_count < self._ignore_internet_connection_retry)
                    ):
                        retry_count += 1
                        if self._echo_retry_warnings:
                            _warn("无法链接互联网, 等待 %.2f 秒后重试(%d)..." % (self._ignore_internet_connection_wait, retry_count))
                        await _aio_sleep(self._ignore_internet_connection_wait)
                        continue
                    exc = errors.InternetConnectionError("无法链接互联网, 请检查网络连接", url, str(err))
                    if params is not None:
                        exc.add_note("请求参数: %r" % params)
                    if body is not None:
                        exc.add_note("请求实体: %r" % body)
                    if retry_count > 0:
                        exc.add_note("请求重试: %d" % retry_count)
                    raise exc from err
                # Server 无响应
                raise errors.ServerError("领星 API 服务器无响应, 若无网络问题, 请检查账号 IP 白名单设置", url, err) from err
            except Exception as err:
                if params is not None:
                    err.add_note("请求参数: %r" % params)
                if body is not None:
                    err.add_note("请求实体: %r" % body)
                raise err
            # fmt: on

    async def _request_with_sign(
        self,
        method: REQUEST_METHOD,
        url: str,
        params: dict = None,
        body: dict | None = None,
        headers: dict | None = None,
        extract_data: bool = False,
    ) -> dict | list:
        """(internal) 基于 params 和 body 生成签名, 并发送带签名的 HTTP 请求，自动处理过期 Access Token 的获取与刷新

        :param method `<'str'>`: HTTP 请求方法, 如: `"GET"`, `"POST"`, `"PUT"`, `"DELETE"`
        :param url `<'str'>`: 业务请求路径, 如: `"/api/auth-server/oauth/access-token"`
        :param params `<'dict'>`: 可选请求参数, 默认 `None`
        :param body `<'dict/None'>`: 可选业务请参数, 默认 `None`
        :param headers `<'dict/None'>`: 可选请求头, 如: `{"X-API-VERSION": "2"}`, 默认 `None`
        :param extract_data `<'bool'>`: 是否提取响应数据中的 `data` 字段并直接返回, 默认为 `False`
        :returns `<'list/dict'>`: 返回解析并验证后响应数据
        """
        # 确保 access token 可用
        if BaseAPI._access_token is None:
            await self._UpdateToken()

        # 构建参数
        reqs_params = {
            "app_key": self._app_id,
            "access_token": BaseAPI._access_token,
            "timestamp": utils.now_ts(),
        }
        if isinstance(params, dict):
            reqs_params.update(params)
        sign_params = {k: v for k, v in reqs_params.items()}
        if isinstance(body, dict):
            sign_params.update(body)

        # 生成签名
        sign = utils.generate_sign(sign_params, self._app_cipher)
        reqs_params["sign"] = sign

        # 发送请求
        try:
            return await self._request(
                method,
                url,
                reqs_params,
                body=body,
                headers=headers,
                extract_data=extract_data,
            )
        except errors.TokenError:
            await self._UpdateToken()  # 刷新 Token
            return await self._request_with_sign(method, url, params, body)

    def _handle_response_data(
        self,
        url: str,
        res_data: bytes,
        extract_data: bool,
    ) -> dict | list:
        """解析并验证响应数据, 并数据中的 `data` 字段

        :param url `<'str'>`: 对应业务请求路径, 用于构建错误信息
        :param res_data `<'bytes'>`: 原始响应数据
        :param extract_data `<'bool'>`: 是否提取响应数据中的 `data` 字段
        :returns `<'dict/list'>`: 返回解析并验证后的响应数据中的 `data` 字段
        """
        # 解析响应数据
        try:
            data: dict = _orjson_loads(res_data)
        except Exception as err:
            raise errors.ResponseDataError(
                "响应数据解析错误, 可能不是有效的JSON格式", url, res_data
            ) from err

        # 验证响应数据
        code = data.get("code")
        if code is None:
            raise errors.ResponseDataError("响应数据错误, 缺少 code 字段", url, data)
        if code not in (0, 1, "200"):
            try:
                errno: int = int(code)
            except ValueError:
                raise errors.ResponseDataError(
                    "响应数据错误, code 字段不是整数", url, data, code
                )
            # 常见错误码
            if errno == 2001003:
                raise errors.AccessTokenExpiredError(
                    "access token 过期, 请重新获取", url, data, code
                )
            if errno == 2001008:
                raise errors.RefreshTokenExpiredError(
                    "refresh token过期, 请重新获取", url, data, code
                )
            if errno == 2001007:
                raise errors.SignatureExpiredError(
                    "签名过期, 请重新发起请求", url, data, code
                )
            if errno == 3001008:
                raise errors.TooManyRequestsError(
                    "接口请求太频繁触发限流", url, data, code
                )
            if errno == 103:
                raise errors.ApiLimitError(
                    "请求速率过高导致被限流拦截", url, data, code
                )
            # 其他错误码
            if errno in (400, 405):
                raise errors.InvalidApiUrlError(
                    "请求 url 或 params 不正确", url, data, code
                )
            if errno in (100, 500):
                raise errors.InternalServerError(
                    "领星 API 服务器发生内部错误", url, data, code
                )
            if errno == 2001001:
                raise errors.AppIdOrSecretError(
                    "appId 不存在, 请检查值有效性", url, data, code
                )
            if errno == 1001:
                raise errors.AppIdOrSecretError(
                    "appSecret 中可能有特殊字符", url, data, code
                )
            if errno == 2001002:
                raise errors.AppIdOrSecretError(
                    "appSecret 不正确, 请检查值有效性", url, data, code
                )
            if errno == 2001004:
                raise errors.UnauthorizedApiError(
                    "请求的 api 被未授权, 请联系领星确认", url, data, code
                )
            if errno == 401:
                raise errors.UnauthorizedApiError(
                    "api 授权被禁用, 请检查授权状态", url, data, code
                )
            if errno == 403:
                raise errors.UnauthorizedApiError(
                    "api 授权失效, 请检查授权状态", url, data, code
                )
            if errno == 2001005:
                raise errors.InvalidAccessTokenError(
                    "access token 不正确, 请检查有效性", url, data, code
                )
            if errno == 2001009:
                raise errors.InvalidRefreshTokenError(
                    "refresh token 不正确, 请检查有效性", url, data, code
                )
            if errno == 2001006:
                raise errors.InvalidSignatureError(
                    "接口签名不正确, 请检查生成签名的正确性", url, data, code
                )
            if errno == 102:
                raise errors.InvalidParametersError("参数不合法", url, data, code)
            if errno == 3001001:
                # fmt: off
                raise errors.InvalidParametersError(
                    "必传参数缺失, 公共参数必须包含 (access_token, app_key, timestamp, sign)",
                    url, data, code,
                )
                # fmt: on
            if errno == 3001002:
                raise errors.UnauthorizedRequestIpError(
                    "发起请求的 ip 未加入领星 api 白名单", url, data, code
                )
            # 未知错误码
            raise errors.UnknownRequestError("未知的 api 错误", url, data, code)

        # 是否成功 (特殊返回检查情况)
        if not data.get("success", True):
            raise errors.InvalidParametersError("参数不合法", url, data, code)

        # 返回响应数据
        return data if not extract_data else self._extract_data(data, url, code)

    def _extract_data(self, res_data: dict, url: str, code: int | None = None) -> dict:
        """(internal) 提取响应数据中的 `data` 字段

        :param res_data `<'dict'>`: 原始响应数据
        :param url `<'str'>`: 对应业务请求路径, 用于构建错误信息
        :param code `<'int'>`: 可选的状态码, 用于构建错误信息
        :returns `<'dict'>`: 返回解析并验证后的响应数据中的 `data` 字段
        """
        try:
            return res_data["data"]
        except KeyError:
            raise errors.ResponseDataError(
                "响应数据错误, 缺少 data 字段", url, res_data, code
            )
