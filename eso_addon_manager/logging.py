import logging
import sys

import colorama



def init_cli_logger():
    class ColorizedStreamHandler(logging.Handler):
        _COLOR_MAP = {
            'INFO': colorama.Fore.GREEN,
            'WARNING': colorama.Fore.YELLOW,
            'CRITICAL': colorama.Fore.RED,
            'ERROR': colorama.Fore.RED,
            'EXCEPTION': colorama.Fore.RED
        }

        def __init__(self):
            super().__init__()

        def emit(self, record):
            msg = self.format(record)
            sys.stdout.write(self._COLOR_MAP[record.levelname])
            sys.stdout.write(msg + '\n')
            sys.stdout.write(colorama.Style.RESET_ALL)


    formatter = logging.Formatter(fmt='%(asctime)s %(message)s')
    csh = ColorizedStreamHandler()
    csh.setLevel(logging.INFO)
    csh.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(csh)
    logger.setLevel(logging.INFO)


