"""Prospective ceremony formatting with existing helpers; no production dispatch credit."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.context_ceremony_v806 import TABLES
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.probe_tavern_continuation_layout_v768 import format_case as ordinary
from scripts.verify_arrival_native_v792 import prepared, run
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/ceremony_layout_v807')
MANUSCRIPT=Path('translations/ceremony_editorial_manuscript_v1.json')
ROM=Path('out/all_routes_combined_v803_candidate.nds')
MODAL=(289,290,291,293,294,295)


def result_case(u,row,values):
    raw=b' '+row['english'].removesuffix('{PAD}').encode('ascii')
    template,out,arg=0x02426000,0x02426420,0x02426800
    u.mem_write(template,raw+b'\0');u.mem_write(arg,(values[0] if values else b'')+b'\0')
    u.mem_write(out-16,b'\xa5'*288)
    call(u,0xD7720,(out,template,arg))
    expected=raw.replace(b'%s',values[0]) if values else raw
    assert len(expected)<236
    assert bytes(u.mem_read(out,len(expected)+1))==expected+b'\0'
    assert bytes(u.mem_read(out-16,16))==b'\xa5'*16
    assert bytes(u.mem_read(out+len(expected)+1,271-len(expected)))==b'\xa5'*(271-len(expected))
    # Explicit proxy: ID348 selects the existing balanced modal path. The
    # ceremony IDs are NOT enabled in the production dispatcher by this probe.
    formatted,wrapped=run(u,0x020546E8,348,expected)
    assert wrapped and b' '.join(formatted.split())==b' '.join(expected.split())
    lines=[s.strip().decode('ascii') for s in formatted.split(b'\n')]
    findings=[]
    if len(lines)>4 or any(len(s)>35 for s in lines):findings.append('four_row_width_bound')
    if len(lines)>1 and len(lines[-1])<=8:findings.append('short_final_row')
    weak={'a','an','as','at','for','from','in','of','the','to','with'}
    if any(s.split()[-1].strip('.,!?;:').lower() in weak for s in lines[:-1] if s.split()):findings.append('weak_line_end')
    return dict(id=row['message_id'],source_values_hex=[s.hex() for s in values],
        formatted_hex=formatted.hex(),lines=lines,findings=findings,
        exact_printf_complete_words_guards_and_callee_saved_ABI=True,
        production_dispatch_ID348_proxy_only_ceremony_scope_not_yet_enabled=True)


def name_catalog(arm,context):
    raw=Path(context['source_RAM']).read_bytes()
    assert sha(raw)==context['source_RAM_sha256']
    u=machine(arm);u.mem_write(BASE,raw)
    def get(fn,args=()):
        call(u,fn,args,instruction_limit=300000)
        return u.reg_read(UC_ARM_REG_R0)
    def word(at):return struct.unpack('<I',u.mem_read(at,4))[0]
    def text(at):return bytes(u.mem_read(at,256)).split(b'\0')[0]
    root=get(0xCB184);names=[]
    for hero in context['hero_names']:
        ob=root+4+hero['index']*32
        names.append(dict(hero_index=hero['index'],given_name_hex=text(get(0x7EB0C,(ob,))).hex(),
            original_given_name_getter=BASE+0x7EB0C,actor=ob))
    ob=root+0x19E4
    edited=text(get(word(word(ob)+0x20)-BASE,(ob,)))
    return names,dict(current_admiral_object=ob,given_name_hex=edited.hex(),
        original_virtual_given_name_getter=word(word(ob)+0x20))


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin')
    context=read('work/analysis/ceremony_context_v806/native_context.json');doc=read(MANUSCRIPT)
    assert sha(ROM.read_bytes())==context['candidate_sha256']
    assert sha(arm)==context['current_ARM9_sha256']
    assert sha(Path(doc['native_context_proof']).read_bytes())==doc['native_context_sha256']
    names,edited=name_catalog(arm,context)
    save(ROOT/'native_given_names.json',dict(names=names,current_admiral=edited))
    given=sorted({bytes.fromhex(r['given_name_hex']) for r in names}|{bytes.fromhex(edited['given_name_hex']),b'ABCDEFGHIJKLMNOPQRSTUVW'})
    cases=[]
    for row in doc['records']:
        n=row['message_id']
        if n==1219:variants=[(bytes.fromhex(s['name_hex']),) for s in context['site_name_catalog']]
        elif n in MODAL and row['source_native_arguments']:variants=[(s,) for s in given]
        else:variants=[()]
        for values in variants:
            u=prepared(arm)
            case=result_case(u,row,values) if n in MODAL else ordinary(u,row,values)
            case['prospective_consumer']='modal-result' if n in MODAL else ('four-protagonist-reaction' if any(n in t for t in TABLES.values()) else 'NPC-dialogue-or-offer')
            if n==64:case['shared64_original_presentation_not_changed']=True
            cases.append(case)
    findings=[r for r in cases if r['findings']]
    save(ROOT/'native_layout_matrix.json',dict(count=len(cases),findings_count=len(findings),cases=cases,
        supplied_site_catalog_and_name_bounds_not_all_legal_or_earned_states=True,
        production_dispatch_COMMON_integration_and_actual_gameplay_pending=True))
    save(ROOT/'layout_findings.json',findings)
    # Render every distinct complete text plane, including every site/name value.
    planes=[];kanji=rom.read_file('/GRP/KANJI.FNT')
    for i,case in enumerate(cases):
        pixels=raster(arm,bytes.fromhex(case['formatted_hex']),0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
        assert pixels==independent_font(arm,kanji,case['lines']),case
        path=ROOT/f'complete_font_{i:03d}_ID{case["id"]}.png'
        Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(path)
        planes.append(dict(case_index=i,path=str(path),sha256=sha(path.read_bytes()),independent_full_native_font_and_blank_plane_exact=True))
    sheets=[]
    for start in range(0,len(planes),12):
        sheet=Image.new('RGB',(1428,720),'#30343c');draw=ImageDraw.Draw(sheet)
        for j,p in enumerate(planes[start:start+12]):
            case=cases[p['case_index']];x,y=j%3*476,j//3*180
            draw.text((x+6,y+4),f'RESEARCH ID{case["id"]} case{start+j}',fill='white')
            sheet.paste(Image.open(p['path']).convert('RGB').resize((456,128),Image.Resampling.NEAREST),(x+6,y+24))
            if case['findings']:draw.text((x+6,y+156),','.join(case['findings']),fill='#ffb080')
        path=ROOT/f'preview_{start//12:02d}.png';sheet.save(path)
        sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'research_report.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),
        manuscript_sha256=sha(MANUSCRIPT.read_bytes()),source_context_sha256=sha(Path(doc['native_context_proof']).read_bytes()),
        layouts=len(cases),findings=len(findings),native_given_names=names,current_admiral=edited,
        complete_font_planes=planes,sheets=sheets,
        source_expected_parent_contracts={'ordinary':0x02054014,'yes_no':0x02053FCC,'hero':0x02053C14,'modal':0x020546E8},
        modal_existing_ID348_proxy_exercises_balanced_path_without_enabling_ceremony_IDs=True,
        ordinary_direct_LITERAL_helper_not_production_dispatch_verification=True,
        shared64_external_consumer_audit_still_required=True,
        all52_formatting_gates_still_false=True,ROM_changed=False,new_completion_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(f'{len(cases)} prospective native layouts;{len(planes)} complete independently matched font planes;{len(findings)} findings. No production dispatch or gameplay credit.',flush=True)


if __name__=='__main__':main()
