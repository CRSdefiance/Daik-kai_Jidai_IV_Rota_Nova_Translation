"""Register the complete guild-search and survey batch."""

from argparse import ArgumentParser
from copy import deepcopy
from pathlib import Path
from shutil import copyfile
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import finish_ruin_statue_registration_20261118 as windows
from scripts import reconcile_shared_speaker_labels_20261111 as nameplates
from scripts import replay_guild_search_and_survey_20261118 as replay
from scripts import stage_guild_survey_wraps_20261118 as stage


base, native, parent = stage.base, stage.native, stage.parent
workflow = parent.workflow
PROFILE = 'all-routes-guild-search-and-survey-v1-20261118'
ROOT = Path('out/guild_search_and_survey_registered_20261118_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Guild_Search_and_Survey_20261118_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261118_guild_search_and_survey_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_guild_search_and_survey_20261118.md')
QA, STARTUP = stage.ROOT / 'supported_qa.xml', stage.ROOT / 'own_startup_verification.json'
SHOWN = replay.scope['folder'](replay.CASE)
RETENTION_REASONS = {
    (0, 266, 8): 'Keep the complaint private and let the companion resent the habitual bossing.',
    (0, 266, 53): 'Jean stammers, laughs nervously, and appeals to his own word after denying the charge twice.',
    (0, 272, 19): 'Keep Mozambique as the reported base, with the uncertainty of a tip.',
    (1, 257, 6): 'The runtime name is retained in an address to the recognized man. The nearby quest dialogue establishes the London guild.',
    (1, 258, 27): 'Hodram reassesses Yuris after his abrupt reveal. The line recognizes an aristocratic bearing.',
    (2, 257, 16): 'The guildmaster expresses thanks and downplays the value of the reward before handing it over.',
    (3, 225, 24): 'Indonesia is the only broad clue. The contact still poses as unwilling to ask for help.',
    (3, 226, 23): 'Plett admits his identity after giving himself away. He has time to resist before he gives up.',
    (3, 230, 49): 'Jean stammers, laughs nervously, and appeals to his own word after denying the charge twice.',
}


def replay_dependencies(final):
    before = native.files(base.NdsImage.open(stage.prior.ROM))
    after = native.files(final)
    assert before.keys() == after.keys()
    edited = {f'/data/SC{route}.DK4' for route, _, _ in stage.PHRASES}
    assert {path for path in before if before[path] != after[path]} == edited
    for path in sorted(edited):
        route = int(path.removesuffix('.DK4')[-1])
        old, new = [native.IlnkContainer.parse(source[path]).blocks for source in (before, after)]
        assert {i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b} == {
            block for r, block, _ in stage.PHRASES if r == route}
    archive = native.IlnkContainer.parse(after['/data/SC3.DK4'])
    expected = {native.ARM: native.digest(after[native.ARM]),
                '/GRP/KANJI.FNT': native.digest(after['/GRP/KANJI.FNT'])}
    expected.update({f'/data/SC3.DK4:B{block}': native.digest(archive.blocks[block]) for block in (33, 226)})
    return expected


