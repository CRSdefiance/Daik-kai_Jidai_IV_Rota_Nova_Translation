"""Positive exact reconstruction and semantic pre-mutation negative controls for names."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import generic_speaker_labels_release_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.seal_generic_speaker_labels_v5887 import OUTPUT,DISPLAY,NAMES,ACTUAL
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/generic_speaker_labels_atomic_v5889')
PARENT=Path('out/all_routes_combined_v5872_candidate.nds')
SEAL=Path('work/analysis/generic_speaker_labels_approval_v5887/three_label_source_native_display_approval.json')

if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();ROOT.mkdir(parents=True)
    prior=read('work/analysis/editorial_handoff_verification_v5878/verified_handoff.json')
    assert sha(PARENT.read_bytes())==prior['candidate_sha256']
    parent=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');clean=NdsImage.open('work/clean.nds')
    deps={OUTPUT,DISPLAY,NAMES,ACTUAL,SEAL,Path(owned.__file__).relative_to(Path.cwd()),Path('dk4tool/patch/generic_speaker_label_data_v1.py'),
        Path('scripts/current_build_native_context_v4774.py'),Path('scripts/generic_name_macro_owned_v5886b.py'),Path('scripts/lil_current_font_oracles_v4792.py'),Path(__file__).relative_to(Path.cwd())}
    for p in [OUTPUT,DISPLAY,NAMES,ACTUAL,SEAL]:
        doc=read(p)
        for field in ['evidence','whole_context_evidence']:
            for path,digest in doc.get(field,{}).items():
                assert sha(Path(path).read_bytes())==digest;deps.add(Path(path))
    for version in read(ACTUAL)['versions']:
        for speech in version['complete_speech_intervals']:
            for hold in speech['holds']:
                p=Path(hold['capture']);assert sha(p.read_bytes())==hold['capture_sha256'];deps.add(p)
    for row in read(DISPLAY)['viewed_sheets']:
        p=Path(row['path']);assert sha(p.read_bytes())==row['sha256'];deps.add(p)
    final=read(OUTPUT);deps.add(Path(final['target_ARM9']))
    conf=dict(format=owned.FORMAT,manuscript=str(OUTPUT),approval=str(SEAL),names=str(NAMES),actual=str(ACTUAL),display=str(DISPLAY),
        source_ARM9_sha256=sha(parent.read_file(owned.PATH)),target_ARM9_sha256=final['target_ARM9_sha256'],
        canonical_ARM9_sha256=sha(baseline.read_file(owned.PATH)),clean_ARM9_sha256=sha(clean.read_file(owned.PATH)),
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        source_files={p:sha(data) for _,p,data in parent.iter_files()},source_components={p:sha(data) for p,data in parent.iter_components()},
        dependencies={str(p):sha(p.read_bytes()) for p in sorted(deps,key=str)},full_goal_complete=False)
    config=ROOT/'positive_config.json';save(config,conf)
    image=NdsImage.open(PARENT);calls=[];replace=image.replace_file
    image.replace_file=lambda *a,**k:(calls.append((a,k)),replace(*a,**k))[1]
    positive=owned.apply_release(image,baseline,config)
    assert len(calls)==1 and image.read_file(owned.PATH)==Path(final['target_ARM9']).read_bytes()
    assert all(image.read_file(p)==data for _,p,data in parent.iter_files())
    assert all(image.read_file(p)==data for p,data in parent.iter_components() if p!=owned.PATH)
    save(ROOT/'positive_reconstruction.json',positive)
    negatives=[];original_load=owned.load
    def reject(label,path,change):
        value=deepcopy(read(path));change(value);image=NdsImage.open(PARENT);before=image.read_file(owned.PATH);calls=[];replace=image.replace_file
        image.replace_file=lambda *a,**k:(calls.append((a,k)),replace(*a,**k))[1]
        owned.load=lambda p:value if Path(p)==Path(path) else original_load(p)
        try:
            try:owned.apply_release(image,baseline,config)
            except (ValueError,AssertionError,KeyError) as exc:reason=str(exc) or type(exc).__name__
            else:raise RuntimeError('Negative accepted:'+label)
        finally:owned.load=original_load
        assert not calls and image.read_file(owned.PATH)==before
        negatives.append(dict(label=label,rejected_before_sole_mutation=True,reason=reason))
    for key in ['source_ARM9_sha256','target_ARM9_sha256','canonical_ARM9_sha256','clean_ARM9_sha256','clean_ROM_sha256']:
        reject('wrong-'+key,config,lambda v,k=key:v.update({k:'0'*64}))
    reject('wrong-cumulative-files',config,lambda v:v['source_files'].update({'/data/SC2.DK4':'0'*64}))
    reject('wrong-cumulative-component',config,lambda v:v['source_components'].update({owned.PATH:'0'*64}))
    reject('wrong-policy',OUTPUT,lambda v:v.update(translation_policy='natural-dialogue-v1'))
    reject('wrong-locale',OUTPUT,lambda v:v.update(target_locale='en-GB'))
    reject('missing-label',OUTPUT,lambda v:v['records'].pop())
    reject('invented-extra-label',OUTPUT,lambda v:v['records'].append(deepcopy(v['records'][0])))
    reject('premature-full-goal-complete',OUTPUT,lambda v:v.update(full_goal_complete=True))
    reject('lost207-review-scope',OUTPUT,lambda v:v.update(all207_name_review_scope_remains_open=False))
    reject('duplicate-prior-review-credit',OUTPUT,lambda v:v.update(no_duplicate_dialogue_or_prior_name_review_credit=False))
    for i in range(3):
        for gate in ['source','context','localization','naturalness','formatting']:
            reject(f'label{i}-lost-{gate}',OUTPUT,lambda v,i=i,g=gate:v['records'][i]['review'].update({g:False}))
        for field,value in [('english','Wife'),('source_Japanese','別人'),('current_English','Someone'),('actor_ID',163),('new_name_completion_credit',1),('new_dialogue_completion_credit',1),('context',''),('formatting_reason','')]:
            reject(f'label{i}-wrong-{field}',OUTPUT,lambda v,i=i,k=field,x=value:v['records'][i].update({k:x}))
        for reference in ['source_reference','current_reference']:
            reject(f'label{i}-wrong-{reference}',OUTPUT,lambda v,i=i,k=reference:v['records'][i][k].update(pointer_field=0))
    for path,key in [(SEAL,'all621_parent_and621_target_primary_secondary_middle_consumers_pass'),(SEAL,'only_three_primary_outputs_change'),
        (SEAL,'no_full_catalogue_UI_natural_event_activation_original_location_full_route_or_hardware_claim'),
        (NAMES,'all204_unaffected_actors_both_name_consumers_exact'),(NAMES,'all207_voice_classes_and_original_name_ownership_paths_exact'),
        (ACTUAL,'complete_native_ASCII_glyph_masks_first_final_characters_and_blank_guards_exact'),
        (DISPLAY,'parent_target_macro_and_literal_outputs_exact'),(DISPLAY,'actual_nameplate_independent_masks_and_five_complete_context_sheets_viewed'),
        (DISPLAY,'all_unowned4MiB_models_RNG_inputs_outputs_ABI_canaries_and_source_owned_name_ring_restoration_exact')]:
        reject('missing-'+key,path,lambda v,k=key:v.update({k:False}))
    for path,key,value in [(ACTUAL,'complete_speech_observations',27),(ACTUAL,'actual_target_nameplate_cases',15),(DISPLAY,'native_macro_alignment_cases',63)]:
        reject('incomplete-'+key,path,lambda v,k=key,x=value:v.update({k:x}))
    save(ROOT/'negative_cases.json',negatives)
    save(ROOT/'atomic_validation_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),
        positive_proof=str(ROOT/'positive_reconstruction.json'),positive_proof_sha256=sha((ROOT/'positive_reconstruction.json').read_bytes()),
        positive_records=3,negative_count=len(negatives),all_negatives_reject_before_mutation=True,
        negative_cases=str(ROOT/'negative_cases.json'),dependency_count=len(deps),parent_ROM_sha256=sha(PARENT.read_bytes()),
        no_registered_ROM_registry_or_ledger_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(positive_labels=3,semantic_negatives=len(negatives),locked_dependencies=len(deps),all_rejected_before_mutation=True))
