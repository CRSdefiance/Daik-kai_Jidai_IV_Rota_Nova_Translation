"""Frozen-source successors for original-battle samples and title comparison."""

from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_battle_cooking_livestock_native_v909 import successor as create_successor
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/battle_chapel_planning_v917')


def successor(source,target,changes,provenance):
    # Resume a stopped generator by verifying,never replacing,already-created files.
    source,target=Path(source),Path(target)
    if not target.exists():return create_successor(source,target,changes,provenance)
    before=source.read_bytes();text=source.read_text(encoding='utf-8')
    for old,new in changes:
        assert old in text,old
        text=text.replace(old,new)
    assert target.read_text(encoding='utf-8')==text and source.read_bytes()==before
    provenance.append({'source':str(source),'source_before_sha256':sha(before),'source_after_sha256':sha(source.read_bytes()),
        'source_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes()),'existing_identical_output_preserved':True})


def main():
    ROOT.mkdir(parents=True,exist_ok=True);p=[]
    successor('scripts/check_battle_cooking_livestock_title_v911.py','scripts/check_battle_chapel_planning_title_v917.py',[
        ('battle_cooking_livestock_v911','battle_chapel_planning_v917'),("('904','910')","('910','916')"),
        ("version=='904'","version=='910'"),('battle_repair_medical_v905_title_904','battle_cooking_livestock_v911_title_910'),
        ("reports['904'][0][1100].tobytes()==reports['910'][0][1100].tobytes()","reports['910'][0][1100].tobytes()==reports['916'][0][1100].tobytes()"),('V904','V910')],p)
    successor('scripts/native_battle_standoff_v911.py','scripts/native_battle_standoff_v917.py',[
        ('all_routes_combined_v910_candidate','all_routes_combined_v916_candidate'),
        ('translations/battle_cooking_livestock_editorial_release_v2.json','translations/battle_chapel_planning_editorial_release_v1.json'),
        ('V910','V916'),('V911','V917')],p)
    successor('scripts/native_battle_cooking_livestock_fixture_v9112.py','scripts/native_battle_chapel_planning_fixture_v917.py',[
        ('cooking/livestock room','Chapel/Planning room'),('battle_cooking_livestock','battle_chapel_planning'),
        ('battle_chapel_planning_editorial_release_v2','battle_chapel_planning_editorial_release_v1'),
        ("{'SeraGalley':(24,15),'CaptainGalley':(1,15),'EmilioLivestock':(14,17),'Voice1Livestock':(12,17)}",
         "{'ChristinaChapel':(7,18),'CaptainChapel':(1,18),'EmilioPlanning':(14,19),'CaptainPlanning':(1,19)}")],p)
    successor('scripts/run_battle_cooking_livestock_adapter_v9112.py','scripts/run_battle_chapel_planning_adapter_v917.py',[
        ('battle_cooking_livestock','battle_chapel_planning'),('v9112','v917'),
        ('battle-cooking-livestock','battle-chapel-planning')],p)
    successor('scripts/run_battle_cooking_livestock_live_v9112.py','scripts/run_battle_chapel_planning_live_v917.py',[
        ('battle_cooking_livestock','battle_chapel_planning'),('v9112','v917'),('v911','v917'),('V911','V917'),
        ('battle_chapel_planning_v917_910_','battle_chapel_planning_v917_916_'),('battle-cooking-livestock','battle-chapel-planning')],p)
    successor('scripts/battle_cooking_livestock_flags_v911.py','scripts/battle_chapel_planning_flags_v917.py',[
        ('battle_cooking_livestock_layout_v908','battle_chapel_planning_layout_v914'),
        ('all_routes_combined_v910_candidate','all_routes_combined_v916_candidate'),('V911','V917')],p)
    save(ROOT/'test_successor_provenance.json',{'files':p,'all_source_hashes_unchanged':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('Six title/actual successors created.Original harness,donors and prior test helpers unchanged.',flush=True)


if __name__=='__main__':main()
