"""Original signed fatigue/number/modal pipelines and202 full native font planes."""
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
from scripts.fatigue_status_native_plan_v1589 import compiled
from scripts.probe_inspection_status_fonts_v1574 import literal_independent
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/fatigue_status_fonts_v1590')
PLAN=Path('work/analysis/fatigue_status_payload_v1589/native_payload_plan.json')
DOC=Path('translations/fatigue_status_editorial_manuscript_v1.json')
BASE=0x02000000

def pipeline(arm,common,raw,plan,number,amount):
    assert number in [308,309] and 0<=amount<=100
    cpu,get,provider=machine(arm,common,raw,plan);seen={}
    fleets=get(0xCB1A8);fleet=fleets+4+132*get(0x2E58C);fatigue_before=bytes(cpu.mem_read(fleet+0x3D,1))[0]
    def observe(u,pc,size,data):
        if pc==BASE+0x546B8:
            assert u.reg_read(UC_ARM_REG_R0)==number
            pointer=u.reg_read(UC_ARM_REG_R1);value=bytes(u.mem_read(pointer,64)).split(b'\0')[0]
            seen.update(message_ID=number,source_amount_hex=value.hex())
        elif pc==BASE+0x54788:
            seen['loaded_template_hex']=bytes(u.mem_read(u.reg_read(UC_ARM_REG_R1),256)).split(b'\0')[0].hex()
        elif pc==BASE+0x54798:
            sp=u.reg_read(UC_ARM_REG_SP);seen['original_wrapper_parent']=struct.unpack('<I',u.mem_read(sp+0xc4,4))[0]
            inp=struct.unpack_from('<I',arm,0x54890)[0];seen['original_varargs_output_hex']=bytes(u.mem_read(inp,256)).split(b'\0')[0].hex()
        else:
            out=struct.unpack_from('<I',arm,0x54894)[0];seen['formatted_hex']=bytes(u.mem_read(out,256)).split(b'\0')[0].hex();u.emu_stop()
    for pc in [BASE+0x546B8,BASE+0x54788,BASE+0x54798,BASE+0x5479C]:cpu.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
    signed=amount if number==308 else -amount
    if amount:
        entry=BASE+0x79728;arg=signed
    else:
        # The original helper exits on zero;this is explicitly a formatting-only boundary case.
        value=get(0xABF50,0);cpu.reg_write(UC_ARM_REG_R1,value);entry=BASE+0x546B8;arg=number
    cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP);cpu.reg_write(UC_ARM_REG_R0,arg)
    cpu.emu_start(entry,STOP,count=3000000)
    assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0x5479C and seen['original_wrapper_parent']==BASE+0x546E8
    fatigue_after=bytes(cpu.mem_read(fleet+0x3D,1))[0]
    assert fatigue_after==max(0,min(100,fatigue_before+signed))
    value=''.join(chr(0xFF10+int(c)) for c in str(amount)).encode('cp932')
    assert seen['source_amount_hex']==value.hex()
    return {**seen,'amount':amount,'signed_change':signed,'fatigue_before':fatigue_before,'fatigue_after_original_clamp':fatigue_after,
        'original_entry':entry,'zero_is_CPU_formatting_only_not_real_event':not amount,'file_reads':provider.reads,
        'CPU_boundary':'Host successful file IO and stop before UI constructor;not an emulator event or earned recovery.'}

