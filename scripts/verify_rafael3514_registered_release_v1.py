"""Bind the final four-route ROM to every reviewed record and its own startup."""
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.build_registered_rafael3514_Francisca_v1 import CHECK_KEY, CONFIG, FIELD_KEY, PROFILE, REGISTRY
from scripts.prepare_rafael3514_Francisca_field_v1 import digest
from scripts.verify_release_baseline import REQUIRED_MENU_TEXT, REQUIRED_OPTIONS_TEXT


ROOT = Path('work/rafael3514_Francisca_release_v1')
PREPARATION = Path('work/Rafael3514_dialogue_registered_resume_v1_20261106/registered_preparation.json')
PRIOR = Path('work/Rafael3222_extended_release_verified_v1_20261106/registered_release_verification.json')
RELEASE = ROOT/'registered_release_verification.json'
BINDINGS = ROOT/'exact_integrated_record_bindings.json'


def main():
    assert not RELEASE.exists() and not BINDINGS.exists()
    receipt = ROOT/'registered_name_stage_verification.json'
    getter_path = ROOT/'own_registered_name_getters_v1.json'
    stage, getters, prep, prior = map(load, (receipt, getter_path, PREPARATION, PRIOR))
    candidate, patch = Path(stage['candidate']), Path(stage['patch'])
    startup_path, manifest_path = Path(stage['own_registered_startup']), Path(stage['manifest'])
    manifest, startup, field = map(load, (manifest_path, startup_path, CONFIG))
    assert digest(candidate) == stage['candidate_sha256'] == getters['runtime']['candidate_sha256']
    assert digest(manifest_path) == stage['manifest_sha256'] and digest(startup_path) == stage['own_registered_startup_sha256']
    assert startup['candidate_sha256'] == stage['candidate_sha256'] and startup['frames'] == 4001
    assert startup['cold_boot'] and not startup['savestate'] and not startup['callback_errors']
    assert startup['actual_captain_getter'] == startup['actual_route_word'] == 0
    assert getters['both_name_getters_exact_for_actors_35_and_186']
    assert digest(REGISTRY) == stage['registry_sha256'] == manifest['release_stack_sha256']
    registry = load(REGISTRY)
    assert len(registry['accepted_layers']) == 114 and registry['profiles'][PROFILE][FIELD_KEY] == str(CONFIG)
    assert len(manifest['batches']) == 692 and len(manifest['checks']) == 27
    assert all(manifest['checks'].values()) and manifest['checks'][CHECK_KEY]
    assert not stage['own_registered_startup_pending'] and stage['clean_input_patch_byte_exact']
    rebuilt = ROOT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
    assert digest(patch) == stage['patch_sha256'] and rebuilt.read_bytes() == candidate.read_bytes()

    image, predecessor = map(NdsImage.open, (candidate, prior['candidate']))
    assert digest(prior['candidate']) == prior['candidate_sha256']
    assert digest(prior['canonical_base']) == prior['canonical_sha256'] == manifest['base_sha256']
    assert digest(prior['manifest']) == prior['manifest_sha256']
    assert [path for _, path, data in predecessor.iter_files() if image.read_file(path) != data] == ['/data/SC0.DK4']
    assert [path for path, data in predecessor.iter_components() if image.read_file(path) != data] == ['/__arm9__.bin']
    assert image.read_file('/__arm9__.bin') == Path(field['tested_ARM9']).read_bytes()
    arm = image.read_file('/__arm9__.bin')
    assert all(text in arm for text in REQUIRED_MENU_TEXT) and any(text in arm for text in REQUIRED_OPTIONS_TEXT)
    resource = image.read_file('/data/SC0.DK4')
    old, new = (IlnkContainer.parse(data).blocks for data in (predecessor.read_file('/data/SC0.DK4'), resource))
    assert len(old) == len(new)
    blocks = [i for i, (a,b) in enumerate(zip(old, new, strict=True)) if a != b]
    conf = load(prep['configs'][0])
    assert blocks == conf['blocks'] and len(blocks) == 18 and not ({244,246} & set(blocks))
    reconstruction = load(conf['reconstruction'])
    assert resource == Path(reconstruction['target_archive']).read_bytes()
    assert digest(reconstruction['target_archive']) == reconstruction['target_archive_sha256']
    doc = load(conf['manuscript'])
    stored = load(conf['stored_native'])
    styles = {row['id']: row for row in stored['style_records']}
    bindings = []
    for row in doc['records']:
        ref = dict(row['planned_integrated_reference'])
        block = new[row['block']]
        offset = ref['offset']
        raw = bytes.fromhex(ref['exact_stored_hex'])
        assert block[offset:offset+len(raw)+1] == raw+b'\0' and all(row['review'].values())
        if row['kind'] == 'typed-choice-label':
            command = ref['command_offset']
            assert int.from_bytes(block[command:command+2], 'little') == row['source_word']
            assert ref['source_index'] == row['source_index']
        elif row.get('native_object_kind') == '4100-style-alternative':
            saved = styles[row['id']]
            command = ref['command_offset']
            header = bytes.fromhex(saved['final_header_hex'])
            assert saved['final_command_offset'] == command and block[command:command+len(header)] == header
            assert ref['source_style_indices'] == row['source_style_indices']
            ref['exact_command_header_hex'] = header.hex()
        else:
            assert block[offset-5:offset+1].hex() == row['source_complete_preamble_hex']
        assert ref['target_archive_sha256'] == reconstruction['target_archive_sha256']
        keys = ('file_path', 'id', 'source_reference', 'source_hex', 'current_reference', 'current_hex',
                'decision', 'finding', 'review')
        bindings.append({**{key:row[key] for key in keys}, 'registered_reference':ref})
    assert len(bindings) == len({(r['file_path'],r['id']) for r in bindings}) == 292
    save(BINDINGS, dict(records=bindings, target_ROM_sha256=stage['candidate_sha256'], new_credit=0))
    save(RELEASE, {**stage, 'parent': prior['candidate'], 'parent_sha256':prior['candidate_sha256'],
        'canonical_base':prior['canonical_base'], 'canonical_sha256':prior['canonical_sha256'],
        'complete_stack_entries':692, 'all_eight_registered_final_stages_preserved':True,
        'owned_Francisca_name_field_verified':True, 'exact_all_integrated_references_bound':True,
        'exact_record_bindings':str(BINDINGS), 'exact_record_bindings_sha256':digest(BINDINGS),
        'changed_internal_files':['/data/SC0.DK4'], 'changed_components':['/__arm9__.bin'],
        'only_owned_SC0_blocks_changed':blocks, 'target_SC0_sha256':reconstruction['target_archive_sha256'],
        'target_ARM9_sha256':field['target_ARM9_sha256'], 'new_contextual_records':292, 'prose_revisions':244,
        'justified_retentions':48, 'preparation':str(PREPARATION), 'preparation_sha256':digest(PREPARATION),
        'exact_clean_reconstruction':str(rebuilt), 'own_registered_name_getters':str(getter_path),
        'own_registered_name_getters_sha256':digest(getter_path), 'new_credit':0, 'full_goal_complete':False})
    print('Verified the 692-entry cumulative candidate, 292 exact integrated records, clean patch, and own startup.')


if __name__ == '__main__':
    main()
