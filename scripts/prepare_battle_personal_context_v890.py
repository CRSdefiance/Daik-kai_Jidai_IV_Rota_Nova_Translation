"""Original battle-personal selectors and source packet;no editorial credit."""

import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_PC,UC_ARM_REG_LR
from dk4tool.patch.gunnery_deck_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import snapshot,machine_at,reference
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_personal_v890')
ROM=Path('out/all_routes_combined_v888_candidate.nds')
BASE=0x02000000


def choose(arm,raw,actor,entry,state=None,mode=None,cabin=False):
    cpu,get=machine_at(arm,raw)
    if actor<4:assert get(0x7F244)==actor
    before_hero=get(0x7F244);context=get(0x3F0F8)
    observed=struct.unpack('<2I',cpu.mem_read(context+8,8))
    assert observed!=(0,1),'Ordinary source capture unexpectedly uses battle predicate'
    fields=[]
    if mode is not None:
        cpu.mem_write(context+8,struct.pack('<2I',*mode))
        fields.append({'mode_object':context,'offset':8,'original_fields':list(observed),'isolated_CPU_fields':list(mode)})
    if cabin:
        controller=get(0xCB1A8)+0x2090;model=get(0x82E04,controller)
        old_type=get(0x132C0,model,12)
        for slot in range(31):
            if get(0x82BC4,controller,slot)==actor:get(0x82BA8,controller,slot)
        cpu.mem_write(model+0x1E+12,b'\x0c');get(0x82BB8,controller,12,actor)
        assert get(0x81F54,controller,actor)==12
        fields.append({'CPU_room_slot':12,'original_room_type':old_type,'isolated_role_type':12,'actor_ID':actor})
    selected=[]
    def numeric(u,pc,size,unused):
        selected.append(u.reg_read(UC_ARM_REG_R0));u.reg_write(UC_ARM_REG_R0,0x02450000)
        u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    hook=cpu.hook_add(UC_HOOK_CODE,numeric,begin=BASE+0x5528C,end=BASE+0x5528C)
    try:get(entry,actor,*(() if state is None else (state,)))
    finally:cpu.hook_del(hook)
    assert len(selected)==1 and get(0x7F244)==before_hero
    return {'actor_ID':actor,'source_entry':BASE+entry,'activity_state':state,'selected_message_ID':selected[0],
        'source_mode_fields':list(observed),'declared_CPU_context_fields':fields,'actual_original_captain_ID_preserved':before_hero,
        'native_ABI_and_stack_pass':True,'numeric_provider_intercept_only_no_text_or_renderer_override':True,
        'not_actual_battle_UI_initialization_or_gameplay':True}


