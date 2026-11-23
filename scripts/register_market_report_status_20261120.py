"""Register the repaired Market Info atlas and route chart punctuation."""

from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_market_report_status_20261120 as game
from scripts import register_amsterdam_tavern_editorial_20261120 as boot
from scripts import register_sound_sirens_20261120 as parent
from scripts import stage_market_report_status_20261120 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch, native = parent.base, stage.batch, parent.native
PROFILE = 'all-routes-market-report-status-v1-20261120'
ROOT = Path('out/market_report_status_registered_20261120_v1')
ROM = ROOT / 'Translation_DS_Market_Report_Status_20261120_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261120_market_report_status_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_market_report_status_registered_20261120.md')
STARTUP, QA, VISUAL = (stage.ROOT / name for name in ('own_startup_verification.json', 'qa.xml', 'visual_review.json'))
SHEETS = (game.SHEET,)
STARTUP_CAPTURE = game.ROOT / 'final_startup/capture/capture_report.json'
CHECKPOINT = 'Registered complete Market Info headings, the restored Status field, and regular-width punctuation in the route chart.'
MEANINGS = {
    'DK4_TOWN_CHART_COORDINATES': ('The original town name followed by its latitude and longitude.',
                                   'Keep the original name and all five arguments. Use regular parentheses and spacing.'),
    'DK4_TOWN_CHART_UNKNOWN': ('The field is unknown because the town information is hidden.',
                               'Keep the question mark and its original left inset.'),
    'DK4_TOWN_CHART_SHARE': ('The share of the market the named faction controls.',
                             'Keep the three-cell right-aligned number and use a regular-width percent sign.'),
}


