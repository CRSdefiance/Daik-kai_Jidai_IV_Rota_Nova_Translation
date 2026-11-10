"""Pin B51's exact five approvals, production evidence and complete predecessor stack."""
import sys
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B51_profile_v1 import contract,validate_approved_batch
from dk4tool.dialogue.hodram_B51_names_v1 import validate_scoped_names
from dk4tool.patch import hodram_B51_editorial_v1 as owned
from scripts.Hodram_B51_release_paths_v8595 import PARENT,ROM,DOC,NAMES,SEAL,CONFIG,proofs,observed_scope
from scripts.verify_village_wrap_v608 import read,save

ROOT=SEAL.parent
if __name__=='__main__':
    assert not ROOT.exists() and not CONFIG.exists()
    data={k:read(p) for k,p in proofs().items()};doc=data['manuscript'];frozen=contract()
    validate_approved_batch(doc);validate_scoped_names(data['names'])
    assert doc==read(DOC) and data['names']==read(NAMES) and data['native_contract']==frozen
    assert len(doc['records'])==5 and doc['revised']==4 and doc['retained']==1
    assert data['independent_native']['summary']['native_body_pages_recomputed']==10
    actual=data['independent_actual']['summary']
    assert actual['complete_actual_holds']==56 and actual['unique_speech_IDs']==4 and actual['complete_actual_page_occurrences']==8
    assert data['independent_comparison']['summary']['later_full_RGB_pairs_recomputed']==89
    control=data['independent_controls']['summary']
    assert [control[k] for k in ['independent_final_dispatches','relative_sites','native_relative_cases','raw_query_cases','normal_seeded_ends','original_result_channel_cases']]==[5,8,40,2,25,50]
    refs=data['independent_references']['positive_lifecycles']
    assert len(refs)==2 and all(r['caller_image_unchanged'] and r['atomic_commits']==0 and r['summary']['whole_reference_ROM_equal'] for r in refs)
    assert data['independent_reconstruction']['entire_research_block_byte_exact'] and data['independent_reconstruction']['negative_count']==20
    prior=data['predecessor_compatibility']
    assert prior['whole_registered_V8543_ROM_byte_exact'] and prior['all_native_semantic_production_gates_enabled']
    assert all(data['builder_support'][k] for k in ['all535_prior_outcomes_dependencies_retained_exact','all675_prior_B49_dependencies_retained_exact','all756_prior_B50_dependencies_retained_exact'])
    assert data['builder_validation']['negative_count']==25 and len(data['builder_validation']['positives'])==5
    for key in ['independent_reconstruction','independent_native','independent_actual','independent_comparison','independent_controls','independent_references','independent_loaders','predecessor_compatibility']:
        for path,digest in data[key]['evidence'].items():assert sha(Path(path).read_bytes())==digest,(key,path)
    parent,reference=NdsImage.open(PARENT),NdsImage.open(ROM)
    parent_sha,reference_sha=sha(PARENT.read_bytes()),sha(ROM.read_bytes())
    assert parent_sha==doc['current_ROM_sha256']==data['reference']['parent_sha256']==prior['current_V8543_sha256']
    assert reference_sha==doc['reference_ROM_sha256']==data['reference']['research_ROM_sha256']
    assert data['reference']['only_changed_blocks']==[51] and data['reference']['all324_otherSC1_blocks_andall_other_files_components_exact'] and data['reference']['complete_parent_ROM_inverse_byte_exact']
    policy=data['policy_validation'];assert policy['negative_count']==322 and policy['all_frozen_dependency_guards_remained_enabled']
    approval=data['format_approval'];assert approval['all5_five_gates_true'] and approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['names_sha256']==sha(NAMES.read_bytes())
    scope=observed_scope(data)
    assert scope['complete_page_occurrences']==8 and scope['complete_body_name_holds']==56 and scope['total_actual_frames']==20002 and scope['unvisited_conditional_text_IDs']==['DK4_MES_B51_R0032']
    correction=Path('translations/gerhard_surname_editorial_release_v2.json')
    configurations={
        'correction':correction,
        'registered_B49':Path('translations/hodram_B49_editorial_release_v4.json'),
        'registered_B50':Path('translations/hodram_B50_editorial_release_v1.json'),
        'compatible_B49':Path('translations/hodram_B49_editorial_release_v5.json'),
        'compatible_B50':Path('translations/hodram_B50_editorial_release_v2.json'),
        'compatible_outcomes':Path('translations/hodram_outcomes_editorial_release_v7.json')}
    dependency=dict(predecessor_profile='all-routes-unified-v8543',predecessor_ROM=str(PARENT),predecessor_ROM_sha256=parent_sha,name_span=data['Gerhard_reference']['only_changed_name_span'])
    for key,path in configurations.items():dependency[key]=str(path);dependency[key+'_sha256']=sha(path.read_bytes())
    records=[{k:r[k] for k in ['id','source_reference','current_reference','final_reference','source_hex','current_hex','final_hex']} for r in doc['records']]
    ROOT.mkdir(parents=True)
    save(SEAL,dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),name_review_sha256=sha(NAMES.read_bytes()),parent=str(PARENT),parent_sha256=parent_sha,reference=str(ROM),reference_sha256=reference_sha,records=records,observed_scope=scope,required_registered_stack_dependency=dependency,all5_source_current_final_references_andwhole_image_inverses_independently_verified=True,all_independent_native_actual_controls_loaders_andcomparison_readers_pass=True,prior_complete_V8543_output_andall_prior_dependencies_preserved=True,atomic_semantic_tests_registered_cumulative_build_clean_patch_andstartup_pending=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(Path(p).read_bytes()) for p in [Path(__file__),*map(Path,proofs().values())]}))
    deps=dict(frozen['dependencies']);previous=read(configurations['compatible_B50'])
    for path,digest in previous['dependencies'].items():assert path not in deps or deps[path]==digest;deps[path]=digest
    paths={DOC,NAMES,SEAL,Path(__file__),Path(owned.__file__),Path('scripts/prepare_Hodram_B51_atomic_v8602.py'),Path('work/analysis/Hodram_B51_atomic_tools_v8602/derivation.json'),Path('scripts/Hodram_B51_release_paths_v8595.py'),Path('translations/hodram_B51_native_contract_v1.json'),*configurations.values(),*map(Path,proofs().values())}
    root=Path.cwd().resolve();builder=Path('scripts/build_integrated_release.py').resolve()
    for module in tuple(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename and filename.endswith('.py'):
            path=Path(filename)
            if path.resolve().is_relative_to(root) and path.resolve()!=builder:paths.add(path)
    for path in paths:
        p=str(path.resolve());h=sha(path.read_bytes());assert p not in deps or deps[p]==h;deps[p]=h
    assert all(deps[p]==h for p,h in frozen['dependencies'].items()) and all(deps[p]==h for p,h in previous['dependencies'].items())
    conf=dict(format='dk4-Hodram-B51-editorial-release-v1',manuscripts=[str(DOC)],proofs=proofs(),parent_ROM=str(PARENT),parent_ROM_sha256=parent_sha,reference_ROM=str(ROM),reference_ROM_sha256=reference_sha,canonical_ROM=str(owned.CANONICAL),canonical_ROM_sha256=sha(owned.CANONICAL.read_bytes()),clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),reference_approval=str(SEAL),predecessor_file_hashes={p:sha(v) for _,p,v in parent.iter_files()},predecessor_component_hashes={p:sha(v) for p,v in parent.iter_components()},required_registered_stack_dependency=dependency,archives=[dict(file_path=owned.PATH,source_sha256=sha(parent.read_file(owned.PATH)),target_sha256=sha(reference.read_file(owned.PATH)))],components=[],dependencies=deps)
    save(CONFIG,conf);owned.check_dependencies(conf)
    save(ROOT/'configuration_receipt.json',dict(configuration=str(CONFIG),configuration_sha256=sha(CONFIG.read_bytes()),dependencies=len(deps),all412_frozen_B51_andall_compatible_predecessor_dependencies_preserved=True,all_original_builder_digest_entries_preserved_not_replaced_by_mutable_builder_hash=True,atomic_module=str(Path(owned.__file__)),atomic_module_sha256=sha(Path(owned.__file__).read_bytes()),reference_seal_sha256=sha(SEAL.read_bytes()),no_builder_registry_ROM_orcompletion_credit_change=True,new_credit=0,full_goal_complete=False))
    print('Sealed five B51 references/all independent readers and complete V8543 predecessor; atomic tests/registered build pending.',flush=True)
