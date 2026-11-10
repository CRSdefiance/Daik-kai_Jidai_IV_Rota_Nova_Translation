"""Exercise the inherited production-scope rejection cases against the exact new batch."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/qualify_maria301_registered_v1.py').read_text(encoding='utf-8'),{
    'maria301_release_v2':'maria270_release_v1',
    'prepare_maria301_registered_v2':'prepare_maria270_registered_v2',
    "'record_count',300":"'record_count',269", "'speech_count',298":"'speech_count',265",
    "'scoped_name_count',35":"'scoped_name_count',27", 'all36 scoped name reviews':'all28 scoped name reviews',
})
exec(compile(source,__file__+'::same-eight-pure-production-rejections-exact-Maria270-counts','exec'),globals())
