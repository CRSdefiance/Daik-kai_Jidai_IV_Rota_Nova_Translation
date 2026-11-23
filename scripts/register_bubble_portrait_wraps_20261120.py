"""Register the reviewed bubbles dialogue on the current cumulative release."""

from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_bubble_portrait_replay_20261120 as live
from scripts import register_genoa_tomato_exchange_20261120 as parent
from scripts import replay_bubble_portrait_compatible_20261120 as fixture
from scripts import stage_bubble_portrait_wraps_20261120 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch = parent.base, parent.batch
PROFILE = 'all-routes-bubble-portrait-wraps-v1-20261120'
ROOT = Path('out/bubble_portrait_wraps_registered_20261120_v1')
ROM = ROOT / 'Translation_DS_Bubbles_20261120_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261120_bubble_portrait_wraps_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_bubble_portrait_wraps_registered_20261120.md')
STARTUP, QA = (stage.ROOT / n for n in ('own_startup_verification.json', 'qa.xml'))
STARTUP_CAPTURE = stage.ROOT / 'startup/capture/capture_report.json'
CHECKPOINT = 'Revised three Strange Bubbles warnings and verified the five-panel sighting and sailing return.'
PENDING = Path('translations/editorial_checkpoints/SharedText_20261110_v1/shared_display_worklist_20261120_v1.json')


