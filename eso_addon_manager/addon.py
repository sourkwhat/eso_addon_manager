import logging
import os
import zipfile

from eso_addon_manager.sanitation import clean_link

import requests


class AddOn:
    DOWNLOAD_CHUNK_SIZE = 8192

    def __init__(self, name, raw):
        self.name = name
        self._raw = raw

    @property
    def logger(self):
        return logging.getLogger()

    def local_zip_path(self, link, download_dir):
        fname = link.split('/')[-1]
        assert 'zip' in fname, f'Expected {fname} to be a zip file!'
        full_path = os.path.join(download_dir, f'{fname}')
        return os.path.normpath(full_path)

    def _download_package(self, link, download_path):
        self.logger.info(f'Downloading {self.link} to {download_path}')
        with requests.get(link, stream=True) as resp:
            resp.raise_for_status()
            with open(download_path, 'wb') as local_file:
                for chunk in resp.iter_content(chunk_size=self.DOWNLOAD_CHUNK_SIZE):
                    local_file.write(chunk)
        self.logger.info('Finished download')

    def _unzip_package(self, zip_path, unzip_dir):
        self.logger.info(f'Unzipping {zip_path} tp {unzip_dir}')
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            zip_file.extractall(unzip_dir)

    def download(self, download_dir, deps_to_download):        
        self._download_package(self.link, self.local_zip_path(self.link, download_dir))

        deps_downloaded = set()
        for dep_link in self.dependency_links:
            if dep_link not in deps_to_download:
                self.logger.info(f'{self.name} requested {dep_link}, but it has already been downloaded!')
                continue

            assert dep_link not in deps_downloaded, (
                f'Duplicate dependency of {dep_link} in {self.name}'
            )
            deps_downloaded.add(dep_link)
            self._download_package(
                dep_link,
                self.local_zip_path(dep_link, download_dir)
            )
        return set(deps_downloaded)
        
    def unzip(self, download_dir, unzip_dir, deps_to_unzip):
        self._unzip_package(
            self.local_zip_path(self.link, download_dir),
            unzip_dir
        )

        dep_links_unzipped = set()
        for dep_link in self.dependency_links:
            dep_path = self.local_zip_path(dep_link, download_dir)
            if dep_link not in deps_to_unzip:
                self.logger.info(f'{self.name} requested {dep_path} to be unzipped, but it has already been unzipped!')
                continue

            assert dep_link not in dep_links_unzipped, (
                f'Duplicate dependency of {dep_path} in {self.name}'
            )
            dep_links_unzipped.add(dep_link)
            self._unzip_package(dep_path, unzip_dir)
        return set(dep_links_unzipped)

    def read_api_version(self, unzip_dir):
        pass

    @property
    def link(self):
        return clean_link(self._raw['link'])

    @property
    def ensure_up_to_date(self):
        return self._raw.get('ensure_up_to_date', True)

    @property
    def dependency_links(self):
        dep_links = []
        for dep_link in self._raw.get('dependencies', []):
            dep_links.append(clean_link(dep_link))
        return dep_links