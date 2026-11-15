"""Bind unchanged14 semantic cases to one corrected dependency predicate andnew full positive."""
from pathlib import Path
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import hodram_B49_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_pin_semantics_v8465b')
CONFIG=Path('translations/hodram_B49_editorial_release_v3.json')
POSITIVE=Path('work/analysis/Hodram_B49_atomic_positive_v8465/atomic_positive.json')
NEGATIVE=Path('work/analysis/Hodram_B49_atomic_challenges_v8457/semantic_rejections.json')
FIX=Path('work/analysis/Hodram_B49_builder_pin_fix_v8464/pin_correction.json')
if __name__=='__main__':
    assert not ROOT.exists();conf,positive,negative,fix=map(read,[CONFIG,POSITIVE,NEGATIVE,FIX]);old=read('translations/hodram_B49_editorial_release_v2.json')
    assert all(conf[k]==old[k] for k in old if k!='dependencies') and all(conf['dependencies'][p]==h for p,h in old['dependencies'].items() if p!=fix['builder_dependency_path'])
    assert conf['dependencies'][fix['builder_dependency_path']]==fix['guarded_original_builder_inverse_digest'] and fix['only_one_dependency_predicate_corrected_all_other_prior_entries_exact']
    assert positive['one_complete_NDS_commit'] and positive['original_object_still_exact_after_commit'] and positive['canonical_source_path_withcomplete_V8377_memory']
    assert negative['negative_count']==14 and negative['all_changed_inputs_distinct_andexpected_semantic_guards_match'] and negative['no_frozen_native_orsemantic_guard_bypassed'] and all(c['rejected'] and c['commit_calls']==0 for c in negative['cases'])
    module=Path(owned.__file__);assert positive['evidence'][str(module)]==sha(module.read_bytes())
    watched={Path(p) for p in conf['dependencies']}|{CONFIG,Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json')};hashes={str(p):sha(p.read_bytes()) for p in watched}
    template=NdsImage.open(conf['parent_ROM']);baseline=NdsImage.open(owned.CANONICAL);commit=owned.commit_image;results=[]
    for label,kind in [('canonical-source-wrong-ARM9','ARM9'),('canonical-source-wrong-SC1','SC1'),('canonical-source-missing-prior-stack','canonical')]:
        image=NdsImage(owned.CANONICAL,deepcopy(template.rom)) if kind!='canonical' else NdsImage.open(owned.CANONICAL)
        if kind=='ARM9':image.rom.arm9=bytes([image.rom.arm9[0]^1])+image.rom.arm9[1:]
        if kind=='SC1':
            raw=bytearray(image.read_file(owned.PATH));raw[-1]^=1;image.replace_file(owned.PATH,bytes(raw))
        original=image.rom;before=bytes(original.save());calls=[]
        def forbidden(*args):calls.append('forbidden');raise AssertionError('Changed in-memory predecessor reached commit')
        owned.commit_image=forbidden
        try:
            try:owned.apply_release(image,baseline,config=CONFIG)
            except ValueError as exc:
                assert 'whole in-memory predecessor/reference identities' in str(exc);results.append(dict(case=label,rejected=True,error=str(exc),changed_input_sha256=sha(before),commit_calls=0,all_dependency_frozen_native_andsemantic_guards_enabled=True))
            else:raise AssertionError('Wrong in-memory predecessor accepted')
        finally:owned.commit_image=commit
        assert not calls and image.rom is original and bytes(original.save())==before
    assert hashes=={str(p):sha(p.read_bytes()) for p in watched};ROOT.mkdir(parents=True)
    save(ROOT/'semantic_binding.json',dict(prior14_semantic_cases_reused_not_rerun=True,prior_semantic_suite=str(NEGATIVE),prior_semantic_suite_sha256=sha(NEGATIVE.read_bytes()),same_exact_atomic_module_andall_non_dependency_configuration_fields=True,prior_suite_bypassed_exactly_the_only_corrected_dependency_layer_therefore_semantic_predicates_identical=True,one_documented_builder_dependency_correction=str(FIX),correction_sha256=sha(FIX.read_bytes()),current_complete_positive=str(POSITIVE),current_positive_sha256=sha(POSITIVE.read_bytes()),new_all_guards_enabled_wrong_memory_rejections=results,new_lifecycle_rejection_count=3,all_current_protected_files_hash_exact=True,no_ROM_registry_counter_orcredit_change=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Bound all14 prior semantic cases tosame exact module/metadata andone stricterbuilder inverse predicate;newfullpositive plus3wrong-memory rejections passwithallguards.No replay orcredit.')
