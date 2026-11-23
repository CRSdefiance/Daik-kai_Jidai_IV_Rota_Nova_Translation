"""Register the verified first-discovery text and its Power reward glyph fix."""

from pathlib import Path
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_ruin_discovery_gameplay_20261120 as game
from scripts import register_swimmer_leak_square_dialogue_20261120 as parent
from scripts import stage_ruin_discovery_display_20261120 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, batch, native = parent.base, stage.batch, parent.native
PROFILE = 'all-routes-ruin-discovery-display-v1-20261120'
ROOT = Path('out/ruin_discovery_display_registered_20261120_v1')
ROM = ROOT / 'Translation_DS_Ruin_Discovery_20261120_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261120_ruin_discovery_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_ruin_discovery_display_registered_20261120.md')
NATIVE = stage.ROOT / 'native_discovery.json'
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'qa.xml'
DRAFT, VISUAL = stage.ROOT / 'contextual_review.json', stage.ROOT / 'visual_review.json'
SHEETS = (stage.ROOT / 'ruin_name_lines.png', stage.ROOT / 'portrait_sheet_01.png', game.SHEET)
CHECKPOINT = 'Registered the English ruin discovery banner and regular-width Power reward after the Cappadocia replay.'
RUNTIME_ID = 'DK4_RUINS_DISCOVERY_POWER_ASCII_DIGITS'
PENDING = parent.parent.parent.PENDING


def verify(registry, previous, viewed):
    stored, model, startup, played, draft = map(base.load, (stage.PROOF, NATIVE, STARTUP, game.PROOF, DRAFT))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == model['candidate_sha256'] == startup['candidate_sha256']
    assert candidate == played['candidate_sha256'] == draft['candidate_sha256']
    assert base.digest(parent.ROM) == previous['candidate_sha256'] == stored['parent_sha256'] == played['predecessor_sha256']
    assert base.digest(batch.CLEAN) == previous['clean_input_sha256'] and stored['exact_parent_inverse']
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()
    assert base.digest(stage.ROOT / 'translation.xdelta') == stored['clean_input_patch_sha256']
    assert viewed == {str(path): base.digest(path) for path in SHEETS}
    assert model['name_sheet_sha256'] == viewed[str(SHEETS[0])]
    assert played['reviewed_contact_sheet']['sha256'] == viewed[str(game.SHEET)]
    assert len(model['old_cases']) == len(model['current_cases']) == 21
    assert all(row['body']['within_width'] and row['title']['within_width'] for row in model['current_cases'])
    assert len(model['power_notice']['native_ring_cases']) == 320 and len(model['power_notice']['cases']) == 10
    assert len(startup['exact_matching_frames']) == 6 and len(startup['original_protected_name_getters']) == 24
    assert startup['complete_deployed_payload_exact'] and startup['cold_boot'] and not startup['savestate']
    assert played['independent_full_english_banner_ink'] and played['both_power_notice_full_native_masks']
    assert played['original_banner_and_reward_after_normal_inputs'] and played['displayed_reward'] == 5
    assert played['fixture_modes'] == ['restore-first-discovery', 'ceremony-Cappadocia-map']
    assert all(base.digest(path) == sha for path, sha in played['evidence'].items())
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [32, 0, 0, 2]

    clean, prior, target = map(batch.NdsImage.open, (batch.CLEAN, parent.ROM, stage.ROM))
    before, after = map(batch.files, (prior, target))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {batch.ARM}
    arm, common = after[batch.ARM], after[batch.COMMON]
    compiled, slots, number = stage.patch(before[batch.ARM], clean.read_file(batch.ARM))
    assert compiled == arm and slots == stored['source_slots'] and number == stored['power_call']
    assert batch.digest(arm) == stored['target_ARM9_sha256']
    assert batch.digest(common) == previous['target_COMMON_sha256'] == stored['target_COMMON_sha256']
    target.replace_file(batch.ARM, before[batch.ARM])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    directory = batch.digest(arm[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET])
    current = batch.owned_entries(common, arm, directory)
    pending = base.load(PENDING)['records']
    assert len(pending) == 276 and all(batch.reference(current[row['message_ID']]) == row['current_reference']
        and current[row['message_ID']].text.hex() == row['current_hex'] for row in pending)
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(batch.files(clean), after)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())

    heading, announcement, power = draft['records']
    assert heading['source_and_current_slots'] + announcement['source_and_current_slots'] == slots
    source = batch.common_message_entries(clean.read_file(batch.COMMON), clean.read_file(batch.ARM))
    original, existing = source[stage.POWER_NOTICE], current[stage.POWER_NOTICE]
    assert batch.reference(original) == power['source_reference'] and batch.reference(existing) == power['current_reference']
    assert original.text.hex() == power['source_hex'] and existing.text.hex() == power['current_hex']
    assert original.text.count(b'%s') == existing.text.count(b'%s') == 1
    power['registered_reference'] = power['current_reference'] | {'candidate_sha256': candidate}
    for row in draft['records']:
        row['review']['formatting'] = True
    draft.update(gameplay_gate_pending=False, observed_gameplay=played, checked_story_format_guard=controls,
                 shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'], new_contextual_credit=0,
                 exact_native_display_evidence=dict(path=str(VERIFY / NATIVE.name), sha256=base.digest(NATIVE)))
    validate_natural_dialogue_batch(draft)
    return stored, draft, {batch.ARM: batch.digest(arm)}


