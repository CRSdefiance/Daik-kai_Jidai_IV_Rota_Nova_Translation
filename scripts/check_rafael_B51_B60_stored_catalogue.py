"""Check every stored body against the original current pre-macro catalogue lookup."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/check_rafael_B36_B41_stored_catalogue.py').read_text(encoding='utf-8'),{
    'Rafael_B36_B41_stored_catalogue_20261104':'Rafael_B51_B60_stored_catalogue_20261104',
    'Rafael_B36_B41_stored_native_20261104':'Rafael_B51_B60_stored_native_20261104',
    'Rafael_B36_B41_current_20261104/current_effective.json':'Rafael_B51_B60_current_runtime_20261104/current_effective.json',
    'len(rows)==175':'len(rows)==245',
    'assert len(previous_aliases)==3':'assert all(r in {q[\'id\'] for q in stored[\'records\']} for r in previous_aliases)',
    'all175_stored_effective_body_bindings.json':'all245_stored_effective_body_bindings.json',
    '175 newly stored bodies survive original catalogue lookup byte forbyte;three former alias overrides cannot restore old glyphs orwrapping.':
        '245 stored bodies survive original catalogue lookup byte forbyte;no old wording,glyphs orwraps are restored.',
})
exec(compile(source,__file__+'::same-guarded-current-pre-macro-lookup-all245-stored-bodies','exec'),globals())
