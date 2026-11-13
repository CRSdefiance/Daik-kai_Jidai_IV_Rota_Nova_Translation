"""Archive V1622 integration and exact pending scope;retain every ROM."""
import ast
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/hot_spring_archive_v1630')
DEST=Path('E:/Rota Nova translations/Editorial review/V1630 hot spring integrated discovery verified')
if __name__=='__main__':
    assert not ROOT.exists() and not DEST.exists()
    release=read('work/analysis/hot_spring_release_v1621/registered_release_verification.json')
    checkpoint=read('work/analysis/hot_spring_integration_v1629/integration_receipt.json')
    assert checkpoint['candidate_sha256']==release['candidate_sha256'] and checkpoint['completed_entries_added']==0
    config=read('translations/hot_spring_editorial_release_v1.json');paths={Path(p) for p in config['dependencies']}
    for p,digest in config['dependencies'].items():assert sha(Path(p).read_bytes())==digest,p
    paths.update([Path(__file__),Path('translations/rom_retention_pins.json'),Path('translations/editorial_review_current_v1.json'),
        Path('translations/release_stack.json'),Path('translations/hot_spring_editorial_release_v1.json'),Path('translations/promoted_build.json'),
        Path('scripts/build_integrated_release.py'),Path('dk4tool/patch/hot_spring_editorial.py'),Path(release['candidate']).with_suffix('.manifest.json'),
        Path('docs/editorial_handoff_current.md'),Path('docs/ship_advice_choice_centering_20261022.md'),Path('docs/screenshot_text_repairs_20261022.md')])
    for pattern in ['*hot_spring*v16*.py']:
        for p in Path('scripts').glob(pattern):ast.parse(p.read_text(encoding='utf-8'),filename=str(p));paths.add(p)
    for p in Path('docs').glob('hot_spring_v16*.md'):paths.add(p)
    for name in ['known_issues.md','todo.md','translation_progress.md','editorial_review_goal.md']:paths.add(Path('docs')/name)
    for directory in Path('work/analysis').glob('hot_spring*v16*'):
        if directory.is_dir() and directory!=ROOT:
            paths.update(p for p in directory.rglob('*') if p.is_file() and p.suffix.lower() not in ['.nds','.dsv','.log'])
    ROOT.mkdir(parents=True);DEST.mkdir(parents=True);workspace=Path.cwd().absolute();copied=[]
    for source in sorted(paths):
        target=DEST/'workspace'/source.absolute().relative_to(workspace);target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        digest=sha(source.read_bytes());assert sha(target.read_bytes())==digest;copied.append({'source':str(source),'archive':str(target),'sha256':digest})
    cohorts=[]
    for name,limit in [('hot_spring_v1622_newgame',4000),('hot_spring_v1622_title',1150),('hot_spring_live_v1626_1622',13600)]:
        cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/name;report_path=cap/'capture_report.json';report=read(report_path)
        assert report['ROM_sha256']==release['candidate_sha256'] and report['frames']==limit and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors'] and not report['hardware_device_verification'];refs=[]
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes())==row['PNG_sha256'];refs.append({'path':row['path'],'sha256':row['PNG_sha256'],'kind':'PNG'})
        for key in ['read_only_capture_RAM_snapshots','read_only_pause_RAM_snapshots']:
            for row in report.get(key,[]):assert sha(Path(row['path']).read_bytes())==row['sha256'];refs.append({'path':row['path'],'sha256':row['sha256'],'kind':'RAM'})
        for record in ['capture_report.json','navigation_command_journal.json']:
            source=cap/record
            if source.is_file():
                target=DEST/'terminal_records'/name/record;target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        cohorts.append({'report':str(report_path),'report_sha256':sha(report_path.read_bytes()),'terminal_frame':limit,
            'live13600_terminal_is_rats_notice_not_normal_Sea_View':name=='hot_spring_live_v1626_1622',
            'primary_E_drive_evidence_verified_and_retained':refs})
    guide=Path(checkpoint['guide']);guides=[]
    for source in guide.iterdir():
        target=DEST/'guide'/source.name;target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        guides.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    for key in ['candidate','patch']:assert sha(Path(release[key]).read_bytes())==release[key+'_sha256']
    assert sha(Path(release['reconstruction']).read_bytes())==release['candidate_sha256']
    roms=sorted(set(Path('E:/Rota Nova translations/Generated').rglob('*.nds'))|set(Path('E:/Rota Nova translations').glob('*.nds')))
    inventory=[{'path':str(p),'bytes':p.stat().st_size,'last_write_ns':p.stat().st_mtime_ns} for p in roms]
    save(ROOT/'read_only_ROM_inventory.json',{'ROMs':inventory,'all_ROMs_retained':True,'no_retention_plan_applied':True,
        'unsigned_PowerShell_preview_not_retried_or_bypassed':'Prior policy refusal is documented in V1613;this is inventory only.'})
    receipt={'archive':str(DEST),'workspace_files':copied,'terminal_cohorts':cohorts,'guide_files':guides,
        'candidate':release['candidate'],'candidate_sha256':release['candidate_sha256'],'patch':release['patch'],'patch_sha256':release['patch_sha256'],
        'read_only_ROM_inventory':str(ROOT/'read_only_ROM_inventory.json'),'all_ROMs_retained':len(roms),'no_originals_moved_deleted_or_replaced':True,
        'completed':1350,'source_prose':1507,'reviewed_incomplete_COMMON':157,
        'optional_relaxation_and310_pending_all13_entries_kept_open':True,'authoritative_actual_receipt_uses1628b_corrected_terminal_scope':True,
        'all_current_jobs_terminal_V1622_experimental_V1492_promoted_full_goal_active':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'archive_receipt.json',receipt);copy2(ROOT/'archive_receipt.json',DEST/'archive_receipt.json');copy2(ROOT/'read_only_ROM_inventory.json',DEST/'read_only_ROM_inventory.json')
    print('Archived',len(copied),'workspace files,three terminal cohorts,guide captures;',len(roms),'ROMs retained. V1622 experimental;optional relaxation/310 and full goal remain open.')
