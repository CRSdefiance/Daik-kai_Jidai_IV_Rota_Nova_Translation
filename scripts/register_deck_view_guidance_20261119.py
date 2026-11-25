"""Register the full Deck View guidance and exact retained Filter labels."""

from pathlib import Path
from struct import unpack_from
from types import SimpleNamespace
from xml.etree import ElementTree

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_deck_view_guidance_gameplay_20261119 as live
from scripts import replay_deck_view_guidance_20261119 as replay
from scripts import stage_deck_view_guidance_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_town_shortage_20261119 import PENDING

base, native, parent = stage.base, stage.native, stage.parent
PROFILE = 'all-routes-deck-view-guidance-v1-20261119'
ROOT = Path('out/deck_view_guidance_registered_20261119_v1')
ROM = ROOT / 'Translation_DS_Deck_View_Guidance_20261119_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261119_deck_view_guidance_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_deck_view_guidance_registered_20261119.md')
STARTUP, QA = replay.STARTUP, stage.ROOT / 'registered_qa.xml'
verified = SimpleNamespace(PROOF=stage.ROOT / 'native_proof.json', LIVE=live.PROOF)
CHECKPOINT = 'The six revised Deck View guidance rows and both Filter choices are verified in ordinary gameplay and registered.'
COMMON = '/COMMON/MESFILE.DK4'
IDS = {
    0x14F460: ('DK4_NAV_FILTER_UNASSIGNED', 'Navigators with no assignment.'),
    0x14F490: ('DK4_NAV_FILTER_ALL', 'All navigators.'),
    0x15594: ('DK4_DECK_HELP_INTRO', 'Deck View can assign navigator duties.'),
    0x15598: ('DK4_DECK_HELP_ROOM_TYPE', 'Select a navigator and place them in a room. Room type determines their duty.'),
    0x1559C: ('DK4_DECK_HELP_ABILITY_REQUIREMENTS', 'Each duty has required abilities. Insufficient ability prevents assignment. Higher ability improves effectiveness.'),
}


