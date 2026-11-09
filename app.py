from datetime import datetime

from facades import ClockFacade
from adapters import DigitalClockAdapter
from clocks import AnalogClock
from services import ClockFormatter, ClockHistory


def main() -> None:
    clock = ClockFacade(
        DigitalClockAdapter(AnalogClock()),
        ClockFormatter(),
        ClockHistory(),
    )

    for value in (
        datetime(2026, 11, 5, 0, 0, 0),
        datetime(2026, 11, 5, 12, 0, 0),
        datetime(2026, 11, 5, 18, 45, 30, 123456),
    ):
        clock.set_date_time(value)
        print(f"Установлено: {value.isoformat()} -> прочитано: {clock.get_date_time().isoformat()}")
        print(f"Форматированное: {clock.get_formatted_date_time()}")

    print(f"Время (ISO): {clock.get_formatted_date_time('%Y-%m-%dT%H:%M:%S')}")
    print("История изменений:")
    for item in clock.get_history():
        print(f"  {item.isoformat()}")


if __name__ == "__main__":
    main()
