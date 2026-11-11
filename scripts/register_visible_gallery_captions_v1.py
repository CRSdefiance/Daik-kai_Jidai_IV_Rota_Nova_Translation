"""Register 164 Gallery caption decisions and the verified COMMON 336 retention."""

import argparse
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.gallery_caption_bounds import validate
from scripts import register_arrival_month_labels_v1 as prior
from scripts import register_diplomatic_outcomes_v2 as ledger_base
from scripts import replay_visible_gallery_captions_v1 as startup
from scripts import replay_visible_gallery_captions_v2 as live_replay
from scripts import review_common_336_levelup_v1 as stats
from scripts import stage_visible_gallery_captions_v1 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, parent, review = stage.base, stage.parent, stage.review
ARM, COMMON, CLEAN = parent.ARM, parent.COMMON, parent.CLEAN
PROFILE = 'all-routes-visible-gallery-captions-v1-20261111'
CHECK = 'registered_visible_gallery_captions_levelup_retention_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_visible_gallery_captions_candidate')
VERIFICATION = PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_caption_review.json'
STAT_REVIEW = VERIFICATION / 'registered_levelup_stat_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/visible_gallery_captions_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Gallery_Captions_20261111_candidate.nds'
MANIFEST, PATCH = ROM.with_suffix('.manifest.json'), PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_visible_gallery_captions_registered_20261111.md')
REGISTRY_PENDING = base.REGISTRY.with_name('release_stack.visible_gallery_captions.pending.json')
LEDGER_PENDING = base.LEDGER.with_name('editorial_review_current.visible_gallery_captions.pending.json')
verification = SimpleNamespace(BOOT=startup.BOOT, LIVE=live_replay.LIVE,
                               QA=Path('work/visible_gallery_captions_repo_qa_20261111.xml'))
GATES = ['source', 'context', 'localization', 'naturalness', 'formatting']


def bind_records(proof, live, target):
    draft = base.load(review.OUTPUT)
    assert base.digest(review.OUTPUT) == proof['manuscript_sha256']
    assert draft['current_ROM_sha256'] == proof['parent_sha256']
    assert all(base.digest(path) == sha for path, sha in draft['historical_scene_evidence'].items())
    assert base.digest(stage.SHEET) == proof['sheet_sha256']
    assert proof['sheet_sha256'] == '4fd68acbb799c08c85a5b4accb6a232241842f34e08b5766c3ac9428d79a93db'
    masks = {row['id']: row for row in proof['all_native_caption_masks']}
    selected = {row['id']: row for row in live['selected_captions']}
    final = {row['field']: row for row in validate(target)}
    records = []
    for row in draft['records']:
        n = row['id']
        assert masks[n]['all_glyph_positions_exact']
        field = row['current_reference']['field']
        assert final[field]['English'] == row['english']
        records.append(row | dict(new_dialogue_credit=0, review=row['review'] | {'formatting': True},
            offline_native=masks[n], actual_gameplay=selected.get(n),
            registered_reference=dict(field=field, pointer=final[field]['pointer'],
                stored_hex=(row['english'].encode('ascii')+b'\0').hex(), candidate_sha256=proof['candidate_sha256'])))
    assert len(records) == len(masks) == len(final) == 164
    return records


def batch(records, scope, sha):
    result = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=GATES, records=records, actual_verification_scope=scope, current_ROM_sha256=sha,
        reviewed_visible_captions=164, prose_revisions=13, justified_retentions=151)
    validate_natural_dialogue_batch(result)
    return result


