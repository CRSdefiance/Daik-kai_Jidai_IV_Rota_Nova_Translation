"""Archive the full shared-name correction and preserve every graphics scope."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_region_boundaries_v640 import CAP, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/region_boundaries_v640_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V640 Region name boundaries')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V640 Region names')
KEY = 'all8_shared_region_name_boundaries_and_all7_ordinary_Area_tooltips_v640'


def main():
    proof_path = ROOT / 'release_proof.json'
    proof = read(proof_path)
    assert sha(ROM.read_bytes()) == proof['candidate_sha256']
    assert sha(Path('scripts/verify_region_boundaries_v640.py').read_bytes()) == proof['script_sha256']
    assert len(proof['all7_ordinary_region_tooltips_and_repeat']) == 8
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    GUIDE.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 20)
    pair = Image.new('RGB', (1056, 820), '#263238')
    draw = ImageDraw.Draw(pair)
    for x, name, text in ((8, 'region_boundaries_v640_map_source', 'V636: old joined name'),
                           (536, 'region_boundaries_v640_map', 'V640: complete Americas')):
        report = read(CAP / name / 'capture_report.json')
        shot = next(r for r in report['frames_captured'] if r['frame'] == 37200)
        draw.text((x, 8), text + ' (derived2x)', font=font, fill='white')
        pair.paste(Image.open(shot['path']).resize((512, 768), Image.Resampling.NEAREST), (x, 44))
    pair_path = ROOT / 'AMERICAS_SOURCE_CURRENT_REVIEW_2x_DERIVED.png'
    pair.save(pair_path)
    files = [DOC, proof_path, ROM.with_suffix('.manifest.json'),
             Path('translations/region_name_boundaries_v1.json'), Path('dk4tool/patch/region_name_boundaries.py'),
             Path('scripts/build_integrated_release.py'), Path('scripts/prepare_region_boundaries_v640.py'),
             Path('scripts/verify_region_boundaries_v640.py'), Path(__file__), pair_path]
    files.extend(ROOT / name for name in ('native_preview_proof.json', 'patch_proof.json',
        'preservation_proof.json', 'legacy_fixed_text_boundary_census.json', 'fixed_text_batches.txt',
        'all7_area_inputs.json', 'ordinary_region_tooltip_cases.json', 'handoff_identity.json',
        'build.log', 'ALL8_REGION_NAMES_NATIVE_PREVIEWS.png'))
    files.extend(ROOT.glob('REGION*_NATIVE_PREVIEW.png'))
    for path in files:
        checked_copy(path, ARCHIVE / path.name)
    screenshots, guides = [], []
    for receipt in proof['reports']:
        path = Path(receipt['path'])
        assert sha(path.read_bytes()) == receipt['sha256']
        report = read(path)
        label = path.parent.name
        checked_copy(path, ARCHIVE / (label + '_capture_report.json'))
        journal = path.parent / 'navigation_command_journal.json'
        if journal.exists():
            checked_copy(journal, ARCHIVE / (label + '_navigation_journal.json'))
        shots = {r['frame']: r for r in report['frames_captured']}
        selected = set(shots) if label.endswith('_market') else {f for f in shots if f >= 34800}
        for frame in sorted(selected):
            row = shots[frame]
            target = ARCHIVE / f'{label}_{frame:06d}_UNMODIFIED_NATIVE.png'
            checked_copy(row['path'], target)
            record = {'path': str(target), 'frame': frame, 'sha256': row['PNG_sha256'],
                      'ROM_sha256': report['ROM_sha256'], 'unmodified_capture': True,
                      'ordinary_no_save_no_RAM_or_ROM_fixture': True,
                      'historical_broken_control': label.endswith('_source')}
            screenshots.append(record)
            guide_ok = label.endswith('_market') and frame in (1600, 3600) or label.endswith('_map') and frame == 37200
            if guide_ok:
                checked_copy(row['path'], GUIDE / target.name)
                guides.append({**record, 'path': str(GUIDE / target.name), 'source_report': str(path)})
    save(GUIDE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'screenshots': guides, 'publication_approved': False, 'old_broken_control_excluded': True})
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'screenshots': screenshots, 'guide_candidates': guides, 'full_goal_complete': False,
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir()
                  if p.is_file() and p.name != 'provenance.json'}})
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before_path = ROOT / 'audit_before.json'
    if not before_path.exists():
        save(before_path, {name: read(Path('translations') / name) for name in frozen})
    before = read(before_path)
    entry = {
        'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'], 'profile': proof['profile'],
        'patch_sha256': proof['patch_sha256'], 'status': 'experimental_shared_region_family_boundary_fix_verified',
        'all8_independently_terminated_names_and_native_getters_complete': True,
        'all7_ordinary_Area_tooltips_complete_and_old_AmericasMed_reproduced': True,
        'all_other_pixels_and32_startup_Market_regression_frames_exact': True,
        'all470_batches114_layers921_graphics57_embedded_extents_exact_patch_retained': True,
        'adjacent_nontext_integer_array_geometry_all_code_palettes_and_staged_sections_preserved': True,
        'legacy_census_85_batches7018_records_singular_matching_pattern_not_global_C_string_proof': True,
        'seven_separate_regional_source_pages_not_inferred_from_global_map_area_selection': True,
        'all18_original_plaques_incomplete_all22_scopes_retained': True,
        'archive': str(ARCHIVE), 'guide_archive': str(GUIDE),
        'full_goal_complete': False, 'canonical_promoted': False,
    }
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert all(data[k] == v for k, v in before[name].items()
                   if k not in (KEY, 'latest_compiled_experimental_candidate_with_inherited_native_gap', 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY] = entry
        latest_key = 'latest_compiled_experimental_candidate_with_inherited_native_gap'
        latest = data.get(latest_key, {}).copy()
        latest.update({'candidate': str(ROM), 'sha256': proof['candidate_sha256'], 'profile': proof['profile'],
                       'all8_region_name_boundaries_and_all7_actual_Area_tooltips_verified': True,
                       'broader_graphics_gates_remain_open': True})
        data[latest_key] = latest
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        current = read(path)
        assert all(current[k] == v for k, v in before[name].items()
                   if k not in (KEY, latest_key, 'current_goal_turn_classification'))
    heading = '## V640: complete region-name family boundaries and ordinary Area tooltips'
    addition = '''

Fixes inherited AmericasMed. by repacking all8 complete shared names with owned
NUL terminators in existing80-byte storage72 used. Four pointers move; adjacent
integer-array word,all8 metadata records,code and staged sections stay exact.
Native full96x16 previews and all8 live getters pass. Ordinary X/Area controls
exercise all7 region tooltips and a repeat;paired V636 reproduces the old join.
Complete glyphs,white margins,original blue-border occlusion and restored suffix
tail pass;every other pixel is exact.32 startup/New Game/story/town/Market frames
and4 map prefixes pass. All470/114 layers,921/57 preservation and exact clean patch
retained. V640 SHA25693868a0b250a3b52897225dac48ab29e0b14d1f097208ca9a418208dd29d0b9e.
ROM/patch,screenshots,proof and guide candidates are on E. Bounded85-batch/7018-record
exact-capacity census finds only this matching pattern,not global string clearance.
All18 plaques incomplete and22 scopes exact;other actual regional pages and
broader graphics gates open. Only latest compiled experimental pointer advances;
canonical/V610 verified remain. See [V640 checkpoint](region_boundaries_v640_checkpoint.md).
'''
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n' + addition, encoding='utf-8')
    print(f'Archived{len(screenshots)} unmodified screens/{len(guides)} guides;3 audits updated;all18/22 scopes preserved;compiled experimental pointerV640.')


if __name__ == '__main__':
    main()
