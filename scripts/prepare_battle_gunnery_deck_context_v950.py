"""Map24 next Gunnery/DeckCleaning battle alternatives without prose credit."""

import struct
from pathlib import Path
from shutil import copy2
from dk4tool.patch.battle_sails_boarding_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_battle_repair_medical_context_v899 import select
from scripts.prepare_work_comments_v842 import snapshot,machine_at,reference
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_gunnery_deck_v950')
ROM=Path('out/all_routes_combined_v947_candidate.nds')
BASE=0x02000000
GROUPS=((8,1757,1547,'Gunnery',True),(2,1769,1559,'DeckCleaning',True))
IDS=tuple(range(1757,1781))


def main():
    ROOT.mkdir(parents=True,exist_ok=True);assert not (ROOT/'source_context_packet.json').exists()
    current,clean,canonical=map(NdsImage.open,(ROM,'work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==1042 and ledger['records_with_source_and_prose_pass']==1045
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
            'ordinary_control_base':ordinary,'eight_NPC_and_four_genuine_protagonist_alternatives':has_npc})
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
        (1,'battle_sails_boarding_v948_947_CaptainSails',16500),(2,'ceremony_Lil_approach_v825',23000),
        (3,'ceremony_Maria_approach_v825',26000)]:
        body,rec=snapshot(folder,frame);record(actor,body,rec)
    assert len(cases)==150
    battle=[r for r in cases if r['case']!='main_ordinary_working_control']
    assert len(battle)==100 and {r['selected_message_ID'] for r in battle}==set(IDS)
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),arm)
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    records=[]
    for n in range(1756,1782):
        records.append({'message_id':n,'selected_review_family':n in IDS,
            'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),'source_reference':reference(jp[n]),
            'current_English':en[n].text.decode('cp932'),'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),
            'canonical_text_hex':accepted[n].text.hex(),'prose_review_and_formatting_approval':False})
    helper=Path('scripts/prepare_battle_repair_medical_context_v899.py')
    packet=ROOT/'source_context_packet.json'
    save(packet,{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'COMMON_sha256':sha(current.read_file('/COMMON/MESFILE.DK4')),
        'ARM9_sha256':sha(arm),'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'source_code_spans_exact_clean':[[a,b,sha(arm[a:b])] for a,b in spans],'role_groups':groups,
        'all150_original_battle_helper_main_and_ordinary_control_selections':cases,
        'records_with_immediate_storage_neighbors':records,'independent_voice_variants_not_consecutive_dialogue':True,
        'four_genuine_captains_and21_NPCs_no_actor_substitution':True,
        'no_Sera_special_role15_override_for_roles8_or2':True,
        'source_activity0_working_not_activity1_separate_helper126A8':True,
        'native_selector_fixture_helper':str(helper),'native_selector_fixture_helper_sha256':sha(helper.read_bytes()),
        'review_leads_not_final_translations':[
            {'message_id':1759,'issue':'Review established Aim terminology and source more shots versus current more hits using source help/mechanics.'},
            {'message_id':1763,'issue':'Restore personal intent to sink the enemy flagship,not passive guaranteed sinking.'},
            {'message_id':1764,'issue':'Resolve the established armed-battery room/equipment term before English wording.'},
            {'message_id':1768,'issue':'Order loading the next shot and imminent firing,not already-ready ammunition.'},
            {'message_id':1770,'issue':'Restore polite conditional offer to await orders during hand-to-hand combat.'},
            {'message_id':1778,'issue':'Restore Hodrams personal deck-cleaning intention while leaving combat to others.'},
            {'message_id':1779,'issue':'Preserve Lil leaving the naval battle to others,scrubbing sound and surprised recognition.'}],
        'completed_entries_added':0,'source_prose_review_credit_added':0,'not_manuscript_native_font_or_actual_new_Bridge_display_approval':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger['next_battle_gunnery_deck_source_packet']={'proof':str(packet),'proof_sha256':sha(packet.read_bytes()),'native_message_IDs':list(IDS),
        'status':'150-original-battle-context-and-ordinary-control-cases-proved-prose-pending','no_completion_or_source_prose_credit':True}
    ledger['research_checkpoints'].append({'id':'V950-Battle-Gunnery-Deck24-source-context','proof':str(packet),
        'native_selector_and_discriminating_control_cases':150,'completed_entries_added':0,'source_prose_review_credit_added':0,
        'scope':'Next24 activity0 Gunnery8/DeckCleaning2 battle comments1757-1780. Four genuine protagonist states and21 NPCs for both roles;no activity1 or actual new-room display credit.',
        'full_goal_complete':False})
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/battle_gunnery_deck_v950_source_context.md')
    with doc.open('x',encoding='utf-8') as f:f.write('# V950: next battle Gunnery/DeckCleaning source contexts\n\nNext24 entries1757-1780 are activity0 battle Gunnery8 and DeckCleaning2 comments. Original battle/ordinary tables and all150 direct/helper/main/ordinary controls pass for21 NPCs and four genuine protagonist states. These are independent working variants,not consecutive dialogue or activity1 helper126A8. Exact Japanese,current V947,canonical references and neighbors are saved. No prose,font,actual new-room or completion credit.1042 complete,1045 source/prose reviewed;full editorial goal and separate graphics audit stay open.\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V950 Battle Gunnery Deck source context');assert not archive.exists();copied=[]
    for source_path in (packet,Path(__file__),doc,Path('translations/editorial_review_current_v1.json')):
        target=archive/source_path.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source_path,target)
        assert sha(source_path.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source_path),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'no_new_completion_credit':True})
    print('Next24 battle Gunnery/DeckCleaning entries:150 original source/control cases pass;no prose or completion credit.',flush=True)


if __name__=='__main__':main()
