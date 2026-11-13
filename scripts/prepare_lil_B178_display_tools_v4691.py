"""Prepare complete B178 content fixtures,cold boots and native-plane execution audit."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B178_display_tools_v4691');assert not ROOT.exists()
tools=[derive('scripts/research_lil_B177_display_fixture_v4635.py','scripts/research_lil_B178_display_fixture_v4691.py',{
    'B177':'B178','lil_B177':'lil_B178','display_fixture_v4635':'display_fixture_v4691',
    'all_routes_combined_v4595':'all_routes_combined_v4655','relocation_v4625':'relocation_v4681',
    'editorial_manuscript_v5':'editorial_manuscript_v3','bank[177]':'bank[178]',
    'len(commands)==13':'len(commands)==16','len(walk)==22 and len(speeches)==10':'len(walk)==25 and len(speeches)==13',
    'source_block=177':'source_block=178','display_v4635':'display_v4691',
    'all22_stored_fixture_commands':'all25_stored_fixture_commands',
    'all10_speeches9_progressive1':'all13_speeches12_progressive1',
    'closing_notice_names_Genoa_without_proving_earlier_scene_location_initialized_fixture_town_is_Amsterdam':
        'closing_notice_names_Amsterdam_without_proving_earlier_scene_location_initialized_fixture_town_is_Amsterdam',
    'source_event177_not_selected':'source_event178_not_selected','source_all13_commands':'source_all16_commands',
    'stored_speech_objects=10':'stored_speech_objects=13',
    'fixtures retain all13 commands+9 original init commands,nine progressive':'fixtures retain all16 commands+9 original init commands,twelve progressive',
})]
tools.append(derive('scripts/run_lil_B177_display_fixture_v4637.py','scripts/run_lil_B178_display_fixture_v4693.py',{
    'B177':'B178','lil_B177':'lil_B178','display_fixture_v4635':'display_fixture_v4691',
    'display_run_v4637':'display_run_v4693','display_v4637':'display_v4693',
    'source_event177_not_selected':'source_event178_not_selected',
    "'displayed_original_source_block':177":"'displayed_original_source_block':178",
    'all_source13_commands_9_progressive1':'all_source16_commands_12_progressive1',
}))
tools.append(derive('scripts/audit_lil_B177_actual_v4638.py','scripts/audit_lil_B178_actual_v4694.py',{
    'B177':'B178','lil_B177':'lil_B178','actual_v4638':'actual_v4694',
    'display_fixture_v4635':'display_fixture_v4691','native_approval_v4622':'native_approval_v4678',
    'display_run_v4637':'display_run_v4693','display_v4637':'display_v4693',
    'all10_native_progressive':'all13_native_progressive',
    'source_event177_not_selected':'source_event178_not_selected',
    "source['block']!=177":"source['block']!=178",'original_source_block=177':'original_source_block=178',
    "r.get('original_source_block')==177":"r.get('original_source_block')==178",
    "selected[-1]['original_source_offset']==482":"selected[-1]['original_source_offset']==490",
    "ui[0]['original_source_offset']==480":"ui[0]['original_source_offset']==488",
    'single_source_end482_actually_reached':'single_source_end490_actually_reached',
    'all_source13_commands_9_progressive1':'all_source16_commands_12_progressive1',
    'len(selected)==len(expected)==22':'len(selected)==len(expected)==25',
    "len(intervals)==len({r['id'] for r in intervals})==10":"len(intervals)==len({r['id'] for r in intervals})==13",
    'len(actual)==10':'len(actual)==13','actual_all10_progressive':'actual_all13_progressive',
    'fresh_actual_unique_speech_panels=10':'fresh_actual_unique_speech_panels=13',
    'all13_source_commands_stored_and_all22_fixture_commands':'all16_source_commands_stored_and_all25_fixture_commands',
    'all10_speeches9_progressive1':'all13_speeches12_progressive1',
}))
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,source_speeches=13,source_commands=16,fixture_commands=25,
    source_A000=1,original_prelude_A000=4,impersonal_FE=1,single_end=490,frames=9001,
    all_source_commands_and_readonly_observer_preserved=True,no_new_ROM_or_emulator_run_yet=True,
    no_new_editorial_credit=True,full_goal_complete=False))
