"""Stage and register the exact post-Rafael3514 dialogue and surname successor."""
from copy import deepcopy
import json
import os
from pathlib import Path
import sys

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.rafael_story_b261_b280_release_v1 import plan_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.format_safety_relocated_v1 import bind_registered_story_percent_guard
from scripts.audit_story_glyph_consistency import load, save
from scripts.finalize_rafael_B261_B280_research_v1 import FINAL, NAME_PROOF, STORED
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_rafael_B261_B280_registered_v1 import ARCHIVE, ARM, CONFIG, OUT as PREPARATION
from scripts.qualify_rafael_plett_relocation_v1 import CLEAN, REGISTRY, plan_surnames
from scripts.verify_rafael3514_registered_release_v1 import RELEASE as PARENT
from scripts.verify_rafael_B51_B60_registered_release import KEYS
from scripts.verify_release_baseline import REQUIRED_MENU_TEXT, REQUIRED_OPTIONS_TEXT


OUT = Path('work/rafael3649_release_v1')
PROFILE = 'all-routes-rafael3649-dialogue-surnames-v1-20261106'
CANDIDATE = OUT/'all_routes_rafael3649_candidate.nds'
MANIFEST = CANDIDATE.with_suffix('.manifest.json')
PATCH = CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH = OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED = OUT/'staged_successor.json'
RELEASE = OUT/'registered_release_verification.json'
STARTUP = OUT/'own_registered_startup_verification.json'
GETTERS = OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY = OUT/'release_stack_before_Rafael3649.json'
SURNAME_CONFIG = Path('translations/rafael_B261_B280_surnames_release_v1.json')
QUALIFICATION = PREPARATION/'qualification.json'
CHECK_SC0 = 'registered_B261_B280_dialogue_and_complete_parent_target_inverse'
CHECK_NAMES = 'registered_Plett_Jacob_surnames_and_complete_parent_target_inverse'


