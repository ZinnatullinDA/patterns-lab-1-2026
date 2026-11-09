from datetime import datetime, timezone

import pytest

from adapters import DigitalClockAdapter
from clocks import AnalogClock
from facades import ClockFacade
from services import ClockFormatter, ClockHistory


def test_facade_exposes_current_value_format_and_history() -> None:
    analog = AnalogClock()
    facade = ClockFacade(
        clock=DigitalClockAdapter(analog),
        formatter=ClockFormatter(),
        history=ClockHistory(),
    )
    values = [
        datetime(2026, 9, 24, 12, 34, 56),
        datetime(2026, 9, 25, 0, 0, 1, 123456),
        datetime(2026, 9, 25, 23, 59, 59),
    ]

    assert facade.get_date_time() == datetime(2000, 1, 1)
    assert facade.get_history() == ()

    for value in values:
        facade.set_date_time(value)

    assert facade.get_date_time() == values[-1]
    assert facade.get_formatted_date_time() == values[-1].strftime("%d.%m.%Y %H:%M:%S")
    assert facade.get_formatted_date_time("%Y-%m-%d") == values[-1].strftime("%Y-%m-%d")
    assert facade.get_history() == tuple(values)
    assert analog.get_day() == values[-1].day


def test_failed_update_does_not_enter_history() -> None:
    facade = ClockFacade(
        clock=DigitalClockAdapter(AnalogClock()),
        formatter=ClockFormatter(),
        history=ClockHistory(),
    )
    value = datetime(2026, 9, 24, 12)
    facade.set_date_time(value)

    with pytest.raises(ValueError):
        facade.set_date_time(datetime(2026, 9, 25, tzinfo=timezone.utc))

    assert facade.get_date_time() == value
    assert facade.get_history() == (value,)
