"""Independently validate B174 pending scope before applying all staged metadata."""
import argparse
from collections import Counter
import os
import struct
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.checkpoint_lil_B174_v4475 import ROOT as CHECKPOINT,DOC,FAMILY
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v4476')

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
        'coverage_units','formatting_watchlist','unfinished_editorial_scope_v4475','lil_B174_scope_reconciliation_v4475','latest_checkpoint'}
    unchanged_outside(before,ledger,allowed)
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    doc=read(DOC);validate_natural_dialogue_batch(doc);rows=doc['records']
    assert len(rows)==33 and Counter(r['editorial_decision'] for r in rows)=={'revise':23,'retain-wording':10}
    expected=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    old,fresh=[p['contextual_story_natural_dialogue_pass_v1871'] for p in [before,ledger]]
    mutable={'fresh_pass_records_explicitly_reread','fresh_pass_records_pending_native_actual_release','record_keys','record_IDs',
        'pending_record_keys','pending_contextual_families','latest_pending_contextual_family','latest_contextual_manuscript','coverage_note'}
    unchanged_outside(old,fresh,mutable)
    assert fresh['record_keys']==old['record_keys']+expected and fresh['record_IDs']==old['record_IDs']+[r['id'] for r in rows]
    keys=[historical_key(r) for r in fresh['record_keys']];assert len(keys)==len(set(keys))==5833
    assert fresh['pending_record_keys']==expected and len(fresh['pending_contextual_families'])==1
    pending=fresh['pending_contextual_families'][0]
    assert pending['id']==FAMILY and (pending['records'],pending['proposed_revisions'],pending['retentions'])==(33,23,10)
    assert pending['manuscript_sha256']==sha(DOC.read_bytes()) and pending['completion_credit_added']==0
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5833,5800,33)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==5836
    assert ledger['source_prose_reviewed_counts_by_file']=={**before['source_prose_reviewed_counts_by_file'],'/data/SC2.DK4':3980}
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==5836 and ledger['source_prose_reviewed_counts_by_file']['/data/SC3.DK4']==64
    assert tuple(ledger[k] for k in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed'])==(5800,3686,2114)
    assert ledger['reviewed_but_incomplete_route_record_IDs']=={**before['reviewed_but_incomplete_route_record_IDs'],'/data/SC2.DK4':[r['id'] for r in rows]}
    active,old_active=ledger['active_source_prose_drafts'],before['active_source_prose_drafts']
    unchanged_outside(old_active,active,{'manuscripts','route_record_subsets_pending','status','note'})
    assert active['manuscripts']==old_active['manuscripts']+[str(DOC)]
    assert active['route_record_subsets_pending']=={**old_active['route_record_subsets_pending'],str(DOC):[r['id'] for r in rows]}
    assert ledger['formatting_watchlist']=={**before['formatting_watchlist'],'lil_B174_v4475':ledger['formatting_watchlist']['lil_B174_v4475']}
    assert len(ledger['coverage_units'])==len(before['coverage_units'])+1
    for previous,current in zip(before['coverage_units'],ledger['coverage_units'][:-1],strict=True):
        if previous['id']!='all-route-scenes':assert previous==current
        else:
            unchanged_outside(previous,current,{'reviewed_route_records','completed_route_records','next'})
            assert (current['reviewed_route_records'],current['completed_route_records'])==(4234,4201)
    assert ledger['coverage_units'][-1]['id']==FAMILY and ledger['coverage_units'][-1]['completion_credit_added']==0
    images=[NdsImage.open(p) for p in ['work/clean.nds',doc['current_ROM']]]
    source,current=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[174] for im in images]
    for row in rows:
        assert all(row['review'].values()) and row['source_meaning']==row['fresh_source_gloss'] and row['full_clean_context_precedes_comparison']
        for data,reference,value in [(source,row['source_reference'],row['source_hex']),
                                     (current,row['current_reference'],row['current_hex'])]:
            at=reference['offset'];raw=bytes.fromhex(value)
            assert data[at:at+len(raw)]==raw and data[at+len(raw)]==0
            assert data[at-5:at+1].hex()==row['source_complete_preamble_hex']
        if row['editorial_decision']=='retain-wording':
            assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    fonts=read(doc['native_font_proof'])
    assert len(fonts['cases'])==33 and (fonts['current_original_macro_alignment_calls'],fonts['new_current_original_macro_alignment_calls'],fonts['reused_original_macro_alignment_calls'])==(264,8,256)
    assert len(fonts['source_consumer_negative_controls'])==17 and len(fonts['source_bound_formatter_negatives'])==14
    assert len(fonts['source_macro_absence_negatives'])==3 and not fonts['source_macro_preservation_negatives']
    assert len(fonts['review_sheets'])==5
    assert all(r['rejected'] for key in ['source_consumer_negative_controls','source_bound_formatter_negatives','source_macro_absence_negatives'] for r in fonts[key])
    controls=read(doc['source_effect_and_predicate_contract']);branch=read(doc['branch_proof'])
    assert len(controls['all8_source_current_nonrelative_nonspeech_leaves'])==8 and len(controls['one_resource_word10_boundary_cases'])==10
    assert controls['source_predicate_hex']=='0080ffff0efe0030' and controls['source_predicate_raw_hex_words']==['FE0E','3000']
    assert len(controls['source_predicate_cases'])==2 and all(p['native_result']==[2,1,0,0,0,0] for p in controls['source_predicate_cases'])
    assert controls['source_declared_end_offsets']==[2086] and len(controls['source_C200_pairs'])==1
    assert controls['source_A000_hex_by_offset']=={'2068':'00a0ffff020cc960','2076':'00a0ffff1a100120'}
    paths=controls['complete_two_boolean_suffix_paths'];indices=[r['source_record_index'] for r in rows]
    assert paths[0]['spoken_source_record_indices']==[n for n in indices if n!=69] and paths[1]['spoken_source_record_indices']==indices
    assert all(p['original_A000_offsets']==[2068,2076] and p['native_command_offsets'][-5:]==[2066,2068,2076,2084,2086] for p in paths)
    assert len(branch['cases'])==40 and [r['offset'] for r in branch['operands_requiring_adjustment_when_resizing']]==[882,886,890,938]
    names=read(doc['source_nameplate_consumer_proof']);cases=names['native_eight_consumer_cases']['rows']
    assert names['approved_prose_names']=={'2':'Lil','14':'Emilio','26':'Julian','201':'Mihwa'} and len(cases)==8
    assert sum(r['actor_ID'] in [2,14,26] and bool(r['original_scratch_rings']) and bool(r['original_getter_writes']) for r in cases)==6
    assert sum(r['actor_ID']==201 and not r['original_scratch_rings'] and not r['original_getter_writes'] for r in cases)==2
    assert all(r['all_actor_models_and_unowned4MiB_exact'] and r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for r in cases)
    terms=read(doc['actor_terminology_reconciliation'])
    assert (terms['chosen_crown_title'],terms['chosen_site_title'],terms['chosen_city'])==('Silla Gold Crown','Tomb of King Muryeong','Seoul')
    for image,label in zip(images,['source_string','current_string'],strict=True):
        arm=image.read_file('/__arm9__.bin')
        for key in ['exact_global_item_pointer_binding','exact_global_historic_site_pointer_binding']:
            binding=terms[key];value=binding[label]
            assert struct.unpack_from('<I',arm,binding['pointer_field_offset'])[0]==value['pointer']==0x02000000+value['file_offset']
            assert arm[value['file_offset']:value['file_offset']+value['bytes']].hex()==value['hex'] and arm[value['file_offset']+value['bytes']]==0
    scope=ledger['unfinished_editorial_scope_v4475'];assert scope['incomplete_route_source_prose']==33
    assert scope['remaining_B175_B180_physical_speeches']==90 and scope['canonical_Maria32_pending_uncredited']
    inventory,previous=read(scope['path']),read(before['unfinished_editorial_scope_v4449']['path'])
    assert sha(Path(scope['path']).read_bytes())==scope['sha256']
    unchanged_outside(previous,inventory,{'incomplete_route_source_prose_groups','incomplete_route_source_prose_count','next_focus','broader_coverage_units',
        'B174_fresh_context_review_checkpoint_v4475','remaining_B175_B180_unreviewed_uncredited','earlier_B174_uncredited_leads_are_historical_after_V4475'})
    assert inventory['incomplete_route_source_prose_count']==33
    for a,b in zip(previous['broader_coverage_units'],inventory['broader_coverage_units'],strict=True):
        if a['id']!='all-route-scenes':assert a==b
        else:unchanged_outside(a,b,{'reviewed_route_records','completed_route_records','source_prose_pending_records','source_prose_pending_family','next'})
    receipt=read(CHECKPOINT/'staged_receipt.json')
    for path,digest in {**receipt['evidence'],**receipt['preserved_release_files']}.items():assert sha(Path(path).read_bytes())==digest,path
    promoted=read('translations/promoted_build.json');candidate=ledger['current_integrated_candidate']
    assert promoted['profile']==candidate['profile']=='all-routes-unified-v4445'
    assert sha(Path(promoted['rom']).read_bytes())==promoted['rom_sha256']==candidate['sha256']
    # All semantic checks above precede the first current-file write.
    if args.apply:
        for row in plan:
            assert sha(Path(row['target']).read_bytes())==row['before_sha256']
        for row in plan:
            data=Path(row['planned']).read_bytes()
            with Path(row['target']).open('r+b') as stream:
                stream.write(data);stream.truncate(len(data));stream.flush();os.fsync(stream.fileno())
    for row in plan:assert Path(row['target']).read_bytes()==Path(row['planned']).read_bytes()
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4475')
    ROOT.mkdir(parents=True)
    result=dict(checkpoint='V4475',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5833,integrated=5800,pending=33,
        source_prose=5836,revised=3686,retained=2114,new_source_prose_reviews=33,new_completed_records=0,
        all33_clean_current_references_and10_retentions_verified=True,
        native_planes=33,total_alignment_cases=264,fresh_final_alignment_cases=8,exact_reused_alignment_cases=256,
        all45_commands_four_relative_sites_optional_Emilio_two_A000_C200_and_single_end_bound=True,
        all8_original_name_consumers_owned_and_readonly_paths_preserved=True,
        every_prior_ledger_record_completion_and_wider_scope_preserved=True,
        remaining_B175_B180_physical_speeches=90,remaining_choice_command_leads=0,
        candidate=promoted['rom'],candidate_sha256=promoted['rom_sha256'],promoted_main_unchanged=True,
        actual_selected_B174_IDs=[],new_emulator_runs=0,full_goal_active=True,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(ROOT/'verified_handoff.json',result)
    print('V4475 verified/applied:5833 reread,5800 integrated,33 pending;5836 source/prose. All prior history and full scope preserved;main V4445 unchanged.')
