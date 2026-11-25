"""Exact E-drive archive of the unfinished Lil scene and scoped test evidence."""
from pathlib import Path
from shutil import copyfile
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

DEST=Path('E:/Rota Nova translations/Editorial review/V1703 Lil opening native formatting and reference research')


if __name__=='__main__':
    assert not DEST.exists()
    root=Path.cwd().absolute()
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_opening_context_v1697_1676')
    folders=[Path('work/analysis')/n for n in ['lil_opening_context_v1697','lil_opening_macro_v1698d','lil_opening_fonts_v1699b','lil_opening_review_v1700','lil_opening_relocation_v1701','lil_opening_checks_v1702','lil_opening_checkpoint_v1702']]
    files={p for folder in folders for p in folder.rglob('*') if p.is_file()}
    files.update(Path(n) for n in ['translations/editorial_review_current_v1.json','translations/lil_opening_editorial_manuscript_v2.json',
        'docs/editorial_handoff_current.md','docs/lil_opening_v1702_native_checkpoint.md','docs/editorial_review_goal.md',
        'docs/known_issues.md','docs/todo.md','docs/translation_progress.md','dk4tool/dialogue/profiles.py','dk4tool/dialogue/layout.py','scripts/build_integrated_release.py','tests/test_lil_editorial_literal_guard.py'])
    files.update(p for p in Path('scripts').glob('*.py') if any('_v'+str(n) in p.stem for n in range(1697,1704)))
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
        'native_approved49_not_integrated_or_complete':True,'reference_map_incomplete':True,'73_formatter_regressions_pass':True,'new_finalized_guide_screenshots':0,
        'ordinary_original_opening_context_is_not_revised_scene_gameplay':True,'full_goal_complete':False,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print({'archive':str(DEST),'exact_files':len(records),'all_out_ROMs_retained':len(retained),'current_ROM_unchanged':True})
