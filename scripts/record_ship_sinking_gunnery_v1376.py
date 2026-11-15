"""Preserve the terminal gunnery pilot and its explicitly incomplete status."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_sinking_archive_v1376')
DEST = Path('E:/Rota Nova translations/Editorial review/V1376 Original gunnery pilot')
PROOF = Path('work/analysis/ship_sinking_gunnery_verified_v1375/terminal_gunnery_pilot_verification.json')


def main():
    assert not ROOT.exists() and not DEST.exists()
    proof = read(PROOF)
    assert proof['terminal_frame']==11360 and proof['no_sinking_notice_seen_or_sinking_translation_completion_claimed']
    assert proof['entire4MiB_fixture_delta_and_every_input_audited']
    ledger = read('translations/editorial_review_current_v1.json')
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1307,1395)
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==88
    summary = ('V1375 audits the original gunnery pilot on unchanged registered V1364. '
        'Cold boot reaches11360 with63 PNG captures and58 complete4MiB snapshots,all hashes/inputs verified. '
        'The entire replay prefix through9100 matches the earlier V1364 run. '
        'Only the existing40-owned-byte prebattle location fixture at4800 is applied;'
        'all later actions are normal controls and no health/crew/actor/ID/RNG/result changes occur. '
        'Source and disposable donor saves remain exact. Enemy slot2 naturally changes from Hull30/Crew21 '
        'to Hull26/Crew0;no sinking notice appears. The harness stops with original battle still active;'
        'the attempted eastward departure did not prove a gameplay withdrawal. '
        'No sinking,withdrawal or translation completion credit is added. '
        'Counts remain1307 complete(975 revised332 retained),1395 source/prose and88 reviewed-incomplete COMMON'
        '(16 sinking34 aftermath38 older),plus broader shared/routes/raw prose. '
        'Choose a source-bound test setup that can exhaust Hull before crew;do not lower enemy health or forge outcomes. '
        'The current16 sinking texts remain native/integrated but original visible event/dismissal/transition gates stay open. '
        'Canonical,V997,graphics/all18 plaques and the later older-record re-audit remain unchanged/open;full goal active.')
    document = Path('docs/ship_sinking_gunnery_v1375_checkpoint.md')
    assert not document.exists()
    document.write_text('# V1375 original gunnery pilot: sinking still pending\n\n'+summary+'\n\n'
        '## Exact evidence\n\n'
        '- Current experimental ROM: `E:/Rota Nova translations/Generated/out/all_routes_combined_v1364_candidate.nds`.\n'
        '- SHA-256: `'+proof['candidate_sha256']+'`. No ROM or patch changed.\n'
        '- Verified pilot: `'+str(PROOF)+'`.\n'
        '- Capture folder: `E:/Rota Nova translations/Generated/work/emulation_v193/ship_sinking_gunnery_v1373_1364`.\n'
        '- Source donor SHA-256: `'+proof['source_donor_sha256']+'`.\n'
        '- Native inspections: `work/analysis/ship_sinking_inspection_v1374`.\n\n'
        'The stale wrapped dialogue buffer is not visible-dialogue evidence. Native health getters and the '
        'actual screenshots establish the combat state. No new finalized guide screenshot is added from this '
        'inconclusive pilot. These targeted headless captures do not prove earned travel,a complete route,or hardware behavior.\n\n'
        'The photographed shop676/677 formatting repair remains a required regression reference:complete '
        'leading/trailing glyphs,uniform margins,no internal alignment gaps,no stray text,wraps,pagination,bounds '
        'and following-scene transitions remain part of the editorial goal. The current V1364 proof is '
        '`work/analysis/flagship_precision_release_v1363/photographed_shop_formatting.json`;'
        'this pilot does not claim a fresh shop visit.\n',encoding='utf-8')
    for name in ['docs/known_issues.md','docs/todo.md','docs/translation_progress.md']:
        path = Path(name)
        text = path.read_text(encoding='utf-8')
        assert '## V1375 original gunnery pilot' not in text
        path.write_text(text+'\n\n## V1375 original gunnery pilot\n\n'+summary+
            '\n\nSee [checkpoint](ship_sinking_gunnery_v1375_checkpoint.md).\n',encoding='utf-8')
    ROOT.mkdir(parents=True)
    DEST.mkdir(parents=True)
    paths = [document,Path(__file__),PROOF,Path('translations/editorial_review_current_v1.json')]
    paths += [Path(name) for name in ['docs/known_issues.md','docs/todo.md','docs/translation_progress.md',
        'scripts/run_ship_sinking_gunnery_v1373.py','scripts/inspect_ship_sinking_live_v1374.py',
        'scripts/verify_ship_sinking_gunnery_v1375.py','scripts/native_flagship_capture_fixture_v1368.py',
        'scripts/native_ship_sinking_fixture_v1352.py','scripts/native_ship_sinking_fixture_v1351.py',
        'work/analysis/flagship_precision_release_v1363/photographed_shop_formatting.json',
        'work/analysis/flagship_precision_release_v1363/registered_release_verification.json']]
    for folder in ['work/analysis/ship_sinking_gunnery_v1373','work/analysis/ship_sinking_inspection_v1374',
        'work/analysis/ship_sinking_gunnery_verified_v1375']:
        paths += list(Path(folder).glob('*.json'))+list(Path(folder).glob('*.jsonl'))
    copied = []
    workspace = Path.cwd().absolute()
    for source in sorted(set(paths)):
        relative = source.absolute().relative_to(workspace)
        target = DEST/'workspace'/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        copy2(source,target)
        digest = sha(source.read_bytes())
        assert sha(target.read_bytes())==digest
        copied.append({'source':str(source),'archive':str(target),'sha256':digest})
    report_path = Path(proof['terminal_report'])
    report = read(report_path)
    refs = [{'path':str(report_path),'sha256':sha(report_path.read_bytes())}]
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
        refs.append({'path':row['path'],'sha256':row['PNG_sha256'],'kind':'PNG'})
    for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        assert sha(Path(row['path']).read_bytes())==row['sha256']
        refs.append({'path':row['path'],'sha256':row['sha256'],'kind':'read-only-RAM'})
    for field in ['candidate','source_donor']:
        plan = read('work/analysis/ship_sinking_gunnery_v1373/run_plan.json')
        path = Path(plan[field])
        digest = sha(path.read_bytes())
        assert digest==plan[field+'_sha256']
        refs.append({'path':str(path),'sha256':digest,'kind':field})
    receipt = {'archive':str(DEST),'workspace_files':copied,
        'original_E_drive_capture_ROM_and_donor_references_verified_and_preserved':refs,
        'originals_preserved_no_ROM_moved_changed_or_deleted':True,
        'completion_counts_unchanged':1307,'source_prose_unchanged':1395,'reviewed_incomplete_unchanged':88,
        'no_new_finalized_guide_screenshot_or_sinking_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'archive_receipt.json',receipt)
    copy2(ROOT/'archive_receipt.json',DEST/'archive_receipt.json')
    print(f'Gunnery pilot checkpoint archived:{len(copied)} files;all original E-drive evidence preserved;no new completion credit.',flush=True)


if __name__=='__main__':
    main()
