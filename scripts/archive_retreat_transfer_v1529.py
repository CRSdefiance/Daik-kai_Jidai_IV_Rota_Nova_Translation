"""Archive the complete retreat checkpoint, leaving all original evidence and ROMs intact."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/retreat_transfer_archive_v1529')
DEST = Path('E:/Rota Nova translations/Editorial review/V1529 Replacement-ship retreat completed')
RETENTION = Path('work/rom_retention/20261022T1216120835620Z.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not DEST.exists()
    release = read('work/analysis/retreat_transfer_release_v1519/registered_release_verification.json')
    complete = read('work/analysis/retreat_transfer_completion_v1528/completion_receipt.json')
    assert complete['candidate_sha256'] == release['candidate_sha256'] and complete['newly_completed'] == 7
    retention = read(RETENTION)
    assert len(retention['roms']) == 249 and all(Path(r['path']).is_file() for r in retention['roms'])
    assert not RETENTION.with_suffix('.result.json').exists() and not RETENTION.with_suffix('.journal.jsonl').exists()
    config = read('translations/retreat_transfer_editorial_release_v1.json')
    paths = {Path(p) for p in config['dependencies']}
    for p, digest in config['dependencies'].items():
        assert sha(Path(p).read_bytes()) == digest, p
    paths.update([Path(__file__), RETENTION, Path('translations/rom_retention_pins.json'),
        Path('translations/editorial_review_current_v1.json'), Path('translations/release_stack.json'),
        Path('translations/retreat_transfer_editorial_release_v1.json'), Path('translations/retreat_transfer_final_review_v1.json'),
        Path('translations/promoted_build.json'), Path('docs/retreat_transfer_v1518_native_checkpoint.md'),
        Path('docs/retreat_transfer_v1528_completion.md'), Path('scripts/build_integrated_release.py'),
        Path(release['candidate']).with_suffix('.manifest.json')])
    for name in ['known_issues.md', 'todo.md', 'translation_progress.md', 'editorial_review_goal.md']:
        paths.add(Path('docs') / name)
    for pattern in ['*retreat*v15*.py']:
        paths.update(Path('scripts').glob(pattern))
    for name in ['retreat_transfer_context_v1506', 'retreat_transfer_payload_v1511b', 'retreat_transfer_runtime_v1510',
        'retreat_transfer_fonts_v1512', 'retreat_transfer_payload_v1514', 'retreat_transfer_fonts_v1515',
        'retreat_transfer_copies_v1516', 'retreat_transfer_escape_v1517', 'retreat_transfer_native_review_v1518',
        'retreat_transfer_release_v1519', 'retreat_transfer_fixture_v1523', 'retreat_transfer_replay_v1524',
        'retreat_transfer_control_verified_v1525', 'retreat_transfer_actual_fonts_v1526c',
        'retreat_transfer_actual_pixels_v1526d', 'retreat_transfer_completion_v1528']:
        paths.update(p for p in (Path('work/analysis') / name).glob('*') if p.is_file() and p.suffix.lower() not in ['.nds', '.log', '.dsv'])
    ROOT.mkdir(parents=True)
    DEST.mkdir(parents=True)
    workspace, copied = Path.cwd().absolute(), []
    for source in sorted(paths):
        target = DEST / 'workspace' / source.absolute().relative_to(workspace)
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, target)
        digest = sha(source.read_bytes())
        assert sha(target.read_bytes()) == digest
        copied.append({'source': str(source), 'archive': str(target), 'sha256': digest})
    cohorts = []
    for name in ['retreat_transfer_v1520_newgame', 'retreat_transfer_v1520_title', 'retreat_transfer_v1524_1520']:
        cap = Path('E:/Rota Nova translations/Generated/work/emulation_v193') / name
        report_path = cap / 'capture_report.json'
        report = read(report_path)
        assert report['ROM_sha256'] == release['candidate_sha256'] and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors'] and not report['hardware_device_verification']
        refs = []
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
            refs.append({'path': row['path'], 'sha256': row['PNG_sha256'], 'kind': 'PNG'})
        for key in ['read_only_capture_RAM_snapshots', 'read_only_pause_RAM_snapshots']:
            for row in report.get(key, []):
                assert sha(Path(row['path']).read_bytes()) == row['sha256']
                refs.append({'path': row['path'], 'sha256': row['sha256'], 'kind': 'RAM'})
        for record in ['capture_report.json', 'navigation_command_journal.json']:
            source = cap / record
            if source.is_file():
                target = DEST / 'terminal_records' / name / record
                target.parent.mkdir(parents=True, exist_ok=True)
                copy2(source, target)
                assert sha(source.read_bytes()) == sha(target.read_bytes())
        cohorts.append({'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
            'terminal_frame': report['frames'], 'primary_E_drive_evidence_verified_and_preserved': refs})
    guide_rows = []
    guide = Path('E:/Rota Nova translations/Guide screenshots/V1520 Flagship evacuation and transfer')
    for source in sorted(guide.iterdir()):
        target = DEST / 'guide' / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, target)
        digest = sha(source.read_bytes())
        assert sha(target.read_bytes()) == digest
        guide_rows.append({'source': str(source), 'archive': str(target), 'sha256': digest})
    refs = []
    for key in ['candidate', 'patch']:
        path = Path(release[key])
        assert sha(path.read_bytes()) == release[key + '_sha256']
        refs.append({'path': str(path), 'sha256': release[key + '_sha256']})
    receipt = {'archive': str(DEST), 'workspace_files': copied, 'terminal_cohorts': cohorts,
        'guide_files': guide_rows, 'ROM_and_exact_patch_references': refs, 'retention_preview_only': str(RETENTION),
        'all249_ROMs_preserved': True, 'retention_keep_count': 213, 'retention_proposed_count_not_applied': 36,
        'no_originals_moved_deleted_or_replaced': True, 'completed': 1330, 'source_prose': 1474,
        'reviewed_incomplete_COMMON': 144, 'V1520_experimental_V1492_promoted_and_full_goal_active': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False}
    save(ROOT / 'archive_receipt.json', receipt)
    copy2(ROOT / 'archive_receipt.json', DEST / 'archive_receipt.json')
    print('Retreat7 archived:', len(copied), 'workspace files,3 terminal cohorts,guide screenshots;all249 ROMs retained;goal active.')
