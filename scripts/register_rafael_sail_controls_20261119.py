"""Register Rafael's sailing-controls lesson with exact release ancestry and display evidence."""

from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_rafael_sail_controls_replay_20261119 as live_check
from scripts import prepare_all_routes_promotion_20261111 as runtime
from scripts import register_rafael_ceuta_contract_routes_20261119 as parent
from scripts import review_rafael_sail_controls_20261119 as staged
from scripts import stage_inn_numerals_20261119 as shared_source
from scripts import verify_rafael_sail_controls_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base, native, workflow = parent.base, parent.native, parent.workflow
stage = SimpleNamespace(ROOT=staged.STAGED, ROM=staged.ROM, PROOF=staged.PROOF)
PROFILE = 'all-routes-rafael-sail-controls-v1-20261119'
ROOT = Path('out/rafael_sail_controls_registered_20261119_v1')
ROM = ROOT / 'Translation_DS_Rafael_Sail_Controls_20261119_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261119_rafael_sail_controls_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_rafael_sail_controls_20261119.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'registered_qa.xml'
verified = SimpleNamespace(PROOF=offline.PROOF, LIVE=live_check.PROOF)
CHECKPOINT = 'Rafael’s sailing-controls lesson and the conversation about Athens are registered after native review and an initialized emulator replay.'
SC0, COMMON = '/data/SC0.DK4', '/COMMON/MESFILE.DK4'
ROW_NOTES = {
    12: 'The explanation and complete invitation each fit one line with room for the maximum first name.',
    23: 'Top speed fits the opening line and the action of directing the Sail Handlers stays together.',
    26: 'The half-sail assurance, assignment and result read in three consecutive lines.',
    60: 'The conditional and complete Sail Handlers phrase stay together at the end.',
    107: 'Rafael’s acknowledgement and promise fit a single line.',
    128: 'The recollection reserves space for the maximum first name and the Athens request stays together.',
    137: 'Julio’s assent and reason fit a single line.',
    164: 'Rafael’s complete Athens question fits a single line.',
    180: 'Clau’s exclamation reserves space for the maximum first name and his reaction fits the next line.',
    207: 'The unusual goal-hunting joke fits a single line before Rafael reacts.',
}


def verify(registry, previous, viewed):
    stored, draft, live, layouts, startup = map(base.load, (stage.PROOF, staged.OUTPUT, verified.LIVE, verified.PROOF, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == live['candidate_sha256'] == layouts['candidate_sha256'] == startup['candidate_sha256']
    assert stored['predecessor_sha256'] == live['predecessor_sha256'] == previous['candidate_sha256']
    assert stored['manuscript_sha256'] == base.digest(staged.OUTPUT) and stored['whole_parent_inverse']
    assert layouts['stage_proof_sha256'] == base.digest(stage.PROOF) and layouts['previews'] == 41
    assert all(base.digest(p) == digest for proof in (live, startup) for p, digest in proof['evidence'].items())
    assert len(startup['exact_matching_frames']) == 6 and len(startup['original_protected_name_getters']) == 24
    assert startup['cold_boot'] and not startup['savestate'] and startup['complete_deployed_payload_exact']
    assert live['initialized_gameplay'] and not live['natural_activation'] and not live['hardware']
    assert live['original_end_command_executed'] and all(r['full_body_and_nameplate_match'] for r in live['panels'])
    assert viewed == {s['path']: s['sha256'] for s in layouts['sheets'] + live['sheets']}
    assert all(base.digest(p) == digest for p, digest in viewed.items())
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(key, 0)) for key in ('tests', 'failures', 'errors', 'skipped')] == [51, 0, 0, 2]
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()

    clean, before, after = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    old, new = map(native.files, (before, after))
    assert old.keys() == new.keys() and {p for p in old if old[p] != new[p]} == {SC0}
    arm = new[native.ARM]
    assert native.digest(arm) == previous['target_ARM9_sha256']
    runtime.verify_runtime(arm, previous)
    a, b = [native.IlnkContainer.parse(files[SC0]).blocks for files in (old, new)]
    assert stored['changed_blocks'] == {SC0: [128]}
    assert [i for i, (x, y) in enumerate(zip(a, b, strict=True)) if x != y] == [128]
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), new)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    after.replace_file(SC0, old[SC0])
    assert bytes(after.rom.save()) == parent.ROM.read_bytes()
    shared = shared_source.workflow
    directory = native.digest(arm[shared.DIRECTORY_OFFSET:shared.TABLE_OFFSET])
    entries = shared.owned_entries(new[COMMON], arm, directory)
    carry = base.load(parent.REVIEW)['shared_storage_scope']
    pending = base.load(parent.parent.parent.parent.parent.stage.PENDING)['records']
    assert len(pending) == 276
    assert all(r['current_reference'] == shared.reference(entries[r['message_ID']]) and
               r['current_hex'] == entries[r['message_ID']].text.hex() for r in pending)

    observed = {r['id']: r for r in live['panels']}
    page_proofs = {r['id']: r for r in layouts['revisions']}
    retained = set(layouts['retentions'])
    sha = native.digest(new[SC0])
    group, = stored['groups']
    commands = {i: c for c in group['commands'] for i in c['record_ids']}
    assert draft['counts'] == dict(prose=25, retention=20)
    assert observed.keys() | set(live['unvisited']) == commands.keys()
    assert len(page_proofs) == 25 and len(retained) == 20 and page_proofs.keys() | retained == commands.keys()
    for row in draft['records']:
        ident = row['id']
        command = commands[ident]
        at, raw = command['stored_offset'], bytes.fromhex(command['stored'])
        assert row['block'] == 128 and b[128][at:at + len(raw)] == raw
        value = raw[5:raw.index(0, 6)]
        assert value[0] == row['source_selector']
        row['registered_reference'] = dict(candidate_sha256=candidate, file_path=SC0, block=128,
            command_offset=at, offset=at + 5, archive_sha256=sha, exact_stored_hex=value.hex())
        if ident in observed:
            row['initialized_gameplay_verified'] = observed[ident]
        else:
            row['initialized_gameplay_unvisited'] = True
        if row['decision'] == 'revision':
            plan = group['plans'][ident]
            assert value.hex() == page_proofs[ident]['target_hex']
            warnings = {issue['code'] for issue in plan.get('diagnostics', ())}
            idx = row['source_reference']['record_index']
            assert warnings == ({'line-break-count'} if idx in ROW_NOTES else set())
            row['compiled_lines'] = plan['lines']
            if warnings:
                row['qa_waivers'] = ['line-break-count']
                row['qa_waiver_reason'] = ROW_NOTES[idx]
        else:
            assert ident in retained and row['current_hex'] == value.hex()
        row['review']['formatting'] = True
    draft.update(candidate_sha256=candidate, formatting_and_registration_pending=False, checked_story_format_guard=controls,
        observed_gameplay=live, direct_visual_review=viewed, shared_storage_scope=carry)
    validate_natural_dialogue_batch(draft)
    return stored, draft, {SC0: sha}


