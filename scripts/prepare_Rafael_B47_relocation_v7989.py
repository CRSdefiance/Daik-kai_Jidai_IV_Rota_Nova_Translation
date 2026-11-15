"""Bind all24 exact source/current operands andprepare reversible speech-only research relocation."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B47_archive_tools_v7989')
CURRENT=Path('work/analysis/Rafael_B47_current_v7980/all15_complete_source_current_refs_before_new_English_manuscript.json')
CONTROL=Path('work/analysis/Rafael_B47_source_controls_v7977/source_EV0_24_relative_sites120_cases6_raw_predicates25_seeded_ends.json')
BRANCH=ROOT/'24_exact_source_current_relative_operands_bound_to120_native_cases.json'
if __name__=='__main__':
    assert not ROOT.exists()
    current,control=map(read,[CURRENT,CONTROL]);g=current['groups'][0];block=bytes.fromhex(g['current_block_hex'])
    assert g['block']==47 and len(block)==1284
    operands=[]
    for edge,case in zip(control['operands_requiring_adjustment_when_resizing'],control['source_relative_cases'],strict=True):
        at=edge['offset'];raw=block[at:at+4].hex()
        assert raw==edge['source_operand_hex'] and case['offset']==at and len(case['cases'])==5
        c=next(c for c in g['all_current_commands'] if c['offset']==at)
        assert c['word']==edge['word'] and c['ancestor_0100_offsets']==edge['ancestor_0100_offsets']
        assert at+4 in {p['offset'] for p in g['all_current_commands']} and edge['matched_skip_target'] in {p['offset'] for p in g['all_current_commands']}
        operands.append(dict(**edge,current_operand_hex=raw))
    assert len(operands)==24 and len(g['all_current_commands'])==48
    template=Path('scripts/relocate_Rafael_B45_v7884.py').read_text('utf8')
    old_assert="    assert plan['manuscript_sha256']==sha(Path(doc['prior_manuscript']['path']).read_bytes()) and native['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and all(not any(i['severity'] in ['warning','error'] for i in r['base_QA']['issues']) for r in plan['records'])"
    new_assert="""    assert plan['manuscript_sha256']==sha(Path(doc['prior_manuscript']).read_bytes()) and native['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    for row,p in zip(doc['records'],plan['records'],strict=True):
        assert row['id']==p['id'] and row['compiled_hex']==p['encoded_hex']
        warnings=[i for i in p['base_QA']['issues'] if i['severity']=='warning']
        assert not any(i['severity']=='error' for i in p['base_QA']['issues'])
        if row['source_record_index'] in [5,63]:
            assert row['qa_waivers']==['weak-line-ending'] and row['qa_waiver_reason'] and warnings==[row['qa_waiver_scope']['exact_issue']]
            assert row['qa_waiver_scope']['id']==row['id'] and row['qa_waiver_scope']['source_hex']==row['source_hex'] and row['qa_waiver_scope']['compiled_hex']==p['encoded_hex']
        else:assert warnings==[] and row['qa_waivers']==[] and row['qa_waiver_reason'] is None
"""
    result=derive('scripts/relocate_Rafael_B45_v7884.py','scripts/relocate_Rafael_B47_v7989.py',{
        'Rafael_B45_relocation_v7884':'Rafael_B47_relocation_v7989',
        'Rafael_B45_current_v7871/all12_complete_source_current_refs_before_new_English_manuscript.json':
            'Rafael_B47_current_v7980/all15_complete_source_current_refs_before_new_English_manuscript.json',
        'Rafael_next_clean_v7864/complete_clean_SC0_B45_EV0_andcoverage_before_current_English.json':
            'Rafael_next_clean_v7971/complete_clean_SC0_B47_EV0_andcoverage_before_current_English.json',
        'rafael_B45_editorial_manuscript_v3':'rafael_B47_editorial_manuscript_v2',
        'Rafael_B45_layout_v7881b/12_automatic_plans_full_native_width_zero_preamble_separate_body.json':
            'Rafael_B47_layout_v7984e/15_automatic_plans_full_native_width_zero_preamble_separate_body.json',
        'Rafael_B45_native_review_v7883/12_exact_native_pages_rebound_with_individual_row_review.json':
            'Rafael_B47_native_review_v7988/15_paragraphs16_native_pages4_names_two_scoped_warnings_individual_wrap_review.json',
        'Rafael_B45_archive_tools_v7884/five_exact_source_current_relative_operands_bound_to25_native_cases.json':BRANCH.as_posix(),
        'current_V7857_Rafael_native_v7868':'current_V7964_Rafael_native_v7967',
        old_assert:new_assert,
        "sum(len(g['text_records']) for g in groups)==12 and sum(len(g['relative_fixups']) for g in groups)==5":
            "sum(len(g['text_records']) for g in groups)==15 and sum(len(g['relative_fixups']) for g in groups)==24",
        'SC0_B45_RESEARCH_ONLY.DK4':'SC0_B47_RESEARCH_ONLY.DK4',
        '==[45]':'==[47]',
        'one_block12_speeches5_relative_fixups25_cases_exact_full_inverse.json':
            'one_block15_speeches24_relative_fixups120_cases_exact_full_inverse.json',
        'source_relative_sites=5,relocated_native_skip_cases=25':'source_relative_sites=24,relocated_native_skip_cases=120',
        'all12_six_byte_preambles_macros_selectors_complete_terminal_andseparate_tails_preserved':
            'all15_six_byte_preambles_zero_macros_selectors_complete_terminal_andseparate_tails_preserved',
        'Research-only Rafael B45 reconstruction:five exact nested fixups,complete00 preambles andfull predecessor inverse.':
            'Research-only B47 reconstruction:24 nested fixups,15 complete preambles,16 reviewed pages andfull inverses.',
        'Research archive:12speeches/five relative sites/25guarded native cases;onlyB45 changes,342others exact;predecessor archive andclean block invert exactly.No ROM orcredit.':
            'Research archive:15speeches/24relative sites/120guarded cases;onlyB47 changes,342others exact;full predecessor archive andclean block inverses pass.No ROM orcredit.',
    })
    ROOT.mkdir(parents=True)
    save(BRANCH,dict(candidate=current['current_ROM'],candidate_sha256=current['current_ROM_sha256'],
        current_packet=str(CURRENT),current_packet_sha256=sha(CURRENT.read_bytes()),source_controls=str(CONTROL),source_controls_sha256=sha(CONTROL.read_bytes()),
        operands_requiring_adjustment_when_resizing=operands,
        all24_source_current_four_byte_relative_operands_andboundaries_exact=True,
        source120_native_cases_reused_by_exact_opcode_span_alignment_runtime_andhandler_reads=True,
        handler_reads_only_original_relative_opcode_span_andstructural_argument_not_replaced_body_text=True,
        new_native_current_operand_replays=0,relocated_operand_cases_require_fresh_native_measurement=True,new_credit=0,full_goal_complete=False))
    save(ROOT/'source_locked_derivation.json',result)
    print('Bound24 source/current relative operands;prepared B47 research reconstruction withtwo exact documented warnings retained.')
