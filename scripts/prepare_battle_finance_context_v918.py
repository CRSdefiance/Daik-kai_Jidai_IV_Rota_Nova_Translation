"""Next24 battle Chapel/Planning source contexts;no editorial completion credit."""

import struct
from pathlib import Path
from shutil import copy2
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_R0

from dk4tool.patch.battle_chapel_planning_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import snapshot,machine_at,reference
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_finance_v918')
ROM=Path('out/all_routes_combined_v916_candidate.nds')
BASE=0x02000000
GROUPS=((20,1669,1459,'Battle Finance'),)


def select(arm,raw,actor,role,mode,helper,expected):
    cpu,get=machine_at(arm,raw);hero=get(0x7F244)
    if actor<4:assert hero==actor
    context=get(0x3F0F8);original=list(struct.unpack('<2I',cpu.mem_read(context+8,8)))
    cpu.mem_write(context+8,struct.pack('<2I',*mode))
    controller=get(0xCB1A8)+0x2090;model=get(0x82E04,controller)
    cpu.mem_write(model+0x1E+12,bytes([role]))
    for slot in range(31):
        if get(0x82BC4,controller,slot)==actor:get(0x82BA8,controller,slot)
    get(0x82BB8,controller,12,actor);assert get(0x81F54,controller,actor)==role
    chosen=[]
    def numeric(u,pc,size,unused):
        chosen.append(u.reg_read(UC_ARM_REG_R0));u.reg_write(UC_ARM_REG_R0,0x02450000)
        u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    hook=cpu.hook_add(UC_HOOK_CODE,numeric,begin=BASE+0x5528C,end=BASE+0x5528C)
    try:get(helper,actor,*((0,) if helper==0x12104 else ()))
    finally:cpu.hook_del(hook)
    assert chosen==[expected],(actor,role,mode,hex(helper),chosen,expected)
    assert get(0x7F244)==hero
    return {'actor_ID':actor,'genuine_captain_ID':hero,'source_helper':BASE+helper,'source_role_type':role,
        'original_mode_fields8_12':original,'isolated_CPU_mode_fields8_12':list(mode),
        'selected_message_ID':expected,'complete_native_helper_and_ABI_pass':True,
        'CPU_room_assignment_and_mode_fixture_only_no_actor_or_text_replacement':True,
        'not_native_font_actual_Finance_room_or_gameplay_credit':True}


