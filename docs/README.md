# Структурная диаграмма

```mermaid
classDiagram
    class BaseDigitalClock {
        <<interface>>
        +set_date_time(datetime)
        +get_date_time() datetime
    }
    class BaseAnalogClock {
        <<interface>>
        +set_date_time(year, month, day, hour_angle, minute_angle, second_angle, AM_PM)
        +get_hour_angle() float
        +get_minute_angle() float
        +get_second_angle() float
        +get_day_night_division() DayNightDivision
    }
    class AnalogClock
    class DigitalClockAdapter
    class ClockFormatter {
        +format(datetime, fmt) str
    }
    class ClockHistory {
        +add(datetime)
        +all() tuple
    }
    class ClockFacade {
        +set_date_time(datetime)
        +get_date_time() datetime
        +get_formatted_date_time(fmt) str
        +get_history() tuple
    }
    class DigitalClockDisplay

    BaseDigitalClock <|.. DigitalClockAdapter
    BaseAnalogClock <|.. AnalogClock
    DigitalClockAdapter *-- BaseAnalogClock : хранит
    ClockFacade *-- DigitalClockAdapter
    ClockFacade *-- ClockFormatter
    ClockFacade *-- ClockHistory
    DigitalClockDisplay --> BaseDigitalClock : использует
```

`app.py` обращается только к `ClockFacade`. Отдельный клиент
`DigitalClockDisplay` может напрямую использовать `DigitalClockAdapter`, поскольку
тот реализует `BaseDigitalClock`.
