"""Archive the source-palette finding without changing ROM or release pointers."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_dialogue_palette_v628 import CAP, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/dialogue_palette_v628_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V628 Source dialogue palette')
KEY = 'source_dialogue_palette_all14_captured_planes_v628'


def main():
    proof_path = ROOT / 'palette_proof.json'
    proof = read(proof_path)
    assert proof['script_sha256'] == sha(Path('scripts/verify_dialogue_palette_v628.py').read_bytes())
    assert proof['current_candidate_sha256'] == sha(ROM.read_bytes())
    assert len(proof['cases']) == 14 and proof['all14_full_foreground_and_shadow_planes_match_existing_GPU_captures']
    assert proof['four_CP932_I_comparison_findings_resolved_without_pixel_waivers']
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == proof['current_candidate_sha256']
    assert manifest['profile'] == 'all-routes-unified-v627'
    baseline = Path('out/raphael_natural_v2_accepted_base.nds')
    assert sha(baseline.read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    patch = ROM.with_suffix('.xdelta')
    assert sha(patch.read_bytes()) == 'fb4b3acb17f69174a53759c8ab74053737eade38c11d5cdee6c7d0afe3062966'
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for source in (DOC, Path(__file__), Path('scripts/verify_dialogue_palette_v628.py'), proof_path,
                   ROM.with_suffix('.manifest.json'), CAP / 'capture_report.json'):
        checked_copy(source, ARCHIVE / source.name)
    for name in ('release_proof.json', 'patch_proof.json', 'preservation_proof.json'):
        source = Path('work/analysis/tavern_recruitment_v627') / name
        checked_copy(source, ARCHIVE / ('V627_RETAINED_' + name))
    screenshots = []
    for case in proof['cases']:
        source = Path(case['source_PNG'])
        assert sha(source.read_bytes()) == case['source_PNG_sha256']
        target = ARCHIVE / f"frame_{case['frame']:06d}_UNMODIFIED_NATIVE.png"
        checked_copy(source, target)
        screenshots.append({'path': str(target), 'sha256': case['source_PNG_sha256'],
                            'frame': case['frame'], 'captured_ROM_sha256': proof['captured_candidate_sha256'],
                            'unmodified_capture': True, 'new_run': False})
    for source in ROOT.glob('*.png'):
        checked_copy(source, ARCHIVE / source.name)
    save(ARCHIVE / 'provenance.json', {
        'verification_checkpoint': 'V628', 'current_ROM_unchanged': proof['current_candidate_sha256'],
        'screenshots': screenshots, 'capture_report_sha256': proof['capture_report_sha256'],
        'fixture_disclosure': proof['capture_fixture_disclosure'],
        'actual_crops_and_plain_background_replays_separately_labeled': True,
        'publication_approved': False, 'full_goal_complete': False,
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir()
                  if p.is_file() and p.name != 'provenance.json'}})
    entry = {
        'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'current_candidate': str(ROM), 'current_candidate_sha256': proof['current_candidate_sha256'],
        'captured_candidate_sha256': proof['captured_candidate_sha256'],
        'status': 'four_CP932_I_comparison_findings_resolved_source_palette_verified',
        'all14_complete_foreground_shadow_masks_and_exact_painted_RGB_colors_match': True,
        'all45_previous_differences_are_original_gray_shadows': True,
        'clean_V626_V627_painters_palette_and_font_exact': True,
        'each_captured_RAM_palette_and_font_match_source': True,
        'first_final_letter_and_shadow_erasure_or_black_shadow_controls_rejected': True,
        'no_pixel_waivers_no_ROM_changes_no_new_emulator_run': True,
        'historical_proofs_preserved_with_finding_resolution_in_this_later_entry': True,
        'all18_original_plaques_incomplete_all22_historical_objects_retained': True,
        'broader_Confirm_miniature_village_card_legacy_comic_logo_movie_material_gates_open': True,
        'archive': str(ARCHIVE), 'unmodified_screenshots': len(screenshots),
        'full_goal_complete': False, 'canonical_promoted': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        # Preserve every other entry and pointer, including latest compiled V627.
        before = data.copy()
        data[KEY] = entry
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        current = read(path)
        assert all(current[k] == v for k, v in before.items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert current.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    heading = '## V628: capital-I comparison resolved with the original dialog palette'
    text = '''

All fourteen existing V626 Tavern dialogue captures now pass complete228x80
foreground and shadow masks plus exact painted RGB colors. The45 pixels in
four prior CP932-I comparisons are sourcegray index14 shadows, falsely counted
as missing black by the older foreground1/all-nonzero comparison. Original
dialog setup selectsforeground15. Clean/V626/V627 painter/palette/font bytes
and each captured RAM font/palette match. First/final glyph erasure and erased
or blackened shadow controls fail. No pixels waived, ROM/artwork changed or new
emulator run claimed. Historical proofs remain intact; this later result closes
only that renderer-comparison finding. Latest compiled ROM stays experimental
V627. All18 plaques incomplete,all22 historical scopes and every other audit
entry/release pointer retained. Fourteen unmodified captures, labeled previews,
provenance and proof are on E. Full graphics goal remains active. See
[V628 checkpoint](dialogue_palette_v628_checkpoint.md).
'''
    for name in ('todo', 'translation_progress', 'known_issues', 'release_build'):
        path = Path('docs') / (name + '.md')
        content = path.read_text(encoding='utf-8')
        if heading not in content:
            path.write_text(content.rstrip() + '\n\n' + heading + '\n' + text, encoding='utf-8')
    print('V628 archived14 unmodified screenshots;three audits updated;all18/22 scopes and ROM/release pointers unchanged.')


if __name__ == '__main__':
    main()
