"""Exact E-drive archive of FE resolution, lesson layouts and revised actual tests."""
import re
from pathlib import Path
from shutil import copyfile, disk_usage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

DEST=Path('E:/Rota Nova translations/Editorial review/V1750 Lil lessons native approval and revised wind verification')
ROOTS=['lil_modal_context_v1730','lil_lesson_relocation_v1731','lil_lesson_parity_choices_v1732',
    'lil_modal_context_v1734','lil_lesson_choice_ui_v1735','lil_actual_modal_replay_v1736',
    'lil_FE_display_v1737','lil_FE_visual_v1738','lil_lessons_research_v1739','lil_lessons_loader_v1740',
    'lil_lessons_revised_v1741','lil_lesson_layout_approval_v1742','lil_lesson_navigation_v1745',
    'lil_lessons_checkpoint_v1746','lil_navigation_coordinates_v1747','lil_navigation_audit_v1748',
    'lil_lessons_checkpoint_v1749']
CAPS=['lil_modal_context_v1730_1711','lil_modal_context_v1734_1711',
      'lil_lessons_revised_v1741_RESEARCH_ONLY','lil_lesson_navigation_v1745_RESEARCH_ONLY']

if __name__=='__main__':
    assert not DEST.exists()
    receipt=read('work/analysis/lil_lessons_checkpoint_v1749/checkpoint_receipt.json')
    assert receipt['all_current_jobs_terminal']
    ledger=Path('translations/editorial_review_current_v1.json'); handoff=Path('docs/editorial_handoff_current.md')
    assert sha(ledger.read_bytes())==receipt['ledger_sha256']
    assert sha(handoff.read_bytes())==receipt['handoff_sha256']
    files={ledger,handoff,Path(__file__),Path('translations/release_stack.json'),
        Path('translations/lil_lessons_editorial_manuscript_v3.json'),
        Path('translations/lil_lesson_choices_editorial_draft_v2.json'),
        Path('docs/lil_lessons_v1746_checkpoint.md'),Path('docs/translation_progress.md'),
        Path('docs/known_issues.md'),Path('docs/todo.md'),Path('docs/editorial_review_goal.md')}
    for name in ROOTS:
        directory=Path('work/analysis')/name; assert directory.is_dir(),name
        files.update(p for p in directory.rglob('*') if p.is_file())
    for p in Path('scripts').glob('*.py'):
        match=re.search(r'_v(\d+)',p.stem)
        if match and 1729<=int(match[1])<=1750: files.add(p)
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
        'native_layout_approved64_and_revised_wind22_actual44_holds':True,
        'all64_lesson_entries_still_incomplete_full_goal_active':True,'registered_candidate_unchanged':True,
        'graphics_all18_plaques_separately_unfinished':True,'all_current_jobs_terminal':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'archive':str(DEST),'exact_files':len(records),'bytes':total,'retained_out_ROMs':len(retained)},flush=True)
