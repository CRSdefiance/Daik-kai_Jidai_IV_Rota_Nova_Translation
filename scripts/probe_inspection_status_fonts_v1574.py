"""Full original modal pipelines and independent native font planes for306/307."""
import struct
from copy import deepcopy
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_PC,UC_ARM_REG_SP,UC_ARM_REG_LR
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_escape_direct_source_v1186 import machine
from scripts.probe_button_prompt_native import STACK,STOP
from scripts.inspection_status_native_plan_v1573 import compiled
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/inspection_status_fonts_v1574')
PLAN=Path('work/analysis/inspection_status_payload_v1573/native_payload_plan.json')
DOC=Path('translations/inspection_status_editorial_manuscript_v1.json')
BASE=0x02000000

def pipeline(arm,common,raw,plan,number):
    cpu,get,provider=machine(arm,common,raw,plan);seen={}
    def observe(u,pc,size,data):
        if pc==BASE+0x54788:
            ptr=u.reg_read(UC_ARM_REG_R1)
            seen.update(loaded_template_hex=bytes(u.mem_read(ptr,256)).split(b'\0')[0].hex(),original_template_pointer=ptr)
        elif pc==BASE+0x54798:
            sp=u.reg_read(UC_ARM_REG_SP)
            seen['original_wrapper_parent']=struct.unpack('<I',u.mem_read(sp+0xc4,4))[0]
        else:
            out=struct.unpack_from('<I',arm,0x54894)[0]
            seen['formatted_hex']=bytes(u.mem_read(out,256)).split(b'\0')[0].hex();u.emu_stop()
    for pc in [BASE+0x54788,BASE+0x54798,BASE+0x5479C]:cpu.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
    cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP);cpu.reg_write(UC_ARM_REG_R0,number)
    cpu.emu_start(BASE+0x546B8,STOP,count=3000000)
    assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0x5479C and seen['original_wrapper_parent']==BASE+0x546E8
    return {**seen,'message_ID':number,'original_entry':BASE+0x546B8,'original_loader_varargs_macro_and_registered_hooks_execute':True,
        'file_reads':provider.reads,'file_opens':provider.opens,'CPU_boundary':'Host successful file IO;stop before original modal UI constructor,not actual gameplay.'}

def literal_independent(arm,kanji,text):
    shifted=independent_font(arm,kanji,[text])
    assert all(not any(shifted[y*228:y*228+6]) for y in range(64))
    return b''.join(shifted[y*228+6:(y+1)*228]+bytes(6) for y in range(64))

if __name__=='__main__':
    assert not ROOT.exists()
    plan,doc=read(PLAN),read(DOC)
    assert plan['manuscript_sha256']==sha(DOC.read_bytes())
    arm,common=Path(plan['target_ARM9']).read_bytes(),Path(plan['target_COMMON']).read_bytes()
    rom=NdsImage.open(doc['current_ROM'])
    raw=Path('E:/Rota Nova translations/Generated/work/emulation_v193/sea_inspection_final_v1567d_1563/frame_006100_arm9_ram.bin').read_bytes()
    class CurrentFont:
        @staticmethod
        def open(path):
            assert path=='out/all_routes_combined_v255_candidate.nds';return rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    assert not any(raster(arm,b' ',0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000))
    ROOT.mkdir(parents=True);cases=[]
    sheet=Image.new('RGB',(936,154),'#263238');draw=ImageDraw.Draw(sheet)
    for j,row in enumerate(doc['records']):
        text=compiled(row);native=pipeline(arm,common,raw,plan,row['message_id'])
        assert native['loaded_template_hex']==native['formatted_hex']==text.hex()
        events=[];pixels=raster(arm,text,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000,glyph_events=events)
        assert pixels==literal_independent(arm,rom.read_file('/GRP/KANJI.FNT'),row['english'])
        assert [e['code'] for e in events[:len(text)]]==list(text)
        assert [(e['x'],e['y']) for e in events[:len(text)]]==[(6*i,0) for i in range(len(text))]
        padding=events[len(text):]
        assert len(padding)<=1 and all(e['code']==32 and e['x']==len(text)*6 and e['y']==0 for e in padding)
        assert len(text)*6<=210 and all(not p for p in pixels[228*12:])
        preview=ROOT/f'ID{row["message_id"]}_complete_native.png'
        image=Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels));image.save(preview)
        x=j*468;draw.text((x+6,4),f'ID{row["message_id"]}: '+row['english'],fill='white');sheet.paste(image.resize((456,128),Image.Resampling.NEAREST),(x+6,22))
        cases.append({'message_ID':row['message_id'],'english':row['english'],'compiled_hex':text.hex(),'native_pipeline':native,
            'all_ordered_complete_native_glyph_events':events,'zero_ink_pair_padding':padding,
            'full228x64_native_and_independent_font_equal':True,'literal_modal_origin_x0_native_preserved':True,
            'complete_first_final_letters_single_line_bounds_and_blank_paper_pass':True,
            'preview':str(preview),'preview_sha256':sha(preview.read_bytes()),'native_plane_sha256':sha(bytes(pixels))})
    invalid=[]
    for label,key,value in [('leading-space','english',' Test'),('trailing-space','english','Test '),('internal-gap','english','No  lookout.'),
        ('LF','english','No\nlookout.'),('NUL','english','No\0lookout.'),('printf','english','No %s.'),('layout','english','No {LB}.'),
        ('non-ASCII','english','No lookout—none.'),('long','english','A'*36),('wrong-ID','message_id',308),
        ('argument','native_argument_count',1),('macro','source_native_macros',['IC'])]:
        row=deepcopy(doc['records'][0]);row[key]=value
        try:compiled(row)
        except (ValueError,AssertionError):invalid.append(label)
        else:raise AssertionError(label)
    sheet_path=ROOT/'both_native_status_panels_2x.png';sheet.save(sheet_path)
    save(ROOT/'native_font_proof.json',{'manuscript':str(DOC),'manuscript_sha256':sha(DOC.read_bytes()),'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),
        'source_snapshot':'E:/Rota Nova translations/Generated/work/emulation_v193/sea_inspection_final_v1567d_1563/frame_006100_arm9_ram.bin','source_snapshot_sha256':sha(raw),
        'cases':cases,'invalid_compiler_inputs_rejected':invalid,'review_sheet':str(sheet_path),'review_sheet_sha256':sha(sheet_path.read_bytes()),
        'native_literal_modal_single_line_no_authored_breaks_or_cursor_patch':True,'visual_review_pending':True,
        'release_actual_modal_and_scene_completion_pending':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Both original546B8 pipelines and full native/independent glyph planes pass;12 invalid inputs rejected;literal modal origin x0 preserved.')
