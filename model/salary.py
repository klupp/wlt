from currency_converter import CurrencyConverter

from model.query import Query
from model.stats import SalaryStats


class Salary:
    def __init__(self, amount: float, currency: str = 'EUR'):
        self.amount = amount
        self.currency = currency
        self.converter = CurrencyConverter()

    def convert(self, c: str):
        if self.currency == c:
            return self
        a = self.converter.convert(self.amount, self.currency, c)
        return Salary(a, c)

    def mul(self, multiplier: float):
        return Salary(self.amount * multiplier, self.currency)

    def __str__(self):
        return "%.2f %s" % (self.amount, self.currency)

    def stats(self, query: Query, total_working_hours: float):
        projected_salary = self.mul(total_working_hours)

        return SalaryStats(self, projected_salary)

    def __add__(self, other):
        o = other.convert(self.currency)
        return Salary(self.amount + o.amount, self.currency)

    def __sub__(self, other):
        o = other.convert(self.currency)
        return Salary(self.amount - o.amount, self.currency)
