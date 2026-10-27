"""Exact E-drive archive of the unfinished Lil scene and scoped test evidence."""
from pathlib import Path
from shutil import copyfile
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

DEST=Path('E:/Rota Nova translations/Editorial review/V1696 Lil opening draft and close-range research')


if __name__=='__main__':
    assert not DEST.exists()
    root=Path.cwd().absolute()
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/close_sighting_v1690_1676_closeReady8')
    folders=[Path('work/analysis')/n for n in ['unmapped_shop_references_v1688b','close_sighting_preflight_v1691b',
        'close_sighting_v1690_closeReady8','close_sighting_follow_v1692','close_sighting_negative_v1693',
        'lil_opening_editorial_v1694','editorial_checkpoint_v1695']]
    files={p for folder in folders for p in folder.rglob('*') if p.is_file()}
    files.update(Path(n) for n in ['translations/editorial_review_current_v1.json','translations/lil_opening_editorial_manuscript_v1.json',
        'docs/editorial_handoff_current.md','docs/lil_opening_v1695_editorial_checkpoint.md','docs/editorial_review_goal.md',
        'docs/known_issues.md','docs/todo.md','docs/translation_progress.md'])
    files.update(p for p in Path('scripts').glob('*.py') if any('_v'+str(n) in p.stem for n in range(1688,1697)))
    assert files and all(p.is_file() for p in files)
    ROM=Path('out/all_routes_combined_v1676_candidate.nds');before=sha(ROM.read_bytes())
    assert before=='337edf22ab6ee96536aadb15fb461652149b157e8d9bd1ef60db998f97608510'
    retained={p.name for p in Path('out').glob('*.nds')}
    DEST.mkdir(parents=True)
    records=[]
    for p in sorted(files,key=str):
        relative=p.absolute().relative_to(root);target=DEST/'repository'/relative
        target.parent.mkdir(parents=True,exist_ok=True);copyfile(p,target)
        assert sha(p.read_bytes())==sha(target.read_bytes())
        records.append({'source':str(p),'archived':str(target.relative_to(DEST)),'sha256':sha(target.read_bytes())})
    for p in sorted(cap.rglob('*')):
        if not p.is_file():continue
        target=DEST/'targeted_emulator_capture'/p.relative_to(cap)
        target.parent.mkdir(parents=True,exist_ok=True);copyfile(p,target)
        assert sha(p.read_bytes())==sha(target.read_bytes())
        records.append({'source':str(p),'archived':str(target.relative_to(DEST)),'sha256':sha(target.read_bytes())})
    assert retained=={p.name for p in Path('out').glob('*.nds')} and sha(ROM.read_bytes())==before
    save(DEST/'archive_receipt.json',{'files':records,'all_archived_bytes_equal_sources':True,
        'all_existing_out_ROMs_retained':len(retained),'current_ROM_unchanged_sha256':before,
        'draft49_not_integrated_or_complete':True,'new_finalized_guide_screenshots':0,
        'targeted_negative_test_not_a_playthrough':True,'full_goal_complete':False,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print({'archive':str(DEST),'exact_files':len(records),'all_out_ROMs_retained':len(retained),'current_ROM_unchanged':True})
