from __future__ import annotations

from typing import NoReturn

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from binance_bot import BinanceBotThread
from data_manager import DataManager
from gui_forms import Button, Console, ListBox
from gui_tabs import BotConfiguratorTab, PairEditorTab, TabBox
from logger import Logger
from misc import TimeSyncerThread


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('BBWI v0.1')
        self.resize(1280, 720)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Основной вертикальный макет для блоков
        self.main_vbl = QVBoxLayout()
        self.central_widget.setLayout(self.main_vbl)

        self.__init_UI__()

        self.logger = Logger(self.console)
        self.data_manager = DataManager(self,
                                        self.pair_editor_tab,
                                        self.bot_configurator_tab)
        self.load_cfg()

        self.pair_editor_tab.set_pair_btn.clicked.connect(self.set_pair)
        self.pair_editor_tab.remove_pair_btn.clicked.connect(self.remove_pair)
        self.pair_editor_tab.pairs_lb.currentTextChanged.connect(
            self.data_manager.load_pair)
        self.pair_editor_tab.pairs_lb.setCurrentRow(0)

        self.bot_thread: BinanceBotThread = None
        self.time_syncer_thread: TimeSyncerThread = None

    def __init_UI__console_hbl__(self):
        # Консоль для отладки всех событий бота
        self.console = Console(self.central_widget)
        self.console_hbl.addWidget(self.console)
        pass

    def __init_UI__tab_box_hbl__(self):
        # Таб-виджет, на котором будут находится все вкладки
        self.tab_box = TabBox(self.central_widget)
        self.tab_box_hbl.addWidget(self.tab_box)

        self.pair_editor_tab = PairEditorTab(self.tab_box, 0)
        self.bot_configurator_tab = BotConfiguratorTab(self.tab_box, 1)

        self.tab_box.addTab(self.bot_configurator_tab,
                            self.bot_configurator_tab.title)
        self.tab_box.addTab(self.pair_editor_tab,
                            self.pair_editor_tab.title)
        pass

    def __init_UI__quick_btn_hbl__(self):
        # Кнопка очистки консоли
        self.clear_console_btn = Button(self.central_widget,
                                        'Очистить консоль')
        self.clear_console_btn.clicked.connect(self.clear_console)

        # Кнопка запуска бота
        self.start_bot_btn = Button(self.central_widget, 'Запустить бота')
        self.start_bot_btn.clicked.connect(self.start_bot)

        # Кнопка остановки бота
        self.stop_bot_btn = Button(self.central_widget, 'Остановить бота')
        self.stop_bot_btn.clicked.connect(self.stop_bot)

        # Кнопка сохранения настроек
        self.save_options_btn = Button(self.central_widget, 'Сохранить')
        self.save_options_btn.clicked.connect(self.save_cfg)

        self.quick_btn_hbl.addWidget(self.save_options_btn)
        self.quick_btn_hbl.addWidget(self.start_bot_btn)
        self.quick_btn_hbl.addWidget(self.stop_bot_btn)
        self.quick_btn_hbl.addWidget(self.clear_console_btn)
        pass

    def __init_UI__(self):
        # 1. Гор-макет для блока с консолью
        self.console_hbl = QHBoxLayout()
        self.main_vbl.addLayout(self.console_hbl)

        # 2. Гор-макет для блока с вкладками. Идёт вторым
        self.tab_box_hbl = QHBoxLayout()
        self.main_vbl.addLayout(self.tab_box_hbl)

        # 3. Гор-макет для блока с кнопками для быстрых действий
        self.quick_btn_hbl = QHBoxLayout()
        self.quick_btn_hbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_vbl.addLayout(self.quick_btn_hbl)

        self.__init_UI__console_hbl__()
        self.__init_UI__tab_box_hbl__()
        self.__init_UI__quick_btn_hbl__()
        pass

    def clear_console(self):
        """ Очищает консоль
            @logger.clear """
        self.logger.clear_console()

    def to_minimum_size(self) -> NoReturn:
        """ Ресайзит окно в минимальный размер """
        self.resize(self.minimumSize())

    def to_center(self) -> NoReturn:
        """ Центрирует окно """
        screen_size = _app.primaryScreen().size()
        new_size = screen_size / 2 - self.size() / 2

        self.move(new_size.width(), new_size.height())

    def save_cfg(self):
        self.data_manager.save()
        self.logger.success('Конфиг успешно сохранён')

    def load_cfg(self):
        cfg = self.data_manager.load()
        for pair_name_id in cfg.pairs:
            self.add_pair_in_pairs_lb(pair_name_id)
        self.logger.success('Конфиг успешно загружен')

    def set_pair(self):
        pair = self.data_manager.set_pair(
            self.pair_editor_tab.pair_name_id_le.get_value())
        if pair.pair_name_id:
            self.add_pair_in_pairs_lb(pair.pair_name_id)

    def add_pair_in_pairs_lb(self, pair_name_id: str):
        pairs_lb = self.pair_editor_tab.pairs_lb
        if not pairs_lb.findItems(
                pair_name_id, Qt.MatchFlag.MatchFixedString):
            pairs_lb.addItem(pair_name_id)
            self.logger.success('Пара успешно добавлена')
        else:
            self.logger.warning('Пара с таким именем уже есть в списке')
            self.logger.warning('Ее данные были изменены в соотвествие '
                                'с заданной парой')

    def remove_pair(self):
        try:
            self.data_manager.remove_pair(
                self.pair_editor_tab.pairs_lb.currentItem().text())
            self.pair_editor_tab.pairs_lb.takeItem(
                self.pair_editor_tab.pairs_lb.currentRow())
            self.logger.success('Пара успешно удалена')
        except AttributeError:
            self.logger.warning('Выберите пару для удаления!')

    def start_bot(self):
        try:
            self.bot_thread = BinanceBotThread(None, self.logger,
                                               self.data_manager.get_config())
            self.time_syncer_thread = TimeSyncerThread(
                None,
                self.bot_thread.get_binance_bot(),
                self.logger,
                self.data_manager.get_config()
            )

            self.bot_thread.start()
            self.time_syncer_thread.start()

            self.logger.success('Бот успешно запущен')
        except Exception as e:
            self.logger.error('Не удалось запустить бота!')
            self.logger.error(e)

    def stop_bot(self):
        try:
            if self.bot_thread:
                self.bot_thread.terminate()
                self.bot_thread = None

            if self.time_syncer_thread:
                self.time_syncer_thread.terminate()
                self.time_syncer_thread = None

            self.logger.success('Бот успешно остановлен')
        except Exception as e:
            self.logger.error('Бот остановлен неудачно!')
            self.logger.error(e)


if __name__ == '__main__':
    try:
        import qdarktheme
        _app = QApplication([])
        _app.setFont(QFont('Lucida Sans Unicode', 12))
        _app.setStyleSheet(qdarktheme.load_stylesheet() + """
            QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox, QPushButton {
                min-height: 30px;
            }
        """)
        _window = Window()
        _window.to_minimum_size()
        _window.show()
        _window.to_center()

        _window.logger.info('Тест')
        _window.logger.debug('Тест')
        _window.logger.warning('Тест')
        _window.logger.error('Тест')
        _window.logger.success('Тест')

        _app.exec()
    except Exception as e:
        import traceback
        input(traceback.format_exc())
