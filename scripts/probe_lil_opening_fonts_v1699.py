"""All49 automatic layouts through current native catalog,macro and full fonts."""
import ast
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.codec import parse_markup
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.native_call_abi_v764 import call
from scripts.verify_name_catalog_glyphs_v278 import raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_opening_fonts_v1699')
ROM=Path('out/all_routes_combined_v1676_candidate.nds')
PROOF=Path('work/analysis/lil_opening_macro_v1698d/original_story_macro_proof.json')


if __name__=='__main__':
    assert not ROOT.exists()
    proof=read(PROOF);rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin')
    assert sha(arm)==proof['ARM9_sha256'] and sha(ROM.read_bytes())==proof['ROM_sha256']
    assert rom.read_file('/GRP/KANJI.FNT')==NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT')
    raw=Path(proof['snapshot']).read_bytes();assert sha(raw)==proof['snapshot_sha256']
    cpu,get=get_machine(arm,raw);actors=get(0xCB184);captain=actors+0x19E4
    prior_path=Path('scripts/probe_lil_opening_macro_v1698d.py');tree=ast.parse(prior_path.read_text(encoding='utf-8'))
    functions=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name in ('on_write','expand')]
    assert {n.name for n in functions}=={'on_write','expand'}
    env={'cpu':cpu,'raw':raw,'INPUT':0x02660000,'OUTPUT':0x02662000,'call':call,'writes':[]}
    exec(compile(ast.Module(body=functions,type_ignores=[]),str(prior_path),'exec'),env)
    hook=cpu.hook_add(UC_HOOK_MEM_WRITE,env['on_write'])
    boundary=cpu.hook_add(UC_HOOK_CODE,lambda u,a,z,d:u.reg_write(UC_ARM_REG_PC,0x027E0000),begin=0x020242CC,end=0x020242CC)
    doc=read('translations/lil_opening_editorial_manuscript_v1.json');profile=get_dialogue_profile('lil-opening-editorial-native-v1')
    ROOT.mkdir(parents=True);cases=[];images=[]
    try:
        for row in doc['records']:
            english=row['english'].replace('{PAD}','')
            encoded=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),english,profile)
            value=encoded.encoded[1:];expected=value.replace(b'FI',b'Lil')
            speaker=int(row['source_presentation_prefix_hex'],16);actor_ID=get(0x2434C,speaker)
            actor=captain if actor_ID==2 else actors+4+actor_ID*32
            for alignment in range(4):assert env['expand'](value,actor,alignment)==expected
            pixels,events,font=raster(arm,expected)
            assert pixels==expected_pixels(arm,font,events)
            semantic=[ord(c) for c in expected.decode('ascii') if c not in ' \n']
            assert [e['code'] for e in events if e['code']!=32]==semantic
            assert all(e['kind']=='ascii' and 0<=e['x']<=210 and 0<=e['y']<=48 for e in events if e['code']!=32)
            rows=expected.decode('ascii').split('\n')
            assert len(rows)<=4
            for y,line in enumerate(rows):
                at=0;wanted=[]
                for c in line:
                    if c!=' ':wanted.append((ord(c),at,y*16))
                    at+=6
                actual=[(e['code'],e['x'],e['y']) for e in events if e['code']!=32 and e['y']==y*16]
                assert actual==wanted,(row['id'],y,actual,wanted)
            image=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
            image.putdata([colors[v] for v in pixels]);path=ROOT/(row['id']+'.png');image.save(path)
            cases.append({'id':row['id'],'speaker':row['speaker'],'original_actor_ID':actor_ID,'formatted_markup':encoded.formatted_markup,
                'encoded_hex':encoded.encoded.hex(),'native_expanded_hex':expected.hex(),'visible_lines':[s.rstrip() for s in rows],
                'line_widths_px':[len(s)*6 for s in rows],
                'diagnostics':[{'code':d.code,'severity':d.severity,'message':d.message} for d in encoded.diagnostics],
                'all4_native_macro_alignments_and_entire_memory_preserved':True,
                'complete_native_and_independent216x64_font_planes_equal':True,
                'all_printable_characters_in_order_at_independently_derived_positions':True,
                'complete_leading_trailing_letters_bounds_and_blank_paper_verified':True,
                'native_font_plane_sha256':sha(pixels),'preview':str(path),'preview_sha256':sha(path.read_bytes())})
            images.append(image)
            print(row['id'],[s.rstrip() for s in rows],flush=True)
    finally:cpu.hook_del(hook);cpu.hook_del(boundary)
    sheets=[]
    for start in range(0,49,8):
        sheet=Image.new('RGB',(920,728),(28,36,40));draw=ImageDraw.Draw(sheet)
        for k,(case,im) in enumerate(zip(cases[start:start+8],images[start:start+8],strict=True)):
            x,y=12+(k%2)*458,8+(k//2)*180
            draw.text((x,y),case['id']+' '+case['speaker'],fill='white')
            sheet.paste(im.resize((432,128),Image.Resampling.NEAREST),(x,y+26))
        path=ROOT/f'review_sheet_{start//8+1:02d}.png';sheet.save(path)
        sheets.append({'path':str(path),'sha256':sha(path.read_bytes())})
    save(ROOT/'native_font_proof.json',{'ROM':str(ROM),'ROM_sha256':proof['ROM_sha256'],'ARM9_sha256':sha(arm),
        'source_context':'work/analysis/lil_opening_editorial_v1694/complete_opening_source_context.json',
        'macro_proof':str(PROOF),'macro_proof_sha256':sha(PROOF.read_bytes()),'prior_native_expander_sha256':sha(prior_path.read_bytes()),
        'profile':profile.name,'cases':cases,'full_native_font_cases':49,'native_macro_alignment_cases':196,
        'source_control_order_and_default_FI_preserved':True,'review_sheets':sheets,'visual_review_pending':True,
        'relocation_reference_map_registered_build_exact_patch_and_actual_new_scene_pending':True,
        'no_ROM_or_gameplay_state_changed':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('All49 layouts and full native/independent font planes pass;196 wrapped macro cases preserve memory. Seven visual sheets await review;no integration/gameplay credit.')
