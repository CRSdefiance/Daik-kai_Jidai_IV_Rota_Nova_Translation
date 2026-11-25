"""Register the verified resupply digit change on its own cumulative layer."""

from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_madeira_resupply_numerals_20261120 as price
from scripts import register_amsterdam_tavern_editorial_20261120 as parent
from scripts import stage_madeira_resupply_numerals_20261120 as build
from scripts.check_swimmer_leak_square_dialogue_20261120 import one_frame, ram_at
from scripts.source_locked_derivation_v5118 import checked_text


batch = build.batch
base, native = parent.base, parent.native
stage = SimpleNamespace(ROOT=build.PRICE_ONLY, ROM=build.PRICE_ONLY/build.ROM.name,
                        PROOF=build.PRICE_ONLY/build.PROOF.name, ARM=batch.ARM)
PROFILE = 'all-routes-madeira-resupply-price-v1-20261120'
ROOT = Path('out/madeira_resupply_price_registered_20261120_v1')
ROM = ROOT / 'Translation_DS_Madeira_Resupply_Price_20261120_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261120_madeira_resupply_price_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_madeira_resupply_price_registered_20261120.md')
STARTUP = stage.ROOT / 'own_startup_verification.json'
QA = stage.ROOT / 'qa.xml'
LIVE = stage.ROOT / 'standalone_gameplay.json'
VISUAL = stage.ROOT / 'visual_review.json'
CAPTURE = Path('E:/Rota Nova translations/Generated/work/madeira_resupply_price_only_20261120_v1/capture/capture_report.json')
STARTUP_CAPTURE = Path('E:/Rota Nova translations/Generated/work/madeira_resupply_price_only_20261120_v1_boot'
                       '/release_startup/capture/capture_report.json')
RUNTIME_ID = 'DK4_PORT_RESUPPLY_PRICE_ASCII_DIGITS'
CHECKPOINT = 'The standard paid Port resupply quote uses regular-width digits and is registered after the Madeira purchase and departure replay.'


def gameplay(arm, candidate):
    current, combined = map(base.load, (CAPTURE, price.CAPTURE))
    assert current['ROM_sha256'] == candidate
    assert combined['ROM_sha256'] == base.load(build.PROOF)['candidate_sha256']
    assert current['cold_boot'] and not current['savestate_loaded'] and not current['callback_errors']
    assert current['frames'] == combined['frames'] == 15107
    for key in ('core_options', 'scripted_input_schedule'):
        assert current[key] == combined[key]
    for report in (current, combined):
        save = report['battery_save_preloaded']
        assert save['copied_byte_exact_before_cold_boot'] and base.digest(save['source']) == save['source_sha256']
    assert all(value['frame'] in (8327, 9627) for value in current['synthetic_condition_fixtures'])
    frames = sorted({row['frame'] for row in current['frames_captured']})
    assert frames == sorted({row['frame'] for row in combined['frames_captured']})
    matches = []
    for frame in frames:
        new, old = [one_frame(report, frame)[0] for report in (current, combined)]
        assert new['framebuffer_sha256'] == old['framebuffer_sha256'], frame
        matches.append(new)
    at = unpack_from('<I', arm, 0x54450)[0] - build.BASE
    a, b = [ram_at(report, 10427) for report in (current, combined)]
    assert all(raw[at:at+256].split(b'\0', 1)[0] == b' Want to resupply for 260 gold?' for _, raw in (a, b))
    port = base.load(price.LIVE)
    assert port['exact_speaker_choices_and_return_frames'] and port['observed_gold_after'] == 6480
    result = dict(candidate_sha256=candidate, original_amount=260, paid_amount=260,
                  exact_matching_frames=matches, matching_quote_RAM=a[0],
                  registered_candidate_gameplay=str(CAPTURE), registered_candidate_gameplay_sha256=base.digest(CAPTURE),
                  combined_replay_dependency=str(price.LIVE), combined_replay_sha256=base.digest(price.LIVE),
                  original_purchase_and_return_to_sailing=True, initialized_location=True, hardware=False)
    if LIVE.exists():
        assert base.load(LIVE) == result
    else:
        base.save(LIVE, result)
    return result


