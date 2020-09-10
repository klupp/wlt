import numpy as np
import datetime as dt
from dateutil.parser import parse
import re
import argparse 

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
parser.add_argument('-wh', '--week_hours', type=int, help='The weekly workload in hours.', default=8)
parser.add_argument('-sd', '--start_date', type=date_type, help='The start date of the calculation', default=dt.datetime.today().replace(day=1).date())
parser.add_argument('-ed', '--end_date', type=date_type, help='The end date of the calculation', default=(dt.datetime.today() + dt.timedelta(days=1)).date())
parser.add_argument('-wt', '--worked_time', type=time_type, help='The end date of the calculation')
parser.add_argument('-ad', '--all_days', action='store_true', help='All days compared only to bussiness days')

sd = dt.datetime.today().replace(day=1).date()
ed = (dt.datetime.today() + dt.timedelta(days=1)).date()


def calculate_hours(worked_time, start, end, week_hours=8, all_days=False):

    if not all_days:
        days = np.busday_count(start, end)
        num_work_days = 5
    else:
        days = np.busday_count(start, end, weekmask='1111111')
        num_work_days = 7
    print("Working days:", days)

    total_working_hours = days * (week_hours / num_work_days)
    total_working_time = dt.timedelta(milliseconds = total_working_hours * 3600000)
    print("Working time:", str(total_working_time))


    if worked_time != None:
        remaining_working_time = total_working_time - worked_time
        if (remaining_working_time.total_seconds() >= 0):
            print("Remaining working time:", str(remaining_working_time))
        else:
            print("You have:", str(worked_time - total_working_time), "surplus.")
    
    

def main(args):
    calculate_hours(args.worked_time, args.start_date, args.end_date, args.week_hours, args.all_days)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)