# ymd_utility
ymd_utility is a Python library for working with dates, specifically in YYYY-MM-DD format.

## Required Libraries
- pandas (for US Federal Holiday Calendar)

## Using the Library
The suggested file structure to use this library is:

```
root/
|-- ymd_utility/
|   |-- __init__.py
|   |-- ymd_utility.py
|   |-- requirements.txt
|   `-- README.md
`-- run.py
```

Where the code you write is located in the `run.py` file.

### Creating a YMDDate Object
You can create a YMDDate object from a string, Date, or Datetime object.

```py
from ymd_utility import YMDDate
from datetime import date, datetime

ymd_from_string: YMDDate = YMDDate("2022-04-22")
ymd_from_date: YMDDate = YMDDate(date(2022, 4, 22))
ymd_from_datetime: YMDDate = YMDDate(datetime(2022, 4, 22, 7, 23, 1, 100))

print(ymd_from_string)
print(ymd_from_date)
print(ymd_from_datetime)
```

### Equality Checks
YMDDate object can be compared to strings, date, and datetime objects. Strings must be in the specified YYYY-MM-DD format, as verified by the is_ymd(...) utility function.

```py
from ymd_utility import YMDDate, is_ymd

date_string_to_compare: str = "2022-12-01"
ymd_from_string: YMDDate = YMDDate("2022-04-22")

if is_ymd(date_string_to_compare):
    print(date_string_to_compare == ymd_from_string) # False
```

Inequalities are also provided for less than, greater than, greater than or equal to, and less than or equal to.
```py
from ymd_utility import YMDDate, is_ymd

ymd_1: YMDDate = YMDDate("2022-04-20")
ymd_2: YMDDate = YMDDate("2022-04-22")

print(ymd_1 > ymd_2) # False
print(ymd_1 < ymd_2) # True
```

### Checking for Today's Date

```py
from ymd_utility import YMDDate
from datetime import datetime

not_today: YMDDate = YMDDate("2022-04-22")
print(not_today.is_today()) # False

today = datetime.today()
ymd_today: YMDDate = YMDDate(today)
print(ymd_today.is_today()) # True
```

### Next Day, Month, Year
```py
from ymd_utility import YMDDate
from datetime import datetime

ymd_today: YMDDate = YMDDate(datetime.today())
print("Tomorrow is:", ymd_today.tomorrow())
print("Next week it will be:", ymd_today.next_week())
print("One month from now is:", ymd_today.next_month())
print("Next month is month number:", ymd_today.next_month(full_date=False))
print("Exactly 2 months from now:", ymd_today.n_months(2,units='W',weeks_per_month=4))
print("2 months ago, it was:", ymd_today.n_months(-2, units='W', weeks_per_month=4))
print("One year from now is:", ymd_today.next_year())
print("Next year will be:", ymd_today.next_year(full_date=False))
print("5 years ago it was:", ymd_today.n_years(-5, units='W'))
```

### Type Conversions
```py
from ymd_utility import YMDDate
from datetime import datetime

ymd_today: YMDDate = YMDDate(datetime.today())
print("YMD as a string: ", str(ymd_today))
print("YMD as a date: ", ymd_today.to_date(), " Type: ", type(ymd_today.to_date()))
print("YMD as datetime: ", ymd_today.to_datetime(), " Type: ", type(ymd_today.to_datetime()))
```

### Weekdays, Weekends, Days of the Week

```py
from ymd_utility import YMDDate
from datetime import datetime

ymd_today: YMDDate = YMDDate(datetime.today())
print("Is today a weekday (Monday - Friday)?", ymd_today.is_weekday())
print("Is today a Saturday or Sunday?", ymd_today.is_weekend())
print("Today is: ", ymd_today.get_weekday())
print("Today (abbreviated) is: ", ymd_today.get_weekday(abbreviated=True))
```

### Next Business Day
Obtain the next business using the `next_business_day()` method. It automatically takes into account US Federal Holidays and weekends. It does _not_ take into account user-defined holidays (discussed later).

```py
from ymd_utility import YMDDate
from datetime import datetime

ymd_friday = YMDDate("2024-02-23") # A Friday
print("The next business day from 2024-02-23 is: ", ymd_friday.next_business_day()) # Monday (2/26/2024)
```

### Holidays
User-defined holidays are defined using a list of strings in YYYY-MM-DD format, or a list of YMDDate objects.

```py
from ymd_utility import YMDDate

holidays = ["2024-01-01", "2024-12-31"]
ymd_holiday = YMDDate("2024-12-31")

print(f"Is {ymd_holiday} a holiday?", ymd_holiday.is_holiday(holidays))
print(f"Is 2024-03-04 a holiday?", YMDDate("2024-03-04").is_holiday(holidays))
```

#### US Federal Holidays

For US Federal Holidays, use the following:

```py
from ymd_utility import YMDDate

new_years_2024 = YMDDate("2024-01-01")
print("New Years Day in 2024 was a federal holiday: ", new_years_2024.is_us_federal_holiday())
new_years_2022 = YMDDate("2022-01-01")
print("New Years Day in 2022 was a federal holiday: ", new_years_2022.is_us_federal_holiday())
```

## Contact and Issues
Feel free to create [issue requests](https://github.com/Quantastic-Research/ymd_utility/issues) in this repo. [GitHub Profile](https://github.com/dpsciarrino).

Blog: [Quantastic Research](https://quantasticresearch.com/)
