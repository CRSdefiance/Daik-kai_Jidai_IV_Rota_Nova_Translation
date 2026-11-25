"""Register the item-advice prose and phrase wraps after native and emulator checks."""

from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_sailing_help_20261120 as startup_release
from scripts import register_shore_loss_digits_20261121 as parent
from scripts import replay_item_advice_phrase_wraps_20261121 as live
from scripts import stage_item_advice_phrase_wraps_20261121 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch, portrait = parent.base, parent.batch, stage.portrait
PROFILE = 'all-routes-item-advice-phrase-wraps-v1-20261121'
ROOT = Path('out/item_advice_phrase_wraps_registered_20261121_v1')
ROM = ROOT / 'Translation_DS_Item_Advice_Wraps_20261121_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261121_item_advice_phrase_wraps_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_item_advice_phrase_wraps_registered_20261121.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'qa.xml'
STARTUP_CAPTURE = stage.ROOT / 'startup/capture/capture_report.json'
CHECKPOINT = 'Reviewed 49 item-advice replies, revised 18 pages, and verified two of the revised replies in Lisbon.'
PENDING = parent.PENDING


def verify(registry, previous, viewed):
    stored, actual = map(base.load, (stage.PROOF, live.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == actual['candidate_sha256']
    assert stored['parent_sha256'] == previous['candidate_sha256'] == base.digest(parent.ROM)
    assert stored['parent_inverse'] and stored['clean_reconstruction_exact']
    assert stored['patch_sha256'] == base.digest(stage.PATCH)
    assert stage.REBUILT.read_bytes() == stage.ROM.read_bytes()
    assert viewed == {s['path']: s['sha256'] for s in [*stored['sheets'], actual['sheet']]}
    assert all(base.digest(p) == v for p, v in (viewed | actual['evidence'] | stored['source_receipts']).items())
    assert actual['actual_emulator'] and actual['original_Advice_button'] and actual['original_item_views_and_town_return']
    assert not actual['hardware'] and not actual['natural_inventory_acquisition']
    assert [r['message_ID'] for r in actual['live_items'] if r['revised']] == [3147, 3171]
    assert all(r['complete_body_ink'] and r['return_to_identical_item'] for r in actual['live_items'])
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [17, 0, 0, 0]
    clean, old, image = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    assert base.digest(stage.CLEAN) == previous['clean_input_sha256'] == stored['clean_input_sha256']
    before, after = map(batch.files, (old, image))
    assert before.keys() == after.keys()
    assert {key for key in before if before[key] != after[key]} == {stage.COMMON}
    arm = after[stage.ARM]
    assert batch.digest(arm) == previous['target_ARM9_sha256'] == stored['target_ARM9_sha256']
    assert batch.digest(after[stage.COMMON]) == stored['target_COMMON_sha256']
    image.replace_file(stage.COMMON, before[stage.COMMON])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    directory = batch.digest(arm[portrait.DIRECTORY_OFFSET:portrait.TABLE_OFFSET])
    old_rows, now_rows = [portrait.owned_entries(files[stage.COMMON], arm, directory) for files in (before, after)]
    assert len(old_rows) == len(now_rows) == 3668
    assert {a.message_id for a, b in zip(old_rows, now_rows, strict=True) if a.text != b.text} == stage.EDITS.keys()
    pending = base.load(PENDING)['records']
    assert len(pending) == stored['unchanged_pending_records'] == 276
    shifts = {}
    for row in pending:
        n = row['message_ID']
        old_ref = row['current_reference']
        new_ref = portrait.reference(now_rows[n])
        assert old_ref == portrait.reference(old_rows[n])
        assert old_ref | {'record_index': new_ref['record_index']} == new_ref
        assert now_rows[n].text.hex() == row['current_hex']
        if new_ref != old_ref:
            shifts[str(n)] = dict(before=old_ref, after=new_ref)
    assert shifts == stored['shifted_pending_record_indices']
    guards = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guards)(batch.files(clean), after)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    starter = startup_release.env['startup_check'].startup_proof
    FunctionType(starter.__code__, starter.__globals__ | {'STARTUP': STARTUP, 'STARTUP_CAPTURE': STARTUP_CAPTURE})(
        previous, candidate, arm)

    records = stored['records']
    assert len(records) == 49 and sum(r['decision'] == 'revision' for r in records) == 17
    assert {r['message_ID'] for r in records if r['decision'] == 'wrap revision'} == {3169}
    assert {r['message_ID'] for r in records if r['decision'] == 'retention'} == stage.RETAINED.keys()
    selectors = stored['original_selector_cases']
    assert len(selectors['offline_native_selector_cases']) == 294 and len(selectors['branches']) == 6
    observed = {r['message_ID'] for r in actual['live_items']}
    for row in records:
        n = row['message_ID']
        assert len(row['adviser_proofs']) == 2 and row['expected_pages'] == 1
        assert now_rows[n].text.hex() == row['staged_hex']
        assert portrait.reference(now_rows[n]) == row['staged_reference']
        row['registered_reference'] = row['staged_reference'] | {'candidate_sha256': candidate}
        row['gameplay_observed'] = n in observed
    draft = dict(translation_policy=stored['translation_policy'], target_locale=stored['target_locale'],
                 encoder=stored['encoder'], review_gates=stored['review_gates'], records=records,
                 candidate_sha256=candidate, parent_sha256=previous['candidate_sha256'],
                 checked_story_format_guard=controls, unchanged_pending_payloads_and_native_locations=276,
                 shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'],
                 allocation=stored['allocation'], pending_source_receipt_sha256=base.digest(PENDING),
                 shifted_pending_record_indices=shifts, focused_replay=actual, visual_review_receipt=viewed, new_contextual_credit=0)
    validate_natural_dialogue_batch(draft)
    return stored, draft, {stage.COMMON: stored['target_COMMON_sha256']}


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index('    DOC.write_text'):template.index('    prefix =')]
old_ids = template[template.index('    row, = draft["records"]'):template.index('    manifest["shore_loss_digits_pipeline"]')]
program = checked_text(template, {
    'len(manifest["batches"]) == 957 and len(manifest["checks"]) == 292':
        'len(manifest["batches"]) == 958 and len(manifest["checks"]) == 293',
    'stage.PROOF, STARTUP, QA, live.NATIVE, live.LIVE, args.visual_review,': 'stage.PROOF, STARTUP, QA, live.PROOF, args.visual_review,',
    'release_stack_before_shore_loss_digits.json': 'release_stack_before_item_advice_phrase_wraps.json',
    'release_stack_with_shore_loss_digits.json': 'release_stack_with_item_advice_phrase_wraps.json',
    'verified_shore_predecessor=predecessor, shore_loss_digits_release=str(REVIEW)':
        'verified_shore_loss_predecessor=predecessor, item_advice_phrase_wraps_release=str(REVIEW)',
    'registered_shore_loss_digits_and_complete_parent_inverse': 'registered_item_advice_phrase_wraps_and_complete_parent_inverse',
    'manifest["shore_loss_digits_pipeline"]': 'manifest["item_advice_phrase_wraps_pipeline"]',
    old_ids: '''    for row in draft["records"]:
        key, file = row["id"], row["file_path"]
        assert (file, key) in credited
        ids = manifest["changed_records"][file]
        if row["decision"] != "retention" and key not in ids:
            ids.append(key)
''',
    'base.digest(live.LIVE)': 'base.digest(live.PROOF)',
    'owned_digit_call=stored["call"], target_ARM9_sha256=archives[stage.ARM]':
        'owned_message_IDs=sorted(stage.EDITS), target_COMMON_sha256=archives[stage.COMMON]',
    'changed_components=1, target_ARM9_sha256=archives[stage.ARM]':
        'changed_components=1, target_COMMON_sha256=archives[stage.COMMON]',
    'previously_localized_records=1, new_contextual_records=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1':
        'previously_localized_records=49, new_contextual_records=0, prose_revisions=17, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=31',
    'name_label_revisions=0, text_display_revisions=1, pagination_fixes=0':
        'name_label_revisions=0, text_display_revisions=0, pagination_fixes=0',
    'paired_search_crew_loss=True, regular_digits_observed=True, normal_sailing_return=True, variant_selector_restored=True':
        'focused_lisbon_items=3, revised_replies_observed=2, original_items_and_town_return=True',
    'ledger["shore_loss_digits_20261121"]': 'ledger["item_advice_phrase_wraps_20261121"]',
    'prior_records_reviewed=1, actual_gameplay_records=1, new_contextual_credit=0,\n        prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1, text_display_revisions=1':
        'prior_records_reviewed=49, actual_gameplay_records=3, new_contextual_credit=0,\n        prose_revisions=17, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=31, text_display_revisions=0',
    'Preserve the Search sailor-loss candidate or reconstruction': 'Preserve the revised item-advice candidate or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Item-advice phrase wrap testing candidate

The [testing ROM](../../{ROM.as_posix()}) revises 18 item-advice replies. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Item-advice phrase wraps

Reviewed 49 complete item-advice replies. Seventeen received prose revisions, one was rewrapped with its wording intact, and 31 were retained. The Eagle Figurehead keeps the effect on the whole fleet, the Ceramic Earrings place the adviser’s recollection in the tavern, and all seven regional Proof of Conquest maps use parallel language. [Exact source and registered decisions](../{REVIEW.as_posix()})

Both advisers passed the native portrait checks for every reviewed item. All 18 changed pages were visually reviewed. The Lisbon replay used a disposable item-and-Advice fixture to display the revised Eagle Figurehead and Ceramic Earrings replies and the unchanged Sextant reply. The original item views and Lisbon screen returned exactly. The other replies, Gallery, the compact item screen and Mikhail’s branch were checked offline. Hardware was outside this pass. [Native and emulator evidence](../{VERIFY.as_posix()})

Only COMMON changes. The clean-input patch reconstructs the ROM byte for byte. All 114 accepted layers and the prior ASCII fixes carry forward. All 276 pending shared records keep their bytes and native locations. Five catalog indices changed because the revised records contain more trailing null bytes. Six startup holds, 24 protected name getters and 17 focused tests passed. Six early-wrap leads remain. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register-item-advice-phrase-wraps', 'exec'), env)


if __name__ == '__main__':
    env['main']()

