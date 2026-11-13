"""Archive the registered six-row completion andterminal negative shot evidence."""
from pathlib import Path
from shutil import copy2
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/reinforcement_archive_v1815')
DEST=Path('E:/Rota Nova translations/Editorial review/V1815 Reinforcement6 verified and original shot trace')
E_ROOT=Path('E:/Rota Nova translations')

if __name__=='__main__':
    assert not ROOT.exists()and not DEST.exists()
    receipt=read('work/analysis/reinforcement_completion_v1814/completion_receipt.json')
    assert receipt['counts_before_after']==[1503,1509]
    assert read('work/analysis/observed_lookout_v1799/terminal.json')['terminal']
    folders=[]
    for pattern in('shot_observer_contract_v1796','lookout_contact_preflight_v1798*','observed_lookout_v1799',
        'lookout_navigation_v1800*','current_reinforcement_matrix_v1801*','reinforcement_faction_prose_v1802',
        'reinforcement_review_v1803','reinforcement_faction_release_v1805','lookout_terminal_v1806',
        'lookout_level_successor_v1810','reinforcement_faction_actual_v1812','reinforcement_faction_actual_v1813',
        'reinforcement_completion_v1814'):
        folders.extend(Path('work/analysis').glob(pattern))
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
    folders.extend(cap/name for name in('observed_lookout_v1799_1775','reinforcement_faction_v1807_newgame',
        'reinforcement_faction_v1807_title','reinforcement_faction_actual_v1812_1807'))
    folders.append(E_ROOT/'Guide screenshots/V1807 Reinforcement announcement verified')
    files=[p for folder in folders for p in folder.rglob('*')if p.is_file()]
    files.extend([Path('out/all_routes_combined_v1807_candidate.nds'),Path('out/all_routes_combined_v1807_candidate.xdelta'),
        Path('out/all_routes_combined_v1807_candidate.manifest.json'),Path('translations/release_stack.json'),
        Path('translations/editorial_review_current_v1.json'),Path('translations/reinforcement_faction_prose_release_v1.json'),
        Path('translations/reinforcement_sniping_editorial_manuscript_v2.json'),Path('translations/reinforcement_sniping_editorial_manuscript_v3.json'),
        Path('translations/reinforcement_sniping_editorial_manuscript_v4.json'),Path('translations/reinforcement_faction_final_review_v1.json'),
        Path('dk4tool/patch/reinforcement_faction_prose.py'),Path('scripts/build_integrated_release.py'),Path(__file__)])
    files.extend(Path('docs')/name for name in('editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md',
        'known_issues.md','todo.md','reinforcement_v1814_completion.md'))
    files.extend(p for p in Path('scripts').glob('*.py')if re.search(r'_v(?:179[6-9]|180[0-9]|181[0-5])[a-z]?\.py$',p.name))
    manifest=read('out/all_routes_combined_v1807_candidate.manifest.json');files.extend(map(Path,manifest['batches']))
    config=read('translations/reinforcement_faction_prose_release_v1.json');files.extend(map(Path,config['dependencies']))
    doc=read('translations/reinforcement_sniping_editorial_manuscript_v4.json')
    files.extend(Path(doc[key])for key in('native_context_proof','source_context_supplement'))
    files=sorted({p.absolute()for p in files},key=lambda p:str(p).casefold())
    assert all(p.is_file()for p in files)
    ROOT.mkdir(parents=True);DEST.mkdir(parents=True);copied=[]
    for p in files:
        try:relative=p.relative_to(Path.cwd().absolute())
        except ValueError:relative=p.relative_to(E_ROOT)
        target=DEST/relative;assert not target.exists();target.parent.mkdir(parents=True,exist_ok=True)
        copy2(p,target);digest=sha(p.read_bytes());assert sha(target.read_bytes())==digest
        copied.append({'source':str(p),'archive':str(target),'bytes':p.stat().st_size,'sha256':digest})
    inventory=[{'path':str(p),'bytes':p.stat().st_size}for p in sorted(Path('out').glob('*.nds'))]
    assert len(inventory)==184
    record={'archive':str(DEST),'files':copied,'file_count':len(copied),'bytes':sum(r['bytes']for r in copied),
        'all_source_and_archive_hashes_verified':True,'all_captured_runs_terminal_before_archiving':True,
        'prior_checkpoint':'E:/Rota Nova translations/Editorial review/V1795 Fleet sightings15 close-range verified',
        'registered_ROM_exact_patch_manifest_full477_batch_inputs_and_latest_source_preserved':True,
        'all184_output_ROMs_retained':inventory,'completed_entries':1509,'reviewed_incomplete_COMMON':123,
        'full_goal_active_separate_graphics_and_successful_shot_still_open':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'archive_manifest.json',record);save(DEST/'archive_manifest.json',record)
    assert(ROOT/'archive_manifest.json').read_bytes()==(DEST/'archive_manifest.json').read_bytes()
    print({'archive_files':len(copied),'archive_bytes':record['bytes'],'all_hashes_verified':True,'output_ROMs_retained':184},flush=True)
