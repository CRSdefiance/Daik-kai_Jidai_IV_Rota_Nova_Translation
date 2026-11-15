"""Keep the malformed fixture attempt and use an exact-length injected format command."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/qualify_maria270_source25_v1.py').read_text(encoding='utf-8'),{
    "b'%s     '":"b'%s      '",
})
exec(compile(source,__file__+'::same-source-binding-andfour-negatives-exact-injected-fixture-length','exec'),globals())
