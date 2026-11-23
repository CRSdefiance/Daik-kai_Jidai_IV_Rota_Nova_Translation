"""Register the verified swimmer, ship leak and Square replies cumulatively."""

from pathlib import Path
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_compatible_swimmer_leak_square_20261120 as game
from scripts import register_madeira_resupply_price_20261120 as parent
from scripts import stage_madeira_resupply_numerals_20261120 as price
from scripts import stage_swimmer_leak_square_dialogue_20261120 as batch
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
stage = SimpleNamespace(ROOT=price.ROOT, ROM=price.ROM, PROOF=game.STORED)
PROFILE = 'all-routes-swimmer-leak-square-dialogue-v1-20261120'
ROOT = Path('out/swimmer_leak_square_dialogue_registered_20261120_v1')
ROM = ROOT / 'Translation_DS_Swimmer_Leak_Square_20261120_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261120_swimmer_leak_square_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_swimmer_leak_square_registered_20261120.md')
STARTUP, QA = stage.ROOT / 'startup_against_registered_price.json', stage.ROOT / 'qa.xml'
STARTUP_CAPTURE = price.ROOT / 'own_startup_verification.json'
REBASE = price.ROOT / 'pending_dialogue_rebase.json'
VISUAL = stage.ROOT / 'visual_review.json'
NATIVE_SHEET = batch.ROOT / 'portrait_sheet_01.png'
verified = SimpleNamespace(PROOF=stage.PROOF, LIVE=game.PROOF)
CHECKPOINT = 'Registered seven wording revisions and one wrap fix across the mermaid sighting, ship leaks and Square business replies.'


