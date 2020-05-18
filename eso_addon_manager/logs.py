import logging
import sys

from eso_addon_manager import constants

import colorama


logging.SUCCESS = 15


def init_gui_logger():
    logger = logging.getLogger()
    logger.addHandler(logging.NullHandler())
    logger.setLevel(logging.NOTSET)


def init_cli_logger():
    class ColorizedStreamHandler(logging.Handler):
        _COLOR_MAP = {
            logging.INFO: colorama.Fore.WHITE,
            logging.WARNING: colorama.Fore.YELLOW,
            logging.CRITICAL: colorama.Fore.RED,
            logging.ERROR: colorama.Fore.RED,
            logging.SUCCESS: colorama.Fore.GREEN,
            logging.DEBUG: colorama.Fore.BLUE
        }

        def __init__(self):
            super().__init__()

        def emit(self, record):
            msg = self.format(record)
            sys.stdout.write(self._COLOR_MAP[record.levelno])
            sys.stdout.write(msg + '\n')
            sys.stdout.write(colorama.Style.RESET_ALL)


    formatter = logging.Formatter(fmt=constants.LOGGING_FORMAT)
    csh = ColorizedStreamHandler()
    csh.setLevel(logging.SUCCESS)
    csh.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(csh)
    logger.setLevel(logging.SUCCESS)

