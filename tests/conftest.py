"""正式测试只使用当前项目 SDK，并禁止外部连接。"""

import socket
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """正式 pytest 的失败报告只保留安全诊断；原异常仍供受控 runner 分类。"""
    from response_contract import ContractError

    report = (yield).get_result()
    if report.failed and call.excinfo:
        error = call.excinfo.value
        if isinstance(error, ContractError):
            report.longrepr = f"ContractError[{error.status}]:\n" + "\n".join(error.issues)
        elif item.name == "test_api_contract":
            report.longrepr = f"契约核验运行错误：{type(error).__name__}；未显示原始响应或异常输入"
        else:
            return
        # 捕获输出同样可能含输入；不把它附到失败报告。
        report.sections = []


def pytest_addoption(parser):
    parser.addoption("--marketplace-raw", default=None, metavar="PATH", help="核验固定 raw；缺文件明确 FAIL")
    parser.addoption(
        "--marketplace-fixture",
        default=None,
        metavar="PATH",
        help="显式改为核验脱敏数据集；默认核验固定 raw，检查不写文件",
    )


@pytest.fixture
def contract_case(request):
    if hasattr(request.config, "_contract_case"):
        return request.config._contract_case
    from response_contract import DEFAULT_RAW
    from lingxingapi.basic.schema import Marketplaces
    dataset = request.config.getoption("--marketplace-fixture")
    if dataset:
        return {"fixture": Path(dataset)}
    path = Path(request.config.getoption("--marketplace-raw") or DEFAULT_RAW)
    if path.suffix != ".json" or path.is_symlink() or not path.is_file():
        return {"error": f"原始数据不存在或不是普通 JSON 文件：{path}"}
    try:
        return {"snapshot": path.read_bytes(), "schema": Marketplaces}
    except OSError:
        return {"error": f"原始数据读取失败：{path}"}


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def blocked(*args, **kwargs):
        pytest.fail("正式回归禁止网络和 DNS")

    for target, name in (
        (socket.socket, "connect"),
        (socket.socket, "connect_ex"),
        (socket, "create_connection"),
        (socket, "getaddrinfo"),
    ):
        monkeypatch.setattr(target, name, blocked)
