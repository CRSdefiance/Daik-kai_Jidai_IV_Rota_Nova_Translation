"""Preserve the integrated32-reaction checkpoint and scoped terminal controls."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_reaction_archive_v1500')
DEST=Path('E:/Rota Nova translations/Editorial review/V1500 Battle reaction integration checkpoint')
RETENTION=Path('work/rom_retention/20261022T1047532552618Z.json')

if __name__=='__main__':
    assert not ROOT.exists() and not DEST.exists()
    release=read('work/analysis/battle_reaction_release_v1491/registered_release_verification.json')
    checkpoint=read('work/analysis/battle_reaction_integration_v1499/integration_receipt.json')
    assert checkpoint['candidate_sha256']==release['candidate_sha256'] and checkpoint['completed_entries_added']==0
    plan=read(RETENTION)
    assert len(plan['roms'])==247 and all(Path(r['path']).is_file() for r in plan['roms'])
    assert not RETENTION.with_suffix('.result.json').exists() and not RETENTION.with_suffix('.journal.jsonl').exists()
    for version in [1456,1492]:
        assert next(r for r in plan['roms'] if r['name']==f'all_routes_combined_v{version}_candidate.nds')['reason'].startswith('pinned:')
    config=read('translations/battle_reaction_editorial_release_v1.json')
    paths={Path(p) for p in config['dependencies']}
    for name,digest in config['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    paths.update([Path(__file__),RETENTION,Path('translations/rom_retention_pins.json'),Path('translations/editorial_review_current_v1.json'),
        Path('translations/release_stack.json'),Path('translations/battle_reaction_editorial_release_v1.json'),
        Path('docs/battle_reactions_v1481_source_checkpoint.md'),Path('docs/battle_reactions_v1489_native_checkpoint.md'),
        Path('docs/battle_reactions_v1499_integration_checkpoint.md'),Path(release['candidate']).with_suffix('.manifest.json'),
        Path('scripts/build_integrated_release.py')])
    for name in ['docs/known_issues.md','docs/todo.md','docs/translation_progress.md','docs/editorial_review_goal.md',
        'scripts/verify_battle_reaction_release_v1493.py','scripts/run_battle_reaction_startup_v1494.py',
        'scripts/recheck_shop_formatting_v1495.py','scripts/native_battle_reaction_control_v1496.py',
        'scripts/run_battle_reaction_control_v1497.py','scripts/verify_battle_reaction_control_v1498.py',
        'scripts/record_battle_reaction_integration_v1499.py']:
        paths.add(Path(name))
    for name in ['battle_reactions_source_v1478','battle_reactions_context_v1479','battle_reactions_source_review_v1481',
        'battle_reaction_scope_capacity_v1482','battle_reaction_payload_v1484','battle_reaction_runtime_v1485',
        'battle_reaction_fonts_v1486','battle_reaction_copies_v1487','battle_reaction_escape_v1488',
        'battle_reaction_native_review_v1489','battle_reaction_release_v1491','battle_reaction_control_v1497',
        'battle_reaction_control_verified_v1498','battle_reaction_integration_v1499']:
        paths.update(p for p in (Path('work/analysis')/name).glob('*') if p.is_file() and p.suffix.lower() not in ['.nds','.log'])
    ROOT.mkdir(parents=True);DEST.mkdir(parents=True);workspace=Path.cwd().absolute();copied=[]
    for source in sorted(paths):
        # Lexical paths retain the work/analysis junction's workspace identity.
        target=DEST/'workspace'/source.absolute().relative_to(workspace)
        target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        digest=sha(source.read_bytes());assert sha(target.read_bytes())==digest
        copied.append({'source':str(source),'archive':str(target),'sha256':digest})
    cohorts=[]
    for name in ['battle_reaction_v1492_newgame','battle_reaction_v1492_title','battle_reaction_control_v1497_1492']:
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
        cohorts.append({'report':str(report_path),'report_sha256':sha(report_path.read_bytes()),'terminal_frame':report['frames'],
            'primary_E_drive_evidence_verified_and_preserved':refs})
    refs=[]
    for key in ['candidate','patch']:
        path=Path(release[key]);assert sha(path.read_bytes())==release[key+'_sha256']
        refs.append({'path':str(path),'sha256':release[key+'_sha256']})
    guide=Path('E:/Rota Nova translations/Guide screenshots/V1492 Previous capture control');guide_rows=[]
    for source in sorted(guide.iterdir()):
        assert source.is_file();target=DEST/'guide'/source.name
        target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        digest=sha(source.read_bytes());assert sha(target.read_bytes())==digest
        guide_rows.append({'source':str(source),'archive':str(target),'sha256':digest})
    receipt={'archive':str(DEST),'workspace_files':copied,'terminal_cohorts':cohorts,'guide_files':guide_rows,
        'ROM_and_exact_patch_references':refs,'retention_preview_only':str(RETENTION),'all247_ROMs_preserved':True,
        'retention_keep_count':211,'retention_proposed_count_not_applied':36,
        'no_originals_moved_deleted_or_replaced':True,'no_new32_reaction_family_gameplay_completion_credit':True,
        'completed':1323,'source_prose':1467,'reviewed_incomplete_COMMON':144,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'archive_receipt.json',receipt);copy2(ROOT/'archive_receipt.json',DEST/'archive_receipt.json')
    print('Integrated reaction checkpoint archived:',len(copied),'workspace files,3 terminal cohorts;all247 ROMs retained. Original new reaction scenes remain pending.')