def seal_stat(ledger, release, scope, original, target, common):
    row = base.load(stats.OUTPUT)
    assert row['current_ROM_sha256'] == release['predecessor']['candidate_sha256']
    spans = ((0x7E2E8, 0x7E5C4), (0x7EED8, 0x7EF00), (0xABF50, 0xABFCC), (0xD7720, 0xD7754))
    assert all(original[lo:hi] == target[lo:hi] for lo, hi in spans)
    assert prior.digest(common) == release['target_COMMON_sha256']
    active = stats.owned_entries(common, target, prior.digest(target[stats.DIRECTORY_OFFSET:stats.TABLE_OFFSET]))[336]
    assert stats.reference(active) == row['current_reference'] and active.text == b'%s increased by %s!'
    verified = row | dict(registered_reference=stats.reference(active) | {'candidate_sha256': release['candidate_sha256']},
        registration_pending=False, new_editorial_credit=1)
    review_batch = dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=GATES, records=[verified])
    validate_natural_dialogue_batch(review_batch)
    base.save(STAT_REVIEW, review_batch)
    source = checked_text(getsource(ledger_base.update_ledger), {
        'diplomatic-and-scheme-outcome-notices': 'native-levelup-stat-increase',
        'Thirty-four diplomacy and scheme outcomes are registered.': 'Gallery captions and COMMON 336 are registered.',
        '== 25985': '== 27697', '== 15438': '== 16591', '== 10547': '== 11106',
    })
    env = vars(ledger_base) | globals() | dict(REVIEW=STAT_REVIEW, TOTAL=1, REVISED=0, RETAINED=1,
        PREVIOUS_TOTAL=27696, FAMILY='levelup_stat_notice_336_contextual_20261111', digest=base.digest,
        LIVE_VERIFICATION=STAT_REVIEW)
    exec(compile(source, __file__ + '::one-new-COMMON-retention', 'exec'), env)
    stat_scope = dict(offline_native_current=True, historical_ordinary_and_maximum_gameplay=verified['earlier_ordinary_and_maximum_gameplay'],
                      new_gameplay=False, hardware=False)
    env['update_ledger'](ledger, [verified], release, stat_scope)
    ledger['visible_gallery_captions_20261111'] = dict(review=str(REVIEW), release=str(RELEASE),
        new_dialogue_credit=0, reviewed_visible_captions=164, actual_verification_scope=scope)


def register():
    ledger_start = "    ledger['current_integrated_candidate'].update(path=str(ROM), sha256=sha, profile=PROFILE,"
    ledger_end = "    LEDGER_PENDING.write_bytes(encode_ledger(ledger))"
    template = getsource(prior.register)
    ledger_block = template[template.index(ledger_start):template.index(ledger_end)]
    changes = {
        "proof['research_ROM_sha256']": "proof['candidate_sha256']",
        "proof['parent_inverse_exact']": "proof['complete_parent_inverse']",
        "    assert len(live['observed_changes']) == 12 and len(live['whole_frame_equal']) == 28\n"
        "    assert live['calendars_and_other_pixels_unchanged'] and live['repository_tests'] == 34":
            "    assert len(live['selected_captions']) == 18 and len(live['observed_revision_ids']) == 7\n"
            "    assert live['original_arrows_and_navigation_preserved'] and live['all_image_and_noncaption_pixels_exact']\n"
            "    suites = list(ElementTree.parse(verification.QA).iter('testsuite'))\n"
            "    assert sum(int(row.get('tests', 0)) for row in suites) == 34\n"
            "    assert not any(int(row.get(k, 0)) for row in suites for k in ('errors', 'failures', 'skipped'))",
        '== 27597': '== 27696',
        "== 774 and len(manifest['checks']) == 109": "== 779 and len(manifest['checks']) == 114",
        "== 775 and len(manifest['checks']) == 110": "== 780 and len(manifest['checks']) == 115",
        "    arm, records = stage.transform(original, base.NdsImage.open(CLEAN).read_file(ARM))\n"
        "    assert records == proof['records'] and digest(arm) == proof['research_ARM9_sha256']":
            "    arm, storage = stage.transform(original, base.load(review.OUTPUT)['records'])\n"
            "    assert loads(dumps(storage)) == proof['storage'] and digest(arm) == proof['target_ARM9_sha256']\n"
            "    records = bind_records(proof, live, arm)",
        "proof['research_COMMON_sha256']": "proof['unchanged_original_COMMON_sha256']",
        "    scope = dict(actual_emulator=True, hardware=False, Trade_holds=11, Golden_Route_Found_holds=1,\n"
        "        other_whole_frames_exact=28, original_calendar_and_Guild_return_exact=True,\n"
        "        fixture_scope='One temporary purchase-cost word to reach the original Golden Route screen.')":
            "    scope = dict(actual_emulator=True, hardware=False, stored_and_native_captions=164,\n"
            "        revised_caption_holds=7, original_arrows_and_navigation_preserved=True,\n"
            "        isolated_Gallery_unlock_battery=True, earned_Gallery_unlock=False)",
        "    base.save(REVIEW, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',\n"
        "        records=[row | dict(review=dict.fromkeys(('source', 'context', 'localization', 'naturalness', 'formatting'), True),\n"
        "                            new_dialogue_credit=0) for row in records],\n"
        "        actual_verification_scope=scope, current_ROM_sha256=sha))": "    base.save(REVIEW, batch(records, scope, sha))",
        'release_stack_before_arrival_month_labels.json': 'release_stack_before_visible_gallery_captions.json',
        'verified_golden_route_exchanges_predecessor': 'verified_visible_online_captions_predecessor',
        'arrival_month_labels_release': 'visible_gallery_captions_release',
        'Terminated the original Trade and Golden Route arrival-month labels in their owned slots.':
            'Contextual review of the original Gallery event captions and COMMON 336 retention.',
        "    manifest['changed_records'][ARM].extend(row['id'] for row in records)":
            "    manifest['changed_records'][ARM].extend(row['id'] for row in records\n"
            "        if row['decision'] == 'revision' and row['id'] not in manifest['changed_records'][ARM])",
        "['arrival_month_labels'] = records": "['visible_gallery_captions'] = storage",
        'arrival_month_labels_registered_successor_pipeline': 'visible_gallery_captions_registered_successor_pipeline',
        'registered_manifest_entries=775, passing_release_checks=110':
            'registered_manifest_entries=780, passing_release_checks=115',
        'new_contextual_records=0, prose_revisions=0, justified_retentions=0, reviewed_UI_labels=2':
            'new_contextual_records=1, prose_revisions=0, justified_retentions=1, reviewed_UI_labels=164',
        ledger_block: "    seal_stat(ledger, release, scope, original, arm, parent_image.read_file(COMMON))\n",
        'Staged the exact cumulative arrival-month release for publication.':
            'Staged the Gallery caption and level-up retention release for publication.',
    }
    source = checked_text(template, changes)
    env = vars(prior) | globals()
    exec(compile(source, __file__ + '::register-Gallery-and-stat-review', 'exec'), env)
    env['register']()


