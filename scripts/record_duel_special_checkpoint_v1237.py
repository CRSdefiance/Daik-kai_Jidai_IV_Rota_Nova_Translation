"""Record integrated/native progress without awarding special gameplay credit."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_special_checkpoint_v1237')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V1237 Special moves native integration checkpoint')
ROM = Path('out/all_routes_combined_v1224_candidate.nds')
RELEASE = Path('work/analysis/duel_special_release_v1223')


def main():
    assert not ROOT.exists() and not ARCHIVE.exists()
    release = read(RELEASE/'registered_release_verification.json')
    startup = read(RELEASE/'ordinary_startup_verification.json')
    shop = read(RELEASE/'photographed_shop_formatting.json')
    assert release['candidate_sha256'] == startup['candidate_sha256'] == shop['candidate_sha256'] == sha(ROM.read_bytes())
    assert release['complete_reconstruction_byte_exact'] and startup['all8_complete_startup_title_NewGame_frames_exact']
    runs = []
    for folder, run, scan in [
        ('duel_special_v1225_1224','work/analysis/duel_special_live_v1225','work/analysis/duel_special_actual_v1228/scan_through12302.json'),
        ('duel_special_v1232_1224','work/analysis/duel_special_live_v1232','work/analysis/duel_special_actual_v1234/scan_through9502.json'),
        *[(f'duel_special_v1235_1224_p{p}',f'work/analysis/duel_special_matrix_v1235_{p}',
           f'work/analysis/duel_special_actual_v1236_p{p}/scan_through11502.json') for p in (37,53,71)]]:
        cap = Path('E:/Rota Nova translations/Generated/work/emulation_v193')/folder
        report = read(cap/'capture_report.json')
        assert report['ROM_sha256'] == release['candidate_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert read(Path(run)/'terminal_preservation.json')['source_and_disposable_donors_unchanged']
        assert not read(scan)['complete_visible_holds']
        runs.append({'folder': str(cap), 'run': run, 'report': str(cap/'capture_report.json'),
            'report_sha256': sha((cap/'capture_report.json').read_bytes()),
            'terminal_frame': report['frames'], 'scan': scan, 'scan_sha256': sha(Path(scan).read_bytes()),
            'source_and_disposable_saves_unchanged': True,
            'complete_visible_special_holds': 0})
    doc_path = Path('docs/duel_special_v1237_checkpoint.md')
    assert not doc_path.exists()
    text = '''# V1237 special-move editorial checkpoint

The15 source/prose-reviewed special calls1980-1993 and2146 now have approved
native formatting and a registered combined V1224 candidate. Nine wordings were
revised; six were retained. Their actual-special gameplay gate remains open.
No new entry receives completed editorial credit.

## Exact integrated candidate

- Profile: `all-routes-unified-v1224`; all471 batches and114 accepted layers retained.
- ROM SHA256: `cdc860e53267dbef64ac9d40a1832b00fda6a4da6adbde2b61be830345d55dbd`.
- COMMON SHA256: `752f8eb5a6ccf7d4e20dc0309fd1f8427f28855db01982e6b56c0d62748d682a`.
- ARM9 SHA256: `384b993eb89c5578acb66925ff1f6412e1a3d68073164600b896dc563779276c`.
- Exact clean-input patch SHA256: `f76a2b5a3443e296afd9be68bddef562389f9a671f9d7249aec33e3f3896949e`.
- Canonical accepted parent and prior whole-batch scene-verified V997 remain unchanged.

## Completed evidence

Clean-source dispatch maps all15 actual numeric calls, including Julio2146 outside
the former14-entry group. White Tree school kanji are distinguished from the
separately verified Shiraki surname. Native dispatch checks131324 qualified and
negative cases. Source-owned64-byte unreachable function tail535E8-53628 is used
only after complete incoming reference/PC-relative census; its public ARM entry
535E0 retains the exact return0/BX. The existing108-byte front calls that private
helper. No section,BSS,cache,arena,ITCM or123040-byte staged payload grows.

All15 special and36 prior voice full-font cases pass, as do49 excluded callers,
7336 warm/cold native copies,180 cache sequences and13 original direct escape
pipelines. Every special preview was visually reviewed for complete first/final
letters, uniform margins, word boundaries and the three original144x12 crops.
The first escape-control test mistakenly compared prose without its stored guard;
V1219b fixes the test input while preserving the actual renderer and guard.

The complete release manifest and clean-patch reconstruction pass. Eight ordinary
no-save startup/title/New Game full-screen captures match V1105 and were visually
reviewed. The photographed shop676/677 retains its exact repaired text, native
wrapping and full228x64 fonts; no fresh shop activation is claimed.

## Original gameplay remains open

Five separate cold boots reach original duels and natural victories. No complete
visible special move was observed. The first run uses positive2000 HP before
combat; the original damage method7E108 clamps HP to the normal7DF58 maximum,
so that fixture does not provide the intended long duel. Its31 pre-duel fixtures
have complete4MiB replay/identity/RNG audits. The other four runs retain the
ordinary healthy-contact fixture and recorded A-button schedules, including
predeclared periods37,53,71. Their terminal reports and source/disposable save
preservation pass; their full fixture replays remain separate pending evidence.
No actor ID,numeric message,RNG seed,eligibility flag or result is injected.
No healing,revival or relocation occurs during or after a duel.

Next: map the original HP-limit prerequisites and use a disclosed health/equipment
fixture before combat, or another ordinary encounter, to observe a real special.
Do not infer activation solely from a persistent bitmap or award the15 entries
before the family gameplay gate is verified. These headless targeted runs do not
constitute a whole-route playthrough or hardware verification.

Counts remain1245 complete (925 revised,320 retained),1298 source/prose reviewed.
There are53 reviewed-incomplete COMMON entries, plus the broader unreviewed
shared/routes/raw-source inventory. All18 plaques and the separate graphics audit
remain open. The full editorial goal remains active.
'''
    doc_path.write_text(text, encoding='utf-8')
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert ledger['records_editorially_completed'] == 1245 and ledger['records_with_source_and_prose_pass'] == 1298
    ledger['latest_checkpoint'] = 'V1237:15 specials native-format approved and integrated V1224;51 full fonts49 exclusions,7336 copies180 cache sequences13 escape pipelines,eight startup frames and exact patch pass. Five original duels have no verified special activation;15 entries receive no completed credit.1245 complete/1298 source-prose;full goal active.'
    ledger['latest_registered_formatting_candidate'] = {
        'path': str(ROM), 'sha256': release['candidate_sha256'], 'profile': 'all-routes-unified-v1224',
        'MESFILE_sha256': release['COMMON_sha256'], 'ARM9_sha256': release['ARM9_sha256'],
        'patch': release['patch'], 'patch_sha256': release['patch_sha256'],
        'status': 'experimental;15-native-approved-specials;original-special-activation-and-broader-goal-open',
        'release_verification': str(RELEASE/'registered_release_verification.json'),
        'startup_verification': str(RELEASE/'ordinary_startup_verification.json'),
        'checkpoint': str(doc_path)}
    ledger['current_native_relocation_reference'] = {
        'candidate': str(ROM), 'COMMON_sha256': release['COMMON_sha256'], 'ARM9_sha256': release['ARM9_sha256'],
        'parser': 'dk4tool.patch.duel_special_editorial.current_entries',
        'release_config': 'translations/duel_special_editorial_release_v1.json',
        'requires_guarded_single8192_cache_policy': True,
        'opaque1484byte_prefix_and_carrier1931_are_owned_and_hash_locked': True,
        'only15_reviewed_special_paragraphs_changed_from_V1206_all3653_other_texts_exact': True,
        'candidate_experimental_broader_goal_pending': True}
    special = ledger['duel_special_prose_v1216']
    special.update(native_format_and_actual_pending=False, native_formatting_pass=True,
        actual_gameplay_pending=True, completed_entries=0, integrated_candidate=str(ROM),
        release_verification=str(RELEASE/'registered_release_verification.json'),
        ordinary_startup_verification=str(RELEASE/'ordinary_startup_verification.json'),
        unsuccessful_original_special_observation_runs=runs, checkpoint=str(doc_path))
    watch = ledger['formatting_watchlist']
    watch['latest_reference_proof'] = str(RELEASE/'photographed_shop_formatting.json')
    watch['latest_user_screenshot_recheck'].update(proof=watch['latest_reference_proof'], candidate=str(ROM),
        exact_repaired676_677_bytes_preserved=True, complete_native_wrapping_and_glyph_planes_rechecked=True,
        new_actual_shop_activation_claimed=False)
    save(ledger_path, ledger)
    pins_path = Path('translations/rom_retention_pins.json')
    pins = read(pins_path)
    physical = 'E:/Rota Nova translations/Generated/out/all_routes_combined_v1224_candidate.nds'
    assert not any(p['path'].replace('\\','/').lower() == physical.lower() for p in pins)
    pins.append({'path': physical, 'reason': 'V1237 active special-move integration/native and pending original gameplay reference; do not prune.'})
    save(pins_path, pins)
    for p in ('docs/known_issues.md','docs/todo.md','docs/translation_progress.md','docs/editorial_review_goal.md'):
        with Path(p).open('a',encoding='utf-8') as f:
            f.write('\n\n## V1237 special-move native integration checkpoint\n\n'
                'V1224 integrates15 source/prose/native-format approved special calls, including Julio2146. '
                '51 full fonts49 exclusions,7336 copies180 cache sequences13 escape pipelines,eight ordinary startup frames, '
                'photographed shop676/677 and exact clean-input patch pass. Five original duels have no verified special activation; '
                'the15 entries receive no completed credit. Extra current HP is clamped on damage;map the original HP-limit prerequisite next. '
                '1245 complete/1298 source-prose;53 reviewed-incomplete COMMON plus broader inventory. '
                'Canonical,V997,all18 plaque entries and the separate graphics audit unchanged. Full goal active. '
                'See [checkpoint](duel_special_v1237_checkpoint.md).\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'checkpoint.json', {'candidate':str(ROM), 'candidate_sha256':release['candidate_sha256'],
        'patch_sha256':release['patch_sha256'], 'source_prose_reviewed':1298, 'editorially_complete':1245,
        'new_special_completed_entries':0, 'original_special_observation_runs':runs,
        'startup_sheet_visually_reviewed':True, 'native_special_sheet_visually_reviewed':True,
        'checkpoint_document':str(doc_path), 'producer_sha256':sha(Path(__file__).read_bytes()),
        'full_goal_complete':False})
    ARCHIVE.mkdir(parents=True)
    files = {Path(__file__).absolute(), ledger_path.absolute(), pins_path.absolute(), doc_path.absolute(),
        ROM.with_suffix('.manifest.json').absolute(), ROM.with_suffix('.xdelta').absolute()}
    for p in ('docs/known_issues.md','docs/todo.md','docs/translation_progress.md','docs/editorial_review_goal.md',
              'scripts/build_integrated_release.py','translations/release_stack.json',
              'dk4tool/patch/duel_special_editorial.py','translations/duel_special_editorial_release_v1.json',
              'translations/duel_special_editorial_manuscript_v1.json','translations/duel_special_editorial_manuscript_v2.json'):
        files.add(Path(p).absolute())
    files.update(p.absolute() for p in Path('scripts').glob('*duel_special*.py'))
    for folder in Path('work/analysis').glob('duel_special*'):
        if folder.is_dir():
            files.update(p.absolute() for p in folder.rglob('*') if p.is_file() and p.suffix in ('.json','.jsonl','.py','.png','.bin')
                         and p.name != 'builder_added_optional_stage.bin')
    files.add((RELEASE/'builder_added_optional_stage.bin').absolute())
    copies = []
    for source in sorted(files):
        relative = source.relative_to(Path.cwd().absolute())
        dest = ARCHIVE/'Repository'/relative
        dest.parent.mkdir(parents=True,exist_ok=True)
        copy2(source,dest)
        assert sha(source.read_bytes()) == sha(dest.read_bytes())
        copies.append({'source':str(source),'archived':str(dest),'sha256':sha(dest.read_bytes())})
    for run in runs:
        cap=Path(run['folder'])
        for name in ('capture_report.json','navigation_command_journal.json'):
            source=cap/name;dest=ARCHIVE/'External reports'/cap.name/name
            dest.parent.mkdir(parents=True,exist_ok=True);copy2(source,dest)
            assert source.read_bytes()==dest.read_bytes()
            copies.append({'source':str(source),'archived':str(dest),'sha256':sha(dest.read_bytes())})
    save(ARCHIVE/'archive_manifest.json', {'files':copies,'all_copies_hash_verified':True,
        'ROM_and_raw_emulator_snapshots_remain_in_their_pinned_E_drive_locations':True,
        'no_editorial_completion_credit_or_canonical_promotion':True,'full_goal_complete':False})
    save(ROOT/'archive_receipt.json', {'archive':str(ARCHIVE),'copied_files':len(copies),
        'manifest_sha256':sha((ARCHIVE/'archive_manifest.json').read_bytes())})
    print('V1237 checkpoint:1245 complete unchanged;15 special gameplay gates open;',len(copies),'archive copies verified.',flush=True)


if __name__=='__main__':main()
