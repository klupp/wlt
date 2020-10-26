from datetime import date, timedelta
from typing import Collection

from model.query import Query
from utils import td_str


class SalaryStats:
    def __init__(self, hourly_salary, projected_salary):
        self.hourly_salary = hourly_salary
        self.projected_salary = projected_salary

    def __str__(self):
        result = "With hourly salary of %s your projected salary for this period is %s." % (
            self.hourly_salary, self.projected_salary)

        return result


class ContractStats:
    def __init__(self, contract, from_date: date, to_date: date, working_days: int, workload_per_week: timedelta,
                 workload_per_day: timedelta,
                 total_working_time: timedelta, salary_stats: SalaryStats):
        self.contract = contract
        self.from_date = from_date
        self.to_date = to_date
        self.working_days = working_days
        self.workload_per_day = workload_per_day
        self.total_working_time = total_working_time
        self.salary_stats = salary_stats
        self.workload_per_week = workload_per_week

    def __str__(self):
        result = "Period from %s to %s with %s hours weekly workload.\n\n" \
                 "- For %d working days and %s daily workload you have to work %s hours in total." % (
                     self.from_date, self.to_date, td_str(self.workload_per_week),
                     self.working_days, td_str(self.workload_per_day), td_str(self.total_working_time))

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
        working_days = 0
        total_working_time = timedelta(seconds=0)
        projected_salaries = []
        for index, contract_stat in enumerate(self.contract_stats):
            working_days += contract_stat.working_days
            total_working_time += contract_stat.total_working_time
            if contract_stat.salary_stats is not None:
                projected_salaries.append(contract_stat.salary_stats.projected_salary)
            contract_stats.append("#%d\n%s" % (index + 1, str(contract_stat)))

        # if self.earned_salary is not None:
        #     result += " However with the total worked time you earned %s" % self.earned_salary

        result += "\n-------------------------------------------------\n".join(contract_stats)

        result += f"\n\n===================================================\n\n- For total of {working_days} " \
                  f"working days you have to work {td_str(total_working_time)} hours in total."

        if len(projected_salaries) > 0:
            salary = projected_salaries[0]
            for sal in projected_salaries[1:]:
                salary += sal
            result += f" Your projected salary for the whole period is {salary}."

        if self.query.worked_time is not None:
            result += "\n- You worked %s hours during this period." % td_str(self.query.worked_time)
            remaining_working_time = total_working_time - self.query.worked_time
            if remaining_working_time.total_seconds() >= 0:
                result += " Remaining working time: %s hours." % td_str(remaining_working_time)
            else:
                result += " You have: %s hours surplus." % td_str(self.query.worked_time - total_working_time)

        return result
