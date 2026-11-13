"""Preserve sea8 integration,failed pilots and complete terminal evidence on E."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/sea_responses_archive_v1571')
DEST=Path('E:/Rota Nova translations/Editorial review/V1571 sea inspection integration and open modals')
RETENTION=Path('work/rom_retention/20261022T1347524429614Z.json')

if __name__=='__main__':
    assert not ROOT.exists() and not DEST.exists()
    release=read('work/analysis/sea_responses_release_v1562/registered_release_verification.json')
    checkpoint=read('work/analysis/sea_responses_integration_v1570/integration_receipt.json')
    assert checkpoint['candidate_sha256']==release['candidate_sha256'] and checkpoint['completed_entries_added']==0
    plan=read(RETENTION);assert len(plan['roms'])==253 and all(Path(r['path']).is_file() for r in plan['roms'])
    assert not RETENTION.with_suffix('.result.json').exists() and not RETENTION.with_suffix('.journal.jsonl').exists()
    config=read('translations/sea_responses_editorial_release_v1.json')
    paths={Path(p) for p in config['dependencies']}
    for p,digest in config['dependencies'].items():assert sha(Path(p).read_bytes())==digest,p
    paths.update([Path(__file__),RETENTION,Path('translations/rom_retention_pins.json'),Path('translations/editorial_review_current_v1.json'),
        Path('translations/release_stack.json'),Path('translations/sea_responses_editorial_release_v1.json'),Path('translations/promoted_build.json'),
        Path('scripts/build_integrated_release.py'),Path(release['candidate']).with_suffix('.manifest.json'),Path('docs/editorial_handoff_current.md')])
    for p in Path('scripts').glob('*sea*v15*.py'):paths.add(p)
    for p in Path('docs').glob('sea_responses_v15*.md'):paths.add(p)
    for name in ['known_issues.md','todo.md','translation_progress.md','editorial_review_goal.md']:paths.add(Path('docs')/name)
    for directory in Path('work/analysis').glob('sea*v15*'):
        if directory.is_dir():paths.update(p for p in directory.glob('*') if p.is_file() and p.suffix.lower() not in ['.nds','.log','.dsv'])
    ROOT.mkdir(parents=True);DEST.mkdir(parents=True)
    workspace=Path.cwd().absolute();copied=[]
    for source in sorted(paths):
        target=DEST/'workspace'/source.absolute().relative_to(workspace)
        target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target);digest=sha(source.read_bytes())
        assert sha(target.read_bytes())==digest
        copied.append({'source':str(source),'archive':str(target),'sha256':digest})
    cohorts=[]
    names=['sea_responses_v1563_newgame','sea_responses_v1563_title','sea_inspection_pilot_v1552c_1542',
        'sea_inspection_pilot_v1552d_1542','sea_inspection_live_v1552e_1542','sea_registration_live_v1552h_1542',
        'sea_inspection_actual_v1567_1563','sea_inspection_control_v1567c_1542','sea_inspection_final_v1567d_1563']
    for name in names:
        cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/name
        report_path=cap/'capture_report.json';report=read(report_path)
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and not report['hardware_device_verification']
        assert report['ROM_sha256'] in [release['candidate_sha256'],'b8b256650bb426e99012be06fd060114da0fbf32f763b5c3434204dda8f50437']
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
    guide=Path(checkpoint['guide']);guides=[]
    for source in sorted(guide.iterdir()):
        target=DEST/'guide'/source.name;target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());guides.append({'source':str(source),'archive':str(target),'sha256':sha(source.read_bytes())})
    for key in ['candidate','patch']:assert sha(Path(release[key]).read_bytes())==release[key+'_sha256']
    receipt={'archive':str(DEST),'workspace_files':copied,'terminal_cohorts':cohorts,'guide_files':guides,
        'candidate':release['candidate'],'candidate_sha256':release['candidate_sha256'],'patch':release['patch'],'patch_sha256':release['patch_sha256'],
        'all253_ROMs_retained':True,'retention_preview_only':str(RETENTION),'keep_count':217,'proposed_not_applied':36,
        'no_originals_moved_deleted_or_replaced':True,'completed':1338,'source_prose':1490,'reviewed_incomplete_COMMON':152,
        'V1563_experimental_V1492_promoted_306_307_open_and_full_goal_active':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'archive_receipt.json',receipt);copy2(ROOT/'archive_receipt.json',DEST/'archive_receipt.json')
    print('Sea8 integration archived:',len(copied),'workspace files,',len(cohorts),'terminal cohorts;253 ROMs retained;306/307 remain open.')
