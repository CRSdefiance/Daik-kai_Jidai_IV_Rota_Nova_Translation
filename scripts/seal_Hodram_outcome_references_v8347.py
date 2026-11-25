"""Seal independently reconstructed whole-ROM equality and complete six-record source/current/final map."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_outcomes_profile_v1 import contract,validate_approved_batch,validate_runtime
from dk4tool.dialogue.hodram_outcomes_names_v1 import validate_scoped_names
from dk4tool.patch.hodram_outcome_references_v1 import reconstruct_and_bind,serializable_groups
from scripts.Hodram_outcomes_release_paths_v8347 import PARENT,ROM,DOC,NAMES,MAP,SEAL,proofs,observed_scope
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    assert not MAP.exists() and not SEAL.parent.exists();data={k:read(p) for k,p in proofs().items()};doc=read(DOC);names=read(NAMES);frozen=contract();validate_approved_batch(doc);validate_scoped_names(names)
    assert data['native_contract']==frozen and data['source_final_binding']['manuscript_sha256']==sha(DOC.read_bytes()) and data['source_final_binding']['name_review_sha256']==sha(NAMES.read_bytes())
    parent,clean,reference=[NdsImage.open(p) for p in [PARENT,Path('work/clean.nds'),ROM]];validate_runtime(parent)
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==data['reference']['parent_sha256'] and sha(ROM.read_bytes())==data['reference']['research_ROM_sha256']
    policy=data['policy_validation'];assert policy['positive_count']==6 and policy['negative_count']==len(policy['negatives'])==357 and all(n['rejected'] and n['actual_changed_input'] for n in policy['negatives'])
    result=reconstruct_and_bind(parent,clean,doc,data['relocation'],data['current']);assert serializable_groups(result)==data['independent_rebuild']['groups']
    planned=deepcopy(parent);planned.replace_file(doc['file_path'],result['target_archive']);assert bytes(planned.rom.save())==ROM.read_bytes()
    inverse=deepcopy(planned);inverse.replace_file(doc['file_path'],parent.read_file(doc['file_path']));assert bytes(inverse.rom.save())==PARENT.read_bytes()
    assert data['callers']['external_references_complete'] and data['callers']['all15_source_current_target_commands_zero_relative_sites6_complete_preambles_bound']
    records=[]
    for row in doc['records']:
        group=next(g for g in result['groups'] if g['block']==row['block']);ref=next(r for r in group['text_records'] if r['id']==row['id'])
        records.append(dict(id=row['id'],file_path=doc['file_path'],block=row['block'],source_reference=row['source_reference'],current_reference=row['current_reference'],
            target_reference=dict(file_path=doc['file_path'],block=row['block'],offset=ref['new_offset'],bytes=ref['new_length'],header_offset=ref['new_offset']-5,record_index=ref['new_record_index'],target_block_sha256=group['target_block_sha256']),
            source_hex=row['source_hex'],current_hex=row['current_hex'],compiled_hex=ref['compiled_hex'],stored_hex=ref['target_hex'],consumer=frozen['record_bindings'][row['id']]['consumer']))
    scope=observed_scope(data);assert scope['actual_whole_scene_frames']==40004 and scope['focused_FE_frames']==8002 and scope['complete_body_name_orFE_absent_header_holds']==100
    evidence={str(p):sha(Path(p).read_bytes()) for p in [*proofs().values(),Path(__file__),Path('scripts/Hodram_outcomes_release_paths_v8347.py'),Path('dk4tool/patch/hodram_outcome_rebuild_v1.py'),Path('dk4tool/patch/hodram_outcome_references_v1.py')]}
    SEAL.parent.mkdir(parents=True);save(MAP,dict(format='dk4-Hodram-outcomes-native-relocation-v1',file_path=doc['file_path'],source_ROM=str(PARENT),source_ROM_sha256=sha(PARENT.read_bytes()),reference_ROM=str(ROM),reference_ROM_sha256=sha(ROM.read_bytes()),
        source_archive_sha256=sha(parent.read_file(doc['file_path'])),target_archive_sha256=sha(result['target_archive']),groups=serializable_groups(result),records=records,
        every_clean_source_block_predecessor_archive_andwhole_ROM_inverse_exact=True,all15commands6sixbyte_preambles_zero_relatives_one_FE_one_FI_source_current_target_bound=True,
        external_references_complete=True,source_reference_scope_not_arbitrary_dynamic_pointer_orall_attainable_paths_proof=True,observed_scope=scope,new_credit=0,full_goal_complete=False,evidence=evidence))
    save(SEAL,dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),name_review=str(NAMES),name_review_sha256=sha(NAMES.read_bytes()),
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),independent_entire_ROM_equal_tested_reference=True,all_clean_source_blocks_full_parent_archive_andROM_inverse_exact=True,
        records=6,commands=15,original_source_FE=1,original_source_FI=1,all323_unowned_blocks_all_other_files_andcomponents_exact=True,observed_scope=scope,
        independent_actual_semantic_validation_atomic_challenges_andregistered_integration_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence=evidence))
    print('Sealed6refs/15commands/2clean inverses/323unownedblocks:entire plannedROM equals testedreference.Pinned357policy rejections;actualscope includingB48differences retained.Independent actual/atomic/release next.')
