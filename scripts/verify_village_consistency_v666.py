"""Verify exact integration, preservation and complete repaired native displays."""

import argparse
import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.village_port_consistency import ALIASES, aligned_paragraph, transform
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.native_village_town_v665 import replay
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.probe_worldmap_overlays_v638 import color5
from scripts.run_village_consistency_v666 import INDICES, ROM, ROOT, relocate
from scripts.run_village_visits_v664 import CAP
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_regional_ui_v616 import full_cells, glyphs
from scripts.verify_town_scene_v644 import rgb5
from scripts.verify_village_development_v665 import confirmation
from scripts.verify_village_visits_v664 import artifact, dialog, menu, model
from scripts.verify_village_wrap_v608 import read, save


def static():
    oldpath = Path('out/all_routes_combined_v653_candidate.nds')
    old, new = NdsImage.open(oldpath), NdsImage.open(ROM)
    before = {p: d for _, p, d in old.iter_files()} | dict(old.iter_components())
    after = {p: d for _, p, d in new.iter_files()} | dict(new.iter_components())
    assert before.keys() == after.keys()
    assert [p for p in before if before[p] != after[p]] == ['/__arm9__.bin']
    target, changes = transform(before['/__arm9__.bin'])
    assert target == after['/__arm9__.bin']
    manifest, parent = read(ROM.with_suffix('.manifest.json')), read(oldpath.with_suffix('.manifest.json'))
    pre, stack = read(ROOT / 'preflight.json'), read('translations/release_stack.json')
    assert manifest['profile'] == pre['profile'] == 'all-routes-unified-v666'
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    restored = read('translations/release_stack.json')
    del restored['profiles']['all-routes-unified-v666']
    assert restored == pre['source_registry']
    assert len(stack['accepted_layers']) == 114 and stack['accepted_layers'] == pre['accepted_layers']
    assert manifest['batches'] == parent['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == parent['required_batches'] and all(manifest['checks'].values())
    assert manifest['base_sha256'] == parent['base_sha256'] == pre['canonical_baseline']['sha256']
    assert sha(Path(manifest['base_rom']).read_bytes()) == manifest['base_sha256']
    assert manifest['changed_paths'] == parent['changed_paths']
    inherited = read('work/analysis/region_boundaries_v640/preservation_proof.json')
    assert len(inherited['entries']) == 921 and inherited['all57_embedded_block_extents_exact']
    assert inherited['current921_format_palette_extent_checks']
    graphics = {p for p in before if p.lower().endswith(('.pxl', '.fls'))}
    assert len(graphics) == 675 and {e['path'] for e in inherited['entries']} == graphics
    assert all(before[p] == after[p] for p in graphics)
    clean = Path('work/clean.nds')
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch, rebuilt = ROM.with_suffix('.xdelta'), ROOT / 'all_routes_combined_v666_PATCH_RECONSTRUCTION.nds'
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, rebuilt)
    assert ROM.read_bytes() == rebuilt.read_bytes()
    save(ROOT / 'static_release_proof.json', {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'profile': manifest['profile'],
        'manifest_sha256': sha(ROM.with_suffix('.manifest.json').read_bytes()), 'ARM9_sha256': sha(target),
        'patch_sha256': sha(patch.read_bytes()), 'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
        'transform': changes, 'all921_views675_files57_embedded_extents_and_all_other_components_exact_V653': True,
        'all470_batches114_accepted_layers_and_all_prior_profiles_retained': True,
        'exact_clean_patch_reconstruction': True, 'reconstructed_ROM': str(rebuilt),
        'canonical_promoted': False, 'full_goal_complete': False})
    print('V666 static integration, seven scoped repairs, complete preservation and clean patch reconstruction pass.', flush=True)


