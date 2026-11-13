"""Bind original menu option/style planes to their exact reviewed caption IDs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/approve_hodram_B0_B41_display_v1.py').read_text(encoding='utf-8'),{
    "        for row in proof['records']:\n            assert source[row['id']]['english']==row['english']":
    "        for row in proof['records']:\n            if row['version']=='reviewed-English':\n                assert source[obj['record_ids'][row['option']]]['english']==row['text']",
})
exec(compile(source,__file__+'::same-approval-with-exact-original-caption-option-schema','exec'),globals())
