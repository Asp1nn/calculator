import datetime as dt


class Record:
    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()


class Calculator:
    WEEK = dt.timedelta(days=7)

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        data_now = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == data_now)

    def get_week_stats(self):
        data_now = dt.date.today()
        week = data_now - self.WEEK
        return sum(record.amount for record in self.records
                   if week < record.date <= data_now)


class CaloriesCalculator(Calculator):
    NEGATIVE = 'Хватит есть!'
    POSITIVE = ('Сегодня можно съесть что-нибудь ещё, '
                'но с общей калорийностью не более '
                '{key} кКал')

    def get_calories_remained(self):
        calories_remained = self.limit - self.get_today_stats()
        if calories_remained <= 0:
            return self.NEGATIVE
        return self.POSITIVE.format(key=calories_remained)


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    BALANCE_POSITIVE = 'На сегодня осталось {balance} {currency}'
    BALANCE_NEGATIVE = 'Денег нет, держись: твой долг - {balance} {currency}'
    BALANCE_ZERO = 'Денег нет, держись'
    INVALID_CURRENCY = 'Валюта - {currency} в калькуляторе не используется'
    CURRENCY_DB = {
        'rub': [1, 'руб'],
        'usd': [USD_RATE, 'USD'],
        'eur': [EURO_RATE, 'Euro']
    }

    def get_today_cash_remained(self, currency):
        if currency not in self.CURRENCY_DB:
            raise ValueError(self.INVALID_CURRENCY.format(currency=currency))
        today_remained = self.limit - self.get_today_stats()
        if today_remained == 0:
            return self.BALANCE_ZERO
        rate, name = self.CURRENCY_DB[currency]
        cash = round(today_remained / rate, 2)
        if today_remained > 0:
            return self.BALANCE_POSITIVE.format(balance=cash, currency=name)
        return self.BALANCE_NEGATIVE.format(balance=abs(cash), currency=name)
