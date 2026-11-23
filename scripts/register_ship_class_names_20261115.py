"""Register the verified ship-class names through the cumulative release workflow."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from struct import unpack_from
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import stage_ship_class_names_20261115 as stage
from scripts import verify_ship_class_names_20261115 as live
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_special_target_labels_20261115 import c_string
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_release_baseline import files


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-ship-class-names-v1-20261115'
ROOT = Path('out/ship_class_names_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Ship_Class_Names_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_ship_class_names_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_ship_class_names_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_ship_class_names_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta',
                         REBUILT=stage.ROOT / 'clean_reconstruction_RESEARCH_ONLY.nds')
SOURCE_MEANINGS = {
    'SHIP_CLASS_NAME_5': 'A light galleon, distinguished from the unqualified galleon.',
    'SHIP_CLASS_NAME_20': 'The small galley class.',
    'SHIP_CLASS_NAME_21': 'A galley without a size qualifier.',
    'SHIP_CLASS_NAME_22': 'The large galley class.',
}


def retention(clean, arm):
    refs = []
    for role, field in (('class', 0x11CC40), ('stock design', 0x11D3CC)):
        pointer, = unpack_from('<I', arm, field)
        assert unpack_from('<I', clean, field) == (pointer,)
        source_offset = pointer - stage.BASE
        japanese = 'ガレー'.encode('cp932') + b'\0'
        previous = b'Galley\0'
        assert clean[source_offset:source_offset + len(japanese)] == japanese
        assert arm[source_offset:source_offset + len(previous)] == previous
        refs.append(dict(consumer=role, file_path=stage.ARM, pointer_field=field,
            source_offset=source_offset, Japanese='ガレー', clean_hex=japanese.hex(), previous='Galley',
            previous_hex=previous.hex(), target_offset=source_offset, english='Galley', target_hex=previous.hex()))
    return dict(id='SHIP_CLASS_NAME_21', Japanese='ガレー', english='Galley', decision='retention',
        source_references=refs, context='The unqualified design and class between Small Galley and Large Galley.',
        localization_note='Galley preserves the unqualified Japanese class and remains distinct from both size variants.',
        review=dict.fromkeys(('source', 'context', 'localization', 'naturalness', 'formatting'), True))


def verify(prior, guard, viewed):
    staged, boot, game = map(base.load, (stage.STORED, STARTUP, live.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert all(p['candidate_sha256'] == candidate for p in (staged, boot, game))
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert all(base.digest(path) == sha for proof in (boot, game) for path, sha in proof['evidence'].items())
    assert base.digest(live.SHEET) == viewed == game['sheet_sha256'] and game['ordinary_standard_list_navigation']
    assert sum(map(len, game['verified_label_locations'].values())) == 22 and len(game['unchanged_frames']) == 13
    assert len(game['adjacent_galley_retention']) == 2

    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests == 32 and all(int(suite.get(k, 0)) == 0 for k in ('failures', 'errors', 'skipped'))
    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    a, b = map(files, (old, new))
    assert a.keys() == b.keys() and {p for p in a if a[p] != b[p]} == {stage.ARM}
    arm, records = stage.owned_patch(clean, old)
    assert arm == b[stage.ARM] and stage.sha256(arm).hexdigest() == staged['target_ARM9_sha256']
    assert records == staged['records']
    snapshot = boot['read_only_snapshot']
    raw = Path(snapshot['path']).read_bytes()
    assert snapshot['read_only_export'] and stage.sha256(raw).hexdigest() == snapshot['sha256']
    cpu, get = get_machine(arm, raw)
    classes = get(0xCB154)
    for cls, *_, name in stage.RECORDS:
        address = get(0x1FD74, classes + 4 + cls * 64)
        assert c_string(cpu, address, 'ascii')['text'] == name
    checked = bind_registered_story_percent_guard(guard)(files(clean), b)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    new.replace_file(stage.ARM, a[stage.ARM])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()

    records.append(retention(clean.read_file(stage.ARM), arm))
    for row in records:
        row['review']['formatting'] = True
        row['speaker'] = 'Shipyard catalogue and ship-class display'
        row['source_meaning'] = SOURCE_MEANINGS[row['id']]
        row['registered_candidate_sha256'] = candidate
    draft = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'], records=records,
        gameplay=game, checked_story_format_guard=checked, candidate_sha256=candidate,
        visually_reviewed_changed_frames=list(game['verified_label_locations']))
    validate_natural_dialogue_batch(draft)
    if not review.PATCH.exists():
        make_xdelta(stage.CLEAN, stage.ROM, review.PATCH)
    if not review.REBUILT.exists():
        apply_xdelta(stage.CLEAN, review.PATCH, review.REBUILT)
    assert review.REBUILT.read_bytes() == stage.ROM.read_bytes()
    return staged, draft, tests


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', required=True)
    viewed = parser.parse_args().viewed_sha
    original = getsource(workflow.main)
    first = original.index('    base.replace_checked(DOC, f')
    last = original.index("'''.encode('utf-8'))", first) + len("'''.encode('utf-8'))")
    note = """    base.replace_checked(DOC, f'''# Standard ship-class names

**Light Galleon**, **Small Galley** and **Large Galley** replace `Lt Galleon`, `Sm Galley` and `Lg Galley` in both the class table and the matching standard designs. **Galley** is retained for the unqualified design between the two size variants. Source and current pointer fields and complete Japanese/English strings are listed in the [registered review](../{REVIEW.as_posix()}). The separate `LineShip` and specialized design abbreviations still need a display pass.

Paired cold boots used ordinary controller input through Istanbul’s Shipyard and the Standard list. All three complete labels fit in the list and both detail fields. Twenty-two label pairs passed complete font-mask checks and all other pixels matched over 25 captured frame pairs, including menu returns. The original masts, capacity, prices and durability remain exact. The native sea-inspection formatter also returned all three names with their leading and trailing characters intact. No sailing encounter, purchase or hardware test was performed. [Emulator comparison](../{(VERIFY / live.SHEET.name).as_posix()})

Comparing all 39 class getters and 155 initialized ship records found only the three intended name changes in each. The six affected pointers share 48 bytes whose previous uses were already relocated. Six startup frames, 24 protected name getters, {tests} supported tests and byte-exact reconstruction from clean Japanese input passed. The [registered candidate](../{PACKAGE.as_posix()}/README.md) preserves all 114 accepted layers and the ASCII right bound. The dialogue ledger remains at 27,700 credited reviews, with 276 mapped shared keys still open.
'''.encode('utf-8'))"""
    replacements = {
        original[first:last]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 831 and len(manifest['checks']) == 166",
        '825 entries, 114 accepted layers and 160 passing checks': '832 entries, 114 accepted layers and 167 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160':
            'registered_manifest_entries=832, passing_release_checks=167',
        "verify(prior, profile['source25_multiarchive_guard'])": "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.ship_class_names.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.ship_class_names.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_ship_class_names.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_special_target_labels_predecessor=predecessor, ship_class_names_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['ship_class_names_pipeline']",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_ARM9_fields=[ref['pointer_field'] for row in staged['records'] for ref in row['source_references']],\n"
            "        owned_label_span=[staged['allocation_offset'], staged['allocation_size']]",
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=3, text_display_revisions=0, justified_retentions=1, reviewed_UI_labels=4',
        'initialized_Rafael_dialogue=True': 'ordinary_istanbul_shipyard_standard_list=True',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['ship_class_names_20261115']",
        'name_label_revisions=2, justified_retentions=13': 'name_label_revisions=3, justified_retentions=1',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'The Standard Shipyard list and details spell out Light Galleon, Small Galley and Large Galley.',
        '# Ritual Officiant Labels test candidate': '# Standard Ship Class Names test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            'spells out Light Galleon, Small Galley and Large Galley in their original class and design fields',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, QA)",
        'Preserve verified ritual title candidate': 'Preserve verified ship class name candidate',
    }
    env = vars(workflow) | globals() | {'VIEWED': viewed}
    exec(compile(checked_text(original, replacements), __file__ + '::registered-ship-class-name-fields', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
