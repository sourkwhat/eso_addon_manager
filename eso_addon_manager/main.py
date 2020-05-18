from eso_addon_manager.cli import run_cli
from eso_addon_manager.gui import run_gui
from eso_addon_manager.logs import init_cli_logger

from colorama import init as colorama_init


def cli_main():
    run_cli()

def gui_main():
    init_gui_logger()
    run_gui()

if __name__ == '__main__':
    cli_main()
