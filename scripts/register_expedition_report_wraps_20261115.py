"""Register the reviewed expedition reports and their verified native display."""

from inspect import getsource
from pathlib import Path
from xml.etree import ElementTree

from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import checkpoint_expedition_search_replay_20261115 as live
from scripts import register_refit_help_wraps_20261115 as precedent
from scripts import stage_expedition_report_wraps_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-expedition-report-wraps-v1-20261115'
ROOT = Path('out/expedition_report_wraps_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Expedition_Report_Wraps_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_expedition_report_wraps_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_expedition_report_wraps_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'repository_qa_verified.xml'
NATIVE_SHEET = stage.ROOT / 'portrait_sheet_01.png'
VIEWED = 'bdc33b5ffea1b84224fad515d04637ae110172f248048d0484bf450eaa21f038'
CHECKPOINT = 'Thirty-five expedition reports are reviewed. Nineteen received prose or wrap corrections.'
EDITED = sorted(stage.PHRASES.keys() | stage.PROSE.keys())


def verify(prior, guard):
    storage, review, gameplay, startup = map(base.load, (stage.STORED, stage.MANUSCRIPT, live.OUTPUT, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == storage['candidate_sha256'] == review['candidate_sha256'] == startup['candidate_sha256']
    assert candidate == gameplay['candidate_sha256']
    assert base.digest(parent.ROM) == prior['candidate_sha256'] == storage['previous_sha256'] == review['previous_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256'] == review['clean_sha256']
    assert base.digest(stage.MANUSCRIPT) == storage['manuscript_sha256']
    assert storage['whole_parent_inverse'] and storage['preserved_entries'] == 3649
    assert sorted(map(int, storage['allocations'])) == EDITED and storage['native_checked_records'] == 35
    sheet, = storage['sheets']
    assert Path(sheet['path']) == NATIVE_SHEET and base.digest(NATIVE_SHEET) == sheet['sha256'] == VIEWED
    assert sheet['messages'] == EDITED
    assert gameplay['native_message'] == 2244 and gameplay['original_sailor_loss'] == 11
    assert gameplay['original_return_to_sailing']
    assert startup['cold_boot'] and not startup['savestate'] and startup['complete_deployed_payload_exact']
    assert len(startup['exact_matching_frames']) == 6 and len(startup['original_protected_name_getters']) == 24
    for bundle in (gameplay, startup):
        assert all(base.digest(path) == digest for path, digest in bundle['evidence'].items())
    tests, = ElementTree.parse(QA).iter('testsuite')
    assert tuple(int(tests.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')) == (40, 0, 0, 0)
    old, new = map(base.NdsImage.open, (parent.ROM, stage.ROM))
    before, after = map(stage.files, (old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {stage.COMMON}
    precedent.verify_runtime(after[stage.ARM], prior)
    assert precedent.digest(after[stage.COMMON]) == storage['target_COMMON_sha256']
    checked = bind_registered_story_percent_guard(guard)(stage.files(base.NdsImage.open(stage.CLEAN)), after)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    new.replace_file(stage.COMMON, before[stage.COMMON])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    rows = review['records']
    assert len(rows) == 35 and sorted(r['message_ID'] for r in rows if r['decision'] != 'retention') == EDITED
    for row in rows:
        assert 1 <= len(row['visible_lines']) <= 4 and row['glyph_count'] > 0
        row['review']['formatting'] = True
        row['registered_reference'] = row['staged_reference'] | dict(exact_stored_hex=row['staged_hex'],
                                                                       candidate_sha256=candidate)
    document = review | dict(checked_story_format_guard=checked, observed_gameplay=gameplay,
        reviewed_sheet_sha256=VIEWED, direct_visual_review_complete=True, new_editorial_credit=0)
    precedent.validate_natural_dialogue_batch(document)
    return storage, document


def update_ledger(ledger, release, sha, checkpoint):
    pending = ledger['pending_shared_consumer_checkpoint_20261114']
    assert pending['remaining_total'] == 276 and pending['candidate_sha256'] == release['predecessor']['candidate_sha256']
    assert not set(pending['remaining_legacy_keys']).intersection(stage.NUMBERS)
    pending['candidate_sha256'] = sha
    ledger['current_integrated_candidate'].update(path=str(ROM), sha256=sha, profile=PROFILE, patch=str(PATCH),
        patch_sha256=release['patch_sha256'], manifest=str(MANIFEST), manifest_sha256=release['manifest_sha256'],
        MESFILE_sha256=release['target_COMMON_sha256'], registered_release_verification=str(RELEASE))
    ledger['latest_checkpoint'] = checkpoint
    ledger['expedition_report_wraps_20261115'] = dict(review=str(REVIEW), release=str(RELEASE),
        revised_existing_keys=EDITED, retained_existing_keys=sorted(set(stage.NUMBERS) - set(EDITED)),
        new_dialogue_credit=0, remaining_mapped_shared_records=276)


def main():
    source = getsource(precedent.main)
    lo = source.index("    doc = '''")
    hi = source.index("    source = source[:doc_lo]", lo)
    doc = '''    doc = \'\'\'    base.replace_checked(DOC, f"""# Expedition report wraps

The [registered review](../{REVIEW.as_posix()}) covers all 35 oasis, mirage, bog, and preliminary-discovery reports. Seven received prose revisions, twelve were rewrapped without changing the wording, and sixteen were retained. The original speaker tables and provisional language are preserved. Two oasis reactions fit on one line, the bog warning keeps “I hear” together, and the preliminary reports keep “found something” together.

All 35 native portrait cases passed. The [19 revised pages](../{(VERIFY / "portrait_sheet_01.png").as_posix()}) received visual review. A representative emulator Search replay used the existing copied save and disclosed location and crew setup. It reproduced the related shore report, the loss of 11 sailors, and the original return to sailing. The 19 changed variants received offline checks. Hardware testing remains open.

The cumulative startup matched six frames and 24 protected name getters. Forty current tests passed. A separate historical test module could not run because its V254 ROM fixture was unavailable. The [registered cumulative ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers and the ASCII right bound. All 35 records already had credit. The ledger stands at 27,700 reviews with 276 mapped shared records remaining.
""".encode())\'\'\'
'''
    source = source[:lo] + doc + source[hi:]
    replacements = {
        '== 813 and len(manifest["checks"]) == 148': '== 815 and len(manifest["checks"]) == 150',
        'release_stack.refit_help_wraps.pending.json': 'release_stack.expedition_report_wraps.pending.json',
        'editorial_review_current.refit_help_wraps.pending.json': 'editorial_review_current.expedition_report_wraps.pending.json',
        'release_stack_before_refit_help_wraps.json': 'release_stack_before_expedition_report_wraps.json',
        'NATIVE, \'\n            \'Path(base.load(NATIVE)["review_sheets"][0]["path"]), Path(base.load(live.OUTPUT)["screenshot"])':
            'stage.MANUSCRIPT, \'\n            \'NATIVE_SHEET',
        'verified_name_or_words_confirmation_predecessor=lineage, refit_help_wraps_release':
            'verified_price_info_wraps_predecessor=lineage, expedition_report_wraps_release',
        'Source-reviewed Refit help and verified native wrapping.': 'Source-reviewed expedition reports and native wrapping.',
        'registered_refit_help_wraps_and_complete_parent_inverse': 'registered_expedition_report_wraps_and_complete_parent_inverse',
        'sorted(stage.REVISIONS)': 'EDITED',
        'refit_help_wraps_registered_successor_pipeline': 'expedition_report_wraps_registered_successor_pipeline',
        'registered_manifest_entries=814,passing_release_checks=149,repository_tests=16,legacy_fixture_tests_skipped=2':
            'registered_manifest_entries=816,passing_release_checks=151,repository_tests=40,legacy_fixture_tests_skipped=0',
        'prose_revisions=6,justified_retentions=25,text_display_revisions=6':
            'prose_revisions=7,justified_retentions=16,text_display_revisions=19',
        'observed_revised_refit_holds=4,exact_surrounding_holds=11': 'observed_related_shore_report=2244,original_return_to_sailing=True',
        'offline_complete_refit_planes=6': 'offline_complete_native_portraits=35',
        '# Shipyard Refit Help test candidate': '# Expedition Report Wraps test candidate',
        'includes the revised Shipyard Refit help': 'includes the revised expedition reports',
        'Preserve Refit help release and verified replay.': 'Preserve expedition report release and verified replay.',
        '814 entries, 114 accepted layers, 149 checks.': '816 entries, 114 accepted layers, 151 checks.',
    }
    env = vars(precedent) | globals()
    exec(compile(checked_text(source, replacements), __file__ + '::expedition-registration', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
