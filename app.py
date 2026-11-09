from datetime import datetime

from facades import ClockFacade


def main() -> None:
    clock = ClockFacade()
    clock.set_date_time(datetime.now().replace(microsecond=0))
    print(f"Время: {clock.get_formatted_date_time()}")
    print("История установок:")
    for value in clock.get_history():
        print(f"  {value:%d.%m.%Y %H:%M:%S}")


if __name__ == "__main__":
    main()
