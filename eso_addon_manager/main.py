from eso_addon_manager.cli import run_subprogram
from eso_addon_manager.logging import init_cli_logger

from colorama import init as colorama_init


def cli_main():
    colorama_init()
    init_cli_logger()
    run_subprogram()

def gui_main():
    print('Nothing to see here yet!')

if __name__ == '__main__':
    cli_main()
