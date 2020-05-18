import os

from eso_addon_manager.exceptions import UnexpectedLinkFormatError


def clean_link(link):
    if '?' not in link:
        return link

    # We'd like to strip out query parameters!
    pieces = link.split('?')
    if len(pieces) > 2:
    	raise UnexpectedLinkFormatError(link)

    return pieces[0]


def config_name_from_link(link):
	file_name = file_name_from_link(link)
	return os.path.splitext(file_name)[0]


def file_name_from_link(link):
	link = clean_link(link)
	return link.split('/')[-1]