def main():
    ROOT.mkdir(parents=True,exist_ok=True);assert not (ROOT/'source_context_packet.json').exists()
    current,clean,canonical=map(NdsImage.open,(ROM,'work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==856 and ledger['records_with_source_and_prose_pass']==859
    assert sha(ROM.read_bytes())==ledger['current_integrated_candidate']['sha256']
    arm,jp_arm=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    assert arm[0x12104:0x12920]==jp_arm[0x12104:0x12920]
    assert arm[0x3F0F8:0x3F100]==jp_arm[0x3F0F8:0x3F100]
    assert struct.unpack_from('<I',arm,0x1271C)[0]==1571
    assert struct.unpack_from('<I',arm,0x128B0)[0]==1361
    folders={0:('personal_activity_v839_838_Rafael_later',3200),1:('gunnery_deck_v889_888_JoakimDeck',3400),
        2:('ceremony_Lil_approach_v825',23000),3:('ceremony_Maria_approach_v825',26000)}
    cases=[]
    for actor in range(25):
        raw,receipt=snapshot(*folders[actor if actor<4 else 1])
        specs=(('direct_battle_personal',0x126A8,None,None,False,1571+actor),
            ('battle_activity1',0x12104,1,(0,1),False,1571+actor),
            ('ordinary_activity1_control',0x12104,1,(0,0),False,1361+actor),
            ('nonzero_field8_blocks_battle_control',0x12104,1,(1,1),False,1361+actor),
            ('battle_working_Cabin12',0x12104,0,(0,1),True,1571+actor))
        for label,entry,state,mode,cabin,expected in specs:
            row=choose(arm,raw,actor,entry,state,mode,cabin);assert row['selected_message_ID']==expected,(actor,label,row)
            row.update(case=label,source_RAM=receipt);cases.append(row)
    assert len(cases)==125
    raw,receipt=snapshot(*folders[1]);special=[]
    for actor in (25,26,27):
        row=choose(arm,raw,actor,0x126A8);row.update(source_RAM=receipt,not_claimed_unlocked_or_owned_or_editorially_reviewed=True)
        if actor==25:assert row['selected_message_ID']==struct.unpack_from('<I',arm,0x12710)[0]
        if actor==26:assert row['selected_message_ID']==struct.unpack_from('<I',arm,0x12714)[0]
        if actor==27:assert row['selected_message_ID'] in (1888,struct.unpack_from('<I',arm,0x12718)[0])
        special.append(row)
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),jp_arm)
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),arm)
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    records=[]
    for n in range(1570,1597):
        records.append({'message_id':n,'selected_review_family':1571<=n<=1595,
            'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),'source_reference':reference(jp[n]),
            'current_English':en[n].text.decode('cp932'),'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),
            'canonical_text_hex':accepted[n].text.hex(),'prose_review_and_formatting_approval':False})
    special_ids=sorted({r['selected_message_ID'] for r in special}|{1888,struct.unpack_from('<I',arm,0x12718)[0]})
    save(ROOT/'source_context_packet.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'COMMON_sha256':sha(current.read_file('/COMMON/MESFILE.DK4')),'ARM9_sha256':sha(arm),
        'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'source_selector_span':[0x12104,0x12920,sha(arm[0x12104:0x12920])],
        'battle_personal_base1571_and_ordinary_base1361':True,
        'source_battle_predicate':{'getter':BASE+0x3F0F8,'object_field8_must_equal':0,'object_field12_must_equal':1},
        'all125_original_selector_and_discriminating_control_cases':cases,
        'battle_role12_working_and_activity1_paths_both_source_proven':True,
        'four_genuine_captain_states_and21_NPCs_no_actor_replacement':True,
        'records_with_immediate_storage_neighbors':records,
        'additional_special_actor_numeric_cases_not_new_family_credit':special,
        'additional_source_references_not_editorially_reviewed':[{'message_id':n,'source_Japanese':jp[n].text.decode('cp932'),
            'source_reference':reference(jp[n]),'current_English':en[n].text.decode('cp932'),'current_reference':reference(en[n])} for n in special_ids],
        'actor27_other_condition_branch_not_claimed_executed':True,
        'review_leads_not_final_translations':['These25 battle-time hobby reactions are distinct from completed1361-1385 ordinary reactions.',
            'Retain individual character voice,combat context,sleeping/eating/dancing/reading jokes,and deliberate hesitation.',
            'Do not turn encouragement into a guaranteed morale/stat effect or complainants into active combatants.'],
        'actual_battle_initializer_scene_and_body_display_still_pending':True,
        'completed_entries_added':0,'source_prose_review_credit_added':0,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    packet=ROOT/'source_context_packet.json'
    ledger['next_battle_personal_source_packet']={'proof':str(packet),'proof_sha256':sha(packet.read_bytes()),
        'native_message_IDs':list(range(1571,1596)),'status':'125-original-context-and-control-cases-source-packet-proved-prose-pending',
        'no_completion_or_source_prose_credit':True}
    ledger['research_checkpoints'].append({'id':'V890-Battle-personal25-context','proof':str(packet),
        'original_numeric_context_and_control_cases':125,'extra_special_actor_numeric_cases':3,
        'scope':'25 distinct battle-personal entries1571-1595. Main source gate,ordinary controls and working Cabin12 path execute in isolated CPU snapshots;actual battle initialization not claimed.',
        'completed_entries_added':0,'source_prose_review_credit_added':0,'full_goal_complete':False})
    save('translations/editorial_review_current_v1.json',ledger)
    print('Next battle-personal25:125 original selector/control cases and3 special numeric leads pass;no prose/completion credit.',flush=True)


if __name__=='__main__':main()
