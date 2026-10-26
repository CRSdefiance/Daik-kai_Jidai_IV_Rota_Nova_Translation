"""Exact source-review checkpoint archive;all64 lesson drafts remain open."""
from pathlib import Path
from shutil import copyfile
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

DEST=Path('E:/Rota Nova translations/Editorial review/V1721 Lil lessons64 source review')


if __name__=='__main__':
    assert not DEST.exists()
    receipt=read('work/analysis/lil_lessons_checkpoint_v1720/checkpoint_receipt.json')
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1424,1632)
    ids=[i for v in ledger['active_source_prose_drafts']['route_record_subsets_pending'].values() for i in v]
    assert len(ids)==len(set(ids))==64
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==144
    assert sha(Path(receipt['candidate']).read_bytes())==receipt['candidate_sha256']
    manifest=read(Path(receipt['candidate']).with_suffix('.manifest.json'))
    assert sha(Path('translations/release_stack.json').read_bytes())==manifest['release_stack_sha256']
    assert sha(Path('work/clean.nds').read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    for p,digest in receipt['proofs'].items():assert sha(Path(p).read_bytes())==digest
    handoff=Path('docs/editorial_handoff_current.md')
    assert sha(handoff.read_bytes())==receipt['handoff_sha256']
    text=handoff.read_text(encoding='utf-8')
    old='Source/prose count did not increase at this completion.'
    new='Opening-completion V1715 added no source/prose credit;the subsequent V1720 lesson review added64.'
    assert text.count(old)==1
    handoff.write_text(text.replace(old,new,1),encoding='utf-8')
    files={Path(p) for p in ['translations/editorial_review_current_v1.json','translations/release_stack.json',
        'translations/lil_lessons_editorial_manuscript_v1.json','translations/lil_lesson_choices_editorial_draft_v1.json',
        'docs/editorial_handoff_current.md','docs/lil_lessons_v1720_source_review.md','docs/editorial_review_goal.md',
        'docs/translation_progress.md','docs/known_issues.md','docs/todo.md',__file__]}
    for name in ['lil_lessons_source_v1717','lil_lesson_choices_v1718','lil_lessons_editorial_v1719','lil_lessons_checkpoint_v1720']:
        files.update(p for p in (Path('work/analysis')/name).rglob('*') if p.is_file())
    files.update(Path(p) for p in ['scripts/inventory_lil_lessons_v1717.py','scripts/map_lil_lesson_choices_v1718.py',
        'scripts/author_lil_lessons_v1719.py','scripts/checkpoint_lil_lessons_v1720.py'])
    retained={p.name for p in Path('out').glob('*.nds')}
    root=Path.cwd().absolute();DEST.mkdir(parents=True);records=[]
    for p in sorted(files,key=str):
        relative=p.absolute().relative_to(root);target=DEST/'repository'/relative
        target.parent.mkdir(parents=True,exist_ok=True);copyfile(p,target)
        digest=sha(p.read_bytes());assert sha(target.read_bytes())==digest
        records.append({'source':str(p),'archived':str(target.relative_to(DEST)),'sha256':digest})
    assert retained=={p.name for p in Path('out').glob('*.nds')}
    assert sha(Path(receipt['candidate']).read_bytes())==receipt['candidate_sha256']
    save(DEST/'archive_receipt.json',{'files':records,'all_archived_bytes_equal_sources':True,
        'all_existing_out_ROMs_retained':len(retained),'current_ROM_unchanged_sha256':receipt['candidate_sha256'],
        'source_prose_reviews_added':64,'completed_entries_added':0,'all64_new_drafts_incomplete':True,
        'no_new_ROM_patch_or_finalized_guide_capture':True,'handoff_counter_history_clarified':True,
        'handoff_sha256':sha(handoff.read_bytes()),'full_goal_active_graphics_separate':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'archive':str(DEST),'exact_files':len(records),'all_out_ROMs_retained':len(retained),
        'completed':1424,'source_prose_reviewed':1632,'new_route_drafts_open':64},flush=True)
