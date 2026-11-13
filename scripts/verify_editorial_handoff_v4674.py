"""Independently audit uncredited B178 progress and preservation of verified B177."""
from collections import Counter
import gzip
import json
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.checkpoint_lil_B178_draft_v4673 import ROOT as CHECKPOINT,DOC,PRIOR
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v4674')


def same_except(a,b,allowed):
    assert {k:v for k,v in a.items() if k not in allowed}=={k:v for k,v in b.items() if k not in allowed}


if __name__=='__main__':
    assert not ROOT.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    beforebytes=gzip.decompress((CHECKPOINT/'ledger.before.json.gz').read_bytes());before=json.loads(beforebytes)
    assert sha(beforebytes)==read(PRIOR)['ledger_sha256']
    same_except(before,ledger,{'latest_checkpoint','lil_B178_uncredited_draft_v4673','coverage_units'})
    for a,b in zip(before['coverage_units'],ledger['coverage_units'],strict=True):
        if a['id']=='all-route-scenes':same_except(a,b,{'next'})
        else:assert a==b
    assert lp.read_bytes()==encode_ledger(ledger) and lp.stat().st_size<100*1024*1024
    assert tuple(ledger[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass',
        'records_revised_and_integrated','retained_wordings_editorially_completed'])==(5885,5888,3738,2147)
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert tuple(fresh[k] for k in ['fresh_pass_records_explicitly_reread','fresh_pass_records_integrated',
        'fresh_pass_records_pending_native_actual_release'])==(5885,5885,0)
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    receipt=read(CHECKPOINT/'checkpoint_receipt.json')
    assert receipt['ledger_sha256']==sha(lp.read_bytes()) and receipt['uncredited_B178_draft']==13
    for p,h in {**receipt['evidence'],**receipt['stable_release_files'],**receipt['updated_files']}.items():assert sha(Path(p).read_bytes())==h,p
    draft=ledger['lil_B178_uncredited_draft_v4673'];doc=read(DOC);rows=doc['records']
    assert draft['manuscript_sha256']==sha(DOC.read_bytes()) and len(rows)==13
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':2,'retain-wording':11}
    assert doc['formatting_review_pending'] and doc['source_prose_or_completion_credit_added']==0
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in rows)
    clean=NdsImage.open('work/clean.nds');current=NdsImage.open(doc['current_ROM'])
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==ledger['current_integrated_candidate']['sha256']
    source=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[178]
    predecessor=IlnkContainer.parse(current.read_file('/data/SC2.DK4')).blocks[178]
    for r in rows:
        for data,ref,value in [(source,r['source_reference'],r['source_hex']),(predecessor,r['current_reference'],r['current_hex'])]:
            at=ref['offset'];raw=bytes.fromhex(value)
            assert data[at:at+len(raw)]==raw and data[at+len(raw)]==0 and data[at-5:at+1].hex()==r['source_complete_preamble_hex']
        assert r['source_meaning']==r['fresh_source_gloss'] and r['source_selector']==int(r['english'][9:11],16)
        body=r['english'].split('}',1)[1]
        if r['editorial_decision']=='retain-wording':assert body==r['effective_predecessor_paragraph'] and r['fresh_retained_wording_justification']
        elif r['source_record_index']==32:assert body=="I'll show you how."
        else:assert r['source_record_index']==47 and body=='Wheat first, of course!'
    assert Counter(r['kind'] for r in rows)=={'progressive':12,'system-FE':1}
    for key in ['source_context','control_contract','whole_exchange_context_notes','actor_voice_contract','branch_proof','source_entry_proof',
        'source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof','effective_current_comparison']:
        assert sha(Path(doc[key]).read_bytes())==doc[key+'_sha256']
    names,terms,controls,entry,dispatch,voices=[read(doc[k]) for k in ['source_nameplate_consumer_proof','actor_terminology_reconciliation',
        'source_effect_and_predicate_contract','source_entry_proof','control_contract','actor_voice_contract']]
    assert names['approved_prose_names']=={'166':'Lady','167':'Lady','168':'Lady'} and len(names['native_six_consumer_cases']['rows'])==6
    assert all(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['all_actor_models_and_unowned4MiB_exact']
        for r in names['native_six_consumer_cases']['rows'])
    assert len(dispatch['speech_dispatch_cases'])==26 and len(voices['fresh3_actor_names']['rows'])==3
    assert [(r['event_ID'],r['script_block'],r['action_index']) for r in entry['selected_B178_source_events']]==[(178,178,179)]
    assert [(r['offset'],r['source_current_hex']) for r in controls['all3_source_current_nonrelative_nonspeech_leaves']]==[
        (8,'00a0ffff010002a1'),(488,'00c2'),(490,'00000000')]
    assert terms['husband_explicit_for167_only_no_named_husband_or_other_marriages_invented']
    assert terms['exact167_teaching_offer_then_ingredient_question_and168_wheat_suggestion_not_reassigned']
    assert len(terms['exact_city_source_current_inline_span_and_pointer_bindings'])==4
    assert [(r['file_offset'],r['text']) for r in terms['exact_wheat_source_current_pointer_selected_name_and_metadata_bindings']]==[(0x15B938,'小麦'),(0x15BC56,'Wheat')]
    promoted=read('translations/promoted_build.json')
    assert promoted['profile']=='all-routes-unified-v4595' and ledger['current_integrated_candidate']['profile']=='all-routes-unified-v4655'
    assert sha(Path(promoted['rom']).read_bytes())==promoted['rom_sha256']
    release=read('work/analysis/lil_B177_release_v4656/registered_release_verification.json')
    assert Path(release['candidate']).read_bytes()==Path('out/lil_B177_reference_v4630_RESEARCH_ONLY.nds').read_bytes()==Path(release['exact_patch_reconstruction']).read_bytes()
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert read('work/analysis/lil_B177_build_v4655/build_terminal.json')['returncode']==0
    for case in ['newgame','town']:assert read('work/analysis/lil_B177_runs_v4657/'+case+'_terminal.json')['terminal']
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        assert Path('docs',name).read_text(encoding='utf-8').endswith((CHECKPOINT/(name+'.before')).read_text(encoding='utf-8').split('\n',1)[1])
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4673')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4673',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5885,integrated=5885,pending=0,
        source_prose=5888,revised=3738,retained=2147,uncredited_B178_draft_objects=13,proposed_revisions=2,justified_retentions=11,
        all_prior_root_nested_ledger_history_counts_and_full_objective_preserved=True,
        all13_clean_source_current_draft_and11_retention_references_exact=True,three_Lady_roles26_dispatches6_readonly_names3_control_leaves_and_terms_bound=True,
        formatting_native_actual_reference_and_release_still_pending=True,main_V4595_preserved=True,latest_experimental_V4655_exact_patch_verified=True,
        all_jobs_terminal=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('V4673 independently verified:5885 completed;13 uncredited B178 decisions (2 revisions/11 retentions),full history/main V4595/latest V4655 preserved.')
