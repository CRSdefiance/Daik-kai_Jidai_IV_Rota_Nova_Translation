"""Archive51-source/native Stockholm checkpoint with exact evidence scope."""
from pathlib import Path
from shutil import copy2,disk_usage
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Stockholm_archive_v1860')
DEST=Path('E:/Rota Nova translations/Editorial review/V1860 Stockholm51 source and native font review')
E_ROOT=Path('E:/Rota Nova translations')

def selected(name):
    m=re.search(r'_v(\d+)[a-z]?(?:\.py)?$',name)
    return bool(m and 1846<=int(m[1])<=1859)

if __name__=='__main__':
    assert not ROOT.exists()and not DEST.exists()
    ledger=read('translations/editorial_review_current_v1.json')
    assert(ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1529,1696)
    assert len(ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'])==51
    assert read('work/analysis/lil_Stockholm_context_run_v1851/terminal.json')['frame']==62850
    assert read('work/analysis/Gerhard_story_control_v1856/terminal.json')['frame']==7160
    assert len(read('work/analysis/lil_Stockholm_fonts_v1858/all51_native_macros_and_complete_font_planes.json')['cases'])==51
    approval=read('work/analysis/lil_Stockholm_font_approval_v1859b/approval_receipt.json')
    assert approval['complete_font_cases']==51 and approval['native_macro_alignment_calls']==408
    assert len(approval['negative_scope_cases'])==5
    folders=[p for p in Path('work/analysis').iterdir()if p.is_dir()and selected(p.name)]
    folders.extend([E_ROOT/'Generated/work/emulation_v193/lil_Stockholm_context_run_v1851_RESEARCH_ONLY',
        E_ROOT/'Generated/work/emulation_v193/Gerhard_story_control_v1856_V1841'])
    files=[p for folder in folders for p in folder.rglob('*')if p.is_file()]
    files.extend(p for p in Path('scripts').glob('*.py')if selected(p.name))
    files.extend(Path(p)for p in [__file__,'translations/editorial_review_current_v1.json','translations/release_stack.json',
        'translations/lil_Stockholm_encounter_editorial_manuscript_v1.json',
        'translations/lil_Stockholm_encounter_editorial_manuscript_v2.json',
        'dk4tool/dialogue/lil_stockholm_profile.py','docs/editorial_handoff_current.md',
        'docs/translation_progress.md','docs/known_issues.md','docs/todo.md','docs/editorial_review_goal.md',
        'docs/lil_Stockholm_v1852_source_review.md','docs/lil_Stockholm_v1859b_native_checkpoint.md',
        'out/all_routes_combined_v1841_candidate.nds','out/all_routes_combined_v1841_candidate.xdelta',
        'out/all_routes_combined_v1841_candidate.manifest.json',
        'work/analysis/lil_B24_archive_v1845/archive_manifest.json'])
    files=sorted({p.absolute()for p in files},key=lambda p:str(p).casefold());assert all(p.is_file()for p in files)
    total=sum(p.stat().st_size for p in files);assert disk_usage(E_ROOT).free>total+512*1024**2
    ROOT.mkdir(parents=True);DEST.mkdir(parents=True);copied=[]
    print({'planned_files':len(files),'bytes':total},flush=True)
    for p in files:
        try:relative=p.relative_to(Path.cwd().absolute())
        except ValueError:relative=p.relative_to(E_ROOT)
        target=DEST/relative;assert not target.exists();target.parent.mkdir(parents=True,exist_ok=True)
        copy2(p,target);digest=sha(p.read_bytes());assert sha(target.read_bytes())==digest
        copied.append({'source':str(p),'archive':str(target),'bytes':p.stat().st_size,'sha256':digest})
    roms=[{'path':str(p),'bytes':p.stat().st_size}for p in sorted(Path('out').glob('*.nds'))];assert len(roms)==185
    current=ledger['current_integrated_candidate'];assert sha(Path(current['path']).read_bytes())==current['sha256']
    record={'archive':str(DEST),'files':copied,'file_count':len(copied),'bytes':total,
        'all_source_archive_hashes_verified':True,'all_test_jobs_terminal':True,
        'completed_entries_unchanged':1529,'source_prose_reviewed':1696,'reviewed_incomplete_COMMON':116,
        'reviewed_incomplete_route51_not_integrated_or_complete':True,
        'native_full_font_cases':51,'native_macro_alignment_calls':408,
        'old_Stockholm_context36_speeches_not_revised_gameplay':True,
        'current_Hodram_Gerhard_control_mapping_not_a_B27_branch_visit':True,
        'four_scope_negative_controls_and_one_per_record_review_negative':True,
        'no_global_profile_orcodec_change':'Only new exact-source dk4tool/dialogue/lil_stockholm_profile.py',
        'current_registered_ROM':current['path'],'current_ROM_sha256':current['sha256'],
        'current_patch_sha256':current['patch_sha256'],'all185_output_ROMs_preserved':roms,
        'full_goal_active_graphics_and_later_older_record_reaudit_separate':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'archive_manifest.json',record);save(DEST/'archive_manifest.json',record)
    assert(ROOT/'archive_manifest.json').read_bytes()==(DEST/'archive_manifest.json').read_bytes()
    print({'archived_files':len(copied),'bytes':total,'all_hashes_verified':True,'output_ROMs_retained':185},flush=True)
