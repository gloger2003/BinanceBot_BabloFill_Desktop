from __future__ import annotations
from typing import Any, Union

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class Console(QTextBrowser):
    to_log = pyqtSignal(str)

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setObjectName('Console')
        self.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.setText('Я консоль')

        self.to_log.connect(self.setHtml)
        self.to_log.connect(
            lambda: self.moveCursor(QTextCursor.MoveOperation.End))


class LineEdit(QLineEdit):
    def __init__(self, parent: QWidget = None, name: str = 'None'):
        super().__init__(parent=parent)

        self.setObjectName('LineEdit')
        self.setMinimumSize(200, 100)
        self.name = name

    def get_value(self) -> str:
        return self.text()

    def set_value(self, value: Any) -> None:
        if not isinstance(value, str):
            value = str(value)
        self.setText(value)


class Button(QPushButton):
    def __init__(self, parent: QWidget = None, text: str = 'Кнопка',
                 name: str = 'None'):
        super().__init__(parent=parent)

        self.setObjectName('Button')
        self.setMinimumSize(200, 30)
        self.name = name
        self.setText(text)


class IntSpinBox(QSpinBox):
    def __init__(self, parent: QWidget = None,
                 min_value: int = 0,
                 max_value: int = 100,
                 step: int = 1,
                 name: str = 'None') -> None:
        super().__init__(parent=parent)

        self.setObjectName('SpinBox')
        self.setMinimumSize(200, 50)

        self.name = name

        self.setMinimum(min_value)
        self.setMaximum(max_value)
        self.setSingleStep(step)

    def get_value(self) -> int:
        return self.value()

    def set_value(self, value: Union[int, str, float]) -> None:
        if not isinstance(value, int):
            value = int(value)
        self.setValue(value)


class FloatSpinBox(QDoubleSpinBox):
    def __init__(self, parent: QWidget = None,
                 min_value: float = 0,
                 max_value: float = 100,
                 step: float = 1,
                 name: str = 'None') -> None:
        super().__init__(parent=parent)

        self.setObjectName('SpinBox')
        self.setMinimumSize(200, 50)

        self.name = name

        self.setMinimum(min_value)
        self.setMaximum(max_value)
        self.setSingleStep(step)

    def get_value(self) -> float:
        return self.value()

    def set_value(self, value: Union[int, str, float]) -> None:
        if not isinstance(value, float):
            value = float(value)
        self.setValue(value)


class ComboBox(QComboBox):
    def __init__(self, parent: QWidget = None, name: str = 'None') -> None:
        super().__init__(parent=parent)

        self.setObjectName('ComboBox')
        self.setMinimumSize(200, 50)

        self.name = name

    def get_value(self) -> str:
        return self.currentText()

    def set_value(self, value: Union[str, int]) -> None:
        if isinstance(value, str):
            self.setCurrentText(value)
        elif isinstance(value, int):
            self.setCurrentIndex(value)


class CheckBox(QCheckBox):
    def __init__(self, parent: QWidget = None, text: str = 'Активировать',
                 name: str = 'None'):
        super().__init__(parent)

        self.setObjectName('CheckBox')
        self.setMinimumSize(200, 30)
        self.name = name
        self.setText(text)

    def get_value(self) -> bool:
        return self.isChecked()

    def set_value(self, value: Union[bool, int, float, str]) -> None:
        if not isinstance(value, bool):
            value = bool(value)
        self.setChecked(value)


class ListBox(QListWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent=parent)

        self.setObjectName('ListBox')
        self.setStyleSheet('ListBox {font-size: 20px}')
