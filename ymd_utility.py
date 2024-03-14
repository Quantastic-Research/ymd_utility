from datetime import datetime as dt
from datetime import date as date_object
from datetime import timedelta

from pandas.tseries.holiday import USFederalHolidayCalendar

from re import compile, IGNORECASE


def is_ymd(ymd_date: str) -> bool:
    """
    Takes in a string representation of a date. Checks to make sure it
    is a valid date in YYYY-MM-DD format.

    Parameters:
    -----------
    - ymd_date: str = Input string representing a date.
    """
    # Check regex pattern for YYYY-MM-DD format
    date_pattern = compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", IGNORECASE)
    if not date_pattern.match(ymd_date):
        return False
    
    year, month, day = ymd_date.split("-")
    try:
        date_object(int(year), int(month), int(day))
        return True
    except ValueError:
        return False

def is_ymd_date(ymd_date: date_object) -> bool:
    """
    Takes in a datetime.date object. Checks to make sure it
    contains valid YMD date data.

    Parameters:
    -----------
    - ymd_date: datetime.date = Date object to verify.
    """
    # Convert date to string
    ymd_string = str(ymd_date)
    return is_ymd(ymd_string)

def is_ymd_datetime(ymd_datetime: dt) -> bool:
    """
    Takes in a datetime.datetime object. Checks to make sure it
    contains valid YMD date data.

    Parameters:
    -----------
    - ymd_datetime: datetime.datetime = Datetime object to verify.
    """
    # Expects a string representation with hour:minute:second.ms data
    dt_string = str(ymd_datetime)
    # Remove hour:minute:second.ms data from string
    ymd_str = dt_string.split(" ")[0]
    # Wrap is_ymd function
    return is_ymd(ymd_str)