def verify(registry, previous, viewed):
    stored, played, boot, offline = map(base.load, (stage.PROOF, verified.LIVE, STARTUP, verified.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == played['candidate_sha256'] == boot['candidate_sha256']
    assert stored['predecessor_sha256'] == played['predecessor_sha256'] == previous['candidate_sha256']
    assert stored['whole_parent_inverse'] and stored['previous_exact_help_pixels'] == 2325
    assert all(base.digest(p) == sha for proof in (stored, played, boot) for p, sha in proof['evidence'].items())
    assert offline['all_words_keep_one_row_all_glyphs_fit_and_first_last_letters_present']
    assert offline['native_header_view_and_pixel_guards_ABI_pass'] and offline['font_line_spacing'] == 16
    assert played['ordinary_existing_save'] and not played['hardware'] and played['exact_live_strings']
    assert played['unrelated_pixels_and_filter_transitions_preserved'] and len(played['revised_help']['rows']) == 6
    assert all([s['text'] for s in r['options']] == ['Unassigned', 'All'] for r in played['filter_labels'])
    assert len(played['filter_labels']) == 2
    assert viewed == {s['path']: s['sha256'] for s in stored['sheets'] + played['sheets']}
    assert all(base.digest(p) == sha for p, sha in viewed.items())
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [51, 0, 0, 2]
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()

    clean, original, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    old, new = map(native.files, (original, target))
    assert old.keys() == new.keys() and {p for p in old if old[p] != new[p]} == {stage.ARM}
    arm = new[stage.ARM]
    assert native.digest(arm) == stored['target_ARM9_sha256']
    stage.verify_runtime(arm, previous)
    before, after = [MainCodeFile(f[stage.ARM], stage.BASE) for f in (old, new)]
    source_arm = clean.read_file(stage.ARM)
    rows = []
    for r in stored['records']:
        field = r['field']
        ident, meaning = IDS[field]
        assert unpack_from('<I', source_arm, field)[0] == r['source_pointer']
        assert unpack_from('<I', arm, field) == unpack_from('<I', old[stage.ARM], field) == (r['target_pointer'],)
        at = r['target_pointer'] - stage.POOL
        current = bytes.fromhex(r['current_hex'])
        assert bytes(before.sections[3].data[at:at + len(current)]) == current
        value = (r['compiled'].encode('ascii') + b'\0').ljust(len(current), b'\0')
        assert bytes(after.sections[3].data[at:at + len(current)]) == value
        after.sections[3].data[at:at + len(current)] = current
        source = r['source_Japanese'].encode('cp932') + b'\0'
        source_offset = r['source_pointer'] - stage.BASE
        assert source_arm[source_offset:source_offset + len(source)] == source
        rows.append(r | dict(id=ident, file_path=stage.ARM, english=r['English'], source_meaning=meaning,
            source_reference=dict(field=field, pointer=r['source_pointer'], exact_stored_hex=source.hex()),
            current_reference=dict(field=field, pointer=r['target_pointer'], exact_stored_hex=current.hex()),
            registered_reference=dict(candidate_sha256=candidate, field=field, pointer=r['target_pointer'], exact_stored_hex=value.hex()),
            review=r['review'] | {'formatting': True}))
    assert len(rows) == 5 and sum(r['decision'] == 'revision' for r in rows) == 2
    assert bytes(after.save()) == old[stage.ARM]
    target.replace_file(stage.ARM, old[stage.ARM])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    assert stage.cache_plan(arm) == stage.cache_plan(old[stage.ARM])
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), new)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    w = parent.parent.stage.review
    active = w.owned_entries(new[COMMON], arm, native.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    pending = base.load(PENDING)['records']
    assert len(pending) == 276
    assert all(w.reference(active[r['message_ID']]) == r['current_reference'] and
               active[r['message_ID']].text.hex() == r['current_hex'] for r in pending)
    gates = ['source', 'context', 'localization', 'naturalness', 'formatting']
    draft = dict(candidate_sha256=candidate, translation_policy='natural-dialogue-v2', encoder='dialogue-relocatable-v1',
        target_locale='en-US', review_gates=gates, records=rows, observed_gameplay=played,
        checked_story_format_guard=controls, direct_visual_review=viewed,
        shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'])
    validate_natural_dialogue_batch(draft)
    return stored, draft, {stage.ARM: native.digest(arm)}


publish = parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index('    DOC.write_text'):publish.index('    prefix =')]
program = checked_text(publish, {
    'len(manifest["batches"]) == 932 and len(manifest["checks"]) == 267':
        'len(manifest["batches"]) == 933 and len(manifest["checks"]) == 268',
    'verified_twisted_horn_rumor_predecessor': 'verified_artifact_rumor_wraps_predecessor',
    'previously_localized_records=10': 'previously_localized_records=5',
    'reviewed_UI_labels=0': 'reviewed_UI_labels=5',
    'prose_revisions=3, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=7':
        'prose_revisions=2, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=3',
    'text_display_revisions=3': 'text_display_revisions=2',
    'initialized_Lisbon_Guild_Kings_Shield_and_return=True': 'ordinary_Deck_View_and_Filter=True',
    'natural_activation=False, hardware=False': 'natural_activation=True, hardware=False',
    'artifact_rumor_wraps': 'deck_view_guidance',
    'owned_shared_records=': 'owned_UI_records=',
    'changed_components=2, target_ARM9_sha256=archives[stage.ARM], target_COMMON_sha256=archives[stage.COMMON]':
        'changed_components=1, target_ARM9_sha256=archives[stage.ARM]',
    'ARM9_sha256=archives[stage.ARM], MESFILE_sha256=archives[stage.COMMON]':
        'ARM9_sha256=archives[stage.ARM], MESFILE_sha256=previous["target_COMMON_sha256"]',
    'Preserve the Guild artifact rumors ROM or reconstruction': 'Preserve the Deck View guidance ROM or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Deck View guidance test candidate

The [local ROM](../../{ROM.as_posix()}) clarifies room assignment and ability requirements in Deck View and includes prior registered corrections.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Deck View assignment guidance

Two revised paragraphs keep room type together and give each ability requirement a clear sentence. The introduction, Unassigned and All are retained. The original five pointer fields and fixed allocations are preserved. [Source-bound ledger](../{REVIEW.as_posix()})

Paired ordinary Lisbon replays from identical copies of the established save verified all six lines, both complete Filter labels, and the menu transitions. Both in-memory string sets matched their expected bytes. Differences in the compared screens were confined to the two edited help fields. Hardware testing remains open. [Ordinary replay](../{VERIFY.as_posix()}/ordinary_gameplay.json) · [Before and after](../{VERIFY.as_posix()}/deck_help_gameplay.png)

The clean-input patch rebuilds the candidate byte for byte. Six startup holds, 24 protected name getters and 49 focused tests passed. Two optional historical fixtures skipped. The ledger still credits 27,700 reviews, with 276 shared keys open. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register', 'exec'), env)


if __name__ == '__main__':
    env['main']()
