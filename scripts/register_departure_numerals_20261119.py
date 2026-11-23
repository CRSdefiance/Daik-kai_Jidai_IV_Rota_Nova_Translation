"""Register the verified departure numeral correction on the cumulative ROM."""

from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_departure_numerals_gameplay_20261119 as live
from scripts import check_departure_numerals_native_20261119 as offline
from scripts import replay_departure_numerals_20261119 as replay
from scripts import stage_departure_numerals_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native, parent = stage.base, stage.native, stage.parent
PROFILE = 'all-routes-departure-numerals-v1-20261119'
ROOT = Path('out/departure_numerals_registered_20261119_v1')
ROM = ROOT / 'Translation_DS_Departure_Numerals_20261119_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261119_departure_numerals_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_departure_numerals_20261119.md')
STARTUP, QA = replay.STARTUP, stage.ROOT / 'registered_qa.xml'
verified = SimpleNamespace(PROOF=offline.PROOF, LIVE=live.PROOF)
CHECKPOINT = 'The sailing estimate and departure date now use regular digits, verified during Rafael’s ordinary departure from Ceuta.'


def verify(registry, previous, viewed):
    stored, draft, played, boot = map(base.load, (stage.PROOF, verified.PROOF, verified.LIVE, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == draft['candidate_sha256'] == played['candidate_sha256'] == boot['candidate_sha256']
    assert stored['predecessor_sha256'] == draft['predecessor_sha256'] == played['predecessor_sha256'] == previous['candidate_sha256']
    assert stored['entire_parent_inverse'] and len(draft['executed_num_cases']) == 1728
    assert draft['modeled_date_sky_town_combinations'] == 100440
    assert all(base.digest(p) == sha for receipt in (stored, draft, played, boot) for p, sha in receipt['evidence'].items())
    assert all(played[key] for key in ('ordinary_existing_save', 'dismissal_input', 'later_sailing_and_fog_frame'))
    assert not played['hardware'] and len(played['exact_other_frames']) == 6
    assert [r['message_ID'] for r in played['panels'] if r['exact_live_buffer_and_pixels']] == [85, 86]
    assert viewed == {s['path']: s['sha256'] for s in draft['sheets'] + played['sheets']}
    assert all(base.digest(p) == sha for p, sha in viewed.items())
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [51, 0, 0, 2]
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()

    clean, before, after = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    old, new = map(native.files, (before, after))
    assert old.keys() == new.keys() and {p for p in old if old[p] != new[p]} == {stage.ARM}
    arm = new[stage.ARM]
    assert native.digest(arm) == stored['target_ARM9_sha256']
    recompiled, calls = stage.recompile(old[stage.ARM], clean.read_file(stage.ARM), bytes.fromhex(stored['helper_hex']))
    assert arm == recompiled and calls == stored['original_calls']
    stage.verify_runtime(arm, previous)
    after.replace_file(stage.ARM, old[stage.ARM])
    assert bytes(after.rom.save()) == parent.ROM.read_bytes()
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), new)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    assert [r['message_ID'] for r in draft['records']] == [85, 86]
    w = stage.inn.stage.workflow
    directory = native.digest(arm[w.DIRECTORY_OFFSET:w.TABLE_OFFSET])
    current = w.owned_entries(new[stage.COMMON], arm, directory)
    pending = base.load(parent.parent.parent.parent.parent.parent.stage.PENDING)['records']
    assert len(pending) == 276
    assert all(w.reference(current[r['message_ID']]) == r['current_reference'] and
               current[r['message_ID']].text.hex() == r['current_hex'] for r in pending)
    for record, panel in zip(draft['records'], played['panels'], strict=True):
        message = record['message_ID']
        assert record['decision'] == 'retention' and record['current_hex'] == current[message].text.hex()
        assert record['current_reference'] == w.reference(current[message])
        assert panel['message_ID'] == message
        record['ordinary_gameplay_verified'] = panel
    draft.update(observed_gameplay=played, checked_story_format_guard=controls, direct_visual_review=viewed,
                 shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'], new_contextual_credit=0,
                 target_ARM9_sha256=native.digest(arm))
    validate_natural_dialogue_batch(draft)
    return stored, draft, {stage.ARM: native.digest(arm)}


publish = parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index('    DOC.write_text'):publish.index('    prefix =')]
program = checked_text(publish, {
    'len(manifest["batches"]) == 928 and len(manifest["checks"]) == 263':
        'len(manifest["batches"]) == 929 and len(manifest["checks"]) == 264',
    'verified_ceuta_contract_routes_predecessor': 'verified_rafael_sail_controls_predecessor',
    'previously_localized_records=45': 'previously_localized_records=2',
    'prose_revisions=25, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=20':
        'prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=2',
    'text_display_revisions=25': 'text_display_revisions=2',
    'initialized_Rafael_sailing_controls_lesson=True': 'ordinary_Ceuta_departure_notices_and_dismissal=True',
    'natural_activation=False, hardware=False': 'natural_activation=True, hardware=False',
    'rafael_sail_controls_release=str(REVIEW)': 'departure_numerals_release=str(REVIEW), departure_numeral_call_sites=stored["original_calls"]',
    'rafael_sail_controls': 'departure_numerals',
    'owned_story_records=[row["registered_reference"] for row in draft["records"] if row["decision"] == "revision"], target_ARM9_sha256=previous["target_ARM9_sha256"]':
        'owned_runtime_calls=stored["original_calls"], target_ARM9_sha256=archives[stage.ARM]',
    'changed_components=1, target_ARM9_sha256=previous["target_ARM9_sha256"]': 'changed_components=1, target_ARM9_sha256=archives[stage.ARM]',
    "ARM9_sha256=previous[\"target_ARM9_sha256\"], MESFILE_sha256": 'ARM9_sha256=archives[stage.ARM], MESFILE_sha256',
    'glob("sail_controls_staged_v*")': 'glob("staged_v*")',
    'Preserve the Rafael Sailing Controls ROM or reconstruction': 'Preserve the departure numeral ROM or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Departure numerals test candidate

The [local ROM](../../{ROM.as_posix()}) uses regular dialogue digits in the sailing estimate and departure date and includes all prior registered fixes.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Departure notice numerals

Both Port notices retain their wording and original argument order. The sailing estimate’s count and the departure notice’s month and day use the installed regular-digit converter. The sky and port-name arguments and original three-line date layout remain exact. The only ROM changes are the three caller instructions. All 1,728 isolated number cases preserved the original return pointers, values, and adjacent bytes. Seven native displays passed exact glyph and bounds checks and direct visual review. [Per-record references and native proof](../{REVIEW.as_posix()})

An ordinary Ceuta replay displayed “Sailing days left: about 20.” and “1/23” in the regular dialogue font. Both live buffers and the complete displayed text matched the expected bytes and native raster. The other six held frames matched the earlier replay, including the departure menu, the missing Surveyor warning and the fog interruption after dismissing the date. Hardware testing remains open. [Before and after](../{VERIFY.as_posix()}/departure_digit_comparison.png) · [Ordinary replay](../{VERIFY.as_posix()}/ordinary_departure_verification.json)

The clean-input patch rebuilds the candidate byte for byte. Six startup holds, 24 protected name getters and 49 focused tests passed. Two optional historical fixtures skipped. The ledger remains at 27,700 credited reviews and 276 shared keys open. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register', 'exec'), env)


if __name__ == '__main__':
    env['main']()
