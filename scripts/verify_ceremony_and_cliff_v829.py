"""Last actual Lil ceremony variant, corrected cliff scene and ordinary boot."""

import json
import struct
from pathlib import Path

from PIL import Image,ImageChops

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.levelup_stat_format import current_entries
from dk4tool.rom.nds import NdsImage
from scripts.native_ceremony_map_fixture_v828 import set_condition as map_condition
from scripts.native_ceremony_istanbul_fixture_v827 import set_condition as access_condition
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_ceremony_consumers_v808 import production_functions
from scripts.verify_ceremony_heroes_v825 import cstring,identity
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_levelup_gameplay_v819 import glyphs
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/cliff_editorial_v829')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def capture(name):
    folder = CAP/name
    report = read(folder/'capture_report.json')
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['goal_complete'] and not report['hardware_device_verification']
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    rom = NdsImage.open(report['ROM'])
    assert sha(rom.source.read_bytes()) == report['ROM_sha256']
    frames = {r['frame']:r for r in report['frames_captured']}
    snapshots = {r['frame']:r for r in report.get('read_only_pause_RAM_snapshots',[])}
    def raw_at(frame):
        row = snapshots[frame]
        raw = Path(row['path']).read_bytes()
        assert len(raw) == 0x400000 and sha(raw) == row['sha256'] and row['read_only_export']
        return raw
    def picture(frame):
        row = frames[frame]
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        return Image.open(row['path']).convert('RGB')
    donor = report.get('battery_save_preloaded')
    if donor:
        assert 'disposable' in donor['source'].lower() and donor['source'] != donor['destination']
        assert donor['copied_byte_exact_before_cold_boot'] and sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    return report,rom,frames,raw_at,picture


