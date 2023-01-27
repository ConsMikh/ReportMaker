'''
Проверка правильности правил проверки записей о помидорах
'''

import pytest
from common.complainer import *
from report.etl import PomidorRulesList


def correct_pom():
    '''Возвращает корректные помидорки для тестов'''
    correct_pom = [
        "Уют: 2\n",
        "Семья и близкие: Встреча с друзьями: 4\n",
        "HardSkills: Data engineering: Fundamentals of DE: 2\n",
        "Проекты: Личная эффективность: [[Report Maker 2.0]]: Создание базовых классов: 10\n",
        "Уют: Ванная: Закрепил смеситель на раковине: ++++\n",
        "Семья и близкие: Встреча с друзьями: + ++   +++\n",
        "Помидорка: с несколькими: числами: 3 5\n",
        "Помидорка: с числом: и маркерами: 3+++ 5 +++\n"
    ]
    for ind, pom in enumerate(correct_pom):
        yield pytest.param(pom, id=str(ind))


# err_pom = ["Обычный текст без разделителя\n",
#            "Запись: без: суммы: помидоров\n",
#            "Запись: без суммы помидоров: после последнего разделителя:\n",
#            "Неправильное: Количество: Частей: В: Помидорке: 5\n",
#            "Неправильный! разделитель! частей! ++++ +\n",
#            "Помидорка: с отрицательным количеством: помидоров: -3\n",
#            "Помидорка: с очень большим: количестовом помидоров: 10000\n",
#            "Помидорка: с неправильными: маркерами: ----- -\n",
#            "Помидорка: с несколькими: числами: 3 5\n",
#            "https://github.com/selimrbd/py-obsidianmd\n",
#            "Запись: уточнение: 4: запись после числа\n",
#            "HardSkills: Data engineering: Fundamentals of DE: 2 6\n"
#            ]


@pytest.fixture(scope='module')
def complainer():
    '''Описание теста'''
    cmp = Complainer(PomidorRulesList())

    return cmp

# Корректные записи о помидорках---------------------------------------------


@pytest.mark.parametrize("pom", correct_pom())
def test_correct_pom(complainer, pom):
    '''Тестирование проверки на наличие частей с корректными данными'''
    assert complainer.compliance(pom) == True

# test_check_has_parts------------------------------------------------


@pytest.mark.parametrize("pom", [
    pytest.param(
        "Обычный текст без разделителя\n", id=str("just text")),
    pytest.param(
        5, id=str("number - 5")),
])
def test_check_has_parts_err(complainer, pom):
    '''Тестирование проверки на наличие частей с неверными данными'''
    assert complainer.compliance(pom) == False

# test_check_num_parts------------------------------------------------


@pytest.mark.parametrize("pom", [
    pytest.param(
        "Неправильное: Количество: Частей: В: Помидорке: 5\n", id=str("just text")),
    pytest.param(
        5, id=str("number - 5")),
])
def test_check_num_parts_err(complainer, pom):
    '''Тестирование проверки на наличие частей с неверными данными'''
    assert complainer.compliance(pom) == False

# test_check_num_pom----------------------------------------------------


@pytest.mark.parametrize("pom", [
    pytest.param(
        "Запись: без: суммы: помидоров\n", id=str("without pom sum in last part")),
    pytest.param(
        "Запись: без суммы помидоров: после последнего разделителя:\n", id=str("without pom sum")),
    pytest.param(
        "Помидорка: с неправильными: маркерами: -+++-  - +\n", id=str("wrong markers")),
    pytest.param(
        5, id=str("number - 5")),
])
def test_check_num_pom_err(complainer, pom):
    '''Тестирование формата записи о помидорках'''
    assert complainer.compliance(pom) == False

# test_check_num_pom_2----------------------------------------------------


@pytest.mark.parametrize("pom", [
    pytest.param(
        "Помидорка: с очень большим: количестовом помидоров: 10000\n", id=str("10000")),
    pytest.param(
        "Помидорка: с отрицательным количеством: помидоров: -3\n", id=str("-3")),
    pytest.param(
        "Помидорка: с 0 количеством: помидоров: 0\n", id=str("0")),
    pytest.param(
        "Помидорка: с очень большим: количестовом помидоров: 10+++ 30 +++3\n", id=str("10+++ 30 +++3")),
    pytest.param(5, id=str("number - 5")),
])
def test_check_num_pom_2_err(complainer, pom):
    '''Тестирование формата записи о помидорках'''
    assert complainer.compliance(pom) == False

# test_raised_complainer ------------------------------------------------


@pytest.mark.parametrize("pom", [
    pytest.param(
        "Обычный текст без разделителя\n", id=str("just text")),
    pytest.param(
        "Запись: без: суммы: помидоров\n", id=str("without pom sum in last part")),
    pytest.param(
        "Помидорка: с неправильными: маркерами: -+++-  - +\n", id=str("wrong markers")),
    pytest.param(
        "Помидорка: с очень большим: количестовом помидоров: 10+++ 30 +++3\n", id=str("10+++ 30 +++3")),
    pytest.param(5, id=str("number - 5")),
])
def test_raised_complainer(pom):
    '''Проверяется режим работы Complainer с пробросом исключение во вне'''
    cmp = Complainer(PomidorRulesList(), raised=True)
    with pytest.raises(ComplainError):
        cmp.compliance(pom)
