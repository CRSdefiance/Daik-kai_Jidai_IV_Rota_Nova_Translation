"""Original Inn-parent trampoline layout/font research for every reviewed entry."""

import inspect
import struct
from pathlib import Path

from PIL import Image,ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch import inn_editorial_runtime as runtime
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_tavern_continuation_layout_v768 as old
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/inn_runtime_v802/layout')
MANUSCRIPT=Path('translations/inn_editorial_manuscript_v1.json')


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    rom=NdsImage.open('out/all_routes_combined_v799_candidate.nds')
    source=rom.read_file('/__arm9__.bin')
    arm=Path('work/analysis/inn_runtime_v802/ARM9_RUNTIME_RESEARCH_ONLY.bin').read_bytes()
    assert arm==runtime.apply(source)
    raw=Path('E:/Rota Nova translations/Generated/work/emulation_v193/inn_v801_context/frame_004000_arm9_ram.bin').read_bytes()
    cpu=machine(source);cpu.mem_write(BASE,raw)
    def get(fn,args=()):
        call(cpu,fn,args);return cpu.reg_read(UC_ARM_REG_R0)
    def ptr(at):return struct.unpack('<I',cpu.mem_read(at,4))[0]
    catalog={}
    for kind,getter,count,stride in (('towns',0xCB178,90,108),('goods',0xCB124,124,16),('companies',0xCB160,20,76)):
        root=get(getter)+4;rows=[]
        for i in range(count):
            ob=root+i*stride;p=get(ptr(ptr(ob)+8)-BASE,(ob,))
            name=bytes(cpu.mem_read(p,128)).split(b'\0')[0]
            assert name and name.isascii() and len(name)<64
            rows.append(dict(index=i,native_object=ob,native_name_pointer=p,name_hex=name.hex(),name=name.decode('ascii')))
        catalog[kind]=rows
    save(ROOT/'original_name_getters.json',dict(catalog=catalog,source_RAM_sha256=sha(raw),
        objects_not_all_claimed_eligible_for_every_Inn_event=True))
    towns=sorted({bytes.fromhex(r['name_hex']) for r in catalog['towns']})
    goods=sorted({bytes.fromhex(r['name_hex']) for r in catalog['goods']})
    companies=sorted({bytes.fromhex(r['name_hex']) for r in catalog['companies']}|{b'ABCDEFGHIJKLMNOPQRSTUVW'})
    times=sorted({bytes.fromhex(r['text_hex']) for r in read('work/analysis/inn_runtime_v802/complete_month_phrases.json')['cases']})
    longest=lambda values:max(values,key=lambda v:(len(v),v))
    lt,lg,lc,lm=map(longest,(towns,goods,companies,times))
    def variants(n):
        if n in (1182,1184):return sorted({(t,lg) for t in towns}|{(lt,g) for g in goods})
        if n in (1183,1185) or 1186<=n<=1193:return [(c,) for c in companies]
        if n in (1195,1196):
            subjects=set(towns)|set(companies)
            ls=longest(subjects)
            return sorted({(lm,s,lc) for s in subjects}|{(lm,ls,c) for c in companies}|{(t,ls,lc) for t in times})
        if n in (1197,1198):return sorted({(lm,c,lt) for c in companies}|{(lm,lc,t) for t in towns}|{(t,lc,lt) for t in times})
        if n==1180:return [(str(v).translate(str.maketrans('0123456789','０１２３４５６７８９')).encode('cp932'),) for v in (3,10,30)]
        return [()]
    program=inspect.getsource(old.format_case)
    marker='    call(u, LITERAL - BASE, (wrapped, output, 0), instruction_limit=2000000)'
    replacement='''    n=row['message_id']
    parent=0x02053DB8 if 1186<=n<=1193 else 0x02053FCC if n in (1177,1180,1199) else 0x02054014
    queue=0x021180E0 if 1186<=n<=1193 else 0
    for at,value in ((0x264,parent),(0x274,n),(0x27C,queue),(0x270,0)):
        u.mem_write(STACK+at,struct.pack('<I',value))
    call(u,0x01FFCF3C-BASE,(wrapped,output,0),instruction_limit=2000000)
    for p,value in zip(pointers,values):
        assert bytes(u.mem_read(p,len(value)+1))==value+b'\\0' '''
    assert program.count(marker)==1
    program=program.replace(marker,replacement)
    (ROOT/'effective_format_case.py').write_text(program,encoding='utf-8')
    env={**old.__dict__};exec(compile(program,str(ROOT/'effective_format_case.py'),'exec'),env)
    cases=[];findings=[]
    for row in read(MANUSCRIPT)['records']:
        n=row['message_id'];values=variants(n)
        for i,args in enumerate(values):
            if i%64==0:u=prepared(arm)
            case=env['format_case'](u,row,args);cases.append(case)
            if case['findings']:findings.append(case)
        print(f'Inn{n}:{len(values)} original-parent layouts;{len(findings)} findings so far.',flush=True)
    save(ROOT/'native_layout_matrix.json',dict(count=len(cases),cases=cases,findings=findings,
        manuscript_sha256=sha(MANUSCRIPT.read_bytes()),research_ARM9_sha256=sha(arm),
        coverage='Every native town/goods/company name exercised against the longest counterpart;all12 relative-month forms against longest subjects;23-letter explicit synthetic company-name stress. Not all Cartesian combinations or event eligibility claimed.',
        COMMON_repack_and_actual_revised_playback_pending=True))
    assert not findings,f'{len(findings)} native layouts need review'
    planes=[];seen=set();kanji=rom.read_file('/GRP/KANJI.FNT')
    for case in cases:
        marker=(case['id'],tuple(len(line.encode('cp932'))%2 for line in case['lines']))
        if marker in seen:continue
        seen.add(marker)
        pixels=raster(arm,bytes.fromhex(case['formatted_hex']),0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
        assert pixels==independent_font(arm,kanji,case['lines'])
        path=ROOT/f'full_font_{len(planes):03d}_ID{case["id"]}.png'
        Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(path)
        planes.append(dict(**case,path=str(path),sha256=sha(path.read_bytes()),full_independent_font_exact=True))
    sheets=[]
    for start in range(0,len(planes),12):
        im=Image.new('RGB',(1428,720),'#30343c');draw=ImageDraw.Draw(im)
        for i,row in enumerate(planes[start:start+12]):
            x,y=i%3*476,i//3*180;draw.text((x+5,y+4),f'RESEARCH ID{row["id"]} / {start+i}',fill='white')
            im.paste(Image.open(row['path']).convert('RGB').resize((456,128),Image.Resampling.NEAREST),(x+5,y+24))
        path=ROOT/f'all_fonts_{start//12:02d}_2x.png';im.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'verification.json',dict(native_layouts=len(cases),full_font_planes=planes,preview_sheets=sheets,
        all23_native_IDs=sorted({c['id'] for c in cases}),findings=[],research_ARM9_sha256=sha(arm),
        manuscript_sha256=sha(MANUSCRIPT.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),effective_program_sha256=sha(program.encode()),
        actual_revised_playback_and_COMMON_integration_pending=True,visual_review_pending=True,full_goal_complete=False))
    print(f'Inn:{len(cases)} native layouts/{len(planes)} complete independent fonts pass;COMMON integration and actual revised scenes pending.',flush=True)


if __name__=='__main__':main()
