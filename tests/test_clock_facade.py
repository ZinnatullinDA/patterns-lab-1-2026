from datetime import datetime, timezone

import pytest

from clocks import AnalogClock
from facades import ClockFacade


def test_facade_exposes_current_value_format_and_history() -> None:
    analog = AnalogClock()
    facade = ClockFacade(analog)
    first = datetime(2026, 9, 24, 12, 34, 56)
    second = datetime(2026, 9, 25, 0, 0, 1, 123456)

    assert facade.get_date_time() == datetime(2000, 1, 1)
    assert facade.get_history() == ()

    facade.set_date_time(first)
    facade.set_date_time(second)

    assert facade.get_date_time() == second
    assert facade.get_formatted_date_time() == "25.09.2026 00:00:01"
    assert facade.get_formatted_date_time("%Y-%m-%d") == "2026-09-25"
    assert facade.get_history() == (first, second)
    assert analog.get_day() == 25


def test_failed_update_does_not_enter_history() -> None:
    facade = ClockFacade()
    value = datetime(2026, 9, 24, 12)
    facade.set_date_time(value)

    with pytest.raises(ValueError):
        facade.set_date_time(datetime(2026, 9, 25, tzinfo=timezone.utc))

    assert facade.get_date_time() == value
    assert facade.get_history() == (value,)
