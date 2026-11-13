"""Hash-verified, additive new-thread checkpoint; preserve every generated ROM."""
from pathlib import Path
from shutil import copy2, disk_usage
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/editorial_thread_archive_v1869')
DEST=Path('E:/Rota Nova translations/Editorial review/V1869 New thread handoff Stockholm revised gameplay')
E_ROOT=Path('E:/Rota Nova translations')

def selected(name):
    m=re.search(r'_v(\d+)[a-z]?(?:\.py)?$',name)
    return bool(m and 1861<=int(m[1])<=1868)

if __name__=='__main__':
    assert not ROOT.exists() and not DEST.exists()
    checkpoint=read('work/analysis/editorial_thread_checkpoint_v1868/checkpoint_receipt.json')
    assert checkpoint['all_jobs_terminal'] and checkpoint['completion_count_unchanged']==1529
    for p,digest in checkpoint['evidence'].items():assert sha(Path(p).read_bytes())==digest
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_with_source_and_prose_pass']==1696
    assert read('work/analysis/lil_Stockholm_revised_run_v1864/terminal.json')['frame']==62850
    folders=[p for p in Path('work/analysis').iterdir() if p.is_dir() and selected(p.name)]
    folders.append(E_ROOT/'Generated/work/emulation_v193/lil_Stockholm_revised_run_v1864_RESEARCH_ONLY')
    files=[p for folder in folders for p in folder.rglob('*')if p.is_file()]
    files.extend(p for p in Path('scripts').glob('*.py')if selected(p.name))
    files.extend(Path(p) for p in [__file__,
        'translations/editorial_review_current_v1.json','translations/release_stack.json',
        'translations/lil_Stockholm_encounter_editorial_manuscript_v1.json',
        'translations/lil_Stockholm_encounter_editorial_manuscript_v2.json',
        'dk4tool/dialogue/lil_stockholm_profile.py','docs/editorial_handoff_current.md',
        'docs/editorial_next_thread_prompt_v1868.txt','docs/editorial_review_goal.md',
        'docs/translation_progress.md','docs/known_issues.md','docs/todo.md',
        'out/all_routes_combined_v1841_candidate.nds','out/all_routes_combined_v1841_candidate.xdelta',
        'out/all_routes_combined_v1841_candidate.manifest.json',
        'work/analysis/lil_Stockholm_archive_v1860/archive_manifest.json'])
    files=sorted({p.absolute()for p in files},key=lambda p:str(p).casefold())
    assert all(p.is_file()for p in files)
    total=sum(p.stat().st_size for p in files)
    assert disk_usage(E_ROOT).free>total+512*1024**2
    roms=[{'path':str(p),'bytes':p.stat().st_size}for p in sorted(Path('out').glob('*.nds'))]
    assert len(roms)==185
    ROOT.mkdir(parents=True);DEST.mkdir(parents=True);copied=[]
    print({'planned_files':len(files),'bytes':total},flush=True)
    for p in files:
        try:relative=p.relative_to(Path.cwd().absolute())
        except ValueError:relative=p.relative_to(E_ROOT)
        target=DEST/relative;assert not target.exists()
        target.parent.mkdir(parents=True,exist_ok=True);copy2(p,target)
        digest=sha(p.read_bytes());assert sha(target.read_bytes())==digest
        copied.append({'source':str(p),'archive':str(target),'bytes':p.stat().st_size,'sha256':digest})
    proof={'archive':str(DEST),'files':copied,'file_count':len(copied),'bytes':total,
        'all_source_archive_hashes_verified':True,'all_test_jobs_terminal':True,
        'existing_V1860_archive_retains_preceding_source_and_font_evidence':True,
        'registered_V1841_unchanged':True,'V1492_still_promoted':True,
        'source_prose_reviewed':1696,'completed_entries':1529,
        'Stockholm51_still_pending_registered_integration_and_final_approval':True,
        'actual_revised_speeches':36,'complete_actual_holds':72,
        'all185_output_ROMs_preserved':roms,'no_files_pruned_or_moved':True,
        'full_goal_active_not_complete':True,'producer_sha256':sha(Path(__file__).read_bytes())}
    save(ROOT/'archive_manifest.json',proof);save(DEST/'archive_manifest.json',proof)
    assert (ROOT/'archive_manifest.json').read_bytes()==(DEST/'archive_manifest.json').read_bytes()
    print({'archived_files':len(copied),'bytes':total,'all_hashes_verified':True,'output_ROMs_retained':185},flush=True)
