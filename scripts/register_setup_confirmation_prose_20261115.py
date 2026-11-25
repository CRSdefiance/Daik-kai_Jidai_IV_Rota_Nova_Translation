"""Register the source-bound setup and system-data prose revision."""

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
from scripts import stage_setup_confirmation_prose_20261115 as stage
from scripts import verify_setup_confirmation_prose_20261115 as live
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_release_baseline import files

base, parent = stage.base, stage.parent
PROFILE = 'all-routes-setup-confirmation-prose-v1-20261115'
ROOT = Path('out/setup_confirmation_prose_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Setup_Confirmation_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_setup_confirmation_prose_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_setup_confirmation_prose_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_setup_confirmation_prose_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_rebuilt.nds')


def verify(prior, guard, viewed):
    staged, boot, game = map(base.load, (stage.STORED, STARTUP, live.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert all(d['candidate_sha256'] == candidate for d in (staged, boot, game))
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert all(base.digest(path) == digest for d in (boot, game) for path, digest in d['evidence'].items())
    assert viewed == (base.digest(stage.SHEET), base.digest(live.SHEET))
    assert viewed == (staged['native_sheet']['sha256'], game['sheet_sha256'])
    assert len(game['exact_control_frames']) == 12 and game['ordinary_rafael_new_game']
    assert game['ordinary_cancel_return_frame'] in game['exact_control_frames'] and not game['hardware']
    assert game['offline_only_revisions'] == [122, 123]

    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests == 32 and all(int(suite.get(key, 0)) == 0 for key in ('failures', 'errors', 'skipped'))
    clean, before, after = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    old, new = map(files, (before, after))
    assert old.keys() == new.keys() and {p for p in old if old[p] != new[p]} == {stage.COMMON}
    arm, common = new[stage.ARM], new[stage.COMMON]
    assert stage.digest(arm) == prior['target_ARM9_sha256'] == staged['target_ARM9_sha256']
    assert stage.digest(common) == staged['target_COMMON_sha256']
    existing = owned_entries(old[stage.COMMON], arm, stage.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    rows = staged['records']
    wanted = {row['message_ID']: bytes.fromhex(row['deployed_hex']) for row in rows if row['decision'] == 'revision'}
    assert set(wanted) == {120, 122, 123} and len(rows) == 6
    compiled, _, allocations = stage.owned_deployment(old[stage.COMMON], arm, existing, wanted)
    assert compiled == common and allocations == {int(n): entry for n, entry in staged['allocations'].items()}
    checked = bind_registered_story_percent_guard(guard)(files(clean), new)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    after.replace_file(stage.COMMON, old[stage.COMMON])
    assert bytes(after.rom.save()) == parent.ROM.read_bytes()

    draft = {
        'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US', 'encoder': 'dialogue-relocatable-v1',
        'review_gates': list(stage.GATES), 'candidate_sha256': candidate, 'records': rows,
        'gameplay': game, 'native_sheet': staged['native_sheet'], 'checked_story_format_guard': checked,
    }
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
    note = """    base.replace_checked(DOC, f'''# New Game confirmation and system-data notices

After the character details are entered, the game now asks **Is everything OK?** The two load-failure messages share **Couldn't load system data.** The recovery variant places **The game will start with defaults.** on its own line. **Start the game?**, **System data not found.**, and **System data is corrupted.** stay as written for their distinct branches. The [registered review](../{REVIEW.as_posix()}) records all six clean sources, exact original callers and individual wording decisions.

Paired cold boots used ordinary Rafael New Game controls. The revised confirmation passed complete glyph-mask verification, and the other 12 held frames match pixel for pixel, including cancellation back to the editor. Both revised load-failure notices passed stored native format, leading and trailing glyph, width, and complete-word checks offline. [Emulator comparison](../{(VERIFY / live.SHEET.name).as_posix()})

The [cumulative ROM and clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve 114 accepted layers and the ASCII right-bound correction. The exact reconstruction, six startup holds, 24 protected getters and {tests} targeted tests passed. These were already credited records. The ledger remains at 27,700 reviewed records and 276 pending shared keys.
'''.encode('utf-8'))"""
    replacements = {
        original[first:last]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 841 and len(manifest['checks']) == 176",
        '825 entries, 114 accepted layers and 160 passing checks': '842 entries, 114 accepted layers and 177 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160':
            'registered_manifest_entries=842, passing_release_checks=177',
        "verify(prior, profile['source25_multiarchive_guard'])":
            "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.setup_confirmation_prose.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.setup_confirmation_prose.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_setup_confirmation_prose.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_square_shop_captions_predecessor=predecessor, setup_confirmation_prose_release=str(REVIEW)',
        "manifest['changed_records'][stage.ARM].extend(r['id'] for r in draft['records'] if r['decision'] == 'revision')":
            "previous_records = manifest['changed_records'][stage.COMMON]\n"
            "    previous_records.extend(r['id'] for r in draft['records'] if r['decision'] == 'revision' and r['id'] not in previous_records)",
        "manifest['ritual_officiant_pipeline']": "manifest['setup_confirmation_prose_pipeline']",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_COMMON_slots=staged['allocations']",
        "registry_sha256=base.digest(reg_tmp), predecessor=predecessor, target_ARM9_sha256=staged['target_ARM9_sha256'],":
            "registry_sha256=base.digest(reg_tmp), predecessor=predecessor, target_ARM9_sha256=staged['target_ARM9_sha256'],\n"
            "        target_COMMON_sha256=staged['target_COMMON_sha256'],",
        "ARM9_sha256=release['target_ARM9_sha256'], registered_release_verification=str(RELEASE)":
            "ARM9_sha256=release['target_ARM9_sha256'], COMMON_sha256=release['target_COMMON_sha256'],\n"
            "        registered_release_verification=str(RELEASE)",
        'changed_components=[stage.ARM], changed_internal_files=[]':
            'changed_components=[], changed_internal_files=[stage.COMMON]',
        'new_contextual_records=0, prose_revisions=0,': 'new_contextual_records=0, prose_revisions=3,',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=1, justified_retentions=3, reviewed_UI_labels=0',
        'initialized_Rafael_dialogue=True': 'ordinary_Rafael_setup=True, offline_system_data_failures=True',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['setup_confirmation_prose_20261115']",
        'name_label_revisions=2, justified_retentions=13':
            'prose_revisions=3, text_display_revisions=1, justified_retentions=3',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'New Game and system-data load failures use clearer wording.',
        '# Ritual Officiant Labels test candidate': '# Setup Confirmation test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            'revises the New Game confirmation and two system-data failure notices',
        'Preserve verified ritual title candidate': 'Preserve verified Setup Confirmation candidate',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, stage.SHEET, QA)",
    }
    scope = vars(workflow) | globals() | {'VIEWED': viewed}
    exec(compile(checked_text(original, replacements), __file__ + '::register', 'exec'), scope)  # noqa: S102
    scope['main']()


if __name__ == '__main__':
    main()
