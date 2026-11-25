"""Bind five unchanged source/current relative operands; derive guarded research-only relocation."""
import struct
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/Rafael_B45_archive_tools_v7884')
CURRENT=Path('work/analysis/Rafael_B45_current_v7871/all12_complete_source_current_refs_before_new_English_manuscript.json')
SOURCE=Path('work/analysis/Rafael_next_clean_v7864/complete_clean_SC0_B45_EV0_andcoverage_before_current_English.json')
CONTROLS=Path('work/analysis/Rafael_B45_source_controls_v7870b/source_EV0_five_relative_sites_predicate_resources_structural_andnormal_end.json')
if __name__=='__main__':
    assert not ROOT.exists();current,source,controls=map(read,[CURRENT,SOURCE,CONTROLS]);edges=[]
    sg,cg=source['groups'][0],current['groups'][0]
    clean,old=bytes.fromhex(sg['clean_block_hex']),bytes.fromhex(cg['current_block_hex'])
    source_commands=sg['commands'];commands=cg['all_current_commands']
    boundaries={c['offset'] for c in commands}|{cg['current_logical_end']}
    for a,b in zip(source_commands,commands,strict=True):
        assert a['offset']==b['offset'] and a['word']==b['word'] and a['native_extent']==b['native_extent']
        if a['word'] not in [0x100,0x200,0x300,0x400]:continue
        at=a['offset'];span=struct.unpack_from('<H',old,at+2)[0]
        assert clean[at:at+4]==old[at:at+4] and at+4 in boundaries and at+4+span in boundaries
        proof=next(r for r in controls['source_relative_sites'] if r['offset']==at)
        assert proof['word']==a['word'] and proof['span']==span and len(proof['cases'])==5
        assert all(r['next_offset']==at+4+(span if r['taken'] else 0) and r['all4MiB_ABI_owner_input_output_andcanary_guards_exact'] for r in proof['cases'])
        edges.append(dict(block=45,offset=at,word=a['word'],span_field_offset=at+2,source_span=span,
            unmatched_next_offset=at+4,matched_skip_target=at+4+span,ancestor_0100_offsets=b['ancestor_0100_offsets'],
            source_operand_hex=clean[at:at+4].hex(),current_operand_hex=old[at:at+4].hex()))
    assert len(edges)==5 and controls['source_relative_cases']==25
    results=derive('scripts/relocate_Maria_confrontation_v7802.py','scripts/relocate_Rafael_B45_v7884.py',{
        'Research-only three-block reconstruction with exact nested fixups and full predecessor inverse.':'Research-only Rafael B45 reconstruction:five exact nested fixups,complete00 preambles andfull predecessor inverse.',
        'from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext':
        'from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext',
        "ctx=MariaUnlockedCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')":
        "ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')",
        'work/analysis/maria_confrontation_relocation_v7802':'work/analysis/Rafael_B45_relocation_v7884',
        'work/analysis/maria_confrontation_current_v7789/all16_complete_source_current_refs_before_new_English_manuscript.json':str(CURRENT).replace('\\','/'),
        'work/analysis/maria_next_clean_v7786/complete_clean_SC3_B36_EV3_andcoverage_before_current_English.json':str(SOURCE).replace('\\','/'),
        'translations/maria_B36_editorial_manuscript_v2.json':'translations/rafael_B45_editorial_manuscript_v3.json',
        'work/analysis/maria_confrontation_row_reasons_v7801b/16_full_width_plans_nine_individual_row_reasons.json':
        'work/analysis/Rafael_B45_layout_v7881b/12_automatic_plans_full_native_width_zero_preamble_separate_body.json',
        'work/analysis/maria_confrontation_row_reasons_v7801b/16_native_pages_exact_with_nine_individual_row_reasons.json':
        'work/analysis/Rafael_B45_native_review_v7883/12_exact_native_pages_rebound_with_individual_row_review.json',
        'work/analysis/maria_confrontation_archive_tools_v7802/source_current_no_relative_orpredicate_commands.json':
        'work/analysis/Rafael_B45_archive_tools_v7884/five_exact_source_current_relative_operands_bound_to25_native_cases.json',
        'work/analysis/current_V7779_native_v7782/route3/current_native_input.json':
        'work/analysis/current_V7857_Rafael_native_v7868/current_native_input.json',
        "assert plan['manuscript_sha256']==native['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())":
        "assert plan['manuscript_sha256']==sha(Path(doc['prior_manuscript']['path']).read_bytes()) and native['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())",
        "assert b'\\0' not in value and value[0]==oldraw[0]":
        "assert b'\\0' not in value[1:] and value[0]==oldraw[0]",
        "f'SC3_block{number}_RESEARCH_ONLY.bin'":"f'SC0_block{number}_RESEARCH_ONLY.bin'",
        "sum(len(g['text_records']) for g in groups)==16 and sum(len(g['relative_fixups']) for g in groups)==0":
        "sum(len(g['text_records']) for g in groups)==12 and sum(len(g['relative_fixups']) for g in groups)==5",
        'SC3_B36_RESEARCH_ONLY.DK4':'SC0_B45_RESEARCH_ONLY.DK4',
        "if a!=b]==[36]":"if a!=b]==[45]",
        'one_block16_speeches_no_relative_fixups_exact_full_inverse.json':'one_block12_speeches5_relative_fixups25_cases_exact_full_inverse.json',
        'other302_blocks_exact=True':'other342_blocks_exact=len(parsed.blocks)==343',
        'source_relative_sites=0,relocated_native_skip_cases=0':'source_relative_sites=5,relocated_native_skip_cases=25',
        'all16_six_byte_preambles_macros_selectors_complete_terminal_andseparate_tails_preserved=True':
        'all12_six_byte_preambles_macros_selectors_complete_terminal_andseparate_tails_preserved=True',
        'existing_system_only_unlock_fixture=True,earned_unlock_verified=False':
        'ordinary_captain0_opening_context_no_unlock_orstate_fixture=True',
        'Research archive:16speeches/no relative sites;onlyB36 changes,302others exact;predecessor archive andclean block invert exactly.No ROM orcredit.':
        'Research archive:12speeches/five relative sites/25guarded native cases;onlyB45 changes,342others exact;predecessor archive andclean block invert exactly.No ROM orcredit.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'five_exact_source_current_relative_operands_bound_to25_native_cases.json',dict(
        operands_requiring_adjustment_when_resizing=edges,source_control_proof=str(CONTROLS),source_control_proof_sha256=sha(CONTROLS.read_bytes()),
        source_native_cases_reused_by_exact_current_operand_offset_command_extent_andboundaries=25,
        source_current_relative_function_reads_identical_four_byte_operands=True,
        source_current_English_bodies_not_relabelled_as_fresh_decoder_execution=True,
        FE_R52_conditional_result1_not_unconditional_orfull_trade_mechanics=True,
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,SOURCE,CONTROLS,Path(__file__)]},new_credit=0,full_goal_complete=False))
    save(ROOT/'provenance.json',dict(derivation=results,
        all_original_native_high_constants_nested_scope_canary_inverse_andzero_tail_guards_preserved=True,
        source00_allowed_only_in_complete_original_preamble_body_zero_still_forbidden=True,
        source_current_unchanged_relative_cases_bound_not_unnecessarily_reexecuted=True,
        actual_relocated25cases_will_be_fresh=True,research_archive_only_no_ROM_registry_orcredit=True,full_goal_complete=False))
