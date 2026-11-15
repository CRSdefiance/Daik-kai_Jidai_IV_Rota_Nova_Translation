"""Map28 next Captain/First Mate/Helm battle alternatives without prose credit."""

import struct
from pathlib import Path
from shutil import copy2
from dk4tool.patch.battle_finance_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_battle_repair_medical_context_v899 import select
from scripts.prepare_work_comments_v842 import snapshot,machine_at,reference
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_bridge_v924')
ROM=Path('out/all_routes_combined_v922_candidate.nds')
BASE=0x02000000
GROUPS=((5,1681,1471,'Captain',False),(6,1685,1475,'First Mate',True),(4,1697,1487,'Helm',True))
IDS=tuple(range(1681,1709))


def main():
    ROOT.mkdir(parents=True,exist_ok=True);assert not (ROOT/'source_context_packet.json').exists()
    current,clean,canonical=map(NdsImage.open,(ROM,'work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==966 and ledger['records_with_source_and_prose_pass']==969
    assert sha(ROM.read_bytes())==ledger['current_integrated_candidate']['sha256']
    arm,source=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    spans=((0x12104,0x12920),(0x53C6C,0x53CB0),(0x53F4C,0x53F9C),(0x3F0F8,0x3F100))
    assert all(arm[a:b]==source[a:b] for a,b in spans)
    nt,ht=struct.unpack_from('<I',arm,0x126A4)[0],struct.unpack_from('<I',arm,0x12788)[0]
    ont,oht=struct.unpack_from('<I',arm,0x12834)[0],struct.unpack_from('<I',arm,0x1291C)[0]
    groups=[]
    for role,first,ordinary,label,has_npc in GROUPS:
        npc,hero=struct.unpack_from('<I',arm,nt-BASE+role*4)[0],struct.unpack_from('<I',arm,ht-BASE+role*4)[0]
        onpc,ohero=struct.unpack_from('<I',arm,ont-BASE+role*4)[0],struct.unpack_from('<I',arm,oht-BASE+role*4)[0]
        hero_first=first+8 if has_npc else first;ordinary_hero=ordinary+8 if has_npc else ordinary
        assert struct.unpack_from('<4I',arm,hero-BASE)==tuple(range(hero_first,hero_first+4))
        assert struct.unpack_from('<4I',arm,ohero-BASE)==tuple(range(ordinary_hero,ordinary_hero+4))
        if has_npc:
            assert struct.unpack_from('<8I',arm,npc-BASE)==tuple(range(first,first+8))
            assert struct.unpack_from('<8I',arm,onpc-BASE)==tuple(range(ordinary,ordinary+8))
        else:assert npc==onpc==0
        groups.append({'role_ID':role,'label':label,'NPC_pointer':npc,'NPC_IDs':list(range(first,first+8)) if has_npc else [],
            'actual_protagonist_pointer':hero,'protagonist_IDs':list(range(hero_first,hero_first+4)),
            'ordinary_control_base':ordinary,'Captain5_only_has_four_genuine_protagonist_alternatives':not has_npc})
    raw,receipt=snapshot('battle_personal_v897_893_Julio',14700)
    cpu,get=machine_at(arm,raw);actors=get(0xCB184);cases=[]
    def record(actor,body,rec,voice=None):
        for role,first,ordinary,label,has_npc in GROUPS:
            if actor>=4 and not has_npc:continue
            suffix=8+actor if actor<4 and has_npc else actor if actor<4 else voice
            helper=0x12720 if actor<4 else 0x12600
            for kind,entry,mode,expected in [('direct_battle_working',helper,(0,1),first+suffix),
                ('main_battle_working',0x12104,(0,1),first+suffix),
                ('main_ordinary_working_control',0x12104,(0,0),ordinary+suffix)]:
                row=select(arm,body,actor,role,mode,entry,expected)
                row.update(case=kind,native_voice_class=voice,source_RAM=rec,
                    source_activity_state=0 if entry==0x12104 else None,
                    not_separate_activity1_helper126A8=True)
                cases.append(row)
    for actor in range(4,25):
        voice=get(0x7E988,actors+4+actor*32);assert 0<=voice<8
        record(actor,raw,receipt,voice)
    for actor,folder,frame in [(0,'personal_activity_v839_838_Rafael_later',3200),
        (1,'battle_finance_v923_922_CaptainFinance',16500),(2,'ceremony_Lil_approach_v825',23000),
        (3,'ceremony_Maria_approach_v825',26000)]:
        body,rec=snapshot(folder,frame);record(actor,body,rec)
    assert len(cases)==162
    battle=[r for r in cases if r['case']!='main_ordinary_working_control']
    assert len(battle)==108 and {r['selected_message_ID'] for r in battle}==set(IDS)
    assert all(r['actor_ID']<4 for r in cases if r['source_role_type']==5)
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),arm)
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    records=[]
    for n in range(1680,1710):
        records.append({'message_id':n,'selected_review_family':n in IDS,
            'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),'source_reference':reference(jp[n]),
            'current_English':en[n].text.decode('cp932'),'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),
            'canonical_text_hex':accepted[n].text.hex(),'prose_review_and_formatting_approval':False})
    helper=Path('scripts/prepare_battle_repair_medical_context_v899.py')
    packet=ROOT/'source_context_packet.json'
    save(packet,{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'COMMON_sha256':sha(current.read_file('/COMMON/MESFILE.DK4')),
        'ARM9_sha256':sha(arm),'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'source_code_spans_exact_clean':[[a,b,sha(arm[a:b])] for a,b in spans],'role_groups':groups,
        'all162_original_battle_helper_main_and_ordinary_control_selections':cases,
        'records_with_immediate_storage_neighbors':records,'independent_voice_variants_not_consecutive_dialogue':True,
        'four_genuine_captains_and21_NPCs_no_actor_substitution':True,
        'Captain5_null_NPC_tables_preserved_and_never_called_as_supported_alternatives':True,
        'source_activity0_working_not_activity1_separate_helper126A8':True,
        'native_selector_fixture_helper':str(helper),'native_selector_fixture_helper_sha256':sha(helper.read_bytes()),
        'review_leads_not_final_translations':[
            {'message_id':1682,'issue':'Review covering-fire and deck-crew hand-to-hand preparation rather than generic gunners fire.'},
            {'message_id':1683,'issue':'Preserve Camille and replace obsolete full-width initial I only through complete native glyph proof.'},
            {'message_id':1684,'issue':'Source Xien name is currently Shen;review established Xien spelling and the battle-status request.'},
            {'message_id':1687,'issue':'Captain/First Mate requirement for city surrender must not become a guarantee that a city yields.'},
            {'message_id':1706,'issue':'Review charging the enemy ship versus an invented equipped ram;preserve the explicit Gerhard boarding order.'}],
        'completed_entries_added':0,'source_prose_review_credit_added':0,'not_manuscript_native_font_or_actual_new_Bridge_display_approval':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger['next_battle_bridge_source_packet']={'proof':str(packet),'proof_sha256':sha(packet.read_bytes()),'native_message_IDs':list(IDS),
        'status':'162-original-battle-context-and-ordinary-control-cases-proved-prose-pending','no_completion_or_source_prose_credit':True}
    ledger['research_checkpoints'].append({'id':'V924-Battle-Bridge28-source-context','proof':str(packet),
        'native_selector_and_discriminating_control_cases':162,'completed_entries_added':0,'source_prose_review_credit_added':0,
        'scope':'Next28 activity0 Captain5/FirstMate6/Helm4 battle comments1681-1708. NPC Captain5 tables are null and not called. Four real captain states,21 NPCs for two supported NPC roles;no activity1 or actual new-room display credit.',
        'full_goal_complete':False})
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/battle_bridge_v924_source_context.md')
    with doc.open('x',encoding='utf-8') as f:f.write('# V924: next battle Bridge source contexts\n\n'
        'Next28 entries1681-1708 are activity0 battle Captain5,First Mate6 and Helm4 comments. Original battle and ordinary tables are source-verified. Captain5 has four genuine-protagonist alternatives and null NPC tables;no unsupported NPC Captain5 call is made. All162 direct battle/helper,main battle and ordinary controls pass for the supported cases. These are working comments,not the separate activity1 helper126A8. Exact clean Japanese,current V922,canonical references and storage neighbors are saved. No prose,font,actual Bridge scene or completion credit.966 complete,969 source/prose reviewed;full editorial goal and separate graphics audit remain open.\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V924 Battle Bridge source context');assert not archive.exists();copied=[]
    for source_path in (packet,Path(__file__),doc,Path('translations/editorial_review_current_v1.json')):
        target=archive/source_path.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source_path,target)
        assert sha(source_path.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source_path),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'no_new_completion_credit':True})
    print('Next28 battle Bridge entries:162 original source/control cases pass;no prose or completion credit.',flush=True)


if __name__=='__main__':main()
