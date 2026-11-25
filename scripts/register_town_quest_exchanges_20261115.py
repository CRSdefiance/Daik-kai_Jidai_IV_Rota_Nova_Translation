"""Register the verified town quest revision with the cumulative clean-input patch."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import reconcile_shared_speaker_labels_20261111 as names
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import replay_town_quest_exchanges_20261115 as replay
from scripts import stage_town_quest_exchanges_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, parent, native = stage.base, stage.parent, stage.native
PROFILE = 'all-routes-town-quest-exchanges-v1-20261115'
ROOT = Path('out/town_quest_exchanges_registered_20261115_v2')
ROM = ROOT / 'Translation_DS_All_Routes_Town_Quest_Exchanges_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_town_quest_exchanges_v2_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_town_quest_exchanges_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_town_quest_exchanges_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_rebuilt.nds')
CHOICE_SOURCE = Path('work/analysis/lil_B197_source_paths_v5661/three_actual_source_menu_paths_and_original_response_intervals.json')


def verify(prior, guard, viewed):
    staged, draft, boot = map(base.load, (stage.STORED, stage.MANUSCRIPT, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == staged['candidate_sha256'] == draft['candidate_sha256'] == boot['candidate_sha256']
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(native.CLEAN) == prior['clean_input_sha256']
    assert staged['manuscript_sha256'] == base.digest(stage.MANUSCRIPT)
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert all(base.digest(path) == sha for path, sha in boot['evidence'].items())
    proof_sheets = list(staged['sheets'])
    assert len(proof_sheets) == 7 and staged['preview_count'] == 55
    indexed_artifacts, gameplay = {}, {}
    for case, count in [('book', 14), ('prophecy', 18), ('sextant', 9)]:
        path = replay.folder(case) / 'verified.json'
        result = base.load(path)
        assert result['candidate_sha256'] == candidate
        assert result['initialized_emulator'] and not result['natural_activation'] and not result['hardware']
        assert len(result['complete_holds']) == count
        assert all(base.digest(p) == sha for p, sha in result['evidence'].items())
        proof_sheets.extend(result['sheets'])
        indexed_artifacts.update({Path(r['path']): f'{case}_{Path(r["path"]).name}' for r in result['sheets']})
        indexed_artifacts[path] = f'{case}_replay_receipt.json'
        gameplay[case] = result
    book_capture = base.load(gameplay['book']['report'])['frames_captured']
    book_frames = {f['frame']: f for f in book_capture}
    for frame, name in ((6575, 'book_delegate_selected'), (9450, 'book_gift_notice'), (9775, 'book_charm_notice')):
        scanned = book_frames[frame]
        assert base.digest(scanned['path']) == scanned['PNG_sha256']
        proof_sheets.append(dict(path=scanned['path'], sha256=scanned['PNG_sha256']))
        indexed_artifacts[Path(scanned['path'])] = f'{name}.png'
        gameplay['book'][name] = scanned
    assert tuple(s['sha256'] for s in proof_sheets) == viewed
    assert all(base.digest(r['path']) == r['sha256'] for r in proof_sheets)
    choice_proof = base.load(CHOICE_SOURCE)
    assert [r['actual_choice_result'] for r in choice_proof['versions']] == [[2, 0], [2, 1], [2, 2]]
    assert all(r['source_FE_Ian_Charm_notice_selected'] for r in choice_proof['versions'])

    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests == 32 and not any(int(suite.get(key, 0)) for key in ('failures', 'errors', 'skipped'))
    clean, old, final = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    before, after = map(native.files, (old, final))
    story_hashes = staged['target_story_archive_sha256']
    assert len(story_hashes) == 4 and before.keys() == after.keys()
    assert after[native.ARM] == before[native.ARM]
    assert native.digest(after[native.ARM]) == staged['target_ARM9_sha256']
    assert {p for p in before if before[p] != after[p]} == story_hashes.keys()
    records, choices = draft['records'], draft['retained_menu_options']
    assert len(records) == 198 and len(choices) == 12
    assert sum(r['decision'] == 'revision' for r in records) == 52
    credited = {(r['file_path'], r['id']) for r in base.load(base.LEDGER)[base.CONTEXT]['integrated_record_keys']}
    assert all((r['file_path'], r['id']) in credited for r in records)
    targets = dict(native.transform(old, records))
    for path, expected in story_hashes.items():
        assert targets[path] == after[path] and native.digest(after[path]) == expected
        final.replace_file(path, before[path])
    assert bytes(final.rom.save()) == parent.ROM.read_bytes()
    guard_check = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert guard_check['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(guard_check['source_bound_new_command_counts'].values())
    ctx = native.RegisteredRuntime(parent.RELEASE, prior['own_registered_startup'], captain=3)
    name_ids = (161, 169, 170)
    actors = dict(zip(name_ids, ('Villager', 'Alluring Woman', 'Mysterious Old Man'), strict=True))
    original_names = [r for r in base.load(native.PREVIOUS)['records'] if r['actor_ID'] in name_ids]
    assert {r['actor_ID']: r['english'] for r in original_names} == actors
    actual_names = names.current_getters(ctx)['rows']
    for name in original_names:
        ident = name['actor_ID']
        getters = actual_names[2 * ident:2 * ident + 2]
        assert all(g['actor_ID'] == ident and g['text'] == actors[ident] for g in getters)
        name['verified_predecessor_getters'] = getters
        name['verified_ARM9_sha256'] = staged['target_ARM9_sha256']
        name['candidate_sha256'] = candidate
    for row in records:
        if row['source_selector'] in actors:
            row['speaker'] = actors[row['source_selector']]
        row['registered_reference'] = row['staged_reference'] | dict(candidate_sha256=candidate)
        row['display_scope'] = 'offline native renderer' if row['decision'] == 'revision' else 'byte-identical retention'
        observed = any(row['id'] == hold['id'] for result in gameplay.values() for hold in result['complete_holds'])
        if row['route'] == 3 and (observed or (row['group'] == 'book' and row['turn'] == 20)):
            row['display_scope'] += ' and initialized emulator'
    for choice in choices:
        choice['initialized_Maria_menu_observation'] = choice['file_path'] == '/data/SC3.DK4'
        choice['review'] = dict.fromkeys(native.GATES, True)
        choice['registered_offset'] = choice['current_offset']
        choice['review_scope'] = 'Byte-identical menu label and choice command. All three outcomes were observed in the earlier Lil source replay.'
    draft.update(registered=True, zero_new_credit=True, native_sheets=staged['sheets'], gameplay=gameplay,
                 retained_speaker_labels=original_names,
                 earlier_Lil_book_choice_proof=dict(path=str(CHOICE_SOURCE), sha256=base.digest(CHOICE_SOURCE)),
                 checked_story_format_guard=guard_check)
    validate_natural_dialogue_batch(draft)
    assert review.REBUILT.read_bytes() == stage.ROM.read_bytes() and review.PATCH.is_file()
    return staged, draft, tests, indexed_artifacts


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', nargs='+', required=True)
    args = parser.parse_args()
    source = getsource(workflow.main)
    start = source.index('    base.replace_checked(DOC, f')
    end = source.index("'''.encode('utf-8'))", start) + len("'''.encode('utf-8'))")
    note = """    base.replace_checked(DOC, f'''# Town quest exchanges

The book sale, Kublai Khan prophecy, sextant request and handover were reviewed from the clean Japanese on all four routes. The book costs 8,500 gold, the seller keeps the Indian story’s celestial maiden and sage, and Ian's responses reflect each of the three choices. The royal prophecy now turns the page before the emperor's command to give up his sword. The sextant request preserves the elder's uncertainty about the instrument and withholds the reward until the trade. [Exact review ledger](../{REVIEW.as_posix()})

The registered batch has {prose} prose revisions, {len(changed)-prose} display-only corrections, 146 justified speech retentions and 12 menu retentions. All 55 changed native pages were visually reviewed. The changed text passed four native parser alignments, original control and allocation checks, complete glyph and bounds validation, and page counts. Villager, Alluring Woman and Mysterious Old Man retain their verified speaker labels. The book choices retain their command and text bytes. All three branch outcomes have earlier initialized clean-Japanese Lil gameplay evidence.

Initialized Maria replays observed 41 complete speech pages. These include the prophecy's new sword-instruction page, the full sextant request, and the book menu and delegated gift branch. The gift and Ian's Charm notices appeared before the return to the host scene. Other book outcomes and the sextant handover have offline checks on this candidate. Natural quest activation and hardware remain unvisited. [Book menu](../{(VERIFY / 'book_delegate_selected.png').as_posix()}) · [Prophecy page turn](../{(VERIFY / 'prophecy_live_2.png').as_posix()}) · [Sextant request](../{(VERIFY / 'sextant_live_1.png').as_posix()})

The [cumulative ROM and clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve the 114 accepted layers, the ASCII right bound, the Market and Sailor Info runtime repairs and all existing credits. Six startup frames, 24 protected name getters and {tests} targeted tests passed.
'''.encode('utf-8'))"""
    changes = {
        source[start:end]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 848 and len(manifest['checks']) == 183",
        '825 entries, 114 accepted layers and 160 passing checks': '849 entries, 114 accepted layers and 184 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160': 'registered_manifest_entries=849, passing_release_checks=184',
        "staged, draft, tests = verify(prior, profile['source25_multiarchive_guard'])":
            "staged, draft, tests, indexed = verify(prior, profile['source25_multiarchive_guard'], VIEWED)\n"
            "    changed = [r for r in draft['records'] if r['decision'] == 'revision']\n"
            "    prose = sum(r['english'].split('}', 1)[1] != r['previous_English'] for r in changed)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.town_quest_exchanges_v2.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.town_quest_exchanges_v2.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_town_quest_exchanges.json',
        'stage.digest(registry_before), ledger_before=stage.digest(ledger_before)':
            'native.digest(registry_before), ledger_before=native.digest(ledger_before)',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_town_trend_exchanges_predecessor=predecessor, town_quest_exchanges_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['town_quest_exchanges_pipeline']",
        "manifest['changed_records'][stage.ARM].extend(r['id'] for r in draft['records'] if r['decision'] == 'revision')":
            "for row in changed:\n"
            "        records = manifest['changed_records'][row['file_path']]\n"
            "        if row['id'] not in records:\n"
            "            records.append(row['id'])",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_story_blocks={f'/data/SC{i}.DK4': [b[i] for b in stage.BLOCKS.values()] for i in range(4)}",
        'changed_components=[stage.ARM], changed_internal_files=[]':
            "changed_components=[], changed_internal_files=sorted(staged['target_story_archive_sha256']),\n"
            "        **{f'target_SC{i}_sha256': staged['target_story_archive_sha256'][f'/data/SC{i}.DK4'] for i in range(4)}",
        "ARM9_sha256=release['target_ARM9_sha256'], registered_release_verification=str(RELEASE)":
            "ARM9_sha256=release['target_ARM9_sha256'], registered_release_verification=str(RELEASE),\n"
            "        **{f'SC{i}_sha256': release[f'target_SC{i}_sha256'] for i in range(4)}",
        'initialized_Rafael_dialogue=True': 'initialized_Maria_town_quests=True, natural_quest_activation=False',
        'new_contextual_records=0, prose_revisions=0,': 'new_contextual_records=0, prose_revisions=prose,',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=len(changed)-prose, justified_retentions=146, reviewed_UI_labels=0',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['town_quest_exchanges_20261115']",
        'name_label_revisions=2, justified_retentions=13':
            'prose_revisions=prose, wrap_or_glyph_revisions=len(changed)-prose, justified_retentions=146, retained_menu_labels=12, existing_credit=198',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'The book sale, Kublai Khan prophecy and sextant exchange have 52 revisions across all four routes.',
        '# Ritual Officiant Labels test candidate': '# Town Quest Exchanges test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            'revises the book sale, Kublai Khan prophecy and sextant exchange across all four routes',
        'Preserve verified ritual title candidate': 'Preserve verified town quest candidate',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.STORED, STARTUP, QA, *(Path(s['path']) for s in draft['native_sheets']))",
        '    base.save(REVIEW, draft)': (
            '    for path, name in indexed.items():\n'
            '        copyfile(path, VERIFY / name)\n'
            '        assert base.digest(path) == base.digest(VERIFY / name)\n'
            '    base.save(REVIEW, draft)'),
    }
    env = vars(workflow) | globals() | dict(VIEWED=tuple(args.viewed_sha))
    exec(compile(checked_text(source, changes), __file__ + '::register', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
