"""Register the verified character-editor labels with a byte-exact clean patch."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import stage_rafael_setup_labels_20261115 as stage
from scripts import verify_rafael_setup_labels_20261115 as live
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_release_baseline import files


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-rafael-setup-labels-v1-20261115'
ROOT = Path('out/rafael_setup_labels_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Rafael_Setup_Labels_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_rafael_setup_labels_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_rafael_setup_labels_20261115.md')
STARTUP, QA = live.replay.STARTUP, stage.ROOT / 'repository_qa.xml'
CHECK = 'registered_rafael_setup_labels_birthday_formatter_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_reconstruction_RESEARCH_ONLY.nds')


def verify(prior, guard, viewed):
    staged, start, game, native = map(base.load, (stage.STORED, STARTUP, live.OUTPUT, live.NATIVE))
    candidate = base.digest(stage.ROM)
    assert all(p['candidate_sha256'] == candidate for p in (staged, start, game, native))
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert start['cold_boot'] and not start['savestate'] and start['complete_deployed_payload_exact']
    assert len(start['exact_matching_frames']) == 5 and len(start['original_protected_name_getters']) == 24
    assert start['date_only_hold']['frame'] == 3340 and start['date_only_hold']['complete_Maria_date_mask']['text'].strip() == '6/7'
    assert all(base.digest(path) == sha for proof in (start, game) for path, sha in proof['evidence'].items())
    assert game['ordinary_cold_boot'] and game['exact_outside_edit_regions_every_sample']
    assert [len(game[k]) for k in ('heading_masks', 'calendar_heading_masks', 'date_masks')] == [5, 3, 5]
    assert base.digest(live.SHEET) == game['sheet_sha256'] == viewed
    assert native['supported_dates_checked'] == len(native['cases']) == 365
    assert native['ARM9_sha256'] == staged['target_ARM9_sha256'] and native['complete_native_ink_blank_fields_and_canaries']
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [20, 0, 0, 0]

    source, old, new = [base.NdsImage.open(path) for path in (stage.CLEAN, parent.ROM, stage.ROM)]
    before, after = map(files, (old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {stage.ARM}
    arm, rows = stage.install(source, old, prior)
    assert len(rows) == 8 and rows == staged['fields'] and arm == after[stage.ARM]
    assert stage.digest(arm) == staged['target_ARM9_sha256']
    assert stage.digest(after['/COMMON/MESFILE.DK4']) == prior['target_COMMON_sha256']
    checked = bind_registered_story_percent_guard(guard)(files(source), after)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    new.replace_file(stage.ARM, before[stage.ARM])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    for row in rows:
        row['registered_reference']['candidate_sha256'] = candidate
    draft = dict(translation_policy='natural-dialogue-v2', encoder='dialogue-relocatable-v1', target_locale='en-US',
        review_gates=stage.GATES, records=rows, candidate_sha256=candidate, native_date_proof_sha256=base.digest(live.NATIVE),
        actual=game, checked_story_format_guard=checked, new_dialogue_credit=0)
    validate_natural_dialogue_batch(draft)

    if not review.PATCH.exists():
        make_xdelta(stage.CLEAN, stage.ROM, review.PATCH)
    if not review.REBUILT.exists():
        apply_xdelta(stage.CLEAN, review.PATCH, review.REBUILT)
    assert stage.ROM.read_bytes() == review.REBUILT.read_bytes()
    return staged, draft, 20


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', required=True)
    viewed = parser.parse_args().viewed_sha
    original = getsource(workflow.main)
    first = original.index('    base.replace_checked(DOC, f')
    last = original.index("'''.encode('utf-8'))", first) + len("'''.encode('utf-8'))")
    note = '''    base.replace_checked(DOC, f\'''# Rafael New Game setup labels

The character editor now uses **Edit First Name**, **Edit Middle Name**, **Edit Last Name**, **Edit Company**, and **Edit Birthday**. The Birth row shows a standard American date such as **3/5**. The birthday calendar labels the month selector **Month** and displays the month number without the old M suffix. Both date arguments and the calendar’s line feed are preserved. The first draft left stale trailing letters when moving from a longer heading to a shorter one. The registered headings clear the full 16-cell strip. [Exact review](../{REVIEW.as_posix()})

Paired ordinary cold boots with no saves exercised all five fields, March and April in the calendar, the change from March 5 to April 13, and cancellation of the setup confirmation. All differences in the sampled frames fit inside the changed text areas. A native formatting check verified all 365 dates allowed by the game, with complete glyphs and memory guards. The cumulative startup matched five complete frames and Maria’s revised date field, with all 24 protected name getters exact. All {tests} targeted tests passed. [Emulator comparison](../{(VERIFY / live.SHEET.name).as_posix()})

The observed setup flow looked up COMMON 120. The replay recorded zero requests for the legacy setup records 100–107. Their other possible consumers and hardware testing remain open. The [registered candidate and patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers and the ASCII right-bound correction. The ledger remains at 27,700 credited reviews with 276 mapped shared keys open.
\'''.encode('utf-8'))'''
    replacements = {
        original[first:last]: note,
        '825 entries, 114 accepted layers and 160 passing checks': '827 entries, 114 accepted layers and 162 passing checks',
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159": "len(manifest['batches']) == 826 and len(manifest['checks']) == 161",
        'registered_manifest_entries=825, passing_release_checks=160': 'registered_manifest_entries=827, passing_release_checks=162',
        "verify(prior, profile['source25_multiarchive_guard'])": "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.rafael_setup_labels.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.rafael_setup_labels.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_rafael_setup_labels.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_cristina_recruitment_predecessor=predecessor, rafael_setup_labels_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['rafael_setup_labels_pipeline']",
        ",\n        owned_alignment_span=staged['new_label_span']": '',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=8, justified_retentions=0, reviewed_UI_labels=8, story_name_revisions=0',
        'initialized_Rafael_dialogue=True': 'ordinary_Rafael_character_setup=True',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['rafael_setup_labels_20261115']",
        'name_label_revisions=2, justified_retentions=13': 'reviewed_UI_labels=8, native_date_cases=365',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'New Game now shows natural editor headings and clean month/day dates.',
        '# Ritual Officiant Labels test candidate': '# Rafael Setup Labels test candidate',
        'distinguishes two ritual officials from the Christian Priest role': 'updates the New Game character editor and birthday picker',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            '(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, live.NATIVE, QA)',
        'Preserve verified ritual title candidate': 'Preserve verified character setup candidate',
    }
    namespace = vars(workflow) | globals() | dict(VIEWED=viewed)
    exec(compile(checked_text(original, replacements), __file__ + '::registered-setup-text-successor', 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
