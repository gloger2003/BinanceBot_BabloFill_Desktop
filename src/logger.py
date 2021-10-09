from __future__ import annotations

from gui_forms import Console
from datetime import datetime
from loguru import logger

import os


def try_restore_folder():
    if not os.path.exists('./logs'):
        os.mkdir('./logs')


INFO = ('INFO   ', 'rgb(200, 190, 180)', 'rgb(200, 190, 180)')
DEBUG = ('DEBUG  ', 'rgb(70, 210, 250)', 'rgb(70, 210, 250)')
ERROR = ('ERROR  ', 'rgb(255, 50, 50)', 'rgb(255, 50, 50)')
SUCCESS = ('SUCCESS', 'rgb(170, 230, 45)', 'rgb(170, 230, 45)')
WARNING = ('WARNING', 'rgb(250, 230, 90)', 'rgb(250, 230, 90)')


class Logger:
    @staticmethod
    def get_new_filename():
        return datetime.now().strftime('./logs/%d-%m-%Y %H.%M.%S.log')

    @staticmethod
    def get_log_datetime():
        return datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    def __init__(self, console: Console) -> None:
        self.__filename = self.get_new_filename()
        self.__console = console
        self.__log_lines: list[str] = []
        self.__max_lines = 100

    def log(self, message: str, log: tuple[str]):
        if len(self.__log_lines) == self.__max_lines:
            self.__log_lines = []

        self.__log_lines.append(log[0])
        # self.__console.setHtml('<br>'.join(self.__log_lines))
        self.__console.to_log.emit('<br>'.join(self.__log_lines))

        try_restore_folder()
        with open(self.__filename, 'a', encoding='utf-8') as f:
            f.write(f'{log[1]}\n')
        pass

    def clear_console(self):
        self.__log_lines = []
        self.__console.clear()

    def decorate_message(self, message: str, level: str,
                         lvl_color: str, msg_color: str):
        d_msg = (f'<span style="color: {lvl_color}">'
                 f'{self.get_log_datetime()}</span style> | '
                 f'<span style="color: {msg_color}">{message}</span style>')

        d_msg_file = f'{self.get_log_datetime()} | {level} | {message}'
        return d_msg, d_msg_file

    def debug(self, message: str):
        logger.debug(message)
        self.log(message, self.decorate_message(message, *DEBUG))

    def success(self, message: str):
        logger.success(message)
        self.log(message, self.decorate_message(message, *SUCCESS))

    def info(self, message: str):
        logger.info(message)
        self.log(message, self.decorate_message(message, *INFO))

    def error(self, message: str):
        logger.error(message)
        self.log(message, self.decorate_message(message, *ERROR))

    def exception(self, message: str = ''):
        # import traceback
        # self.error(traceback.format_exc())
        self.error(message)

    def warning(self, message: str):
        logger.warning(message)
        self.log(message, self.decorate_message(message, *WARNING))
