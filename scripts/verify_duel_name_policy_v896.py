"""Resolve the observed duel first name against the documented full-name policy."""

import struct
from pathlib import Path
from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.finish_refit_display_v712 import load
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_name_v896')
ROM=Path('out/all_routes_combined_v893_candidate.nds')
BASE=0x02000000


def main():
    assert not (ROOT/'name_policy_resolution.json').exists()
    policy_path=Path('translations/character_name_localization_policy_v1.json');policy=read(policy_path)
    full=next(r for r in policy['confirmed_decisions'] if r.get('localized_first_name')=='Hodram')
    middle=next(r for r in policy['confirmed_decisions'] if r.get('localized_middle_name')=='Joakim')
    assert full['localized_full_name']=='Hodram Joakim Bergstrom' and middle['localized_middle_name']=='Joakim'
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x1371C:0x13724]==clean[0x1371C:0x13724]==bytes.fromhex('200080e21eff2fe1')
    assert arm[0xD700:0xD79C]==clean[0xD700:0xD79C]
    folder=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_name_v896_fresh_Joakim')
    report,images,receipt=load(folder,sha(ROM.read_bytes()),4000)
    assert 'battery_save_preloaded' not in report
    assert not any(v for k,v in report.items() if k.startswith('synthetic_'))
    fresh=(folder/'frame_004000_arm9_ram.bin').read_bytes();cpu,get=get_machine(arm,fresh)
    assert get(0x7F244)==1
    people=get(0xCB184);own=people+struct.unpack_from('<I',arm,0x1229C)[0]
    fields=[bytes(cpu.mem_read(own+offset,17)).split(b'\0')[0].decode('ascii') for offset in (32,49,66)]
    assert fields==['Hodram','Bergstrom','Joakim']
    path=Path('E:/Rota Nova translations/Generated/work/emulation_v193/battle_personal_v894_893_encounter/frame_013200_arm9_ram.bin')
    raw=path.read_bytes();cpu,get=get_machine(arm,raw)
    def word(at):return struct.unpack('<I',cpu.mem_read(at,4))[0]
    duel=0x0218D4D8;actor=word(duel+0x34);vtable=word(actor);fn=word(vtable+0x20)
    assert actor==get(0xCB184)+struct.unpack_from('<I',arm,0x1229C)[0]
    assert fn==BASE+0x1371C
    pointer=get(fn-BASE,actor);assert pointer==actor+32
    first=bytes(cpu.mem_read(pointer,16)).split(b'\0')[0].decode('ascii');assert first=='Hodram'
    # The actual unmodified duel source bitmap independently contains the two
    # complete names at its original6x12 source positions,including blank cells.
    view=duel+0x1E4;header=word(view+0x10)
    h=struct.unpack('<5I',cpu.mem_read(header,20));assert h[:3]==(4,116,96)
    pixels=(header+h[4])&0xFFFFFFFF;packed=bytes(cpu.mem_read(pixels,464*96//2))
    actual=bytes((packed[(y*464+x)//2]>>(4*(x%2)))&15 for y in range(24) for x in range(256))
    expected=bytearray(256*24);font=GameAsciiFont.from_arm9(arm)
    for row,name in enumerate(('Hodram','Speyer')):
        for i,ch in enumerate(name):
            glyph=font.decode(ch)
            for y in range(11):
                for x in range(6):
                    if glyph.getpixel((x,y)):expected[(row*12+y)*256+i*6+x]=1
    assert actual==bytes(expected)
    screenshot=path.with_name('frame_013200_navigation.png')
    with Image.open(screenshot) as im:im.crop((152,270,252,292)).resize((800,176),Image.Resampling.NEAREST).save(ROOT/'actual_duel_first_name_8x.png')
    save(ROOT/'name_policy_resolution.json',{'candidate_sha256':sha(ROM.read_bytes()),'policy':str(policy_path),'policy_sha256':sha(policy_path.read_bytes()),
        'documented_full_name':'Hodram Joakim Bergstrom','documented_first_name':'Hodram','documented_middle_name':'Joakim',
        'fresh_no_save_control_receipt':receipt,'fresh_captain_ID':1,'fresh_first_last_middle_fields':fields,
        'actual_duel_RAM':str(path),'actual_duel_RAM_sha256':sha(raw),'actual_screenshot':str(screenshot),'actual_screenshot_sha256':sha(screenshot.read_bytes()),
        'actual_duel_actor':actor,'actual_virtual_name_getter':fn,'actual_name_pointer':pointer,'actual_returned_first_name':first,
        'original_name_getter_and_duel_setup_exact_clean':True,'all6144_actual_name_bitmap_cells_match_independent_font':True,
        'duel_Hodram_label_is_consistent_with_recorded_user_name_decision':True,
        'earlier_Hodram_versus_Joakim_audit_lead_was_first_middle_role_misclassification':True,
        'no_ROM_save_or_player_name_modified':True,'initial_argument_free_getter_diagnostic_rejected_as_invalid_contract':True,
        'fresh_name_field_offsets_and_capacity':[32,49,66,17],
        'initial16_byte_stride_assumption_rejected_before_proof_creation':True,
        'initial_wrong_font_constructor_rejected_by_whole_canvas_check':True,
        'scope':'Resolves this duel first-name lead only. Does not certify every old save,name field,caption or artwork.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Duel name resolved:documented first Hodram/middle Joakim;fresh control and original getter/full6144-cell bitmap pass.No name patch warranted.',flush=True)


if __name__=='__main__':main()
