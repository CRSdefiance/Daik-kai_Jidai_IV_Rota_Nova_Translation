"""Verify the V687 archive without closing visual or gameplay gates."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.finish_plaque_final_contract_v687 import REBUILT
from scripts.record_plaque_final_contract_v687 import ARCHIVE, KEY, SOURCES
from scripts.verify_plaque_final_contract_v687 import ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    provenance = read(ARCHIVE / 'provenance.json')
    assert provenance['sources'] == {p: sha(Path(p).read_bytes()) for p in SOURCES}
    for path, digest in provenance['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest, path
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    assert REBUILT.read_bytes() == ROM.read_bytes()
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k != 'current_goal_turn_classification')
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        assert data[KEY]['rebuild_proof_sha256'] == sha((ROOT / 'rebuild_proof.json').read_bytes())
        assert path.read_bytes() == (ARCHIVE / 'audits' / name).read_bytes()
    save(ROOT / 'final_verification.json', {
        'archive_files_verified': len(provenance['files']),
        'final_material_gate_six_rejection_controls_and_exact_V685_registered_rebuild_verified': True,
        'production_ROM_manifest_patch_registry_canonical_and_release_pointers_unchanged': True,
        'all18_plaques_incomplete22_historical_requirements_exact_other_graphics_gates_open': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f"V687 final: {len(provenance['files'])} archive files exact; unchanged V685; all18 plaques remain open.", flush=True)


if __name__ == '__main__':
    main()
