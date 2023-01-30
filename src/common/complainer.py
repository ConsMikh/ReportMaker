'''
Содержит классы для проверки объектов на соответствие набору правил
'''
import logging


class Complainer():
    '''
    Проводит проверку объектов на соответствие набору правил
    Набор правил задается объектов класса RulesList

    Метода complaince последовательно применяет все проверки к объекту.
    Если они пройдены, то возвращает True

    logger - если установлен в True, то описание ошибок про выполнении правил
    будет выводится сообщения в консоль

    raised - если установлен в True, то Complainer будет пробрасывать ошибки 
    при выполнении правил выше
    '''

    def __init__(self, rules_list=None, logger=False, raised=False) -> None:
        if isinstance(rules_list, RulesList):
            self.rules_list = rules_list
        if logger:
            self.log = self._get_logger()
        self.raised = raised

    def _log(self, mes):
        '''Вывод лога'''
        if hasattr(self, 'log'):
            self.log.debug(mes)
        if self.raised:
            raise ComplainError(mes)

    def _get_logger(self):
        '''Создание логера '''
        formatter = logging.Formatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setLevel("DEBUG")
        console_handler.setFormatter(formatter)

        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)

        return logger

    def set_rules_list(self, rules_list):
        '''Установить список правил в явном виде'''
        if isinstance(rules_list, RulesList):
            self.rules_list = rules_list
        else:
            self._log(
                f"Неверный набор правил. Не подкласс RulesList")

    def compliance(self, val):
        '''
        Проверка объекта на соответствие правилам. последовательно применяет все проверки к объекту.
        Если они пройдены, то возвращает True
        '''
        if self.rules_list:
            for rule in self.rules_list:
                try:
                    rule(val)
                except ComplainError as e:
                    self._log(e)
                    return False
        else:
            self._log(f"Отсутствует набор правил")
            return False
        return True


class RulesList():
    '''
    Родительский класс для всех списков правил.
    Правила реализуются как функции, название которых начинается с check_
    Объект класса является итератором. На каждой итерации применяется очередное правило
    Функции, которые начинаются не с check_ не считаются проверками и при итерировании не возвращаются

    Каждая функция проверки в случае провала должна вызывать исключение ComplainError
    Функции проверки не должны зависеть друг от друга.

    Если последовательность важна, то она вручную формируется в __init__ при создании класса-потомка.
    Для этого надо в self.rules сохранить список, в котором будут храниться имена функций в той последовательности,
    в которой их надо вызывать

    Функции проверки будут выполняться в алфавитном порядке. Так что можно закодировать последовательность в имена
    функций: check_01_smth, check_02_smthelse
    '''

    def __init__(self) -> None:
        self.rules = [meth for meth in dir(self) if "check_" in meth]

    def __iter__(self):
        self.ind = 0
        return self

    def __next__(self):
        if self.ind < len(self.rules):
            func = getattr(self, self.rules[self.ind])
            self.ind += 1
            return func
        raise StopIteration


class RulesList2():
    '''
    Родительский класс для всех списков правил.
    Правила реализуются как функции, декорированные @check
    Объект класса является итератором. На каждой итерации применяется очередное правило
    Функции, которые начинаются не с check_ не считаются проверками и при итерировании не возвращаются

    Каждая функция проверки в случае провала должна вызывать исключение ComplainError
    Функции проверки не должны зависеть друг от друга.

    '''

    r_list = []

    def __init__(self) -> None:
        # self.rules = [meth for meth in dir(self) if "check_" in meth]
        pass

    def __iter__(self):
        self.ind = 0
        return self

    def __next__(self):
        if self.ind < len(RulesList2.r_list):
            func = RulesList2.r_list[self.ind]
            self.ind += 1
            return func
        raise StopIteration

    def check(func):
        RulesList2.r_list.append(func)
        return (func)


class ComplainError(Exception):
    pass
