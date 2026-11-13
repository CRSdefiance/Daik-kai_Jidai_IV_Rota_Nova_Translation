"""Exact positive reconstruction and semantic rejection before the sole ARM9 mutation."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch import shady_man_label_release_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.seal_shady_man_label_v6266 import OUTPUT,NAMES,ACTUAL,DISPLAY,DIFFERENCES
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shady_man_label_atomic_v6267');PARENT=Path('out/all_routes_combined_v6220_candidate.nds');SEAL=Path('work/analysis/shady_man_label_approval_v6266/one_label_source_native_display_approval.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();ROOT.mkdir(parents=True)
    prior=read('work/analysis/editorial_handoff_verification_v6256/verified_handoff.json');assert sha(PARENT.read_bytes())==prior['candidate_sha256']
    parent=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');clean=NdsImage.open('work/clean.nds');deps={OUTPUT,NAMES,ACTUAL,DISPLAY,DIFFERENCES,SEAL,Path(__file__).relative_to(Path.cwd()),Path(owned.__file__).relative_to(Path.cwd()),Path('dk4tool/patch/shady_man_label_data_v1.py'),Path('scripts/shady_man_font_oracles_v6263.py'),Path('scripts/current_build_native_context_v6261.py'),Path('scripts/current_build_native_context_v6097.py'),Path('scripts/generic_name_macro_owned_v5886b.py')}
    queue=list(deps);seen=set()
    while queue:
        p=queue.pop()
        if p in seen:continue
        seen.add(p)
        if p.suffix!='.json':continue
        d=read(p)
        if not isinstance(d,dict):continue
        for field in ['evidence','whole_context_evidence']:
            for path,digest in d.get(field,{}).items():
                q=Path(path);assert sha(q.read_bytes())==digest
                if q not in deps:deps.add(q);queue.append(q)
    for r in read(ACTUAL)['complete_speech_intervals']:
        for h in r['holds']:
            p=Path(h['capture']);assert sha(p.read_bytes())==h['capture_sha256'];deps.add(p)
    seal=read(SEAL)
    for r in seal['viewed_sheets']:
        p=Path(r['path']);assert sha(p.read_bytes())==r['sha256'];deps.add(p)
    deps.add(Path(seal['viewed_native_plane']['image']));final=read(OUTPUT);deps.add(Path(final['target_ARM9']))
    conf=dict(format=owned.FORMAT,manuscript=str(OUTPUT),approval=str(SEAL),names=str(NAMES),actual=str(ACTUAL),display=str(DISPLAY),source_ARM9_sha256=sha(parent.read_file(owned.PATH)),target_ARM9_sha256=final['target_ARM9_sha256'],canonical_ARM9_sha256=sha(baseline.read_file(owned.PATH)),clean_ARM9_sha256=sha(clean.read_file(owned.PATH)),clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),source_files={p:sha(v) for _,p,v in parent.iter_files()},source_components={p:sha(v) for p,v in parent.iter_components()},dependencies={str(p):sha(p.read_bytes()) for p in sorted(deps,key=str)},full_goal_complete=False)
    config=ROOT/'positive_config.json';save(config,conf);image=NdsImage.open(PARENT);calls=[];replace=image.replace_file;image.replace_file=lambda *a,**k:(calls.append((a,k)),replace(*a,**k))[1]
    positive=owned.apply_release(image,baseline,config);assert len(calls)==1 and image.read_file(owned.PATH)==Path(final['target_ARM9']).read_bytes()
    assert all(image.read_file(p)==v for _,p,v in parent.iter_files()) and all(image.read_file(p)==v for p,v in parent.iter_components() if p!=owned.PATH)
    save(ROOT/'positive_reconstruction.json',positive);negatives=[];original_load=owned.load
    def reject(label,path,change):
        value=deepcopy(read(path));change(value);image=NdsImage.open(PARENT);before=image.read_file(owned.PATH);calls=[];replace=image.replace_file
        image.replace_file=lambda *a,**k:(calls.append((a,k)),replace(*a,**k))[1];owned.load=lambda p:value if Path(p)==Path(path) else original_load(p)
        try:
            try:owned.apply_release(image,baseline,config)
            except (ValueError,AssertionError,KeyError,IndexError) as exc:reason=str(exc) or type(exc).__name__
            else:raise RuntimeError('Negative accepted:'+label)
        finally:owned.load=original_load
        assert not calls and image.read_file(owned.PATH)==before;negatives.append(dict(label=label,rejected_before_sole_mutation=True,reason=reason))
    for key in ['source_ARM9_sha256','target_ARM9_sha256','canonical_ARM9_sha256','clean_ARM9_sha256','clean_ROM_sha256']:reject('wrong-'+key,config,lambda v,k=key:v.update({k:'0'*64}))
    reject('lost-cumulative-story',config,lambda v:v['source_files'].update({'/data/SC2.DK4':'0'*64}));reject('lost-cumulative-component',config,lambda v:v['source_components'].update({owned.PATH:'0'*64}))
    for key,value in [('translation_policy','natural-dialogue-v1'),('target_locale','en-GB'),('full_goal_complete',True),('all207_name_review_scope_remains_open',False),('no_duplicate_dialogue_or_prior_name_review_credit',False)]:reject('wrong-'+key,OUTPUT,lambda v,k=key,x=value:v.update({k:x}))
    reject('missing-label',OUTPUT,lambda v:v['records'].pop());reject('extra-label',OUTPUT,lambda v:v['records'].append(deepcopy(v['records'][0])))
    for gate in ['source','context','localization','naturalness','formatting']:reject('missing-'+gate,OUTPUT,lambda v,k=gate:v['records'][0]['review'].update({k:False}))
    for key,value in [('english','Arab Merchant'),('source_Japanese','別人'),('current_English','Someone'),('actor_ID',172),('new_name_completion_credit',1),('new_dialogue_completion_credit',1),('context',''),('formatting_reason','')]:reject('wrong-row-'+key,OUTPUT,lambda v,k=key,x=value:v['records'][0].update({k:x}))
    for ref in ['source_reference','current_reference']:
        for key in ['pointer_field','pointer' if ref=='source_reference' else 'runtime_pointer']:reject('wrong-'+ref+'-'+key,OUTPUT,lambda v,r=ref,k=key:v['records'][0][r].update({k:0}))
    for key in ['all_five_gates_complete_for_one_source_owned_label','all621_parent_and621_target_fields_pass','all414_parent_and414_target_name_consumers_pass','only_actor173_primary_changes_all206_other_names_and_voices_exact','original96_macro_alignments_and_complete_font_plane_pass','actual18_nameplates10_target_headers_two_sheets_and_native_plane_viewed','no_catalogue_UI_natural_activation_original_location_full_effects_routes_earned_progress_or_hardware_claim','timing_and_RNG_differences_explicitly_preserved','full207_name_and_wider_editorial_goal_remains_open']:reject('missing-seal-'+key,SEAL,lambda v,k=key:v.update({k:False}))
    for path,keys in [(NAMES,['all414_parent_and414_target_name_consumers_pass','all621_parent_and621_target_fields_pass','all206_unaffected_actors_both_name_consumers_exact','all207_voice_classes_and_original_name_ownership_paths_exact','only_actor173_primary_changes_secondary_middle_and_all_pointers_exact']),(ACTUAL,['complete_native_ASCII_glyph_masks_first_final_characters_and_blank_guards_exact','source_and_target_command_offsets_words_results_lengths_and_UI_words_exact','no_whole_state_or_broad_simulation_equivalence_claim']),(DISPLAY,['parent_target_macro_and_literal_outputs_exact','all_unowned4MiB_models_RNG_inputs_outputs_ABI_canaries_and_source_owned_name_ring_restoration_exact'])]:
        for key in keys:reject('missing-'+key,path,lambda v,k=key:v.update({k:False}))
    for path,key,value in [(NAMES,'changed_catalog_actor_IDs',[172]),(ACTUAL,'complete_speech_observations',17),(ACTUAL,'actual_target_nameplate_cases',9),(ACTUAL,'exit_frame',7893),(ACTUAL,'following_B120_end_frame',12697),(DISPLAY,'native_macro_alignment_cases',95)]:reject('incomplete-'+key,path,lambda v,k=key,x=value:v.update({k:x}))
    reject('concealed-RNG-differences',DIFFERENCES,lambda v:v.update(no_timing_RNG_whole_state_or_broad_simulation_equivalence_claim=False))
    save(ROOT/'negative_cases.json',negatives);save(ROOT/'atomic_validation_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),positive_proof=str(ROOT/'positive_reconstruction.json'),positive_proof_sha256=sha((ROOT/'positive_reconstruction.json').read_bytes()),positive_records=1,negative_count=len(negatives),all_negatives_reject_before_mutation=True,dependency_count=len(deps),parent_ROM_sha256=sha(PARENT.read_bytes()),no_registered_ROM_registry_or_ledger_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(positive_labels=1,semantic_negatives=len(negatives),locked_dependencies=len(deps),all_rejected_before_mutation=True))
