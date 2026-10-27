"""Independent native input, development, dialogue and complete Town screen checks."""

import argparse
import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import (
    SJIS_GLYPH_COUNT,
    SJIS_MAP_OFFSET,
    GameAsciiFont,
    decode_glyph,
)
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.village_portrait_wrap import paragraph
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_village_town_v665 import replay
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.probe_worldmap_overlays_v638 import color5
from scripts.run_village_development_v665 import PREVIOUS, ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_regional_ui_v616 import full_cells, glyphs
from scripts.verify_town_scene_v644 import rgb5
from scripts.verify_village_visits_v664 import CARDS, artifact, dialog, fixture, menu, model
from scripts.verify_village_wrap_v608 import read, save


def confirmation(image, rom, font, answer):
    arm = rom.read_file('/__arm9__.bin')
    table = common_message_entries(rom.read_file('/COMMON/MESFILE.DK4'), arm, clean=False)
    entry = next(e for e in table if e.message_id == 296)
    assert entry.text == b'\x82hs %s all right?'
    mapping = struct.unpack_from(f'<{SJIS_GLYPH_COUNT}H', arm, SJIS_MAP_OFFSET)
    code = int.from_bytes('Ｉ'.encode('cp932'), 'big')
    slot = mapping.index(code)
    mask = decode_glyph(rom.read_file('/GRP/KANJI.FNT'), slot)
    leading = {(16 + x, 296 + y) for y in range(11) for x in range(12) if mask.getpixel((x, y))}
    expected = leading | {(28 + x, 296 + y) for x, y in glyphs(font, 's ' + answer + ' all right?')}
    actual = {(x, y) for y in range(296, 344) for x in range(16, 240)
              if image.getpixel((x, y)) == (0, 8, 0)}
    assert actual == expected and len(leading) == 9
    assert actual - leading != expected
    return {'COMMON_ID': 296, 'actual_source_template_hex': entry.text.hex(),
            'English': 'Is ' + answer + ' all right?', 'source_fullwidth_I_glyph_index': slot,
            'complete_first_I_pixels': len(leading), 'first_I_native_deletion_control_rejected': True,
            'whole224x48_foreground_and_blank_cells_exact': True,
            'fullwidth_leading_I_and_remaining_ASCII_are_distinct_native_fonts_not_missing_letter': True}


def current_clue(image, font, text, index):
    lines = [s.strip() for s in paragraph(text).split('\n')]
    if index not in (4, 23):
        return dialog(image, font, text, 22 if len(lines) > 1 else 16)
    # Explicitly preserve this failing alignment result, rather than crediting
    # the different origins as a correct final layout. All lettering is present.
    assert len(lines) == 2 and len(lines[0]) == 36
    origins = (16, 22)
    masks = [full_cells(image, font, line, origins[i], 296 + i * 16, (0, 8, 0))
             for i, line in enumerate(lines)]
    expected = {(origins[i] + x, 296 + i * 16 + y)
                for i, line in enumerate(lines) for x, y in glyphs(font, line)}
    actual = {(x, y) for y in range(296, 344) for x in range(16, 240)
              if image.getpixel((x, y)) == (0, 8, 0)}
    assert actual == expected
    return {'paragraph': text, 'complete_lines': masks,
        'whole224x48_foreground_and_blank_cells_exact': True,
        'alignment_defect': 'First line starts at16; continuation starts at22',
        'six_pixel_indent_difference_requires_repair': True,
        'all_letters_present_not_a_missing_leading_character': True}


