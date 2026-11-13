"""Archive current condition evidence and add it without closing prior scopes."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_condition_matrix_v637 import CAP, ROM, ROOT
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_condition_matrix_v637 import AUDIT_KEY
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/condition_matrix_v637_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V637 Condition matrix')


def main():
    proof_path = ROOT / 'current_condition_matrix_proof.json'
    proof = read(proof_path)
    assert sha(ROM.read_bytes()) == proof['candidate_sha256']
    assert len(proof['all84_actual_health_mood_combinations']) == 84
    assert len(proof['all86_fixture_replays']) == 86
    for path, digest in proof['scripts'].items():
        assert sha(Path(path).read_bytes()) == digest
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    files = [DOC, proof_path, ROOT / 'preflight.json', ROOT / 'cases.json', ROOT / 'visual_review.json',
             ROOT / 'commands.jsonl', ROOT / 'initial_inputs.json',
             ROOT / 'audit_before.json', CAP / 'capture_report.json',
             CAP / 'navigation_command_journal.json', Path(__file__),
             ROM.with_suffix('.manifest.json')]
    files.extend(Path(path) for path in proof['scripts'])
    for path in files:
        checked_copy(path, ARCHIVE / path.name)
    screenshots = []
    for row in proof['all84_actual_health_mood_combinations']:
        source = Path(row['image'])
        target = ARCHIVE / f"SYNTHETIC_actor{row['actor']}_health{row['health']}_mood{row['mood']}_frame{row['frame']:06d}_UNMODIFIED_NATIVE.png"
        checked_copy(source, target)
        screenshots.append({'path': str(target), 'sha256': sha(target.read_bytes()),
                            'actor': row['actor'], 'health': row['health'], 'mood': row['mood'],
                            'frame': row['frame'], 'unmodified_capture': True,
                            'synthetic_conditions_not_natural_events': True, 'guide_eligible': False})
    sheets = []
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 17)
    for actor in (3, 10):
        sheet = Image.new('RGB', (6 * 372 + 16, 7 * 156 + 82), '#263238')
        draw = ImageDraw.Draw(sheet)
        draw.text((16, 8), f'V636 {"Maria" if actor == 3 else "Xien"}: all42 isolated health/mood display combinations', font=font, fill='white')
        draw.text((16, 35), 'Derived review crops at3x nearest-neighbor; full unmodified captures saved separately. Plaque audit remains open.', font=font, fill='#dfd3ac')
        for row in (r for r in proof['all84_actual_health_mood_combinations'] if r['actor'] == actor):
            x, y = 16 + row['mood'] * 372, 76 + row['health'] * 156
            names = ' / '.join(label['text'] for label in row['labels'])
            draw.text((x, y), names, font=font, fill='#dfd3ac')
            crop = Image.open(row['image']).crop((0, 103, 120, 144))
            sheet.paste(crop.resize((360, 123), Image.Resampling.NEAREST), (x, y + 22))
        path = ROOT / f'{"Maria" if actor == 3 else "Xien"}_CONDITION_REVIEW_3x_DERIVED.png'
        sheet.save(path)
        checked_copy(path, ARCHIVE / path.name)
        sheets.append({'path': str(ARCHIVE / path.name), 'sha256': sha(path.read_bytes()),
                       'derived_review_not_unmodified_capture': True})
    save(ARCHIVE / 'provenance.json', {
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
        'report': proof['report'], 'report_sha256': proof['report_sha256'],
        'screenshots': screenshots, 'derived_review_sheets': sheets,
        'RAM_snapshots_retained_in_Generated_run': True,
        'synthetic_states_excluded_from_guide': True, 'publication_approved': False,
        'full_goal_complete': False, 'canonical_promoted': False,
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.iterdir()
                  if p.is_file() and p.name != 'provenance.json'}})
    entry = {
        'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
        'status': 'current_V636_conditions_verified_all18_plaque_entries_still_open',
        'all42_condition_combinations_on_Maria_and_Xien_actual_views': True,
        'complete_condition_fields': 168, 'complete_original_getter_skill_fields': 840,
        'source_reviewed_Sailor_Info_plaque_crops': 924,
        'all86_two_byte_fixture_replays_exact': True,
        'cursor_ring_explicitly_excluded_no_unqualified_full_frame_claim': True,
        'ROM_patch_registry_canonical_and_all_release_pointers_unchanged': True,
        'all18_original_plaques_incomplete_all22_scopes_retained': True,
        'other_characters_equipment_contexts_and_texture_approval_remain_open': True,
        'ordinary_miniature_Confirm_village_legacy_movie_material_gates_remain_open': True,
        'archive': str(ARCHIVE), 'unmodified_synthetic_captures': len(screenshots),
        'synthetic_captures_excluded_from_guide': True,
        'full_goal_complete': False, 'canonical_promoted': False,
    }
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = read(ROOT / 'audit_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert all(data[k] == v for k, v in before[name].items()
                   if k not in (AUDIT_KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[AUDIT_KEY] = entry
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        current = read(path)
        assert all(current[k] == v for k, v in before[name].items()
                   if k not in (AUDIT_KEY, 'current_goal_turn_classification'))
        assert current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    heading = '## V637: current-ROM health/mood matrix and Sailor Info plaques'
    addition = '''

One fresh38600-frame V636 cold boot verifies all42 Health/Mood combinations on
both Maria and Xien:84 views,168 complete48x16 condition fields,840 complete60x12
skill fields checked against original getter values, and924 full source-reviewed
plaque/header crops697872 pixels. All86 isolated two-byte fixtures replay exactly.
Original condition-dependent skill changes are verified rather than ignored;
only the declared272-pixel equipment selection ring is excluded from context
equality. Other7322272 context pixels match; no unqualified whole-frame claim.
All84 unmodified synthetic captures and derived review sheets are archived on E,
excluded from guide acquisition evidence. No ROM/patch/registry/save or release
pointer changes; V636 remains the current compiled experimental candidate.
All18 plaque/hint objects remain incomplete and all22 historical scopes exact.
Texture approval, other owners/equipment contexts and the wider graphics gates
remain open. Full goal active. See [V637 checkpoint](condition_matrix_v637_checkpoint.md).
'''
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n' + addition, encoding='utf-8')
    print('Archived84 unmodified condition captures and2 derived review sheets; added evidence to3 audits; all18/22 scopes and release pointers preserved.')


if __name__ == '__main__':
    main()
