from currency_converter import CurrencyConverter
import datetime as dt

from model.query import Query
from model.stats import SalaryStats


class Salary:
    def __init__(self, amount: float, currency: str = 'EUR'):
        self.amount = amount
        self.currency = currency
        self.converter = CurrencyConverter()

    def convert(self, c: str):
        a = self.converter.convert(self.amount, self.currency, c)
        return Salary(a, c)

    def mul(self, multiplier: float):
        return Salary(self.amount * multiplier, self.currency)

    def __str__(self):
        return "%.2f %s" % (self.amount, self.currency)

    def stats(self, query: Query, total_working_hours: float):
        projected_salary = self.mul(total_working_hours)
        if query.worked_time is not None:
            earned_salary = self.mul(query.worked_time / dt.timedelta(hours=1))

        return SalaryStats(self, projected_salary, earned_salary)
