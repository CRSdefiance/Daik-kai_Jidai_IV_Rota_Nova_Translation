"""Archive the registered lessons checkpoint and new captures without pruning."""
import re
from pathlib import Path
from shutil import copyfile,disk_usage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

DEST=Path('E:/Rota Nova translations/Editorial review/V1780 Lil lessons64 registered and verified')
ROOTS=['lil_sailing_choice0_v1770','lil_sailing_navigation_v1771','lil_sailing_choice0_audit_v1772',
    'lil_lessons_reference_approval_v1773','lil_lessons_release_v1774','lil_lessons_completion_v1779']
CAPS=['lil_sailing_choice0_v1770_RESEARCH_ONLY','lil_lessons_v1775_newgame','lil_lessons_v1775_title']

if __name__=='__main__':
    assert not DEST.exists()
    receipt=read('work/analysis/lil_lessons_completion_v1779/completion_receipt.json')
    assert receipt['all_current_jobs_terminal'] and receipt['newly_completed']==64
    ledger,handoff=Path('translations/editorial_review_current_v1.json'),Path('docs/editorial_handoff_current.md')
    assert sha(ledger.read_bytes())==receipt['ledger_sha256'] and sha(handoff.read_bytes())==receipt['handoff_sha256']
    release=read('work/analysis/lil_lessons_release_v1774/registered_release_verification.json')
    files={ledger,handoff,Path(__file__),Path('translations/release_stack.json'),
        Path('translations/lil_lessons_final_review_v1.json'),Path('translations/lil_lessons_editorial_release_v1.json'),
        Path('scripts/build_integrated_release.py'),Path('dk4tool/patch/lil_lessons_editorial.py'),
        Path('docs/lil_lessons_v1779_completion.md'),Path(release['candidate']),Path(release['patch']),
        Path(release['candidate']).with_suffix('.manifest.json')}
    files.update(Path(p)for p in read('translations/lil_lessons_editorial_release_v1.json')['dependencies'])
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        files.add(Path('docs')/name)
    for name in ROOTS:
        directory=Path('work/analysis')/name;assert directory.is_dir()
        files.update(p for p in directory.rglob('*')if p.is_file())
    for p in Path('scripts').glob('*.py'):
        match=re.search(r'_v(\d+)',p.stem)
        if match and 1770<=int(match[1])<=1780:files.add(p)
    captures=[]
    for name in CAPS:
        directory=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/name
        assert (directory/'capture_report.json').is_file()
        captures.extend((directory,p)for p in directory.rglob('*')if p.is_file())
    guide=Path(receipt['guide']);assert (guide/'capture_provenance.json').is_file()
    guide_files=[p for p in guide.rglob('*')if p.is_file()]
    inherited=[]
    for name in ['V1750 Lil native choices FE resolution and revised wind','V1769 Lil crew both choices and current lesson wording']:
        archive=Path('E:/Rota Nova translations/Editorial review')/name
        if archive.is_dir():
            record=archive/'archive_receipt.json';assert record.is_file()
            inherited.append({'archive':str(archive),'receipt_sha256':sha(record.read_bytes())})
    assert any('V1769' in r['archive']for r in inherited)
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
    save(DEST/'archive_receipt.json',{'files':records,'all_archived_bytes_equal_sources':True,
        'archived_source_bytes':total,'all_existing_out_ROMs_retained':len(retained),
        'inherited_archives_retained_for_earlier_source_native_and_actual_evidence':inherited,
        'registered_candidate':release['candidate'],'registered_candidate_sha256':release['candidate_sha256'],
        'exact_clean_patch_sha256':release['patch_sha256'],'newly_completed':64,'complete':1488,
        'individual_actual_speech_count':55,'explicit_unvisited_native_equivalents':5,
        'full_editorial_goal_active_graphics_all18_plaques_separately_unfinished':True,
        'all_current_jobs_terminal':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'archive':str(DEST),'exact_files':len(records),'bytes':total,'retained_out_ROMs':len(retained)},flush=True)
