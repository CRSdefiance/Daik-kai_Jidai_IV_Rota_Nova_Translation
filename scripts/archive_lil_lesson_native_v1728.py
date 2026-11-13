"""Archive exact branch/font/actual-context research with unresolved FE metrics."""
from pathlib import Path
from shutil import copyfile
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.verify_village_wrap_v608 import read,save

DEST=Path('E:/Rota Nova translations/Editorial review/V1728 Lil lessons native branches and FE context')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_lesson_context_v1723_1711')


if __name__=='__main__':
    assert not DEST.exists()
    checkpoint=Path('work/analysis/lil_lesson_native_checkpoint_v1727b/checkpoint_receipt.json');receipt=read(checkpoint)
    assert receipt['all_current_jobs_terminal'] and receipt['actual_multiline_FE_model_findings']==5
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1424,1632)
    assert sum(len(v) for v in ledger['active_source_prose_drafts']['route_record_subsets_pending'].values())==64
    assert sha(Path(receipt['candidate']).read_bytes())==receipt['candidate_sha256']=='251594f89f950f1deb68d6359b6861d6f4a96eb8e9a9045c148d6d6cb64b1201'
    manifest=read(Path(receipt['candidate']).with_suffix('.manifest.json'))
    assert sha(Path('translations/release_stack.json').read_bytes())==manifest['release_stack_sha256']
    assert sha(harness.CORE.read_bytes())==read(CAP/'capture_report.json')['core_DLL_sha256']
    for p,digest in receipt['proofs'].items():assert sha(Path(p).read_bytes())==digest
    assert sha(Path('docs/editorial_handoff_current.md').read_bytes())==receipt['handoff_sha256']
    files={Path(p) for p in ['translations/editorial_review_current_v1.json','translations/release_stack.json',
        'translations/lil_lessons_editorial_manuscript_v1.json','translations/lil_lessons_editorial_manuscript_v2.json',
        'translations/lil_lesson_choices_editorial_draft_v1.json','docs/editorial_handoff_current.md',
        'docs/lil_lessons_v1727_native_checkpoint.md','docs/editorial_review_goal.md','docs/translation_progress.md',
        'docs/known_issues.md','docs/todo.md',__file__]}
    for name in ['lil_lesson_branches_v1722','lil_lesson_context_v1723','lil_lesson_fonts_v1724','lil_lesson_fonts_v1724b',
        'lil_lesson_fonts_v1724c','lil_lesson_layout_v1725','lil_lesson_context_audit_v1726c',
        'lil_lesson_native_checkpoint_v1727','lil_lesson_native_checkpoint_v1727b']:
        files.update(p for p in (Path('work/analysis')/name).rglob('*') if p.is_file())
    files.update(p for p in Path('scripts').glob('*.py') if any('_v'+str(n) in p.stem for n in range(1722,1729)))
    retained={p.name for p in Path('out').glob('*.nds')};root=Path.cwd().absolute();DEST.mkdir(parents=True);records=[]
    for p in sorted(files,key=str):
        target=DEST/'repository'/p.absolute().relative_to(root);target.parent.mkdir(parents=True,exist_ok=True);copyfile(p,target)
        digest=sha(p.read_bytes());assert sha(target.read_bytes())==digest
        records.append({'source':str(p),'archived':str(target.relative_to(DEST)),'sha256':digest})
    for p in sorted(CAP.rglob('*')):
        if not p.is_file():continue
        target=DEST/'ordinary_original_wind_lesson_cold_boot'/p.relative_to(CAP)
        target.parent.mkdir(parents=True,exist_ok=True);copyfile(p,target)
        digest=sha(p.read_bytes());assert sha(target.read_bytes())==digest
        records.append({'source':str(p),'archived':str(target.relative_to(DEST)),'sha256':digest})
    assert retained=={p.name for p in Path('out').glob('*.nds')}
    assert sha(Path(receipt['candidate']).read_bytes())==receipt['candidate_sha256']
    save(DEST/'archive_receipt.json',{'files':records,'all_archived_bytes_equal_sources':True,
        'all_existing_out_ROMs_retained':len(retained),'current_ROM_unchanged_sha256':receipt['candidate_sha256'],
        '36_native_relative_skip_sites360_cases':True,'60_isolated_native_font_planes_9_FE_dispatchers':True,
        'current_original_wind_branch_terminal29930_and262_callbacks_audited':True,
        'actual_multiline_FE_geometry_remains_unresolved_not_claimed_complete':True,
        'source_alignment_address_report_erratum_preserved':True,'all64_drafts_still_open':True,
        'no_new_ROM_patch_or_finalized_guide_capture':True,'full_goal_active_graphics_separate':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'archive':str(DEST),'exact_files':len(records),'all_out_ROMs_retained':len(retained),
        'completed':1424,'source_prose_reviewed':1632,'all64_lesson_drafts_open':True},flush=True)
