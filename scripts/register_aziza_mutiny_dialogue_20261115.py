"""Register the verified Aziza story revisions and clean-input patch."""

from argparse import ArgumentParser
from inspect import getsource
import json
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import replay_aziza_mutiny_dialogue_20261115 as replay
from scripts import stage_aziza_mutiny_dialogue_20261115 as stage
from scripts import verify_aziza_mutiny_dialogue_20261115 as live
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_release_baseline import files

base, parent = stage.base, stage.parent
PROFILE = 'all-routes-aziza-mutiny-dialogue-v1-20261115'
ROOT = Path('out/aziza_mutiny_dialogue_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Aziza_Mutiny_Dialogue_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_aziza_mutiny_dialogue_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_aziza_mutiny_dialogue_20261115.md')
STARTUP, QA = replay.STARTUP, stage.ROOT / 'repository_qa.xml'
CHECK = 'registered_aziza_mutiny_layout_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta',
                         REBUILT=stage.ROOT / 'clean_reconstruction_RESEARCH_ONLY.nds')
NAMES = Path('translations/lil_residual_A_382_scoped_names_final_v1.json')


def verify(prior, guard, viewed):
    staged, boot, game, draft = map(base.load, (stage.STORED, STARTUP, live.OUTPUT, stage.REVIEW))
    candidate = base.digest(stage.ROM)
    assert all(p['candidate_sha256'] == candidate for p in (staged, boot, game, draft))
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert all(base.digest(path) == sha for proof in (boot, game) for path, sha in proof['evidence'].items())
    assert game['initialized_story_excerpts'] and len(game['holds']) == 3
    assert {row['record'] for row in game['holds']} == {row['id'] for row in draft['records'] if row['decision'] == 'revision'}
    sheet, = staged['sheets']
    assert (base.digest(live.SHEET), base.digest(sheet['path'])) == viewed == (game['sheet_sha256'], sheet['sha256'])
    assert base.digest(stage.REVIEW) == staged['review_sha256']
    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests > 0 and all(int(suite.get(k, 0)) == 0 for k in ('failures', 'errors', 'skipped'))
    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    a, b = map(files, (old, new))
    ctx = RegisteredRuntime(parent.RELEASE, prior['own_registered_startup'], captain=3)
    planned, records, scenes, _ = stage.plan(clean, ctx, base.load(parent.MANIFEST))
    assert a.keys() == b.keys() and {p for p in a if a[p] != b[p]} == set(planned)
    assert stage.sha(b[stage.ARM]) == staged['target_ARM9_sha256'] == prior['target_ARM9_sha256']
    assert all(b[p] == data and stage.sha(data) == staged['route_archives'][p] for p, data in planned.items())
    assert draft['contexts'] == json.loads(json.dumps(scenes))
    for row, rebound in zip(draft['records'], json.loads(json.dumps(records)), strict=True):
        assert all(row[k] == v for k, v in rebound.items())
        row['registered_reference'] = row['staged_reference'] | {'candidate_sha256': candidate}
        row['review']['formatting'] = True
    past = {row['actor_ID']: row for row in base.load(NAMES)['records']}
    for row in draft['nameplates']:
        previous = past[row['actor_ID']]
        assert all(previous['review'].values()) and previous['english'] == row['english']
        assert previous['actual_progressive_header_observed_in_disclosed_fixture']
        row['previous_name_review'] = {'path': str(NAMES), 'sha256': base.digest(NAMES), 'id': previous['id']}
        row['current_nameplate_replay'] = game['complete_nameplates'].get(row['english'], [])
        row['review']['formatting'] = True
    checked = bind_registered_story_percent_guard(guard)(files(clean), b)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    for p in planned:
        new.replace_file(p, a[p])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
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
    note = """    base.replace_checked(DOC, f'''# Aziza’s mutiny dialogue

Angel now orders his crew to take out both Aziza and the man who comes to her aid in Rafael’s and Hodram’s routes. His accusation about their losing streak and empty earnings also reads more like spoken dialogue in Hodram’s route. Lil’s and Maria’s existing orders already identify both targets. The [registered review](../{REVIEW.as_posix()}) retains Angel, Snake and Dandy as distinct pirate nicknames across 12 source exchanges.

All three revised lines fit on two rows and passed complete native glyph checks. Paired initialized Rafael and Hodram replays displayed the revised lines and complete Angel and Snake nameplates. The replays use selected original speech commands and ordinary button presses. Dandy has earlier Lil replay evidence and current getter checks. Natural activation, other branches, the name catalog layout and physical hardware remain open. [Before-and-after captures](../{(VERIFY / live.SHEET.name).as_posix()})

The [candidate and patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers, including the ASCII right-bound correction. Six cumulative startup frames, 24 protected name getters and {tests} targeted tests passed. The patch reconstructs the ROM byte for byte.
'''.encode('utf-8'))"""
    replacements = {
        original[first:last]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 829 and len(manifest['checks']) == 164",
        '825 entries, 114 accepted layers and 160 passing checks': '830 entries, 114 accepted layers and 165 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160':
            'registered_manifest_entries=830, passing_release_checks=165',
        "verify(prior, profile['source25_multiarchive_guard'])": "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.aziza_mutiny.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.aziza_mutiny.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_aziza_mutiny.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_port_supply_dialogue_predecessor=predecessor, aziza_mutiny_dialogue_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['aziza_mutiny_dialogue_pipeline']",
        "    manifest['changed_records'][stage.ARM].extend(r['id'] for r in draft['records'] if r['decision'] == 'revision')":
            """    for row in draft['records']:
        if row['decision'] == 'revision':
            manifest['changed_records'][row['file_path']].append(row['id'])""",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_route_archives=staged['route_archives']",
        'changed_components=[stage.ARM], changed_internal_files=[]':
            "changed_components=[], changed_internal_files=list(staged['route_archives'])",
        'new_contextual_records=0, prose_revisions=0': 'new_contextual_records=0, prose_revisions=3',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=0, justified_retentions=2, reviewed_UI_labels=0',
        'initialized_Rafael_dialogue=True': 'initialized_Rafael_and_Hodram_dialogue=True',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['aziza_mutiny_dialogue_20261115']",
        'name_label_revisions=2, justified_retentions=13': 'prose_revisions=3, justified_retentions=2, retained_nameplates=3',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'Three dialogue revisions clarify the mutiny against Aziza in Rafael’s and Hodram’s routes.',
        '# Ritual Officiant Labels test candidate': '# Aziza Mutiny Dialogue test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            'clarifies Angel’s accusation and order during the mutiny against Aziza',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, Path(draft['native_sheet']['path']), QA)",
        'Preserve verified ritual title candidate': 'Preserve verified Aziza mutiny dialogue candidate',
    }
    registration_stage = SimpleNamespace(**(vars(stage) | {'digest': stage.sha}))
    env = vars(workflow) | globals() | {'VIEWED': viewed, 'stage': registration_stage}
    exec(compile(checked_text(original, replacements), __file__ + '::registered-two-story-archives', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
