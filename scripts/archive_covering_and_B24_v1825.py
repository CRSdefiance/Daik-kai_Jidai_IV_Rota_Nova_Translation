"""Archive completed covering-fire7 andunfinished B24 source/prose13 separately."""
from pathlib import Path
from shutil import copy2
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/covering_B24_archive_v1825')
DEST=Path('E:/Rota Nova translations/Editorial review/V1825 Covering fire7 and Lil B24 source review')
E_ROOT=Path('E:/Rota Nova translations')

if __name__=='__main__':
    assert not ROOT.exists()and not DEST.exists()
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==1516 and ledger['records_with_source_and_prose_pass']==1645
    assert len(ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'])==13
    assert read('work/analysis/covering_fire_run_v1817/terminal_preservation.json')['source_and_disposable_donors_unchanged']
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/covering_fire_v1817_1807')
    assert read(cap/'capture_report.json')['frames']==6310
    folders=[*Path('work/analysis').glob('covering_fire_*_v1816'),Path('work/analysis/covering_fire_run_v1817'),
        Path('work/analysis/covering_fire_current_v1818'),Path('work/analysis/covering_fire_actual_v1819'),
        Path('work/analysis/covering_fire_completion_v1820'),*Path('work/analysis').glob('lil_followup_inventory_v1821*'),
        Path('work/analysis/lil_B24_source_v1822'),Path('work/analysis/lil_B24_prose_v1823'),
        Path('work/analysis/lil_B24_checkpoint_v1824'),cap,E_ROOT/'Guide screenshots/V1807 Covering fire verified']
    files=[p for folder in folders for p in folder.rglob('*')if p.is_file()]
    files.extend(p for p in Path('scripts').glob('*.py')if re.search(r'_v(?:181[6-9]|182[0-5])[a-z]?\.py$',p.name))
    files.extend([Path('translations/editorial_review_current_v1.json'),Path('translations/release_stack.json'),
        Path('translations/covering_fire_final_review_v1.json'),Path('translations/lil_trade_routes_officers_editorial_manuscript_v1.json'),
        Path('translations/lil_trade_routes_officers_editorial_manuscript_v2.json'),Path('translations/reinforcement_sniping_editorial_manuscript_v4.json'),
        Path('out/all_routes_combined_v1807_candidate.nds'),Path('out/all_routes_combined_v1807_candidate.xdelta'),
        Path('out/all_routes_combined_v1807_candidate.manifest.json'),Path(__file__),
        Path('work/analysis/reinforcement_archive_v1815/archive_manifest.json')])
    files.extend(Path('docs')/name for name in('editorial_handoff_current.md','translation_progress.md','known_issues.md','todo.md',
        'editorial_review_goal.md','covering_fire_v1820_completion.md','lil_B24_v1824_source_review.md'))
    files=sorted({p.absolute()for p in files},key=lambda p:str(p).casefold());assert all(p.is_file()for p in files)
    ROOT.mkdir(parents=True);DEST.mkdir(parents=True);copied=[]
    for p in files:
        try:relative=p.relative_to(Path.cwd().absolute())
        except ValueError:relative=p.relative_to(E_ROOT)
        target=DEST/relative;assert not target.exists();target.parent.mkdir(parents=True,exist_ok=True)
        copy2(p,target);digest=sha(p.read_bytes());assert sha(target.read_bytes())==digest
        copied.append({'source':str(p),'archive':str(target),'bytes':p.stat().st_size,'sha256':digest})
    roms=[{'path':str(p),'bytes':p.stat().st_size}for p in sorted(Path('out').glob('*.nds'))];assert len(roms)==184
    record={'archive':str(DEST),'files':copied,'file_count':len(copied),'bytes':sum(r['bytes']for r in copied),
        'all_source_and_archive_hashes_verified':True,'all_captured_runs_terminal':True,
        'completed_entries':1516,'source_prose_reviewed':1645,'reviewed_incomplete_COMMON':116,'unfinished_B24_route_drafts':13,
        'seven_covering_fire_entries_completed_with_four_revisions_three_retentions':True,
        'B24_drafts_not_counted_as_complete_or_integrated':True,'current_registered_V1807_ROM_patch_manifest_unchanged':True,
        'all184_output_ROMs_preserved':roms,'prior_complete_source_archive':
            'E:/Rota Nova translations/Editorial review/V1815 Reinforcement6 verified and original shot trace',
        'full_goal_active_graphics_and_later_older_record_reaudit_separate':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'archive_manifest.json',record);save(DEST/'archive_manifest.json',record)
    assert(ROOT/'archive_manifest.json').read_bytes()==(DEST/'archive_manifest.json').read_bytes()
    print({'archived_files':len(copied),'bytes':record['bytes'],'all_hashes_verified':True,'output_ROMs_retained':184,
        'complete':1516,'source_prose_reviewed':1645,'B24_incomplete_drafts':13},flush=True)
