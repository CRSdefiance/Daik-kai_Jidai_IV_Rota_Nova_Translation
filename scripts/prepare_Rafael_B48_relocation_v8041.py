"""Bind28 exact source/current relative operands andprepare full reversible91-speech reconstruction."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_archive_tools_v8041')
CURRENT=Path('work/analysis/Rafael_B48_current_v8028/all91_complete_source_current_refs_before_new_English_manuscript.json')
CONTROL=Path('work/analysis/Rafael_B48_source_controls_v8024/source_EV0_28_relative_sites140_cases5_raw_predicates2_queries25_seeded_ends.json')
BRANCH=ROOT/'28_exact_source_current_relative_operands_bound_to140_native_cases.json'
if __name__=='__main__':
    assert not ROOT.exists()
    current,control=map(read,[CURRENT,CONTROL]);g=current['groups'][0];block=bytes.fromhex(g['current_block_hex'])
    assert g['block']==48 and len(block)==5252
    operands=[]
    for edge,case in zip(control['operands_requiring_adjustment_when_resizing'],control['source_relative_cases'],strict=True):
        at=edge['offset'];raw=block[at:at+4].hex()
        assert raw==edge['source_operand_hex'] and case['offset']==at and len(case['cases'])==5
        c=next(c for c in g['all_current_commands'] if c['offset']==at)
        assert c['word']==edge['word'] and c['ancestor_0100_offsets']==edge['ancestor_0100_offsets']
        assert at+4 in {p['offset'] for p in g['all_current_commands']} and edge['matched_skip_target'] in {p['offset'] for p in g['all_current_commands']}
        operands.append(dict(**edge,current_operand_hex=raw))
    assert len(operands)==28 and len(g['all_current_commands'])==163
    result=derive('scripts/relocate_Rafael_B47_v7989b.py','scripts/relocate_Rafael_B48_v8041.py',{
        'work/analysis/Rafael_B47_relocation_v7989':'work/analysis/Rafael_B48_relocation_v8041',
        'Rafael_B47_current_v7980/all15_complete_source_current_refs_before_new_English_manuscript.json':
            'Rafael_B48_current_v8028/all91_complete_source_current_refs_before_new_English_manuscript.json',
        'Rafael_next_clean_v7971/complete_clean_SC0_B47_EV0_andcoverage_before_current_English.json':
            'Rafael_next_clean_v8020/complete_clean_SC0_B48_EV0_andcoverage_before_current_English.json',
        'rafael_B47_editorial_manuscript_v2.json':'rafael_B48_editorial_manuscript_v3.json',
        'Rafael_B47_layout_v7984e/15_automatic_plans_full_native_width_zero_preamble_separate_body.json':
            'Rafael_B48_layout_v8035d/91_automatic_plans_full_native_width_source_preambles4_FE.json',
        'Rafael_B47_native_review_v7988/15_paragraphs16_native_pages4_names_two_scoped_warnings_individual_wrap_review.json':
            'Rafael_B48_native_review_v8040/91_paragraphs92_native_pages9_names_two_scoped_warnings37_infos_wrap_review.json',
        'work/analysis/Rafael_B47_archive_tools_v7989/24_exact_source_current_relative_operands_bound_to120_native_cases.json':BRANCH.as_posix(),
        'current_V7964_Rafael_native_v7967':'current_V8013_Rafael_native_v8016',
        "row['source_record_index'] in [5,63]":"row['source_record_index'] in [86,406]",
        "sum(len(g['text_records']) for g in groups)==15 and sum(len(g['relative_fixups']) for g in groups)==24":
            "sum(len(g['text_records']) for g in groups)==91 and sum(len(g['relative_fixups']) for g in groups)==28",
        'SC0_B47_RESEARCH_ONLY.DK4':'SC0_B48_RESEARCH_ONLY.DK4','==[47]':'==[48]',
        'one_block15_speeches24_relative_fixups120_cases_exact_full_inverse.json':
            'one_block91_speeches28_relative_fixups140_cases_exact_full_inverse.json',
        'source_relative_sites=24,relocated_native_skip_cases=120':'source_relative_sites=28,relocated_native_skip_cases=140',
        '15speeches/24relative sites/120guarded cases;onlyB47':'91speeches/28relative sites/140guarded cases;onlyB48',
        'Research-only B47 reconstruction:24 nested fixups,15 complete preambles,16 reviewed pages andfull inverses.':
            'Research-only B48 reconstruction:28nested fixups,91complete preambles,92reviewed pages andfull inverses.',
    })
    ROOT.mkdir(parents=True)
    save(BRANCH,dict(candidate=current['current_ROM'],candidate_sha256=current['current_ROM_sha256'],
        source_context=str(CURRENT),source_context_sha256=sha(CURRENT.read_bytes()),
        source_control_proof=str(CONTROL),source_control_proof_sha256=sha(CONTROL.read_bytes()),
        operands_requiring_adjustment_when_resizing=operands,
        all28_source_current_fourbyte_operands_offsets_ancestors_alignment_runtime_equal=True,
        original140_structural_source_cases_reused_by_exact_operand_andnative_read_scope_not_new_current_replays=True,
        source_control_cases=control['source_relative_cases'],source_English_opaque_speech_bytes_not_executed_by_relative_primitive=True,
        source_locked_reconstruction_derivation=result,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('28exact source/current operands bound to140source native cases;B48reconstruction prepared.No ROM orcredit.')
