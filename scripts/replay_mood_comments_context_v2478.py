"""Map39 source mood0/4/5 responses and372 defined selector/control cases."""
import struct
from pathlib import Path
from shutil import copy2
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_LR,UC_ARM_REG_PC
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import snapshot,machine_at,reference
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/mood_comments_context_v2478')
ROM=Path('out/all_routes_combined_v2284_candidate.nds')
BASE=0x02000000
IDS=tuple(range(1833,1872))
FAMILIES={0:(1833,1841,1845,0x12420,0x12488,0x123C0),4:(1846,1854,1858,0x12424,0x1248C,0x123C4),5:(1859,1867,1871,0x12428,0x12490,0x123BC)}
SPANS=((0x12104,0x12494),(0x7E0B4,0x7E0BC),(0x7E100,0x7E108),(0x7EF28,0x7EF58),(0x53C6C,0x53CB0),(0x53F4C,0x53F9C))


def select(arm,raw,actor,helper,mode,condition,mood,expected,receipt,priority=False):
    cpu,get=machine_at(arm,raw);hero=get(0x7F244)
    if actor<4:assert hero==actor
    for a,b in SPANS:assert bytes(cpu.mem_read(BASE+a,b-a))==arm[a:b]
    for nfirst,hfirst,sera,nt,ht,st in FAMILIES.values():
        for literal,size in ((nt,32),(ht,16)):
            table=struct.unpack_from('<I',arm,literal)[0];assert bytes(cpu.mem_read(table,size))==arm[table-BASE:table-BASE+size]
    actors=get(0xCB184);obj=actors+struct.unpack_from('<I',arm,0x1229C)[0] if actor<4 else actors+4+actor*32
    old_condition,old_mood=get(0x7E100,obj),get(0x7E0B4,obj)
    assert (old_condition,old_mood)==tuple(raw[obj-BASE+6:obj-BASE+8])
    context=get(0x3F0F8);before=bytes(cpu.mem_read(BASE,len(raw)));assert before==raw
    cpu.mem_write(obj+6,bytes([condition,mood]));cpu.mem_write(context+8,struct.pack('<2I',*mode))
    prepared=bytes(cpu.mem_read(BASE,len(raw)));allowed={obj+6,obj+7,*range(context+8,context+16)}
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(before,prepared,strict=True)) if a!=b]
    assert all(r['address'] in allowed for r in changes)
    assert prepared[obj-BASE:obj-BASE+6]==raw[obj-BASE:obj-BASE+6] and prepared[obj-BASE+8:obj-BASE+32]==raw[obj-BASE+8:obj-BASE+32]
    assert get(0x7E100,obj)==condition and get(0x7E0B4,obj)==mood
    selected=[];roles=[];moods=[]
    def numeric(u,pc,size,unused):
        selected.append(u.reg_read(UC_ARM_REG_R0));u.reg_write(UC_ARM_REG_R0,0x02450000);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    hooks=[cpu.hook_add(UC_HOOK_CODE,numeric,begin=BASE+0x5528C,end=BASE+0x5528C),
        cpu.hook_add(UC_HOOK_CODE,lambda *args:roles.append(True),begin=BASE+0x81F54,end=BASE+0x81F54),
        cpu.hook_add(UC_HOOK_CODE,lambda *args:moods.append(True),begin=BASE+0x7E0B4,end=BASE+0x7E0B4)]
    try:result=get(helper,actor,0) if helper==0x12104 else get(helper,obj)
    finally:
        for hook in hooks:cpu.hook_del(hook)
    assert selected==([] if expected is None else [expected]),(actor,hex(helper),condition,mood,mode,selected,expected)
    if expected is None:assert result==0
    assert not roles and get(0x7F244)==hero
    if priority:assert not moods
    else:assert moods
    return {'actor_ID':actor,'genuine_captain_ID':hero,'source_helper':BASE+helper,'source_activity_state':0 if helper==0x12104 else None,
        'source_RAM':receipt,'original_condition':old_condition,'original_mood':old_mood,'isolated_CPU_condition':condition,'isolated_CPU_mood':mood,
        'source_condition_byte_offset':6,'source_mood_byte_offset':7,'original_mode_fields8_12':list(struct.unpack_from('<2I',raw,context-BASE+8)),
        'isolated_CPU_mode_fields8_12':list(mode),'fixture_changes':changes,'only_declared_condition_mood_and_mode_fields_change':True,
        'other30_actor_bytes_and_all_other_source_RAM_exact':True,'selected_message_ID':expected,'numeric_selection_provider_boundary_only':True,
        'original_selector_and_callee_saved_ABI_pass':True,'job_role_getter_not_called':True,'source_mood_getter_calls':len(moods),
        'physical_priority_bypasses_mood_getter':priority,'not_prose_font_actual_gameplay_or_earned_mood_credit':True}


