"""公开States fixture契约；明确真实样本文件，复用原严格checker。"""

from pathlib import Path

from lingxingapi.basic.schema import States
from response_contract import ContractError, load_json_bytes, validate_response

FIXTURE = Path(__file__).with_name("fixtures") / "basic/states.json"


def test_states_fixture_contract() -> None:
    if FIXTURE.is_symlink() or not FIXTURE.is_file():
        raise ContractError("input_error", [f"States fixture不存在或不是普通文件：{FIXTURE}"])
    fixture = load_json_bytes(FIXTURE.read_bytes())
    if type(fixture) is not dict or fixture.get("source") not in {"live", "local_raw"}:
        raise ContractError("input_error", ["States fixture缺少实际样本包装身份"])
    if fixture.get("endpoint") != "basic.States":
        raise ContractError("input_error", ["States fixture接口身份不符"])
    validate_response(fixture.get("response"), States)
