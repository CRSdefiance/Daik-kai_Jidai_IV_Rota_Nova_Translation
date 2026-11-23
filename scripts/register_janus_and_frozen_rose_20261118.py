"""Register the cross-route review of Janus's glove rumor and the Frozen Rose quest."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import replay_janus_and_frozen_rose_20261118 as replay
from scripts import stage_frozen_rose_pagination_20261118 as stage
from scripts.reconcile_shared_speaker_labels_20261111 import current_getters
from scripts.source_locked_derivation_v5118 import checked_text

base, parent, native = stage.base, stage.parent, stage.native
PROFILE = 'all-routes-janus-and-frozen-rose-v1-20261118'
ROOT = Path('out/janus_and_frozen_rose_registered_20261118_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Janus_and_Frozen_Rose_20261118_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261118_janus_and_frozen_rose_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_janus_and_frozen_rose_20261118.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_janus_and_frozen_rose_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_rebuilt.nds')


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
    assert {row['id'] for row in expected} == {f'DK4_MES_B{block}_R{n:04d}' for n in turns} | {'DK4_MES_B212_R0109'}
    assert len(expected) == 12 and [r['id'] for r in expected if r['page'] == 2] == ['DK4_MES_B212_R0109']
    assert all(base.digest(p) == sha for p, sha in result['evidence'].items())
    proof_sheets.extend(result['sheets'])
    indexed = {Path(r['path']): f'frozen_rose_{Path(r["path"]).name}' for r in result['sheets']}
    indexed[location] = 'frozen_rose_replay_receipt.json'
    capture = base.load(result['report'])
    assert capture['cold_boot'] and not capture['savestate_loaded']
    handoff, = (r for r in capture['frames_captured'] if r['frame'] == 5900)
    handoff_path = Path(handoff['path'])
    assert base.digest(handoff_path) == handoff['PNG_sha256'] == (
        '323083c8e523fe826b884dccff320a309b4e6e7077d8557a80725455d9dca9ed'
    )
    indexed[handoff_path] = 'frozen_rose_handoff.png'
    result['visual_system_hold'] = handoff | dict(id='DK4_MES_B214_R0016',
        text='Handed over the Frozen Rose.', item_card='Frozen Rose', verification='visual inspection')
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
    assert len({(r['route'], r['block']) for r in records}) == 14
    assert len({(r['file_path'], r['id']) for r in records}) == len(records)
    assert len(records) == 313 and len(edited) == 106 and staged['preview_count'] == 110
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
    assert set(speakers) == actors == {0, 1, 2, 3, 4, 5, 9, 10, 67, 92, 113, 186}
    fresh_retention_notes = {
        (1, 242, 10): "Francisca recognizes an object she has a personal reason to see. The existing question carries her surprise and asks permission.",
        (2, 239, 117): "Camille asks Lil to try Havana for Francisca's sake while acknowledging the man may have nothing to do with the theft.",
        (2, 240, 17): "The debtor gives in and offers the object for his drink bill before naming the alleged material.",
        (2, 240, 62): "Lil explains that the owner asked her to find the ornament and refuses to accept the man's denial. Her forceful reply fits the confrontation.",
        (3, 214, 9): "Maria presents the recovered object so Francisca can identify it. The short existing question fits the handoff."
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
        if row['route'] == 3 and row['block'] in (212, 214):
            if row['id'] in seen:
                row['display_scope'] += ' and initialized emulator'
            elif row['id'] == result['visual_system_hold']['id']:
                assert row['decision'] == 'retention' and row['source_selector'] == 254
                row['display_scope'] += ' and initialized emulator visual system hold'
    previous_stage = base.load(stage.prior.STORED)
    assert previous_stage['preview_count'] == 110 and len(stage.PAGE_EDITS) == 4
    indexed[stage.prior.STORED] = 'initial_native_staging.json'
    draft.update(registered=True, native_sheets=staged['sheets'], gameplay=gameplay,
                 checked_story_format_guard=guard_check, speaker_nameplates=list(speakers.values()),
                 verified_preview_reuse=dict(draft=str(stage.prior.STORED),
                     draft_sha256=base.digest(stage.prior.STORED), inherited_pages=102, fresh_pages=8,
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
    note = """    base.replace_checked(DOC, f'''# Janus and the Frozen Rose

Reviewed Janus's glove rumor and the Frozen Rose quest in every route. The {prose} prose revisions keep the Jutland Peninsula clue intact, preserve the secondhand nature of Francisca's Havana lead, and restore the cadence of the tavern keeper's unpaid-tab joke. Hodram's guild reward, Rafael's initiative, Camille's argument for helping, and Xien's inspection remain tied to their own routes. The ledger records {len(changed)-prose} wrap-only revisions and {retained} justified retentions. [Exact review ledger](../{REVIEW.as_posix()})

All {staged['preview_count']} revised pages passed native checks and visual review. An initialized DeSmuME run checked Maria's Frozen Rose return, the unchanged item card and handoff panel, the church lead, and both pages of the Havana rumor excerpt. The other exchanges were checked offline. Natural activation and hardware remain unverified for this batch. [Emulator playback](../{(VERIFY / 'frozen_rose_live_1.png').as_posix()})

The clean-input patch reconstructs the candidate byte for byte. All 114 accepted layers and the ASCII right-bound correction carry forward. The startup comparison, 24 protected name getters and {tests} targeted tests passed. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)

The next 210 progressive and system records cover the figurehead discovery, the gold-dust lead and the local ruins. Rafael's Lamenting Jar exchange is included. Start at SC0 B254–259, SC1 B243–247, SC2 B242–246 and SC3 B215–219. [Clean and current comparison](../work/figurehead_and_ruins_source_20261118/)
'''.encode('utf-8'))"""
    changes = {
        source[start:end]: note,
        'Current editorial checkpoint - 2026-11-15': 'Current editorial checkpoint - 2026-11-18',
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 854 and len(manifest['checks']) == 189",
        '825 entries, 114 accepted layers and 160 passing checks': '855 entries, 114 accepted layers and 190 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160': 'registered_manifest_entries=855, passing_release_checks=190',
        "staged, draft, tests = verify(prior, profile['source25_multiarchive_guard'])":
            "staged, draft, tests, indexed = verify(prior, profile['source25_multiarchive_guard'], VIEWED)\n"
            "    changed = [r for r in draft['records'] if r['decision'] == 'revision']\n"
            "    prose = sum(native_english(r['english']) != r['previous_English'] for r in changed)\n"
            "    retained = len(draft['records']) - len(changed)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.janus_and_frozen_rose.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.janus_and_frozen_rose.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_janus_and_frozen_rose.json',
        'stage.digest(registry_before), ledger_before=stage.digest(ledger_before)':
            'native.digest(registry_before), ledger_before=native.digest(ledger_before)',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_crew_accounts_predecessor=predecessor, janus_and_frozen_rose_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['janus_and_frozen_rose_pipeline']",
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
        'initialized_Rafael_dialogue=True': 'initialized_Maria_frozen_rose=True, natural_activation=False',
        'new_contextual_records=0, prose_revisions=0,': 'new_contextual_records=0, prose_revisions=prose,',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=len(changed)-prose, justified_retentions=retained, reviewed_UI_labels=0',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['janus_and_frozen_rose_20261118']",
        'name_label_revisions=2, justified_retentions=13':
            'prose_revisions=prose, wrap_only_revisions=len(changed)-prose, justified_retentions=retained, existing_credit=len(draft["records"])',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'The Janus glove rumor and Frozen Rose quest are reviewed across all routes.',
        '# Ritual Officiant Labels test candidate': '# Janus and the Frozen Rose test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            "revises Janus's glove rumor and the Frozen Rose quest across all routes",
        'Preserve verified ritual title candidate': 'Preserve Janus and Frozen Rose candidate and checked draft',
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
