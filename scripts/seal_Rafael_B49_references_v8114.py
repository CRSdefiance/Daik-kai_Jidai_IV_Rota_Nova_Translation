"""Seal exact B49 references after full reversible speech-only reconstruction."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.rafael_B49_profile_v1 import validate_approved_batch
from scripts.source_locked_derivation_v5118 import derive
from scripts.Rafael_B49_release_paths_v8114 import PARENT,ROM,DRAFT,APPROVED,MAP,SEAL,RELOCATION,FLAGS,proofs
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Rafael_B49_reference_tools_v8114')
HELPER=Path('dk4tool/patch/rafael_B49_reconstruction_v1.py')

def summary(group):
    return dict(source_English_exits=group['source_English_exits'],
        command_difference_rows=len(group['command_comparison_differences']),
        duration_difference_rows=len(group['duration_differences']),
        later_RGB_differences=len(group['later_RGB_differences']),later_samples=group['later_sample_count'],
        five_component_equality=group['five_native_component_equality'],whole_actor_equality=group['whole_actors_equal'],
        final_PRNG_seeds=group['final_PRNG_seeds'],
        raw_calendars_no_invented_date_interpretation=group['raw_calendars_no_invented_date_interpretation'])

if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [APPROVED,MAP,SEAL,HELPER])
    result=derive('dk4tool/patch/rafael_B45_reconstruction_v1.py',str(HELPER),{'B45':'B49'})
    from dk4tool.patch.rafael_B49_reconstruction_v1 import reconstruct
    doc=read(DRAFT);validate_approved_batch(doc)
    mapping=read(RELOCATION);p=proofs();data={k:read(path) for k,path in p.items()}
    current,policy,approval,actual,later,branches=[data[k] for k in [
        'source_context','native_policy_validation','actual_approval','actual_proof','later_scope_proof','source_branch_proof']]
    assert approval['manuscript_sha256']==sha(DRAFT.read_bytes()) and policy['positive_count']==61 and policy['negative_count']==1014
    assert not actual['unresolved'] and len(actual['groups'])==2
    assert data['native_loader_proof']['fresh_native_whole_loads_andcache_hits']==343
    assert data['native_loader_proof']['fresh_initial_parent_modes']==686
    assert sha(PARENT.read_bytes())==mapping['candidate_sha256']==current['current_ROM_sha256']
    parent,reference,clean=[NdsImage.open(path) for path in [PARENT,ROM,'work/clean.nds']]
    oldbank,newbank,cleanbank=[IlnkContainer.parse(im.read_file('/data/SC0.DK4')).blocks for im in [parent,reference,clean]]
    group=deepcopy(mapping['groups'][0]);assert group['block']==49
    target=reconstruct(oldbank[49],cleanbank[49],group,current['groups'][0],doc['records'],branches['operands_requiring_adjustment_when_resizing'])
    assert target==newbank[49] and len(target)==3792
    assert [i for i,(a,b) in enumerate(zip(oldbank,newbank,strict=True)) if a!=b]==[49] and len(oldbank)==343
    restored=list(newbank);restored[49]=oldbank[49]
    assert IlnkContainer(restored).to_bytes()==parent.read_file('/data/SC0.DK4')
    assert [path for _,path,v in parent.iter_files() if reference.read_file(path)!=v]==['/data/SC0.DK4']
    assert all(reference.read_file(path)==v for path,v in parent.iter_components())
    assert data['native_caller_proof']['all_command_maps']==group['command_map']
    assert data['native_caller_proof']['relative_operand_maps']==group['relative_fixups']
    group.update(route=0,route_identity='Rafael',external_references_complete=True,original_entry_payload_offset=8,
        source_archive_sha256=sha(parent.read_file('/data/SC0.DK4')),target_archive_sha256=sha(reference.read_file('/data/SC0.DK4')),
        approved_manuscript=str(DRAFT),approved_manuscript_sha256=sha(DRAFT.read_bytes()))
    evidence={str(path):sha(path.read_bytes()) for path in [
        DRAFT,RELOCATION,*map(Path,p.values()),HELPER,Path(__file__),Path('scripts/Rafael_B49_release_paths_v8114.py')]}
    save(MAP,dict(format='dk4-Rafael61-B49-source-relocation-map-v1',source_ROM=str(PARENT),source_ROM_sha256=sha(PARENT.read_bytes()),
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),file_path='/data/SC0.DK4',
        source_archive_sha256=group['source_archive_sha256'],target_archive_sha256=group['target_archive_sha256'],
        groups=[group],preserve_record_parity=True,observed_comparison_contract=summary(later['groups'][0]),
        evidence=evidence,**{k:True for k in FLAGS},new_credit=0,full_goal_complete=False))
    successor=deepcopy(doc)
    for row in successor['records']:
        positive=next(r for r in policy['positives'] if r['id']==row['id'])
        ref=next(r for r in group['text_records'] if r['id']==row['id'])
        row.update(base_QA_report=positive['qa'],
            target_reference=dict(block=49,offset=ref['new_offset'],bytes=ref['new_length'],header_offset=ref['new_offset']-5,record_index=ref['new_record_index']),
            stored_target_hex=ref['target_hex'],stored_parity_space=ref['parity_space_added'])
        assert row['qa_waivers']==next(r for r in doc['records'] if r['id']==row['id'])['qa_waivers']
    successor.update(native_approved_manuscript=str(DRAFT),native_approved_manuscript_sha256=sha(DRAFT.read_bytes()),
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),reference_approval=str(SEAL),
        reference_research_ROM=str(ROM),reference_research_ROM_sha256=sha(ROM.read_bytes()),
        status='sixty-one exact source/context/prose/native andrepresentative actual decisions sealed;atomic registered integration pending')
    validate_approved_batch(successor)
    save(APPROVED,successor);SEAL.parent.mkdir(parents=True)
    save(SEAL,dict(manuscript=str(APPROVED),manuscript_sha256=sha(APPROVED.read_bytes()),
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),
        all61_five_gates_andexact_references_approved=True,all154_commands56_relative_sites280_cases_source_bound=True,
        complete_clean_predecessor_blocks_andwhole_archive_inverse_exact=True,
        all61_single_pages_three_exact_warning_exceptions22_infos_unchanged=True,
        eleven_native_only_speeches_andthree_headers_explicit=True,
        observed_comparison_contract=summary(later['groups'][0]),all_measured_limits_preserved=True,
        evidence=evidence,helper_derivation=result,atomic_production_andregistered_release_pending=True,
        new_credit=0,full_goal_complete=False))
    ROOT.mkdir(parents=True)
    save(ROOT/'reference_seal_receipt.json',dict(seal=str(SEAL),seal_sha256=sha(SEAL.read_bytes()),
        manuscript=str(APPROVED),manuscript_sha256=sha(APPROVED.read_bytes()),
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        helper_derivation=result,all61_records_exact=True,atomic_production_andregistered_release_pending=True,
        no_ROM_registry_orcredit_change=True,new_credit=0,full_goal_complete=False))
    print('B49 references sealed:61 exact records/154commands/56fixups,full block/archive inverses. Single-page/three-warning scopes unchanged. Atomic integration pending.')