def aligned_clue(image, font, text):
    lines = [line.strip() for line in aligned_paragraph(text).splitlines()]
    assert len(lines) == 2 and all(len(line) <= 35 for line in lines)
    origin = 22
    fields = [full_cells(image, font, line, origin, 296 + row * 16, (0, 8, 0))
              for row, line in enumerate(lines)]
    expected = {(origin + x, 296 + row * 16 + y) for row, line in enumerate(lines)
                for x, y in glyphs(font, line)}
    actual = {(x, y) for y in range(296, 344) for x in range(16, 240)
              if image.getpixel((x, y)) == (0, 8, 0)}
    assert actual == expected
    controls = []
    for row, line in enumerate(lines):
        for pos in (0, len(line) - 1):
            edge = {(origin + pos * 6 + x, 296 + row * 16 + y) for x, y in glyphs(font, line[pos])}
            assert edge and edge <= actual and actual - edge != expected
            controls.append({'row': row, 'index': pos, 'letter': line[pos], 'removed_ink': len(edge), 'rejected': True})
    return {'paragraph': text, 'lines': fields, 'all_row_origins': [22, 22],
        'whole224x48_foreground_including_blank_cells_exact': True, 'first_final_deletion_controls': controls}


def check(index):
    static_proof = read(ROOT / 'static_release_proof.json')
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    folder = CAP / f'village_consistency_v666_{index:02d}'
    report_path = folder / 'capture_report.json'
    r, c = read(report_path), read(folder / 'controller_progress.json')
    phases = c['phases']
    assert c['error'] is None and r['frames'] == phases['developed_town_return']
    assert r['ROM_sha256'] == static_proof['candidate_sha256']
    assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
    donor = read('work/analysis/village_development_v665/preflight.json')
    assert r['battery_save_preloaded']['source_sha256'] == donor['donor_sha256']
    assert r['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert r['core_DLL_sha256'] == sha(Path('work/emulation_v193/desmume_libretro.dll').read_bytes())
    assert not any(v for k, v in r.items() if k.startswith('synthetic_') and k != 'synthetic_location_fixtures')
    assert not r['hardware_device_verification'] and not r['normal_travel_verified']
    shots, snapshots = {}, {}
    for s in r['frames_captured']:
        assert sha(Path(s['path']).read_bytes()) == s['PNG_sha256']
        if s['frame'] in shots:
            assert shots[s['frame']]['PNG_sha256'] == s['PNG_sha256']
        shots[s['frame']] = s
    for row in r['read_only_pause_RAM_snapshots']:
        assert row['read_only_export'] and len(artifact(row)) == 0x400000
        snapshots[row['frame']] = row
    def raw(frame):
        return Path(snapshots[frame]['path']).read_bytes()
    def image(frame):
        return Image.open(shots[frame]['path']).convert('RGB')
    oldcase = read(f'work/analysis/village_development_v665/cases/village_{index:02d}.json')
    oldreport = read(oldcase['report']['path'])
    assert phases == oldcase['phases'] and r['scripted_input_schedule'] == oldreport['scripted_input_schedule']
    assert c['controller_source_sha256'] == sha(Path('scripts/run_village_development_v665.py').read_bytes())
    journal = read(folder / 'navigation_command_journal.json')['commands_received']
    assert all(x['validation_passed'] for x in journal)
    assert [{'frame': x['frame'], 'command': x['command']} for x in journal] == c['commands']
    assert c['commands'][-1] == {'frame': r['frames'], 'command': {'stop': True}}
    assert len(r['synthetic_location_fixtures']) == (2 if index in (22, 23) else 1)
    for recorded in r['synthetic_location_fixtures']:
        after, calculated = relocate(arm, raw(recorded['frame']), index)
        assert dict(calculated, frame=recorded['frame']) == recorded
        lo = calculated['active_ship'] - BASE + 16
        source_ram = raw(recorded['frame'])
        assert source_ram[:lo] == after[:lo] and source_ram[lo + 8:] == after[lo + 8:]
        point = calculated['expected_selector_point_after_original_update']
        assert any(q['map_point'] == point and q['collision_free'] for q in calculated['terrain_proof']['queries'])
        assert sum((x - y) ** 2 for x, y in zip(point, calculated['village_center'], strict=True)) < 32 ** 2
    names = read('translations/village_ui_manuscript_v1.json')['records']
    name = next(t['english'] for t in names if t['kind'] == 'name' and t['index'] == index)
    texts = read('translations/village_promised_words_manuscript_v1.json')['records']
    answer = next(t['english'] for t in texts if t['kind'] == 'ANSWER' and t['index'] == index)
    clue = next(t['english'] for t in texts if t['kind'] == 'CLUE' and t['index'] == index)
    assert len(c['entered_character_states']) == len(answer) + 1
    marker = read('work/analysis/village_promised_words_plan.json')['keyboard_wrapper']['provider_vtable']
    for i, state in enumerate(c['entered_character_states']):
        data, parent = raw(state['frame']), state['parent'] - BASE
        assert sha(data) == state['RAM_sha256'] and state['entry'] == answer[:i]
        assert struct.unpack_from('<I', data, parent + 4)[0] == marker
        assert struct.unpack_from('<I', data, parent + 0x78)[0] == i
        assert struct.unpack_from('<I', data, parent + 0xD8)[0] == 18
        assert data[parent + 0xB4:parent + 0xB4 + i + 1] == answer[:i].encode('ascii') + b'\0'
        im = image(state['frame'])
        assert {(x, y) for y in range(11) for x in range(108)
                if im.getpixel((60 + x, 244 + y)) == (230, 230, 230)} == glyphs(font, answer[:i])
    clue_text = 'They say it means ' + clue + '.'
    notice = next(t['english'] for t in texts if t['kind'] == 'MESSAGE' and t['index'] == 2)
    dialogs = {'confirmation': confirmation(image(phases['answer_confirmation']), rom, font, answer),
        'clue': aligned_clue(image(phases['accepted_clue']), font, clue_text) if index in (4, 23)
        else dialog(image(phases['accepted_clue']), font, clue_text,
                    22 if len(aligned_paragraph(clue_text).splitlines()) > 1 else 16),
        'facilities': dialog(image(phases['facilities_notice']), font, notice, 22)}
    labels = read('work/analysis/village_visits_v664/proof.json')['all24_original_native_menu_filter_cases'][index]['complete_English_choices'][:-1]
    menu_proof = menu(image(phases['developed_village_menu']), font, labels)
    states = []
    for phase in ('chief_request', 'answer_confirmation', 'accepted_clue', 'developed_town_return'):
        state = model(arm, raw(phases[phase]), index, name, 1)
        assert state['native_development'] == (0 if phase in ('chief_request', 'answer_confirmation') else 2)
        states.append({'phase': phase, **state})
    native = r['read_only_native_state']
    artifact(native)
    for row in native['regions'].values():
        artifact(row)
    data = artifact(r['read_only_RAM_snapshot'])
    assert data == raw(r['frames'])
    io, lcdm, dtcm, itcm = [Path(native['regions'][k]['path']).read_bytes() for k in ('9REG', 'LCDM', 'DTCM', 'ITCM')]
    upper, lower, execution = replay(rom, data, io, lcdm, dtcm, itcm)
    final = image(r['frames'])
    assert [rgb5(upper), rgb5(lower)] == [[color5(final.getpixel((x, y + sy)))
        for y in range(192) for x in range(256)] for sy in (0, 192)]
    assert upper == lcdm[0x40000:0x58000] and lower == lcdm[0x60000:0x78000]
    u = machine(arm)
    u.mem_write(BASE, data)
    call(u, 0xCB178, ())
    town = u.reg_read(UC_ARM_REG_R0) + 4 + (90 + index) * 108
    call(u, 0xB5630, (town,))
    pointer = u.reg_read(UC_ARM_REG_R0)
    assert bytes(u.mem_read(pointer, 64)).split(b'\0')[0].decode('ascii') == name
    if index in {a[0] for a in ALIASES}:
        assert pointer == next(a[3] for a in ALIASES if a[0] == index)
    header = find_mask(font, name, final, (0, 10, 256, 40))
    docking_frame = phases.get('reapproach_docking_prompt', phases['return_docking_prompt'])
    dialogs['developed_port_docking_prompt'] = dialog(image(docking_frame), font, 'Dock at ' + name + '?', 22)
    unchanged, altered = [], []
    for oldshot in oldreport['frames_captured']:
        frame = oldshot['frame']
        oldim, newim = Image.open(oldshot['path']).convert('RGB'), image(frame)
        assert sha(Path(oldshot['path']).read_bytes()) == oldshot['PNG_sha256']
        if oldim.tobytes() == newim.tobytes():
            unchanged.append(frame)
        else:
            altered.append(frame)
            if index in (4, 23) and frame == phases['accepted_clue']:
                allowed = (16, 296, 240, 344)
            elif index in {a[0] for a in ALIASES} and frame == phases['developed_town_return']:
                allowed = (0, 10, 256, 40)
            elif index in {a[0] for a in ALIASES} and frame == docking_frame:
                allowed = (16, 296, 240, 344)
            else:
                raise AssertionError((index, frame, 'unexpected screen difference'))
            assert all(oldim.getpixel((x, y)) == newim.getpixel((x, y))
                       for y in range(384) for x in range(256)
                       if not (allowed[0] <= x < allowed[2] and allowed[1] <= y < allowed[3]))
    assert set(altered) == ({phases['accepted_clue']} if index in (4, 23)
                            else {phases['developed_town_return'], docking_frame})
    ROOT.joinpath('cases').mkdir(exist_ok=True)
    save(ROOT / f'cases/native_town_{index:02d}.json', execution)
    result = {'index': index, 'name': name, 'answer': answer, 'phases': phases,
        'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
        'actual_Town_name_pointer': pointer, 'complete_header': header, 'complete_dialogues': dialogs,
        'complete_developed_menu': menu_proof, 'native_original_development_states': states,
        'typed_prefix_count': len(c['entered_character_states']), 'all_input_buffers_cursors_and_full_masks_pass': True,
        'both_complete_native_Town_screens98304_pixels_match': True,
        'unchanged_whole_two_screen_frames': sorted(set(unchanged)),
        'changed_frames_only_expected_field_all_other_pixels_exact': sorted(set(altered)),
        'coordinate_fixtures_no_earned_travel_claim': True, 'full_goal_complete': False}
    save(ROOT / f'cases/village_{index:02d}.json', result)
    print(f'V666 {index} {name}: actual header, full text, alignment and whole native screens pass.', flush=True)


def finish():
    proof = read(ROOT / 'static_release_proof.json')
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    cases = [read(ROOT / f'cases/village_{i:02d}.json') for i in INDICES]
    header_controls, reports = [], []
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    for case in cases:
        path = Path(case['report'])
        assert sha(path.read_bytes()) == case['report_sha256']
        r = read(path)
        assert r['ROM_sha256'] == proof['candidate_sha256']
        assert case['both_complete_native_Town_screens98304_pixels_match']
        assert case['all_input_buffers_cursors_and_full_masks_pass']
        final_path = path.parent / f"frame_{case['phases']['developed_town_return']:06d}_navigation.png"
        final = Image.open(final_path).convert('RGB')
        x, y = case['complete_header']['bounds'][:2]
        color = tuple(case['complete_header']['color'])
        full_cells(final, font, case['name'], x, y, color)
        for pos in (0, len(case['name']) - 1):
            mutated = final.copy()
            edge = {(x + pos * 6 + dx, y + dy) for dx, dy in glyphs(font, case['name'][pos])}
            assert edge and all(final.getpixel(p) == color for p in edge)
            for point in edge:
                mutated.putpixel(point, (255, 0, 255))
            try:
                full_cells(mutated, font, case['name'], x, y, color)
            except AssertionError:
                header_controls.append({'index': case['index'], 'letter_index': pos,
                    'letter': case['name'][pos], 'removed_ink': len(edge), 'rejected': True})
            else:
                raise AssertionError('Header checker accepted a deleted edge glyph')
        reports.append({'path': str(path), 'sha256': sha(path.read_bytes()),
            'frames': r['frames'], 'capture_records': len(r['frames_captured'])})
    # A fresh ordinary New Game must preserve title, selection, opening story and town UI.
    newpath = CAP / 'village_consistency_v666_newgame/capture_report.json'
    meta = read('work/analysis/queued_portrait_wrap_v653/initial_newgame_report.json')
    assert sha(Path(meta['path']).read_bytes()) == meta['sha256']
    old, new = read(meta['path']), read(newpath)
    assert old['frames'] == new['frames'] == 24100
    assert new['ROM_sha256'] == proof['candidate_sha256']
    assert new['cold_boot'] and not new['savestate_loaded'] and not new['callback_errors']
    assert not any(v for k, v in new.items() if k.startswith('synthetic_'))
    assert old['scripted_input_schedule'] == new['scripted_input_schedule']
    assert new['core_DLL_sha256'] == old['core_DLL_sha256'] == sha(Path('work/emulation_v193/desmume_libretro.dll').read_bytes())
    previous = {s['frame']: s for s in old['frames_captured']}
    matched = []
    for s in new['frames_captured']:
        assert sha(Path(s['path']).read_bytes()) == s['PNG_sha256']
        prior = previous[s['frame']]
        assert sha(Path(prior['path']).read_bytes()) == prior['PNG_sha256']
        assert Image.open(s['path']).convert('RGB').tobytes() == Image.open(prior['path']).convert('RGB').tobytes()
        matched.append(s['frame'])
    assert set(matched) == set(previous)
    reports.append({'path': str(newpath), 'sha256': sha(newpath.read_bytes()),
        'frames': new['frames'], 'capture_records': len(new['frames_captured'])})
    sheets = []
    for label, indices, phase, crop, scale in (
        ('five_names', (6, 12, 16, 21, 22), 'developed_town_return', (0, 8, 256, 44), 3),
        ('two_clues', (4, 23), 'accepted_clue', (0, 288, 256, 352), 3),
    ):
        height = (crop[3] - crop[1]) * scale
        sheet = Image.new('RGB', (1566, len(indices) * (height + 34)), '#263238')
        draw = ImageDraw.Draw(sheet)
        for row, i in enumerate(indices):
            case = next(c for c in cases if c['index'] == i)
            oldcase = read(f'work/analysis/village_development_v665/cases/village_{i:02d}.json')
            top = row * (height + 34)
            for col, entry, title in ((0, oldcase, 'V653 before'), (1, case, 'V666 corrected')):
                folder = Path(entry['report']['path'] if col == 0 else entry['report']).parent
                im = Image.open(folder / f"frame_{case['phases'][phase]:06d}_navigation.png").convert('RGB')
                draw.text((8 + col * 780, top + 4), f"{case['name']} - {title} - LOCATION FIXTURE", fill='white')
                sheet.paste(im.crop(crop).resize((768, height), Image.Resampling.NEAREST), (8 + col * 780, top + 26))
        target = ROOT / f'{label}_ACTUAL_COMPARISON.png'
        sheet.save(target)
        sheets.append({'path': str(target), 'sha256': sha(target.read_bytes()), 'derived_not_native_screenshot': True})
    failure = ROOT / 'retained_verifier_assumptions.json'
    save(failure, {
        'initial_verifier': 'initial_verifier_before_docking_name_check.py',
        'initial_verifier_sha256': sha((ROOT / 'initial_verifier_before_docking_name_check.py').read_bytes()),
        'failures': [{'village': 6, 'frame': 12540}, {'village': 12, 'frame': 12180}],
        'cause': 'Initial comparison omitted the shared Town getter docking prompts. The five data aliases correctly affect these prompts too.',
        'followup': 'Complete docking font fields and first/final controls pass; all surrounding pixels remain exact.',
        'ROM_changed_in_response_to_verifier_failure': False, 'full_goal_complete': False})
    save(ROOT / 'release_proof.json', {**proof, 'cases': cases, 'reports': reports,
        'all_seven_changed_contexts_cold_boot_verified': True,
        'all_five_Town_headers_and_shared_docking_prompts_use_approved_names': True,
        'both_reflowed_clues_complete_with_identical22_pixel_left_margins': True,
        'seven_both_native_Town_screens688128_pixels_exact': True,
        'whole_header_first_final_deletion_controls': header_controls,
        'newgame_whole_two_screen_frames_exact_V653': sorted(set(matched)),
        'village_unchanged_whole_two_screen_comparisons': sum(len(c['unchanged_whole_two_screen_frames']) for c in cases),
        'derived_comparison_sheets': sheets, 'verifier_sha256': sha(Path(__file__).read_bytes()),
        'Karibib_return_eight_white_cards_six_controls_and_other_graphics_gates_still_open': True,
        'all18_plaques_incomplete_and_all22_historical_scopes_retained': True,
        'current_goal_turn_classification': 'progress', 'full_goal_complete': False})
    print('V666 seven complete repairs and ordinary New Game regression verified; full graphics goal remains active.', flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--static', action='store_true')
    parser.add_argument('--finish', action='store_true')
    parser.add_argument('--village', type=int, choices=INDICES)
    args = parser.parse_args()
    if args.static:
        static()
    if args.village is not None:
        check(args.village)
    if args.finish:
        finish()


if __name__ == '__main__':
    main()
