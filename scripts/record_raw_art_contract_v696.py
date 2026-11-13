"""Record the final comic guard without promoting old artwork or native coverage."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.verify_raw_art_final_contract_v696 import REBUILT, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V696 Final raw comic contract')
KEY = 'final18_raw_comic_planes11_untouched_frames4320_mark_bytes_seven_controls_exact_V692_rebuild_v696'
DOC = Path('docs/raw_art_final_contract_v696_checkpoint.md')
SOURCES = ('dk4tool/graphics/raw_art_contract.py', 'dk4tool/graphics/raw_bgr555_art.py',
    'dk4tool/graphics/raw_caption_restore.py', 'dk4tool/graphics/raw_chase_restore.py',
    'dk4tool/graphics/raw_maria_tiles.py', 'dk4tool/graphics/raw_reveal_comic.py',
    'scripts/build_integrated_release.py', 'scripts/verify_raw_art_final_contract_v696.py',
    'scripts/finish_raw_art_contract_v696.py', 'scripts/record_raw_art_contract_v696.py',
    'scripts/verify_raw_art_contract_archive_v696.py', 'translations/gallery_chase_fringe_raw_art_v8.json')


def main():
    pp = ROOT / 'contract_proof.json'
    proof, rebuild, pre = read(pp), read(ROOT / 'rebuild_proof.json'), read(ROOT / 'preflight.json')
    assert proof['gate_sha256'] == sha(Path('dk4tool/graphics/raw_art_contract.py').read_bytes())
    assert proof['builder_sha256'] == sha(Path('scripts/build_integrated_release.py').read_bytes())
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_raw_art_final_contract_v696.py').read_bytes())
    assert rebuild['verifier_sha256'] == sha(Path('scripts/finish_raw_art_contract_v696.py').read_bytes())
    assert REBUILT.read_bytes() == ROM.read_bytes()
    assert len(proof['seven_later_stage_corruptions_rejected']) == 7
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'visual_review.json', {'retained_source_current_sheets_opened': [
        'work/analysis/comic_current_v506/source_current_frames_04_07.png',
        'work/analysis/comic_current_v506/source_current_frames_12_15.png'],
        'no_clear_new_artwork_defect_identified_in_these_sheets': True,
        'hidden_scenery_reconstruction_remains_estimated_and_unknown_comic_viewer_remains_open': True,
        'guard_protects_existing_reviewed_art_not_user_acceptance_or_new_native_display': True})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'rebuild_proof': str(ROOT / 'rebuild_proof.json'),
        'rebuild_proof_sha256': sha((ROOT / 'rebuild_proof.json').read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'final18_complete_caption_regions11_untouched_frames_and4320_user_preserved_bytes_protected': True,
        'complete3225600_byte_raw_block_unowned_source_and_original_high_bits_preserved': True,
        'seven_later_stage_corruptions_escape_old_menu_gate_and_are_rejected_here': True,
        'all470_batches114_layers_and_all_prior_checks_retained_in_byte_exact_V692_rebuild': True,
        'historical_V185_and_unrelated_story_other_archive_block_controls_pass': True,
        'no_new_art_native_context_or_hidden_source_recovery_clearance': True,
        'all18_plaques_incomplete22_original_requirements_and_broader_goal_open_or_exact': True,
        'production_ROM_manifest_patch_registry_canonical_and_release_pointers_unchanged': True,
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
    heading = '## V696: final-build protection for the raw comic family'
    addition = (
        'A new final guard checks all18 reviewed comic caption/restoration regions,all11 '
        'untouched frames,unowned source words,original high bits and4320 preserved brown-mark '
        'bytes after every registered stage. Seven in-memory leading/final glyph,Japanese '
        'reversion,mark,alpha,unowned-scene and restoration corruptions pass the older final '
        'menu gate but are rejected here. Historical V185,not-applicable and unrelated story/'
        'archive-block controls pass. Full registered rebuild is byte-exact V692,retaining '
        '470 batches114 layers and every prior check/path/record/relocation;only reproduction '
        'manifest gains the contract. No production ROM/art/prose/manifest/patch/registry or '
        'pointer changes. Two retained source/current sheets opened;hidden scenery remains '
        'estimated and original comic consumer/readability remain open. All18 plaques '
        'incomplete,22 historical scopes exact;broader graphics,older checks and acceptance '
        'remain open. Evidence on E,no new native run,guide promotion,commit or push. '
        'Full goal active. See [V696 checkpoint](raw_art_final_contract_v696_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for path in (*map(Path, SOURCES), DOC, Path('AGENTS.md'), Path('docs/build_continuity_protocol.md')):
        copy(path, ARCHIVE / 'sources' / path)
    for path in ROOT.rglob('*'):
        if path.is_file():
            copy(path, ARCHIVE / 'analysis' / path.relative_to(ROOT))
    copy(REBUILT.with_suffix('.manifest.json'), ARCHIVE / 'reproduction.manifest.json')
    external = {str(REBUILT): sha(REBUILT.read_bytes())}
    for sheet in read(ROOT / 'visual_review.json')['retained_source_current_sheets_opened']:
        p = Path(sheet)
        external[str(p)] = sha(p.read_bytes())
    save(ARCHIVE / 'provenance.json', {'scripts_and_configs': {p: sha(Path(p).read_bytes()) for p in SOURCES},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'external_E_drive_evidence': external, 'no_new_ROM_content_or_guide_promotion': True,
        'full_goal_complete': False})
    print('V696 final comic guard, exact complete V692 rebuild and unchanged full audit scope recorded on E.', flush=True)


if __name__ == '__main__':
    main()
