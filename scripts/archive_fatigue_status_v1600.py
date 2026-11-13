"""Preserve sea8 integration,failed pilots and complete terminal evidence on E."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/fatigue_status_archive_v1600')
DEST=Path('E:/Rota Nova translations/Editorial review/V1600 fatigue integration and recovery pending')
RETENTION=Path('work/rom_retention/20261022T1454293088417Z.json')

if __name__=='__main__':
    assert not ROOT.exists() and not DEST.exists()
    release=read('work/analysis/fatigue_status_release_v1593/registered_release_verification.json')
    checkpoint=read('work/analysis/fatigue_status_integration_v1599/integration_receipt.json')
    assert checkpoint['candidate_sha256']==release['candidate_sha256'] and checkpoint['completed_entries_added']==0
    plan=read(RETENTION);assert len(plan['roms'])==257 and all(Path(r['path']).is_file() for r in plan['roms'])
    assert not RETENTION.with_suffix('.result.json').exists() and not RETENTION.with_suffix('.journal.jsonl').exists()
    config=read('translations/fatigue_status_editorial_release_v1.json')
    paths={Path(p) for p in config['dependencies']}
    for p,digest in config['dependencies'].items():assert sha(Path(p).read_bytes())==digest,p
    paths.update([Path(__file__),RETENTION,Path('translations/rom_retention_pins.json'),Path('translations/editorial_review_current_v1.json'),
        Path('translations/release_stack.json'),Path('translations/fatigue_status_editorial_release_v1.json'),Path('translations/promoted_build.json'),
        Path('scripts/build_integrated_release.py'),Path(release['candidate']).with_suffix('.manifest.json'),Path('docs/editorial_handoff_current.md'),Path('scripts/verify_dialogue_palette_v628.py'),Path('docs/fatigue_status_v1587_context.md'),Path('docs/fatigue_status_v1588_source_review.md'),Path('docs/fatigue_status_v1599_integration_checkpoint.md')])
    for p in Path('scripts').glob('*fatigue*v15*.py'):paths.add(p)
    for p in Path('docs').glob('fatigue_status_v15*.md'):paths.add(p)
    for name in ['known_issues.md','todo.md','translation_progress.md','editorial_review_goal.md']:paths.add(Path('docs')/name)
    for directory in Path('work/analysis').glob('fatigue*v15*'):
        if directory.is_dir():paths.update(p for p in directory.glob('*') if p.is_file() and p.suffix.lower() not in ['.nds','.log','.dsv'])
    ROOT.mkdir(parents=True);DEST.mkdir(parents=True)
    workspace=Path.cwd().absolute();copied=[]
    for source in sorted(paths):
        target=DEST/'workspace'/source.absolute().relative_to(workspace)
        target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target);digest=sha(source.read_bytes())
        assert sha(target.read_bytes())==digest
        copied.append({'source':str(source),'archive':str(target),'sha256':digest})
    cohorts=[]
    names=['fatigue_status_v1594_newgame','fatigue_status_v1594_title','fatigue_search_pilot_v1587b_1578',
        'fatigue_shore_live_v1587e_1578','fatigue_increase_actual_v1597_1594','fatigue_recovery_live_v1597c_1594']
    for name in names:
        cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/name
        report_path=cap/'capture_report.json';report=read(report_path)
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and not report['hardware_device_verification']
        assert report['ROM_sha256'] in [release['candidate_sha256'],'d29f08026385628b47fcc0aa996402501975f986dbe2426ba348be723b37e79b']
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
        'all257_ROMs_retained':True,'retention_preview_only':str(RETENTION),'keep_count':221,'proposed_not_applied':36,
        'no_originals_moved_deleted_or_replaced':True,'completed':1348,'source_prose':1494,'reviewed_incomplete_COMMON':146,
        'V1594_experimental_V1492_promoted_309_recovery_open_full_goal_active':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'archive_receipt.json',receipt);copy2(ROOT/'archive_receipt.json',DEST/'archive_receipt.json')
    print('Fatigue integration archived:',len(copied),'workspace files,',len(cohorts),'terminal cohorts;257 ROMs retained;309 recovery and full goal remain open.')
