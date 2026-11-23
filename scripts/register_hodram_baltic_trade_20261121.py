"""Register Hodram's verified port lesson and its byte-exact cumulative patch."""

from pathlib import Path
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_refit_sailing_parallel_routes_20261121 as parent
from scripts import verify_hodram_baltic_trade_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, workflow = display.stage, parent.base, parent.native, parent.workflow
live = SimpleNamespace(PROOF=display.LIVE)
PROFILE = 'all-routes-hodram-baltic-trade-lesson-v1-20261121'
ROOT = Path('out/hodram_baltic_trade_registered_20261121')
ROM = ROOT / 'Translation_DS_Hodram_Baltic_Trade_20261121_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261121_hodram_baltic_trade_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_hodram_baltic_trade_registered_20261121.md')
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / 'own_startup_verification.json', EVIDENCE / 'qa_passed.xml'
STARTUP_CAPTURE = display.replay.STARTUP_CAPTURE
CHECKPOINT = ("Registered five revisions to Hodram's Baltic trade lesson and four justified retentions. "
              "Ordinary Hamburg gameplay verified all nine panels and the return to port.")


def verify(registry, previous, viewed):
    stored, draft, rendered, playback = map(base.load, (stage.PROOF, stage.OUTPUT, display.PROOF, live.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == rendered['candidate_sha256'] == playback['candidate_sha256']
    assert stored['predecessor_sha256'] == draft['previous_sha256'] == previous['candidate_sha256'] == base.digest(parent.ROM)
    assert stored['manuscript_sha256'] == base.digest(stage.OUTPUT)
    assert rendered['stage_proof_sha256'] == base.digest(stage.PROOF)
    assert draft['source_packet_sha256'] == base.digest(draft['source_packet'])
    assert draft['decisions'] == {'revision': 5, 'retention': 4} and stored['whole_parent_inverse']
    assert playback['natural_activation'] and playback['exact_native_glyph_matches']
    assert playback['original_port_transition'] and not playback['hardware_verified']
    assert rendered['newly_rendered_pages'] == 5 and not rendered['actual_gameplay']
    assert len(playback['holds']) == 5 and len(playback['unchanged_controls']) == 4
    assert viewed == {s['path']: s['sha256'] for s in rendered['sheets'] + playback['sheets']} and len(viewed) == 3
    assert all(base.digest(path) == sha for path, sha in (viewed | playback['evidence']).items())
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, '0')) for k in ('tests', 'failures', 'errors', 'skipped')] == [17, 0, 0, 0]
    assert base.digest(native.CLEAN) == previous['clean_input_sha256']
    assert (EVIDENCE / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()

    clean, old_rom, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    source, before, after = map(native.files, (clean, old_rom, target))
    path, number = stage.SCENE, stage.BLOCK
    group, = stored['groups']
    assert (group['file_path'], group['block']) == (path, number)
    assert before.keys() == after.keys() and {name for name in before if before[name] != after[name]} == {path}
    old, new = [native.IlnkContainer.parse(data).blocks for data in (before[path], after[path])]
    assert [i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b] == [number]
    assert native.digest(old[number]) == group['before'] and native.digest(new[number]) == group['after']
    target.replace_file(path, before[path])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    target.replace_file(path, after[path])
    assert bytes(target.rom.save()) == stage.ROM.read_bytes()
    arm = after[native.ARM]
    assert native.digest(arm) == previous['target_ARM9_sha256']
    assert native.digest(after['/COMMON/MESFILE.DK4']) == previous['target_COMMON_sha256']
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(source, after)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())

    startup = parent.scope['startup_check'].startup_proof
    FunctionType(startup.__code__, startup.__globals__ |
                 {'STARTUP': STARTUP, 'STARTUP_CAPTURE': STARTUP_CAPTURE})(previous, candidate, arm)
    checked = {row['id']: row for row in rendered['records']}
    revised = {row['id'] for row in playback['holds']}
    retained = {row['id'] for row in playback['unchanged_controls']}
    assert len(checked) == len(draft['records']) == 9 and revised.isdisjoint(retained)
    assert set(checked) == revised | retained
    archive_sha256 = native.digest(after[path])
    for row in draft['records']:
        ident = row['id']
        result = checked[ident]
        raw, at = bytes.fromhex(result['stored_command_hex']), result['stored_offset']
        assert new[number][at:at + len(raw)] == raw
        assert row['decision'] == result['decision']
        assert (ident in revised) == (row['decision'] == 'revision') and result['native_pages'] == 1
        row['review']['formatting'] = True
        row['registered_reference'] = dict(file_path=path, block=number, command_offset=at, offset=at + 5,
            exact_stored_hex=result['installed_selector_and_body'], exact_command_hex=raw.hex(),
            archive_sha256=archive_sha256, block_sha256=group['after'], candidate_sha256=candidate)
        row['observed_in_ordinary_gameplay'] = True
        row['native_formatting_evidence'] = result
    draft.update(candidate_sha256=candidate, status='registered', direct_visual_review=viewed,
        review_gates=sorted(REQUIRED_REVIEW_GATES),
        checked_story_format_guard=controls, new_contextual_credit=0, shared_payload_and_lookup_exact=True,
        native_preview_evidence=str(display.PROOF), ordinary_town_replay_evidence=str(live.PROOF),
        shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'])
    validate_natural_dialogue_batch(draft)
    return stored, draft, {path: archive_sha256}


readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'verified_fernando_parallel_routes_predecessor': 'verified_refit_sailing_parallel_routes_predecessor',
    'len(batches) == 994 and len(checks) == 329': 'len(batches) == 995 and len(checks) == 330',
    'original_refit_and_sailing_command_maps_preserved=True': 'original_Baltic_trade_lesson_command_map_preserved=True',
    'changed_components=3, repository_tests': 'changed_components=1, repository_tests',
    'previously_localized_records=134, new_contextual_records=0, prose_revisions=84':
        'previously_localized_records=9, new_contextual_records=0, prose_revisions=5',
    'wrap_only_revisions=1, justified_retentions=49': 'wrap_only_revisions=0, justified_retentions=4',
    'pagination_fixes=3': 'pagination_fixes=0',
    'focused_Hodram_sailing_and_Lil_refit=True': 'ordinary_Hodram_Hamburg_docking=True',
    'native_revised_pages=85, observed_holds=36, native_choice_captions=8, natural_activation=False':
        'native_revised_pages=5, observed_holds=9, natural_activation=True',
    'prior_records_reviewed=134, observed_Hodram_and_Lil_panels=36, native_pages=85':
        'prior_records_reviewed=9, observed_Hodram_panels=9, native_pages=5',
    'prose_revisions=84, justified_retentions=49, wrap_only_revisions=1':
        'prose_revisions=5, justified_retentions=4, wrap_only_revisions=0',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram's Baltic trade lesson testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes the reviewed Baltic trade lesson. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace('refit_sailing_parallel_routes', 'hodram_baltic_trade').replace(
    'verified_hodram_baltic_trade_predecessor', 'verified_refit_sailing_parallel_routes_predecessor')

