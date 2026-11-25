"""Seal exact B50 references after full reversible speech-only reconstruction."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.rafael_B50_profile_v1 import validate_approved_batch
from scripts.source_locked_derivation_v5118 import derive
from scripts.Rafael_B50_release_paths_v8164 import PARENT,ROM,DRAFT,APPROVED,MAP,SEAL,RELOCATION,FLAGS,proofs
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Rafael_B50_reference_tools_v8164')
HELPER=Path('dk4tool/patch/rafael_B50_reconstruction_v1.py')

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
    result=derive('dk4tool/patch/rafael_B45_reconstruction_v1.py',str(HELPER),{'B45':'B50'})
    from dk4tool.patch.rafael_B50_reconstruction_v1 import reconstruct
    doc=read(DRAFT);validate_approved_batch(doc)
    mapping=read(RELOCATION);p=proofs();data={k:read(path) for k,path in p.items()}
    current,policy,approval,actual,later,branches=[data[k] for k in [
        'source_context','native_policy_validation','actual_approval','actual_proof','later_scope_proof','source_branch_proof']]
    assert approval['manuscript_sha256']==sha(DRAFT.read_bytes()) and policy['positive_count']==28 and policy['negative_count']==511
    assert not actual['unresolved'] and len(actual['groups'])==2
    assert data['native_loader_proof']['fresh_native_whole_loads_andcache_hits']==343
    assert data['native_loader_proof']['fresh_initial_parent_modes']==686
    assert sha(PARENT.read_bytes())==mapping['candidate_sha256']==current['current_ROM_sha256']
    parent,reference,clean=[NdsImage.open(path) for path in [PARENT,ROM,'work/clean.nds']]
    oldbank,newbank,cleanbank=[IlnkContainer.parse(im.read_file('/data/SC0.DK4')).blocks for im in [parent,reference,clean]]
    group=deepcopy(mapping['groups'][0]);assert group['block']==50
    target=reconstruct(oldbank[50],cleanbank[50],group,current['groups'][0],doc['records'],branches['operands_requiring_adjustment_when_resizing'])
    assert target==newbank[50] and len(target)==1376
    assert [i for i,(a,b) in enumerate(zip(oldbank,newbank,strict=True)) if a!=b]==[50] and len(oldbank)==343
    restored=list(newbank);restored[50]=oldbank[50]
    assert IlnkContainer(restored).to_bytes()==parent.read_file('/data/SC0.DK4')
    assert [path for _,path,v in parent.iter_files() if reference.read_file(path)!=v]==['/data/SC0.DK4']
    assert all(reference.read_file(path)==v for path,v in parent.iter_components())
    assert data['native_caller_proof']['all_command_maps']==group['command_map']
    assert data['native_caller_proof']['relative_operand_maps']==group['relative_fixups']
    group.update(route=0,route_identity='Rafael',external_references_complete=True,original_entry_payload_offset=8,
        source_archive_sha256=sha(parent.read_file('/data/SC0.DK4')),target_archive_sha256=sha(reference.read_file('/data/SC0.DK4')),
        approved_manuscript=str(DRAFT),approved_manuscript_sha256=sha(DRAFT.read_bytes()))
    evidence={str(path):sha(path.read_bytes()) for path in [
        DRAFT,RELOCATION,*map(Path,p.values()),HELPER,Path(__file__),Path('scripts/Rafael_B50_release_paths_v8164.py')]}
    save(MAP,dict(format='dk4-Rafael28-B50-source-relocation-map-v1',source_ROM=str(PARENT),source_ROM_sha256=sha(PARENT.read_bytes()),
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),file_path='/data/SC0.DK4',
        source_archive_sha256=group['source_archive_sha256'],target_archive_sha256=group['target_archive_sha256'],
        groups=[group],preserve_record_parity=True,observed_comparison_contract=summary(later['groups'][0]),
        evidence=evidence,**{k:True for k in FLAGS},new_credit=0,full_goal_complete=False))
    successor=deepcopy(doc)
    for row in successor['records']:
        positive=next(r for r in policy['positives'] if r['id']==row['id'])
        ref=next(r for r in group['text_records'] if r['id']==row['id'])
        row.update(base_QA_report=positive['qa'],
            target_reference=dict(block=50,offset=ref['new_offset'],bytes=ref['new_length'],header_offset=ref['new_offset']-5,record_index=ref['new_record_index']),
            stored_target_hex=ref['target_hex'],stored_parity_space=ref['parity_space_added'])
        assert row['qa_waivers']==next(r for r in doc['records'] if r['id']==row['id'])['qa_waivers']
    successor.update(native_approved_manuscript=str(DRAFT),native_approved_manuscript_sha256=sha(DRAFT.read_bytes()),
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),reference_approval=str(SEAL),
        reference_research_ROM=str(ROM),reference_research_ROM_sha256=sha(ROM.read_bytes()),
        status='twenty-eight exact source/context/prose/native andall actual decisions sealed;atomic registered integration pending')
    validate_approved_batch(successor)
    save(APPROVED,successor);SEAL.parent.mkdir(parents=True)
    save(SEAL,dict(manuscript=str(APPROVED),manuscript_sha256=sha(APPROVED.read_bytes()),
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),
        all28_five_gates_andexact_references_approved=True,all37_commands_zero_relative_predicate_query_sites_source_bound=True,
        complete_clean_predecessor_blocks_andwhole_archive_inverse_exact=True,
        all28_single_pages_two_exact_warning_exceptions18_infos_unchanged=True,
        all28_actual_speeches_andthree_headers_explicit=True,
        observed_comparison_contract=summary(later['groups'][0]),all_measured_limits_preserved=True,
        evidence=evidence,helper_derivation=result,atomic_production_andregistered_release_pending=True,
        new_credit=0,full_goal_complete=False))
    ROOT.mkdir(parents=True)
    save(ROOT/'reference_seal_receipt.json',dict(seal=str(SEAL),seal_sha256=sha(SEAL.read_bytes()),
        manuscript=str(APPROVED),manuscript_sha256=sha(APPROVED.read_bytes()),
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        helper_derivation=result,all28_records_exact=True,atomic_production_andregistered_release_pending=True,
        no_ROM_registry_orcredit_change=True,new_credit=0,full_goal_complete=False))
    print('B50 references sealed:28 exact records/37commands/zero relative sites,full block/archive inverses. Single-page/two-warning scopes unchanged. Atomic integration pending.')
