"""Independently verify uncredited B179 context and all prior completed editorial history."""
import gzip
import json
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.checkpoint_lil_B179_context_v4716 import ROOT as CHECKPOINT,PRIOR,GLOSS,SOURCE,VOICE,DISPATCH,BRANCH,ENTRY,NAMES,CONTROL,IDENTITY
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v4717')


def same_except(a,b,allowed):
    assert {k:v for k,v in a.items() if k not in allowed}=={k:v for k,v in b.items() if k not in allowed}


if __name__=='__main__':
    assert not ROOT.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    oldbytes=gzip.decompress((CHECKPOINT/'ledger.before.json.gz').read_bytes());before=json.loads(oldbytes)
    assert sha(oldbytes)==read(PRIOR)['ledger_sha256']
    same_except(before,ledger,{'latest_checkpoint','lil_B179_clean_context_native_research_v4716','coverage_units'})
    for a,b in zip(before['coverage_units'],ledger['coverage_units'],strict=True):
        if a['id']=='all-route-scenes':same_except(a,b,{'next'})
        else:assert a==b
    assert lp.read_bytes()==encode_ledger(ledger) and lp.stat().st_size<100*1024*1024
    assert tuple(ledger[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass',
        'records_revised_and_integrated','retained_wordings_editorially_completed'])==(5898,5901,3740,2158)
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert tuple(fresh[k] for k in ['fresh_pass_records_explicitly_reread','fresh_pass_records_integrated',
        'fresh_pass_records_pending_native_actual_release'])==(5898,5898,0)
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    receipt=read(CHECKPOINT/'checkpoint_receipt.json');assert receipt['ledger_sha256']==sha(lp.read_bytes())
    for p,h in {**receipt['evidence'],**receipt['stable_release_files'],**receipt['updated_files']}.items():assert sha(Path(p).read_bytes())==h,p
    gloss,source,voice,dispatch,branch,entry,names,controls,identity=map(read,[GLOSS,SOURCE,VOICE,DISPATCH,BRANCH,ENTRY,NAMES,CONTROL,IDENTITY])
    assert gloss['all14_clean_source_read_and_individually_glossed_before_predecessor_English'] and gloss['no_predecessor_English_exposed']
    assert len(source['records'])==len(gloss['block']['records'])==14
    assert not Path('translations/lil_B179_editorial_manuscript_v1.json').exists() and not Path('work/analysis/lil_B179_comparison_v4716').exists()
    for proof in [voice,dispatch,branch,entry,names,controls,identity]:assert proof['source_context_sha256']==sha(SOURCE.read_bytes())
    current=NdsImage.open(source['current_ROM']);clean=NdsImage.open('work/clean.nds')
    assert sha(Path(source['current_ROM']).read_bytes())==source['current_ROM_sha256']==ledger['current_integrated_candidate']['sha256']
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[179] for im in [clean,current]]
    by={r['id']:r for r in gloss['block']['records']}
    for r in source['records']:
        assert r['fresh_source_gloss']==by[r['id']]['fresh_source_gloss'] and r['source_Japanese']==by[r['id']]['source_Japanese']
        for block,ref,value in zip(blocks,[r['source_reference'],r['current_reference']],[r['source_hex'],r['current_hex']],strict=True):
            at=ref['offset'];raw=bytes.fromhex(value)
            assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0 and block[at-5:at+1].hex()==r['source_complete_preamble_hex']
    assert source['source_macro_counts']=={'FI':0,'FA':0,'FO':0} and source['source_static_actor_selectors']==[92,96,152]
    assert len(dispatch['speech_dispatch_cases'])==28 and sum(r['source_selector']==254 for r in dispatch['speech_dispatch_cases'])==2
    assert not branch['cases'] and not branch['operands_requiring_adjustment_when_resizing']
    assert [(r['event_ID'],r['script_block'],r['action_index']) for r in entry['selected_B179_source_events']]==[(179,179,180)]
    assert [(r['offset'],r['source_current_hex']) for r in controls['all2_source_current_nonrelative_nonspeech_leaves']]==[(8,'00a0ffff01221da1'),(508,'00000000')]
    assert controls['source_has_no_C200_and_no_C200_probe_invented'] and not controls['source_C200_pairs']
    assert controls['source_A000_packed_operand_semantics_not_inferred'] and len(controls['one_A000_structural_cases'])==1
    assert names['approved_prose_names']==identity['approved_dialogue_roles']=={'92':'Barkeep','96':'Patron','152':'Sailor'}
    assert names['full_catalogue_values']=={'92':'Barkeep','96':'Patron','152':'Retainer'}
    assert names['readonly_consumer_count']==6 and names['source_owned_scratch_consumer_count']==0
    assert all(not r['original_getter_writes'] and not r['original_scratch_rings'] and r['all_actor_models_and_unowned4MiB_exact']
        for r in names['native_six_consumer_cases']['rows'])
    arm,original=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    for b in identity['progressive_role_source_current_bindings']:
        at=b['file_offset'];a=bytes.fromhex(b['source_complete_terminated_hex']);v=bytes.fromhex(b['current_complete_terminated_hex'])
        assert original[at:at+len(a)]==a and arm[at:at+len(v)]==v and b['pointer']==0x02000000+at
    assert identity['exact_progressive_source_Sailor_Japanese_suifu_not_inferred_from_catalogue_Retainer']
    assert identity['separate_catalogue152_pointer']==0x02387E48 and identity['staged_payload_bytes']==123040
    promoted=read('translations/promoted_build.json')
    assert promoted['profile']=='all-routes-unified-v4595' and sha(Path(promoted['rom']).read_bytes())==promoted['rom_sha256']
    assert ledger['current_integrated_candidate']['profile']=='all-routes-unified-v4701'
    release=read('work/analysis/lil_B178_release_v4702/registered_release_verification.json')
    assert Path(release['candidate']).read_bytes()==Path('out/lil_B178_reference_v4686_RESEARCH_ONLY.nds').read_bytes()==Path(release['exact_patch_reconstruction']).read_bytes()
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert read('work/analysis/lil_B178_build_v4701/build_terminal.json')['returncode']==0
    for case in ['newgame','town']:assert read('work/analysis/lil_B178_runs_v4703/'+case+'_terminal.json')['terminal']
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        assert Path('docs',name).read_text(encoding='utf-8').endswith((CHECKPOINT/(name+'.before')).read_text(encoding='utf-8').split('\n',1)[1])
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4716')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4716',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5898,integrated=5898,pending=0,
        source_prose=5901,revised=3740,retained=2158,uncredited_B179_clean_glosses=14,
        all_prior_root_nested_history_counts_and_full_objective_preserved=True,all14_clean_gloss_source_current_references_bound=True,
        three_static_roles28_dispatches6_readonly_name_paths_A000_and_single_end_no_C200_bound=True,
        source_dialogue_Sailor152_and_separate_catalogue_Retainer152_distinguished=True,
        terms_comparison_prose_native_actual_reference_and_release_still_pending=True,
        main_V4595_preserved=True,latest_experimental_V4701_and_exact_patch_verified=True,
        all_jobs_terminal=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('V4716 independently verified:5898 completed;14 uncredited B179 glosses/native bindings,Sailor152/catalogRetainer152 distinguished,full history/main V4595/latest V4701 preserved.')
