"""Register the verified specialized class and design labels."""

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
from scripts import stage_specialized_ship_labels_20261115 as stage
from scripts import verify_specialized_ship_labels_20261115 as live
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-specialized-ship-labels-v1-20261115'
ROOT = Path('out/specialized_ship_labels_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Specialized_Ship_Labels_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_specialized_ship_labels_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_specialized_ship_labels_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_specialized_ship_labels_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_rebuilt.nds')


def verify(prior, guard, viewed):
    staged, native, focused, boot = map(base.load, (stage.OUTPUT, live.OUTPUT, live.FOCUSED, STARTUP))
    candidate = base.digest(stage.ROM)
    assert all(row['candidate_sha256'] == candidate for row in (staged, native, focused, boot))
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert all(base.digest(path) == sha for proof in (native, focused, boot) for path, sha in proof['evidence'].items())
    assert viewed == (base.digest(live.SHEET), base.digest(live.COMPARISON)) == (
        native['sheet_sha256'], focused['sheet_sha256'])
    assert native['class_getters_compared'] == 39 and native['initialized_models_compared'] == 155
    assert len(native['offline_previews']) == 17 and native['unchanged_actual_frame_count'] == 30
    assert focused['same_pixels_except_complete_design_names'] and focused['verified_entry_and_returns']
    assert len(focused['verified']) == 3 and focused['unlisted_models'] == [65, 82]
    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests == 32 and not any(int(suite.get(key, 0)) for key in ('failures', 'errors', 'skipped'))

    clean, old, test = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(stage.files, (old, test))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {stage.ARM}
    runtime = RegisteredRuntime(parent.RELEASE, prior['own_registered_startup'], captain=3)
    arm, records = stage.stage(runtime, clean, old)
    assert arm == after[stage.ARM] and stage.sha256(arm).hexdigest() == staged['target_ARM9_sha256']
    assert dumps(records, sort_keys=True) == dumps(staged['records'], sort_keys=True)
    guard_result = bind_registered_story_percent_guard(guard)(stage.files(clean), after)
    assert guard_result['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(guard_result['source_bound_new_command_counts'].values())
    test.replace_file(stage.ARM, before[stage.ARM])
    assert bytes(test.rom.save()) == parent.ROM.read_bytes()
    for row in records:
        row['review']['formatting'] = True
        row['speaker'] = 'Ship catalogue'
        row['registered_candidate_sha256'] = candidate
    draft = staged | dict(records=records, native=native, focused=focused,
                          checked_story_format_guard=guard_result, display_checks_pending=False, registered=True)
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
    last = upstream.index("'''.encode('utf-8'))", first) + len("'''.encode('utf-8'))")
    note = """    base.replace_checked(DOC, f'''# Specialized ship labels

The catalogue now uses **Ship of the Line** for the standard hull and design. **Suetsugu** replaces the earlier romanization and supplies the English missing from the standard design. **Trade Suetsugu** and **Armed Suetsugu** preserve the two fittings. **Cargo Galley**, **Large Cargo Galley** and **Cargo Galleass** distinguish the three designs. **Cargo Line Ship**, **War Line Ship** and **Cargo Ironclad** show the hull and fitting in full. The 17 individual decisions include seven justified retentions and exact Japanese and English references. [Registered review](../{REVIEW.as_posix()})

The Nagasaki Museum of History and Culture uses Suetsugu for 末次船 in its collection. Royal Museums Greenwich uses the established English hull term ship of the line. [Nagasaki museum catalogue](https://jmapps.ne.jp/nmhc_public/det.html?data_id=30343) · [Royal Museums Greenwich](https://www.rmg.co.uk/collections/library/rmgl-152988)

The ordinary Istanbul Special purchase entry matches in 30 paired frames. A focused test used one stock model link in a copied-save session, and the original Shipyard screen drew **Large Cargo Galley** in full in the list and detail field. The hull, cargo capacity, price and surrounding pixels match the previous build. The same route did not list Ship of the Line or Suetsugu. Those two class labels passed the native sea-inspection formatter offline. All 39 class getters, 155 initialized models and 17 native font previews passed. [Focused comparison](../{(VERIFY / live.COMPARISON.name).as_posix()}) · [Font previews](../{(VERIFY / live.SHEET.name).as_posix()})

The [cumulative candidate and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve 114 accepted layers and the ASCII right bound. The build passed its own cold boot, six comparison frames, 24 protected name getters and {tests} targeted tests. Hardware and ordinary acquisition of the revised designs remain unvisited. The other abbreviated trade and armed designs remain in scope. The ledger credits 27,700 reviewed dialogue and prose records and tracks 276 pending stored COMMON keys.
'''.encode('utf-8'))"""
    replacements = {
        upstream[first:last]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 845 and len(manifest['checks']) == 180",
        '825 entries, 114 accepted layers and 160 passing checks': '846 entries, 114 accepted layers and 181 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160':
            'registered_manifest_entries=846, passing_release_checks=181',
        "verify(prior, profile['source25_multiarchive_guard'])":
            "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.specialized_ship_labels.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.specialized_ship_labels.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_specialized_ship_labels.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_market_trade_predecessor=predecessor, specialized_ship_labels_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['specialized_ship_labels_pipeline']",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_ARM9_fields=[ref['pointer_field'] for row in staged['records'] if row['decision'] == 'revision'\n"
            "                          for ref in row['source_references']], owned_payload_reuse=stage.BANK",
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=10, text_display_revisions=0, justified_retentions=7, reviewed_UI_labels=17',
        'initialized_Rafael_dialogue=True': 'stock_model_link_shipyard=True, other_ship_names_offline=True',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['specialized_ship_labels_20261115']",
        'name_label_revisions=2, justified_retentions=13': 'name_label_revisions=10, justified_retentions=7',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'Ship of the Line, Suetsugu and the related specialized designs have ten label revisions.',
        '# Ritual Officiant Labels test candidate': '# Specialized Ship Labels test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            'updates Ship of the Line, Suetsugu and the related specialized designs',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.OUTPUT, STARTUP, live.OUTPUT, live.SHEET, live.FOCUSED, live.COMPARISON, QA)",
        'Preserve verified ritual title candidate': 'Preserve verified specialized ship label candidate',
        'stage.digest(registry_before), ledger_before=stage.digest(ledger_before)':
            'stage.sha256(registry_before).hexdigest(), ledger_before=stage.sha256(ledger_before).hexdigest()',
    }
    env = vars(workflow) | globals() | {'VIEWED': viewed}
    exec(compile(checked_text(upstream, replacements), __file__ + '::registered-ship-label-fields', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
