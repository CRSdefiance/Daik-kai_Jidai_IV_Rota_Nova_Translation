"""Full native prospective outputs/fonts for25 source-reviewed paragraphs."""

import inspect
import struct
from pathlib import Path

from PIL import Image,ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R8

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_tavern_continuation_layout_v768 as prior
from scripts import recruitment_runtime_research_v771 as runtime
from scripts.context_tavern_recruitment_v771 import CURRENT,RAM_REPORT,ROOT
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE,STACK
from scripts.review_tavern_recruitment_v771 import MANUSCRIPT
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

OUT=ROOT/'native_layout_phrases_v2'


def formatter():
    source=inspect.getsource(prior.format_case)
    marker="    for p, value in zip(pointers, values): u.mem_write(p, value + b'\\0')"
    replacement='''    status_index = None
    if row['message_id'] in (905,906):
        status_pointers = struct.unpack('<13I',u.mem_read(0x02156430,52))
        labels = [bytes(u.mem_read(p,128)).split(b'\\0')[0] for p in status_pointers]
        status_index = labels.index(values[1])
        assert status_index < 12
        pointers[1] = status_pointers[status_index]
    for i,(p,value) in enumerate(zip(pointers,values)):
        if status_index is not None and i==1:
            assert bytes(u.mem_read(p,len(value)+1)) == value+b'\\0'
        else:
            u.mem_write(p,value+b'\\0')'''
    assert source.count(marker)==1;source=source.replace(marker,replacement)
    marker='    call(u, LITERAL - BASE, (wrapped, output, 0), instruction_limit=2000000)'
    replacement='''    n = row['message_id']
    parent = 0x02053D24 if 890<=n<=896 else 0x02053DB8 if 883<=n<=889 or 897<=n<=903 else 0x02053E38 if n==904 else 0x02054014
    table = 0x02118380 if 890<=n<=896 else 0x021183A0 if 883<=n<=889 else 0x02118360 if 897<=n<=903 else 904 if n==904 else pointers[1] if n in(905,906) else 0
    for off,value in ((0x264,parent),(0x274,n),(0x27C,table)):
        u.mem_write(STACK+off,struct.pack('<I',value))
    call(u, 0x01FFCF3C - BASE, (wrapped, output, 0), instruction_limit=2000000)'''
    assert source.count(marker)==1;source=source.replace(marker,replacement)
    marker="    assert b' '.join(result.split()) == b' '.join(expected.split())"
    replacement="    if n in(905,906):\n        suffix=runtime.STATUS_SUFFIX\n        assert expected.endswith(values[-1]+suffix)\n        expected=expected[:-len(values[-1])-len(suffix)]+runtime.STATUS_PHRASES[status_index].encode()+suffix\n        assert bytes(u.mem_read(pointers[1],len(values[-1])+1))==values[-1]+b'\\0'\n"+marker
    assert source.count(marker)==1;source=source.replace(marker,replacement)
    local=dict(prior.__dict__);local['runtime']=runtime
    exec(compile(source,str(Path(__file__)),'exec'),local)
    return local['format_case'],source


