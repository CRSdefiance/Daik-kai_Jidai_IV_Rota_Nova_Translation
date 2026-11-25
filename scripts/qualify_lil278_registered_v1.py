"""Run the eight production-scope rejection checks for Lil B299–B311."""

from scripts.qualify_lil361_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'dk4tool.patch.lil361_release_v1': 'dk4tool.patch.lil278_release_v1',
    'scripts.prepare_lil361_registered_v1': 'scripts.prepare_lil278_registered_v1',
    "'record_count',360": "'record_count',277",
    "'speech_count',351": "'speech_count',271",
    "conf['blocks']+[299]": "conf['blocks']+[312]",
    "'scoped_name_count',14": "'scoped_name_count',9",
})

if __name__ == '__main__':
    exec(compile(source, __file__, 'exec'), globals())
