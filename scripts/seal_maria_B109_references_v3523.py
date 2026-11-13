"""Seal the exact source-owned repair and fully tested relocated objects."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B109_reference_approval_v3523')
INPUT=Path('translations/maria_B109_editorial_manuscript_v9.json')
OUTPUT=Path('translations/maria_B109_editorial_manuscript_v10.json')
MAP=Path('translations/maria_B109_editorial_relocation_map_v1.json')
REFERENCE=Path('work/analysis/maria_B109_references_v3522/B109_source_entry34_commands26_relocated_dispatches_and_C200.json')
APPROVAL=Path('work/analysis/maria_B109_native_approval_v3520/approval_and_production_scope_research_receipt.json')
STORED=Path('work/analysis/maria_B109_stored_target_v3518/all26_stored_objects104_macro_cases14_formatter_guards_and_viewed_sheets.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists() and not MAP.exists();doc=deepcopy(read(INPUT));ref,approval,stored=map(read,[REFERENCE,APPROVAL,STORED]);planpath=Path(approval['plan']);plan=read(planpath)
    assert sha(INPUT.read_bytes())==approval['manuscript_sha256'] and sha(planpath.read_bytes())==approval['plan_sha256']
    assert ref['all303_loader_cache_hits606_parent_modes_each_image'] and ref['all26_stored_targets_reach_expected_original_progressive_consumer'] and ref['C200_source_owned9_writes_and_Maria_index54_preserved']
    assert stored['stored_target_macro_alignment_cases']==104 and len(stored['stored_target_cases'])==26 and len(stored['source_bound_formatter_negatives'])==14
    parent,target,clean,base=[NdsImage.open(p) for p in [approval['parent'],approval['research_ROM'],'work/clean.nds','out/raphael_natural_v2_accepted_base.nds']]
    path='/data/SC3.DK4';a,b,jp=[IlnkContainer.parse(im.read_file(path)).blocks[109] for im in [parent,target,clean]]
    assert b[8:18]==jp[8:18] and a[8:18]!=jp[8:18] and len(b)==1752 and len(a)==1816
    assert sha(b)==plan['target_block_sha256'] and b[:4]==a[:4]==jp[:4]==b'CS\1\1'
    evidence={str(p):sha(p.read_bytes()) for p in [INPUT,REFERENCE,APPROVAL,STORED,planpath,Path(approval['actual_proof']),Path(doc['native_font_proof']),Path(__file__)]}
    mapping=dict(format='dk4-maria-B109-source-relocation-map-v1',file_path=path,block=109,required_runtime_ARM9_sha256=sha(parent.read_file('/__arm9__.bin')),source_SC3_sha256=sha(parent.read_file(path)),target_SC3_sha256=sha(target.read_file(path)),clean_SC3_sha256=sha(clean.read_file(path)),canonical_SC3_sha256=sha(base.read_file(path)),source_block_sha256=sha(a),target_block_sha256=sha(b),clean_block_sha256=sha(jp),entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,text_records=plan['text_records'],mapped_native_commands=plan['mapped_native_commands'],source_owned_control_repair=plan['source_owned_prefix_span'],relative_skip_fixups=[],all34_source_command_boundaries26_complete_preambles8_source_non_speech_commands_verified=True,all26_final_targets104_macro_cases_and_independent_native_planes_verified=True,source_prefix_numeric_not_name_text=True,all302_other_SC3_blocks_every_other_file_component_exact=True,exact_inverse_recovers_predecessor_including_bad_prefix=True,source_EV3_event109_action110_dependency_and_original_loader_bound=True,focused_actual_B109_content_in_B33_entry_fixture_approved=True,source_event109_natural_activation_not_claimed=True,source_English_immediate_normal_Hangzhou_return_equal=True,no_open_translation_specific_display_or_control_finding=True,reference_proof=str(REFERENCE),stored_target_proof=str(STORED),actual_display_proof=approval['actual_proof'],source_plan=str(planpath),target_block=plan['target_block'],evidence=evidence,full_goal_complete=False)
    save(MAP,mapping)
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),reference_map_pending=False,relocated_control_proof=str(REFERENCE),relocated_control_proof_sha256=sha(REFERENCE.read_bytes()),final_padding_proof=str(STORED),final_padding_proof_sha256=sha(STORED.read_bytes()),representative_proof=approval['actual_proof'],representative_proof_sha256=approval['actual_proof_sha256'],registered_integration_pending=True,status='all-editorial-native-reference-and-focused-actual-gates-approved;registered-release-startup-pending')
    for r in doc['records']:r.update(status=doc['status'],native_display_consumer='original_progressive_54020')
    validate_natural_dialogue_batch(doc);save(OUTPUT,doc);ROOT.mkdir(parents=True)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),research_ROM=approval['research_ROM'],research_ROM_sha256=approval['research_ROM_sha256'],all26_source_native_reference_and_focused_display_gates_approved=True,source_prose_English_unchanged=True,existing_V1492_promotion_unchanged=True,registered_release_startup_and_ledger_pending=True,evidence=evidence,no_ledger_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('26 source/native/reference/focused-display reviews sealed; registered cumulative release and fresh startup remain.')
