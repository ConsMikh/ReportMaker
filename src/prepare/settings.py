'''
Содержит классы для обработки файла настроек
'''
import json
import os

from common.worker import Worker
from common.complainer import *


class SettingsParser(Worker):

    DEFAULT_SETTINGS = {
        "path": {
            "daily_base": "D:\\DailyBase",
            "kbase": "D:\\KBase",
            "output_md_path": "D:\\Reports\\md",
            "output_json_path": "D:\\Reports\\json",
        },
        "analyst": {
            "norma": 14,
            "max_year": 2050,
            "min_year": 2010
        }
    }

    def __init__(self, log_level='ERROR', set_default=False) -> None:
        super().__init__(log_level)
        if set_default:
            self.settings = self._set_default_settings(self)
        else:
            self.settings = {}
        self.settings_file = 'settings.json'
        dirname, _ = os.path.split(os.path.abspath(__file__))
        self.dirname = dirname

    def _set_default_settings(self, dir=None):
        self.settings = SettingsParser.DEFAULT_SETTINGS
        self.rewrite_settings()

    def _set_setting(self, part, key, value):
        self.settings[part][key] = value

    def get_settings_namespace(self):
        '''Загрузка настроек из файла настроек
        '''
        self.log.info('Парсинг файла настроек начат')

        path = os.path.join(self.dirname, self.settings_file)
        try:
            with open(path) as f:
                self.settings = json.load(f)
        except FileNotFoundError as e:
            self.log.warning(
                'Файл настроек не обнаружен! Создан новый пустой файл настроек')
            with open(os.path.join(self.dirname, self.settings_file), "w") as f:
                f.write("")
        except Exception as e:
            self.log.warning(
                f'Получена ошибка при выполнении парсинга файла настроек: {e}')
        return self.settings

    def check_settings(self):
        for dir, path in self.settings['path'].items():
            self.log.debug(f'Проверка пути: {dir} - {path}')
            if os.path.isdir(path):
                self.log.debug(f'{dir} - {path} - существует')
                self._set_setting('path', dir, path)
            else:
                self.log.debug(
                    f'{dir} - {path} - не существует. Установлен в значение по умолчанию')
                self._set_setting(
                    'path', dir, SettingsParser.DEFAULT_SETTINGS['path'][dir])

    def change_settings(self, input):
        '''Меняет настройки'''
        self.settings = self.get_settings_namespace()

        if input.get('show', False):
            self.pretty_print(self.settings)
            return

        if input.get('set_default', False):
            self._set_default_settings()
            return

        group = input.get('group', False)

        if group not in self.settings.keys() and not input.get('del_param', False):
            self.settings[group] = {}

        if input.get('set_param', False):
            param = input.get('set_param')
            cmp = Complainer()
            if group:
                match group:
                    case 'path':
                        cmp.set_rules_list(PathSettingsRulesList())
                    case 'analyst':
                        cmp.set_rules_list(AnalystSettingsRulesList())
                    case _:
                        cmp.set_rules_list(SettingsRulesList())
            if cmp.compliance(param):
                key = input.get('set_param').split('=')[0].strip()
                value = input.get('set_param').split('=')[1].strip()
                self.settings[group][key] = value

        if input.get('del_param', False):
            key = input.get('del_param')
            if not group:
                if key in self.settings.keys():
                    del self.settings[key]
                else:
                    self.log.warning(
                        f"Группа {group} в настройках отсутствует")
            else:
                if self.settings.get(group, {}).get(key, False):
                    del self.settings[group][key]
                else:
                    self.log.warning(
                        f"Ключ {key} в группе {group} в настройках отсутствует")

        self.rewrite_settings()

    def rewrite_settings(self):
        dirname, _ = os.path.split(os.path.abspath(__file__))
        path = os.path.join(self.dirname, self.settings_file)
        try:
            with open(path, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except:
            pass

    def pretty_print(self, d, indent=0):
        for key, value in d.items():
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                self.pretty_print(value, indent+1)
            else:
                print('\t' * (indent+1) + str(value))


class SettingsRulesList(RulesList):

    def __init__(self) -> None:
        super().__init__()

    def check_has_parts(self, val):
        '''Проверяет наличие частей в параметре'''
        if isinstance(val, str):
            parts_num = val.split('=')
            if len(parts_num) < 2:
                raise ComplainError(
                    f"В записи {val} отсутствуют части, разделенные =")
            else:
                return True
        raise ComplainError(f"{val} - не строка")


class AnalystSettingsRulesList(SettingsRulesList):

    def __init__(self) -> None:
        super().__init__()

    def check_correct_param(self, val):
        '''Проверяет наличие частей в параметре'''
        correct_param = ["norma", "max_year", "min_year"]
        if isinstance(val, str):
            key = val.split('=')[0].strip()
            if key not in correct_param:
                raise ComplainError(
                    f"Параметр {key} некорректен для группы path")
            else:
                return True
        raise ComplainError(f"{val} - не строка")


class PathSettingsRulesList(SettingsRulesList):

    def __init__(self) -> None:
        super().__init__()

    def check_correct_param(self, val):
        '''Проверяет наличие частей в параметре'''
        correct_param = ["kbase", "output_md_path", "output_json_path",
                         "daily_base"]
        if isinstance(val, str):
            key = val.split('=')[0].strip()
            if key not in correct_param:
                raise ComplainError(
                    f"Параметр {key} некорректен для группы analyst")
            else:
                return True
        raise ComplainError(f"{val} - не строка")

    def check_path(self, val):
        '''Проверяет является ли параметр путем'''
        if isinstance(val, str):
            path = val.split('=')[1].strip()
            if not os.path.isdir(path):
                raise ComplainError(
                    f"Значение {path} не является путем к существующему каталогу")
            else:
                return True
        raise ComplainError(f"{val} - не строка")