def check(index, rom, pre):
    tag = 'reapproach' if index in (2, 5, 7, 8, 10, 14, 22, 23) else 'first'
    folder = CAP / f'village_development_v665_{index:02d}_{tag}'
    rp = folder / 'capture_report.json'
    r, controller = read(rp), read(folder / 'controller_progress.json')
    assert controller['error'] is None
    assert controller['controller_source_sha256'] == sha(Path('scripts/run_village_development_v665.py').read_bytes())
    phases = controller['phases']
    assert r['ROM_sha256'] == pre['candidate_sha256'] and r['frames'] == phases['developed_town_return']
    assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
    assert r['battery_save_preloaded']['source_sha256'] == pre['donor_sha256']
    assert r['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert not any(v for k, v in r.items() if k.startswith('synthetic_') and k != 'synthetic_location_fixtures')
    assert r['core_DLL_sha256'] == sha(Path('work/emulation_v193/desmume_libretro.dll').read_bytes())
    journal = read(folder / 'navigation_command_journal.json')
    assert [{'frame': x['frame'], 'command': x['command']} for x in journal['commands_received']] == controller['commands']
    assert all(x['validation_passed'] for x in journal['commands_received'])
    assert controller['commands'][-1] == {'frame': r['frames'], 'command': {'stop': True}}
    initial_file = PREVIOUS / ('inputs_Ezo_chief.json' if index == 18 else f'inputs_chief_{index:02d}.json')
    schedule = read(initial_file)
    for row in controller['commands']:
        cmd = row['command']
        if cmd.get('buttons') or cmd.get('touch') is not None:
            ev = {'start': row['frame'] + 1, 'duration': cmd['duration'], 'buttons': cmd.get('buttons', [])}
            if cmd.get('touch') is not None:
                ev['touch'] = cmd['touch']
            schedule.append(ev)
    assert schedule == r['scripted_input_schedule']
    shots, snapshots = {}, {}
    for s in r['frames_captured']:
        assert sha(Path(s['path']).read_bytes()) == s['PNG_sha256']
        if s['frame'] in shots:
            assert s['PNG_sha256'] == shots[s['frame']]['PNG_sha256']
        shots[s['frame']] = s
    for row in r['read_only_pause_RAM_snapshots']:
        data = artifact(row)
        assert len(data) == 0x400000 and row['read_only_export']
        snapshots[row['frame']] = row
    def raw(frame):
        return Path(snapshots[frame]['path']).read_bytes()
    def image(frame):
        return Image.open(shots[frame]['path']).convert('RGB')
    arm, font = rom.read_file('/__arm9__.bin'), GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin'))
    assert len(r['synthetic_location_fixtures']) == (2 if index == 18 or tag == 'reapproach' else 1)
    for f in r['synthetic_location_fixtures']:
        fixture(arm, raw(f['frame']), f, index, f['frame'])
    old = read(PREVIOUS / 'proof.json')['reports']['Ezo_chief' if index == 18 else f'chief_{index:02d}']
    prefix = read(old['path'])
    assert all(s['PNG_sha256'] == shots[s['frame']]['PNG_sha256'] for s in prefix['frames_captured'])
    retained_first = None
    if tag != 'first':
        first_path = CAP / f'village_development_v665_{index:02d}_first/capture_report.json'
        first = read(first_path)
        assert first['cold_boot'] and not first['savestate_loaded'] and not first['callback_errors']
        assert first['ROM_sha256'] == pre['candidate_sha256']
        shared_end = phases.get('missed_return_before_reapproach', first['frames'])
        shared = []
        for s in first['frames_captured']:
            assert sha(Path(s['path']).read_bytes()) == s['PNG_sha256']
            if s['frame'] <= shared_end:
                assert s['PNG_sha256'] == shots[s['frame']]['PNG_sha256']
                shared.append(s['frame'])
        for s in first['read_only_pause_RAM_snapshots']:
            artifact(s)
        retained_first = {'path': str(first_path), 'sha256': sha(first_path.read_bytes()),
            'frames': first['frames'], 'capture_records': len(first['frames_captured']),
            'unique_captured_frames': len({s['frame'] for s in first['frames_captured']}),
            'exact_shared_prefix_frames': shared, 'no_Town_screen_credit_for_this_first_attempt': True}
    texts = read('translations/village_promised_words_manuscript_v1.json')['records']
    answer = next(t['english'] for t in texts if t['kind'] == 'ANSWER' and t['index'] == index)
    clue = next(t['english'] for t in texts if t['kind'] == 'CLUE' and t['index'] == index)
    notice = next(t['english'] for t in texts if t['kind'] == 'MESSAGE' and t['index'] == 2)
    name = next(t['english'] for t in read('translations/village_ui_manuscript_v1.json')['records']
                if t['kind'] == 'name' and t['index'] == index)
    marker = read('work/analysis/village_promised_words_plan.json')['keyboard_wrapper']['provider_vtable']
    assert len(controller['entered_character_states']) == len(answer) + 1
    entered = []
    for i, state in enumerate(controller['entered_character_states']):
        data, p = raw(state['frame']), state['parent'] - BASE
        assert state['RAM_sha256'] == sha(data) and state['entry'] == answer[:i]
        assert struct.unpack_from('<I', data, p + 4)[0] == marker
        assert struct.unpack_from('<I', data, p + 0x78)[0] == i
        assert struct.unpack_from('<I', data, p + 0xD8)[0] == 18
        assert data[p + 0xB4:p + 0xB4 + i + 1] == answer[:i].encode('ascii') + b'\0'
        im = image(state['frame'])
        actual = {(x, y) for y in range(11) for x in range(108)
                  if im.getpixel((60 + x, 244 + y)) == (230, 230, 230)}
        assert actual == glyphs(font, answer[:i])
        entered.append(state)
    clue_text = 'They say it means ' + clue + '.'
    dialogs = {'confirmation': confirmation(image(phases['answer_confirmation']), rom, font, answer),
        'clue': current_clue(image(phases['accepted_clue']), font, clue_text, index),
        'facilities': dialog(image(phases['facilities_notice']), font, notice, 22)}
    menu_rows = read(PREVIOUS / 'proof.json')['all24_original_native_menu_filter_cases'][index]['complete_English_choices'][:-1]
    developed_menu = menu(image(phases['developed_village_menu']), font, menu_rows)
    states = []
    for phase in ('chief_request', 'complete_password_before_submission', 'answer_confirmation',
                  'accepted_clue', 'developed_village_menu', 'developed_town_return'):
        value = model(arm, raw(phases[phase]), index, name, 1)
        assert value['native_development'] == (0 if phase in
            ('chief_request', 'complete_password_before_submission', 'answer_confirmation') else 2)
        states.append({'phase': phase, 'frame': phases[phase], **value})
    data = artifact(r['read_only_RAM_snapshot'])
    assert data == raw(r['frames'])
    native = r['read_only_native_state']
    artifact(native)
    for row in native['regions'].values():
        artifact(row)
    io, lcdm, dtcm, itcm = [Path(native['regions'][k]['path']).read_bytes() for k in ('9REG', 'LCDM', 'DTCM', 'ITCM')]
    final = image(r['frames'])
    execution = None
    if index != 9:
        upper, lower, execution = replay(rom, data, io, lcdm, dtcm, itcm)
        expected = [[color5(final.getpixel((x, y + sy))) for y in range(192) for x in range(256)] for sy in (0, 192)]
        assert [rgb5(upper), rgb5(lower)] == expected
        assert upper == lcdm[0x40000:0x58000] and lower == lcdm[0x60000:0x78000]
    u = machine(arm)
    u.mem_write(BASE, data)
    call(u, 0xCB178, ())
    town = u.reg_read(UC_ARM_REG_R0) + 4 + (90 + index) * 108
    call(u, 0xB5630, (town,))
    town_name_pointer = u.reg_read(UC_ARM_REG_R0)
    town_name = bytes(u.mem_read(town_name_pointer, 64)).split(b'\0')[0].decode('ascii')
    call(u, 0xB5690, (town,))
    meta = u.reg_read(UC_ARM_REG_R0)
    assert struct.unpack('<I', u.mem_read(meta, 4))[0] == town_name_pointer
    call(u, 0xB7294, (90 + index, 0))
    bg = f'/towngrp/towngrp{u.reg_read(UC_ARM_REG_R0):02d}.pxl'
    blob = rom.read_file(bg)
    assert blob == NdsImage.open('work/clean.nds').read_file(bg)
    resident = data.find(blob) >= 0
    header, specialty_proof = None, None
    if index != 9:
        header = find_mask(font, town_name, final, (0, 10, 256, 40))
        assert resident
        cache = struct.unpack_from('<6I', data, 0x15DC24)
        assert cache[5] == 1 and BASE <= cache[0] < BASE + len(data) - 64
        specialty = data[cache[0] - BASE:cache[0] - BASE + 64].split(b'\0')[0].decode('ascii')
        specialty_ink = glyphs(font, specialty, 5)
        actual_ink = {(x, y) for y in range(12) for x in range(96)
                      if final.getpixel((160 + x, 88 + y)) == (230, 230, 230)}
        assert specialty_ink == actual_ink and specialty_ink
        edge_controls = []
        for pos in (0, len(specialty) - 1):
            edge = {(pos * 5 + x, y) for x, y in glyphs(font, specialty[pos])}
            assert edge and edge <= actual_ink and actual_ink - edge != specialty_ink
            edge_controls.append({'index': pos, 'letter': specialty[pos], 'ink_removed': len(edge), 'rejected': True})
        specialty_proof = {'English': specialty, 'actual_cached_name_pointer': cache[0],
            'whole96x12_foreground_and_blank_cells_exact': True, 'first_final_letter_controls': edge_controls}
    absence = []
    for phase in ('complete_password_before_submission', 'answer_confirmation', 'accepted_clue',
                  'facilities_notice', 'developed_village_menu', 'departure', 'return_docking_prompt', 'developed_town_return'):
        data = raw(phases[phase])
        assert all(data.find(rom.read_file(f'/evstill/evstill{card:03d}.pxl')) < 0 for card in CARDS)
        absence.append({'phase': phase, 'frame': phases[phase], 'no_complete_eight_card_files_in_this_RAM_snapshot': True})
    ROOT.joinpath('cases').mkdir(exist_ok=True)
    native_replay = None
    if execution is not None:
        save(ROOT / f'cases/native_town_{index:02d}.json', execution)
        native_replay = {'path': str(ROOT / f'cases/native_town_{index:02d}.json'),
                         'sha256': sha((ROOT / f'cases/native_town_{index:02d}.json').read_bytes())}
    result = {'index': index, 'village_name': name, 'answer': answer, 'phases': phases,
        'report': {'path': str(rp), 'sha256': sha(rp.read_bytes()), 'frames': r['frames'],
                   'capture_records': len(r['frames_captured']), 'unique_captured_frames': len(shots)},
        'retained_original_return_attempt': retained_first,
        'controller': {'path': str(folder / 'controller_progress.json'),
                       'sha256': sha((folder / 'controller_progress.json').read_bytes())},
        'all_entered_character_prefixes_native_buffer_cursor_capacity_and_complete_display_verified': entered,
        'complete_dialogue_fields': dialogs, 'complete_developed_menu': developed_menu,
        'native_development_states': states,
        'entire_both_intended_Town_native_scenes98304_pixels_repainted_over_poison_match_capture': index != 9,
        'native_Town_replay': native_replay, 'complete_actual_Town_header': header,
        'Karibib_original_encounter_interrupts_return_actual_Town_screen_still_open': index == 9,
        'actual_Town_name': town_name, 'actual_Town_name_pointer': town_name_pointer,
        'actual_Town_metadata_name_field': meta, 'Town_name_matches_locked_village_name': town_name == name,
        'complete_actual_specialty_name': specialty_proof,
        'intended_Town_native_selected_backdrop_file': bg, 'complete_resident_intended_backdrop_source_exact_clean': resident,
        'sampled_card_file_absence_not_unused_proof': absence,
        'coordinate_fixtures_only_no_password_or_development_injection': True,
        'verifier_sha256': sha(Path(__file__).read_bytes())}
    save(ROOT / f'cases/village_{index:02d}.json', result)
    label = header['text'] if header is not None else 'not credited: original Karibib encounter'
    print(f'V665 {index} {name}: typed {answer!r}; original0->2 acceptance; actual final header={label!r}.', flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--village', type=int)
    args = parser.parse_args()
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    rom = NdsImage.open(pre['candidate'])
    indices = [args.village] if args.village is not None else list(range(24))
    cases = [check(i, rom, pre) for i in indices]
    if args.village is not None:
        return
    defects = [c for c in cases if not c['Town_name_matches_locked_village_name']]
    assert [c['index'] for c in defects] == [6, 12, 16, 21, 22]
    sheets = []
    for group in range(6):
        canvas = Image.new('RGB', (4 * 512 + 40, 816), '#263238')
        draw = ImageDraw.Draw(canvas)
        for col, c in enumerate(cases[group * 4:group * 4 + 4]):
            folder = Path(c['report']['path']).parent
            draw.text((8 + col * 520, 8), f'{c["index"]:02d} {c["village_name"]} - LOCATION FIXTURE', fill='white')
            for row, phase in enumerate(('facilities_notice', 'developed_town_return')):
                image = Image.open(folder / f'frame_{c["phases"][phase]:06d}_navigation.png').convert('RGB')
                # Notice shows its lower screen; Town shows both screens at native size.
                if row == 0:
                    image = image.crop((0, 192, 256, 384)).resize((512, 384), Image.Resampling.NEAREST)
                else:
                    image = image.resize((256, 384), Image.Resampling.NEAREST)
                canvas.paste(image, (8 + col * 520, 30 + row * 400))
                if row == 1:
                    note = ('Return unverified: encounter' if c['index'] == 9 else
                            'Native full scene verified\nActual port label: ' + c['actual_Town_name'])
                    if not c['Town_name_matches_locked_village_name']:
                        note += '\nName repair required: ' + c['village_name']
                    if c['index'] in (4, 23):
                        note += '\nClue indentation repair required'
                    draw.multiline_text((280 + col * 520, 446), note, fill='white', spacing=8)
        path = ROOT / f'development_and_Town_sheet_{group + 1:02d}.png'
        canvas.save(path)
        sheets.append({'path': str(path), 'sha256': sha(path.read_bytes()), 'derived_not_native_screenshot': True})
    scripts = [Path(__file__), Path('scripts/run_village_development_v665.py'),
        Path('scripts/run_village_return_v665.py'), Path('scripts/run_village_story_v665.py'),
        Path('scripts/run_village_Karibib_escape_v665.py'), Path('scripts/native_village_town_v665.py'),
        Path('scripts/verify_village_visits_v664.py'), Path('scripts/verify_town_scene_v644.py'),
        Path('scripts/research_town_scene_v644.py'), Path('scripts/native_village_visits_v664.py')]
    save(ROOT / 'proof.json', {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'previous_goal_turn_classification': 'progress: V66424 complete initial village branches and archives',
        'current_goal_turn_classification': 'progress', 'all24_development_cases': cases,
        'five_existing_developed_port_name_discrepancies_require_repair': [{k: c[k] for k in
            ('index', 'village_name', 'actual_Town_name', 'actual_Town_name_pointer', 'actual_Town_metadata_name_field')}
            for c in defects], 'derived_sheets': sheets,
        'two_clue_alignment_defects_require_repair': [4, 23],
        'all24_original_acceptances_and23_actual_intended_returns_not_earned_travel': True,
        'all23_both_native_Town_screens2260992_pixels_verified': True,
        'Karibib_actual_Town_return_still_open_due_original_encounter': True,
        'all_eight_white_card_ordinary_display_contexts_still_open': True,
        'source_fullwidth_I_confirmation_is_complete_distinct_native_font_not_dropped_character': True,
        'ROM_patch_registry_release_pointers_unchanged': True,
        'all18_plaques_incomplete22_historical_scopes_retained': True,
        'scripts': {str(p): sha(p.read_bytes()) for p in scripts}, 'full_goal_complete': False})


if __name__ == '__main__':
    main()
