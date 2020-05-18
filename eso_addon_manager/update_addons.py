import copy
import io
import logging
import os
import shutil
import tempfile

from eso_addon_manager.config import Config
from eso_addon_manager.exceptions import (
    AddOnsFolderDoesntExistError,
    FailedDownloadAddOnError,
    FailedUnzipAddonError
)
from eso_addon_manager.filesystem import (
    delete_directory,
    delete_directory_contents,
    copy_replace_directory_contents,
    file_exists,
    empty_directory,
    directory_exists
)


def update_addons(config, yes_no_cb=None):
    if yes_no_cb is None:
        yes_no_cb = lambda: False

    _optional_clean_addons_directory(config, yes_no_cb)
    _log_summary_of_intentions(config, yes_no_cb)
    _install_addons(
        config,
        yes_no_cb,
        _download_addons(
            config,
            yes_no_cb
        )
    )


def _optional_clean_addons_directory(config, yes_no_cb):
    logger = logging.getLogger()

    if not directory_exists(config.addons_directory):
        raise AddOnsFolderDoesntExistError(config.addons_directory)

    if empty_directory(config.addons_directory):
        logger.info(f'{config.addons_directory} is empty')
        logger.info('Doing a clean install!')
    else:
        logger.info(f'{config.addons_directory} is not empty')
        logger.info(f'Would you like to clear the directory?')

        if yes_no_cb():
            logger.info(f'Deleting current files in {config.addons_directory}')
            delete_directory_contents(config.addons_directory)


def _log_summary_of_intentions(config, yes_no_cb):
    logger = logging.getLogger()

    logger_msg = io.StringIO()
    logger_msg.write('About to download the following addons:\n')
    for addon in config.specified_addons:
        logger_msg.write(f'\t {addon.name}: {addon.link}\n')
        for dep in addon.dependency_links:
            logger_msg.write(f'\t\t {dep}\n')
    logger.info(logger_msg.getvalue())


def _download_addons(config, yes_no_cb):
    logger = logging.getLogger()

    try:
        download_dir = tempfile.mkdtemp()
        logger.info(f'Created temporary directory addons at {download_dir}')
        for addon in config.all_addons:
            addon.download(download_dir)
        logger.info('Downloading finished!')
        return download_dir
    except:
        logger.critical('Error occured while downloading')
        if config.delete_temporary_directories_on_error:
            logger.info('Rolling back downloads')
        delete_directory(download_dir)
        raise


def _install_addons(config, yes_no_cb, download_dir):
    logger = logging.getLogger()

    logger.info('Install addons?')
    try:
        if not config.prompt_to_install or yes_no_cb():
            copy_replace_directory_contents(
                download_dir,
                config.addons_directory
            )
        else:
            logger.info(f'Addons will not be installed. They are still inside {download_dir}, would you like to delete them now?')
            if yes_no_cb():
                delete_directory(download_dir)
    except:
        logger.info('Error occurred during installation!')
        if config.delete_temporary_directories_on_err:
            logger.info('Rolling back downloads')
            delete_directory(unzip_dir)
        raise
