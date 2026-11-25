"""Register Rafael's source-reviewed trade and town-defense lessons."""

from pathlib import Path
from struct import unpack_from
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_choice_object_v2 import count_and_base, labels
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_rafael_trade_and_arms_replay_20261119 as live_check
from scripts import check_rafael_trade_and_arms_20261119 as offline
from scripts import register_rafael_sail_controls_20261119 as template
from scripts import replay_rafael_trade_and_arms_20261119 as replay
from scripts import review_rafael_trade_and_arms_20261119 as staged
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_town_shortage_20261119 import PENDING

base, native, parent = staged.base, staged.native, staged.parent
stage = SimpleNamespace(ROOT=staged.STAGED, ROM=staged.ROM, PROOF=staged.PROOF)
PROFILE = 'all-routes-rafael-trade-and-arms-v1-20261119'
ROOT = Path('out/rafael_trade_and_arms_registered_20261119_v1')
ROM = ROOT / 'Translation_DS_Rafael_Trade_and_Arms_20261119_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261119_rafael_trade_and_arms_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_rafael_trade_and_arms_registered_20261119.md')
STARTUP, QA = replay.STARTUP, stage.ROOT / 'registered_qa.xml'
verified = SimpleNamespace(PROOF=offline.PROOF, LIVE=live_check.PROOF)
CHECKPOINT = 'Rafael’s trade and town-defense lessons are registered after emulator checks of both trading responses and Janus’s advice.'
SC0, COMMON = '/data/SC0.DK4', '/COMMON/MESFILE.DK4'
ROW_NOTES = {
    'DK4_MES_B129_R0005': 'The question has two readable lines, one reserving the maximum first-name width.',
    'DK4_MES_B129_R0042': 'The full instruction fits on one line.',
    'DK4_MES_B129_R0045': 'Commercial Investment and new local goods stay together within three lines.',
    'DK4_MES_B140_R0012': 'The Arms rating, military investment and qualified comparison fit together within one page.',
}


