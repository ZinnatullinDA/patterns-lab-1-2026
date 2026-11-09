from datetime import datetime

from adapters import DigitalClockAdapter
from interfaces import BaseAnalogClock
from services import ClockFormatter, ClockHistory


class ClockFacade:
    def __init__(self, clock: BaseAnalogClock | None = None) -> None:
        self._clock = DigitalClockAdapter(clock)
        self._formatter = ClockFormatter()
        self._history = ClockHistory()

    def set_date_time(self, value: datetime) -> None:
        self._clock.set_date_time(value)
        self._history.add(self._clock.get_date_time())

    def get_date_time(self) -> datetime:
        return self._clock.get_date_time()

    def get_formatted_date_time(self, fmt: str = "%d.%m.%Y %H:%M:%S") -> str:
        return self._formatter.format(self.get_date_time(), fmt)

    def get_history(self) -> tuple[datetime, ...]:
        return self._history.all()
