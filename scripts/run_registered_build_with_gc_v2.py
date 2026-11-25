"""Run the unchanged registered drivers with qualified payload-free path lookup and cycle collection."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.audit_story_glyph_consistency import load
from dk4tool.patch.grand_race_menu_release import sha

previous = Path('scripts/run_registered_build_with_gc_v1.py')
proof_path = Path('work/analysis/ROM_path_lookup_memory_20261105/equivalence_v1.json')
proof = load(proof_path)
assert sha(Path(proof['current_source']).read_bytes()) == proof['current_sha256']
assert len(proof['ROM_cases']) == 3 and all(r['every_mapping_andread_payload_exact'] for r in proof['ROM_cases'])
source = checked_text(previous.read_text(encoding='utf-8'), {
    "no_test_skip_rewrite_orrelaxed_release_contract=True,new_credit=0)":
    "no_test_skip_rewrite_orrelaxed_release_contract=True,new_credit=0,\n        payload_free_path_lookup_equivalence=str(proof_path),payload_free_path_lookup_equivalence_sha256=sha(proof_path.read_bytes()),\n        ROM_core_source_sha256=proof['current_sha256'],wrapper_predecessor_sha256=sha(previous.read_bytes()))",
})
if __name__ == '__main__':
    exec(compile(source, str(previous)+'::same-registered-drivers-qualified-path-lookup', 'exec'), globals())
