"""Register the bounded rat and search report revisions with the exact patch."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import register_square_trend_dialogue_20261115 as previous
from scripts import stage_voyage_rat_and_search_dialogue_20261115 as stage
from scripts import verify_voyage_rat_and_search_dialogue_20261115 as live
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.source_locked_derivation_v5118 import checked_text


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-voyage-rats-and-search-v1-20261115'
ROOT = Path('out/voyage_rats_and_search_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Voyage_Rats_and_Search_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_voyage_rats_and_search_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_voyage_rats_and_search_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_voyage_rats_and_search_dialogue_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_rebuilt.nds',
                         NATIVE=live.REGIONAL)


def verify(prior, guard, viewed):
    original = getsource(previous.verify)
    old_matrix = """    for n in stage.REVISIONS:
        cases = [r for r in staged['native_cases'] if r['id'] == n]
        assert len(cases) == (1 if n == 732 else 124)
        assert all(not row['findings'] and row['complete_bytes_and_guarded_printf_wrap_ABI'] for row in cases)"""
    new_matrix = """    assert {row['message_ID'] for row in staged['native_cases']} == set(stage.RATS) | set(stage.SEARCH)
    assert all(row['one_panel'] and row['original_wrapper_after']['original_file_reads'] for row in staged['native_cases'])
    assert (base.digest(staged['observation']) == staged['observation_sha256'] and
            base.load(live.REGIONAL)['candidate_sha256'] == prior['candidate_sha256'])"""
    replacements = {
        "game['ordinary_saved_game'] and game['comparison_dependencies_match_parent'] and not game['hardware']":
            "game['ordinary_saved_game'] and game['comparison_ROM_sha256'] == prior['candidate_sha256'] and not game['hardware']",
        "len(game['revised_holds']) == 5 and {row['message_ID'] for row in game['revised_holds']} == {654, 732}":
            "len(game['revised_holds']) == 2 and {row['message_ID'] for row in game['revised_holds']} == {408, 2221}",
        "len(game['native_only_revisions']) == 3 and game['exact_control_frames']":
            "len(game['native_only_revisions']) == 4 and len(game['exact_control_frames']) == 4",
        "len(sheet['messages']) == 13 and len(staged['native_cases']) == 640":
            "len(sheet['messages']) == 19 and len(staged['native_cases']) == 13",
        old_matrix: new_matrix,
        "    checked = bind_registered_story_percent_guard(guard)(stage.files(clean), after)":
            "    verify_runtime(after[stage.ARM], prior)\n"
            "    checked = bind_registered_story_percent_guard(guard)(stage.files(clean), after)",
        "len(draft['records']) == 8 and sum(row['decision'] == 'revision' for row in draft['records']) == 5":
            "len(draft['records']) == 13 and sum(row['decision'] == 'revision' for row in draft['records']) == 6",
    }
    env = vars(previous) | globals()
    exec(compile(checked_text(original, replacements), __file__ + '::verify', 'exec'), env)
    return env['verify'](prior, guard, viewed)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', nargs=2, required=True)
    viewed = tuple(parser.parse_args().viewed_sha)
    original = getsource(workflow.main)
    first = original.index('    base.replace_checked(DOC, f')
    last = original.index("'''.encode('utf-8'))", first) + len("'''.encode('utf-8'))")
    note = """    base.replace_checked(DOC, f'''# Rat warnings and shore-search replies

I reviewed all eight rat-warning variants and all five replies for an empty shore search against the clean Japanese. Six revisions keep whole phrases on the same line, and seven individually justified retentions keep the already effective voices. The warnings report food at risk. The search replies preserve the difference between an area that seems empty and a report of nothing worth bringing back. [Exact review](../{REVIEW.as_posix()})

A cold load of the original voyage save reproduced Manuel’s rat warning and his empty-search report. The original message requests identify COMMON 408 and 2221. The revised hold for 408 keeps the ship-wide warning together. The revised 2221 puts the expedition’s return and its tentative result on two complete rows. Both before-and-after masks, Manuel’s nameplate and four unchanged sample frames passed. COMMON 405 was verified offline and did not trigger in this voyage. The four other revisions received native offline checks. All 19 native previews were viewed. [Voyage comparison](../{(VERIFY / live.SHEET.name).as_posix()})

Separate cold loads covered six Lisbon Square and Tavern holds and a ship alert followed by all eight lines in Maria’s encounter with Kurushima after departing Nagasaki. The replay used a copy of the Nagasaki save without the older Osaka position fixture. The trace leaves three lines in that encounter for a contextual prose follow-up. [Regional observation](../{(VERIFY / live.REGIONAL.name).as_posix()})

The [registered ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve 114 accepted layers and the ASCII right-bound correction. Six startup frames, 24 protected name getters and {tests} targeted tests passed. The 13 shared reports already carried editorial credit.
'''.encode('utf-8'))"""
    replacements = {
        original[first:last]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 837 and len(manifest['checks']) == 172",
        '825 entries, 114 accepted layers and 160 passing checks': '838 entries, 114 accepted layers and 173 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160':
            'registered_manifest_entries=838, passing_release_checks=173',
        "verify(prior, profile['source25_multiarchive_guard'])":
            "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.voyage_rats_and_search.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.voyage_rats_and_search.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_voyage_rats_and_search.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_embedded_story_roles_predecessor=predecessor, voyage_rats_and_search_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['voyage_rats_and_search_pipeline']",
        "manifest['changed_records'][stage.ARM].extend(r['id'] for r in draft['records'] if r['decision'] == 'revision')":
            "records = manifest['changed_records'][stage.COMMON]\n"
            "    for row in draft['records']:\n"
            "        if row['decision'] == 'revision' and row['id'] not in records:\n"
            "            records.append(row['id'])",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_COMMON_allocations=staged['allocations']",
        "target_ARM9_sha256=staged['target_ARM9_sha256'],":
            "target_ARM9_sha256=staged['target_ARM9_sha256'], target_COMMON_sha256=staged['target_COMMON_sha256'],",
        "ARM9_sha256=release['target_ARM9_sha256'], registered_release_verification=str(RELEASE)":
            "ARM9_sha256=release['target_ARM9_sha256'], COMMON_sha256=release['target_COMMON_sha256'], "
            "registered_release_verification=str(RELEASE)",
        'changed_components=[stage.ARM], changed_internal_files=[]':
            'changed_components=[], changed_internal_files=[stage.COMMON]',
        'initialized_Rafael_dialogue=True': 'ordinary_saved_voyage=True',
        'new_contextual_records=0, prose_revisions=0,':
            'new_contextual_records=0, prose_revisions=6,',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=6, justified_retentions=7, reviewed_UI_labels=0',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['voyage_rats_and_search_20261115']",
        'name_label_revisions=2, justified_retentions=13': 'prose_revisions=6, justified_retentions=7',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'Rat warnings and empty-search replies now keep their phrases together in the voyage dialogue.',
        '# Ritual Officiant Labels test candidate': '# Voyage Rats and Search test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            'improves the rat warnings and empty shore-search replies',
        'Preserve verified ritual title candidate': 'Preserve verified Voyage Rats and Search candidate',
    }
    env = vars(workflow) | globals() | {'VIEWED': viewed}
    exec(compile(checked_text(original, replacements), __file__ + '::register', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
