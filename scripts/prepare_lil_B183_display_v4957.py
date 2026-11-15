"""Prepare complete B183 paired content boots with enough input for all25 panels."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B183_display_tools_v4957')
if __name__=='__main__':
    assert not ROOT.exists();tools=[]
    tools.append(derive('scripts/research_lil_B181_display_fixture_v4857.py','scripts/research_lil_B183_display_fixture_v4957.py',{
        'B181':'B183','display_fixture_v4857':'display_fixture_v4957','display_v4857':'display_v4957',
        'combined_v4821':'combined_v4914','relocation_v4846':'relocation_v4947','editorial_manuscript_v3':'editorial_manuscript_v7',
        'bank[181]':'bank[183]','source_block=181':'source_block=183','len(commands)==13':'len(commands)==28',
        'len(walk)==22 and len(speeches)==10':'len(walk)==37 and len(speeches)==25',
        "sum(r['source_selector']==254 for r in texts)==1":"sum(r['source_selector']==254 for r in texts)==2",
        'all22_stored_fixture_commands':'all37_stored_fixture_commands','all10_speeches9_progressive1_impersonal_FE':'all25_speeches23_progressive2_impersonal_FE',
        'closing_notice_names_Athens':'closing_notice_names_Basra','source_event181_not_selected':'source_event183_not_selected',
        'source_all13_commands':'source_all28_commands','source_FE_notice_remains_impersonal':'both_source_FE_sound_and_notice_remain_impersonal',
        'stored_speech_objects=10':'stored_speech_objects=25',
        'all13 commands+9 original init commands,nine progressive/one impersonal FE':'all28 commands+9 original init commands,23 progressive/two impersonal FE'}))
    tools.append(derive('scripts/pin_lil_B181_display_v4858.py','scripts/pin_lil_B183_display_v4958.py',{
        'B181':'B183','display_tools_v4858':'display_tools_v4958','display_fixture_v4857':'display_fixture_v4957',
        'source_speeches=10,progressive=9,FE=1':'source_speeches=25,progressive=23,FE=2',
        'source_commands=13,stored_fixture_commands=22':'source_commands=28,stored_fixture_commands=37','frames=9001':'frames=11001','All10 panels':'All25 panels'}))
    tools.append(derive('scripts/run_lil_B181_display_fixture_v4860.py','scripts/run_lil_B183_display_fixture_v4959.py',{
        'B181':'B183','display_fixture_v4857':'display_fixture_v4957','display_run_v4860':'display_run_v4959','display_v4860':'display_v4959',
        'source_event181_not_selected':'source_event183_not_selected',"'displayed_original_source_block':181":"'displayed_original_source_block':183",
        'all_source13_commands_9_progressive1_FE_A000_C200_end_retained':'all_source28_commands_23_progressive2_FE_A000_C200_end_retained',
        'range(2600,8501,240)':'range(2600,10501,240)',"'requested_frames':9001":"'requested_frames':11001",
        '"\'--frames\',\'9001\'"':'"\'--frames\',\'11001\'"','range(2350,9001,60)':'range(2350,11001,60)'}))
    tools.append(derive('scripts/audit_lil_B181_actual_v4861.py','scripts/audit_lil_B183_actual_v4960.py',{
        'B181':'B183','actual_v4861':'actual_v4960','display_fixture_v4857':'display_fixture_v4957',
        'fonts_v4844/all10_progressive_FE_native_planes_and80_alignment_cases':'fonts_v4945/all25_progressive_FE_native_planes_and200_alignment_cases',
        'display_run_v4860':'display_run_v4959','display_v4860':'display_v4959',"report['frames']==9001":"report['frames']==11001",
        'source_event181_not_selected':'source_event183_not_selected','all_source13_commands_9_progressive1':'all_source28_commands_23_progressive2',
        "source['block']!=181":"source['block']!=183",'original_source_block=181':'original_source_block=183',
        "r.get('original_source_block')==181":"r.get('original_source_block')==183",
        'len(selected)==len(expected)==22':'len(selected)==len(expected)==37',
        "len(intervals)==len({r['id'] for r in intervals})==10":"len(intervals)==len({r['id'] for r in intervals})==25",
        "sum(r['prefix']==254 for r in intervals)==1":"sum(r['prefix']==254 for r in intervals)==2",
        "selected[-1]['original_source_offset']==392":"selected[-1]['original_source_offset']==952",
        "ui[0]['original_source_offset']==390":"ui[0]['original_source_offset']==950",
        'single_source_end392':'single_source_end952',"len(actual)==10 and sum(r['prefix']==254 for r in actual)==1":"len(actual)==25 and sum(r['prefix']==254 for r in actual)==2",
        'actual_all10':'actual_all25','fresh_actual_unique_speech_panels=10':'fresh_actual_unique_speech_panels=25',
        'frames_per_boot=9001':'frames_per_boot=11001','all13_source_commands_stored_and_all22_fixture_commands':'all28_source_commands_stored_and_all37_fixture_commands',
        'all10_speeches9_progressive1_impersonal_FE':'all25_speeches23_progressive2_impersonal_FE',
        'actual_source_event181':'actual_source_event183','actual_panels=10,FE=1':'actual_panels=25,FE=2'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=tools,source_commands=28,stored_fixture_commands=37,
        speeches=25,progressive=23,FE=2,source_A000=1,prelude_A000=4,C200=1,single_end=True,
        frames_per_boot=11001,A_schedule_extends_through10480_with_final_panel_advances=True,
        original_readonly_observer_reused=True,no_new_ROM_or_emulator_run_yet=True,new_review_credit=0,full_goal_complete=False))
    print('Prepared B183 complete fixtures,11001-frame paired cold boots and25-panel actual audit;no commands omitted.')