def verify(registry, previous, viewed):
    staged, model, combined = map(base.load, (stage.PROOF, price.NATIVE, build.PROOF))
    candidate = base.digest(stage.ROM)
    assert staged['price_only'] and staged['candidate_sha256'] == candidate
    assert staged['immediate_parent_sha256'] == previous['candidate_sha256'] == base.digest(parent.ROM)
    assert staged['clean_input_sha256'] == previous['clean_input_sha256'] == base.digest(batch.CLEAN)
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()
    assert base.digest(stage.ROOT / 'translation.xdelta') == staged['clean_input_patch_sha256']
    assert viewed == {str(path): base.digest(path) for path in (build.ROOT/'portrait_sheet_01.png', build.ROOT/'resupply_comparison.png')}
    assert model['candidate_sha256'] == combined['candidate_sha256'] == base.digest(build.ROM)
    assert len(model['tested_ring_cases']) == 320 and len(model['tested_natural_layouts']) == 10
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(key, 0)) for key in ('tests', 'failures', 'errors', 'skipped')] == [32, 0, 0, 2]
    assert base.digest(build.HELPER_PROOF) == staged['helper_proof_sha256']
    clean, prior, deployed, combined_rom = map(base.NdsImage.open, (batch.CLEAN, parent.ROM, stage.ROM, build.ROM))
    before, after = map(batch.files, (prior, deployed))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {batch.ARM}
    arm, common = after[batch.ARM], after[batch.COMMON]
    assert native.digest(arm) == combined['target_ARM9_sha256'] == staged['target_ARM9_sha256']
    assert arm == combined_rom.read_file(batch.ARM)
    assert native.digest(common) == staged['target_COMMON_sha256'] == previous['target_COMMON_sha256']
    assert build.patch(before[batch.ARM], clean.read_file(batch.ARM)) == (arm, staged['original_call'])
    deployed.replace_file(batch.ARM, before[batch.ARM])
    assert bytes(deployed.rom.save()) == parent.ROM.read_bytes()
    directory = native.digest(arm[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET])
    current = batch.owned_entries(common, arm, directory)
    pending = base.load(parent.PENDING)['records']
    assert len(pending) == 276 and all(batch.reference(current[r['message_ID']]) == r['current_reference']
               and current[r['message_ID']].text.hex() == r['current_hex'] for r in pending)
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(batch.files(clean), after)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    source = batch.common_message_entries(clean.read_file(batch.COMMON), clean.read_file(batch.ARM))
    s, c = source[49], current[49]
    assert batch.reference(s) == model['source_reference'] and batch.reference(c) == model['current_reference']
    assert s.text.hex() == model['source_hex'] and c.text.hex() == model['current_hex']
    assert c.text.count(b'%s') == s.text.count(b'%s') == 1
    checked = gameplay(arm, candidate)
    startup = FunctionType(parent.startup_proof.__code__, parent.startup_proof.__globals__ |
                           {'STARTUP': STARTUP, 'STARTUP_CAPTURE': STARTUP_CAPTURE})
    startup(previous, candidate, arm)
    row = dict(id='COMMON_MESSAGE_49', message_ID=49, file_path=batch.COMMON, speaker='Port Worker',
               context='The Port Worker quotes the full cost before the captain chooses Yes or No.',
               source_meaning='The port worker offers to restock the fleet for the quoted number of gold coins.',
               localization_note=model['reason'], clean_Japanese=s.text.decode('cp932'),
               english=c.text.decode('ascii'), source_reference=batch.reference(s), current_reference=batch.reference(c),
               source_hex=s.text.hex(), current_hex=c.text.hex(), registered_reference=batch.reference(c) |
               {'candidate_sha256': candidate}, decision='retention', review=dict.fromkeys(batch.GATES, True))
    draft = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
                 review_gates=batch.GATES, records=[row], candidate_sha256=candidate,
                 shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'],
                 checked_story_format_guard=controls, native_price=model, observed_gameplay=checked,
                 complete_quote_dependency_match=True, new_contextual_credit=0)
    validate_natural_dialogue_batch(draft)
    return staged, draft, {batch.ARM: native.digest(arm)}


