"""Next24 clean-source sail0/boarding7 comments;no premature prose credit."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_R0

from dk4tool.patch.survey_lookout_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import snapshot,machine_at,reference
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sails_boarding_v878')
ROM=Path('out/all_routes_combined_v876_candidate.nds')
BASE=0x02000000
GROUPS=((0,1523,'Sail Handling'),(7,1535,'Boarding'))


def select(arm,raw,actor,role,expected):
    cpu,get=machine_at(arm,raw);controller=get(0xCB1A8)+0x2090;model=get(0x82E04,controller)
    # This is an isolated CPU numeric-selector fixture only.
    cpu.mem_write(model+0x1E+12,bytes([role]))
    for slot in range(31):
        if get(0x82BC4,controller,slot)==actor:get(0x82BA8,controller,slot)
    get(0x82BB8,controller,12,actor);assert get(0x81F54,controller,actor)==role
    chosen=[]
    def numeric(u,pc,size,unused):
        chosen.append(u.reg_read(UC_ARM_REG_R0));u.reg_write(UC_ARM_REG_R0,0x02450000)
        u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    helper=0x128B4 if actor<4 else 0x1278C
    hook=cpu.hook_add(UC_HOOK_CODE,numeric,begin=BASE+0x5528C,end=BASE+0x5528C)
    try:get(helper,actor)
    finally:cpu.hook_del(hook)
    assert chosen==[expected],(actor,role,chosen,expected)
    return {'actor_ID':actor,'source_helper':BASE+helper,'source_role_type':role,'selected_message_ID':expected,
        'complete_native_helper_and_ABI_pass':True,'CPU_role_assignment_only_no_actor_or_text_replacement':True,
        'ordinary_condition_gate_and_actual_display_not_claimed':True}


def main():
    assert not (ROOT/'source_context_packet.json').exists()
    ROOT.mkdir(parents=True,exist_ok=True)
    current,clean,canonical=map(NdsImage.open,(ROM,'work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    ledger=read('translations/editorial_review_current_v1.json')
    assert sha(ROM.read_bytes())==ledger['current_integrated_candidate']['sha256']
    assert ledger['records_editorially_completed']==808 and ledger['records_with_source_and_prose_pass']==811
    arm,source=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    spans=((0x12104,0x12920),(0x53C6C,0x53CB0),(0x53F4C,0x53F9C))
    assert all(arm[a:b]==source[a:b] for a,b in spans)
    npc_table=struct.unpack_from('<I',arm,0x12834)[0];hero_table=struct.unpack_from('<I',arm,0x1291C)[0]
    groups=[]
    for role,first,name in GROUPS:
        npc=struct.unpack_from('<I',arm,npc_table-BASE+role*4)[0]
        hero=struct.unpack_from('<I',arm,hero_table-BASE+role*4)[0]
        assert struct.unpack_from('<8I',arm,npc-BASE)==tuple(range(first,first+8))
        assert struct.unpack_from('<4I',arm,hero-BASE)==tuple(range(first+8,first+12))
        groups.append({'role_ID':role,'label':name,'NPC_pointer':npc,'NPC_IDs':list(range(first,first+8)),
            'actual_protagonist_pointer':hero,'protagonist_IDs':list(range(first+8,first+12))})
    raw,receipt=snapshot('personal_cabin_v840_838_Charles_after',3200);cpu,get=machine_at(arm,raw);actors=get(0xCB184)
    cases=[]
    for actor in range(4,25):
        voice=get(0x7E988,actors+4+actor*32);assert 0<=voice<8
        for role,first,name in GROUPS:
            row=select(arm,raw,actor,role,first+voice);row.update(native_voice_class=voice,source_RAM=receipt)
            cases.append(row)
    for actor,folder,frame in [(0,'personal_activity_v839_838_Rafael_later',3200),
        (1,'personal_cabin_v840_838_Charles_after',3200),(2,'ceremony_Lil_approach_v825',23000),
        (3,'ceremony_Maria_approach_v825',26000)]:
        hraw,hrec=snapshot(folder,frame);_,hget=machine_at(arm,hraw);assert hget(0x7F244)==actor
        for role,first,name in GROUPS:
            row=select(arm,hraw,actor,role,first+8+actor)
            row.update(source_RAM=hrec,actual_original_captain_ID_preserved=actor);cases.append(row)
    assert len(cases)==50 and {r['selected_message_ID'] for r in cases}==set(range(1523,1547))
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),arm)
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    records=[]
    for n in range(1522,1548):
        records.append({'message_id':n,'selected_review_family':1523<=n<=1546,
            'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),'source_reference':reference(jp[n]),
            'current_English':en[n].text.decode('cp932'),'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),
            'canonical_text_hex':accepted[n].text.hex(),'prose_review_and_formatting_approval':False})
    packet={'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'COMMON_sha256':sha(current.read_file('/COMMON/MESFILE.DK4')),'ARM9_sha256':sha(arm),
        'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'source_code_spans_exact_clean':[[a,b,sha(arm[a:b])] for a,b in spans],'role_groups':groups,
        'all50_original_role_helper_selections':cases,'records_with_immediate_storage_neighbors':records,
        'independent_voice_variants_not_consecutive_dialogue':True,
        'no_Sera_special_override_for_roles0_or7':True,
        'review_leads_not_final_translations':[
            {'message_id':1524,'issue':'Restore choosing between the two source sail types according to the wind.'},
            {'message_id':1528,'issue':'Restore the two distinct source sail types and their strong difference.'},
            {'message_id':1530,'issue':'Restore reading wind as competence for a fully fledged sail handler;do not invent a new sailmaster rank.'},
            {'message_id':1534,'issue':'Source says a dead calm remains difficult regardless of skill;current None beats a dead calm is ambiguous and can imply the opposite.'},
            {'message_id':1540,'issue':'Preserve the just-now back-cracking sound and comic reaction without an invented injury.'},
            {'message_id':1546,'issue':'Restore both leading from the front and taking command in boarding combat.'}],
        'completed_entries_added':0,'source_prose_review_credit_added':0,
        'not_manuscript_native_font_or_actual_display_approval':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'source_context_packet.json',packet)
    ledger['next_sails_boarding_source_packet']={'proof':str(ROOT/'source_context_packet.json'),
        'proof_sha256':sha((ROOT/'source_context_packet.json').read_bytes()),'native_message_IDs':list(range(1523,1547)),
        'status':'50-original-role-selectors-and-clean-current-packet-proved-prose-review-pending','no_completion_or_source_prose_credit':True}
    ledger['research_checkpoints'].append({'id':'V878-Sails-Boarding-context','proof':str(ROOT/'source_context_packet.json'),
        'original_numeric_helper_cases':50,'scope':'24 independent roles0/7 comments1523-1546 plus two storage neighbors;four real captains and all eight NPC voice classes.',
        'completed_entries_added':0,'source_prose_review_credit_added':0,'full_goal_complete':False})
    save('translations/editorial_review_current_v1.json',ledger)
    print('Next sails/boarding24 context:50 original helper selections pass;no editorial completion credit.',flush=True)


if __name__=='__main__':main()
