"""Current13-paragraph native macro/alignment andcomplete progressive glyph proof."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.modal_cursor_guard import buffered_helper
from dk4tool.patch.common_dialogue_alignment import paint
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_name_catalog_glyphs_v278 import raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B24_fonts_v1826')
DOC=Path('translations/lil_trade_routes_officers_editorial_manuscript_v2.json')
ROM=Path('out/all_routes_combined_v1807_candidate.nds')
INPUT,OUTPUT=0x02660000,0x02662000

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    doc=read(DOC);image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin')
    inventory=read('work/analysis/lil_followup_inventory_v1821b/source_event_state_and_dependency_inventory.json')
    raw=Path(inventory['historical_verified_snapshot']).read_bytes();assert sha(raw)==inventory['snapshot_sha256']
    assert sha(ROM.read_bytes())==doc['current_ROM_sha256']
    cpu,get=get_machine(arm,raw);actors=get(0xCB184);captain=actors+0x19E4
    assert get(0x7F244)==2 and get(0x2434C,9)==9
    word=struct.unpack_from('<I',arm,0xD5544)[0];rel=word&0xFFFFFF;rel=rel-(1<<24)if rel&(1<<23)else rel
    helper=0x020D5544+8+4*rel;implementation=buffered_helper(helper)
    assert bytes(cpu.mem_read(helper,len(implementation)))==implementation
    itcm=MainCodeFile(arm,0x02000000).sections[4]
    word=struct.unpack_from('<I',itcm.data,0xF24)[0];assert word>>24==0xEA
    rel=word&0xFFFFFF;rel=rel-(1<<24)if rel&(1<<23)else rel
    alignment=0x01FFCF24+8+4*rel;alignment_bytes=paint(alignment,alignment-4)
    assert bytes(cpu.mem_read(alignment-4,4))==b'  \0\0'
    assert bytes(cpu.mem_read(alignment,len(alignment_bytes)))==alignment_bytes
    profile=get_dialogue_profile('lil-opening-editorial-native-v1');cases=[];failures=[];pictures=[]
    boundary=cpu.hook_add(UC_HOOK_CODE,lambda u,a,z,d:u.reg_write(UC_ARM_REG_PC,0x027E0000),begin=0x020242CC,end=0x020242CC)
    try:
        for row in doc['records']:
            try:
                result=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'].removesuffix('{PAD}'),profile)
                prefix=int(row['source_presentation_prefix_hex'],16);assert result.encoded[0]==prefix
                actor_ID=get(0x2434C,prefix);actor=captain if actor_ID==2 else actors+4+actor_ID*32
                wrapped=result.encoded[1:]
                logical=row['english'].removesuffix('{PAD}').split('}',1)[1].replace('{MACRO:FI}','FI').encode('ascii')
                checks=[]
                for kind,value in(('logical',logical),('wrapped',wrapped)):
                    expected=value.replace(b'FI',b'Lil')
                    for phase in range(4):
                        cpu.mem_write(INPUT-16,b'\xA5'*2080);cpu.mem_write(INPUT+phase,value+b'\0')
                        before=bytes(cpu.mem_read(INPUT-16,2080));cpu.mem_write(OUTPUT-16,b'\xA5'*4128)
                        call(cpu,0x242C8,(OUTPUT,INPUT+phase,actor),instruction_limit=400000)
                        output=bytes(cpu.mem_read(OUTPUT,4096)).split(b'\0')[0]
                        assert output==expected
                        assert bytes(cpu.mem_read(0x02000000,0x400000))==raw and bytes(cpu.mem_read(INPUT-16,2080))==before
                        assert bytes(cpu.mem_read(OUTPUT-16,16))==b'\xA5'*16
                        assert bytes(cpu.mem_read(OUTPUT+len(output)+1,4095-len(output)))==b'\xA5'*(4095-len(output))
                        checks.append({'kind':kind,'alignment':phase,'output_hex':output.hex(),'all4MiB_ABI_input_output_guards_exact':True})
                expected=wrapped.replace(b'FI',b'Lil');pixels,events,font=raster(arm,expected)
                assert pixels==expected_pixels(arm,font,events)
                assert[e['code']for e in events if e['code']!=32]==[ord(c)for c in expected.decode('ascii')if c not in' \n']
                visible=[e for e in events if e['code']!=32]
                assert all(0<=e['x']<=210 and 0<=e['y']<=48 for e in visible)
                assert len(visible)==len({(e['x'],e['y'])for e in visible})
                origins={y:min(e['x']for e in visible if e['y']==y)for y in sorted({e['y']for e in visible})}
                assert all(x==0 for x in origins.values())
                im=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
                im.putdata([colors[p]for p in pixels]);path=ROOT/(row['id']+'.png');im.save(path)
                pictures.append((row['id'],row['speaker'],im))
                cases.append({'id':row['id'],'encoded_hex':result.encoded.hex(),'native_expanded_hex':expected.hex(),
                    'formatted_markup':result.formatted_markup,'macro_cases':checks,'glyphs':events,
                    'whole_native_independent_font_plane_exact':True,'native_font_plane_sha256':sha(pixels),
                    'all_glyphs_complete_in_order_unique_cells_within216x64':True,'visible_origins_by_native_row':origins,
                    'all_continuation_visible_origins_equal_first_row_zero':True,
                    'diagnostics':[{'severity':d.severity,'code':d.code,'message':d.message}for d in result.diagnostics],
                    'preview':str(path),'preview_sha256':sha(path.read_bytes())})
            except(ValueError,AssertionError)as error:failures.append({'id':row['id'],'error':str(error),'type':type(error).__name__})
    finally:cpu.hook_del(boundary)
    sheets=[]
    for start in range(0,len(pictures),8):
        sheet=Image.new('RGB',(920,640),'#263238');draw=ImageDraw.Draw(sheet)
        for k,(ident,speaker,im)in enumerate(pictures[start:start+8]):
            x,y=460*(k%2),160*(k//2);draw.text((x+5,y+3),ident+' / '+speaker,fill='white')
            sheet.paste(im.resize((432,128),Image.Resampling.NEAREST),(x+5,y+24))
        path=ROOT/f'review_sheet_{start//8+1:02d}.png';sheet.save(path);sheets.append({'path':str(path),'sha256':sha(path.read_bytes())})
    save(ROOT/'all13_native_macros_and_complete_font_planes.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'ARM9_sha256':sha(arm),'manuscript':str(DOC),'manuscript_sha256':sha(DOC.read_bytes()),'cases':cases,'failures':failures,
        'source_snapshot':inventory['historical_verified_snapshot'],'source_snapshot_sha256':sha(raw),
        'existing_cursor_helper':helper,'existing_cursor_helper_hex':implementation.hex(),
        'existing_alignment_helper':alignment,'existing_alignment_helper_hex':alignment_bytes.hex(),
        'source_helper_contract_established_before_font_positions_not_fitted_to_glyphs':True,
        'review_sheets':sheets,'native_macro_calls':sum(len(r['macro_cases'])for r in cases),
        'actual_B24_activation_andfull_scene_still_pending':True,'not_a_ROM_or_whole_GPU_orhardware_proof':True,
        'visual_review_pending':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'native_font_cases':len(cases),'native_macro_calls':sum(len(r['macro_cases'])for r in cases),'failures':failures},flush=True)
