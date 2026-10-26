"""Exact E-drive checkpoint of sighting completion and all current test evidence."""
from pathlib import Path
from shutil import copyfile,disk_usage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

DEST=Path('E:/Rota Nova translations/Editorial review/V1795 Fleet sightings15 close-range verified')
ROOTS=['close_follow_preflight_v1781','close_follow_v1782_openWaterReady8','close_follow_navigation_v1783',
    'close_follow_navigation_v1783b','close_follow_inheritance_v1784','close_admission_research_v1785',
    'two_stage_sighting_v1787_twoStageReady8','two_stage_navigation_v1788','close_sighting_live_v1790',
    'close_sighting_terminal_v1791','current_sighting_matrix_v1792','close_loading_findings_v1793','sighting_completion_v1794']
CAPS=['close_follow_v1782_1775_openWaterReady8','two_stage_sighting_v1787_1775_twoStageReady8']

if __name__=='__main__':
    assert not DEST.exists()
    receipt=read('work/analysis/sighting_completion_v1794/completion_receipt.json');assert receipt['all_current_jobs_terminal']
    ledger,handoff=Path('translations/editorial_review_current_v1.json'),Path('docs/editorial_handoff_current.md')
    assert sha(ledger.read_bytes())==receipt['ledger_sha256'] and sha(handoff.read_bytes())==receipt['handoff_sha256']
    release=read('work/analysis/lil_lessons_release_v1774/registered_release_verification.json')
    files={ledger,handoff,Path(__file__),Path('translations/release_stack.json'),Path('translations/sighting_editorial_final_review_v1.json'),
        Path('docs/sighting_v1794_completion.md'),Path(release['candidate']),Path(release['patch']),
        Path(release['candidate']).with_suffix('.manifest.json')}
    files.update(Path(p)for p in receipt['proofs'])
    # Keep the current Python source tree,including failed explicit predecessors.
    files.update(Path('scripts').glob('*.py'));files.update(Path('dk4tool').rglob('*.py'))
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        files.add(Path('docs')/name)
    empty=[]
    for name in ROOTS:
        directory=Path('work/analysis')/name;assert directory.is_dir(),name
        found=[p for p in directory.rglob('*')if p.is_file()]
        if not found:empty.append(str(directory))
        files.update(found)
    doc=read('translations/sighting_editorial_manuscript_v9.json')
    for key in ('native_context_proof','source_context_supplement','native_provider_proof','native_font_proof','visual_review'):
        files.add(Path(doc[key]))
    captures=[]
    for name in CAPS:
        directory=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/name
        assert (directory/'capture_report.json').is_file()
        captures.extend((directory,p)for p in directory.rglob('*')if p.is_file())
    guide=Path(receipt['guide']);guide_files=[p for p in guide.rglob('*')if p.is_file()]
    root=Path.cwd().absolute();files={p.absolute()for p in files}
    for p in files:p.relative_to(root)
    total=sum(p.stat().st_size for p in files)+sum(p.stat().st_size for _,p in captures)+sum(p.stat().st_size for p in guide_files)
    assert disk_usage('E:/').free>total+64*1024*1024
    retained={p.name for p in Path('out').glob('*.nds')};assert len(retained)==183
    DEST.mkdir(parents=True);records=[]
    def archive_file(source,target):
        target.parent.mkdir(parents=True,exist_ok=True);copyfile(source,target)
        digest=sha(source.read_bytes());assert sha(target.read_bytes())==digest
        records.append({'source':str(source),'archived':str(target.relative_to(DEST)),'sha256':digest})
    for p in sorted(files,key=str):archive_file(p,DEST/'repository'/p.relative_to(root))
    for directory,p in captures:archive_file(p,DEST/'captures'/directory.name/p.relative_to(directory))
    for p in guide_files:archive_file(p,DEST/'guide'/p.relative_to(guide))
    assert retained=={p.name for p in Path('out').glob('*.nds')}
    assert sha(ledger.read_bytes())==receipt['ledger_sha256'] and sha(handoff.read_bytes())==receipt['handoff_sha256']
    inherited=Path('E:/Rota Nova translations/Editorial review/V1780 Lil lessons64 registered and verified/archive_receipt.json')
    assert inherited.is_file()
    save(DEST/'archive_receipt.json',{'files':records,'all_archived_bytes_equal_sources':True,'archived_source_bytes':total,
        'empty_failed_observation_directories_preserved_as_metadata':empty,
        'all_existing_out_ROMs_retained':len(retained),'candidate_bytes_unchanged':release['candidate_sha256'],
        'exact_clean_patch_sha256':release['patch_sha256'],'newly_completed':15,'complete':1503,
        'current_native_substitution_cases':2700,'fresh_current_native_full_font_samples':15,
        'current_actual_close_range_holds':2,'positive_and_negative_terminal_evidence_preserved':True,
        'inherited_archive_receipt':str(inherited),'inherited_archive_receipt_sha256':sha(inherited.read_bytes()),
        'full_editorial_goal_active_graphics_separate_andunfinished':True,
        'Armed_Latina_UI_andsuccessful_Lookout_shot_still_open':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'archive':str(DEST),'exact_files':len(records),'bytes':total,'retained_out_ROMs':len(retained)},flush=True)
