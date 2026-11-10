"""Apply only the proven Francisca width correction after the eight-stage build."""
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load


def require(condition, message):
    if not condition:
        raise ValueError('Registered Francisca field: ' + message)


def plan_release(image, config_path):
    conf = load(config_path)
    require(conf['format'] == 'dk4-registered-Francisca-name-field-v1', 'schema')
    for path, expected in conf['dependencies'].items():
        require(sha(Path(path).read_bytes()) == expected, 'changed dependency: ' + path)
    before = bytes(image.rom.save())
    require(sha(before) == conf['parent_ROM_sha256'], 'exact ordered eight-stage predecessor')
    clean = Path(conf['clean_ROM'])
    require(sha(clean.read_bytes()) == conf['clean_ROM_sha256'], 'exact clean Japanese source')
    names, proposal, native, pixels, visual, fixture = [
        load(conf[key]) for key in ('manuscript', 'proposal', 'native', 'actual_pixels', 'actual_visual', 'fixture')
    ]
    validate_natural_dialogue_batch(names)
    actor = next((row for row in names['records'] if row['actor_ID'] == 186), None)
    require(actor and all(actor['review'].values()) and actor['english'] == 'Francisca'
            and actor['exclusive_field_native_and_progressive_fixture_pass'], 'reviewed actor 186 spelling')
    require(len(proposal['fields']) == 1, 'one exclusively owned field')
    field = proposal['fields'][0]
    require((field['actor'], field['column'], field['kind'], field['current_text'], field['target_text']) ==
            (186, 0, 'latin-width-normalization', 'Ｆrancisca', 'Francisca'), 'scope of the F correction')
    require(native['proposal_sha256'] == sha(Path(conf['proposal']).read_bytes())
            and native['original_progressive_andfull_name_getters_pass']
            and len(native['planes']) == 4 and len(native['negative_cases_rejected']) == 8,
            'exact proposed name getters, planes and ownership rejections')
    proposed = native['versions'][1]['names']['rows']
    require({row['consumer'] for row in proposed} == {'progressive-nameplate', 'full-catalogue'}
            and all(row['actor_ID'] == 186 and row['text'] == 'Francisca' for row in proposed),
            'both consumers return the approved name')
    require(fixture['verified_Francisca_field_applied']
            and fixture['Francisca_name_proof_sha256'] == sha(Path(conf['native']).read_bytes())
            and pixels['evidence'][conf['fixture']] == sha(Path(conf['fixture']).read_bytes())
            and visual['evidence'][conf['actual_pixels']] == sha(Path(conf['actual_pixels']).read_bytes())
            and visual['all_actual_pages_and_menus_directly_viewed']
            and pixels['all_complete_native_body_andheader_planes_andblank_guards_match'],
            'exact emulator fixture and inspected pages')
    headers = [row for row in pixels['headers'] if row['expected_actor_ID'] == 186]
    require(headers and all(row['text'] == 'Francisca' and row['complete_name_glyphs_andblank_guards_exact']
                            for row in headers), 'complete corrected nameplate observed')
    parent_arm = image.read_file('/__arm9__.bin')
    target, proof = plan_arm9_name_fields(parent_arm, proposal, NdsImage.open(clean).read_file('/__arm9__.bin'))
    require(proof == native['name_data_plan'] and sha(target) == conf['target_ARM9_sha256']
            and target == Path(conf['tested_ARM9']).read_bytes() and proof['owned_span_bytes'] == 10,
            'exact native-tested field plan and inverse')
    copy = NdsImage.open(conf['parent_ROM'])
    require(bytes(copy.rom.save()) == before, 'exact immutable predecessor image')
    copy.replace_file('/__arm9__.bin', target)
    require(sha(bytes(copy.rom.save())) == conf['target_ROM_sha256']
            and all(copy.read_file(path) == value for _, path, value in image.iter_files())
            and [path for path, value in image.iter_components() if copy.read_file(path) != value] == ['/__arm9__.bin'],
            'complete target and component ownership')
    copy.replace_file('/__arm9__.bin', parent_arm)
    require(bytes(copy.rom.save()) == before and bytes(image.rom.save()) == before, 'complete parent inverse')
    return target, {**proof, 'changed_records': ['ACTOR186_NAME_COLUMN0_F_WIDTH_LOCALIZED'],
        'native_full_catalogue_getter_verified_but_UI_unvisited': True,
        'complete_actual_progressive_header_verified': True, 'new_credit': 0,
        'final_ROM_sha256': conf['target_ROM_sha256']}
