"""Map original conditions2/3 to13 wound responses,with healthy and fatigue controls."""
import struct
from pathlib import Path
from shutil import copy2
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import snapshot,machine_at,reference
from scripts.prepare_physical_fatigue_context_v957 import select,SPANS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/physical_wounds_context_v2462')
ROM=Path('out/all_routes_combined_v2284_candidate.nds')
BASE=0x02000000
IDS=tuple(range(1794,1807))


def main():
    ROOT.mkdir(parents=True,exist_ok=True);packet_path=ROOT/'source_context_packet.json';assert not packet_path.exists()
    ledger=read('translations/editorial_review_current_v1.json');assert ledger['records_editorially_completed']==2143 and ledger['contextual_story_natural_dialogue_pass_v1871']['fresh_pass_records_integrated']==1818
    current,clean,canonical=map(NdsImage.open,(ROM,'work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    assert sha(ROM.read_bytes())==ledger['current_integrated_candidate']['sha256']
    arm,j=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    for a,b in SPANS:assert arm[a:b]==j[a:b]
    npc_table=struct.unpack_from('<I',arm,0x12578)[0];hero_table=struct.unpack_from('<I',arm,0x125F4)[0]
    assert struct.unpack_from('<8I',arm,npc_table-BASE)==tuple(range(1794,1802))
    assert struct.unpack_from('<4I',arm,hero_table-BASE)==tuple(range(1802,1806)) and struct.unpack_from('<I',arm,0x12500)[0]==1806
    npc,npc_receipt=snapshot('battle_personal_v897_893_Julio',14700);cpu,get=machine_at(arm,npc);actors=get(0xCB184)
    selections=[];healthy=[];fatigue=[]
    def record(actor,body,receipt,voice=None):
        helper=0x12584 if actor<4 else 0x12494 if actor==24 else 0x1250C
        expected=1802+actor if actor<4 else 1806 if actor==24 else 1794+voice
        for status in (2,3):
            for name,entry,mode in [('direct_physical_helper',helper,(0,1)),('main_battle_status_priority',0x12104,(0,1)),('main_ordinary_status_priority',0x12104,(0,0))]:
                row=select(arm,body,actor,entry,mode,status,expected,receipt)
                row.update(case=name,native_voice_class=voice,Sera24_has_source_special_alternative=actor==24)
                selections.append(row)
        row=select(arm,body,actor,helper,(0,1),0,None,receipt);row.update(case='healthy_direct_helper_no_message',native_voice_class=voice);healthy.append(row)
        prior=1789+actor if actor<4 else 1793 if actor==24 else 1781+voice
        row=select(arm,body,actor,helper,(0,1),1,prior,receipt);row.update(case='condition1_selects_prior_fatigue_not_wound',native_voice_class=voice);fatigue.append(row)
    for actor in range(4,25):
        voice=get(0x7E988,actors+4+actor*32);assert 0<=voice<8;record(actor,npc,npc_receipt,voice)
    for actor,folder,frame in [(0,'personal_activity_v839_838_Rafael_later',3200),(1,'physical_fatigue_v964_962_CaptainFatigue',16500),
            (2,'ceremony_Lil_approach_v825',23000),(3,'ceremony_Maria_approach_v825',26000)]:
        body,receipt=snapshot(folder,frame);record(actor,body,receipt)
    assert len(selections)==150 and len(healthy)==len(fatigue)==25 and {r['selected_message_ID'] for r in selections}==set(IDS)
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),j)
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),arm)
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    records=[{'message_id':n,'selected_review_family':n in IDS,'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),
        'source_reference':reference(jp[n]),'current_English':en[n].text.decode('cp932'),'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),
        'canonical_text_hex':accepted[n].text.hex(),'prose_review_and_formatting_approval':False} for n in range(1793,1808)]
    save(packet_path,{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'COMMON_sha256':sha(current.read_file('/COMMON/MESFILE.DK4')),'ARM9_sha256':sha(arm),
        'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'source_code_spans_exact_clean':[[a,b,sha(arm[a:b])] for a,b in SPANS],
        'source_condition_IDs':[2,3],'both_source_conditions_share_dialogue_family_not_all_gameplay_effects_claimed_equal':True,
        'condition2_3_wound_NPC_IDs':list(range(1794,1802)),'condition2_3_genuine_protagonist_IDs':list(range(1802,1806)),'Sera24_special_ID':1806,
        'all150_original_direct_main_battle_and_ordinary_wound_selections':selections,'all25_healthy_direct_helper_no_message_controls':healthy,
        'all25_condition1_prior_fatigue_discriminating_controls':fatigue,'four_genuine_protagonists_and21_NPCs_no_ID_substitution':True,
        'source_condition_byte6_only_with_declared_CPU_mode_fields':True,'job_role_and_mood_getters_not_called':True,
        'records_with_immediate_storage_neighbors':records,
        'review_leads_not_final_translations':[{'message_id':1797,'issue':'Preserve the unfinished personal reassurance rather than inventing its conclusion.'},
            {'message_id':1798,'issue':'Treat the spit remedy as rough character speech,not a medical or item-effect guarantee.'},
            {'message_id':1800,'issue':'Restore explicit personal injury;review old added Ow against source.'},
            {'message_id':1802,'issue':'Current English omits Rafaels unfinished personal resolve after the ongoing bleeding.'},
            {'message_id':1804,'issue':'Preserve Lils personal admiral responsibility and pain,not a generic maxim.'}],
        'completed_entries_added':0,'source_prose_review_credit_added':0,'original_select_helper':'scripts/prepare_physical_fatigue_context_v957.py',
        'original_select_helper_sha256':sha(Path('scripts/prepare_physical_fatigue_context_v957.py').read_bytes()),'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('150 current wound selections,25 healthy and25 fatigue controls pass;zero new editorial credit.',flush=True)
if __name__=='__main__':main()
