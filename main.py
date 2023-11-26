import datetime
import hashlib
import json
import logging
import math
import random


class Business:
    def __init__(self, money: int, competition: int, renown: int):
        self.statistics = {'competition': [], 'employee_proficiency': [], 'manager_proficiency': [],
                           'products_quality': [], 'products_quantity': [], 'resources_quality': [],
                           'resources_quantity': [], 'tax': [], 'user_product_quality': [],
                           'working_standards': [], 'renown': [], 'expenses': [], 'revenue': [], 'money': []}

        self._competition = competition
        self._employee_proficiency = None
        self._manager_proficiency = None
        self._products_quality = None
        self._products_quantity = None
        self._resources_quality = None
        self._resources_quantity = None
        self._tax = None
        self._user_product_quality = None
        self._working_standards = None

        self.money = money
        self.renown = renown

    @property
    def dict(self):
        return {key: item for key, item in self.__dict__.items() if key != "statistics"}

    @property
    def competition(self):
        return self._competition

    @competition.setter
    def competition(self, competition):
        if competition < 0:
            competition = 0
        self._competition = competition

    @property
    def employee_proficiency(self):
        return self._employee_proficiency

    @employee_proficiency.setter
    def employee_proficiency(self, employees: [int]):
        for e in employees:
            assert 1 <= e <= 5
        self.employees = employees
        self._employee_proficiency = sum(x ** 2 for x in employees)

    @property
    def manager_proficiency(self):
        return self._manager_proficiency

    @manager_proficiency.setter
    def manager_proficiency(self, managers: [int]):
        for m in managers:
            assert 1 <= m <= 5
        self.managers = managers
        self._manager_proficiency = sum([x ** 2 for x in managers])

    @property
    def resources_quality(self):
        return self._resources_quality

    @resources_quality.setter
    def resources_quality(self, quality: int):
        assert 0 < quality <= 100
        self._resources_quality = quality

    @property
    def resources_quantity(self):
        return self._resources_quality

    @resources_quantity.setter
    def resources_quantity(self, quantity: int):
        assert 0 < quantity <= 100
        self._resources_quantity = quantity

    @property
    def tax(self):
        return self._tax

    @tax.setter
    def tax(self, tax: int):
        assert 0 <= tax < 100
        self._tax = tax

    @property
    def user_product_quality(self):
        return self._user_product_quality

    @user_product_quality.setter
    def user_product_quality(self, user_product_quality: int):
        assert 0 < user_product_quality < 100
        self._user_product_quality = user_product_quality

    @property
    def working_standards(self):
        return self._working_standards

    @working_standards.setter
    def working_standards(self, working_standards):
        assert 1 <= working_standards <= 5
        self._working_standards = working_standards

    @property
    def products_quality(self) -> float:
        if self._products_quality is not None:
            return self._products_quality

        quality = random.uniform(0.5, 1) ** 2 * self.user_product_quality
        quality *= self.working_standards ** 1.5 * self.employee_proficiency
        quality /= self.resources_quantity
        self._products_quality = int(max(quality, 1))

        self.statistics['products_quality'].append(self._products_quality)
        logging.debug(f'Product Quality: {self._products_quality}')
        return self._products_quality

    @property
    def products_quantity(self) -> int:
        if self._products_quantity is not None:
            return self._products_quantity

        quantity = random.uniform(0.5, 1) ** 2 * (100 - self.user_product_quality)
        quantity *= self.working_standards ** 1.5 * self.employee_proficiency
        quantity *= self.products_quality / 100
        self._products_quantity = int(max(quantity, 1))

        self.statistics['products_quantity'].append(self._products_quantity)
        logging.debug(f'Product Quantity: {self._products_quantity}')
        return self._products_quantity

    @property
    def expenses(self) -> int:
        wages = sum(self.managers)
        wages += sum(self.employees)
        wages *= self.working_standards ** 1.7
        running_cost = self.working_standards ** 4 * random.randint(-(self.working_standards ** 3),
                                                                    self.working_standards ** 4)
        expenses = wages + running_cost
        self.statistics['expenses'].append(expenses)
        logging.debug(f'Expenses: {expenses} = {wages} (wages) + {running_cost} (running cost)')
        return expenses

    @property
    def revenue(self) -> int:
        turnover = math.log(self.products_quality**3) * self.products_quantity * self.manager_proficiency
        tax = self.tax / 100 * turnover
        revenue = turnover - tax - self.expenses
        self.statistics['revenue'].append(revenue)
        logging.debug(f'Revenue: {revenue}, Turnover: {turnover}, Tax: {tax}')
        return revenue

    def update_renown(self):
        delta = (self.products_quality * self.products_quantity) / (10 * self.renown + 1)
        delta += random.randint(-10, 10)
        logging.debug(f'Renown: {self.renown + delta} = {self.renown} (original) + {delta}')
        self.renown += delta
        self.statistics['renown'].append(self.renown)

    def update_competition(self, revenue):
        delta = ((revenue * self.renown) / 100) / (self.competition + 1)
        delta += random.randint(-20, 20)
        logging.debug(f'Competition: {self.competition + delta} = {self.competition} (original) + {delta}')
        self.competition += delta
        self.statistics['competition'].append(self.competition)

    def work(self):
        self._products_quality = None
        self._products_quantity = None

        self.statistics['tax'].append(self.tax)
        self.statistics['user_product_quality'].append(self.user_product_quality)
        self.statistics['working_standards'].append(self.working_standards)
        self.statistics['employee_proficiency'].append(self.employee_proficiency)
        self.statistics['manager_proficiency'].append(self.manager_proficiency)
        self.statistics['resources_quality'].append(self.resources_quality)
        self.statistics['resources_quantity'].append(self.resources_quantity)

        logging.debug(f'Start money: {self.money}')
        revenue = self.revenue
        self.money += revenue
        self.statistics['money'].append(self.money)
        logging.debug(f'Money after earnings: {self.money}')

        self.update_renown()
        self.update_competition(revenue)


