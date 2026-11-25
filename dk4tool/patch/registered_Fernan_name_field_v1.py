"""One source-owned name field after the unchanged seven-stage cumulative pipeline."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load


def plan_release(image, config_path):
    conf = load(config_path)
    def need(ok, message):
        if not ok:
            raise ValueError('Registered Fernan field: ' + message)
    need(conf['format'] == 'dk4-registered-Fernan-name-field-v1', 'schema')
    for path,digest in conf['dependencies'].items():
        need(sha(Path(path).read_bytes()) == digest, 'changed dependency: ' + path)
    before = bytes(image.rom.save())
    need(sha(before) == conf['parent_ROM_sha256'], 'exact ordered seven-stage predecessor')
    clean_path = Path(conf['clean_ROM'])
    need(sha(clean_path.read_bytes()) == conf['clean_ROM_sha256'], 'clean Japanese input')
    doc, proposal, native, tested, dependencies, pixels, visual = [load(conf[k]) for k in
        ['manuscript','proposal','native','rebased_plan','dependency_qualification','actual_pixels','actual_visual']]
    validate_natural_dialogue_batch(doc)
    rows = [r for r in doc['records'] if r['actor_ID'] == 35]
    need(len(rows) == len(proposal['fields']) == 1, 'one reviewed source identity andexclusive field')
    row, field = rows[0], proposal['fields'][0]
    need(row['proposed_owned_field'] == field and row['english'] == 'Fernan Silveira'
         and field['actor'] == 35 and field['column'] == 0 and field['kind'] == 'latin-width-normalization'
         and field['current_text'] == 'Ｆernan' and field['target_text'] == 'Fernan', 'only source-bound F width correction')
    need(native['original_progressive_andfull_name_getters_pass'] and len(native['negative_cases_rejected']) == 8
         and len(native['planes']) == 4, 'both native getters/four native planes/eight rejected alias cases')
    need(dependencies['Fernan_fixed_field_commutes_with_all_six_registered_data_spans']
         and dependencies['Fernan_native_name_getters_planes_andnegative_cases_reused_not_reexecuted'], 'explicit current-parent exact native reuse')
    need(proposal['runtime'] == dependencies['runtime'] and sha(image.read_file('/__arm9__.bin')) == proposal['runtime']['ARM9_sha256'], 'exact current ARM9 dependency')
    need(visual['all_six_sheets_directly_viewed'] and pixels['all_complete_native_body_andheader_planes_andblank_guards_match'], 'direct approved actual headers')
    headers = [h for h in pixels['headers'] if h['actor_ID'] == 35]
    need(headers and all(h['text'] == row['english'] and h['complete_name_glyphs_andblank_guards_exact'] for h in headers), 'complete actual normal-F progressive header')
    need(doc['full_catalogue_UI_andglobal207_review_still_open'], 'honest full catalogue scope')
    arm, proof = plan_arm9_name_fields(image.read_file('/__arm9__.bin'), proposal, NdsImage.open(clean_path).read_file('/__arm9__.bin'))
    need(proof == tested and sha(arm) == conf['target_ARM9_sha256'], 'exact rebased ownership plan andtarget')
    prior = native['name_data_plan']
    need({k:v for k,v in proof.items() if k not in ['parent_ARM9_sha256','target_ARM9_sha256']} ==
         {k:v for k,v in prior.items() if k not in ['parent_ARM9_sha256','target_ARM9_sha256']}, 'all ownership/reference/inverse proofs preserved')
    need(arm == Path(conf['tested_ARM9']).read_bytes() and proof['owned_span_bytes'] == 7 and proof['changed_bytes'] == 6, 'tested exclusive seven-byte slot')
    result = deepcopy(image)
    result.replace_file('/__arm9__.bin',arm)
    need(sha(bytes(result.rom.save())) == conf['target_ROM_sha256'], 'exact complete final target')
    need(all(result.read_file(p) == v for _,p,v in image.iter_files())
         and [p for p,v in image.iter_components() if result.read_file(p) != v] == ['/__arm9__.bin'], 'all other files/components unchanged')
    inverse = deepcopy(result)
    inverse.replace_file('/__arm9__.bin',image.read_file('/__arm9__.bin'))
    need(bytes(inverse.rom.save()) == before and bytes(image.rom.save()) == before, 'complete serialized parent inverse andpure caller')
    return arm, dict(**proof,changed_records=['ACTOR35_NAME_COLUMN0_F_WIDTH_LOCALIZED'],
        registered_source_reviewed_metadata_only=True,complete_actual_progressive_header_verified=True,
        native_full_catalogue_getter_verified_butfull_catalogue_UI_unvisited=True,new_credit=0,
        final_ROM_sha256=conf['target_ROM_sha256'])
