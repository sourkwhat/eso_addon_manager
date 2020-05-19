from eso_addon_manager.cli import run_cli
from eso_addon_manager.gui import run_gui

from colorama import init as colorama_init


def cli_main():
    run_cli()

def gui_main():
    run_gui()

if __name__ == '__main__':
    cli_main()
