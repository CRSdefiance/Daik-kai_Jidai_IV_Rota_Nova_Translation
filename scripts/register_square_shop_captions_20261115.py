"""Register the reviewed Square captions through the cumulative release workflow."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import stage_square_shop_captions_20261115 as stage
from scripts import verify_square_shop_captions_20261115 as live
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_release_baseline import files


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-square-shop-captions-v1-20261115'
ROOT = Path('out/square_shop_captions_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Square_Shop_Captions_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_square_shop_captions_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_square_shop_captions_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_square_shop_captions_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_rebuilt.nds')


def verify(prior, guard, viewed):
    staged, boot, draft = map(base.load, (stage.STORED, STARTUP, live.REPORT))
    candidate = base.digest(stage.ROM)
    assert all(result['candidate_sha256'] == candidate for result in (staged, boot, draft))
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    game = draft['gameplay']
    assert all(base.digest(path) == digest for proof in (boot, game) for path, digest in proof['evidence'].items())
    assert viewed == (base.digest(live.SHEET), base.digest(live.GAME_SHEET))
    assert viewed == (draft['native_sheet']['sha256'], game['sheet_sha256'])
    assert game['ordinary_saved_lisbon'] and len(game['exact_frames']) == 11
    assert len(game['focused_changed_frames']) == 8 and len(game['focused_full_label_masks']) == 32
    assert len(game['focused_control_frames']) == 3 and game['focused_trend_fixture_fields'] == 4
    assert len(draft['category_getter_controls']) == 144 and draft['square_sentinel_controls'] == 241
    assert len(draft['records']) == 18
    assert {r['category'] for r in draft['records'] if r['decision'] == 'revision'} == set(stage.EXPANSIONS)
    validate_natural_dialogue_batch(draft)

    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests == 32 and all(int(suite.get(key, 0)) == 0 for key in ('failures', 'errors', 'skipped'))
    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(files, (old, new))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {stage.ARM}
    arm, owned = stage.transform(before[stage.ARM])
    assert arm == after[stage.ARM] and owned == staged['owned']
    verify_runtime(arm, prior)
    checked = bind_registered_story_percent_guard(guard)(files(clean), after)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    new.replace_file(stage.ARM, before[stage.ARM])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()

    if not review.PATCH.exists():
        make_xdelta(stage.CLEAN, stage.ROM, review.PATCH)
    if not review.REBUILT.exists():
        apply_xdelta(stage.CLEAN, review.PATCH, review.REBUILT)
    assert review.REBUILT.read_bytes() == stage.ROM.read_bytes()
    return staged, draft | dict(checked_story_format_guard=checked), tests


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', nargs=2, required=True)
    viewed = tuple(parser.parse_args().viewed_sha)
    original = getsource(workflow.main)
    first = original.index('    base.replace_checked(DOC, f')
    last = original.index("'''.encode('utf-8'))", first) + len("'''.encode('utf-8'))")
    note = """    base.replace_checked(DOC, f'''# Square shop captions

**Medicine Shop** and **Sundries Shop** replace **Med Shop** and **Goods Shop** in the Square. These are the same categories that the shopkeeper already calls Medicine and Sundries in forecasts. The [registered review](../{REVIEW.as_posix()}) records the clean Japanese, actual stock context, exact source/current pointers and 16 individual retention reasons. **Cond. Shop** and **Metals Shop** still use compact wording because their full forms exceed the original cell. **Fiber Shop** still includes woven cloth in the original inventory, and **Textile Shop** is a follow-up wording lead.

All 18 native captions passed complete leading and trailing glyph, blank cell and bounds checks in the original 64×12 viewport. The two revisions use the registered full-name pointers. The original format string, other five category callers, shopkeeper's forecast substitutions and out-of-range return values passed 144 shared getter checks and 241 Square fallback checks.

Four cold boots from the same Lisbon cartridge save covered the ordinary route and a focused test. Eleven ordinary frame pairs match in full. The focused test set four bytes in two original town trend pairs to select Medicine and Sundries through the game’s usual shop selector. Thirty-two held label masks passed, and all eight changed frame pairs differed only in the expected caption cells. An earned trend and hardware were outside the test. [Emulator comparison](../{(VERIFY / live.GAME_SHEET.name).as_posix()})

The [registered ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve 114 accepted layers and the ASCII right-bound correction. Six startup frames, 24 protected name getters and {tests} targeted tests passed. The dialogue ledger still credits 27,700 reviews, with 276 mapped shared keys open.
'''.encode('utf-8'))"""
    replacements = {
        original[first:last]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 840 and len(manifest['checks']) == 175",
        '825 entries, 114 accepted layers and 160 passing checks': '841 entries, 114 accepted layers and 176 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160':
            'registered_manifest_entries=841, passing_release_checks=176',
        "verify(prior, profile['source25_multiarchive_guard'])":
            "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.square_shop_captions.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.square_shop_captions.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_square_shop_captions.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_fleet_sighting_alerts_predecessor=predecessor, square_shop_captions_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['square_shop_captions_pipeline']",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_caption_dispatch_spans=staged['owned']",
        "stage.digest(registry_before), ledger_before=stage.digest(ledger_before)":
            "stage.sha256(registry_before).hexdigest(), ledger_before=stage.sha256(ledger_before).hexdigest()",
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=2, justified_retentions=16, reviewed_UI_labels=18',
        'initialized_Rafael_dialogue=True': 'ordinary_Lisbon=True, focused_original_town_trend=True',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['square_shop_captions_20261115']",
        'name_label_revisions=2, justified_retentions=13': 'text_display_revisions=2, justified_retentions=16',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'The Square menu now reads Medicine Shop and Sundries Shop in full.',
        '# Ritual Officiant Labels test candidate': '# Square Shop Captions test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            'spells out Medicine Shop and Sundries Shop in the Square',
        'Preserve verified ritual title candidate': 'Preserve verified Square Shop Captions candidate',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.STORED, STARTUP, live.REPORT, live.SHEET, live.GAME_SHEET, QA)",
    }
    env = vars(workflow) | globals() | {'VIEWED': viewed}
    exec(compile(checked_text(original, replacements), __file__ + '::register', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