def main():
    ROOT.mkdir(parents=True,exist_ok=True);packet_path=ROOT/'source_context_packet.json';assert not packet_path.exists()
    ledger=read('translations/editorial_review_current_v1.json');assert ledger['records_editorially_completed']==2143 and ledger['contextual_story_natural_dialogue_pass_v1871']['fresh_pass_records_integrated']==1857
    current,clean,canonical=map(NdsImage.open,(ROM,'work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    assert sha(ROM.read_bytes())==ledger['current_integrated_candidate']['sha256']
    arm,j=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    for a,b in SPANS:assert arm[a:b]==j[a:b]
    assert arm[0x7E0B4:0x7E0BC]==bytes.fromhex('0700d0e51eff2fe1') and arm[0x7E100:0x7E108]==bytes.fromhex('0600d0e51eff2fe1')
    literals=[]
    for mood,(nfirst,hfirst,sera,nt,ht,st) in FAMILIES.items():
        np,hp=struct.unpack_from('<I',arm,nt)[0],struct.unpack_from('<I',arm,ht)[0]
        assert struct.unpack_from('<8I',arm,np-BASE)==tuple(range(nfirst,nfirst+8))
        assert struct.unpack_from('<4I',arm,hp-BASE)==tuple(range(hfirst,hfirst+4)) and struct.unpack_from('<I',arm,st)[0]==sera
        literals.append({'mood_ID':mood,'NPC_literal':nt,'NPC_IDs':list(range(nfirst,nfirst+8)),'protagonist_literal':ht,
            'protagonist_IDs':list(range(hfirst,hfirst+4)),'Sera_literal':st,'Sera_ID':sera})
    npc,npc_receipt=snapshot('battle_personal_v897_893_Julio',14700);cpu,get=machine_at(arm,npc);actors=get(0xCB184)
    cases=[];priority=[];normal=[]
    def record(actor,body,receipt,voice=None):
        helper=0x1242C if actor<4 else 0x12380 if actor==24 else 0x123C8
        for mood,(nfirst,hfirst,sera,*unused) in FAMILIES.items():
            expected=hfirst+actor if actor<4 else sera if actor==24 else nfirst+voice
            for label,entry,mode in [('direct_mood_helper',helper,(0,1)),('main_battle_mood_priority',0x12104,(0,1)),('main_ordinary_mood_priority',0x12104,(0,0))]:
                row=select(arm,body,actor,entry,mode,0,mood,expected,receipt);row.update(case=label,native_voice_class=voice,Sera24_has_source_special_alternative=actor==24);cases.append(row)
            fatigue_id=1789+actor if actor<4 else 1793 if actor==24 else 1781+voice
            row=select(arm,body,actor,0x12104,(0,0),1,mood,fatigue_id,receipt,True);row.update(case='physical_condition1_preempts_mood',native_voice_class=voice);priority.append(row)
        if actor!=24:
            for mood in (1,2,3):
                row=select(arm,body,actor,helper,(0,1),0,mood,None,receipt);row.update(case='ordinary_moods_direct_NPC_hero_helper_no_message',native_voice_class=voice);normal.append(row)
    for actor in range(4,25):
        voice=get(0x7E988,actors+4+actor*32);assert 0<=voice<8;record(actor,npc,npc_receipt,voice)
    for actor,folder,frame in [(0,'personal_activity_v839_838_Rafael_later',3200),(1,'illness_critical_v976_975_CaptainIllness',16500),
            (2,'ceremony_Lil_approach_v825',23000),(3,'ceremony_Maria_approach_v825',26000)]:
        body,receipt=snapshot(folder,frame);record(actor,body,receipt)
    assert len(cases)==225 and len(priority)==75 and len(normal)==72 and {r['selected_message_ID'] for r in cases}==set(IDS)
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),j);en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),arm)
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    records=[{'message_id':n,'selected_review_family':n in IDS,'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),'source_reference':reference(jp[n]),
        'current_English':en[n].text.decode('cp932'),'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),'canonical_text_hex':accepted[n].text.hex(),'prose_review_and_formatting_approval':False} for n in range(1832,1873)]
    save(packet_path,{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'COMMON_sha256':sha(current.read_file('/COMMON/MESFILE.DK4')),'ARM9_sha256':sha(arm),
        'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'source_code_spans_exact_clean':[[a,b,sha(arm[a:b])] for a,b in SPANS],
        'source_mood_getter':'0207E0B4:LDRB r0,[r0,#7];BX lr','source_mood_IDs':[0,4,5],'source_mood_literal_tables':literals,
        'all225_original_direct_main_battle_and_ordinary_mood_selections':cases,'all75_physical_condition1_priority_controls':priority,
        'all72_direct_NPC_hero_normal_mood1_2_3_no_message_controls':normal,'four_genuine_protagonists_and21_NPCs_no_ID_replacement':True,
        'source_physical_condition0_required_for_mood_selection':True,'job_role_getter_not_called_in_selected_or_control_paths':True,
        'Sera_normal_mood1_2_3_direct_helper_not_executed':True,
        'Sera_helper_precondition_note':'Original main12104 calls12380 only for mood0 or>=4;valid0/4/5 branches initialize r4. Direct12380 with1/2/3 does not initialize r4 and is outside this original caller contract. No undefined direct calls or normal-helper no-message claims for Sera are made.',
        'records_with_immediate_storage_neighbors':records,'review_leads_not_final_translations':[{'message_id':1845,'issue':'Restore complete ASCII first-person I only after native and actual proof.'},
            {'message_id':1855,'issue':'Clean source is only an ellipsis;current ..Ug has stray letters and needs independent source-bound correction.'},
            {'message_id':1857,'issue':'Preserve personal inability to concentrate and the proposed change of pace.'},
            {'message_id':1871,'issue':'Source is intentional nonverbal symbol panic;review an appropriate English comic-symbol equivalent without inventing spoken meaning or unsafe formatter characters.'}],
        'completed_entries_added':0,'source_prose_review_credit_added':0,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('225 current mood selections,75 physical-priority and72 defined normal-mood controls pass;zero new editorial credit.',flush=True)
if __name__=='__main__':main()
