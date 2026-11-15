"""Preflight disclosed room assignments and late condition2/3 cold-boot fixtures."""
import ast
from pathlib import Path
from scripts.prepare_physical_fatigue_native_v961 import rendered
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/physical_wounds_v970')


def main():
    items=[]
    items.append(rendered('scripts/native_battle_gunnery_deck_fixture_v955.py','scripts/native_physical_wounds_room_v970.py',[
        ('Gunnery/DeckCleaning','wound-panel'),
        ("CASES={'CamilleGunnery':(9,8),'YukihisaDeck':(12,2),'EmilioDeck':(14,2),'CaptainDeck':(1,2)}","CASES={'CamilleWound':(9,2),'JulioWound':(6,2),'CaptainWound':(1,2),'SeraWound':(24,2)}"),
        ('battle_gunnery_deck_editorial_release','physical_wounds_editorial_release'),('synthetic_battle_gunnery_deck_assignment_fixture','synthetic_physical_wounds_room_assignment_fixture')]))
    items.append(rendered('scripts/native_physical_fatigue_fixture_v964.py','scripts/native_physical_wounds_fixture_v970.py',[
        ('native_physical_fatigue_fixture_v963','native_physical_wounds_room_v970'),('physical_fatigue_editorial_release','physical_wounds_editorial_release'),
        ('CASES=initial.CASES',"CASES=initial.CASES\nCONDITIONS={'CamilleWound':2,'JulioWound':3,'CaptainWound':2,'SeraWound':3}"),
        ("label=request['case'];assert label in CASES and len(raw)==0x400000","label=request['case'];assert label in CASES and len(raw)==0x400000;status=CONDITIONS[label]"),
        ('assert condition in (0,1)','assert condition==0'),('after[obj-BASE+6]=1','after[obj-BASE+6]=status'),
        ("'after':1}] if condition!=1 else []","'after':status}]"),
        ("before[:6]+b'\\x01'+before[7:]","before[:6]+bytes([status])+before[7:]"),('verify(0x7E100,obj)==1','verify(0x7E100,obj)==status'),
        ('synthetic_physical_fatigue_late_condition_fixture','synthetic_physical_wounds_late_condition_fixture'),("'fixture_condition':1","'fixture_condition':status"),('no_earned_fatigue_or_recovery_claim','no_earned_wound_or_recovery_claim')]))
    items.append(rendered('scripts/run_physical_fatigue_adapter_v964.py','scripts/run_physical_wounds_adapter_v970.py',[
        ('native_physical_fatigue_fixture_v964','native_physical_wounds_fixture_v970'),('physical_fatigue','physical_wounds'),('physical-fatigue','physical-wounds'),
        ('fatigue condition1','declared wound condition2/3'),('fatigue credit','injury credit')]))
    items.append(rendered('scripts/native_physical_fatigue_standoff_v963.py','scripts/native_physical_wounds_standoff_v970.py',[
        ('all_routes_combined_v962','all_routes_combined_v969'),('physical_fatigue_editorial_release','physical_wounds_editorial_release'),('V962','V969'),('V963','V970')]))
    items.append(rendered('scripts/run_physical_fatigue_live_v964.py','scripts/run_physical_wounds_live_v970.py',[
        ('run_physical_fatigue_adapter_v964','run_physical_wounds_adapter_v970'),('native_physical_fatigue_standoff_v963','native_physical_wounds_standoff_v970'),
        ('native_physical_fatigue_fixture_v963','native_physical_wounds_room_v970'),('physical_fatigue_v964_962','physical_wounds_v970_969'),('physical_fatigue_v964','physical_wounds_v970'),
        ('physical-fatigue','physical-wounds'),('declared_room_early_condition_and_late_condition1_fixtures_plus_two_coordinate_approaches','declared_room_assignment_and_late_condition2_3_fixture_plus_two_coordinate_approaches'),("print('V964'","print('V970'")]))
    items.append(rendered('scripts/navigate_physical_fatigue_v964.py','scripts/navigate_physical_wounds_v970.py',[
        ('native_physical_fatigue_fixture_v963','native_physical_wounds_room_v970'),('physical_fatigue_v964_962','physical_wounds_v970_969'),('physical_fatigue_v964','physical_wounds_v970'),
        ('all_routes_combined_v962','all_routes_combined_v969'),('physical_fatigue_fixture','physical_wounds_fixture')]))
    items.append(rendered('scripts/physical_fatigue_flags_v963.py','scripts/physical_wounds_flags_v970.py',[
        ('physical_fatigue_layout_v960','physical_wounds_layout_v968b'),('all_routes_combined_v962','all_routes_combined_v969'),('V963','V970')]))
    source=Path('scripts/verify_physical_fatigue_gameplay_v964.py').read_text(encoding='utf-8')
    start=source.index("    assert layout(rows[1783]");end=source.index('    sheet=Image.new',start)
    final_asserts="""    assert layout(rows[1796]['english'])==["I'm all right...","It's not a serious wound..."]
    assert layout(rows[1799]['english'])==["I'm in a bad way...","This wound's sapping my strength..."]
    assert len(layout(rows[1799]['english'])[1])==35
    assert layout(rows[1803]['english'])==["A scratch won't stop me."]
    assert layout(rows[1806]['english'])==["Don't worry.","It's not a serious wound..."]
"""
    scope_start=source.index("        'scope':");scope_end=source.index("        'producer_sha256':",scope_start)
    scope="""        'scope':'Four separate V969 fresh cold boots:Camille9 condition2 wound1796,Julio6 condition3 wound1799,genuine captain1 condition2 retained1803,and Sera24 condition3 special1806. Two full native bitmap/actual RGB holds and normal return per case. Room assignment only after observed original combat0/1;one explicitly bounded actor condition byte6 is inserted after Deck opens,before selecting the officer. Two coordinate approaches. No savestate,actor/captain identity replacement,battle-mode/outcome/money/text/code injection or earned injury/recruitment/refit claim. Other nine entries,including Rafael1802 and Lil1804,have complete source/native-font proof rather than individual actual visits. No full-route,hardware,clinical grade or recovery-effect guarantee.',
"""
    items.append(rendered('scripts/verify_physical_fatigue_gameplay_v964.py','scripts/verify_physical_wounds_gameplay_v970.py',[
        ('physical_fatigue_flags_v963','physical_wounds_flags_v970'),('physical_fatigue_layout_v960','physical_wounds_layout_v968b'),('physical_fatigue_v964_962','physical_wounds_v970_969'),('physical_fatigue_v964','physical_wounds_v970'),
        ('all_routes_combined_v962','all_routes_combined_v969'),('physical_fatigue_editorial_manuscript','physical_wounds_editorial_manuscript'),
        ("SPECS={'CamilleFatigue':(1783,9,2,False),'CristinaFatigue':(1784,7,2,False),'CaptainFatigue':(1790,1,2,True),'SeraFatigue':(1793,24,2,False)}","SPECS={'CamilleWound':(1796,9,2,False,2),'JulioWound':(1799,6,2,False,3),'CaptainWound':(1803,1,2,True,2),'SeraWound':(1806,24,2,False,3)}"),
        ('(number,actor,role,owned)','(number,actor,role,owned,expected_condition)'),('physical_fatigue_Cabin_assignment_fixtures','physical_wounds_Cabin_assignment_fixtures'),('synthetic_physical_fatigue_late_condition_fixture','synthetic_physical_wounds_late_condition_fixture'),
        ("late['fixture_condition']==1","late['fixture_condition']==expected_condition"),('len(late[\'changes\'])==(0 if owned else 1)',"len(late['changes'])==1"),
        ("and fixture['fixture_condition']==1",''),('len(fixture[\'changes\'])==(4 if owned else 3)',"len(fixture['changes'])==(3 if owned else 2)"),
        ("fixture['other31_actor_bytes_exact'] and fixture['all_other4MiB_RAM_including_other31_actor_bytes_captain_identity_battle_money_calendar_RNG_text_code_exact']","fixture['all_other4MiB_RAM_including_battle_mode_actor_captain_health_money_calendar_RNG_text_code_exact']"),
        ('get(0x7E100,obj)==1','get(0x7E100,obj)==expected_condition'),('actual_physical_condition_ID=1','actual_physical_condition_ID=expected_condition'),
        ("'room_and_condition_fixture':fixture","'room_assignment_fixture':fixture"),
        ("if label=='CristinaFatigue':cells.append((1,0,'delete-Recreation-Room-row-initial-i'))","if label=='JulioWound':cells.append((1,0,'delete-strength-continuation-T'))"),
        ("if label=='CamilleFatigue':cells.append((0,len(lines[0])-4,'delete-rest-final-t'))","if label=='CamilleWound':cells.append((1,0,'delete-reassurance-continuation-I'))"),
        ("if label=='SeraFatigue':cells.append((0,4,'delete-first-person-I'))","if label=='SeraWound':cells.append((1,0,'delete-Sera-continuation-I'))"),
        (source[start:end],final_asserts),('eight_complete_actual_fatigue_holds','eight_complete_actual_wound_holds'),
        ('Camille_ASCII_I_Cristina_Recreation_Room_genuine_captain_and_Sera_special_pass','Camille_ASCII_I_Julio35cell_continuation_genuine_captain_and_Sera_special_pass'),
        (source[scope_start:scope_end],scope),('Eight complete fatigue holds','Eight complete wound holds')]))
    ROOT.mkdir(parents=True,exist_ok=True);provenance=[]
    for source,target,raw,text in items:
        ast.parse(text)
        with target.open('x',encoding='utf-8') as f:f.write(text)
        assert source.read_bytes()==raw
        provenance.append({'source':str(source),'source_before_sha256':sha(raw),'source_after_sha256':sha(source.read_bytes()),'source_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes())})
    save(ROOT/'actual_tools_provenance.json',{'files':provenance,'all_replacements_preflighted_before_output':True,
        'only_late_condition2_3_tag_after_Deck_and_declared_room_assignment':True,'actual_scenes_pending':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('Eight historical tools unchanged;wound cold-boot successors and late condition2/3 fixture created.',flush=True)


if __name__=='__main__':main()
