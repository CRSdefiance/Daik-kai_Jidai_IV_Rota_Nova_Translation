"""Archive completed opening evidence and handoff without removing any ROM."""
from pathlib import Path
from shutil import copyfile

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

DEST = Path('E:/Rota Nova translations/Editorial review/V1716 Lil opening49 complete V1711')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_opening_trace_v1706_RESEARCH_ONLY')


if __name__ == '__main__':
    assert not DEST.exists()
    root = Path.cwd().absolute()
    receipt = read('work/analysis/lil_opening_completion_v1715b/completion_receipt.json')
    assert receipt['newly_completed'] == 49 and receipt['all_current_jobs_terminal']
    rom = Path(receipt['candidate']); digest = sha(rom.read_bytes())
    assert digest == receipt['candidate_sha256']
    ledger = read('translations/editorial_review_current_v1.json')
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],
        ledger['retained_wordings_editorially_completed']) == (1424,1076,348)
    ids = [i for f in ledger['completed_editorial_families'] for i in f.get('native_message_IDs',[])]
    assert len(ids) == len(set(ids)) == 1374
    rows = read(receipt['final_review'])['records']
    assert len({(r['file_path'],r['block'],r['record_index']) for r in rows}) == 49
    assert sha(Path('docs/editorial_handoff_current.md').read_bytes()) == receipt['handoff_sha256']
    retained = {p.name for p in Path('out').glob('*.nds')}
    files = {Path(n) for n in ['translations/editorial_review_current_v1.json','translations/release_stack.json',
        'translations/rom_retention_pins.json','translations/lil_opening_final_review_v1.json',
        'translations/lil_opening_editorial_release_v1.json','docs/editorial_handoff_current.md',
        'docs/lil_opening_v1715_completion.md','docs/known_issues.md','docs/todo.md','docs/translation_progress.md',
        'docs/editorial_review_goal.md','scripts/build_integrated_release.py',__file__]}
    config = read('translations/lil_opening_editorial_release_v1.json')
    for name, expected in config['dependencies'].items():
        p = Path(name); assert sha(p.read_bytes()) == expected
        files.add(p)
    names = ['lil_opening_research_v1704','lil_opening_loader_v1705','lil_opening_trace_v1706',
        'lil_opening_navigation_v1707','lil_opening_navigation_v1707b','lil_opening_scene_v1708',
        'lil_opening_references_v1709','lil_opening_release_v1710','lil_opening_terminal_v1713b',
        'lil_opening_completion_v1715b']
    files.update(p for name in names for p in (Path('work/analysis')/name).rglob('*') if p.is_file() and p.suffix != '.nds')
    files.update(p for p in Path('scripts').glob('*.py') if any('_v'+str(n) in p.stem for n in range(1704,1717)))
    files.update([rom.with_suffix('.manifest.json'),rom.with_suffix('.xdelta')])
    assert all(p.is_file() for p in files)
    DEST.mkdir(parents=True); archived=[]
    # Normalize lexically; resolving junctions would incorrectly escape the repository.
    unique = {p.absolute():p for p in files}
    for absolute,p in sorted(unique.items(),key=lambda item:str(item[0])):
        rel = absolute.relative_to(root); target = DEST/'repository'/rel
        target.parent.mkdir(parents=True,exist_ok=True);copyfile(p,target)
        expected = sha(p.read_bytes()); assert sha(target.read_bytes()) == expected
        archived.append({'source':str(p),'archived':str(target.relative_to(DEST)),'sha256':expected})
    capture_roots = [(CAP,'complete_actual_opening_cold_boot'),
        (Path(receipt['guide']),'guide_screenshots'),
        (CAP.parent/'lil_opening_v1711_newgame','registered_startup_newgame'),
        (CAP.parent/'lil_opening_v1711_title','registered_startup_title')]
    for folder,label in capture_roots:
        assert folder.exists()
        for p in sorted(folder.rglob('*')):
            if not p.is_file():continue
            target = DEST/label/p.relative_to(folder)
            target.parent.mkdir(parents=True,exist_ok=True);copyfile(p,target)
            expected = sha(p.read_bytes());assert sha(target.read_bytes()) == expected
            archived.append({'source':str(p),'archived':str(target.relative_to(DEST)),'sha256':expected})
    assert retained == {p.name for p in Path('out').glob('*.nds')} and sha(rom.read_bytes()) == digest
    save(DEST/'archive_receipt.json',{'files':archived,'all_archived_bytes_equal_sources':True,
        'candidate':str(rom),'candidate_sha256':digest,'all_existing_out_ROMs_retained':len(retained),
        'all49_completed_43_revised6_retained':True,'all98_holds90_commands8_startup_controls':True,
        'exact_clean_input_patch_archived':True,'ROMs_retained_in_original_E_generated_locations_not_duplicated_in_archive':True,
        'next_observed_scene_SC2_B120_unreviewed':True,'guide_screenshots':8,
        'failed_V1713_journal_assumption_and_V1715_enum_assumption_preserved_with_successors':True,
        'full_goal_active_graphics_separate':True,'full_goal_complete':False,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print({'archive':str(DEST),'exact_files':len(archived),'all_out_ROMs_retained':len(retained),
        'completed_editorial_entries':1424,'full_goal_active':True},flush=True)
