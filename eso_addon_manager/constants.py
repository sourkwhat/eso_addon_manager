import os

HOMEDIR = os.path.join(
	os.environ['HomeDrive'],
    os.environ['HomePath']
)

# Global logging format
LOGGING_FORMAT = '%(asctime)s %(message)s'

# Defaults for the configuration file.
DEFAULT_CONFIG_PATH = os.path.join(
    HOMEDIR,
    '.eso_addon_manager'
)
DEFAULT_PROMPT_TO_INSTALL = True
DEFAULT_DELETE_TEMPORARY_DIRECTORIES_ON_ERROR = True
DEFAULT_ADDONS_DIRECTORY = os.path.join(
	HOMEDIR,
	'Documents\\Elder Scrolls Online\\live\\AddOns'
)

# The config file that will be written first as a starting point.
DEFAULT_CONFIG_FILE = {
    'config': {
        'addons_directory':
            DEFAULT_ADDONS_DIRECTORY,
        'prompt_to_install':
            DEFAULT_PROMPT_TO_INSTALL,
        'delete_temporary_directories_on_error':
            DEFAULT_DELETE_TEMPORARY_DIRECTORIES_ON_ERROR
    }
}

# Streaming chunk size for downloading addons
DEFAULT_BYTE_CHUNK_SIZE = 8192

# GUI main window parameters
MAIN_WINDOW_WIDTH = 700
MAIN_WINDOW_HEIGHT = 500
MAIN_WINDOW_TITLE = 'Harro earthlings!!!!'