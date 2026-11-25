"""Register the complete palace and village exchange review."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import replay_palace_and_village_exchanges_20261115 as replay
from scripts import stage_palace_and_village_exchanges_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, parent, native = stage.base, stage.parent, stage.native
PROFILE = 'all-routes-palace-and-village-exchanges-v1-20261115'
ROOT = Path('out/palace_and_village_exchanges_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Palace_and_Village_Exchanges_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_palace_and_village_exchanges_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_palace_and_village_exchanges_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_palace_and_village_exchanges_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_rebuilt.nds')


def verify(prior, guard, viewed, award_frame):
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
    assert len(proof_sheets) == 4 and staged['preview_count'] == 32
    indexed, gameplay = {}, {}
    for case, count in (('faith', 11), ('dagger', 4)):
        location = replay.SCOPE['folder'](case) / 'verified.json'
        result = base.load(location)
        assert result['candidate_sha256'] == candidate
        assert result['initialized_emulator'] and not result['natural_activation'] and not result['hardware']
        assert len(result['complete_holds']) == count
        assert all(base.digest(p) == sha for p, sha in result['evidence'].items())
        proof_sheets.extend(result['sheets'])
        indexed.update({Path(r['path']): f'{case}_{Path(r["path"]).name}' for r in result['sheets']})
        indexed[location] = f'{case}_replay_receipt.json'
        gameplay[case] = result
    captures = base.load(gameplay['dagger']['report'])['frames_captured']
    award = next(r for r in captures if r['frame'] == award_frame)
    assert gameplay['dagger']['complete_holds'][-2]['frame'] < award_frame < gameplay['dagger']['complete_holds'][-1]['frame']
    gameplay['dagger']['directly_viewed_24k_notice'] = award
    proof_sheets.append(dict(path=award['path'], sha256=award['PNG_sha256']))
    indexed[Path(award['path'])] = 'dagger_gold_notice.png'
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
    assert len(records) == 441 and len(edited) == 24
    assert len({(r['file_path'], r['id']) for r in records}) == 441
    credited = {(r['file_path'], r['id']) for r in base.load(base.LEDGER)[base.CONTEXT]['integrated_record_keys']}
    assert all((r['file_path'], r['id']) in credited for r in records)
    for route in range(3):
        path = f'/data/SC{route}.DK4'
        copied = stage.BLOCKS['bandits'][route]
        assert native.IlnkContainer.parse(before[path]).blocks[copied] == native.IlnkContainer.parse(after[path]).blocks[copied]
    rebuilt = dict(native.transform(old, edited))
    for path, expected in archives.items():
        assert rebuilt[path] == after[path] and native.digest(after[path]) == expected
        final.replace_file(path, before[path])
    assert bytes(final.rom.save()) == parent.ROM.read_bytes()
    guard_check = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert guard_check['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(guard_check['source_bound_new_command_counts'].values())
    seen = {hold['id'] for result in gameplay.values() for hold in result['complete_holds']}
    seen.add('DK4_MES_B100_R0019')
    for row in records:
        row['registered_reference'] = row['staged_reference'] | dict(candidate_sha256=candidate)
        row['display_scope'] = 'fresh offline native rendering' if row['decision'] == 'revision' else 'byte-identical retention'
        if row['route'] == 3 and row['id'] in seen:
            row['display_scope'] += ' and initialized emulator'
    draft.update(registered=True, native_sheets=staged['sheets'], gameplay=gameplay,
                 checked_story_format_guard=guard_check)
    validate_natural_dialogue_batch(draft)
    assert review.REBUILT.read_bytes() == stage.ROM.read_bytes() and review.PATCH.is_file()
    return staged, draft, tests, indexed


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', nargs='+', required=True)
    parser.add_argument('--award-frame', type=int, required=True)
    args = parser.parse_args()
    source = getsource(workflow.main)
    start = source.index('    base.replace_checked(DOC, f')
    end = source.index("'''.encode('utf-8'))", start) + len("'''.encode('utf-8'))")
    note = """    base.replace_checked(DOC, f'''# Palace and village exchanges

The review covers 20 blocks and 441 previously credited speeches from the clean Japanese. It preserves each captain's palace departure and the grandfather's urgent plea, relief and gratitude. The lamp scene keeps the village's account in the villager's voice and gives the entrusted lamp its own beat. The dagger scene preserves the discoverers' right to the blade, the speaker's gratitude and the 24,000-gold notice. The three earlier-route copies of the bandit block remain byte-identical. [Exact record ledger](../{REVIEW.as_posix()})

The batch has {prose} wording revisions, {len(changed)-prose} wrap-only fixes and 417 justified retentions. All 32 revised display previews were visually reviewed. Xien's question preserves the native first-name substitution. Default and 1-, 2-, 15- and 16-character cases passed the parser, full glyph and bounds checks. The edited multi-page speeches advance at complete sentences.

Initialized Maria replays displayed all 15 speech pages in the lamp and dagger exchanges, including the lamp's page turn, the original gold notice and the return. Other copies and the custom-name cases were checked offline. Natural scene activation and hardware remain unvisited. [Lamp replay](../{(VERIFY / 'faith_live_2.png').as_posix()}) · [Dagger gold notice](../{(VERIFY / 'dagger_gold_notice.png').as_posix()})

The [registered ROM and clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers and the existing ASCII right bound, Market and Sailor Info fixes. The patch reconstructs the exact ROM. Six startup frames, 24 protected name getters and {tests} targeted tests passed. Existing editorial credit stays at 27,700.
'''.encode('utf-8'))"""
    changes = {
        source[start:end]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 849 and len(manifest['checks']) == 184",
        '825 entries, 114 accepted layers and 160 passing checks': '850 entries, 114 accepted layers and 185 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160': 'registered_manifest_entries=850, passing_release_checks=185',
        "staged, draft, tests = verify(prior, profile['source25_multiarchive_guard'])":
            "staged, draft, tests, indexed = verify(prior, profile['source25_multiarchive_guard'], VIEWED, AWARD_FRAME)\n"
            "    changed = [r for r in draft['records'] if r['decision'] == 'revision']\n"
            "    prose = sum(native_english(r['english']) != r['previous_English'] for r in changed)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.palace_village.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.palace_village.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_palace_village.json',
        'stage.digest(registry_before), ledger_before=stage.digest(ledger_before)':
            'native.digest(registry_before), ledger_before=native.digest(ledger_before)',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_town_quest_exchanges_predecessor=predecessor, palace_village_exchanges_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['palace_village_exchanges_pipeline']",
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
        'initialized_Rafael_dialogue=True': 'initialized_Maria_lamp_and_dagger=True, natural_activation=False',
        'new_contextual_records=0, prose_revisions=0,': 'new_contextual_records=0, prose_revisions=prose,',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=len(changed)-prose, justified_retentions=417, reviewed_UI_labels=0',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['palace_village_exchanges_20261115']",
        'name_label_revisions=2, justified_retentions=13':
            'prose_revisions=prose, wrap_only_revisions=len(changed)-prose, justified_retentions=417, existing_credit=441',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'Palace and village scenes have 24 revisions and 417 justified retentions in 20 blocks.',
        '# Ritual Officiant Labels test candidate': '# Palace and Village Exchanges test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            'updates the palace rescue and village exchanges across the routes',
        'Preserve verified ritual title candidate': 'Preserve verified palace and village candidate',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.STORED, STARTUP, QA, *(Path(s['path']) for s in draft['native_sheets']))",
        '    base.save(REVIEW, draft)': (
            '    for path, name in indexed.items():\n'
            '        copyfile(path, VERIFY / name)\n'
            '        assert base.digest(path) == base.digest(VERIFY / name)\n'
            '    base.save(REVIEW, draft)'),
    }
    env = vars(workflow) | globals() | dict(VIEWED=tuple(args.viewed_sha), AWARD_FRAME=args.award_frame,
                                           native_english=stage.normalize)
    exec(compile(checked_text(source, changes), __file__ + '::register', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
