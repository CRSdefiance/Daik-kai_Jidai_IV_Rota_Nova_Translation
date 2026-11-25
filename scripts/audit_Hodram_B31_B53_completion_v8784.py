"""Independently audit exactly five B52 credits, direct ROM references and preserved full scope."""
import gzip,json
from collections import Counter
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import complete_Hodram_B31_B53_v8783 as completion
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B31_B53_completion_audit_v8784')

if __name__=='__main__':
    assert not ROOT.exists();plan=read(completion.ROOT/'staged_completion.json')
    old=json.loads(gzip.decompress((completion.ROOT/'ledger.before.json.gz').read_bytes()))
    new=read(plan['files'][0]['planned']);final=read(completion.FINAL);doc=read(completion.DOC)
    assert completion.restore(new)==old and [new[k]-old[k] for k in completion.COUNTERS]==[3,3,3,3,0]
    oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
    newkeys={historical_key(r) for f in new['completed_editorial_families'] for r in f['records']}
    rows,approved=final['records'],doc['records']
    assert len(oldkeys)==7234 and len(newkeys)==7237 and newkeys-oldkeys=={historical_key(r) for r in rows}
    assert len(rows)==3 and Counter(r['decision'] for r in rows)==dict(revision=3)
    assert [r['id'] for r in rows]==[r['id'] for r in approved]
    current=NdsImage.open(final['candidate']);clean=NdsImage.open('work/clean.nds');predecessor=NdsImage.open(doc['current_ROM'])
    banks=[IlnkContainer.parse(i.read_file('/data/SC1.DK4')).blocks for i in [clean,predecessor,current]]
    for row,before in zip(rows,approved,strict=True):
        blocks=[bank[row["block"]] for bank in banks]
        assert row['pre_integration_review_record_preserved']==before
        assert all(row[k]==before[k] for k in ['id','english','source_reference','source_hex','source_meaning','context','localization_note','decision','retention_reason','review','final_reference','final_hex'])
        assert all(row[k] is False for k in completion.PENDING_FLAGS if k in row)
        assert row['current_reference']==before['final_reference'] and row['predecessor_reference']==before['current_reference']
        for bank,ref,raw in [(blocks[0],row['source_reference'],bytes.fromhex(row['source_hex'])),
                             (blocks[1],row['predecessor_reference'],bytes.fromhex(row['predecessor_hex'])),
                             (blocks[2],row['current_reference'],bytes.fromhex(row['current_hex']))]:
            at=ref['offset'];assert bank[at:at+len(raw)+1]==raw+b'\0' and bank[:at].count(b'\0')==ref['record_index']
        assert row['integrated_reference']['ROM_sha256']==sha(Path(final['candidate']).read_bytes())
        assert row['all_current_editorial_formatting_policy_atomic_registered_requirements_completed']
        assert not row['individually_activated_in_current_build'] and row['actual_initialized_source_andEnglish_selected_paths_observed']==(row['id']!='DK4_MES_B31_R0013')
        assert row['offline_only_variant_with_complete_native_andrepresentative_sameconsumer_evidence']==(row['id']=='DK4_MES_B31_R0013')
        assert row['opaque_effect_gameplay_semantics_outer_eligibility_andfuture_causality_remain_unproven']
    scope=read(completion.RELEASE)['actual_scope_limits']
    assert scope['actual_unique_speech_IDs']==['DK4_MES_B31_R0018','DK4_MES_B53_R0007'] and scope['unvisited_conditional_text_IDs']==['DK4_MES_B31_R0013']
    assert (scope['complete_page_occurrences'],scope['complete_body_name_holds'],scope['total_actual_frames'])==(4,76,24004)
    assert [g['later_RGB_difference_count'] for g in scope['measured_comparisons']]==[0,0]
    assert all(g['whole_actors_equal'] and all(g['five_native_component_equality'].values()) for g in scope['measured_comparisons'])
    pending=new[completion.NEXT_KEY]
    assert pending['blocks']==[54,55,56,57,58,59,60] and pending['physical_speeches']==82 and pending['typed_choice_labels']==0 and pending['completion_credit_added']==0 and pending['current_English_forall_seven_blocks_still_unconsulted']
    pendingkeys={historical_key(r) for group in pending['source_groups'] for r in group['records']}
    assert len(pendingkeys)==82 and not pendingkeys&newkeys
    prior=read(completion.PRIOR);oldscope=read(old[prior['unfinished_scope']]['path']);newscope=read(new[completion.SCOPE]['path'])
    assert all(newscope[k]==v for k,v in oldscope.items()) and set(newscope)-set(oldscope)=={completion.KEY,completion.NEXT_KEY,'latest_next_focus_v8783'}
    assert new['current_integrated_candidate']['sha256']==final['candidate_sha256'] and new['goal_status']=='active' and not new['full_goal_complete']
    assert new['completed_editorial_record_counts_by_file']['/data/SC1.DK4']==157
    assert all(new['completed_editorial_record_counts_by_file'][p]==old['completed_editorial_record_counts_by_file'][p] for p in old['completed_editorial_record_counts_by_file'] if p!='/data/SC1.DK4')
    for index,row in enumerate(plan['files']):
        assert sha(Path(row['target']).read_bytes())==row['before_sha256'] and sha(Path(row['planned']).read_bytes())==row['planned_sha256']
        if index:
            original=gzip.decompress((completion.ROOT/f'{index:02d}.before.gz').read_bytes())
            assert Path(row['planned']).read_bytes().endswith(original)
    ROOT.mkdir(parents=True)
    save(ROOT/'independent_staged_completion_audit.json',dict(exact_full_prior_ledger_inverse=True,three_disjoint_new_keys_only=True,counter_deltas=[3,3,3,3,0],
         three_speeches_two_blocks_nochoices_exact_source_predecessor_final_ROM_references=True,
         canonical_source_IDs13_18_7_andall_final_recordindices_preserved=True,
         all_approved_words_reasons_glosses_andindividual_gates_exact=True,
         two_observed_utterances_andshort_B31_offline_scope_all_bounded_comparison_limits_preserved=True,
         no_natural_activation_fullcatalogue_orunvisited_variant_scope_upgrade=True,
         next82_B54_B60_clean_glosses_disjoint_uncredited_older_English_unread=True,
         full_goal_active_every_prior_family_lead_counter_candidate_anddocument_preserved=True,
         no_shared_ledger_ROM_orregistry_mutation=True,full_goal_complete=False,
         evidence={str(p):sha(Path(p).read_bytes()) for p in [__file__,completion.ROOT/'staged_completion.json',completion.FINAL,completion.DOC,completion.RELEASE]}))
    print('Independent B31/B53 completion audit:exactly3new keys/allrevisions;all direct source/predecessor/final ROMrefs andfull priorinverse. Shortvariant offline,next82meanings uncredited,all oldscopevalues exact. Full scope active.')
