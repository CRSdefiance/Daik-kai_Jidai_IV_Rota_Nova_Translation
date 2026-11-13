"""Hash-verified complete B24 checkpoint archive;preserve every generated ROM."""
from pathlib import Path
from shutil import copy2,disk_usage
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B24_archive_v1845')
DEST=Path('E:/Rota Nova translations/Editorial review/V1845 Lil trade routes and officers13 complete')
E_ROOT=Path('E:/Rota Nova translations')

def in_range(name):
    match=re.search(r'_v(\d+)[a-z]?(?:\.py)?$',name)
    return bool(match and 1826<=int(match[1])<=1844)

if __name__=='__main__':
    assert not ROOT.exists()and not DEST.exists()
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==1529 and ledger['records_with_source_and_prose_pass']==1645
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    for number,frame in ((1831,43800),(1834,47650)):
        assert read(f'work/analysis/lil_B24_research_run_v{number}/terminal.json')['frame']==frame
    completion=read('work/analysis/lil_B24_completion_v1844/completion_receipt.json')
    assert completion['all_required_scene_native_actual_registered_patch_startup_visual_gates_passed']
    handoff=Path('docs/editorial_handoff_current.md');before=sha(handoff.read_bytes())
    with handoff.open('a',encoding='utf-8')as f:
        f.write('\n\n## Output size precaution\n\nAlways redirect build_integrated_release.py stdout to a new log file. Its full manifest output is tens of megabytes; inspect only selected keys from the saved manifest. Do not return full builder output to chat. This avoids unnecessary context growth and compaction.\n')
    folders=[p for p in Path('work/analysis').iterdir()if p.is_dir()and in_range(p.name)]
    folders.extend([E_ROOT/'Generated/work/emulation_v193/lil_B24_research_run_v1831_RESEARCH_ONLY',
        E_ROOT/'Generated/work/emulation_v193/lil_B24_research_run_v1834_RESEARCH_ONLY',
        E_ROOT/'Generated/work/emulation_v193/lil_B24_v1841_newgame',
        E_ROOT/'Generated/work/emulation_v193/lil_B24_v1841_title',
        E_ROOT/'Guide screenshots/V1841 Lil trade routes and officers verified'])
    files=[p for folder in folders for p in folder.rglob('*')if p.is_file()]
    files.extend(p for p in Path('scripts').glob('*.py')if in_range(p.name))
    files.extend(Path(p)for p in ['translations/editorial_review_current_v1.json','translations/release_stack.json',
        'translations/lil_trade_routes_officers_editorial_manuscript_v3.json',
        'translations/lil_trade_routes_officers_editorial_manuscript_v4.json',
        'translations/lil_trade_routes_editorial_relocation_map_v1.json',
        'translations/lil_trade_routes_editorial_release_v1.json','translations/lil_trade_routes_officers_final_review_v1.json',
        'dk4tool/patch/lil_trade_routes_editorial.py','scripts/build_integrated_release.py',__file__,
        'out/all_routes_combined_v1841_candidate.nds','out/all_routes_combined_v1841_candidate.xdelta',
        'out/all_routes_combined_v1841_candidate.manifest.json',
        'docs/editorial_handoff_current.md','docs/translation_progress.md','docs/known_issues.md','docs/todo.md',
        'docs/editorial_review_goal.md','docs/lil_B24_v1836_native_checkpoint.md','docs/lil_B24_v1844_completion.md'])
    files=sorted({p.absolute()for p in files},key=lambda p:str(p).casefold());assert all(p.is_file()for p in files)
    total=sum(p.stat().st_size for p in files);assert disk_usage(E_ROOT).free>total+512*1024**2
    ROOT.mkdir(parents=True);DEST.mkdir(parents=True);copied=[]
    print({'archive_files_planned':len(files),'bytes':total},flush=True)
    for p in files:
        try:relative=p.relative_to(Path.cwd().absolute())
        except ValueError:relative=p.relative_to(E_ROOT)
        target=DEST/relative;assert not target.exists();target.parent.mkdir(parents=True,exist_ok=True)
        copy2(p,target);digest=sha(p.read_bytes());assert sha(target.read_bytes())==digest
        copied.append({'source':str(p),'archive':str(target),'bytes':p.stat().st_size,'sha256':digest})
    roms=[{'path':str(p),'bytes':p.stat().st_size}for p in sorted(Path('out').glob('*.nds'))]
    assert len(roms)==185
    record={'archive':str(DEST),'files':copied,'file_count':len(copied),'bytes':total,
        'all_source_archive_hashes_verified':True,'all_captured_runs_terminal':True,
        'completed_entries':1529,'source_prose_reviewed':1645,'reviewed_incomplete_COMMON':116,
        'unfinished_reviewed_route_drafts':0,'all185_output_ROMs_preserved':roms,
        'current_registered_candidate':'out/all_routes_combined_v1841_candidate.nds',
        'current_ROM_sha256':completion['candidate_sha256'],'patch_sha256':completion['patch_sha256'],
        'handoff_before_output_precaution_sha256':before,'handoff_current_sha256':sha(handoff.read_bytes()),
        'full_goal_active_graphics_and_later_older_record_reaudit_separate':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'archive_manifest.json',record);save(DEST/'archive_manifest.json',record)
    assert(ROOT/'archive_manifest.json').read_bytes()==(DEST/'archive_manifest.json').read_bytes()
    print({'archived_files':len(copied),'bytes':total,'all_hashes_verified':True,'output_ROMs_retained':185},flush=True)
