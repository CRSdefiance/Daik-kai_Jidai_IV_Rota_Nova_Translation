"""Register the Port dialogue batch with the exact clean-input patch."""

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
from scripts import replay_port_supply_dialogue_20261115 as replay
from scripts import stage_port_supply_dialogue_20261115 as stage
from scripts import verify_port_supply_dialogue_20261115 as live
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.verify_release_baseline import files


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-port-supply-dialogue-v1-20261115'
ROOT = Path('out/port_supply_dialogue_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Port_Supply_Dialogue_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_port_supply_dialogue_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_port_supply_dialogue_20261115.md')
STARTUP, QA = replay.STARTUP, stage.ROOT / 'registered_qa.xml'
CHECK = 'registered_port_supply_dialogue_layout_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta',
                         REBUILT=stage.ROOT / 'clean_reconstruction_RESEARCH_ONLY.nds')


def verify(prior, guard, viewed):
    staged, boot, game, draft = map(base.load, (stage.STORED, STARTUP, live.OUTPUT, stage.MANUSCRIPT))
    candidate = base.digest(stage.ROM)
    assert all(p['candidate_sha256'] == candidate for p in (staged, boot, game, draft))
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert all(base.digest(p) == sha for proof in (boot, game) for p, sha in proof['evidence'].items())
    assert game['ordinary_Riga_departure'] and game['Copenhagen_preconditions_fixture_only']
    holds = [hold['record'] for case in game['cases'] for hold in case['complete_changed_message_holds']]
    assert holds == [813, 806, 814, 814] and game['native_only_changed_records'] == [816, 817]
    sheet, = staged['sheets']
    assert (base.digest(live.SHEET), base.digest(sheet['path'])) == viewed == (game['sheet_sha256'], sheet['sha256'])
    assert base.digest(stage.MANUSCRIPT) == staged['manuscript_sha256']
    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests == 42 and all(int(suite.get(k, 0)) == 0 for k in ('failures', 'errors', 'skipped'))

    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(files, (old, new))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {stage.COMMON}
    arm, common = before[stage.ARM], before[stage.COMMON]
    entries = owned_entries(common, arm, stage.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    edited = stage.encoded_changes({row['message_ID']: row['english'] for row in draft['records']})
    patched, _, slots = owned_deployment(common, arm, entries, edited)
    assert set(edited) == {row['n'] for row in staged['native_cases']}
    assert patched == after[stage.COMMON] and {str(k): v for k, v in slots.items()} == staged['allocations']
    assert stage.digest(patched) == staged['target_COMMON_sha256']
    assert stage.digest(arm) == staged['target_ARM9_sha256'] == prior['target_ARM9_sha256']
    checked = bind_registered_story_percent_guard(guard)(files(clean), after)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    new.replace_file(stage.COMMON, common)
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    for row in draft['records']:
        row['registered_reference'] = row['staged_reference'] | {'candidate_sha256': candidate}
        row['review']['formatting'] = True
    assert len(draft['records']) == 8 and sum(r['decision'] != 'retention' for r in draft['records']) == 5
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
    note = """    base.replace_checked(DOC, f'''# Port resupply and departure dialogue

The [registered review](../{REVIEW.as_posix()}) covers eight Port Worker lines. The worker now explains that extra food will be thrown out, offers a smaller refill when the player is short of gold, and asks about changing the mix of water and food. The low-water question and inn suggestion keep their prior wording with complete questions on the second line. The rest of the exchange retains the water-disposal warning, the empty-cargo reply and the price quote.

Two Copenhagen cold boots used the original refill and disposal controls. A fixture set the copied fleet’s supplies to zero water and 700 food before the player chose resupply. Both runs finished with 350 water, 350 food and 25,975 gold. The ordinary Riga departure showed the complete inn suggestion. The four revised panels match the native font masks. The small refill offer and supply mix prompt were checked offline. [Gameplay comparison](../{(VERIFY / live.SHEET.name).as_posix()})

The [registered ROM and clean-input patch](../{PACKAGE.as_posix()}/README.md) maintain the 114 accepted layers and ASCII right-bound correction. Six startup frames matched, 24 protected name getters and {tests} targeted tests passed, and the patch reproduced every ROM byte. Two repository tests for older optional mapper fixtures were outside the focused run. Physical hardware and the remaining shared-text scope are open.
'''.encode('utf-8'))"""
    replacements = {
        original[first:last]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 828 and len(manifest['checks']) == 163",
        '825 entries, 114 accepted layers and 160 passing checks': '829 entries, 114 accepted layers and 164 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160':
            'registered_manifest_entries=829, passing_release_checks=164',
        "verify(prior, profile['source25_multiarchive_guard'])": "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.port_supply_dialogue.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.port_supply_dialogue.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_port_supply_dialogue.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_london_stockholm_predecessor=predecessor, port_supply_dialogue_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['port_supply_dialogue_pipeline']",
        "manifest['changed_records'][stage.ARM].extend(r['id'] for r in draft['records'] if r['decision'] == 'revision')":
            "manifest['changed_records'][stage.COMMON].extend(r['id'] for r in draft['records'] if r['decision'] != 'retention')",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_COMMON_slots=staged['allocations']",
        "target_ARM9_sha256=staged['target_ARM9_sha256'],":
            "target_ARM9_sha256=staged['target_ARM9_sha256'], target_COMMON_sha256=staged['target_COMMON_sha256'],",
        'changed_components=[stage.ARM], changed_internal_files=[]': 'changed_components=[], changed_internal_files=[stage.COMMON]',
        'new_contextual_records=0, prose_revisions=0': 'new_contextual_records=0, prose_revisions=3',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=2, justified_retentions=3, reviewed_UI_labels=0',
        'initialized_Rafael_dialogue=True': 'Riga_departure=True, Copenhagen_supply_fixture=True',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['port_supply_dialogue_20261115']",
        'name_label_revisions=2, justified_retentions=13': 'prose_revisions=3, wrap_revisions=2, justified_retentions=3',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'Five resupply and departure prompts were revised, with three individual retentions.',
        '# Ritual Officiant Labels test candidate': '# Port Supply Dialogue test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            'improves Port resupply, disposal and departure dialogue',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, Path(draft['native_sheet']['path']), QA)",
        'Preserve verified ritual title candidate': 'Preserve verified Port supply dialogue candidate',
    }
    env = vars(workflow) | globals() | {'VIEWED': viewed}
    exec(compile(checked_text(original, replacements), __file__ + '::registered-Port-COMMON-successor', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
