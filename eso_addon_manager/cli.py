import contextlib
import os
import sys

from eso_addon_manager import (
    constants,
    __version__
)
from eso_addon_manager.config import Config
from eso_addon_manager.filesystem import delete_directory_contents
from eso_addon_manager.exceptions import (
    InvalidCommandError,
    NoConfigFileError
)
from eso_addon_manager.logs import init_cli_logger
from eso_addon_manager.update_addons import update_addons

import colorama
import yaml


@contextlib.contextmanager
def print_color(color):
    sys.stdout.write(color)
    yield
    sys.stdout.write(colorama.Style.RESET_ALL)


def run_cli():
    colorama.init()
    init_cli_logger()
    run_subprogram()


def run_subprogram():
    subprograms = {
        'help': cli_help,
        'config': cli_config,
        'update': cli_update,
        'version': cli_version,
        'delete': cli_delete
    }

    if len(sys.argv) == 1:
        command = 'help'
    else:
        command = sys.argv[1].lower()

    if command not in subprograms:
        raise InvalidCommandError(command)

    try:
        subcommand = sys.argv[2:][0]
    except IndexError:
        subcommand = None

    subprograms[command](subcommand)


def cli_help(subcommand):
    with print_color(colorama.Fore.GREEN):
        print(
            'Usage: eso_addons <command>\n Command must be one of config, update, delete, version.\n Use eso_addons <command> help for more information'
        )


def cli_config(subcommand):
    def _print_config_file(config_path):
        with open(constants.DEFAULT_CONFIG_PATH, 'r') as config_file:
            contents = config_file.read()
        print(contents)

    def _cli_config_show():
        if not os.path.exists(constants.DEFAULT_CONFIG_PATH):
            raise NoConfigFileError

        with print_color(colorama.Fore.GREEN):
            print('Contents of configuration file:')
        _print_config_file(constants.DEFAULT_CONFIG_PATH)

    def _cli_config_default():
        if os.path.exists(constants.DEFAULT_CONFIG_PATH):
            with print_color(colorama.Fore.YELLOW):
                print('The configuration file exists, are you sure you want to overwrite?')

            if not prompt_yn():
                return

        with open(constants.DEFAULT_CONFIG_PATH, 'w') as config_file:
            yaml.dump(
                constants.DEFAULT_CONFIG_FILE,
                config_file,
                default_flow_style=False
            )

        with print_color(colorama.Fore.GREEN):
            print('Wrote config:')
            print('=============')

        _print_config_file(constants.DEFAULT_CONFIG_PATH)

    def _cli_config_delete():
        if not os.path.exists(constants.DEFAULT_CONFIG_PATH):
            with print_color(colorama.Fore.YELLOW):
                print('Configuration file doesn\'t exist. Doing nothing.')
            return

        print('Are you sure you want to delete the configuration file?')
        if prompt_yn():
            try:
                os.remove(constants.DEFAULT_CONFIG_PATH)
                with print_color(colorama.Fore.GREEN):
                    print('Configuration deleted')
            except:
                with print_color(colorama.Fore.RED):
                    print(f'Unable to delete {constants.DEFAULT_CONFIG_PATH}')

    def _cli_config_help():
        with print_color(colorama.Fore.GREEN):
            print('Usage: eso_addons config <command>\nCommand must be one of show, delete, empty, or help.')

    def _cli_config_open():
        os.system(f'notepad "{constants.DEFAULT_CONFIG_PATH}"')

    subprograms = {
        'show': _cli_config_show,
        'delete': _cli_config_delete,
        'default': _cli_config_default,
        'open': _cli_config_open,
        'help': _cli_config_help
    }

    subprograms.get(subcommand, _cli_config_help)()


def cli_update(subcommand):
    print(
        colorama.Fore.GREEN +
        'Starting update!' +
        colorama.Style.RESET_ALL
    )
    update_addons(Config.from_path(), yes_no_cb=prompt_yn)


def cli_version(subcommand):
    with print_color(colorama.Fore.GREEN):
        print(f'Version {__version__}')


def cli_delete(subcommand):
    with print_color(colorama.Fore.YELLOW):
        print('This will delete all of your addons! Are you sure you want to continue?')
        if prompt_yn():
            delete_directory_contents(constants.DEFAULT_ADDONS_DIRECTORY)


def prompt_yn():
    yn = input('(y/n?): ')
    max_errors = 3
    error = 0

    while error < max_errors:
        if yn.lower() == 'y':
            return True
        elif yn.lower() == 'n':
            return False
        else:
            error += 1

            with print_color(colorama.Fore.RED):
                print('Bad input, received {0} expected \'y\' or \'n\'')
    exit(1)