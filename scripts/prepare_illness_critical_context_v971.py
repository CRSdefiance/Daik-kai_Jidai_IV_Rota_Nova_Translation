"""Map the26 remaining physical comments from original condition4/5 tables and branches."""
import struct
from pathlib import Path
from shutil import copy2
from dk4tool.patch.physical_wounds_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import snapshot,machine_at,reference
from scripts.prepare_physical_fatigue_context_v957 import select,SPANS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/illness_critical_v971')
ROM=Path('out/all_routes_combined_v969_candidate.nds')
BASE=0x02000000
IDS=tuple(range(1807,1833))
FAMILIES={4:(1820,1828,1832,0x1257C,0x125F8,0x12504),5:(1807,1815,1819,0x12580,0x125FC,0x12508)}


def main():
    ROOT.mkdir(parents=True,exist_ok=True);packet_path=ROOT/'source_context_packet.json';assert not packet_path.exists()
    ledger=read('translations/editorial_review_current_v1.json');assert ledger['records_editorially_completed']==1092 and ledger['records_with_source_and_prose_pass']==1095
    current,clean,canonical=map(NdsImage.open,(ROM,'work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    assert sha(ROM.read_bytes())==ledger['current_integrated_candidate']['sha256']
    arm,j=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    for a,b in SPANS:assert arm[a:b]==j[a:b]
    literals=[]
    for condition,(npc_first,hero_first,sera_id,npc_literal,hero_literal,sera_literal) in FAMILIES.items():
        nt,ht=struct.unpack_from('<I',arm,npc_literal)[0],struct.unpack_from('<I',arm,hero_literal)[0]
        assert struct.unpack_from('<8I',arm,nt-BASE)==tuple(range(npc_first,npc_first+8))
        assert struct.unpack_from('<4I',arm,ht-BASE)==tuple(range(hero_first,hero_first+4))
        assert struct.unpack_from('<I',arm,sera_literal)[0]==sera_id
        assert arm[nt-BASE:nt-BASE+32]==j[nt-BASE:nt-BASE+32] and arm[ht-BASE:ht-BASE+16]==j[ht-BASE:ht-BASE+16]
        literals.append({'condition_ID':condition,'NPC_literal':npc_literal,'NPC_table':nt,'NPC_IDs':list(range(npc_first,npc_first+8)),
            'protagonist_literal':hero_literal,'protagonist_table':ht,'protagonist_IDs':list(range(hero_first,hero_first+4)),
            'Sera_literal':sera_literal,'Sera_ID':sera_id,'source_and_current_exact':True})
    npc,npc_receipt=snapshot('battle_personal_v897_893_Julio',14700);cpu,get=machine_at(arm,npc);actors=get(0xCB184)
    cases=[];controls=[]
    def record(actor,body,receipt,voice=None):
        helper=0x12584 if actor<4 else 0x12494 if actor==24 else 0x1250C
        for literal in literals:
            assert body[literal['NPC_table']-BASE:literal['NPC_table']-BASE+32]==arm[literal['NPC_table']-BASE:literal['NPC_table']-BASE+32]
            assert body[literal['protagonist_table']-BASE:literal['protagonist_table']-BASE+16]==arm[literal['protagonist_table']-BASE:literal['protagonist_table']-BASE+16]
        for status,(nfirst,hfirst,sera,*unused) in FAMILIES.items():
            expected=hfirst+actor if actor<4 else sera if actor==24 else nfirst+voice
            for name,entry,mode in [('direct_physical_helper',helper,(0,1)),('main_battle_status_priority',0x12104,(0,1)),('main_ordinary_status_priority',0x12104,(0,0))]:
                row=select(arm,body,actor,entry,mode,status,expected,receipt);row.update(case=name,native_voice_class=voice,Sera24_has_source_special_alternative=actor==24);cases.append(row)
        for status in (0,1,2,3):
            expected=None if status==0 else (1793 if actor==24 else 1789+actor if actor<4 else 1781+voice) if status==1 else (1806 if actor==24 else 1802+actor if actor<4 else 1794+voice)
            row=select(arm,body,actor,helper,(0,1),status,expected,receipt);row.update(case='prior_healthy_fatigue_or_wound_discriminating_control',native_voice_class=voice);controls.append(row)
    for actor in range(4,25):
        voice=get(0x7E988,actors+4+actor*32);assert 0<=voice<8;record(actor,npc,npc_receipt,voice)
    for actor,folder,frame in [(0,'personal_activity_v839_838_Rafael_later',3200),(1,'physical_wounds_v970_969_CaptainWound',16500),
            (2,'ceremony_Lil_approach_v825',23000),(3,'ceremony_Maria_approach_v825',26000)]:
        body,receipt=snapshot(folder,frame);record(actor,body,receipt)
    assert len(cases)==150 and len(controls)==100 and {r['selected_message_ID'] for r in cases}==set(IDS)
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),j);en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),arm)
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    records=[{'message_id':n,'selected_review_family':n in IDS,'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),
        'source_reference':reference(jp[n]),'current_English':en[n].text.decode('cp932'),'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),
        'canonical_text_hex':accepted[n].text.hex(),'prose_review_and_formatting_approval':False} for n in range(1806,1834)]
    save(packet_path,{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'COMMON_sha256':sha(current.read_file('/COMMON/MESFILE.DK4')),'ARM9_sha256':sha(arm),
        'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'source_code_spans_exact_clean':[[a,b,sha(arm[a:b])] for a,b in SPANS],
        'source_condition_IDs':[4,5],'source_literal_tables':literals,
        'condition4_selects_critical_sounding1820_1832_not_illness1807_1819':True,'condition5_selects_illness1807_1819':True,
        'labels_describe_source_dialogue_not_measured_injury_grade_death_probability_or_recovery_effects':True,
        'all150_original_direct_main_battle_and_ordinary_condition4_5_selections':cases,'all100_prior_condition0_1_2_3_discriminating_controls':controls,
        'four_genuine_protagonists_and21_NPCs_no_ID_substitution':True,'source_condition_byte6_only_with_declared_CPU_mode_fields':True,
        'job_role_and_mood_getters_not_called':True,'records_with_immediate_storage_neighbors':records,
        'review_leads_not_final_translations':[{'message_id':1816,'issue':'Preserve Hodrams personal admiral responsibility rather than a generic role maxim.'},
            {'message_id':1825,'issue':'Localize the death euphemism naturally,without inventing a family visitor or a literal escort.'},
            {'message_id':1828,'issue':'Preserve Rafaels unfinished dream and personal determination.'},
            {'message_id':1829,'issue':'Preserve Hodrams strongest-fleet ambition as his personal unfinished resolve.'},
            {'message_id':1830,'issue':'Use locked Camille for clean Japanese Kamil and retain Lils direct call in the death-fear fragment.'},
            {'message_id':1832,'issue':'Preserve Seras hesitant explicit wish not to die;do not erase the first person or add an outcome.'}],
        'completed_entries_added':0,'source_prose_review_credit_added':0,'original_select_helper':'scripts/prepare_physical_fatigue_context_v957.py',
        'original_select_helper_sha256':sha(Path('scripts/prepare_physical_fatigue_context_v957.py').read_bytes()),'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger['next_illness_critical_source_packet']={'proof':str(packet_path),'proof_sha256':sha(packet_path.read_bytes()),'native_message_IDs':list(IDS),
        'status':'150-original-condition4-5-selections100-prior-status-controls-proved-prose-pending','no_completion_or_source_prose_credit':True}
    ledger['research_checkpoints'].append({'id':'V971-Illness-Critical26-source-context','proof':str(packet_path),'original_selector_and_discriminating_control_cases':250,
        'completed_entries_added':0,'source_prose_review_credit_added':0,'scope':'26 remaining physical comments1807-1832. Source condition4 selects1820-1832 and5 selects1807-1819. Both direct/main ordinary/battle paths and prior statuses0-3 discriminated. CPU research only,no new prose,font,actual critical/illness display or earned-condition claim.','full_goal_complete':False})
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/illness_critical_v971_source_context.md')
    with doc.open('x',encoding='utf-8') as f:f.write('# V971: remaining physical-state source contexts\n\nTwenty-six comments1807-1832 map through original helpers1250C/12584/12494 and main12104. Source condition4 selects critical-sounding1820-1832,and5 selects illness1807-1819;literal tables and executed code establish this order. All150 direct/main ordinary/battle selections and100 prior-status0-3 controls pass over four genuine protagonists and21 NPCs. Only declared CPU condition byte6 and mode fields change. No prose/font/new actual scene or completion credit.1092 complete,1095 source/prose reviewed;full goal and separate graphics audit remain open.\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V971 Illness Critical source context');assert not archive.exists();copied=[]
    for p in (packet_path,Path(__file__),doc,Path('translations/editorial_review_current_v1.json')):
        target=archive/p.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(p,target)
        assert sha(p.read_bytes())==sha(target.read_bytes());copied.append({'source':str(p),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'no_new_completion_credit':True})
    print('Next26 physical comments:150 source4/5 selections and100 prior-status controls pass;no prose/completion credit.',flush=True)


if __name__=='__main__':main()
