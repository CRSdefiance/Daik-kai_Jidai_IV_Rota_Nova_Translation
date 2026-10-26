"""Archive completed fatigue2 and unapproved hot-spring13 without removing ROMs."""
import ast
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/fatigue_hot_spring_archive_v1613')
DEST=Path('E:/Rota Nova translations/Editorial review/V1613 fatigue complete and hot spring prose')

if __name__=='__main__':
    assert not ROOT.exists() and not DEST.exists()
    completion=read('work/analysis/fatigue_status_completion_v1609/completion_receipt.json')
    review=read('work/analysis/hot_spring_review_v1612/source_review_receipt.json')
    ledger=read('translations/editorial_review_current_v1.json')
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'],len(ledger['reviewed_but_incomplete_COMMON_IDs']))==(1350,1507,157)
    assert review['completed_entries_added']==0 and completion['newly_completed']==2
    config=read('translations/fatigue_status_editorial_release_v1.json');paths={Path(p) for p in config['dependencies']}
    for p,digest in config['dependencies'].items():assert sha(Path(p).read_bytes())==digest,p
    pins_path=Path('translations/rom_retention_pins.json');pins=read(pins_path)
    candidate=Path('E:/Rota Nova translations/Generated/out/screenshot_text_repairs_20261022_candidate.nds')
    assert sha(candidate.read_bytes())=='ba0c910644725ef54a3d817b1754a861244c11fe7c95a06974f32440773bbf54'
    if not any(Path(p['path'])==candidate for p in pins):
        pins.append({'path':str(candidate),'reason':'Current hot-spring source/prose parent preserves later screenshot corrections;changed scenes remain pending.'});save(pins_path,pins)
    scripts=set()
    for pattern in ['*fatigue*v16*.py','*hot_spring*v16*.py']:
        scripts.update(Path('scripts').glob(pattern))
    for p in scripts:ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
    paths.update(scripts)
    paths.update([Path(__file__),pins_path,Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),
        Path('translations/fatigue_status_final_review_v1.json'),Path('translations/hot_spring_editorial_manuscript_v1.json'),
        Path('translations/screenshot_text_repairs_20261022_release_v1.json'),Path('translations/screenshot_text_repairs_20261022_manuscript_v1.json'),
        Path('dk4tool/patch/screenshot_text_repairs.py'),Path('scripts/build_integrated_release.py'),
        Path('out/all_routes_combined_v1594_candidate.manifest.json'),Path('out/screenshot_text_repairs_20261022_candidate.manifest.json')])
    for p in Path('docs').glob('*'):
        if p.is_file() and (p.name in ['editorial_handoff_current.md','known_issues.md','todo.md','translation_progress.md','editorial_review_goal.md','screenshot_text_repairs_20261022.md'] or p.name.startswith(('fatigue_status_v1609','hot_spring_v1612'))):paths.add(p)
    for pattern in ['fatigue*v16*','hot_spring*v16*']:
        for directory in Path('work/analysis').glob(pattern):
            if directory.is_dir() and directory!=ROOT:paths.update(p for p in directory.rglob('*') if p.is_file() and p.suffix.lower() not in ['.nds','.dsv','.log'])
    ROOT.mkdir(parents=True);DEST.mkdir(parents=True);workspace=Path.cwd().absolute();copied=[]
    for source in sorted(paths):
        target=DEST/'workspace'/source.absolute().relative_to(workspace)
        target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target);digest=sha(source.read_bytes());assert sha(target.read_bytes())==digest
        copied.append({'source':str(source),'archive':str(target),'sha256':digest})
    cohorts=[]
    for name in ['fatigue_recovery_live_v1603_1594','fatigue_recovery_live_v1606_1594']:
        cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/name;report_path=cap/'capture_report.json';report=read(report_path)
        assert report['frames']==6200 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and not report['hardware_device_verification']
        refs=[]
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes())==row['PNG_sha256'];refs.append({'path':row['path'],'sha256':row['PNG_sha256'],'kind':'PNG'})
        for key in ['read_only_capture_RAM_snapshots','read_only_pause_RAM_snapshots']:
            for row in report[key]:assert sha(Path(row['path']).read_bytes())==row['sha256'];refs.append({'path':row['path'],'sha256':row['sha256'],'kind':'RAM'})
        for record in ['capture_report.json','navigation_command_journal.json']:
            source=cap/record;target=DEST/'terminal_records'/name/record;target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
            assert sha(source.read_bytes())==sha(target.read_bytes())
        cohorts.append({'report':str(report_path),'report_sha256':sha(report_path.read_bytes()),'terminal_frame':6200,'primary_E_drive_evidence_verified_and_retained':refs})
    guide=Path(completion['guide']);guides=[]
    for source in guide.iterdir():
        target=DEST/'guide'/source.name;target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        guides.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    roms=sorted(set(Path('E:/Rota Nova translations/Generated').rglob('*.nds'))|set(Path('E:/Rota Nova translations').glob('*.nds')))
    inventory=[{'path':str(p),'bytes':p.stat().st_size,'last_write_ns':p.stat().st_mtime_ns} for p in roms]
    save(ROOT/'read_only_ROM_inventory.json',{'ROMs':inventory,'no_retention_plan_applied_no_ROMs_removed':True,
        'preview_not_rerun':'Default preview script was read and its ApplyPlan-only deletion guard verified after an initial automatic review rejection. Retry was approved but Windows refused the unsigned script. No execution-policy bypass attempted.',
        'prior_preview_retained':'work/rom_retention/20261022T1454293088417Z.json'})
    receipt={'archive':str(DEST),'workspace_files':copied,'terminal_cohorts':cohorts,'guide_files':guides,
        'completed':1350,'source_prose':1507,'reviewed_incomplete_COMMON':157,'newly_completed_fatigue_records':2,
        'hot_spring13_source_prose_only_native_release_and_actual_pending':True,'all_ROMs_retained':len(roms),
        'no_originals_moved_deleted_or_replaced':True,'read_only_inventory':str(ROOT/'read_only_ROM_inventory.json'),
        'frozen_failed_draft_validator_producers_preserved_and_successors_used':True,
        'strict_v2_build_gate_rejects_formatting_unapproved_draft':True,'all_current_emulator_and_CPU_jobs_terminal':True,
        'later_screenshot_repair_candidate_preserved_and_pinned':str(candidate),
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'archive_receipt.json',receipt);copy2(ROOT/'archive_receipt.json',DEST/'archive_receipt.json')
    copy2(ROOT/'read_only_ROM_inventory.json',DEST/'read_only_ROM_inventory.json')
    print('Archived',len(copied),'workspace files,two terminal cohorts,guide captures;',len(roms),'ROMs retained. Fatigue2 complete,hot-spring13 native/scene gates pending;full goal active.')
