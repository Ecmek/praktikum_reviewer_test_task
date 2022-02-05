import datetime as dt


class Record:
    """
    В данном случае для аргумента date, лучше использовать None
    https://pythonworld.ru/tipy-dannyx-v-python/none.html
    Неплохо было бы еще добавить аннотации типов.
    """
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        """
        Здесь лучше проверять, передан ли аргмент даты 'if date'
        то преобразовать строку в формат datetime, иначе подставить
        текущую дату.

        Следует немного подправить переносы строк
        https://pythonworld.ru/osnovy/pep-8-rukovodstvo-po-napisaniyu-koda-na-python.html#section-5
        не использовав при этом обратный слэш
        """
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment

        """
        Было бы неплохо описать магический метод __str__ для вывода данных
        https://russianblogs.com/article/42011550723/
        """


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        """
        Можно воспользоваться функцией sum.
        Она принимает последовательность значений и выводит их сумму.
        Так же было бы неплохо здесь с sum использовать конструкцию
        list comprehension.
        https://dvmn.org/encyclopedia/qna/5/chto-takoe-list-comprehension-zachem-ono-kakie-esche-byvajut/
        """
        today_stats = 0
        """
        Название переменной должно начинаться с маленькой буквы PEP8 N806.
        Данные записи уже записаны в формате класса Record и мы по ним
        проходимся циклом.
        Так же текущую дату лучше вынести в переменную за пределы цикла,
        чтобы не вычислять текущую дату на каждом шаге цикла.
        """
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        """Здесь дата вынесена за цикл, отлично!"""
        today = dt.datetime.now().date()
        """
        Здесь лучше выбрать немного другой подход, сразу вычислить дату
        недельной давности и проверять, что запись лежит между ними.
        Неплохо бы использовать тут sum + list comprehension.
        """
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats

    """Здесь так же можно описать метод __str__ для вывода лимита"""


class CaloriesCalculator(Calculator):
    """
    Комментарий к функции находится не на своем месте
    При обращении к func.__doc__ мы не получим данную подсказку
    Надо перенести его под функцию.
    https://blog.finxter.com/what-is-__-doc-__-in-python/
    """
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        """
        Однобуквенную переменную для лучшей читаемости, лучше назвать
        соответствующем именем, например - remainder.
        Так же данный функционал для вычисления остатка мы используем в
        CashCalculator, лучше данный функционал вынести в родительский класс
        тем самым следуя принципу DRY - Don't Repeat Yourself.
        """
        x = self.limit - self.get_today_stats()
        if x > 0:
            """
            Если в строке нет подстановки - нет нужды делать ее f строкой.
            Давай для переноса строк будем использовать скобки и уберем
            обратный слэш.
            """
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        """
        Давай подумаем нужна ли здесь ветка else?
        Если в предыдущем if есть return или raise, то elif и else не
        нужны, если предыдущее условие выполнится, то мы выйдем из данной
        функции.
        """
        else:
            """
            В данном случае нет нужды использования скобок в return, так как
            мы не переносим строки.
            """
            return('Хватит есть!')


class CashCalculator(Calculator):

    """
    Я так понимаю тут хотелось добавить аннотацию типов?
    Данный числа у нас имеют фиксированное значение и тип, в данном случае int
    и нет необходимости конвертировать их в float.
    """
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.
    """
    В данном случае в функцию лучше передавать только один дополнительный
    аргумент - currnecy.
    У нас очень много if-ов и это пока что всего 3 валюты, если их будет
    больше, то у нас будет простыня из них.
    Есть решение получше, внутри функции создать словарь и в качестве ключа
    использовать аббревиатуры валют (currency), а в качестве значений будет
    кортеж из имени валюты и курса.
    """
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        """
        Давай уберем эту лишнюю переменную и сделаем проверку валюты, если
        валюты нет в словаре, вывести об этом сообщение.
        """
        currency_type = currency
        """Об этом писал в CaloriesCalculator - get_calories_remained """
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            """
            Здесь логическая ошибка.
            В данном случае если у нас валюта будет в рублях, то остаток
            всегда будет равен 1 =)
            """
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        """
        Так же как и выше написано про использованием elif.
        Здесь будет будет достаточно if.
        И так же данное условие при не выполнении условий cash_remained > 0 и
        cash_remained < 0, можно перенести в конец и проводить проверку на
        cash_remained == 0
        """
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            """
            Давай и здесь уберем обратный слэш и перенесем строки с
            использованием скобок.
            Для вычисления абсолютного значения лучше использовать функцию abs.
            Можно использовать f строку для лучшей читаемости и лучше
            придерживаться одного стиля кода.
            Давай приведем код к одному стилю, и для округления будем
            использовать функцию round, как выше.
            """
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    """
    Написание давнного метода излишне, так как CashCalculator наследуется от
    Calculator и уже имеет его. Мы можем к нему обратиться через интерфейс
    self.get_week_stats()
    """
    def get_week_stats(self):
        super().get_week_stats()
