"""Register and credit the live-verified ship command over the exact Lil261 stack."""

import gzip
import os
from copy import deepcopy
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.ship_command_label_v1 import FIELD, NEW_POINTER, OLD_OFFSET, OLD_TEXT, TEXT, transform
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.stage_ship_command_release_v1 import (
    ARM, CANDIDATE, CLEAN, GETTERS, INVERSE_PATCH, MANIFEST, OUT, PARENT, PARENT_REGISTRY,
    PATCH, PROFILE, REGISTRY, RELEASE, STAGED, STARTUP,
)
from scripts.verify_ship_command_live_v1 import OUTPUT as ACTUAL


REVIEW = Path('translations/ship_command_label_final_review_v1.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
PROMOTED = Path('translations/promoted_build.json')
RECORD = 'DK4_ARM9_SHIP_ABANDON_COMMAND'
FAMILY = 'ship_command_label_contextual_20261110'
CONTEXT = 'contextual_story_natural_dialogue_pass_v1871'
CHECK = 'registered_ship_command_label_native_live_and_complete_parent_inverse'
SUMMARY = ('Abandon Ship is registered and credited once. The exact live menu label and its Back/No return passed. '
    'All 30 shared notice decisions remain preserved, with 19 static pages visually reviewed. The wider editorial review continues.')


def main():
    assert not any(p.exists() for p in [RELEASE, MANIFEST, REVIEW])
    parent, stage, startup, getters, actual = map(load, (PARENT, STAGED, STARTUP, GETTERS, ACTUAL))
    assert digest(PARENT) == stage['predecessor_release_sha256']
    assert digest(parent['manifest']) == stage['predecessor_manifest_sha256']
    assert digest(REGISTRY) == digest(PARENT_REGISTRY) == stage['predecessor_registry_sha256']
    assert digest(CANDIDATE) == stage['candidate_sha256'] == startup['candidate_sha256'] == actual['candidate_sha256']
    assert digest(CANDIDATE) == getters['runtime']['candidate_sha256']
    assert getters['both_name_getters_exact_for_all12_protected_actors']
    assert not stage['own_registered_startup_pending'] and digest(STARTUP) == stage['own_registered_startup_sha256']
    assert startup['new_ship_andboth_preserved_market_pointers_present_in_actual_startup_WRAM']
    assert actual['complete_normal_and_highlight_label_pixels'] and actual['no_returns_to_pixel_identical_menu_and_preserves_ship']
    assert actual['actual_ITCM_both_market_and_ship_literals_exact']
    assert len(actual['exact_normal_and_highlight_caption_masks']) == 6
    assert digest(PATCH) == stage['patch_sha256'] and INVERSE_PATCH.read_bytes() == CANDIDATE.read_bytes()
    assert stage['whole_parent_inverse_exact'] and stage['all_predecessor_stage_dependencies_preserved']
    assert digest(CLEAN) == stage['clean_input_sha256']
    prior = load(LEDGER)
    assert prior['records_editorially_completed'] == 25898 and not prior['full_goal_complete']
    assert prior['current_integrated_candidate']['sha256'] == stage['parent_sha256']
    assert FAMILY not in prior and not any(u['id'] == FAMILY for u in prior['coverage_units'])
    old = load(parent['manifest'])
    registry = load(REGISTRY)
    assert len(registry['accepted_layers']) == 114 and PROFILE not in registry['profiles']
    assert len(old['batches']) == 731 and len(old['checks']) == 66 and all(old['checks'].values())
    image = NdsImage.open(CANDIDATE)
    parent_image = NdsImage.open(parent['candidate'])
    source_arm = NdsImage.open(CLEAN).read_file(ARM)
    before_arm, target_arm = parent_image.read_file(ARM), image.read_file(ARM)
    assert source_arm[OLD_OFFSET:OLD_OFFSET+len(OLD_TEXT)] == before_arm[OLD_OFFSET:OLD_OFFSET+len(OLD_TEXT)] == OLD_TEXT
    assert transform(before_arm) == (target_arm, stage['original_data_only_transform'])
    assert list(parent_image.iter_files()) == list(image.iter_files())
    assert [p for p, data in parent_image.iter_components() if image.read_file(p) != data] == [ARM]
    assert old['story_percent_contract'] == stage['original_final_story_percent_contract']
    target_offset = target_arm.index(TEXT)
    assert target_arm.count(TEXT) == 1
    key = dict(file_path=ARM, id=RECORD)
    record = dict(**key, english=TEXT[:-1].decode('ascii'), decision='revision', speaker='Assign Sailors menu',
        context='The original forced-assignment menu offers Assign and a command acting on the selected ship.',
        source_meaning='Abandon the ship.',
        localization_note='Abandon Ship states the full action in the original command style beside Assign.',
        source_hex=OLD_TEXT.hex(), current_hex=OLD_TEXT.hex(),
        source_reference=dict(file_path=ARM, offset=OLD_OFFSET, pointer_field=FIELD),
        current_reference=dict(file_path=ARM, offset=OLD_OFFSET, pointer_field=FIELD, ROM_sha256=stage['parent_sha256']),
        registered_reference=dict(file_path=ARM, offset=target_offset, pointer_field=FIELD, runtime_address=NEW_POINTER,
            exact_stored_hex=TEXT.hex(), ROM_sha256=stage['candidate_sha256']),
        review=dict(source=True, context=True, localization=True, naturalness=True, formatting=True))
    scope = dict(actual_emulator=True, conditional_activation='initialized isolated one-byte crew fixture',
        normal_and_highlight_caption_masks=6, original_back_then_no_and_ship_preservation_observed=True,
        earned_crew_loss=False, confirmed_abandonment=False, hardware=False, guide_photos=False)
    reviewed = dict(format='dk4-reviewed-ship-command-label-v1', encoder='dialogue-relocatable-v1',
        translation_policy='natural-dialogue-v2', target_locale='en-US',
        review_gates=['source','context','localization','naturalness','formatting'], records=[record],
        ROM_sha256=stage['candidate_sha256'], clean_input_sha256=stage['clean_input_sha256'],
        review_actual=str(ACTUAL), review_actual_sha256=digest(ACTUAL), actual_verification_scope=scope,
        original_data_transform=stage['original_data_only_transform'], full_goal_complete=False)
    validate_natural_dialogue_batch(reviewed)

    promoted_hash = digest(PROMOTED)
    registry_pending = REGISTRY.with_name('release_stack.ship_command.pending.json')
    ledger_pending = LEDGER.with_name('editorial_review_current.ship_command.pending.json')
    backup = OUT/'ledger_before_completion.json.gz'
    assert not any(p.exists() for p in [registry_pending, ledger_pending, backup])
    predecessor = dict(profile=parent['profile'], candidate=parent['candidate'], candidate_sha256=parent['candidate_sha256'],
        manifest=parent['manifest'], manifest_sha256=parent['manifest_sha256'],
        registry=str(PARENT_REGISTRY), registry_sha256=digest(PARENT_REGISTRY))
    profile = deepcopy(registry['profiles'][parent['profile']])
    assert profile['ascii_glyph_right_bounds'] == stage['right_bound_configuration']
    profile.update(verified_lil261_predecessor=predecessor, ship_command_label=str(REVIEW),
        note='Cumulative test candidate with the localized Assign Sailors ship command.')
    registry['profiles'][PROFILE] = profile
    save(registry_pending, registry)

    save(REVIEW, reviewed)
    manifest = deepcopy(old)
    manifest.update(profile=PROFILE, candidate_rom=str(CANDIDATE), candidate_sha256=stage['candidate_sha256'],
        release_stack_sha256=digest(registry_pending))
    manifest['batches'].append(str(REVIEW))
    assert RECORD not in manifest['changed_records'][ARM]
    manifest['changed_records'][ARM].append(RECORD)
    manifest['checks'][CHECK] = True
    manifest['relocations'][ARM]['ship-command-label'] = stage['original_data_only_transform']
    manifest['ship_command_label_registered_successor_pipeline'] = dict(predecessor=predecessor, driver=__file__,
        driver_sha256=digest(__file__), review=str(REVIEW), review_sha256=digest(REVIEW),
        actual=str(ACTUAL), actual_sha256=digest(ACTUAL))
    assert manifest['batches'][:-1] == old['batches'] and len(manifest['checks']) == 67
    save(MANIFEST, manifest)
    preserve = ['owned_Francisca_name_field_verified','owned_Plett_Jacob_surnames_verified','owned_Zaganos_surname_verified',
        'owned_Hodram_residual_surnames_verified','owned_Rafael_residual_middle_fields_verified',
        'all_nine_registered_final_stages_preserved','all_eight_registered_final_stages_preserved']
    assert all(parent[k] for k in preserve)
    save(RELEASE, {**stage, **{k:parent[k] for k in preserve}, 'actual_menu_approval_pending':False, 'registration_pending':False,
        'manifest':str(MANIFEST), 'manifest_sha256':digest(MANIFEST), 'registry_sha256':digest(registry_pending),
        'predecessor':predecessor, 'complete_stack_entries':732, 'registered_manifest_entries':732,
        'passing_release_checks':67, 'accepted_layers':114, 'own_registered_name_getters':str(GETTERS),
        'own_registered_name_getters_sha256':digest(GETTERS), 'registered_market_format_andboth_data_pointers_preserved':True,
        'final_story_percent_contract':old['story_percent_contract'], 'target_SC2_sha256':parent['target_SC2_sha256'],
        'actual_ship_menu':str(ACTUAL), 'actual_ship_menu_sha256':digest(ACTUAL),
        'changed_components':[ARM], 'changed_internal_files':[], 'new_contextual_records':1,
        'prose_revisions':1, 'justified_retentions':0, 'full_goal_complete':False})

    ledger = dict(prior)
    context = deepcopy(prior[CONTEXT])
    for name in ['record_keys','integrated_record_keys']:
        assert key not in context[name] and len(context[name]) == 25898
        context[name].append(key)
    context['record_IDs'].append(RECORD)
    for name in ['fresh_pass_records_explicitly_reread','fresh_pass_records_integrated']:
        context[name] += 1
    context.update(latest_completed_family=FAMILY, latest_final_review=str(REVIEW))
    context['reconciled_families'].append(dict(id=FAMILY, records=1, final_review=str(REVIEW), new_revisions=1,
        justified_retentions=0, new_completed_records=1, historical_reconciliation_only=False, actual_verification_scope=scope))
    ledger[CONTEXT] = context
    family = dict(id=FAMILY, kind='raw-player-facing-label', records=1, record_keys=[key], final_review=str(REVIEW),
        final_review_sha256=digest(REVIEW), revised_count=1, retained_count=0, fresh_revisions=1,
        fresh_retentions=0, actual_verification_scope=scope, integrated_record_bindings=str(REVIEW))
    ledger['completed_editorial_families'] = [*prior['completed_editorial_families'], family]
    ledger['coverage_units'] = [*prior['coverage_units'], dict(**family, status='complete-contextual-native-stored-representative-registered-release',
        completion_credit_added=1, release_verification=str(RELEASE), release_verification_sha256=digest(RELEASE), full_goal_complete=False)]
    for name in ['records_editorially_completed','records_revised_and_integrated','records_with_source_and_prose_pass','records_with_source_prose_drafts']:
        ledger[name] += 1
    current = dict(prior['current_integrated_candidate'], path=str(CANDIDATE), sha256=stage['candidate_sha256'],
        profile=PROFILE, ARM9_sha256=stage['target_ARM9_sha256'], patch=str(PATCH), patch_sha256=digest(PATCH),
        manifest=str(MANIFEST), manifest_sha256=digest(MANIFEST), registered_release_verification=str(RELEASE))
    ledger['current_integrated_candidate'] = current
    leads = deepcopy(prior['unreviewed_player_facing_prose_leads'])
    lead, = [r for r in leads if r['id'] == 'V911-Assign-Sailors-abandon-ship-raw-caption']
    lead.update(status='completed-registered-contextual-review', source_consumer_layout_and_translation_not_yet_reviewed=False,
        completed_entries_added=1, final_review=str(REVIEW), final_review_sha256=digest(REVIEW))
    ledger['unreviewed_player_facing_prose_leads'] = leads
    ledger[FAMILY] = dict(new_credit=1, final_review=str(REVIEW), release_verification=str(RELEASE),
        actual_verification=str(ACTUAL), registered_integration_pending=False)
    ledger['latest_checkpoint'] = SUMMARY
    assert len(context['integrated_record_keys']) == ledger['records_editorially_completed'] == 25899
    assert ledger['records_revised_and_integrated'] == 15402
    before = LEDGER.read_bytes()
    backup.write_bytes(gzip.compress(before, compresslevel=1, mtime=0))
    assert gzip.decompress(backup.read_bytes()) == before
    ledger_pending.write_bytes(encode_ledger(ledger))
    save(OUT/'registration_mutation_plan.json', dict(registry_before=digest(REGISTRY), registry_after=digest(registry_pending),
        ledger_before=digest(LEDGER), ledger_after=digest(ledger_pending), release_sha256=digest(RELEASE)))
    assert digest(REGISTRY) == stage['predecessor_registry_sha256'] and LEDGER.read_bytes() == before
    os.replace(registry_pending, REGISTRY)
    os.replace(ledger_pending, LEDGER)
    assert digest(REGISTRY) == load(RELEASE)['registry_sha256'] and digest(PROMOTED) == promoted_hash
    registered = load(REGISTRY)
    assert {k:v for k,v in registered['profiles'].items() if k != PROFILE} == load(PARENT_REGISTRY)['profiles']
    assert {k:v for k,v in registered.items() if k != 'profiles'} == {k:v for k,v in load(PARENT_REGISTRY).items() if k != 'profiles'}
    save(OUT/'completion_checkpoint.json', dict(new_credit=1, counts=dict(completed=25899,revised=15402,retained=10497),
        candidate_sha256=stage['candidate_sha256'], ledger_sha256=digest(LEDGER), original_main_unchanged=True, full_goal_complete=False))
    print('Registered 732 entries and 67 checks. Credited the ship label once and preserved main.')


if __name__ == '__main__':
    main()
