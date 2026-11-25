"""Preserve the completed fire-family evidence and preview-only ROM inventory."""
import re
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/powder_fire_archive_v1324')
DEST = Path('E:/Rota Nova translations/Editorial review/V1324 Powder fire completed release')
RETENTION = Path('work/rom_retention/20261022T0122020772771Z.json')


def main():
    assert not ROOT.exists() and not DEST.exists()
    release = read('work/analysis/powder_fire_release_v1315/registered_release_verification.json')
    for field in ['candidate','patch']:
        assert sha(Path(release[field]).read_bytes()) == release[field+'_sha256']
    completion = read('work/analysis/powder_fire_completion_v1323/completion_receipt.json')
    assert (completion['completed'],completion['source_prose']) == (1302,1379)
    ledger = read('translations/editorial_review_current_v1.json')
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass']) == (1302,1379)
    plan = read(RETENTION)
    assert len(plan['roms']) == 235 and all(Path(r['path']).is_file() for r in plan['roms'])
    assert sum(r['action']=='keep' for r in plan['roms']) == 207
    for version in [1266,1316]:
        pin = next(r for r in plan['roms'] if r['name']==f'all_routes_combined_v{version}_candidate.nds')
        assert pin['action']=='keep' and pin['reason'].startswith('pinned:')
    paths = {Path('dk4tool/patch/powder_fire_editorial.py'),Path('scripts/build_integrated_release.py'),
        Path('translations/powder_fire_editorial_release_v1.json'),Path('translations/release_stack.json'),
        Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json'),
        Path('translations/powder_fire_editorial_manuscript_v1.json'),
        Path('translations/powder_fire_editorial_manuscript_v2.json'),
        Path('translations/powder_fire_editorial_final_review_v1.json'),
        Path('docs/powder_fire_v1323_completion.md'),Path('docs/translation_progress.md'),
        Path('docs/editorial_review_goal.md'),Path('docs/known_issues.md'),Path('docs/todo.md'),
        Path(release['candidate']).with_suffix('.manifest.json'),Path(release['patch']),RETENTION}
    pattern = r'_v(?:130[7-9]|131\d|132[0-4])(?:[a-z])?'
    paths.update(p for p in Path('scripts').glob('*.py') if re.search(pattern+r'\.py$',p.name))
    for folder in Path('work/analysis').iterdir():
        if folder.is_dir() and re.search(pattern+r'$',folder.name):
            paths.update(p for p in folder.rglob('*') if p.is_file() and p.suffix.lower()!='.nds')
    repo = Path.cwd().absolute()
    DEST.mkdir(parents=True)
    archived = []
    for source in sorted(paths,key=lambda p:str(p).lower()):
        target = DEST/'Workspace'/source.absolute().relative_to(repo)
        target.parent.mkdir(parents=True,exist_ok=True)
        copy2(source,target)
        digest = sha(source.read_bytes())
        assert sha(target.read_bytes()) == digest
        archived.append({'source':str(source),'archive':str(target.relative_to(DEST)),'sha256':digest})
    reports = []
    capture_root = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
    for folder in capture_root.iterdir():
        if not folder.is_dir() or not (folder.name.startswith('powder_fire_v1316_') or folder.name=='powder_fire_v1320_1316'):
            continue
        source = folder/'capture_report.json'
        report = read(source)
        assert report['ROM_sha256']==release['candidate_sha256'] and not report['callback_errors']
        assert report['cold_boot'] and not report['savestate_loaded']
        assert not report['hardware_device_verification'] and not report['goal_complete']
        ram = report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']
        for row in ram:
            assert sha(Path(row['path']).read_bytes())==row['sha256']
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
        target = DEST/'Capture reports'/folder.name/source.name
        target.parent.mkdir(parents=True)
        copy2(source,target)
        assert target.read_bytes()==source.read_bytes()
        reports.append({'report':str(source),'sha256':sha(source.read_bytes()),
            'terminal_frame':report['frames'],'RAM_references':len(ram),'PNG_references':len(report['frames_captured'])})
    assert len(reports)==3
    guide = []
    for source in Path('E:/Rota Nova translations/Guide screenshots/V1316 Powder fire').iterdir():
        assert source.is_file()
        target = DEST/'Guide screenshots'/source.name
        target.parent.mkdir(exist_ok=True)
        copy2(source,target)
        assert target.read_bytes()==source.read_bytes()
        guide.append({'source':str(source),'sha256':sha(source.read_bytes())})
    receipt = {'archive':str(DEST),'files':archived,'file_count':len(archived),
        'capture_reports_all_primary_E_RAM_and_PNG_references_verified':reports,'guide_files':guide,
        'candidate':release['candidate'],'candidate_sha256':release['candidate_sha256'],
        'patch':release['patch'],'patch_sha256':release['patch_sha256'],
        'completed':1302,'source_prose_reviewed':1379,'reviewed_incomplete_COMMON':77,
        'all235_ROMs_still_present_preview_only_no_ApplyPlan':True,
        'all_originals_preserved_no_ROM_deleted_moved_or_rebuilt':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    ROOT.mkdir(parents=True)
    save(ROOT/'archive_receipt.json',receipt)
    save(DEST/'archive_receipt.json',receipt)
    print(f'{len(archived)} completed-release evidence files archived;three terminal capture reports verified;all235 ROMs retained.',flush=True)


if __name__=='__main__':
    main()