def preserve_copy(source, destination):
    if not destination.exists():
        parent.env['copyfile'](source, destination)
    assert base.digest(source) == base.digest(destination)


template = parent.program
readme = template[template.index('    (PACKAGE / "README.md").write_text'):template.index('    base.save(PACKAGE / "checksums.json",')]
doc = template[template.index('    DOC.write_text'):template.index('    prefix =')]
program = checked_text(template, {
    'assert not any(p.exists() for p in (ROOT, PACKAGE, DOC))':
        'assert not any(p.exists() for p in (MANIFEST, RELEASE, DOC))',
    'ROOT.mkdir()': 'ROOT.mkdir(exist_ok=True)',
    'VERIFY.mkdir(parents=True)': 'VERIFY.mkdir(parents=True, exist_ok=True)',
    'copyfile(stage.ROOT / "translation.xdelta", PATCH)': 'preserve_copy(stage.ROOT / "translation.xdelta", PATCH)',
    'copyfile(stage.ROOT / "clean_rebuilt.nds", ROM)': 'preserve_copy(stage.ROOT / "clean_rebuilt.nds", ROM)',
    'copyfile(source, dest)': 'preserve_copy(source, dest)',
    '    base.save(REVIEW, draft)': '''    if REVIEW.exists():
        assert base.load(REVIEW) == draft
    else:
        base.save(REVIEW, draft)''',
    '    backup.write_bytes(registry_before)': '''    if backup.exists():
        assert backup.read_bytes() == registry_before
    else:
        backup.write_bytes(registry_before)''',
    '    base.save(registry_draft, registry)': '''    if registry_draft.exists():
        assert base.load(registry_draft) == registry
    else:
        base.save(registry_draft, registry)''',
    'len(manifest["batches"]) == 937 and len(manifest["checks"]) == 272':
        'len(manifest["batches"]) == 938 and len(manifest["checks"]) == 273',
    'stage.PROOF, STARTUP, QA, verified.LIVE, game.SQUARE, game.replay.PROOF, REBASE, args.visual_review':
        'stage.PROOF, STARTUP, QA, NATIVE, game.PROOF, game.PALACE, args.visual_review',
    'release_stack_before_swimmer_leak_square.json': 'release_stack_before_ruin_discovery.json',
    'release_stack_with_swimmer_leak_square.json': 'release_stack_with_ruin_discovery.json',
    'verified_madeira_resupply_price_predecessor=predecessor, swimmer_leak_square_release=str(REVIEW)':
        'verified_swimmer_leak_square_predecessor=predecessor, ruin_discovery_display_release=str(REVIEW)',
    'registered_swimmer_leak_square_and_complete_parent_inverse': 'registered_ruin_discovery_and_complete_parent_inverse',
    '''    assert all((row["file_path"], row["id"]) in credited for row in draft["records"])
    ids = manifest["changed_records"][tavern.COMMON]
    for row in draft["records"]:
        if row["decision"] != "retention" and row["id"] not in ids:
            ids.append(row["id"])
''': '''    assert (batch.COMMON, 'COMMON_MESSAGE_288') in credited
    ids = manifest["changed_records"][batch.ARM]
    new_ids = [row['id'] for row in draft['records'] if row['file_path'] == batch.ARM] + [RUNTIME_ID]
    assert not any(new in ids for new in new_ids)
    ids.extend(new_ids)
''',
    'manifest["swimmer_leak_square_pipeline"]': 'manifest["ruin_discovery_display_pipeline"]',
    'native_display_sha256=base.digest(verified.PROOF)': 'native_display_sha256=base.digest(NATIVE)',
    'owned_shared_allocations=stored["allocations"], target_COMMON_sha256=archives[tavern.COMMON]':
        'owned_ARM9_slots=stored["source_slots"], owned_power_digit_call=stored["power_call"], target_ARM9_sha256=archives[batch.ARM]',
    'changed_components=1, target_COMMON_sha256=archives[tavern.COMMON]':
        'changed_components=1, target_ARM9_sha256=archives[batch.ARM]',
    'reviewed_UI_labels=0, new_contextual_records=0, prose_revisions=7, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=26':
        'reviewed_UI_labels=2, new_contextual_records=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1',
    'text_display_revisions=0, pagination_fixes=0': 'text_display_revisions=1, pagination_fixes=0',
    'initialized_revised_leak_fixture_and_Square=True, inherited_mermaid_sequence=True':
        'initialized_Cappadocia_first_discovery_and_power_reward=True, offline_other_ruin_names=20',
    'ARM9_sha256=previous["target_ARM9_sha256"], MESFILE_sha256=archives[tavern.COMMON]':
        'ARM9_sha256=archives[batch.ARM], MESFILE_sha256=previous["target_COMMON_sha256"]',
    'ledger["swimmer_leak_square_dialogue_20261120"]': 'ledger["ruin_discovery_display_20261120"]',
    '''previously_localized_records=34,
        new_contextual_credit=0, prose_revisions=7, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=26)''':
        '''previously_localized_records=1, newly_english_UI_labels=2, digit_display_fixes=1,
        new_contextual_credit=0, prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1)
    ledger["palace_fee_digit_finding_20261120"] = dict(status="observed-open", message_ID=1156,
        paired_emulator_evidence=str(VERIFY / game.PALACE.name), same_native_fee=2842,
        related_alternate_quote_to_check=1149)''',
    '''                  batch.ROM, batch.ROOT/"clean_rebuilt.nds", batch.ROOT.with_name("swimmer_leak_square_dialogue_20261120_v1")/"candidate.nds", game.replay.ROM]''':
        '''                  parent.ROM]''',
    'Preserve the swimmer, leak and Square dialogue ROM or reconstruction': 'Preserve the ruin discovery display ROM or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Ruin discovery candidate

The [local ROM](../../{ROM.as_posix()}) translates the first-discovery banner and uses regular-width digits in the following Power notice.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# First-discovery banner and Power reward registered

The first-discovery heading and announcement are now in English. The original catalogue supplies all 21 names. The native display fits even the longest announced name, with eight pixels on each side. The wording of the separate Power notice is retained, and its existing amount now uses regular-width digits. [Source and current ledger](../{REVIEW.as_posix()}) · [Native pages](../{(VERIFY / SHEETS[0].name).as_posix()})

Both builds used ordinary Gate and dialogue controls from the existing post-rockfall test save. The setup reset one discovery flag and transferred the original Cave Village Map through the game’s inventory routine. The revised Cappadocia labels matched independent glyph masks, both Power notices displayed the original award of 5, and the game set the same discovery flag and returned to an identical Istanbul screen. The other 20 names were checked offline. [Paired emulator captures](../{(VERIFY / game.SHEET.name).as_posix()}) · [Replay evidence](../{(VERIFY / game.PROOF.name).as_posix()})

Six startup holds, 24 protected name getters and 30 focused tests passed. Two optional historical fixtures skipped. The clean-input patch rebuilds the cumulative candidate exactly. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)

The Istanbul Palace’s minimum contract fee used wide digits in dialogue and regular digits in the payment screen. That separate display issue is confirmed in both builds. [Fee quote and payment evidence](../{(VERIFY / game.PALACE.name).as_posix()})
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register', 'exec'), env)


if __name__ == '__main__':
    env['main']()
