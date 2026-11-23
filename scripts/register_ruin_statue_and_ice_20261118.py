"""Register the cross-route review of the compassionate statue and ice puzzle."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import replay_ruin_statue_and_ice_20261118 as replay
from scripts import stage_ruin_statue_wraps_20261118 as stage
from scripts.reconcile_shared_speaker_labels_20261111 import current_getters
from scripts.source_locked_derivation_v5118 import checked_text

base, parent, native = stage.base, stage.parent, stage.native
PROFILE = 'all-routes-ruin-statue-and-ice-v1-20261118'
ROOT = Path('out/ruin_statue_and_ice_registered_20261118_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Ruin_Statue_and_Ice_20261118_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261118_ruin_statue_and_ice_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_ruin_statue_and_ice_20261118.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_ruin_statue_and_ice_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_rebuilt.nds')


def menu_choices(images):
    inventory, _, _ = native.scoped_inventory()
    evidence = []
    for route, start in enumerate(stage.prior.FIRST_BLOCK):
        path = f'/data/SC{route}.DK4'
        commands = {}
        for label, image in images.items():
            bank = native.IlnkContainer.parse(image.read_file(path))
            block = bank.blocks[start + 1]
            entries, _ = native.raw_speeches(image.read_file(native.ARM), block, inventory)
            menus = [row for row in entries if row['word'] in (0x2200, 0x2100)]
            assert [menu['word'] for menu in menus] == [0x2200, 0x2100]
            commands[label] = []
            for menu in menus:
                raw = bytes.fromhex(menu['whole_command_hex'])
                table_end = 8 if menu['word'] == 0x2200 else 6
                labels = [value.decode('cp932') for value in raw[table_end:].split(bytes(1)) if value]
                commands[label].append(dict(offset=menu['offset'], hex=raw.hex(), labels=labels,
                                            block_sha256=native.digest(block)))
        assert all(term in label for term, label in zip(('正面', '左', '右'),
                   commands['clean'][0]['labels'], strict=True))
        assert commands['current'][0]['labels'] in (
            ['Stone ahead', 'Left stone', 'Right stone'],
            ['Front stone', 'Left stone', 'Right stone'],
            ['Ahead', 'Left', 'Right'],
        )
        assert commands['clean'][1]['labels'] == ['そうだ', '違う']
        assert commands['current'][1]['labels'] in (["I did.", "I didn't."], ['Yes', 'No'])
        for before, after in zip(commands['current'], commands['registered'], strict=True):
            assert before['hex'] == after['hex'] and before['offset'] == after['offset']
        evidence.append(dict(file_path=path, block=start + 1, references=commands, decision='retention',
            rationale='The positional labels and the reply to the voice match the original options and byte layout.'))
    return evidence


def verify_replay_dependencies(final):
    report = base.load(stage.prior.STORED)
    replay_sha = base.digest(stage.prior.ROM)
    assert replay_sha == report['candidate_sha256']
    assert base.digest(stage.prior.MANUSCRIPT) == report['manuscript_sha256']
    earlier = base.NdsImage.open(stage.prior.ROM)
    before, after = map(native.files, (earlier, final))
    assert before.keys() == after.keys()
    allowed = {f'/data/SC{route}.DK4': block for route, block in enumerate(stage.prior.FIRST_BLOCK)}
    assert {p for p in before if before[p] != after[p]} == allowed.keys()
    preserved = {path: native.digest(after[path]) for path in (native.ARM, '/GRP/KANJI.FNT')}
    for path, block in allowed.items():
        old_bank, new_bank = [native.IlnkContainer.parse(data[path]) for data in (before, after)]
        differences = [i for i, (a, b) in enumerate(zip(old_bank.blocks, new_bank.blocks, strict=True)) if a != b]
        assert differences == [block]
        for i in ((33, block + 1) if path == '/data/SC3.DK4' else (block + 1,)):
            assert old_bank.blocks[i] == new_bank.blocks[i]
            preserved[f'{path}:B{i}'] = native.digest(new_bank.blocks[i])
    return dict(replay_candidate_sha256=replay_sha, final_candidate_sha256=base.digest(stage.ROM),
                byte_identical_dependencies=preserved, changed_statue_blocks=allowed,
                fresh_native_pages=len(stage.WRAP_REVISIONS),
                reused_native_pages=report['preview_count'] - len(stage.WRAP_REVISIONS))


def verify(prior, guard, viewed):
    staged, draft, boot = map(base.load, (stage.STORED, stage.MANUSCRIPT, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == staged['candidate_sha256'] == draft['candidate_sha256'] == boot['candidate_sha256']
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(native.CLEAN) == prior['clean_input_sha256']
    assert staged['manuscript_sha256'] == base.digest(stage.MANUSCRIPT)
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert all(base.digest(p) == sha for p, sha in boot['evidence'].items())

    final_image = base.NdsImage.open(stage.ROM)
    reuse = verify_replay_dependencies(final_image)
    proof_sheets = list(staged['sheets'])
    assert sum(len(r['after_native']['pages']) for r in draft['records'] if r['decision'] == 'revision') == staged['preview_count']
    gameplay, indexed = {}, {}
    for case, (_, block, turns) in replay.CASES.items():
        location = replay.SCOPE['folder'](case) / 'verified.json'
        result = base.load(location)
        assert result['candidate_sha256'] == reuse['replay_candidate_sha256']
        assert result['initialized_emulator'] and not result['natural_activation'] and not result['hardware']
        expected = base.load(location.with_name('fixture.json'))['expected_pages']
        assert [(r['id'], r['page']) for r in result['complete_holds']] == [
            (row['id'], row['page']) for row in expected
        ]
        assert {row['id'] for row in expected} == {f'DK4_MES_B{block}_R{n:04d}' for n in turns}
        assert all(base.digest(p) == sha for p, sha in result['evidence'].items())
        proof_sheets.extend(result['sheets'])
        indexed.update({Path(r['path']): f'ice_{case}_{Path(r["path"]).name}' for r in result['sheets']})
        indexed[location] = f'ice_{case}_receipt.json'
        gameplay[case] = result
    assert tuple(s['sha256'] for s in proof_sheets) == viewed
    assert all(base.digest(r['path']) == r['sha256'] for r in proof_sheets)

    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests == 32 and not any(int(suite.get(key, 0)) for key in ('failures', 'errors', 'skipped'))
    clean, old = map(base.NdsImage.open, (native.CLEAN, parent.ROM))
    final = final_image
    before, after = map(native.files, (old, final))
    archives = staged['target_story_archive_sha256']
    assert set(archives) == {f'/data/SC{route}.DK4' for route in range(4)}
    assert before.keys() == after.keys()
    assert before[native.ARM] == after[native.ARM]
    assert native.digest(after[native.ARM]) == staged['target_ARM9_sha256']
    assert {p for p in before if before[p] != after[p]} == archives.keys()
    records = draft['records']
    edited = [r for r in records if r['decision'] == 'revision']
    assert len({(r['route'], r['block']) for r in records}) == 20
    assert len({(r['file_path'], r['id']) for r in records}) == len(records)
    assert len(records) == 244 and len(edited) == staged['preview_count'] == 73
    credited = {(r['file_path'], r['id']) for r in base.load(base.LEDGER)[base.CONTEXT]['integrated_record_keys']}
    assert all((r['file_path'], r['id']) in credited for r in records)
    rebuilt = dict(native.transform(old, edited))
    for path, expected in archives.items():
        assert rebuilt[path] == after[path] and native.digest(after[path]) == expected
        final.replace_file(path, before[path])
    assert bytes(final.rom.save()) == parent.ROM.read_bytes()
    guard_check = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert guard_check['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(guard_check['source_bound_new_command_counts'].values())
    seen = {hold['id'] for result in gameplay.values() for hold in result['complete_holds']}
    ctx = native.RegisteredRuntime(parent.RELEASE, prior['own_registered_startup'], captain=3)
    actors = {r['source_selector'] for r in records if r['source_selector'] < 207}
    speakers = {r['actor_ID']: r for r in current_getters(ctx)['rows']
                if r['actor_ID'] in actors and r['consumer'] == 'progressive-nameplate'}
    assert set(speakers) == actors == {0, 1, 2, 3, 13, 20, 189, 190, 200}
    for row in records:
        key = row['route'], row['block'], row['source_reference']['record_index']
        if row['decision'] == 'retention' and not row['earlier_review']['same_logical_English']:
            if key == (2, 250, 98):
                row['localization_note'] = "Cesare agrees aloud while privately regretting the decision. Keep the parenthetical contrast."
            else:
                assert key in {(0, 261, 6), (1, 252, 6), (2, 251, 6), (3, 221, 5)}
                row['localization_note'] = "Fernando calls the captain over to show the writing. The natural opening supplies the object of the next two panels."
        if row['source_selector'] in speakers:
            actual = speakers[row['source_selector']]['text']
            if row['speaker'] != actual:
                row['earlier_review']['speaker'] = row['speaker']
            row['speaker'] = actual
        if row['source_selector'] == 254 and row['decision'] == 'revision':
            row['speaker'] = 'Inscription'
        row['registered_reference'] = row['staged_reference'] | dict(candidate_sha256=candidate)
        if row['decision'] == 'revision':
            row['display_scope'] = ('fresh offline native rendering' if key in stage.WRAP_REVISIONS
                                    else 'native rendering verified against byte-identical inputs')
        else:
            row['display_scope'] = 'byte-identical retention'
        if row['route'] == 3 and row['block'] == 221 and row['id'] in seen:
            row['display_scope'] += ' and initialized emulator on byte-identical scene'
    choices = menu_choices(dict(clean=clean, current=old, registered=base.NdsImage.open(stage.ROM)))
    changed_fe = [row for row in edited if row['source_selector'] == 254]
    assert len(changed_fe) == 8 and all(len(row['after_native']['processor']['cases']) == 4 for row in changed_fe)
    draft.update(registered=True, native_sheets=staged['sheets'], gameplay=gameplay,
                 checked_story_format_guard=guard_check, speaker_nameplates=list(speakers.values()),
                 stone_choice_retentions=choices, checked_FE_inscriptions=len(changed_fe),
                 verification_reuse=reuse)
    validate_natural_dialogue_batch(draft)
    assert review.REBUILT.read_bytes() == stage.ROM.read_bytes() and review.PATCH.is_file()
    return staged, draft, tests, indexed


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', nargs='+', required=True)
    args = parser.parse_args()
    source = getsource(workflow.main)
    start = source.index('    base.replace_checked(DOC, f')
    end = source.index("'''.encode('utf-8'))", start) + len("'''.encode('utf-8'))")
    note = """    base.replace_checked(DOC, f'''# Ruin statue and floating-ice puzzle

Reviewed the compassionate statue, the floating-ice riddle and the nearby ruin replies across the four routes. The {prose} prose revisions keep the protective voice unidentified, Fernando's fear of a curse tentative, and each captain's distinct reactions. The new inscriptions restore the brim-full vessel consistently and associate the front stone with a rise, left with a fall, and right with no change. The ledger records {len(changed)-prose} wrap-only revisions and {retained} retentions. [Exact review ledger](../{REVIEW.as_posix()})

All {staged['preview_count']} revised pages passed native checks and visual review. The final statue reflow received 16 fresh page checks. The remaining 57 page checks carry forward with identical render inputs. The eight inscriptions also passed the original FE painter and null-actor input checks. Three initialized DeSmuME tests on Maria's puzzle verified the original stone selections and their replies. The final candidate retains the exact puzzle block, replay host and renderer from those runs. The other routes and the remaining voice branch were checked offline. Natural activation and hardware are unverified. [Right-stone replay](../{(VERIFY / 'ice_right_live_1.png').as_posix()})

The patch reconstructs the candidate byte for byte from clean input. All 114 accepted layers and the ASCII right-bound correction carry forward. Startup, 24 protected name getters and {tests} targeted tests passed. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)

Next editorial batch covers the survey, guild leads and crew exchanges in SC0 B265–272, SC1 B248–250 and B256–260, SC2 B247–249 and B255–258, and SC3 B225–232. The 206 clean-Japanese and current-English turns are staged for contextual review under work/guild_search_and_survey_source_20261118. Confirm the survey results, crew names, quest rewards and locations across each exchange. The 27,700 credited records and 276 pending shared keys are carried forward.
'''.encode('utf-8'))"""
    changes = {
        source[start:end]: note,
        'Current editorial checkpoint - 2026-11-15': 'Current editorial checkpoint - 2026-11-18',
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 856 and len(manifest['checks']) == 191",
        '825 entries, 114 accepted layers and 160 passing checks': '857 entries, 114 accepted layers and 192 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160': 'registered_manifest_entries=857, passing_release_checks=192',
        "staged, draft, tests = verify(prior, profile['source25_multiarchive_guard'])":
            "staged, draft, tests, indexed = verify(prior, profile['source25_multiarchive_guard'], VIEWED)\n"
            "    changed = [r for r in draft['records'] if r['decision'] == 'revision']\n"
            "    prose = sum(native_english(r['english']) != r['previous_English'] for r in changed)\n"
            "    retained = len(draft['records']) - len(changed)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.ruin_statue_and_ice.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.ruin_statue_and_ice.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_ruin_statue_and_ice.json',
        'stage.digest(registry_before), ledger_before=stage.digest(ledger_before)':
            'native.digest(registry_before), ledger_before=native.digest(ledger_before)',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_figurehead_and_ruins_predecessor=predecessor, ruin_statue_and_ice_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['ruin_statue_and_ice_pipeline']",
        "manifest['changed_records'][stage.ARM].extend(r['id'] for r in draft['records'] if r['decision'] == 'revision')":
            "for row in changed:\n"
            "        records = manifest['changed_records'][row['file_path']]\n"
            "        if row['id'] not in records:\n"
            "            records.append(row['id'])",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_story_blocks={p: sorted({r['block'] for r in changed if r['file_path']==p}) for p in staged['target_story_archive_sha256']}",
        'changed_components=[stage.ARM], changed_internal_files=[]':
            "changed_components=[], changed_internal_files=sorted(staged['target_story_archive_sha256']),\n"
            "        **{f'target_SC{i}_sha256': staged['target_story_archive_sha256'][f'/data/SC{i}.DK4'] for i in range(4)}",
        "ARM9_sha256=release['target_ARM9_sha256'], registered_release_verification=str(RELEASE)":
            "ARM9_sha256=release['target_ARM9_sha256'], registered_release_verification=str(RELEASE),\n"
            "        **{f'SC{i}_sha256': release[f'target_SC{i}_sha256'] for i in range(4)}",
        'initialized_Rafael_dialogue=True': 'initialized_Maria_all_three_stones=True, natural_activation=False',
        'new_contextual_records=0, prose_revisions=0,': 'new_contextual_records=0, prose_revisions=prose,',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=len(changed)-prose, justified_retentions=retained, reviewed_UI_labels=0',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['ruin_statue_and_ice_20261118']",
        'name_label_revisions=2, justified_retentions=13':
            'prose_revisions=prose, wrap_only_revisions=len(changed)-prose, justified_retentions=retained, existing_credit=len(draft["records"])',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'The ruin statue, floating-ice puzzle and nearby ruin replies are reviewed across all routes.',
        '# Ritual Officiant Labels test candidate': '# Ruin Statue and Ice test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            "revises the ruin statue and floating-ice puzzle across all routes",
        'Preserve verified ritual title candidate': 'Preserve verified ruin statue and ice candidate',
        'for path in (ROM, stage.ROM):': 'for path in (ROM, stage.ROM, stage.prior.ROM):',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.STORED, STARTUP, QA, *(Path(s['path']) for s in draft['native_sheets']))",
        '    base.save(REVIEW, draft)': (
            '    for path, name in indexed.items():\n'
            '        copyfile(path, VERIFY / name)\n'
            '        assert base.digest(path) == base.digest(VERIFY / name)\n'
            '    base.save(REVIEW, draft)'),
    }
    env = vars(workflow) | globals() | dict(VIEWED=tuple(args.viewed_sha),
                                           native_english=stage.precedent.normalize)
    exec(compile(checked_text(source, changes), __file__ + '::register', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
