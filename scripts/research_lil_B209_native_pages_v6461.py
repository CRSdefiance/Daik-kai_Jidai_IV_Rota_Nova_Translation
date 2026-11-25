"""Research native four-row continuation on the exact current font; not a layout approval."""
import json,struct
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from ndspy.code import MainCodeFile
from PIL import Image,ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from scripts.probe_button_prompt_native import STACK,machine
from scripts.research_online_loader_v190 import resource_call as call
from scripts.shady_man_font_oracles_v6263 import expected_pixels
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B209_native_pages_v6461')
DOC=Path('translations/lil_B209_editorial_manuscript_v1.json')
WIDTH,HEIGHT=216,64

def pages(arm,font,text):
    assert sha(arm)=='4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351'
    cpu=machine(arm);sections=MainCodeFile(arm,BASE).sections;payload=bytes(sections[3].data[:-48]);assert len(payload)==123264
    cpu.mem_write(POOL,payload);sections=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)]
    executed=set()
    def exact(u,pc,size,unused):
        owners=[s for s in sections if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)];assert len(owners)==1,hex(pc)
        s=owners[0];at=pc-s.ramAddress;assert bytes(u.mem_read(pc,size))==bytes(s.data[at:at+size]),hex(pc);executed.add(pc)
    codehook=cpu.hook_add(UC_HOOK_CODE,exact)
    header,view,ctx,string=0x02450000,0x02453000,0x02454000,0x02455000;size=WIDTH*HEIGHT//2
    raw_header=struct.pack('<5I',4,WIDTH//4,HEIGHT,0x02452000-header,20)
    cpu.mem_write(header-16,b'\xa5'*(size+52));cpu.mem_write(header,raw_header+bytes(size))
    call(cpu,0xD3D80,(view,));cpu.mem_write(STACK,struct.pack('<4I',WIDTH,HEIGHT,0,0));call(cpu,0xD3AFC,(view,header,0,0))
    metrics=struct.unpack_from('<I',arm,0xD5088)[0];cpu.mem_write(metrics+4,struct.pack('<2I',6,16));cpu.mem_write(struct.unpack_from('<I',arm,0xD19B8)[0],font)
    cpu.mem_write(string-16,b'\xa5'*(len(text)+33));cpu.mem_write(string,text+b'\0');offset=0;results=[];events=[]
    def observe(u,pc,size,unused):
        if pc in [BASE+0xD16B4,0x01FF83AC]:
            code,style=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8));events.append(dict(kind='ascii' if pc==BASE+0xD16B4 else 'cp932',code=code,style=style,x=u.reg_read(UC_ARM_REG_R2),y=u.reg_read(UC_ARM_REG_R3)))
    hook=cpu.hook_add(UC_HOOK_CODE,observe)
    try:
        while offset<len(text):
            assert len(results)<8;events.clear();cpu.mem_write(header+20,bytes(size));call(cpu,0xD5160,(ctx,view,1));call(cpu,0xD5404,(ctx,string+offset))
            end=cpu.reg_read(UC_ARM_REG_R0)-string;assert offset<end<=len(text),(offset,end,len(text))
            pixels=bytes(n for b in cpu.mem_read(header+20,size) for n in [b&15,b>>4]);expected=expected_pixels(arm,font,events)
            assert pixels==expected and bytes(cpu.mem_read(header,20))==raw_header
            assert bytes(cpu.mem_read(string,len(text)+1))==text+b'\0'
            for at in [header-16,header+20+size,string-16,string+len(text)+1]:assert bytes(cpu.mem_read(at,16))==b'\xa5'*16
            visible=[e for e in events if e['code']!=32];assert visible and len(visible)==len({(e['x'],e['y']) for e in visible})
            assert all(0<=e['x']<=210 and e['y'] in [0,16,32,48] for e in visible)
            results.append(dict(page=len(results)+1,start=offset,end=end,consumed_hex=text[offset:end].hex(),events=list(events),native_plane_hex=pixels.hex(),native_independent_plane_equal=True,first_visible_origin=[visible[0]['x'],visible[0]['y']],all_bitmap_header_input_canaries_exact=True))
            offset=end
    finally:cpu.hook_del(hook);cpu.hook_del(codehook)
    assert [e['code'] for r in results for e in r['events'] if e['code']!=32]==[v for v in text if v not in [32,10]]
    return dict(pages=results,total_bytes=len(text),complete_consumed_bytes=offset,all_visible_first_internal_final_characters_in_order=True,no_blank_or_overlap_page=True,current_instruction_addresses=len(executed))

if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');font=image.read_file('/GRP/KANJI.FNT');row=doc['records'][0]
    assert row['id']=='DK4_MES_B209_R0027' and len(row['english'].split('}',1)[1])==182
    profile=replace(get_dialogue_profile('lil-opening-editorial-native-v1'),name='B209-native-pagination-RESEARCH-ONLY',max_lines=8,leading_speaker_bytes=frozenset([2,11,12,208]))
    encoded=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile);body=encoded.encoded[1:];ROOT.mkdir(parents=True)
    save(ROOT/'research_input.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),id=row['id'],English=row['english'],compiled_hex=encoded.encoded.hex(),formatted_markup=encoded.formatted_markup,diagnostics=[dict(code=d.code,message=d.message,severity=d.severity) for d in encoded.diagnostics],research_max_total_rows8_not_changed_native_four_row_viewport=True,not_approved_layout_profile=True))
    proof=pages(arm,font,body);pics=[]
    for p in proof['pages']:
        pixels=bytes.fromhex(p.pop('native_plane_hex'));path=ROOT/f'page{p["page"]}_complete_native_216x64.bin';path.write_bytes(pixels);p.update(native_plane=str(path),native_plane_sha256=sha(pixels))
        picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};picture.putdata([colors[v] for v in pixels]);pics.append(picture)
    sheet=Image.new('RGB',(648,125*len(pics)),'#263238');draw=ImageDraw.Draw(sheet)
    for i,p in enumerate(pics):draw.text((3,i*125+3),f'B209 first letter native page{i+1}',fill='white');sheet.paste(p.resize((648,192),Image.Resampling.NEAREST),(0,i*125+22))
    # Full-size separate pages are authoritative; sheet only supplies a readable overview.
    for i,p in enumerate(pics):p.save(ROOT/f'page{i+1}_complete_native.png')
    sp=ROOT/'native_pages_overview.png';sheet.save(sp)
    save(ROOT/'complete_current_native_four_row_pages_research.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),input=str(ROOT/'research_input.json'),input_sha256=sha((ROOT/'research_input.json').read_bytes()),**proof,review_sheet=str(sp),review_sheet_sha256=sha(sp.read_bytes()),only_original_D5404_four_row_renderer_resumed_at_exact_return_pointer=True,original216x64_viewport6px_font16px_pitch_current_code_and_guards_unchanged=True,native_page_renderer_complete_not_actual_progressive_button_input_or_scene_observation=True,earlier_live_pagination_lead='work/analysis/dialogue_pagination_v288/actual_page_proof.json',current_actual_two_page_scene_transition_still_required=True,prose_wrap_weak_endings_page_boundary_and_footer_editorial_approval_pending=True,new_review_credit=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print([(p['page'],p['start'],p['end'],p['first_visible_origin']) for p in proof['pages']]);print('All182 English characters preserved across original native pages;current actual button/page behavior and editorial wrapping remain pending.')
