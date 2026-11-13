"""Map13 physical-status1 fatigue alternatives with role-independent native controls."""
import struct
from pathlib import Path
from shutil import copy2
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_PC,UC_ARM_REG_LR
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import snapshot,machine_at,reference
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/physical_fatigue_context_v2454')
ROM=Path('out/all_routes_combined_v2284_candidate.nds')
BASE=0x02000000
IDS=tuple(range(1781,1794))
SPANS=((0x12104,0x12600),(0x7E100,0x7E108),(0x7EF28,0x7EF58),(0x53C6C,0x53CB0),(0x53F4C,0x53F9C))

def select(arm,raw,actor,helper,mode,status,expected,source_receipt):
    cpu,get=machine_at(arm,raw);hero=get(0x7F244)
    if actor<4:assert hero==actor
    for a,b in SPANS:assert bytes(cpu.mem_read(BASE+a,b-a))==arm[a:b]
    for literal,count in ((0x12574,8),(0x125F0,4)):
        table=struct.unpack_from('<I',arm,literal)[0]
        assert bytes(cpu.mem_read(table,count*4))==arm[table-BASE:table-BASE+count*4]
    actors=get(0xCB184);obj=actors+struct.unpack_from('<I',arm,0x1229C)[0] if actor<4 else actors+4+actor*32
    before_status=get(0x7E100,obj);assert before_status==raw[obj-BASE+6]
    context=get(0x3F0F8);before=bytes(cpu.mem_read(BASE,len(raw)));assert before==raw
    cpu.mem_write(obj+6,bytes([status]));cpu.mem_write(context+8,struct.pack('<2I',*mode))
    prepared=bytes(cpu.mem_read(BASE,len(raw)));allowed={obj+6,*range(context+8,context+16)}
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(before,prepared,strict=True)) if a!=b]
    assert all(r['address'] in allowed for r in changes) and get(0x7E100,obj)==status
    assert bytes(cpu.mem_read(obj,6))==before[obj-BASE:obj-BASE+6] and bytes(cpu.mem_read(obj+7,25))==before[obj-BASE+7:obj-BASE+32]
    chosen=[];roles=[];moods=[]
    def numeric(u,pc,size,unused):
        chosen.append(u.reg_read(UC_ARM_REG_R0));u.reg_write(UC_ARM_REG_R0,0x02450000);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    hooks=[cpu.hook_add(UC_HOOK_CODE,numeric,begin=BASE+0x5528C,end=BASE+0x5528C),
        cpu.hook_add(UC_HOOK_CODE,lambda *args:roles.append(True),begin=BASE+0x81F54,end=BASE+0x81F54),
        cpu.hook_add(UC_HOOK_CODE,lambda *args:moods.append(True),begin=BASE+0x7E0B4,end=BASE+0x7E0B4)]
    try:result=get(helper,actor,0) if helper==0x12104 else get(helper,obj)
    finally:
        for hook in hooks:cpu.hook_del(hook)
    assert chosen==([] if expected is None else [expected]),(actor,hex(helper),status,mode,chosen,expected)
    if expected is None:assert result==0
    assert not roles and not moods and get(0x7F244)==hero
    return {'actor_ID':actor,'genuine_captain_ID':hero,'source_helper':BASE+helper,'source_activity_state':0 if helper==0x12104 else None,'source_RAM':source_receipt,
        'original_condition':before_status,'isolated_CPU_condition':status,'source_condition_byte_offset':6,
        'source_original_mode_fields8_12':list(struct.unpack_from('<2I',raw,context-BASE+8)),
        'isolated_CPU_mode_fields8_12':list(mode),'fixture_changes':changes,
        'only_declared_CPU_condition_and_mode_fields_changed':True,'actor_other31_bytes_and_all_other_source_RAM_preserved':True,
        'selected_message_ID':expected,'numeric_selection_provider_boundary_only':True,
        'original_native_selector_and_callee_saved_ABI_pass':True,'job_role_and_mood_getters_not_called':True,
        'not_prose_font_actual_gameplay_or_earned_fatigue_credit':True}

