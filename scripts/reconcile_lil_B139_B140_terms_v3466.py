"""Bind three items,approved names,polder/Proof terms,entries and potential text copies."""
import struct,unicodedata
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B139_B140_terms_v3466')
SOURCE=Path('work/analysis/lil_remaining_B139_B140_source_v3456/next67_B139_B140_clean_current_context.json')
CONTEXT=Path('work/analysis/lil_B139_B140_clean_context_v3465/all67_complete_clean_context_and_fresh_glosses.json')
VOICE=Path('work/analysis/lil_B139_B140_voices_v3460/current_seven_static_names_voices_and207_catalog_rebind.json')
CONTROL=Path('work/analysis/lil_B139_B140_controls_v3464/all67_dispatches12_predicates1_query_and_C200_contract.json')
CATALOG=Path('translations/all_item_names_arm9_v1.json')
ITEMS={158:('ソロンの葉地図','Solon Leaf Map'),177:('枯れないハスの葉','Evergreen Lotus Leaf'),184:('クシャナ朝の大皿','Kushan Platter')}
def norm(value):return ''.join(unicodedata.normalize('NFKC',value).split())
if __name__=='__main__':
    assert not ROOT.exists();source,context,voice,control,catalog=map(read,[SOURCE,CONTEXT,VOICE,CONTROL,CATALOG]);assert context['all67_complete_clean_source_objects_read_before_older_English_comparison'] and context['all67_fresh_source_glosses_precede_localized_English']
    versions=[];current=NdsImage.open(source['current_ROM']);clean=NdsImage.open('work/clean.nds');blocks=IlnkContainer.parse(current.read_file('/data/SC2.DK4')).blocks
    for version,image,path in [('clean',clean,'work/clean.nds'),('current',current,source['current_ROM'])]:
        arm=image.read_file('/__arm9__.bin');code=MainCodeFile(arm,0x02000000);views=[(s.ramAddress,bytes(s.data),'original-main-code-section') for s in code.sections]
        if version=='current':assert len(code.sections[3].data)-48==123040;views.append((POOL,bytes(code.sections[3].data[:-48]),'registered123040-byte-runtime-pool-copy'))
        items=[]
        for ident,(jp,en) in ITEMS.items():
            row=next(r for r in catalog['records'] if r['id']==f'DK4_ITEM_POINTER_{ident:03d}');assert row['english']==en;ptr=struct.unpack_from('<I',arm,row['offset'])[0];hits=[v for v in views if v[0]<=ptr<v[0]+len(v[1])];assert len(hits)==1
            base,data,owner=hits[0];tail=data[ptr-base:];end=tail.index(b'\0');name=tail[:end].decode('cp932');assert name==(jp if version=='clean' else en)
            items.append(dict(item_ID=ident,catalog_record_ID=row['id'],pointer_file_offset=row['offset'],pointer=ptr,storage_owner=owner,complete_C_string_hex=tail[:end+1].hex(),text=name))
        versions.append(dict(version=version,ROM=path,ROM_sha256=sha(Path(path).read_bytes()),ARM9_sha256=sha(arm),items=items))
    names={r['actor_ID']:r['current_catalog_name'] for r in voice['fresh_seven_actor_names']['rows']};assert names[4]=='Janus Pasar' and names[171]=='Research Student' and set(names)=={2,4,9,16,20,21,171}
    ledger=read('translations/editorial_review_current_v1.json');completed=[(f,r) for f in ledger['completed_editorial_families'] for r in f['records']];polder=[];copies=[]
    for family,r in completed:
        jp=r.get('source_Japanese','')
        if 'ポルダー' in jp:
            assert r['file_path']=='/data/SC2.DK4';ref=r['integrated_reference'];value=bytes.fromhex(r['integrated_hex']);assert blocks[r['block']][ref['offset']:ref['offset']+ref['bytes']]==value and 'polder' in r['english'].casefold()
            polder.append(dict(family=family['id'],final_review=family['final_review'],final_review_sha256=sha(Path(family['final_review']).read_bytes()),id=r['id'],source_Japanese=jp,source_reference=r['source_reference'],integrated_reference=ref,integrated_hex=r['integrated_hex'],english=r['english']))
    assert len(polder)==12
    for r in source['records']:
        matches=[]
        for family,prior in completed:
            if prior['file_path']!='/data/SC2.DK4' or len(norm(r['source_Japanese']))<12:continue
            raw=bytes.fromhex(prior.get('source_hex',''))
            if raw and raw[0]==r['source_selector'] and norm(prior.get('source_Japanese',''))==norm(r['source_Japanese']):matches.append(dict(family=family['id'],id=prior['id'],block=prior['block'],source_reference=prior['source_reference'],source_hex=prior['source_hex'],final_review=family['final_review'],final_review_sha256=sha(Path(family['final_review']).read_bytes())))
        if matches:copies.append(dict(id=r['id'],block=r['block'],source_reference=r['source_reference'],source_hex=r['source_hex'],normalized_Japanese=norm(r['source_Japanese']),potential_same_text_same_static_selector=matches,not_assumed_same_complete_exchange_or_new_credit=True))
    ev=current.read_file('/data/EV2.DK4');assert ev==clean.read_file('/data/EV2.DK4');history=read(source['prior_state_inventory']);entries=[]
    for b in source['blocks']:
        record=b['original_event_source'];assert record==history['all336_original_events'][b['block']] and record['SC2_action_block']==b['block'] and record['action_index']==b['block']+1
        at=96+record['body_offset'];value=bytes.fromhex(record['source_hex']);assert ev[at:at+len(value)]==value;entries.append(dict(block=b['block'],file_offset=at,record=record))
    assert entries[1]['record']['must_be_completed']==[37] and control['original_event_queries'][0]['event']==129
    ROOT.mkdir(parents=True);terms=ROOT/'clean_current_items_polder_names_entries_and_copy_census.json'
    save(terms,dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),complete_clean_context=str(CONTEXT),complete_clean_context_sha256=sha(CONTEXT.read_bytes()),voice_proof=str(VOICE),voice_proof_sha256=sha(VOICE.read_bytes()),control_proof=str(CONTROL),control_proof_sha256=sha(CONTROL.read_bytes()),registered_item_catalog=str(CATALOG),registered_item_catalog_sha256=sha(CATALOG.read_bytes()),complete_item_pointer_versions=versions,approved_item_names={str(k):v[1] for k,v in ITEMS.items()},exact_current_actor_names=names,approved_dialogue_names=dict(Lil='Lil',Janus='Janus',Camille='Camille',Gerhard='Gerhard',Fernando='Fernando',Ian='Ian',student='Research Student;unnamed,no invented degree or nationality'),approved_polder_term='polder',polder_cultural_context='Coastal dikes,enclosing sea andpumping out seawater tocreate usable land;the invention claim remains the student\'s speech,not real-world historical narration.',completed_polder_term_references=polder,potential_nontrivial_source_text_copy_records=copies,physical_target_count=67,copy_matches_are_context_leads_not_duplicate_credit_to_old_records=True,two_separate_physical_entry_blocks_require_their_complete_contexts=True,original_EV2_entries=entries,current_EV2_sha256=sha(ev),original_entry_bindings_reused_from_exact_EV2_and_historical336_event_inventory=True,event140_requires_source37_but_current_eligibility_not_claimed=True,source_query129_preserved=True,source_FI_occurrences=7,current_bound_FI_expansion='Lil',FI_runtime_tokens_preserved_not_hardcoded=True,source_ellipsis_records=[[140,71],[140,130],[140,274]],leaf177_platter184_map158_operands_preserved=True,map_dialogue_Indian_Ocean_reference_not_forced_to_Solon_catalogue_name=True,Proof='Proof of Supremacy;source-short Proof stays Proof where clear',whole_goal_Proof_consistency_lead=ledger['Proof_terminology_consistency_lead_v3286'],whole_goal_Proof_consistency_reconciliation_remains_open=True,no_completed_record_reopened_renamed_or_recounted=True,no_ROM_registry_or_editorial_credit_change=True,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    a=Path('scripts/compare_lil_B138_effective_v3431.py');b=Path('scripts/compare_lil_B139_B140_effective_v3467.py');assert not b.exists();t=a.read_text(encoding='utf-8')
    changes=[('lil_B138_comparison_v3431','lil_B139_B140_comparison_v3467'),('work/analysis/lil_remaining_B138_B140_source_v3422/next44_B138_clean_current_context.json',SOURCE.as_posix()),('work/analysis/lil_B138_controls_v3426e/all44_source_current_dispatches10_predicates_and1_query.json',CONTROL.as_posix()),('work/analysis/lil_B138_clean_context_v3428/all44_complete_clean_context_and_fresh_glosses.json',CONTEXT.as_posix()),('work/analysis/lil_B138_terms_v3429/clean_current_names_leaf_price_macro_and_entry_reconciliation.json',terms.as_posix()),('all44','all67'),('fresh44','fresh67'),('len(rows)==44','len(rows)==67'),('source_current_comparisons=44','source_current_comparisons=67'),('Seven static names,FO1,ten predicates,one event137 query,raw predicate result2,price100,shared leaf item177 and original B138 entry bound.','Seven static names including Janus4 andStudent171,FI7,twelve predicates,query129,C200 source-owned UI request,three items,polder terms andseparate B139/B140 entries bound. C200 resource bodies/actual transition remain unexecuted.')]
    for x,y in changes:assert x in t,x;t=t.replace(x,y)
    compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');save(ROOT/'comparison_tool_provenance.json',dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(items={k:v[1] for k,v in ITEMS.items()},polder_completed_references=len(polder),potential_copy_records=len(copies),voices=7,FI=7,query=129,current_entry_eligibility_not_claimed=True,credit=0))
