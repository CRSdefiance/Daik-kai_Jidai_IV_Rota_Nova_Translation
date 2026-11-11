"""Reject malformed Lil261 production scopes without mutating either input."""

from scripts.qualify_lil254_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    "lil254_release_v1": "lil261_release_v1",
    "prepare_lil254_registered_v1": "prepare_lil261_registered_v1",
    "'record_count',253": "'record_count',260",
    "'speech_count',245": "'speech_count',254",
    "conf['blocks']+[320]": "conf['blocks']+[322]",
    "'scoped_name_count',9": "'scoped_name_count',8",
})

if __name__ == '__main__':
    exec(compile(source, __file__, 'exec'), globals())
