"""Explicit frozen-source successors for the registered release and actual tests."""

from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_repair_medical_v905')


def main():
    ROOT.mkdir(parents=True,exist_ok=True);outputs=[]
    def successor(source,target,pairs):
        source,target=Path(source),Path(target);before=source.read_bytes();text=before.decode('utf-8').replace('\r\n','\n')
        for old,new in pairs:
            assert old in text,(source,old);text=text.replace(old,new)
        assert not target.exists()
        with target.open('x',encoding='utf-8') as f:f.write(text)
        assert source.read_bytes()==before
        outputs.append({'source':str(source),'source_before_sha256':sha(before),'source_after_sha256':sha(source.read_bytes()),
            'source_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes())})
    successor('scripts/verify_battle_personal_release_v893.py','scripts/verify_battle_repair_medical_release_v904.py',[
        ('battle_personal','battle_repair_medical'),('v893','v904'),('V893','V904'),('v888','v893'),('V888','V893'),
        ('from dk4tool.patch.gunnery_deck_editorial import current_entries as previous_entries','from dk4tool.patch.battle_personal_editorial import current_entries as previous_entries'),
        ('==18 and len(actual)','==19 and len(actual)'),('all3643','all3644'),('only25','only24'),('battle-personal','battle-repair-medical')])
    successor('scripts/run_battle_personal_startup_v893.py','scripts/run_battle_repair_medical_startup_v904.py',[
        ('battle_personal','battle_repair_medical'),('v893','v904')])
    successor('scripts/verify_battle_personal_startup_v893.py','scripts/verify_battle_repair_medical_startup_v904.py',[
        ('battle_personal','battle_repair_medical'),('v893','v904'),('gunnery_deck_v888','battle_personal_v893'),('V888','V893')])
    successor('scripts/check_battle_personal_title_v898.py','scripts/check_battle_repair_medical_title_v905.py',[
        ('battle_personal_v898','battle_repair_medical_v905'),("('888','893')","('893','904')"),
        ("version=='888'","version=='893'"),('gunnery_deck_v889_title_888','battle_personal_v898_title_893'),
        ("reports['888'][0][1100].tobytes()==reports['893'][0][1100].tobytes()","reports['893'][0][1100].tobytes()==reports['904'][0][1100].tobytes()"),('V888','V893')])
    successor('scripts/native_battle_standoff_v897.py','scripts/native_battle_standoff_v905.py',[
        ('all_routes_combined_v893_candidate','all_routes_combined_v904_candidate'),
        ('translations/battle_personal_editorial_release_v1.json','translations/battle_repair_medical_editorial_release_v1.json'),
        ('V893','V904'),('V897','V905')])
    successor('scripts/run_battle_personal_adapter_v895.py','scripts/run_battle_repair_medical_adapter_v905.py',[
        ('battle_personal','battle_repair_medical'),('v895','v905'),('battle-personal','battle-repair-medical'),
        ('one/two Cabin occupant bytes','two/three room and occupant bytes')])
    successor('scripts/run_battle_personal_choice_v897.py','scripts/run_battle_repair_medical_live_v905.py',[
        ('battle_personal','battle_repair_medical'),('v895','v905'),('v897','v905'),('V897','V905'),
        ('battle-personal','battle-repair-medical'),('battle_repair_medical_v905_893_','battle_repair_medical_v905_904_'),
        ('one_or_two_Cabin_occupant_bytes_plus_two_existing_coordinate_fixtures_only','two_or_three_room_occupant_bytes_plus_two_existing_coordinate_fixtures_only')])
    save(ROOT/'test_successor_provenance.json',{'files':outputs,'all_source_hashes_unchanged':True,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print('Seven explicit release/startup/title/actual successors created;all source files unchanged.',flush=True)


if __name__=='__main__':main()
