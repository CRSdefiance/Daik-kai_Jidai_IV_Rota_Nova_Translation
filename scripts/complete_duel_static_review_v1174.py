"""Close20 static duel entries with family gameplay; keep13 escape entries open."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from shutil import copy2
from dk4tool.patch import duel_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.duel_editorial_layout_v1155 import DUEL_IDS, ESCAPE_IDS
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_static_completion_v1174')
FINAL = Path('translations/duel_static_editorial_final_review_v1.json')
DOC = Path('docs/duel_v1174_static_completion.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V1174 Combined V1166 and static duel completion')


def main():
    assert not ROOT.exists() and not FINAL.exists() and not DOC.exists() and not ARCHIVE.exists()
    config_path = Path(owned.CONFIG)
    config = read(config_path)
    manuscript_path = Path(config['manuscript'])
    manuscript = read(manuscript_path)
    release_path = Path('work/analysis/duel_release_v1165/registered_release_verification.json')
    actual_path = Path('work/analysis/duel_terminal_v1173/terminal_gameplay_verification.json')
    startup_path = Path('work/analysis/duel_release_v1165/ordinary_startup_verification.json')
    release, actual, startup = read(release_path), read(actual_path), read(startup_path)
    rom_path = Path(release['candidate'])
    assert sha(rom_path.read_bytes()) == release['candidate_sha256'] == actual['candidate_sha256'] == startup['candidate_sha256']
    assert release['complete_reconstruction_byte_exact']
    assert len(startup['pairs']) == 8 and actual['actual_IDs'] == [1932, 1939, 1945]
    assert len(actual['actual_complete_holds']) == 6 and len(actual['all31_fixture_replays']) == 31
    assert actual['terminal_Sea_View_without_portrait_paper_or_duel_box_visually_reviewed']
    assert actual['source_and_disposable_saves_unchanged']
    rom = NdsImage.open(rom_path)
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    entries = owned.current_entries(common, arm)
    native = read(manuscript['resident_font_proof'])
    assert len(native['cases']) == 1356
    records = []
    for row in manuscript['records']:
        n = row['message_id']
        if n not in DUEL_IDS:
            continue
        assert all(row['review'][g] for g in ('source', 'context', 'localization', 'naturalness', 'formatting'))
        assert entries[n].text.hex() == row['compiled_hex']
        cases = [i for i, case in enumerate(native['cases']) if case['message_ID'] == n]
        assert len(cases) == (168 if n <= 1938 else 1)
        completed = deepcopy(row)
        completed.update(before_reference=row['current_reference'], before_text_hex=row['current_text_hex'],
            current_reference={k: v for k, v in asdict(entries[n]).items() if k != 'text'},
            current_text_hex=entries[n].text.hex(), current_English=entries[n].text.decode('cp932'),
            completed_candidate_reference=str(rom_path), completed_candidate_sha256=release['candidate_sha256'],
            decision='revised-and-integrated' if row['editorial_decision'] == 'revise' else 'retained-and-editorially-reviewed',
            complete_native_font_case_indices=cases, native_font_proof=manuscript['resident_font_proof'],
            native_font_proof_sha256=manuscript['resident_font_proof_sha256'],
            actual_holds=[case for case in actual['actual_complete_holds'] if case['message_ID'] == n],
            all_source_native_copy_font_and_family_actual_gates_pass=True,
            individual_actual_activation_not_claimed_when_actual_holds_empty=True,
            status='complete-with-source-native-and-representative-original-duel-gameplay')
        records.append(completed)
    assert len(records) == 20
    revised = sum(r['editorial_decision'] == 'revise' for r in records)
    assert revised == 13
    ROOT.mkdir(parents=True)
    scope = ('All20 original challenge, acceptance and defeated-opponent alternatives have source/context/prose '
        'review, all1356 distinct complete native font/name cases, scoped loader/ABI checks and exact registered '
        'integration. Actual1932,1939 and1945 have two full native bitmap and RGB holds each in one original '
        'duel. The game naturally produces a victory, capture/loot/cargo flow and normal sea return. The '
        'remaining17 static IDs have family sample evidence, not claimed individual activations. All31 '
        'disclosed fixtures precede the duel and have complete4MiB delta/RNG/identity audits; original and '
        'disposable saves are unchanged. There are no duel-time health/location/message/RNG/outcome edits. '
        'The13 separate portrait-speech escape notices remain incomplete pending a representative original '
        'defeat path. This is not earned progression, a complete route, or hardware verification.')
    save(FINAL, {'format': 'dk4-editorial-final-review-v1', 'family': 'Shared-static-duel1931-1950',
        'records': records, 'native_message_IDs': list(DUEL_IDS), 'source_and_prose_already_counted': True,
        'new_completed_entries': 20, 'new_revised_completed': 13, 'new_retained_completed': 7,
        'candidate': str(rom_path), 'candidate_sha256': release['candidate_sha256'],
        'registered_release': str(release_path), 'registered_release_sha256': sha(release_path.read_bytes()),
        'actual_proof': str(actual_path), 'actual_proof_sha256': sha(actual_path.read_bytes()),
        'actual_verification_scope': scope, 'remaining_escape_IDs': list(ESCAPE_IDS),
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert ledger['records_editorially_completed'] == 1196 and ledger['records_revised_and_integrated'] == 891
    assert ledger['retained_wordings_editorially_completed'] == 305 and ledger['records_with_source_and_prose_pass'] == 1267
    assert set(DUEL_IDS) <= set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    family = {'id': 'Shared-static-duel1931-1950', 'native_message_IDs': list(DUEL_IDS), 'records': records,
        'final_review': str(FINAL), 'documentation': str(DOC), 'actual_verification_scope': scope}
    assert all(item['id'] != family['id'] for item in ledger['completed_editorial_families'])
    ledger['completed_editorial_families'].append(family)
    ledger['coverage_units'].append({'id': family['id'], 'status': 'complete-with-source-native-and-representative-gameplay-evidence',
        'native_message_IDs': list(DUEL_IDS), 'final_review': str(FINAL), 'actual_proof': str(actual_path), 'full_goal_complete': False})
    ledger['records_editorially_completed'] = 1216
    ledger['records_revised_and_integrated'] = 904
    ledger['retained_wordings_editorially_completed'] = 312
    ledger['reviewed_but_incomplete_COMMON_IDs'] = [n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in DUEL_IDS]
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs']) == 51
    drafts = ledger['active_source_prose_drafts']
    drafts['native_message_IDs'] = [n for n in drafts['native_message_IDs'] if n not in DUEL_IDS]
    drafts['manuscripts'] = [str(manuscript_path) if Path(p) == Path('translations/duel_editorial_manuscript_v3.json') else p for p in drafts['manuscripts']]
    drafts['status'] = 'older3-context;successful-shot;15-sighting-remaining-UI;13-escape-original-defeat-path-pending'
    drafts['manuscript_record_subsets_pending'] = {str(manuscript_path): list(ESCAPE_IDS)}
    drafts['note'] = '51 reviewed incomplete COMMON entries are not the entire remaining shared,route,other player prose or raw-source scope.'
    duel = ledger['duel_prose_v1103']
    duel.update(manuscript=str(manuscript_path), completed_entries_added=20, completed_static_IDs=list(DUEL_IDS),
        remaining_escape_IDs=list(ESCAPE_IDS), current_registered_release=str(release_path),
        native_format_approved_record_count=33, actual_static_final_review=str(FINAL),
        actual_original_duel_proof=str(actual_path), actual_observed_static_IDs=[1932, 1939, 1945],
        compiled_formatter_source='scripts/duel_layout_native_v1141.c', compiled_formatter_binary_bytes=1480,
        compiled_formatter_binary_sha256=owned.COMPONENT_SHA,
        compiled_formatter_ISA='work/analysis/duel_native_ISA_v1160b/exact_binary_ISA_and_reproduction.json',
        formatting_status='20-static-complete;13-escape-native-approved-and-integrated-original-defeat-path-pending',
        formatter_next_action='Verify13 portrait escape notices in an original defeat-path family sample, preserving the actual actor/captain IDs and unmodified RNG/outcome code; then continue all remaining shared/route/raw-source editorial coverage.')
    ledger['formatting_watchlist']['duel_compiled_native24x3'].update(status='complete-for20-static-duel-family;13-portrait-escape-actual-and-general-formatting-audit-open',
        current_manuscript=str(manuscript_path), all33_formatting_gates_still_false=False,
        actual_static_proof=str(actual_path), final_static_review=str(FINAL))
    ledger['formatting_watchlist']['latest_registered_preservation'] = {
        'candidate': str(rom_path), 'candidate_sha256': release['candidate_sha256'],
        'user_shop676_677': 'work/analysis/duel_release_v1165/photographed_shop_formatting.json',
        'earlier_actual_shop_capture_reused_no_new_shop_activation_claimed': True,
        'static_duel20_complete_and_escape13_actual_still_open': True}
    ledger['previous_registered_formatting_candidate_before_V1166'] = ledger.get('latest_registered_formatting_candidate')
    ledger['latest_registered_formatting_candidate'] = {'path': str(rom_path), 'sha256': release['candidate_sha256'],
        'profile': release['profile'], 'MESFILE_sha256': release['COMMON_sha256'], 'ARM9_sha256': release['ARM9_sha256'],
        'patch': release['patch'], 'patch_sha256': release['patch_sha256'], 'status': 'experimental;static20-complete;escape13-actual-pending',
        'release_verification': str(release_path), 'original_static_duel_verification': str(actual_path)}
    ledger['previous_native_relocation_reference_before_V1166'] = ledger['current_native_relocation_reference']
    ledger['current_native_relocation_reference'] = {'candidate': str(rom_path), 'COMMON_sha256': release['COMMON_sha256'],
        'ARM9_sha256': release['ARM9_sha256'], 'parser': 'dk4tool.patch.duel_editorial.current_entries',
        'release_config': owned.CONFIG, 'requires_guarded_single8192_cache_policy': True,
        'opaque1484byte_prefix_and_carrier1931_are_owned_and_hash_locked': True,
        'all3635_unselected_strings_and_unowned_payloads_preserved': True,
        'candidate_experimental_remaining_escape_actual_and_broader_goal_pending': True}
    summary = ('V1174 closes the20 static duel paragraphs1931-1950:13 revisions and7 justified retentions. '
        'Source/prose totals stay1267; completed totals rise to1216, comprising904 revised and312 retained. '
        'Registered combined V1166 preserves all471 batches114 accepted layers, all earlier graphics/routes/fonts '
        'and the exact123040-byte staged payload. Its clean-input patch reconstructs byte for byte. Eight no-save '
        'startup/title/New Game frames match V1105 and were visually reviewed. All7336 native copies180 cache '
        'sequences, final53 scope/36 font bindings,1356 full duel and1417 escape font cases pass. One original '
        'duel verifies1932 challenge,1939 acceptance and1945 defeated threat in six complete native font/RGB '
        'holds. Original combat naturally yields HP109/0, then capture,loot,cargo,ordinary dock refusal and '
        'normal sea return. All31 disclosed pre-duel location/positive-health/diplomatic fixtures have complete '
        '4MiB delta audits with RNG,actor IDs and result bytes preserved; none occur during or after the duel. '
        'Source/disposable saves remain exact. Three actual UI captures are saved for the guide on E:. '
        'The13 escape notices are integrated and native-format approved but need an original defeat-path '
        'sample; they receive no completion credit.51 reviewed COMMON entries remain incomplete, alongside '
        'the broader unreviewed shared/routes/raw-source inventory. V1166 remains experimental; canonical '
        'and prior whole-batch scene-verified V997 remain unchanged. User shop676/677 formatting again passes '
        'native wrapping/full fonts in V1166; no fresh shop activation is claimed. All18 plaques and the '
        'separate graphics audit remain unfinished. The full editorial goal remains active.')
    ledger['latest_checkpoint'] = summary
    ledger['goal_status'] = 'active'
    ledger['full_goal_complete'] = False
    ledger['research_checkpoints'].append({'id': 'V1174-static-duel-completion', 'documentation': str(DOC),
        'previous_goal_turn_classification': 'progress:scoped resident native code/fonts and escape memberships verified',
        'this_goal_turn_classification': 'progress:registered combined ROM/exact patch,ordinary cold boot,original duel and transitions,20 completed records',
        'full_goal_complete': False})
    save(ledger_path, ledger)
    DOC.write_text('# V1174: combined V1166 and static duel editorial completion\n\n'+summary+
        '\n\n## Evidence scope\n\n'+scope+
        '\n\n## Candidate\n\n'
        f'- ROM: `{rom_path}`\n- SHA-256: `{release["candidate_sha256"]}`\n'
        f'- Profile: `{release["profile"]}` (experimental)\n- Exact clean-input patch: `{release["patch"]}`\n'
        f'- Patch SHA-256: `{release["patch_sha256"]}`\n'
        '- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, '
        '`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.\n'
        '- Changes from V1105: COMMON blocks20-22/message metadata, original DA28 owned function, '
        'and the existing escape-membership bank/status literal. Other files and allocations remain exact.\n\n'
        'No canonical promotion is authorized. The remaining13 escape messages need original defeat-path '
        'UI/transition evidence. Close-range/Armed Latina UI, successful Lookout shot, COMMON750-752 context, '
        'full route/raw-source inventory and broader formatting audit remain open. The older-record re-audit '
        'still follows the full editorial goal.\n', encoding='utf-8')
    for name in ('docs/translation_progress.md', 'docs/todo.md', 'docs/known_issues.md'):
        with Path(name).open('a', encoding='utf-8') as stream:
            stream.write('\n\n## V1174: static duel editorial completion\n\n'+summary+
                         ' See [V1174 evidence](duel_v1174_static_completion.md).\n')
    # Preserve the active candidate as a research dependency under retention.
    pins_path = Path('translations/rom_retention_pins.json')
    pins = read(pins_path)
    path = str(rom_path.absolute())
    if not any(Path(p['path']) == Path(path) for p in pins):
        pins.append({'path': path, 'reason': 'V1166 current registered source for remaining escape-family gameplay and full editorial review; static20 completed at V1174.'})
        save(pins_path, pins)
    sources = [Path(__file__), FINAL, DOC, ledger_path, manuscript_path, config_path, owned.COMPONENT,
        Path('dk4tool/patch/duel_editorial.py'), rom_path.with_suffix('.manifest.json'), Path(release['patch']), pins_path,
        Path('docs/translation_progress.md'), Path('docs/todo.md'), Path('docs/known_issues.md')]
    for path in Path('scripts').iterdir():
        if path.is_file() and any(f'v{n}' in path.name for n in range(1162, 1175)):
            sources.append(path)
    for folder in ('duel_native_release_v1162', 'duel_cache_copies_v1163', 'duel_final_consumer_v1164',
        'duel_release_v1165', 'duel_contact_v1169_compassAttack8', 'duel_contact_preflight_v1169',
        'duel_contact_observer_v1170', 'duel_actual_holds_v1171', 'duel_actual_holds_v1172', 'duel_terminal_v1173'):
        for path in (Path('work/analysis')/folder).rglob('*'):
            if path.is_file() and path.suffix.lower() != '.nds':
                sources.append(path)
    sources += [Path(actual['terminal_report']), *Path('E:/Rota Nova translations/Guide screenshots/V1166 Duel').glob('*')]
    ARCHIVE.mkdir(parents=True)
    files, seen = [], set()
    external = Path('E:/Rota Nova translations')
    for source in sources:
        source = source.absolute()
        if source in seen or not source.is_file():
            continue
        seen.add(source)
        try:
            relative = source.relative_to(Path.cwd())
        except ValueError:
            relative = Path('External E archive')/source.relative_to(external)
        target = ARCHIVE/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, target)
        digest = sha(source.read_bytes())
        assert sha(target.read_bytes()) == digest
        files.append({'source': str(source), 'archived': str(target), 'sha256': digest})
    save(ARCHIVE/'archive_manifest.json', {'files': files, 'all_hashes_verified': True,
        'ROM_retained_at_registered_E_Generated_out_path_not_duplicated': str(rom_path.absolute()),
        'ROM_sha256': release['candidate_sha256'], 'earlier_native_evidence_archive': 'E:/Rota Nova translations/Editorial review/V1161 Resident duel and escape native verification',
        'new_completed_entries': 20, 'remaining_escape_entries': 13, 'full_goal_complete': False})
    save(ROOT/'checkpoint.json', {'summary': summary, 'final_review': str(FINAL), 'actual_proof': str(actual_path),
        'archive': str(ARCHIVE), 'archive_files': len(files), 'new_completed_entries': 20,
        'records_editorially_completed': 1216, 'records_source_prose_reviewed': 1267,
        'reviewed_incomplete_COMMON_count': 51, 'full_goal_complete': False})
    print(f'V1174:20 static duel entries completed;1216 complete/1267 source-prose reviewed;13 escapes remain open. {len(files)} archive hashes verified.', flush=True)


if __name__ == '__main__':
    main()
