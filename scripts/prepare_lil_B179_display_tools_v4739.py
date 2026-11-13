"""Prepare complete14-panel B179 cold boots and source-bound actual audit."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B179_display_tools_v4739')
assert not ROOT.exists()
tools=[derive('scripts/research_lil_B178_display_fixture_v4691.py','scripts/research_lil_B179_display_fixture_v4739.py',{
    'B178':'B179','display_fixture_v4691':'display_fixture_v4739',
    'all_routes_combined_v4655':'all_routes_combined_v4701','relocation_v4681':'relocation_v4729',
    'bank[178]':'bank[179]','source_block=178':'source_block=179',
    'len(speeches)==13':'len(speeches)==14',
    '[0xA000,0xC200,0]':'[0xA000,0]',
    "sum(c['word']==0xC200 for c in walk)==1":"sum(c['word']==0xC200 for c in walk)==0",
    'display_v4691':'display_v4739','all13_speeches12_progressive1':'all14_speeches13_progressive1',
    'FE_one_source_A000_C200_single_end':'FE_one_source_A000_single_end_no_C200',
    'closing_notice_names_Amsterdam_without_proving':'closing_notice_names_Sao_Jorge_without_proving',
    'source_event178_not_selected':'source_event179_not_selected',
    'stored_speech_objects=13':'stored_speech_objects=14',
    'twelve progressive/one impersonal FE,one source A000,C200 and single end.':
        'thirteen progressive/one impersonal FE,one source A000,single end and no C200.',
})]
tools.append(derive('scripts/run_lil_B178_display_fixture_v4693.py','scripts/run_lil_B179_display_fixture_v4741.py',{
    'B178':'B179','display_fixture_v4691':'display_fixture_v4739',
    'display_run_v4693':'display_run_v4741','display_v4693':'display_v4741',
    'source_event178_not_selected':'source_event179_not_selected',
    "'displayed_original_source_block':178":"'displayed_original_source_block':179",
    'all_source16_commands_12_progressive1':'all_source16_commands_13_progressive1',
    'FE_A000_C200_and_single_end':'FE_A000_and_single_end_no_C200',
}))
source=Path('scripts/audit_lil_B178_actual_v4694b.py');text=source.read_text(encoding='utf-8')
old_ui="""        assert len(ui)==1 and ui[0]['original_source_offset']==488 and ui[0]['result_words']==[3,0]
        assert intervals[-1]['returned']<=ui[0]['start']<=ui[0]['returned']<=selected[-1]['start']"""
new_ui="""        assert ui==[]
        assert intervals[-1]['returned']<=selected[-1]['start']"""
tools.append(derive(source,'scripts/audit_lil_B179_actual_v4742.py',{
    old_ui:new_ui,'source_C200=ui[0]':'source_C200=ui',
    'B178':'B179','actual_v4694':'actual_v4742',
    'display_fixture_v4691':'display_fixture_v4739','native_approval_v4678':'native_approval_v4726',
    'display_run_v4693':'display_run_v4741','display_v4693':'display_v4741',
    'all13_native_progressive':'all14_native_progressive',
    'source_event178_not_selected':'source_event179_not_selected',
    "source['block']!=178":"source['block']!=179",'original_source_block=178':'original_source_block=179',
    "r.get('original_source_block')==178":"r.get('original_source_block')==179",
    "selected[-1]['original_source_offset']==490":"selected[-1]['original_source_offset']==508",
    'single_source_end490_actually_reached':'single_source_end508_actually_reached',
    'all_source16_commands_12_progressive1':'all_source16_commands_13_progressive1',
    'FE_A000_C200_and_single_end':'FE_A000_and_single_end_no_C200',
    "len(intervals)==len({r['id'] for r in intervals})==13":"len(intervals)==len({r['id'] for r in intervals})==14",
    'len(actual)==13':'len(actual)==14','actual_all13_progressive':'actual_all14_progressive',
    'fresh_actual_unique_speech_panels=13':'fresh_actual_unique_speech_panels=14',
    'all13_speeches12_progressive1':'all14_speeches13_progressive1',
    'source_A000_C200_and_single_end_actually_executed_without_source_omission':
        'source_A000_and_single_end_actually_executed_without_source_omission_no_C200',
    'FE_A000_C200_and_single_end.json':'FE_A000_and_single_end_no_C200.json',
    'actual_source_event178_not_selected':'actual_source_event179_not_selected','actual_panels=13':'actual_panels=14',
}))
pin_source=Path('scripts/pin_lil_B178_display_v4692.py');pin_text=pin_source.read_text(encoding='utf-8')
start=pin_text.index("tool=derive(");end=pin_text.index('fixture_path=',start)
tools.append(derive(pin_source,'scripts/pin_lil_B179_display_v4740.py',{
    pin_text[start:end]:'tool=None\n',
    'B178':'B179','display_tools_v4692':'display_tools_v4740','display_fixture_v4691':'display_fixture_v4739',
    'source_speeches=13,progressive=12':'source_speeches=14,progressive=13',
    'Pin both complete B179 content fixtures and correct an unexecuted audit summary label.':
        'Pin both complete B179 content fixtures while preserving every earlier ROM.',
    'Corrected13-panel audit summary before execution.':'All14-panel audit counts are source bound;no C200 probe.',
}))
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,source_speeches=14,source_commands=16,fixture_commands=25,
    source_A000=1,original_prelude_A000=4,C200=0,impersonal_FE=1,single_end=508,frames=9001,
    all_source_commands_and_readonly_observer_preserved=True,no_new_ROM_or_emulator_run_yet=True,
    no_new_editorial_credit=True,full_goal_complete=False))
