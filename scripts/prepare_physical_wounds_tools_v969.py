"""Preflight release verification/startup successors and one optional wound builder stage."""
from pathlib import Path
from scripts.prepare_physical_fatigue_native_v961 import rendered
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/physical_wounds_v969')


def main():
    work=[]
    work.append(rendered('scripts/verify_physical_fatigue_release_v962.py','scripts/verify_physical_wounds_release_v969.py',[
        ('physical_fatigue','physical_wounds'),('physical_wounds_release_v962','physical_wounds_release_v969'),
        ('from dk4tool.patch.battle_gunnery_deck_editorial import current_entries as previous_entries','from dk4tool.patch.physical_fatigue_editorial import current_entries as previous_entries'),
        ('all_routes_combined_v962','all_routes_combined_v969'),('all-routes-unified-v962','all-routes-unified-v969'),('all-routes-unified-v954','all-routes-unified-v962'),
        ('len(changed_IDs)==10','len(changed_IDs)==11'),('V962_exact_patch','V969_exact_patch'),('changed_components_relative_to_V954','changed_components_relative_to_V962'),
        ('V962: full471/114 inheritance,bounded physical-fatigue','V969: full471/114 inheritance,bounded physical-wounds')]))
    work.append(rendered('scripts/run_physical_fatigue_startup_v962.py','scripts/run_physical_wounds_startup_v969.py',[
        ('physical_fatigue_v962','physical_wounds_v969'),('all_routes_combined_v962','all_routes_combined_v969')]))
    work.append(rendered('scripts/verify_physical_fatigue_startup_v962.py','scripts/verify_physical_wounds_startup_v969.py',[
        ('physical_fatigue_v962','physical_wounds_v969'),('all_routes_combined_v962','all_routes_combined_v969'),('battle_gunnery_deck_v954','physical_fatigue_v962'),('V954','V962')]))
    work.append(rendered('scripts/check_physical_fatigue_title_v963.py','scripts/check_physical_wounds_title_v970.py',[
        ("choices=('962',)","choices=('969',)"),('V954','V962'),
        ("('954',CAP/'battle_gunnery_deck_v955_title_954'),('962',CAP/'physical_fatigue_v963_title_962')","('962',CAP/'physical_fatigue_v963_title_962'),('969',CAP/'physical_wounds_v970_title_969')"),
        ("reports['954'][0][1100].tobytes()==reports['962'][0][1100].tobytes()","reports['962'][0][1100].tobytes()==reports['969'][0][1100].tobytes()"),
        ("assert args.run=='962'","assert args.run=='969'"),('all_routes_combined_v962_candidate','all_routes_combined_v969_candidate'),
        ("folder=CAP/'physical_fatigue_v963_title_962'","folder=CAP/'physical_wounds_v970_title_969'"),
        ("ROOT=Path('work/analysis/physical_fatigue_v963')","ROOT=Path('work/analysis/physical_wounds_v970')"),('title_962_run_plan','title_969_run_plan')]))
    builder=Path('scripts/build_integrated_release.py');before=builder.read_bytes();anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('physical_wounds_editorial')" not in before
    lo=before.index(b"    physical_fatigue_editorial = profile_config.get('physical_fatigue_editorial')");hi=before.index(anchor)
    block=before[lo:hi].replace(b'physical_fatigue',b'physical_wounds').replace(b'PHYSICAL_FATIGUE',b'PHYSICAL_WOUNDS')
    after=before[:hi]+block+before[hi:];assert after.replace(block,b'',1)==before;compile(after,str(builder),'exec')
    ROOT.mkdir(parents=True,exist_ok=True);assert not (ROOT/'builder_before.py').exists()
    (ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(block);provenance=[]
    for source,target,raw,text in work:
        with target.open('x',encoding='utf-8') as f:f.write(text)
        assert source.read_bytes()==raw
        provenance.append({'source':str(source),'source_before_sha256':sha(raw),'source_after_sha256':sha(source.read_bytes()),'source_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes())})
    assert builder.read_bytes()==before;builder.write_bytes(after)
    save(ROOT/'registered_tools_provenance.json',{'files':provenance,'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),
        'builder_prior_bytes_restored_by_removing_exact_optional_block':builder.read_bytes().replace(block,b'',1)==before,
        'all_successor_replacements_syntax_and_stage_preflighted_before_output':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('Four historical tools unchanged;successors and one optional wound builder stage preflighted.',flush=True)


if __name__=='__main__':main()
