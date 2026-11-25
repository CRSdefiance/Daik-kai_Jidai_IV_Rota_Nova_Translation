"""Retain all eight pure production-scope rejection tests for the310-record append."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/qualify_maria301_registered_v1.py').read_text(encoding='utf-8'),{
    'maria301_release_v2':'maria310_release_v1',
    'prepare_maria301_registered_v2':'prepare_maria310_registered_v1',
    "'record_count',300":"'record_count',309", "'speech_count',298":"'speech_count',309",
    "'scoped_name_count',35":"'scoped_name_count',25",'all36 scoped name reviews':'all26 scoped name reviews',
})
exec(compile(source,__file__+'::same-eight-pure-production-scope-guards310','exec'),globals())
