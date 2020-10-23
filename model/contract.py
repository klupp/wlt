import datetime as dt
from datetime import date, timedelta

import numpy as np

from model.query import Query
from model.salary import Salary
from model.stats import ContractStats, SalaryStats


class Contract:
    def __init__(self, employer: str, week_hours: float, start: date = date.today(), end: date = None,
                 hourly_salary: Salary = None):
        self.employer = employer
        self.start = start
        self.end = end
        self.hourly_salary = hourly_salary
        self.week_hours = week_hours

    def __str__(self):
        return "Contract with %s from %s to %s with hourly salary %s. Workload %.2f hours weekly" % (
            self.employer, self.start, self.end, self.hourly_salary, self.week_hours)

    def stats(self, query: Query):
        from_date = max(query.from_date, self.start)
        if self.end is None:
            to_date = query.to_date
        else:
            to_date = min(query.to_date, self.end)

        working_days = np.busday_count(from_date, to_date, query.week_mask)

        workload_per_week = dt.timedelta(milliseconds=self.week_hours * 3600000)

        hours_per_day = self.week_hours / query.work_days_per_week()
        workload_per_day = dt.timedelta(milliseconds=hours_per_day * 3600000)

        total_working_hours = working_days * hours_per_day
        total_working_time = dt.timedelta(milliseconds=total_working_hours * 3600000)
        remaining_working_time: timedelta = None
        if query.worked_time is not None:
            remaining_working_time = total_working_time - query.worked_time

        salary_stats: SalaryStats = None
        if self.hourly_salary is not None:
            salary_stats = self.hourly_salary.stats(query, total_working_hours)

        return ContractStats(self, from_date, to_date, working_days, workload_per_week, workload_per_day,
                             total_working_time,
                             query.worked_time, remaining_working_time, salary_stats)