def main():
    ROOT.mkdir(parents=True,exist_ok=True);packet=ROOT/'source_context_packet.json';assert not packet.exists()
    ledger=read('translations/editorial_review_current_v1.json');assert ledger['records_editorially_completed']==2143 and ledger['contextual_story_natural_dialogue_pass_v1871']['fresh_pass_records_integrated']==1805
    current,clean,canonical=map(NdsImage.open,(ROM,'work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    assert sha(ROM.read_bytes())==ledger['current_integrated_candidate']['sha256']
    arm,source=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    for a,b in SPANS:assert arm[a:b]==source[a:b]
    assert arm[0x7E100:0x7E108]==bytes.fromhex('0600d0e51eff2fe1')
    npc_table=struct.unpack_from('<I',arm,0x12574)[0];hero_table=struct.unpack_from('<I',arm,0x125F0)[0]
    assert struct.unpack_from('<8I',arm,npc_table-BASE)==tuple(range(1781,1789))
    assert struct.unpack_from('<4I',arm,hero_table-BASE)==tuple(range(1789,1793))
    assert struct.unpack_from('<I',arm,0x124FC)[0]==1793
    npc,npc_receipt=snapshot('battle_personal_v897_893_Julio',14700);cpu,get=machine_at(arm,npc);actors=get(0xCB184)
    cases=[];controls=[]
    def record(actor,body,receipt,voice=None):
        helper=0x12584 if actor<4 else 0x12494 if actor==24 else 0x1250C
        expected=1789+actor if actor<4 else 1793 if actor==24 else 1781+voice
        for label,entry,mode in [('direct_physical_helper',helper,(0,1)),('main_battle_status_priority',0x12104,(0,1)),('main_ordinary_status_priority',0x12104,(0,0))]:
            row=select(arm,body,actor,entry,mode,1,expected,receipt);row.update(case=label,native_voice_class=voice,Sera24_has_source_special_alternative=actor==24);cases.append(row)
        row=select(arm,body,actor,helper,(0,1),0,None,receipt);row.update(case='healthy_direct_physical_helper_returns_no_message',native_voice_class=voice);controls.append(row)
    for actor in range(4,25):
        voice=get(0x7E988,actors+4+actor*32);assert 0<=voice<8
        record(actor,npc,npc_receipt,voice)
    for actor,folder,frame in [(0,'personal_activity_v839_838_Rafael_later',3200),(1,'battle_gunnery_deck_v955_954_CaptainDeck',16500),(2,'ceremony_Lil_approach_v825',23000),(3,'ceremony_Maria_approach_v825',26000)]:
        body,receipt=snapshot(folder,frame);record(actor,body,receipt)
    assert len(cases)==75 and len(controls)==25 and {r['selected_message_ID'] for r in cases}==set(IDS)
    prior_raw,prior_receipt=snapshot('battle_bridge_v930_928_ManuelHelm',16300)
    cpu,get=machine_at(arm,prior_raw);obj=get(0xCB184)+4+23*32;assert get(0x7E100,obj)==1
    prior_actual=select(arm,prior_raw,23,0x12104,(0,1),1,1788,prior_receipt)
    assert not prior_actual['fixture_changes']
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),arm)
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    records=[{'message_id':n,'selected_review_family':n in IDS,'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),'source_reference':reference(jp[n]),'current_English':en[n].text.decode('cp932'),'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),'canonical_text_hex':accepted[n].text.hex(),'prose_review_and_formatting_approval':False} for n in range(1780,1795)]
    save(packet,{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'COMMON_sha256':sha(current.read_file('/COMMON/MESFILE.DK4')),'ARM9_sha256':sha(arm),'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'source_code_spans_exact_clean':[[a,b,sha(arm[a:b])] for a,b in SPANS],'source_condition_getter':'0207E100:LDRB r0,[r0,#6];BX lr','source_condition_ID':1,
        'condition1_fatigue_NPC_IDs':list(range(1781,1789)),'condition1_genuine_protagonist_IDs':list(range(1789,1793)),'Sera24_special_ID':1793,
        'all75_original_direct_main_battle_and_ordinary_fatigue_selections':cases,'all25_healthy_direct_helper_no_message_controls':controls,
        'four_genuine_captains_and21_NPCs_no_actor_ID_replacement':True,'job_role_and_mood_not_queried_in_physical_status_branch':True,
        'prior_genuine_actual_Manuel_fatigue1788_selection_without_new_fixture':prior_actual,
        'prior_actual_snapshot_from_V928_not_new_V954_gameplay_credit':True,'records_with_immediate_storage_neighbors':records,
        'review_leads_not_final_translations':[{'message_id':1783,'issue':'Clean IC is a native first-person macro;require a new source-bound expansion proof and complete English I.'},{'message_id':1784,'issue':'Preserve explicit Recreation Room reference without inventing a completed reassignment.'},{'message_id':1793,'issue':'Sera has an independent fatigue-specific fragment;do not replace it with the generic NPC voice response or invent a diagnosis.'}],
        'completed_entries_added':0,'source_prose_review_credit_added':0,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('75 current selections,25 healthy controls and genuine prior1788 control pass;zero new editorial credit.',flush=True)
if __name__=='__main__':main()
