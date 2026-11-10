"""Freeze exact stored parity andonly the control types actually present inB36."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_confrontation_stored_control_tools_v7803')
MAP='work/analysis/maria_confrontation_relocation_v7802/one_block16_speeches_no_relative_fixups_exact_full_inverse.json'
FONT='work/analysis/maria_confrontation_row_reasons_v7801b/16_native_pages_exact_with_nine_individual_row_reasons.json'
STORED='work/analysis/maria_confrontation_stored_v7803/16_final_stored_targets64_alignments11_zero_ink_tails16_pages.json'
CURRENT='work/analysis/maria_confrontation_current_v7789/all16_complete_source_current_refs_before_new_English_manuscript.json'
SOURCE='work/analysis/maria_next_clean_v7786/complete_clean_SC3_B36_EV3_andcoverage_before_current_English.json'
INPUT='work/analysis/current_V7779_native_v7782/route3/current_native_input.json'
if __name__=='__main__':
    assert not ROOT.exists();mapping=read(MAP)
    assert len(mapping['groups'])==1 and mapping['groups'][0]['block']==36
    assert sum(r['parity_space_added'] for r in mapping['groups'][0]['text_records'])==11
    results=[]
    results.append(derive('scripts/prove_Maria_story_stored_v7743.py','scripts/prove_Maria_confrontation_stored_v7803.py',{
        'maria_story_stored_v7743':'maria_confrontation_stored_v7803',
        'work/analysis/maria_story_relocation_v7742/three_blocks67_speeches20_fixups100_native_target_cases_exact_inverse.json':MAP,
        'work/analysis/maria_story_pages_v7738/67_compiled268_alignments68_complete_native_pages.json':FONT,
        'translations/maria_B34_B108_B35_editorial_manuscript_v2.json':'translations/maria_B36_editorial_manuscript_v2.json',
        'work/analysis/current_V7717_native_v7720/route3/current_native_input.json':INPUT,
        "len(rows)==67 and fresh+reused==268 and sum(r['parity_space_added'] for r in rows)==33":"len(rows)==16 and fresh+reused==64 and sum(r['parity_space_added'] for r in rows)==11",
        "sum(len(r['complete_pages']['pages']) for r in rows)==68":"sum(len(r['complete_pages']['pages']) for r in rows)==16",
        '67_final_stored_targets268_alignments33_zero_ink_tails68_pages.json':'16_final_stored_targets64_alignments11_zero_ink_tails16_pages.json',
        'stored_alignment_cases=268':'stored_alignment_cases=64',
        'zero_ink_parity_tail_count=33':'zero_ink_parity_tail_count=11','complete_stored_native_pages=68':'complete_stored_native_pages=16',
        'all67_stored_targets_equal_reviewed_complete_native_ink':'all16_stored_targets_equal_reviewed_complete_native_ink',
        'source_macro_counts_andall8_static_selectors_preserved':'source_macro_order_counts_andall3_static_selectors_preserved',
        'two_page_R111_has_no_lost_character_extra_blank_page_orparity_ink':'all16_single_pages_no_lost_character_extra_blank_page_orparity_ink',
        'all67_formatting_gates_false':'all16_formatting_gates_false',
        'Stored67targets/268alignments:':'Stored16targets/64alignments:',
        '33zero-ink tails;68complete pages;':'11zero-ink tails;16complete pages;',
    }))
    results.append(derive('scripts/prove_Maria_story_final_controls_v7745.py','scripts/prove_Maria_confrontation_controls_v7804.py',{
        'maria_story_final_controls_v7745':'maria_confrontation_controls_v7804',
        'work/analysis/maria_story_relocation_v7742/three_blocks67_speeches20_fixups100_native_target_cases_exact_inverse.json':MAP,
        'work/analysis/maria_story_current_v7728/all67_complete_source_current_refs_before_new_English_manuscript.json':CURRENT,
        'work/analysis/maria_story_chain_clean_v7725/complete_clean_34_108_35_67_refs_explicit_source_dependency_chain_before_current_English.json':SOURCE,
        'work/analysis/maria_story_effective_v7729/all67_effective_English_templates134_original_dispatches.json':
        'work/analysis/maria_confrontation_effective_v7790/all16_effective_English_templates32_original_dispatches.json',
        'work/analysis/maria_story_stored_v7743/67_final_stored_targets268_alignments33_zero_ink_tails68_pages.json':STORED,
        'work/analysis/current_V7717_native_v7720/route3/current_native_input.json':INPUT,
        'word in [0x633F,0x632D,0x633C,0x632A]':'word in [0x633D,0x632A]',
        'for word in [0x633F,0x632D,0x633C,0x632A]:':'for word in [0x633D,0x632A]:',
        '0x050A,0x623C]':'0x050A,0x623D]',
        "            pauses.append(ctx.execute(pause,previous,returned));ctx.machines.pop()":
        "            if any(r['word']==0x2000 for r in numeric):pauses.append(ctx.execute(pause,previous,returned));ctx.machines.pop()",
        "len(dispatches)==67 and len(resources)==40 and len(setups)==len(pauses)==10 and len(c200)==3 and len(ends)==45":
        "len(dispatches)==16 and len(resources)==20 and len(setups)==10 and len(pauses)==0 and len(c200)==0 and len(ends)==15",
        '67_final_dispatches_numeric_leaves_opaque_controls_resources_pause_C200_ends.json':
        '16_final_dispatches_six_numeric_leaves_623D_resources_setup_ends.json',
        'all67_final_stored_dispatches_have_no_catalogue_override':'all16_final_stored_dispatches_have_no_catalogue_override',
        '67final dispatches;numeric leaves':'16final dispatches;numeric leaves',
        '40resources/10setup/10pause/3C200/45complete-end':'20resources/10setup/0pause/0C200/15complete-end',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'provenance.json',dict(derivations=results,
        exact11_parity_tails_bound_to_measured_reconstruction=True,
        only_original6000_633D_623D_632A_A000_andfourbyte_end_present=True,
        absent2000_C200_andrelative_commands_not_executed_orinvented=True,
        resource_callee_bodies_and623D_A000_structural_boundaries_not_full_effect_mechanics=True,
        all_original_native_high_constants_ABI_canaries_ownership_andcomplete_ink_guards_preserved=True,
        map_sha256=sha(Path(MAP).read_bytes()),new_credit=0,full_goal_complete=False))
