"""Register the complete outfitted ship-design label review."""

from argparse import ArgumentParser
from inspect import getsource
from json import dumps
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import stage_trade_and_armed_ship_labels_20261115 as stage
from scripts import verify_trade_and_armed_ship_labels_20261115 as live
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-trade-and-armed-ship-labels-v1-20261115'
ROOT = Path('out/trade_and_armed_ship_labels_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Trade_and_Armed_Ship_Labels_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_trade_and_armed_ship_labels_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_trade_and_armed_ship_labels_20261115.md')
STARTUP, QA = live.STARTUP, stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_trade_and_armed_ship_labels_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_rebuilt.nds')


def verify(prior, guard, viewed):
    staged, checks, boot = map(base.load, (stage.OUTPUT, live.OUTPUT, STARTUP))
    candidate = base.digest(stage.ROM)
    assert all(row['candidate_sha256'] == candidate for row in (staged, checks, boot))
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert all(base.digest(path) == sha for proof in (checks, boot) for path, sha in proof['evidence'].items())
    assert viewed == (base.digest(live.NATIVE), base.digest(live.SHEET)) == (
        checks['native_sheet_sha256'], checks['sheet_sha256'])
    assert checks['catalogue'] == dict(catalogue_class_count=39, catalogue_model_count=155,
                                      changed_models=sorted(stage.REVISIONS), reviewed_models=60)
    assert len(checks['changed_label_previews']) == 6 and len(checks['focused_shipyard']['held_labels']) == 3
    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests == 32 and not any(int(suite.get(key, 0)) for key in ('failures', 'errors', 'skipped'))

    clean, old, final = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(stage.files, (old, final))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {stage.ARM}
    runtime = RegisteredRuntime(parent.RELEASE, prior['own_registered_startup'], captain=3)
    arm, records, storage = stage.deploy(runtime, clean, old)
    assert arm == after[stage.ARM] and stage.sha256(arm).hexdigest() == staged['target_ARM9_sha256']
    assert dumps(records, sort_keys=True) == dumps(staged['records'], sort_keys=True)
    assert dumps(storage, sort_keys=True) == dumps(staged['owned_banks'], sort_keys=True)
    guard_check = bind_registered_story_percent_guard(guard)(stage.files(clean), after)
    assert guard_check['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(guard_check['source_bound_new_command_counts'].values())
    final.replace_file(stage.ARM, before[stage.ARM])
    assert bytes(final.rom.save()) == parent.ROM.read_bytes()
    for row in records:
        row['review']['formatting'] = True
        row['registered_candidate_sha256'] = candidate
    draft = staged | dict(records=records, native_and_actual=checks, checked_story_format_guard=guard_check,
                          display_checks_pending=False, registered=True)
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
    start = upstream.index('    base.replace_checked(DOC, f')
    end = upstream.index("'''.encode('utf-8'))", start) + len("'''.encode('utf-8'))")
    note = """    base.replace_checked(DOC, f'''# Trade and armed ship designs

The sixty outfitted designs have six wording changes and 54 justified retentions. **Armed Sekibune**, **Armed Hanse Cog**, **War Light Galleon**, **Armed Small Galley** and **Armed Large Galley** show their full hull names. **Trade Lt Galleon** restores the full word Galleon. That design uses the short weight qualifier in the 18-character field, while its hull class displays **Light Galleon**. Previous decisions for the related cargo and Suetsugu variants are linked in the review. [Exact Japanese and English references](../{REVIEW.as_posix()})

Five existing catalogue regions fit the revised labels. Armed Schooner moves within its existing group with identical text. The adjacent names and all ship data outside the six revised design names match the previous build across 39 class getters and 155 initialized models. The six offline previews show complete leading and trailing glyphs. [Font previews](../{(VERIFY / live.NATIVE.name).as_posix()})

A paired cold-boot replay linked the saved fleet to one existing stock model. With ordinary controls, the original Istanbul Shipyard displayed **Armed Large Galley** in the list and the detail heading across three holds. The surrounding pixels matched on the two holds with the same highlight phase. Two other samples show a highlight-phase difference, and the last menu frame matches. The other five revisions were checked offline. Ordinary acquisition and hardware remain unvisited. [Emulator comparison](../{(VERIFY / live.SHEET.name).as_posix()})

The [cumulative ROM and clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve 114 accepted layers and the ASCII right bound. The exact reconstruction, six cold-boot frames, 24 protected getters and {tests} targeted tests passed. The ledger credits 27,700 dialogue and prose reviews and retains 276 stored shared-text keys awaiting consumer evidence.
'''.encode('utf-8'))"""
    replacements = {
        upstream[start:end]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 846 and len(manifest['checks']) == 181",
        '825 entries, 114 accepted layers and 160 passing checks': '847 entries, 114 accepted layers and 182 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160':
            'registered_manifest_entries=847, passing_release_checks=182',
        "verify(prior, profile['source25_multiarchive_guard'])":
            "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.trade_armed_designs.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.trade_armed_designs.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_trade_armed_designs.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_specialized_ship_labels_predecessor=predecessor, trade_armed_designs_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['trade_armed_designs_pipeline']",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_ARM9_fields=[stage.design_field(n) for bank in staged['owned_banks'] for n in bank['model_ids']],\n"
            "        owned_label_regions=staged['owned_banks']",
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=6, text_display_revisions=0, justified_retentions=54, reviewed_UI_labels=60',
        'initialized_Rafael_dialogue=True': 'stock_model_link_shipyard=True, other_ship_names_offline=True',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['trade_armed_designs_20261115']",
        'name_label_revisions=2, justified_retentions=13': 'name_label_revisions=6, justified_retentions=54',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'The full outfitted ship catalogue has six readable design labels and 54 justified retentions.',
        '# Ritual Officiant Labels test candidate': '# Trade and Armed Ship Labels test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            'updates six abbreviated trade and armed design labels',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.OUTPUT, STARTUP, live.OUTPUT, live.SHEET, live.NATIVE, QA)",
        'Preserve verified ritual title candidate': 'Preserve verified trade and armed label candidate',
        'stage.digest(registry_before), ledger_before=stage.digest(ledger_before)':
            'stage.sha256(registry_before).hexdigest(), ledger_before=stage.sha256(ledger_before).hexdigest()',
    }
    env = vars(workflow) | globals() | {'VIEWED': viewed}
    exec(compile(checked_text(upstream, replacements), __file__ + '::register-stock-design-labels', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
