import logging
import os
import io
import zipfile

from eso_addon_manager import constants
from eso_addon_manager.link import clean_link

import requests


class AddOn:
    def __init__(self, name, raw):
        self.name = name
        self._raw = raw

    @property
    def logger(self):
        return logging.getLogger()

    def download(self, download_dir):
        self.logger.info(f'Downloading {self.link} to {download_dir}')

        in_memory_zip = io.BytesIO()

        with requests.get(self.link, stream=True) as resp:
            resp.raise_for_status()
            for chunk in resp.iter_content(chunk_size=constants.DEFAULT_BYTE_CHUNK_SIZE):
                in_memory_zip.write(chunk)

        with zipfile.ZipFile(in_memory_zip, mode='r', compression=zipfile.ZIP_DEFLATED) as zf:
            zf.extractall(download_dir)

        self.logger.info('Finished download')

    def read_api_version(self, unzip_dir):
        pass

    @property
    def link(self):
        return clean_link(self._raw['link'])

    @property
    def is_dependency(self):
        return self._raw.get('is_dependency', False)

    @property
    def dependency_links(self):
        dep_links = []
        for dep_link in self._raw.get('dependencies', []):
            dep_links.append(clean_link(dep_link))
        return dep_links