def stage():
    assert not OUT.exists()
    release, qualification, config = map(load, (PARENT, QUALIFICATION, CONFIG))
    assert digest(PARENT) == qualification['predecessor_release_sha256']
    assert digest(CONFIG) == qualification['config_sha256']
    assert digest(REGISTRY) == release['registry_sha256'] == qualification['registry_sha256']
    assert not release['own_registered_startup_pending'] and release['all_preceding_eight_stages_and_exclusive_field_preserved']
    parent_path, canonical_path = Path(release['candidate']), Path(release['canonical_base'])
    assert digest(parent_path) == config['parent_ROM_sha256'] == release['candidate_sha256']
    assert digest(canonical_path) == config['canonical_ROM_sha256'] == release['canonical_sha256']
    assert digest(CLEAN) == config['clean_ROM_sha256'] == release['clean_input_sha256']
    assert digest(release['manifest']) == release['manifest_sha256'] == qualification['predecessor_manifest_sha256']
    assert digest(qualification['name_proposal']) == qualification['name_proposal_sha256']
    assert digest(qualification['name_ownership_proof']) == qualification['name_ownership_proof_sha256']
    old_manifest = load(release['manifest'])
    registry = load(REGISTRY)
    old_profile = registry['profiles'][release['profile']]
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers']) == 114
    stages = [Path(old_profile[key]) for key in [*KEYS, 'owned_Francisca_name_field']]
    assert [Path(path) for path in old_manifest['batches'][-9:]] == stages
    assert all(layer.get('baked_into_baseline') or layer['batch'] in old_manifest['batches'] for layer in registry['accepted_layers'])
    assert len(old_manifest['batches']) == 692 and len(old_manifest['checks']) == 27 and all(old_manifest['checks'].values())

    parent = NdsImage.open(parent_path)
    clean = NdsImage.open(CLEAN)
    original_arm, original_archive = parent.read_file(ARM), parent.read_file(ARCHIVE)
    dialogue, dialogue_proof = plan_release(parent, NdsImage.open(canonical_path), CONFIG)
    assert len(dialogue_proof['changed_records']) == 135
    proposed = NdsImage.open(load(config['reconstruction'])['research_ROM'])
    assert bytes(dialogue.save()) == bytes(proposed.rom.save())
    names, name_proof = plan_surnames(original_arm, load(qualification['name_proposal']), clean.read_file(ARM))
    native_names = load(NAME_PROOF)
    assert json.loads(json.dumps(name_proof)) == native_names['name_data_plan']
    assert names == Path(native_names['proposed_ARM9']).read_bytes()
    assert name_proof['target_ARM9_sha256'] == qualification['target_ARM9_sha256']
    proposed.replace_file(ARM, names)
    assert [path for _, path, data in parent.iter_files() if proposed.read_file(path) != data] == [ARCHIVE]
    assert [path for path, data in parent.iter_components() if proposed.read_file(path) != data] == [ARM]
    assert all(text in names for text in REQUIRED_MENU_TEXT) and any(text in names for text in REQUIRED_OPTIONS_TEXT)
    final_archive = proposed.read_file(ARCHIVE)
    before, after = (IlnkContainer.parse(data).blocks for data in (original_archive, final_archive))
    assert [index for index, (a, b) in enumerate(zip(before, after, strict=True)) if a != b] == config['blocks']
    # The final four-archive guard runs fresh because SC0 changed. Earlier
    # renderer and asset proofs apply to the exact retained code and files.
    paths = [f'/data/SC{route}.DK4' for route in range(4)]
    percent = bind_registered_story_percent_guard(old_manifest['story_percent_contract']['exact_relocation_receipt'])(
        {path: clean.read_file(path) for path in paths}, {path: proposed.read_file(path) for path in paths})
    assert percent == old_manifest['story_percent_contract']
    output = bytes(proposed.rom.save())
    proposed.replace_file(ARM, original_arm)
    proposed.replace_file(ARCHIVE, original_archive)
    assert bytes(proposed.rom.save()) == parent_path.read_bytes()

    OUT.mkdir()
    PARENT_REGISTRY.write_bytes(REGISTRY.read_bytes())
    assert digest(PARENT_REGISTRY) == release['registry_sha256']
    CANDIDATE.write_bytes(output)
    assert digest(CANDIDATE) == qualification['target_ROM_sha256']
    reopened = NdsImage.open(CANDIDATE)
    assert bytes(reopened.rom.save()) == output and reopened.read_file(ARCHIVE) == final_archive and reopened.read_file(ARM) == names
    make_xdelta(CLEAN, CANDIDATE, PATCH)
    apply_xdelta(CLEAN, PATCH, INVERSE_PATCH)
    assert INVERSE_PATCH.read_bytes() == output
    assert digest(REGISTRY) == release['registry_sha256']
    save(STAGED, dict(profile=PROFILE, candidate=str(CANDIDATE), candidate_sha256=digest(CANDIDATE),
        patch=str(PATCH), patch_sha256=digest(PATCH), clean_input_sha256=digest(CLEAN),
        exact_clean_reconstruction=str(INVERSE_PATCH), reconstructed_sha256=digest(INVERSE_PATCH),
        clean_input_patch_byte_exact=True, own_registered_startup_pending=True, experimental_not_promoted=True,
        parent=str(parent_path), parent_sha256=release['candidate_sha256'], canonical_base=str(canonical_path),
        canonical_sha256=release['canonical_sha256'], predecessor_profile=release['profile'],
        predecessor_release_sha256=digest(PARENT), predecessor_manifest_sha256=release['manifest_sha256'],
        predecessor_registry_sha256=digest(PARENT_REGISTRY), qualification_sha256=digest(QUALIFICATION),
        dialogue_release_config_sha256=digest(CONFIG), target_SC0_sha256=digest_bytes(final_archive),
        target_ARM9_sha256=qualification['target_ARM9_sha256'], only_owned_SC0_blocks_changed=config['blocks'],
        both_components_whole_parent_inverse_exact=True, all_nine_registered_final_stages_preserved=True,
        final_story_percent_contract=percent, all_four_story_archives_rechecked=True,
        dialogue_proof=dialogue_proof, surname_proof=name_proof, new_credit=0))
    print('Staged Rafael3649. Exact clean-input patch and whole predecessor inverse passed.')


