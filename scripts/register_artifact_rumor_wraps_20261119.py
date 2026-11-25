"""Register the three checked Guild rumor revisions on the cumulative ROM."""

from pathlib import Path
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_artifact_rumor_wraps_gameplay_20261119 as live
from scripts import replay_artifact_rumor_wraps_20261119 as replay
from scripts import stage_artifact_rumor_wraps_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_town_shortage_20261119 import PENDING

base, native, parent = stage.base, stage.native, stage.parent
PROFILE = 'all-routes-artifact-rumor-wraps-v1-20261119'
ROOT = Path('out/artifact_rumor_wraps_registered_20261119_v1')
ROM = ROOT / 'Translation_DS_Artifact_Rumor_Wraps_20261119_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261119_artifact_rumor_wraps_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_artifact_rumor_wraps_registered_20261119.md')
STARTUP, QA = replay.STARTUP, stage.ROOT / 'registered_qa.xml'
verified = SimpleNamespace(PROOF=replay.RECEIPT, LIVE=live.PROOF)
CHECKPOINT = 'Three Guild artifact rumors are registered after native display checks and a focused King’s Shield replay.'


def verify(registry, previous, viewed):
    stored, played, boot = map(base.load, (stage.PROOF, verified.LIVE, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == played['candidate_sha256'] == boot['candidate_sha256']
    assert stored['predecessor_sha256'] == played['predecessor_sha256'] == previous['candidate_sha256']
    assert stored['whole_parent_inverse'] and stored['new_coverage_credit'] == 0
    assert all(base.digest(p) == sha for proof in (stored, played, boot) for p, sha in proof['evidence'].items())
    assert played['initialized_gameplay'] and not played['natural_selection'] and not played['hardware']
    assert played['full_native_glyph_masks_equal'] and played['live_expanded_and_wrapped_bytes_verified']
    assert played['observed_message_ID'] == 3666 and played['other_revised_messages_checked_offline'] == [3661, 3664]
    assert len(played['unchanged_frames']) == 5 and played['item_list_frame'] in played['unchanged_frames']
    assert viewed == {s['path']: s['sha256'] for s in stored['sheets'] + played['sheets']}
    assert all(base.digest(p) == sha for p, sha in viewed.items())
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [51, 0, 0, 2]
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()

    ja, before, after = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    old, new = map(native.files, (before, after))
    assert old.keys() == new.keys() and {p for p in old if old[p] != new[p]} == {stage.ARM, stage.COMMON}
    arm, common = new[stage.ARM], new[stage.COMMON]
    hashes = {p: native.digest(new[p]) for p in (stage.ARM, stage.COMMON)}
    assert (hashes[stage.ARM], hashes[stage.COMMON]) == (stored['target_ARM9_sha256'], stored['target_COMMON_sha256'])
    assert arm[:DIRECTORY_OFFSET] == old[stage.ARM][:DIRECTORY_OFFSET] and arm[TABLE_END:] == old[stage.ARM][TABLE_END:]
    parent.parent.parent.stage.verify_runtime(arm, previous)
    w = stage.prior.review
    source = w.common_message_entries(ja.read_file(stage.COMMON), ja.read_file(stage.ARM))
    directory = native.digest(old[stage.ARM][DIRECTORY_OFFSET:TABLE_OFFSET])
    repack = FunctionType(stage.prior.relocate.__code__, stage.prior.relocate.__globals__ | {'DIRECTORY': directory})
    rows = {r['message_ID']: r for r in stored['records']}
    replacements = {n: bytes.fromhex(row['staged_hex']) for n, row in rows.items() if row['decision'] == 'revision'}
    assert set(rows) == set(range(3658, 3668)) and sorted(replacements) == [3661, 3664, 3666]
    packed, tables, current, allocation = repack(old[stage.COMMON], old[stage.ARM], rows, replacements)
    for key in ('source_block_lengths', 'target_block_lengths'):
        allocation[key] = {str(block): length for block, length in allocation[key].items()}
    assert packed == common and tables == arm and allocation == stored['allocation']
    for p in hashes:
        after.replace_file(p, old[p])
    assert bytes(after.rom.save()) == parent.ROM.read_bytes()
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(native.files(ja), new)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    pending = base.load(PENDING)['records']
    assert len(pending) == 276
    assert all(w.reference(current[r['message_ID']]) == r['current_reference'] and
               current[r['message_ID']].text.hex() == r['current_hex'] for r in pending)

    for n, row in rows.items():
        assert row['source_hex'] == source[n].text.hex() and row['source_reference'] == w.reference(source[n])
        assert row['staged_hex'] == current[n].text.hex() and row['staged_reference'] == w.reference(current[n])
        if n in replacements:
            assert row['complete_native_page']
            row['validation_scope'] = 'initialized Guild replay' if n == replay.ID else 'offline native portrait'
        else:
            assert row['current_hex'] == row['staged_hex']
        row['registered_reference'] = w.reference(current[n]) | dict(candidate_sha256=candidate)
        row['review']['formatting'] = True
    gates = ['source', 'context', 'localization', 'naturalness', 'formatting']
    draft = dict(candidate_sha256=candidate, translation_policy='natural-dialogue-v2', encoder='dialogue-relocatable-v1',
        target_locale='en-US', review_gates=gates, records=list(rows.values()), observed_gameplay=played,
        checked_story_format_guard=controls, direct_visual_review=viewed,
        shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'])
    validate_natural_dialogue_batch(draft)
    return stored, draft, hashes


publish = parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index('    DOC.write_text'):publish.index('    prefix =')]
program = checked_text(publish, {
    'len(manifest["batches"]) == 931 and len(manifest["checks"]) == 266':
        'len(manifest["batches"]) == 932 and len(manifest["checks"]) == 267',
    'verified_rafael_trade_and_arms_predecessor': 'verified_twisted_horn_rumor_predecessor',
    'previously_localized_records=12': 'previously_localized_records=10',
    'prose_revisions=1, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=11':
        'prose_revisions=3, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=7',
    'text_display_revisions=1': 'text_display_revisions=3',
    'ordinary_Lisbon_Guild_rumor_and_return=True': 'initialized_Lisbon_Guild_Kings_Shield_and_return=True',
    'natural_activation=True, hardware=False': 'natural_activation=False, hardware=False',
    'twisted_horn_rumor': 'artifact_rumor_wraps',
    'Preserve the Twisted Horn rumor ROM or reconstruction': 'Preserve the Guild artifact rumors ROM or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Guild artifact rumors test candidate

The [local ROM](../../{ROM.as_posix()}) improves the Rose Quartz, Witch Idol and King’s Shield rumors and includes all prior registered corrections.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Guild artifact rumors

All ten artifact rumors received a contextual rereview. Three revisions keep the star pattern, the witch on the bow and the sailors’ praise readable in full phrases. Seven records retain their wording with individual reasons. The three new pages passed the original portrait renderer and visual checks. [Per-record ledger](../{REVIEW.as_posix()})

The recorded Guild inputs were replayed with one temporary in-memory artifact selection. The original selectors fetched the King’s Shield rumor, which matched the complete glyph mask and both text buffers. Restoring the artifact input before dismissal preserved five other held frames, including the purchase question and item list. Rose Quartz and Witch Idol have offline display coverage. Natural selection and hardware testing remain open. [Initialized replay](../{VERIFY.as_posix()}/initialized_gameplay.json) · [Verified screens](../{VERIFY.as_posix()}/lesson_display.png)

Only the three COMMON templates and their allocation table change. The clean-input patch rebuilds the candidate byte for byte. Six startup holds, 24 protected name getters and 49 focused tests passed. Two optional historical fixtures skipped. The ledger still credits 27,700 reviews, with 276 shared keys open. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register', 'exec'), env)


if __name__ == '__main__':
    env['main']()
