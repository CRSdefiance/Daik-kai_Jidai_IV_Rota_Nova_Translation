"""Register the verified Refit help revisions as a cumulative candidate."""

from inspect import getsource
from pathlib import Path
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha as digest
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import checkpoint_refit_help_replay_20261115 as live
from scripts import register_tavern_influence_20261114 as publisher
from scripts import stage_refit_help_wraps_20261115 as stage
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_release_baseline import files


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-refit-help-wraps-v1-20261115'
ROOT = Path('out/refit_help_wraps_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Refit_Help_Wraps_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_refit_help_wraps_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_refit_help_wraps_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'repository_qa.xml'
NATIVE = stage.ROOT / 'native_verified/native_font_verification.json'
VIEWED_NATIVE = '90c3b4e17779dd9c80e0d3985d24bf13fe377de6ef598d4676480576b1d68b23'
VIEWED_GAMEPLAY = '9b94fa3a35b99448d784ea6c659e493defb601382b97535118748fb4ae8c90c3'
CHECKPOINT = 'Six Shipyard Refit help revisions are registered, with 25 justified retentions.'


def verify(prior, guard):
    storage, review, native, gameplay, startup = map(base.load, (stage.STORED, stage.REVIEW, NATIVE, live.OUTPUT, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == storage['candidate_sha256'] == gameplay['candidate_sha256'] == startup['candidate_sha256']
    assert candidate == native['candidate_sha256']
    predecessor = base.digest(parent.ROM)
    assert predecessor == prior['candidate_sha256'] == storage['previous_sha256'] == review['current_candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256'] == review['clean_sha256']
    assert review['records'] and storage['whole_parent_inverse'] and storage['preserved_entries'] == 3662
    assert base.digest(stage.REVIEW) == storage['manuscript_sha256'] == native['manuscript_sha256']
    sheet, = native['review_sheets']
    assert base.digest(sheet['path']) == sheet['sha256'] == VIEWED_NATIVE
    assert base.digest(gameplay['screenshot']) == gameplay['screenshot_sha256'] == VIEWED_GAMEPLAY
    formatted = {row['message_id']: row for row in native['records']}
    assert formatted.keys() == stage.REVISIONS.keys()
    assert len(gameplay['revised_holds']) == 4 and len(gameplay['exact_transition_and_control_frames']) == 11
    assert startup['cold_boot'] and not startup['savestate'] and startup['complete_deployed_payload_exact']
    assert len(startup['exact_matching_frames']) == 6 and len(startup['original_protected_name_getters']) == 24
    for bundle in (gameplay, startup):
        assert all(base.digest(path) == digest for path, digest in bundle['evidence'].items())
    tests, = ElementTree.parse(QA).iter('testsuite')
    assert tuple(int(tests.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')) == (18, 0, 0, 2)
    old, new = map(base.NdsImage.open, (parent.ROM, stage.ROM))
    before, after = files(old), files(new)
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {stage.COMMON}
    verify_runtime(after[stage.ARM], prior)
    for component, key in ((stage.COMMON, 'target_COMMON_sha256'), (stage.ARM, 'target_ARM9_sha256')):
        assert digest(after[component]) == storage[key]
    checked = bind_registered_story_percent_guard(guard)(files(base.NdsImage.open(stage.CLEAN)), after)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    new.replace_file(stage.COMMON, before[stage.COMMON])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    for row in review['records']:
        n = row['message_id']
        if n in formatted:
            proof = formatted[n]
            assert proof['complete_independent_font_plane_equal'] and proof['text_and_pixel_guards_and_ABI_preserved']
            assert proof['all_body_rows_start_at_x0_and_fit_first60_rows']
            assert proof['lines'] == row['generated_lines'] and proof['compiled_hex'] == row['staged_hex'] + '00'
            assert base.digest(proof['native_preview']) == proof['native_preview_sha256']
            row['formatting_evidence'] = 'Fresh complete native plane at the current +1 pixel font origin.'
        else:
            assert row['exact_current_hex'] == row['staged_hex']
            row['formatting_evidence'] = 'Byte-exact current body and regenerated layout, with identical ARM9 and help consumer.'
        row['review']['formatting'] = True
        row['registered_reference'] = row['staged_reference'] | dict(exact_stored_hex=row['staged_hex'],
                                                                       candidate_sha256=candidate)
    return storage, seal_review(review, candidate, native, gameplay, checked)


def seal_review(review, candidate, native, gameplay, checked):
    document = review | dict(review_gates=list(stage.GATES), candidate_sha256=candidate,
        checked_story_format_guard=checked, native_font=native, observed_gameplay=gameplay,
        direct_visual_review_complete=True, new_editorial_credit=0)
    validate_natural_dialogue_batch(document)
    return document


def update_ledger(ledger, release, sha, checkpoint):
    reconciled = ledger['pending_shared_consumer_checkpoint_20261114']
    assert reconciled['remaining_total'] == 276
    assert reconciled['candidate_sha256'] == release['predecessor']['candidate_sha256']
    assert not set(reconciled['remaining_legacy_keys']).intersection(stage.REVISIONS)
    reconciled['candidate_sha256'] = sha
    ledger['current_integrated_candidate'].update(path=str(ROM), sha256=sha, profile=PROFILE, patch=str(PATCH),
        patch_sha256=release['patch_sha256'], manifest=str(MANIFEST), manifest_sha256=release['manifest_sha256'],
        MESFILE_sha256=release['target_COMMON_sha256'], registered_release_verification=str(RELEASE))
    ledger['latest_checkpoint'] = checkpoint
    ledger['refit_help_wraps_20261115'] = dict(review=str(REVIEW), release=str(RELEASE),
        revised_existing_keys=sorted(stage.REVISIONS), retained_existing_keys=sorted(stage.RETENTIONS),
        new_dialogue_credit=0, remaining_mapped_shared_records=276)


def main():
    source = getsource(publisher.main)
    ledger_lo = source.index('    ledger["current_integrated_candidate"].update(')
    ledger_hi = source.index('    write_pending(ledger_tmp,encode_ledger(ledger))', ledger_lo)
    source = source[:ledger_lo] + '    update_ledger(ledger, release, sha, checkpoint)\n' + source[ledger_hi:]
    doc_lo = source.index('    base.replace_checked(DOC,f"""')
    doc_hi = source.index('""".encode())', doc_lo) + len('""".encode())')
    doc = '''    base.replace_checked(DOC, f"""# Shipyard Refit help wraps

The [registered review](../{REVIEW.as_posix()}) covers all 31 Refit help panels. It records six revisions and 25 individual retentions from the clean Japanese. The new spritsail and topsail instructions keep “square sail performance” together. The ram describes striking an enemy ship’s side, and the room instructions keep the original limits of four boarding rooms, four gun decks, and five cargo holds.

All six revised panels passed complete native glyph, bounds, allocation, and single-page checks. The [native sheet](../{(VERIFY / 'native_review_sheet_1.png').as_posix()}) was visually reviewed. The [Copenhagen replay](../{(VERIFY / 'refit_before_after.png').as_posix()}) verified four changed holds covering the topsail and cargo-hold panels. Eleven surrounding two-screen frames, including the exit, matched the parent. The replay used an existing copied five-ship test save. The other four revised panels received controlled native checks. Hardware testing remains open.

The cumulative startup matched six frame holds and 24 protected name getters. Sixteen targeted tests passed. Two historical tests skipped because their ROM fixtures were unavailable. The [registered ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers and the ASCII right bound. All 31 entries had existing credit. The ledger remains at 27,700 credited reviews, with 276 mapped shared records remaining.
""".encode())'''
    source = source[:doc_lo] + doc + source[doc_hi:]
    replacements = {
        '== 27699 and not ledger': '== 27700 and not ledger',
        'len(manifest["batches"]) == 810 and len(manifest["checks"]) == 145':
            'len(manifest["batches"]) == 813 and len(manifest["checks"]) == 148',
        'release_stack.tavern_influence.pending.json': 'release_stack.refit_help_wraps.pending.json',
        'editorial_review_current.tavern_influence.pending.json': 'editorial_review_current.refit_help_wraps.pending.json',
        'release_stack_before_tavern_influence.json': 'release_stack_before_refit_help_wraps.json',
        'for p in (stage.STORED,live.OUT,STARTUP,QA,TOWNS):':
            'for p in (stage.STORED, live.OUTPUT, STARTUP, QA, NATIVE, '
            'Path(base.load(NATIVE)["review_sheets"][0]["path"]), Path(base.load(live.OUTPUT)["screenshot"])):',
        'verified_about_extras_predecessor=lineage, tavern_influence_release':
            'verified_name_or_words_confirmation_predecessor=lineage, refit_help_wraps_release',
        'Natural barkeep wording and verified native display for COMMON 821.': 'Source-reviewed Refit help and verified native wrapping.',
        'registered_tavern_influence_and_complete_parent_inverse': 'registered_refit_help_wraps_and_complete_parent_inverse',
        '    if "COMMON_MESSAGE_821" not in ids:\n        ids.append("COMMON_MESSAGE_821")':
            '    ids.extend(key for n in sorted(stage.REVISIONS) if (key := f"COMMON_MESSAGE_{n}") not in ids)',
        'tavern_influence_registered_successor_pipeline': 'refit_help_wraps_registered_successor_pipeline',
        'staged["byte_allocation"]': 'staged["allocations"]',
        'registered_manifest_entries=811,passing_release_checks=146,repository_tests=26,legacy_fixture_tests_skipped=2':
            'registered_manifest_entries=814,passing_release_checks=149,repository_tests=16,legacy_fixture_tests_skipped=2',
        'prose_revisions=1,justified_retentions=11,reviewed_UI_labels=0':
            'prose_revisions=6,justified_retentions=25,text_display_revisions=6,reviewed_UI_labels=0',
        'observed_revised_rumors=1,retained_observed_holds=13,\n            offline_role_and_name_variants=17':
            'observed_revised_refit_holds=4,exact_surrounding_holds=11,\n            offline_complete_refit_planes=6',
        'checkpoint = "The Istanbul barkeep’s influence rumor is registered, with current coverage in three towns."':
            'checkpoint = CHECKPOINT',
        'digest = parent.source.current.assets.edit.digest': 'digest = DIGEST',
        '# Tavern Influence test candidate': '# Shipyard Refit Help test candidate',
        'includes the revised Istanbul Tavern rumor': 'includes the revised Shipyard Refit help',
        'Preserve Tavern rumor release and verified replay.': 'Preserve Refit help release and verified replay.',
        '# Current editorial checkpoint - 2026-11-14': '# Current editorial checkpoint - 2026-11-15',
        '811 entries, 114 accepted layers, 146 checks.': '814 entries, 114 accepted layers, 149 checks.',
    }
    env = vars(publisher) | globals() | dict(DIGEST=digest)
    exec(compile(checked_text(source, replacements), __file__ + '::cumulative-registration', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
