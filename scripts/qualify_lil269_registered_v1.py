"""Retain all eight production rejections and pure caller-preservation guards."""
from scripts.qualify_lil382_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'dk4tool.patch.lil382_release_v1': 'dk4tool.patch.lil269_release_v1',
    'scripts.prepare_lil382_registered_v1': 'scripts.prepare_lil269_registered_v1',
    "'record_count',381": "'record_count',268",
    "'speech_count',377": "'speech_count',261",
    "conf['blocks']+[243]": "conf['blocks']+[283]",
    "'scoped_name_count',33": "'scoped_name_count',24",
})
if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-eight-rejections-andcomplete-caller-preservation', 'exec'), globals())
