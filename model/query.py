from datetime import date, timedelta
import datetime as dt

import numpy as np


class Query:
    def __init__(self, worked_time: timedelta = None, from_date: date = dt.datetime.today().replace(day=1).date(),
                 to_date: date = (dt.datetime.today() + dt.timedelta(days=1)).date(),
                 week_mask=np.array([1, 1, 1, 1, 1, 0, 0]), holidays=None):
        self.worked_time = worked_time
        self.from_date = from_date
        self.to_date = to_date
        self.week_mask = week_mask
        self.holidays = holidays
        self.all_week_mask = np.ones(7)

    def days_passed(self):
        return np.busday_count(self.from_date, self.to_date, self.all_week_mask)

    def work_days_per_week(self):
        return sum(self.week_mask)

    def working_days_passed(self):
        return np.busday_count(self.from_date, self.to_date, self.week_mask)
