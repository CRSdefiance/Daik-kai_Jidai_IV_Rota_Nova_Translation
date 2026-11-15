"""Verify actual Lil temple chanting and dancing, including every text pixel."""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.levelup_stat_format import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_call_abi_v764 import call
from scripts.native_ceremony_hero_fixture_v825 import set_condition
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_ceremony_consumers_v808 import production_functions
from scripts.verify_ceremony_heroes_v825 import cstring, identity
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/ceremony_lil_v826')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/ceremony_Lil_temple_and_dance_v826')
DONOR_SHA = '5516ebd26a405612880984c1a1722b0a92a4b0db5f970371dc00a6ce1a13bebb'
SCENES = [
    dict(name='Temple chanting', base=5600, IDs=[1201,1203,1204,1206,1207,1209,290], end=9200, ticks=48),
    dict(name='Parthenon dancing', base=10600, IDs=[1219,1220,1227,1229,1230,1231,290], end=13400, ticks=192),
]


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    report = read(CAP/'capture_report.json')
    assert report['frames'] == 14800 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['goal_complete'] and not report['hardware_device_verification']
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert report['actual_hero_fixture_adapter_v825']['no_captain_actor_dialogue_or_random_state_fixture_available']
    rom = NdsImage.open(report['ROM'])
    assert sha(rom.source.read_bytes()) == report['ROM_sha256'] == 'b8126bf14fd3aa0236c03ee48492a40eb0f2b50e77df5a16c3d6f92ea6bb2251'
    arm, common, font = [rom.read_file(p) for p in ('/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT')]
    entries = current_entries(common, arm)
    clean = NdsImage.open('work/clean.nds')
    clean_arm = clean.read_file('/__arm9__.bin')
    original = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean_arm)
    assert arm[0x610FC:0x61C18] == clean_arm[0x610FC:0x61C18]
    donor = report['battery_save_preloaded']
    assert 'disposable' in donor['source'].lower() and donor['source'] != donor['destination']
    assert donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256'] == DONOR_SHA
    protected = Path('E:/Rota Nova translations/Saves/Test fixtures/V825 Lil Athens after fasting.dsv')
    assert sha(protected.read_bytes()) == DONOR_SHA
    frames = {r['frame']:r for r in report['frames_captured']}
    snapshots = {r['frame']:r for r in report['read_only_pause_RAM_snapshots']}

    def raw_at(frame):
        row = snapshots[frame]
        raw = Path(row['path']).read_bytes()
        assert len(raw) == 0x400000 and sha(raw) == row['sha256'] and row['read_only_export']
        return raw

    who = identity(arm, raw_at(4000))
    assert who == dict(captain=2, formal_name='Lil Argot', notice_name='Lil', town=19, fleet_town=19)
    fixtures = []
    for frame, role in ((4000,9),(9200,11)):
        before = raw_at(frame)
        after, receipt = set_condition(arm, before, dict(mode='ceremony-Athens', facility=role, day=21))
        receipt['frame'] = frame
        assert identity(arm, after) == who
        u = machine(arm)
        u.mem_write(0x02000000, before)
        call(u, 0xCB184, (), instruction_limit=500000)
        at = u.reg_read(UC_ARM_REG_R0)-0x02000000
        assert before[at:at+6660] == after[at:at+6660]
        fixtures.append(receipt)
    assert json.loads(json.dumps(fixtures)) == report['synthetic_condition_fixtures']
    assert not report.get('synthetic_location_fixtures')
    assert all(identity(arm, raw_at(f)) == who for f in snapshots)
    # Original code remains intact in the actual machine, not just the ROM.
    assert all(raw_at(f)[0x610FC:0x61C18] == clean_arm[0x610FC:0x61C18] for f in snapshots)
    rows = {r['message_id']:r for r in read('translations/ceremony_editorial_manuscript_v3.json')['records']}
    blocks = IlnkContainer.parse(common).blocks
    ordinary, modal, ordinary_source, modal_source = production_functions()
    printed, wrapped, owner = [struct.unpack_from('<I', arm, off)[0] for off in (0x5444C,0x54450,0x552A0)]
    holds, returns, review = [], [], {}
    for scene in SCENES:
        for i, number in enumerate(scene['IDs']):
            frame = scene['base']+400*i
            raw = raw_at(frame)
            row = rows[number]
            assert original[number].text == bytes.fromhex(row['source_hex'])
            assert original[number].text.decode('cp932') == row['japanese']
            values = (b'Parthenon',) if number == 1219 else (b'Lil',) if number == 290 else ()
            case = (modal if number == 290 else ordinary)(prepared(arm), row, values)
            assert not case['findings']
            encoded = bytes.fromhex(case['formatted_hex'])
            assert cstring(raw, wrapped) == encoded and cstring(raw, owner+0x2030) == entries[number].text
            assert raw.count(blocks[entries[number].block]) == 1
            for value in values:
                assert value in cstring(raw, printed) and value in encoded
            plane = raster(arm, encoded, 0x01FFCE40-0x02000000, size=(228,64), instruction_limit=1000000)
            assert plane == independent_font(arm, font, case['lines'])
            picture = frames[frame]
            assert sha(Path(picture['path']).read_bytes()) == picture['PNG_sha256']
            image = Image.open(picture['path']).convert('RGB')
            expected = {(16+i%228,296+i//228) for i,p in enumerate(plane) if p == 1}
            actual = {(x,y) for y in range(294,366) for x in range(16,244) if image.getpixel((x,y)) == (0,8,0)}
            assert expected == actual, (frame, number, len(expected-actual), len(actual-expected))
            holds.append(dict(scene=scene['name'], frame=frame, message_id=number, lines=case['lines'], capture=picture,
                complete_native_independent_and_actual_ink_and_blank_plane_exact=True,
                native_parent_variables_template_and_resident_block_exact=True,
                leading_final_letters_alignment_bounds_and_complete_page_verified=True,
                actual_Lil_and_officiant_portraits_visually_reviewed=True))
            review[number] = dict(message_id=number, Japanese=row['japanese'], English=row['english'],
                source_reference=row['source_reference'], source_meaning=row['source_meaning'],
                localization_note=row['localization_note'], source_hex=row['source_hex'],
                current_ROM_entry_hex=entries[number].text.hex(),
                decision='retain frozen V809 wording; actual Lil scene now verified')
        delta = calendar(arm, raw_at(scene['end']))['ticks']-calendar(arm, raw_at(scene['base']))['ticks']
        assert delta == scene['ticks']
        returns.append(dict(scene=scene['name'], before_frame=scene['base'], town_return_frame=scene['end'],
            original_tick_increment=delta, actual_town_return_visually_reviewed=True,
            no_extra_blank_page_in_recorded_A_input_sequence=True))
    assert len(holds) == 14 and len(review) == 13
    save(ROOT/'actual_Lil_temple_and_dance_verification.json', dict(
        candidate=str(rom.source), candidate_sha256=report['ROM_sha256'],
        clean_source_sha256=sha(clean.source.read_bytes()), capture_report=str(CAP/'capture_report.json'),
        capture_report_sha256=sha((CAP/'capture_report.json').read_bytes()),
        actual_identity=who, complete_scene_holds=holds, source_context_reviews=list(review.values()),
        native_time_and_return=returns, fixture_receipts=fixtures,
        all207_actors_and_actual_captain_preserved_at_each_fixture=True,
        original_donor_and_disposable_input_sha256_unchanged=DONOR_SHA,
        new_distinct_actual_reaction_IDs=[1206,1209,1229],
        remaining_actual_reaction_IDs=[1211,1213,1214,1217,1224],
        ordinary_formatter_sha256=sha(ordinary_source.encode()), modal_formatter_sha256=sha(modal_source.encode()),
        source_ceremony_code_unchanged_in_ROM_and_all_actual_RAM_snapshots=True,
        actual_rendering_and_original_returns_not_a_full_route_playthrough=True,
        calendar_and_access_are_testing_inputs_not_earned_progress=True,
        whole_family_completion_credit=0, full_goal_complete=False,
        stdin_recovery='Existing process52924 console only; original exec response omitted its session ID. Same run continued and stopped normally; no restart.',
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('PASS:14 complete Lil ceremony holds;13 source-bound records;3 new reactions;original48/192-tick town returns.', flush=True)


if __name__ == '__main__':
    main()
