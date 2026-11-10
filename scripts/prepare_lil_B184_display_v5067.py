"""Prepare complete paired B184 content fixtures and read-only playback checks."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B184_display_tools_v5067')
if __name__=='__main__':
    assert not ROOT.exists();tools=[]
    tools.append(derive('scripts/research_lil_B183_display_fixture_v4957.py','scripts/research_lil_B184_display_fixture_v5067.py',{
        'B183':'B184','display_fixture_v4957':'display_fixture_v5067','display_v4957':'display_v5067',
        'combined_v4914':'combined_v5030','relocation_v4947':'relocation_v5059','editorial_manuscript_v7':'editorial_manuscript_v4',
        'bank[183]':'bank[184]','source_block=183':'source_block=184','len(commands)==28':'len(commands)==12',
        'len(walk)==37 and len(speeches)==25':'len(walk)==21 and len(speeches)==9',
        "sum(r['source_selector']==254 for r in texts)==2":"sum(r['source_selector']==254 for r in texts)==1",
        'all37_stored_fixture_commands':'all21_stored_fixture_commands','all25_speeches23_progressive2_impersonal_FE':'all9_speeches8_progressive1_impersonal_FE',
        'closing_notice_names_Basra':'closing_notice_names_Sofala','source_event183_not_selected':'source_event184_not_selected',
        'source_all28_commands':'source_all12_commands','both_source_FE_sound_and_notice_remain_impersonal':'source_FE_notice_remains_impersonal',
        'stored_speech_objects=25':'stored_speech_objects=9',
        'all28 commands+9 original init commands,23 progressive/two impersonal FE':'all12 commands+9 original init commands,8 progressive/one impersonal FE'}))
    tools.append(derive('scripts/pin_lil_B183_display_v4958.py','scripts/pin_lil_B184_display_v5068.py',{
        'B183':'B184','display_tools_v4958':'display_tools_v5068','display_fixture_v4957':'display_fixture_v5067',
        'source_speeches=25,progressive=23,FE=2':'source_speeches=9,progressive=8,FE=1',
        'source_commands=28,stored_fixture_commands=37':'source_commands=12,stored_fixture_commands=21','frames=11001':'frames=9001','All25 panels':'All9 panels'}))
    tools.append(derive('scripts/run_lil_B183_display_fixture_v4959.py','scripts/run_lil_B184_display_fixture_v5069.py',{
        'B183':'B184','display_fixture_v4957':'display_fixture_v5067','display_run_v4959':'display_run_v5069','display_v4959':'display_v5069',
        'source_event183_not_selected':'source_event184_not_selected',"'displayed_original_source_block':183":"'displayed_original_source_block':184",
        'all_source28_commands_23_progressive2_FE_A000_C200_end_retained':'all_source12_commands_8_progressive1_FE_A000_C200_end_retained',
        'range(2600,10501,240)':'range(2600,8501,240)',"'requested_frames':11001":"'requested_frames':9001",
        '"\'--frames\',\'11001\'"':'"\'--frames\',\'9001\'"','range(2350,11001,60)':'range(2350,9001,60)'}))
    tools.append(derive('scripts/audit_lil_B183_actual_v4960.py','scripts/audit_lil_B184_actual_v5070.py',{
        'B183':'B184','actual_v4960':'actual_v5070','display_fixture_v4957':'display_fixture_v5067',
        'fonts_v4945/all25_progressive_FE_native_planes_and200_alignment_cases':'fonts_v5054/all9_progressive_FE_native_planes_and72_alignment_cases',
        'display_run_v4959':'display_run_v5069','display_v4959':'display_v5069',"report['frames']==11001":"report['frames']==9001",
        'source_event183_not_selected':'source_event184_not_selected','all_source28_commands_23_progressive2':'all_source12_commands_8_progressive1',
        "source['block']!=183":"source['block']!=184",'original_source_block=183':'original_source_block=184',
        "r.get('original_source_block')==183":"r.get('original_source_block')==184",
        'len(selected)==len(expected)==37':'len(selected)==len(expected)==21',
        "len(intervals)==len({r['id'] for r in intervals})==25":"len(intervals)==len({r['id'] for r in intervals})==9",
        "sum(r['prefix']==254 for r in intervals)==2":"sum(r['prefix']==254 for r in intervals)==1",
        "selected[-1]['original_source_offset']==952":"selected[-1]['original_source_offset']==428",
        "ui[0]['original_source_offset']==950":"ui[0]['original_source_offset']==426",
        'single_source_end952':'single_source_end428',"len(actual)==25 and sum(r['prefix']==254 for r in actual)==2":"len(actual)==9 and sum(r['prefix']==254 for r in actual)==1",
        'actual_all25':'actual_all9','fresh_actual_unique_speech_panels=25':'fresh_actual_unique_speech_panels=9',
        'frames_per_boot=11001':'frames_per_boot=9001','all28_source_commands_stored_and_all37_fixture_commands':'all12_source_commands_stored_and_all21_fixture_commands',
        'all25_speeches23_progressive2_impersonal_FE':'all9_speeches8_progressive1_impersonal_FE',
        'actual_source_event183':'actual_source_event184','actual_panels=25,FE=2':'actual_panels=9,FE=1'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=tools,source_commands=12,stored_fixture_commands=21,
        speeches=9,progressive=8,FE=1,source_A000=1,prelude_A000=4,C200=1,single_end=True,
        frames_per_boot=9001,original_readonly_observer_reused=True,new_ROM_or_emulator_run_yet=False,new_review_credit=0,full_goal_complete=False))
