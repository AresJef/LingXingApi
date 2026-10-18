"""汇率日期仅按cytimes解析并格式化；月份输入补日，完整日期保留。"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from lingxingapi.basic.schema import ExchangeRate


def rate_values(date: str) -> dict[str, object]:
    """复用既有公开fixture的其他字段，仅替换待测日期。"""
    fixture = Path(__file__).with_name("fixtures") / "basic/exchange_rates.json"
    row = json.loads(fixture.read_bytes())["response"]["data"][0]
    return {**row, "date": date}


@pytest.mark.parametrize("source,expected", [
    ("2026-09", "2026-09-01"),
    ("2026-09-17", "2026-09-17"),
    ("2024-02-29", "2024-02-29"),
])
def test_exchange_rate_date_parses_month_or_full_date_as_string(source: str, expected: str):
    rate = ExchangeRate.model_validate(rate_values(source))
    assert type(rate.date) is str and rate.date == expected
    assert rate.model_dump()["date"] == expected
    assert json.loads(rate.model_dump_json())["date"] == expected


@pytest.mark.parametrize("source", ["not-a-date", ""])
def test_exchange_rate_date_parse_failure_is_a_pydantic_validation_error(source: str):
    with pytest.raises(ValidationError) as error:
        ExchangeRate.model_validate(rate_values(source))
    issue, = error.value.errors()
    assert issue["loc"] == ("date",) and issue["type"] == "value_error"
    assert isinstance(issue["ctx"]["error"], ValueError)
