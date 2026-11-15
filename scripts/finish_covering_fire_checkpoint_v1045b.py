"""Finish evidence copies after explicit-E capture paths exceeded repo-relative mapping."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save


def main():
    root=Path('work/analysis/reinforcement_sniping_v1045')
    actual_path=Path('work/analysis/reinforcement_sniping_v1042/actual_covering_fire_verification.json')
    actual=read(actual_path);lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    doc=Path('docs/reinforcement_sniping_v1045_actual_checkpoint.md')
    assert ledger['reinforcement_sniping_actual_v1045']['actual_covering_fire_proof_sha256']==sha(actual_path.read_bytes())
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1219
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert doc.exists() and not (root/'archive_manifest.json').exists()
    guide=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V1045 Covering fire')
    gp=read(guide/'provenance.json');assert sha(Path(gp['unmodified_screenshot']).read_bytes())==gp['sha256']
    archive=Path('E:/Rota Nova translations/Editorial review/V1045 Covering fire gameplay');assert archive.exists()
    files=[lp,doc,actual_path,Path('scripts/record_covering_fire_checkpoint_v1045.py'),Path(__file__),
        Path('scripts/verify_covering_fire_gameplay_v1042.py')]
    for version,frame in ((1037,5100),(1039,5510),(1041,6310),(1044,6550)):
        folder=Path(f'work/analysis/reinforcement_sniping_v{version}')
        assert read(folder/'terminal_preservation.json')['source_and_disposable_donors_unchanged']
        files+=list(folder.glob('*.json'))+list(folder.glob('*.jsonl'))
        files+=[Path(f'scripts/run_reinforcement_regional_live_v{version}.py')]
        report=Path(f'E:/Rota Nova translations/Generated/work/emulation_v193/reinforcement_sniping_v{version}_1034_regional/capture_report.json')
        assert read(report)['frames']==frame;files.append(report)
    files += [Path('scripts/native_reinforcement_location_v1038.py'),Path('scripts/native_reinforcement_proximity_v1040.py'),
        Path('scripts/native_reinforcement_lookout_v1043.py'),Path('work/analysis/reinforcement_sniping_v1043/offline_exact_fixture_proof.json')]
    files += [Path(r['capture']) for r in actual['complete_actual_holds']]+[Path(actual['actual_duel_entry_screenshot'])]
    copied=[]
    generated=Path('E:/Rota Nova translations/Generated')
    for source in dict.fromkeys(files):
        try:relative=source.absolute().relative_to(Path.cwd())
        except ValueError:relative=Path('Generated')/source.absolute().relative_to(generated)
        target=archive/relative;target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists():assert target.read_bytes()==source.read_bytes()
        else:copy2(source,target)
        assert target.read_bytes()==source.read_bytes()
        copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(root/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'actual_guide_screenshots':1,
        'completed_entries_added':0,'full_goal_complete':False,
        'failed_predecessor':'scripts/record_covering_fire_checkpoint_v1045.py',
        'failed_predecessor_sha256':sha(Path('scripts/record_covering_fire_checkpoint_v1045.py').read_bytes()),
        'successor_change':'Existing matching archive copies preserved;explicit E Generated captures mapped relative to that approved physical root. Repo paths retain lexical repo-relative mapping without resolve().',
        'producer_sha256':sha(Path(__file__).read_bytes())})
    save(root/'final_goal_turn_check.json',{'actual_covering_fire_proof_sha256':sha(actual_path.read_bytes()),
        'four_terminal_cold_boot_runs_and_original_donors_preserved':True,
        'no_live_process_left_by_this_checkpoint':True,'completed_records':1196,'source_prose_records':1219,
        'remaining_actual_families':['reinforcement','admiral_shot'],'full_goal_active_and_incomplete':True})
    print('Covering-fire actual proof and guide archived. All four pilots terminal;1196 complete;reinforcement and successful-shot gates remain.',flush=True)


if __name__=='__main__':main()
