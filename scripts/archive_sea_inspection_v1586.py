"""Archive completed sea8/status2 and all four terminal V1578 cohorts on E."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/sea_inspection_archive_v1586')
DEST=Path('E:/Rota Nova translations/Editorial review/V1586 sea responses and inspection statuses completed')
RETENTION=Path('work/rom_retention/20261022T1409379077452Z.json')
if __name__=='__main__':
    assert not ROOT.exists() and not DEST.exists()
    release=read('work/analysis/inspection_status_release_v1577/registered_release_verification.json')
    completion=read('work/analysis/sea_inspection_completion_v1584/completion_receipt.json')
    assert completion['candidate_sha256']==release['candidate_sha256'] and completion['newly_completed']==10
    retention=read(RETENTION);assert len(retention['roms'])==255 and all(Path(r['path']).is_file() for r in retention['roms'])
    assert not RETENTION.with_suffix('.result.json').exists() and not RETENTION.with_suffix('.journal.jsonl').exists()
    config=read('translations/inspection_status_editorial_release_v1.json');paths={Path(p) for p in config['dependencies']}
    for p,digest in config['dependencies'].items():assert sha(Path(p).read_bytes())==digest,p
    paths.update([Path(__file__),RETENTION,Path('translations/rom_retention_pins.json'),Path('translations/editorial_review_current_v1.json'),
        Path('translations/release_stack.json'),Path('translations/inspection_status_editorial_release_v1.json'),
        Path('translations/sea_responses_final_review_v1.json'),Path('translations/inspection_status_final_review_v1.json'),
        Path('translations/promoted_build.json'),Path('scripts/build_integrated_release.py'),Path(release['candidate']).with_suffix('.manifest.json'),
        Path('docs/editorial_handoff_current.md'),Path('docs/sea_inspection_v1584_completion.md'),Path('docs/inspection_status_v1572_source_review.md')])
    for pattern in ['*inspection_status*v15*.py','*sea_inspection*v158*.py']:paths.update(Path('scripts').glob(pattern))
    for name in ['known_issues.md','todo.md','translation_progress.md','editorial_review_goal.md']:paths.add(Path('docs')/name)
    for pattern in ['inspection_status_*v15*','sea_inspection_completion_v1584']:
        for directory in Path('work/analysis').glob(pattern):
            if directory.is_dir():paths.update(p for p in directory.glob('*') if p.is_file() and p.suffix.lower() not in ['.nds','.log','.dsv'])
    ROOT.mkdir(parents=True);DEST.mkdir(parents=True);workspace=Path.cwd().absolute();copied=[]
    for source in sorted(paths):
        target=DEST/'workspace'/source.absolute().relative_to(workspace);target.parent.mkdir(parents=True,exist_ok=True)
        copy2(source,target);digest=sha(source.read_bytes());assert sha(target.read_bytes())==digest
        copied.append({'source':str(source),'archive':str(target),'sha256':digest})
    cohorts=[]
    for name in ['inspection_status_v1578_newgame','inspection_status_v1578_title','inspection_status_lookout_v1582_1578','inspection_status_no_lookout_v1582b_1578']:
        cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/name;report_path=cap/'capture_report.json';report=read(report_path)
        assert report['ROM_sha256']==release['candidate_sha256'] and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors'] and not report['hardware_device_verification'] and not report['goal_complete']
        refs=[]
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes())==row['PNG_sha256'];refs.append({'path':row['path'],'sha256':row['PNG_sha256'],'kind':'PNG'})
        for key in ['read_only_capture_RAM_snapshots','read_only_pause_RAM_snapshots']:
            for row in report.get(key,[]):
                assert sha(Path(row['path']).read_bytes())==row['sha256'];refs.append({'path':row['path'],'sha256':row['sha256'],'kind':'RAM'})
        for record in ['capture_report.json','navigation_command_journal.json']:
            source=cap/record
            if source.is_file():
                target=DEST/'terminal_records'/name/record;target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
                assert sha(source.read_bytes())==sha(target.read_bytes())
        cohorts.append({'report':str(report_path),'report_sha256':sha(report_path.read_bytes()),'terminal_frame':report['frames'],'primary_E_drive_evidence_verified_and_preserved':refs})
    guides=[]
    for source in sorted(Path(completion['guide']).iterdir()):
        target=DEST/'guide'/source.name;target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());guides.append({'source':str(source),'archive':str(target),'sha256':sha(source.read_bytes())})
    for key in ['candidate','patch']:assert sha(Path(release[key]).read_bytes())==release[key+'_sha256']
    receipt={'archive':str(DEST),'workspace_files':copied,'terminal_cohorts':cohorts,'guide_files':guides,
        'candidate':release['candidate'],'candidate_sha256':release['candidate_sha256'],'patch':release['patch'],'patch_sha256':release['patch_sha256'],
        'all255_ROMs_retained':True,'retention_preview_only':str(RETENTION),'keep_count':219,'proposed_not_applied':36,
        'no_originals_moved_deleted_or_replaced':True,'completed':1348,'source_prose':1492,'reviewed_incomplete_COMMON':144,
        'V1578_experimental_V1492_promoted_and_full_goal_active':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'archive_receipt.json',receipt);copy2(ROOT/'archive_receipt.json',DEST/'archive_receipt.json')
    print('Completed sea/status archive:',len(copied),'workspace files,4 terminal cohorts,4 guide captures;all255 ROMs retained;full goal active.')
