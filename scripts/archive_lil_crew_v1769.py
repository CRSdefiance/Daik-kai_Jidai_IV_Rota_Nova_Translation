"""Exact E-drive archive of FE resolution, lesson layouts and revised actual tests."""
import re
from pathlib import Path
from shutil import copyfile, disk_usage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

DEST=Path('E:/Rota Nova translations/Editorial review/V1769 Lil crew both choices and current lesson wording')
ROOTS=['lil_crew_trigger_v1751','lil_Bruges_location_v1752c','lil_crew_lesson_v1753',
    'lil_Bruges_location_v1754','lil_Deck_label_v1755','lil_crew_lesson_v1756','lil_failed_approach_v1757',
    'lil_Deck_label_approval_v1758','lil_crew_navigation_v1759','lil_crew_navigation_v1759b',
    'lil_lessons_relocation_v1760','lil_lessons_research_v1761','lil_lessons_loader_v1762',
    'lil_crew_scene_v1763_initial','lil_crew_scene_v1763_final','lil_crew_final_text_v1764',
    'lil_crew_decline_v1766','lil_crew_decline_v1767_decline','lil_crew_checkpoint_v1768']
CAPS=['lil_crew_lesson_v1753_RESEARCH_ONLY','lil_crew_lesson_v1756_RESEARCH_ONLY',
    'lil_crew_final_text_v1764_RESEARCH_ONLY','lil_crew_decline_v1766_RESEARCH_ONLY']

if __name__=='__main__':
    assert not DEST.exists()
    receipt=read('work/analysis/lil_crew_checkpoint_v1768/checkpoint_receipt.json')
    assert receipt['all_current_jobs_terminal']
    ledger=Path('translations/editorial_review_current_v1.json'); handoff=Path('docs/editorial_handoff_current.md')
    assert sha(ledger.read_bytes())==receipt['ledger_sha256']
    assert sha(handoff.read_bytes())==receipt['handoff_sha256']
    files={ledger,handoff,Path(__file__),Path('translations/release_stack.json'),
        Path('translations/lil_lessons_editorial_manuscript_v5.json'),
        Path('translations/lil_lesson_choices_editorial_draft_v2.json'),Path('translations/lil_lessons_editorial_manuscript_v4.json'),
        Path('docs/lil_crew_v1768_checkpoint.md'),Path('docs/translation_progress.md'),
        Path('docs/known_issues.md'),Path('docs/todo.md'),Path('docs/editorial_review_goal.md')}
    for name in ROOTS:
        directory=Path('work/analysis')/name; assert directory.is_dir(),name
        files.update(p for p in directory.rglob('*') if p.is_file())
    for p in Path('scripts').glob('*.py'):
        match=re.search(r'_v(\d+)',p.stem)
        if match and 1751<=int(match[1])<=1769: files.add(p)
    captures=[]
    for name in CAPS:
        folder=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/name
        assert (folder/'capture_report.json').exists()
        captures.extend((folder,p) for p in folder.rglob('*') if p.is_file())
    total=sum(p.stat().st_size for p in files)+sum(p.stat().st_size for _,p in captures)
    assert disk_usage('E:/').free>total+64*1024*1024
    retained={p.name for p in Path('out').glob('*.nds')}
    root=Path.cwd().absolute(); DEST.mkdir(parents=True); records=[]
    for p in sorted(files,key=str):
        target=DEST/'repository'/p.absolute().relative_to(root)
        target.parent.mkdir(parents=True,exist_ok=True); copyfile(p,target)
        digest=sha(p.read_bytes()); assert sha(target.read_bytes())==digest
        records.append({'source':str(p),'archived':str(target.relative_to(DEST)),'sha256':digest})
    for folder,p in captures:
        target=DEST/'captures'/folder.name/p.relative_to(folder)
        target.parent.mkdir(parents=True,exist_ok=True); copyfile(p,target)
        digest=sha(p.read_bytes()); assert sha(target.read_bytes())==digest
        records.append({'source':str(p),'archived':str(target.relative_to(DEST)),'sha256':digest})
    assert retained=={p.name for p in Path('out').glob('*.nds')}
    assert sha(ledger.read_bytes())==receipt['ledger_sha256'] and sha(handoff.read_bytes())==receipt['handoff_sha256']
    save(DEST/'archive_receipt.json', {'files':records,'all_archived_bytes_equal_sources':True,
        'archived_source_bytes':total,'all_existing_out_ROMs_retained':len(retained),
        'native_layout_current64_wind22_and_crew_both_choices31_actual_verified':True,
        'all64_lesson_entries_still_incomplete_full_goal_active':True,'registered_candidate_unchanged':True,
        'graphics_all18_plaques_separately_unfinished':True,'all_current_jobs_terminal':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'archive':str(DEST),'exact_files':len(records),'bytes':total,'retained_out_ROMs':len(retained)},flush=True)
