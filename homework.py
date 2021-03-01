import datetime as dt

date_now = dt.datetime.now().date()


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = date_now
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        return sum([record.amount for record in self.records
                    if record.date == date_now])

    def get_week_stats(self):
        date_7 = date_now - dt.timedelta(days=7)
        return sum([record.amount for record in self.records
                    if date_7 <= record.date <= date_now])

    def get_today_remained(self):
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_remained = self.limit - self.get_today_stats()
        if calories_remained <= 0:
            return('Хватит есть!')
        else:
            return('Сегодня можно съесть что-нибудь ещё, '
                   'но с общей калорийностью не более '
                   f'{calories_remained} кКал')


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def get_today_cash_remained(self, currency):
        count = self.limit - self.get_today_stats()
        if currency == 'rub':
            money = f'{abs(count)} руб'
        elif currency == 'usd':
            money = f'{abs(round(count/self.USD_RATE, 2))} USD'
        elif currency == 'eur':
            money = f'{abs(round(count/self.EURO_RATE, 2))} Euro'
        if count > 0:
            return f'На сегодня осталось {money}'
        elif count < 0:
            return f'Денег нет, держись: твой долг - {money}'
        else:
            return 'Денег нет, держись'