def verify(registry, previous, viewed):
    stored, actual = map(base.load, (stage.PROOF, live.PROOF))
    cand = base.digest(stage.ROM)
    assert cand == stored['candidate_sha256'] == actual['candidate_sha256']
    assert stored['parent_sha256'] == previous['candidate_sha256'] == base.digest(parent.ROM)
    assert stored['full_parent_inverse'] and base.digest(stage.CLEAN) == previous['clean_input_sha256']
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()
    assert actual['compatible_test_ROM_sha256'] == base.digest(fixture.ROM)
    assert viewed == {r['path']: r['sha256'] for r in stored['sheets']} | {actual['sheet']['path']: actual['sheet']['sha256']}
    assert all(base.digest(p) == digest for p, digest in (viewed | stored['evidence'] | actual['evidence']).items())
    assert actual['selector_and_table_restored'] and actual['actual_emulator'] and not actual['natural_random_selection']
    assert [r['message_ID'] for r in actual['exact_glyph_panels']] == [461, 463, 469, 470, 478]
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [17, 0, 0, 0]
    clean, old, image = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(batch.files, (old, image))
    assert before.keys() == after.keys() and {key for key in before if before[key] != after[key]} == {stage.COMMON}
    arm = after[stage.ARM]
    assert batch.digest(arm) == stored['target_ARM9_sha256'] == previous['target_ARM9_sha256']
    assert batch.digest(after[stage.COMMON]) == stored['target_COMMON_sha256']
    old_rows, now_rows = map(fixture.records, (old, image))
    assert len(old_rows) == len(now_rows) == 3668
    assert {i for i, (a, b) in enumerate(zip(old_rows, now_rows, strict=True)) if a.text != b.text} == stage.EDITS.keys()
    shifted_indices = {}
    for i, (a, b) in enumerate(zip(old_rows, now_rows, strict=True)):
        if i in stage.EDITS:
            continue
        original, current = stage.reference(a), stage.reference(b)
        if original != current:
            assert original | {'record_index': current['record_index']} == current
            shifted_indices[i] = dict(before=original, after=current)
    pending = {r['message_ID'] for r in base.load(PENDING)['records']}
    assert len(pending) == 276 and not pending.intersection(shifted_indices)
    assert len(shifted_indices) == 21
    image.replace_file(stage.COMMON, before[stage.COMMON])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    guards = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guards)(batch.files(clean), after)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    starter = parent.parent.env['startup_check'].startup_proof
    FunctionType(starter.__code__, starter.__globals__ | {'STARTUP': STARTUP, 'STARTUP_CAPTURE': STARTUP_CAPTURE})(
        previous, cand, arm)
    records = stored['records']
    assert len(records) == 30 and {r['message_ID'] for r in records if r['decision'] == 'revision'} == stage.EDITS.keys()
    for row in records:
        now = now_rows[row['message_ID']]
        assert now.text.hex() == row['staged_hex'] and stage.reference(now) == row['staged_reference']
        row['registered_reference'] = row['staged_reference'] | {'candidate_sha256': cand}
        row['review']['formatting'] = True
    draft = dict(translation_policy=stored['translation_policy'], target_locale=stored['target_locale'],
                 encoder=stored['encoder'], review_gates=stored['review_gates'], records=records,
                 candidate_sha256=cand, parent_sha256=previous['candidate_sha256'],
                 checked_story_format_guard=controls, unchanged_pending_records=276,
                 shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'],
                 changed_physical_record_indices=shifted_indices,
                 pending_source_receipt_sha256=base.digest(PENDING),
                 focused_replay=actual, new_contextual_credit=0)
    validate_natural_dialogue_batch(draft)
    return stored, draft, {stage.COMMON: stored['target_COMMON_sha256']}


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index('    DOC.write_text'):template.index('    prefix =')]
program = checked_text(template, {
    'len(manifest["batches"]) == 953 and len(manifest["checks"]) == 288':
        'len(manifest["batches"]) == 954 and len(manifest["checks"]) == 289',
    'stage.STORED, STARTUP, QA, live.PROOF, town.OUTPUT, args.visual_review,':
        'stage.PROOF, STARTUP, QA, live.PROOF, fixture.PROOF, args.visual_review,',
    'release_stack_before_genoa_tomatoes.json': 'release_stack_before_bubble_portraits.json',
    'release_stack_with_genoa_tomatoes.json': 'release_stack_with_bubble_portraits.json',
    'verified_sailing_help_predecessor=predecessor, genoa_tomatoes_release=str(REVIEW)':
        'verified_genoa_predecessor=predecessor, bubble_portraits_release=str(REVIEW)',
    'registered_genoa_tomatoes_and_complete_parent_inverse': 'registered_bubble_portraits_and_complete_parent_inverse',
    'manifest["genoa_tomatoes_pipeline"]': 'manifest["bubble_portraits_pipeline"]',
    'stored_proof_sha256=base.digest(stage.STORED)': 'stored_proof_sha256=base.digest(stage.PROOF)',
    'owned_story_blocks={path: n for path, n in zip(sorted(archives), (189, 181, 150), strict=True)}, target_story_archive_sha256=archives':
        'owned_message_IDs=sorted(stage.EDITS), target_COMMON_sha256=archives[stage.COMMON]',
    'changed_components=3': 'changed_components=1, target_COMMON_sha256=archives[stage.COMMON]',
    'MESFILE_sha256=previous["target_COMMON_sha256"]': 'MESFILE_sha256=release["target_COMMON_sha256"]',
    'previously_localized_records=40, new_contextual_records=0, prose_revisions=10, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=30':
        'previously_localized_records=30, new_contextual_records=0, prose_revisions=3, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=27',
    'ordinary_Genoa_10_pages=True, original_scene_trigger_and_town_return=True':
        'compatible_focused_five_bubble_pages=True, selector_inputs_restored=True',
    'ledger["genoa_tomatoes_20261120"]': 'ledger["bubble_portrait_wraps_20261120"]',
    'prior_records_reviewed=40, ordinary_story_pages=10, new_contextual_credit=0,\n        prose_revisions=10, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=30':
        'prior_records_reviewed=30, compatible_gameplay_pages=5, new_contextual_credit=0,\n        prose_revisions=3, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=27',
    'Preserve the Genoa tomato candidate or reconstruction': 'Preserve the bubble portrait candidate or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Strange Bubbles dialogue testing candidate

The [testing ROM](../../{ROM.as_posix()}) revises three Strange Bubbles warnings. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Strange Bubbles dialogue and wrap review

Reviewed all 30 variants from the first sighting, recognition and evasive order through the ship-danger reports. The older lookout now points out the bubbles in two complete beats. Each of the two revised damage warnings fits in one line and preserves whether the danger is imminent or already underway. Twenty-seven other variants keep their existing wording and have individual retention reasons. [Exact source, prior and registered references](../{REVIEW.as_posix()})

All 30 installed pages passed the original portrait consumer and complete glyph checks. The three revised pages were visually reviewed. Two replays on the cumulative ROM encountered a water shortage and a port sighting before the target. The earlier working voyage with the exact revised lookout record displayed all five scene panels and returned to sailing. The test selected the event and lookout variant temporarily, then restored both selectors. Both later damage variants received offline checks. Hardware and natural random selection remain unvisited. [Native and emulator evidence](../{VERIFY.as_posix()})

Only the shared message archive changes. The cumulative patch reconstructs the registered ROM exactly, all 114 accepted layers and the ASCII right-bound fix carry forward, and the 276 pending records keep their payloads and locations. Six startup holds, 24 protected getters, and 17 focused tests passed. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register-bubble-portraits', 'exec'), env)


if __name__ == '__main__':
    env['main']()
