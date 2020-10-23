import argparse
import datetime as dt
import re

import numpy as np
from iso4217 import Currency

from model.contract import Contract
from model.profile import Profile
from model.query import Query
from model.salary import Salary


def date_type(dtt):
    print("#### ", dtt)
    value = dt.datetime.strptime(dtt, '%Y-%m-%d')
    return value.date()


regex = re.compile(r'((?P<hours>\d+?):)?((?P<minutes>\d+?):)?((?P<seconds>\d+?))?')


def time_type(t):
    parts = regex.match(t)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for (name, param) in parts.items():
        if param:
            time_params[name] = int(param)
    return dt.timedelta(**time_params)


parser = argparse.ArgumentParser(description='WLT (Workload TIme) helps you monitor your workload status.')
parser.add_argument('-wh', '--week_hours', type=int, help='The weekly workload in hours.', default=12)
parser.add_argument('-hs', '--hourly_salary', type=float, help='Hourly Salary.')
parser.add_argument('-c', '--currency', help='The currency used for the salary. E.g. \'MKD\', \'EUR\', \'DKK\', etc.',
                    default='EUR')
parser.add_argument('-sd', '--start_date', type=date_type, help='The start date of the calculation',
                    default=dt.datetime.today().replace(day=1).date())
parser.add_argument('-ed', '--end_date', type=date_type, help='The end date of the calculation',
                    default=(dt.datetime.today() + dt.timedelta(days=1)).date())
parser.add_argument('-wt', '--worked_time', type=time_type, help='The end date of the calculation')
parser.add_argument('-ad', '--all_days', action='store_true', help='All days compared only to business days')

sd = dt.datetime.today().replace(day=1).date()
ed = (dt.datetime.today() + dt.timedelta(days=1)).date()


def calculate_hours(worked_time, start, end, week_hours, all_days, hourly_salary_amount, currency):
    hourly_salary: Salary = None
    if hourly_salary_amount is not None:
        hourly_salary = Salary(hourly_salary_amount, currency)

    contract = Contract("YYYYY", week_hours, start, end, hourly_salary=hourly_salary)
    profile = Profile("XXXXXX", [contract])

    if all_days:
        week_mask = np.ones(1, 7)
    else:
        week_mask = np.array([1, 1, 1, 1, 1, 0, 0])

    query = Query(worked_time, start, end, week_mask)

    print(profile.stats(query))


def main(args):
    calculate_hours(args.worked_time, args.start_date, args.end_date, args.week_hours, args.all_days,
                    args.hourly_salary, args.currency)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
