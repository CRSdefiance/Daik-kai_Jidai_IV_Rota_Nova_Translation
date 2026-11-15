"""Register the verified Price Info wrap review on the cumulative stack."""

from inspect import getsource
from pathlib import Path
from xml.etree import ElementTree

from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import checkpoint_price_info_wraps_20261115 as live
from scripts import register_refit_help_wraps_20261115 as precedent
from scripts import stage_price_info_wraps_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-price-info-wraps-v1-20261115'
ROOT = Path('out/price_info_wraps_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Price_Info_Wraps_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_price_info_wraps_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_price_info_wraps_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'repository_qa_verified.xml'
NATIVE_SHEET = stage.ROOT / 'portrait_sheet_01.png'
VIEWED_NATIVE = '9b0f2c9e5a123e4d6160fa6635f37416dfce502a24da8f1e29831da0a513be70'
VIEWED_GAMEPLAY = '3844dd7aa0098c572d93c96804a7e685864b55df54ff669849feeaca5de342b7'
CHECKPOINT = 'Nine two-page Price Info descriptions are reviewed. Seven now fit on one page.'


def verify(prior, guard):
    storage, review, gameplay, startup = map(base.load, (stage.STORED, stage.MANUSCRIPT, live.OUTPUT, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == storage['candidate_sha256'] == gameplay['candidate_sha256'] == startup['candidate_sha256']
    assert base.digest(parent.ROM) == prior['candidate_sha256'] == storage['previous_sha256'] == review['previous_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256'] == review['clean_sha256']
    assert base.digest(stage.MANUSCRIPT) == storage['manuscript_sha256']
    assert storage['whole_parent_inverse'] and storage['preserved_entries'] == 3660
    assert len(storage['allocations']) == 8
    sheet, = storage['sheets']
    assert Path(sheet['path']) == NATIVE_SHEET and base.digest(NATIVE_SHEET) == sheet['sha256'] == VIEWED_NATIVE
    assert len(sheet['messages']) == 9
    assert base.digest(gameplay['screenshot']) == gameplay['screenshot_sha256'] == VIEWED_GAMEPLAY
    assert (gameplay['parent_pages_observed'], gameplay['revised_pages_observed']) == (2, 1)
    assert len(gameplay['exact_control_frames']) == 12
    assert startup['cold_boot'] and not startup['savestate'] and startup['complete_deployed_payload_exact']
    assert len(startup['exact_matching_frames']) == 6 and len(startup['original_protected_name_getters']) == 24
    for bundle in (gameplay, startup):
        assert all(base.digest(path) == digest for path, digest in bundle['evidence'].items())
    tests, = ElementTree.parse(QA).iter('testsuite')
    assert tuple(int(tests.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')) == (36, 0, 0, 2)
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
    assert len(rows) == 9 and sum(len(row['pages']) for row in rows) == 11
    assert {row['message_id'] for row in rows if len(row['pages']) == 2} == {139, 199}
    prior_review = Path('releases/all_routes_editorial_20261111_trade_good_descriptions_candidate/'
                        'verification/registered_review.json')
    labels = {r['id']: r['commodity_name'] for r in base.load(prior_review)['records']}
    for row in rows:
        row['commodity_menu_label'] = labels[row['id']]
        row['review']['formatting'] = True
        row['registered_reference'] = row['staged_reference'] | dict(exact_stored_hex=row['staged_hex'],
                                                                       candidate_sha256=candidate)
    diagnostics = dict(review_gates=list(stage.GATES), candidate_sha256=candidate, observed_gameplay=gameplay,
        checked_story_format_guard=checked, reviewed_sheet_sha256=VIEWED_NATIVE, direct_visual_review_complete=True,
        menu_label_provenance=dict(path=str(prior_review), sha256=base.digest(prior_review)), new_editorial_credit=0)
    document = review | diagnostics
    precedent.validate_natural_dialogue_batch(document)
    return storage, document


def update_ledger(ledger, release, sha, checkpoint):
    pending = ledger['pending_shared_consumer_checkpoint_20261114']
    assert pending['remaining_total'] == 276 and pending['candidate_sha256'] == release['predecessor']['candidate_sha256']
    assert not set(pending['remaining_legacy_keys']).intersection(stage.REVIEWS)
    pending['candidate_sha256'] = sha
    ledger['current_integrated_candidate'].update(path=str(ROM), sha256=sha, profile=PROFILE, patch=str(PATCH),
        patch_sha256=release['patch_sha256'], manifest=str(MANIFEST), manifest_sha256=release['manifest_sha256'],
        MESFILE_sha256=release['target_COMMON_sha256'], registered_release_verification=str(RELEASE))
    ledger['latest_checkpoint'] = checkpoint
    ledger['price_info_wraps_20261115'] = dict(review=str(REVIEW), release=str(RELEASE),
        revised_existing_keys=sorted(set(stage.REVIEWS) - {199}), retained_existing_keys=[199],
        new_dialogue_credit=0, remaining_mapped_shared_records=276)


def main():
    source = getsource(precedent.main)
    lo = source.index("    doc = '''")
    hi = source.index("    source = source[:doc_lo]", lo)
    doc = '''    doc = \'\'\'    base.replace_checked(DOC, f"""# Market Price Info wraps

The [registered review](../{REVIEW.as_posix()}) revisits all nine Price Info descriptions that used two pages. Seven now fit on one page. Clove retains its plant family, aroma, use in meat dishes, and comparison with pepper and cinnamon. Bananas regains the plant family. Corn keeps the same wording with a complete sentence at the page turn. Jade keeps its existing wording and pagination.

The original native loader and renderer passed nine selections and eleven complete pages. All nine revised pages received visual review. In the [Lisbon replay](../{(VERIFY / "price_info_before_after.png").as_posix()}), Cheese fit on one page and returned to the original list after one advance. The parent displayed two pages. Twelve other frames matched. The replay used the existing copied Lisbon save. Corn and the other revised descriptions received offline checks. Hardware testing remains open.

The startup controls matched six frames and 24 protected getters. Thirty-four targeted tests passed. Two historical tests skipped because their ROM fixtures were unavailable. The [cumulative ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) retain all 114 accepted layers and the ASCII right bound. All nine reviews had existing credit. The ledger stands at 27,700 credited reviews and 276 mapped shared records remaining.
""".encode())\'\'\'
'''
    source = source[:lo] + doc + source[hi:]
    replacements = {
        '== 813 and len(manifest["checks"]) == 148': '== 814 and len(manifest["checks"]) == 149',
        'release_stack.refit_help_wraps.pending.json': 'release_stack.price_info_wraps.pending.json',
        'editorial_review_current.refit_help_wraps.pending.json': 'editorial_review_current.price_info_wraps.pending.json',
        'release_stack_before_refit_help_wraps.json': 'release_stack_before_price_info_wraps.json',
        'NATIVE, \'\n            \'Path(base.load(NATIVE)["review_sheets"][0]["path"])':
            'stage.MANUSCRIPT, \'\n            \'NATIVE_SHEET',
        'verified_name_or_words_confirmation_predecessor=lineage, refit_help_wraps_release':
            'verified_refit_help_wraps_predecessor=lineage, price_info_wraps_release',
        'Source-reviewed Refit help and verified native wrapping.': 'Source-reviewed Market Price Info wraps.',
        'registered_refit_help_wraps_and_complete_parent_inverse': 'registered_price_info_wraps_and_complete_parent_inverse',
        'sorted(stage.REVISIONS)': 'sorted(set(stage.REVIEWS) - {199})',
        'refit_help_wraps_registered_successor_pipeline': 'price_info_wraps_registered_successor_pipeline',
        'registered_manifest_entries=814,passing_release_checks=149,repository_tests=16':
            'registered_manifest_entries=815,passing_release_checks=150,repository_tests=34',
        'prose_revisions=6,justified_retentions=25,text_display_revisions=6':
            'prose_revisions=7,justified_retentions=1,text_display_revisions=8',
        'observed_revised_refit_holds=4,exact_surrounding_holds=11': 'observed_revised_price_info_holds=1,exact_surrounding_holds=12',
        'offline_complete_refit_planes=6': 'offline_complete_price_info_pages=11',
        '# Shipyard Refit Help test candidate': '# Market Price Info Wraps test candidate',
        'includes the revised Shipyard Refit help': 'includes the revised Market Price Info descriptions',
        'Preserve Refit help release and verified replay.': 'Preserve Price Info release and verified replay.',
        '814 entries, 114 accepted layers, 149 checks.': '815 entries, 114 accepted layers, 150 checks.',
    }
    env = vars(precedent) | globals()
    exec(compile(checked_text(source, replacements), __file__ + '::price-info-registration', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
