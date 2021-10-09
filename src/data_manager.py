from __future__ import annotations

from PyQt6.QtWidgets import QMainWindow, QTextBrowser
from gui_tabs import BotConfiguratorTab, PairEditorTab
from datatypes import Config, Pair

import json
from pprint import pprint
import os

CONFIG_FILENAME = './config.json'


class DataManager:
    def __init__(self, window: QMainWindow,
                 pair_editor_tab: PairEditorTab,
                 bot_configurator_tab: BotConfiguratorTab) -> None:

        self._window = window

        self.__pair_editor_tab = pair_editor_tab
        self.__bot_configurator_tab = bot_configurator_tab
        self.__default_pair = Pair('Тестовая пара', 'ETH', 'ADA',
                                   0.02, 1, False, 1, True)
        self.__default_config = Config('default', {self.__default_pair},
                                       '', '', 200, 7, True, '1h')
        self.__config = Config('default', {}, '', '', 200, 7, True, '1h')
        pass

    def save(self):
        data = {form.name: form.get_value()
                for form in self.__bot_configurator_tab.forms}

        data['pairs'] = {}
        for name, pair in self.__config.pairs.items():
            data['pairs'][name] = {form.name: getattr(pair, form.name)
                                   for form in self.__pair_editor_tab.forms}

        with open(CONFIG_FILENAME, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # Подгружаем эти же значения для работы Бота
        self.load()

    def get_cfg_data_from_file(self):
        try:
            with open(CONFIG_FILENAME, 'r', encoding='utf-8') as f:
                cfg_data = json.load(f, parse_float=float, parse_int=int)
            return cfg_data
        except FileNotFoundError:
            self.save()
        return self.get_cfg_data_from_file()

    def load(self):
        cfg_data = self.get_cfg_data_from_file()

        data = {}

        for form in self.__bot_configurator_tab.forms:
            try:
                form.set_value(cfg_data[form.name])
                data[form.name] = cfg_data[form.name]
            except KeyError:
                default_value = getattr(self.__default_config, form.name)
                form.set_value(default_value)
                data[form.name] = default_value

        all_pair_data = {}
        for pair_name, cfg_pair_data in cfg_data['pairs'].items():
            pair_data = {}
            for form in self.__pair_editor_tab.forms:
                pair_data[form.name] = cfg_pair_data[form.name]
            all_pair_data[pair_name] = Pair(**pair_data)

        data['pairs'] = all_pair_data
        self.__config = Config(**data)
        return self.__config

    def load_pair(self, pair_name: str = 'None'):
        try:
            pair = self.__config.pairs[pair_name]

            for form in self.__pair_editor_tab.forms:
                form.set_value(getattr(pair, form.name))
        except KeyError:
            for form in self.__pair_editor_tab.forms:
                form.set_value(getattr(self.__default_pair, form.name))
        pass

    def set_pair(self, pair_name_id: str = 'Test pair'):
        pair_data = {}
        for form in self.__pair_editor_tab.forms:
            pair_data[form.name] = form.get_value()
        self.__config.pairs[pair_name_id] = Pair(**pair_data)
        return self.__config.pairs[pair_name_id]

    def remove_pair(self, pair_name_id: str = 'Test pair'):
        try:
            self.__config.pairs.pop(pair_name_id)
        except KeyError:
            pass

    def get_config(self):
        return self.__config
