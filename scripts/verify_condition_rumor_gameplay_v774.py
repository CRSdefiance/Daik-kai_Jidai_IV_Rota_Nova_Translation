"""Verify an actual original rumor consumer with a disclosed two-byte fixture."""

import struct
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageChops
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import recruitment_editorial_runtime as runtime
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts import probe_recruitment_layout_v771 as layout
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.native_town_condition_fixture_v774 import set_condition
from scripts.native_town_condition_baseline_v774 import set_condition as baseline_condition
from scripts.probe_button_prompt_native import BASE
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_shipyard_gameplay_v760 import models, independent_font
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/condition_rumor_v774')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
BODY = (16,294,244,366)
ADVANCE = (224,360,240,376)
SCENES = (28000,28400)


def load(folder, baseline=False):
    path = CAP/folder/'capture_report.json'
    r = read(path)
    assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
    assert not r['hardware_device_verification'] and not r['goal_complete']
    assert r['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert r['ROM_sha256'] == sha(Path(r['ROM']).read_bytes())
    arm = NdsImage.open(r['ROM']).read_file('/__arm9__.bin')
    donor = r['battery_save_preloaded']
    pin = read(ROOT/'source_donor.json')
    assert Path(donor['source']).resolve() == Path(pin['path']).resolve()
    assert donor['source'] != donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256'] == pin['sha256']
    assert not any(v for k,v in r.items() if k.startswith('synthetic_') and k != 'synthetic_town_condition_fixtures')
    ram = {}
    for row in r['read_only_capture_RAM_snapshots'] + r['read_only_pause_RAM_snapshots']:
        assert row['read_only_export'] and row['bytes'] == 0x400000
        raw = Path(row['path']).read_bytes()
        assert sha(raw) == row['sha256']
        if row['frame'] in ram: assert ram[row['frame']] == raw
        ram[row['frame']] = raw
    fixture, = r['synthetic_town_condition_fixtures']
    apply = baseline_condition if baseline else set_condition
    _, expected = apply(arm,ram[3200],{'town':2,'status':3,'days':30})
    assert fixture == {**expected,'frame':3200}
    adapter = r['controlled_town_condition_adapter']
    suffix = 'baseline' if baseline else 'capture'
    producer = 'baseline' if baseline else 'fixture'
    assert adapter['original_harness_file_unchanged']
    assert adapter['original_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
    assert adapter['adapter_sha256'] == sha(Path(f'scripts/run_town_condition_{suffix}_v774.py').read_bytes())
    assert adapter['fixture_producer_sha256'] == sha(Path(f'scripts/native_town_condition_{producer}_v774.py').read_bytes())
    frames = {}
    for row in r['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        frames[row['frame']] = row
    return path,r,arm,frames,ram


def main():
    pa,old,old_arm,before,old_ram = load('condition_rumor_v774_fourth_round_baseline',True)
    pb,new,arm,after,new_ram = load('condition_rumor_v774_fourth_round_live')
    assert old['frames'] == new['frames'] == 32800
    assert old['scripted_input_schedule'] == new['scripted_input_schedule']
    assert old['core_options'] == new['core_options']
    assert set(before) == set(after) and old_ram.keys() == new_ram.keys()
    rom = NdsImage.open(new['ROM'])
    entries = common_message_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm,clean=False)
    blocks = IlnkContainer.parse(rom.read_file('/COMMON/MESFILE.DK4')).blocks
    row = next(r for r in read('translations/recruitment_editorial_manuscript_v3.json')['records'] if r['message_id'] == 906)
    env = dict(layout.__dict__)
    env['runtime'] = runtime
    formatter = FunctionType(layout.formatter.__code__,env)()[0]
    p,w,owner = [struct.unpack_from('<I',arm,off)[0] for off in (0x5444C,0x54450,0x552A0)]
    scenes,controls,states = [],[],[]
    baseline_indicators = {f:Image.open(r['path']).convert('RGB').crop(ADVANCE).tobytes() for f,r in before.items()}
    for f in sorted(after):
        a,b = [Image.open(r[f]['path']).convert('RGB') for r in (before,after)]
        diff = ImageChops.difference(a,b)
        if f not in SCENES:
            assert diff.getbbox() is None,(f,diff.getbbox())
            controls.append(f)
            continue
        raw = new_ram[f]
        assert cstring(raw,owner+0x2030) == entries[906].text
        assert raw.count(blocks[entries[906].block]) == 1
        assert cstring(raw,p) == b" Word is, Amsterdam's been going through a major economic boom lately."
        u = machine(arm)
        u.mem_write(BASE,raw)
        call(u,0xCB178,())
        town = u.reg_read(UC_ARM_REG_R0)+4+108*2
        call(u,0xB2E04,(town,))
        assert u.reg_read(UC_ARM_REG_R0) == 3 and bytes(u.mem_read(town+107,1)) == b'\x1e'
        call(u,0xB2D58,(town,))
        assert bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0),5)) == b'Boom\0'
        native = formatter(u,row,(b'Amsterdam',b'Boom'))
        assert not native['findings']
        assert bytes.fromhex(native['formatted_hex']) == cstring(raw,w)
        plane = raster(arm,bytes.fromhex(native['formatted_hex']),0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
        assert plane == independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),native['lines'])
        expected = {(16+i%228,296+i//228) for i,v in enumerate(plane) if v == 1}
        actual = {(x,y) for y in range(BODY[1],BODY[3]) for x in range(BODY[0],BODY[2]) if b.getpixel((x,y)) == (0,8,0)}
        assert expected == actual,(f,len(expected-actual),len(actual-expected))
        previous = {(x,y) for y in range(BODY[1],BODY[3]) for x in range(BODY[0],BODY[2]) if a.getpixel((x,y)) == (0,8,0)}
        shadows = {(x+1,y+1) for x,y in expected|previous}
        unexpected = [(x,y) for y in range(BODY[1],BODY[3]) for x in range(BODY[0],BODY[2])
            if not(ADVANCE[0]<=x<ADVANCE[2] and ADVANCE[1]<=y<ADVANCE[3])
            and (x,y) not in expected|previous|shadows and a.getpixel((x,y)) != b.getpixel((x,y))]
        assert not unexpected,(f,unexpected[:10])
        matches = [n for n,v in baseline_indicators.items() if v == b.crop(ADVANCE).tobytes()]
        assert matches,(f,'unrecognized original advance animation')
        diff.paste((0,0,0),BODY)
        diff.paste((0,0,0),ADVANCE)
        assert diff.getbbox() is None,(f,diff.getbbox())
        scenes.append({'frame':f,'message_ID':906,'source_arguments':['Amsterdam','Boom'],
            'English_status_phrase':'a major economic boom','lines':native['lines'],'capture':after[f],
            'complete_independent_font_and_blank_paper_cells_exact':True,
            'all_other_pixels_and_portrait_exact':True,'source_advance_animation_matches_frames':matches})
    for f in sorted(new_ram):
        assert state(old_arm,old_ram[f]) == state(arm,new_ram[f]),(f,'state')
        assert models(old_arm,old_ram[f]) == models(arm,new_ram[f]),(f,'models')
        assert persistent_objects(old_arm,old_ram[f]) == persistent_objects(arm,new_ram[f]),(f,'objects')
        states.append(f)
    table = struct.unpack_from('<13I',arm,0x156430)
    for f in (28000,28400,28800,32800):
        for label in table:
            assert cstring(old_ram[f],label) == cstring(new_ram[f],label)
    patch = read('work/analysis/recruitment_release_v773/patch_proof.json')
    assert patch['candidate_sha256'] == new['ROM_sha256'] and patch['byte_exact_reconstruction']
    save(ROOT/'gameplay_verification.json',{
        'candidate':new['ROM'],'candidate_sha256':new['ROM_sha256'],
        'capture_reports':[str(pa),str(pb)],'actual_condition_rumor_holds':scenes,
        'whole_screen_controls':controls,'paired_native_state_model_object_frames':states,
        'four_paid_rounds_selected_by_original_game_logic':True,
        'normal_Tavern_menu_dismissal_frame':28800,
        'normal_dismissal_and_town_return_frame':32800,'all13_global_UI_status_labels_unchanged':True,
        'same_two_byte_fixture_receipt_reproduced_on_both_ROMs':True,
        'original_save_unchanged':True,'natural_condition_event_verified':False,
        'formal905_actual_activation':False,
        'formal905_scope':'Same original portrait consumer/provider/status helper; all114 towns x12 statuses x2 voices have prior native coverage. Actual family sample is906 only.',
        'existing_V773_exact_patch_retained':True,'producer_sha256':sha(Path(__file__).read_bytes()),
        'full_goal_complete':False})
    print('Two actual906 holds,complete fonts/blank paper,paired states and ordinary town return pass.',flush=True)


if __name__ == '__main__': main()
