


class NoConfigFileError(Exception):
    def __str__(self):
        return 'No configuration file found, make one first!'


class InvalidCommandError(Exception):
    def __init__(self, invalid_cmd):
        self.invalid_cmd = invalid_cmd

    def __str__(self):
        return f'Invalid command given {self.invalid_cmd}'


class UnexpectedLinkFormatError(Exception):
    def __init__(self, bad_link):
        self.bad_link = bad_link

    def __str__(self):
        return f'Bad link format: {self.bad_link}'


class AddOnsFolderDoesntExistError(Exception):
    def __init__(self, addon_directory):
        self.addon_directory

    def __str__(self):
        return f'AddOn directory doesn\'t exist {self.addon_directory}'


class FailedDownloadAddOnError(Exception):
    def __init__(self, addon):
        self.addon = addon

    def __str__(self):
        return f'Failed to download addon {addon.name}'


class FailedUnzipAddonError(Exception):
    def __init__(self, addon):
        self.addon = addon

    def __str__(self):
        return f'Failed to unzip addon {addon.name}'