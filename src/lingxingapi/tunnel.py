from __future__ import annotations

import asyncio
import contextlib
import ipaddress
import json
import math
import re
from pathlib import Path
from types import TracebackType
from urllib.parse import urlparse

import aiohttp
import asyncssh
from aiohttp_socks import ProxyConnector
from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator
from typing_extensions import Self

_IPV4_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_IPV6_PATTERN = re.compile(
    r"(?<![\w:])(?:[0-9a-fA-F]{0,4}:){2,}[0-9a-fA-F:.%]*(?![\w:])"
)


def _validate_timeout(value: float) -> float:
    """校验一次性操作的超时时间。

    :param value: 超时时间，单位为秒。
    :returns: 转换后的浮点数秒数。
    :raises TypeError: 当超时时间不是整数或浮点数时抛出。
    :raises ValueError: 当超时时间不是有限正数时抛出。
    """
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(f"timeout must be int or float, not {type(value).__name__}")
    value = float(value)
    if not math.isfinite(value) or value <= 0:
        raise ValueError("timeout must be greater than 0")
    return value


def _normalize_ip_address(value: object) -> str | None:
    """尝试将输入值标准化为合法 IP 地址字符串。"""
    if value is None:
        return None

    try:
        return str(ipaddress.ip_address(str(value).strip()))
    except ValueError:
        return None


def _extract_ip_address(text: str) -> str:
    """从健康检查响应文本中提取 IP 地址。

    支持两类常见响应格式：
    - JSON：例如 `{"ip": "1.2.3.4"}`。
    - 纯文本：例如 `当前 IP：1.2.3.4 来自于：中国 ...`。

    :param text: 健康检查接口返回的响应文本。
    :returns: 解析出的 IPv4 或 IPv6 地址。
    :raises ValueError: 当响应中无法识别 IP 地址时抛出。
    """
    with contextlib.suppress(json.JSONDecodeError):
        data = json.loads(text)
        if isinstance(data, dict):
            for key in ("ip", "origin", "query", "address"):
                value = data.get(key)
                if isinstance(value, str):
                    for item in value.split(","):
                        ip = _normalize_ip_address(item)
                        if ip is not None:
                            return ip
                else:
                    ip = _normalize_ip_address(value)
                    if ip is not None:
                        return ip

    for pattern in (_IPV4_PATTERN, _IPV6_PATTERN):
        for match in pattern.finditer(text):
            ip = _normalize_ip_address(match.group(0))
            if ip is not None:
                return ip

    raise ValueError("health check response does not contain an IP address")


def _normalize_url(value: object) -> str:
    """标准化并校验 HTTP(S) URL。"""
    if not isinstance(value, str):
        raise ValueError("health check URLs must be strings")

    value = value.strip()
    if not value:
        raise ValueError("health check URLs cannot be empty")

    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("health check URLs must be absolute HTTP(S) URLs")

    return value


