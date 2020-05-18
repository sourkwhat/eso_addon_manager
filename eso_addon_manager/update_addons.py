import copy
import io
import logging
import os
import shutil
import tempfile

from eso_addon_manager.config import Config
from eso_addon_manager.filesystem import (
    delete_directory,
    delete_directory_contents,
    copy_replace_directory_contents,
    file_exists,
    empty_directory
)


def update_addons(config, yes_no_cb=None):
    logger = logging.getLogger()

    if yes_no_cb is None:
        yes_no_cb = lambda: False

    if not file_exists(config.addons_directory):
        logger.critical(f'{config.addons_directory} doesn\'t exist, can\'t do anything')
        return

    if empty_directory(config.addons_directory):
        logger.info(f'{config.addons_directory} is empty')
        logger.info('Doing a clean install!')
    else:
        logger.info(f'{config.addons_directory} is not empty')
        logger.info(f'Would you like to clear the directory?')

        if yes_no_cb():
            logger.info(f'Deleting current files in {config.addons_directory}')
            delete_directory_contents(config.addons_directory)

    logger_msg = io.StringIO()
    logger_msg.write('About to download the following addons:\n')
    for addon in config.addons:
        logger_msg.write(f'\t {addon.name}: {addon.link}\n')
        for dep in addon.dependency_links:
            logger_msg.write(f'\t\t {dep}\n')
    logger.info(logger_msg.getvalue())

    try:
        download_dir = tempfile.mkdtemp()
        logger.info(f'Created temporary directory for zip files at {download_dir}')
        deps_to_download = config.unique_dependency_links
        for addon in config.addons:
            deps_downloaded = addon.download(download_dir, deps_to_download)
            deps_to_download -= deps_downloaded
        logger.info('Downloading finished!')
    except:
        logger.critical('Error occured while downloading')
        if config.delete_temporary_directories_on_error:
            logger.info('Deleting zip file directory')
        delete_directory(download_dir)
        raise

    try:
        unzip_dir = tempfile.mkdtemp()
        logger.info(f'Created temporary directory for unzipped files at {unzip_dir}')
        deps_to_unzip = config.unique_dependency_links
        for addon in config.addons:
            deps_unzipped = addon.unzip(download_dir, unzip_dir, deps_to_unzip)
            deps_to_unzip -= deps_unzipped
        logger.info('Unzipping complete!')
    except:
        logger.critical('Error occurred while unzipping')
        if config.delete_temporary_directories_on_error:
            logger.info('Deleting both zipped and unzipped directories')
            delete_directory(download_dir)
            delete_directory(unzip_dir)
        raise

    logger.info('Removing temporary directory with zip files')
    shutil.rmtree(download_dir)

    logger.info('Install addons?')
    try:
        if not config.prompt_to_install or yes_no_cb():
            copy_replace_directory_contents(unzip_dir, config.addons_directory)
        else:
            logger.info(f'Addons will not be installed. They are still inside {unzip_dir}, would you like to delete them now?')
            if yes_no_cb():
                delete_directory(unzip_dir)
    except:
        logger.info('Error occurred during installation!')
        if config.delete_temporary_directories_on_error:
            logger.info('deleting unzipped directory')
            delete_directory(unzip_dir)
        raise