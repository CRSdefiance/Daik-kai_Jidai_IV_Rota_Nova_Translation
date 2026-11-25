"""Record the integrated candidate and successful boots;keep22 actual scenes incomplete."""
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_declaration_v998')
BUILD = Path('work/analysis/battle_declaration_v997b')
ROM = Path('out/all_routes_combined_v997_candidate.nds')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
RETENTION = Path('work/rom_retention/20261021T0337253474054Z.json')


def main():
    assert not ROOT.exists()
    release = read(BUILD/'registered_release_verification.json')
    startup = read(BUILD/'ordinary_startup_verification.json')
    visual = read('work/analysis/battle_declaration_v996/visual_review.json')
    assert sha(ROM.read_bytes()) == release['candidate_sha256'] == startup['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes()) == release['patch_sha256']
    assert sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes()) == release['candidate_sha256']
    assert release['complete_reconstruction_byte_exact'] and startup['all8_complete_startup_title_NewGame_frames_exact']
    assert len(startup['pairs']) == 8 and visual['all176_complete_previews_visually_reviewed_via8_full_canvas_sheets']
    assert sha(Path(startup['review_sheet']).read_bytes()) == startup['review_sheet_sha256']
    assert release['startup_actual_UI_RGB_choices_dismissal_and_scene_returns_pending']
    plan = read(RETENTION)
    assert len(plan['roms']) == 217 and all(r['action'] == 'keep' for r in plan['roms'])
    assert sha(Path('scripts/prune_generated_roms.ps1').read_bytes()) == 'aacaca07b50f1bafcfc5bb8579b609b0be2a8e79e3107f336405ba370a435f6f'
    protected = read('work/analysis/full_fleet_victory_v654/replay_preflight.json')
    for key in ('donor', 'inputs', 'commands', 'fixture_source'):
        assert sha(Path(protected[key]).read_bytes()) == protected[key+'_sha256']
    preflight_provenance = Path('work/analysis/battle_declaration_v997/successor_provenance.json')
    preflight_targets = read(preflight_provenance)['preserved_preflight_targets']
    checked_targets = []
    for name, digest in preflight_targets.items():
        if Path(name) == preflight_provenance:
            assert digest == sha(b'')
        else:
            assert sha(Path(name).read_bytes()) == digest
            checked_targets.append(name)
    assert len(checked_targets) == 3
    guide = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V998 Startup checks')
    archive = Path('E:/Rota Nova translations/Editorial review/V998 Battle declaration combined build')
    doc = Path('docs/battle_declaration_v998_integrated_checkpoint.md')
    assert not guide.exists() and not archive.exists() and not doc.exists()
    guide_sources = [(CAP/'battle_declaration_v997_title/frame_001100_cold_boot.png', '01_Title_Menu.png'),
                     (CAP/'battle_declaration_v997_newgame/frame_002000_cold_boot.png', '02_New_Game_Confirmation.png')]
    assert all(p.exists() for p, name in guide_sources)
    ROOT.mkdir(parents=True)
    provenance_note = ROOT/'preflight_provenance_creation_state_note.json'
    save(provenance_note, {'historical_provenance': str(preflight_provenance),
        'historical_full_written_JSON_sha256': sha(preflight_provenance.read_bytes()),
        'all3_actual_preflight_targets_freshly_reverified': checked_targets,
        'self_entry_note': 'The historical inventory was evaluated after exclusive creation of its output file but before JSON contents were written. Its own empty-file hash records that creation state,not an enduring preservation claim. All three actual preflight targets remain exact. The release dependency separately pins the complete written provenance JSON hash. Preserve the historical file and do not treat its creation-state self entry as a current file checksum.',
        'release_ROM_patch_and_native_proofs_unaffected': True})
    startup_visual = ROOT/'startup_visual_review.json'
    save(startup_visual, {'ordinary_startup_verification': str(BUILD/'ordinary_startup_verification.json'),
        'ordinary_startup_verification_sha256': sha((BUILD/'ordinary_startup_verification.json').read_bytes()),
        'all8_complete_startup_and_title_screens_visually_reviewed': True,
        'title_captain_selection_confirmation_and_Rafael_opening_display_correctly': True,
        'new_battle_declaration_prompts_not_yet_activated': True,
        'review_sheet': startup['review_sheet'], 'review_sheet_sha256': startup['review_sheet_sha256'],
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    candidate = {'path': str(ROM), 'sha256': release['candidate_sha256'], 'profile': 'all-routes-unified-v997',
        'MESFILE_sha256': release['COMMON_sha256'], 'ARM9_sha256': release['ARM9_sha256'],
        'patch': str(ROM.with_suffix('.xdelta')), 'patch_sha256': release['patch_sha256'],
        'manifest': str(ROM.with_suffix('.manifest.json')),
        'status': 'experimental-native-font-copy-patch-startup-verified-battle-prompt-scenes-pending',
        'details': str(doc), 'full_goal_complete': False}
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass']) == (1174, 1199)
    assert ledger['current_integrated_candidate']['sha256'] == 'bac5998ad942868c85d51d2a3f589e43ffced4dbc93659de7cc659a066c17078'
    save(ROOT/'editorial_ledger_before_integrated_checkpoint.json', ledger)
    ledger['pending_registered_battle_declaration_candidate'] = candidate
    ledger['battle_declaration_v998'] = {'candidate': candidate, 'native_message_IDs': list(range(1889, 1911)),
        'status': 'registered-and-exact-patch-startup-verified-representative-scene-controls-pending',
        'release_proof': str(BUILD/'registered_release_verification.json'),
        'startup_proof': str(BUILD/'ordinary_startup_verification.json'), 'startup_visual_review': str(startup_visual),
        'completed_entries_added': 0, 'source_prose_reviews_added': 0}
    ledger['next_battle_declaration_actual_verification'] = {
        'candidate': candidate, 'protected_replay_preflight': 'work/analysis/full_fleet_victory_v654/replay_preflight.json',
        'protected_donor_sha256': protected['donor_sha256'],
        'original_departure_inputs': protected['inputs'], 'original_replay_commands': protected['commands'],
        'required_samples': ['original First Mate battle-readiness announcement',
            'known-faction confirmation with actual complete faction name,Cancel and Yes outcomes',
            'unknown-faction confirmation including Emilio voice6 ID1909 literal I at generated line end',
            'complete ordinary modal dismissal and return without blank or extra pages'],
        'fixture_constraints': 'Use a disposable cold-boot save copy and source-mapped location/crew-role/relation/knowledge/menu-state fixtures if required. Preserve actual captain,actor identities and source selection/renderer code;never inject a numeric message or forge a battle outcome. Document every RAM delta and no-earned-progression scope.',
        'no_live_process_left_by_this_checkpoint': True}
    checkpoint = ('V998 records registered combined V997 for the22 battle/declaration paragraphs. All471 batches114 accepted layers and final guards pass. Every unrelated file,graphics,route,name,font,ARM7/overlay and3646 unselected message strings,including user676/677 repair,remain exact to V987. The exact clean-input xdelta reconstructs every ROM byte. Two ordinary no-save cold boots provide eight whole-screen title/New Game frames exact to V987 and visually reviewed.176 native font cases,7336 native copies178 cache sequences and prior bounded runtime regressions are pinned. The actual battle/known/unknown prompt scenes,choice outcomes,dismissal,geometry and return remain pending;especially1909 literal I at a generated line end. No new editorial completion credit:1174 complete,1199 source/prose. V987 remains the current fully verified scene candidate;V997 is explicit pending test candidate,canonical unchanged. Global editorial scope,separate graphics/all18 plaques,older750-752,raw inventory,Samwell header and later older-record re-audit remain open;goal active.')
    ledger['latest_checkpoint'] = checkpoint
    ledger['research_checkpoints'].append({'id': 'V998-battle-declaration-integrated-startup',
        'proof': str(BUILD/'registered_release_verification.json'), 'candidate': candidate,
        'completed_entries_added': 0, 'source_prose_reviews_added': 0,
        'previous_goal_turn_classification': 'progress:22 source/prose reviews and fixed-footprint source runtime research verified',
        'this_goal_turn_classification': 'progress:176 full font canvases,macro-safe compiler,registered V997 exact patch,7336 native copies178 cache sequences and eight actual cold-boot screens',
        'full_goal_complete': False})
    previous = read(ROOT/'editorial_ledger_before_integrated_checkpoint.json')
    for key in ('current_integrated_candidate', 'source_pins', 'current_native_relocation_reference',
                'unresolved_graphics_work', 'older_record_reaudit_after_full_editorial_goal', 'raw_source_coverage_revisit', 'approved_name_roles'):
        assert ledger[key] == previous[key]
    save(ledger_path, ledger)
    with doc.open('x', encoding='utf-8') as f:
        f.write('# V998: registered V997 battle/declaration build and cold boots\n\n'+checkpoint+'\n\n')
        f.write('## Exact candidate\n\n- ROM: '+str(ROM)+'\n- SHA-256: '+candidate['sha256']+'\n- Profile: all-routes-unified-v997\n- Clean-input patch SHA-256: '+candidate['patch_sha256']+'\n- Clean input SHA-256: '+release['clean_input_sha256']+'\n- Canonical base SHA-256: '+release['canonical_sha256']+'\n\n')
        f.write('## Remaining gameplay gates\n\nExercise original ready/known/unknown source branches with real native role and faction getters. Confirm full words and uniform text origins against actual modal bitmap and RGB,portrait/name ownership,button/cursor bounds,Cancel and Yes side effects,normal dismissal and scene return. The one-paragraph compiler prevents pre-expansion I/LF macro collision;actual1909 at its generated boundary is a required sample. Fixtures must remain disclosed and source-bound;no earned progression or full route/hardware verification is claimed.\n')
    for p in map(Path, ('docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md', 'docs/known_issues.md')):
        with p.open('a', encoding='utf-8') as f:
            f.write('\n\n## V998: combined V997 and startup checks\n\n'+checkpoint+' See [V998 integrated checkpoint](battle_declaration_v998_integrated_checkpoint.md).\n')
    guide.mkdir(parents=True)
    guide_files = []
    for source, name in guide_sources:
        target = guide/name
        copy2(source, target)
        assert source.read_bytes() == target.read_bytes()
        guide_files.append({'source': str(source), 'guide_candidate': str(target), 'sha256': sha(target.read_bytes())})
    save(guide/'provenance.json', {'candidate': candidate, 'files': guide_files,
        'unmodified_actual_cold_boot_PNGs': True, 'no_save_savestate_or_fixtures': True,
        'scope': 'Title and New Game confirmation only;not new battle/declaration scene verification.'})
    files = [Path(__file__), doc, ledger_path, ROM.with_suffix('.manifest.json'), Path('translations/battle_declaration_editorial_release_v1.json'),
        Path('translations/battle_declaration_editorial_manuscript_v3.json'), Path('dk4tool/patch/battle_declaration_editorial.py'),
        Path('scripts/battle_declaration_layout_v996.py'), Path('scripts/prepare_battle_declaration_release_v997.py'),
        Path('scripts/prepare_battle_declaration_release_v997b.py'), Path('scripts/verify_battle_declaration_release_v997.py'),
        Path('scripts/run_battle_declaration_startup_v997.py'), Path('work/analysis/battle_declaration_v997/successor_provenance.json'),
        BUILD/'repack_plan.json', BUILD/'native_copy_proof.json', BUILD/'native_audit/audit.json',
        BUILD/'registration_provenance.json', BUILD/'registered_release_verification.json',
        BUILD/'ordinary_startup_verification.json', BUILD/'newgame_run_plan.json', BUILD/'title_run_plan.json',
        startup_visual, provenance_note, Path(startup['review_sheet']), RETENTION, guide/'provenance.json']
    for mode in ('newgame', 'title'):
        files.append(CAP/f'battle_declaration_v997_{mode}/capture_report.json')
        files += list((CAP/f'battle_declaration_v997_{mode}').glob('frame_*_cold_boot.png'))
    archived = []
    for source in dict.fromkeys(files):
        if source.is_relative_to(CAP):
            relative = Path('actual_captures')/source.relative_to(CAP)
        elif source.is_relative_to(guide):
            relative = Path('guide_provenance')/source.relative_to(guide)
        else:
            relative = source.absolute().relative_to(Path.cwd())
        target = archive/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        assert not target.exists()
        copy2(source, target)
        assert source.read_bytes() == target.read_bytes()
        archived.append({'source': str(source), 'archive': str(target), 'sha256': sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json', {'files': archived, 'all_hashes_verified': True,
        'no_ROM_or_patch_duplicated': True, 'two_unmodified_actual_guide_candidates': guide_files})
    save(ROOT/'final_goal_turn_check.json', {'candidate': candidate, 'all_archived_files_fresh_rehash_pass':
        all(sha(Path(r['archive']).read_bytes()) == r['sha256'] for r in archived),
        'both_guide_PNGs_exact': all(sha(Path(r['source']).read_bytes()) == sha(Path(r['guide_candidate']).read_bytes()) == r['sha256'] for r in guide_files),
        'completed_entries': 1174, 'source_prose_reviewed': 1199, 'new_completion_credit': 0,
        'registered_patch_startup_and_native_proofs_agree': True,
        'retention_preview': str(RETENTION), 'keep217_delete0_no_apply': True,
        'no_live_process_left': True, 'actual_changed_scene_gates_pending': True,
        'goal_status': 'active', 'full_goal_complete': False, 'producer_sha256': sha(Path(__file__).read_bytes())})
    print('V998 checkpoint archived on E:V997 exact combined ROM/patch and eight startup screens pass. Two guide PNGs saved.1174 complete,1199 source/prose;changed prompt scenes pending;goal active.')


if __name__ == '__main__':
    main()
