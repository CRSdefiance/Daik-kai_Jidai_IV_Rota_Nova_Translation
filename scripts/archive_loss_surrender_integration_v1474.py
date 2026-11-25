"""Archive an incomplete integration checkpoint and its terminal control evidence."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/loss_surrender_archive_v1474')
DEST=Path('E:/Rota Nova translations/Editorial review/V1474 Loss surrender integration checkpoint')
RETENTION=Path('work/rom_retention/20261022T0658293916922Z.json')

def main():
    assert not ROOT.exists() and not DEST.exists()
    release=read('work/analysis/ship_loss_surrender_release_v1455/registered_release_verification.json')
    checkpoint=read('work/analysis/ship_loss_surrender_integration_v1473/integration_receipt.json')
    assert checkpoint['candidate_sha256']==release['candidate_sha256'] and checkpoint['completed_entries_added']==0
    plan=read(RETENTION)
    assert len(plan['roms'])==245 and all(Path(r['path']).is_file() for r in plan['roms'])
    assert not RETENTION.with_suffix('.result.json').exists() and not RETENTION.with_suffix('.journal.jsonl').exists()
    assert next(r for r in plan['roms'] if r['name']=='all_routes_combined_v1456_candidate.nds')['reason'].startswith('pinned:')
    config=read('translations/ship_loss_surrender_editorial_release_v1.json')
    paths={Path(__file__),RETENTION,Path('translations/rom_retention_pins.json'),Path('translations/editorial_review_current_v1.json'),
        Path('translations/release_stack.json'),Path('translations/ship_loss_surrender_editorial_release_v1.json'),
        Path('docs/ship_loss_surrender_v1473_integration_checkpoint.md'),Path('dk4tool/patch/ship_loss_surrender_editorial.py'),
        Path(release['candidate']).with_suffix('.manifest.json')}
    for name,digest in config['dependencies'].items():
        path=Path(name);assert sha(path.read_bytes())==digest;paths.add(path)
    for name in ['docs/known_issues.md','docs/todo.md','docs/translation_progress.md','docs/editorial_review_goal.md',
        'scripts/register_ship_loss_surrender_v1455.py','scripts/verify_ship_loss_surrender_release_v1457.py',
        'scripts/run_ship_loss_surrender_startup_v1458.py','scripts/recheck_shop_formatting_v1459.py',
        'scripts/native_loss_surrender_fixture_v1460.py','scripts/run_loss_surrender_control_v1461b.py',
        'scripts/verify_loss_surrender_control_v1465.py','scripts/research_combat_approach_v1462.py',
        'scripts/native_combat_approach_fixture_v1463.py','scripts/run_combat_approach_v1464.py',
        'scripts/native_close_approach_fixture_v1467.py','scripts/run_close_combat_approach_v1468.py',
        'scripts/research_original_fleet_guns_v1469.py','scripts/verify_approach_pilots_v1470.py',
        'scripts/record_loss_surrender_integration_v1473.py']:
        paths.add(Path(name))
    for name in ['ship_loss_surrender_release_v1455','loss_surrender_control_v1461b','loss_surrender_control_verified_v1465',
        'combat_approach_v1462','combat_approach_fixture_v1463','combat_approach_v1464',
        'close_approach_fixture_v1467','close_combat_approach_v1468','original_fleet_guns_v1469',
        'approach_pilots_verified_v1470','ship_loss_surrender_integration_v1473']:
        # Growing survey logs are excluded; incomplete live runs are not terminal cohorts.
        paths.update(p for p in (Path('work/analysis')/name).glob('*') if p.is_file()
            and p.suffix.lower() not in ['.nds','.log'])
    ROOT.mkdir(parents=True);DEST.mkdir(parents=True);workspace=Path.cwd().absolute();copied=[]
    for source in sorted(paths):
        target=DEST/'workspace'/source.absolute().relative_to(workspace)
        target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        digest=sha(source.read_bytes());assert sha(target.read_bytes())==digest
        copied.append({'source':str(source),'archive':str(target),'sha256':digest})
    cohorts=[]
    for name in ['loss_surrender_v1456_newgame','loss_surrender_v1456_title',
        'loss_surrender_control_v1461b_1456','combat_approach_v1464_1456','close_combat_approach_v1468_1456']:
        cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/name
        report_path=cap/'capture_report.json';report=read(report_path)
        assert report['ROM_sha256']==release['candidate_sha256'] and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors'] and not report['hardware_device_verification']
        refs=[]
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
            refs.append({'path':row['path'],'sha256':row['PNG_sha256'],'kind':'PNG'})
        for key in ['read_only_capture_RAM_snapshots','read_only_pause_RAM_snapshots']:
            for row in report.get(key,[]):
                assert sha(Path(row['path']).read_bytes())==row['sha256']
                refs.append({'path':row['path'],'sha256':row['sha256'],'kind':'RAM'})
        for record in ['capture_report.json','navigation_command_journal.json']:
            source=cap/record
            if source.is_file():
                target=DEST/'terminal_records'/name/record;target.parent.mkdir(parents=True,exist_ok=True)
                copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        cohorts.append({'report':str(report_path),'report_sha256':sha(report_path.read_bytes()),
            'terminal_frame':report['frames'],'primary_E_drive_evidence_preserved':refs})
    refs=[]
    for key in ['candidate','patch']:
        path=Path(release[key]);assert sha(path.read_bytes())==release[key+'_sha256']
        refs.append({'path':str(path),'sha256':release[key+'_sha256']})
    guide=Path('E:/Rota Nova translations/Guide screenshots/V1456 Previous capture control');guide_rows=[]
    for source in sorted(guide.iterdir()):
        assert source.is_file();target=DEST/'guide'/source.name
        target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        digest=sha(source.read_bytes());assert sha(target.read_bytes())==digest
        guide_rows.append({'source':str(source),'archive':str(target),'sha256':digest})
    receipt={'archive':str(DEST),'workspace_files':copied,'terminal_cohorts':cohorts,'guide_files':guide_rows,
        'ROM_and_exact_patch_references':refs,'retention_preview_only':str(RETENTION),'all245_ROMs_preserved':True,
        'retention_keep_count':209,'retention_proposed_count_not_applied':36,
        'no_originals_moved_deleted_or_replaced':True,'no_new_report_family_completion_credit':True,
        'completed':1323,'source_prose':1435,'reviewed_incomplete_COMMON':112,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'archive_receipt.json',receipt);copy2(ROOT/'archive_receipt.json',DEST/'archive_receipt.json')
    print('Integration checkpoint archived:',len(copied),'workspace files,5 terminal cohorts;all245 ROMs retained. New report events remain pending.')

if __name__=='__main__':main()
