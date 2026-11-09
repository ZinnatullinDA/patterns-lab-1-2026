from datetime import datetime

from clocks import AnalogClock
from consts import DayNightDivision
from interfaces import BaseAnalogClock, BaseDigitalClock


class DigitalClockAdapter(BaseDigitalClock):
    def __init__(self, clock: BaseAnalogClock | None = None) -> None:
        self._clock = clock if clock is not None else AnalogClock()

    def set_date_time(self, date: datetime) -> None:
        if date.utcoffset() is not None:
            raise ValueError("Аналоговые часы не хранят часовой пояс")

        seconds = date.second + date.microsecond / 1_000_000
        minutes = date.minute + seconds / 60
        hours = date.hour % 12 + minutes / 60
        self._clock.set_date_time(
            date.year,
            date.month,
            date.day,
            hours * 30,
            minutes * 6,
            seconds * 6,
            DayNightDivision.AM if date.hour < 12 else DayNightDivision.PM,
        )

    def get_date_time(self) -> datetime:
        total_microseconds = round(self._clock.get_second_angle() / 6 * 1_000_000)
        total_microseconds %= 60_000_000
        second, microsecond = divmod(total_microseconds, 1_000_000)
        minute = int(self._clock.get_minute_angle() // 6) % 60
        hour_12 = int(self._clock.get_hour_angle() // 30) % 12
        division = self._clock.get_day_night_division()
        if division not in (DayNightDivision.AM, DayNightDivision.PM):
            raise ValueError("Неизвестное значение AM/PM")
        hour = hour_12 + (12 if division is DayNightDivision.PM else 0)
        return datetime(
            self._clock.get_year(),
            self._clock.get_month(),
            self._clock.get_day(),
            hour,
            minute,
            second,
            microsecond,
        )
