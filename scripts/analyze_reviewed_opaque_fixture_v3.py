"""Retain both exact source speakers: Sera24's symbols and actor78's reply."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/analyze_reviewed_opaque_fixture_v1.py').read_text(encoding='utf-8'),{
    "assert row['source_selector']==78 and row['compiled_hex'].startswith('4e')":
        "assert bytes.fromhex(row['compiled_hex'])[0]=={'DK4_MES_B40_R0088':24,'DK4_MES_B40_R0092':78}[ident]",
})
exec(compile(source,__file__+'::same-complete-color-masks-two-exact-source-speaker-controls','exec'),globals())
