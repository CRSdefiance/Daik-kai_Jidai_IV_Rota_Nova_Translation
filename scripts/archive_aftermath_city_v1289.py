"""Preserve city-defense verification and uncredited navigation research on E."""
import re
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

DEST = Path('E:/Rota Nova translations/Editorial review/V1289 City defense verification')
ROOT = Path('work/analysis/aftermath_city_archive_v1289')


def main():
    assert not DEST.exists() and not ROOT.exists()
    repo = Path.cwd().absolute()
    ledger = read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed'] == 1288 and ledger['records_with_source_and_prose_pass'] == 1373
    release = read('work/analysis/battle_aftermath_release_v1265/registered_release_verification.json')
    for field in ['candidate', 'patch']:
        assert sha(Path(release[field]).read_bytes()) == release[field+'_sha256']
    files = {Path('translations/editorial_review_current_v1.json'), Path('translations/release_stack.json'),
        Path('translations/rom_retention_pins.json'), Path('translations/battle_aftermath_city_defense_final_review_v1.json'),
        Path('translations/battle_aftermath_editorial_manuscript_v3.json'),
        Path('docs/aftermath_city_v1288_completion.md'), Path('docs/editorial_review_goal.md'),
        Path('docs/translation_progress.md'), Path('docs/known_issues.md'), Path('docs/todo.md')}
    files.update(path for path in Path('scripts').glob('*.py') if re.search(r'_v128[0-9](?:[a-z])?\.py$', path.name))
    for folder in Path('work/analysis').iterdir():
        if folder.is_dir() and re.search(r'_v128[0-8](?:[a-z])?$', folder.name):
            files.update(path for path in folder.rglob('*') if path.is_file() and path.suffix.lower() != '.nds')
    retention = max(Path('work/rom_retention').glob('*.json'), key=lambda p:p.stat().st_mtime)
    plan = read(retention)
    pin = next(row for row in plan['roms'] if row['name'] == 'all_routes_combined_v1266_candidate.nds')
    assert pin['action'] == 'keep' and pin['reason'].startswith('pinned:')
    assert all(Path(row['path']).is_file() for row in plan['roms'])
    files.add(retention)
    DEST.mkdir(parents=True)
    archived = []
    for source in sorted(files, key=lambda p:str(p).lower()):
        assert source.is_file() and source.suffix.lower() != '.nds'
        target = DEST/'Workspace'/source.absolute().relative_to(repo)
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, target)
        digest = sha(source.read_bytes())
        assert sha(target.read_bytes()) == digest
        archived.append({'source':str(source), 'archive':str(target.relative_to(DEST)), 'sha256':digest})
    captures = []
    for name in ['aftermath_navigation_v1281_1266', 'aftermath_city_v1283b_1266', 'aftermath_city_v1286_1266']:
        report_path = Path('E:/Rota Nova translations/Generated/work/emulation_v193')/name/'capture_report.json'
        report = read(report_path)
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['ROM_sha256'] == release['candidate_sha256']
        ram = report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']
        for row in ram:
            assert sha(Path(row['path']).read_bytes()) == row['sha256']
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        target = DEST/'Capture reports'/name/'capture_report.json'
        target.parent.mkdir(parents=True)
        copy2(report_path, target)
        assert sha(target.read_bytes()) == sha(report_path.read_bytes())
        captures.append({'report':str(report_path), 'report_sha256':sha(report_path.read_bytes()),
            'terminal_frame':report['frames'], 'RAM_references':len(ram), 'PNG_references':len(report['frames_captured']),
            'all_primary_E_RAM_and_PNG_hashes_verified':True, 'archived_report':str(target.relative_to(DEST))})
    guide_files = []
    guide = Path('E:/Rota Nova translations/Guide screenshots/V1266 City defense')
    for source in guide.iterdir():
        assert source.is_file()
        target = DEST/'Guide screenshots'/source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        guide_files.append({'source':str(source), 'archive':str(target.relative_to(DEST)), 'sha256':sha(target.read_bytes())})
    result = {'archive':str(DEST), 'files':archived, 'file_count':len(archived), 'capture_reports':captures,
        'guide_files':guide_files, 'candidate':release['candidate'], 'candidate_sha256':release['candidate_sha256'],
        'patch':release['patch'], 'patch_sha256':release['patch_sha256'],
        'complete':1288, 'source_prose':1373, 'aftermath_complete':28, 'aftermath_pending':47,
        'retention_preview':str(retention), 'all_ROMs_in_preview_still_present':len(plan['roms']),
        'all_originals_preserved_no_ROM_deleted_moved_or_rebuilt':True,
        'all_archived_and_primary_capture_references_hash_verified':True,
        'no_uncredited_pilot_translation_completion':True, 'full_goal_complete':False,
        'producer_sha256':sha(Path(__file__).read_bytes())}
    ROOT.mkdir(parents=True)
    save(ROOT/'archive_receipt.json', result)
    save(DEST/'archive_receipt.json', result)
    print(f'{len(archived)} checkpoint files archived;all3 terminal capture/RAM sets and guide files verified.', flush=True)


if __name__ == '__main__':
    main()
