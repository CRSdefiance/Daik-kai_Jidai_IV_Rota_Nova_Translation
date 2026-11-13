"""Reuse exact ordinary name consumers; run only three missing actors fresh."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/bind_hodram_B191_B210_identities.py').read_text(encoding='utf-8'),{
    "ROOT = Path('work/analysis/Hodram_B191_B210_clean_20261104')":"ROOT = Path('work/analysis/Hodram_B211_B230_clean_20261104')",
    "LATEST = Path('work/analysis/Hodram_B171_B190_clean_20261102/native_identity_and_term_checkpoint_v1.json')":
        "LATEST = Path('work/analysis/Hodram_B191_B210_clean_20261104/native_identity_checkpoint_v1.json')",
    "FRESH = [Path('work/analysis/Hodram_B191_B210_new_names_20261104/names.json'),\n    Path('work/analysis/Hodram_B191_B210_actor154_current_runtime_20261104/names.json')]":
        "FRESH = [Path('work/analysis/Hodram_B211_B230_new_names_20261104/names.json'), Path('work/analysis/Hodram_B211_B230_Emilio_current_runtime_20261104/names.json')]",
    "assert len(rows) == 43 and sum(r['fresh_native'] for r in rows) == 15":
        "assert len(rows) == 23 and sum(r['fresh_native'] for r in rows) == 4",
    'ordinary_actor_bindings=43, current_name_consumer_bindings=86':'ordinary_actor_bindings=23, current_name_consumer_bindings=46',
    'fresh_actors=15, reused_actors=28, fresh_clean_andcurrent_getters_each=30, unchanged_getters_reused_not_replayed=56':
        'fresh_actors=4, reused_actors=19, fresh_clean_andcurrent_getters_each=8, unchanged_getters_reused_not_replayed=38',
    "actor154_fresh_reason='Its available standalone native proof predates the registered runtime-bound repair; use two fresh current consumers rather than infer compatibility from a count of executed instructions.'":
        "fresh_reason='Actors149/197/199 lack compatible getters in reused scoped proofs. Actor14’s standalone inherited proof predates the owned Emilio/Ferog glyph repair; one fresh current pair resolves the concrete dependency mismatch without replaying the three new actors.'",
    'Bound 43 actors/86 consumers: 15 fresh and 28 exact reuses.':'Bound23 actors/46 consumers: four fresh and19 exact reuses.',
    'assert not pointer or raw == cstring(old.raw, pointer)':
        "assert not pointer or raw == cstring(old.raw, pointer), (actor,column,str(path),raw,cstring(old.raw,pointer))",
    'for path in [PREVIOUS, LATEST]:':
        "for path in [PREVIOUS, Path('work/analysis/Hodram_B171_B190_clean_20261102/native_identity_and_term_checkpoint_v1.json'), LATEST]:",
    '[LATEST, PREVIOUS, *FRESH, *OLDER, source_path, means_path, Path(__file__)]':
        "[LATEST, PREVIOUS, Path('work/analysis/Hodram_B171_B190_clean_20261102/native_identity_and_term_checkpoint_v1.json'), *FRESH, *OLDER, source_path, means_path, Path(__file__)]",
})
exec(compile(source,__file__+'::same-qualified-ordinary-identities-current-scope','exec'),globals())
