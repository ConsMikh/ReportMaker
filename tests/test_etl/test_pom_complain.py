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
        "Семья и близкие: Встреча с друзьями: + ++   +++\n"
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


@pytest.mark.parametrize("pom", correct_pom())
def test_check_01_has_parts_cor(complainer, pom):
    '''Описание теста'''
    assert complainer.compliance(pom) == True


@pytest.mark.parametrize("pom", [
    pytest.param(
        "Обычный текст без разделителя\n", id=str("just text"))
])
def test_check_01_has_parts_err(complainer, pom):
    '''Описание теста'''
    assert complainer.compliance(pom) == False