def verify(registry, previous, viewed):
    stored, draft, live, layouts, boot = map(base.load, (stage.PROOF, staged.OUTPUT, verified.LIVE, verified.PROOF, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == live['candidate_sha256'] == layouts['candidate_sha256'] == boot['candidate_sha256']
    assert stored['predecessor_sha256'] == live['predecessor_sha256'] == previous['candidate_sha256']
    assert stored['manuscript_sha256'] == base.digest(staged.OUTPUT) and stored['whole_parent_inverse']
    assert layouts['stage_proof_sha256'] == base.digest(stage.PROOF) and layouts['previews'] == 19
    assert all(base.digest(p) == sha for proof in (live, boot) for p, sha in proof['evidence'].items())
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert live['initialized_gameplay'] and not live['natural_activation'] and not live['hardware']
    assert len(live['panels']) == 18 and all(p['full_body_and_nameplate_match'] for p in live['panels'])
    assert [r['result_words'] for r in live['choices']] == [[2, 0], [2, 1]]
    assert all(m['both_full_caption_masks_equal'] for m in live['choices']) and all(c['original_end'] for c in live['cases'])
    assert viewed == {s['path']: s['sha256'] for s in layouts['sheets'] + live['sheets']}
    assert all(base.digest(p) == sha for p, sha in viewed.items())
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [51, 0, 0, 2]
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()

    clean, before, after = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    old, new = map(native.files, (before, after))
    assert old.keys() == new.keys() and {p for p in old if old[p] != new[p]} == {SC0}
    arm = new[native.ARM]
    assert native.digest(arm) == previous['target_ARM9_sha256']
    parent.stage.verify_runtime(arm, previous)
    a, b = [native.IlnkContainer.parse(files[SC0]).blocks for files in (old, new)]
    assert stored['changed_blocks'] == {SC0: [129, 140]}
    assert [i for i, (x, y) in enumerate(zip(a, b, strict=True)) if x != y] == [129, 140]
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), new)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    after.replace_file(SC0, old[SC0])
    assert bytes(after.rom.save()) == parent.ROM.read_bytes()
    w = parent.stage.inn.stage.workflow
    directory = native.digest(arm[w.DIRECTORY_OFFSET:w.TABLE_OFFSET])
    current = w.owned_entries(new[COMMON], arm, directory)
    pending = base.load(PENDING)['records']
    assert len(pending) == 276
    assert all(w.reference(current[r['message_ID']]) == r['current_reference'] and
               current[r['message_ID']].text.hex() == r['current_hex'] for r in pending)

    observed = {r['id']: r for r in live['panels']}
    choice_ids = {i for menu in live['choices'] for i in menu['ids']}
    page_proofs = {r['id']: r for r in layouts['revisions']}
    retained = set(layouts['retentions'])
    archive_sha = native.digest(new[SC0])
    commands = {ident: (c, g['plans'].get(ident)) for g in stored['groups'] for c in g['commands'] for ident in c['record_ids']}
    assert observed.keys() | choice_ids == page_proofs.keys() | retained == commands.keys()
    assert len(choice_ids) == 2 and draft['counts'] == dict(prose=9, retention=11)
    for row in draft['records']:
        ident, block = row['id'], row['block']
        command, plan = commands[ident]
        at, raw = command['stored_offset'], bytes.fromhex(command['stored'])
        assert b[block][at:at + len(raw)] == raw
        if ident in choice_ids:
            index, = row['native_slots']
            count, header = count_and_base(raw)
            assert count == 2 and raw.hex() == command['current']
            value = labels(raw)[index]
            offset = header + unpack_from('<H', raw, 2 + index * 2)[0]
            row['initialized_choice_verified'] = next(r for r in live['choices'] if r['selected'] == index)
        else:
            offset = 5
            value = raw[5:raw.index(0, 6)]
            assert value[0] == row['source_selector']
            row['initialized_gameplay_verified'] = observed[ident]
        assert b[block][at + offset:at + offset + len(value)] == value
        row['registered_reference'] = dict(candidate_sha256=candidate, file_path=SC0, block=block,
            command_offset=at, offset=at + offset, archive_sha256=archive_sha, exact_stored_hex=value.hex())
        if row['decision'] == 'revision':
            assert value.hex() == page_proofs[ident]['target_hex']
            warnings = {issue['code'] for issue in plan.get('diagnostics', ())}
            assert warnings == ({'line-break-count'} if ident in ROW_NOTES else set())
            row['compiled_lines'] = plan['lines']
            if warnings:
                row.update(qa_waivers=['line-break-count'], qa_waiver_reason=ROW_NOTES[ident])
        else:
            assert ident in retained and row['current_hex'] == value.hex()
        row['review']['formatting'] = True
    draft.update(candidate_sha256=candidate, formatting_and_registration_pending=False, checked_story_format_guard=controls,
        observed_gameplay=live, direct_visual_review=viewed, shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'])
    validate_natural_dialogue_batch(draft)
    return stored, draft, {SC0: archive_sha}


publish = template.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index('    DOC.write_text'):publish.index('    prefix =')]
program = checked_text(publish, {
    'len(manifest["batches"]) == 928 and len(manifest["checks"]) == 263':
        'len(manifest["batches"]) == 930 and len(manifest["checks"]) == 265',
    'verified_ceuta_contract_routes_predecessor': 'verified_departure_numerals_predecessor',
    'previously_localized_records=45': 'previously_localized_records=20',
    'prose_revisions=25, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=20':
        'prose_revisions=9, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=11',
    'text_display_revisions=25': 'text_display_revisions=9',
    'initialized_Rafael_sailing_controls_lesson=True': 'initialized_Rafael_trade_choices_and_Arms_lesson=True',
    'rafael_sail_controls': 'rafael_trade_and_arms',
    'glob("sail_controls_staged_v*")': 'glob("staged_v*")',
    'Preserve the Rafael Sailing Controls ROM or reconstruction': 'Preserve the Rafael Trade and Arms ROM or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael trade and town-defense test candidate

The [local ROM](../../{ROM.as_posix()}) includes Julio’s revised trade lesson, Janus’s Arms advice, and all prior registered corrections.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Rafael’s trade and town-defense lessons

Nine revisions clarify trade expansion through Madeira, the availability of market share and the effect of commercial investment. Janus uses the established Arms, Palace and Governor’s Office names. His investment advice retains the expectation that Portuguese construction techniques will help the fleet raise Arms more cheaply. Eleven records retain their exact wording. All nine revised pages and both substitutions passed native and visual review. [Per-record ledger](../{REVIEW.as_posix()})

Three initialized emulator runs exercised both trade choices and Janus’s four replies. The original interpreter returned both choice indices and completed all three paths. All 18 unique dialogue panels and both captions matched their full glyph masks. Natural scenario activation and hardware testing remain open. [Replay proof](../{VERIFY.as_posix()}/live_display.json) · [Screen samples](../{VERIFY.as_posix()}/lesson_display.png)

Only B129 and B140 change. The clean-input patch rebuilds the candidate exactly. Six startup frames, 24 protected name getters and 49 focused tests passed. Two optional historical fixtures skipped. The ledger still credits 27,700 reviews with 276 shared keys open. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = template.env | globals()
exec(compile(program, __file__ + '::register', 'exec'), env)


if __name__ == '__main__':
    env['main']()
