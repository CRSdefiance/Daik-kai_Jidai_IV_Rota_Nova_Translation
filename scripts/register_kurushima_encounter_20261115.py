"""Register Maria's Kurushima encounter and its byte-exact clean-input patch."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import register_cristina_dance_patrons_20261115 as story
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import replay_kurushima_encounter_20261115 as live
from scripts import stage_kurushima_encounter_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-kurushima-encounter-v1-20261115'
ROOT = Path('out/kurushima_encounter_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Kurushima_Encounter_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_kurushima_encounter_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_kurushima_encounter_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_kurushima_encounter_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_rebuilt.nds')


def verify(prior, guard, viewed):
    source = getsource(story.verify)
    replacements = {
        "game['initialized_story'] and not game['natural_event_activation'] and not game['hardware']":
            "game['ordinary_saved_game'] and not game['injected_location'] and not game['hardware']",
        "len(game['held_panels']) == 3 and len(game['exact_control_frames']) == 9":
            "len(game['held_panels']) == 4 and len(game['exact_control_frames']) == 8",
        """    sheet, = staged['sheets']
    assert (base.digest(live.SHEET), base.digest(sheet['path'])) == viewed == (game['sheet_sha256'], sheet['sha256'])
    assert len(sheet['messages']) == 12 and base.digest(stage.MANUSCRIPT) == staged['manuscript_sha256']""":
            """    sheet, *other_sheets = staged['sheets']
    expected_views = tuple(row['sha256'] for row in staged['sheets'])
    assert (base.digest(live.SHEET), *expected_views) == viewed
    assert base.digest(live.SHEET) == game['sheet_sha256']
    assert all(base.digest(row['path']) == row['sha256'] for row in (sheet, *other_sheets))
    assert len(other_sheets) == 2 and staged['preview_count'] == 22
    assert base.digest(stage.MANUSCRIPT) == staged['manuscript_sha256']
    assert base.digest(stage.OBSERVATION) == staged['observation_sha256']
    draft['native_sheets'] = staged['sheets']""",
        "len(draft['records']) == 72 and sum(row['decision'] == 'revision' for row in draft['records']) == 9":
            "len(draft['records']) == 8 and sum(row['decision'] == 'revision' for row in draft['records']) == 4",
    }
    env = vars(story) | globals()
    exec(compile(checked_text(source, replacements), __file__ + '::verify', 'exec'), env)
    return env['verify'](prior, guard, viewed)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', nargs=4, required=True)
    viewed = tuple(parser.parse_args().viewed_sha)
    source = getsource(workflow.main)
    first = source.index('    base.replace_checked(DOC, f')
    last = source.index("'''.encode('utf-8'))", first) + len("'''.encode('utf-8'))")
    note = """    base.replace_checked(DOC, f'''# Maria’s encounter with Kurushima

All eight speeches were reviewed as one exchange. Four revisions sharpen Sojin’s accusation and coercive offer, restore Maria’s beard taunt, and give the opening challenge a stable wrap with a custom name. Four lines retain their earlier wording, including Yukihisa’s rebuke and counterquestion. Each decision has its exact clean Japanese, predecessor and registered record references. [Review ledger](../{REVIEW.as_posix()})

The earlier 16-character name split “woman” after “wom” and stranded “settling” on a row by itself. The two revised lines keep the runtime first-name substitution. The 1-, 2-, 5-, 15- and 16-character examples passed the original parser at four alignments and the progressive renderer’s complete glyph and one-page checks. All 22 before, after and retention previews were visually checked.

An ordinary cold load from the Nagasaki save reproduced the ship alert and all eight lines in the original encounter. The four revised panels matched their full native masks, and eight control frames matched exactly. No location fixture was used. The live run used Maria’s default name. Custom names were checked offline. [Emulator comparison](../{(VERIFY / live.SHEET.name).as_posix()})

The preceding alert displayed “in the E” for COMMON 618. The original sighting tables supply eight compass abbreviations and a separate close-range label. Their shared dialogue templates remain a follow-up.

The [registered ROM and clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve 114 accepted layers and the ASCII right-bound correction. Six startup frames, 24 protected name getters and {tests} targeted tests passed. These eight speeches already carried editorial credit.
'''.encode('utf-8'))"""
    replacements = {
        source[first:last]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 838 and len(manifest['checks']) == 173",
        '825 entries, 114 accepted layers and 160 passing checks': '839 entries, 114 accepted layers and 174 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160':
            'registered_manifest_entries=839, passing_release_checks=174',
        "verify(prior, profile['source25_multiarchive_guard'])":
            "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.kurushima_encounter.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.kurushima_encounter.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_kurushima_encounter.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_voyage_rats_and_search_predecessor=predecessor, kurushima_encounter_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['kurushima_encounter_pipeline']",
        "manifest['changed_records'][stage.ARM].extend(r['id'] for r in draft['records'] if r['decision'] == 'revision')":
            "records = manifest['changed_records'][stage.FILE]\n"
            "    for row in draft['records']:\n"
            "        if row['decision'] == 'revision' and row['id'] not in records:\n"
            "            records.append(row['id'])",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_story_blocks={stage.FILE: list(stage.BLOCKS)}",
        "target_ARM9_sha256=staged['target_ARM9_sha256'],":
            "target_ARM9_sha256=staged['target_ARM9_sha256'], "
            "target_SC3_sha256=staged['target_story_archive_sha256'][stage.FILE],",
        "ARM9_sha256=release['target_ARM9_sha256'], registered_release_verification=str(RELEASE)":
            "ARM9_sha256=release['target_ARM9_sha256'], SC3_sha256=release['target_SC3_sha256'], "
            "registered_release_verification=str(RELEASE)",
        'changed_components=[stage.ARM], changed_internal_files=[]':
            'changed_components=[], changed_internal_files=[stage.FILE]',
        'initialized_Rafael_dialogue=True': 'ordinary_saved_nagasaki_encounter=True',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=2, justified_retentions=4, reviewed_UI_labels=0',
        'new_contextual_records=0, prose_revisions=0,': 'new_contextual_records=0, prose_revisions=4,',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['kurushima_encounter_20261115']",
        'name_label_revisions=2, justified_retentions=13': 'prose_revisions=4, justified_retentions=4',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'Maria’s encounter with Kurushima has four dialogue revisions and stable custom-name wrapping.',
        '# Ritual Officiant Labels test candidate': '# Kurushima Encounter test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            'revises Maria’s complete Kurushima encounter',
        'Preserve verified ritual title candidate': 'Preserve verified Kurushima Encounter candidate',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, QA, *(Path(s['path']) for s in draft['native_sheets']))",
    }
    env = vars(workflow) | globals() | {'VIEWED': viewed}
    exec(compile(checked_text(source, replacements), __file__ + '::register', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
