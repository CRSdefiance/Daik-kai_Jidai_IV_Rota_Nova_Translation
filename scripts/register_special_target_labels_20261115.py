"""Register the verified Ghost Ship class label and exact clean-input patch."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import stage_special_target_labels_20261115 as stage
from scripts import verify_special_target_labels_20261115 as live
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_release_baseline import files

base, parent = stage.base, stage.parent
PROFILE = 'all-routes-special-target-labels-v1-20261115'
ROOT = Path('out/special_target_labels_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Special_Target_Labels_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_special_target_labels_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_special_target_labels_20261115.md')
STARTUP = stage.ROOT / 'own_startup_verification.json'
QA = stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_special_target_labels_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta',
                         REBUILT=stage.ROOT / 'clean_reconstruction_RESEARCH_ONLY.nds')


def verify(prior, guard, viewed):
    staged, boot, game, draft = map(base.load, (stage.STORED, STARTUP, live.OUTPUT, stage.REVIEW))
    candidate = base.digest(stage.ROM)
    assert all(p['candidate_sha256'] == candidate for p in (staged, boot, game, draft))
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert all(base.digest(path) == sha for proof in (boot, game) for path, sha in proof['evidence'].items())
    assert base.digest(live.SHEET) == viewed == game['sheet_sha256'] and game['actual_selected_tooltips']
    assert all(len(item['panels']) == 2 for item in game['cases'].values())
    assert base.digest(stage.REVIEW) == staged['review_sha256']
    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests > 0 and all(int(suite.get(k, 0)) == 0 for k in ('failures', 'errors', 'skipped'))
    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    a, b = map(files, (old, new))
    assert a.keys() == b.keys() and {p for p in a if a[p] != b[p]} == {stage.ARM}
    arm = b[stage.ARM]
    assert arm == stage.patch(a[stage.ARM], clean.read_file(stage.ARM))
    assert stage.digest(arm) == staged['target_ARM9_sha256']
    snapshot = boot['read_only_snapshot']
    raw = Path(snapshot['path']).read_bytes()
    assert snapshot['read_only_export'] and stage.digest(raw) == snapshot['sha256']
    cpu, get = get_machine(arm, raw)
    obj = get(0xCB154) + 4 + 38 * 64
    address = get(0x1FD74, obj)
    assert address == stage.ALIAS_GHOST_SHIP and stage.c_string(cpu, address, 'ascii')['text'] == 'Ghost Ship'
    checked = bind_registered_story_percent_guard(guard)(files(clean), b)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    new.replace_file(stage.ARM, a[stage.ARM])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    assert len(draft['records']) == 6 and sum(row['decision'] == 'revision' for row in draft['records']) == 1
    for row in draft['records']:
        row['review']['formatting'] = True
        row['registered_candidate_sha256'] = candidate
    draft.update(gameplay=game, fresh_registered_class_name_startup={'pointer': address, 'name': 'Ghost Ship'},
                 checked_story_format_guard=checked, scene_activation_pending=False)
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
    note = """    base.replace_checked(DOC, f'''# Sea-inspection target names

The sea-inspection tooltip now shows the full **Ghost Ship** name. One class-table pointer uses the wording already approved for the battle result. The five retentions cover **Monster**, **Monster Fish**, **Giant Squid**, **Shark** and **Whale**. The original Japanese uses generic 鯨 for the class and 白鯨 for the White Whale model. The two English name getters for actor 181 use exactly the same **Monster** string seen in the tooltip. The selected tooltip supplies the player-facing context. A spoken header for that actor remains unobserved. [Exact references and review](../{REVIEW.as_posix()})

The current Monster Fish replay shows the complete category and class. In paired Ghost Ship replays, the setup selected the existing model by changing one link in the established encounter fixture. The game’s own inspection controls and formatter drew the tooltip, showed Charles’s reaction and the information notice, and returned to Info Mode. Both complete tooltip rows passed glyph checks before and after dismissal. A follow-up controller schedule allowed the earlier inspection and notice to settle before advancing. No natural spawn or hardware test was recorded. [Emulator comparison](../{(VERIFY / live.SHEET.name).as_posix()})

The [registered ROM and patch](../{PACKAGE.as_posix()}/README.md) preserve the other 38 class names, model records, and all 114 accepted layers. Six startup frames, 24 protected name getters and {tests} supported repository tests passed. The patch reconstructs every ROM byte. The legacy tooltip test files depend on the unavailable V139 ROM. The current formatter and gameplay checks supply direct evidence for this release.
'''.encode('utf-8'))"""
    replacements = {
        original[first:last]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 830 and len(manifest['checks']) == 165",
        '825 entries, 114 accepted layers and 160 passing checks': '831 entries, 114 accepted layers and 166 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160':
            'registered_manifest_entries=831, passing_release_checks=166',
        "verify(prior, profile['source25_multiarchive_guard'])": "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.special_target_labels.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.special_target_labels.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_special_target_labels.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_aziza_mutiny_predecessor=predecessor, special_target_labels_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['special_target_labels_pipeline']",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_ARM9_field={key: staged[key] for key in ('field', 'old_pointer', 'new_pointer')}",
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=1, text_display_revisions=0, justified_retentions=5, reviewed_UI_labels=6',
        'initialized_Rafael_dialogue=True': 'initialized_special_target_inspection=True',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['special_target_labels_20261115']",
        'name_label_revisions=2, justified_retentions=13': 'name_label_revisions=1, justified_retentions=5',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'The sea-inspection tooltip now names the Ghost Ship in full.',
        '# Ritual Officiant Labels test candidate': '# Special Target Labels test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            'shows the full Ghost Ship name in the sea-inspection tooltip',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, QA)",
        'Preserve verified ritual title candidate': 'Preserve verified special-target tooltip candidate',
    }
    env = vars(workflow) | globals() | {'VIEWED': viewed}
    exec(compile(checked_text(original, replacements), __file__ + '::registered-class-name-field', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
