"""Seal completed independent readers and pin an unregistered cumulative atomic stage."""
import sys
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B49_profile_v2 import contract,validate_approved_batch
from dk4tool.dialogue.hodram_B49_names_v2 import validate_scoped_names
from dk4tool.patch import hodram_B49_editorial_v1 as owned
from scripts.Hodram_B49_release_paths_v8447 import PARENT,ROM,DOC,NAMES,SEAL,CONFIG,proofs,observed_scope
from scripts.verify_village_wrap_v608 import read,save

ROOT=SEAL.parent
if __name__=='__main__':
    assert not ROOT.exists() and not CONFIG.exists();data={k:read(p) for k,p in proofs().items()};doc=data['manuscript'];frozen=contract();validate_approved_batch(doc);validate_scoped_names(data['names'])
    assert doc==read(DOC) and data['names']==read(NAMES) and data['native_contract']==frozen
    assert data['independent_native']['independent_native_summary']['native_body_pages_recomputed']==28
    assert data['independent_actual']['actual_summary']['complete_actual_holds']==200 and data['independent_actual']['actual_summary']['unique_speech_IDs']==14
    assert data['independent_FE']['result']['complete_actual_VRAM_bitmap_palette_RGB_holds_recomputed']==4
    assert data['independent_menu']['result']['actual_owned_backing_samples_recomputed']==12 and data['independent_menu']['result']['complete_visible_label_samples_recomputed']==24
    assert data['independent_comparison']['result']['later_full_RGB_pairs_recomputed']==231
    assert data['independent_controls']['result']['native_relative_cases']==40 and data['independent_controls']['result']['normal_seeded_ends']==25
    assert data['independent_references']['canonical_source_withfull_current_ROM_positive'] and data['independent_references']['references']['whole_reference_ROM_equal']
    assert data['predecessor_compatibility']['all506_prior_dependencies_preserved'] and data['predecessor_compatibility']['new_builder_guard_rejections']==16 and len(data['predecessor_compatibility']['actual_changed_oldconfig_rejections'])==4
    for key in ['independent_native','independent_actual','independent_FE','independent_menu','independent_comparison','independent_controls','independent_references']:
        for path,digest in data[key]['evidence'].items():assert sha(Path(path).read_bytes())==digest
    parent,reference=NdsImage.open(PARENT),NdsImage.open(ROM);parent_sha,reference_sha=sha(PARENT.read_bytes()),sha(ROM.read_bytes())
    assert parent_sha==doc['current_ROM_sha256']==data['reference']['parent_sha256'] and reference_sha==doc['reference_ROM_sha256']==data['reference']['research_ROM_sha256']
    assert data['reference']['all324_otherSC1_blocks_andall_other_files_components_exact'] and data['reference']['complete_parent_ROM_inverse_byte_exact']
    assert data['policy_validation']['negative_count']==838 and data['format_approval']['all16_five_gates_true']
    scope=observed_scope(data);assert scope['complete_page_occurrences']==34 and scope['complete_body_name_orabsent_FE_header_holds']==200 and scope['total_actual_frames']==69868
    correction=Path('translations/gerhard_surname_editorial_release_v2.json')
    dependency=dict(predecessor_profile='all-routes-unified-v8377',predecessor_ROM=str(PARENT),predecessor_ROM_sha256=parent_sha,correction=str(correction),correction_sha256=sha(correction.read_bytes()),name_span=data['Gerhard_reference']['only_changed_name_span'])
    records=[dict(id=r['id'],source_reference=r['source_reference'],current_reference=r['current_reference'],final_reference=r['final_reference'],source_hex=r['source_hex'],current_hex=r['current_hex'],final_hex=r['final_hex']) for r in doc['records']+doc['typed_choice_records']]
    ROOT.mkdir(parents=True);save(SEAL,dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),name_review_sha256=sha(NAMES.read_bytes()),parent=str(PARENT),parent_sha256=parent_sha,reference=str(ROM),reference_sha256=reference_sha,records=records,observed_scope=scope,required_registered_Gerhard_dependency=dependency,all16_source_current_final_references_andwhole_image_inverses_independently_verified=True,all_independent_native_actual_menu_FE_controls_loaders_andcomparison_readers_pass=True,prior_stage_exact_output_andall_prior_dependencies_preserved=True,atomic_semantic_tests_registered_cumulative_build_clean_patch_andstartup_pending=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(Path(p).read_bytes()) for p in [Path(__file__),*map(Path,proofs().values())]}))
    deps=dict(frozen['dependencies']);previous=read('translations/hodram_outcomes_editorial_release_v4.json')
    for path,digest in previous['dependencies'].items():
        assert path not in deps or deps[path]==digest;deps[path]=digest
    paths={DOC,NAMES,SEAL,Path(__file__),Path(owned.__file__),Path('scripts/Hodram_B49_release_paths_v8447.py'),Path('translations/hodram_outcomes_editorial_release_v4.json'),Path('translations/hodram_B49_native_contract_v2.json'),*map(Path,proofs().values())}
    root=Path.cwd().resolve()
    for module in tuple(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename and filename.endswith('.py'):
            path=Path(filename)
            if path.resolve().is_relative_to(root):paths.add(path)
    for path in paths:
        p=str(path.resolve());h=sha(path.read_bytes());assert p not in deps or deps[p]==h;deps[p]=h
    conf=dict(format='dk4-Hodram-B49-editorial-release-v1',manuscripts=[str(DOC)],proofs=proofs(),parent_ROM=str(PARENT),parent_ROM_sha256=parent_sha,reference_ROM=str(ROM),reference_ROM_sha256=reference_sha,canonical_ROM=str(owned.CANONICAL),canonical_ROM_sha256=sha(owned.CANONICAL.read_bytes()),clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),reference_approval=str(SEAL),predecessor_file_hashes={p:sha(v) for _,p,v in parent.iter_files()},predecessor_component_hashes={p:sha(v) for p,v in parent.iter_components()},required_registered_Gerhard_dependency=dependency,archives=[dict(file_path=owned.PATH,source_sha256=sha(parent.read_file(owned.PATH)),target_sha256=sha(reference.read_file(owned.PATH)))],components=[],dependencies=deps)
    save(CONFIG,conf);owned.check_dependencies(conf)
    save(ROOT/'configuration_receipt.json',dict(configuration=str(CONFIG),configuration_sha256=sha(CONFIG.read_bytes()),dependencies=len(deps),all445_frozen_B49_and515_compatible_predecessor_dependencies_preserved=True,atomic_module=str(Path(owned.__file__)),atomic_module_sha256=sha(Path(owned.__file__).read_bytes()),reference_seal_sha256=sha(SEAL.read_bytes()),no_builder_registry_ROM_orcompletion_credit_change=True,new_credit=0,full_goal_complete=False))
    print('Sealed16 B49 references andall independentreaders;production dependencies pinned. Atomic positive/semantic challenges/registered build stillpending.No ROM orcredit.')
