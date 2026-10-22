"""Exact five-table scope and original loader/PIC/full-font reaction proof."""
import inspect
import struct
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_LR,UC_ARM_REG_SP,UC_ARM_REG_PC
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_duel_cache_scope_v1150 as original_scope
from scripts import probe_duel_resident_fonts_v1151 as original_fonts
from scripts.duel_bark_front_v1201 import ADDRESS,TABLES
from scripts.probe_button_prompt_native import STACK,STOP
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_bark_native_v1202')
PLAN=Path('work/analysis/duel_bark_native_v1201/native_payload_plan.json')


def front_scope(arm,raw):
    cpu,get=get_machine(arm,raw)
    cpu.mem_write(ADDRESS,arm[ADDRESS-0x02000000:ADDRESS-0x02000000+108])
    context,pointer=0x02460000,0x02461000
    for pc in (0x0205528C,0x020D5404):cpu.hook_add(UC_HOOK_CODE,lambda c,p,s,d:c.emu_stop(),begin=pc,end=pc)
    def check(parent,table):
        cpu.mem_write(context+108,struct.pack('<I',parent));cpu.mem_write(context+148,struct.pack('<I',table))
        cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP)
        cpu.reg_write(UC_ARM_REG_R0,context);cpu.reg_write(UC_ARM_REG_R1,pointer)
        cpu.emu_start(ADDRESS|1,STOP,count=200)
        selected=parent==0x0200D4BC and table in TABLES
        assert cpu.reg_read(UC_ARM_REG_PC)==(0x0205528C if selected else 0x020D5404),(hex(parent),hex(table))
        if selected:assert cpu.reg_read(UC_ARM_REG_R0)==1931
        else:assert (cpu.reg_read(UC_ARM_REG_R0),cpu.reg_read(UC_ARM_REG_R1))==(context,pointer)
        assert cpu.reg_read(UC_ARM_REG_SP)==STACK-16
        return selected
    count,selected=0,0
    for low in range(65536):selected+=check(0x0200D4BC,0x02110000|low);count+=1
    assert selected==5
    for parent in (0,0xFFFFFFFF,0x1200D4BC,0x0200D528,0x0200D4B8,0x0200D4C0):
        for table in (*TABLES,0,0xFFFFFFFF,0x02117500,0x02117620):assert not check(parent,table);count+=1
    for high in (0,0x0210,0x0212,0x1211,0xFFFF):
        for table in TABLES:assert not check(0x0200D4BC,(high<<16)|(table&65535));count+=1
    return {'cases':count,'all65536_source_table_low_words_exactly_five_memberships':True,
        'wrong_parent_high_word_direct_numeric_and_escape_controls_excluded':True,
        'dispatch_boundary_before_loader_or_font_not_full_ABI_proof':True}


