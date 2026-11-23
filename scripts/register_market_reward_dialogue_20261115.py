"""Register the verified Market letter and reward exchanges."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import stage_market_reward_dialogue_20261115 as stage
from scripts import verify_market_reward_dialogue_20261115 as live
from scripts.source_locked_derivation_v5118 import checked_text


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-market-reward-dialogue-v1-20261115'
ROOT = Path('out/market_reward_dialogue_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Market_Reward_Dialogue_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_market_reward_dialogue_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_market_reward_dialogue_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_market_reward_dialogue_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_rebuilt.nds')


def verify(prior, guard, viewed):
    staged, boot, game, draft = map(base.load, (stage.STORED, STARTUP, live.OUTPUT, stage.MANUSCRIPT))
    candidate = base.digest(stage.ROM)
    assert all(row['candidate_sha256'] == candidate for row in (staged, boot, game, draft))
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert all(base.digest(path) == sha for evidence in (boot, game) for path, sha in evidence['evidence'].items())
    sheet, = staged['sheets']
    assert len(sheet['messages']) == 18
    assert viewed == (base.digest(sheet['path']), base.digest(live.SHEET)) == (sheet['sha256'], game['sheet_sha256'])
    assert game['original_reward_sequence'] == live.CHAIN and game['exact_final_frame'] == 12001
    assert game['supplied_cargo_share_demand_qualification_and_bonus'] and not game['hardware']
    assert [r['message_ID'] for r in game['held_pages']] == live.CHAIN
    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests == 32 and not any(int(suite.get(key, 0)) for key in ('failures', 'errors', 'skipped'))

    clean, parent_image, candidate_image = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(stage.files, (parent_image, candidate_image))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {stage.COMMON}
    clean_arm, arm, common = clean.read_file(stage.ARM), before[stage.ARM], before[stage.COMMON]
    assert base.digest(stage.MANUSCRIPT) == staged['manuscript_sha256']
    assert stage.original_branches(clean_arm, arm) == draft['native_bindings']
    entries = stage.owned_entries(common, arm, stage.digest(arm[stage.DIRECTORY_OFFSET:stage.TABLE_OFFSET]))
    compiled, _, allocations = stage.owned_deployment(common, arm, entries, stage.encoded_changes())
    assert compiled == after[stage.COMMON] and allocations == {int(n): row for n, row in staged['allocations'].items()}
    assert stage.digest(compiled) == staged['target_COMMON_sha256']
    assert stage.digest(arm) == staged['target_ARM9_sha256'] == prior['target_ARM9_sha256']
    checked = bind_registered_story_percent_guard(guard)(stage.files(clean), after)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    candidate_image.replace_file(stage.COMMON, common)
    assert bytes(candidate_image.rom.save()) == parent.ROM.read_bytes()

    assert len(draft['records']) == 12 and {row['message_ID'] for row in draft['records'] if row['reflow']} == stage.PHRASES.keys()
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
    upstream = getsource(workflow.main)
    first = upstream.index('    base.replace_checked(DOC, f')
    end_marker = "'''.encode('utf-8'))"
    last = upstream.index(end_marker, first) + len(end_marker)
    note = """    base.replace_checked(DOC, f'''# Market reward dialogue

The Market trader’s offers, letter upgrade, instructions and closing replies were reviewed as complete exchanges. Eight rewrites clarify the two letters and keep their names and “governor’s office” together. An introduction works in small towns. A recommendation works in any town. Four records retain their wording, including one offer with improved line breaks. [Exact source and current references](../{REVIEW.as_posix()})

The revised recommendation, its instructions and the original farewell passed full dialogue-mask checks in paired emulator replays. Both replays returned to the same final screen. The test supplied cargo, market share, demand and qualification inputs to reproduce the recommendation branch. The other revised branches passed native formatting, full glyph, bounds and allocation checks offline. [Emulator comparison](../{(VERIFY / live.SHEET.name).as_posix()}) · [Native page previews](../{(VERIFY / Path(draft['native_sheet']['path']).name).as_posix()})

The [cumulative ROM and clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers and the ASCII right-bound correction. Byte-exact reconstruction, six startup frames, 24 protected getters and {tests} targeted tests passed. The ledger credits 27,700 reviewed records and has 276 mapped shared keys awaiting consumer adjudication.
'''.encode('utf-8'))"""
    replacements = {
        upstream[first:last]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 843 and len(manifest['checks']) == 178",
        '825 entries, 114 accepted layers and 160 passing checks': '844 entries, 114 accepted layers and 179 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160':
            'registered_manifest_entries=844, passing_release_checks=179',
        "verify(prior, profile['source25_multiarchive_guard'])":
            "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.market_reward_dialogue.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.market_reward_dialogue.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_market_reward_dialogue.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_market_economy_predecessor=predecessor, market_reward_dialogue_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['market_reward_dialogue_pipeline']",
        "manifest['changed_records'][stage.ARM].extend(r['id'] for r in draft['records'] if r['decision'] == 'revision')":
            "previous_records = manifest['changed_records'][stage.COMMON]\n"
            "    previous_records.extend(r['id'] for r in draft['records'] if r['reflow'] and r['id'] not in previous_records)",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_COMMON_slots=staged['allocations']",
        "target_ARM9_sha256=staged['target_ARM9_sha256'],":
            "target_ARM9_sha256=staged['target_ARM9_sha256'], target_COMMON_sha256=staged['target_COMMON_sha256'],",
        "ARM9_sha256=release['target_ARM9_sha256'], registered_release_verification=str(RELEASE)":
            "ARM9_sha256=release['target_ARM9_sha256'], MESFILE_sha256=release['target_COMMON_sha256'], "
            "registered_release_verification=str(RELEASE)",
        'changed_components=[stage.ARM], changed_internal_files=[]': 'changed_components=[], changed_internal_files=[stage.COMMON]',
        'new_contextual_records=0, prose_revisions=0,': 'new_contextual_records=0, prose_revisions=8,',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=9, justified_retentions=4, reviewed_UI_labels=0',
        'initialized_Rafael_dialogue=True': 'focused_market_recommendation=True, offline_other_reward_branches=True',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['market_reward_dialogue_20261115']",
        'name_label_revisions=2, justified_retentions=13': 'prose_revisions=8, text_display_revisions=9, justified_retentions=4',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'The Market trader’s letter offers, instructions and closing replies have clearer wording and wraps.',
        '# Ritual Officiant Labels test candidate': '# Market Reward Dialogue test candidate',
        'distinguishes two ritual officials from the Christian Priest role': 'revises the Market trader’s letter and reward dialogue',
        'Preserve verified ritual title candidate': 'Preserve verified Market reward dialogue candidate',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, Path(draft['native_sheet']['path']), QA)",
    }
    scope = vars(workflow) | globals() | {'VIEWED': viewed}
    exec(compile(checked_text(upstream, replacements), __file__ + '::register', 'exec'), scope)
    scope['main']()


if __name__ == '__main__':
    main()
