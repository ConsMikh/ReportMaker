
import pytest
from report.etl import Extractor

path = 'tests\\testdata\\TestNotes'

target = [
    True,
    "HardSkills: Data engineering: Fundamentals of DE: 2\n",
    "Проекты: Личная эффективность: [[Report Maker 2.0]]: Создание базовых классов: 10\n",
    "Уют: Ванная: Закрепил смеситель на раковине: +\n",
    "Семья и близкие: Встреча с друзьями: 4\n",
]


@pytest.fixture()
def extractor(scope='function'):
    '''Создание экстрактора для извлечения помидорок'''
    ext = Extractor(log_level="CRITICAL")
    return ext


def test_correct_note(extractor):
    '''Заметка с корректными помидорками без других разделов - correct_note.md'''
    file = 'correct_note.md'
    test_block = extractor.parseFile(path, file)
    test_target = target

    assert test_block == test_target


def test_correct_full_note(extractor):
    '''Заметка с корректными помидорками с другими разделами - correct_full_note.md'''
    file = 'correct_full_note.md'
    test_block = extractor.parseFile(path, file)
    test_target = target

    assert test_block == test_target


def test_correct_empty_note(extractor):
    '''Заметка без помидорок - correct_empty_note.md'''
    file = 'correct_empty_note.md'
    test_block = extractor.parseFile(path, file)
    test_target = [True, '0']

    assert test_block == test_target


def test_err_empty_note(extractor):
    '''Пустая заметка - err_empty_note.md'''
    file = 'err_empty_note.md'
    test_block = extractor.parseFile(path, file)
    test_target = [True, '0']

    assert test_block == test_target


def test_err_empty_pom_part(extractor):
    '''Заметка с 1 пустым разделом про помидорки - err_empty_pom_part.md'''
    file = 'err_empty_pom_part.md'
    test_block = extractor.parseFile(path, file)
    test_target = [True, '0']

    assert test_block == test_target


def test_err_empty_pom_part_2(extractor):
    '''Заметка с несколькими пустыми разделами про помидорки - err_empty_pom_part_2.md'''
    file = 'err_empty_pom_part_2.md'
    test_block = extractor.parseFile(path, file)
    test_target = [True, '0']

    assert test_block == test_target


def test_err_combo_pom_part(extractor):
    '''Заметка с одним нормальным и одним пустым разделом - err_combo_pom_part.md'''
    file = 'err_combo_pom_part.md'
    test_block = extractor.parseFile(path, file)
    test_target = target

    assert test_block == test_target


def test_correct_pom_part_add_part(extractor):
    '''Заметка, в которой есть раздел про помидорки, после которого идет другой раздел - correct_pom_part_add_part.md'''
    file = 'correct_pom_part_add_part.md'
    test_block = extractor.parseFile(path, file)
    test_target = target

    assert test_block == test_target


def test_err_pom_part_add_part(extractor):
    '''Заметка, в которой есть корректные помидорки, но после записи про помидорки начинаются другие без перехода - err_pom_part_add_part.md'''
    file = 'err_pom_part_add_part.md'
    test_block = extractor.parseFile(path, file)
    add_part = [
        "Плагин для доступа к записям Obsidian\n",
        "https://github.com/selimrbd/py-obsidianmd\n",
        "[[Плагины для Obsidian]]\n"
    ]

    test_target = target + add_part

    assert test_block == test_target


def test_err_pom_part_no_pom(extractor):
    '''Заметка, в которой в разделе с помидорками вообще не помидорки - err_pom_part_no_pom.md'''
    file = 'err_pom_part_no_pom.md'
    test_block = extractor.parseFile(path, file)
    test_target = [
        True,
        "Плагин для доступа к записям Obsidian\n",
        "https://github.com/selimrbd/py-obsidianmd\n",
        "[[Плагины для Obsidian]]\n"
    ]

    assert test_block == test_target


def test_err_full_note_2(extractor):
    '''Заметка, которой 2 раздела с корректными помидорками - err_full_note_2.md'''
    file = 'err_full_note_2.md'
    test_block = extractor.parseFile(path, file)
    test_target = target + target[1:]

    assert test_block == test_target
