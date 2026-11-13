"""Inventory13 independent cooking comments and prove the special Sera branch."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.work_comments_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import snapshot,machine_at,reference
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/cooking_comments_v847')
ROM=Path('out/all_routes_combined_v845_candidate.nds')
BASE=0x02000000


def select(arm,raw,actor,expected):
    cpu,get=machine_at(arm,raw)
    controller=get(0xCB1A8)+0x2090;model=get(0x82E04,controller)
    # CPU-only role/occupant fixture,not a live assignment or earned role.
    cpu.mem_write(model+0x1E+12,bytes([15]))
    for slot in range(31):
        if get(0x82BC4,controller,slot)==actor:get(0x82BA8,controller,slot)
    get(0x82BB8,controller,12,actor)
    assert get(0x81F54,controller,actor)==15
    chosen=[]
    def numeric(u,pc,size,unused):
        chosen.append(u.reg_read(UC_ARM_REG_R0))
        u.reg_write(UC_ARM_REG_R0,0x02450000)
        u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    helper=0x128B4 if actor<4 else 0x1278C
    hook=cpu.hook_add(UC_HOOK_CODE,numeric,begin=BASE+0x5528C,end=BASE+0x5528C)
    try:get(helper,actor)
    finally:cpu.hook_del(hook)
    assert chosen==[expected],(actor,chosen,expected)
    return {'actor_ID':actor,'source_helper':BASE+helper,'source_role_type':15,
        'selected_message_ID':expected,'complete_native_helper_and_ABI_pass':True,
        'CPU_role_assignment_only_no_text_or_actor_record_replacement':True,
        'ordinary_condition_gate_and_actual_display_not_claimed':True}


def main():
    assert not (ROOT/'source_context_packet.json').exists()
    ROOT.mkdir(parents=True,exist_ok=True)
    current,clean,canonical=map(NdsImage.open,(ROM,'work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    ledger=read('translations/editorial_review_current_v1.json')
    assert sha(ROM.read_bytes())==ledger['current_integrated_candidate']['sha256']
    arm,source=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    spans=((0x12104,0x12920),(0x53C6C,0x53CB0),(0x53F4C,0x53F9C))
    assert all(arm[a:b]==source[a:b] for a,b in spans)
    npc_table,hero_table=struct.unpack_from('<I',arm,0x12834)[0],struct.unpack_from('<I',arm,0x1291C)[0]
    npc=struct.unpack_from('<I',arm,npc_table-BASE+15*4)[0]
    hero=struct.unpack_from('<I',arm,hero_table-BASE+15*4)[0]
    assert struct.unpack_from('<8I',arm,npc-BASE)==tuple(range(1410,1418))
    assert struct.unpack_from('<4I',arm,hero-BASE)==tuple(range(1418,1422))
    assert struct.unpack_from('<I',arm,0x1282C)[0]==1422
    raw,receipt=snapshot('personal_cabin_v840_838_Charles_after',3200)
    cpu,get=machine_at(arm,raw);actors=get(0xCB184)
    cases=[]
    for actor in range(4,25):
        voice=get(0x7E988,actors+4+actor*32)
        assert 0<=voice<8
        row=select(arm,raw,actor,1422 if actor==24 else 1410+voice)
        row.update(native_voice_class=voice,source_RAM=receipt,special_Sera_branch_overrides_ordinary_voice=(actor==24))
        cases.append(row)
    for actor,folder,frame in [(0,'personal_activity_v839_838_Rafael_later',3200),
        (1,'personal_cabin_v840_838_Charles_after',3200),(2,'ceremony_Lil_approach_v825',23000),
        (3,'ceremony_Maria_approach_v825',26000)]:
        hraw,hrec=snapshot(folder,frame);_,hget=machine_at(arm,hraw);assert hget(0x7F244)==actor
        row=select(arm,hraw,actor,1418+actor)
        row.update(source_RAM=hrec,actual_original_captain_ID_preserved=actor)
        cases.append(row)
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),arm)
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    records=[]
    for n in range(1409,1424):
        records.append({'message_id':n,'selected_cooking_family':1410<=n<=1422,
            'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),'source_reference':reference(jp[n]),
            'current_English':en[n].text.decode('cp932'),'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),
            'canonical_text_hex':accepted[n].text.hex(),'prose_review_and_formatting_approval':False})
    packet={'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'COMMON_sha256':sha(current.read_file('/COMMON/MESFILE.DK4')),'ARM9_sha256':sha(arm),
        'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'source_code_spans_exact_clean':[[a,b,sha(arm[a:b])] for a,b in spans],
        'role15_Cook_NPC_group':npc,'NPC_IDs':list(range(1410,1418)),
        'role15_actual_protagonist_group':hero,'protagonist_IDs':list(range(1418,1422)),
        'special_Sera_actor24_ID':1422,'special_branch':'127BC CMP role15;127D8 CMP actor24;127E0 loads ID1422 from literal1282C;127E4 calls5528C.',
        'all25_original_role_helper_selections':cases,'records_with_immediate_storage_neighbors':records,
        'independent_alternatives_not_a_conversation_sequence':True,
        'findings_pending_editorial_review':[
            {'message_id':1419,'issue':'Current My apprentice handiwork loses the retrospective thought that the speaker often cooked this during his apprenticeship. Original hero1 selector is proven;do not invent his profession or a new rank.'},
            {'message_id':1422,'issue':'Special Sera cooking line bypasses the eight-voice table. Include it rather than declaring cooking complete after only12 ordinary entries. Review her short source phrasing in character before choosing English.'}],
        'completed_entries_added':0,'source_prose_review_credit_added':0,
        'not_manuscript_or_native_font_actual_display_approval':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'source_context_packet.json',packet)
    ledger['next_cooking_source_packet']={'proof':str(ROOT/'source_context_packet.json'),
        'proof_sha256':sha((ROOT/'source_context_packet.json').read_bytes()),'native_message_IDs':list(range(1410,1423)),
        'status':'25-native-role-selections-and-source-current-packet-proved-prose-review-pending','no_completion_or_source_prose_credit':True}
    ledger['research_checkpoints'].append({'id':'V847-Cooking-context-and-Sera-extra-selection',
        'proof':str(ROOT/'source_context_packet.json'),'original_numeric_helper_cases':25,
        'scope':'13 independent cooking records1410-1422 plus two storage neighbors. Four actual captain states;no fake captain IDs.',
        'completed_entries_added':0,'source_prose_review_credit_added':0,'full_goal_complete':False})
    save('translations/editorial_review_current_v1.json',ledger)
    print('Next cooking13 context:25 original helper selections pass,including special Sera1422;no editorial completion credit.',flush=True)


if __name__=='__main__':main()