def main():
    assert not ROOT.exists()
    plan=read(PLAN);arm=Path(plan['target_ARM9']).read_bytes();common=Path(plan['target_COMMON']).read_bytes()
    assert sha(arm)==plan['target_ARM9_sha256'] and sha(common)==plan['target_COMMON_sha256']
    context=read('work/analysis/duel_bark_context_v1199/source_context_packet.json');raw=Path(context['actual_snapshot']).read_bytes()
    assert sha(raw)==context['actual_snapshot_sha256']
    rom=NdsImage.open('out/all_routes_combined_v1189_candidate.nds')
    class ExactSource:
        @staticmethod
        def open(path):
            assert str(path)=='out/all_routes_combined_v1105_candidate.nds'
            return rom
    pipeline=FunctionType(original_scope.pipeline.__code__,{**original_scope.pipeline.__globals__,
        'PLAN_PATH':PLAN,'TABLES':TABLES,'NdsImage':ExactSource},argdefs=original_scope.pipeline.__defaults__)
    font_source=inspect.getsource(original_fonts.execute)
    old="0 if family == 'challenge' else 1"
    assert font_source.count(old)==1
    font_source=font_source.replace(old,"0 if family in ('challenge','positive_action_reaction','negative_action_reaction') else 1")
    env={**original_fonts.__dict__,'pipeline':pipeline,'PLAN_PATH':PLAN}
    exec(compile(font_source,__file__,'exec'),env);execute=env['execute']
    scope_source=inspect.getsource(original_scope.execute)
    old="0 if family=='challenge' else 1"
    assert scope_source.count(old)==1
    scope_source=scope_source.replace(old,"0 if family in ('challenge','positive_action_reaction','negative_action_reaction') else 1")
    scope_env={**original_scope.__dict__,'pipeline':pipeline,'TABLES':TABLES,'PLAN_PATH':PLAN}
    exec(compile(scope_source,__file__,'exec'),scope_env);execute_scope=scope_env['execute']
    dispatch=front_scope(arm,raw)
    ROOT.mkdir(parents=True);save(ROOT/'front_dispatch.json',dispatch)
    records={r['message_id']:r for r in read('translations/duel_bark_editorial_manuscript_v1.json')['records']}
    old_records={r['message_id']:r for r in read('translations/duel_editorial_manuscript_v5.json')['records']}
    cpu,get=get_machine(arm,raw);representatives={}
    for choice in context['all416_unchanged_native_voice_selections']:
        representatives.setdefault(choice['message_ID'],choice['actor_object'])
    font,kanji=GameAsciiFont.from_arm9(arm),rom.read_file('/GRP/KANJI.FNT')
    cases=[];previews=[];negative=[]
    for n,row in records.items():
        family=row['source_family'];table=row['source_table'];actor=representatives[n]
        assert get(0x53F4C,actor,table)==n
        result,visible=execute(arm,common,raw,actor,b'',family,table,n,row['english'].encode('ascii'),font,kanji)
        assert result['native_getter_IDs']==[n,1931]
        cases.append(result)
        image=Image.new('L',(144,36),255)
        image.putdata([0 if v else 255 for v in visible]);p=ROOT/f'COMMON{n}_native.png';image.save(p)
        previews.append({'message_ID':n,'path':str(p),'sha256':sha(p.read_bytes()),'lines':result['lines']})
        print(n,'complete original loader/PIC/native fonts/crops pass',flush=True)
    # Replay every earlier static alternative under the changed front, including
    # a legitimate short name argument. No original name is changed in gameplay.
    for n,row in old_records.items():
        if not 1931<=n<=1950:continue
        table=row['source_table'];actor=None
        actors=get(0xCB184)
        for slot in range(208):
            obj=actors+4+slot*32 if slot<207 else actors+0x19E4
            if get(0x53F4C,obj,table)==n:actor=obj;break
        assert actor
        family='challenge' if n<=1938 else 'acceptance' if n<=1944 else 'threat'
        name=b'Rafael';text=row['english'].encode('ascii').replace(b'%s',name)
        result,visible=execute(arm,common,raw,actor,name,family,table,n,text,font,kanji)
        result['preserved_static_regression']=True;cases.append(result)
    actor=representatives[1957]
    for n in (*range(1931,1951),*range(1957,1973)):
        text=(records[n] if n in records else old_records[n])['english'].encode('ascii')
        negative.append(execute_scope(arm,common,raw,actor,b'Rafael','direct_negative',0,n,text,direct=True))
    assert len(cases)==36 and len(negative)==36
    sheet=Image.new('RGB',(4*308,4*110),'#263238');draw=ImageDraw.Draw(sheet)
    for i,row in enumerate(previews):
        x,y=i%4*308,i//4*110
        draw.text((x+5,y+3),f"COMMON{row['message_ID']}; native CPU fonts",fill='white')
        with Image.open(row['path']) as im:sheet.paste(im.resize((288,72),Image.Resampling.NEAREST),(x+5,y+24))
    image=ROOT/'all16_reaction_native_review.png';sheet.save(image)
    save(ROOT/'native_font_scope_verification.json',{'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),
        'payload_plan':str(PLAN),'payload_plan_sha256':sha(PLAN.read_bytes()),'front_dispatch':dispatch,
        'cases':cases,'all16_new_and20_preserved_complete_native_font_cases':True,'direct_numeric_exclusion_cases':negative,
        'all_original_selector_loader_printf_macro_PIC_ASCII_CP932_fonts_and_three_source_crops_execute':True,
        'all47_cache_flush_and_invalidate_lines_and_no_COMMON_reentry_or_code_writes_pass':True,
        'no_section_BSS_cache_arena_ITCM_or_staged_payload_growth':True,
        'effective_font_binding_sha256':sha(font_source.encode()),'effective_scope_binding_sha256':sha(scope_source.encode()),
        'previews':previews,'review_sheet':str(image),'review_sheet_sha256':sha(image.read_bytes()),
        'visual_review_pending':True,'actual_original_timed_feedback_and_registered_integration_pending':True,
        'no_completed_editorial_credit':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('16 new+20 previous full native fonts;36 direct exclusions;all five-table scope cases pass.',flush=True)


if __name__=='__main__':main()
