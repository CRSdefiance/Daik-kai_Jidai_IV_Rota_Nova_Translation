"""Archive original comic software-scaling evidence without scene/GPU clearance."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.research_comic_scaling_v680 import ROOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V680 Comic native scales')
DOC = Path('docs/comic_scaling_v680_checkpoint.md')
KEY = 'all21_raw_comic_frames42_original_native_scales72_caption_edges_and_preserved_brown_marks_v680'
SCRIPTS = ('scripts/research_comic_scaling_v680.py', 'scripts/verify_comic_scaling_v680.py',
    'scripts/record_comic_scaling_v680.py', 'scripts/verify_comic_scaling_archive_v680.py',
    'scripts/verify_comic_final_letters_v251.py')


def copy(source, target):
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, target)


def main():
    pp, ip = ROOT / 'proof.json', ROOT / 'independent_verification.json'
    proof, independent, pre = read(pp), read(ip), read(ROOT / 'preflight.json')
    assert independent['verifier_sha256'] == sha(Path('scripts/verify_comic_scaling_v680.py').read_bytes())
    assert len(proof['complete_native_scale_cases']) == 42 and proof['caption_edge_checks'] == 72
    assert not proof['projected_missing_edge_letter_contrasts']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'independent_verification': str(ip), 'independent_verification_sha256': sha(ip.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'status': 'controlled_original_raw16_scaling_and_caption_edges_verified_comic_parent_GPU_still_open',
        'all21_original_partial_frame_reads_only_SDK_filesystem_bridged': True,
        '42_complete_native_scaled_two_screen_buffers8257536_bytes_and4_coordinate_controls': True,
        '18_stored_caption_planes_and72_scaled_leading_trailing_contrasts_verified': True,
        'original_scaler_resamples_complete_source_into_clipped_destination_contract': True,
        'all21_frames_exact_prior_art_and_brown_mark4320_bytes_exact_canonical_source': True,
        'six_source_current_native_software_sheets_all21_frames_visually_reviewed': True,
        'research_descriptor_and_viewport_supplied_no_actual_comic_GPU_or_scene_credit': True,
        'original_color_high_bits_unchanged_no_opacity_fix_or_guide_promotion': True,
        'plaque_material_packet_presented_no_user_acceptance_assumed': True,
        'all18_plaques_incomplete22_historical_requirements_exact_other_gates_open': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
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
    heading = '## V680: all21 raw comic frames through original native scaling'
    addition = ('Original SLACK reads load all21 direct16 frames with only SDK filesystem '
        'bridged.42 full native scale cases compare8257536 complete two-screen bytes, '
        'including guards and ABI;four supplied X/Y planes verify source sampling. The '
        'original scaler resamples the whole source into clipped destination dimensions, '
        'rather than post-scale cropping.18 stored caption planes remain exact;all72 first/'
        'final character contrasts survive these supplied scales. An independent source-' 
        'forward model verifies all output hashes/RGB planes. All21 stored frames match '
        'earlier reviewed art;the4320-byte brown-mark rectangle remains canonical-exact. '
        'Six source/current/native-software sheets opened. These are isolated research '
        'descriptors and RGB software planes,not actual comic scene/GPU/readability proof. '
        'Original high bits/production art remain unchanged. Plaque comparisons presented '
        'for material review;no acceptance assumed. V678/patch/registry/pointers unchanged; '
        'all18 plaques incomplete and22 scopes exact. Other contexts/restoration/older '
        'checks/final acceptance remain open. Evidence on E,no guide promotion. Full goal '
        'active. See [V680 checkpoint](comic_scaling_v680_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        value = path.read_text(encoding='utf-8')
        assert heading not in value
        path.write_text(value.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    for source in (DOC, *map(Path, SCRIPTS), Path('translations/gallery_chase_fringe_raw_art_v8.json')):
        copy(source, ARCHIVE / 'sources' / source.name)
    for source in ROOT.rglob('*'):
        if source.is_file():
            copy(source, ARCHIVE / 'analysis' / source.relative_to(ROOT))
    copy(Path('work/analysis/comic_scaling_v680_run.log'), ARCHIVE / 'analysis' / 'native_run.log')
    for name in frozen:
        copy(Path('translations') / name, ARCHIVE / 'audits' / name)
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        copy(Path('docs') / name, ARCHIVE / 'docs' / name)
    save(ARCHIVE / 'provenance.json', {'source_scripts': {p: sha(Path(p).read_bytes()) for p in SCRIPTS},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
            if p.is_file() and p.name != 'provenance.json'}, 'candidate_sha256': pre['candidate_sha256'],
        'software_projection_not_original_GPU_scene_or_guide_capture': True, 'full_goal_complete': False})
    print('V680 native scale evidence archived; full18/22 graphics scopes retained.', flush=True)


if __name__ == '__main__':
    main()
