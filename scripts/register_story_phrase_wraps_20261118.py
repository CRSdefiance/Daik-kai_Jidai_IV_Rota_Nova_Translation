"""Register nine verified story phrase wraps."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import replay_story_phrase_wraps_20261118 as replay
from scripts import stage_story_phrase_wraps_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, parent, native = stage.base, stage.parent, stage.native
PROFILE = 'all-routes-story-phrase-wraps-v1-20261118'
ROOT = Path('out/story_phrase_wraps_registered_20261118_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Story_Phrase_Wraps_20261118_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261118_story_phrase_wraps_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_story_phrase_wraps_20261118.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_story_phrase_wraps_and_complete_parent_inverse'
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
    assert len(proof_sheets) == 2 and staged['preview_count'] == 9
    location = replay.SCOPE['folder'](replay.CASE) / 'verified.json'
    result = base.load(location)
    assert result['candidate_sha256'] == candidate
    assert result['initialized_emulator'] and not result['natural_activation'] and not result['hardware']
    assert [(r['id'], r['page']) for r in result['complete_holds']] == [
        (f'DK4_MES_B{block}_R{number:04d}', 1) for block, ids in replay.EXCERPTS.items() for number in ids
    ]
    assert all(base.digest(p) == sha for p, sha in result['evidence'].items())
    proof_sheets.extend(result['sheets'])
    indexed = {Path(r['path']): f'rafael_proof_{Path(r["path"]).name}' for r in result['sheets']}
    indexed[location] = 'rafael_proof_replay_receipt.json'
    gameplay = {replay.CASE: result}
    assert tuple(s['sha256'] for s in proof_sheets) == viewed
    assert all(base.digest(r['path']) == r['sha256'] for r in proof_sheets)

    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests == 32 and not any(int(suite.get(key, 0)) for key in ('failures', 'errors', 'skipped'))
    clean, old, final = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    before, after = map(native.files, (old, final))
    archives = staged['target_story_archive_sha256']
    assert len(archives) == 4 and before.keys() == after.keys()
    assert before[native.ARM] == after[native.ARM]
    assert native.digest(after[native.ARM]) == staged['target_ARM9_sha256']
    assert {p for p in before if before[p] != after[p]} == archives.keys()
    records = draft['records']
    edited = [r for r in records if r['decision'] == 'revision']
    assert len(records) == 335 and len(edited) == 9
    assert len({(r['file_path'], r['id']) for r in records}) == 335
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
    for row in records:
        row['registered_reference'] = row['staged_reference'] | dict(candidate_sha256=candidate)
        row['display_scope'] = 'fresh offline native rendering' if row['decision'] == 'revision' else 'byte-identical retention'
        if row['route'] == 0 and row['id'] in seen:
            row['display_scope'] += ' and initialized emulator'
    draft.update(registered=True, native_sheets=staged['sheets'], gameplay=gameplay,
                 checked_story_format_guard=guard_check)
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
    note = """    base.replace_checked(DOC, f'''# Story phrase wraps

The nine flagged breaks were reviewed in their original exchanges across all four routes. The batch keeps Proof of Conquest, Indian Ocean, Shandong Peninsula, Southeast Asia and trade house together. Rafael's crown clue keeps the speaker's uncertainty and the item description. Maria still asks what serves as the map before Xien suggests the coin. Both versions of Maria's completed collection use the same line. The batch records {prose} wording revisions, {len(changed)-prose} wrap-only fixes and 326 retentions with source and current references. [Exact review ledger](../{REVIEW.as_posix()})

All nine revised pages passed native rendering and visual review. Initialized DeSmuME playback showed nine original dialogue commands from Rafael's two excerpts, including both revisions and the surrounding replies. B79 used the conditional reply in the excerpt. Other routes were checked offline. Natural scene activation and hardware remain unvisited. [Rafael replay](../{(VERIFY / 'rafael_proof_live_1.png').as_posix()})

The clean-input patch reconstructs the registered candidate byte for byte. The combined build carries all 114 accepted layers. The startup comparison, 24 protected name getters and {tests} targeted tests passed. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
'''.encode('utf-8'))"""
    changes = {
        source[start:end]: note,
        'Current editorial checkpoint - 2026-11-15': 'Current editorial checkpoint - 2026-11-18',
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 850 and len(manifest['checks']) == 185",
        '825 entries, 114 accepted layers and 160 passing checks': '851 entries, 114 accepted layers and 186 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160': 'registered_manifest_entries=851, passing_release_checks=186',
        "staged, draft, tests = verify(prior, profile['source25_multiarchive_guard'])":
            "staged, draft, tests, indexed = verify(prior, profile['source25_multiarchive_guard'], VIEWED)\n"
            "    changed = [r for r in draft['records'] if r['decision'] == 'revision']\n"
            "    prose = sum(native_english(r['english']) != r['previous_English'] for r in changed)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.story_phrase_wraps.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.story_phrase_wraps.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_story_phrase_wraps.json',
        'stage.digest(registry_before), ledger_before=stage.digest(ledger_before)':
            'native.digest(registry_before), ledger_before=native.digest(ledger_before)',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_palace_village_exchanges_predecessor=predecessor, story_phrase_wraps_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['story_phrase_wraps_pipeline']",
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
        'initialized_Rafael_dialogue=True': 'initialized_Rafael_proof_excerpts=True, natural_activation=False',
        'new_contextual_records=0, prose_revisions=0,': 'new_contextual_records=0, prose_revisions=prose,',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=len(changed)-prose, justified_retentions=326, reviewed_UI_labels=0',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['story_phrase_wraps_20261118']",
        'name_label_revisions=2, justified_retentions=13':
            'prose_revisions=prose, wrap_only_revisions=len(changed)-prose, justified_retentions=326, existing_credit=335',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'Nine story phrase breaks are fixed across all four routes.',
        '# Ritual Officiant Labels test candidate': '# Story Phrase Wraps test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            'keeps nine previously split story phrases together',
        'Preserve verified ritual title candidate': 'Preserve verified story phrase wrap candidate',
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
