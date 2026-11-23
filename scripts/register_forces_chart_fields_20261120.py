"""Register the verified Forces chart values in the cumulative candidate."""

from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_forces_chart_gameplay_20261120 as game
from scripts import check_forces_chart_native_20261120 as chart
from scripts import register_amsterdam_tavern_editorial_20261120 as boot
from scripts import register_palace_contract_fee_20261120 as parent
from scripts import stage_forces_chart_fields_20261120 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch, native = parent.base, stage.batch, parent.native
PROFILE = 'all-routes-forces-chart-fields-v1-20261120'
ROOT = Path('out/forces_chart_fields_registered_20261120_v1')
ROM = ROOT / 'Translation_DS_Forces_Chart_Fields_20261120_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261120_forces_chart_fields_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_forces_chart_fields_registered_20261120.md')
STARTUP, QA, VISUAL = (stage.ROOT / name for name in ('own_startup_verification.json', 'qa.xml', 'visual_review.json'))
SHEETS = (chart.SHEET, game.SHEET)
STARTUP_CAPTURE = game.ROOT / 'startup/capture/capture_report.json'
CHECKPOINT = 'Registered English no-home text and regular-width punctuation in the original Forces chart after the paired Lisbon replay.'


def verify(registry, previous, viewed):
    stored, model, played = map(base.load, (stage.PROOF, chart.OUTPUT, game.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == model['candidate_sha256'] == played['candidate_sha256']
    assert stored['parent_sha256'] == played['predecessor_sha256'] == previous['candidate_sha256'] == base.digest(parent.ROM)
    assert stored['clean_input_sha256'] == previous['clean_input_sha256'] == base.digest(batch.CLEAN)
    assert stored['whole_parent_inverse'] and stored['clean_input_patch_byte_exact']
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()
    assert base.digest(stage.ROOT / 'translation.xdelta') == stored['clean_input_patch_sha256']
    assert viewed == {str(p): base.digest(p) for p in SHEETS}
    assert viewed[str(chart.SHEET)] == model['sheet_sha256'] and viewed[str(game.SHEET)] == played['sheet_sha256']
    assert len(model['cases']) == 28 and all(row['full_glyph_plane'] for row in model['cases'])
    assert len({row['field'] for row in played['gameplay']}) == 8
    assert played['same_before_and_after'] == [13000, 14980]
    assert all(base.digest(path) == sha for path, sha in played['evidence'].items())
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [32, 0, 0, 2]

    clean, prior, target = map(batch.NdsImage.open, (batch.CLEAN, parent.ROM, stage.ROM))
    before, after = map(batch.files, (prior, target))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {batch.ARM}
    arm, common = after[batch.ARM], after[batch.COMMON]
    source_arm = clean.read_file(batch.ARM)
    assert stage.patch(before[batch.ARM], source_arm) == (arm, stored['rows'])
    assert batch.digest(arm) == stored['target_ARM9_sha256']
    assert batch.digest(common) == stored['target_COMMON_sha256'] == previous['target_COMMON_sha256']
    target.replace_file(batch.ARM, before[batch.ARM])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(batch.files(clean), after)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    table = batch.owned_entries(common, arm, batch.digest(arm[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET]))
    pending = base.load(parent.parent.PENDING)['records']
    assert len(pending) == 276 and all(batch.reference(table[row['message_ID']]) == row['current_reference']
        and table[row['message_ID']].text.hex() == row['current_hex'] for row in pending)
    for row in played['records']:
        offset, size = row['offset'], row['slot_bytes']
        row['registered_reference'] = dict(candidate_sha256=candidate, offset=offset, slot_bytes=size,
                                           pointer_offset=row['literal_offset'])
        if row['decision'] == 'retention':
            assert source_arm[offset:offset + size].hex() == row['source_hex']
            assert before[batch.ARM][offset:offset + size] == arm[offset:offset + size] == bytes.fromhex(row['current_hex'])
        else:
            assert arm[offset:offset + size] == bytes.fromhex(row['target_hex'])
    verify_start = FunctionType(boot.startup_proof.__code__, boot.startup_proof.__globals__ |
                                {'STARTUP': STARTUP, 'STARTUP_CAPTURE': STARTUP_CAPTURE})
    verify_start(previous, candidate, arm)
    draft = played | dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=batch.GATES, checked_story_format_guard=controls,
        shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'], new_contextual_credit=0)
    validate_natural_dialogue_batch(draft)
    return stored, draft, {batch.ARM: batch.digest(arm)}


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index('    DOC.write_text'):template.index('    prefix =')]
program = checked_text(template, {
    'len(manifest["batches"]) == 939 and len(manifest["checks"]) == 274':
        'len(manifest["batches"]) == 940 and len(manifest["checks"]) == 275',
    'stage.PROOF, STARTUP, QA, game.PROOF, args.visual_review':
        'stage.PROOF, STARTUP, QA, chart.OUTPUT, game.PROOF, args.visual_review',
    'release_stack_before_palace_fee.json': 'release_stack_before_forces_chart.json',
    'release_stack_with_palace_fee.json': 'release_stack_with_forces_chart.json',
    'verified_ruin_discovery_predecessor=predecessor, palace_contract_fee_release=str(REVIEW)':
        'verified_palace_contract_fee_predecessor=predecessor, forces_chart_release=str(REVIEW)',
    'registered_palace_fee_and_complete_parent_inverse': 'registered_forces_chart_and_complete_parent_inverse',
    '    assert all((row["file_path"], row["id"]) in credited for row in draft["records"])\n': '',
    "new_ids = [row['id'] for row in draft['records'] if row['file_path'] == batch.ARM] + [RUNTIME_ID]":
        "new_ids = [row['id'] for row in draft['records'] if row['decision'] == 'revision']",
    'manifest["palace_contract_fee_pipeline"]': 'manifest["forces_chart_fields_pipeline"]',
    'native_display_sha256=base.digest(game.PROOF)': 'native_display_sha256=base.digest(chart.OUTPUT)',
    'owned_contract_digit_calls=stored["native_calls"]': 'owned_chart_slots=stored["rows"]',
    'reviewed_UI_labels=0, new_contextual_records=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=4':
        'reviewed_UI_labels=10, new_contextual_records=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=2',
    'text_display_revisions=2, pagination_fixes=0': 'text_display_revisions=8, pagination_fixes=0',
    'ordinary_Istanbul_payment=True, initialized_insufficient_funds_refusal=True':
        'ordinary_Lisbon_chart_and_unknown_faction=True, initialized_no_home_fallback=True',
    'ledger["palace_contract_fee_20261120"]': 'ledger["forces_chart_fields_20261120"]',
    '''previously_localized_records=4, digit_display_fixes=2, new_contextual_credit=0, prose_revisions=0,
        spacing_revisions=0, wrap_only_revisions=0, justified_retentions=4)
    ledger["palace_fee_digit_finding_20261120"].update(status="verified-fixed-in-both-branches",
        registered_review=str(REVIEW), checked_alternate_quote=1149)''':
        '''ui_labels_reviewed=10, display_revisions=8, new_contextual_credit=0, prose_revisions=0,
        spacing_revisions=0, wrap_only_revisions=0, justified_retentions=2)''',
    'Preserve the Palace contract fee ROM or reconstruction': 'Preserve the Forces chart ROM or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Forces chart fields candidate

The [local ROM](../../{ROM.as_posix()}) displays the English no-home fallback and regular-width punctuation in the Forces chart.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Forces chart field text registered

When a faction has no home, the Forces chart now displays **None**. An unknown home and the other hidden values use the regular question mark. The Power row keeps its original total, region and regional subtotal in order and uses standard punctuation. The leader and unknown-faction captions have individual reasons for retaining their wording. The exact review covers eight revised fields and two retentions. [Registered review](../{REVIEW.as_posix()})

All 28 original native draw cases passed with complete glyphs and safe bounds. The Power cases cover all seven regions and their original numeric limits. The region names come from the existing catalogue, including its extra trailing space after SE Asia. [Native pages](../{(VERIFY / chart.SHEET.name).as_posix()})

The ordinary Lisbon replay showed the player and unknown faction panels. The paired no-home case set only Castor Co.’s original home byte to its no-home value and then restored it. All eight revised fields matched complete glyph masks. The original return to Market matched both screens byte for byte. Six startup holds, 24 protected name getters and 30 focused tests passed. Two optional legacy tests skipped. [Paired gameplay](../{(VERIFY / game.SHEET.name).as_posix()}) · [Candidate and exact clean-input patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register', 'exec'), env)


if __name__ == '__main__':
    env['main']()
