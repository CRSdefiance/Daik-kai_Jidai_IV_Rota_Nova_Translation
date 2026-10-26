"""Refine one conditional explanation and recheck only its changed native plane."""
from copy import deepcopy
from pathlib import Path
from PIL import Image,ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC

from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_name_catalog_glyphs_v278 import raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_lesson_layout_v1725')
OLD=Path('translations/lil_lessons_editorial_manuscript_v1.json')
OUT=Path('translations/lil_lessons_editorial_manuscript_v2.json')
PRIOR=Path('work/analysis/lil_lesson_fonts_v1724c/native_consumer_and_font_research.json')


if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    prior=read(PRIOR);doc=read(OLD);before=deepcopy(doc)
    assert not prior['failures'] and len(prior['cases'])==60 and len(prior['FE_dispatch_cases'])==9
    assert sha(OLD.read_bytes())==prior['manuscript_sha256']
    row=next(r for r in doc['records'] if r['id']=='DK4_MES_B23_R0069')
    row['english']='{SPEAKER:09}At Half Open, the Sail Handlers adjust the sails automatically.{PAD}'
    row['localization_note']='Use the exact current Half Open setting and Sail Handler role. State the original conditional rule directly;the complete predicate stays together instead of leaving automatically on its own final row. No source mechanic is omitted.'
    assert len([1 for a,b in zip(doc['records'],before['records'],strict=True) if a!=b])==1
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin')
    snap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_opening_trace_v1706_RESEARCH_ONLY/final_arm9_ram.bin');raw=snap.read_bytes()
    cpu,get=get_machine(arm,raw);actors=get(0xCB184);actor_ID=get(0x2434C,9);actor=actors+4+actor_ID*32
    compiled=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'].replace('{PAD}',''),get_dialogue_profile('lil-opening-editorial-native-v1'))
    value=compiled.encoded[1:];assert b'FI' not in value
    hook=cpu.hook_add(UC_HOOK_CODE,lambda u,a,z,d:u.reg_write(UC_ARM_REG_PC,0x027E0000),begin=0x020242CC,end=0x020242CC)
    try:
        for alignment in range(4):
            cpu.mem_write(0x02660000-16,b'\xA5'*2080);cpu.mem_write(0x02660000+alignment,value+b'\0')
            source=bytes(cpu.mem_read(0x02660000-16,2080));cpu.mem_write(0x02662000-16,b'\xA5'*4128)
            call(cpu,0x242C8,(0x02662000,0x02660000+alignment,actor),instruction_limit=300000)
            assert bytes(cpu.mem_read(0x02662000,len(value)+1))==value+b'\0'
            assert bytes(cpu.mem_read(0x02000000,0x400000))==raw
            assert bytes(cpu.mem_read(0x02660000-16,2080))==source
            assert bytes(cpu.mem_read(0x02662000-16,16))==b'\xA5'*16
            assert bytes(cpu.mem_read(0x02662000+len(value)+1,4096-len(value)-1))==b'\xA5'*(4096-len(value)-1)
    finally:cpu.hook_del(hook)
    pixels,events,font=raster(arm,value);assert pixels==expected_pixels(arm,font,events)
    assert [e['code'] for e in events if e['code']!=32]==[ord(c) for c in value.decode('ascii') if c not in ' \n']
    assert all(0<=e['x']<=210 and 0<=e['y']<=48 for e in events if e['code']!=32)
    assert len(value.split(b'\n'))==2
    ROOT.mkdir(parents=True);im=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
    im.putdata([colors[v] for v in pixels]);path=ROOT/(row['id']+'.png');im.save(path)
    cases=deepcopy(prior['cases']);case=next(r for r in cases if r['id']==row['id'])
    case.update(encoded_hex=compiled.encoded.hex(),native_expanded_hex=value.hex(),formatted_markup=compiled.formatted_markup,
        diagnostics=[{'severity':d.severity,'code':d.code,'message':d.message} for d in compiled.diagnostics],glyphs=events,
        native_font_plane_sha256=sha(pixels),preview=str(path),preview_sha256=sha(path.read_bytes()))
    for r in cases:
        assert sha(Path(r['preview']).read_bytes())==r['preview_sha256']
    doc.update(native_font_research=str(ROOT/'all60_native_font_reconciliation.json'),
        status='60-source-prose-and-native-font-reviewed;visual-refinement-branch-relocation-release-and-actual-pending')
    save(OUT,doc)
    # Recreate only the one changed sheet;the other seven reviewed sheets remain exact.
    sheet=Image.new('RGB',(1080,1016),(28,36,40));draw=ImageDraw.Draw(sheet)
    for n,r in enumerate(cases[32:40]):
        x,y=8+536*(n%2),6+252*(n//2);speaker=next(v['speaker'] for v in doc['records'] if v['id']==r['id'])
        draw.text((x,y),r['id']+' '+speaker,fill='white')
        picture=Image.open(r['preview']).convert('RGB');sheet.paste(picture.resize((picture.width*2,picture.height*2),Image.Resampling.NEAREST),(x,y+22))
    sheet_path=ROOT/'review_sheet_05_refined.png';sheet.save(sheet_path)
    sheets=deepcopy(prior['review_sheets']);sheets[4]={'path':str(sheet_path),'sha256':sha(sheet_path.read_bytes())}
    save(ROOT/'all60_native_font_reconciliation.json',{'manuscript':str(OUT),'manuscript_sha256':sha(OUT.read_bytes()),
        'candidate':doc['current_ROM'],'candidate_sha256':doc['current_ROM_sha256'],'ARM9_sha256':sha(arm),
        'prior_native_proof':str(PRIOR),'prior_native_proof_sha256':sha(PRIOR.read_bytes()),
        'unchanged59_rows_and_compiled_planes_reused_exactly':True,'only_refined_id':row['id'],
        'four_fresh_macro_alignment_and_full_native_independent_font_cases_for_refined_row':True,
        'cases':cases,'FE_dispatch_cases':prior['FE_dispatch_cases'],'review_sheets':sheets,
        'all8_prior_sheets60_panels_actually_viewed':True,'refined_sheet_visual_review_pending':True,
        'global_profile_runtime_and_ROM_unchanged':True,'source_reference_map_choices_native_scene_release_and_actual_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Refined only B23R69 into a faithful two-line conditional;four native macro cases and complete native/independent font pass. Other59 verified planes unchanged.',flush=True)
