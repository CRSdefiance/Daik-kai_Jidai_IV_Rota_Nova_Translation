"""Exact modal dispatch scope, original printf, complete glyphs and no growth."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE

from dk4tool.patch.arrival_notices_editorial import ROOT, IDS, compiled, modal_code
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

TEXT,DEST,VALUE=0x0242D000,0x0242E000,0x0242F000


def prepared(arm):
    cpu=machine(arm)
    cpu.mem_write(POOL,bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]))
    return cpu


def run(cpu,parent,n,raw):
    capacity=max(256,len(raw)+1)
    cpu.mem_write(TEXT,raw+b'\0');cpu.mem_write(DEST-16,b'\xa5'*(capacity+32))
    cpu.mem_write(STACK+0xC4,struct.pack('<I',parent));cpu.mem_write(STACK+0xD0,struct.pack('<I',n))
    visited=[]
    h=cpu.hook_add(UC_HOOK_CODE,lambda c,pc,size,data:visited.append(pc),begin=0x01FFCA00,end=0x01FFCA00)
    try:call(cpu,0x01FFC900-BASE,(DEST,TEXT,0),instruction_limit=2000000)
    finally:cpu.hook_del(h)
    assert bytes(cpu.mem_read(TEXT,len(raw)+1))==raw+b'\0'
    assert bytes(cpu.mem_read(DEST-16,16))==bytes(cpu.mem_read(DEST+capacity,16))==b'\xa5'*16
    output=bytes(cpu.mem_read(DEST,capacity)).split(b'\0')[0]
    return output,bool(visited)


def format_case(cpu,row,value):
    raw=compiled(row);template=VALUE+0x200;output=VALUE+0x400
    cpu.mem_write(template,raw+b'\0');cpu.mem_write(VALUE,value+b'\0')
    cpu.mem_write(output-16,b'\xa5'*288)
    call(cpu,0xD7720,(output,template,VALUE))
    text=raw.replace(b'%s',value)
    assert bytes(cpu.mem_read(output,len(text)+1))==text+b'\0'
    assert bytes(cpu.mem_read(output-16,16))==b'\xa5'*16
    result,wrapped=run(cpu,0x020546E8,row['message_id'],text)
    assert wrapped and b' '.join(result.split())==b' '.join(text.split())
    lines=[s.strip().decode('cp932') for s in result.split(b'\n')]
    assert len(lines)<=4 and all(len(s.encode('cp932'))<=35 for s in lines)
    findings=[]
    if len(lines)>1 and len(lines[-1].encode('cp932'))<=8:findings.append('short_final_row')
    weak={'a','an','as','at','for','from','in','of','the','to','with'}
    if any(s.split()[-1].strip('.,!?;:').lower() in weak for s in lines[:-1]):findings.append('weak_line_end')
    return {'id':row['message_id'],'value_hex':value.hex(),'formatted_hex':result.hex(),'lines':lines,'findings':findings}


def main():
    rom=NdsImage.open('out/all_routes_combined_v788_candidate.nds');source=rom.read_file('/__arm9__.bin')
    arm=(ROOT/'ARM9_RESEARCH_ONLY.bin').read_bytes();plan=read(ROOT/'prospective_repack.json')
    old,new=prepared(source),prepared(arm)
    text=b'These instructions contain several complete words and preserve every leading and final character.'
    changed=[]
    for n in range(3668):
        if n%64==0:old,new=prepared(source),prepared(arm)
        a,aw=run(old,0x020546E8,n,text);b,bw=run(new,0x020546E8,n,text)
        if n in IDS:
            assert not aw and bw and a!=b and b' '.join(b.split())==text
            changed.append(n)
        else:assert (a,aw)==(b,bw),n
    controls=[]
    for parent in (0x0205469C,0x02054720,0x02054764,0x02054014):
        for n in (*range(127,135),*range(269,273),321,327,*range(344,351)):
            assert run(old,parent,n,text)==run(new,parent,n,text)
            controls.append([parent,n])
    failures=[]
    for text in (b'',b'A'*237,b' '.join([b'Extraordinary']*25)):
        for n in (127,269,321,327):
            assert run(old,0x020546E8,n,text)==run(new,0x020546E8,n,text)
            failures.append([n,len(text)])
    rows=read('translations/arrival_notices_editorial_manuscript_v2.json')['records']
    context=read('work/analysis/tavern_continuation_v768/native_context_partial.json')
    names=sorted({bytes.fromhex(r['name_hex']) for r in context['real_company_names']}|{b'Castor Co.',b'ABCDEFGHIJKLMNOPQRSTUVW'})
    amounts=[str(n).translate(str.maketrans('0123456789','０１２３４５６７８９')).encode('cp932') for n in (0,1,5,9,10,99,100)]
    cases=[];planes=[];seen=set()
    for row in rows:
        for value in (amounts if row['message_id']==348 else names):
            case=format_case(prepared(arm),row,value);cases.append(case)
            assert not case['findings'],case
            marker=(case['id'],tuple(len(s.encode('cp932'))%2 for s in case['lines']))
            if marker in seen:continue
            seen.add(marker)
            pixels=raster(arm,bytes.fromhex(case['formatted_hex']),0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
            assert pixels==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),case['lines'])
            path=ROOT/f'complete_font_{len(planes):02d}_ID{case["id"]}.png'
            Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(path)
            planes.append({**case,'path':str(path),'sha256':sha(path.read_bytes()),'complete_independent_font_and_guards':True})
    sheet=Image.new('RGB',(700,170*len(planes)),'#30343c');draw=ImageDraw.Draw(sheet)
    for n,p in enumerate(planes):
        draw.text((8,n*170+4),f'ID{p["id"]} / {bytes.fromhex(p["value_hex"]).decode("cp932")}',fill='white')
        sheet.paste(Image.open(p['path']).convert('RGB').resize((456,128),Image.Resampling.NEAREST),(8,n*170+24))
    path=ROOT/'all_fonts_2x.png';sheet.save(path)
    save(ROOT/'native_verification.json',{'source_ARM9_sha256':sha(source),'research_ARM9_sha256':sha(arm),
        'manuscript_sha256':sha(Path('translations/arrival_notices_editorial_manuscript_v2.json').read_bytes()),
        'exact_modal_scope_added':changed,'all_other3665_IDs_byte_exact':True,'wrong_parent_controls':controls,
        'old_empty_and_failure_controls':failures,'all_calls_preserve_callee_saved_ABI_and_input_output_guards':True,
        'layouts':cases,'complete_font_planes':planes,'preview_sheet':str(path),'preview_sha256':sha(path.read_bytes()),
        'only_existing_modal128_bytes_and_COMMON_metadata_change':True,
        'repacked_blocks':plan['repacked_block_range'],'ARM_Thumb_interworking_on_ARM946_native_model':True,
        'actual_corrected_gameplay_and_registered_ROM_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print(f'3668 modal IDs;{len(controls)} other-parent controls;{len(cases)} original printf/layout cases;{len(planes)} full glyph planes pass.',flush=True)


if __name__=='__main__':main()
