"""Register the Sirens label and coverage of every original SFX menu index."""

from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_sound_sirens_20261120 as game
from scripts import register_amsterdam_tavern_editorial_20261120 as boot
from scripts import register_forces_chart_fields_20261120 as parent
from scripts import stage_sound_sirens_20261120 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch, native = parent.base, stage.batch, parent.native
PROFILE = 'all-routes-sound-sirens-v1-20261120'
ROOT = Path('out/sound_sirens_registered_20261120_v1')
ROM = ROOT / 'Translation_DS_Sound_Sirens_20261120_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261120_sound_sirens_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_sound_sirens_registered_20261120.md')
STARTUP, QA, VISUAL = (stage.ROOT / name for name in ('own_startup_verification.json', 'qa.xml', 'visual_review.json'))
SHEETS = (game.SHEET,)
STARTUP_CAPTURE = game.ROOT / 'startup/capture/capture_report.json'
CHECKPOINT = 'Registered the English Sirens label after verifying all 59 selectable Sound Setup effects and the return to title.'
OPTIONS = Path('translations/editorial_checkpoints/SharedText_20261110_v1/options_legacy_observed_consumers_20261114_v1.json')


def verify(registry, previous, viewed):
    staged, result = map(base.load, (stage.PROOF, game.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == staged['candidate_sha256'] == result['candidate_sha256']
    assert staged['parent_sha256'] == result['parent_sha256'] == previous['candidate_sha256'] == base.digest(parent.ROM)
    assert staged['clean_input_sha256'] == previous['clean_input_sha256'] == base.digest(batch.CLEAN)
    assert staged['whole_parent_inverse'] and staged['clean_input_patch_byte_exact']
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()
    assert base.digest(stage.ROOT / 'translation.xdelta') == staged['clean_input_patch_sha256']
    assert viewed == {str(game.SHEET): base.digest(game.SHEET)} and viewed[str(game.SHEET)] == result['sheet_sha256']
    assert len(result['titles']) == result['active_selection_count'] == 59
    assert result['native_direction_checks'] == 118 and len(result['complete_current_actual_title_masks']) == 60
    assert result['original_selector_audio_ID_table_preserved'] and not result['actual_audio_output_checked']
    assert all(base.digest(path) == sha for path, sha in result['evidence'].items())
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [32, 0, 0, 2]

    clean, prior, target = map(batch.NdsImage.open, (batch.CLEAN, parent.ROM, stage.ROM))
    before, after = map(batch.files, (prior, target))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {batch.ARM}
    arm, common = after[batch.ARM], after[batch.COMMON]
    assert stage.patch(before[batch.ARM], clean.read_file(batch.ARM)) == (arm, staged['slot'])
    assert batch.digest(arm) == staged['target_ARM9_sha256']
    assert batch.digest(common) == staged['target_COMMON_sha256'] == previous['target_COMMON_sha256']
    target.replace_file(batch.ARM, before[batch.ARM])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(batch.files(clean), after)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    table = batch.owned_entries(common, arm, batch.digest(arm[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET]))
    pending = base.load(parent.parent.parent.PENDING)['records']
    assert len(pending) == 276 and all(batch.reference(table[row['message_ID']]) == row['current_reference']
        and table[row['message_ID']].text.hex() == row['current_hex'] for row in pending)
    startup = FunctionType(boot.startup_proof.__code__, boot.startup_proof.__globals__ |
                           {'STARTUP': STARTUP, 'STARTUP_CAPTURE': STARTUP_CAPTURE})
    startup(previous, candidate, arm)
    record = staged['slot'] | dict(id='DK4_SOUND_SFX_SIRENS', file_path=batch.ARM, speaker='Sound Setup',
        context='Name of the Sirens sound effect in the original title menu, between Dolphin and Rain.',
        source_meaning='The Sirens from the encounter at sea.',
        localization_note='Use Sirens, the established name in voyage dialogue and the sailing condition list.',
        registered_reference=dict(candidate_sha256=candidate, offset=stage.SLOT, size=stage.SIZE),
        decision='revision', review=dict.fromkeys(batch.GATES, True))
    nearby = result['titles'][31:34]
    assert [r['english'] for r in nearby] == ['Dolphin', 'Sirens', 'Wet']
    prior_trace = base.load(OPTIONS)
    assert [r['message_ID'] for r in prior_trace['checked_pending_legacy_keys']] == [102, 330, 331, 332, 333]
    draft = result | dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=batch.GATES, records=[record], checked_story_format_guard=controls,
        shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'], new_contextual_credit=0,
        sound_setup_owner_scope=dict(native_SFX_title_owner='ARM9 pointer table, 59 indices',
            earlier_observed_title_menu_requests=str(OPTIONS), evidence_sha256=base.digest(OPTIONS),
            legacy_ids=[102, 330, 331], classification='Other possible uses remain open. Sound Setup title selection is independently bound.'))
    validate_natural_dialogue_batch(draft)
    return staged, draft, {batch.ARM: batch.digest(arm)}


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index('    DOC.write_text'):template.index('    prefix =')]
program = checked_text(template, {
    'len(manifest["batches"]) == 940 and len(manifest["checks"]) == 275':
        'len(manifest["batches"]) == 941 and len(manifest["checks"]) == 276',
    'stage.PROOF, STARTUP, QA, chart.OUTPUT, game.PROOF, args.visual_review':
        'stage.PROOF, STARTUP, QA, game.PROOF, args.visual_review',
    'release_stack_before_forces_chart.json': 'release_stack_before_sound_sirens.json',
    'release_stack_with_forces_chart.json': 'release_stack_with_sound_sirens.json',
    'verified_palace_contract_fee_predecessor=predecessor, forces_chart_release=str(REVIEW)':
        'verified_forces_chart_predecessor=predecessor, sound_sirens_release=str(REVIEW)',
    'registered_forces_chart_and_complete_parent_inverse': 'registered_sound_sirens_and_complete_parent_inverse',
    'manifest["forces_chart_fields_pipeline"]': 'manifest["sound_sirens_pipeline"]',
    'native_display_sha256=base.digest(chart.OUTPUT)': 'native_display_sha256=base.digest(game.PROOF)',
    'owned_chart_slots=stored["rows"]': 'owned_sound_title_slot=stored["slot"]',
    'reviewed_UI_labels=10, new_contextual_records=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=2':
        'reviewed_UI_labels=1, new_contextual_records=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=0',
    'text_display_revisions=8, pagination_fixes=0': 'text_display_revisions=1, pagination_fixes=0',
    'ordinary_Lisbon_chart_and_unknown_faction=True, initialized_no_home_fallback=True':
        'ordinary_sound_setup_all_SFX_titles=True, audio_output_assessed=False',
    'natural_activation=False, hardware=False': 'natural_activation=True, hardware=False',
    'ledger["forces_chart_fields_20261120"]': 'ledger["sound_sirens_20261120"]',
    '''ui_labels_reviewed=10, display_revisions=8, new_contextual_credit=0, prose_revisions=0,
        spacing_revisions=0, wrap_only_revisions=0, justified_retentions=2)''':
        '''ui_labels_reviewed=1, display_revisions=1, actual_effect_titles=59, new_contextual_credit=0,
        prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=0)''',
    'Preserve the Forces chart ROM or reconstruction': 'Preserve the Sound Setup Sirens ROM or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Sound Setup Sirens candidate

The [local ROM](../../{ROM.as_posix()}) displays **Sirens** in the original Sound Setup effect selector.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Sound Setup Sirens title registered

Sound Setup now displays **Sirens** at the original effect index 32 between Dolphin and the rain effect. This uses the name already established in the sailing condition and the encounter. The original effect ID, volume logic, title position and controls carry forward. [Exact source and current references](../{REVIEW.as_posix()})

The native selector has 59 entries. The earlier 57-slot storage inventory included Replay, which this selector does not point to. It omitted Cancel, Message and Sirens. Cancel and Message already had English labels. The new offline check executed the original painter for all 59 entries and checked Up and Down at every index against the game’s effect table. [Selector and glyph evidence](../{(VERIFY / game.PROOF.name).as_posix()})

The paired ordinary title-menu replays matched the complete rendered text at every selectable effect, including wraparound and the exit to title. **Sirens** is the only visual difference. The replay issued Play at Sirens. Audio output was outside the comparison, and the earlier tested volume path continues to account for the observed Sound Setup controls. Potential other uses of the stored COMMON 102, 330 and 331 remain open. [Before and after](../{(VERIFY / game.SHEET.name).as_posix()})

Six startup holds, 24 protected name getters and 30 focused tests passed. Two optional legacy tests skipped. The clean-input patch rebuilds the cumulative candidate byte for byte. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register', 'exec'), env)


if __name__ == '__main__':
    env['main']()
