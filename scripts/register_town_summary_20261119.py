"""Register the verified Town Summary heading with the full cumulative release."""

from json import dumps
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_town_summary_20261119 as game
from scripts import stage_town_summary_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

parent, base, native = stage.parent, stage.base, stage.native
workflow = parent.workflow
PROFILE = 'all-routes-town-summary-v1-20261119'
ROOT = Path('out/town_summary_registered_20261119_v1')
ROM = ROOT / 'Translation_DS_Town_Summary_20261119_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261119_town_summary_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_town_summary_20261119.md')
STARTUP, QA = game.STARTUP_PROOF, stage.ROOT / 'registered_qa.xml'
CHECKPOINT = 'Town Summary shows the full Status heading, verified in five Lisbon gameplay frames.'
verified = SimpleNamespace(PROOF=stage.PROOF, LIVE=game.PLAYBACK)


def verify(registry, previous, viewed):
    stored, live, boot = map(base.load, (stage.PROOF, game.PLAYBACK, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == live['candidate_sha256'] == boot['candidate_sha256']
    assert stored['parent_sha256'] == previous['candidate_sha256'] == base.digest(parent.ROM)
    assert base.digest(stage.CLEAN) == stored['clean_input_sha256'] == previous['clean_input_sha256']
    assert stored['entire_parent_inverse'] and stored['atlas_bound'] == [228, 72] and stored['atlas_rectangles'] == 16
    assert all(base.digest(p) == digest for evidence in (stored['source_proofs'], live['evidence'], boot['evidence'])
               for p, digest in evidence.items())
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 5 and len(boot['original_protected_name_getters']) == 24
    assert boot['complete_town_status_mask']['text'] == 'Status'
    assert live['ordinary_input'] and not live['hardware'] and live['pixels_outside_status_exact'] and live['original_draw_and_clip_exact']
    assert len(live['sampled_changed_frames']) == 5 and len(live['complete_heading_masks']) == 40
    assert viewed == {s['path']: s['sha256'] for s in live['sheets']}
    assert all(base.digest(p) == digest for p, digest in viewed.items())
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(key, 0)) for key in ('tests', 'failures', 'errors', 'skipped')] == [51, 0, 0, 2]
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()

    clean, predecessor, target = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    old, new = map(native.files, (predecessor, target))
    assert old.keys() == new.keys() and {p for p in old if old[p] != new[p]} == {stage.ARM}
    assert native.digest(new[stage.ARM]) == stored['target_ARM9_sha256']
    observed, = base.load(stage.TRACE)['rows']
    expected, records = stage.transform(clean.read_file(stage.ARM), old[stage.ARM], observed)
    assert expected == new[stage.ARM] and dumps(records, sort_keys=True) == dumps(stored['records'], sort_keys=True)
    stage.verify_runtime(expected, previous)
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), new)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    target.replace_file(stage.ARM, old[stage.ARM])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    shared = parent.parent.parent.stage.workflow
    directory = native.digest(expected[shared.DIRECTORY_OFFSET:shared.TABLE_OFFSET])
    entries = shared.owned_entries(new[stage.COMMON], expected, directory)
    pending = base.load(stage.PENDING)['records']
    assert len(pending) == 276
    assert all(row['current_reference'] == shared.reference(entries[row['message_ID']]) and
               row['current_hex'] == entries[row['message_ID']].text.hex() for row in pending)
    for row in records:
        row['registered_reference'] = row['staged_reference'] | dict(candidate_sha256=candidate)
        row['observed_in_ordinary_town_summary'] = True
    review = {key: stored[key] for key in ('translation_policy', 'target_locale', 'encoder', 'review_gates')}
    review.update(candidate_sha256=candidate, records=records, checked_story_format_guard=controls, new_contextual_credit=0,
        shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'], direct_visual_review=viewed,
        observed_gameplay=live, source_and_native_dependency_proofs=stored['source_proofs'])
    validate_natural_dialogue_batch(review)
    return stored, review, {stage.ARM: native.digest(expected)}


publish = parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index('    DOC.write_text'):publish.index('    prefix =')]
program = checked_text(publish, {
    'len(manifest["batches"]) == 921 and len(manifest["checks"]) == 256':
        'len(manifest["batches"]) == 922 and len(manifest["checks"]) == 257',
    'verified_trade_labels_predecessor': 'verified_trade_categories_predecessor',
    'if row["decision"] != "retention" and row["id"] not in ids:':
        'if (row["decision"] != "retention" or row["original_geometry"] != row["staged_geometry"]) and row["id"] not in ids:',
    'owned_label_records=[row["registered_reference"] for row in draft["records"] if row["decision"] == "revision"]':
        'owned_label_records=[row["registered_reference"] for row in draft["records"] if row["original_geometry"] != row["staged_geometry"]]',
    'trade_categories': 'town_summary',
    'reviewed_UI_labels=18': 'reviewed_UI_labels=4',
    'previously_localized_records=18': 'previously_localized_records=4',
    'prose_revisions=6, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=12':
        'prose_revisions=1, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=3',
    'text_display_revisions=6': 'text_display_revisions=1',
    'ordinary_Lisbon_Trade_Local_and_Cargo=True': 'ordinary_Lisbon_Town_Summary=True',
    'Preserve Trade category ROM or reconstruction': 'Preserve Town Summary ROM or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Town Summary test candidate

The [local ROM](../../{ROM.as_posix()}) includes the full Status heading and the previous cumulative fixes.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Town Summary headings

Town Summary now shows Status in full. The source describes the settlement's condition above values such as Normal and Boom. Type, Growth and Arms retain their wording and screen positions. The four text records use one original 20-byte string. The revised atlas layout keeps all 16 active regions within 228 by 72 pixels with no overlaps. [Exact references and editorial decisions](../{REVIEW.as_posix()})

Paired ordinary Lisbon replays from an existing battery save verified complete glyphs for all four headings in five gameplay frames. Every sampled pixel outside the Status heading matched the predecessor. The shared Town Summary layout seen in the Amsterdam report uses this same original reader. The corrected replay visited Lisbon. [Gameplay comparison and checks](../{VERIFY.as_posix()}/town_summary_comparison.png)

The candidate preserves the registered ASCII right bound, the earlier Trade fixes and all 276 open shared entries. The clean-input patch reconstructs it byte for byte. Five startup frames matched exactly. The sixth matched outside the corrected Status heading. All 24 protected getters and 49 focused tests passed. Two tests that require optional historical ROM fixtures skipped. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register', 'exec'), env)


if __name__ == '__main__':
    env['main']()