notes = parent.commit_candidate[parent.commit_candidate.index('    DOC.write_text'):
                                parent.commit_candidate.index('    prefix =')]
commit_candidate = checked_text(parent.commit_candidate, {
    'Preserve the parallel refit and sailing candidate, staging and focused emulator ROMs':
        'Preserve the Baltic trade candidate, staged build and its registered predecessor',
    notes: '''    DOC.write_text(f"""# Hodram's Baltic trade lesson

Reviewed all nine records against the clean Japanese, with five wording revisions and four justified retentions. Gerhard's opening makes the two orders direct. Charles's explanation restores the role of a strong fleet and clarifies wartime investment. Manuel explains why even a one percent share lets players spread their contracts. Hodram's summary keeps both comparisons intact in three lines. [Exact review ledger](../{REVIEW.as_posix()})

The captured Copenhagen departure and ordinary voyage reached the original Hamburg docking prompt. The revised build displayed all five new pages with complete glyphs and nameplates. The four retained screens and the return to the Hamburg port menu matched the predecessor. [Native and gameplay evidence](../{VERIFY.as_posix()})

Six startup holds, 24 protected name getters, 17 focused tests and exact clean-input reconstruction passed. The nine records already carried editorial credit. [Testing ROM and clean-input patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace('refit_sailing_parallel_routes', 'hodram_baltic_trade')

scope = vars(parent.template) | globals()
for source in (build, commit_candidate):
    exec(compile(source, __file__, 'exec'), scope)


if __name__ == '__main__':
    scope['main']()
