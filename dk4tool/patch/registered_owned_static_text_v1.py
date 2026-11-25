"""Apply only the separately qualified Abkhaz/Elysion fixed-slot data stage."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_static_labels_v1 import plan_static_labels
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load


def plan_release(image, config_path):
    conf = load(config_path)
    def need(value, message):
        if not value:
            raise ValueError('Registered static labels: ' + message)
    need(conf['format'] == 'dk4-registered-owned-static-text-v1', 'schema')
    for path, digest in conf['dependencies'].items():
        need(sha(Path(path).read_bytes()) == digest, 'changed dependency: ' + path)
    before = bytes(image.rom.save())
    need(sha(before) == conf['parent_ROM_sha256'], 'complete ordered predecessor')
    clean_path = Path(conf['clean_ROM'])
    need(sha(clean_path.read_bytes()) == conf['clean_ROM_sha256'], 'clean Japanese input')
    doc, native, actual = map(load, [conf['manuscript'], conf['native'], conf['actual']])
    validate_natural_dialogue_batch(doc)
    need(doc['all_five_gates_pass_in_scoped_context'] and len(doc['records']) == 39, 'all scoped name/term decisions')
    need(native['all_native_getter_copy_full_characters_bounds_canaries_andparent_inverse_pass'], 'native ownership/copy/font proof')
    need(actual['all_required_distinct_display_cases_match'] and len(actual['static_source_envelopes']) == 2,
        'completed representative gameplay and bounded static-data scope')
    need(all(r['complete_target_advance_including_flush'] <= r['clean_advance'] and r['actual_widget_unvisited']
        for r in actual['static_source_envelopes']), 'honest compact source-envelope scope')
    arm, proof = plan_static_labels(image.read_file('/__arm9__.bin'), load(conf['proposal']),
        NdsImage.open(clean_path).read_file('/__arm9__.bin'))
    need(proof == native['complete_owned_data_plan'], 'exact tested complete data plan')
    target = deepcopy(image)
    target.replace_file('/__arm9__.bin', arm)
    need(sha(bytes(target.rom.save())) == conf['target_ROM_sha256'], 'complete tested target')
    need(all(target.read_file(p) == value for _, p, value in image.iter_files()), 'all unowned files')
    need([p for p, value in image.iter_components() if target.read_file(p) != value] == ['/__arm9__.bin'], 'only ARM9 data component')
    need(bytes(image.rom.save()) == before, 'pure caller preservation')
    records = [dict(id=r['id'], file_path='/__arm9__.bin', physical_offset=r['physical_offset'],
        owned_prefix_bytes=r['owned_prefix_bytes'], old_hex=r['parent_prefix_hex'], new_hex=r['target_prefix_hex'],
        source_typed_pointer_field=r['source_typed_pointer_field']) for r in proof['fields']]
    return arm, dict(changed_records=records, complete_owned_data_plan=proof,
        complete_parent_target_inverse_andall_unowned_bytes_exact=True,
        static_city_andship_widgets_unvisited=True, no_new_dialogue_credit_orpromotion=True)
