"""Prepare exact source-preserving B199 fixture and observation tools."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B199_source_tools_v5779')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B198_source_fixture_v5712.py','scripts/research_lil_B199_source_fixture_v5780.py',{
        'B198':'B199','fixture_v5712':'fixture_v5780','source_v5702':'source_v5767',
        'source_v5712':'source_v5780','all17_clean_current':'all31_clean_current',
        '.blocks[198]':'.blocks[199]',"source_block=198":"source_block=199",
        'assert len(jp)==end==544':'assert len(jp)==1168 and end==1166 and jp[end:]==bytes(2)',
        "len(commands)==46 and len(speeches)==17 and sum(c['word']==0x8000 for c in commands)==2":
        "len(commands)==56 and len(speeches)==31 and sum(c['word']==0x8000 for c in commands)==0",
        "sum(c['word']==0xA000 for c in commands)==6":"sum(c['word']==0xA000 for c in commands)==5",
        'all46_stored_fixture_commands':'all56_stored_fixture_commands',
        'all37_source_commands_plus9_original_initializers_stored':'all47_source_commands_plus9_original_initializers_stored',
        'source_predicates_roster_funds_RNG_results_and_effects_not_forced':'source_controls_roster_funds_RNG_results_and_effects_not_forced',
        'source_event198_not_naturally_activated':'source_event199_not_naturally_activated',
        'Namahage/dream/presentation':'portrait/chase/misunderstood-gift',
        '37 original+9 initializer commands,17 speeches,two original predicates':'47 original+9 initializer commands,31 speeches,no predicates'})]
    rows.append(derive('scripts/run_lil_B198_source_fixture_v5713.py','scripts/run_lil_B199_source_fixture_v5781.py',{
        'B198':'B199','fixture_v5712':'fixture_v5780','run_v5713':'run_v5781','source_v5713':'source_v5781',
        "selected['source_block']==198":"selected['source_block']==199",
        'source_event198_not_naturally_selected':'source_event199_not_naturally_selected',
        "'displayed_original_source_block':198":"'displayed_original_source_block':199",
        'all37_source_commands_retained':'all47_source_commands_retained'}))
    rows.append(derive('scripts/audit_lil_B198_source_paths_v5714.py','scripts/audit_lil_B199_source_paths_v5782.py',{
        'B198':'B199','paths_v5714':'paths_v5782','fixture_v5712':'fixture_v5780','run_v5713':'run_v5781',
        "pairs[-1]['source_offset']==540":"pairs[-1]['source_offset']==1162",
        'source_end540_return_frame':'source_end1162_return_frame','stored_source_objects=17':'stored_source_objects=31',
        'all37_source_plus9_original_initializer_commands_stored':'all47_source_plus9_original_initializer_commands_stored',
        'initialized_Amsterdam_fixture_not_natural_event198_activation_or_original_location':'initialized_Amsterdam_fixture_not_natural_event199_activation_or_original_location',
        '[10,38,42,49,53,65,72,80,84,95]':'[5,9,19,31,34,37,43,47,54,58,70,88,95,103,115]'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_tool_derivations.json',dict(derived=rows,no_runtime_ROM_or_review_credit=True))
    print('Three B199 source fixture/run/audit tools prepared; native numeric constants unchanged.')