def run(business: Business):
    logging.info(business.__dict__)
    for _ in range(1000):
        business.work()
    filename = f'{datetime.datetime.now()}.json'.replace(' ', '_')
    with open(f'data/{filename}', 'w') as handler:
        json.dump(business.statistics, handler)


def test_single():
    b = Business(money=0, competition=10, renown=0)
    b.working_standards = 2
    b.manager_proficiency = [1]
    b.employee_proficiency = [1, 1, 1, 1, 1]
    b.user_product_quality = 80
    b.resources_quality = 50
    b.resources_quantity = 100
    b.tax = 20
    run(b)


def test():
    working_standards = [1, 2, 3, 4, 5]
    employees = [[1], [1, 1, 1, 1, 1], [2], [2, 2, 2, 2], [3], [3, 3, 3, 3], [4], [4, 4, 4, 4], [5], [5, 5, 5, 5]]
    user_product_quality = [30, 50, 70]
    resources = [i*20-10 for i in range(1, 6)] # 10 - 90
    renown = [i * 200 for i in range(-3, 4)]  # -600 - 600
    competition = [i * 100 for i in range(-2, 3)]  # -200 - 200
    tax = [i * 10 for i in range(6)]  # 0 - 50
    for ws in working_standards:
        for m in employees:
            for e in employees:
                for upq in user_product_quality:
                    for res_qual in resources:
                        for res_quan in resources:
                            for ren in renown:
                                for c in competition:
                                    for t in tax:
                                        b = Business(money=0, competition=c, renown=ren)
                                        b.working_standards = ws
                                        b.manager_proficiency = m
                                        b.employee_proficiency = e
                                        b.user_product_quality = upq
                                        b.resources_quality = res_qual
                                        b.resources_quantity = res_quan
                                        b.tax = t
                                        run(b)
    print('Done')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # test()
    test_single()
