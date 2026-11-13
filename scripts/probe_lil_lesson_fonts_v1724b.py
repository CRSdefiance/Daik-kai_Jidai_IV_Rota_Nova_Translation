"""Scoped research:51 progressive bodies and9 original FE modal bodies."""
from dataclasses import replace
import inspect
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_LR,UC_ARM_REG_R0

from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.modal_cursor_guard import buffered_helper
from dk4tool.rom.nds import NdsImage
from scripts import execute_scene_caption_raster as modal
from scripts.native_call_abi_v764 import call
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_name_catalog_glyphs_v278 import raster,expected_pixels
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels as modal_expected
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_lesson_fonts_v1724b')
MANUSCRIPT=Path('translations/lil_lessons_editorial_manuscript_v1.json')
ROM=Path('out/all_routes_combined_v1711_candidate.nds')
SNAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_opening_trace_v1706_RESEARCH_ONLY/final_arm9_ram.bin')
INPUT,OUTPUT=0x02660000,0x02662000


if __name__=='__main__':
    assert not ROOT.exists()
    doc=read(MANUSCRIPT);image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin');raw=SNAP.read_bytes()
    assert sha(ROM.read_bytes())==doc['current_ROM_sha256']
    cpu,get=get_machine(arm,raw);actors=get(0xCB184);captain=actors+0x19E4
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    # Local research instance only. No global profile,old source guard or production byte changes.
    panel=replace(base,name='lil-lessons-FE-local-research-v1',leading_speaker_bytes=base.leading_speaker_bytes|frozenset({254}))
    word=struct.unpack_from('<I',arm,0xD5544)[0];delta=word&0xFFFFFF
    if delta&(1<<23):delta-=1<<24
    helper=0x020D5544+8+4*delta;implementation=buffered_helper(helper)
    assert bytes(cpu.mem_read(helper,len(implementation)))==implementation
    staged=bytes(MainCodeFile(arm,0x02000000).sections[3].data[:-48])
    itcm=MainCodeFile(arm,0x02000000).sections[4]
    assert itcm.ramAddress==0x01FFC000 and len(itcm.data)==4096
    # Frozen modal harness lacks staged cursor-helper initialization. Add exactly that
    # source-verified pool and whitelist exactly that helper;keep every other gate.
    source=inspect.getsource(modal.execute)
    anchor='    item_helper_ranges, item_helper_executed = [], set()\n'
    addition=('    if modal:\n'
        '        machine.mem_write(0x02387A20, MODAL_STAGED)\n'
        '        machine.mem_write(MODAL_ITCM_START, MODAL_ITCM)\n'
        '        item_helper_ranges.append((MODAL_ITCM_START, MODAL_ITCM_START+len(MODAL_ITCM)))\n'
        '        item_helper_ranges.append((MODAL_CURSOR, MODAL_CURSOR+len(MODAL_CURSOR_BYTES)))\n'
        '        assert bytes(machine.mem_read(MODAL_CURSOR,len(MODAL_CURSOR_BYTES))) == MODAL_CURSOR_BYTES\n')
    assert source.count(anchor)==1;source=source.replace(anchor,anchor+addition,1)
    env={**modal.__dict__,'MODAL_STAGED':staged,'MODAL_CURSOR':helper,'MODAL_CURSOR_BYTES':implementation,'MODAL_ITCM_START':itcm.ramAddress,'MODAL_ITCM':bytes(itcm.data)}
    exec(compile(source,'scoped_modal_cursor_initialization_v1724','exec'),env)
    modal_execute=env['execute']
    ROOT.mkdir(parents=True);(ROOT/'scoped_modal_adapter_source.txt').write_text(source,encoding='utf-8')
    cases=[];failures=[];pictures=[];dispatch=[]
    boundary=cpu.hook_add(UC_HOOK_CODE,lambda u,a,z,d:u.reg_write(UC_ARM_REG_PC,0x027E0000),begin=0x020242CC,end=0x020242CC)
    try:
        for row in doc['records']:
            try:
                is_panel=row['source_presentation_prefix_hex']=='fe'
                text=row['english'].replace('{PAD}','')
                compiled=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),text,panel if is_panel else base)
                value=compiled.encoded[1:];expected=value.replace(b'FI',b'Lil')
                speaker=int(row['source_presentation_prefix_hex'],16)
                actor_ID=None if is_panel else get(0x2434C,speaker)
                actor=0 if is_panel else captain if actor_ID==2 else actors+4+actor_ID*32
                for alignment in range(4):
                    cpu.mem_write(INPUT-16,b'\xA5'*2080);cpu.mem_write(INPUT+alignment,value+b'\0')
                    before=bytes(cpu.mem_read(INPUT-16,2080));cpu.mem_write(OUTPUT-16,b'\xA5'*4128)
                    call(cpu,0x242C8,(OUTPUT,INPUT+alignment,actor),instruction_limit=300000)
                    output=bytes(cpu.mem_read(OUTPUT,4096)).split(b'\0')[0]
                    assert output==expected and bytes(cpu.mem_read(0x02000000,0x400000))==raw
                    assert bytes(cpu.mem_read(INPUT-16,2080))==before
                    assert bytes(cpu.mem_read(OUTPUT-16,16))==b'\xA5'*16
                    assert bytes(cpu.mem_read(OUTPUT+len(output)+1,4096-len(output)-1))==b'\xA5'*(4096-len(output)-1)
                if is_panel:
                    result=modal_execute(arm,expected.decode('ascii'),modal=True,modal_guarded=True,
                        audit_modal_legacy_guards=True,mode=16)
                    events=result['glyph_events'];pixels=result['pixels']
                    assert pixels==modal_expected(arm,None,events,16,background=9)
                    assert {0x548A8,0xD5404,0xD16B4}<=set(result['executed_offsets'])
                    assert all(0<=e['x']<=250 and 0<=e['y']<=84 for e in events if e['code']!=32)
                    im=Image.new('RGB',(256,192))
                    im.putdata([(239,232,201) if p==9 else (0,8,0) for p in struct.unpack('<49152H',pixels)])
                    im=im.crop((0,0,256,96));kind='original_FE_modal_548A8'
                else:
                    pixels,events,font=raster(arm,expected)
                    assert pixels==expected_pixels(arm,font,events)
                    assert all(0<=e['x']<=210 and 0<=e['y']<=48 for e in events if e['code']!=32)
                    im=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
                    im.putdata([colors[v] for v in pixels]);kind='progressive_complete_font_plane'
                assert [e['code'] for e in events if e['code']!=32]==[ord(c) for c in expected.decode('ascii') if c not in ' \n']
                visible=[e for e in events if e['code']!=32]
                assert len(visible)==len({(e['x'],e['y']) for e in visible})
                path=ROOT/(row['id']+'.png');im.save(path);pictures.append((row['id'],row['speaker'],im))
                cases.append({'id':row['id'],'consumer':kind,'encoded_hex':compiled.encoded.hex(),
                    'native_expanded_hex':expected.hex(),'formatted_markup':compiled.formatted_markup,
                    'diagnostics':[{'severity':d.severity,'code':d.code,'message':d.message} for d in compiled.diagnostics],
                    'all4_macro_alignments_ABI_full4MiB_and_input_output_guards_exact':True,
                    'whole_native_and_independent_font_plane_exact':True,
                    'complete_printable_glyph_order_unique_cells_and_bounds_verified':True,
                    'glyphs':events,'native_font_plane_sha256':sha(pixels),
                    'preview':str(path),'preview_sha256':sha(path.read_bytes())})
            except (ValueError,AssertionError) as error:
                failures.append({'id':row['id'],'error':str(error),'type':type(error).__name__})
    finally:cpu.hook_del(boundary)
    # Execute the original FE dispatcher including its actual native catalog/macro call.
    for row in doc['records']:
        if row['source_presentation_prefix_hex']!='fe':continue
        compiled=next((r for r in cases if r['id']==row['id']),None)
        if compiled is None:continue
        value=bytes.fromhex(compiled['encoded_hex'])[1:]
        cpu.mem_write(INPUT,value+b'\0');observed=[]
        def hook(u,address,size,_):
            if address==0x020940B0:u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
            elif address in (0x0205473C,0x02053AC4,0x02054020):
                pointer=u.reg_read(UC_ARM_REG_R0);body=bytes(u.mem_read(pointer,1024)).split(b'\0')[0]
                observed.append({'consumer':address,'body_hex':body.hex()})
                u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
        h=cpu.hook_add(UC_HOOK_CODE,hook)
        try:call(cpu,0x2425C,(254,INPUT),instruction_limit=300000)
        finally:cpu.hook_del(h)
        assert observed==[{'consumer':0x0205473C,'body_hex':value.hex()}]
        assert bytes(cpu.mem_read(0x02000000,0x400000))==raw
        dispatch.append({'id':row['id'],'original_FE_dispatch_and_current_catalog_macro_executed':True,
            'consumer':0x0205473C,'UI_state_update_and_modal_parent_call_are_explicit_bridges':True,
            'body_hex':value.hex(),'full4MiB_and_ABI_preserved':True})
    sheets=[]
    for start in range(0,len(pictures),8):
        sheet=Image.new('RGB',(1080,1016),(28,36,40));draw=ImageDraw.Draw(sheet)
        for n,(ident,speaker,im) in enumerate(pictures[start:start+8]):
            x,y=8+536*(n%2),6+252*(n//2);draw.text((x,y),ident+' '+speaker,fill='white')
            sheet.paste(im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST),(x,y+22))
        path=ROOT/f'review_sheet_{start//8+1:02d}.png';sheet.save(path)
        sheets.append({'path':str(path),'sha256':sha(path.read_bytes())})
    save(ROOT/'native_consumer_and_font_research.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'ARM9_sha256':sha(arm),'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'cases':cases,'failures':failures,'FE_dispatch_cases':dispatch,'review_sheets':sheets,
        'native_staged_cursor_helper':helper,'native_staged_cursor_helper_hex':implementation.hex(),
        'modal_harness_added_exact_staged_copy_cursor_helper_and_source_ITCM_section4':True,
        'source_ITCM_section4_sha256':sha(bytes(itcm.data)),
        'predecessor_1724_rejected_FE_due_to_missing_existing_ITCM_alignment_wrapper':True,
        'frozen_modal_harness_sha256':sha(Path(modal.__file__).read_bytes()),
        'local_FE_profile_does_not_change_global_profiles_or_release_guards':True,
        'visual_review_pending':True,'native_branch_relocation_registered_release_and_actual_revised_gameplay_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'native_font_cases':len(cases),'FE_dispatch_cases':len(dispatch),'failures':failures,'sheets':len(sheets)},flush=True)
