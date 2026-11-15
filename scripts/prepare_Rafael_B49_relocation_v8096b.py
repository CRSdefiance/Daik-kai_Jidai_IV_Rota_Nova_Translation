"""Bind56 source/current relative operands andprepare exact reversible61-speech research reconstruction."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_archive_tools_v8096')
CURRENT=Path('work/analysis/Rafael_B49_current_v8086/all61_complete_source_current_refs_before_new_English_manuscript.json')
CONTROL=Path('work/analysis/Rafael_B49_source_controls_v8081/source_EV0_56_relative_sites280_cases13_raw_predicates1_query25_seeded_ends.json')
BRANCH=ROOT/'56_exact_source_current_relative_operands_bound_to280_native_cases.json'
if __name__=='__main__':
    assert not ROOT.exists();current,control=map(read,[CURRENT,CONTROL]);g=current['groups'][0];block=bytes.fromhex(g['current_block_hex'])
    assert g['block']==49 and len(block)==3976;operands=[]
    for edge,case in zip(control['operands_requiring_adjustment_when_resizing'],control['source_relative_cases'],strict=True):
        at=edge['offset'];raw=block[at:at+4].hex();assert raw==edge['source_operand_hex'] and case['offset']==at and len(case['cases'])==5
        c=next(c for c in g['all_current_commands'] if c['offset']==at);assert c['word']==edge['word'] and c['ancestor_0100_offsets']==edge['ancestor_0100_offsets']
        assert at+4 in {c['offset'] for c in g['all_current_commands']} and edge['matched_skip_target'] in {c['offset'] for c in g['all_current_commands']}
        operands.append(dict(**edge,current_operand_hex=raw))
    assert len(operands)==56 and len(g['all_current_commands'])==154
    result=derive('scripts/relocate_Rafael_B48_v8041.py','scripts/relocate_Rafael_B49_v8096.py',{
        'B48':'B49','Rafael_B48_relocation_v8041':'Rafael_B49_relocation_v8096',
        'Rafael_B48_current_v8028/all91_complete_source_current_refs':'Rafael_B49_current_v8086/all61_complete_source_current_refs',
        'Rafael_next_clean_v8020':'Rafael_next_clean_v8073',
        'rafael_B48_editorial_manuscript_v3':'rafael_B49_editorial_manuscript_v2',
        'Rafael_B48_layout_v8035d/91_automatic_plans_full_native_width_source_preambles4_FE.json':'Rafael_B49_layout_v8090c/61_automatic_plans_full_native_width_exact_source00_02_09_no_FE.json',
        'Rafael_B48_native_review_v8040/91_paragraphs92_native_pages9_names_two_scoped_warnings37_infos_wrap_review.json':'Rafael_B49_native_review_v8095/61_native_pages7_names_three_scoped_warnings22_infos_wrap_review.json',
        'Rafael_B48_archive_tools_v8041/28_exact_source_current_relative_operands_bound_to140_native_cases.json':BRANCH.as_posix().removeprefix('work/analysis/'),
        'current_V8013_Rafael_native_v8016':'current_V8066_Rafael_native_v8069',
        "row['source_record_index'] in [86,406]":"row['source_record_index'] in [213,244,405]",
        "sum(len(g['text_records']) for g in groups)==91 and sum(len(g['relative_fixups']) for g in groups)==28":"sum(len(g['text_records']) for g in groups)==61 and sum(len(g['relative_fixups']) for g in groups)==56",
        '==[48]':'==[49]','one_block91_speeches28_relative_fixups140_cases':'one_block61_speeches56_relative_fixups280_cases',
        'source_relative_sites=28,relocated_native_skip_cases=140':'source_relative_sites=56,relocated_native_skip_cases=280',
        'all15_six_byte_preambles_zero_macros_selectors_complete_terminal_andseparate_tails_preserved':'all61_six_byte_preambles_twoFI_macros_selectors_complete_terminal_andseparate_tails_preserved',
        'source_UI_effects_waits_A000_C200_wholecontrols':'source_UI_effects_waits_seven_A000_C281_wholecontrols',
        '91speeches/28relative sites/140guarded cases':'61speeches/56relative sites/280guarded cases',
        '28nested fixups,91complete preambles,92reviewed pages':'56nested fixups,61complete preambles,61reviewed pages',
    })
    ROOT.mkdir(parents=True)
    save(BRANCH,dict(candidate=current['current_ROM'],candidate_sha256=current['current_ROM_sha256'],source_context=str(CURRENT),source_context_sha256=sha(CURRENT.read_bytes()),
        source_control_proof=str(CONTROL),source_control_proof_sha256=sha(CONTROL.read_bytes()),operands_requiring_adjustment_when_resizing=operands,
        all56_source_current_fourbyte_operands_offsets_ancestors_alignment_runtime_equal=True,
        original280_structural_source_cases_reused_by_exact_operand_andnative_read_scope_not_new_current_replays=True,
        source_control_cases=control['source_relative_cases'],source_English_opaque_speech_bytes_not_executed_by_relative_primitive=True,
        source_locked_reconstruction_derivation=result,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('56exact source/current operands bound to280source native cases;B49research reconstruction prepared. No ROM orcredit.')
