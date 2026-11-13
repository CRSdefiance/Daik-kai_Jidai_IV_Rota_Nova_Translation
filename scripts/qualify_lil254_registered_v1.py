"""Reject malformed Lil254 production scopes without mutating either input."""

from scripts.qualify_lil278_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'lil278_release_v1': 'lil254_release_v1',
    'prepare_lil278_registered_v1': 'prepare_lil254_registered_v1',
    "'record_count',277": "'record_count',253",
    "'speech_count',271": "'speech_count',245",
    "conf['blocks']+[312]": "conf['blocks']+[320]",
})

if __name__ == '__main__':
    exec(compile(source, __file__, 'exec'), globals())
