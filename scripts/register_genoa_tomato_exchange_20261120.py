"""Register the Genoa exchange after native validation and its normal town trigger."""

from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_additional_town_visits_20261120 as town
from scripts import check_genoa_tomato_exchange_20261120 as live
from scripts import register_sailing_help_20261120 as parent
from scripts import stage_genoa_tomato_exchange_20261120 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch = parent.base, parent.batch
PROFILE = 'all-routes-genoa-tomatoes-v1-20261120'
ROOT = Path('out/genoa_tomatoes_registered_20261120_v1')
ROM = ROOT / 'Translation_DS_Genoa_Tomatoes_20261120_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261120_genoa_tomatoes_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_genoa_tomatoes_registered_20261120.md')
STARTUP, QA = (stage.ROOT / n for n in ('own_startup_verification.json', 'qa.xml'))
STARTUP_CAPTURE = stage.ROOT / 'startup/capture/capture_report.json'
CHECKPOINT = 'Registered the four-route Genoa tomato scene and recorded its ordinary Square trigger and Julio’s Tavern recruitment.'


def verify(registry, previous, viewed):
    stored, draft, actual, nearby = map(base.load, (stage.STORED, stage.MANUSCRIPT, live.PROOF, town.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == draft['candidate_sha256'] == actual['candidate_sha256']
    assert base.digest(parent.ROM) == previous['candidate_sha256'] == stored['previous_sha256'] == nearby['candidate_sha256']
    assert stored['whole_parent_inverse'] and base.digest(stage.MANUSCRIPT) == stored['manuscript_sha256']
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()
    assert viewed == {r['path']: r['sha256'] for r in stored['sheets']} | actual['sheet']
    assert all(base.digest(p) == sha for p, sha in (viewed | actual['evidence'] | nearby['evidence']).items())
    assert actual['original_square_entrance_ordinary_inputs'] and actual['observed_revisions'] == 4
    assert len(actual['panels']) == 10 and sum(map(len, nearby['scenes'].values())) == 18
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [17, 0, 0, 0]
    clean, prior, target = map(base.NdsImage.open, (stage.original.CLEAN, parent.ROM, stage.ROM))
    before, after = map(batch.files, (prior, target))
    allowed = {f'/data/SC{i}.DK4': n for i, n in enumerate((189, 181, 177, 150)) if i != 2}
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == allowed.keys()
    archives = {path: batch.digest(after[path]) for path in allowed}
    assert archives == stored['target_story_archive_sha256']
    arm = after[stage.original.ARM]
    assert batch.digest(arm) == stored['target_ARM9_sha256'] == previous['target_ARM9_sha256']
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(batch.files(clean), after)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    for path, block in allowed.items():
        old, new = (stage.original.IlnkContainer.parse(f[path]).blocks for f in (before, after))
        assert [i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b] == [block]
        target.replace_file(path, before[path])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    records = draft['records']
    assert len(records) == 40 and sum(r['decision'] == 'revision' for r in records) == stored['preview_count'] == 10
    for row in records:
        row['registered_reference'] = row['staged_reference'] | {'candidate_sha256': candidate}
        row['ordinary_square_gameplay'] = row['route'] == 1
    validate_natural_dialogue_batch(draft)
    starter = parent.env['startup_check'].startup_proof
    FunctionType(starter.__code__, starter.__globals__ | {'STARTUP': STARTUP, 'STARTUP_CAPTURE': STARTUP_CAPTURE})(
        previous, candidate, arm)
    draft.update(candidate_sha256=candidate, checked_story_format_guard=controls,
        shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'], unchanged_pending_records=276,
        original_Genoa_trigger=actual, town_evidence={'path': str(town.OUTPUT), 'sha256': base.digest(town.OUTPUT)},
        new_contextual_credit=0)
    return stored, draft, archives


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index('    DOC.write_text'):template.index('    prefix =')]
program = checked_text(template, {
    'len(manifest["batches"]) == 952 and len(manifest["checks"]) == 287':
        'len(manifest["batches"]) == 953 and len(manifest["checks"]) == 288',
    'stage.PROOF, stage.PLAN, STARTUP, QA, replay.LIVE, replay.NAV, args.visual_review,':
        'stage.STORED, STARTUP, QA, live.PROOF, town.OUTPUT, args.visual_review,',
    'release_stack_before_sailing_help.json': 'release_stack_before_genoa_tomatoes.json',
    'release_stack_with_sailing_help.json': 'release_stack_with_genoa_tomatoes.json',
    'verified_tavern_help_predecessor=predecessor, sailing_help_release=str(REVIEW)':
        'verified_sailing_help_predecessor=predecessor, genoa_tomatoes_release=str(REVIEW)',
    'registered_sailing_help_and_complete_parent_inverse': 'registered_genoa_tomatoes_and_complete_parent_inverse',
    '    for row in draft["records"]:\n        key, file = row["id"], row["file_path"]\n        if file == stage.HELP:\n            assert (file, key) in credited':
        '    for row in draft["records"]:\n        key, file = row["id"], row["file_path"]\n        assert (file, key) in credited',
    'manifest["sailing_help_pipeline"]': 'manifest["genoa_tomatoes_pipeline"]',
    'stored_proof_sha256=base.digest(stage.PROOF)': 'stored_proof_sha256=base.digest(stage.STORED)',
    'native_and_emulator_evidence_sha256=base.digest(replay.LIVE)': 'native_and_emulator_evidence_sha256=base.digest(live.PROOF)',
    'owned_help_pages=base.load(stage.PLAN)["owned_topic_ids"], target_HELP_sha256=archives[stage.HELP]':
        'owned_story_blocks={path: n for path, n in zip(sorted(archives), (189, 181, 150), strict=True)}, target_story_archive_sha256=archives',
    'changed_components=1, target_HELP_sha256=archives[stage.HELP]': 'changed_components=3',
    'reviewed_UI_labels=3, previously_localized_records=11, new_contextual_records=0, prose_revisions=4, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=7':
        'reviewed_UI_labels=0, previously_localized_records=40, new_contextual_records=0, prose_revisions=10, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=30',
    'ordinary_sailing_help_4_pages=True, command_links_and_history=True':
        'ordinary_Genoa_10_pages=True, original_scene_trigger_and_town_return=True',
    'ledger["sailing_help_20261120"]': 'ledger["genoa_tomatoes_20261120"]',
    'prior_records_reviewed=11, actual_help_pages=4, new_contextual_credit=0,\n        prose_revisions=4, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=7':
        'prior_records_reviewed=40, ordinary_story_pages=10, new_contextual_credit=0,\n        prose_revisions=10, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=30',
    'Preserve the Sailing Help candidate or reconstruction': 'Preserve the Genoa tomato candidate or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Genoa tomato exchange testing candidate

The [testing ROM](../../{ROM.as_posix()}) contains the reviewed recurring Genoa scene. The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Genoa tomato trend and regional town visits

Reviewed all ten turns of the Genoa tomato scene on Rafael, Hodram, Lil, and Maria's routes. The owner keeps her enthusiasm and romantic digression, and the cook keeps his dry replies. Ten wordings changed and thirty kept their existing wording for individual reasons. Owner and Cook stay as the speaker labels. [Exact clean, prior, and installed references](../{REVIEW.as_posix()})

The ordinary Square visit on Hodram's route played all nine speeches, the forecast, and the return to town in both emulator runs. All four changed panels matched the complete native glyph masks. All ten revised pages across the three changed routes passed offline display review. The other route copies received offline checks. [Replay and native pages](../{VERIFY.as_posix()})

The Genoa Tavern visit reached Julio's recruitment with both choices set to their first option, then returned to the Tavern menu. Eighteen regional dialogue and nameplate holds passed in Copenhagen, Riga, and Tripoli. These separate runs used the prior registered build. Alternate Julio outcomes and hardware were outside the observed coverage. [Town coverage](../{town.OUTPUT.as_posix()})

The cumulative candidate keeps 114 accepted layers, passes six startup holds, 24 protected getters, and 17 focused tests, and reconstructs byte for byte from the clean-input patch. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register-genoa', 'exec'), env)


if __name__ == '__main__':
    env['main']()
