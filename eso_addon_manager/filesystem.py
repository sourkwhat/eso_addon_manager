import logging
import os
import shutil


def iter_top_directories(dir_path):
    for entry in os.listdir(dir_path):
        full_path = os.path.join(dir_path, entry)

        if not os.path.isdir(full_path):
            continue

        yield entry


def empty_directory(dir_path):
    return not bool(os.listdir(dir_path))


def file_exists(file_path):
    return os.path.isfile(file_path)


def directory_exists(dir_path):
    return os.path.isdir(dir_path)


def copy_directory(src_dir, target_dir):
    shutil.copytree(src_dir, target_dir, dirs_exist_ok=True)


def delete_directory(dir_path):
    shutil.rmtree(dir_path)


def delete_directory_contents(dir_path):
    for entity in os.listdir(dir_path):
        full_path = os.path.join(dir_path, entity)

        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            delete_directory(full_path)


def copy_replace_directory_contents(src_dir, target_dir):
    logger = logging.getLogger()

    for entry in iter_top_directories(src_dir):
        src_sub_dir = os.path.join(src_dir, entry)
        target_sub_dir = os.path.join(target_dir, entry)

        if not os.path.isdir(src_sub_dir):
            continue

        if entry in os.listdir(target_dir):
            logger.info(f'{target_sub_dir} already exists, deleting it before copying')

        logger.info(f'Copying {src_sub_dir} to {target_sub_dir}')
        copy_directory(src_sub_dir, target_sub_dir)