class AsyncSshSocksTunnelConfig(BaseModel):
    """AsyncSSH SOCKS 隧道配置。

    该模型用于集中保存 SSH 服务器、密码或认证文件、本地 SOCKS 监听地址、
    超时与健康检查相关配置。模型是冻结的，创建后不可修改；字符串字段
    会自动去除首尾空白，并由 Pydantic 完成基础类型与范围校验。
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
    )

    server_host: str = Field(min_length=1, strict=True)
    server_user: str = Field(min_length=1, strict=True)
    server_password: SecretStr | None = Field(default=None, min_length=1, repr=False)

    server_port: int = Field(default=22, ge=1, le=65535, strict=True)

    # Use 127.0.0.1 unless you intentionally want other local machines
    # to access this SOCKS proxy.
    local_host: str = Field(default="127.0.0.1", min_length=1, strict=True)

    # Use 0 if you want the OS to pick an available port automatically.
    local_port: int = Field(default=1080, ge=0, le=65535, strict=True)

    # Validate outbound traffic before start()/__aenter__ returns.
    validate_on_start: bool = Field(default=True, strict=True)

    # Example:
    # client_keys=["/home/app/.ssh/id_ed25519"]
    client_keys: tuple[str, ...] | None = None

    # Production:
    # known_hosts="/home/app/.ssh/known_hosts"
    #
    # Testing only:
    # known_hosts=None
    known_hosts: str | Path | None = None

    connect_timeout: float = Field(default=15.0, gt=0, allow_inf_nan=False)
    close_timeout: float = Field(default=1.0, gt=0, allow_inf_nan=False)

    # SSH keepalive. Similar idea to OpenSSH ServerAliveInterval /
    # ServerAliveCountMax.
    keepalive_interval: float = Field(default=30.0, ge=0, allow_inf_nan=False)
    keepalive_count_max: int = Field(default=3, ge=1, strict=True)

    # Optional health check targets.
    # These should return your tunnel/server public IP.
    health_check_urls: tuple[str, ...] = (
        "http://myip.ipip.net",
        "https://ip.3322.net",
        "https://api.ipify.org?format=json",
    )

    def __init__(
        self,
        server_host: str | None = None,
        server_user: str | None = None,
        server_password: str | None = None,
        **data: object,
    ) -> None:
        """初始化隧道配置。

        支持两种调用方式：
        - `AsyncSshSocksTunnelConfig(server_host="host", server_user="user")`
        - `AsyncSshSocksTunnelConfig("host", "user")`
        - `AsyncSshSocksTunnelConfig("host", "user", "password")`

        :param server_host: SSH 服务器主机名或 IP 地址。
        :param server_user: SSH 登录用户名。
        :param server_password: SSH 登录密码；若使用密钥认证，可保持为 `None`。
        :param data: 其他配置字段，例如端口、密钥路径和超时时间。
        """
        if server_host is not None:
            if "server_host" in data:
                raise TypeError("server_host was provided twice")
            data["server_host"] = server_host

        if server_user is not None:
            if "server_user" in data:
                raise TypeError("server_user was provided twice")
            data["server_user"] = server_user

        if server_password is not None:
            if "server_password" in data:
                raise TypeError("server_password was provided twice")
            data["server_password"] = server_password

        super().__init__(**data)

    @field_validator("client_keys", mode="before")
    @classmethod
    def _normalize_client_keys(cls, value: object) -> tuple[str, ...] | None:
        """标准化 SSH 客户端私钥路径。

        `client_keys` 可以传入单个字符串路径、单个 `Path`，也可以传入
        多个路径组成的序列。返回值统一为非空字符串元组，便于直接传给
        `asyncssh.connect()`。
        """
        if value is None:
            return None

        if isinstance(value, (str, Path)):
            keys = (cls._normalize_path_value(value),)
        else:
            try:
                keys = tuple(cls._normalize_path_value(item) for item in value)
            except TypeError as exc:
                raise ValueError(
                    "client_keys must be a path or sequence of paths"
                ) from exc

        if not keys:
            raise ValueError("client_keys cannot be empty")
        return keys

    @field_validator("known_hosts", mode="before")
    @classmethod
    def _normalize_known_hosts(cls, value: object) -> str | None:
        """标准化 known_hosts 文件路径。

        允许传入字符串或 `Path`；如果传入 `None`，表示不使用 known_hosts
        文件校验，通常只应在测试环境中使用。
        """
        if value is None:
            return None
        return cls._normalize_path_value(value)

    @field_validator("health_check_urls", mode="before")
    @classmethod
    def _normalize_health_check_urls(cls, value: object) -> tuple[str, ...]:
        """标准化健康检查地址列表。

        健康检查地址可以传入单个字符串，也可以传入字符串序列。地址会按
        顺序尝试，第一个成功返回可解析 IP 的地址会作为结果来源。
        """
        if isinstance(value, str):
            urls = (_normalize_url(value),)
        else:
            try:
                urls = tuple(_normalize_url(url) for url in value)
            except TypeError as exc:
                raise ValueError(
                    "health_check_urls must be a URL or sequence of URLs"
                ) from exc

        if not urls:
            raise ValueError("health_check_urls cannot be empty")
        return urls

    @staticmethod
    def _normalize_path_value(value: object) -> str:
        """将路径值转换为非空字符串。

        :param value: 字符串路径或 `pathlib.Path` 对象。
        :returns: 去除首尾空白后的字符串路径。
        :raises ValueError: 当路径类型不支持或路径为空时抛出。
        """
        if not isinstance(value, (str, Path)):
            raise ValueError("path values must be str or Path")
        value = str(value).strip()
        if not value:
            raise ValueError("path values cannot be empty")
        return value


class AsyncSshSocksTunnel:
    """基于 AsyncSSH 的异步 SOCKS 代理隧道。

    该类负责连接远程 SSH 服务器，并在本机启动一个 SOCKS5 代理监听端口。
    默认会在启动时验证 SOCKS 隧道能否访问外网；如果只想验证 SSH 连接
    和本地端口绑定，可在配置中设置 `validate_on_start=False`。
    可以通过 `async with` 自动启动和关闭隧道，也可以手动调用 `start()`
    与 `stop()` 控制生命周期。
    """

    def __init__(self, config: AsyncSshSocksTunnelConfig) -> None:
        """初始化隧道实例。

        初始化不会立即建立 SSH 连接；连接会在调用 `start()` 或进入异步
        上下文管理器时创建。

        :param config: 已通过 Pydantic 校验的隧道配置。
        """
        self.config = config

        self.conn: asyncssh.SSHClientConnection | None = None
        self.listener: asyncssh.SSHListener | None = None

        self._local_port: int | None = None
        self._lock = asyncio.Lock()

    async def __aenter__(self) -> Self:
        """进入异步上下文并启动隧道。

        :returns: 已启动的隧道实例。
        """
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """退出异步上下文并关闭隧道。

        无论上下文内部是否发生异常，都会尝试关闭 SOCKS 监听器和 SSH 连接。
        """
        await self.stop()

    @property
    def is_started(self) -> bool:
        """判断隧道是否处于已启动且 SSH 连接未关闭的状态。"""
        return (
            self.conn is not None
            and self.listener is not None
            and not self.conn.is_closed()
        )

    @property
    def local_host(self) -> str:
        """返回本地 SOCKS 代理监听地址。"""
        return self.config.local_host

    @property
    def local_port(self) -> int:
        """返回本地 SOCKS 代理实际监听端口。

        当配置 `local_port=0` 时，端口由操作系统自动分配；该属性会在
        隧道启动后返回最终绑定的端口。

        :raises RuntimeError: 当隧道尚未启动时抛出。
        """
        if self._local_port is None:
            raise RuntimeError("SSH SOCKS tunnel has not been started")
        return self._local_port

    @property
    def proxy_url(self) -> str:
        """返回可用于 aiohttp-socks 的 SOCKS5 代理 URL。

        `aiohttp_socks.ProxyConnector` 支持 `socks5://`，不支持 curl 风格的
        `socks5h://`。SOCKS5 仍可以转发域名请求，是否远端解析由连接器的
        `rdns` 参数控制。
        """
        return f"socks5://{self.local_host}:{self.local_port}"

    async def start(self) -> None:
        """启动 SSH SOCKS 隧道。

        方法是幂等的：如果隧道已经启动，则直接返回。若上一次启动留下了
        半初始化资源，会先清理旧资源，再重新建立 SSH 连接和 SOCKS 监听器。
        当 `validate_on_start=True` 时，还会在返回前验证出站代理可用性。
        启动过程中发生异常时，会关闭已经创建的资源后再继续抛出异常。
        """
        async with self._lock:
            if self.is_started:
                return

            if self.conn is not None or self.listener is not None:
                await self._close_resources(
                    self.listener,
                    self.conn,
                    self.config.close_timeout,
                )
                self.listener = None
                self.conn = None
                self._local_port = None

            conn: asyncssh.SSHClientConnection | None = None
            listener: asyncssh.SSHListener | None = None

            try:
                conn = await asyncssh.connect(
                    self.config.server_host,
                    port=self.config.server_port,
                    username=self.config.server_user,
                    password=(
                        self.config.server_password.get_secret_value()
                        if self.config.server_password is not None
                        else None
                    ),
                    client_keys=self.config.client_keys,
                    known_hosts=self.config.known_hosts,
                    login_timeout=self.config.connect_timeout,
                    keepalive_interval=self.config.keepalive_interval,
                    keepalive_count_max=self.config.keepalive_count_max,
                )

                listener = await conn.forward_socks(
                    self.config.local_host,
                    self.config.local_port,
                )

                self.conn = conn
                self.listener = listener
                self._local_port = listener.get_port()

                if self.config.validate_on_start:
                    await self.check_outbound_ip()

            except BaseException:
                await self._close_resources(
                    listener,
                    conn,
                    self.config.close_timeout,
                )
                self.conn = None
                self.listener = None
                self._local_port = None
                raise

    async def stop(self) -> None:
        """关闭 SSH SOCKS 隧道。

        方法是幂等的：即使隧道未启动，也可以安全调用。关闭时会先清空实例
        状态，再等待监听器和 SSH 连接关闭，避免并发调用看到过期状态。
        """
        async with self._lock:
            listener = self.listener
            conn = self.conn

            self.listener = None
            self.conn = None
            self._local_port = None

            await self._close_resources(listener, conn, self.config.close_timeout)

    @staticmethod
    async def _close_resources(
        listener: asyncssh.SSHListener | None,
        conn: asyncssh.SSHClientConnection | None,
        timeout: float,
    ) -> None:
        """关闭 AsyncSSH 监听器和连接。

        该方法会先停止本地监听，再尝试优雅关闭 SSH 连接。如果 SSH 连接
        未能在指定时间内关闭，会调用 `abort()` 强制终止。监听器关闭等待
        放在 SSH 连接处理之后，并同样设置上限，避免退出异步上下文后进程
        仍被后台连接挂住。

        :param listener: 可选的本地 SOCKS 监听器。
        :param conn: 可选的 SSH 客户端连接。
        :param timeout: 等待资源关闭的最大时间，单位为秒。
        """
        if listener is not None:
            listener.close()

        if conn is not None:
            conn.close()

        if conn is not None:
            try:
                await asyncio.wait_for(conn.wait_closed(), timeout=timeout)
            except Exception:
                conn.abort()
                with contextlib.suppress(Exception):
                    await asyncio.wait_for(conn.wait_closed(), timeout=1.0)

        if listener is not None:
            with contextlib.suppress(Exception):
                await asyncio.wait_for(listener.wait_closed(), timeout=timeout)

    async def check_local_port(self, timeout: float = 5.0) -> None:
        """检查本地 SOCKS 监听端口是否可连接。

        该方法只验证本机端口是否能建立 TCP 连接，不验证代理转发是否可用。

        :param timeout: 最大等待时间，单位为秒。
        :raises RuntimeError: 当隧道尚未启动时抛出。
        :raises TimeoutError: 当连接检查超时时抛出。
        :raises OSError: 当本地端口无法连接时抛出。
        """
        await asyncio.wait_for(
            self._check_local_port_once(),
            timeout=_validate_timeout(timeout),
        )

    async def _check_local_port_once(self) -> None:
        """执行一次本地监听端口 TCP 连接检查。"""
        _, writer = await asyncio.open_connection(
            self.local_host,
            self.local_port,
        )
        writer.close()
        with contextlib.suppress(Exception):
            await writer.wait_closed()

    async def check_outbound_ip(self, timeout: float = 5.0) -> str:
        """通过 SOCKS 隧道请求健康检查地址并返回出口 IP。

        默认按顺序请求 `health_check_urls` 中的地址。该方法同时支持
        `{"ip": "1.2.3.4"}` 这类 JSON 响应，以及包含 IP 地址的纯文本
        响应，可用于确认请求确实经由 SSH 隧道转发。

        :param timeout: 整个健康检查流程的总超时时间，单位为秒。
        :returns: 健康检查服务返回的出口 IP 字符串。
        :raises RuntimeError: 当隧道尚未启动时抛出。
        :raises ValueError: 当健康检查响应中没有 `ip` 字段时抛出。
        :raises aiohttp.ClientError: 当 HTTP 请求失败时抛出。
        """
        timeout = _validate_timeout(timeout)
        return await asyncio.wait_for(
            self._check_outbound_ip_with_fallback(timeout),
            timeout=timeout,
        )

    async def _check_outbound_ip_with_fallback(self, timeout: float) -> str:
        """按顺序尝试所有健康检查地址并返回第一个成功解析的出口 IP。

        :param timeout: 整个健康检查流程的总超时时间，单位为秒。
        :returns: 解析出的出口 IP。
        :raises RuntimeError: 当所有健康检查地址都失败时抛出。
        """
        urls = self._health_check_urls()
        deadline = asyncio.get_running_loop().time() + timeout
        last_exc: BaseException | None = None

        for index, url in enumerate(urls):
            remaining = deadline - asyncio.get_running_loop().time()
            if remaining <= 0:
                break

            per_url_timeout = remaining / (len(urls) - index)
            try:
                return await asyncio.wait_for(
                    self._fetch_outbound_ip(url, per_url_timeout),
                    timeout=per_url_timeout,
                )
            except Exception as exc:
                last_exc = exc

        raise RuntimeError("all outbound IP health check URLs failed") from last_exc

    def _health_check_urls(self) -> tuple[str, ...]:
        """返回去重后的健康检查地址列表。

        :returns: 按优先级排序的健康检查地址元组。
        """
        urls: list[str] = []
        for url in self.config.health_check_urls:
            if url not in urls:
                urls.append(url)
        return tuple(urls)

    async def _fetch_outbound_ip(self, url: str, timeout: float) -> str:
        """请求单个健康检查地址并解析出口 IP。

        :param url: 健康检查地址。
        :param timeout: 单个请求的超时时间，单位为秒。
        :returns: 解析出的出口 IP。
        """
        timeout_config = aiohttp.ClientTimeout(total=timeout)
        connector = ProxyConnector.from_url(self.proxy_url, rdns=True)

        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout_config,
        ) as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                text = await resp.text()

        return _extract_ip_address(text)

    def create_connector(self) -> ProxyConnector:
        """创建绑定当前隧道代理地址的 aiohttp-socks 连接器。

        调用方负责将连接器交给 `aiohttp.ClientSession` 使用，并按 aiohttp
        的资源管理规则关闭会话。

        :returns: 指向当前 SOCKS 代理的 `ProxyConnector`。
        :raises RuntimeError: 当隧道尚未启动时抛出。
        """
        return ProxyConnector.from_url(self.proxy_url, rdns=True)