def zero_origin_glyphs(arm,font,picture,encoded,lines):
    plane = raster(arm,encoded,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=1000000)
    expected = independent_font(arm,font,lines)
    expected = b''.join(expected[y*228+6:(y+1)*228]+bytes(6) for y in range(64))
    assert plane == expected
    ink = {(16+i%228,296+i//228) for i,p in enumerate(plane) if p == 1}
    actual = {(x,y) for y in range(294,366) for x in range(16,244) if picture.getpixel((x,y)) == (0,8,0)}
    assert ink == actual,(len(ink-actual),len(actual-ink),lines)


def main():
    release = read(ROOT/'registered_binary_and_patch_verification.json')
    report,rom,frames,raw_at,picture = capture('ceremony_Lil_map_and_chant_v828')
    assert report['frames'] == 19400 and report['source_map_fixture_adapter_v828']['no_captain_dialogue_source_code_random_state_or_quest_fixture_available']
    arm,common,font = [rom.read_file(p) for p in ('/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT')]
    entries = current_entries(common,arm)
    blocks = IlnkContainer.parse(common).blocks
    for receipt in report['synthetic_condition_fixtures']:
        frame = receipt['frame']
        request = {'mode':'ceremony-Cappadocia-map'} if frame == 4000 else {'mode':'ceremony-Istanbul','facility':11,'day':24}
        after,expected = map_condition(arm,raw_at(frame),request)
        expected['frame'] = frame
        assert json.loads(json.dumps(expected)) == receipt
        assert identity(arm,after) == identity(arm,raw_at(frame))
    assert [r['frame'] for r in report['synthetic_condition_fixtures']] == [4000,12400]
    rows = {r['message_id']:r for r in read('translations/ceremony_editorial_manuscript_v3.json')['records']}
    ordinary,modal,_,_ = production_functions()
    printed,wrapped,owner = [struct.unpack_from('<I',arm,n)[0] for n in (0x5444C,0x54450,0x552A0)]
    holds = []
    for i,number in enumerate((1219,1220,1203,1222,1224,1225,1209,290)):
        frame = 13200+400*i
        raw = raw_at(frame)
        who = identity(arm,raw)
        assert who['captain'] == 2 and who['notice_name'] == 'Lil' and who['town'] == who['fleet_town'] == 22
        values = (b'Cappadocia',) if number == 1219 else (b'Lil',) if number == 290 else ()
        case = (modal if number == 290 else ordinary)(prepared(arm),rows[number],values)
        assert not case['findings']
        encoded = bytes.fromhex(case['formatted_hex'])
        assert cstring(raw,wrapped) == encoded and cstring(raw,owner+0x2030) == entries[number].text
        assert raw.count(blocks[entries[number].block]) == 1
        for value in values:
            assert value in cstring(raw,printed) and value in encoded
        glyphs(arm,font,picture(frame),encoded,case['lines'])
        holds.append(dict(frame=frame,message_id=number,lines=case['lines'],capture=frames[frame],
            original_actual_Lil_portrait_and_native_selected_template_variables_and_block_exact=True,
            complete_native_independent_and_actual_ink_blank_plane_alignment_bounds_and_all_letters=True))
    assert calendar(arm,raw_at(17200))['ticks']-calendar(arm,raw_at(13200))['ticks'] == 192
    assert identity(arm,raw_at(17200))['captain'] == 2
    header = cstring(raw_at(16400),wrapped)
    assert header == b'Lil leveled up!!'
    zero_origin_glyphs(arm,font,picture(16400),header,[header.decode()])
    stats = cstring(raw_at(16800),wrapped)
    stat_lines = [s.strip().decode('cp932') for s in stats.split(b'\n')]
    assert stat_lines == ['Wits increased by ２!']
    glyphs(arm,font,picture(16800),stats,stat_lines)
    prior = set(read('translations/editorial_review_current_v1.json')['actual_ceremony_preparations_v827']['cumulative_distinct_actual_family_IDs'])
    covered = prior | {r['message_id'] for r in holds}
    assert len(covered) == 52 and covered-prior == {1224}
    save(ROOT/'last_Lil_ceremony_variant_v828.json',dict(candidate=report['ROM'],candidate_sha256=report['ROM_sha256'],
        complete_scene_holds=holds,extra_growth_holds=[dict(frame=f,capture=frames[f]) for f in (16400,16800)],
        map164_source_bound_original_transfer_receipt_exact=True,calendar_access_receipt_exact=True,
        no_captain_script_dialogue_random_state_or_quest_mutation_supplied=True,
        original_four_day192_tick_return_and_actual_town_return_verified=True,
        cumulative_distinct_actual_family_IDs=sorted(covered),new_actual_variant_IDs=[1224],
        ceremony_source_ROM_bytes_and_native_code_exact_in_V829=True,
        full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    # Actual corrected record and every adjacent dialogue hold through town return.
    report,new,frames,raw_at,picture = capture('cliff_editorial_v829_actual')
    assert report['frames'] == 11400 and report['ROM_sha256'] == release['candidate_sha256']
    assert new.read_file('/__arm9__.bin') == arm and new.read_file('/COMMON/MESFILE.DK4') == common
    block = IlnkContainer.parse(new.read_file('/data/SC2.DK4')).blocks[294]
    assert len(report['synthetic_condition_fixtures']) == 1
    after,receipt = access_condition(arm,raw_at(4000),dict(mode='ceremony-Istanbul',facility=11,day=24))
    receipt['frame'] = 4000
    assert json.loads(json.dumps(receipt)) == report['synthetic_condition_fixtures'][0]
    assert identity(arm,after) == identity(arm,raw_at(4000))
    scene_holds = []
    for frame,record in ((9800,73),(10200,76),(10600,80),(11000,84)):
        raw = raw_at(frame)
        source = block.split(b'\0')[record]
        encoded = cstring(raw,wrapped)
        assert encoded == source[1:] and raw.count(block) == 1
        assert source[0] == (2 if record == 80 else 0x94)
        lines = [s.strip().decode('cp932') for s in encoded.split(b'\n')]
        zero_origin_glyphs(arm,font,picture(frame),encoded,lines)
        assert identity(arm,raw)['captain'] == 2
        scene_holds.append(dict(frame=frame,SC2_block=294,record=record,lines=lines,capture=frames[frame],
            whole_native_independent_actual_font_and_blank_plane_exact=True,
            original_Guildmaster_or_Lil_portrait_caption_and_control_byte_exact=True,
            first_and_last_letters_all_rows_left_aligned_at_native_x16=True))
    assert scene_holds[0]['lines'] == ["You're set on it, huh? Just",'for you, then.']
    assert calendar(arm,raw_at(4000)) == calendar(arm,raw_at(11400))
    assert identity(arm,raw_at(11400))['town'] == 22
    save(ROOT/'actual_cliff_scene_and_transition_verification.json',dict(candidate_sha256=release['candidate_sha256'],
        complete_holds=scene_holds,original94_body_reaches_original_native_consumer=True,
        single_A_after_repaired_line_reaches_original_next_record_no_blank_page=True,
        original_town_return_and_calendar_preserved=True,no_savestate_or_dialogue_fixture=True,
        full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    # Unmodified startup input schedule, no cartridge save and no runtime fixtures.
    old = read(CAP/'levelup_v820_registered_newgame_matching_options'/'capture_report.json')
    new = read(CAP/'cliff_v829_ordinary_newgame'/'capture_report.json')
    assert old['core_options'] == new['core_options'] and old['scripted_input_schedule'] == new['scripted_input_schedule']
    assert new['cold_boot'] and not new['savestate_loaded'] and not new.get('battery_save_preloaded') and not new['callback_errors']
    assert not any(value for key,value in new.items() if key.startswith('synthetic_'))
    before = {r['frame']:r for r in old['frames_captured']}
    after = {r['frame']:r for r in new['frames_captured']}
    assert set(before) == set(after) == {1,60,180,1600,2000,3200,4000}
    pairs = []
    for frame,row in after.items():
        assert ImageChops.difference(Image.open(row['path']).convert('RGB'),Image.open(before[frame]['path']).convert('RGB')).getbbox() is None
        pairs.append(dict(frame=frame,capture=row,complete_two_screen_frame_exact_to_V820=True))
    save(ROOT/'ordinary_New_Game_verification.json',dict(candidate_sha256=release['candidate_sha256'],
        seven_complete_frame_pairs=pairs,no_save_savestate_or_runtime_fixture=True,
        original_full_input_schedule_and_core_options_exact=True,hardware_or_full_route_verification=False))
    print('PASS:last1224 and8 full ceremony holds,2 growth holds;corrected cliff+3 next holds aligned;7 ordinary startup frames.',flush=True)


if __name__ == '__main__':
    main()
