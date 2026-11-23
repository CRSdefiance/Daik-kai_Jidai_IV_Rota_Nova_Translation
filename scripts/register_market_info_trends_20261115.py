"""Register the verified Market Info trend heading as a cumulative release."""

from hashlib import sha256
from inspect import getsource
from pathlib import Path
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import stage_market_info_trends_20261115 as stage
from scripts import verify_market_info_trends_20261115 as live
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_release_baseline import files


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-market-info-trends-v1-20261115'
CHECK = 'registered_market_info_trends_slot_and_complete_parent_inverse'
ROOT = Path('out/market_info_trends_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Market_Info_Trends_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_market_info_trends_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_market_info_trends_20261115.md')
STARTUP, QA = (stage.ROOT / name for name in ('own_startup_verification.json', 'repository_qa.xml'))
CHECKPOINT = 'Lisbon Market Info displays “Trends” when the local report has an active trend.'


def verify(prior, guard):
    staged, boot, gameplay = map(base.load, (stage.STORED, STARTUP, live.OUTPUT))
    sha = base.digest(stage.ROM)
    assert sha == staged['candidate_sha256'] == boot['candidate_sha256'] == gameplay['candidate_sha256']
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert all(base.digest(path) == digest for bundle in (boot, gameplay) for path, digest in bundle['evidence'].items())
    assert gameplay['active_trend_actual_gameplay'] and gameplay['no_trend_frame_pixel_identical']
    assert gameplay['complete_glyph_pixels'] == 74 and gameplay['complete_blank_and_shadow_checks']
    assert gameplay['B_return_to_chart_frame'] == 13000 and gameplay['complete_Forces_footer_pixels'] == 67
    assert base.digest(live.SHEET) == gameplay['sheet_sha256']
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [15, 0, 0, 0]
    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(files, (old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {stage.ARM}
    arm, field = stage.apply(clean.read_file(stage.ARM), before[stage.ARM])
    assert arm == after[stage.ARM] and field == staged['changed_slot']
    assert sha256(arm).hexdigest() == staged['target_ARM9_sha256']
    assert sha256(after['/COMMON/MESFILE.DK4']).hexdigest() == prior['target_COMMON_sha256']
    verify_runtime(arm, prior)
    checked = bind_registered_story_percent_guard(guard)(files(clean), after)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    new.replace_file(stage.ARM, before[stage.ARM])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    review = dict(translation_policy='natural-dialogue-v2', encoder='dialogue-relocatable-v1', target_locale='en-US',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        storage_transform='fixed ARM9 C-string slot', candidate_sha256=sha,
        records=[dict(id=stage.RECORD, file_path=stage.ARM, source_Japanese=stage.JAPANESE,
            speaker='Market Info report', source_meaning='A heading for locally popular trade goods.',
            context='Above the original Market Info trend tag. Only visible when the report has an active trend.',
            previous_display=stage.JAPANESE, english=stage.ENGLISH, decision='revision',
            localization_note='Trends matches the Square command for trade trends and fits the full existing heading.',
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=True),
            source_reference=dict(offset=stage.OFFSET, capacity=stage.SLOT, source_hex=field['clean_hex']),
            current_reference=dict(offset=stage.OFFSET, pointer_field=stage.POINTER, previous_hex=field['previous_hex']),
            registered_reference=dict(offset=stage.OFFSET, target_hex=field['target_hex'], candidate_sha256=sha),
            controls=dict(pointer_preserved=True, native_activation_preserved=True, runtime_substitutions=0,
                          native_pages=1, allocation=stage.SLOT))],
        actual=gameplay, checked_story_format_guard=checked, prior_ledger_credit_change=0)
    validate_natural_dialogue_batch(review)
    return staged, review


def main():
    original = getsource(parent.main)
    lo = original.index('    base.replace_checked(DOC, f"""')
    hi = original.index('""".encode())', lo) + len('""".encode())')
    note = '''    base.replace_checked(DOC, f"""# Market Info trend heading

Lisbon’s Market Info report displayed 流行品 when a local trend was active. The term identifies goods that are popular in that market. The heading now reads **Trends**, matching the established Square command. The original eight-byte ARM9 slot, pointer and display condition are preserved. [Exact review](../{REVIEW.as_posix()})

Before and after cold boots used the same inputs and copied Lisbon save. The active-trend cases supplied one two-byte municipal trend record for Olive Oil. The revised heading matches all 74 English font pixels and clears the old mixed foreground and shadow. Everything outside the heading and the full ordinary report without a trend match exactly. Pressing B returns to the route chart. A separate cold boot matched six startup frames and 24 protected name getters. All 15 focused tests passed. [Comparison](../{(VERIFY / live.SHEET.name).as_posix()})

The [registered ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers and 158 passing release checks. The ledger credits 27,700 reviews, with 276 mapped shared records open. The original acquisition of a trend and hardware remain untested.
""".encode())'''
    changes = {
        original[lo:hi]: note,
        "len(manifest['batches']) == 821 and len(manifest['checks']) == 156":
            "len(manifest['batches']) == 822 and len(manifest['checks']) == 157",
        'registered_manifest_entries=822, passing_release_checks=157':
            'registered_manifest_entries=823, passing_release_checks=158',
        'release_stack.developed_port_menu.pending.json': 'release_stack.market_info_trends.pending.json',
        'editorial_review_current.developed_port_menu.pending.json': 'editorial_review_current.market_info_trends.pending.json',
        'release_stack_before_developed_port_menu.json': 'release_stack_before_market_info_trends.json',
        'verified_barmaid_town_labels_predecessor=predecessor, developed_port_menu_release=str(REVIEW)':
            'verified_developed_port_menu_predecessor=predecessor, market_info_trends_release=str(REVIEW)',
        "manifest['developed_port_menu_pipeline']": "manifest['market_info_trends_pipeline']",
        "ledger['developed_port_menu_20261115']": "ledger['market_info_trends_20261115']",
        'developed_Narvik_Port=True': 'Market_Info_trend=True',
        'location_fixture_only=True': 'two_byte_municipal_trend_fixture=True',
        '# Developed Port Menu test candidate': '# Market Info Trends test candidate',
        'shows Back to Town in the developed Port menu': 'localizes the Trends heading in Market Info',
        'Preserve developed Port menu candidate': 'Preserve Market Info Trends candidate',
        '822 entries, 114 accepted layers and 157 passing checks':
            '823 entries, 114 accepted layers and 158 passing checks',
    }
    env = vars(parent) | globals()
    exec(compile(checked_text(original, changes), __file__ + '::registered-fixed-ARM9-slot', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