def verify(registry, previous, viewed):
    stored, result, chart = map(base.load, (stage.PROOF, game.PROOF, game.chart.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == result['candidate_sha256']
    assert stored['parent_sha256'] == result['previous_sha256'] == previous['candidate_sha256'] == base.digest(parent.ROM)
    assert stored['clean_input_sha256'] == previous['clean_input_sha256'] == base.digest(batch.CLEAN)
    assert stored['whole_parent_inverse'] and stored['clean_input_patch_byte_exact']
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()
    assert base.digest(stage.ROOT / 'translation.xdelta') == stored['clean_input_patch_sha256']
    assert viewed == {str(game.SHEET): base.digest(game.SHEET)} and viewed[str(game.SHEET)] == result['sheet_sha256']
    assert len(chart['title_draws']) == 114 and len(chart['percentages']) == 101 and chart['hidden_fields'] == 5
    assert chart['candidate_sha256'] == stored['charts_only_sha256']
    assert len(result['original_stock_status_cases']) == 14 and len(result['actual_emulator_masks']) == 4
    assert result['matches_chart_only_stage_on_all_chart_frames']
    assert all(base.digest(path) == sha for path, sha in result['evidence'].items())
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [32, 0, 0, 2]

    clean, prior, target, chart_only = map(batch.NdsImage.open,
        (batch.CLEAN, parent.ROM, stage.ROM, stage.headings.chart.ROM))
    before, after = map(batch.files, (prior, target))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {batch.ARM}
    arm, common = after[batch.ARM], after[batch.COMMON]
    source = clean.read_file(batch.ARM)
    rebuilt, chart_rows, heads, positions = stage.patch(before[batch.ARM], source)
    assert rebuilt == arm and chart_rows == stored['chart_rows'] and positions == stored['status_geometry']
    comparable = bytearray(arm)
    original = before[batch.ARM]
    for row in [*heads, *positions]:
        off = row['descriptor_offset'] if 'descriptor_offset' in row else row['offset']
        comparable[off:off + 28] = original[off:off + 28]
    assert bytes(comparable) == chart_only.read_file(batch.ARM)
    assert base.digest(stage.headings.chart.ROM) == stored['charts_only_sha256']
    assert batch.digest(arm) == stored['target_ARM9_sha256']
    assert batch.digest(common) == stored['target_COMMON_sha256'] == previous['target_COMMON_sha256']
    target.replace_file(batch.ARM, original)
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(batch.files(clean), after)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    table = batch.owned_entries(common, arm, batch.digest(arm[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET]))
    pending = base.load(parent.parent.parent.parent.PENDING)['records']
    assert len(pending) == 276 and all(batch.reference(table[row['message_ID']]) == row['current_reference']
        and table[row['message_ID']].text.hex() == row['current_hex'] for row in pending)
    startup = FunctionType(boot.startup_proof.__code__, boot.startup_proof.__globals__ |
                           {'STARTUP': STARTUP, 'STARTUP_CAPTURE': STARTUP_CAPTURE})
    startup(previous, candidate, arm)
    records = []
    for row in chart_rows:
        gloss, reason = MEANINGS[row['id']]
        records.append(row | dict(english=row['english'].strip(), file_path=batch.ARM, speaker='Route chart', context='Market Info route chart.',
            source_meaning=gloss, localization_note=reason, decision='revision', review=dict.fromkeys(batch.GATES, True)))
    japanese = ('種類', '状態', '発展度', '武装度')
    for i, (row, jp) in enumerate(zip(heads, japanese, strict=True)):
        off = row['descriptor_offset']
        x, _, width, _ = row['previous'][3:]
        first = stage.headings.PACKED + (x - 84) // 6
        fragment = original[first:first + width // 6].decode('ascii')
        revision = row['heading'] != fragment
        records.append(row | dict(id=f'DK4_MARKET_REPORT_HEADING_{i}', file_path=batch.ARM, speaker='Market Info',
            english=row['heading'], clean_Japanese=jp, context='Heading above a town field in the detailed Market Info report.',
            source_meaning=f'The settlement’s {row["heading"].lower()} field.',
            previous_display=fragment, source_descriptor_hex=source[off:off + 28].hex(),
            current_descriptor_hex=original[off:off + 28].hex(), target_descriptor_hex=arm[off:off + 28].hex(),
            localization_note='Retain the agreed English heading. Use its complete glyphs beside the correct value.',
            decision='revision' if revision else 'retention', review=dict.fromkeys(batch.GATES, True)))
    draft = result | dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=batch.GATES, records=records, checked_story_format_guard=controls,
        shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'], new_contextual_credit=0,
        atlas_value_binding=positions, chart_native_reference=dict(path=str(game.chart.OUTPUT), sha256=base.digest(game.chart.OUTPUT)))
    validate_natural_dialogue_batch(draft)
    return stored, draft, {batch.ARM: batch.digest(arm)}


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index('    DOC.write_text'):template.index('    prefix =')]
program = checked_text(template, {
    'len(manifest["batches"]) == 941 and len(manifest["checks"]) == 276':
        'len(manifest["batches"]) == 942 and len(manifest["checks"]) == 277',
    'stage.PROOF, STARTUP, QA, game.PROOF, args.visual_review':
        'stage.PROOF, STARTUP, QA, game.chart.OUTPUT, game.PROOF, args.visual_review',
    'release_stack_before_sound_sirens.json': 'release_stack_before_market_report.json',
    'release_stack_with_sound_sirens.json': 'release_stack_with_market_report.json',
    'verified_forces_chart_predecessor=predecessor, sound_sirens_release=str(REVIEW)':
        'verified_sound_sirens_predecessor=predecessor, market_report_status_release=str(REVIEW)',
    'registered_sound_sirens_and_complete_parent_inverse': 'registered_market_report_status_and_complete_parent_inverse',
    'manifest["sound_sirens_pipeline"]': 'manifest["market_report_status_pipeline"]',
    'owned_sound_title_slot=stored["slot"]': 'owned_chart_slots=stored["chart_rows"], owned_report_rectangles=stored["status_geometry"]',
    'reviewed_UI_labels=1, new_contextual_records=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=0':
        'reviewed_UI_labels=7, new_contextual_records=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1',
    'text_display_revisions=1, pagination_fixes=0': 'text_display_revisions=7, pagination_fixes=0',
    'ordinary_sound_setup_all_SFX_titles=True, audio_output_assessed=False':
        'ordinary_Lisbon_report=True, initialized_hidden_fields=True',
    'natural_activation=True, hardware=False': 'natural_activation=False, hardware=False',
    'ledger["sound_sirens_20261120"]': 'ledger["market_report_status_20261120"]',
    'ui_labels_reviewed=1, display_revisions=1, actual_effect_titles=59, new_contextual_credit=0,\n        prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=0':
        'ui_labels_reviewed=7, display_revisions=7, actual_paired_states=4, new_contextual_credit=0,\n        prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1',
    'Preserve the Sound Setup Sirens ROM or reconstruction': 'Preserve the Market Info ROM or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Market Info candidate

The [local ROM](../../{ROM.as_posix()}) repairs the Market Info headings and status field and normalizes the route chart punctuation.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Market Info headings and route chart punctuation

Market Info now shows full **Type**, **Status**, **Growth** and **Arms** headings. The panel reads the correct glyphs from the shared atlas and displays the Status value beside its heading. The native slot fits the full eight letters of **Shortage**. The route chart uses regular parentheses, question marks and percent signs while keeping every original argument. [Exact decisions](../{REVIEW.as_posix()})

The paired Lisbon replay checked four display states. It also checked both World Map selection modes and the return to Market. The hidden-information example supplied one original information bit, then restored it before the ordinary known-town report. Offline tests cover 114 town headings, 101 percentage values, five unknown fields and 14 status cases. [Before and after](../{(VERIFY / game.SHEET.name).as_posix()}) · [Replay and atlas checks](../{(VERIFY / game.PROOF.name).as_posix()})

The clean-input patch rebuilds the complete candidate byte for byte. Six startup frames, 24 protected getters and 30 focused tests passed. Two tests with optional historical inputs skipped. [Registered candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register', 'exec'), env)


if __name__ == '__main__':
    env['main']()
