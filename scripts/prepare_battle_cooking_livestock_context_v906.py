"""Next25 Galley15/Livestock17 contexts,including Seras actual Galley override."""

import struct
from pathlib import Path
from shutil import copy2
from dk4tool.patch.battle_repair_medical_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_battle_repair_medical_context_v899 import select
from scripts.prepare_work_comments_v842 import snapshot,machine_at,reference
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_cooking_livestock_v906')
ROM=Path('out/all_routes_combined_v904_candidate.nds')
BASE=0x02000000
GROUPS=((15,1620,1410,'Battle cooking'),(17,1633,1423,'Battle livestock'))


def main():
    ROOT.mkdir(parents=True,exist_ok=True);assert not (ROOT/'source_context_packet.json').exists()
    current,clean,canonical=map(NdsImage.open,(ROM,'work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    ledger=read('translations/editorial_review_current_v1.json')
    assert sha(ROM.read_bytes())==ledger['current_integrated_candidate']['sha256']
    assert ledger['records_editorially_completed']==905 and ledger['records_with_source_and_prose_pass']==908
    arm,source=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    spans=((0x12104,0x12920),(0x53C6C,0x53CB0),(0x53F4C,0x53F9C),(0x3F0F8,0x3F100))
    assert all(arm[a:b]==source[a:b] for a,b in spans)
    npc_table=struct.unpack_from('<I',arm,0x126A4)[0];hero_table=struct.unpack_from('<I',arm,0x12788)[0]
    ordinary_npc_table=struct.unpack_from('<I',arm,0x12834)[0]
    ordinary_hero_table=struct.unpack_from('<I',arm,0x1291C)[0]
    assert struct.unpack_from('<I',arm,0x1282C)[0]==1422
    groups=[]
    for role,first,ordinary,label in GROUPS:
        npc=struct.unpack_from('<I',arm,npc_table-BASE+role*4)[0];hero=struct.unpack_from('<I',arm,hero_table-BASE+role*4)[0]
        assert npc and hero
        assert struct.unpack_from('<8I',arm,npc-BASE)==tuple(range(first,first+8))
        assert struct.unpack_from('<4I',arm,hero-BASE)==tuple(range(first+8,first+12))
        ordinary_npc=struct.unpack_from('<I',arm,ordinary_npc_table-BASE+role*4)[0]
        ordinary_hero=struct.unpack_from('<I',arm,ordinary_hero_table-BASE+role*4)[0]
        assert struct.unpack_from('<8I',arm,ordinary_npc-BASE)==tuple(range(ordinary,ordinary+8))
        assert struct.unpack_from('<4I',arm,ordinary_hero-BASE)==tuple(range(ordinary+8,ordinary+12))
        groups.append({'role_ID':role,'label':label,'NPC_pointer':npc,'NPC_IDs':list(range(first,first+8)),
            'actual_protagonist_pointer':hero,'protagonist_IDs':list(range(first+8,first+12)),
            'ordinary_control_base':ordinary,'additional_Sera_battle_ID':1632 if role==15 else None})
    assert arm[0x1264C:0x12660]==source[0x1264C:0x12660]
    mood_raw,mood_receipt=snapshot('battle_repair_medical_v905_904_CamilleMedical',16100)
    mood_cpu,mood_get=machine_at(arm,mood_raw);mood_actor=mood_get(0xCB184)+4+18*32
    assert mood_get(0x7E100,mood_actor)==0 and mood_get(0x7E0B4,mood_actor)==0
    mood_control=select(arm,mood_raw,18,15,(0,1),0x12104,1833)
    mood_control.update(source_RAM=mood_receipt,condition_getter_value=0,mood_getter_value=0,
        not_forced_to_working_comment=True,not_editorially_reviewed_or_actual_body_credit=True)
    raw,receipt=snapshot('battle_personal_v897_893_Julio',14700);cpu,get=machine_at(arm,raw);actors=get(0xCB184)
    cases=[]
    def record(actor,body,rec,voice=None):
        for role,first,ordinary,label in GROUPS:
            suffix=8+actor if actor<4 else voice;helper=0x12720 if actor<4 else 0x12600
            for kind,entry,mode,expected in [('direct_battle_working',helper,(0,1),first+suffix),
                ('main_battle_working',0x12104,(0,1),first+suffix),
                ('main_ordinary_working_control',0x12104,(0,0),ordinary+suffix)]:
                if role==15 and actor==24:expected=1422 if kind=='main_ordinary_working_control' else 1632
                r=select(arm,body,actor,role,mode,entry,expected)
                r.update(case=kind,native_voice_class=voice,source_RAM=rec,
                    Sera_specific_Galley_override_executed=role==15 and actor==24)
                cases.append(r)
    for actor in range(4,25):
        voice=get(0x7E988,actors+4+actor*32);assert 0<=voice<8
        record(actor,raw,receipt,voice)
    for actor,folder,frame in [(0,'personal_activity_v839_838_Rafael_later',3200),
        (1,'battle_repair_medical_v905_904_CaptainRepair',14700),(2,'ceremony_Lil_approach_v825',23000),
        (3,'ceremony_Maria_approach_v825',26000)]:
        body,rec=snapshot(folder,frame);record(actor,body,rec)
    assert len(cases)==150
    assert {r['selected_message_ID'] for r in cases if r['case']!='main_ordinary_working_control'}==set(range(1620,1645))
    assert len([r for r in cases if r['Sera_specific_Galley_override_executed']])==3
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),arm)
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    records=[]
    for n in range(1619,1646):
        records.append({'message_id':n,'selected_review_family':1620<=n<=1644,
            'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),'source_reference':reference(jp[n]),
            'current_English':en[n].text.decode('cp932'),'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),
            'canonical_text_hex':accepted[n].text.hex(),'prose_review_and_formatting_approval':False})
    packet=ROOT/'source_context_packet.json'
    save(packet,{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'COMMON_sha256':sha(current.read_file('/COMMON/MESFILE.DK4')),'ARM9_sha256':sha(arm),
        'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'source_code_spans_exact_clean':[[a,b,sha(arm[a:b])] for a,b in spans],'role_groups':groups,
        'all150_original_battle_helper_main_and_ordinary_control_selections':cases,
        'additional_original_mood_response_control':{**mood_control,'source_Japanese':jp[1833].text.decode('cp932'),
            'source_reference':reference(jp[1833]),'current_English':en[1833].text.decode('cp932'),
            'current_reference':reference(en[1833]),
            'note':'Actual Charles model with mood getter0 selects1833 rather than Galley1620. Its Japanese says he is feeling on a roll;do not label this as fear or alter the model to hide it. Normal working cases use a separately recorded genuine battle snapshot with eligible original mood.'},
        'records_with_immediate_storage_neighbors':records,'independent_voice_variants_not_consecutive_dialogue':True,
        'four_genuine_captains_and21_NPCs_no_actor_substitution':True,
        'Sera_role15_battle1632_and_ordinary1422_overrides_proved':True,
        'Sera_role17_uses_ordinary_native_voice_table_not_the_Galley_override':True,
        'duty_labels_source_verified_Galley15_and_Livestock17_not_Chapel18':True,
        'initial_static_inventory_rejected_null_roles10_11_and_out_of_table_role21_before_any_gameplay_call':True,
        'initial_ordinary_cooking_base1411_guess_rejected_by_native_selector_before_packet_write':True,
        'review_leads_not_final_translations':[
            {'message_id':1629,'issue':'Source captain1 questions whether he should be cooking;old English replaces the speaker with a generic cook.'},
            {'message_id':1631,'issue':'Review hesitant morale question naturally and remove inherited manual padding only through the compiler.'},
            {'message_id':1632,'issue':'Source Sera offers this food before fighting;do not expand one battle into a whole war or omit this.'},
            {'message_id':1633,'issue':'Preserve the explicitly frightened pig and cannon sound.'},
            {'message_id':1644,'issue':'The assigned livestock context makes this reassurance to animals,not an assertion about the campaign ending.'}],
        'upstream_selector_source':'scripts/prepare_battle_repair_medical_context_v899.py',
        'upstream_selector_source_sha256':sha(Path('scripts/prepare_battle_repair_medical_context_v899.py').read_bytes()),
        'completed_entries_added':0,'source_prose_review_credit_added':0,
        'not_manuscript_native_font_or_actual_cooking_livestock_display_approval':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger['next_battle_cooking_livestock_source_packet']={'proof':str(packet),'proof_sha256':sha(packet.read_bytes()),
        'native_message_IDs':list(range(1620,1645)),'status':'150-original-battle-ordinary-and-Sera-override-controls-proved-prose-pending',
        'no_completion_or_source_prose_credit':True}
    ledger['research_checkpoints'].append({'id':'V906-Battle-cooking-livestock25-source-context','proof':str(packet),
        'native_selector_and_discriminating_control_cases':150,'completed_entries_added':0,'source_prose_review_credit_added':0,
        'scope':'Next25 Galley15/Livestock17 comments1620-1644,including original Sera24 Galley-specific1632 override. Isolated CPU contexts only;no actual new-room display or editorial credit.',
        'full_goal_complete':False})
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/battle_cooking_livestock_v906_source_context.md')
    with doc.open('x',encoding='utf-8') as f:f.write('# V906: next battle cooking and livestock source contexts\n\nNext25 entries1620-1644 belong to Galley15 and Livestock17. The original Sera24 Galley override chooses battle1632 and ordinary1422 before the NPC voice table;it is not a Chapel/prayer branch. All150 direct battle helper,main battle and ordinary controls pass with21 NPCs and four genuine captains. A separately preserved actual Charles state with mood getter0 selects1833,whose Japanese says he feels on a roll,rather than a work comment. This is retained as an additional native eligibility control and unreviewed lead;no actor mood is changed to hide it. Normal working cases use a separately hash-checked genuine battle snapshot with eligible original mood. Null unsupported roles and an out-of-table static pointer were rejected during initial inventory;no gameplay call was made for them. The guessed ordinary cooking base1411 was rejected by the native selector;source tables prove1410 with special1422. Exact clean Japanese,current V904,canonical references and storage neighbors are saved. No prose,font,actual new-room or completion credit.905 complete,908 source/prose reviewed;full editorial goal and separate graphics audit remain open.\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V906 Battle cooking livestock source context');assert not archive.exists();copied=[]
    for p in (packet,Path(__file__),doc,Path('translations/editorial_review_current_v1.json')):
        target=archive/p.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(p,target)
        assert sha(p.read_bytes())==sha(target.read_bytes());copied.append({'source':str(p),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'no_new_completion_credit':True})
    print('Next battle cooking/livestock25:150 original context/control cases including Sera override pass;no prose/completion credit.',flush=True)


if __name__=='__main__':main()
