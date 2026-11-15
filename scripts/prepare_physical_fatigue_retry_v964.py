"""Retain failed timing evidence and preflight explicit late-condition successors."""
from pathlib import Path
from scripts.prepare_physical_fatigue_native_v961 import rendered
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/physical_fatigue_v964')


def main():
    changes=[
        ('scripts/run_physical_fatigue_adapter_v963.py','scripts/run_physical_fatigue_adapter_v964.py',[
            ('native_physical_fatigue_fixture_v963','native_physical_fatigue_fixture_v964')]),
        ('scripts/run_physical_fatigue_live_v963.py','scripts/run_physical_fatigue_live_v964.py',[
            ('run_physical_fatigue_adapter_v963','run_physical_fatigue_adapter_v964'),('physical_fatigue_v963','physical_fatigue_v964'),("print('V963'","print('V964'"),
            ('three_or_four_room_occupant_and_condition1_bytes_plus_two_existing_coordinate_fixtures_only','declared_room_early_condition_and_late_condition1_fixtures_plus_two_coordinate_approaches')]),
        ('scripts/navigate_physical_fatigue_v963.py','scripts/navigate_physical_fatigue_v964.py',[
            ('physical_fatigue_v963','physical_fatigue_v964'),("{'until':16300,'touch':[66,110],'duration':8}","{'until':16300,'touch':[66,110],'duration':8,'physical_fatigue_fixture':{'case':args.case,'late_condition_only':True}}")]),
        ('scripts/verify_physical_fatigue_gameplay_v963.py','scripts/verify_physical_fatigue_gameplay_v964.py',[
            ('physical_fatigue_v963','physical_fatigue_v964'),
            ("assignment=report['synthetic_physical_fatigue_Cabin_assignment_fixtures'];assert len(assignment)==1;fixture=assignment[0]", "all_fixtures=report['synthetic_physical_fatigue_Cabin_assignment_fixtures'];assert len(all_fixtures)==2\n        assignment=[f for f in all_fixtures if not f.get('synthetic_physical_fatigue_late_condition_fixture')];assert len(assignment)==1;fixture=assignment[0]\n        late=[f for f in all_fixtures if f.get('synthetic_physical_fatigue_late_condition_fixture')];assert len(late)==1;late=late[0]\n        assert late['actor_ID']==actor and late['fixture_condition']==1 and late['only_condition_byte6_changes_all_other4MiB_exact']\n        assert late['other31_actor_bytes_and_actor_captain_identity_exact'] and len(late['changes'])==(0 if owned else 1)"),
            ("'room_and_condition_fixture':fixture,'coordinate_fixtures':coordinates", "'room_and_condition_fixture':fixture,'late_condition_fixture':late,'coordinate_fixtures':coordinates"),
            ('Disclosed room/occupant bytes plus officer condition byte6=1,after observed original combat0/1;two coordinate approaches.','Disclosed room/occupant bytes and early condition byte6=1 after observed original combat0/1;the NPC tag is recomputed before Deck,so one further condition byte6=1 is inserted after Deck opens and before selecting the officer. Genuine captain already retains1;late insertion changes no captain byte. Two coordinate approaches. Prior V963 timing trials are retained without NPC fatigue credit.')]),
        ('scripts/record_physical_fatigue_completion_v963.py','scripts/record_physical_fatigue_completion_v964.py',[
            ('verify_physical_fatigue_gameplay_v963','verify_physical_fatigue_gameplay_v964'),('physical_fatigue_v963','physical_fatigue_v964'),('V963','V964'),
            ('range(957,964)','range(957,965)'),
            ('Disclosed room assignment and condition byte6 fixtures follow observed original combat0/1.','Disclosed room and early condition fixtures follow observed original combat0/1;NPC condition1 is inserted again after Deck opens because original simulation recomputes it before arrival. Initial V963 timing trials remain non-credit evidence.')])]
    prepared=[rendered(*args) for args in changes]
    ROOT.mkdir(parents=True,exist_ok=True);assert not (ROOT/'timing_correction.json').exists();provenance=[]
    for source,target,raw,text in prepared:
        with target.open('x',encoding='utf-8') as f:f.write(text)
        assert source.read_bytes()==raw
        provenance.append({'source':str(source),'source_before_sha256':sha(raw),'source_after_sha256':sha(source.read_bytes()),'source_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes())})
    save(ROOT/'timing_correction.json',{'prior_trials':'work/analysis/physical_fatigue_v963','prior_actual_verifier_sha256':sha(Path('scripts/verify_physical_fatigue_gameplay_v963.py').read_bytes()),
        'finding':'Original game recomputes visiting NPC actor byte6 to0 before Deck. Actual captain1 retains1. Original trials selected working comments1771/1772 for NPCs;captain1790 appeared correctly. Not a V962 ROM or English formatting defect.',
        'new_action':'Fresh cold boots with an additional explicit source-bounded condition1 byte inserted after Deck opens,before officer selection. No savestate reuse,identity,text or code injection.',
        'failed_NPC_trials_not_counted_as_fatigue_verification':True,'files':provenance,'all_historical_files_unchanged':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('Failed timing trials retained;five late-condition successors preflighted. ROM and historical scripts unchanged.',flush=True)


if __name__=='__main__':main()
