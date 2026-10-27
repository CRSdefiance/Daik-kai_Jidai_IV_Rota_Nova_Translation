"""Close the source-reviewed 50-entry batch; keep the full editorial goal active."""

import shutil
from collections import Counter
from dataclasses import asdict
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch import shared_dialogue_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.register_shared_metadata_v783 import ROOT, CONFIG, MANUSCRIPT
from scripts.verify_shared_metadata_v783 import ROM
from scripts.verify_village_wrap_v608 import read, save

SOURCE = Path('work/analysis/shared_integration_v782')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/shared_dialogue_v783_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V783 Shared dialogue completed batch')
SHOTS = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V783 Shared dialogue')


def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert sha(source.read_bytes()) == sha(target.read_bytes())


def main():
    manuscript, config = read(MANUSCRIPT), read(CONFIG)
    validate_natural_dialogue_batch(manuscript)
    assert [r['message_id'] for r in manuscript['records']] == list(range(1020, 1070))
    assert Counter(r['decision'] for r in manuscript['records']) == {'revise': 34, 'retain': 16}
    assert all(all(r['review'].values()) for r in manuscript['records'])
    for p, h in config['dependencies'].items():
        assert sha(Path(p).read_bytes()) == h, p
    assert sha(MANUSCRIPT.read_bytes()) == config['manuscript_sha256']
    replay = read(ROOT/'verification.json')
    digest = sha(ROM.read_bytes())
    assert digest == replay['candidate_sha256'] == sha(Path('out/all_routes_combined_v782_candidate.nds').read_bytes())
    assert replay['whole_ROM_identical_to_V782'] and replay['registered_speaker_context_replay_complete']
    assert replay['byte_exact_clean_input_reconstruction']
    assert sha(ROM.with_suffix('.xdelta').read_bytes()) == replay['patch_sha256']
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['profile'] == 'all-routes-unified-v783' and manifest['candidate_sha256'] == digest
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert all(manifest['checks'].values()) and len(manifest['batches']) == 470
    release = read(SOURCE/'registered_verification.json')
    assert release['candidate_sha256'] == digest and all(release['negative_gates'].values())
    assert release['all470_batches114_accepted_layers_and_graphics_retained'] and release['all7336_complete_native_copies']
    assert release['all3618_other_strings_exact'] and release['only_COMMON_ARM9_change_from_V780']
    layout = read(SOURCE/'production_layout/verification.json')
    assert layout['native_layouts'] == 857 and not layout['findings']
    assert len(layout['all83_complete_native_font_planes_exact_to_visually_reviewed_images']) == 83
    assert read(SOURCE/'full_entry_layout_verification.json')['all857_original_target_trampoline_and_private_dispatch_outputs_exact']
    boot = read(SOURCE/'newgame_regression.json')
    assert boot['candidate_sha256'] == digest and boot['all_pixels_exact'] and boot['no_savestate_or_test_fixture']
    assert len(boot['whole_screen_frame_pairs']) == 7
    watch = read('work/analysis/dialogue_formatting_user_recheck_v782/COMMON676_677.json')
    assert watch['sha256'] == digest and all(p['exact_repaired_text_and_native_formatting_preserved'] for p in watch['entries'])
    paths = [SOURCE/p for p in ('recruit_capacity_gameplay_verification.json', 'recruit_shortfall_gameplay_verification.json',
             'warning_gameplay_verification.json', 'information_gameplay_verification.json',
             'village_casual_gameplay_verification.json', 'village_formal_gameplay_verification.json')]
    paths += [ROOT/p for p in ('fleet_gameplay_verification.json', 'private_barmaid_gameplay_verification.json')]
    scenarios = [read(p) for p in paths]
    assert all(p['candidate_sha256'] == digest for p in scenarios)
    holds = [h for p in scenarios for h in p['holds']]
    ids = sorted({h['message_id'] for h in holds})
    assert ids == [1020, 1022, 1028, 1029, 1032, 1034, 1035, 1042, 1065] and len(holds) == 17
    assert all(h['complete_independent_font_and_blank_paper_exact'] and h['all_other_pixels_exact'] for h in holds)
    controls = sum(len(p['whole_screen_controls']) for p in scenarios)
    states = sum(len(p['paired_state_model_object_task_frames']) for p in scenarios)
    phases = sum(len(p['original_whole_screen_blink_phase_controls']) for p in scenarios)
    assert (controls, states, phases) == (410, 405, 2)
    assert scenarios[-1]['private_family_actual_sample_complete'] and scenarios[-1]['no_location_relationship_rng_or_dialogue_injection']
    assert scenarios[-1]['gift_fixture_receipt_reproduced_from_prefixture_RAM_in_both_ROMs']
    assert scenarios[-2]['fixture_receipt_reproduced_from_prefixture_RAM_in_both_ROMs']
    for p, h in replay['protected_files_unchanged'].items():
        assert sha(Path(p).read_bytes()) == h, p
    donor = Path('E:/Rota Nova translations/Saves/maria-seoul-rested-v514.dsv')
    assert sha(donor.read_bytes()) == '942c74828a7b7396f7567ca2d405ddc4cdd329e4837f591777d35ee458794b0f'
    rom = NdsImage.open(ROM)
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    entries = common_message_entries(common, arm, clean=False)
    clean = NdsImage.open('work/clean.nds')
    japanese = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    for row in manuscript['records']:
        n = row['message_id']
        assert entries[n].text == owned.compile_text(row)
        assert japanese[n].text.hex() == row['source_hex']
        if 1035 <= n <= 1048:
            assert 'First Mate' in row['speaker'] and 'fallback' in row['speaker']
    native_map = ROOT/'complete_native_message_map_v783.json'
    save(native_map, {'candidate_sha256': digest, 'COMMON_sha256': sha(common), 'ARM9_sha256': sha(arm),
                     'inventory_only_not_editorial_coverage': True,
                     'entries': [{**asdict(e), 'text': None, 'text_hex': e.text.hex()} for e in entries]})
    game = {'candidate_sha256': digest, 'scenarios': scenarios,
            'scenario_proofs': [{'path': str(p), 'sha256': sha(p.read_bytes())} for p in paths],
            'actual_IDs': ids, 'actual_complete_holds': len(holds), 'strict_whole_screen_controls': controls,
            'whole_original_blink_phase_controls': phases, 'paired_state_model_object_task_frames': states,
            'newgame_whole_screen_pairs': 7, 'all_required_consumer_families_sampled': True,
            'other41_entries_have_source_native_matrix_font_and_family_sampling_not_individual_activation': True,
            'no_full_route_or_physical_hardware_completion_claim': True, 'full_goal_complete': False}
    save(ROOT/'shared_batch_gameplay_verification.json', game)
    ledger = read(LEDGER)
    old_ids = [n for f in ledger['completed_editorial_families'] for n in f['native_message_IDs']]
    assert len(old_ids) == len(set(old_ids)) == ledger['records_editorially_completed']
    assert ledger['records_editorially_completed'] in (367, 417)
    assert ledger['records_with_source_and_prose_pass'] == 420
    if ledger['records_editorially_completed'] == 367:
        assert set(range(1020, 1070)).isdisjoint(old_ids)
        save(ROOT/'editorial_ledger_before_batch_closure.json', ledger)
    else:
        assert (ROOT/'editorial_ledger_before_batch_closure.json').exists()
    family = 'Shared-warning-village-fleet-recruitment-and-private-barmaid1020-1069'
    records = [{'message_id': r['message_id'],
                'decision': 'revised-and-integrated' if r['decision'] == 'revise' else 'retain-wording',
                'manuscript': str(MANUSCRIPT), 'source_native_context_and_complete_font_verified': True,
                'ordinary_actual_display_verified': False, 'actual_display_with_disclosed_fixture': r['message_id'] in ids,
                'actual_display_scope': 'Nine IDs represent all required original consumer families in seventeen complete holds;the other41 have full source/native/font coverage and family sampling,not individual activation.',
                'source_native_arguments': r['source_native_arguments'],
                'English_argument_source_indices': r['English_argument_source_indices'],
                'gameplay_evidence': str(ROOT/'shared_batch_gameplay_verification.json')} for r in manuscript['records']]
    if not any(f['id'] == family for f in ledger['completed_editorial_families']):
        ledger['completed_editorial_families'].append({'id': family, 'native_message_IDs': list(range(1020, 1070)), 'records': records})
    if family not in ledger['coverage_units'][0]['completed_families']:
        ledger['coverage_units'][0]['completed_families'].append(family)
    latest = {'path': str(ROM), 'sha256': digest, 'profile': manifest['profile'],
              'MESFILE_sha256': sha(common), 'ARM9_sha256': sha(arm), 'patch_sha256': replay['patch_sha256'],
              'manifest': str(ROM.with_suffix('.manifest.json')), 'status': 'experimental', 'details': str(DOC),
              'supplemental_verification': str(ROOT/'shared_batch_gameplay_verification.json'),
              'remaining_in_this_registered_batch': 'All50 entries reviewed and verified by full native coverage and actual consumer-family samples. Wider shared text,routes,other prose and separate graphics audit remain unfinished.',
              'full_goal_complete': False}
    ledger.update({'records_editorially_completed': 417, 'records_revised_and_integrated': 293,
                   'retained_wordings_editorially_completed': 124, 'current_integrated_candidate': latest})
    ledger['active_source_prose_drafts'] = {'native_message_IDs': [750, 751, 752],
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],
        'status': '750-752-context-unmapped', 'note': 'Original caller mapping remains required before native formatting and integration approval.'}
    historical = ledger.pop('pending_integrated_candidate', None)
    if historical:
        ledger['shared_v783_historical_partial_checkpoint'] = dict(historical, superseded_by=str(DOC), historical_record=True)
    if 'native_relocation_reference_before_V783' not in ledger:
        ledger['native_relocation_reference_before_V783'] = ledger['current_native_relocation_reference']
    ledger['current_native_relocation_reference'] = {'profile': manifest['profile'], 'candidate_sha256': digest,
        'complete3668_native_message_map': str(native_map), 'map_sha256': sha(native_map.read_bytes()),
        'inherited7336_native_copy_proof': str(SOURCE/'registered_verification.json'),
        'historical_manuscript_reference_offsets_are_pinned_to_their_own_input_builds': True}
    ledger['coverage_units'][0]['next'] = 'Review COMMON1070 onward and resolve original contexts for750-752. Continue wider shared text,all route scenes and other player-facing prose. Preserve separate graphics audit and older-record follow-up.'
    summary = ('V783 completes50 shared entries:34 revised/16 retained. Overall417 complete(293 revised/124 retained),420 source/prose and three drafts750-752. '
               '857 production layouts,83 fonts,7336 complete copies,exact clean patch,seventeen actual holds across nine IDs,410 strict screens,two complete original blink controls,405 state/model/object/task pairs and seven ordinary New Game pairs pass. '
               'Original gift/relationship and financial outcomes,source-coordinate buffer,full names/counts and normal returns are verified. '
               'First Mate speaker-context erratum is registered;whole ROM equals V782. Wider shared/routes/prose and separate graphics audit remain open.')
    ledger['latest_checkpoint'] = summary
    checkpoint = {'id': 'V783-shared50-integrated-and-gameplay-verified', 'documentation': str(DOC),
                  'new_editorially_completed': 50, 'revised': 34, 'retained': 16, 'manuscript': str(MANUSCRIPT),
                  'evidence': str(ROOT/'shared_batch_gameplay_verification.json'), 'new_ROM_bytes': False,
                  'experimental': True, 'full_goal_complete': False}
    if not any(p['id'] == checkpoint['id'] for p in ledger['research_checkpoints']):
        ledger['research_checkpoints'].append(checkpoint)
    completed = [n for f in ledger['completed_editorial_families'] for n in f['native_message_IDs']]
    assert len(completed) == len(set(completed)) == 417
    assert ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed'] == 417
    save(LEDGER, ledger)
    save('out/editorial_review_latest.json', latest)
    DOC.write_text('''# V783: fifty shared dialogue entries completed

COMMON1020-1069 complete this editorial batch:34 revisions and16 justified retained
wordings. Overall417 entries are complete(293 revised/124 retained),420 have source/
prose review, and three drafts750-752 still need original caller mapping. The full
editorial goal remains active. COMMON1070 onward, every route and remaining prose
still need review. The separate graphics audit, including18 plaques, remains open.

## English and original meaning

All50 final Japanese/English pairs were reviewed again before closure. Warnings
preserve the source strength and speaker distinctions. Village rumors distinguish
coordinates from names, and fleet rumors distinguish anchorage from destination.
Recruitment keeps required crew shortfall separate from remaining cabin capacity,
with number-neutral wording. Personal topics preserve character opinions, family
facts, wishes and teasing without inventing death, weddings, relationships or pet
sex. Natural existing wording is retained. All records follow natural-dialogue-v2,
with individual source/context/localization/naturalness/formatting review gates.

The corrected V3 manuscript identifies recruitment speech as the original role1
First Mate provider, with native officer fallback. Frozen V2's Barkeep description
was wrong; its historical inputs remain unchanged. V783 explicitly registers V3,
and every ROM byte equals the fully registered V782 candidate. The complete stack
retains470 batches,114 accepted layers and all earlier graphics. No section,BSS,
cache,arena or123040-byte staged payload grows. Source/canonical inputs remain exact.

857 production/native-dispatch layouts,83 independent font planes,7336 complete
warm/cold native copies and12 rejection gates pass. All3618 other visible strings,
opaque1854/1865 payloads and13 other blocks are preserved. The clean-input patch
reconstructs every ROM byte. A fresh current3668-entry message map replaces the
ledger's stale V753 current-map pointer; historical source offsets stay pinned to
their own input builds. This map is inventory, not extra editorial-review credit.

## Targeted actual gameplay

Seventeen complete holds cover nine IDs and all required original consumer families:
1020 missing information;1022 low-success warning;1028/1029 both village styles;
1032/1034 unidentified destination/anchorage;1035 crew shortfall;1042 spare capacity;
and1065 private barmaid conversation. There are410 strict whole-screen controls,
two whole-screen original blink-phase controls,405 paired state/model/object/task
snapshots and seven ordinary cold-boot/New Game comparisons. Independent complete
native font and blank-paper masks prove full leading/trailing letters,substitutions,
visible margins and bounds in each sampled hold. Normal dismissals/returns pass.
The other41 entries have complete source/native/font coverage and family sampling,
not individual actual activations. These are not full-route or hardware tests.

Reika's private topic appears at32000 in paired39200-frame Seoul cold boots. Only
the disclosed three-byte gift acquisition fixture is used,through the original
inventory methods. No location,relationship,RNG or dialogue result is injected.
The source introduction advances relationship0 to1. The gift response at26000 is
still pending; closing it advances to2 and consumes Embroidered Carpet143 normally.
Four post-gift drinks use the original5+10 coin charges:cash38711 to38651. Original
chance selection chooses1065. Its four rows are visually reviewed and match the
complete independent game-font plane. Ninety-three other whole screens and91 state/
model/object/task pairs match; town return at39200 is normal. Cached1065 at32400
shows a menu and receives no second text-hold credit. No job is created.

Two early input-pause probes ended with EOF before any fixture or dialogue testing.
They are terminal failures and receive no coverage. The final interactive runs
complete normally. An initial verifier incorrectly expected stage0 before the gift
and stage2 while its response was still displayed; original snapshots show the
source-ordered0/1/1/2 progression. The final verifier checks those actual transitions.
The earlier-run wallet value was not reused; current source costs are checked.

The user's676/677 shop formatting repair remains exact by whole-ROM identity to
its V782 byte/native-wrap proof. Its earlier V747 actual screenshot remains the
gameplay reference; no fresh V783 shop activation is claimed. Alignment,internal
gaps,complete words/letters,bounds,pagination and dismissal remain ongoing checks.

## Artifacts and remaining scope

Experimental registered candidate:out/all_routes_combined_v783_candidate.nds.
SHA256:9f55817772d2b1e940462f69103536654f0cbedbe959fb42670fc601f2d6e31d.
Profile:all-routes-unified-v783. Canonical base is the unchanged
out/raphael_natural_v2_accepted_base.nds,
SHA256:3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe.
Only COMMON/MESFILE.DK4 and ARM9 differ from V780. All files equal V782.
Patch:out/all_routes_combined_v783_candidate.xdelta,
SHA256:9a23ef0e69dea7a460e48c35e9278936344778d20b93cb1161441f2c56014b7f.
Clean input SHA256:f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d.

ROM,patch,archive and test-fixture screenshots are on E:/Rota Nova translations.
Original saves and all frozen dependencies stay exact. Test images are not promoted
as finished guide screenshots. No canonical promotion,commit or GitHub push occurs.
The wider shared/routes/prose review,750-752 context mapping,unresolved graphics,
Online-body exclusion,preserved brown marks and older-record follow-up remain intact.
''', encoding='utf-8')
    for file in ('docs/todo.md', 'docs/known_issues.md', 'docs/translation_progress.md'):
        path = Path(file)
        text = path.read_text(encoding='utf-8')
        heading = '## V783: fifty shared dialogue entries integrated and verified'
        if heading not in text:
            path.write_text(text+'\n\n'+heading+'\n\n'+summary+' See [V783 completed shared batch](shared_dialogue_v783_checkpoint.md).\n', encoding='utf-8')
    save(ROOT/'completed_shared_batch_checkpoint.json', {**checkpoint, 'candidate': latest,
        'protected_files_unchanged': replay['protected_files_unchanged'],
        'previous_goal_turn_classification': 'Progress: information/village/fleet actual samples and registered metadata replay. This turn finishes private sample and closes50 entries.',
        'producer_sha256': sha(Path(__file__).read_bytes())})
    for h in scenarios[-1]['holds']:
        copy(Path(h['capture']['path']), SHOTS/f'ID{h["message_id"]}_{h["frame"]}_V783_VERIFIED_TEST.png')
    for p in paths:
        copy(p, ARCHIVE/'evidence'/p.name)
    for p in (CONFIG, MANUSCRIPT, LEDGER, DOC, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
              Path('translations/release_stack.json'), Path('out/editorial_review_latest.json')):
        copy(p, ARCHIVE/'registered_artifacts'/p.name)
    for p in (ROOT/'shared_batch_gameplay_verification.json', ROOT/'complete_native_message_map_v783.json',
              ROOT/'completed_shared_batch_checkpoint.json', ROOT/'verification.json',
              ROOT/'effective_private_barmaid_gameplay_verifier.py', ROOT/'private_gift_fixture_preflight.json'):
        copy(p, ARCHIVE/'evidence'/p.name)
    for name in ('native_barmaid_gift_fixture_v783.py', 'run_private_barmaid_capture_v783.py',
                 'verify_private_barmaid_gameplay_v783.py', 'finalize_shared_editorial_v783.py'):
        copy(Path('scripts')/name, ARCHIVE/'scripts'/name)
    for p in scenarios[-1]['capture_reports']:
        path = Path(p)
        copy(path, ARCHIVE/'capture_reports'/path.parent.name/path.name)
        copy(path.parent/'navigation_command_journal.json', ARCHIVE/'capture_reports'/path.parent.name/'navigation_command_journal.json')
    for h in scenarios[-1]['holds']:
        p = SHOTS/f'ID{h["message_id"]}_{h["frame"]}_V783_VERIFIED_TEST.png'
        copy(p, ARCHIVE/'fixture_screenshots'/p.name)
    save(ROOT/'completed_batch_archive_receipt.json', {'archive': str(ARCHIVE), 'every_copy_SHA256_verified': True,
        'completed_this_batch': 50, 'completed_total': 417, 'full_goal_complete': False})
    print('V783 batch closed:50 entries(34 revised/16 retained);417 complete,420 source/prose,three drafts. Full editorial goal and graphics audit remain open.', flush=True)


if __name__ == '__main__':
    main()