def publish_prepared():
    changes = {
        'Preserve the arrival-month build.': 'Preserve the Gallery caption build.',
        '# Arrival-month labels candidate': '# All Routes Gallery Captions candidate',
        'Trade shows “Arr.” and Golden Route Found shows “Arrival.” Both labels terminate before the following string in ARM9. '
        'The 40-frame Lisbon comparison found 12 label-only differences and 28 exact frames. Both complete glyph masks, the month grids, '
        'the Guild return, cold boot, 24 protected getters, 34 targeted tests and 110 release checks passed.':
            'All 164 Gallery event captions received contextual review. Thirteen revisions and 151 retentions passed '
            'native font and bounds checks. The four route carousels rendered seven of the revisions in focused gameplay. '
            'The original COMMON 336 notice is a newly credited retention with verified stat names, numbers and pagination. '
            'Cold boot, 24 protected getters, 34 targeted tests and 115 release checks passed.',
        '''    document = """# Arrival-month labels registered''': '''    document = """# Visible Gallery captions registered''',
        'The Trade and Golden Route Found calendars now display complete terminated labels. The eight-byte fields at '
        '\x600215A000\x60 and \x600216AFB0\x60 hold “Arr.” and “Arrival.” The original callers and the strings that follow both slots are byte-exact. '
        'The replay verified the new labels and preserved all other screen pixels in the 40 sampled frames.':
            'All 164 original event captions received a contextual reread. Thirteen changed and 151 were retained with reasons. '
            'Every complete native mask fits within the arrow-safe window. Seven revised titles, original photos, arrows and menu returns '
            'passed focused emulator navigation. The borrowed unlock save provides access to the Gallery.',
        'releases/all_routes_editorial_20261111_arrival_month_labels_candidate/README.md':
            'releases/all_routes_editorial_20261111_visible_gallery_captions_candidate/README.md',
        'The dialogue ledger remains at 27,597 reviews, with 379 native shared keys to review or classify. '
        'Continue with the [Ancient Map manuscript](../translations/editorial_checkpoints/SharedText_20261110_v1/treasure_map_documents_context_v1.json). '
        'It records 51 contextual decisions and the 20 original region and direction pairs. '
        'The native document layout and representative replay are pending.':
            'The [stat result review](../releases/all_routes_editorial_20261111_visible_gallery_captions_candidate/verification/registered_levelup_stat_review.json) '
            'credits COMMON 336 once as a justified retention. The original game supplies the stat first and the gain second. '
            'The current native renderer verified one, two and six rows. The maximum case uses a four-row page followed by two rows. '
            'Earlier ordinary and maximum-growth gameplay evidence is linked in the review. The dialogue ledger now credits '
            '27,697 reviews, with 279 native shared keys left to review or classify.',
        'The two arrival-month labels are registered.': 'Gallery captions and the COMMON 336 stat increase review are registered.',
        'Registered 775 entries, 114 accepted layers and 110 checks. Dialogue credit remains 27,597.':
            'Registered 780 entries, 114 accepted layers and 115 checks. Dialogue credit is 27,697.',
    }
    source = checked_text(getsource(prior.publish_prepared), changes)
    env = vars(prior) | globals()
    exec(compile(source, __file__ + '::publish-Gallery-release', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--register', action='store_true')
    group.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
