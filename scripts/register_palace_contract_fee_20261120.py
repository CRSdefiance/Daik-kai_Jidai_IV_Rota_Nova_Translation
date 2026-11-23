"""Register the verified digit correction in both Palace fee offers."""

from inspect import getsource
from pathlib import Path
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_palace_contract_fee_20261120 as game
from scripts import register_amsterdam_tavern_editorial_20261120 as boot
from scripts import register_ruin_discovery_display_20261120 as parent
from scripts import stage_palace_contract_fee_20261120 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch, native = parent.base, stage.batch, parent.native
PROFILE = 'all-routes-palace-contract-fee-v1-20261120'
ROOT = Path('out/palace_contract_fee_registered_20261120_v1')
ROM = ROOT / 'Translation_DS_Palace_Contract_Fee_20261120_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261120_palace_contract_fee_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_palace_contract_fee_registered_20261120.md')
STARTUP, QA, VISUAL = (stage.ROOT / name for name in ('own_startup_verification.json', 'qa.xml', 'visual_review.json'))
STARTUP_CAPTURE = Path('E:/Rota Nova translations/Generated/work/palace_contract_fee_20261120/startup_v1/release_startup/capture/capture_report.json')
SHEETS = (stage.ROOT / 'portrait_sheet_01.png', game.SHEET)
CHECKPOINT = 'Registered regular-width minimum contract fees in both Palace branches after the payment and refusal replays.'
RUNTIME_ID = 'DK4_PALACE_MINIMUM_CONTRACT_FEE_ASCII_DIGITS'
CONTEXT = {
    1149: ('The ruler quotes the minimum before explaining the player cannot afford it.',
           'The ruler agrees that the player may trade in town and quotes the minimum fee in gold coins.'),
    1156: ('The ruler quotes the minimum before asking how much the player will offer.',
           'The ruler considers allowing the player to trade and quotes this town’s minimum contract fee in gold coins.'),
    1157: ('The ruler follows the quote with the amount selection.',
           'The market share depends on the offered fee. The ruler asks how much the player will pay.'),
    1162: ('The ruler responds to a captain whose funds fall below the minimum.',
           'The player is short of the fee and should return another time.'),
}


def startup_proof(previous, candidate, arm):
    program = checked_text(getsource(boot.startup_proof), {
        "    assert old['core_options'] == new['core_options']": '''
    assert old['core_DLL_sha256'] == new['core_DLL_sha256']
    pointer_option = 'desmume_pointer_type'
    old_options, new_options = (dict(report['core_options']) for report in (old, new))
    assert (old_options.pop(pointer_option), new_options.pop(pointer_option)) == ('touch', 'mouse')
    assert old_options == new_options and not any('touch' in row for row in new['scripted_input_schedule'])
'''.strip('\n'),
        "                  complete_deployed_payload_exact=True, actual_captain_getter=3,":
            """                  startup_pointer_modes=['touch', 'mouse'], scripted_startup_pad_only=True,
                  complete_deployed_payload_exact=True, actual_captain_getter=3,""",
    })
    env = boot.startup_proof.__globals__ | {'STARTUP': STARTUP, 'STARTUP_CAPTURE': STARTUP_CAPTURE}
    exec(compile(program, __file__ + '::startup', 'exec'), env)
    env['startup_proof'](previous, candidate, arm)


