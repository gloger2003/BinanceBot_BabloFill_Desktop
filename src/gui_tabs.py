from __future__ import annotations
from gui_forms import (Button, CheckBox, ComboBox,
                       FloatSpinBox, IntSpinBox, LineEdit,
                       ListBox)
from typing import Any

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class TabBox(QTabWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent=parent)

        self.setObjectName('TabBox')


class __Tab(QWidget):
    def __init__(self, parent: QWidget = None,
                 title: str = 'Вкладка', index: int = 0):
        super().__init__(parent=parent)

        # Имя вкладки
        self.__title = title

        # Статичный индекс вкладки
        self.__index = index

        # Гор-макет для верт-макетов с формами
        self.main_hbl = QHBoxLayout()
        self.main_hbl.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.main_hbl)

        # Список, хранящий формы
        self.forms = []

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title: Any):
        self.__title = title if isinstance(title, str) else str(title)
        if self.parent():
            self.parent().setTabText(self.__index, title)


class PairEditorTab(__Tab):
    def __init__(self, parent: QWidget = None, index: int = 0):
        super().__init__(parent, 'Редактор пар', index)

        self.vbl_1 = QVBoxLayout()
        self.vbl_2 = QVBoxLayout()
        self.vbl_2.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.main_hbl.addLayout(self.vbl_2)
        self.main_hbl.addLayout(self.vbl_1)

        # Уникальное имя для пары
        self.pair_name_id_le = LineEdit(self)
        self.pair_name_id_le.setPlaceholderText('Уникальное имя пары')
        self.vbl_2.addWidget(self.pair_name_id_le)

        # Листбокс со списком всех пар
        self.pairs_lb = ListBox(self)
        self.vbl_1.addWidget(self.pairs_lb)

        # Гор-макет для кнопок действия с парами
        self.pair_btn_forms_hbl = QHBoxLayout()
        self.pair_btn_forms_hbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.vbl_1.addLayout(self.pair_btn_forms_hbl)

        self.set_pair_btn = Button(self, 'Задать пару')
        self.pair_btn_forms_hbl.addWidget(self.set_pair_btn)

        self.remove_pair_btn = Button(self, 'Удалить пару')
        self.pair_btn_forms_hbl.addWidget(self.remove_pair_btn)

        # Гор-макет для указания пары
        self.pair_forms_hbl = QHBoxLayout()
        self.vbl_2.addLayout(self.pair_forms_hbl)

        # base: str
        self.base_coin_le = LineEdit(self)
        self.base_coin_le.setPlaceholderText('base')
        self.base_coin_le.setToolTip('это базовая пара '
                                     '(BTC, ETH,  BNB, USDT) '
                                     '- то, что на бинансе пишется '
                                     'в табличке сверху')
        self.pair_forms_hbl.addWidget(self.base_coin_le)

        # quote: str
        self.quote_coin_le = LineEdit(self)
        self.quote_coin_le.setPlaceholderText('quote')
        self.quote_coin_le.setToolTip('quote - это квотируемая валюта. '
                                      'Например, для торгов по паре NEO/USDT '
                                      'базовая валюта USDT, NEO - квотируемая')
        self.pair_forms_hbl.addWidget(self.quote_coin_le)

        # spend_sum: float
        self.spend_sum_fsb = FloatSpinBox(self, 0, 1000, 0.01)
        self.spend_sum_fsb.setToolTip('spend_sum\n\n'
                                      'Сколько тратить base '
                                      'каждый раз при покупке quote')
        self.vbl_2.addWidget(self.spend_sum_fsb)

        # profit_markup: int
        self.profit_markup_isb = FloatSpinBox(self, 0, 100, 0.01)
        self.profit_markup_isb.setToolTip('profit_markup\n\n'
                                          'Какой навар нужен '
                                          'с каждой сделки? (1=1%)')
        self.vbl_2.addWidget(self.profit_markup_isb)

        # use_stop_loss: bool
        self.use_stop_loss_cb = CheckBox(self, 'Активировать StopLoss')
        self.use_stop_loss_cb.setToolTip('Нужно ли продавать '
                                         'с убытком при падении цены')
        self.vbl_2.addWidget(self.use_stop_loss_cb)

        # stop_loss: int
        self.stop_loss_isb = IntSpinBox(self, 0, 100, 1)
        self.stop_loss_isb.setToolTip('stop_loss\n\n'
                                      '1% - На сколько должна упасть цена, '
                                      'что бы продавать с убытком')
        self.vbl_2.addWidget(self.stop_loss_isb)

        # active: bool
        self.active_cb = CheckBox(self, 'Активировать')
        self.active_cb.setToolTip('active\n\nПо этому параметру '
                                  'ничего не написано')
        self.vbl_2.addWidget(self.active_cb)

        self.active_cb.name = 'active'
        self.base_coin_le.name = 'base'
        self.quote_coin_le.name = 'quote'
        self.spend_sum_fsb.name = 'spend_sum'
        self.stop_loss_isb.name = 'stop_loss'
        self.pair_name_id_le.name = 'pair_name_id'
        self.use_stop_loss_cb.name = 'use_stop_loss'
        self.profit_markup_isb.name = 'profit_markup'

        self.forms = [
            self.pair_name_id_le,
            self.base_coin_le,
            self.quote_coin_le,
            self.spend_sum_fsb,
            self.profit_markup_isb,
            self.use_stop_loss_cb,
            self.stop_loss_isb,
            self.active_cb
        ]


