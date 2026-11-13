"""Register complete individually reviewed owner groups after all prior name stages."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.owned_name_fields_v3 import plan_arm9_name_fields
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load


def plan_release(image, config_path):
    config = load(config_path)
    def require(ok, message):
        if not ok:
            raise ValueError('Registered grouped name fields: ' + message)
    require(config['format'] == 'dk4-registered-owned-name-fields-v4', 'registered group schema')
    for path, digest in config['dependencies'].items():
        require(sha(Path(path).read_bytes()) == digest, 'changed dependency: ' + path)
    require(sha(bytes(image.rom.save())) == config['parent_ROM_sha256'], 'exact complete predecessor')
    clean_path = Path(config['clean_ROM'])
    require(sha(clean_path.read_bytes()) == config['clean_ROM_sha256'], 'clean Japanese input')
    doc, proposal, native, actual = [load(config[k]) for k in ['manuscript', 'proposal', 'native', 'actual']]
    validate_natural_dialogue_batch(doc)
    require(doc['format'] == 'dk4-scoped-owned-name-fields-review-v3', 'all owner review schema')
    require(native['offline_visual_approved'] and not native['direct_view_pending']
        and native['proposal_sha256'] == sha(Path(config['proposal']).read_bytes()), 'reviewed exact native proposal')
    owners = {(o['actor'], o['column']): (field, o) for field in proposal['fields'] for o in field['owners']}
    require(len(owners) == len(doc['records']) == len(config['actual_policy']) == 3
        and len(proposal['fields']) == 2, 'two spans and all three reviewed owners')
    require({(r['reviewed_owner']['actor'], r['reviewed_owner']['column']) for r in doc['records']} == set(owners), 'exact whole owner membership')
    policies = {p['actor']: p for p in config['actual_policy']}
    versions = {v['version']: v['names']['rows'] for v in native['versions']}
    changes = []
    for row in doc['records']:
        owner = row['reviewed_owner']
        actor, column = owner['actor'], owner['column']
        field, expected = owners[actor, column]
        require(row['owned_field'] == field and owner == expected
            and row['physical_field_group_actor'] == field['actor'], 'individual source/group binding')
        policy = policies[actor]
        proposed = {r['consumer']: r['text'] for r in versions['proposed'] if r['actor_ID'] == actor}
        current = {r['consumer']: r['text'] for r in versions['current'] if r['actor_ID'] == actor}
        require(row['english'] == proposed['full-catalogue'] == policy['full_name'], 'reviewed complete full spelling')
        require(policy['kind'] == 'unchanged-progressive-middle-component' and column == 8
            and current['progressive-nameplate'] == proposed['progressive-nameplate']
            and row['full_catalogue_UI_unvisited'] and actual['all_three_changed_full_catalogue_UIs_unvisited'],
            'honest distinct full-name-only offline coverage')
        changes.append(f'ACTOR{actor}_NAME_COLUMN{column}_LOCALIZED')
    arm, proof = plan_arm9_name_fields(image.read_file('/__arm9__.bin'), proposal, NdsImage.open(clean_path).read_file('/__arm9__.bin'))
    require(proof == native['name_data_plan'] and sha(arm) == config['target_ARM9_sha256'], 'frozen complete native inverse and target')
    require(arm == Path(native['proposed_ARM9']).read_bytes() and proof['owned_span_bytes'] == 4, 'exact tested four-byte data')
    return arm, dict(**proof, changed_records=changes, registered_source_reviewed_metadata_only=True,
                     all_shared_owners_individually_reviewed=True, new_credit=0, final_ROM_sha256=config['target_ROM_sha256'])
