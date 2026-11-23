"""Register ten verified Deck comment revisions on the cumulative candidate."""

from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_bubble_portrait_wraps_20261120 as parent
from scripts import replay_deck_phrase_wraps_20261121 as live
from scripts import stage_deck_phrase_wraps_20261121 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch = parent.base, parent.batch
PROFILE = 'all-routes-deck-phrase-wraps-v1-20261121'
ROOT = Path('out/deck_phrase_wraps_registered_20261121_v1')
ROM = ROOT / 'Translation_DS_Deck_Phrase_Wraps_20261121_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261121_deck_phrase_wraps_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_deck_phrase_wraps_registered_20261121.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'qa.xml'
STARTUP_CAPTURE = stage.ROOT / 'startup/capture/capture_report.json'
CHECKPOINT = 'Revised ten Deck comments with premature line breaks and verified Gerhard’s sail-handling comment and town return.'
PENDING = parent.PENDING


def verify(registry, previous, viewed):
    stored, actual = map(base.load, (stage.PROOF, live.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == actual['candidate_sha256']
    assert stored['parent_sha256'] == previous['candidate_sha256'] == base.digest(parent.ROM)
    assert stored['complete_parent_inverse'] and stored['exact_clean_patch_reconstruction']
    assert stored['patch_sha256'] == base.digest(stage.PATCH)
    assert stage.REBUILT.read_bytes() == stage.ROM.read_bytes()
    sheets = [stored['native_sheet'], actual['sheet']]
    assert viewed == {s['path']: s['sha256'] for s in sheets}
    assert all(base.digest(p) == digest for p, digest in (viewed | actual['evidence']).items())
    assert actual['actual_emulator'] and actual['normal_return_frame'] == 4800
    assert not actual['natural_assignment'] and not actual['hardware']
    assert [r['message_id'] for r in actual['complete_holds']] == [1524, 1524]
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [17, 0, 0, 0]
    clean, old, image = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    assert base.digest(stage.CLEAN) == previous['clean_input_sha256']
    before, after = map(batch.files, (old, image))
    assert before.keys() == after.keys() and {key for key in before if before[key] != after[key]} == {stage.ARM, stage.COMMON}
    old_arm, arm = before[stage.ARM], after[stage.ARM]
    assert batch.digest(arm) == stored['target_ARM9_sha256']
    assert batch.digest(after[stage.COMMON]) == stored['target_COMMON_sha256']
    assert len(arm) == len(old_arm)
    assert arm[:DIRECTORY_OFFSET] == old_arm[:DIRECTORY_OFFSET] and arm[TABLE_END:] == old_arm[TABLE_END:]

    old_rows, now_rows = [
        stage.owned_entries(files[stage.COMMON], files[stage.ARM],
                            batch.digest(files[stage.ARM][DIRECTORY_OFFSET:TABLE_OFFSET]))
        for files in (before, after)
    ]
    assert len(old_rows) == len(now_rows) == 3668
    assert {a.message_id for a, b in zip(old_rows, now_rows, strict=True) if a.text != b.text} == stage.EDIT.keys()
    assert stored['allocation']['all_unselected_native_copy_spans_exact']
    assert stored['allocation']['complete_COMMON_and_ARM9_table_inverse']
    pending = base.load(PENDING)['records']
    assert len(pending) == stored['unchanged_pending'] == 276
    for row in pending:
        now = now_rows[row['message_ID']]
        assert stage.reference(now) == row['current_reference'] and now.text.hex() == row['current_hex']

    image.replace_file(stage.COMMON, before[stage.COMMON])
    image.replace_file(stage.ARM, old_arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    guards = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guards)(batch.files(clean), after)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    starter = parent.parent.parent.env['startup_check'].startup_proof
    FunctionType(starter.__code__, starter.__globals__ | {'STARTUP': STARTUP, 'STARTUP_CAPTURE': STARTUP_CAPTURE})(
        previous, candidate, arm)

    records = stored['records']
    assert len(records) == 10 and {r['message_ID'] for r in records} == stage.EDIT.keys()
    for row in records:
        n = row['message_ID']
        assert now_rows[n].text.hex() == row['staged_hex'] and stage.reference(now_rows[n]) == row['staged_reference']
        row['registered_reference'] = row['staged_reference'] | {'candidate_sha256': candidate}
        row['gameplay_observed'] = n == 1524
    draft = dict(translation_policy=stored['translation_policy'], target_locale=stored['target_locale'],
                 encoder=stored['encoder'], review_gates=stored['review_gates'], records=records,
                 candidate_sha256=candidate, parent_sha256=previous['candidate_sha256'],
                 checked_story_format_guard=controls, unchanged_pending_records=276,
                 shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'],
                 directory_allocation=stored['allocation'], pending_source_receipt_sha256=base.digest(PENDING),
                 focused_replay=actual, visual_review_receipt=viewed, new_contextual_credit=0)
    validate_natural_dialogue_batch(draft)
    return stored, draft, {stage.ARM: stored['target_ARM9_sha256'], stage.COMMON: stored['target_COMMON_sha256']}


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index('    DOC.write_text'):template.index('    prefix =')]
program = checked_text(template, {
    'len(manifest["batches"]) == 954 and len(manifest["checks"]) == 289':
        'len(manifest["batches"]) == 955 and len(manifest["checks"]) == 290',
    'stage.PROOF, STARTUP, QA, live.PROOF, fixture.PROOF, args.visual_review,':
        'stage.PROOF, STARTUP, QA, live.PROOF, args.visual_review,',
    'release_stack_before_bubble_portraits.json': 'release_stack_before_deck_phrase_wraps.json',
    'release_stack_with_bubble_portraits.json': 'release_stack_with_deck_phrase_wraps.json',
    'verified_genoa_predecessor=predecessor, bubble_portraits_release=str(REVIEW)':
        'verified_bubble_predecessor=predecessor, deck_phrase_wraps_release=str(REVIEW)',
    'registered_bubble_portraits_and_complete_parent_inverse': 'registered_deck_phrase_wraps_and_complete_parent_inverse',
    'manifest["bubble_portraits_pipeline"]': 'manifest["deck_phrase_wraps_pipeline"]',
    'owned_message_IDs=sorted(stage.EDITS), target_COMMON_sha256=archives[stage.COMMON]':
        'owned_message_IDs=sorted(stage.EDIT), target_COMMON_sha256=archives[stage.COMMON], target_ARM9_sha256=archives[stage.ARM]',
    'changed_components=1, target_COMMON_sha256=archives[stage.COMMON]':
        'changed_components=2, target_COMMON_sha256=archives[stage.COMMON], target_ARM9_sha256=archives[stage.ARM]',
    'ARM9_sha256=previous["target_ARM9_sha256"], MESFILE_sha256=release["target_COMMON_sha256"]':
        'ARM9_sha256=release["target_ARM9_sha256"], MESFILE_sha256=release["target_COMMON_sha256"]',
    'previously_localized_records=30, new_contextual_records=0, prose_revisions=3, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=27':
        'previously_localized_records=10, new_contextual_records=0, prose_revisions=10, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=0',
    'compatible_focused_five_bubble_pages=True, selector_inputs_restored=True':
        'focused_gerhard_holds=2, normal_town_return=True, disposable_room_assignment=True',
    'ledger["bubble_portrait_wraps_20261120"]': 'ledger["deck_phrase_wraps_20261121"]',
    'prior_records_reviewed=30, compatible_gameplay_pages=5, new_contextual_credit=0,\n        prose_revisions=3, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=27':
        'prior_records_reviewed=10, actual_gameplay_records=1, new_contextual_credit=0,\n        prose_revisions=10, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=0',
    'Preserve the bubble portrait candidate or reconstruction': 'Preserve the Deck phrase-wrap candidate or reconstruction',
    'Current editorial checkpoint - 2026-11-20': 'Current editorial checkpoint - 2026-11-21',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Deck phrase-wrap testing candidate

The [testing ROM](../../{ROM.as_posix()}) revises ten Deck comments. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Deck comment phrase wraps

Revised ten earlier Deck comments against the clean Japanese and their original role, battle or health selectors. The new wraps keep the financial report together and give Hodram two complete clauses about winning with fewer casualties. Six comments now fit on one row. These are separate conditional remarks and carry no new dialogue credit. [Exact clean, prior and registered references](../{REVIEW.as_posix()})

All ten pages were visually reviewed after native output checks. A Copenhagen replay displayed both lines of Gerhard’s revised sail-handling comment in two holds and returned to town. The replay used a disclosed room-assignment fixture on a disposable save. The other nine comments were checked offline. Hardware remains unvisited. [Native and emulator evidence](../{VERIFY.as_posix()})

The patch reconstructs the registered ROM exactly. Only COMMON and its ARM9 directory data change. All 114 accepted layers, the ASCII right-bound fix and the positions and payloads of 276 pending records carry forward. Six startup holds, 24 protected getters and 17 focused tests passed. Twenty-three leads from the early-break scan remain. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register-deck-phrase-wraps', 'exec'), env)


if __name__ == '__main__':
    env['main']()

