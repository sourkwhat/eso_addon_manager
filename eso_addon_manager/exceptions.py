


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