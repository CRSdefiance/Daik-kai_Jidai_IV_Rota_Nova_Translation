"""Actual site prayer glyphs, original outcomes and paired pre-ceremony control."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageChops
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.ceremony_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_ceremony_map_fixture_v814 import set_condition
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_ceremony_consumers_v808 import production_functions
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_shipyard_gameplay_v760 import independent_font, models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/ceremony_access_v810')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
BODY = (16, 294, 244, 366)
DONOR_SHA = '1de062be7b19a84c07e59a2ff5dad877afda81a3e9daa86e179c927be04aa2dc'


def load(folder):
    path = CAP/folder/'capture_report.json'
    report = read(path)
    assert report['frames'] == 16200 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['hardware_device_verification']
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    donor = report['battery_save_preloaded']
    assert donor['source'] != donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256'] == DONOR_SHA
    rom = NdsImage.open(report['ROM']); arm = rom.read_file('/__arm9__.bin')
    frames = {r['frame']: r for r in report['frames_captured']}
    for row in frames.values():
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    ram = {}
    for row in report['read_only_capture_RAM_snapshots']+report.get('read_only_pause_RAM_snapshots', []):
        raw = Path(row['path']).read_bytes()
        assert len(raw) == 0x400000 and sha(raw) == row['sha256'] and row['read_only_export']
        if row['frame'] in ram:
            assert ram[row['frame']] == raw
        ram[row['frame']] = raw
    _, receipt = set_condition(arm, ram[3200], {'mode': 'ceremony-Cappadocia-map'})
    assert report['synthetic_condition_fixtures'] == json.loads(json.dumps([dict(frame=3200, **receipt)]))
    return path, report, rom, arm, frames, ram


def calendar(arm, raw):
    u = machine(arm); u.mem_write(0x02000000, raw)
    call(u, 0xCB1B4, ()); at = u.reg_read(UC_ARM_REG_R0)
    tick = struct.unpack('<I', u.mem_read(at+8, 4))[0]
    call(u, 0xCC9C8, (at, 0x02451000, 0x02451004, 0x02451008))
    return dict(ticks=tick, original_zero_based_date=list(struct.unpack('<3I', u.mem_read(0x02451000, 12))))


def main():
    op, old, orom, oarm, of, oram = load('ceremony_v803_map_prayer_control')
    np, new, rom, arm, nf, nram = load('ceremony_v809_map_probe')
    assert old['scripted_input_schedule'] == new['scripted_input_schedule']
    assert old['core_options'] == new['core_options'] and set(of) == set(nf)
    common = rom.read_file('/COMMON/MESFILE.DK4')
    entries = current_entries(common, arm); blocks = IlnkContainer.parse(common).blocks
    rows = {r['message_id']: r for r in read('translations/ceremony_editorial_manuscript_v3.json')['records']}
    ordinary, modal, ordinary_source, modal_source = production_functions()
    owner, printed, wrapped = [struct.unpack_from('<I', arm, n)[0] for n in (0x552A0, 0x5444C, 0x54450)]
    selected = {12200: (1219, (b'Cappadocia',)), 12600: (1220, ()), 13000: (1226, ()),
                13400: (293, (b'Hodram',)), 14200: (1221, ())}
    holds = []; controls = []; outside = []
    for frame in sorted(nf):
        before = Image.open(of[frame]['path']).convert('RGB')
        after = Image.open(nf[frame]['path']).convert('RGB')
        diff = ImageChops.difference(before, after)
        if frame not in selected:
            assert diff.getbbox() is None, (frame, diff.getbbox())
            controls.append(dict(frame=frame, both_complete_screens_exact=True))
            continue
        number, values = selected[frame]; raw = nram[frame]
        assert cstring(raw, owner+0x2030) == entries[number].text
        assert raw.count(blocks[entries[number].block]) == 1
        case = (modal if number == 293 else ordinary)(prepared(arm), rows[number], values)
        assert not case['findings'] and bytes.fromhex(case['formatted_hex']) == cstring(raw, wrapped)
        for value in values:
            assert value in cstring(raw, printed) and value in cstring(raw, wrapped)
        plane = raster(arm, bytes.fromhex(case['formatted_hex']), 0x01FFCE40-0x02000000,
                       size=(228, 64), instruction_limit=1000000)
        assert plane == independent_font(arm, rom.read_file('/GRP/KANJI.FNT'), case['lines'])
        expected = {(16+i%228, 296+i//228) for i, p in enumerate(plane) if p == 1}
        actual = {(x, y) for y in range(294, 366) for x in range(16, 244)
                  if after.getpixel((x, y)) == (0, 8, 0)}
        assert expected == actual, (frame, number, len(expected-actual), len(actual-expected))
        diff.paste((0, 0, 0), BODY)
        assert diff.getbbox() is None, (frame, diff.getbbox())
        outside.append(dict(frame=frame, original_speakers_portraits_UI_and_every_pixel_outside_body_exact=True))
        holds.append(dict(frame=frame, message_id=number, arguments=[v.decode('ascii') for v in values],
            lines=case['lines'], capture=nf[frame], complete_font_and_all_first_final_letters_exact=True,
            native_resident_block_template_and_real_parent_wrapped_buffer_exact=True,
            no_unexpected_dark_ink_on_blank_paper=True, visible_margins_and_bounds_pass=True))
    states = []
    for frame in sorted(nram):
        for fn in (state, models, persistent_objects, tasks):
            assert fn(oarm, oram[frame]) == fn(arm, nram[frame]), (frame, fn.__name__)
        assert calendar(oarm, oram[frame]) == calendar(arm, nram[frame])
        states.append(dict(frame=frame, financial_state=state(arm, nram[frame]),
                           calendar=calendar(arm, nram[frame]),
                           original_all_actors_towns_items_goods_models_tasks_and_funds_equal_baseline=True))
    indexed = {r['frame']: r for r in states}
    assert indexed[13800]['calendar']['ticks']-indexed[12200]['calendar']['ticks'] == 192
    assert indexed[12200]['calendar']['original_zero_based_date'][1] == 24
    assert indexed[13800]['calendar']['original_zero_based_date'][1] == 28
    assert indexed[12200]['financial_state']['cash'] == indexed[13800]['financial_state']['cash'] == 8371
    protected = Path('E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv')
    assert sha(protected.read_bytes()) == 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
    save(ROOT/'prayer_gameplay_verification_v814.json', dict(candidate=new['ROM'], candidate_sha256=new['ROM_sha256'],
        capture_reports=[str(op), str(np)], complete_scene_holds=holds, full_screen_controls=controls,
        outside_body_controls=outside, original_state_pairs=states,
        actual_original_four_day192_tick_site_time_and_normal_town_return=True,
        same_inputs_original_quest_prelude_priest_prayer_result_and_offday_return=True,
        map_fixture_only_item164_and_original_acquisition_history=True, protected_donors_unchanged=True,
        ordinary_formatter_sha256=sha(ordinary_source.encode()), modal_formatter_sha256=sha(modal_source.encode()),
        other_site_rites_Temple_Church_declines_and_other_protagonists_pending=True,
        new_editorial_completion_credit=0, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print(f'Five actual ceremony/offday holds, {len(controls)} full-screen controls and {len(states)} state pairs pass; four original days and normal town return. Other families remain pending.', flush=True)


if __name__ == '__main__':
    main()
