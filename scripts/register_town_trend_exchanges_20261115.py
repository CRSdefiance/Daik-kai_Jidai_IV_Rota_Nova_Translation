"""Register the four-route town trend review on its exact cumulative parent."""

from argparse import ArgumentParser
from inspect import getsource
from json import dumps
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import replay_town_trend_exchanges_20261115 as replay
from scripts import stage_town_trend_exchanges_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, parent = stage.base, stage.parent
PROFILE = 'all-routes-town-trend-exchanges-v1-20261115'
ROOT = Path('out/town_trend_exchanges_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Town_Trend_Exchanges_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_town_trend_exchanges_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_town_trend_exchanges_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_town_trend_exchanges_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_rebuilt.nds')


def verify(prior, guard, viewed, notice_frames):
    staged, draft, boot = map(base.load, (stage.STORED, stage.MANUSCRIPT, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == staged['candidate_sha256'] == draft['candidate_sha256'] == boot['candidate_sha256']
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert base.digest(stage.MANUSCRIPT) == staged['manuscript_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert all(base.digest(path) == sha for path, sha in boot['evidence'].items())

    native = staged['sheets']
    assert len(native) == 7 and staged['preview_count'] == 55
    assert all(base.digest(row['path']) == row['sha256'] for row in native)
    assert viewed[:len(native)] == tuple(row['sha256'] for row in native)
    gameplay, indexed_artifacts = {}, {}
    for block, expected_notice, view in zip(replay.GUESTS, notice_frames, viewed[len(native):], strict=True):
        folder, setup, _ = replay.paths(block)
        receipt_path = folder / 'initialized_exchange.json'
        result = base.load(receipt_path)
        assert result['candidate_sha256'] == candidate and result['original_scene_execution_after_initialized_Maria_entry']
        assert len(result['progressive_holds']) == replay.GUESTS[block][1] - 1
        assert not result['natural_random_activation'] and not result['hardware']
        assert all(base.digest(path) == sha for path, sha in result['evidence'].items())
        assert base.load(setup)['whole_checked_ROM_inverse_exact']
        assert view == result['sheet_sha256'] == base.digest(result['sheet'])
        notice = next(row for row in result['captures'] if row['frame'] == expected_notice)
        assert expected_notice > result['progressive_holds'][-1]['frame']
        assert all(hold['frame'] in {r['frame'] for r in result['captures']} for hold in result['progressive_holds'])
        assert all(frame in {r['frame'] for r in result['captures']} for frame in (9250, 10250))
        town = replay.GUESTS[block][0].lower()
        gameplay[town] = result | dict(directly_viewed_notice=notice, directly_viewed_followup_frames=[9250, 10250])
        indexed_artifacts[receipt_path] = f'{town}_initialized_exchange.json'
        indexed_artifacts[Path(result['sheet'])] = f'{town}_complete_exchange.png'

    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests == 32 and not any(int(suite.get(key, 0)) for key in ('failures', 'errors', 'skipped'))
    clean, old, final = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(stage.files, (old, final))
    story_hashes = staged['target_story_archive_sha256']
    assert len(story_hashes) == 4 and before.keys() == after.keys()
    assert after[stage.ARM] == before[stage.ARM] and stage.digest(after[stage.ARM]) == staged['target_ARM9_sha256']
    assert {p for p in before if before[p] != after[p]} == story_hashes.keys()
    records = draft['records']
    changed = [r for r in records if r['decision'] == 'revision']
    assert len(records) == 276 and len(changed) == 55
    assert len({(r['file_path'], r['id']) for r in records}) == 276
    assert len({(r['file_path'], r['block']) for r in records}) == 24
    assert all(r['review'] == dict.fromkeys(stage.GATES, True) for r in records)
    targets = dict(stage.transform(old, records))
    for path, expected in story_hashes.items():
        assert targets[path] == after[path] and stage.digest(after[path]) == expected
        final.replace_file(path, before[path])
    assert bytes(final.rom.save()) == parent.ROM.read_bytes()
    guard_check = bind_registered_story_percent_guard(guard)(stage.files(clean), after)
    assert guard_check['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(guard_check['source_bound_new_command_counts'].values())
    for row in records:
        row['registered_reference'] = row['staged_reference'] | {'candidate_sha256': candidate}
        row['display_scope'] = ('offline native rendering' if row['decision'] == 'revision' else 'byte-identical retention')
        if row['route'] == 3 and row['block'] in replay.GUESTS:
            row['display_scope'] += ' and initialized original scene replay'
    draft.update(registered=True, zero_new_credit=True, native_sheets=native,
                 gameplay=gameplay, checked_story_format_guard=guard_check)
    validate_natural_dialogue_batch(draft)
    assert review.REBUILT.read_bytes() == stage.ROM.read_bytes() and review.PATCH.is_file()
    return staged, draft, tests, indexed_artifacts


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', nargs=9, required=True)
    parser.add_argument('--notice-frames', type=int, nargs=2, required=True)
    args = parser.parse_args()
    source = getsource(workflow.main)
    start = source.index('    base.replace_checked(DOC, f')
    end = source.index("'''.encode('utf-8'))", start) + len("'''.encode('utf-8'))")
    note = """    base.replace_checked(DOC, f'''# Town trend exchanges

The six complete exchanges cover homemade bread in Amsterdam, fragrance in Lisbon, a ruby necklace in Athens, a royal engagement in London, the owner's sweets forecast in Alexandria and chili peppers in Seoul. The four route copies of each were checked against the clean Japanese. The ledger has 55 changed records and 221 individual retentions, including all 24 forecast notices. Alexandria keeps the cook's dry responses and the owner's previous punch line, “Of course! I said so, didn't I?” [Exact review ledger](../{REVIEW.as_posix()})

All 55 changed pages passed the original parser at four input alignments and the one-page native renderer. The review checked complete glyphs, wrap boundaries, byte allocation, retained speaker preambles and original scene commands. Every final preview page was visually reviewed. The four story archives invert to the exact predecessor. ARM9, COMMON, font and graphics stay byte-identical.

Two initialized Maria emulator replays ran the complete London and Alexandria scenes, including 18 complete speech holds, the two original forecast notices and dismissal. The other copies were checked offline. Natural random activation and hardware are unvisited. [London replay](../{(VERIFY / 'london_complete_exchange.png').as_posix()}) · [Alexandria replay](../{(VERIFY / 'alexandria_complete_exchange.png').as_posix()})

The [cumulative ROM and clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers, the ASCII right-bound correction and the Sailor Info fix. Six fresh startup frames, 24 protected name getters and {tests} targeted tests passed. Existing editorial credit remains 27,700, with 276 stored shared keys still awaiting display ownership.
'''.encode('utf-8'))"""
    replacements = {
        source[start:end]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 847 and len(manifest['checks']) == 182",
        '825 entries, 114 accepted layers and 160 passing checks': '848 entries, 114 accepted layers and 183 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160': 'registered_manifest_entries=848, passing_release_checks=183',
        "staged, draft, tests = verify(prior, profile['source25_multiarchive_guard'])":
            "staged, draft, tests, indexed = verify(prior, profile['source25_multiarchive_guard'], VIEWED, NOTICE_FRAMES)\n"
            "    changed = [r for r in draft['records'] if r['decision'] == 'revision']\n"
            "    prose = sum(r['english'].split('}', 1)[1] != r['previous_English'] for r in changed)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.town_trend_exchanges.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.town_trend_exchanges.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_town_trend_exchanges.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_trade_armed_designs_predecessor=predecessor, town_trend_exchanges_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['town_trend_exchanges_pipeline']",
        "manifest['changed_records'][stage.ARM].extend(r['id'] for r in draft['records'] if r['decision'] == 'revision')":
            "for row in changed:\n"
            "        records = manifest['changed_records'][row['file_path']]\n"
            "        if row['id'] not in records:\n"
            "            records.append(row['id'])",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_story_blocks={f'/data/SC{i}.DK4': [b[i] for b in stage.BLOCK_MAP.values()] for i in range(4)}",
        'changed_components=[stage.ARM], changed_internal_files=[]':
            "changed_components=[], changed_internal_files=sorted(staged['target_story_archive_sha256']),\n"
            "        **{f'target_SC{i}_sha256': staged['target_story_archive_sha256'][f'/data/SC{i}.DK4'] for i in range(4)}",
        "ARM9_sha256=release['target_ARM9_sha256'], registered_release_verification=str(RELEASE)":
            "ARM9_sha256=release['target_ARM9_sha256'], registered_release_verification=str(RELEASE),\n"
            "        **{f'SC{i}_sha256': release[f'target_SC{i}_sha256'] for i in range(4)}",
        'initialized_Rafael_dialogue=True': 'initialized_Maria_town_exchanges=True, natural_random_activation=False',
        'new_contextual_records=0, prose_revisions=0,': 'new_contextual_records=0, prose_revisions=prose,',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=len(changed)-prose, justified_retentions=221, reviewed_UI_labels=0',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['town_trend_exchanges_20261115']",
        'name_label_revisions=2, justified_retentions=13':
            'prose_revisions=prose, wrap_only_revisions=len(changed)-prose, justified_retentions=221, existing_credit=276',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'Six town trend exchanges have 55 revisions across all four routes, with 221 justified retentions.',
        '# Ritual Officiant Labels test candidate': '# Town Trend Exchanges test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            'revises six town trend exchanges across all four routes',
        'Preserve verified ritual title candidate': 'Preserve verified town trend candidate',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.STORED, STARTUP, QA, *(Path(s['path']) for s in draft['native_sheets']))",
        '    base.save(REVIEW, draft)': (
            '    for path, name in indexed.items():\n'
            '        copyfile(path, VERIFY / name)\n'
            '        assert base.digest(path) == base.digest(VERIFY / name)\n'
            '    base.save(REVIEW, draft)'),
    }
    env = vars(workflow) | globals() | dict(VIEWED=tuple(args.viewed_sha), NOTICE_FRAMES=args.notice_frames)
    exec(compile(checked_text(source, replacements), __file__ + '::register', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
