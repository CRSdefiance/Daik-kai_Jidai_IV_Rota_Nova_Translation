"""Independently audit staged B51 decisions, scope, statuses and exact five-record credit."""
import gzip,json
from pathlib import Path
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import complete_Hodram_B51_v8623 as completion
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B51_completion_audit_v8625')
if __name__=='__main__':
    assert not ROOT.exists();plan=read(completion.ROOT/'staged_completion.json')
    old=json.loads(gzip.decompress((completion.ROOT/'ledger.before.json.gz').read_bytes()))
    new=read(plan['files'][0]['planned']);final=read(completion.FINAL);doc=read(completion.DOC)
    assert completion.restore(new)==old
    assert [new[k]-old[k] for k in completion.COUNTERS]==[5,5,5,4,1]
    prior_keys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
    new_keys={historical_key(r) for f in new['completed_editorial_families'] for r in f['records']}
    rows=final['records'];assert len(rows)==5 and new_keys-prior_keys=={historical_key(r) for r in rows}
    assert len(prior_keys)==7224 and len(new_keys)==7229
    assert Counter(r['decision'] for r in rows)==dict(revision=4,retention=1)
    assert [r['id'] for r in rows]==[r['id'] for r in doc['records']]
    reference=NdsImage.open(final['candidate']);block=IlnkContainer.parse(reference.read_file('/data/SC1.DK4')).blocks[51]
    pending=['source_meaning_only_not_localized_orformatting_approval','native_speakers_queries_branch_paths_names_current_editorial_actual_andregistered_integration_pending','current_contextual_prose_formatting_actual_andrelease_pending','formatting_native_stored_actual_policy_atomic_andregistered_integration_pending','all_stored_controls_actual_branch_context_headers_policy_andregistered_release_pending','formal_frozen_policy_independent_production_atomic_andregistered_integration_pending','formatting_registered_release_pending']
    for row,approved in zip(rows,doc['records'],strict=True):
        assert row['pre_integration_review_record_preserved']==approved
        assert all(row[k]==approved[k] for k in ['id','english','source_reference','source_hex','source_meaning','context','localization_note','decision','retention_reason','review','final_reference','final_hex','actual_display_evidence'])
        assert all(row[k] is False for k in pending)
        assert row['current_reference']==approved['final_reference'] and row['predecessor_reference']==approved['current_reference']
        raw=bytes.fromhex(row['current_hex']);at=row['current_reference']['offset']
        assert block[at:at+len(raw)+1]==raw+b'\0' and row['integrated_reference']['ROM_sha256']==sha(Path(final['candidate']).read_bytes())
    conditional=next(r for r in rows if r['id']=='DK4_MES_B51_R0032')
    assert conditional['actual_B51_conditional_not_visited'] and not conditional['actual_B51_source_andEnglish_body_header_covered'] and conditional['actual_display_evidence']==[]
    assert all(r['actual_B51_source_andEnglish_body_header_covered'] for r in rows if r is not conditional)
    actual_scope=read(completion.RELEASE)['actual_scope_limits']
    assert actual_scope['actual_unique_speech_IDs']==['DK4_MES_B51_R0006','DK4_MES_B51_R0010','DK4_MES_B51_R0014','DK4_MES_B51_R0039']
    assert actual_scope['complete_page_occurrences']==8 and actual_scope['complete_body_name_holds']==56 and actual_scope['unvisited_conditional_text_IDs']==['DK4_MES_B51_R0032']
    next_batch=new[completion.NEXT_KEY]
    assert next_batch['blocks']==[52] and next_batch['physical_speeches']==3 and next_batch['typed_choice_labels']==2 and next_batch['completion_credit_added']==0 and next_batch['current_English_dialogue_bodies_andchoices_still_unconsulted']
    assert new['current_integrated_candidate']['sha256']==final['candidate_sha256'] and new['goal_status']=='active' and not new['full_goal_complete']
    for row in plan['files']:
        assert sha(Path(row['target']).read_bytes())==row['before_sha256'] and sha(Path(row['planned']).read_bytes())==row['planned_sha256']
    ROOT.mkdir(parents=True);save(ROOT/'independent_staged_completion_audit.json',dict(exact_full_prior_ledger_inverse=True,five_disjoint_new_keys_only=True,counter_deltas=[5,5,5,4,1],all_five_source_approved_prose_refs_retention_reasons_andgates_exact=True,complete_registered_target_bytes_bound=True,current_pending_flags_cleared_original_flags_preserved=True,four_observed_speeches_Charles_offline_unvisited_preserved=True,B52_three_speeches_two_choices_still_uncredited_currentEnglish_unread=True,full_goal_active_all_prior_families_andunfinished_scope_preserved=True,no_shared_ledger_orROM_mutation=True,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),completion.ROOT/'staged_completion.json',completion.FINAL,completion.DOC,completion.RELEASE]}))
    print('Independent staged B51 audit passes: exactly five new keys/4 revisions/1 retention; exact prior inverse; actual four speeches versus offline Charles; next B52 uncredited.')
