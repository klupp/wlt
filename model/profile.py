from typing import Collection

from model.contract import Contract
from model.query import Query
from model.stats import ProfileStats


class Profile:
    def __init__(self, name: str, contracts: Collection[Contract]):
        self.name = name
        self.contracts = contracts

    def stats(self, query: Query):
        contract_stats = list(map((lambda contract: contract.stats(query)), self.contracts))

        return ProfileStats(self, contract_stats, query)

    def __str__(self):
        return "This %s's profile" % self.name
