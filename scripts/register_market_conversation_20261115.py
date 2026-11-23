"""Register the Market dialogue with the cumulative clean-input patch."""

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
from scripts import stage_market_conversation_20261115 as stage
from scripts import verify_market_conversation_20261115 as live
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.verify_release_baseline import files


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-market-conversation-v1-20261115'
ROOT = Path('out/market_conversation_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Market_Conversation_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_market_conversation_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_market_conversation_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_market_conversation_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_rebuilt.nds')


def verify(prior, guard, viewed):
    staged, boot, game, draft = map(base.load, (stage.STORED, STARTUP, live.OUTPUT, stage.MANUSCRIPT))
    candidate = base.digest(stage.ROM)
    assert all(p['candidate_sha256'] == candidate for p in (staged, boot, game, draft))
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert all(base.digest(p) == sha for proof in (boot, game) for p, sha in proof['evidence'].items())
    assert game['message_ID'] == 18 and game['complete_ink_pixels'] > 0 and game['original_town_picker']
    assert len(game['exact_control_frames']) == 6 and game['native_only_revisions'] == [10, 19, 20, 24]
    sheet, = staged['sheets']
    assert (base.digest(live.SHEET), base.digest(sheet['path'])) == viewed == (game['sheet_sha256'], sheet['sha256'])
    assert base.digest(stage.MANUSCRIPT) == staged['manuscript_sha256']
    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests == 32 and all(int(suite.get(k, 0)) == 0 for k in ('failures', 'errors', 'skipped'))

    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(files, (old, new))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {stage.COMMON}
    arm, common = before[stage.ARM], before[stage.COMMON]
    entries = owned_entries(common, arm, stage.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    changed = stage.encoded_changes()
    compiled, _, slots = owned_deployment(common, arm, entries, changed)
    assert set(changed) == {row['n'] for row in staged['native_cases']}
    assert compiled == after[stage.COMMON] and {str(k): v for k, v in slots.items()} == staged['allocations']
    assert stage.digest(compiled) == staged['target_COMMON_sha256']
    assert stage.digest(arm) == staged['target_ARM9_sha256'] == prior['target_ARM9_sha256']
    checked = bind_registered_story_percent_guard(guard)(files(clean), after)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    new.replace_file(stage.COMMON, common)
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()

    assert len(draft['records']) == 19 and sum(r['decision'] == 'revision' for r in draft['records']) == 5
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
    note = """    base.replace_checked(DOC, f'''# Market trade and price-check dialogue

The [registered review](../{REVIEW.as_posix()}) covers 19 Market lines. The trader's price-check prompt now gives the fee and asks which town on two complete lines. The bargaining concession and three requests for a better price have more natural phrasing. Fourteen lines retain their wording, including the greeting, the ordinary farewell and all seven trade confirmation variants. The individual source and current references, retentions and all five review gates are in the ledger.

Paired Lisbon cold boots reached the Price Info prompt and then the original town picker. The new two-line prompt matches the complete native font mask. The original message requests and six other screens match their controls. The four other revisions were checked offline using the original native text paths. Both eight-slot voice tables, their fallback and the two original concession selections were exercised. The ledger distinguishes each voice alternative. [Emulator comparison](../{(VERIFY / live.SHEET.name).as_posix()})

The [registered candidate and clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve the 114 accepted layers and the ASCII right bound. Six startup frames, 24 protected name getters, {tests} targeted tests and byte-exact reconstruction passed. The dialogue tally remains 27,700 because these lines already carried contextual credit. Other callers for COMMON 750–752 remain open, along with 273 other mapped shared keys. Hardware was outside this pass.
'''.encode('utf-8'))"""
    replacements = {
        original[first:last]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 832 and len(manifest['checks']) == 167",
        '825 entries, 114 accepted layers and 160 passing checks': '833 entries, 114 accepted layers and 168 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160':
            'registered_manifest_entries=833, passing_release_checks=168',
        "verify(prior, profile['source25_multiarchive_guard'])": "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.market_conversation.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.market_conversation.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_market_conversation.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_ship_class_names_predecessor=predecessor, market_conversation_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['market_conversation_pipeline']",
        "manifest['changed_records'][stage.ARM].extend(r['id'] for r in draft['records'] if r['decision'] == 'revision')":
            "manifest['changed_records'][stage.COMMON].extend(r['id'] for r in draft['records'] if r['decision'] == 'revision')",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_COMMON_slots=staged['allocations']",
        "target_ARM9_sha256=staged['target_ARM9_sha256'],":
            "target_ARM9_sha256=staged['target_ARM9_sha256'], target_COMMON_sha256=staged['target_COMMON_sha256'],",
        "ARM9_sha256=release['target_ARM9_sha256'], registered_release_verification=str(RELEASE)":
            "ARM9_sha256=release['target_ARM9_sha256'], MESFILE_sha256=release['target_COMMON_sha256'], registered_release_verification=str(RELEASE)",
        'changed_components=[stage.ARM], changed_internal_files=[]': 'changed_components=[], changed_internal_files=[stage.COMMON]',
        'new_contextual_records=0, prose_revisions=0': 'new_contextual_records=0, prose_revisions=5',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=0, justified_retentions=14, reviewed_UI_labels=0',
        'initialized_Rafael_dialogue=True': 'ordinary_lisbon_price_check=True',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['market_conversation_20261115']",
        'name_label_revisions=2, justified_retentions=13': 'prose_revisions=5, justified_retentions=14',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'The Market price-check prompt and four bargaining replies are revised.',
        '# Ritual Officiant Labels test candidate': '# Market Conversation test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            'improves the Market price-check prompt and bargaining dialogue',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, Path(draft['native_sheet']['path']), QA)",
        'Preserve verified ritual title candidate': 'Preserve verified Market dialogue candidate',
    }
    env = vars(workflow) | globals() | {'VIEWED': viewed}
    exec(compile(checked_text(original, replacements), __file__ + '::registered-market-dialogue', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
