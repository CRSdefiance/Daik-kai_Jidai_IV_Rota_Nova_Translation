"""Prospective complete Palace paragraphs through the existing native balancer."""

import struct
from pathlib import Path

from PIL import Image,ImageDraw
from unicorn.arm_const import UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_SP,UC_ARM_REG_PC

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.context_palace_v795 import ROOT,ROM,RAM
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import BASE,STACK
from scripts.probe_tavern_continuation_layout_v768 import format_case
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

MANUSCRIPT=Path('translations/palace_editorial_manuscript_v2.json')


def main():
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');context=read(ROOT/'native_context.json')
    manuscript=read(MANUSCRIPT);out=ROOT/'prototype_layout';out.mkdir(parents=True,exist_ok=True)
    cpu=machine(arm);cpu.mem_write(BASE,RAM.read_bytes())
    call(cpu,0xCB178,());from unicorn.arm_const import UC_ARM_REG_R0
    towns=cpu.reg_read(UC_ARM_REG_R0);amounts=[]
    for n in range(114):
        town=towns+4+n*108;cpu.reg_write(UC_ARM_REG_R7,town);cpu.reg_write(UC_ARM_REG_SP,STACK)
        cpu.emu_start(BASE+0x5E004,BASE+0x5E03C,count=100000)
        assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0x5E03C
        amount=cpu.reg_read(UC_ARM_REG_R6);call(cpu,0xABF50,(amount,))
        text=bytes(cpu.mem_read(cpu.reg_read(UC_ARM_REG_R0),128)).split(b'\0')[0]
        amounts.append({'town_index':n,'native_minimum_contract_fee':amount,'amount_hex':text.hex(),
            'original_two_growth_getters_and_fee_arithmetic_execute':True})
    assert amounts[22]['native_minimum_contract_fee']==2842
    save(out/'native_contract_amounts.json',{'rows':amounts,'not_all_town_objects_claimed_Palace_eligible':True})
    peers={bytes.fromhex(r['leader_address_hex']) for r in context['active_faction_leader_address_forms']}
    names={bytes.fromhex(r['address_form_hex']) for r in context['four_hero_address_forms']}
    names.add(bytes.fromhex(context['native_player_address_hex']))
    # This is a separately disclosed name-length stress input,not a claimed NPC.
    peers.add(b'ABCDEFGHIJKLMNOPQRSTUVW');names.add(b'ABCDEFGHIJKLMNOPQRSTUVW')
    fees={bytes.fromhex(r['amount_hex']) for r in amounts}
    fees|={str(n).translate(str.maketrans('0123456789','０１２３４５６７８９')).encode('cp932') for n in (1,9,10,99,100,999999999,2147483647)}
    monthly={bytes.fromhex(r['formatted_amount_hex']) for r in context['all218_native_item_monthly_price_providers']}
    cases=[];planes=[];seen=set();findings=[]
    for row in manuscript['records']:
        n=row['message_id']
        values=sorted(peers if n==1147 else names if n in (1151,1154) else fees if n in (1149,1156) else monthly if n==1166 else {b''})
        for i,value in enumerate(values):
            if i%64==0:u=prepared(arm)
            case=format_case(u,row,(value,) if row['source_native_arguments'] else ())
            cases.append(case)
            if case['findings']:findings.append(case);continue
            actual_fee='２８４２'.encode('cp932')
            marker=(n,tuple(len(s.encode('cp932'))%2 for s in case['lines']),
                value if n==1156 and value==actual_fee else None)
            if marker in seen:continue
            seen.add(marker)
            pixels=raster(arm,bytes.fromhex(case['formatted_hex']),0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
            assert pixels==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),case['lines'])
            p=out/f'complete_font_{len(planes):03d}_ID{n}.png'
            Image.frombytes('L',(228,64),bytes(0 if v else 255 for v in pixels)).save(p)
            planes.append({**case,'path':str(p),'sha256':sha(p.read_bytes()),'independent_full_native_font_exact':True})
    save(out/'native_layout_matrix.json',{'count':len(cases),'cases':cases,'findings':findings,'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'scope':'Existing native literal/balance helper only;new Palace runtime routing and production lookup not yet approved.'})
    assert not findings,findings[:3]
    sheets=[]
    for start in range(0,len(planes),12):
        sheet=Image.new('RGB',(1428,720),'#30343c');draw=ImageDraw.Draw(sheet)
        for i,row in enumerate(planes[start:start+12]):
            x,y=i%3*476,i//3*180
            draw.text((x+5,y+4),f'ID{row["id"]} / {start+i}',fill='white')
            sheet.paste(Image.open(row['path']).convert('RGB').resize((456,128),Image.Resampling.NEAREST),(x+5,y+24))
        p=out/f'all_fonts_{start//12:02d}_2x.png';sheet.save(p);sheets.append({'path':str(p),'sha256':sha(p.read_bytes())})
    save(out/'verification.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'native_layouts':len(cases),'findings':findings,'complete_font_planes':planes,'preview_sheets':sheets,
        'all31_native_IDs':sorted({c['id'] for c in cases}),'actual_revised_gameplay_and_production_routing_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print(f'{len(cases)} Palace native layouts and{len(planes)} independent full-font planes pass;production routing/revised playback pending.',flush=True)


if __name__=='__main__':main()