if __name__=='__main__':
    assert not ROOT.exists()
    plan,doc=read(PLAN),read(DOC);assert plan['manuscript_sha256']==sha(DOC.read_bytes())
    arm,common=Path(plan['target_ARM9']).read_bytes(),Path(plan['target_COMMON']).read_bytes();rom=NdsImage.open(doc['current_ROM'])
    raw=Path('E:/Rota Nova translations/Generated/work/emulation_v193/inspection_status_lookout_v1582_1578/frame_006100_arm9_ram.bin').read_bytes()
    class CurrentFont:
        @staticmethod
        def open(path):
            assert path=='out/all_routes_combined_v255_candidate.nds';return rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    assert not any(raster(arm,b' ',0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000))
    # Zero adjustment must not invoke a status or change any game RAM.
    cpu,get,provider=machine(arm,common,raw,plan);zero_before=bytes(cpu.mem_read(BASE,0x400000));get(0x79728,0)
    assert bytes(cpu.mem_read(BASE,0x400000))==zero_before
    ROOT.mkdir(parents=True);cases=[];previews=[]
    for row in doc['records']:
        text=compiled(row)
        for amount in range(101):
            native=pipeline(arm,common,raw,plan,row['message_id'],amount)
            argument=bytes.fromhex(native['source_amount_hex']);expanded=text.replace(b'%s',argument)
            assert native['loaded_template_hex']==text.hex() and native['original_varargs_output_hex']==native['formatted_hex']==expanded.hex()
            english=expanded.decode('cp932');assert len(expanded)<=35 and b'\n' not in expanded
            events=[];pixels=raster(arm,expanded,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000,glyph_events=events)
            assert pixels==literal_independent(arm,rom.read_file('/GRP/KANJI.FNT'),english)
            index,x,guards=0,0,[]
            for char in english:
                encoded=char.encode('cp932');code=int.from_bytes(encoded,'big')
                if len(encoded)==2 and events[index]['code']==32 and events[index]['x']==x:
                    guards.append(events[index]);index+=1
                assert events[index]['code']==code and (events[index]['x'],events[index]['y'])==(x,0),(row['message_id'],amount,char,events[index])
                index+=1;x+=6*len(encoded)
            assert len(guards)<=1
            padding=events[index:];assert len(padding)<=1 and all(e['code']==32 and (e['x'],e['y'])==(x,0) for e in padding)
            assert x<=210 and all(not p for p in pixels[228*12:])
            case={'message_ID':row['message_id'],'amount':amount,'english_expanded':english,'compiled_hex':text.hex(),'native_pipeline':native,
                'original_actual_amount':amount in row['original_actual_amount_values'],'other_amounts_CPU_only_numeric_stress_not_events':amount not in row['original_actual_amount_values'],
                'all_ordered_real_glyphs':events,'zero_ink_ASCII_to_CP932_transition_guards':guards,'zero_ink_final_pair_padding':padding,
                'whole228x64_native_independent_and_complete_F_amount_period_match':True,'literal_modal_origin_x0_and_bounds_blank_paper_pass':True,
                'native_plane_sha256':sha(bytes(pixels))}
            if amount in set(row['original_actual_amount_values'])|{0,9,99,100}:
                path=ROOT/f'ID{row["message_id"]}_amount{amount:03d}_complete.png'
                Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(path)
                case.update(preview=str(path),preview_sha256=sha(path.read_bytes()));previews.append(case)
            cases.append(case)
    invalid=[]
    for label,key,value in [('leading-space','english',' Fatigue +%s.'),('trailing-space','english','Fatigue +%s. '),('internal-gap','english','Fatigue  +%s.'),
        ('LF','english','Fatigue\n+%s.'),('NUL','english','Fatigue\0+%s.'),('missing-placeholder','english','Fatigue rose.'),('extra-placeholder','english','Fatigue %s %s.'),
        ('literal-percent','english','Fatigue %s percent%.'),('layout','english','Fatigue %s {LB}.'),('non-ASCII','english','Fatigue—%s.'),
        ('expanded-overflow','english','A'*30+'%s'),('wrong-ID','message_id',310),('wrong-argc','native_argument_count',0),
        ('invented-macro','source_native_macros',['IC']),('wrong-amount-contract','original_actual_amount_values',[999])]:
        row=deepcopy(doc['records'][0]);row[key]=value
        try:compiled(row)
        except (ValueError,AssertionError):invalid.append(label)
        else:raise AssertionError(label)
    sheet=Image.new('RGB',(936,152*((len(previews)+1)//2)),'#263238');draw=ImageDraw.Draw(sheet)
    for i,case in enumerate(previews):
        x,y=i%2*468,i//2*152;draw.text((x+6,y+4),f'ID{case["message_ID"]}; amount{case["amount"]}; '+('actual source' if case['original_actual_amount'] else 'CPU stress'),fill='white')
        with Image.open(case['preview']) as im:sheet.paste(im.resize((456,128),Image.Resampling.NEAREST),(x+6,y+22))
    image=ROOT/'all_source_and_boundary_native_panels.png';sheet.save(image)
    save(ROOT/'native_font_proof.json',{'manuscript':str(DOC),'manuscript_sha256':sha(DOC.read_bytes()),'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),
        'cases':cases,'invalid_compiler_inputs_rejected':invalid,'review_sheet':str(image),'review_sheet_sha256':sha(image.read_bytes()),
        'source_actual_amount_cases':5,'CPU_numeric_cases':202,'zero_helper_skips_status_and_preserves_all4MiB':True,
        'original_numeric_varargs_and_macro_expansion_preserved_without_wrap_code_change':True,'visual_review_pending':True,
        'release_and_actual_increase_recovery_events_pending':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('202 original numeric/modal and full native font planes pass,including5 actual source amounts,complete F/digits/period;15 invalid compiler inputs rejected.')
