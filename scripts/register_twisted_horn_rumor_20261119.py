"""Register the Lisbon Guild rumor and its source-reviewed shared exchanges."""

from pathlib import Path
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_twisted_horn_rumor_gameplay_20261119 as live
from scripts import replay_twisted_horn_rumor_20261119 as replay
from scripts import stage_twisted_horn_rumor_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_town_shortage_20261119 import PENDING

base, native, parent = stage.base, stage.native, stage.parent
PROFILE = 'all-routes-twisted-horn-rumor-v1-20261119'
ROOT = Path('out/twisted_horn_rumor_registered_20261119_v1')
ROM = ROOT / 'Translation_DS_Twisted_Horn_Rumor_20261119_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261119_twisted_horn_rumor_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_twisted_horn_rumor_20261119.md')
STARTUP, QA = replay.STARTUP, stage.ROOT / 'registered_qa.xml'
verified = SimpleNamespace(PROOF=stage.review.OUTPUT, LIVE=live.PROOF)
CHECKPOINT = 'The Twisted Horn rumor’s complete final phrase is registered and verified in ordinary Lisbon Guild gameplay.'
MEANINGS = {
    62: ('A casual hello and an invitation to say why the visitor has come.', 'At the Guild counter before the menu.'),
    67: ('The Sailor asks whether the fleet should call at the named port.', 'The fleet approaches Lisbon and the player can choose to dock.'),
    97: ('The named character has gained a level.', 'The level-up announcement appears during travel.'),
    297: ('The named location has been discovered.', 'The navigation notice identifies Seville after the Sailor spots land.'),
    397: ('The Sailor reports that the sailors appear to have scurvy.', 'An illness interruption on the voyage back toward Lisbon.'),
    426: ('The Sailor complains that fog has started coming in.', 'Fog interrupts the manual voyage.'),
    633: ('There is no Surveyor for the route.', 'The crew explains why Auto Move cannot proceed as planned.'),
    1071: ('The Guildmaster asks the customer which item they want.', 'The question leads into the Guild’s item list.'),
    1293: ('The Sailor addresses the admiral and reports a town in sight.', 'The sighting comes before the location is named.'),
    2903: ('A book finished in the 13th century recounts what Marco Polo saw and heard in the East.', 'The Guild’s item list shows the book description.'),
    2940: ('A navigation tool for finding an accurate position at sea.', 'The Sextant description appears on its equipped item card.'),
}


