"""Independently audit exactly82 B54-B60 credits, direct ROM references and preserved full scope."""
import gzip,json
from collections import Counter
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import complete_Hodram_B54_B60_v8870b as completion
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_completion_audit_v8871')

if __name__=='__main__':
    assert not ROOT.exists();plan=read(completion.ROOT/'staged_completion.json')
    old=json.loads(gzip.decompress((completion.ROOT/'ledger.before.json.gz').read_bytes()))
    new=read(plan['files'][0]['planned']);final=read(completion.FINAL);doc=read(completion.DOC)
    assert completion.restore(new)==old and [new[k]-old[k] for k in completion.COUNTERS]==[82,82,82,46,36]
    oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
    newkeys={historical_key(r) for f in new['completed_editorial_families'] for r in f['records']}
    rows,approved=final['records'],doc['records']
    assert len(oldkeys)==7237 and len(newkeys)==7319 and newkeys-oldkeys=={historical_key(r) for r in rows}
    assert len(rows)==82 and Counter(r['decision'] for r in rows)==dict(revision=46,retention=36)
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
        assert not row['individually_activated_in_current_build'] and row['actual_initialized_source_andEnglish_selected_paths_observed']==(row['id'] in final['actual_unique_speech_IDs'])
        assert row['offline_only_speech_with_complete_native_andrepresentative_sameconsumer_evidence']==(row['id'] in final['offline_only_text_IDs'])
        assert row['opaque_effect_gameplay_semantics_outer_eligibility_andfuture_causality_remain_unproven']
    scope=read(completion.RELEASE)['actual_scope_limits']
    assert len(scope['actual_unique_speech_IDs'])==63 and len(scope['offline_only_text_IDs'])==19 and len(scope['unvisited_conditional_text_IDs'])==18
    assert (scope['complete_page_occurrences'],scope['complete_body_name_holds'],scope['total_actual_frames'])==(150,676,130014)
    assert [g['later_RGB_difference_count'] for g in scope['measured_comparisons']]==[3,0,0,3,65,61,11]
    assert not scope['measured_comparisons'][5]['whole_actors_equal'] and scope['measured_comparisons'][6]['whole_actors_equal'] and all(scope['measured_comparisons'][6]['five_native_component_equality'].values())
    pending=new[completion.NEXT_KEY]
    assert pending['blocks']==list(range(61,71)) and pending['physical_speeches']==224 and pending['typed_choice_labels']==0 and pending['completion_credit_added']==0 and pending['current_English_forall_ten_blocks_still_unconsulted']
    assert pending['first_meanings_completed']==44 and pending['other_first_meanings_pending']==180 and not pending['all224_glossed']
    pendingkeys={historical_key(r) for group in pending['source_groups'] for r in group['records']}
    assert len(pendingkeys)==224 and not pendingkeys&newkeys
    source_rows={r['id']:r for g in pending['source_groups'] for r in g['records']}
    meaning_rows=[r for g in pending['first_meaning_groups'] for r in g['records']]
    assert len(meaning_rows)==44 and len({r['id'] for r in meaning_rows})==44
    for r in meaning_rows:
        assert all(r[k]==source_rows[r['id']][k] for k in ['source_hex','source_reference','source_selector','source_Japanese'])
        assert r['source_meaning_gloss'] and r['whole_exchange_fidelity_note'] and r['current_English_dialogue_still_unconsulted']
    prior=read(completion.PRIOR);oldscope=read(old['unfinished_editorial_scope_v8874']['path']);newscope=read(new[completion.SCOPE]['path'])
    assert all(newscope[k]==v for k,v in oldscope.items()) and set(newscope)-set(oldscope)=={completion.KEY,completion.NEXT_KEY,'latest_next_focus_v8870'}
    assert new['current_integrated_candidate']['sha256']==final['candidate_sha256'] and new['goal_status']=='active' and not new['full_goal_complete']
    assert new['completed_editorial_record_counts_by_file']['/data/SC1.DK4']==239
    assert all(new['completed_editorial_record_counts_by_file'][p]==old['completed_editorial_record_counts_by_file'][p] for p in old['completed_editorial_record_counts_by_file'] if p!='/data/SC1.DK4')
    for index,row in enumerate(plan['files']):
        assert sha(Path(row['target']).read_bytes())==row['before_sha256'] and sha(Path(row['planned']).read_bytes())==row['planned_sha256']
        if index:
            original=gzip.decompress((completion.ROOT/f'{index:02d}.before.gz').read_bytes())
            assert Path(row['planned']).read_bytes().endswith(original)
    ROOT.mkdir(parents=True)
    save(ROOT/'independent_staged_completion_audit.json',dict(exact_full_prior_ledger_inverse=True,eighty_two_disjoint_new_keys_only=True,counter_deltas=[82,82,82,46,36],
         all82_speeches_seven_blocks_nochoices_exact_source_predecessor_final_ROM_references=True,
         all82_canonical_source_IDs_andall_final_recordindices_preserved=True,
         all_approved_words_reasons_glosses_andindividual_gates_exact=True,
         observed63_utterances19_offline_all_main_focused_actor_RNG_RGB_andbounded_comparison_limits_preserved=True,
         no_natural_activation_fullcatalogue_orunvisited_variant_scope_upgrade=True,
         next224_B61_B70_candidates_first44_meanings180_notglossed_disjoint_uncredited_older_English_unread=True,
         full_goal_active_every_prior_family_lead_counter_candidate_anddocument_preserved=True,
         no_shared_ledger_ROM_orregistry_mutation=True,full_goal_complete=False,
         evidence={str(p):sha(Path(p).read_bytes()) for p in [__file__,completion.ROOT/'staged_completion.json',completion.FINAL,completion.DOC,completion.RELEASE]}))
    print('Independent B54-B60 completion audit:82new keys/46revisions36retentions;all direct source/predecessor/final ROMrefs andfull priorinverse.63actual19offline;next224 candidates/first44 meanings uncredited;all oldscopevalues exact.Full scope active.')
