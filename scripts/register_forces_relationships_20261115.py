"""Publish the verified Forces relationship labels and cumulative clean-input patch."""

from hashlib import sha256
from inspect import getsource
from pathlib import Path
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_developed_port_menu_20261115 as workflow
from scripts import stage_forces_relationships_20261115 as stage
from scripts import verify_forces_relationships_20261115 as live
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_release_baseline import files


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-forces-relationships-v1-20261115'
CHECK = 'registered_forces_relationship_slots_and_complete_parent_inverse'
ROOT = Path('out/forces_relationships_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Forces_Relationships_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_forces_relationships_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_forces_relationships_20261115.md')
STARTUP, QA = (stage.ROOT / name for name in ('own_startup_verification.json', 'repository_qa.xml'))
CHECKPOINT = 'Allied, At War and Subordinate relationship lines are localized in the Forces chart.'


def verify(prior, guard):
    staged, boot, game = map(base.load, (stage.STORED, STARTUP, live.OUTPUT))
    sha = base.digest(stage.ROM)
    assert sha == staged['candidate_sha256'] == boot['candidate_sha256'] == game['candidate_sha256']
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert all(base.digest(path) == digest for block in (boot, game) for path, digest in block['evidence'].items())
    assert game['original_return_to_market_menu'] == 16400 and game['fixtures_only_relationship_model_bytes']
    assert len(game['exact_control_frames']) == 4 and len(game['actual_relationship_frames']) == 3
    assert tuple(row['format_id'] for row in game['actual_relationship_frames']) == tuple(row.id for row in stage.LABELS)
    assert len(game['native_name_matrix']) == 12
    assert all(r['exact_complete_native_plane'] and r['unchanged_header_and_adjacent_guards']
               and r['original_C_format_and_renderer'] for r in game['native_name_matrix'])
    assert base.digest(live.SHEET) == game['sheet_sha256']
    assert base.digest(live.NATIVE_SHEET) == game['name_matrix_sheet_sha256']
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [15, 0, 0, 0]
    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(files, (old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {stage.ARM}
    arm, slots = stage.apply(clean.read_file(stage.ARM), before[stage.ARM])
    assert arm == after[stage.ARM] and slots == staged['changed_slots']
    assert sha256(arm).hexdigest() == staged['target_ARM9_sha256']
    assert sha256(after['/COMMON/MESFILE.DK4']).hexdigest() == prior['target_COMMON_sha256']
    verify_runtime(arm, prior)
    checked = bind_registered_story_percent_guard(guard)(files(clean), after)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    new.replace_file(stage.ARM, before[stage.ARM])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    rows = []
    for label, slot in zip(stage.LABELS, slots, strict=True):
        rows.append(dict(id=label.id, file_path=stage.ARM, speaker='Forces chart',
            source_Japanese=label.japanese, source_meaning=label.meaning, english=label.english,
            context='Relationship below the Ties field for the currently selected opposing faction.',
            localization_note=label.reason, decision='revision',
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=True),
            source_reference=dict(offset=label.offset, capacity=label.size, source_hex=slot['clean_hex']),
            current_reference=dict(offset=label.offset, pointer_field=label.pointer, previous_hex=slot['previous_hex']),
            registered_reference=dict(offset=label.offset, target_hex=slot['target_hex'], candidate_sha256=sha),
            controls=dict(original_relationship_selector_preserved=True, original_right_alignment_preserved=True,
                          runtime_substitutions=['%s'], color_preserved=True, native_pages=1)))
    review = dict(translation_policy='natural-dialogue-v2', encoder='dialogue-relocatable-v1', target_locale='en-US',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        storage_transform='three fixed ARM9 C-string slots', candidate_sha256=sha, records=rows,
        actual=game, checked_story_format_guard=checked, prior_ledger_credit_change=0)
    validate_natural_dialogue_batch(review)
    return staged, review


def main():
    original = getsource(workflow.main)
    lo = original.index('    base.replace_checked(DOC, f"""')
    hi = original.index('""".encode())', lo) + len('""".encode())')
    note = '''    base.replace_checked(DOC, f"""# Forces chart relationship lines

The original chart adds a relationship line below Ties when the selected faction is allied, at war or subordinate. All three lines mixed the English company name with Japanese text. They now read **Allied with %s**, **At war with %s** and **Subject to %s**. Each keeps its original name substitution, color, right alignment and fixed slot. [Exact review](../{REVIEW.as_posix()})

The original controller replay selected the faction next to Castor Co. in the Lisbon chart. A two-byte relationship fixture let the same inputs exercise all three conditions on the old and new builds, then restored the neutral state. All three complete glyph masks match the independent native font. Everything outside the relationship line matches, and four full control frames match, including neutral and the return to the Market menu. The relationships were supplied for display testing. [Gameplay comparison](../{(VERIFY / live.SHEET.name).as_posix()})

Twelve distinct native format-and-render checks preserve the complete inserted names, including FIONA, a name with a literal percent sign, and an 18-byte company name. Those checks used the original formatter and painter with a supplied bitmap. A separate boot matched six startup frames and 24 protected name getters. All 15 focused tests passed. [Name checks](../{(VERIFY / live.NATIVE_SHEET.name).as_posix()})

The [registered ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve 114 accepted layers and 159 passing checks. The ledger credits 27,700 reviews with 276 mapped shared records open. The independent ARM9 friendship drawer and hardware remain open.
""".encode())'''
    changes = {
        original[lo:hi]: note,
        "len(manifest['batches']) == 821 and len(manifest['checks']) == 156":
            "len(manifest['batches']) == 823 and len(manifest['checks']) == 158",
        'registered_manifest_entries=822, passing_release_checks=157':
            'registered_manifest_entries=824, passing_release_checks=159',
        'release_stack.developed_port_menu.pending.json': 'release_stack.forces_relationships.pending.json',
        'editorial_review_current.developed_port_menu.pending.json': 'editorial_review_current.forces_relationships.pending.json',
        'release_stack_before_developed_port_menu.json': 'release_stack_before_forces_relationships.json',
        'verified_barmaid_town_labels_predecessor=predecessor, developed_port_menu_release=str(REVIEW)':
            'verified_market_info_trends_predecessor=predecessor, forces_relationships_release=str(REVIEW)',
        "manifest['developed_port_menu_pipeline']": "manifest['forces_relationships_pipeline']",
        "manifest['changed_records'][stage.ARM].append(stage.RECORD)":
            "manifest['changed_records'][stage.ARM].extend(row.id for row in stage.LABELS)",
        "owned_ARM9_field=staged['changed_slot']": "owned_ARM9_fields=staged['changed_slots']",
        "ledger['developed_port_menu_20261115']": "ledger['forces_relationships_20261115']",
        'record=stage.RECORD': 'records=[row.id for row in stage.LABELS]',
        'text_display_revisions=1': 'text_display_revisions=3',
        'reviewed_UI_labels=1': 'reviewed_UI_labels=3',
        'developed_Narvik_Port=True': 'Forces_chart_relationships=True',
        'location_fixture_only=True': 'isolated_relationship_fixture=True',
        '# Developed Port Menu test candidate': '# Forces Relationships test candidate',
        'shows Back to Town in the developed Port menu': 'localizes all three Forces relationship lines',
        'Preserve developed Port menu candidate': 'Preserve Forces Relationships candidate',
        '(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, QA)': '(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, live.NATIVE_SHEET, QA)',
        '822 entries, 114 accepted layers and 157 passing checks':
            '824 entries, 114 accepted layers and 159 passing checks',
    }
    env = vars(workflow) | globals()
    exec(compile(checked_text(original, changes), __file__ + '::registered-fixed-ARM9-slots', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
