"""Keep all eight production-scope rejection and caller-preservation guards."""
from scripts.qualify_maria305_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'dk4tool.patch.maria305_release_v2': 'dk4tool.patch.maria321_release_v1',
    'scripts.prepare_maria305_registered_v2': 'scripts.prepare_maria321_registered_v2',
    "'record_count',304": "'record_count',320",
    "'speech_count',293": "'speech_count',316",
    "conf['blocks']+[196]": "conf['blocks']+[216]",
    "'scoped_name_count',26": "'scoped_name_count',23",
})

if __name__ == '__main__':
    exec(compile(source,__file__+'::same-eight-production-rejections-andpure-callers-mixed321','exec'),globals())
