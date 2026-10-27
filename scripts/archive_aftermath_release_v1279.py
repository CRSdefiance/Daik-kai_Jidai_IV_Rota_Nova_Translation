"""Archive release and two actual outcome audits without moving any original."""
import re
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

DESTINATION = Path('E:/Rota Nova translations/Editorial review/V1279 Aftermath release and outcome verification')
RETENTION = Path('work/rom_retention/20261021T2304265871364Z.json')


def main():
    assert not DESTINATION.exists()
    repo = Path.cwd().absolute()
    release_path = Path('work/analysis/battle_aftermath_release_v1265/registered_release_verification.json')
    release = read(release_path)
    assert sha(Path(release['candidate']).read_bytes()) == release['candidate_sha256']
    assert sha(Path(release['patch']).read_bytes()) == release['patch_sha256']
    previous_archive = Path('E:/Rota Nova translations/Editorial review/V1264 Aftermath native checkpoint/archive_receipt.json')
    assert read(previous_archive)['all_archived_files_hash_checked']
    ledger = read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed'] == 1280 and ledger['records_with_source_and_prose_pass'] == 1373
    paths = {Path('dk4tool/patch/battle_aftermath_editorial.py'),Path('scripts/build_integrated_release.py'),
        Path('translations/battle_aftermath_editorial_release_v1.json'),Path('translations/release_stack.json'),
        Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json'),
        Path('translations/battle_aftermath_editorial_manuscript_v3.json'),
        Path('translations/battle_aftermath_fled_final_review_v1.json'),
        Path('translations/battle_aftermath_defeat_final_review_v1.json'),
        Path('docs/aftermath_fled_v1273_completion.md'),Path('docs/aftermath_defeat_v1277_completion.md'),
        Path('docs/translation_progress.md'),Path('docs/known_issues.md'),Path('docs/todo.md'),
        Path(release['candidate']).with_suffix('.manifest.json'),Path(release['patch']),RETENTION}
    paths.update(p for p in Path('scripts').glob('*.py') if re.search(r'_v(?:126[5-9]|127\d)(?:[a-z])?\.py$',p.name))
    for folder in Path('work/analysis').iterdir():
        if folder.is_dir() and re.search(r'_v(?:126[5-9]|127\d)(?:[a-z])?$',folder.name):
            paths.update(p for p in folder.rglob('*') if p.is_file() and p.suffix.lower() != '.nds')
    plan = read(RETENTION)
    assert len(plan['roms']) == 233 and all(Path(r['path']).is_file() for r in plan['roms'])
    assert sum(r['action'] == 'keep' for r in plan['roms']) == 205
    current_pin = next(r for r in plan['roms'] if r['name'] == 'all_routes_combined_v1266_candidate.nds')
    assert current_pin['action'] == 'keep' and current_pin['reason'].startswith('pinned:')
    DESTINATION.mkdir(parents=True)
    files = []
    for path in sorted(paths,key=lambda p:str(p).lower()):
        assert path.is_file() and path.suffix.lower() != '.nds'
        relative = path.absolute().relative_to(repo)
        target = DESTINATION/'Workspace'/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        copy2(path,target)
        digest = sha(path.read_bytes())
        assert sha(target.read_bytes()) == digest
        files.append({'source':str(path),'archive':str(target.relative_to(DESTINATION)),
            'sha256':digest,'bytes':target.stat().st_size})
    references = []
    for folder in ('aftermath_victory_v1270_1266','aftermath_defeat_v1275_1266'):
        report_path = Path('E:/Rota Nova translations/Generated/work/emulation_v193')/folder/'capture_report.json'
        report = read(report_path)
        ram = report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']
        for row in ram:
            assert sha(Path(row['path']).read_bytes()) == row['sha256']
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        target = DESTINATION/'Capture reports'/folder/'capture_report.json'
        target.parent.mkdir(parents=True)
        copy2(report_path,target)
        assert target.read_bytes() == report_path.read_bytes()
        references.append({'report':str(report_path),'sha256':sha(report_path.read_bytes()),
            'archived_report':str(target.relative_to(DESTINATION)),
            'all_primary_E_drive_RAM_and_capture_references_hash_verified':True,
            'RAM_snapshots':len(ram),'PNG_captures':len(report['frames_captured']),
            'all_primary_capture_files_retained_without_moving_or_deleting':True})
    guide_files = []
    for name in ('V1266 Battle aftermath','V1266 Defeat aftermath'):
        folder = Path('E:/Rota Nova translations/Guide screenshots')/name
        for source in folder.iterdir():
            if source.is_file():
                target = DESTINATION/'Guide screenshots'/name/source.name
                target.parent.mkdir(parents=True,exist_ok=True)
                copy2(source,target)
                assert source.read_bytes() == target.read_bytes()
                guide_files.append({'source':str(source),'archive':str(target.relative_to(DESTINATION)),
                    'sha256':sha(source.read_bytes())})
    receipt = {'archive':str(DESTINATION),'files':files,'file_count':len(files),
        'primary_native_evidence_archive':str(previous_archive),'primary_native_archive_receipt_sha256':sha(previous_archive.read_bytes()),
        'capture_reports_and_verified_primary_files':references,'guide_files':guide_files,
        'candidate':release['candidate'],'candidate_sha256':release['candidate_sha256'],
        'patch':release['patch'],'patch_sha256':release['patch_sha256'],
        'all233_ROMs_still_present_retention_preview_only_no_ApplyPlan':True,
        'all_originals_and_canonical_preserved_no_ROMs_deleted_moved_or_rebuilt_by_archive':True,
        'complete':1280,'source_prose':1373,'aftermath_records_complete':20,'aftermath_records_pending':55,
        'all_copies_and_referenced_capture_files_hash_verified':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(DESTINATION/'archive_receipt.json',receipt)
    audit = Path('work/analysis/aftermath_archive_v1279')
    assert not audit.exists()
    audit.mkdir(parents=True)
    save(audit/'archive_receipt.json',receipt)
    print(str(len(files))+' release/checkpoint files archived and all capture/RAM references verified. All233 ROMs retained.',flush=True)


if __name__ == '__main__':
    main()