def register():
    assert not RELEASE.exists() and not MANIFEST.exists() and not SURNAME_CONFIG.exists()
    parent, staged, startup, getters = map(load, (PARENT, STAGED, STARTUP, GETTERS))
    assert digest(PARENT) == staged['predecessor_release_sha256']
    assert digest(CONFIG) == staged['dialogue_release_config_sha256']
    assert digest(QUALIFICATION) == staged['qualification_sha256']
    assert not staged['own_registered_startup_pending']
    assert digest(STARTUP) == staged['own_registered_startup_sha256']
    assert digest(CANDIDATE) == staged['candidate_sha256'] == startup['candidate_sha256'] == getters['runtime']['candidate_sha256']
    assert getters['both_name_getters_exact_for_actors_35_65_68_186_203']
    assert startup['frames'] == 4001 and startup['ordinary_title_NewGame_Rafael_Castor_andopening_observed']
    assert digest(PATCH) == staged['patch_sha256'] and INVERSE_PATCH.read_bytes() == CANDIDATE.read_bytes()
    assert digest(REGISTRY) == digest(PARENT_REGISTRY) == staged['predecessor_registry_sha256']
    before = REGISTRY.read_bytes()
    registry = load(REGISTRY)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers']) == 114
    old_manifest = load(parent['manifest'])
    assert digest(parent['manifest']) == staged['predecessor_manifest_sha256']
    profile = deepcopy(registry['profiles'][staged['predecessor_profile']])
    predecessor = dict(profile=parent['profile'], candidate=parent['candidate'], candidate_sha256=parent['candidate_sha256'],
        manifest=parent['manifest'], manifest_sha256=parent['manifest_sha256'], registry=str(PARENT_REGISTRY),
        registry_sha256=digest(PARENT_REGISTRY), verified_nine_stage_output_reused=True)
    image = NdsImage.open(CANDIDATE)
    archive = image.read_file(ARCHIVE)
    assert digest_bytes(archive) == staged['target_SC0_sha256']
    blocks = IlnkContainer.parse(archive).blocks
    stored = load(STORED)
    styles = {row['id']: row for row in stored['style_records']}
    bindings = []
    for row in load(FINAL)['records']:
        ref = dict(row['planned_integrated_reference'])
        block, offset = blocks[row['block']], ref['offset']
        raw = bytes.fromhex(ref['exact_stored_hex'])
        assert block[offset:offset+len(raw)+1] == raw+b'\0' and all(row['review'].values())
        assert ref['target_archive_sha256'] == staged['target_SC0_sha256']
        if row['kind'] == 'typed-choice-label':
            at = ref['command_offset']
            assert int.from_bytes(block[at:at+2], 'little') == row['source_word']
            assert ref['source_index'] == row['source_index']
        elif row.get('native_object_kind') == '4100-style-alternative':
            entry = styles[row['id']]
            at, header = entry['final_command_offset'], bytes.fromhex(entry['final_header_hex'])
            assert ref['command_offset'] == at and block[at:at+len(header)] == header
            assert ref['source_style_indices'] == row['source_style_indices']
            ref['exact_command_header_hex'] = header.hex()
        else:
            assert block[offset-5:offset+1].hex() == row['source_complete_preamble_hex']
        keys = ('file_path', 'id', 'source_reference', 'source_hex', 'current_reference', 'current_hex', 'decision', 'finding', 'review')
        bindings.append({**{key: row[key] for key in keys}, 'registered_reference': ref})
    assert len(bindings) == len({(r['file_path'], r['id']) for r in bindings}) == 135
    binding_path = OUT/'exact_integrated_record_bindings.json'
    save(binding_path, dict(records=bindings, target_ROM_sha256=staged['candidate_sha256'], new_credit=0))
    save(SURNAME_CONFIG, dict(format='dk4-registered-Plett-Jacob-surname-stage-v1',
        exact_parent=predecessor, target_ARM9_sha256=staged['target_ARM9_sha256'],
        ownership=staged['surname_proof'], own_getters=str(GETTERS), own_getters_sha256=digest(GETTERS),
        changed_records=[dict(id='RAFAEL261_280_NAME_65', actor_ID=65, english='Plett Perrault'),
                         dict(id='RAFAEL261_280_NAME_68', actor_ID=68, english='Jacob Portunto')], new_credit=0))
    profile.update(verified_post_nine_stage_predecessor=predecessor, rafael_B261_B280_late_dialogue=str(CONFIG),
                   owned_Plett_Jacob_surnames=str(SURNAME_CONFIG),
                   note='Experimental registered four-route successor with Rafael B261–B280 and two source-owned surnames.')
    registry['profiles'][PROFILE] = profile
    pending = REGISTRY.with_name('release_stack.Rafael3649.pending.json')
    assert not pending.exists()
    save(pending, registry)
    result = deepcopy(old_manifest)
    result.update(profile=PROFILE, candidate_rom=str(CANDIDATE), candidate_sha256=staged['candidate_sha256'],
        release_stack_sha256=digest(pending), story_percent_contract=staged['final_story_percent_contract'])
    result['batches'].extend([str(FINAL), str(SURNAME_CONFIG)])
    result['changed_records'][ARCHIVE].extend(staged['dialogue_proof']['changed_records'])
    result['changed_records'].setdefault(ARM, []).extend(load(SURNAME_CONFIG)['changed_records'])
    result['checks'].update({CHECK_SC0: True, CHECK_NAMES: True})
    result['relocations'][ARCHIVE]['late_editorial:rafael-b261-b280'] = staged['dialogue_proof']
    result['relocations'].setdefault(ARM, {})['owned_Plett_Jacob_surnames'] = staged['surname_proof']
    result['Rafael3649_post_nine_stage_pipeline'] = dict(driver=__file__, driver_sha256=digest(__file__),
        predecessor=predecessor, qualification=str(QUALIFICATION), qualification_sha256=digest(QUALIFICATION),
        all_prior_stage_contracts_preserved=True, original_canonical_prefix_was_verified_and_reused=True,
        final_four_archive_percent_check_reexecuted=True)
    assert result['batches'][:692] == old_manifest['batches'] and len(result['batches']) == 694
    assert len(result['checks']) == 29 and all(result['checks'].values())
    assert REGISTRY.read_bytes() == before
    save(MANIFEST, result)
    os.replace(pending, REGISTRY)
    registered, previous = load(REGISTRY), load(PARENT_REGISTRY)
    assert set(registered['profiles']) == set(previous['profiles']) | {PROFILE}
    assert all(registered['profiles'][name] == value for name, value in previous['profiles'].items())
    assert all(registered[key] == value for key, value in previous.items() if key != 'profiles')
    assert digest(REGISTRY) == result['release_stack_sha256']
    save(RELEASE, {**staged, 'manifest': str(MANIFEST), 'manifest_sha256': digest(MANIFEST),
        'registry_sha256': digest(REGISTRY), 'predecessor': predecessor,
        'complete_stack_entries': 694, 'registered_manifest_entries': 694, 'passing_release_checks': 29,
        'accepted_layers': 114, 'all_eight_registered_final_stages_preserved': True,
        'owned_Francisca_name_field_verified': True, 'owned_Plett_Jacob_surnames_verified': True,
        'exact_all_integrated_references_bound': True, 'exact_record_bindings': str(binding_path),
        'exact_record_bindings_sha256': digest(binding_path), 'changed_internal_files': [ARCHIVE],
        'changed_components': [ARM], 'new_contextual_records': 135, 'prose_revisions': 118,
        'justified_retentions': 17, 'preparation': str(QUALIFICATION), 'preparation_sha256': digest(QUALIFICATION),
        'own_registered_name_getters': str(GETTERS), 'own_registered_name_getters_sha256': digest(GETTERS),
        'full_goal_complete': False})
    print('Registered Rafael3649 with 694 entries and 29 release checks. Main and all prior profiles are unchanged.')


from dk4tool.patch.grand_race_menu_release import sha as digest_bytes

if __name__ == '__main__':
    if sys.argv[1:] == ['--register']:
        register()
    else:
        assert not sys.argv[1:]
        stage()
