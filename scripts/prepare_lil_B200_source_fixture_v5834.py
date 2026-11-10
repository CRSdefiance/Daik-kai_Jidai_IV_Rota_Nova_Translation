"""Prepare exact source-preserving B200 fixture,observation and source-screen audit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B200_source_tools_v5834')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/research_lil_B199_source_fixture_v5780.py','scripts/research_lil_B200_source_fixture_v5835.py',{
        'B199':'B200','fixture_v5780':'fixture_v5835','source_v5767':'source_v5826',
        'source_v5780':'source_v5835','all31_clean_current':'all19_clean_current',
        '.blocks[199]':'.blocks[200]','source_block=199':'source_block=200',
        'len(jp)==1168 and end==1166':'len(jp)==932 and end==930',
        "len(commands)==56 and len(speeches)==31":"len(commands)==40 and len(speeches)==19",
        "sum(c['word']==0xA000 for c in commands)==5":"sum(c['word']==0xA000 for c in commands)==6",
        'all56_stored_fixture_commands':'all40_stored_fixture_commands',
        'all47_source_commands_plus9_original_initializers_stored':'all31_source_commands_plus9_original_initializers_stored',
        'source_event199_not_naturally_activated':'source_event200_not_naturally_activated',
        'portrait/chase/misunderstood-gift':'collapse/inn-recovery/thanks-and-Charm',
        '47 original+9 initializer commands,31 speeches,no predicates':'31 original+9 initializer commands,19 speeches,no predicates'})]
    tools.append(derive('scripts/run_lil_B199_source_fixture_v5781.py','scripts/run_lil_B200_source_fixture_v5836.py',{
        'B199':'B200','fixture_v5780':'fixture_v5835','run_v5781':'run_v5836','source_v5781':'source_v5836',
        "selected['source_block']==199":"selected['source_block']==200",
        'source_event199_not_naturally_selected':'source_event200_not_naturally_selected',
        "'displayed_original_source_block':199":"'displayed_original_source_block':200",
        'all47_source_commands_retained':'all31_source_commands_retained'}))
    tools.append(derive('scripts/audit_lil_B199_source_paths_v5782.py','scripts/audit_lil_B200_source_paths_v5837.py',{
        'B199':'B200','paths_v5782':'paths_v5837','fixture_v5780':'fixture_v5835','run_v5781':'run_v5836',
        "pairs[-1]['source_offset']==1162":"pairs[-1]['source_offset']==926",
        'source_end1162_return_frame':'source_end926_return_frame','stored_source_objects=31':'stored_source_objects=19',
        'all47_source_plus9_original_initializer_commands_stored':'all31_source_plus9_original_initializer_commands_stored',
        'initialized_Amsterdam_fixture_not_natural_event199_activation_or_original_location':'initialized_Amsterdam_fixture_not_natural_event200_activation_or_original_location',
        '[5,9,19,31,34,37,43,47,54,58,70,88,95,103,115]':'[5,9,17,21,33,40,47,54,58,62,65,69,72]',
        "assert set(selected).issubset({r['source_record_index'] for r in records.values()})":
        "assert set(selected)=={r['source_record_index'] for r in records.values()} and len(selected)==19\n    assert len(pairs)==40 and {p['source_offset'] for p in pairs if p['source_offset'] is not None}=={r['source_offset'] for r in fixture['selected_original_objects']}"}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_tool_derivations.json',dict(derived=tools,no_runtime_ROM_or_review_credit=True))
    print('Three B200 source fixture/run/audit tools prepared;native numeric constants unchanged.')
