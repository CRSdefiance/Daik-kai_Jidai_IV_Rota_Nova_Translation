"""Archive the integrated/native sinking checkpoint without completion credit."""
import re
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_sinking_archive_v1349')
DEST = Path('E:/Rota Nova translations/Editorial review/V1349 Sinking native and integrated checkpoint')
RETENTION = Path('work/rom_retention/20261022T0200041701486Z.json')


def main():
    assert not ROOT.exists() and not DEST.exists()
    release = read('work/analysis/ship_sinking_release_v1343/registered_release_verification.json')
    for field in ['candidate','patch']:
        assert sha(Path(release[field]).read_bytes())==release[field+'_sha256']
    checkpoint = read('work/analysis/ship_sinking_checkpoint_v1348/checkpoint_receipt.json')
    assert checkpoint['original_sinking_scenes_pending'] and checkpoint['completed_entries_added']==0
    ledger = read('translations/editorial_review_current_v1.json')
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1302,1395)
    plan = read(RETENTION)
    assert len(plan['roms'])==237 and all(Path(r['path']).is_file() for r in plan['roms'])
    assert sum(r['action']=='keep' for r in plan['roms'])==209
    for v in [1266,1316,1344]:
        pin = next(r for r in plan['roms'] if r['name']==f'all_routes_combined_v{v}_candidate.nds')
        assert pin['action']=='keep' and pin['reason'].startswith('pinned:')
    paths = {Path('dk4tool/patch/ship_sinking_editorial.py'),Path('scripts/build_integrated_release.py'),
        Path('translations/ship_sinking_editorial_release_v1.json'),Path('translations/release_stack.json'),
        Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json'),
        Path('docs/ship_sinking_v1327_source_checkpoint.md'),Path('docs/ship_sinking_v1348_integrated_checkpoint.md'),
        Path('docs/translation_progress.md'),Path('docs/editorial_review_goal.md'),Path('docs/known_issues.md'),Path('docs/todo.md'),
        Path(release['candidate']).with_suffix('.manifest.json'),Path(release['patch']),RETENTION}
    paths.update(Path('translations').glob('ship_sinking_editorial_manuscript_v*.json'))
    pattern = r'_v(?:132[5-9]|133\d|134\d)(?:[a-z])?'
    paths.update(p for p in Path('scripts').glob('*.py') if re.search(pattern+r'\.py$',p.name))
    for folder in Path('work/analysis').iterdir():
        if folder.is_dir() and re.search(pattern+r'$',folder.name):
            paths.update(p for p in folder.rglob('*') if p.is_file() and p.suffix.lower()!='.nds')
    repo = Path.cwd().absolute()
    DEST.mkdir(parents=True)
    archived = []
    for source in sorted(paths,key=lambda p:str(p).lower()):
        assert source.is_file() and source.suffix.lower()!='.nds'
        target = DEST/'Workspace'/source.absolute().relative_to(repo)
        target.parent.mkdir(parents=True,exist_ok=True)
        copy2(source,target)
        digest = sha(source.read_bytes())
        assert sha(target.read_bytes())==digest
        archived.append({'source':str(source),'archive':str(target.relative_to(DEST)),'sha256':digest})
    reports = []
    for mode,frames in [('newgame',4000),('title',1150)]:
        source = Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'ship_sinking_v1344_{mode}'/'capture_report.json'
        report = read(source)
        assert report['frames']==frames and report['ROM_sha256']==release['candidate_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not any(v for k,v in report.items() if k.startswith('synthetic_'))
        ram = report['read_only_capture_RAM_snapshots']+report.get('read_only_pause_RAM_snapshots',[])
        for row in ram:
            assert sha(Path(row['path']).read_bytes())==row['sha256']
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
        target = DEST/'Capture reports'/mode/'capture_report.json'
        target.parent.mkdir(parents=True)
        copy2(source,target)
        assert source.read_bytes()==target.read_bytes()
        reports.append({'report':str(source),'sha256':sha(source.read_bytes()),'terminal_frame':frames,
            'RAM_references':len(ram),'PNG_references':len(report['frames_captured']),
            'all_primary_E_references_hash_verified':True})
    bound = read('work/analysis/ship_name_bound_v1335b/original_ship_rename_capacity.json')
    old_report = Path(bound['source_report'])
    report = read(old_report)
    image = next(r for r in report['frames_captured'] if r['frame']==13700)
    old_files = [old_report,Path(bound['snapshot']),Path(image['path'])]
    assert sha(old_report.read_bytes())==bound['source_report_sha256']
    assert sha(old_files[1].read_bytes())==bound['snapshot_sha256']
    assert sha(old_files[2].read_bytes())==image['PNG_sha256']
    for source in old_files:
        target = DEST/'Earlier source ship editor - not finalized guide'/source.name
        target.parent.mkdir(exist_ok=True)
        copy2(source,target)
        assert source.read_bytes()==target.read_bytes()
    receipt = {'archive':str(DEST),'files':archived,'file_count':len(archived),'startup_capture_reports':reports,
        'earlier_source_editor_files_copied_to_E_without_moving_originals':[str(p) for p in old_files],
        'candidate':release['candidate'],'candidate_sha256':release['candidate_sha256'],
        'patch':release['patch'],'patch_sha256':release['patch_sha256'],
        'native_integrated_records':16,'completed_entries_added':0,'completed':1302,'source_prose_reviewed':1395,
        'reviewed_incomplete_COMMON':93,'original_sinking_events_GPU_dismissals_and_transitions_pending':True,
        'all237_ROMs_still_present_preview_only_no_ApplyPlan':True,
        'all_originals_preserved_no_ROM_deleted_moved_or_rebuilt':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    ROOT.mkdir(parents=True)
    save(ROOT/'archive_receipt.json',receipt)
    save(DEST/'archive_receipt.json',receipt)
    print(f'{len(archived)} sinking checkpoint files archived;both startup reports/RAM/PNGs verified;all237 ROMs retained.',flush=True)


if __name__=='__main__':
    main()
