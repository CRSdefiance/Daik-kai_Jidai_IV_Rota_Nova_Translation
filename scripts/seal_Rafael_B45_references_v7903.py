"""Seal all twelve exact references and the complete source-owned reversible B45 reconstruction."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.Rafael_B45_release_paths_v7903 import PARENT,ROM,DRAFT,APPROVED,MAP,SEAL,RELOCATION,FLAGS,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_reference_tools_v7903')
HELPER=Path('dk4tool/patch/rafael_B45_reconstruction_v1.py')
def summary(group):
    return dict(source_English_exits=group['source_English_exits'],command_difference_rows=len(group['command_comparison_differences']),
        duration_difference_rows=len(group['duration_differences']),later_RGB_differences=len(group['later_RGB_differences']),
        later_samples=group['later_sample_count'],five_component_equality=group['five_native_component_equality'],
        whole_actor_equality=group['whole_actors_equal'],final_PRNG_seeds=group['final_PRNG_seeds'])
if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [APPROVED,MAP,SEAL,HELPER])
    result=derive('dk4tool/patch/retrospective_SC2_reconstruction_v2.py',str(HELPER),{
        'Retrospective SC2 reconstruction: ':'Rafael B45 reconstruction: ',
        "group['file_path']=='/data/SC2.DK4'":"group['file_path']=='/data/SC0.DK4'",
        "value.hex()==ref['compiled_hex'] and b'\\0' not in value":
        "value.hex()==ref['compiled_hex'] and b'\\0' not in value[1:]",
    })
    from dk4tool.patch.rafael_B45_reconstruction_v1 import reconstruct
    doc=read(DRAFT);mapping=read(RELOCATION);p=proofs();data={k:read(path) for k,path in p.items()}
    current,policy,approval,actual,later,branches=data['source_context'],data['native_policy_validation'],data['actual_approval'],data['actual_proof'],data['later_scope_proof'],data['source_branch_proof']
    assert approval['manuscript_sha256']==sha(DRAFT.read_bytes()) and policy['positive_count']==12 and policy['negative_count']==159
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness','formatting']) for r in doc['records'])
    assert not actual['unresolved'] and data['native_loader_proof']['fresh_native_whole_loads_andcache_hits']==343
    assert data['native_loader_proof']['fresh_initial_parent_modes']==686 and data['native_caller_proof']['only_original24070_interpreter_call_no_literal_alias']
    assert sha(PARENT.read_bytes())==mapping['candidate_sha256']==current['current_ROM_sha256']
    parent,reference,clean=[NdsImage.open(path) for path in [PARENT,ROM,'work/clean.nds']]
    oldbank,newbank,cleanbank=[IlnkContainer.parse(im.read_file('/data/SC0.DK4')).blocks for im in [parent,reference,clean]]
    group=deepcopy(mapping['groups'][0]);assert group['block']==45
    target=reconstruct(oldbank[45],cleanbank[45],group,current['groups'][0],doc['records'],branches['operands_requiring_adjustment_when_resizing'])
    assert target==newbank[45]
    assert [i for i,(a,b) in enumerate(zip(oldbank,newbank,strict=True)) if a!=b]==[45] and len(oldbank)==343
    restored=list(newbank);restored[45]=oldbank[45]
    assert IlnkContainer(restored).to_bytes()==parent.read_file('/data/SC0.DK4')
    assert [path for _,path,v in parent.iter_files() if reference.read_file(path)!=v]==['/data/SC0.DK4']
    assert all(reference.read_file(path)==v for path,v in parent.iter_components())
    assert data['native_caller_proof']['all_command_maps']==group['command_map'] and data['native_caller_proof']['relative_operand_maps']==group['relative_fixups']
    group.update(route=0,route_identity='Rafael',external_references_complete=True,original_entry_payload_offset=8,
        source_archive_sha256=sha(parent.read_file('/data/SC0.DK4')),target_archive_sha256=sha(reference.read_file('/data/SC0.DK4')),
        approved_manuscript=str(DRAFT),approved_manuscript_sha256=sha(DRAFT.read_bytes()))
    evidence={str(path):sha(path.read_bytes()) for path in [DRAFT,RELOCATION,*map(Path,p.values()),HELPER,Path(__file__),
        Path('scripts/Rafael_B45_release_paths_v7903.py')]}
    save(MAP,dict(format='dk4-Rafael12-B45-source-relocation-map-v1',source_ROM=str(PARENT),source_ROM_sha256=sha(PARENT.read_bytes()),
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),file_path='/data/SC0.DK4',
        source_archive_sha256=group['source_archive_sha256'],target_archive_sha256=group['target_archive_sha256'],
        groups=[group],preserve_record_parity=True,observed_comparison_contract=summary(later['groups'][0]),
        evidence=evidence,**{k:True for k in FLAGS},new_credit=0,full_goal_complete=False))
    successor=deepcopy(doc)
    for row in successor['records']:
        positive=next(r for r in policy['positive_cases'] if r['id']==row['id'])
        ref=next(r for r in group['text_records'] if r['id']==row['id'])
        binding=data['native_contract']['record_bindings'][row['id']]
        row.update(base_QA_report=positive['qa'],qa_waivers=[],qa_waiver_reason=None,native_page_count=1,
            row_count_reason=binding['row_count_reason'],actual_record_observed=True,
            target_reference=dict(block=45,offset=ref['new_offset'],bytes=ref['new_length'],header_offset=ref['new_offset']-5,record_index=ref['new_record_index']),
            stored_target_hex=ref['target_hex'],stored_parity_space=ref['parity_space_added'])
    successor.update(native_approved_manuscript=str(DRAFT),native_approved_manuscript_sha256=sha(DRAFT.read_bytes()),
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),reference_approval=str(SEAL),
        reference_research_ROM=str(ROM),reference_research_ROM_sha256=sha(ROM.read_bytes()),
        status='twelve exact source/context/prose/native/actual decisions sealed;atomic registered integration pending')
    save(APPROVED,successor);SEAL.parent.mkdir(parents=True)
    save(SEAL,dict(manuscript=str(APPROVED),manuscript_sha256=sha(APPROVED.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),
        all12_five_gates_andexact_references_approved=True,all24_commands5_relative_sites25_cases_source_bound=True,
        complete_clean_predecessor_blocks_andwhole_archive_inverse_exact=True,actual12_each_language_no_unplayed_speeches=True,
        measured_RNG_one_step_andall_scope_limits_preserved=True,evidence=evidence,new_credit=0,full_goal_complete=False))
    ROOT.mkdir(parents=True);save(ROOT/'provenance.json',dict(reconstruction_derivation=result,
        source00_only_original_prefix_body_zero_still_forbidden=True,
        all_original_numeric_native_cache_nested_control_extent_andinverse_guards_preserved=True,
        approved=str(APPROVED),approved_sha256=sha(APPROVED.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        no_ROM_registration_orcompletion_credit=True,full_goal_complete=False))
    print('Twelve B45 decisions sealed;24commands/five relative sites25cases,source00/FE,full clean/predecessor inverse and342otherblocks exact.Atomic production pending;zero credit.')
