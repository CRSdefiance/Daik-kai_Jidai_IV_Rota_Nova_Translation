"""Preserve eight production mutation rejections and exact caller preservation."""
from scripts.qualify_maria349_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'dk4tool.patch.maria349_release_v1': 'dk4tool.patch.maria315_release_v1',
    'scripts.prepare_maria349_registered_v1': 'scripts.prepare_maria315_registered_v1',
    "'record_count',348": "'record_count',314",
    "'speech_count',340": "'speech_count',308",
    "conf['blocks']+[286]": "conf['blocks']+[303]",
    "'scoped_name_count',18": "'scoped_name_count',13",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-eight-production-rejections-andpure-callers', 'exec'), globals())
