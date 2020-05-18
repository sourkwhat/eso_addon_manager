import logging
import os

from eso_addon_manager import constants
from eso_addon_manager.addon import AddOn

import yaml


class Config:
    def __init__(self, **kwargs):
        self._raw = kwargs

        self.addons_directory = self._raw['config'].get(
            'addons_directory',
            constants.DEFAULT_ADDONS_DIRECTORY
        )
        self.prompt_to_install = self._raw['config'].get(
            'prompt_to_install',
            constants.DEFAULT_PROMPT_TO_INSTALL
        )
        self.delete_temporary_directories_on_error = self._raw['config'].get(
            'delete_temporary_directories_on_error',
            constants.DEFAULT_DELETE_TEMPORARY_DIRECTORIES_ON_ERROR
        )
        self.addons = [AddOn(name, addon) for name, addon in self._raw.items() if name != 'config']

    @property
    def logger(self):
        return logging.getLogger()

    @property
    def unique_dependency_links(self):
        all_dep_links = []
        for addon in self.addons:
            all_dep_links.extend(addon.dependency_links)
        return set(all_dep_links)

    def write_config(self, config_path):
        with open(config_path, 'w') as config_file:
            yaml.dump(self._raw, indent=2, default_flow_style=False)

    @classmethod
    def from_path(cls, config_path=None):
        if config_path is None:
            config_path = constants.DEFAULT_CONFIG_PATH

        if not os.path.exists(config_path):
            LOGGER.critical(f'Configuration file {config_path} does not exist')
            exit(1)

        with open(config_path, 'r') as config_file:
            return cls(**yaml.load(config_file, Loader=yaml.CLoader))
