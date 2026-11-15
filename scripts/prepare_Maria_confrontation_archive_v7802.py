"""Bind absence ofrelative commands andfreeze unchanged full-inverse reconstruction forB36."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_confrontation_archive_tools_v7802')
SOURCE=Path('work/analysis/maria_next_clean_v7786/complete_clean_SC3_B36_EV3_andcoverage_before_current_English.json')
CURRENT=Path('work/analysis/maria_confrontation_current_v7789/all16_complete_source_current_refs_before_new_English_manuscript.json')
BRANCH=ROOT/'source_current_no_relative_orpredicate_commands.json'
if __name__=='__main__':
    assert not ROOT.exists();source,current=map(read,[SOURCE,CURRENT])
    assert len(source['groups'])==len(current['groups'])==1 and source['groups'][0]['block']==current['groups'][0]['block']==36
    for group in source['groups']:
        assert len(group['commands'])==22 and len(group['records'])==16
        assert not any(c['word'] in [0x100,0x200,0x300,0x400,0x8000,0x8100] for c in group['commands'])
    assert not any(c['word'] in [0x100,0x200,0x300,0x400,0x8000,0x8100] for g in current['groups'] for c in g['all_current_commands'])
    ROOT.mkdir(parents=True);save(BRANCH,dict(operands_requiring_adjustment_when_resizing=[],
        original_source_andcurrent_complete_native_command_lists_bound=True,source_current_relative_andinblock_predicate_commands=0,
        no_fresh_native_skip_cases_for_absent_commands=True,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CURRENT,Path(__file__)]},
        new_credit=0,full_goal_complete=False))
    result=derive('scripts/relocate_Maria_story_final_v7758.py','scripts/relocate_Maria_confrontation_v7802.py',{
        'maria_story_final_relocation_v7758':'maria_confrontation_relocation_v7802',
        'work/analysis/maria_story_current_v7728/all67_complete_source_current_refs_before_new_English_manuscript.json':str(CURRENT).replace('\\','/'),
        'work/analysis/maria_story_chain_clean_v7725/complete_clean_34_108_35_67_refs_explicit_source_dependency_chain_before_current_English.json':str(SOURCE).replace('\\','/'),
        'translations/maria_B34_B108_B35_editorial_manuscript_v3.json':'translations/maria_B36_editorial_manuscript_v2.json',
        'work/analysis/maria_story_final_prose_v7756b/67_final_v3_plans_two_refinements65_exact_compiled_retentions.json':
        'work/analysis/maria_confrontation_row_reasons_v7801b/16_full_width_plans_nine_individual_row_reasons.json',
        'work/analysis/maria_story_final_native_v7757b/67_final_v3_native_pages_andfully_bound_logical_lineage.json':
        'work/analysis/maria_confrontation_row_reasons_v7801b/16_native_pages_exact_with_nine_individual_row_reasons.json',
        'work/analysis/maria_story_branches_v7741/20_relative_sites200_guarded_original_source_current_cases.json':str(BRANCH).replace('\\','/'),
        'work/analysis/current_V7717_native_v7720/route3/current_native_input.json':'work/analysis/current_V7779_native_v7782/route3/current_native_input.json',
        "sum(len(g['text_records']) for g in groups)==67 and sum(len(g['relative_fixups']) for g in groups)==20":
        "sum(len(g['text_records']) for g in groups)==16 and sum(len(g['relative_fixups']) for g in groups)==0",
        'SC3_three_blocks_RESEARCH_ONLY.DK4':'SC3_B36_RESEARCH_ONLY.DK4',
        '==[34,35,108]':'==[36]',
        'three_blocks67_speeches20_fixups100_native_target_cases_exact_inverse.json':'one_block16_speeches_no_relative_fixups_exact_full_inverse.json',
        'exactly_three_blocks_changed=True,other300_blocks_exact=True':'exactly_one_block_changed=True,other302_blocks_exact=True',
        'all_three_clean_source_blocks_reconstructed_exactly':'complete_clean_source_block_reconstructed_exactly',
        'source_relative_sites=20,relocated_native_skip_cases=100':'source_relative_sites=0,relocated_native_skip_cases=0',
        'all67_six_byte_preambles_macros_selectors_complete_terminal_andseparate_tails_preserved':'all16_six_byte_preambles_macros_selectors_complete_terminal_andseparate_tails_preserved',
        'Research archive:67speeches/20fixups/100relocated native cases;three blocks changed,300others exact;predecessor archive andthree clean blocks invert exactly.':
        'Research archive:16speeches/no relative sites;onlyB36 changes,302others exact;predecessor archive andclean block invert exactly.',
    })
    save(ROOT/'provenance.json',dict(derivation=result,original_native_bounds_preambles_macro_order_all_commands_andfull_inverse_guards_preserved=True,
        zero_relative_sites_verified_from_complete_original_source_andcurrent_native_inventories=True,
        no_ROM_registry_orcredit_change=True,full_goal_complete=False))
