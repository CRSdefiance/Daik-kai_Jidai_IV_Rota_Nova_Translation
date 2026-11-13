"""First actual capacity-confirmation sample, its original controls and state."""

import re
import struct
from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.register_shared_release_v782 import MANUSCRIPT, ROOT
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_port_gameplay_v762 import capture, cstring
from scripts.verify_shipyard_gameplay_v760 import independent_font, models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import read, save

BODY, ADVANCE = (16, 294, 244, 366), (224, 360, 240, 376)


def load(folder):
    path, report, arm, frames = capture(folder)
    assert report['frames'] == 8800
    assert report['battery_save_preloaded']['source_sha256'] == 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    ram = {}
    for row in report.get('read_only_capture_RAM_snapshots', [])+report['read_only_pause_RAM_snapshots']:
        raw = Path(row['path']).read_bytes()
        assert len(raw) == row['bytes'] == 0x400000 and row['read_only_export']
        assert sha(raw) == row['sha256']
        if row['frame'] in ram:
            assert ram[row['frame']] == raw
        ram[row['frame']] = raw
    return path, report, arm, frames, ram


def main():
    pa, old, oa, before, old_ram = load('shared_v782_recruit_baseline')
    pb, new, arm, after, new_ram = load('shared_v782_recruit_live')
    assert old['scripted_input_schedule'] == new['scripted_input_schedule'] and old['core_options'] == new['core_options']
    assert before.keys() == after.keys() and old_ram.keys() == new_ram.keys()
    pc, blink, unused_arm, blink_frames = capture('shared_v782_recruit_highlight_baseline')
    assert blink['frames'] == old['frames'] and blink['core_options'] == old['core_options']
    assert blink['scripted_input_schedule'] == old['scripted_input_schedule']
    assert blink['ROM_sha256'] == old['ROM_sha256']
    for f in (3200, 5200, 5600, 6000, 6400, 6800, 7200, 7600, 8400, 8800):
        assert Image.open(blink_frames[f]['path']).convert('RGB').tobytes() == Image.open(before[f]['path']).convert('RGB').tobytes()
    rom = NdsImage.open(new['ROM'])
    common = rom.read_file('/COMMON/MESFILE.DK4')
    entries = common_message_entries(common, arm, clean=False)
    blocks = IlnkContainer.parse(common).blocks
    rows = {r['message_id']: r for r in read(MANUSCRIPT)['records']}
    p, w, owner = [struct.unpack_from('<I', arm, off)[0] for off in (0x5444C, 0x54450, 0x552A0)]
    source = (ROOT/'full_entry_format_case.py').read_text(encoding='utf-8')
    env = {**original.__dict__, 're': re}
    exec(compile(source, str(ROOT/'full_entry_format_case.py'), 'exec'), env)
    selected = {6800: 1042, 7200: 1042}
    phases = {f: Image.open(before[f]['path']).convert('RGB').crop(ADVANCE).tobytes() for f in selected}
    holds, controls, states, blink_controls = [], [], [], []
    for f in sorted(after):
        a, b = [Image.open(fs[f]['path']).convert('RGB') for fs in (before, after)]
        diff = ImageChops.difference(a, b)
        if f not in selected:
            if f == 8000:
                # Only this observed blink discrepancy may use a different frame.
                # Compare the entire screen to actual original-build captures,
                # including the unchanged confirmation,portrait and ship row.
                matches = [k for k, row in blink_frames.items() if 7900 <= k <= 8000
                           and Image.open(row['path']).convert('RGB').tobytes() == b.tobytes()]
                assert matches, (f, 'no complete original blink phase matches')
                blink_controls.append({'frame': f, 'complete_whole_frame_matches_original_control_frames': matches,
                                       'capture_report': str(pc), 'no_rectangular_pixel_exclusion': True})
                continue
            assert diff.getbbox() is None, (f, 'unselected full screen', diff.getbbox())
            controls.append(f)
            continue
        n, raw = selected[f], new_ram[f]
        assert cstring(raw, owner+0x2030) == entries[n].text
        assert raw.count(blocks[entries[n].block]) == 1
        pattern = b'(.*?)'.join(re.escape(part) for part in entries[n].text.split(b'%s'))
        match = re.fullmatch(pattern, cstring(raw, p))
        assert match and match.groups() == ('５１'.encode('cp932'),)
        args = match.groups()
        u = machine(arm)
        u.mem_write(BASE, raw)
        native = env['format_case'](u, rows[n], args)
        assert not native['findings']
        formatted = bytes.fromhex(native['formatted_hex'])
        assert formatted == cstring(raw, w)
        plane = raster(arm, formatted, 0x01FFCE40-BASE, size=(228, 64), instruction_limit=1000000)
        assert plane == independent_font(arm, rom.read_file('/GRP/KANJI.FNT'), native['lines'])
        expected = {(16+i%228, 296+i//228) for i, v in enumerate(plane) if v == 1}
        actual = {(x, y) for y in range(BODY[1], BODY[3]) for x in range(BODY[0], BODY[2]) if b.getpixel((x, y)) == (0, 8, 0)}
        assert expected == actual, (f, len(expected-actual), len(actual-expected))
        previous = {(x, y) for y in range(BODY[1], BODY[3]) for x in range(BODY[0], BODY[2]) if a.getpixel((x, y)) == (0, 8, 0)}
        glyphs = expected | previous
        shadows = {(x+1, y+1) for x, y in glyphs}
        unexpected = [(x, y) for y in range(BODY[1], BODY[3]) for x in range(BODY[0], BODY[2])
                      if not (ADVANCE[0] <= x < ADVANCE[2] and ADVANCE[1] <= y < ADVANCE[3])
                      and (x, y) not in glyphs | shadows and a.getpixel((x, y)) != b.getpixel((x, y))]
        assert not unexpected, (f, unexpected[:10])
        matches = [k for k, v in phases.items() if v == b.crop(ADVANCE).tobytes()]
        assert matches
        diff.paste((0, 0, 0), ADVANCE)
        diff.paste((0, 0, 0), BODY)
        assert diff.getbbox() is None, (f, 'outside text', diff.getbbox())
        holds.append({'frame': f, 'message_id': n, 'lines': native['lines'], 'arguments': [v.decode('cp932') for v in args],
                      'capture': after[f], 'complete_independent_font_and_blank_paper_exact': True,
                      'all_other_pixels_exact': True, 'original_advance_phase_matches': matches,
                      'observed_speaker': 'Charles Rochefort'})
    for f in new_ram:
        assert state(oa, old_ram[f]) == state(arm, new_ram[f]), (f, 'state')
        assert models(oa, old_ram[f]) == models(arm, new_ram[f]), (f, 'models')
        assert persistent_objects(oa, old_ram[f]) == persistent_objects(arm, new_ram[f]), (f, 'objects')
        assert tasks(oa, old_ram[f]) == tasks(arm, new_ram[f]), (f, 'tasks')
        states.append(f)
    save(ROOT/'recruit_capacity_gameplay_verification.json', {
        'candidate_sha256': new['ROM_sha256'], 'capture_reports': [str(pa), str(pb)], 'holds': holds,
        'whole_screen_controls': controls, 'paired_state_model_object_task_frames': states,
        'original_whole_screen_blink_phase_controls': blink_controls,
        'original_positive_capacity_count_and_cancellation_then_assign_sailors_flow_verified': True,
        'normal_town_return_frame': 8800, 'no_test_fixture_or_earned_unlock_claim': True,
        'other_shared_families_pending': ['information1020', 'warning1021-1027', 'village1028-1029',
                                          'fleet1030-1034', 'required-shortfall1035-1041', 'private1049-1069'],
        'batch_completion_credit': False, 'full_goal_complete': False, 'producer_sha256': sha(Path(__file__).read_bytes())})
    print(f'{len(holds)} complete1042 holds,{len(controls)} whole-screen controls,{len(states)} state/model/task pairs and town return pass. Other families pending.', flush=True)


if __name__ == '__main__':
    main()
