from datetime import date, timedelta
from typing import Collection

from model.query import Query
from utils import td_str


class SalaryStats:
    def __init__(self, hourly_salary, projected_salary, earned_salary):
        self.hourly_salary = hourly_salary
        self.projected_salary = projected_salary
        self.earned_salary = earned_salary

    def __str__(self):
        result = "With hourly salary of %s your projected salary for this period is %s." % (
            self.hourly_salary, self.projected_salary)
        if self.earned_salary is not None:
            result += " However with the total worked time you earned %s" % self.earned_salary

        return result


class ContractStats:
    def __init__(self, contract, from_date: date, to_date: date, working_days: int, workload_per_week: timedelta,
                 workload_per_day: timedelta,
                 total_working_time: timedelta,
                 worked_time: timedelta, remaining_working_time: timedelta, salary_stats: SalaryStats):
        self.contract = contract
        self.from_date = from_date
        self.to_date = to_date
        self.working_days = working_days
        self.workload_per_day = workload_per_day
        self.total_working_time = total_working_time
        self.worked_time = worked_time
        self.remaining_working_time = remaining_working_time
        self.salary_stats = salary_stats
        self.workload_per_week = workload_per_week

    def __str__(self):
        result = "Period from %s to %s with %s hours weekly workload.\n\n" \
                 "- For %d working days and %s daily workload you have to work %s hours in total." % (
                     self.from_date, self.to_date, td_str(self.workload_per_week),
                     self.working_days, td_str(self.workload_per_day), td_str(self.total_working_time))
        if self.worked_time is not None:
            result += "\n- You worked %s hours during this period." % td_str(self.worked_time)

            if self.remaining_working_time.total_seconds() >= 0:
                result += " Remaining working time: %s hours." % td_str(self.remaining_working_time)
            else:
                result += " You have: %s hours surplus." % td_str(self.worked_time - self.total_working_time)

        if self.salary_stats is not None:
            result += "\n- %s" % self.salary_stats

        return result


class ProfileStats:
    def __init__(self, profile, contract_stats: Collection[ContractStats], query: Query):
        self.profile = profile
        self.contract_stats = contract_stats
        self.query = query

    def __str__(self):
        result = "===================================================\n\n" \
                 "Stats for the period from %s to %s.\n" \
                 "%d days with %d work days per week resulting in %d working days.\n\n" \
                 "===================================================\n" % (
                     self.query.from_date, self.query.to_date, self.query.days_passed(),
                     self.query.work_days_per_week(), self.query.working_days_passed())
        contract_stats = []
        for index, contract_stat in enumerate(self.contract_stats):
            contract_stats.append("#%d\n%s" % (index + 1, str(contract_stat)))

        return result + "\n-------------------------------------------------\n".join(contract_stats)
