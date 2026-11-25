"""Apply four visual phrase-continuity findings without changing logical prose or native code."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/check_shared_deck_current_native_v3.py').read_text(encoding='utf-8'),{
    'Shared_Deck_current_native_v4_20261104':'Shared_Deck_current_native_v5_20261104',
    'from dk4tool.dialogue.refit_help import compile_paragraph':'from scripts.shared_deck_formatting_v1 import compile_paragraph,PREFERENCES',
    "compiled,lines=compile_paragraph(row['english'].removesuffix('{PAD}'))":"compiled,lines=compile_paragraph(row['english'].removesuffix('{PAD}'),record_id=row['id'])",
    "plans.append(dict(id=row['id'],current_offset=at,allocation=end-at,compiled_hex=compiled.hex(),lines=lines,logical_English=row['english'].removesuffix('{PAD}')))":
        "plans.append(dict(id=row['id'],current_offset=at,allocation=end-at,compiled_hex=compiled.hex(),lines=lines,logical_English=row['english'].removesuffix('{PAD}'),phrase_preference_reason=PREFERENCES[row['id']][2]))",
    "layout_path,Path('dk4tool/dialogue/refit_help.py'),Path(__file__)":
        "layout_path,Path('dk4tool/dialogue/refit_help.py'),Path('scripts/shared_deck_formatting_v1.py'),Path('scripts/check_shared_deck_current_native_v3.py'),Path(__file__)",
})
exec(compile(source,__file__+'::same-verified-native-source-andfull-glyph-guards-with-phrase-continuity-findings','exec'),globals())