class BotConfiguratorTab(__Tab):
    def __init__(self, parent: QWidget = None, index: int = 1):
        super().__init__(parent, 'Конфигуратор бота', index)

        self.vbl_2 = QVBoxLayout()
        self.main_hbl.addLayout(self.vbl_2)

        # config_name_id: str
        self.cfg_name_id_le = LineEdit(self)
        self.cfg_name_id_le.setPlaceholderText('Название конфига')
        self.vbl_2.addWidget(self.cfg_name_id_le)

        # API_KEY: str
        self.api_key_le = LineEdit(self)
        self.api_key_le.setEchoMode(LineEdit.EchoMode.Password)
        self.api_key_le.setPlaceholderText('API_KEY')
        self.vbl_2.addWidget(self.api_key_le)

        # API_SECRET: str
        self.api_secret_le = LineEdit(self)
        self.api_secret_le.setEchoMode(LineEdit.EchoMode.Password)
        self.api_secret_le.setPlaceholderText('API_SECRET')
        self.vbl_2.addWidget(self.api_secret_le)

        # KLINES_LIMITS: int
        self.klines_limit_isb = IntSpinBox(self, 0, 1000, 1)
        self.klines_limit_isb.setToolTip('KLINES_LIMIT')
        self.vbl_2.addWidget(self.klines_limit_isb)

        # POINTS_TO_ENTER: int
        self.points_to_enter_isb = IntSpinBox(self, 0, 100, 1)
        self.points_to_enter_isb.setToolTip('POINTS_TO_ENTER')
        self.vbl_2.addWidget(self.points_to_enter_isb)

        # USE_OPEN_CANDLES: bool
        self.use_open_candles_cb = CheckBox(self)
        self.use_open_candles_cb.setText('Использовать последнюю '
                                         'свечу для расчётов')
        self.vbl_2.addWidget(self.use_open_candles_cb)

        # TIMEFRAME: list[str]
        self.timeframes_cmb = ComboBox(self)
        self.timeframes_cmb.setToolTip('Таймфрейм')
        self.timeframes_cmb.addItems(['1m', '3m', '5m', '15m', '30m',
                                      '1h', '2h', '4h', '6h', '8h',
                                      '12h', '1d', '3d', '1w', '1M'])
        self.vbl_2.addWidget(self.timeframes_cmb)

        self.api_key_le.name = 'api_key'
        self.api_secret_le.name = 'api_secret'
        self.timeframes_cmb.name = 'timeframe'
        self.cfg_name_id_le.name = 'config_name_id'
        self.klines_limit_isb.name = 'klines_limits'
        self.points_to_enter_isb.name = 'points_to_enter'
        self.use_open_candles_cb.name = 'use_open_candles'

        self.forms = [
            self.cfg_name_id_le,
            self.api_key_le,
            self.api_secret_le,
            self.klines_limit_isb,
            self.points_to_enter_isb,
            self.use_open_candles_cb,
            self.timeframes_cmb
        ]
