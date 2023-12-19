import datetime
import json
import logging

from business import Business


def run(business: Business):
    logging.info(business.__dict__)
    for _ in range(1000):
        business.work()
    filename = f'{datetime.datetime.now()}.json'.replace(' ', '_')
    with open(f'data/{filename}', 'w') as handler:
        json.dump(business.statistics, handler)


def test_best():
    logging.debug('### Best')
    b = Business(money=0, competition=0, renown=100)
    b.working_standards = 100
    b.manager_proficiency = [100]
    b.employee_proficiency = [100]
    b.user_product_quality = 80
    b.resources_quality = 100
    b.resources_quantity = 100
    b.tax = 0
    run(b)


def test_worst():
    logging.debug('### Worst')
    b = Business(money=0, competition=100, renown=0)
    b.working_standards = 5
    b.manager_proficiency = [1]
    b.employee_proficiency = [1]
    b.user_product_quality = 80
    b.resources_quality = 50
    b.resources_quantity = 50
    b.tax = 0
    run(b)


def test_one():
    logging.debug('### One')
    b = Business(money=0, competition=30, renown=0)
    b.working_standards = 10
    b.manager_proficiency = [50]
    b.employee_proficiency = [15, 10, 10, 10, 10]
    b.user_product_quality = 80
    b.resources_quality = 100
    b.resources_quantity = 100
    b.tax = 0
    run(b)


def test():
    working_standards = [i * 25 for i in range(1, 5)]  # 25 - 100
    employees = [[i * 25] for i in range(1, 5)]  # 25 - 100
    # employees = [[i*20]*4 for i in range(6)]
    user_product_quality = [30, 50, 70]
    resources = [i * 25 for i in range(1, 5)]  # 25 - 100
    for ws in working_standards:
        for m in employees:
            for e in employees:
                for upq in user_product_quality:
                    for res_qual in resources:
                        for res_quan in resources:
                            b = Business(money=0, competition=0, renown=0)
                            b.working_standards = ws
                            b.manager_proficiency = m
                            b.employee_proficiency = e
                            b.user_product_quality = upq
                            b.resources_quality = res_qual
                            b.resources_quantity = res_quan
                            b.tax = 15
                            run(b)
    print('Done')


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # test()
    test_best()
    test_worst()
    test_one()
