"""Exercise all eight production-scope mutations against the303-record transaction."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source = checked_text(Path('scripts/qualify_maria301_registered_v1.py').read_text(encoding='utf-8'), {
    'maria301_release_v2': 'maria303_release_v1',
    'prepare_maria301_registered_v2': 'prepare_maria303_registered_v2',
    "'record_count',300": "'record_count',302",
    "'scoped_name_count',35": "'scoped_name_count',19", 'all36 scoped name reviews': 'all20 scoped name reviews',
})
exec(compile(source, __file__+'::same-eight-pure-production-scope-rejections303', 'exec'), globals())
