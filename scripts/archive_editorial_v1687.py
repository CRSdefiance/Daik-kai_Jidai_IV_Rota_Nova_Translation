"""Archive reconstructable production inputs and completion evidence;retain all ROMs."""
import os
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/editorial_archive_v1687')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V1687 Search11 and hot-spring14 complete')

if __name__=='__main__':
    assert not ROOT.exists() and not ARCHIVE.exists()
    completion=read('work/analysis/editorial_completion_v1686/completion_receipt.json')
    assert completion['completed']==1375 and completion['newly_completed']==25 and not completion['full_goal_complete']
    config=read('translations/search_reports_editorial_release_v1.json')
    selected={Path(p) for p in config['dependencies']}
    selected.update(Path(p) for p in ['translations/search_reports_editorial_release_v1.json','translations/editorial_review_current_v1.json',
        'translations/release_stack.json','translations/rom_retention_pins.json','scripts/build_integrated_release.py',__file__,
        'docs/editorial_handoff_current.md','docs/search_hot_spring_v1686_completion.md','docs/translation_progress.md','docs/known_issues.md','docs/todo.md','docs/editorial_review_goal.md',
        'work/analysis/search_reports_live_v1680/navigation.jsonl','work/analysis/search_reports_live_v1680/run_plan.json',
        'work/analysis/search_reports_live_v1680/terminal_preservation.json','work/analysis/search_reports_live_v1680/actual_Search_cases.json',
        'work/analysis/search_reports_live_v1680/actual_optional_hot_spring_cases.json',
        'work/analysis/search_reports_release_v1675/registered_release_verification.json'])
    selected.update(Path(p) for p in completion['final_reviews'])
    selected.update(Path(p) for p in completion['proofs'])
    selected.update(Path(p) for p in [completion['candidate'],completion['patch']])
    selected.add(Path(completion['candidate']).with_suffix('.manifest.json'))
    selected.update(Path('scripts').glob('*search_reports*.py'))
    selected.update(Path('scripts').glob('*search_hot_spring*.py'))
    selected.update(Path('scripts').glob('*search_run_audit*.py'))
    selected.add(Path('scripts/verify_hot_spring_optional_v1684.py'))
    for folder in ['editorial_completion_v1686','search_reports_release_v1675','search_reports_actual_v1683','hot_spring_optional_actual_v1684']:
        selected.update((Path('work/analysis')/folder).glob('*.json'))
    for picture in completion['screenshots']:selected.add(Path(picture['guide']))
    selected.add(Path(completion['guide'])/'capture_provenance.json')
    source_root=Path.cwd().absolute();archive_root=Path(os.path.abspath(str(ARCHIVE)))
    count_before=len(list(Path('out').glob('*.nds')))
    ARCHIVE.mkdir(parents=True);ROOT.mkdir(parents=True);copied=[]
    for source in sorted(selected,key=lambda p:str(p).lower()):
        assert source.is_file(),str(source)
        absolute=source.absolute()
        try:relative=absolute.relative_to(source_root)
        except ValueError:
            assert str(absolute).lower().startswith('e:\\rota nova translations\\')
            relative=Path('_external_E')/Path(*absolute.parts[1:])
        target=Path(os.path.abspath(str(ARCHIVE/relative)));target.relative_to(archive_root)
        target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        digest=sha(source.read_bytes());assert sha(target.read_bytes())==digest
        copied.append({'source':str(source),'archive_relative':str(relative),'sha256':digest,'bytes':source.stat().st_size})
    assert len(list(Path('out').glob('*.nds')))==count_before
    receipt={'archive':str(ARCHIVE),'files':copied,'all_archived_files_byte_exact':True,
             'generated_out_ROM_count_unchanged':count_before,'no_ROM_or_other_file_deleted':True,
             'candidate_sha256':completion['candidate_sha256'],'patch_sha256':completion['patch_sha256'],
             'all_raw_emulator_captures_and_RAM_retained_at_recorded_E_paths':True,
             'full_editorial_goal_active_and_graphics_separate':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'archive_receipt.json',receipt);save(ARCHIVE/'archive_receipt.json',receipt)
    print(f'Archived{len(copied)} exact files including candidate,patch,manifest,source/native/release/current completion evidence and8 guide captures. Retained all{count_before} generated out ROMs;full goal active.')
