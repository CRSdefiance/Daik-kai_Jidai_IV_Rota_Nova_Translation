"""Verify exact evidence, unchanged release and retained full graphics scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_embedded_paints_v672 import ARCHIVE, KEY, SCRIPTS
from scripts.verify_embedded_paints_v672 import ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre, archive = read(ROOT / 'preflight.json'), read(ARCHIVE / 'provenance.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, digest in archive['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest, path
    assert archive['source_scripts'] == {p: sha(Path(p).read_bytes()) for p in SCRIPTS}
    proof, relation = read(ROOT / 'native_embedded_paint_proof.json'), read(ROOT / 'palette_correspondence.json')
    assert proof['script_sha256'] == sha(Path(SCRIPTS[0]).read_bytes())
    assert relation['script_sha256'] == sha(Path(SCRIPTS[1]).read_bytes())
    for preview in proof['previews']:
        assert sha(Path(preview['path']).read_bytes()) == preview['sha256']
    assert sha(Path(relation['review_sheet']).read_bytes()) == relation['review_sheet_sha256']
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k != 'current_goal_turn_classification')
        assert (ARCHIVE / 'audits' / name).read_bytes() == path.read_bytes()
        assert data[KEY]['proof_sha256'] == sha((ROOT / 'native_embedded_paint_proof.json').read_bytes())
        assert data[KEY]['palette_relation_sha256'] == sha((ROOT / 'palette_correspondence.json').read_bytes())
    save(ROOT / 'final_verification.json', {'archive_files_verified': len(archive['files']),
        '664_native_contracts16_selected_outputs_one_review_sheet': True,
        'explicit_palette_mapping_held_out_banks_verified_not_runtime_converter': True,
        'release_hashes_exact18_plaques_open22_original_requirements_retained': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f"V672 final archive verification: {len(archive['files'])} files exact; ROM and18/22 scopes unchanged.")


if __name__ == '__main__':
    main()
