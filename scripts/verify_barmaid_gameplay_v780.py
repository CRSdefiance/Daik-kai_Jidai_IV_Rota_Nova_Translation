"""Paired cold-boot samples; incomplete families receive no completion credit."""

import re
import struct
from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_barmaid_location_fixture_v780_v2 import relocate
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.verify_barmaid_scoped_layout_v780 import formatter
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_shipyard_gameplay_v760 import models, independent_font
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/barmaid_integration_v780')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
BODY, ADVANCE = (16, 294, 244, 366), (224, 360, 240, 376)


def load(folder):
    path = CAP/folder/'capture_report.json'
    report = read(path)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['hardware_device_verification'] and not report['goal_complete']
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    arm = NdsImage.open(report['ROM']).read_file('/__arm9__.bin')
    donor = report['battery_save_preloaded']
    assert donor['source'] != donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256'] == '05fa512b078fd01a8f6bee605254e9f72bfe3453c0ea098d977c87d86b6b693e'
    ram, frames = {}, {}
    for row in report.get('read_only_capture_RAM_snapshots', []) + report['read_only_pause_RAM_snapshots']:
        raw = Path(row['path']).read_bytes()
        assert row['read_only_export'] and len(raw) == row['bytes'] == 0x400000
        assert sha(raw) == row['sha256']
        if row['frame'] in ram:
            assert ram[row['frame']] == raw
        ram[row['frame']] = raw
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        frames[row['frame']] = row
    adapter = report['controlled_location_adapter']
    assert adapter['original_harness_file_unchanged']
    assert adapter['original_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
    assert adapter['adapter_sha256'] == sha(Path('scripts/run_barmaid_location_capture_v780_v2.py').read_bytes())
    assert adapter['fixture_producer_sha256'] == sha(Path('scripts/native_barmaid_location_fixture_v780_v2.py').read_bytes())
    assert adapter['single_import_replacement']
    assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_location_fixtures')
    assert len(report['synthetic_location_fixtures']) == 3
    for fixture in report['synthetic_location_fixtures']:
        assert fixture['town_id'] == 13
        _, expected = relocate(arm, ram[fixture['frame']], fixture['town_id'])
        assert fixture == dict(expected, frame=fixture['frame'])
    return path, report, arm, frames, ram


def main():
    pa, old, oa, before, old_ram = load('barmaid_v780_seville_baseline')
    pb, new, arm, after, new_ram = load('barmaid_v780_seville_pilot2')
    assert old['frames'] == new['frames'] == 37600
    assert old['scripted_input_schedule'] == new['scripted_input_schedule']
    assert old['core_options'] == new['core_options'] and before.keys() == after.keys()
    assert old_ram.keys() == new_ram.keys()
    selected = {35600: 989, 36000: 989}
    expected_args = {989: (b'Donna', b'Hodram')}
    rows = {r['message_id']: r for r in read('translations/barmaid_editorial_manuscript_v2.json')['records']}
    rom = NdsImage.open(new['ROM'])
    common = rom.read_file('/COMMON/MESFILE.DK4')
    entries = common_message_entries(common, arm, clean=False)
    blocks = IlnkContainer.parse(common).blocks
    p, w, owner = [struct.unpack_from('<I', arm, off)[0] for off in (0x5444C, 0x54450, 0x552A0)]
    run, _ = formatter()
    phases = {f: Image.open(before[f]['path']).convert('RGB').crop(ADVANCE).tobytes() for f in selected}
    holds, controls, states = [], [], []
    for f in sorted(after):
        a, b = [Image.open(fs[f]['path']).convert('RGB') for fs in (before, after)]
        diff = ImageChops.difference(a, b)
        if f not in selected:
            assert diff.getbbox() is None, (f, 'unselected full screen', diff.getbbox())
            controls.append(f)
            continue
        n, raw = selected[f], new_ram[f]
        assert cstring(raw, owner+0x2030) == entries[n].text
        assert raw.count(blocks[entries[n].block]) == 1
        pattern = b'(.*?)'.join(re.escape(part) for part in entries[n].text.split(b'%s'))
        match = re.fullmatch(pattern, cstring(raw, p))
        assert match and match.groups() == expected_args[n]
        args = match.groups()
        u = machine(arm)
        u.mem_write(BASE, raw)
        native = run(u, rows[n], args)
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
        assert matches, (f, 'unknown original advance phase')
        diff.paste((0, 0, 0), ADVANCE)
        diff.paste((0, 0, 0), BODY)
        assert diff.getbbox() is None, (f, 'outside text', diff.getbbox())
        holds.append({'frame': f, 'message_id': n, 'lines': native['lines'], 'arguments': [v.decode() for v in args],
                      'capture': after[f], 'complete_independent_font_and_blank_paper_exact': True,
                      'all_other_pixels_exact': True, 'original_advance_phase_matches': matches, 'observed_speaker': 'Donna'})
    for f in new_ram:
        assert state(oa, old_ram[f]) == state(arm, new_ram[f]), (f, 'state')
        assert models(oa, old_ram[f]) == models(arm, new_ram[f]), (f, 'models')
        assert persistent_objects(oa, old_ram[f]) == persistent_objects(arm, new_ram[f]), (f, 'objects')
        assert tasks(oa, old_ram[f]) == tasks(arm, new_ram[f]), (f, 'task records')
        states.append(f)
    save(ROOT/'seville_intro_gameplay_verification.json', {
        'candidate_sha256': new['ROM_sha256'], 'capture_reports': [str(pa), str(pb)],
        'holds': holds, 'whole_screen_controls': controls, 'paired_state_model_object_task_frames': states,
        'normal_town_return_frame': 37600, 'all_declared_coordinate_fixtures_reproduced_exactly': True,
        'no_normal_travel_earned_unlock_or_hardware_claim': True,
        'other_barmaid_families_pending': ['intro990', 'ordinary-chat', 'name-bearing-gift999', 'other-gift-responses', 'casual-chat'],
        'batch_completion_credit': False, 'full_goal_complete': False,
        'producer_sha256': sha(Path(__file__).read_bytes())})
    print(len(holds), 'complete intro holds;', len(controls), 'whole controls;', len(states), 'state/model/task pairs;other families pending.', flush=True)


if __name__ == '__main__':
    main()
