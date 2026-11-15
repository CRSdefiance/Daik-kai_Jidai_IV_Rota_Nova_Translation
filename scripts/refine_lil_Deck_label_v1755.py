"""Match the actual Deck View menu label; recheck only this changed FE paragraph."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import struct
from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_Deck_label_v1755')
OLD=Path('translations/lil_lessons_editorial_manuscript_v3.json')
OUT=Path('translations/lil_lessons_editorial_manuscript_v4.json')
IDENT='DK4_MES_B23_R0166'

if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    doc=deepcopy(read(OLD)); original=deepcopy(doc)
    row=next(r for r in doc['records'] if r['id']==IDENT)
    row['english']="{SPEAKER:FE}Press X and choose Deck View from the menu. On the Deck screen, you can change each officer's post."
    row['localization_note']+=' Use the exact visible sailing-menu label Deck View;the screen title itself remains Deck. Actual original menu capture is V1745frame32530.'
    row['review']['formatting']=False
    row['actual_revised_gameplay_and_registered_release_pending']=True
    for key in ('compiled_hex','formatted_markup','formatting_evidence','qa_waivers','qa_waiver_reason'):
        row.pop(key,None)
    assert [a['id'] for a,b in zip(doc['records'],original['records'],strict=True) if a!=b]==[IDENT]
    arm=NdsImage.open(doc['current_ROM']).read_file('/__arm9__.bin')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    panel=replace(base,name='lil-lessons-FE-runtime-bound-v1',leading_speaker_bytes=base.leading_speaker_bytes|frozenset({254}))
    compiled=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],panel)
    value=compiled.encoded[1:]
    assert compiled.encoded[0]==254 and b'FI' not in value
    raw=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_lessons_revised_v1741_RESEARCH_ONLY/final_arm9_ram.bin').read_bytes()
    cpu,get=get_machine(arm,raw); actor=get(0xCB184)+0x19E4
    hook=cpu.hook_add(UC_HOOK_CODE,lambda u,a,z,d:u.reg_write(UC_ARM_REG_PC,0x027E0000),begin=0x020242CC,end=0x020242CC)
    try:
        for alignment in range(4):
            cpu.mem_write(0x02660000-16,b'\xA5'*2080);cpu.mem_write(0x02660000+alignment,value+b'\0')
            before=bytes(cpu.mem_read(0x02660000-16,2080));cpu.mem_write(0x02662000-16,b'\xA5'*4128)
            call(cpu,0x242C8,(0x02662000,0x02660000+alignment,actor),instruction_limit=300000)
            assert bytes(cpu.mem_read(0x02662000,len(value)+1))==value+b'\0'
            assert bytes(cpu.mem_read(0x02000000,0x400000))==raw
            assert bytes(cpu.mem_read(0x02660000-16,2080))==before
            assert bytes(cpu.mem_read(0x02662000-16,16))==b'\xA5'*16
            assert bytes(cpu.mem_read(0x02662000+len(value)+1,4096-len(value)-1))==b'\xA5'*(4096-len(value)-1)
    finally:cpu.hook_del(hook)
    obs_path=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_modal_context_v1734_1711/modal_observer/actual_modal_contexts.json')
    obs=read(obs_path); captured=next(r for r in obs['rows'] if r.get('complete_readonly_snapshots'))
    snapshots={k:Path(v['path']).read_bytes() for k,v in captured['complete_readonly_snapshots'].items()}
    for k,v in captured['complete_readonly_snapshots'].items():assert sha(snapshots[k])==v['sha256']
    prior=read('work/analysis/lil_FE_display_v1737/actual_paper_contract_and_all9_reviewed_FE_panels.json')
    assert prior['same_mode1_context_geometry_clip_spacing_and_font_metrics_confirmed_by_readonly_capture']
    descriptor=struct.unpack('<25I',bytes.fromhex(captured['bitmap_100_hex']))[4]
    header=struct.unpack_from('<5I',snapshots['WRAM'],descriptor-0x02000000)
    assert header[0]&255==4 and list(header[1:3])==[72,48]
    pixels_address=(descriptor+header[4])&0xFFFFFFFF
    font=GameAsciiFont.from_arm9(arm)
    old=bytes.fromhex(row['current_text_hex']); target=compiled.encoded
    if len(target)%2!=len(old)%2:target+=b' '
    cases=[]; physical=None
    for label,body in [('compiled',value),('parity_storage',target[1:])]:
        native=machine(arm);native.mem_write(0x02000000,snapshots['WRAM']);native.mem_write(0x01FF8000,snapshots['ITCM'])
        native.mem_write(captured['DTCM_base'],snapshots['DTCM']);native.mem_map(0x06000000,0x800000)
        inp=0x02660000;native.mem_write(inp-16,b'\xA5'*(len(body)+33));native.mem_write(inp,body+b'\0');events=[]
        def glyph(u,address,size,_):
            code,style=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8))
            events.append({'code':code,'style':style,'x':u.reg_read(UC_ARM_REG_R2),'y':u.reg_read(UC_ARM_REG_R3)})
        hook=native.hook_add(UC_HOOK_CODE,glyph,begin=0x020D16B4,end=0x020D16B4)
        try:call(native,0x01FFCE40-0x02000000,(captured['context'],inp),instruction_limit=1000000)
        finally:native.hook_del(hook)
        assert native.reg_read(UC_ARM_REG_R0)==inp+len(body)
        assert bytes(native.mem_read(inp,len(body)+1))==body+b'\0'
        assert bytes(native.mem_read(inp-16,16))==bytes(native.mem_read(inp+len(body)+1,16))==b'\xA5'*16
        visible=[e for e in events if e['code']!=32]
        assert [e['code'] for e in visible]==[c for c in body if c not in (32,10)]
        assert len(visible)==len({(e['x'],e['y']) for e in visible})
        assert all(0<=e['x']<=222 and e['y']%12==0 and 0<=e['y']<=36 for e in visible)
        expected=bytearray(288*48); display=bytearray(228*64)
        for e in visible:
            char=font.decode(chr(e['code']))
            for y in range(11):
                for x in range(6):
                    if char.getpixel((x,y)):
                        expected[(e['y']+y)*288+e['x']+x]=e['style']
                        display[(e['y']//12*16+y)*228+e['x']+x]=1
        actual=bytes(n for b in native.mem_read(pixels_address,72*2*48) for n in (b&15,b>>4))
        assert actual==bytes(expected)
        if physical is not None:assert physical==bytes(display)
        physical=bytes(display)
        cases.append({'label':label,'body_hex':body.hex(),'glyphs':events,'complete_one_page_and_independent_plane_exact':True})
    ROOT.mkdir(parents=True)
    preview=Image.new('RGB',(228,64));preview.putdata([(0,8,0) if v else (239,232,201) for v in physical])
    path=ROOT/(IDENT+'_display.png');preview.save(path)
    doc.update(formatting_review_pending=True,status='59-native-layout-approved;Deck-View-menu-label-refinement-native-proved-visual-approval-pending',
               native_label_refinement_proof=str(ROOT/'Deck_View_label_native_proof.json'))
    save(OUT,doc)
    save(ROOT/'Deck_View_label_native_proof.json',{'source_manuscript':str(OLD),'source_sha256':sha(OLD.read_bytes()),
        'draft_manuscript':str(OUT),'draft_sha256':sha(OUT.read_bytes()),'only_changed_id':IDENT,
        'actual_menu_capture':'E:/Rota Nova translations/Generated/work/emulation_v193/lil_lesson_navigation_v1745_RESEARCH_ONLY/frame_032530_navigation.png',
        'clean_source_meaning_and_all59_other_paragraphs_unchanged':True,'four_macro_alignment_ABI_4MiB_and_guards_pass':True,
        'encoded_hex':compiled.encoded.hex(),'storage_target_hex':target.hex(),'formatted_markup':compiled.formatted_markup,
        'diagnostics':[{'severity':d.severity,'code':d.code,'message':d.message} for d in compiled.diagnostics],
        'cases':cases,'preview':str(path),'preview_sha256':sha(path.read_bytes()),
        'captured_actual_FE_context_replayed_source12_to_display16_contract':True,
        'explicit_zero_VRAM_offline_initialization_not_actual_GPU_trace':True,
        'visual_approval_actual_revised_text_and_new_research_ROM_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'only_refined':IDENT,'formatted':compiled.formatted_markup,'four_native_macro_cases_and_both_native_planes':True})
