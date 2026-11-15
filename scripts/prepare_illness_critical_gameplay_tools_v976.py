"""Preflight six disclosed illness/near-death cold-boot samples without editing historical tools."""
from pathlib import Path
from scripts.prepare_physical_fatigue_native_v961 import rendered
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/illness_critical_v976')


def main():
    items=[]
    items.append(rendered('scripts/native_physical_wounds_room_v970.py','scripts/native_illness_critical_room_v976.py',[
        ('wound-panel','illness/near-death-panel'),
        ("CASES={'CamilleWound':(9,2),'JulioWound':(6,2),'CaptainWound':(1,2),'SeraWound':(24,2)}","CASES={'CristinaIllness':(7,2),'ClaudioIllness':(5,2),'CaptainIllness':(1,2),'CamilleCritical':(9,2),'JulioCritical':(6,2),'SeraCritical':(24,2)}"),
        ('physical_wounds_editorial_release','illness_critical_editorial_release'),('synthetic_physical_wounds_room_assignment_fixture','synthetic_illness_critical_room_assignment_fixture')]))
    items.append(rendered('scripts/native_physical_wounds_fixture_v970.py','scripts/native_illness_critical_fixture_v976.py',[
        ('native_physical_wounds_room_v970','native_illness_critical_room_v976'),('physical_wounds_editorial_release','illness_critical_editorial_release'),
        ("CONDITIONS={'CamilleWound':2,'JulioWound':3,'CaptainWound':2,'SeraWound':3}","CONDITIONS={'CristinaIllness':5,'ClaudioIllness':5,'CaptainIllness':5,'CamilleCritical':4,'JulioCritical':4,'SeraCritical':4}"),
        ('synthetic_physical_wounds_late_condition_fixture','synthetic_illness_critical_late_condition_fixture'),('no_earned_wound_or_recovery_claim','no_earned_illness_critical_condition_or_recovery_claim')]))
    items.append(rendered('scripts/run_physical_wounds_adapter_v970.py','scripts/run_illness_critical_adapter_v976.py',[
        ('physical_wounds','illness_critical'),('native_illness_critical_fixture_v970','native_illness_critical_fixture_v976'),('physical-wounds','illness-critical'),
        ('declared wound condition2/3','declared illness/near-death condition4/5')]))
    items.append(rendered('scripts/native_physical_wounds_standoff_v970.py','scripts/native_illness_critical_standoff_v976.py',[
        ('all_routes_combined_v969','all_routes_combined_v975'),('physical_wounds_editorial_release','illness_critical_editorial_release'),('V969','V975'),('V970','V976')]))
    items.append(rendered('scripts/run_physical_wounds_live_v970.py','scripts/run_illness_critical_live_v976.py',[
        ('physical_wounds','illness_critical'),('run_illness_critical_adapter_v970','run_illness_critical_adapter_v976'),('native_illness_critical_standoff_v970','native_illness_critical_standoff_v976'),
        ('native_illness_critical_room_v970','native_illness_critical_room_v976'),('illness_critical_v970_969','illness_critical_v976_975'),('illness_critical_v970','illness_critical_v976'),
        ('physical-wounds','illness-critical'),('declared_room_assignment_and_late_condition2_3_fixture_plus_two_coordinate_approaches','declared_room_assignment_and_late_condition4_5_fixture_plus_two_coordinate_approaches'),("print('V970'","print('V976'")]))
    items.append(rendered('scripts/navigate_physical_wounds_v970.py','scripts/navigate_illness_critical_v976.py',[
        ('physical_wounds','illness_critical'),('native_illness_critical_room_v970','native_illness_critical_room_v976'),('illness_critical_v970_969','illness_critical_v976_975'),('illness_critical_v970','illness_critical_v976'),
        ('all_routes_combined_v969','all_routes_combined_v975')]))
    items.append(rendered('scripts/physical_wounds_flags_v970.py','scripts/illness_critical_flags_v976.py',[
        ('physical_wounds_layout_v968b','illness_critical_layout_v974'),('all_routes_combined_v969','all_routes_combined_v975'),('V970','V976')]))
    ROOT.mkdir(parents=True,exist_ok=True);provenance=[]
    for source,target,raw,text in items:
        with target.open('x',encoding='utf-8') as f:f.write(text)
        assert source.read_bytes()==raw
        provenance.append({'source':str(source),'source_before_sha256':sha(raw),'source_after_sha256':sha(source.read_bytes()),'source_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes())})
    save(ROOT/'actual_tools_provenance.json',{'files':provenance,'all_replacements_preflighted_before_output':True,
        'only_late_condition4_5_after_Deck_and_declared_room_assignment':True,'actual_scenes_pending':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('Seven historical tools unchanged;six condition4/5 cold-boot sample successors created.',flush=True)


if __name__=='__main__':main()
