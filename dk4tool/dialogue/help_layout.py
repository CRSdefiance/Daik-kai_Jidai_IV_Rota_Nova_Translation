"""Opt-in semantic Help lists; prose remains unpositioned editorial text."""

from scripts.prepare_help_pages_v281 import wrap


def wrap_body(english, policy='paragraph-v1'):
    if policy == 'paragraph-v1':
        return wrap(english)
    if policy != 'semicolon-entries-v1':
        raise ValueError('Unknown semantic HELP layout policy')
    entries = english.split('; ')
    if len(entries) < 2 or any(not entry.strip() for entry in entries):
        raise ValueError('A reviewed HELP list requires complete semantic entries')
    rows = []
    for index, entry in enumerate(entries):
        text = entry + (';' if index < len(entries) - 1 else '')
        try:
            item = wrap(text)
        except AssertionError as error:
            raise ValueError('One complete HELP list entry must fit one native row') from error
        if len(item) != 1:
            raise ValueError('One complete HELP list entry must fit one native row')
        rows.extend(item)
    return rows
