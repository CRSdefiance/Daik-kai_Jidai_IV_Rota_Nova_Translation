"""Register the verified Square trend dialogue in the cumulative release."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import stage_square_trend_dialogue_20261115 as stage
from scripts import verify_square_trend_dialogue_20261115 as live
from scripts.source_locked_derivation_v5118 import checked_text


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-square-trend-dialogue-v1-20261115'
ROOT = Path('out/square_trend_dialogue_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Square_Trend_Dialogue_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_square_trend_dialogue_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_square_trend_dialogue_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_square_trend_dialogue_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_rebuilt.nds')


def verify(prior, guard, viewed):
    staged, boot, game, draft = map(base.load, (stage.STORED, STARTUP, live.OUTPUT, stage.MANUSCRIPT))
    candidate = base.digest(stage.ROM)
    assert all(row['candidate_sha256'] == candidate for row in (staged, boot, game, draft))
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert all(base.digest(p) == sha for proof in (boot, game) for p, sha in proof['evidence'].items())
    assert game['ordinary_saved_game'] and game['comparison_dependencies_match_parent'] and not game['hardware']
    assert len(game['revised_holds']) == 5 and {row['message_ID'] for row in game['revised_holds']} == {654, 732}
    assert len(game['native_only_revisions']) == 3 and game['exact_control_frames']
    sheet, = staged['sheets']
    assert (base.digest(live.SHEET), base.digest(sheet['path'])) == viewed == (game['sheet_sha256'], sheet['sha256'])
    assert len(sheet['messages']) == 13 and len(staged['native_cases']) == 640
    for n in stage.REVISIONS:
        cases = [r for r in staged['native_cases'] if r['id'] == n]
        assert len(cases) == (1 if n == 732 else 124)
        assert all(not row['findings'] and row['complete_bytes_and_guarded_printf_wrap_ABI'] for row in cases)
    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests == 32 and all(int(suite.get(key, 0)) == 0 for key in ('failures', 'errors', 'skipped'))

    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(stage.files, (old, new))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {stage.COMMON}
    arm, common = before[stage.ARM], before[stage.COMMON]
    entries = stage.owned_entries(common, arm, stage.digest(arm[stage.DIRECTORY_OFFSET:stage.TABLE_OFFSET]))
    compiled, _, slots = stage.owned_deployment(common, arm, entries, stage.encoded_changes())
    assert compiled == after[stage.COMMON] and {str(key): val for key, val in slots.items()} == staged['allocations']
    assert stage.digest(compiled) == staged['target_COMMON_sha256']
    assert stage.digest(arm) == staged['target_ARM9_sha256'] == prior['target_ARM9_sha256']
    checked = bind_registered_story_percent_guard(guard)(stage.files(clean), after)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    new.replace_file(stage.COMMON, common)
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()

    assert base.digest(stage.MANUSCRIPT) == staged['manuscript_sha256']
    assert len(draft['records']) == 8 and sum(row['decision'] == 'revision' for row in draft['records']) == 5
    for row in draft['records']:
        row['registered_reference'] = row['staged_reference'] | {'candidate_sha256': candidate}
        row['review']['formatting'] = True
    draft.update(gameplay=game, native_sheet=sheet, checked_story_format_guard=checked)
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
    note = """    base.replace_checked(DOC, f'''# Square trade-trend dialogue

All eight original shopkeeper alternatives were reviewed against the Japanese. Five revisions preserve the selling advice, sales enthusiasm, pursuit of profit and tentative forecasts. Three alternatives retain their wording with individual reasons. The Tunis forecast now reads “This trend may last quite a while.” The stock advice keeps Whale Meat together and moves the Market destination to a complete line. [Exact source and current references](../{REVIEW.as_posix()})

The native formatter checked all 124 goods where a product substitutes, all 18 category arguments, and both static replies. All five revisions passed glyph, expansion, wrapper and allocation checks. The Tunis replay from the same battery save and inputs verified five revised holds and {len(draft['gameplay']['exact_control_frames'])} unchanged controls. The retail nameplate and original message requests passed. The changes to 653, 655 and 733 were checked offline. Hardware remains outside this pass. [Emulator comparison](../{(VERIFY / live.SHEET.name).as_posix()})

The [cumulative ROM and clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve the 114 accepted layers and the ASCII right-bound correction. Six startup frames, 24 protected name getters, {tests} targeted tests and byte-exact reconstruction passed. These alternatives already had editorial credit. The ledger remains at 27,700 credited records and 276 mapped shared keys still open.
'''.encode('utf-8'))"""
    replacements = {
        original[first:last]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 834 and len(manifest['checks']) == 169",
        '825 entries, 114 accepted layers and 160 passing checks': '835 entries, 114 accepted layers and 170 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160':
            'registered_manifest_entries=835, passing_release_checks=170',
        "verify(prior, profile['source25_multiarchive_guard'])": "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.square_trend_dialogue.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.square_trend_dialogue.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_square_trend_dialogue.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_seoul_recruitment_predecessor=predecessor, square_trend_dialogue_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['square_trend_dialogue_pipeline']",
        "manifest['changed_records'][stage.ARM].extend(r['id'] for r in draft['records'] if r['decision'] == 'revision')":
            "manifest['changed_records'][stage.COMMON].extend(r['id'] for r in draft['records'] "
            "if r['decision'] == 'revision' and r['id'] not in manifest['changed_records'][stage.COMMON])",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_COMMON_slots=staged['allocations']",
        "target_ARM9_sha256=staged['target_ARM9_sha256'],":
            "target_ARM9_sha256=staged['target_ARM9_sha256'], target_COMMON_sha256=staged['target_COMMON_sha256'],",
        "ARM9_sha256=release['target_ARM9_sha256'], registered_release_verification=str(RELEASE)":
            "ARM9_sha256=release['target_ARM9_sha256'], MESFILE_sha256=release['target_COMMON_sha256'], registered_release_verification=str(RELEASE)",
        'changed_components=[stage.ARM], changed_internal_files=[]': 'changed_components=[], changed_internal_files=[stage.COMMON]',
        'new_contextual_records=0, prose_revisions=0': 'new_contextual_records=0, prose_revisions=5',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=0, justified_retentions=3, reviewed_UI_labels=0',
        'initialized_Rafael_dialogue=True': 'ordinary_tunis_square_dialogue=True',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['square_trend_dialogue_20261115']",
        'name_label_revisions=2, justified_retentions=13': 'prose_revisions=5, justified_retentions=3',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'Five Square trend replies are revised, including both wraps observed in Tunis.',
        '# Ritual Officiant Labels test candidate': '# Square Trend Dialogue test candidate',
        'distinguishes two ritual officials from the Christian Priest role': 'improves five original Square trade-trend replies',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, Path(draft['native_sheet']['path']), QA)",
        'Preserve verified ritual title candidate': 'Preserve verified Square trend dialogue candidate',
    }
    env = vars(workflow) | globals() | {'VIEWED': viewed}
    exec(compile(checked_text(original, replacements), __file__ + '::registered-square-trend-dialogue', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
