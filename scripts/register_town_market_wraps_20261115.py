"""Register the verified town and Market text on the existing cumulative release."""

from hashlib import sha256
from inspect import getsource
from pathlib import Path
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import checkpoint_town_market_wraps_20261115 as live
from scripts import register_tavern_influence_20261114 as publisher
from scripts import stage_town_market_wraps_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-town-market-wraps-v1-20261115'
ROOT = Path('out/town_market_wraps_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Town_Market_Wraps_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_town_market_wraps_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_town_market_wraps_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'repository_qa_verified.xml'
NATIVE_SHEET = stage.ROOT / 'portrait_sheet_01.png'
VIEWED_NATIVE = 'c0dc980f66c25bd7577d6de00cbe45d08edb4773538241830fb268784e6f66c6'
CHECKPOINT = 'The traveling promoter, specialty request, and Market warnings are reviewed, with four changes registered.'
EDITED = sorted(stage.PHRASES)


def digest(payload):
    return sha256(payload).hexdigest()


def verify(prior, guard):
    storage, review, gameplay, startup = map(base.load, (stage.STORED, stage.MANUSCRIPT, live.OUTPUT, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == storage['candidate_sha256'] == review['candidate_sha256'] == startup['candidate_sha256']
    assert candidate == gameplay['candidate_sha256']
    assert base.digest(parent.ROM) == prior['candidate_sha256'] == storage['previous_sha256'] == review['previous_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256'] == review['clean_sha256']
    assert base.digest(stage.MANUSCRIPT) == storage['manuscript_sha256']
    assert storage['whole_parent_inverse'] and storage['preserved_entries'] == 3664
    assert sorted(map(int, storage['allocations'])) == EDITED
    assert len(review['records']) == 12 and len(review['specialty_title_arguments']) == 25
    sheet, = storage['sheets']
    assert Path(sheet['path']) == NATIVE_SHEET and base.digest(NATIVE_SHEET) == sheet['sha256'] == VIEWED_NATIVE
    assert len(sheet['messages']) == 8 and storage['changed_native_pages'] == len(EDITED)
    assert gameplay['observed_changed_keys'] == [739, 743, 748] and gameplay['offline_only_changed_keys'] == [749]
    assert len(gameplay['complete_holds']) == 9 and len(gameplay['transitions']) == 3
    assert base.digest(live.SHEET) == gameplay['sheet_sha256']
    assert startup['cold_boot'] and not startup['savestate'] and startup['complete_deployed_payload_exact']
    assert len(startup['exact_matching_frames']) == 6 and len(startup['original_protected_name_getters']) == 24
    for bundle in (gameplay, startup):
        assert all(base.digest(path) == sha for path, sha in bundle['evidence'].items())
    tests, = ElementTree.parse(QA).iter('testsuite')
    assert tuple(int(tests.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')) == (40, 0, 0, 0)
    old, new = map(base.NdsImage.open, (parent.ROM, stage.ROM))
    before, after = map(stage.files, (old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {stage.COMMON}
    publisher.verify_runtime(after[stage.ARM], prior)
    assert digest(after[stage.COMMON]) == storage['target_COMMON_sha256']
    checked = bind_registered_story_percent_guard(guard)(stage.files(base.NdsImage.open(stage.CLEAN)), after)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    new.replace_file(stage.COMMON, before[stage.COMMON])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()

    rows = review['records']
    assert sorted(row['message_ID'] for row in rows if row['decision'] != 'retention') == EDITED
    for row in rows:
        row['review']['formatting'] = True
        row['registered_reference'] = row['staged_reference'] | dict(exact_stored_hex=row['staged_hex'], candidate_sha256=candidate)
    document = review | dict(checked_story_format_guard=checked, observed_gameplay=gameplay, new_editorial_credit=0,
                             reviewed_sheet_sha256=VIEWED_NATIVE, direct_visual_review_complete=True)
    validate_natural_dialogue_batch(document)
    return storage, document


def update_ledger(ledger, release, sha, checkpoint):
    pending = ledger['pending_shared_consumer_checkpoint_20261114']
    assert pending['remaining_total'] == 276 and pending['candidate_sha256'] == release['predecessor']['candidate_sha256']
    assert not set(pending['remaining_legacy_keys']).intersection(stage.NUMBERS)
    pending['candidate_sha256'] = sha
    ledger['current_integrated_candidate'].update(path=str(ROM), sha256=sha, profile=PROFILE, patch=str(PATCH),
        patch_sha256=release['patch_sha256'], manifest=str(MANIFEST), manifest_sha256=release['manifest_sha256'],
        MESFILE_sha256=release['target_COMMON_sha256'], registered_release_verification=str(RELEASE))
    ledger['latest_checkpoint'] = checkpoint
    ledger['town_market_wraps_20261115'] = dict(review=str(REVIEW), release=str(RELEASE), revised_existing_keys=EDITED,
        retained_existing_keys=sorted(set(stage.NUMBERS) - set(EDITED)), new_dialogue_credit=0, remaining_mapped_shared_records=276)


def main():
    source = getsource(publisher.main)
    start = source.index('    ledger["current_integrated_candidate"].update(')
    end = source.index('    write_pending(ledger_tmp,encode_ledger(ledger))', start)
    source = source[:start] + '    update_ledger(ledger, release, sha, checkpoint)\n' + source[end:]
    start = source.index('    base.replace_checked(DOC,f"""')
    end = source.index('""".encode())', start) + len('""".encode())')
    document = '''    base.replace_checked(DOC, f"""# Town and Market dialogue wraps

The [registered review](../{REVIEW.as_posix()}) covers twelve lines from the traveling promoter, the local specialty request, and the Market. The promoter asks directly for a ride to another town square. The trader's investment refusal keeps the surprise, apology, and invitation to come back. Both are one line shorter. The specialty thank-you and full cargo warning preserve their wording with better phrase breaks. Eight other lines have individual retention reasons.

Three Istanbul emulator replays verified nine complete glyph masks. They include the promoter request and response, the specialty request with Baby Shark and Caviar, the revised thank-you, and the investment warning. The original ride flag set, the item handover consumed the supplied item, and the rejected investment left the test wallet and market share as expected. The replays used copied saves and the previously documented event, inventory and wallet fixtures. The full cargo warning and the remaining specialty item and product pairs received offline checks. All four [changed native pages](../{(VERIFY / 'portrait_sheet_01.png').as_posix()}) and the [gameplay sheet](../{(VERIFY / 'gameplay_lower_screens.png').as_posix()}) received visual review. Hardware remains untested.

The cumulative startup matched six frames and 24 protected name getters. All 40 targeted tests passed. The [registered ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers and the ASCII right-bound correction. All twelve records had existing credit. The ledger stands at 27,700 reviews and 276 mapped shared records still to review or classify.
""".encode())'''
    source = source[:start] + document + source[end:]
    changes = {
        '== 27699 and not ledger': '== 27700 and not ledger',
        'len(manifest["batches"]) == 810 and len(manifest["checks"]) == 145':
            'len(manifest["batches"]) == 816 and len(manifest["checks"]) == 151',
        'tavern_influence.pending.json': 'town_market_wraps.pending.json',
        'release_stack_before_tavern_influence.json': 'release_stack_before_town_market_wraps.json',
        'for p in (stage.STORED,live.OUT,STARTUP,QA,TOWNS):':
            'for p in (stage.STORED, live.OUTPUT, STARTUP, QA, NATIVE_SHEET, live.SHEET):',
        'verified_about_extras_predecessor=lineage, tavern_influence_release':
            'verified_expedition_report_wraps_predecessor=lineage, town_market_wraps_release',
        'Natural barkeep wording and verified native display for COMMON 821.': 'Source-reviewed town and Market prose and wraps.',
        'registered_tavern_influence_and_complete_parent_inverse': 'registered_town_market_wraps_and_complete_parent_inverse',
        '    if "COMMON_MESSAGE_821" not in ids:\n        ids.append("COMMON_MESSAGE_821")':
            '    ids.extend(key for n in EDITED if (key := f"COMMON_MESSAGE_{n}") not in ids)',
        'tavern_influence_registered_successor_pipeline': 'town_market_wraps_registered_successor_pipeline',
        'staged["byte_allocation"]': 'staged["allocations"]',
        'registered_manifest_entries=811,passing_release_checks=146,repository_tests=26,legacy_fixture_tests_skipped=2':
            'registered_manifest_entries=817,passing_release_checks=152,repository_tests=40,legacy_fixture_tests_skipped=0',
        'prose_revisions=1,justified_retentions=11,reviewed_UI_labels=0':
            'prose_revisions=2,justified_retentions=8,text_display_revisions=4,reviewed_UI_labels=0',
        'observed_revised_rumors=1,retained_observed_holds=13,\n            offline_role_and_name_variants=17':
            'observed_changed_keys=[739, 743, 748], observed_complete_holds=9, offline_specialty_argument_pairs=25',
        'checkpoint = "The Istanbul barkeep’s influence rumor is registered, with current coverage in three towns."':
            'checkpoint = CHECKPOINT',
        'digest = parent.source.current.assets.edit.digest': 'digest = DIGEST',
        '# Tavern Influence test candidate': '# Town and Market Wraps test candidate',
        'includes the revised Istanbul Tavern rumor': 'includes the revised town and Market dialogue',
        'Preserve Tavern rumor release and verified replay.': 'Preserve town and Market wrap release and verified replays.',
        '# Current editorial checkpoint - 2026-11-14': '# Current editorial checkpoint - 2026-11-15',
        '811 entries, 114 accepted layers, 146 checks.': '817 entries, 114 accepted layers, 152 checks.',
    }
    env = vars(publisher) | globals() | dict(DIGEST=digest)
    exec(compile(checked_text(source, changes), __file__ + '::registered-successor', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