def source_amounts(arm,raw,context):
    u=machine(arm);u.mem_write(BASE,raw);rows=[]
    for city in context['actual114_native_town_objects']:
        call(u,0xB3FD4,(city['object'],0));growth=u.reg_read(UC_ARM_REG_R0)
        assert 0<=growth<=65535
        u.emu_start(BASE+0x57420,BASE+0x57438,count=100)
        cost=u.reg_read(UC_ARM_REG_R8);assert cost==500+growth//5
        call(u,0xABF50,(cost,));at=u.reg_read(UC_ARM_REG_R0)
        value=bytes(u.mem_read(at,64)).split(b'\0')[0]
        assert int(value.decode('cp932'))==cost
        rows.append({'town_index':city['index'],'native_growth':growth,'native_recruitment_cost':cost,'amount_hex':value.hex()})
    return rows


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    context=read(ROOT/'native_context.json');doc=read(MANUSCRIPT)
    contracts=read(ROOT/'typed_status_contracts.json')
    assert contracts['count']==140
    assert contracts['runtime_source_sha256']==sha(Path(runtime.__file__).read_bytes())
    rom=NdsImage.open(CURRENT);arm=rom.read_file('/__arm9__.bin');raw=snapshot(read(RAM_REPORT),3200)
    amounts=source_amounts(arm,raw,context);save(OUT/'actual114_recruitment_costs.json',amounts)
    digits=lambda n:str(n).translate(str.maketrans('0123456789','０１２３４５６７８９')).encode('cp932')
    numeric={digits(n) for n in(0,1,2,9,10,99,100,500,999,1573,9999,65535,999999,2147483647)}
    costs=sorted(numeric|{bytes.fromhex(r['amount_hex']) for r in amounts})
    quantities=sorted(numeric|{digits(n) for n in(15,20,25,30,31,32,33,34,35,36,37,38,50,1000)})
    town_names=[bytes.fromhex(r['name_hex']) for r in context['actual114_native_town_objects']]
    status=[r['current_UI_label'].encode() for r in context['all13_source_status_names_and_UI_labels'] if r['eligible_for_source_rumor']]
    def variants(n):
        if 890<=n<=896:yield from((v,) for v in costs)
        elif n==904:yield from((v,) for v in quantities)
        elif n in(905,906):yield from((a,b) for a in town_names for b in status)
        else:yield ()
    format_case,effective=formatter();cases=[];findings=[]
    for row in doc['records']:
        n=row['message_id'];before=len(cases)
        for i,values in enumerate(variants(n)):
            if i%64==0:
                u=machine(arm);u.mem_write(BASE,raw);runtime.load(u)
            result=format_case(u,row,values);cases.append(result)
            if result['findings']:findings.append(result)
        print(f'ID{n}:{len(cases)-before} native layouts;{len(findings)} findings so far.',flush=True)
    save(OUT/'matrix.json',{'count':len(cases),'cases':cases,'findings_count':len(findings),
        'all114_names_by12_states_are_supplied_field_combinations_not_all_earned_world_states':True,
        'numeric_boundaries_include_synthetic_amounts_not_claimed_reachable_recruitment_costs':True})
    save(OUT/'findings.json',findings)
    assert not findings,f'{len(findings)} presentation findings remain'
    previews=[];seen=set();kanji=rom.read_file('/GRP/KANJI.FNT')
    for row in cases:
        marker=(row['id'],tuple(len(s.encode('cp932'))%2 for s in row['lines']))
        if row['id'] in range(890,897) or row['id']==904:
            marker+=(len(bytes.fromhex(row['English_values_hex'][0])),)
        if marker in seen:continue
        seen.add(marker);formatted=bytes.fromhex(row['formatted_hex'])
        plane=raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
        assert plane==independent_font(arm,kanji,row['lines'])
        path=OUT/f'font_{len(previews):03d}_ID{row["id"]}.png'
        Image.frombytes('L',(228,64),bytes(0 if v else 255 for v in plane)).save(path)
        previews.append({**row,'path':str(path),'sha256':sha(path.read_bytes()),'independent_complete_font_plane_exact':True})
    sheets=[]
    for start in range(0,len(previews),12):
        sheet=Image.new('RGB',(1428,720),'#30343c');draw=ImageDraw.Draw(sheet)
        for i,row in enumerate(previews[start:start+12]):
            x,y=i%3*476,i//3*180;draw.text((x+5,y+4),f'RESEARCH ID{row["id"]} / {start+i}',fill='white')
            sheet.paste(Image.open(row['path']).convert('RGB').resize((456,128),Image.Resampling.NEAREST),(x+5,y+24))
        path=OUT/f'fonts_{start//12:02d}_2x.png';sheet.save(path);sheets.append({'path':str(path),'sha256':sha(path.read_bytes())})
    save(OUT/'verification.json',{'source_ROM_sha256':sha(CURRENT.read_bytes()),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'complete_native_layouts':len(cases),'all25_IDs':sorted({r['id'] for r in cases}),
        'independent_full_font_planes':previews,'preview_sheets':sheets,
        'effective_formatter_sha256':sha(effective.encode()),'producer_sha256':sha(Path(__file__).read_bytes()),
        'scratch_runtime_only_no_owned_storage_registered_ROM_patch_or_actual_gameplay_claim':True,'full_goal_complete':False})
    print(f'{len(cases)} scoped native layouts,{len(previews)} independent font planes,{len(sheets)} sheets pass. Research only.',flush=True)


if __name__=='__main__':main()
