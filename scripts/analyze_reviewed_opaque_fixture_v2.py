"""Read the qualified selector from the original compiled native record byte."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/analyze_reviewed_opaque_fixture_v1.py').read_text(encoding='utf-8'),{
    "row['source_selector']==78":"bytes.fromhex(row['compiled_hex'])[0]==78",
})
exec(compile(source,__file__+'::same-two-complete-color-masks-source-qualified-selector-byte','exec'),globals())