def verify(prior, guard, viewed):
    staged, draft, startup = map(base.load, (stage.STORED, stage.MANUSCRIPT, STARTUP))
    candidate = base.digest(stage.ROM)
    assert staged['candidate_sha256'] == draft['candidate_sha256'] == startup['candidate_sha256'] == candidate
    assert staged['manuscript_sha256'] == base.digest(stage.MANUSCRIPT)
    assert staged['previous_sha256'] == prior['candidate_sha256'] == base.digest(parent.ROM)
    assert startup['cold_boot'] and not startup['savestate'] and startup['complete_deployed_payload_exact']
    assert len(startup['exact_matching_frames']) == 6 and len(startup['original_protected_name_getters']) == 24
    assert all(base.digest(path) == sha for path, sha in startup['evidence'].items())
    live = base.load(SHOWN / 'verified.json')
    assert live['candidate_sha256'] == base.digest(stage.prior.ROM)
    assert live['initialized_emulator'] and not live['natural_activation'] and not live['hardware']
    assert tuple(r['turn'] for r in live['complete_holds']) == replay.TURNS
    assert all(base.digest(path) == sha for path, sha in live['evidence'].items())
    sheets = list(staged['sheets']) + live['sheets']
    assert all(base.digest(s['path']) == s['sha256'] for s in sheets)
    assert tuple(s['sha256'] for s in sheets) == viewed
    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests == 32 and all(int(suite.get(k, 0)) == 0 for k in ('failures', 'errors', 'skipped'))

    clean, old, final = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    assert base.digest(native.CLEAN) == prior['clean_input_sha256']
    replayed = replay_dependencies(final)
    before, after = map(native.files, (old, final))
    assert before.keys() == after.keys()
    archives = staged['target_story_archive_sha256']
    assert {p for p in before if before[p] != after[p]} == archives.keys()
    assert archives.keys() == {f'/data/SC{i}.DK4' for i in range(4)}
    assert native.digest(after[native.ARM]) == staged['target_ARM9_sha256']
    records = draft['records']
    edited = [r for r in records if r['decision'] == 'revision']
    assert len(records) == 206 and len(edited) == staged['preview_count'] == 42
    assert len({(r['file_path'], r['id']) for r in records}) == len(records)
    assert len({(r['route'], r['block']) for r in records}) == len(stage.prior.BLOCKS)
    proof = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert proof['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(proof['source_bound_new_command_counts'].values())
    new_banks = dict(native.transform(old, edited))
    for path, sha in archives.items():
        assert after[path] == new_banks[path] and native.digest(after[path]) == sha
        final.replace_file(path, before[path])
    assert bytes(final.rom.save()) == parent.ROM.read_bytes()

    ctx = native.RegisteredRuntime(parent.RELEASE, prior['own_registered_startup'], captain=3)
    actors = {r['source_selector'] for r in records if r['source_selector'] != 254}
    names = {r['actor_ID']: r for r in nameplates.current_getters(ctx)['rows']
             if r['actor_ID'] in actors and r['consumer'] == 'progressive-nameplate'}
    assert names.keys() == actors
    seen = {r['id'] for r in live['complete_holds']}
    revisited_retentions = set()
    for row in records:
        key = row['route'], row['block'], row['source_reference']['record_index']
        if row['decision'] == 'retention' and not row['earlier_review']['same_logical_English']:
            row['localization_note'] = RETENTION_REASONS[key]
            revisited_retentions.add(key)
        if row['source_selector'] in names:
            row['speaker'] = names[row['source_selector']]['text']
        row['registered_reference'] = row['staged_reference'] | dict(candidate_sha256=candidate)
        row['display_scope'] = 'checked native preview' if row['decision'] == 'revision' else 'byte-identical retention'
        if key[:2] == (3, 226) and row['id'] in seen:
            row['display_scope'] += ' and initialized emulator on byte-identical scene'
    assert revisited_retentions == RETENTION_REASONS.keys()
    draft.update(registered=True, native_sheets=staged['sheets'], initialized_gameplay=live,
                 offline_only_Plett_turns=sorted(set(replay.SCENE_TURNS) - set(replay.TURNS)),
                 replay_dependencies=replayed, checked_story_format_guard=proof, speaker_nameplates=list(names.values()))
    validate_natural_dialogue_batch(draft)
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()
    return staged, draft, edited, tests, sheets


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', required=True, nargs='+')
    args = parser.parse_args()
    assert not any(p.exists() for p in (ROOT, PACKAGE, DOC))
    registry_before, ledger_before = base.REGISTRY.read_bytes(), base.LEDGER.read_bytes()
    main_sha = base.digest(base.PROMOTED)
    registry, ledger, manifest, prior = map(base.load, (base.REGISTRY, base.LEDGER, parent.MANIFEST, parent.RELEASE))
    assert native.digest(registry_before) == prior['registry_sha256'] and base.digest(parent.MANIFEST) == prior['manifest_sha256']
    assert len(registry['accepted_layers']) == 114 and PROFILE not in registry['profiles']
    assert len(manifest['batches']) == 857 and len(manifest['checks']) == 192 and all(manifest['checks'].values())
    profile = deepcopy(registry['profiles'][prior['profile']])
    staged, draft, edited, tests, sheets = verify(prior, profile['source25_multiarchive_guard'], tuple(args.viewed_sha))
    candidate = staged['candidate_sha256']
    credited = {(r['file_path'], r['id']) for r in ledger[base.CONTEXT]['integrated_record_keys']}
    assert all((r['file_path'], r['id']) in credited for r in draft['records'])
    assert ledger['records_editorially_completed'] == 27700 and not ledger['full_goal_complete']
    assert ledger['current_integrated_candidate']['sha256'] == prior['candidate_sha256']
    pending = ledger['pending_shared_consumer_checkpoint_20261114']
    assert pending['remaining_total'] == 276 and pending['candidate_sha256'] == prior['candidate_sha256']

    ROOT.mkdir()
    VERIFY.mkdir(parents=True)
    copyfile(stage.ROOT / 'clean_input.xdelta', PATCH)
    copyfile(stage.ROOT / 'clean_rebuilt.nds', ROM)
    assert base.digest(ROM) == candidate
    for source in (stage.STORED, STARTUP, QA, SHOWN / 'verified.json'):
        copyfile(source, VERIFY / source.name)
        assert base.digest(source) == base.digest(VERIFY / source.name)
    for item in sheets:
        name = Path(item['path']).name
        copyfile(item['path'], VERIFY / name)
        assert base.digest(VERIFY / name) == item['sha256']
    base.save(REVIEW, draft)
    predecessor = {k: prior[k] for k in ('profile', 'candidate', 'candidate_sha256', 'manifest', 'manifest_sha256', 'registry_sha256')}
    backup = ROOT / 'release_stack_before_guild_survey.json'
    backup.write_bytes(registry_before)
    predecessor['registry'] = str(backup)
    profile.update(verified_ruin_statue_and_ice_predecessor=predecessor, guild_search_and_survey_release=str(REVIEW))
    registry['profiles'][PROFILE] = profile
    registry_draft = ROOT / 'release_stack_with_guild_survey.json'
    base.save(registry_draft, registry)
    registry_sha = base.digest(registry_draft)
    manifest.update(profile=PROFILE, candidate_rom=str(ROM), candidate_sha256=candidate, release_stack_sha256=registry_sha)
    manifest['batches'].append(str(REVIEW))
    manifest['checks']['registered_guild_search_and_survey_and_complete_parent_inverse'] = True
    for row in edited:
        ids = manifest['changed_records'][row['file_path']]
        if row['id'] not in ids:
            ids.append(row['id'])
    manifest['guild_search_and_survey_pipeline'] = dict(
        predecessor=predecessor, registered_review=str(REVIEW), registered_review_sha256=base.digest(REVIEW),
        registration_driver_sha256=base.digest(__file__), producer_sha256=base.digest(stage.__file__),
        complete_parent_inverse=True,
        owned_story_blocks={p: sorted({r['block'] for r in edited if r['file_path'] == p})
                            for p in staged['target_story_archive_sha256']})
    base.save(MANIFEST, manifest)
    startup_path = VERIFY / STARTUP.name
    released = prior | dict(profile=PROFILE, candidate=str(ROM), candidate_sha256=candidate, patch=str(PATCH),
        patch_sha256=base.digest(PATCH), manifest=str(MANIFEST), manifest_sha256=base.digest(MANIFEST),
        registry_sha256=registry_sha, predecessor=predecessor, registered_manifest_entries=858, passing_release_checks=193,
        own_registered_startup=str(startup_path), own_registered_startup_sha256=base.digest(startup_path),
        changed_internal_files=sorted(staged['target_story_archive_sha256']), repository_tests=tests,
        new_contextual_records=0, prose_revisions=len(edited), name_label_revisions=0, text_display_revisions=0,
        justified_retentions=len(draft['records']) - len(edited),
        actual_verification_scope=dict(own_startup=True, initialized_Maria_Plett=True, natural_activation=False, hardware=False),
        **{f'target_SC{i}_sha256': staged['target_story_archive_sha256'][f'/data/SC{i}.DK4'] for i in range(4)})
    base.save(RELEASE, released)
    base.save(PACKAGE / 'release_manifest.json', released | {'user_acceptance_pending': True})
    workflow.archive_file(MANIFEST.read_bytes(), PACKAGE / 'build_manifest.json.gz')
    workflow.archive_file(registry_draft.read_bytes(), PACKAGE / 'build_release_stack.json.gz')
    workflow.archive_file(ledger_before, ROOT / 'editorial_ledger_before.json.gz')
    pending['candidate_sha256'] = candidate
    ledger['current_integrated_candidate'].update(path=str(ROM), sha256=candidate, profile=PROFILE, patch=str(PATCH),
        patch_sha256=released['patch_sha256'], manifest=str(MANIFEST), manifest_sha256=released['manifest_sha256'],
        registered_release_verification=str(RELEASE),
        **{f'SC{i}_sha256': released[f'target_SC{i}_sha256'] for i in range(4)})
    checkpoint = 'The survey parties and four guild searches are reviewed across all routes.'
    ledger['guild_search_and_survey_20261118'] = dict(registered_candidate_sha256=candidate, registered_review=str(REVIEW),
        registered_release=str(RELEASE), existing_credit=206, prose_revisions=len(edited),
        justified_retentions=released['justified_retentions'])
    ledger['latest_checkpoint'] = checkpoint
    ledger_after = workflow.encode_ledger(ledger)
    receipt = dict(registry_before=native.digest(registry_before), ledger_before=native.digest(ledger_before),
                   registry_after=registry_sha, ledger_after=native.digest(ledger_after), main_sha256=main_sha)
    base.save(VERIFY / 'registration_mutation_plan.json', receipt)
    (PACKAGE / 'README.md').write_text(f'''# Guild searches and surveys test candidate

The [local ROM](../../{ROM.as_posix()}) includes the survey and guild-search dialogue review and all preceding accepted layers.
The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
Hardware and acceptance for main are pending.
''', encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', workflow.package_checksums(PACKAGE))
    assert base.digest(base.REGISTRY) == receipt['registry_before'] and base.digest(base.LEDGER) == receipt['ledger_before']
    assert base.digest(base.PROMOTED) == main_sha
    base.replace_checked(base.REGISTRY, registry_draft.read_bytes())
    try:
        windows.update_ledger_in_place(ledger_before, ledger_after)
    except (AssertionError, OSError):
        base.replace_checked(base.REGISTRY, registry_before)
        raise
    assert base.digest(base.REGISTRY) == registry_sha and base.digest(base.LEDGER) == receipt['ledger_after']

    pins = Path('translations/rom_retention_pins.json')
    rows = base.load(pins)
    for path in (ROM, stage.ROM, stage.prior.ROM, stage.ROOT.with_name('guild_search_and_survey_20261118_v2') / stage.ROM.name):
        resolved = str(path.resolve())
        assert path.is_file() and all(r['path'] != resolved for r in rows)
        rows.append(dict(path=resolved, reason=f'Preserve guild survey candidate {base.digest(path)}'))
    base.replace_checked(pins, (workflow.dumps(rows, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode())
    with DOC.open('x', encoding='utf-8', newline='\n') as out:
        out.write(f'''# Guild searches and surveys

Reviewed 206 turns in complete exchanges across the four routes. There are {len(edited)} revisions and {released['justified_retentions']} justified retentions. The wording keeps the reports of Jean and Jacob tentative, preserves both surveys' sailor and funding instructions, and restores the tone of the meetings with Yuris, Jacks and Plett. [Exact review ledger](../{REVIEW.as_posix()})

All 42 revised pages passed native checks and visual review. Six phrase refinements received fresh layout checks. Maria's original tavern scene produced 11 exact dialogue holds on the short surrender path in an initialized DeSmuME replay. The crew-dependent turns were checked offline. The final draft preserves the replayed scene, host, font and renderer byte for byte. Natural activation and physical hardware remain unverified. The candidate passed six cold-boot holds, 24 protected names and {tests} targeted repository tests. [Tavern replay](../{(VERIFY / 'live_1.png').as_posix()})

The clean-input patch reconstructs the candidate byte for byte and preserves all 114 accepted layers. Main retains its accepted build. The credited total stays at 27,700 with 276 pending shared keys. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)

The next 135 story turns are staged under work/port_favors_and_searches_source_20261118. They cover SC0 B273–278, SC1 B261–266, SC2 B259–264 and SC3 B233–238. Use both command-index references for Hodram B266 and Maria B233.
''')
    prefix = f'# Current editorial checkpoint - 2026-11-18\n\n{checkpoint} [Checkpoint]({DOC.name})\n\n'.encode()
    for name in ('editorial_handoff_current.md', 'translation_progress.md', 'build_continuity_protocol.md'):
        path = Path('docs') / name
        base.replace_checked(path, prefix + path.read_bytes())
    assert base.digest(base.PROMOTED) == main_sha
    print(f'Registered {candidate} with 858 entries, 114 accepted layers and 193 passing checks.')


if __name__ == '__main__':
    main()
