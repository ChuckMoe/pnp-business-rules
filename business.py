import logging
from random import randint

logger = logging.getLogger()


def calculate_proficiency(l: [int]) -> int:
    """Range: 0 - 100"""
    s = sum([i ** 2 for i in l])
    a = s / sum(l)
    return int(a)


def calculate_wages(employees: [int]) -> int:
    return int(sum(e ** 2.5 for e in employees))


class Business:
    def __init__(self, money: int, competition: int, renown: int):
        self.statistics = {'competition': [], 'employee_proficiency': [], 'manager_proficiency': [],
                           'products_quality': [], 'products_quantity': [], 'resources_quality': [],
                           'resources_quantity': [], 'tax': [], 'user_product_quality': [],
                           'working_standards': [], 'renown': [], 'expenses': [], 'revenue': [], 'money': []}

        self.managers = []
        self.employees = []

        self._competition = competition
        self._employee_proficiency = None
        self._manager_proficiency = None
        self._products_quality = None
        self._products_quantity = None
        self._resources_quality = None
        self._resources_quantity = 999999
        self._tax = None
        self._user_product_quality = None
        self._working_standards = None
        self._renown = renown

        self.money = money

    @property
    def dict(self):
        return {key: item for key, item in self.__dict__.items() if key != "statistics"}

    @property
    def competition(self):
        return self._competition

    @competition.setter
    def competition(self, competition):
        assert 0 <= competition <= 100
        self._competition = competition

    @property
    def employee_proficiency(self):
        return self._employee_proficiency

    @employee_proficiency.setter
    def employee_proficiency(self, employees: [int]):
        for e in employees:
            assert 0 <= e <= 100
        self.employees = employees
        self._employee_proficiency = calculate_proficiency(employees)

    @property
    def manager_proficiency(self):
        return self._manager_proficiency

    @manager_proficiency.setter
    def manager_proficiency(self, managers: [int]):
        for m in managers:
            assert 0 <= m <= 100
        self.managers = managers
        self._manager_proficiency = calculate_proficiency(managers)

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
        assert 0 < quantity  # <= 100
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
        assert 0 <= working_standards <= 100
        self._working_standards = working_standards

    @property
    def products_quality(self) -> float:
        if self._products_quality is not None:
            return self._products_quality

        quality = self.employee_proficiency
        quality *= randint(50, 100) / 100
        quality *= self.working_standards / 100
        quality += randint(-10, 10)
        quality = max(1, int(quality))
        quality = min(self.resources_quality, quality)
        self._products_quality = int(quality)

        self.statistics['products_quality'].append(self._products_quality)
        logging.debug(f'Product Quality: {self._products_quality}')
        return self._products_quality

    @property
    def products_quantity(self) -> int:
        if self._products_quantity is not None:
            return self._products_quantity

        quantity = randint(50, 100) / 100
        quantity *= self.working_standards
        quantity *= len(self.employees)
        quantity += randint(-10, 10)
        quantity = max(1, int(quantity))
        quantity = min(self.resources_quantity, quantity)
        self._products_quantity = int(quantity)

        self.statistics['products_quantity'].append(self._products_quantity)
        logging.debug(f'Product Quantity: {self._products_quantity}')
        return self._products_quantity

    @property
    def expenses(self) -> int:
        wages = calculate_wages(self.managers)
        wages += calculate_wages(self.employees)
        wages *= self.working_standards ** 2 // 100
        running_cost = randint(-self.working_standards, self.working_standards) ** 2
        expenses = wages + running_cost
        self.statistics['expenses'].append(expenses)
        logging.debug(
            f'Expenses: {expenses} = {wages} (wages) + {running_cost} (running cost)')
        return expenses

    @property
    def renown(self):
        return self._renown

    @renown.setter
    def renown(self, renown: int):
        renown = max(-100, renown)
        renown = min(100, renown)
        self._renown = int(renown)

    @property
    def revenue(self) -> int:
        turnover = self.products_quality ** 2
        turnover *= self.products_quantity
        turnover *= self.manager_proficiency
        tax = max(0, (self.tax / 100) * turnover)
        revenue = turnover - tax - self.expenses
        self.statistics['revenue'].append(revenue)
        logging.debug(f'Revenue: {revenue}, Turnover: {turnover}, Tax: {tax}')
        return revenue

    def update_renown(self):
        delta = self.working_standards / 100 * self.products_quality
        delta += randint(-5, 5)
        self.renown += delta
        logging.debug(f'Renown: {self.renown} = {self.renown - delta} (original) + {delta}')
        self.statistics['renown'].append(self.renown)

    def work(self):
        self._products_quality = None
        self._products_quantity = None

        self.statistics['tax'].append(self.tax)
        self.statistics['competition'].append(self.competition)
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
