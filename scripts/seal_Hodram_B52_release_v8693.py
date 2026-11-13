"""Seal B52 approvals, all independent readers and complete registered V8609 ancestry."""
import sys
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B52_profile_v1 import contract,validate_approved_batch
from dk4tool.dialogue.hodram_B52_names_v1 import validate_scoped_names
from dk4tool.patch import hodram_B52_editorial_v2 as owned
from scripts.Hodram_B52_release_paths_v8693 import PARENT,ROM,DOC,NAMES,SEAL,CONFIG,proofs,observed_scope
from scripts.verify_village_wrap_v608 import read,save

if __name__=='__main__':
    root=SEAL.parent
    assert not root.exists() and not CONFIG.exists()
    data={k:read(p) for k,p in proofs().items()};doc=data['manuscript'];frozen=contract()
    validate_approved_batch(doc);validate_scoped_names(data['names'])
    assert doc==read(DOC) and data['native_contract']==frozen
    assert len(doc['records'])==3 and len(doc['typed_choice_records'])==2 and (doc['revised'],doc['retained'])==(2,3)
    assert data['policy_validation']['negative_count']==243 and data['policy_validation']['all_frozen_dependency_guards_remained_enabled']
    counts={'independent_reconstruction':26,'independent_references':20,'independent_native':10,'independent_menu':12,
            'independent_controls':9,'independent_loaders':7,'independent_actual':7,'independent_comparison':6}
    for key,count in counts.items():
        assert len(data[key]['negative_cases'])==count
        for path,digest in data[key]['evidence'].items():assert sha(Path(path).read_bytes())==digest,(key,path)
    assert data['independent_actual']['summary']['complete_actual_holds']==138
    assert data['independent_actual']['summary']['unique_speech_IDs']==3
    assert data['independent_comparison']['summary']['later_full_RGB_pairs_recomputed']==199
    assert [data['independent_controls']['summary'][k] for k in ['independent_final_dispatches','native_relative_cases','distinct_seeded_ends','exact_reused_original_result_channel_cases']]==[3,20,50,50]
    q=data['independent_controls']['summary']['source_context_qualification']
    assert q['original_source_context_is_V8543_not_V8609'] and q['whole_RAM_snapshots_equal'] is False and q['no_historical_RAM_overlay_orcode_patch']
    parent,reference=NdsImage.open(PARENT),NdsImage.open(ROM)
    parent_sha,reference_sha=sha(PARENT.read_bytes()),sha(ROM.read_bytes())
    assert parent_sha==doc['current_ROM_sha256']==data['predecessor_release']['candidate_sha256']==data['reference']['parent_sha256']
    assert reference_sha==doc['reference_ROM_sha256']==data['reference']['research_ROM_sha256']
    assert data['reference']['only_changed_blocks']==[52] and data['reference']['all324_otherSC1_blocks_andall_other_files_components_exact'] and data['reference']['complete_parent_ROM_inverse_byte_exact']
    approval=data['format_approval'];assert approval['all5_five_gates_true'] and approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['names_sha256']==sha(NAMES.read_bytes())
    scope=observed_scope(data)
    assert (scope['complete_page_occurrences'],scope['complete_body_name_holds'],scope['total_actual_frames'])==(12,138,50406)
    configurations=[Path('translations')/p for p in ['gerhard_surname_editorial_release_v2.json','hodram_outcomes_editorial_release_v7.json',
        'hodram_B49_editorial_release_v5.json','hodram_B50_editorial_release_v2.json','hodram_B51_editorial_release_v1.json']]
    dependency=dict(profile='all-routes-unified-v8609',ROM=str(PARENT),ROM_sha256=parent_sha,
        configurations={str(p):sha(p.read_bytes()) for p in configurations})
    records=[{k:r[k] for k in ['id','source_reference','current_reference','final_reference','source_hex','current_hex','final_hex']} for r in doc['records']+doc['typed_choice_records']]
    root.mkdir(parents=True)
    save(SEAL,dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),name_review_sha256=sha(NAMES.read_bytes()),
         parent=str(PARENT),parent_sha256=parent_sha,reference=str(ROM),reference_sha256=reference_sha,records=records,
         observed_scope=scope,required_registered_stack_dependency=dependency,
         all5_disjoint_source_current_final_references_andwhole_image_inverses_verified=True,
         all_independent_production_readers_and340_real_changedinput_rejections_pass=True,
         historical_source_context_andunequal_whole_snapshots_qualified_without_RAM_overlay=True,
         complete_registered_V8609_andall_prior_dependencies_preserved=True,
         atomic_tests_registered_cumulative_build_clean_patch_ownstartup_andcredit_pending=True,
         new_credit=0,full_goal_complete=False,evidence={str(p):sha(Path(p).read_bytes()) for p in [__file__,*proofs().values()]}))
    deps=dict(frozen['dependencies']);previous=read('translations/hodram_B52_editorial_release_v1.json')
    for path,digest in previous['dependencies'].items():assert path not in deps or deps[path]==digest;deps[path]=digest
    paths={DOC,NAMES,SEAL,Path('translations/hodram_B52_editorial_release_v1.json'),Path(__file__),Path(owned.__file__),Path('scripts/Hodram_B52_release_paths_v8693.py'),
           Path('translations/hodram_B52_native_contract_v1.json'),*configurations,*map(Path,proofs().values())}
    workspace=Path.cwd().resolve();builder=Path('scripts/build_integrated_release.py').resolve()
    for module in tuple(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename and filename.endswith('.py'):
            path=Path(filename)
            if path.resolve().is_relative_to(workspace) and path.resolve()!=builder:paths.add(path)
    for path in paths:
        resolved=str(path.resolve());digest=sha(path.read_bytes());assert resolved not in deps or deps[resolved]==digest;deps[resolved]=digest
    assert all(deps[p]==h for p,h in frozen['dependencies'].items()) and all(deps[p]==h for p,h in previous['dependencies'].items())
    conf=dict(format='dk4-Hodram-B52-editorial-release-v1',manuscripts=[str(DOC)],proofs=proofs(),parent_ROM=str(PARENT),parent_ROM_sha256=parent_sha,
        reference_ROM=str(ROM),reference_ROM_sha256=reference_sha,canonical_ROM=str(owned.CANONICAL),canonical_ROM_sha256=sha(owned.CANONICAL.read_bytes()),
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),reference_approval=str(SEAL),
        predecessor_file_hashes={p:sha(v) for _,p,v in parent.iter_files()},predecessor_component_hashes={p:sha(v) for p,v in parent.iter_components()},
        required_registered_stack_dependency=dependency,archives=[dict(file_path=owned.PATH,source_sha256=sha(parent.read_file(owned.PATH)),target_sha256=sha(reference.read_file(owned.PATH)))],components=[],dependencies=deps)
    save(CONFIG,conf);owned.check_dependencies(conf)
    save(root/'configuration_receipt.json',dict(configuration=str(CONFIG),configuration_sha256=sha(CONFIG.read_bytes()),dependencies=len(deps),
         frozen_B52_dependency_count=len(frozen['dependencies']),prior_complete_release_dependency_count=len(previous['dependencies']),
         every_frozen_B52_andoriginal855_B51_dependency_entry_retained_exact=True,
         original_builder_digest_entries_preserved_not_replaced_by_mutable_builder_hash=True,
         atomic_module=str(Path(owned.__file__)),atomic_module_sha256=sha(Path(owned.__file__).read_bytes()),reference_seal_sha256=sha(SEAL.read_bytes()),
         no_builder_registry_ROM_orcompletion_credit_change=True,new_credit=0,full_goal_complete=False))
    print('Sealed B52:5 approvals/all independent readers/whole registeredV8609;',len(deps),'dependencies including all471 frozen and855 predecessor entries. Atomic tests/registered integration pending; no ROM/credit.')
