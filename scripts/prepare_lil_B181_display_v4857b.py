"""Prepare complete B181 content cold boots and actual current-font audit."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive as original_derive
import re
from dk4tool.patch.grand_race_menu_release import sha
def derive(a,b,changes):
    if not Path(b).exists():return original_derive(a,b,changes)
    old=Path(a).read_text(encoding='utf-8')
    for key in changes:assert key in old,key
    expected=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],old)
    assert Path(b).read_text(encoding='utf-8')==expected
    return dict(previous=str(a),previous_sha256=sha(Path(a).read_bytes()),successor=str(b),successor_sha256=sha(Path(b).read_bytes()),exact_existing_prepared_tool_reused=True)

from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B181_display_tools_v4857')
if __name__=='__main__':
    assert not ROOT.exists();tools=[]
    tools.append(derive('scripts/research_lil_B178_display_fixture_v4691.py','scripts/research_lil_B181_display_fixture_v4857.py',{
        'B178':'B181','display_fixture_v4691':'display_fixture_v4857','display_v4691':'display_v4857','combined_v4655':'combined_v4821',
        'relocation_v4681':'relocation_v4846','bank[178]':'bank[181]','source_block=178':'source_block=181',
        'len(commands)==16':'len(commands)==13','len(walk)==25 and len(speeches)==13':'len(walk)==22 and len(speeches)==10',
        'all25_stored_fixture_commands':'all22_stored_fixture_commands','all13_speeches12_progressive1':'all10_speeches9_progressive1',
        'closing_notice_names_Amsterdam':'closing_notice_names_Athens','source_event178_not_selected':'source_event181_not_selected',
        'source_all16_commands':'source_all13_commands','stored_speech_objects=13':'stored_speech_objects=10',
        'all16 commands+9 original init commands,twelve progressive':'all13 commands+9 original init commands,nine progressive'}))
    tools.append(derive('scripts/pin_lil_B179_display_v4740.py','scripts/pin_lil_B181_display_v4858.py',{
        'B179':'B181','display_tools_v4740':'display_tools_v4858','display_fixture_v4739':'display_fixture_v4857',
        'source_speeches=14,progressive=13':'source_speeches=10,progressive=9',
        'source_commands=16,stored_fixture_commands=25':'source_commands=13,stored_fixture_commands=22',
        'All14-panel audit counts are source bound;no C200 probe.':'All10 panels and original A000/C200/end retained;actual observation pending.'}))
    tools.append(derive('scripts/run_lil_B180_display_fixture_v4810.py','scripts/run_lil_B181_display_fixture_v4860.py',{
        'B180':'B181','display_fixture_v4808':'display_fixture_v4857','display_run_v4810':'display_run_v4860','display_v4810':'display_v4860',
        'source_event180_not_selected':'source_event181_not_selected',"'displayed_original_source_block':180":"'displayed_original_source_block':181",
        'all_source28_commands_10_progressive1_FE_two_predicates_ten_branches_three_A000_C200_end_retained':
        'all_source13_commands_9_progressive1_FE_A000_C200_end_retained',
        'from scripts import observe_lil_B180_v4810 as original':'from scripts import observe_lil_B180_v4810 as original'}))
    tools.append(derive('scripts/audit_lil_B178_actual_v4694b.py','scripts/audit_lil_B181_actual_v4861.py',{
        'B178':'B181','actual_v4694':'actual_v4861','display_fixture_v4691':'display_fixture_v4857',
        'work/analysis/lil_B178_native_approval_v4678/all13_native_progressive_FE_and_source_reconciliation.json':
        'work/analysis/lil_B181_fonts_v4844/all10_progressive_FE_native_planes_and80_alignment_cases.json',
        'display_run_v4693':'display_run_v4860','display_v4693':'display_v4860',
        'source_event178_not_selected':'source_event181_not_selected',
        'all_source16_commands_12_progressive1_impersonal_FE_A000_C200_and_single_end_retained':
        'all_source13_commands_9_progressive1_FE_A000_C200_end_retained',
        "source['block']!=178":"source['block']!=181",'original_source_block=178':'original_source_block=181',
        "r.get('original_source_block')==178":"r.get('original_source_block')==181",
        "extent=row['decoded_length'],result_words=row['result_words'])":
        "extent=row['decoded_length'],result_words=row['result_words'],before_seed=entry['original_RNG_seed'],after_seed=row['original_RNG_seed'],UI_request_after=row['native_UI_request_words'],UI_pending_after=row['native_UI_pending_flag'])",
        'len(selected)==len(expected)==25':'len(selected)==len(expected)==22',
        "len(intervals)==len({r['id'] for r in intervals})==13":"len(intervals)==len({r['id'] for r in intervals})==10",
        "selected[-1]['original_source_offset']==490":"selected[-1]['original_source_offset']==392",
        "ui[0]['original_source_offset']==488":"ui[0]['original_source_offset']==390",
        'single_source_end490_actually_reached':'single_source_end392_actually_reached',
        'len(actual)==13':'len(actual)==10','actual_all13':'actual_all10','fresh_actual_unique_speech_panels=13':'fresh_actual_unique_speech_panels=10',
        'all16_source_commands_stored_and_all25_fixture_commands_actually_selected':'all13_source_commands_stored_and_all22_fixture_commands_actually_selected',
        'all13_speeches12_progressive1':'all10_speeches9_progressive1','actual_source_event178_not_selected':'actual_source_event181_not_selected',
        'actual_panels=13':'actual_panels=10'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=tools,
        complete_source_commands=13,stored_fixture_commands=22,speeches=10,progressive=9,FE=1,A000=5,C200=1,single_end=True,
        original_shared_readonly_observer_with_RNG_and_UI_boundary_fields_reused=True,frames_per_boot=9001,
        no_new_ROM_or_emulator_run_yet=True,no_review_credit=True,full_goal_complete=False))
    print('Prepared complete B181 fixtures,paired cold boots and ten-panel current-font audit.')
