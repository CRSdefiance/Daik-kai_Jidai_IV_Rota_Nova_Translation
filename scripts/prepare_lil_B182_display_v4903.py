"""Prepare complete conditional B182 content fixtures and actual native-plane audit."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B182_display_tools_v4903')
if __name__=='__main__':
    assert not ROOT.exists();tools=[]
    tools.append(derive('scripts/research_lil_B180_display_fixture_v4808.py','scripts/research_lil_B182_display_fixture_v4903.py',{
        'B180':'B182','display_fixture_v4808':'display_fixture_v4903','display_v4808':'display_v4903',
        'combined_v4766':'combined_v4867','relocation_v4798':'relocation_v4893','bank[180]':'bank[182]',
        'source_block=180':'source_block=182','len(commands)==28':'len(commands)==25',
        'len(walk)==37 and len(speeches)==11':'len(walk)==34 and len(speeches)==8',
        'all37_stored_fixture_commands':'all34_stored_fixture_commands',
        'all11_speeches10_progressive1':'all8_speeches7_progressive1','closing_notice_names_Lisbon':'closing_notice_names_London',
        'source_event180_not_selected':'source_event182_not_selected','source_all28_commands':'source_all25_commands',
        'stored_speech_objects=11':'stored_speech_objects=8','all28 commands+9 original init commands,ten progressive':'all25 commands+9 original init commands,seven progressive'}))
    tools.append(derive('scripts/pin_lil_B181_display_v4858.py','scripts/pin_lil_B182_display_v4904.py',{
        'B181':'B182','display_tools_v4858':'display_tools_v4904','display_fixture_v4857':'display_fixture_v4903',
        'source_speeches=10,progressive=9':'source_speeches=8,progressive=7',
        'source_commands=13,stored_fixture_commands=22,source_A000=1':'source_commands=25,stored_fixture_commands=34,source_A000=3',
        'All10 panels':'All8 panels'}))
    tools.append(derive('scripts/run_lil_B180_display_fixture_v4810.py','scripts/run_lil_B182_display_fixture_v4905.py',{
        'B180':'B182','display_fixture_v4808':'display_fixture_v4903','display_run_v4810':'display_run_v4905','display_v4810':'display_v4905',
        'from scripts import observe_lil_B180_v4810 as original':'from scripts import observe_lil_B180_v4810 as original',
        'source_event180_not_selected':'source_event182_not_selected',"'displayed_original_source_block':180":"'displayed_original_source_block':182",
        'all_source28_commands_10_progressive1_FE_two_predicates_ten_branches_three_A000_C200_end_retained':
        'all_source25_commands_7_progressive1_FE_two_predicates_ten_branches_three_A000_C200_end_retained'}))
    tools.append(derive('scripts/audit_lil_B180_actual_v4811c.py','scripts/audit_lil_B182_actual_v4906.py',{
        'B180':'B182','actual_v4811c':'actual_v4906','display_fixture_v4808':'display_fixture_v4903',
        'fonts_v4794/all11_progressive_FE_native_planes_and88_alignment_cases':'fonts_v4891/all8_progressive_FE_native_planes_and64_alignment_cases',
        'display_run_v4810':'display_run_v4905','display_v4810':'display_v4905','source_event180_not_selected':'source_event182_not_selected',
        'all_source28_commands_10_progressive1':'all_source25_commands_7_progressive1',
        "source['block']!=180":"source['block']!=182",'original_source_block=180':'original_source_block=182',
        "r.get('original_source_block')==180":"r.get('original_source_block')==182",
        "pair.get('original_source_block')==180":"pair.get('original_source_block')==182",
        'all37_stored_fixture_commands':'all34_stored_fixture_commands',"==37":"==34",
        "selected[-1]['original_source_offset']==572":"selected[-1]['original_source_offset']==632",
        "len(intervals)==len({r['id'] for r in intervals})==11":"len(intervals)==len({r['id'] for r in intervals})==8",
        "predicates[0]['source_offset']==452":"predicates[0]['source_offset']==512",
        'in [472,504,516]':'in [532,564,576]',"ui[0]['original_source_offset']==570":"ui[0]['original_source_offset']==630",
        'single_source_end572':'single_source_end632','len(actual)==11':'len(actual)==8',
        'actual_all11':'actual_all8','fresh_actual_unique_speech_panels=11':'fresh_actual_unique_speech_panels=8',
        'all28_source_commands':'all25_source_commands','all11_speeches10_progressive1':'all8_speeches7_progressive1',
        'actual_source_event180':'actual_source_event182','actual_panels=11':'actual_panels=8'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=tools,source_commands=25,stored_fixture_commands=34,
        speeches=8,progressive=7,FE=1,predicates=2,relative_sites=10,source_A000=3,prelude_A000=4,C200=1,end=True,
        frames_per_boot=9001,readonly_observer_reused=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Prepared complete B182 fixtures,paired cold boots and eight-panel actual display/conditional audit.')
