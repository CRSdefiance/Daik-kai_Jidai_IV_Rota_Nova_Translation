"""Register the 15 fleet alerts and their scoped spoken bearing mapping."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import register_square_trend_dialogue_20261115 as previous
from scripts import replay_fleet_sighting_alerts_20261115 as live
from scripts import stage_fleet_sighting_alerts_20261115 as stage
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.source_locked_derivation_v5118 import checked_text


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-fleet-sighting-alerts-v1-20261115'
ROOT = Path('out/fleet_sighting_alerts_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Fleet_Sighting_Alerts_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_fleet_sighting_alerts_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_fleet_sighting_alerts_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_fleet_sighting_alerts_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_rebuilt.nds')


def verify(prior, guard, viewed):
    original = getsource(previous.verify)
    matrix = """    for n in stage.REVISIONS:
        cases = [r for r in staged['native_cases'] if r['id'] == n]
        assert len(cases) == (1 if n == 732 else 124)
        assert all(not row['findings'] and row['complete_bytes_and_guarded_printf_wrap_ABI'] for row in cases)"""
    replacements = {
        "game['ordinary_saved_game'] and game['comparison_dependencies_match_parent'] and not game['hardware']":
            "game['ordinary_saved_game'] and not game['injected_location'] and not game['hardware']",
        "len(game['revised_holds']) == 5 and {row['message_ID'] for row in game['revised_holds']} == {654, 732}":
            "len(game['revised_holds']) == 1 and game['revised_holds'][0]['message_ID'] == 618",
        "len(game['native_only_revisions']) == 3 and game['exact_control_frames']":
            "len(game['unvisited_sighting_messages']) == 14 and len(game['exact_control_frames']) == 12",
        """    sheet, = staged['sheets']
    assert (base.digest(live.SHEET), base.digest(sheet['path'])) == viewed == (game['sheet_sha256'], sheet['sha256'])
    assert len(sheet['messages']) == 13 and len(staged['native_cases']) == 640""":
            """    sheet, *others = staged['sheets']
    assert len(others) == 2 and sum(len(row['messages']) for row in staged['sheets']) == 45
    assert all(base.digest(row['path']) == row['sha256'] for row in staged['sheets'])
    assert (base.digest(live.SHEET), *(row['sha256'] for row in staged['sheets'])) == viewed
    assert base.digest(live.SHEET) == game['sheet_sha256'] and len(staged['native_cases']) == 2700
    draft['native_sheets'] = staged['sheets']""",
        matrix: """    assert len(staged['bearing_controls']) == 73 and len(staged['original_compass_cases']) == 9
    assert len(staged['original_faction_names']) == 20
    assert all(row['native_printf_wrap_and_canaries'] for row in staged['native_cases'])
    assert sum('plane_sha256' in row for row in staged['native_cases']) == 45""",
        "{stage.COMMON}\n    arm, common": "{stage.ARM, stage.COMMON}\n    arm, common",
        """    assert stage.digest(arm) == staged['target_ARM9_sha256'] == prior['target_ARM9_sha256']
    checked = bind_registered_story_percent_guard(guard)(stage.files(clean), after)""":
            """    compiled_arm, mapping = stage.bearings.install(arm, clean.read_file(stage.ARM), prior['target_ARM9_sha256'])
    assert compiled_arm == after[stage.ARM] and mapping == staged['bearings']
    assert stage.digest(compiled_arm) == staged['target_ARM9_sha256']
    snapshot = boot['read_only_snapshot']
    assert base.digest(snapshot['path']) == snapshot['sha256']
    raw = Path(snapshot['path']).read_bytes()
    for item in mapping['changes']:
        index = item['address'] - stage.bearings.BASE
        assert raw[index:index + 4].hex() == item['after']
    verify_runtime(compiled_arm, prior)
    checked = bind_registered_story_percent_guard(guard)(stage.files(clean), after)""",
        '    new.replace_file(stage.COMMON, common)': '    new.replace_file(stage.COMMON, common)\n    new.replace_file(stage.ARM, arm)',
        "len(draft['records']) == 8 and sum(row['decision'] == 'revision' for row in draft['records']) == 5":
            "len(draft['records']) == 15 and all(row['decision'] == 'revision' for row in draft['records'])",
    }
    scope = vars(previous) | globals()
    exec(compile(checked_text(original, replacements), __file__ + '::verify', 'exec'), scope)
    return scope['verify'](prior, guard, viewed)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', nargs=4, required=True)
    viewed = tuple(parser.parse_args().viewed_sha)
    original = getsource(workflow.main)
    first = original.index('    base.replace_checked(DOC, f')
    last = original.index("'''.encode('utf-8'))", first) + len("'''.encode('utf-8'))")
    note = """    base.replace_checked(DOC, f'''# Fleet sighting and incoming-attack alerts

The [registered review](../{REVIEW.as_posix()}) updates all eight preparation alerts and all seven incoming-attack alerts from the clean Japanese. The lookout can say “to the east” or “nearby” where the earlier message used “in the E” or “in the vicinity.” The reports preserve the bearing and fleet substitutions, and distinguish preparations from an attack already underway.

Three original call sites reuse the previously registered pirate bearing mapper. The shared code stays in its original allocation, the pirate entry keeps its two-table guard, and the compass provider still returns the original abbreviations. Seventy-three native route tests cover the original call contexts, nine directions and fallback pointers. All 2,700 combinations of message, direction and stock faction fit within three rows with complete bearing phrases and faction names. All 45 native preview pages were checked and viewed.

An ordinary emulator replay from the Nagasaki save verified the complete east-bearing report, its Kurushima substitution and the Sailor nameplate. Twelve complete frames match the prior candidate, including Maria’s eight-line encounter. The other fourteen alerts, including close-range and incoming-attack variants, were checked offline. Hardware remains unvisited. [Emulator comparison](../{(VERIFY / live.SHEET.name).as_posix()})

The [registered ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve 114 accepted layers and the ASCII right-bound correction. Six startup frames, 24 protected name getters and {tests} targeted tests passed. The 15 reports already had editorial credit.
'''.encode('utf-8'))"""
    replacements = {
        original[first:last]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 839 and len(manifest['checks']) == 174",
        '825 entries, 114 accepted layers and 160 passing checks': '840 entries, 114 accepted layers and 175 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160':
            'registered_manifest_entries=840, passing_release_checks=175',
        "verify(prior, profile['source25_multiarchive_guard'])":
            "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.fleet_sighting_alerts.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.fleet_sighting_alerts.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_fleet_sighting_alerts.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_kurushima_encounter_predecessor=predecessor, fleet_sighting_alerts_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['fleet_sighting_alerts_pipeline']",
        "manifest['changed_records'][stage.ARM].extend(r['id'] for r in draft['records'] if r['decision'] == 'revision')":
            "manifest['changed_records'][stage.ARM].append('FLEET_SIGHTING_BEARING_CALLS')\n"
            "    records = manifest['changed_records'][stage.COMMON]\n"
            "    records.extend(row['id'] for row in draft['records'] if row['id'] not in records)",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_bearing_calls=staged['bearings'], owned_COMMON_allocations=staged['allocations'], "
            "native_runtime_producer_sha256=base.digest(stage.bearings.__file__)",
        "target_ARM9_sha256=staged['target_ARM9_sha256'],":
            "target_ARM9_sha256=staged['target_ARM9_sha256'], target_COMMON_sha256=staged['target_COMMON_sha256'],",
        "ARM9_sha256=release['target_ARM9_sha256'], registered_release_verification=str(RELEASE)":
            "ARM9_sha256=release['target_ARM9_sha256'], COMMON_sha256=release['target_COMMON_sha256'], "
            "registered_release_verification=str(RELEASE)",
        'changed_components=[stage.ARM], changed_internal_files=[]':
            'changed_components=[stage.ARM], changed_internal_files=[stage.COMMON]',
        'initialized_Rafael_dialogue=True': 'ordinary_saved_nagasaki_sighting=True',
        'new_contextual_records=0, prose_revisions=0,': 'new_contextual_records=0, prose_revisions=15,',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=15, justified_retentions=0, reviewed_UI_labels=0',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['fleet_sighting_alerts_20261115']",
        'name_label_revisions=2, justified_retentions=13': 'prose_revisions=15, justified_retentions=0',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'Fleet lookouts now give spoken directions in all 15 sighting and attack alerts.',
        '# Ritual Officiant Labels test candidate': '# Fleet Sighting Alerts test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            'localizes directions in all 15 fleet alerts',
        'Preserve verified ritual title candidate': 'Preserve verified Fleet Sighting Alerts candidate',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, QA, *(Path(s['path']) for s in draft['native_sheets']))",
    }
    env = vars(workflow) | globals() | {'VIEWED': viewed}
    exec(compile(checked_text(original, replacements), __file__ + '::register', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()