class YMDDate:
    def __init__(self, date: str | date_object | dt):
        """
        YMDDate takes in a date as a string object, Date object, or Datetime object.

        The date is stored in a way that is easily accessible through attributes and 
        return methods. See the README for information on how to use this class.

        Parameters:
        -----------
        One required parameter is accepted as three separate types:
            str|datetime.date|datetime.datetime

        date: str = A string in YMD format. For verification checks, use the provided
            is_ymd() function.
        date: datetime.date = A datetime.date object. For verification checks, use the
            provided is_ymd_date() function.
        date: datetime.datetime = A datetime.datetime object. For verification checks, 
            use the provided is_ymd_datetime() function.
        """
        self._year: str = None
        self._month: str = None
        self._day: str = None

        self._DAYS_OF_THE_WEEK = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

        # User-defined holidays
        self._holidays: list = []

        if type(date) == str:
            if is_ymd(date):
                self._year, self._month, self._day = self._ymd_from_string(date)
            else:
                raise ValueError(f"String {date} is not in YYYY-MM-DD format or not a valid date.")
        elif type(date) == date_object:
            if is_ymd_date(date):
                self._year, self._month, self._day = self._ymd_from_date(date)
            else:
                raise ValueError(f"Date object {str(date)} is not valid.")
        elif type(date) == dt:
            if is_ymd_datetime(date):
                self._year, self._month, self._day = self._ymd_from_datetime(date)
            else:
                raise ValueError(f"Datetime object {str(date)} is not valid.")
        else:
            raise ValueError(f"YMDDate accepts a Date object, Datetime object, or string value. Got {type(date)}")
        
    
    @property
    def year(self):
        return self._year
    
    @property
    def month(self):
        return self._month
    
    @property
    def day(self):
        return self._day
    
    def is_us_federal_holiday(self):
        """
        Checks whether the YMDDate represents a US federal holiday.
        """
        # Determine whether the date given is a holiday
        start_date = f"{self._year}-01-01"
        end_date = f"{self._year}-12-31"
        cal = USFederalHolidayCalendar()
        holidays_datetime = cal.holidays(start=start_date, end=end_date).to_pydatetime()
        holidays = [h.date() for h in holidays_datetime]
        
        if self.to_date() in holidays:
            return True
        
        return False
    
    def is_holiday(self, holidays:list):
        """
        Checks whether the YMDDate is in the given holidays list.

        Parameters:
        -----------
        - holidays: list of YMDDate objects (or strings in format "YYYY-MM-DD") to check against.
        """
        if len(holidays) == 0:
            return False
        
        for holiday in holidays:
            # For strings, convert into YMDDate object and compare to self
            if type(holiday) == str:
                try:
                    ymd_holiday = YMDDate(holiday)
                except ValueError as ve:
                    print(ve.args[0])
                    return None
                
                if ymd_holiday == self:
                    return True
                
            # For YMDDate objects, compare to self
            elif type(holiday) == self.__class__:
                if holiday == self:
                    return True
            
        return False
    
    def is_today(self):
        """
        Checks whether the YMDDate represents today's date.
        """
        today = dt.today()
        if (int(self._year) == today.year) and (int(self._month) == today.month) and (int(self._day) == today.day):
            return True
        return False
    
    def is_weekend(self):
        """
        Checks whether the YMDDate represents a Saturday or Sunday.
        """
        if dt.weekday(self.to_date()) >= 5:
            return True
        return False
    
    def is_weekday(self):
        """
        Checks whether the YMDDate represents a week day (Monday - Friday)
        """
        if dt.weekday(self.to_date()) < 5:
            return True
        return False
    
    def get_weekday(self, name: bool = True, abbreviated: bool = False, abbreviations:list=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
        """
        Returns the weekday (Monday, Tuesday, etc.) that YMDDate falls on.

        Parameters:
        -----------
        - name: bool = If True, returns the name of the day as a string.
            If False, returns the associated number from datetime from 0 to 6 with
            0 representing Monday.
        - abbreviated: bool = If True, then names are abbreviated as described in abbreviations parameter:
            'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'
        - abbreviations: list = The abbreviations used when abbreviated is True. Length must be 7.
        """
        if name is None:
            raise ValueError("get_weekday parameter 'name' cannot be None.")
        
        if len(abbreviations) != 7:
            raise ValueError("Length of abbreviations list must be 7.")
        
        # Returns the number associated with the day of the week
        if name == False:
            return dt.weekday(self.to_date())
        # Returns the weekday name associated with the day number
        elif name == True:
            # Obtain day number from datetime module
            day_number = dt.weekday(self.to_date())
            # Abbreviate if necessary
            if abbreviated:
                return abbreviations[day_number]
            # Otherwise, return full name
            return self._DAYS_OF_THE_WEEK[day_number]

        raise ValueError("Exception from get_weekday() function.")
    
    def n_days(self, days:int):
        """
        Gets the date exactly n days from the YMDDate. Returns as a YMDDate object.
        
        Parameters:
        -----------
        - days: int representing number of days to jump. Negative numbers go backwards in time.
            Positive numbers go forward in time. Zero duplicates the current YMDDate as a
            second instance.
        """
        if days is None:
            raise ValueError("n_days parameter 'days' cannot be None.")
        
        if days > 0:
            return YMDDate(self.to_datetime() + timedelta(days = days))
        elif days < 0:
            return YMDDate(self.to_datetime() - timedelta(days = abs(days)))
        
        return YMDDate(self.to_datetime())
    
    def n_weeks(self, weeks:int):
        """
        Gets the date exactly n weeks from the YMDDate. Returns as a YMDDate object.
        
        Parameters:
        -----------
        - weeks: int representing number of weeks to jump. Negative numbers go backwards in time.
            Positive numbers go forward in time. Zero duplicates the current YMDDate as a
            second instance.
        """
        if weeks is None:
            raise ValueError("n_weeks parameter 'weeks' cannot be None.")
        
        if weeks > 0:
            return YMDDate(self.to_datetime() + timedelta(weeks = weeks))
        elif weeks < 0:
            return YMDDate(self.to_datetime() - timedelta(weeks = abs(weeks)))
        
        return YMDDate(self.to_datetime())
    
    def n_months(self, months: int, units:str = "W", weeks_per_month: int = 4, days_per_month: int = 30):
        """
        Gets the date exactly n months from the YMDDate. Returns as a YMDDate object.
        
        Parameters:
        -----------
        - months: int representing number of months to jump. Negative numbers go backwards in time.
            Positive numbers go forward in time. Zero duplicates the current YMDDate as a
            second instance.
        - units: a string value representing whether to measure 1 month in weeks or days
            For weeks, specify 'W' and use the weeks_per_month parameter.
            For days, specify 'D' and use the days_per_month parameter.
        - weeks_per_month: an integer specifying the number of weeks to consider as 1 month.
        - days_per_month: an integer specifying the number of days to consider as 1 month. 
        """
        if months is None:
            raise ValueError("n_days parameter 'months' cannot be None.")
        
        if months == 0:
            return YMDDate(self.to_datetime())
        
        if units.upper() == 'W':
            number_of_weeks = abs(weeks_per_month * months)
            if months > 0:
                return YMDDate(self.to_datetime() + timedelta(weeks = number_of_weeks))
            elif months < 0:
                return YMDDate(self.to_datetime() - timedelta(weeks = number_of_weeks))
            
        elif units.upper() == 'D':
            number_of_days = abs(days_per_month * months)
            if months > 0:
                return YMDDate(self.to_datetime() + timedelta(days = number_of_days))
            elif months < 0:
                return YMDDate(self.to_datetime() - timedelta(days = number_of_days))
        
        else:
            raise ValueError("Units parameter must be either 'W' or 'D'.")

    
    def n_years(self, years: int, units: str = "W", days_per_year: int = 365, weeks_per_year: int = 52):
        """
        Gets the date exactly n years from the YMDDate. Returns as a YMDDate object.
        
        Parameters:
        -----------
        - years: int representing number of years to jump. Negative numbers go backwards in time.
            Positive numbers go forward in time. Zero duplicates the current YMDDate as a
            second instance.
        - units: a string value representing whether to measure 1 year in weeks or days
            For weeks, specify 'W' and use the weeks_per_year parameter.
            For days, specify 'D' and use the days_per_year parameter.
        - weeks_per_year: an integer specifying the number of weeks to consider as 1 year.
        - days_per_year: an integer specifying the number of days to consider as 1 year. 
        """
        if years is None:
            raise ValueError("n_years parameter 'years' cannot be None.")
        
        if years == 0:
            return YMDDate(self.to_datetime())

        if units == 'D':
            number_of_days = abs(years * days_per_year)
            if years > 0:
                return YMDDate(self.to_datetime() + timedelta(days = number_of_days))
            elif years < 0:
                return YMDDate(self.to_datetime() - timedelta(days = number_of_days))
        elif units == 'W':
            number_of_weeks = abs(years * weeks_per_year)
            if years > 0:
                return YMDDate(self.to_datetime() + timedelta(weeks = number_of_weeks))
            elif years < 0:
                return YMDDate(self.to_datetime() - timedelta(weeks = number_of_weeks))
        
        else:
            raise ValueError("Units parameter must be either 'W' or 'D'.")
    
    def next_business_day(self):
        """
        Retrieves the next business day, accounting for weekends and US Federal holidays.

        Returns a YMDDate instance.
        """
        next_day = self.tomorrow()

        while next_day.is_us_federal_holiday() or next_day.is_weekend():
            next_day = next_day.tomorrow()
        
        return next_day
    
    def next_week(self):
        """
        Retrieves the date exactly one week from YMDDate. Returns as a YMDDate object.
        """
        next_week:dt = self.to_datetime() + timedelta(days = 7)
        return YMDDate(next_week)
    
    def next_month(self, full_date=True):
        """
        Parameters:
        -----------
        - full_date: bool = If True, returns the YMDDate exactly one month from current. If
            False, returns the month as an integer between 1 and 12, inclusive.
        """
        if full_date:
            return self.n_months(1)
        
        return int(self.n_months(1).month)
    
    def next_year(self, full_date=True):
        """
        Parameters:
        -----------
        - full_date: bool = If True, returns the YMDDate exactly one year from current. If
            False, returns the year as an integer.
        """
        if full_date:
            return self.n_years(1)
        
        return int(self.year) + 1
    
    def tomorrow(self):
        """
        Returns tomorrows date as a YMDDate object.
        """
        next_day:dt = self.to_datetime() + timedelta(days = 1)
        return YMDDate(next_day)
    
    def to_date(self) -> date_object:
        """
        Converts YMDDate object to date object.
        """
        return date_object(int(self._year), int(self._month), int(self._day))
    
    def to_datetime(self) -> dt:
        """
        Converts YMDDate object to datetime object.
        """
        return dt(year=int(self._year), month=int(self._month), day=int(self._day))
    
    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            if (self._year == other.year) and (self._month == other.month) and (self._day == other.day):
                return True
            return False
        elif isinstance(other, str):
            if is_ymd(other):
                y, m, d = self._ymd_from_string(other)
                if (self._year == y) and (self._month == m) and (self._day == d):
                    return True
            return False
        elif isinstance(other, dt):
            if is_ymd_datetime(other):
                (y, m, d) = self._ymd_from_datetime(other) # strings
                if (self._year == y) and (self._month == m) and (self._day == d):
                    return True
            return False
        elif isinstance(other, date_object):
            if is_ymd_date(other):
                (y, m, d) = self._ymd_from_date(other) # strings
                if (self._year == y) and (self._month == m) and (self._day == d):
                    return True
            return False
        else:
            return False
        
    def __gt__(self, other) -> bool:
        # Calculate this objects date representation
        this_date = date_object(int(self._year), int(self._month), int(self._day))

        # Compare all supported instances
        if isinstance(other, self.__class__):
            other_date = date_object(int(other._year), int(other._month), int(other._day))
            return this_date > other_date
        
        elif isinstance(other, str):
            if is_ymd(other):
                y, m, d = self._ymd_from_string(other)
                other_date = date_object(int(y), int(m), int(d))
                
                return this_date > other_date
            return False
        
        elif isinstance(other, dt):
            if is_ymd_datetime(other):
                (y, m, d) = self._ymd_from_datetime(other) # strings
                other_date = date_object(int(y), int(m), int(d))

                return this_date > other_date
                
            return False
        elif isinstance(other, date_object):
            if is_ymd_date(other):
                (y, m, d) = self._ymd_from_date(other) # strings
                other_date = date_object(int(y), int(m), int(d))
                return this_date > other_date
            
            return False
        else:
            return False
    
    def __ge__(self, other) -> bool:
        # Calculate this objects date representation
        this_date = date_object(int(self._year), int(self._month), int(self._day))

        # Compare all supported instances
        if isinstance(other, self.__class__):
            other_date = date_object(int(other._year), int(other._month), int(other._day))
            return this_date >= other_date
        
        elif isinstance(other, str):
            if is_ymd(other):
                y, m, d = self._ymd_from_string(other)
                other_date = date_object(int(y), int(m), int(d))
                
                return this_date >= other_date
            return False
        
        elif isinstance(other, dt):
            if is_ymd_datetime(other):
                (y, m, d) = self._ymd_from_datetime(other) # strings
                other_date = date_object(int(y), int(m), int(d))

                return this_date >= other_date
                
            return False
        elif isinstance(other, date_object):
            if is_ymd_date(other):
                (y, m, d) = self._ymd_from_date(other) # strings
                other_date = date_object(int(y), int(m), int(d))
                return this_date >= other_date
            
            return False
        else:
            return False

    def __str__(self):
        """
        Use str(YMDDate) to easily obtain the YYYY-MM-DD string representation.
        """
        return f"{self._year}-{self._month}-{self._day}"
    
    def _ymd_from_string(self, ymd_string: str):
        """
        !!!INTERNAL METHOD!!!
        This method should only be used by the Watchlists library classes and functions. Outside use
        is not suggested and may result in broken code and unexpected behavior.

        Description:
        ------------
        Converts a verified string-representation of a YYYY-MM-DD date to a 3-tuple of year, month, date
        string values. Returns as a 3-tuple.
        """
        year, month, day = ymd_string.split("-")
        return (str(year), str(month), str(day))
    
    def _ymd_from_date(self, ymd_date: date_object):
        """
        !!!INTERNAL METHOD!!!
        This method should only be used by the Watchlists library classes and functions. Outside use
        is not suggested and may result in broken code and unexpected behavior.

        Description:
        ------------
        Converts a verified date-representation of a YYYY-MM-DD date to a 3-tuple of year, month, date
        string values. Returns as a 3-tuple.
        """
        # Convert date object to string and wrap _ymd_from_string method
        ymd_str = str(ymd_date)
        return self._ymd_from_string(ymd_str)

    def _ymd_from_datetime(self, ymd_datetime: dt):
        """
        !!!INTERNAL METHOD!!!
        This method should only be used by the Watchlists library classes and functions. Outside use
        is not suggested and may result in broken code and unexpected behavior.

        Description:
        ------------
        Converts a verified datetime-representation of a YYYY-MM-DD date to a 3-tuple of year, month, date
        string values. Returns as a 3-tuple.
        """
        # Convert datetime object to string and extract YYYY-MM-DD representation.
        ymd_str = str(ymd_datetime).split(" ")[0]
        return self._ymd_from_string(ymd_str)


