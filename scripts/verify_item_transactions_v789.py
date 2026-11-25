"""Actual transaction glyphs,blank paper,original screens and economic outcomes."""

import re
import struct
from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import item_diplomacy_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_shipyard_gameplay_v760 import independent_font, models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/item_transactions_v789')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
BODY, ADVANCE = (16, 294, 244, 366), (224, 360, 240, 376)
SELECTED = {7200: 1071, 8000: 1073, 8400: 1071, 9200: 1073, 9600: 1074,
            10000: 1071, 11600: 1085, 12400: 1086, 12800: 1085, 13600: 1086, 14000: 1096}


def load(folder):
    path = CAP/folder/'capture_report.json'
    report = read(path)
    assert report['frames'] == 15600 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['hardware_device_verification'] and not report['goal_complete']
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    donor = report['battery_save_preloaded']
    assert donor['source'] != donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256'] == '942c74828a7b7396f7567ca2d405ddc4cdd329e4837f591777d35ee458794b0f'
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    frames, ram = {}, {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        frames[row['frame']] = row
    for row in report.get('read_only_capture_RAM_snapshots', [])+report.get('read_only_pause_RAM_snapshots', []):
        raw = Path(row['path']).read_bytes()
        assert len(raw) == row['bytes'] == 0x400000 and row['read_only_export'] and sha(raw) == row['sha256']
        if row['frame'] in ram: assert ram[row['frame']] == raw
        ram[row['frame']] = raw
    rom = NdsImage.open(report['ROM'])
    return path, report, rom, frames, ram


def main():
    pa, old, old_rom, before, old_ram = load('item_transactions_v789_baseline')
    pb, new, rom, after, new_ram = load('item_transactions_v789_live')
    assert old['scripted_input_schedule'] == new['scripted_input_schedule'] and old['core_options'] == new['core_options']
    assert set(before) == set(after)
    arm, oa = rom.read_file('/__arm9__.bin'), old_rom.read_file('/__arm9__.bin')
    common = rom.read_file('/COMMON/MESFILE.DK4')
    entries = owned.current_entries(common, arm)
    old_entries = common_message_entries(old_rom.read_file('/COMMON/MESFILE.DK4'), oa, clean=False)
    blocks = IlnkContainer.parse(common).blocks
    rows = {r['message_id']: r for r in read('translations/item_diplomacy_editorial_manuscript_v2.json')['records']}
    program = Path('work/analysis/item_diplomacy_integration_v788/production_layout/effective_format_case.py').read_text(encoding='utf-8')
    from scripts.probe_item_production_v788 import native_parent
    env = {**original.__dict__, 'native_parent': native_parent}
    exec(compile(program, '<verified original-entry formatter>', 'exec'), env)
    p, w, owner = [struct.unpack_from('<I', arm, off)[0] for off in (0x5444C, 0x54450, 0x552A0)]
    holds, controls, states = [], [], []
    for f in sorted(after):
        a, b = [Image.open(fs[f]['path']).convert('RGB') for fs in (before, after)]
        diff = ImageChops.difference(a, b)
        if f not in SELECTED:
            assert diff.getbbox() is None, (f, 'unselected full screen', diff.getbbox())
            controls.append(f)
            continue
        n, raw = SELECTED[f], new_ram[f]
        assert cstring(raw, owner+0x2030) == entries[n].text
        assert cstring(old_ram[f], owner+0x2030) == old_entries[n].text
        assert raw.count(blocks[entries[n].block]) == 1
        match = re.fullmatch(b'(.*?)'.join(re.escape(part) for part in entries[n].text.split(b'%s')), cstring(raw, p))
        assert match
        args = match.groups()
        assert len(args) == len(rows[n]['source_native_arguments'])
        old_match = re.fullmatch(b'(.*?)'.join(re.escape(part) for part in old_entries[n].text.split(b'%s')), cstring(old_ram[f], p))
        assert old_match and old_match.groups() == args
        expected_number = 7700 if n == 1073 else 6160 if n == 1086 else None
        if expected_number is not None: assert args == (str(expected_number).translate(str.maketrans('0123456789','０１２３４５６７８９')).encode('cp932'),)
        case = env['format_case'](machine(arm), rows[n], args)
        assert not case['findings'] and bytes.fromhex(case['formatted_hex']) == cstring(raw, w)
        plane = raster(arm, bytes.fromhex(case['formatted_hex']), 0x01FFCE40-BASE, size=(228,64), instruction_limit=1000000)
        assert plane == independent_font(arm, rom.read_file('/GRP/KANJI.FNT'), case['lines'])
        expected = {(16+i%228,296+i//228) for i,v in enumerate(plane) if v == 1}
        actual = {(x,y) for y in range(BODY[1],BODY[3]) for x in range(BODY[0],BODY[2]) if b.getpixel((x,y)) == (0,8,0)}
        assert expected == actual, (f,len(expected-actual),len(actual-expected))
        previous = {(x,y) for y in range(BODY[1],BODY[3]) for x in range(BODY[0],BODY[2]) if a.getpixel((x,y)) == (0,8,0)}
        glyphs = expected|previous
        shadows = {(x+1,y+1) for x,y in glyphs}
        unexpected = [(x,y) for y in range(BODY[1],BODY[3]) for x in range(BODY[0],BODY[2])
            if not(ADVANCE[0]<=x<ADVANCE[2] and ADVANCE[1]<=y<ADVANCE[3]) and (x,y) not in glyphs|shadows and a.getpixel((x,y)) != b.getpixel((x,y))]
        assert not unexpected, (f,unexpected[:12])
        assert a.crop(ADVANCE).tobytes() == b.crop(ADVANCE).tobytes(), (f,'advance phase')
        diff.paste((0,0,0),BODY)
        assert diff.getbbox() is None, (f,'outside reviewed text',diff.getbbox())
        holds.append({'frame':f,'message_id':n,'lines':case['lines'],'arguments':[s.decode('cp932') for s in args],
            'capture':after[f],'complete_independent_font_and_blank_paper_exact':True,'all_other_pixels_exact':True})
    for f in sorted(new_ram):
        if f < 3200: continue
        a,b = state(oa,old_ram[f]),state(arm,new_ram[f])
        assert a == b and models(oa,old_ram[f]) == models(arm,new_ram[f])
        assert persistent_objects(oa,old_ram[f]) == persistent_objects(arm,new_ram[f])
        assert tasks(oa,old_ram[f]) == tasks(arm,new_ram[f])
        states.append({'frame':f,'cash':b['cash'],'full_native_models_objects_and_tasks_exact':True})
    cash = {r['frame']:r['cash'] for r in states}
    assert cash[3200] == cash[8000] == cash[8400] == cash[9600] == 38816
    assert cash[10000] == cash[12400] == cash[12800] == cash[14000] == 38816-7700
    assert cash[14400] == cash[15600] == 38816-7700+6160
    initial_models, final_models = [models(arm,new_ram[f]) for f in (3200,15600)]
    assert {k:v for k,v in initial_models.items() if k != 'company'} == {k:v for k,v in final_models.items() if k != 'company'}
    assert persistent_objects(arm,new_ram[3200]) == persistent_objects(arm,new_ram[15600])
    save(ROOT/'ordinary_transactions_gameplay.json', {'candidate_sha256':new['ROM_sha256'],
        'source_reports':[str(pa),str(pb)],'source_report_sha256':[sha(p.read_bytes()) for p in (pa,pb)],
        'holds':holds,'strict_whole_screen_controls':controls,'paired_native_state_model_object_task_frames':states,
        'purchase_7700_sale_6160_original_outcomes_preserved':True,'both_declines_preserve_cash':True,
        'fleet_ships_and_persistent_objects_return_to_original_state':True,
        'company_cash_change_is_expected_transaction_result_not_a_preservation_failure':True,
        'normal_town_return_frame':15600,'no_fixtures_or_savestates':True,
        'other_rows_and_bargaining_diplomacy_require_separate_evidence':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print(f'{len(holds)} complete transaction holds,{len(controls)} strict full screens,{len(states)} native state pairs;7700 purchase,6160 sale,both declines and town return pass.',flush=True)


if __name__ == '__main__': main()
