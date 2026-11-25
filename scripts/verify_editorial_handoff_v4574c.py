"""Audit every B176 pending addition and preservation invariant before metadata writes."""
import argparse
import os
from collections import Counter
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.checkpoint_lil_B176_v4573b import ROOT as CHECKPOINT,DOC,FAMILY
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v4574c')

def unchanged_outside(before,after,allowed):
    assert {k:v for k,v in before.items() if k not in allowed}=={k:v for k,v in after.items() if k not in allowed}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    assert not ROOT.exists()
    workspace=Path.cwd().resolve();plan=read(CHECKPOINT/'mutation_plan.json');assert len(plan)==6
    for row in plan:
        target,staged=Path(row['target']),Path(row['planned'])
        assert target.is_relative_to(workspace) and staged.is_relative_to(CHECKPOINT.resolve())
        assert sha(staged.read_bytes())==row['planned_sha256']
        if args.apply:assert sha(target.read_bytes())==row['before_sha256']
    lp=Path('translations/editorial_review_current_v1.json')
    ledger_plan=next(r for r in plan if Path(r['target'])==lp.resolve())
    ledger=read(ledger_plan['planned']);before=read(CHECKPOINT/(lp.name+'.before'))
    assert Path(ledger_plan['planned']).read_bytes()==encode_ledger(ledger)
    assert Path(ledger_plan['planned']).stat().st_size<100*1024*1024
    allowed={'records_with_source_and_prose_pass','records_with_source_prose_drafts','source_prose_reviewed_counts_by_file',
        'reviewed_but_incomplete_route_record_IDs','active_source_prose_drafts','contextual_story_natural_dialogue_pass_v1871',
        'coverage_units','formatting_watchlist','unfinished_editorial_scope_v4573','lil_B176_scope_reconciliation_v4573','latest_checkpoint'}
    unchanged_outside(before,ledger,allowed)
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    doc=read(DOC);validate_natural_dialogue_batch(doc);rows=doc['records']
    assert len(rows)==10 and Counter(r['editorial_decision'] for r in rows)=={'revise':5,'retain-wording':5}
    selected=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    newkeys={historical_key(r) for r in selected};assert len(newkeys)==10
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];old=before['contextual_story_natural_dialogue_pass_v1871']
    unchanged_outside(old,fresh,{'record_keys','record_IDs','fresh_pass_records_explicitly_reread','fresh_pass_records_integrated',
        'fresh_pass_records_pending_native_actual_release','pending_record_keys','pending_contextual_families',
        'latest_pending_contextual_family','latest_contextual_manuscript','coverage_note'})
    assert not newkeys & {historical_key(r) for r in old['record_keys']}
    assert fresh['record_keys']==old['record_keys']+selected and fresh['record_IDs']==old['record_IDs']+[r['id'] for r in rows]
    assert len({historical_key(r) for r in fresh['record_keys']})==5875
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5875,5865,10)
    assert fresh['pending_record_keys']==selected and fresh['latest_pending_contextual_family']==FAMILY
    assert len(fresh['pending_contextual_families'])==1 and fresh['pending_contextual_families'][0]['record_keys']==selected
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==5878
    assert ledger['records_editorially_completed']==5865
    assert (ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(3728,2137)
    assert ledger['source_prose_reviewed_counts_by_file']=={**before['source_prose_reviewed_counts_by_file'],'/data/SC2.DK4':4022}
    assert ledger['reviewed_but_incomplete_route_record_IDs']=={**before['reviewed_but_incomplete_route_record_IDs'],'/data/SC2.DK4':[r['id'] for r in rows]}
    a,b=before['active_source_prose_drafts'],ledger['active_source_prose_drafts']
    unchanged_outside(a,b,{'manuscripts','route_record_subsets_pending','status','note'})
    assert b['manuscripts']==a['manuscripts']+[str(DOC)]
    assert b['route_record_subsets_pending']=={**a['route_record_subsets_pending'],str(DOC):[r['id'] for r in rows]}
    assert len(ledger['coverage_units'])==len(before['coverage_units'])+1
    for a,b in zip(before['coverage_units'],ledger['coverage_units'][:-1],strict=True):
        if a['id']!='all-route-scenes':assert a==b
        else:
            unchanged_outside(a,b,{'reviewed_route_records','completed_route_records','next'})
            assert (b['reviewed_route_records'],b['completed_route_records'])==(4276,4266)
    assert ledger['coverage_units'][-1]['id']==FAMILY and ledger['coverage_units'][-1]['completion_credit_added']==0
    unchanged_outside(before['formatting_watchlist'],ledger['formatting_watchlist'],{'lil_B176_v4573'})
    source,current=[IlnkContainer.parse(NdsImage.open(p).read_file('/data/SC2.DK4')).blocks[176] for p in ['work/clean.nds',doc['current_ROM']]]
    for row in rows:
        assert all(row['review'].values()) and row['source_meaning']==row['fresh_source_gloss'] and row['full_clean_context_precedes_comparison']
        for data,ref,value in [(source,row['source_reference'],row['source_hex']),(current,row['current_reference'],row['current_hex'])]:
            at=ref['offset'];raw=bytes.fromhex(value)
            assert data[at:at+len(raw)]==raw and data[at+len(raw)]==0
            assert data[at-5:at+1].hex()==row['source_complete_preamble_hex']
        if row['editorial_decision']=='retain-wording':
            assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    fonts=read(doc['native_font_proof'])
    assert len(fonts['cases'])==10 and fonts['current_original_macro_alignment_calls']==80
    assert (fonts['progressive_planes'],fonts['FE_planes'])==(9,1)
    for field,count in [('source_consumer_negative_controls',18),('source_bound_formatter_negatives',28),('source_macro_preservation_negatives',3)]:
        assert len(fonts[field])==count and all(r['rejected'] for r in fonts[field])
    assert len(fonts['review_sheets'])==2 and all(r['viewed_in_full_current_turn'] for r in fonts['review_sheets'])
    for r in fonts['review_sheets']:assert sha(Path(r['path']).read_bytes())==r['sha256']
    controls=read(doc['source_effect_and_predicate_contract']);branch=read(doc['branch_proof'])
    assert len(controls['all3_source_current_nonrelative_nonspeech_leaves'])==3
    assert controls['source_declared_end_offsets']==[386] and len(controls['source_C200_pairs'])==1
    assert len(controls['one_A000_structural_cases'])==1
    assert controls['source_A000_hex_by_offset']=={'8':'00a0ffff010a0da1'}
    assert not controls['source_predicate_cases'] and not controls['source_pause_resume_pairs']
    assert controls['no_source_relative_predicate_2000_pause_2100_4100_resources_or_presentation_sites'] and not branch['cases']
    assert len(controls['source_linear_path_command_offsets'])==13 and controls['all10_speeches_on_complete_linear_structural_path']
    names=read(doc['source_nameplate_consumer_proof']);cases=names['native_four_consumer_cases']['rows']
    assert names['approved_prose_names']=={'174':'Owner','175':'Cook'} and len(cases)==4
    assert all(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['actor_ID'] in [174,175] for r in cases)
    assert all(r['all_actor_models_and_unowned4MiB_exact'] and r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for r in cases)
    terms=read(doc['actor_terminology_reconciliation'])
    assert terms['chosen_city']=='Seville' and len(terms['exact_city_source_current_pointer_bindings'])==2
    assert terms['chosen_ordinary_commodity_word']=='bananas' and terms['FE_Seville_notice_preserves_prospective_likelihood_not_current_or_guaranteed_boom']
    scope=ledger['unfinished_editorial_scope_v4573'];assert scope['incomplete_route_source_prose']==10 and scope['remaining_B177_B180_physical_speeches']==48
    assert scope['canonical_Maria32_pending_uncredited'] and scope['wider_story_shared_town_random_help_prose_open']
    inventory=read(scope['path']);previous=read(before['unfinished_editorial_scope_v4545']['path'])
    assert sha(Path(scope['path']).read_bytes())==scope['sha256']
    unchanged_outside(previous,inventory,{'incomplete_route_source_prose_groups','incomplete_route_source_prose_count','next_focus','broader_coverage_units',
        'B176_fresh_context_review_checkpoint_v4573','remaining_B177_B180_unreviewed_uncredited','earlier_B176_uncredited_leads_are_historical_after_V4573'})
    assert inventory['incomplete_route_source_prose_count']==10
    for a,b in zip(previous['broader_coverage_units'],inventory['broader_coverage_units'],strict=True):
        if a['id']!='all-route-scenes':assert a==b
        else:unchanged_outside(a,b,{'reviewed_route_records','completed_route_records','source_prose_pending_records','source_prose_pending_family','next'})
    receipt=read(CHECKPOINT/'staged_receipt.json')
    for path,digest in {**receipt['evidence'],**receipt['preserved_release_files']}.items():assert sha(Path(path).read_bytes())==digest,path
    promoted=read('translations/promoted_build.json');candidate=ledger['current_integrated_candidate']
    assert promoted['profile']==candidate['profile']=='all-routes-unified-v4541'
    assert sha(Path(promoted['rom']).read_bytes())==promoted['rom_sha256']==candidate['sha256']
    for r in plan:
        if Path(r['target']).suffix=='.md':
            prior=Path(CHECKPOINT/(Path(r['target']).name+'.before')).read_text(encoding='utf-8')
            assert Path(r['planned']).read_text(encoding='utf-8').endswith(prior.split('\n',1)[1])
    # All semantic and complete-plan checks precede the first current metadata write.
    if args.apply:
        for row in plan:assert sha(Path(row['target']).read_bytes())==row['before_sha256']
        for row in plan:
            data=Path(row['planned']).read_bytes()
            with Path(row['target']).open('r+b') as stream:
                stream.write(data);stream.truncate(len(data));stream.flush();os.fsync(stream.fileno())
    for row in plan:assert Path(row['target']).read_bytes()==Path(row['planned']).read_bytes()
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4573')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4573',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5875,
        integrated=5865,pending=10,source_prose=5878,revised=3728,retained=2137,new_source_prose_reviews=10,new_completed_records=0,
        all10_exact_source_current_references_and5_retentions_verified=True,progressive_planes=9,FE_planes=1,
        native_alignment_cases=80,negative_controls=49,all2_complete_native_sheets_viewed=True,
        all_prior_ledger_values_completions_and_scope_preserved=True,main_V4541_unchanged=True,
        remaining_B177_B180_physical_speeches=48,actual_selected_B176_IDs=[],new_emulator_runs=0,
        relocation_representative_registered_release_pending=True,full_goal_active=True,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('V4573 independently verified and applied:5875 reread/5865 completed/10 pending. Main V4541 and every earlier record preserved.')
