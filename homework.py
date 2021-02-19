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

    def get_today_status(self):
        return sum([record.amount for record in self.records
                    if record.date == date_now])

    def get_week_status(self):
        date_7 = date_now - dt.timedelta(days=7)
        return sum([record.amount for record in self.records
                    if date_7 <= record.date <= self.date])

    def get_today_remained(self):
        return self.limit - self.get_today_status


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        if self.get_today_remained() >= self.limit:
            return('Хватит есть!')
        else:
            return('Сегодня можно съесть что-нибудь ещё, '
                   'но с общей калорийностью не более '
                   f'{self.get_today_remained()} кКал')


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def get_today_cash_remained(self, currency):
        count = 0.0
        if currency == 'rub':
            count = self.get_today_remained()
        elif currency == 'usd':
            count = self.get_today_remained()/self.USD_RATE
        elif currency == 'eur':
            count = self.get_today_remained()/self.EURO_RATE
        if count == self.limit:
            return 'Денег нет, держись'
        elif count < self.limit:
            return f'На сегодня осталось {count} {currency}'
        else:
            count = count - self.limit
            return f'Денег нет, держись: твой долг - {count} {currency}'