"""Retain final material checks while preserving every original open audit item."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.finish_plaque_final_contract_v687 import REBUILT
from scripts.record_memory_streams_v682 import copy
from scripts.verify_plaque_final_contract_v687 import ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V687 Final plaque contract')
DOC = Path('docs/plaque_final_contract_v687_checkpoint.md')
KEY = 'final17_plaque_material_masks_source_hint_contract_six_regressions_and_byte_exact_V685_rebuild_v687'
SOURCES = (
    'dk4tool/graphics/plaque_contract.py', 'scripts/build_integrated_release.py',
    'scripts/verify_plaque_final_contract_v687.py', 'scripts/finish_plaque_final_contract_v687.py',
    'scripts/record_plaque_final_contract_v687.py', 'scripts/verify_plaque_contract_archive_v687.py',
    'docs/plaque_texture_workflow.md', 'translations/source_plaque_grain_v1.json',
    'translations/local_plaque_texture_v1.json', 'translations/equipment_grain_join_v1.json',
    'dk4tool/patch/main_pool_cache_visibility.py')


def main():
    pre = read(ROOT / 'preflight.json')
    cp, bp = ROOT / 'contract_proof.json', ROOT / 'rebuild_proof.json'
    proof, rebuilt = read(cp), read(bp)
    assert proof['gate_sha256'] == sha(Path(SOURCES[0]).read_bytes())
    assert proof['builder_sha256'] == sha(Path(SOURCES[1]).read_bytes())
    assert rebuilt['complete_ROM_bytes_exact_V685_no_graphics_code_or_translation_changed']
    assert sha(REBUILT.read_bytes()) == sha(ROM.read_bytes())
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    review = Path('work/analysis/plaque_review_v671')
    sheets = [review / f'{name}_V666_SOURCE_REVIEW_4x.png' for name in ('Assign_Sailors', 'Sailor_Info')]
    save(ROOT / 'visual_review.json', {
        'existing_original_current_V671_sheets_opened_again': {str(p): sha(p.read_bytes()) for p in sheets},
        'earlier_fine_grain_repair_visible_current_art_not_changed_this_checkpoint': True,
        'no_new_V685_gameplay_capture_or_user_approval_claim': True,
        'all18_entries_remain_incomplete': True})
    entry = {'documentation': str(DOC), 'contract_proof': str(cp), 'contract_proof_sha256': sha(cp.read_bytes()),
        'rebuild_proof': str(bp), 'rebuild_proof_sha256': sha(bp.read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'final_all_stage_guard_preserves_two_whole_atlases17_complete_masks_and1408_source_hint_bytes': True,
        'six_in_memory_regressions_rejected_older_menu_placeholder_gate_did_not_detect_them': True,
        'source_startup_copy_binding_used_initial_section_address_assumption_retained': True,
        'full_registered_rebuild_exact_V685470_batches114_layers_and_prior_checks_preserved': True,
        'original_runtime_review_evidence_inherited_not_a_new_playthrough': True,
        'all18_plaques_incomplete22_requirements_exact_user_visual_approval_and_other_contexts_open': True,
        'production_ROM_manifest_patch_registry_canonical_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data == pre['all_original_audits_before'][name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        copy(path, ARCHIVE / 'audits' / name)
    heading = '## V687: final plaque material contract and unchanged complete V685 rebuild'
    addition = (
        'A final builder check now preserves the two complete review-pending '
        'plaque atlases,17 independent whole English masks and1408-byte '
        'source-derived equipment hint tile after all registered stages. '
        'Six in-memory wood/letter/palette/old-repeat-seam regressions escape '
        'the older menu/placeholder gate but are rejected here. Original startup '
        'copy binds staged tile to live POOL; initial address-model failure '
        'retained. Historical and unrelated controls pass. Complete registered '
        'rebuild is byte-exact V685,retaining470 batches114 layers and prior '
        'checks; only its reproduction manifest adds the new contract. '
        'Production ROM/manifest/patch/registry/pointers unchanged. Existing '
        'original/current review sheets opened again;no new runtime or '
        'visual-acceptance claim. All18 plaques remain incomplete and22 scopes '
        'exact;controls/cards/comics/legacy/material review/older checks/final '
        'acceptance remain open. Evidence on E,no guide promotion. See '
        '[V687 checkpoint](plaque_final_contract_v687_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for p in (DOC, *map(Path, SOURCES)):
        copy(p, ARCHIVE / 'sources' / p)
    for p in ROOT.rglob('*'):
        if p.is_file():
            copy(p, ARCHIVE / 'analysis' / p.relative_to(ROOT))
    for p in sheets:
        copy(p, ARCHIVE / 'retained_review' / p.name)
    copy(review / 'current_plaque_review_proof.json', ARCHIVE / 'retained_review/current_plaque_review_proof.json')
    copy(REBUILT.with_suffix('.manifest.json'), ARCHIVE / 'rebuild' / REBUILT.with_suffix('.manifest.json').name)
    save(ARCHIVE / 'provenance.json', {
        'sources': {p: sha(Path(p).read_bytes()) for p in SOURCES},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'reproduction_ROM': str(REBUILT), 'reproduction_ROM_sha256': sha(REBUILT.read_bytes()),
        'candidate_sha256': sha(ROM.read_bytes()), 'full_goal_complete': False})
    print('V687 final material contract, byte-exact rebuild and review-pending scope recorded on E.', flush=True)


if __name__ == '__main__':
    main()
