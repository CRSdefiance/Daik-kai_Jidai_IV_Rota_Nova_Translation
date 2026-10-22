"""Archive eight new prose reviews and the terminal Carronade pilot on E."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/battle_victory_archive_v1395')
DEST = Path('E:/Rota Nova translations/Editorial review/V1395 Victory source review')
RETENTION = Path('work/rom_retention/20261022T0418312408201Z.json')


if __name__=='__main__':
    assert not ROOT.exists() and not DEST.exists()
    completion = read('work/analysis/battle_victory_source_v1394/source_review_receipt.json')
    assert (completion['completed'],completion['source_prose'],completion['source_prose_reviews_added'])==(1307,1403,8)
    ledger = read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==1307 and ledger['records_with_source_and_prose_pass']==1403
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==96
    plan = read(RETENTION)
    assert len(plan['roms'])==239 and all(Path(r['path']).is_file() for r in plan['roms'])
    assert not RETENTION.with_suffix('.result.json').exists() and not RETENTION.with_suffix('.journal.jsonl').exists()
    for version in [1266,1316,1344,1364]:
        row = next(r for r in plan['roms'] if r['name']==f'all_routes_combined_v{version}_candidate.nds')
        assert row['action']=='keep' and row['reason'].startswith('pinned:')
    release = read('work/analysis/flagship_precision_release_v1363/registered_release_verification.json')
    for kind in ['candidate','patch']:
        assert sha(Path(release[kind]).read_bytes())==release[kind+'_sha256']
    pilot_path = Path('work/analysis/carronade_verified_v1390/terminal_carronade_verification.json')
    pilot = read(pilot_path)
    report_path = Path(pilot['terminal_report'])
    assert sha(report_path.read_bytes())==pilot['terminal_report_sha256']
    report = read(report_path)
    assert report['frames']==11880 and pilot['no_sinking_notice_or_new_translation_completion_credit']
    paths = [Path(__file__),RETENTION,pilot_path,
        Path('translations/battle_victory_editorial_manuscript_v1.json'),
        Path('translations/editorial_review_current_v1.json'),
        Path('docs/battle_victory_v1394_source_checkpoint.md')]
    paths += [Path(p) for p in ['docs/known_issues.md','docs/todo.md','docs/translation_progress.md',
        'docs/editorial_review_goal.md','scripts/native_carronade_fixture_v1387.py',
        'scripts/run_carronade_sinking_v1388.py','scripts/inspect_carronade_sinking_v1389.py',
        'scripts/verify_carronade_pilot_v1390.py','scripts/research_battle_victory_v1392.py',
        'scripts/research_battle_victory_v1392b.py','scripts/author_battle_victory_v1393.py',
        'scripts/record_battle_victory_source_v1394.py',
        'work/analysis/flagship_precision_release_v1363/registered_release_verification.json',
        'work/analysis/flagship_precision_release_v1363/photographed_shop_formatting.json']]
    for folder in ['work/analysis/carronade_sinking_v1388','work/analysis/carronade_inspection_v1389',
        'work/analysis/carronade_verified_v1390','work/analysis/battle_victory_context_v1392b',
        'work/analysis/battle_victory_source_v1394']:
        paths += list(Path(folder).glob('*.json'))+list(Path(folder).glob('*.jsonl'))
    ROOT.mkdir(parents=True)
    DEST.mkdir(parents=True)
    copied = []
    workspace = Path.cwd().absolute()
    for source in sorted(set(paths)):
        target = DEST/'workspace'/source.absolute().relative_to(workspace)
        target.parent.mkdir(parents=True,exist_ok=True)
        copy2(source,target)
        digest = sha(source.read_bytes())
        assert sha(target.read_bytes())==digest
        copied.append({'source':str(source),'archive':str(target),'sha256':digest})
    references = []
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
        references.append({'path':row['path'],'sha256':row['PNG_sha256'],'kind':'PNG'})
    for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        assert sha(Path(row['path']).read_bytes())==row['sha256']
        references.append({'path':row['path'],'sha256':row['sha256'],'kind':'read-only-RAM'})
    for name in ['capture_report.json','navigation_command_journal.json']:
        source = report_path.parent/name
        target = DEST/'terminal_records'/name
        target.parent.mkdir(parents=True,exist_ok=True)
        copy2(source,target)
        assert sha(target.read_bytes())==sha(source.read_bytes())
    context = read('work/analysis/battle_victory_context_v1392b/source_and_original_victory_context.json')
    old = context['prior_actual_2131']
    for key in ['capture','snapshot','report']:
        assert sha(Path(old[key]).read_bytes())==old[key+'_sha256']
    receipt = {'archive':str(DEST),'workspace_files':copied,'terminal_pilot_report':str(report_path),
        'terminal_pilot_report_sha256':sha(report_path.read_bytes()),
        'original_E_drive_capture_and_RAM_references_verified_and_preserved':references,
        'earlier_actual2131_context_references_verified':old,
        'completed_unchanged':1307,'source_prose':1403,'new_source_prose':8,'reviewed_incomplete_COMMON':96,
        'retention_preview_only':str(RETENTION),'all239_ROMS_preserved':True,
        'retention_plan_keep_count':sum(r['action']=='keep' for r in plan['roms']),
        'retention_proposed_count_not_applied':sum(r['action']=='delete' for r in plan['roms']),
        'no_ROM_build_change_move_deletion_or_new_finalized_guide_claim':True,
        'all16_sinking_entries_native_but_actual_scenes_still_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'archive_receipt.json',receipt)
    copy2(ROOT/'archive_receipt.json',DEST/'archive_receipt.json')
    print(f'Victory source review archived:{len(copied)} files;1403 reviewed/1307 complete;all239 ROMs preserved;full goal active.',flush=True)
