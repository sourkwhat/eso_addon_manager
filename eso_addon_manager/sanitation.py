from eso_addon_manager.exceptions import UnexpectedLinkFormatError


def clean_link(link):
    if '?' not in link:
        return link

    # We'd like to strip out query parameters!
    pieces = link.split('?')
    if len(pieces) > 2:
    	raise UnexpectedLinkFormatError(link)

    return pieces[0]
