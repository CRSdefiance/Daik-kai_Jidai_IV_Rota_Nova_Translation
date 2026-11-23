"""Register the cross-route review of the figurehead and other town clues."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import replay_figurehead_and_ruins_20261118 as replay
from scripts import stage_figurehead_wraps_20261118 as stage
from scripts.reconcile_shared_speaker_labels_20261111 import current_getters
from scripts.source_locked_derivation_v5118 import checked_text

base, parent, native = stage.base, stage.parent, stage.native
PROFILE = 'all-routes-figurehead-and-ruins-v1-20261118'
ROOT = Path('out/figurehead_and_ruins_registered_20261118_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Figurehead_and_Ruins_20261118_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261118_figurehead_and_ruins_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_figurehead_and_ruins_20261118.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_figurehead_and_ruins_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_rebuilt.nds')


def menu_choices(images):
    inventory, _, _ = native.scoped_inventory()
    evidence = []
    for route, block in enumerate((254, 243, 242, 215)):
        path = f'/data/SC{route}.DK4'
        commands = {}
        for label, image in images.items():
            bank = native.IlnkContainer.parse(image.read_file(path))
            entries, _ = native.raw_speeches(image.read_file(native.ARM), bank.blocks[block], inventory)
            menu, = (row for row in entries if row['word'] == 0x2100)
            raw = bytes.fromhex(menu['whole_command_hex'])
            labels = [value.decode('cp932') for value in raw[6:].split(bytes(1)) if value]
            commands[label] = dict(offset=menu['offset'], hex=raw.hex(), labels=labels,
                                   block_sha256=native.digest(bank.blocks[block]))
        assert commands['clean']['labels'] == ['やってみよう', 'やめておこう']
        assert commands['current']['labels'] == (
            ["Let's try.", "Let's leave it."] if route == 0 else ['Try it', 'Leave it']
        )
        assert commands['current']['hex'] == commands['registered']['hex']
        assert commands['current']['offset'] == commands['registered']['offset']
        evidence.append(dict(file_path=path, block=block, references=commands, decision='retention',
            rationale='Each label names the actual action the player can choose. Keep the route wording and exact command.'))
    return evidence


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

    proof_sheets = list(staged['sheets'])
    assert sum(len(r['after_native']['pages']) for r in draft['records'] if r['decision'] == 'revision') == staged['preview_count']
    location = replay.SCOPE['folder'](replay.CASE) / 'verified.json'
    result = base.load(location)
    assert result['candidate_sha256'] == candidate
    assert result['initialized_emulator'] and not result['natural_activation'] and not result['hardware']
    expected = base.load(location.with_name('fixture.json'))['expected_pages']
    assert [(r['id'], r['page']) for r in result['complete_holds']] == [
        (row['id'], row['page']) for row in expected
    ]
    _, block, turns = replay.CASES[replay.CASE]
    assert [row['id'] for row in expected] == [f'DK4_MES_B{block}_R{n:04d}' for n in turns]
    assert len(expected) == 19
    assert all(base.digest(p) == sha for p, sha in result['evidence'].items())
    proof_sheets.extend(result['sheets'])
    indexed = {Path(r['path']): f'figurehead_{Path(r["path"]).name}' for r in result['sheets']}
    indexed[location] = 'figurehead_replay_receipt.json'
    gameplay = {replay.CASE: result}
    assert tuple(s['sha256'] for s in proof_sheets) == viewed
    assert all(base.digest(r['path']) == r['sha256'] for r in proof_sheets)

    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests == 32 and not any(int(suite.get(key, 0)) for key in ('failures', 'errors', 'skipped'))
    clean, old, final = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    before, after = map(native.files, (old, final))
    archives = staged['target_story_archive_sha256']
    assert set(archives) == {f'/data/SC{route}.DK4' for route in range(4)}
    assert before.keys() == after.keys()
    assert before[native.ARM] == after[native.ARM]
    assert native.digest(after[native.ARM]) == staged['target_ARM9_sha256']
    assert {p for p in before if before[p] != after[p]} == archives.keys()
    records = draft['records']
    edited = [r for r in records if r['decision'] == 'revision']
    assert len({(r['route'], r['block']) for r in records}) == 21
    assert len({(r['file_path'], r['id']) for r in records}) == len(records)
    assert len(records) == 210 and len(edited) == staged['preview_count'] == 78
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
    actors = {r['source_selector'] for r in records if r['source_selector'] != 254}
    speakers = {r['actor_ID']: r for r in current_getters(ctx)['rows']
                if r['actor_ID'] in actors and r['consumer'] == 'progressive-nameplate'}
    assert set(speakers) == actors == {0, 1, 2, 3, 6, 139, 188, 193, 195, 196}
    fresh_retention_notes = {
        (0, 254, 149): "The priest observes apparent acceptance after the difficult attempt. The current hedge leaves room for Rafael and Julio's explanation of luck.",
        (0, 258, 7): "The resident asks whether Rafael has visited the pyramid. The phrase already reads naturally and the next speech offers directions.",
        (2, 242, 140): "The priest describes the successful attempt as the statue's acceptance. Keep this wording distinct from the failure branch.",
    }
    for row in records:
        key = row['route'], row['block'], row['source_reference']['record_index']
        if row['decision'] == 'retention' and not row['earlier_review']['same_logical_English']:
            row['localization_note'] = fresh_retention_notes[key]
        # FE is a system presentation, not a character name.
        actual = 'System' if row['source_selector'] == 254 else speakers[row['source_selector']]['text']
        if row['speaker'] != actual:
            row['earlier_review']['speaker'] = row['speaker']
        row['speaker'] = actual
        row['registered_reference'] = row['staged_reference'] | dict(candidate_sha256=candidate)
        row['display_scope'] = 'fresh offline native rendering' if row['decision'] == 'revision' else 'byte-identical retention'
        if row['route'] == 3 and row['block'] == 215 and row['id'] in seen:
            row['display_scope'] += ' and initialized emulator'
    choices = menu_choices(dict(clean=clean, current=old, registered=base.NdsImage.open(stage.ROM)))
    captures = {r['frame']: r for r in base.load(result['report'])['frames_captured']}
    selections = ((9500, 'Try it'), (9650, 'Leave it'))
    choices[3]['visual_observations'] = []
    for frame, highlighted in selections:
        capture = captures[frame]
        path = Path(capture['path'])
        assert base.digest(path) == capture['PNG_sha256']
        indexed[path] = f'figurehead_menu_{frame}.png'
        choices[3]['visual_observations'].append(capture | dict(highlighted=highlighted))
    choices[3]['verified_decline_reply'] = next(row for row in result['complete_holds']
                                               if row['id'] == 'DK4_MES_B215_R0174')
    previous_staging = base.load(stage.prior.STORED)
    assert previous_staging['preview_count'] == 78 and len(stage.PAGE_EDITS) == 24
    indexed[stage.prior.STORED] = 'initial_native_staging.json'
    draft.update(registered=True, native_sheets=staged['sheets'], gameplay=gameplay,
                 checked_story_format_guard=guard_check, speaker_nameplates=list(speakers.values()),
                 figurehead_choice_retentions=choices,
                 verified_preview_reuse=dict(draft=str(stage.prior.STORED),
                     draft_sha256=base.digest(stage.prior.STORED), inherited_pages=54, fresh_pages=24,
                     unchanged=['ARM9', 'KANJI.FNT', 'original controls', 'stored revision bytes', 'automatic layouts']))
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
    note = """    base.replace_checked(DOC, f'''# Figurehead and ruins

Reviewed the church figurehead, New World gold-dust story, local ruin directions, pyramid visit and King Solomon's treasury rumor across all routes, plus Rafael's Lamenting Jar conversation. The {prose} prose revisions preserve the priest's account of the figurehead, Julio's reluctance to help, and the separate outcomes. The gold stays a sailor's report. The treasury and jar stay rumors. Four route-specific menu commands retain their wording and behavior. The ledger records {len(changed)-prose} wrap-only revisions and {retained} retentions. [Exact review ledger](../{REVIEW.as_posix()})

All {staged['preview_count']} revised pages passed native checks and visual review. An initialized DeSmuME run displayed the original figurehead conversation and Maria's original Leave it choice and outcome, with the King Figurehead card on screen. The attempt branches and other exchanges were checked offline. Natural activation and hardware remain unverified for this batch. [Emulator playback](../{(VERIFY / 'figurehead_live_1.png').as_posix()})

The patch reconstructs the candidate byte for byte from clean input. All 114 accepted layers and the ASCII right-bound correction carry forward. Startup, 24 protected name getters and {tests} targeted tests passed. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)

The next 244 progressive and system records cover the compassionate statue, the floating-ice puzzle and three local ruin replies in each route. Start at SC0 B260–264, SC1 B251–255, SC2 B250–254 and SC3 B220–224. Preserve the exact puzzle directions and test the outcome transitions separately. The inscriptions use an FE consumer with prior riddle-specific display evidence. Verify that evidence against the current input before proposing new wraps for it. [Clean and current comparison](../work/ruin_statue_and_ice_source_20261118/) [Earlier native riddle check](../scripts/retain_lil269_readable_riddle_v1.py)
'''.encode('utf-8'))"""
    changes = {
        source[start:end]: note,
        'Current editorial checkpoint - 2026-11-15': 'Current editorial checkpoint - 2026-11-18',
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 855 and len(manifest['checks']) == 190",
        '825 entries, 114 accepted layers and 160 passing checks': '856 entries, 114 accepted layers and 191 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160': 'registered_manifest_entries=856, passing_release_checks=191',
        "staged, draft, tests = verify(prior, profile['source25_multiarchive_guard'])":
            "staged, draft, tests, indexed = verify(prior, profile['source25_multiarchive_guard'], VIEWED)\n"
            "    changed = [r for r in draft['records'] if r['decision'] == 'revision']\n"
            "    prose = sum(native_english(r['english']) != r['previous_English'] for r in changed)\n"
            "    retained = len(draft['records']) - len(changed)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.figurehead_and_ruins.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.figurehead_and_ruins.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_figurehead_and_ruins.json',
        'stage.digest(registry_before), ledger_before=stage.digest(ledger_before)':
            'native.digest(registry_before), ledger_before=native.digest(ledger_before)',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_janus_and_frozen_rose_predecessor=predecessor, figurehead_and_ruins_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['figurehead_and_ruins_pipeline']",
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
        'initialized_Rafael_dialogue=True': 'initialized_Maria_figurehead_decline=True, natural_activation=False',
        'new_contextual_records=0, prose_revisions=0,': 'new_contextual_records=0, prose_revisions=prose,',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=len(changed)-prose, justified_retentions=retained, reviewed_UI_labels=0',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['figurehead_and_ruins_20261118']",
        'name_label_revisions=2, justified_retentions=13':
            'prose_revisions=prose, wrap_only_revisions=len(changed)-prose, justified_retentions=retained, existing_credit=len(draft["records"])',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'The figurehead discovery and ruin clues are reviewed across all routes.',
        '# Ritual Officiant Labels test candidate': '# Figurehead and Ruins test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            "revises the figurehead discovery and ruin clues across all routes",
        'Preserve verified ritual title candidate': 'Preserve figurehead and ruins candidate and checked draft',
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
