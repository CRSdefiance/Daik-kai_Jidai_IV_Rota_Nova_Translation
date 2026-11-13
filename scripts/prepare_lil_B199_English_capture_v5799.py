"""Prepare same-context English fixture and paired actual-glyph/transition audit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B199_English_capture_tools_v5799')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B198_English_fixture_v5738.py','scripts/research_lil_B199_English_fixture_v5805.py',{
        'B198':'B199','prepare_lil_B198_research_v5732':'prepare_lil_B199_reference_tools_v5796',
        'English_fixture_v5738':'English_fixture_v5805','English_v5738':'English_v5805',
        'source_fixture_v5712':'source_fixture_v5780','source_fixture_v5713':'source_fixture_v5781',
        'English_fixture_v5739':'English_fixture_v5806','English_run_v5739':'English_run_v5806','English_v5739':'English_v5806',
        'source_run_v5713':'source_run_v5781','source_v5713':'source_v5781',
        'bank[198]':'bank[199]','source_block=198':'source_block=199',
        'assert len(bank[198])==end==644':'assert len(bank[199])==1116 and end==1114 and bank[199][end:]==bytes(2)',
        'len(native)==37 and len(commands)==46 and len(speeches)==17':'len(native)==47 and len(commands)==56 and len(speeches)==31',
        'all46_stored_fixture_commands':'all56_stored_fixture_commands',
        'all37_source_commands_plus9_initializers_retained_without_omission':'all47_source_commands_plus9_initializers_retained_without_omission',
        'not_natural_event198_activation':'not_natural_event199_activation',
        '37 original+9 initializer commands,17 speech objects,two original predicates':'47 original+9 initializer commands,31 speech objects,no predicates'} )]
    rows.append(derive('scripts/audit_lil_B198_actual_v5743.py','scripts/audit_lil_B199_actual_v5807.py',{
        'B198':'B199','actual_v5743':'actual_v5807','source_fixture_v5712':'source_fixture_v5780',
        'English_fixture_v5738':'English_fixture_v5805','source_run_v5713':'source_run_v5781','English_run_v5739':'English_run_v5806',
        'fonts_v5741/all17_progressive_FE_native_planes_and136_alignment_cases':'fonts_v5792/all31_progressive_FE_native_planes_and248_alignment_cases',
        'all37_source_commands_retained':'all47_source_commands_retained',
        '[10,14,18,22,26,30,34,38,42,49,53,72,76,80,84]':'[5,9,12,16,19,23,27,31,34,37,40,43,47,50,54,58,62,66,70,73,77,81,84,88,91,95,99,103,107,111,115]',
        "pairs[-1]['source_offset']==540":"pairs[-1]['source_offset']==1162",
        "assert [(r['source_offset'],r['native_result']) for r in predicates]==[(306,[2,0]),(480,[2,0])]":"assert predicates==[]",
        "len(actual)==15 and sum(r['prefix']==254 for r in actual)==6":"len(actual)==31 and sum(r['prefix']==254 for r in actual)==1",
        'fifteen_actual_panels_source_matched_controls_and_complete_native_holds':'thirty_one_actual_panels_source_matched_controls_and_complete_native_holds',
        'actual_unique_speech_panels=15':'actual_unique_speech_panels=31','offline_only_source_indices=[65,95]':'offline_only_source_indices=[]',
        'all37_source_commands_and9_initializers_stored':'all47_source_commands_and9_initializers_stored',
        'same_observed_source_path_original_results_predicates_and_end540':'same_observed_source_path_original_results_no_predicates_and_end1162',
        'no_natural_event198_activation':'no_natural_event199_activation','panels=15':'panels=31'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_English_fixture_and_actual_audit_tools.json',dict(tools=rows,
        source_boot_reused_not_repeated=True,expected_source_speeches=31,expected_commands=56,source_predicates=0,
        original_inputs_and_source_conditions_roster_funds_RNG_unforced=True,
        no_new_ROM_or_run_or_review_credit_yet=True,full_goal_complete=False))
    print('English content fixture and31-panel paired actual audit prepared. Japanese boot reused;no forced state.')
