"""Bind unchanged prior semantic cases, the exact corrected inverse, and changed-memory lifecycle negatives."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import hodram_outcomes_editorial_v3 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_outcomes_profile_v3 import contract
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.Hodram_outcomes_release_paths_v8347 import PARENT,ROM,DOC,MAP,SEAL
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_fixture_binding_v8375b')
NEGATIVE=Path('work/analysis/Hodram_outcomes_atomic_challenges_v8356b/actual_changing_semantic_precommit_rejections.json')
PRIOR_BINDING=Path('work/analysis/Hodram_builder_semantic_binding_v8359f/50_prior_semantic_rejections_bound_to_unchanged_gates_new_positive_and8_builder_rejections.json')
DERIVATION=Path('work/analysis/Hodram_outcome_fixture_production_tools_v8372/source_locked_production_fixture_inverse_andtwo_exact_owned_builder_stages.json')
CORRECTION=Path('work/analysis/Hodram_fixture_parent_inverse_validation_v8369/canonical_source_path_complete_V8300_memory_original_failure_reproduced_corrected100holds_pass.json')
POSITIVE=Path('work/analysis/Hodram_outcome_atomic_positive_v8374b/one_whole_NDS_commit_exact_reference_andunchanged_precommit_input.json')
GUARD=Path('work/analysis/Hodram_builder_fixture_successor_validation_v8373/three_exact_builder_forms_eleven_changed_builder_rejections_full_source_inverse.json')
if __name__=='__main__':
    assert not ROOT.exists();negative,prior,derivations,correction,positive,guard=map(read,[NEGATIVE,PRIOR_BINDING,DERIVATION,CORRECTION,POSITIVE,GUARD])
    assert negative['negative_count']==50 and negative['all_expected_semantic_guards_match'] and all(c['rejected'] and c['commit_calls']==0 for c in negative['cases'])
    assert prior['exact_source_equivalence_ofall_semantic_checks'] and prior['prior_semantic_cases']==50 and sha(NEGATIVE.read_bytes())==prior['prior_semantic_suite_sha256']
    bindings=[]
    for d in derivations['derivations'][1:]:
        before,after=Path(d['previous']),Path(d['successor']);a,b=before.read_text('utf8'),after.read_text('utf8');assert sha(before.read_bytes())==d['previous_sha256'] and sha(after.read_bytes())==d['successor_sha256']
        pairs=[('hodram_outcomes_profile_v2','hodram_outcomes_profile_v3'),('hodram_outcomes_layout_v2','hodram_outcomes_layout_v3'),('hodram_outcomes_names_v2','hodram_outcomes_names_v3'),('hodram_outcomes_native_guards_v2','hodram_outcomes_native_guards_v3'),('hodram_outcomes_native_evidence_v3','hodram_outcomes_native_evidence_v4'),('hodram_outcomes_controls_v2','hodram_outcomes_controls_v3'),('hodram_outcomes_actual_evidence_v1','hodram_outcomes_actual_evidence_v2'),('hodram_outcomes_builder_guard_v1','hodram_outcomes_builder_guard_v2'),('hodram_outcomes_editorial_release_v2','hodram_outcomes_editorial_release_v3')]
        changes={x:y for x,y in pairs if x in a};assert checked_text(a,changes)==b;bindings.append(dict(**d,only_explicit_namespace_andcorrected_actual_helper_binding_changed=True))
    assert len(bindings)==7
    a=Path('dk4tool/patch/hodram_outcomes_actual_evidence_v1.py').read_text('utf8');b=Path('dk4tool/patch/hodram_outcomes_actual_evidence_v2.py').read_text('utf8');assert checked_text(a,{'parent.source.read_bytes()':'bytes(parent.rom.save())'})==b
    assert correction['original_disk_path_differs_from_validated_current_contents'] and correction['independent_corrected_actual_result']['complete_actual_holds']==100
    assert positive['single_complete_NDS_commit'] and positive['canonical_source_path_with_exact_current_parent_memory'] and positive['original_object_still_exact_after_commit'] and positive['planned_output_sha256']==sha(ROM.read_bytes())
    assert len(guard['positives'])==3 and len(guard['negatives'])==11 and all(n['rejected'] for n in guard['negatives'])
    conf=read(owned.CONFIG);oldconf=read('translations/hodram_outcomes_editorial_release_v2.json');assert all(conf['dependencies'][p]==h for p,h in oldconf['dependencies'].items())
    for key in oldconf:
        if key!='dependencies':assert conf[key]==oldconf[key]
    watched={Path(p) for p in conf['dependencies']}|{Path(owned.CONFIG),PARENT,ROM,DOC,MAP,SEAL,Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json')};hashes={str(p):sha(p.read_bytes()) for p in watched}
    template=NdsImage.open(PARENT);baseline=NdsImage.open(owned.CANONICAL);results=[];commit=owned.commit_image
    for label,kind in [('canonical-source-wrong-ARM9-memory','ARM9'),('canonical-source-wrong-SC1-memory','SC1'),('canonical-source-without-prior-stack','canonical')]:
        image=NdsImage(owned.CANONICAL,deepcopy(template.rom)) if kind!='canonical' else NdsImage.open(owned.CANONICAL)
        if kind=='ARM9':image.rom.arm9=bytes([image.rom.arm9[0]^1])+image.rom.arm9[1:]
        if kind=='SC1':
            raw=bytearray(image.read_file('/data/SC1.DK4'));raw[-1]^=1;image.replace_file('/data/SC1.DK4',bytes(raw))
        original=image.rom;before=bytes(original.save());assert image.source==owned.CANONICAL and before!=PARENT.read_bytes();calls=[]
        def trap(*args):calls.append('forbidden');raise AssertionError('Incorrect lifecycle input reached commit')
        owned.commit_image=trap
        try:
            try:owned.apply_release(image,baseline)
            except ValueError as error:
                assert 'whole predecessor/reference identities' in str(error);results.append(dict(case=label,rejected=True,error=str(error),changed_input_sha256=sha(before),source_path=str(image.source),commit_calls=0,original_identity_andall_input_bytes_unchanged=True,all_dependency_andnative_guards_enabled=True))
            else:raise AssertionError('Invalid in-memory predecessor accepted:'+label)
        finally:owned.commit_image=commit
        assert not calls and image.rom is original and bytes(image.rom.save())==before
    assert len(results)==3 and hashes=={str(p):sha(p.read_bytes()) for p in watched};frozen=contract()
    ROOT.mkdir(parents=True);save(ROOT/'semantic_binding.json',dict(derivations=bindings,prior_semantic_cases=50,prior_semantic_cases_reused_not_rerun=True,prior_semantic_binding=str(PRIOR_BINDING),prior_semantic_binding_sha256=sha(PRIOR_BINDING.read_bytes()),prior50_standalone_parent_source_bytes_equal_parent_memory_so_inverse_predicate_equivalent=True,one_documented_fixture_inverse_change=str(CORRECTION),one_documented_fixture_inverse_change_sha256=sha(CORRECTION.read_bytes()),current_canonical_source_complete_parent_memory_positive=str(POSITIVE),current_positive_sha256=sha(POSITIVE.read_bytes()),new_lifecycle_negatives=results,new_lifecycle_negative_count=3,new_builder_guard_negative_count=11,new_builder_guard_proof=str(GUARD),new_builder_guard_sha256=sha(GUARD.read_bytes()),all417_frozen_dependency_entries_unchanged=True,all492_prior_production_dependency_hashes_retained=True,all_protected_files_hash_exact=True,no_prior50_case_oractual_emulator_capture_replay_claim=True,no_ROM_registry_counter_promotion_orcredit_change=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Bound prior50 cases to7namespace-only successors +explicit tested inverse correction;new canonical-source positive/3precommit lifecycle negatives/11builder negatives.All492prior pins retained.No capture replay orcredit.')
