"""Register the source-reviewed, emulator-verified Online caption batch."""

import argparse
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_arrival_month_labels_v1 as prior
from scripts import replay_visible_online_captions_v1 as replay
from scripts import stage_visible_online_captions_v1 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, parent, review = stage.base, stage.parent, stage.review
ARM, COMMON, CLEAN = parent.ARM, parent.COMMON, parent.CLEAN
PROFILE = 'all-routes-visible-online-captions-v1-20261111'
CHECK = 'registered_visible_online_captions_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_visible_online_captions_candidate')
VERIFICATION = PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_caption_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/visible_online_captions_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Online_Captions_20261111_candidate.nds'
MANIFEST, PATCH = ROM.with_suffix('.manifest.json'), PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_visible_online_captions_registered_20261111.md')
REGISTRY_PENDING = base.REGISTRY.with_name('release_stack.visible_online_captions.pending.json')
LEDGER_PENDING = base.LEDGER.with_name('editorial_review_current.visible_online_captions.pending.json')
verification = SimpleNamespace(BOOT=replay.BOOT, LIVE=replay.LIVE,
                               QA=Path('work/visible_online_captions_repo_qa_20261111.xml'))

GLOSSES = (
    'The goal is a world not found on the map.',
    'Human drama involving many different people.',
    'Players are free to choose how they play.',
    'Take royal orders and embark on further adventures.',
    'Live as a sailor with the whole world as the setting.',
    'Sail beyond the sea and make a name for yourself.',
    'Earn money by buying and selling a variety of trade goods.',
    'Heated battles unfold at sea.',
    'The story changes greatly with the nation you belong to.',
    'Changes bring an excitement unlike anything before.',
    'Set off on an adventure with companions you have met.',
    'Race across the open sea in your own ship.',
    'A grand, thrilling world of adventure.',
)


def bind_records(proof, live):
    source = base.load(review.OUTPUT)
    assert base.digest(review.OUTPUT) == proof['manuscript_sha256']
    assert source['current_ROM_sha256'] == proof['parent_sha256']
    assert base.digest(review.CONSUMERS) == source['observer_report_sha256']
    assert base.digest(stage.SHEET) == proof['sheet_sha256']
    assert proof['sheet_sha256'] == 'aa738e47ae0fd64e8cb969b066015b731ce902012e18b358b507b2e238c98095'
    mask = {row['id']: row for row in proof['all_native_caption_masks']}
    observations = {row['id']: row for row in live['all_observed_caption_masks']}
    rows = []
    for row, gloss in zip(source['records'], GLOSSES, strict=True):
        n = row['id']
        assert mask[n]['complete_leading_internal_and_final_glyphs']
        assert observations[n]['bounds'][0] == mask[n]['original_center']
        assert (observations[n]['changed_rectangle'] is not None) == (row['decision'] == 'revision')
        field = row['current_reference']
        target = row['english'].encode('ascii').ljust(len(bytes.fromhex(field['stored_hex'])), b'\0')
        rows.append(row | dict(source_meaning=gloss, new_dialogue_credit=0,
            review=row['review'] | {'formatting': True}, offline_native=mask[n], actual_gameplay=observations[n],
            registered_reference=dict(offset=field['offset'], pointer=field['pointer'], stored_hex=target.hex(),
                                      candidate_sha256=proof['candidate_sha256'])))
    assert len(rows) == 13
    return rows


def batch(records, scope, sha):
    result = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        records=records, actual_verification_scope=scope, current_ROM_sha256=sha,
        reviewed_visible_captions=13, prose_revisions=4, justified_retentions=9)
    validate_natural_dialogue_batch(result)
    return result


