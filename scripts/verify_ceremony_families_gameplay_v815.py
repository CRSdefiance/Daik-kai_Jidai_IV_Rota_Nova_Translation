"""Source-scoped actual site/Temple/Church scenes and paired original outcomes."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.ceremony_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_ceremony_family_fixture_v815 import set_condition
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_ceremony_consumers_v808 import production_functions
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
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
MODAL = (289, 290, 291, 293, 294, 295)


def load(folder, terminal, donor_sha, requests):
    path = CAP/folder/'capture_report.json'; report = read(path)
    assert report['frames'] == terminal and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['hardware_device_verification']
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    donor = report['battery_save_preloaded']
    assert donor['source'] != donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256'] == donor_sha
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
    receipts = []
    for frame, role, day in requests:
        _, receipt = set_condition(arm, ram[frame], dict(mode='ceremony-family', facility=role, day=day))
        receipts.append(dict(frame=frame, **receipt))
    assert report.get('synthetic_condition_fixtures', []) == json.loads(json.dumps(receipts))
    return path, report, rom, arm, frames, ram


def verify(spec):
    op, old, orom, oarm, of, oram = load(spec['old'], spec['terminal'], spec['donor'], spec['requests'])
    np, new, rom, arm, nf, nram = load(spec['new'], spec['terminal'], spec['donor'], spec['requests'])
    assert old['scripted_input_schedule'] == new['scripted_input_schedule']
    assert old['core_options'] == new['core_options'] and set(of) == set(nf)
    common = rom.read_file('/COMMON/MESFILE.DK4'); entries = current_entries(common, arm)
    blocks = IlnkContainer.parse(common).blocks
    rows = {r['message_id']: r for r in read('translations/ceremony_editorial_manuscript_v3.json')['records']}
    ordinary, modal, ordinary_source, modal_source = production_functions()
    owner, printed, wrapped = [struct.unpack_from('<I', arm, n)[0] for n in (0x552A0, 0x5444C, 0x54450)]
    selected = {f: (n, tuple(v.encode('ascii') for v in values)) for f, n, values in spec['holds']}
    holds = []; controls = []; outside = []
    for frame in sorted(nf):
        before = Image.open(of[frame]['path']).convert('RGB')
        after = Image.open(nf[frame]['path']).convert('RGB')
        diff = ImageChops.difference(before, after)
        if frame not in selected:
            assert diff.getbbox() is None, (spec['name'], frame, diff.getbbox())
            controls.append(dict(frame=frame, both_complete_screens_exact=True))
            continue
        number, values = selected[frame]; raw = nram[frame]
        assert cstring(raw, owner+0x2030) == entries[number].text
        assert raw.count(blocks[entries[number].block]) == 1
        case = (modal if number in MODAL else ordinary)(prepared(arm), rows[number], values)
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
        outside.append(dict(frame=frame, original_portrait_speaker_UI_and_every_outside_pixel_exact=True))
        holds.append(dict(frame=frame, message_id=number, arguments=[v.decode('ascii') for v in values],
            lines=case['lines'], capture=nf[frame], complete_native_and_independent_font_exact=True,
            complete_leading_trailing_letters_bounds_margins_and_blank_paper_pass=True,
            real_parent_printf_wrapped_buffer_and_resident_block_exact=True))
    states = []
    for frame in sorted(nram):
        for fn in (state, models, persistent_objects, tasks):
            assert fn(oarm, oram[frame]) == fn(arm, nram[frame]), (spec['name'], frame, fn.__name__)
        assert calendar(oarm, oram[frame]) == calendar(arm, nram[frame])
        states.append(dict(frame=frame, calendar=calendar(arm, nram[frame]),
            financial_state=state(arm, nram[frame]),
            original_all_actor_town_item_goods_model_task_funds_state_equal_baseline=True))
    indexed = {r['frame']: r for r in states}
    for before, after, ticks in spec['time_pairs']:
        assert indexed[after]['calendar']['ticks']-indexed[before]['calendar']['ticks'] == ticks
    save(ROOT/(spec['name']+'_gameplay_verification_v815.json'), dict(candidate=new['ROM'],
        candidate_sha256=new['ROM_sha256'], specification=spec, capture_reports=[str(op), str(np)],
        complete_scene_holds=holds, full_screen_controls=controls, outside_body_controls=outside,
        original_state_pairs=states, original_time_increments_verified=spec['time_pairs'],
        no_unexpected_pages_and_original_returns_and_outcomes_equal_paired_baseline=True,
        fixture_scope='Only explicit calendar/facility words; normal scenes and effects. Natural campaign access not claimed.',
        ordinary_formatter_sha256=sha(ordinary_source.encode()), modal_formatter_sha256=sha(modal_source.encode()),
        producer_sha256=sha(Path(__file__).read_bytes()), other_ceremony_families_pending=True,
        new_editorial_completion_credit=0, full_goal_complete=False))
    print(f"{spec['name']}: {len(holds)} complete actual glyph holds, {len(controls)} full-screen controls, {len(states)} state pairs pass.", flush=True)


SPECS = [dict(name='site_chant', new='ceremony_v809_temple_work', old='ceremony_v803_site_chant_control',
    terminal=8600, donor='e5beeb4e4be5ecab1ee5312daab1bc81bc9904c5f4b6de45004d401356d8113b',
    requests=[(3200, 9, 24), (7000, 9, 24)], time_pairs=[(3800, 7000, 192)],
    holds=[(3800, 1219, ['Cappadocia']), (4200, 1220, []), (4600, 1203, []), (5000, 1222, []),
           (5400, 1223, []), (5800, 1225, []), (6200, 1208, []), (6600, 290, ['Hodram'])]),
    dict(name='temple_preparations', new='ceremony_v809_temple_preparations', old='ceremony_v803_temple_preparations_control',
    terminal=13200, donor=read('E:/Rota Nova translations/Saves/Test fixtures/V815 Temple day24 isolated setup.fixture.json')['sha256'],
    requests=[(10200, 9, 24), (11600, 10, 24)], time_pairs=[(3800, 7800, 48), (10800, 11600, 0)],
    holds=[(3800, 1201, []), (4200, 1210, []), (4600, 1212, []), (5000, 1215, []),
           (5400, 1216, []), (5800, 291, ['Hodram']), (10800, 1201, [])]),
    dict(name='church_prayer', new='ceremony_v809_church_prayer', old='ceremony_v803_church_prayer_control',
    terminal=7200, donor=read('E:/Rota Nova translations/Saves/Test fixtures/V815 Church day24 isolated setup.fixture.json')['sha256'],
    requests=[(5800, 10, 24)], time_pairs=[(3800, 5000, 48), (6400, 7200, 0)],
    holds=[(3800, 1200, []), (4200, 1202, []), (4600, 289, []), (5400, 1218, []),
           (6400, 1200, []), (6800, 1218, [])])]


if __name__ == '__main__':
    for spec in SPECS:
        verify(spec)
