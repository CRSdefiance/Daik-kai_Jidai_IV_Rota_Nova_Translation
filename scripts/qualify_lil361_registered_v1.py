"""Retain all eight production-scope negatives and pure caller-preservation guards."""
from scripts.qualify_lil269_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'dk4tool.patch.lil269_release_v1': 'dk4tool.patch.lil361_release_v1',
    'scripts.prepare_lil269_registered_v1': 'scripts.prepare_lil361_registered_v1',
    "'record_count',268": "'record_count',360",
    "'speech_count',261": "'speech_count',351",
    "conf['blocks']+[283]": "conf['blocks']+[299]",
    "'scoped_name_count',24": "'scoped_name_count',14",
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-eight-production-rejections-andcaller-preservation', 'exec'), globals())