def register():
    changes = {
        "proof['research_ROM_sha256']": "proof['candidate_sha256']",
        "proof['parent_inverse_exact']": "proof['complete_parent_inverse']",
        "    assert len(live['observed_changes']) == 12 and len(live['whole_frame_equal']) == 28\n"
        "    assert live['calendars_and_other_pixels_unchanged'] and live['repository_tests'] == 34":
            "    assert len(live['all_observed_caption_masks']) == 13 and len(live['changed_caption_frames']) == 4\n"
            "    assert live['original_navigation_and_return_frames_exact'] and live['graphic_artwork_unchanged']\n"
            "    suites = list(ElementTree.parse(verification.QA).iter('testsuite'))\n"
            "    assert sum(int(row.get('tests', 0)) for row in suites) == 34\n"
            "    assert not any(int(row.get(k, 0)) for row in suites for k in ('errors', 'failures', 'skipped'))",
        '== 27597': '== 27696',
        "== 774 and len(manifest['checks']) == 109": "== 778 and len(manifest['checks']) == 113",
        "== 775 and len(manifest['checks']) == 110": "== 779 and len(manifest['checks']) == 114",
        "    arm, records = stage.transform(original, base.NdsImage.open(CLEAN).read_file(ARM))\n"
        "    assert records == proof['records'] and digest(arm) == proof['research_ARM9_sha256']":
            "    records = bind_records(proof, live)\n"
            "    arm, slots = stage.transform(original, base.NdsImage.open(CLEAN).read_file(ARM), records)\n"
            "    assert slots == proof['slots'] and digest(arm) == proof['target_ARM9_sha256']",
        "proof['research_COMMON_sha256']": "proof['unchanged_original_COMMON_sha256']",
        'verification.LIVE, verification.QA):': 'verification.LIVE, verification.QA, review.CONSUMERS):',
        "    scope = dict(actual_emulator=True, hardware=False, Trade_holds=11, Golden_Route_Found_holds=1,\n"
        "        other_whole_frames_exact=28, original_calendar_and_Guild_return_exact=True,\n"
        "        fixture_scope='One temporary purchase-cost word to reach the original Golden Route screen.')":
            "    scope = dict(actual_emulator=True, hardware=False, observed_native_captions=13,\n"
            "        revised_caption_holds=4, original_navigation_and_return_frames_exact=True,\n"
            "        other_whole_frames_exact=len(live['other_whole_frame_matches']), fixture=False)",
        "    base.save(REVIEW, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',\n"
        "        records=[row | dict(review=dict.fromkeys(('source', 'context', 'localization', 'naturalness', 'formatting'), True),\n"
        "                            new_dialogue_credit=0) for row in records],\n"
        "        actual_verification_scope=scope, current_ROM_sha256=sha))": "    base.save(REVIEW, batch(records, scope, sha))",
        'release_stack_before_arrival_month_labels.json': 'release_stack_before_visible_online_captions.json',
        'verified_golden_route_exchanges_predecessor': 'verified_ancient_map_hint_label_predecessor',
        'arrival_month_labels_release': 'visible_online_captions_release',
        'Terminated the original Trade and Golden Route arrival-month labels in their owned slots.':
            'Reviewed the original ARM9 captions for all four Online guide categories.',
        "extend(row['id'] for row in records)": "extend(row['id'] for row in slots if row['id'] not in manifest['changed_records'][ARM])",
        "['arrival_month_labels'] = records": "['visible_online_captions'] = slots",
        'arrival_month_labels_registered_successor_pipeline': 'visible_online_captions_registered_successor_pipeline',
        'registered_manifest_entries=775, passing_release_checks=110':
            'registered_manifest_entries=779, passing_release_checks=114',
        'reviewed_UI_labels=2': 'reviewed_UI_labels=13',
        'The two arrival-month label corrections are registered.': 'The original Online guide captions are registered.',
        'arrival_month_labels_20261111': 'visible_online_captions_20261111',
        'Staged the exact cumulative arrival-month release for publication.':
            'Staged the exact cumulative Online captions release for publication.',
    }
    source = checked_text(getsource(prior.register), changes)
    environment = vars(prior) | globals()
    exec(compile(source, __file__ + '::register-reviewed-online-captions', 'exec'), environment)
    environment['register']()


def publish_prepared():
    changes = {
        'Preserve the arrival-month build.': 'Preserve the Online caption build.',
        '# Arrival-month labels candidate': '# All Routes Online Captions candidate',
        'Trade shows “Arr.” and Golden Route Found shows “Arrival.” Both labels terminate before the following string in ARM9. '
        'The 40-frame Lisbon comparison found 12 label-only differences and 28 exact frames. Both complete glyph masks, the month grids, '
        'the Guild return, cold boot, 24 protected getters, 34 targeted tests and 110 release checks passed.':
            'All 13 Online captions received contextual review. Four revisions and nine retentions passed the original native painter '
            'and gameplay navigation. Four frames changed only within the caption ink. Cold boot, 24 protected getters, '
            '34 targeted tests and 114 release checks passed.',
        '''    document = """# Arrival-month labels registered''': '''    document = """# Visible Online captions registered''',
        'The Trade and Golden Route Found calendars now display complete terminated labels. The eight-byte fields at '
        '\x600215A000\x60 and \x600216AFB0\x60 hold “Arr.” and “Arrival.” The original callers and the strings that follow both slots are byte-exact. '
        'The replay verified the new labels and preserved all other screen pixels in the 40 sampled frames.':
            'All 13 original Online guide captions now have exact clean, previous and registered references and all five review gates. '
            'Four caption slots changed. The original renderer, centering, navigation and artwork are preserved. '
            'The actual emulator replay matched all complete glyph masks.',
        'releases/all_routes_editorial_20261111_arrival_month_labels_candidate/README.md':
            'releases/all_routes_editorial_20261111_visible_online_captions_candidate/README.md',
        'The dialogue ledger remains at 27,597 reviews, with 379 native shared keys to review or classify. '
        'Continue with the [Ancient Map manuscript](../translations/editorial_checkpoints/SharedText_20261110_v1/treasure_map_documents_context_v1.json). '
        'It records 51 contextual decisions and the 20 original region and direction pairs. '
        'The native document layout and representative replay are pending.':
            'The dialogue ledger remains at 27,696 reviews, with 280 native shared keys to review or classify. '
            'The [consumer evidence](../translations/editorial_checkpoints/SharedText_20261110_v1/online_and_gallery_observed_consumers_v1.json) '
            'binds all 13 Online pages and 12 representative Gallery scenes to independent caption owners. '
            'The broader COMMON consumer classification and visible UI review remain active.',
        'The two arrival-month labels are registered.': 'The 13 visible Online captions are registered.',
        'Registered 775 entries, 114 accepted layers and 110 checks. Dialogue credit remains 27,597.':
            'Registered 779 entries, 114 accepted layers and 114 checks. Dialogue credit remains 27,696.',
    }
    source = checked_text(getsource(prior.publish_prepared), changes)
    environment = vars(prior) | globals()
    exec(compile(source, __file__ + '::publish-reviewed-online-captions', 'exec'), environment)
    environment['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--register', action='store_true')
    group.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