def verify(registry, previous, viewed):
    stored, source_review, played, boot = map(base.load, (stage.PROOF, verified.PROOF, verified.LIVE, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == played['candidate_sha256'] == boot['candidate_sha256']
    assert stored['predecessor_sha256'] == played['predecessor_sha256'] == source_review['registered_candidate_sha256'] == previous['candidate_sha256']
    assert stored['whole_parent_inverse'] and stored['revised_lines'][-1].strip() == 'medicine that cures any illness.'
    assert all(base.digest(p) == sha for proof in (stored, source_review, played, boot) for p, sha in proof['evidence'].items())
    assert played['ordinary_gameplay'] and not played['hardware'] and played['message_ID'] == stage.ID
    assert played['live_expanded_and_wrapped_bytes_verified'] and played['full_native_glyph_masks_equal']
    assert len(played['unchanged_frames']) == 8 and played['item_list_frame'] in played['unchanged_frames']
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
    parent.parent.stage.verify_runtime(arm, previous)
    w = stage.review
    source = w.common_message_entries(ja.read_file(stage.COMMON), ja.read_file(stage.ARM))
    directory = native.digest(old[stage.ARM][DIRECTORY_OFFSET:TABLE_OFFSET])
    repack = FunctionType(stage.relocate.__code__, stage.relocate.__globals__ | {'DIRECTORY': directory})
    item = stored['record']
    packed, tables, current, allocation = repack(old[stage.COMMON], old[stage.ARM], {stage.ID: item},
        {stage.ID: bytes.fromhex(item['staged_hex'])})
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

    rows = []
    gates = ['source', 'context', 'localization', 'naturalness', 'formatting']
    for saved in source_review['records']:
        number = saved['message_ID']
        assert saved['source_hex'] == source[number].text.hex() and saved['source_reference'] == w.reference(source[number])
        if number == stage.ID:
            assert item['staged_hex'] == current[number].text.hex()
            row = item | dict(ordinary_gameplay_verified=played['held_frames'][1], compiled_lines=stored['revised_lines'])
        else:
            assert current[number].text.hex() == saved['current_hex']
            meaning, context = MEANINGS[number]
            row = saved | dict(source_meaning=meaning, context=context)
        rows.append(row | dict(review=dict.fromkeys(gates, True), fresh_rendering_pending=False,
            registered_reference=w.reference(current[number]) | dict(candidate_sha256=candidate)))
    assert len(rows) == 12 and [x['message_ID'] for x in rows if x['decision'] == 'revision'] == [stage.ID]
    draft = dict(candidate_sha256=candidate, translation_policy='natural-dialogue-v2', encoder='dialogue-relocatable-v1',
        target_locale='en-US', review_gates=gates, records=rows, observed_gameplay=played,
        checked_story_format_guard=controls, direct_visual_review=viewed,
        shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'])
    validate_natural_dialogue_batch(draft)
    return stored, draft, hashes


publish = parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index('    DOC.write_text'):publish.index('    prefix =')]
program = checked_text(publish, {
    'len(manifest["batches"]) == 930 and len(manifest["checks"]) == 265':
        'len(manifest["batches"]) == 931 and len(manifest["checks"]) == 266',
    'verified_departure_numerals_predecessor': 'verified_rafael_trade_and_arms_predecessor',
    'previously_localized_records=20': 'previously_localized_records=12',
    'prose_revisions=9, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=11':
        'prose_revisions=1, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=11',
    'text_display_revisions=9': 'text_display_revisions=1',
    'initialized_Rafael_trade_choices_and_Arms_lesson=True': 'ordinary_Lisbon_Guild_rumor_and_return=True',
    'natural_activation=False, hardware=False': 'natural_activation=True, hardware=False',
    'rafael_trade_and_arms': 'twisted_horn_rumor',
    'owned_story_records=[row["registered_reference"] for row in draft["records"] if row["decision"] == "revision"], target_ARM9_sha256=previous["target_ARM9_sha256"]':
        'owned_shared_records=[row["registered_reference"] for row in draft["records"] if row["decision"] == "revision"], target_ARM9_sha256=archives[stage.ARM]',
    'changed_components=1, target_ARM9_sha256=previous["target_ARM9_sha256"]':
        'changed_components=2, target_ARM9_sha256=archives[stage.ARM], target_COMMON_sha256=archives[stage.COMMON]',
    'ARM9_sha256=previous["target_ARM9_sha256"], MESFILE_sha256=previous[\'target_COMMON_sha256\']':
        'ARM9_sha256=archives[stage.ARM], MESFILE_sha256=archives[stage.COMMON]',
    'Preserve the Rafael Trade and Arms ROM or reconstruction': 'Preserve the Twisted Horn rumor ROM or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Twisted Horn rumor test candidate

The [local ROM](../../{ROM.as_posix()}) keeps the Guildmaster’s final medicine phrase together and includes all prior registered corrections.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# The Guildmaster’s Twisted Horn rumor

The ordinary Lisbon return supplied twelve contextual decisions. Eleven retain their exact wording. The Twisted Horn rumor formerly left “illness.” alone. It still treats the horn’s shape, possible dragon origin and medicinal claim as reports, and the final row now reads “medicine that cures any illness.” The original portrait consumer wraps the stored paragraph. [Per-record ledger](../{REVIEW.as_posix()})

The recorded ordinary Guild replay verified the full expanded and wrapped buffers and every visible glyph of the revised rumor. Eight other held frames match the earlier replay, including the purchase question, item list and equipped Sextant. Hardware testing remains open. [Before and after](../{VERIFY.as_posix()}/lesson_display.png) · [Replay proof](../{VERIFY.as_posix()}/ordinary_lisbon_verification.json)

Only COMMON 3665 and its allocation table change. The clean-input patch rebuilds the candidate byte for byte. Six startup holds, 24 protected name getters and 49 focused tests passed. Two optional historical fixtures skipped. The ledger still credits 27,700 reviews, with 276 shared keys open. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register', 'exec'), env)


if __name__ == '__main__':
    env['main']()
