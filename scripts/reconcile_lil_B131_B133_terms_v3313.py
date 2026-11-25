"""Bind complete item pointers, approved names andexact share directions."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B131_B133_terms_v3313')
SOURCE=Path('work/analysis/lil_remaining_B131_B140_source_v3306b/next63_B131_B133_clean_current_context.json')
VOICE=Path('work/analysis/lil_B131_B133_voices_v3307b/current_five_static_names_voices_selector00_and207_catalog_rebind.json')
CONTEXT=Path('work/analysis/lil_B131_B133_clean_context_v3312/all63_complete_clean_context_and_fresh_glosses.json')
CATALOG=Path('translations/all_item_names_arm9_v1.json')
PROOF=Path('work/analysis/lil_B122_B127_terms_v3267/clean_current_items_Spirit_static_actors_and_related_terms.json')
ITEMS={174:('古びた羊皮紙','Old Parchment'),181:('紅色の顔料','Red Dye')}
if __name__=='__main__':
    assert not ROOT.exists();source,voice,context,catalog,proof=map(read,[SOURCE,VOICE,CONTEXT,CATALOG,PROOF]);assert context['all63_complete_clean_source_objects_read_before_older_English_comparison'];versions=[]
    for version,path in [('clean','work/clean.nds'),('current',source['current_ROM'])]:
        arm=NdsImage.open(path).read_file('/__arm9__.bin');code=MainCodeFile(arm,0x02000000);views=[(s.ramAddress,bytes(s.data),'original-main-code-section') for s in code.sections]
        if version=='current':assert len(code.sections[3].data)-48==123040;views.append((POOL,bytes(code.sections[3].data[:-48]),'registered123040-byte-runtime-pool-copy'))
        records=[]
        for ident,(jp,en) in ITEMS.items():
            r=next(r for r in catalog['records'] if r['id']==f'DK4_ITEM_POINTER_{ident:03d}');assert r['english']==en
            ptr=struct.unpack_from('<I',arm,r['offset'])[0];hits=[v for v in views if v[0]<=ptr<v[0]+len(v[1])];assert len(hits)==1
            base,data,owner=hits[0];tail=data[ptr-base:];end=tail.index(b'\0');value=tail[:end].decode('cp932');assert value==(jp if version=='clean' else en)
            records.append(dict(item_ID=ident,catalog_record_ID=r['id'],pointer_file_offset=r['offset'],pointer=ptr,storage_owner=owner,complete_C_string_hex=tail[:end+1].hex(),text=value))
        versions.append(dict(version=version,ROM=path,ROM_sha256=sha(Path(path).read_bytes()),ARM9_sha256=sha(arm),items=records))
    names={r['actor_ID']:r['current_catalog_name'] for r in voice['fresh_five_actor_names']['rows']};assert names[0]=='Rafael Castor' and names[5]=='Claudio Manaus' and names[2]=='Lil Argot'
    byid={r['id']:r for r in source['records']};ratioids=['DK4_MES_B133_R0129','DK4_MES_B133_R0132','DK4_MES_B133_R0136','DK4_MES_B133_R0140'];ratios=[{k:byid[i][k] for k in ['id','source_reference','source_hex','source_Japanese']} for i in ratioids]
    assert '２％' in byid[ratioids[2]]['source_Japanese'] and '１％' in byid[ratioids[2]]['source_Japanese']
    ROOT.mkdir(parents=True);save(ROOT/'clean_current_items_names_and_share_ratio_reconciliation.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),complete_clean_context=str(CONTEXT),complete_clean_context_sha256=sha(CONTEXT.read_bytes()),voice_proof=str(VOICE),voice_proof_sha256=sha(VOICE.read_bytes()),registered_item_catalog=str(CATALOG),registered_item_catalog_sha256=sha(CATALOG.read_bytes()),two_complete_item_pointer_versions=versions,approved_item_names={str(k):v[1] for k,v in ITEMS.items()},literal_red_pigment_localizes_as_registered_Red_Dye=True,exact_current_actor_names=names,approved_dialogue_names=dict(Rafael='Rafael',Rafael_full='Rafael Castor',Claudio='Claudio',Camille='Camille',Fernando='Fernando',Lil='Lil'),familiar_Rafi_and_Clau_calls_use_approved_Rafael_and_Claudio_with_familiar_tone=True,no_kinship_rank_new_nickname_or_portrait_claim=True,approved_places_and_terms=dict(Nantes='Nantes',Lisbon='Lisbon',North_Sea='North Sea',Mediterranean='Mediterranean',Castor_Company='Castor Company',market_share='market share',Proof='Proof of Supremacy;source-short Proof stays Proof where context allows'),exact_two_Nantes_for_one_Lisbon_source_references=ratios,Lil_initial_one_for_one_offer_distinct_from_Claudio_two_for_one_counteroffer=True,acceptance_FE_exchange_notice_not_earned_progress=True,prior_Proof_terminology_evidence=str(PROOF),prior_Proof_terminology_evidence_sha256=sha(PROOF.read_bytes()),existing_Proof_terminology_variants=proof['existing_completed_Proof_terminology_variants'],whole_goal_Proof_consistency_reconciliation_remains_open_separate_from_technical_reaudit=True,no_old_completed_record_reopened_recounted_or_silently_renamed=True,no_ROM_registry_or_editorial_credit_change=True,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Old Parchment174/Red Dye181 complete clean/current pointers pass;Rafael/Claudio approved names andtwo-Nantes-for-one-Lisbon direction bound. Whole-goal Proof terminology lead staysopen.')
