"""Create explicitly disclosed fatigue fixtures and cold-boot successors."""
from pathlib import Path
from scripts.prepare_physical_fatigue_native_v961 import rendered
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/physical_fatigue_v963')


def main():
    pairs=[
        ('scripts/native_battle_gunnery_deck_fixture_v955.py','scripts/native_physical_fatigue_fixture_v963.py',[
            ('Bounded Gunnery/DeckCleaning room fixture;all actors,battle mode and resources retained.','Bounded room fixture plus source-proven condition1 byte;other actor bytes and resources retained.'),
            ("CASES={'CamilleGunnery':(9,8),'YukihisaDeck':(12,2),'EmilioDeck':(14,2),'CaptainDeck':(1,2)}","CASES={'CamilleFatigue':(9,2),'CristinaFatigue':(7,2),'CaptainFatigue':(1,2),'SeraFatigue':(24,2)}"),
            ('battle_gunnery_deck_editorial_release','physical_fatigue_editorial_release'),
            ('fields=[(model+0x1E+12,role)]','before_actor=bytes(cpu.mem_read(obj,32));assert arm[0x7E100:0x7E108]==bytes.fromhex("0600d0e51eff2fe1")\n    fields=[(model+0x1E+12,role),(obj+6,1)]'),
            ("    assert sum(a!=b for a,b in zip(raw,after,strict=True))==len(fields)","    assert sum(a!=b for a,b in zip(raw,after,strict=True))==len(fields)\n    assert bytes(after[obj-BASE:obj-BASE+32])==before_actor[:6]+b'\\x01'+before_actor[7:]\n    check,get_after=get_machine(arm,bytes(after));assert get_after(0x7E100,obj)==1\n    assert get_after(0x7F244)==hero and get_after(0x81F54,controller,actor)==role"),
            ('synthetic_battle_gunnery_deck_assignment_fixture','synthetic_physical_fatigue_assignment_and_condition_fixture'),
            ("'source_condition':condition,'source_mood':mood","'source_condition':condition,'fixture_condition':1,'condition_address':obj+6,'other31_actor_bytes_exact':True,'source_mood':mood"),
            ('all_other4MiB_RAM_including_battle_mode_actor_captain_health_money_calendar_RNG_text_code_exact','all_other4MiB_RAM_including_other31_actor_bytes_captain_identity_battle_money_calendar_RNG_text_code_exact'),
            ('no_earned_refit_assignment_or_recruitment_claim','no_earned_fatigue_refit_assignment_or_recruitment_claim')]),
        ('scripts/run_battle_gunnery_deck_adapter_v955.py','scripts/run_physical_fatigue_adapter_v963.py',[
            ('native_battle_gunnery_deck_fixture_v955','native_physical_fatigue_fixture_v963'),('battle_gunnery_deck','physical_fatigue'),('battle-gunnery-deck','physical-fatigue'),
            ('Isolated Cabin occupant applied;no earned assignment or recruitment credit.','Isolated Cabin occupant and fatigue condition1 applied;no earned assignment,recruitment or fatigue credit.'),
            ('Allow only the declared two/three room and occupant bytes in the disposable test.','Allow only three/four declared room,occupant and physical-condition bytes in this disposable test.')]),
        ('scripts/native_battle_standoff_v955.py','scripts/native_physical_fatigue_standoff_v963.py',[
            ('all_routes_combined_v954','all_routes_combined_v962'),('battle_gunnery_deck_editorial_release','physical_fatigue_editorial_release'),('V954','V962'),('V955','V963')]),
        ('scripts/run_battle_gunnery_deck_live_v955.py','scripts/run_physical_fatigue_live_v963.py',[
            ('run_battle_gunnery_deck_adapter_v955','run_physical_fatigue_adapter_v963'),('native_battle_standoff_v955','native_physical_fatigue_standoff_v963'),
            ('native_battle_gunnery_deck_fixture_v955','native_physical_fatigue_fixture_v963'),('battle_gunnery_deck_v955_954','physical_fatigue_v963_962'),
            ('battle_gunnery_deck_v955','physical_fatigue_v963'),('battle-gunnery-deck','physical-fatigue'),
            ('two_or_three_room_occupant_bytes_plus_two_existing_coordinate_fixtures_only','three_or_four_room_occupant_and_condition1_bytes_plus_two_existing_coordinate_fixtures_only'),
            ("print('V955'","print('V963'")]),
        ('scripts/battle_gunnery_deck_flags_v955.py','scripts/physical_fatigue_flags_v963.py',[
            ('battle_gunnery_deck_layout_v952','physical_fatigue_layout_v960'),('all_routes_combined_v954','all_routes_combined_v962'),('V955','V963')])]
    prepared=[rendered(*args) for args in pairs]
    ROOT.mkdir(parents=True,exist_ok=True);provenance=[]
    for source,target,raw,text in prepared:
        with target.open('x',encoding='utf-8') as f:f.write(text)
        assert source.read_bytes()==raw
        provenance.append({'source':str(source),'source_before_sha256':sha(raw),'source_after_sha256':sha(source.read_bytes()),'source_unchanged':True,
            'successor':str(target),'successor_sha256':sha(target.read_bytes())})
    save(ROOT/'actual_tools_provenance.json',{'files':provenance,'all_replacements_preflighted_before_output':True,
        'fixture_discloses_condition1_in_addition_to_room_assignment':True,'actual_scenes_pending':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('Five cold-boot successors created;only declared condition byte6 and room assignment added to prior coordinate fixture.',flush=True)


if __name__=='__main__':main()
