"""Seal all completed B50 independent evidence and pin an unregistered whole-image atomic stage."""
import sys
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B50_profile_v2 import contract,validate_approved_batch
from dk4tool.dialogue.hodram_B50_names_v2 import validate_scoped_names
from dk4tool.patch import hodram_B50_editorial_v1 as owned
from scripts.Hodram_B50_release_paths_v8537 import PARENT,ROM,DOC,NAMES,SEAL,CONFIG,proofs,observed_scope
from scripts.verify_village_wrap_v608 import read,save

ROOT=SEAL.parent
if __name__=='__main__':
    assert not ROOT.exists() and not CONFIG.exists();data={k:read(p) for k,p in proofs().items()};doc=data['manuscript'];frozen=contract();validate_approved_batch(doc);validate_scoped_names(data['names'])
    assert doc==read(DOC) and data['names']==read(NAMES) and data['native_contract']==frozen
    assert data['independent_native']['independent_native_summary']['native_body_pages_recomputed']==6
    assert data['independent_actual_FE']['actual_summary']['complete_actual_holds']==50 and data['independent_actual_FE']['actual_summary']['unique_speech_IDs']==3
    assert data['independent_actual_FE']['FE_summary']['complete_actual_VRAM_bitmap_palette_RGB_holds_recomputed']==6
    assert data['independent_comparison']['result']['later_full_RGB_pairs_recomputed']==89
    assert data['independent_controls']['result']['native_relative_cases']==0 and data['independent_controls']['result']['normal_seeded_ends']==25
    assert data['independent_references']['canonical_source_withfull_current_ROM_positive'] and data['independent_references']['references']['whole_reference_ROM_equal']
    assert data['predecessor_compatibility']['whole_registered_V8475_ROM_byte_exact'] and data['predecessor_compatibility']['all_native_semantic_production_gates_enabled']
    assert data['builder_support']['all524_prior_outcomes_dependencies_retained_exact'] and data['builder_support']['all663_prior_B49_dependencies_retained_exact']
    assert data['builder_validation']['negative_count']==16 and len(data['builder_validation']['positives'])==4
    for key in ['independent_native','independent_actual_FE','independent_comparison','independent_controls','independent_references','predecessor_compatibility']:
        for path,digest in data[key]['evidence'].items():assert sha(Path(path).read_bytes())==digest
    parent,reference=NdsImage.open(PARENT),NdsImage.open(ROM);parent_sha,reference_sha=sha(PARENT.read_bytes()),sha(ROM.read_bytes())
    assert parent_sha==doc['current_ROM_sha256']==data['reference']['parent_sha256']==data['predecessor_compatibility']['current_V8475_sha256']
    assert reference_sha==doc['reference_ROM_sha256']==data['reference']['research_ROM_sha256']
    assert data['reference']['all324_otherSC1_blocks_andall_other_files_components_exact'] and data['reference']['complete_parent_ROM_inverse_byte_exact']
    assert data['policy_validation']['negative_count']==182 and data['format_approval']['all3_five_gates_true']
    assert data['gate_metadata_approval']['manuscript_sha256']==sha(DOC.read_bytes()) and data['gate_metadata_approval']['all_source_current_final_records_names_prose_compiled_bytes_individual_gates_andactual_evidence_value_exact']
    scope=observed_scope(data);assert scope['complete_page_occurrences']==6 and scope['complete_body_name_orabsent_FE_header_holds']==50 and scope['total_actual_frames']==20002
    correction=Path('translations/gerhard_surname_editorial_release_v2.json');registeredB49=Path('translations/hodram_B49_editorial_release_v3.json');compatibleB49=Path('translations/hodram_B49_editorial_release_v4.json');compatibleOutcomes=Path('translations/hodram_outcomes_editorial_release_v6.json')
    dependency=dict(predecessor_profile='all-routes-unified-v8475',predecessor_ROM=str(PARENT),predecessor_ROM_sha256=parent_sha,correction=str(correction),correction_sha256=sha(correction.read_bytes()),name_span=data['Gerhard_reference']['only_changed_name_span'],registered_B49=str(registeredB49),registered_B49_sha256=sha(registeredB49.read_bytes()),compatible_B49=str(compatibleB49),compatible_B49_sha256=sha(compatibleB49.read_bytes()),compatible_outcomes=str(compatibleOutcomes),compatible_outcomes_sha256=sha(compatibleOutcomes.read_bytes()))
    records=[dict(id=r['id'],source_reference=r['source_reference'],current_reference=r['current_reference'],final_reference=r['final_reference'],source_hex=r['source_hex'],current_hex=r['current_hex'],final_hex=r['final_hex']) for r in doc['records']]
    ROOT.mkdir(parents=True);save(SEAL,dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),name_review_sha256=sha(NAMES.read_bytes()),parent=str(PARENT),parent_sha256=parent_sha,reference=str(ROM),reference_sha256=reference_sha,records=records,observed_scope=scope,required_registered_stack_dependency=dependency,all3_source_current_final_references_andwhole_image_inverses_independently_verified=True,all_independent_native_actual_FE_controls_loaders_andcomparison_readers_pass=True,prior_complete_V8475_output_andall_prior_dependencies_preserved=True,atomic_semantic_tests_registered_cumulative_build_clean_patch_andstartup_pending=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(Path(p).read_bytes()) for p in [Path(__file__),*map(Path,proofs().values())]}))
    deps=dict(frozen['dependencies']);previous=read(compatibleB49)
    for path,digest in previous['dependencies'].items():assert path not in deps or deps[path]==digest;deps[path]=digest
    paths={DOC,NAMES,SEAL,Path(__file__),Path(owned.__file__),Path('scripts/Hodram_B50_release_paths_v8537.py'),Path('translations/hodram_B50_native_contract_v2.json'),compatibleB49,compatibleOutcomes,*map(Path,proofs().values())}
    root=Path.cwd().resolve();builder=Path('scripts/build_integrated_release.py').resolve()
    for module in tuple(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename and filename.endswith('.py'):
            path=Path(filename)
            if path.resolve().is_relative_to(root) and path.resolve()!=builder:paths.add(path)
    for path in paths:
        p=str(path.resolve());h=sha(path.read_bytes());assert p not in deps or deps[p]==h;deps[p]=h
    assert all(deps[p]==h for p,h in frozen['dependencies'].items()) and all(deps[p]==h for p,h in previous['dependencies'].items())
    conf=dict(format='dk4-Hodram-B50-editorial-release-v1',manuscripts=[str(DOC)],proofs=proofs(),parent_ROM=str(PARENT),parent_ROM_sha256=parent_sha,reference_ROM=str(ROM),reference_ROM_sha256=reference_sha,canonical_ROM=str(owned.CANONICAL),canonical_ROM_sha256=sha(owned.CANONICAL.read_bytes()),clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),reference_approval=str(SEAL),predecessor_file_hashes={p:sha(v) for _,p,v in parent.iter_files()},predecessor_component_hashes={p:sha(v) for p,v in parent.iter_components()},required_registered_stack_dependency=dependency,archives=[dict(file_path=owned.PATH,source_sha256=sha(parent.read_file(owned.PATH)),target_sha256=sha(reference.read_file(owned.PATH)))],components=[],dependencies=deps)
    save(CONFIG,conf);owned.check_dependencies(conf)
    save(ROOT/'configuration_receipt.json',dict(configuration=str(CONFIG),configuration_sha256=sha(CONFIG.read_bytes()),dependencies=len(deps),all409_frozen_B50_andall_compatible_predecessor_dependencies_preserved=True,all_original_builder_digest_entries_preserved_not_replaced_by_mutable_builder_hash=True,atomic_module=str(Path(owned.__file__)),atomic_module_sha256=sha(Path(owned.__file__).read_bytes()),reference_seal_sha256=sha(SEAL.read_bytes()),no_builder_registry_ROM_orcompletion_credit_change=True,new_credit=0,full_goal_complete=False))
    print('Sealed3 B50 references andall independent readers;production dependencies pinned.Atomic positive/semantic challenges/registered build remain pending.No ROM orcredit.')