def main():
    ROOT.mkdir(parents=True,exist_ok=True);assert not (ROOT/'source_context_packet.json').exists()
    current,clean,canonical=map(NdsImage.open,(ROM,'work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    ledger=read('translations/editorial_review_current_v1.json')
    assert sha(ROM.read_bytes())==ledger['current_integrated_candidate']['sha256']
    assert ledger['records_editorially_completed']==954 and ledger['records_with_source_and_prose_pass']==957
    arm,source=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    spans=((0x12104,0x12920),(0x53C6C,0x53CB0),(0x53F4C,0x53F9C),(0x3F0F8,0x3F100))
    assert all(arm[a:b]==source[a:b] for a,b in spans)
    npc_table=struct.unpack_from('<I',arm,0x126A4)[0];hero_table=struct.unpack_from('<I',arm,0x12788)[0]
    groups=[]
    for role,first,ordinary,label in GROUPS:
        npc=struct.unpack_from('<I',arm,npc_table-BASE+role*4)[0]
        hero=struct.unpack_from('<I',arm,hero_table-BASE+role*4)[0]
        assert struct.unpack_from('<8I',arm,npc-BASE)==tuple(range(first,first+8))
        assert struct.unpack_from('<4I',arm,hero-BASE)==tuple(range(first+8,first+12))
        groups.append({'role_ID':role,'label':label,'NPC_pointer':npc,'NPC_IDs':list(range(first,first+8)),
            'actual_protagonist_pointer':hero,'protagonist_IDs':list(range(first+8,first+12)),
            'ordinary_control_base':ordinary})
    raw,receipt=snapshot('battle_personal_v897_893_Julio',14700);cpu,get=machine_at(arm,raw);actors=get(0xCB184)
    cases=[]
    def record_cases(actor,body,rec,voice=None):
        for role,first,ordinary,label in GROUPS:
            suffix=8+actor if actor<4 else voice
            helper=0x12720 if actor<4 else 0x12600
            for kind,entry,mode,expected in [('direct_battle_working',helper,(0,1),first+suffix),
                ('main_battle_working',0x12104,(0,1),first+suffix),
                ('main_ordinary_working_control',0x12104,(0,0),ordinary+suffix)]:
                r=select(arm,body,actor,role,mode,entry,expected)
                r.update(case=kind,native_voice_class=voice,source_RAM=rec);cases.append(r)
    for actor in range(4,25):
        voice=get(0x7E988,actors+4+actor*32);assert 0<=voice<8
        record_cases(actor,raw,receipt,voice)
    for actor,folder,frame in [(0,'personal_activity_v839_838_Rafael_later',3200),
        (1,'battle_chapel_planning_v917_916_CaptainChapelDelayed',16500),(2,'ceremony_Lil_approach_v825',23000),
        (3,'ceremony_Maria_approach_v825',26000)]:
        body,rec=snapshot(folder,frame);record_cases(actor,body,rec)
    assert len(cases)==75
    battle=[r for r in cases if r['case']!='main_ordinary_working_control']
    assert {r['selected_message_ID'] for r in battle}==set(range(1669,1681))
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),arm)
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    records=[]
    for n in range(1668,1682):
        records.append({'message_id':n,'selected_review_family':1669<=n<=1680,
            'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),'source_reference':reference(jp[n]),
            'current_English':en[n].text.decode('cp932'),'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),
            'canonical_text_hex':accepted[n].text.hex(),'prose_review_and_formatting_approval':False})
    packet=ROOT/'source_context_packet.json'
    save(packet,{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'COMMON_sha256':sha(current.read_file('/COMMON/MESFILE.DK4')),'ARM9_sha256':sha(arm),
        'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'source_code_spans_exact_clean':[[a,b,sha(arm[a:b])] for a,b in spans],'role_groups':groups,
        'all75_original_battle_helper_main_and_ordinary_control_selections':cases,
        'records_with_immediate_storage_neighbors':records,'independent_voice_variants_not_consecutive_dialogue':True,
        'four_genuine_captains_and21_NPCs_no_actor_substitution':True,
        'source_battle_predicate_fields8_12':[0,1],'actual_battle_snapshots_used_for_NPCs_and_genuine_captain1':True,
        'no_Sera_special_role15_override_for_role20':True,
        'review_leads_not_final_translations':[],
        'completed_entries_added':0,'source_prose_review_credit_added':0,
        'not_manuscript_native_font_or_actual_Finance_display_approval':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger['next_battle_finance_source_packet']={'proof':str(packet),'proof_sha256':sha(packet.read_bytes()),
        'native_message_IDs':list(range(1669,1681)),'status':'75-original-battle-context-and-ordinary-control-cases-proved-prose-pending',
        'no_completion_or_source_prose_credit':True}
    ledger['research_checkpoints'].append({'id':'V918-Battle-Finance12-source-context','proof':str(packet),
        'native_selector_and_discriminating_control_cases':75,'completed_entries_added':0,'source_prose_review_credit_added':0,
        'scope':'Next12 original role20 battle comments1669-1680;21 native NPC voice mappings and four genuine captains. Isolated CPU room/mode controls only;no actual new Finance body activation.',
        'full_goal_complete':False})
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/battle_finance_v918_source_context.md')
    with doc.open('x',encoding='utf-8') as f:f.write('# V918: next battle Finance source contexts\n\nNext12 entries1669-1680 map to original Finance20 duties. All75 direct battle-helper,main battle-selector and ordinary-context controls pass for21 NPCs and four genuine captains. NPCs use the genuine Julio battle snapshot;captain1 uses the genuine V916 delayed-Chapel battle capture. Other heroes retain their genuine models with declared CPU mode controls. Exact clean Japanese,current V916 and canonical references and immediate storage neighbors are saved. Independent voice alternatives are not consecutive speech. No prose,font,actual new Finance room or completion credit.954 complete,957 source/prose reviewed;full editorial goal and separate graphics audit remain open.\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V918 Battle Finance source context');assert not archive.exists();rows=[]
    for p in (packet,Path(__file__),doc,Path('translations/editorial_review_current_v1.json')):
        target=archive/p.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(p,target)
        assert sha(p.read_bytes())==sha(target.read_bytes());rows.append({'source':str(p),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':rows,'all_hashes_verified':True,'no_new_completion_credit':True})
    print('Next battle Finance12:all75 original context/control cases pass;no prose/completion credit.',flush=True)


if __name__=='__main__':main()
