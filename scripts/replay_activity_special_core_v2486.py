"""Map next activity2/special selections;leave Chapel UI exceptions and prose unreviewed."""
import struct
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_PC,UC_ARM_REG_LR
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import snapshot,machine_at,reference
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/activity_special_core_v2486')
ROM=Path('out/all_routes_combined_v2284_candidate.nds')
BASE=0x02000000
EXCEPTIONS={15:1872,14:1873,22:1874,11:1875,20:1876,6:1877}

def choose(arm,raw,actor,entry,activity=None,mode=None,condition_mood=None,flag=None):
    cpu,get=machine_at(arm,raw);hero=get(0x7F244);assert hero==1
    context=get(0x3F0F8);actors=get(0xCB184);obj=actors+4+actor*32
    before=bytes(cpu.mem_read(BASE,len(raw)));assert before==raw
    allowed=set();changes=[]
    if mode is not None:
        cpu.mem_write(context+8,struct.pack('<2I',*mode));allowed.update(range(context+8,context+16))
    if condition_mood is not None:
        cpu.mem_write(obj+6,bytes(condition_mood));allowed.update((obj+6,obj+7))
    if flag is not None:
        root=get(0xCB190);at=root+4+0x190+0x11
        old=bytes(cpu.mem_read(at,1))[0];cpu.mem_write(at,bytes([(old&~4)|flag]));allowed.add(at)
        assert get(0x4A224,root+4+0x190)==flag
    prepared=bytes(cpu.mem_read(BASE,len(raw)))
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(before,prepared,strict=True)) if a!=b]
    assert all(r['address'] in allowed for r in changes)
    selected=[];health_queries=[];mood_queries=[];role_queries=[]
    def numeric(u,pc,size,unused):
        selected.append(u.reg_read(UC_ARM_REG_R0));u.reg_write(UC_ARM_REG_R0,0x02450000)
        u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    hooks=[cpu.hook_add(UC_HOOK_CODE,numeric,begin=BASE+0x5528C,end=BASE+0x5528C)]
    for fn,target in ((0x7E100,health_queries),(0x7E0B4,mood_queries),(0x81F54,role_queries)):
        hooks.append(cpu.hook_add(UC_HOOK_CODE,lambda *args,target=target:target.append(True),begin=BASE+fn,end=BASE+fn))
    try:result=get(entry,actor,*(() if activity is None else (activity,)))
    finally:
        for hook in hooks:cpu.hook_del(hook)
    assert get(0x7F244)==hero
    assert len(selected)<=1 and not health_queries and not mood_queries and not role_queries
    if not selected:assert result==0
    return {'actor_argument':actor,'actual_captain_ID_preserved':hero,'entry':BASE+entry,'activity':activity,
        'isolated_CPU_mode':mode,'isolated_CPU_condition_mood':condition_mood,'isolated_CPU_bit2_value':flag,
        'declared_changes':changes,'all_other4MiB_RAM_exact_before_original_selection':True,
        'selected_message_ID':selected[0] if selected else None,'original_ABI_and_stack_pass':True,
        'physical_mood_and_job_getters_not_called':True,'numeric_provider_intercept_only_no_text_rendering':True,
        'not_earned_unlock_recruitment_mood_or_actual_gameplay_credit':True}

def main():
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==2143 and ledger['contextual_story_natural_dialogue_pass_v1871']['fresh_pass_records_integrated']==1896
    rom,clean,canonical=map(NdsImage.open,(ROM,'work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    assert sha(ROM.read_bytes())==ledger['current_integrated_candidate']['sha256']
    arm,jp_arm=rom.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    spans=[(0x12104,0x12380),(0x126A8,0x12720),(0x12838,0x128B4),(0x134B0,0x13720),(0x4A224,0x4A230)]
    for a,b in spans:assert arm[a:b]==jp_arm[a:b]
    assert arm[0x4A224:0x4A230]==bytes.fromhex('1100d0e5040000e21eff2fe1')
    raw,receipt=snapshot('mood_comments_v982_975_CaptainSilent',16100)
    activity=[]
    for actor in range(28):
        case=choose(arm,raw,actor,0x122A4)
        assert case['selected_message_ID']==EXCEPTIONS.get(actor),(actor,case)
        activity.append(case)
    for actor,expected in EXCEPTIONS.items():
        for mode in ((0,0),(0,1)):
            for state in ((0,3),(1,0)):
                case=choose(arm,raw,actor,0x12104,activity=2,mode=mode,condition_mood=state)
                assert case['selected_message_ID']==expected;activity.append(case)
    assert len(activity)==52
    special=[]
    for actor in (25,26,27):
        for battle,entry in ((False,0x12838),(True,0x126A8)):
            for flag in ((None,) if actor!=27 else (0,4)):
                expected=({25:1885,26:1886}.get(actor) if battle else {25:1881,26:1882}.get(actor))
                if actor==27:expected=(1888 if flag else 1887) if battle else (1884 if flag else 1883)
                for main in (False,True):
                    case=choose(arm,raw,actor,0x12104 if main else entry,activity=1 if main else None,
                        mode=(0,1) if battle else (0,0),flag=flag)
                    assert case['selected_message_ID']==expected,(actor,battle,flag,case);special.append(case)
    assert len(special)==16
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),jp_arm)
    en=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    records=[]
    for n in range(1871,1890):
        records.append({'message_id':n,'selected_next_family':1872<=n<=1888,'source_Japanese':jp[n].text.decode('cp932'),
            'source_hex':jp[n].text.hex(),'source_reference':reference(jp[n]),'current_English':en[n].text.decode('cp932'),
            'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),'canonical_text_hex':accepted[n].text.hex(),
            'source_prose_font_actual_approval':False})
    assembly=[];md=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    for a,b in spans:
        assembly.extend(f'{i.address:08X} {i.mnemonic} {i.op_str}' for i in md.disasm(arm[a:b],BASE+a))
    (ROOT/'original_selector_disassembly.txt').write_text('\n'.join(assembly)+'\n',encoding='utf-8')
    proof={'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'COMMON_sha256':sha(rom.read_file('/COMMON/MESFILE.DK4')),
        'ARM9_sha256':sha(arm),'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'source_RAM':receipt,
        'clean_unchanged_source_spans':[[a,b,sha(arm[a:b])] for a,b in spans],
        'all52_activity2_direct_and_main_priority_cases':activity,'activity2_actor_to_message_ID':EXCEPTIONS,
        'activity2_special_speech_preempts_physical_mood_and_work_without_querying_their_getters':True,
        'all16_special_ordinary_battle_direct_and_main_bit2_controls':special,
        'actor27_original_shared_object_byte0x11_bit2_branches_both_proven_no_gender_or_story_interpretation_yet':True,
        'special_actor_arguments25_26_27_not_unlocked_or_recruited_in_save':True,
        'Chapel_exception1878_1879_1880_literals':[0x13710,0x13714,0x1370C],
        'Chapel_exception_menu_owner_arguments_actor_predicates_and_dismissal_still_unmapped':True,
        'all17_source_meaning_voice_English_prose_review_still_pending':True,'records_and_immediate_neighbors':records,
        'completed_entries_added':0,'source_prose_reviews_added':0,'full_goal_complete':False,'producer_sha256':sha(Path(__file__).read_bytes())}
    save(ROOT/'source_selection_research.json',proof)
    print('Next17 candidates:52 activity2 and16 special ordinary/battle controls pass. Chapel UI ownership/context and all prose review remain pending;no completion credit.')

if __name__=='__main__':main()