publish = parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index('    DOC.write_text'):publish.index('    prefix =')]
program = checked_text(publish, {
    'len(manifest["batches"]) == 935 and len(manifest["checks"]) == 270':
        'len(manifest["batches"]) == 936 and len(manifest["checks"]) == 271',
    'verified_captain_name_latin_predecessor=predecessor, amsterdam_tavern_release=str(REVIEW)':
        'verified_amsterdam_tavern_predecessor=predecessor, madeira_resupply_price_release=str(REVIEW)',
    'release_stack_before_amsterdam_tavern.json': 'release_stack_before_resupply_price.json',
    'release_stack_with_amsterdam_tavern.json': 'release_stack_with_resupply_price.json',
    'registered_amsterdam_tavern_and_complete_parent_inverse': 'registered_madeira_price_and_complete_parent_inverse',
    'manifest["amsterdam_tavern_pipeline"]': 'manifest["madeira_resupply_price_pipeline"]',
    'stage.PROOF, STARTUP, QA, verified.PROOF, verified.LIVE, args.visual_review':
        'stage.PROOF, STARTUP, QA, price.NATIVE, price.LIVE, LIVE, args.visual_review',
    '''    ids = manifest["changed_records"][tavern.COMMON]
    for row in draft["records"]:
        if row["decision"] == "revision" and row["id"] not in ids:
            ids.append(row["id"])
''': '''    ids = manifest["changed_records"][stage.ARM]
    assert RUNTIME_ID not in ids
    ids.append(RUNTIME_ID)
''',
    'native_display_sha256=base.digest(verified.PROOF)': 'native_display_sha256=base.digest(price.NATIVE)',
    'owned_shared_allocations=stored["allocations"], target_COMMON_sha256=archives[tavern.COMMON]':
        'owned_resupply_price_call=stored["original_call"], target_ARM9_sha256=archives[stage.ARM]',
    'changed_components=1, target_COMMON_sha256=archives[tavern.COMMON]':
        'changed_components=1, target_ARM9_sha256=archives[stage.ARM]',
    'ARM9_sha256=previous["target_ARM9_sha256"], MESFILE_sha256=archives[tavern.COMMON]':
        'ARM9_sha256=archives[stage.ARM], MESFILE_sha256=previous["target_COMMON_sha256"]',
    'ledger["amsterdam_tavern_editorial_20261120"]': 'ledger["madeira_resupply_price_20261120"]',
    'previously_localized_records=11': 'previously_localized_records=1',
    'prose_revisions=2, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=9':
        'prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1',
    'text_display_revisions=0': 'text_display_revisions=1',
    'ordinary_Amsterdam_drink_offer_both_responses=True, ordinary_tavern_rumors=True':
        'initialized_Madeira_ordinary_purchase_and_departure=True',
    'natural_activation=True, hardware=False': 'natural_activation=False, hardware=False',
    'stage.ROOT.with_name("amsterdam_tavern_editorial_20261120_v1") / "candidate.nds"':
        'build.ROM, build.ROOT/"clean_rebuilt.nds", batch.ROM, batch.ROOT/"clean_rebuilt.nds"',
    'Preserve the Amsterdam Tavern ROM or reconstruction': 'Preserve the Madeira resupply price ROM or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Madeira resupply price candidate

The [local ROM](../../{ROM.as_posix()}) displays the paid Port resupply price in regular-width digits.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 {candidate} byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Madeira resupply price registered

The Port Worker’s standard paid resupply quote now displays regular-width digits. The original price substitution, speaker, choices and payment all carried forward. The original call and its other branches remain bound to the clean Japanese. [Exact decision and gameplay](../{REVIEW.as_posix()})

The registered candidate reproduced the full Madeira purchase and departure from the copied voyage after an initialized approach. All matching frames, native digit cases, protected startup getters and the exact patch rebuild passed. The combined research ROM preserves the eight additional dialogue changes while their sea encounter replays remain open. [Candidate and patch](../{PACKAGE.as_posix()}/README.md) · [Pending dialogue](editorial_swimmer_leak_square_20261120.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register', 'exec'), env)


if __name__ == '__main__':
    env['main']()
