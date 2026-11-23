"""Register the verified town wording and exact clean-input patch."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import replay_london_stockholm_dialogue_20261115 as replay
from scripts import stage_london_stockholm_dialogue_20261115 as stage
from scripts import verify_london_stockholm_dialogue_20261115 as live
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.verify_release_baseline import files


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-london-stockholm-dialogue-v1-20261115'
ROOT = Path('out/london_stockholm_dialogue_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_London_Stockholm_Dialogue_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_london_stockholm_dialogue_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_london_stockholm_dialogue_20261115.md')
STARTUP, QA = replay.STARTUP, stage.ROOT / 'repository_qa.xml'
CHECK = 'registered_london_stockholm_dialogue_layout_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_reconstruction_RESEARCH_ONLY.nds')


def verify(prior, guard, viewed):
    staged, boot, game, draft = map(base.load, (stage.STORED, STARTUP, live.OUTPUT, stage.MANUSCRIPT))
    candidate = base.digest(stage.ROM)
    assert all(p['candidate_sha256'] == candidate for p in (staged, boot, game))
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert all(base.digest(path) == sha for p in (boot, game) for path, sha in p['evidence'].items())
    assert len(draft['records']) == 18 and len(draft['focused_native_cases']) == 16
    assert game['ordinary_cold_boots'] and game['matched_source_NATIVE_requests']
    assert [len(row['complete_changed_message_holds']) for row in game['cases']] == [2, 3]
    assert {n for row in game['cases'] for hold in row['complete_changed_message_holds'] for n in (hold['record'],)} == set(stage.CHOICES)
    native_sheet, = staged['sheets']
    assert (base.digest(live.SHEET), base.digest(native_sheet['path'])) == viewed == (game['sheet_sha256'], native_sheet['sha256'])
    assert base.digest(stage.MANUSCRIPT) == staged['manuscript_sha256']
    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests and all(int(suite.get(k, 0)) == 0 for k in ('failures', 'errors', 'skipped'))

    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(files, (old, new))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {stage.COMMON}
    arm, common = before[stage.ARM], before[stage.COMMON]
    entries = owned_entries(common, arm, stage.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    changes = {n: b' ' + text.encode('ascii') for n, text in stage.CHOICES.items()}
    patched, _, slots = owned_deployment(common, arm, entries, changes)
    assert patched == after[stage.COMMON] and {str(k): v for k, v in slots.items()} == staged['allocations']
    assert stage.digest(patched) == staged['target_COMMON_sha256']
    assert stage.digest(arm) == staged['target_ARM9_sha256'] == prior['target_ARM9_sha256']
    checked = bind_registered_story_percent_guard(guard)(files(clean), after)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    new.replace_file(stage.COMMON, common)
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    for row in draft['records']:
        row['registered_reference'] = row['staged_reference'] | dict(candidate_sha256=candidate)
    draft.update(candidate_sha256=candidate, gameplay=game, native_sheet=native_sheet, checked_story_format_guard=checked)
    validate_natural_dialogue_batch(draft)
    if not review.PATCH.exists():
        make_xdelta(stage.CLEAN, stage.ROM, review.PATCH)
    if not review.REBUILT.exists():
        apply_xdelta(stage.CLEAN, review.PATCH, review.REBUILT)
    assert review.REBUILT.read_bytes() == stage.ROM.read_bytes()
    return staged, draft, tests


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', nargs=2, required=True)
    viewed = tuple(parser.parse_args().viewed_sha)
    original = getsource(workflow.main)
    first = original.index('    base.replace_checked(DOC, f')
    last = original.index("'''.encode('utf-8'))", first) + len("'''.encode('utf-8'))")
    note = '''    base.replace_checked(DOC, f\'''# London and Stockholm town dialogue

The [registered review](../{REVIEW.as_posix()}) covers 18 existing dialogue records from the London Tavern and the Riga-to-Stockholm trip, including the Stockholm Palace and Tavern. Manuel now asks whether spending the quoted amount is all right, with the full amount and “gold” together. The London patron gives a lively thanks and praises the buyer’s generosity once. The Stockholm king welcomes the player and says he’s heard they want to help defend the city. The 15 retentions include the two palace responses, both drink orders, the London tip about Bristol, and the regional rumor and introduction to Francisca in Stockholm.

Paired cold boots used ordinary inputs and exact copies of existing saves. Both runs followed the same in-game text requests. All five revised dialogue holds match complete native font masks. The sampled frames differ only in the revised dialogue bodies. Sixteen more native previews cover ten numeric sizes, four default captain surnames, a long test name and the patron’s cheer. The large prices and long name were supplied offline. The cumulative startup matched six frames and 24 protected name getters. All {tests} targeted tests passed. [Emulator comparison](../{(VERIFY / live.SHEET.name).as_posix()})

The [registered candidate and patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers and the ASCII right-bound correction. The precise patch reconstructs the ROM byte for byte. The ledger remains at 27,700 credited reviews, with 276 mapped shared keys open. Further conditional scenes and physical hardware remain open.
\'''.encode('utf-8'))'''
    replacements = {
        original[first:last]: note,
        '825 entries, 114 accepted layers and 160 passing checks': '828 entries, 114 accepted layers and 163 passing checks',
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159": "len(manifest['batches']) == 827 and len(manifest['checks']) == 162",
        'registered_manifest_entries=825, passing_release_checks=160': 'registered_manifest_entries=828, passing_release_checks=163',
        "verify(prior, profile['source25_multiarchive_guard'])": "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.london_stockholm_dialogue.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.london_stockholm_dialogue.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_london_stockholm_dialogue.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_rafael_setup_labels_predecessor=predecessor, london_stockholm_dialogue_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['london_stockholm_dialogue_pipeline']",
        "manifest['changed_records'][stage.ARM].extend": "manifest['changed_records'][stage.COMMON].extend",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']": "owned_COMMON_slots=staged['allocations']",
        'changed_components=[stage.ARM], changed_internal_files=[]': 'changed_components=[], changed_internal_files=[stage.COMMON]',
        "target_ARM9_sha256=staged['target_ARM9_sha256'],": "target_ARM9_sha256=staged['target_ARM9_sha256'], target_COMMON_sha256=staged['target_COMMON_sha256'],",
        'new_contextual_records=0, prose_revisions=0': 'new_contextual_records=0, prose_revisions=3',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=0, justified_retentions=15, reviewed_UI_labels=0',
        'initialized_Rafael_dialogue=True': 'ordinary_London_Stockholm_town_dialogue=True',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['london_stockholm_dialogue_20261115']",
        'name_label_revisions=2, justified_retentions=13': 'prose_revisions=3, justified_retentions=15',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'London’s Tavern and the Stockholm Palace have three dialogue revisions and 15 justified retentions.',
        '# Ritual Officiant Labels test candidate': '# London and Stockholm Dialogue test candidate',
        'distinguishes two ritual officials from the Christian Priest role': 'improves the London Tavern and Stockholm Palace exchanges',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, Path(draft['native_sheet']['path']), QA)",
        'Preserve verified ritual title candidate': 'Preserve verified London and Stockholm dialogue candidate',
    }
    namespace = vars(workflow) | globals() | dict(VIEWED=viewed)
    exec(compile(checked_text(original, replacements), __file__ + '::registered-common-successor', 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
