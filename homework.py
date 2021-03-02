import datetime as dt


class Record:
    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()


class Calculator:
    WEEK = dt.datetime.now().date() - dt.timedelta(days=7)

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        return sum(record.amount for record in self.records
                   if record.date == dt.datetime.now().date())

    def get_week_stats(self):
        return sum([record.amount for record in self.records
                    if self.WEEK < record.date <= dt.datetime.now().date()])


class CaloriesCalculator(Calculator):
    ANSWER_NEGATIVE = 'Хватит есть!'
    ANSWER_POSITIVE = ('Сегодня можно съесть что-нибудь ещё, '
                       'но с общей калорийностью не более '
                       '{key} кКал')

    def get_calories_remained(self):
        calories_remained = self.limit - self.get_today_stats()
        if calories_remained <= 0:
            return self.ANSWER_NEGATIVE
        return self.ANSWER_POSITIVE.format(key=calories_remained)


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    BALANCE_POSITIVE = 'На сегодня осталось {key}'
    BALANCE_NEGATIVE = 'Денег нет, держись: твой долг - {key}'
    BALANCE_ZERO = 'Денег нет, держись'
    currency_db = {
                    'rub': [1, 'руб'],
                    'usd': [USD_RATE, 'USD'],
                    'eur': [EURO_RATE, 'Euro']
                  }

    def get_today_cash_remained(self, currency):
        today_remained = self.limit - self.get_today_stats()
        cash = round(today_remained/self.currency_db[currency][0], 2)
        if today_remained > 0:
            money = f'{cash} {self.currency_db[currency][1]}'
            return self.BALANCE_POSITIVE.format(key=money)
        elif today_remained < 0:
            money = f'{abs(cash)} {self.currency_db[currency][1]}'
            return self.BALANCE_NEGATIVE.format(key=money)
        else:
            return self.BALANCE_ZERO
