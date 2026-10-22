"""Archive the completed eight-message victory family and terminal evidence."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/battle_victory_archive_v1412')
DEST = Path('E:/Rota Nova translations/Editorial review/V1412 Victory reports completed')
RETENTION = Path('work/rom_retention/20261022T0445599603149Z.json')


if __name__=='__main__':
    assert not ROOT.exists() and not DEST.exists()
    completion = read('work/analysis/battle_victory_completion_v1411/completion_receipt.json')
    assert (completion['completed'],completion['source_prose'],completion['newly_completed'])==(1315,1403,8)
    ledger = read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==1315 and ledger['records_with_source_and_prose_pass']==1403
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==88
    plan = read(RETENTION)
    assert len(plan['roms'])==241 and all(Path(r['path']).is_file() for r in plan['roms'])
    assert not RETENTION.with_suffix('.result.json').exists() and not RETENTION.with_suffix('.journal.jsonl').exists()
    for version in [1105,1266,1316,1344,1364,1404]:
        pin = next(r for r in plan['roms'] if r['name']==f'all_routes_combined_v{version}_candidate.nds')
        assert pin['action']=='keep' and pin['reason'].startswith('pinned:')
    release = read('work/analysis/battle_victory_release_v1403/registered_release_verification.json')
    rom_refs = []
    for field in ['candidate','patch']:
        path = Path(release[field])
        assert sha(path.read_bytes())==release[field+'_sha256']
        rom_refs.append({'path':str(path),'sha256':release[field+'_sha256'],'kind':field})
    manifest = Path(release['candidate']).with_suffix('.manifest.json')
    assert sha(manifest.read_bytes())==release['manifest_sha256']
    paths = {Path(__file__),RETENTION,manifest,Path('scripts/build_integrated_release.py'),
        Path('translations/release_stack.json'),Path('translations/rom_retention_pins.json'),
        Path('translations/editorial_review_current_v1.json'),Path('translations/battle_victory_final_review_v1.json'),
        Path('translations/battle_victory_editorial_release_v1.json'),Path('docs/battle_victory_v1411_completion.md')}
    config = read('translations/battle_victory_editorial_release_v1.json')
    for name,digest in config['dependencies'].items():
        path = Path(name)
        assert sha(path.read_bytes())==digest
        paths.add(path)
    paths.update(Path(n) for n in ['docs/known_issues.md','docs/todo.md','docs/translation_progress.md',
        'docs/editorial_review_goal.md','scripts/verify_battle_victory_release_v1405.py',
        'scripts/run_battle_victory_startup_v1406.py','scripts/recheck_shop_formatting_v1407.py',
        'scripts/native_battle_victory_fixture_v1408.py','scripts/run_battle_victory_replay_v1409.py',
        'scripts/verify_battle_victory_replay_v1410.py','scripts/complete_battle_victory_v1411.py',
        'scripts/native_ship_sinking_fixture_v1351.py','scripts/native_ship_sinking_fixture_v1352.py'])
    for folder in ['work/analysis/battle_victory_payload_v1396','work/analysis/battle_victory_fonts_v1397b',
        'work/analysis/battle_victory_copies_v1399','work/analysis/battle_victory_escape_v1400',
        'work/analysis/battle_victory_native_review_v1401','work/analysis/battle_victory_release_v1403',
        'work/analysis/battle_victory_replay_v1409','work/analysis/battle_victory_verified_v1410',
        'work/analysis/battle_victory_completion_v1411']:
        paths.update(p for p in Path(folder).glob('*') if p.is_file() and p.suffix.lower()!='.nds')
    ROOT.mkdir(parents=True)
    DEST.mkdir(parents=True)
    workspace = Path.cwd().absolute()
    copied = []
    for source in sorted(paths):
        target = DEST/'workspace'/source.absolute().relative_to(workspace)
        target.parent.mkdir(parents=True,exist_ok=True)
        copy2(source,target)
        digest = sha(source.read_bytes())
        assert sha(target.read_bytes())==digest
        copied.append({'source':str(source),'archive':str(target),'sha256':digest})
    cohorts = []
    for name in ['battle_victory_v1404_newgame','battle_victory_v1404_title','battle_victory_v1409_1404']:
        cap = Path('E:/Rota Nova translations/Generated/work/emulation_v193')/name
        report_path = cap/'capture_report.json'
        report = read(report_path)
        assert report['ROM_sha256']==release['candidate_sha256'] and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors'] and not report['hardware_device_verification']
        refs = []
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
            refs.append({'path':row['path'],'sha256':row['PNG_sha256'],'kind':'PNG'})
        for key in ['read_only_capture_RAM_snapshots','read_only_pause_RAM_snapshots']:
            for row in report.get(key,[]):
                assert sha(Path(row['path']).read_bytes())==row['sha256']
                refs.append({'path':row['path'],'sha256':row['sha256'],'kind':'read-only-RAM'})
        for record in ['capture_report.json','navigation_command_journal.json']:
            source = cap/record
            if source.exists():
                target = DEST/'terminal_records'/name/record
                target.parent.mkdir(parents=True,exist_ok=True)
                copy2(source,target)
                assert sha(target.read_bytes())==sha(source.read_bytes())
        cohorts.append({'report':str(report_path),'report_sha256':sha(report_path.read_bytes()),
            'terminal_frame':report['frames'],'original_E_drive_primary_evidence_verified_and_preserved':refs})
    guide = Path('E:/Rota Nova translations/Guide screenshots/V1404 Victory reports')
    guide_rows = []
    for source in sorted(guide.iterdir()):
        assert source.is_file()
        target = DEST/'guide'/source.name
        target.parent.mkdir(parents=True,exist_ok=True)
        copy2(source,target)
        digest = sha(source.read_bytes())
        assert sha(target.read_bytes())==digest
        guide_rows.append({'source':str(source),'archive':str(target),'sha256':digest})
    receipt = {'archive':str(DEST),'workspace_files':copied,'terminal_cohorts':cohorts,
        'verified_guide_files':guide_rows,'original_ROM_and_exact_patch_references_preserved':rom_refs,
        'completed':1315,'source_prose':1403,'newly_completed':8,'reviewed_incomplete_COMMON':88,
        'all16_sinking_entries_still_pending':True,'retention_preview_only':str(RETENTION),
        'all241_ROMs_preserved':True,'retention_keep_count':sum(r['action']=='keep' for r in plan['roms']),
        'retention_proposed_count_not_applied':sum(r['action']=='delete' for r in plan['roms']),
        'no_originals_moved_deleted_or_replaced_no_canonical_promotion':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'archive_receipt.json',receipt)
    copy2(ROOT/'archive_receipt.json',DEST/'archive_receipt.json')
    print(f'Victory8 completion archived:{len(copied)} files,3 terminal cohorts,guide evidence;all241 ROMs preserved. Full goal active.',flush=True)
