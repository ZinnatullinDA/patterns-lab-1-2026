from datetime import datetime, timedelta, timezone

import pytest

from adapters import DigitalClockAdapter
from clocks import AnalogClock
from consts import DayNightDivision
from interfaces import BaseDigitalClock


@pytest.mark.parametrize(
    ("value", "division"),
    [
        (datetime(2026, 1, 1, 0, 0, 0), DayNightDivision.AM),
        (datetime(2026, 1, 1, 11, 59, 59), DayNightDivision.AM),
        (datetime(2026, 1, 1, 12, 0, 0), DayNightDivision.PM),
        (datetime(2026, 1, 1, 23, 59, 59, 999999), DayNightDivision.PM),
        (datetime(2024, 2, 29, 15, 30, 45, 123456), DayNightDivision.PM),
    ],
)
def test_round_trip_and_am_pm(value: datetime, division: DayNightDivision) -> None:
    analog = AnalogClock()
    adapter = DigitalClockAdapter(analog)

    assert isinstance(adapter, BaseDigitalClock)
    adapter.set_date_time(value)

    assert adapter.get_date_time() == value
    assert analog.get_day_night_division() is division


def test_hand_angles_include_smaller_units() -> None:
    analog = AnalogClock()
    DigitalClockAdapter(analog).set_date_time(datetime(2026, 9, 24, 15, 30, 45))

    assert analog.get_hour_angle() == pytest.approx(105.375)
    assert analog.get_minute_angle() == pytest.approx(184.5)
    assert analog.get_second_angle() == pytest.approx(270)


@pytest.mark.parametrize(
    ("division", "expected_hour"),
    [(DayNightDivision.AM, 3), (DayNightDivision.PM, 15)],
)
def test_reads_existing_analog_clock(
    division: DayNightDivision, expected_hour: int
) -> None:
    analog = AnalogClock()
    analog.set_date_time(2026, 9, 24, 105.375, 184.5, 270, division)

    assert DigitalClockAdapter(analog).get_date_time() == datetime(
        2026, 9, 24, expected_hour, 30, 45
    )


def test_reads_independently_set_hand_angles() -> None:
    analog = AnalogClock()
    analog.set_date_time(2026, 9, 24, 90, 180, 270, DayNightDivision.PM)

    assert DigitalClockAdapter(analog).get_date_time() == datetime(2026, 9, 24, 15, 30, 45)


def test_rejects_timezone_that_analog_clock_cannot_store() -> None:
    adapter = DigitalClockAdapter()
    original = adapter.get_date_time()

    with pytest.raises(ValueError, match="часовой пояс"):
        adapter.set_date_time(datetime(2026, 9, 24, tzinfo=timezone(timedelta(hours=5))))

    assert adapter.get_date_time() == original