def verify(registry, previous, viewed):
    stored, played, price_stage, rebase, earlier_boot = map(base.load, (stage.PROOF, game.PROOF, price.PROOF, REBASE, STARTUP_CAPTURE))
    candidate = base.digest(stage.ROM)
    assert candidate == played['candidate_sha256'] == price_stage['candidate_sha256'] == rebase['combined_sha256']
    assert stored['candidate_sha256'] == price_stage['staged_parent_sha256'] == played['previous_square_sha256']
    assert base.digest(parent.ROM) == previous['candidate_sha256'] == rebase['price_fix_candidate_sha256']
    assert rebase['whole_price_fix_candidate_inverse']
    assert base.digest(batch.CLEAN) == previous['clean_input_sha256'] == stored['clean_input_sha256']
    assert stored['complete_inverse'] and stored['verified_entries'] == 3668
    assert {int(key) for key in stored['allocations']} == batch.EDITS.keys()
    assert [r['message_ID'] for r in played['mermaid']['observed']] == [448, 449]
    assert [r['message_ID'] for r in played['leak']['observed']] == [573]
    assert played['revised_emulator_samples'] == [573, 682, 687]
    assert played['fresh_leak_fixture_and_inherited_mermaid_gameplay'] and not played['natural_encounter_selection']
    assert not played['hardware'] and not played['exact_current_sea_ROM_play']
    assert all(base.digest(path) == sha for path, sha in stored['source_proofs'].items())
    for row, keys in ((played, ('square_evidence',)),
                      (played['mermaid'], ('earlier_proof',)),
                      (played['leak'], ('fixture_program', 'capture_report', 'earlier_report'))):
        for key in keys:
            assert base.digest(row[key]) == row[key + '_sha256']
    assert viewed == {str(p): base.digest(p) for p in (NATIVE_SHEET, game.SHEET, batch.ROOT / 'square_gameplay.png')}
    assert [(Path(row['path']), row['sha256']) for row in stored['contact_sheets']] == [(NATIVE_SHEET, viewed[str(NATIVE_SHEET)])]
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(key, 0)) for key in ('tests', 'failures', 'errors', 'skipped')] == [32, 0, 0, 2]
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()

    clean, old, new = map(base.NdsImage.open, (batch.CLEAN, parent.ROM, stage.ROM))
    before, after = map(batch.files, (old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {batch.COMMON}
    arm, common = after[batch.ARM], after[batch.COMMON]
    assert native.digest(arm) == price_stage['target_ARM9_sha256'] == previous['target_ARM9_sha256']
    assert native.digest(common) == stored['target_COMMON_sha256']
    new.replace_file(batch.COMMON, before[batch.COMMON])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(batch.files(clean), after)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    directory = native.digest(arm[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET])
    entries = batch.owned_entries(common, arm, directory)
    pending = base.load(parent.parent.PENDING)['records']
    assert len(pending) == 276
    assert all(batch.reference(entries[row['message_ID']]) == row['current_reference']
               and entries[row['message_ID']].text.hex() == row['current_hex'] for row in pending)
    draft = {key: stored[key] for key in ('source_proofs', 'translation_policy',
                                         'target_locale', 'encoder', 'review_gates', 'records')}
    assert len(draft['records']) == 34 and sum(len(r['native_displays']) for r in draft['records']) == 54
    assert sum(row['decision'] == 'revision' for row in draft['records']) == 7
    assert [row['message_ID'] for row in draft['records'] if row['decision'] == 'wrap revision'] == [445]
    for row in draft['records']:
        entry = entries[row['message_ID']]
        assert row['staged_hex'] == entry.text.hex() and row['staged_reference'] == batch.reference(entry)
        row['registered_reference'] = row['staged_reference'] | {'candidate_sha256': candidate}
        row['review']['formatting'] = True
    startup_base = parent.parent.startup_proof
    startup_report = Path(earlier_boot['exact_matching_frames'][0]['path']).parent / 'capture_report.json'
    startup = FunctionType(startup_base.__code__, startup_base.__globals__ |
                           {'STARTUP': STARTUP, 'STARTUP_CAPTURE': startup_report})
    startup(previous, candidate, arm)
    draft.update(candidate_sha256=candidate, checked_story_format_guard=controls, direct_visual_review=viewed, observed_gameplay=played,
                 preserved_pending_shared_rows=276, new_contextual_credit=0,
                 shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'])
    validate_natural_dialogue_batch(draft)
    return stored, draft, {batch.COMMON: native.digest(common)}


publish = parent.parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index('    DOC.write_text'):publish.index('    prefix =')]
program = checked_text(publish, {
    'len(manifest["batches"]) == 935 and len(manifest["checks"]) == 270':
        'len(manifest["batches"]) == 937 and len(manifest["checks"]) == 272',
    'verified_captain_name_latin_predecessor=predecessor, amsterdam_tavern_release=str(REVIEW)':
        'verified_madeira_resupply_price_predecessor=predecessor, swimmer_leak_square_release=str(REVIEW)',
    'release_stack_before_amsterdam_tavern.json': 'release_stack_before_swimmer_leak_square.json',
    'release_stack_with_amsterdam_tavern.json': 'release_stack_with_swimmer_leak_square.json',
    'registered_amsterdam_tavern_and_complete_parent_inverse': 'registered_swimmer_leak_square_and_complete_parent_inverse',
    'manifest["amsterdam_tavern_pipeline"]': 'manifest["swimmer_leak_square_pipeline"]',
    'stage.PROOF, STARTUP, QA, verified.PROOF, verified.LIVE, args.visual_review':
        'stage.PROOF, STARTUP, QA, verified.LIVE, game.SQUARE, game.replay.PROOF, REBASE, args.visual_review',
    'if row["decision"] == "revision" and row["id"] not in ids:':
        'if row["decision"] != "retention" and row["id"] not in ids:',
    'ledger["amsterdam_tavern_editorial_20261120"]': 'ledger["swimmer_leak_square_dialogue_20261120"]',
    'previously_localized_records=11': 'previously_localized_records=34',
    'prose_revisions=2, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=9':
        'prose_revisions=7, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=26',
    'ordinary_Amsterdam_drink_offer_both_responses=True, ordinary_tavern_rumors=True':
        'initialized_revised_leak_fixture_and_Square=True, inherited_mermaid_sequence=True',
    'natural_activation=True, hardware=False': 'natural_activation=False, hardware=False',
    'stage.ROOT.with_name("amsterdam_tavern_editorial_20261120_v1") / "candidate.nds"':
        'batch.ROM, batch.ROOT/"clean_rebuilt.nds", batch.ROOT.with_name("swimmer_leak_square_dialogue_20261120_v1")/"candidate.nds", game.replay.ROM',
    'Preserve the Amsterdam Tavern ROM or reconstruction': 'Preserve the swimmer, leak and Square dialogue ROM or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Swimmer, ship leak and Square dialogue candidate

The [local ROM](../../{ROM.as_posix()}) improves phrase breaks and dialogue in three shared encounters.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Swimmer, ship leak and Square dialogue

Reviewed 34 records across the unidentified swimmer and mermaid reaction, the flagship and other ship leak reports, and Square shopkeepers’ business replies. Seven wordings changed, one swimmer line was rewrapped, and 26 entries have individual retention reasons. The shipwright’s observations still distinguish confirmed, likely and secondhand reports. The shopkeeper’s concerns about war and the lost regular ship now read as complete thoughts. [Clean, previous and registered references](../{REVIEW.as_posix()})

All 54 native cases passed, including the original named-ship substitutions. Every revised page received direct visual review. The revised flagship warning and sailing return passed a fresh replay using the earlier working voyage with one substituted dialogue record and the original temporary event selector. The two retained mermaid lines match the earlier emulator capture and its port sighting. Both revised Square replies and menu returns passed replay with supplied town conditions. All changed text received native checks on a build whose only later code change is the separate registered resupply price call. The alternate voices received offline checks. Natural encounter selection and hardware remain open. [Native pages](../{(VERIFY / NATIVE_SHEET.name).as_posix()}) · [Sea gameplay](../{(VERIFY / game.SHEET.name).as_posix()}) · [Square gameplay](../{(VERIFY / "square_gameplay.png").as_posix()})

Six startup holds, 24 protected name getters and 30 focused tests passed. Two optional historical tests skipped. The clean-input patch rebuilds the ROM exactly. The ledger still credits 27,700 reviews, with 276 mapped shared records open. [Registered candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.parent.env | globals()
exec(compile(program, __file__ + '::register', 'exec'), env)


if __name__ == '__main__':
    env['main']()