def verify(registry, previous, viewed):
    stored, result = map(base.load, (stage.PROOF, game.PROOF))
    candidate = base.digest(stage.ROM)
    assert stored['candidate_sha256'] == result['candidate_sha256'] == candidate
    assert base.digest(parent.ROM) == previous['candidate_sha256'] == stored['parent_sha256'] == result['predecessor_sha256']
    assert base.digest(batch.CLEAN) == previous['clean_input_sha256'] == stored['clean_input_sha256']
    assert stored['clean_input_patch_byte_exact'] and stored['exact_parent_inverse']
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()
    assert base.digest(stage.ROOT / 'translation.xdelta') == stored['clean_input_patch_sha256']
    assert viewed == {str(p): base.digest(p) for p in SHEETS}
    assert result['gameplay_sheet']['sha256'] == viewed[str(game.SHEET)]
    model = result['offline']
    assert len(model['original_town_fees']) == 114 and len(model['original_format_handoffs']) == 164
    assert model['representatives'][0]['sha256'] == viewed[str(SHEETS[0])]
    played = result['observed_gameplay']
    assert played['paid']['transaction_funds'] == [8371, 5529] and played['refused']['transaction_funds'] == [1, 1]
    for case in played.values():
        assert case['complete_before_after_masks']
        for pair in case['records']:
            assert base.digest(pair['report']) == pair['report_sha256']
            for frame in [pair['held_frame'], *pair['control_frames']]:
                assert base.digest(frame['path']) == frame['PNG_sha256']
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [32, 0, 0, 2]

    clean, prior, target = map(batch.NdsImage.open, (batch.CLEAN, parent.ROM, stage.ROM))
    before, after = map(batch.files, (prior, target))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {batch.ARM}
    arm, common = after[batch.ARM], after[batch.COMMON]
    assert stage.patch(before[batch.ARM], clean.read_file(batch.ARM)) == (arm, stored['native_calls'])
    assert batch.digest(arm) == stored['target_ARM9_sha256']
    assert batch.digest(common) == stored['target_COMMON_sha256'] == previous['target_COMMON_sha256']
    target.replace_file(batch.ARM, before[batch.ARM])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(batch.files(clean), after)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    current = batch.owned_entries(common, arm, batch.digest(arm[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET]))
    source = batch.common_message_entries(clean.read_file(batch.COMMON), clean.read_file(batch.ARM))
    pending = base.load(parent.PENDING)['records']
    assert len(pending) == 276 and all(batch.reference(current[row['message_ID']]) == row['current_reference']
        and current[row['message_ID']].text.hex() == row['current_hex'] for row in pending)
    for row in result['records']:
        n = row['message_ID']
        assert batch.reference(source[n]) == row['source_reference'] and source[n].text.hex() == row['source_hex']
        assert batch.reference(current[n]) == row['current_reference'] and current[n].text.hex() == row['current_hex']
        expected = int(n in stage.CALLS)
        assert source[n].text.count(b'%s') == current[n].text.count(b'%s') == expected
        row['context'], row['source_meaning'] = CONTEXT[n]
        row['registered_reference'] = row['current_reference'] | {'candidate_sha256': candidate}
    startup_proof(previous, candidate, arm)
    draft = result | dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=batch.GATES, checked_story_format_guard=controls,
        shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'], new_contextual_credit=0)
    validate_natural_dialogue_batch(draft)
    return stored, draft, {batch.ARM: batch.digest(arm)}


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index('    DOC.write_text'):template.index('    prefix =')]
program = checked_text(template, {
    'len(manifest["batches"]) == 938 and len(manifest["checks"]) == 273':
        'len(manifest["batches"]) == 939 and len(manifest["checks"]) == 274',
    'stage.PROOF, STARTUP, QA, NATIVE, game.PROOF, game.PALACE, args.visual_review':
        'stage.PROOF, STARTUP, QA, game.PROOF, args.visual_review',
    'release_stack_before_ruin_discovery.json': 'release_stack_before_palace_fee.json',
    'release_stack_with_ruin_discovery.json': 'release_stack_with_palace_fee.json',
    'verified_swimmer_leak_square_predecessor=predecessor, ruin_discovery_display_release=str(REVIEW)':
        'verified_ruin_discovery_predecessor=predecessor, palace_contract_fee_release=str(REVIEW)',
    'registered_ruin_discovery_and_complete_parent_inverse': 'registered_palace_fee_and_complete_parent_inverse',
    "assert (batch.COMMON, 'COMMON_MESSAGE_288') in credited":
        'assert all((row["file_path"], row["id"]) in credited for row in draft["records"])',
    'manifest["ruin_discovery_display_pipeline"]': 'manifest["palace_contract_fee_pipeline"]',
    'native_display_sha256=base.digest(NATIVE)': 'native_display_sha256=base.digest(game.PROOF)',
    'owned_ARM9_slots=stored["source_slots"], owned_power_digit_call=stored["power_call"]':
        'owned_contract_digit_calls=stored["native_calls"]',
    'reviewed_UI_labels=2, new_contextual_records=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1':
        'reviewed_UI_labels=0, new_contextual_records=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=4',
    'text_display_revisions=1, pagination_fixes=0': 'text_display_revisions=2, pagination_fixes=0',
    'initialized_Cappadocia_first_discovery_and_power_reward=True, offline_other_ruin_names=20':
        'ordinary_Istanbul_payment=True, initialized_insufficient_funds_refusal=True',
    'ledger["ruin_discovery_display_20261120"]': 'ledger["palace_contract_fee_20261120"]',
    '''previously_localized_records=1, newly_english_UI_labels=2, digit_display_fixes=1,
        new_contextual_credit=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1)
    ledger["palace_fee_digit_finding_20261120"] = dict(status="observed-open", message_ID=1156,
        paired_emulator_evidence=str(VERIFY / game.PALACE.name), same_native_fee=2842,
        related_alternate_quote_to_check=1149)''':
        '''previously_localized_records=4, digit_display_fixes=2, new_contextual_credit=0, prose_revisions=0,
        spacing_revisions=0, wrap_only_revisions=0, justified_retentions=4)
    ledger["palace_fee_digit_finding_20261120"].update(status="verified-fixed-in-both-branches",
        registered_review=str(REVIEW), checked_alternate_quote=1149)''',
    'Preserve the ruin discovery display ROM or reconstruction': 'Preserve the Palace contract fee ROM or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Palace contract fee candidate

The [local ROM](../../{ROM.as_posix()}) uses regular-width digits in both minimum contract fee quotes and incorporates the registered ruin discovery fixes.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Palace contract fee digits registered

Both Palace contract quotes use regular-width digits. Four source-bound wording retentions preserve the ruler’s distinct responses, the quoted minimum and the relationship between the offered fee and market share. Both quote paths use the original calculation and payment logic. All 164 native format cases cover 82 distinct fee amounts calculated by the game across 114 towns. [Registered review](../{REVIEW.as_posix()}) · [Native pages](../{(VERIFY / SHEETS[0].name).as_posix()})

The ordinary Istanbul replay accepted the same 2,842-gold payment. The paired refusal replay initialized the wallet to one gold through the original money method and confirmed that the refusal leaves it there. Both versions returned to identical screens, and the display diffs stay inside the quote’s final text row. [Paired game captures](../{(VERIFY / game.SHEET.name).as_posix()})

Six startup holds, 24 protected name getters and 30 focused tests passed. Two optional historical fixtures skipped. The patch rebuilds the cumulative candidate byte for byte. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register', 'exec'), env)


if __name__ == '__main__':
    env['main']()
