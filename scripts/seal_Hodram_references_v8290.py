"""Seal the independently reconstructed archive/full ROM and exact source-qualified records."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_three_blocks_profile_v1 import validate_approved_batch,validate_runtime
from dk4tool.patch.hodram_three_blocks_references_v1 import reconstruct_and_bind,serializable_groups
from scripts.Hodram_three_blocks_release_paths_v8290 import PARENT,ROM,DOC,NAMES,MAP,SEAL,proofs,observed_scope
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_reference_tools_v8290')
if __name__=='__main__':
    assert not ROOT.exists() and not MAP.exists() and not SEAL.exists()
    doc=read(DOC);validate_approved_batch(doc);paths=proofs();data={k:read(p) for k,p in paths.items()}
    policy=data['policy_validation'];assert policy['positive_count']==28 and policy['negative_count']==579
    assert all(n['rejected'] for n in policy['negatives']) and len(policy['negatives'])==579
    assert data['display_approval']['all28_five_per_record_gates_true'] and data['native_caller']['external_references_complete']
    assert data['native_loader']['fresh_native_whole_loads_andcache_hits']==325 and data['native_loader']['fresh_initial_parent_modes']==650
    image=NdsImage.open(PARENT);reference=NdsImage.open(ROM);clean=NdsImage.open('work/clean.nds');validate_runtime(image);validate_runtime(reference)
    assert sha(PARENT.read_bytes())==data['reference']['parent_sha256']==doc['current_ROM_sha256']
    assert sha(ROM.read_bytes())==data['reference']['research_ROM_sha256'] and sha(Path('work/clean.nds').read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    result=reconstruct_and_bind(image,clean,doc,data['relocation'],data['current'])
    assert result['target_archive']==reference.read_file(doc['file_path'])
    planned=deepcopy(image);planned.replace_file(doc['file_path'],result['target_archive'])
    assert bytes(planned.rom.save())==ROM.read_bytes() and [p for _,p,v in image.iter_files() if planned.read_file(p)!=v]==[doc['file_path']]
    assert all(planned.read_file(p)==v for p,v in image.iter_components())
    restored=deepcopy(planned);restored.replace_file(doc['file_path'],image.read_file(doc['file_path']));assert bytes(restored.rom.save())==PARENT.read_bytes()
    target=IlnkContainer.parse(result['target_archive']).blocks;refs=[]
    for group in result['groups']:
        for r in group['text_records']:
            row=next(x for x in doc['records'] if x['id']==r['id'])
            refs.append(dict(id=r['id'],file_path=doc['file_path'],block=group['block'],source_reference=row['source_reference'],current_reference=row['current_reference'],
                target_reference=dict(file_path=doc['file_path'],block=group['block'],offset=r['new_offset'],bytes=r['new_length'],header_offset=r['new_offset']-5,
                    record_index=r['new_record_index'],target_block_sha256=sha(target[group['block']])),source_hex=row['source_hex'],previous_hex=row['current_hex'],
                compiled_hex=row['compiled_hex'],stored_hex=r['target_hex'],source_complete_preamble_hex=row['source_complete_preamble_hex'],source_selector=row['source_selector'],
                editorial_decision=row['decision'],retention_reason=row['retention_reason'],review=row['review']))
    assert len(refs)==28 and sum(len(g['relative_fixups']) for g in result['groups'])==8
    scope=observed_scope(data)
    evidence={str(p):sha(Path(p).read_bytes()) for p in [DOC,NAMES,Path(__file__),Path('scripts/Hodram_three_blocks_release_paths_v8290.py'),
        Path('dk4tool/patch/hodram_three_blocks_rebuild_v1.py'),Path('dk4tool/patch/hodram_three_blocks_references_v1.py'),*map(Path,paths.values())]}
    save(MAP,dict(format='Hodram-three-blocks-independent-relocation-map-v1',source_ROM=str(PARENT),source_ROM_sha256=sha(PARENT.read_bytes()),
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),file_path=doc['file_path'],
        source_archive_sha256=sha(image.read_file(doc['file_path'])),target_archive_sha256=sha(result['target_archive']),
        groups=serializable_groups(result),records=refs,observed_scope=scope,external_references_complete=True,
        all60commands28sixbyte_preambles8relatives_source_current_target_bound=True,
        every_clean_source_block_predecessor_archive_andwhole_ROM_inverse_exact=True,
        only_blocks45_46_137_change_all322_other_blocks_andall_other_files_components_exact=True,
        registered_Adernkatz_dependency_bound_to_exact_parent_ARM9=True,all_individual_reasons_source_refs_native_andactual_scope_preserved=True,
        independent_actual_evidence_validation_atomic_production_registered_release_pending=True,new_credit=0,full_goal_complete=False,evidence=evidence))
    SEAL.parent.mkdir(parents=True);save(SEAL,dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),name_review=str(NAMES),name_review_sha256=sha(NAMES.read_bytes()),
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),
        research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),independent_entire_ROM_equal_tested_reference=True,
        all28_source_current_final_refs_andthree_clean_source_block_inverses_exact=True,
        all60commands8relatives322_unowned_blocks_all_other_files_components_preserved=True,observed_scope=scope,
        policy_positives=28,policy_expected_rejections=579,independent_actual_atomic_production_registered_release_pending=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence=evidence))
    ROOT.mkdir(parents=True);save(ROOT/'independent_reference_seal_receipt.json',dict(seal=str(SEAL),seal_sha256=sha(SEAL.read_bytes()),
        map=str(MAP),map_sha256=sha(MAP.read_bytes()),no_ROM_registry_ledger_pin_orcredit_change=True,new_credit=0,full_goal_complete=False))
    print('Independent Hodram seal:whole ROM equals tested8276 reference;all28 refs/60commands/8relatives/threeclean inverses/fullparent inverse pass. Atomic release pending.')