publish = parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index('    DOC.write_text'):publish.index('    prefix =')]
program = checked_text(publish, {
    'len(manifest["batches"]) == 927 and len(manifest["checks"]) == 262':
        'len(manifest["batches"]) == 928 and len(manifest["checks"]) == 263',
    'verified_voyage_ceuta_predecessor': 'verified_ceuta_contract_routes_predecessor',
    'previously_localized_records=32': 'previously_localized_records=45',
    'prose_revisions=13, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=19':
        'prose_revisions=25, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=20',
    'text_display_revisions=13': 'text_display_revisions=25',
    'ordinary_Rafael_Ceuta_docking_trade_and_sea_routes=True': 'initialized_Rafael_sailing_controls_lesson=True',
    'natural_activation=True, hardware=False': 'natural_activation=False, hardware=False',
    'rafael_ceuta_contract_routes': 'rafael_sail_controls',
    'Preserve the Rafael Ceuta Contract and Routes ROM or reconstruction': 'Preserve the Rafael Sailing Controls ROM or reconstruction',
    'glob("staged_v*") if directory != stage.ROOT': 'glob("sail_controls_staged_v*")',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael sailing-controls test candidate

The [local ROM](../../{ROM.as_posix()}) includes Julio’s revised sail and anchor instructions, the conversation about Athens, and all prior registered fixes.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Rafael’s sailing controls and the Athens conversation

The 45 decisions cover Julio’s explanations of full sail, half sail, anchoring, trimming and the promise to Hayreddin. Twenty-five revisions preserve the original A/B and L/R controls and keep related instructions together. Twenty rows retain their exact wording for individual reasons. All 25 revised pages passed native bounds and glyph checks. All 41 previews, including maximum-width first names, were reviewed visually. [Per-record ledger](../{REVIEW.as_posix()})

The emulator replay used the original New Game prelude and the exact lesson commands in an isolated test entry. It verified {len(draft['observed_gameplay']['panels'])} complete dialogue panels and ran the original end command. The {len(draft['observed_gameplay']['unvisited'])} unvisited records are identified in the ledger. The lesson’s natural entry and hardware display remain unverified. [Replay proof](../{VERIFY.as_posix()}/live_display.json) · [Gameplay samples](../{VERIFY.as_posix()}/lesson_display.png)

The clean-input patch reconstructs the candidate byte for byte. Six startup frames, 24 protected name getters and 49 focused tests passed. Two optional historical fixtures skipped. The ledger remains at 27,700 credited reviews and 276 open shared entries. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register', 'exec'), env)


if __name__ == '__main__':
    env['main']()
