"""Pure source-bound correction of selected dialogue; preserve surrounding records."""
from copy import deepcopy
import json
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.sparse_scene_rebuild import rebuild_sparse_block
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory


def load(path):
    return json.loads(Path(path).read_bytes())


def require(value, message):
    if not value:
        raise ValueError('Sparse reviewed scene: ' + message)


def plan_release(image, baseline, config_path):
    conf = load(config_path)
    require(conf['format'] == 'dk4-reviewed-sparse-scene-release-v1', 'release format')
    for path, digest in conf['dependencies'].items():
        require(sha(Path(path).read_bytes()) == digest, 'changed dependency: ' + path)
    before, base_before = bytes(image.rom.save()), bytes(baseline.rom.save())
    require(sha(before) == conf['parent_ROM_sha256'], 'complete ordered predecessor')
    require(sha(baseline.source.read_bytes()) == conf['canonical_ROM_sha256'], 'canonical baseline')
    require(sha(Path(conf['clean_ROM']).read_bytes()) == conf['clean_ROM_sha256'], 'clean input')
    approved, proof, native, actual = [load(conf[k]) for k in ['manuscript', 'reconstruction', 'native', 'actual']]
    validate_natural_dialogue_batch(approved)
    require(approved['translation_policy'] == 'natural-dialogue-v2' and len(approved['records']) == 1,
            'one individually reviewed correction')
    row = approved['records'][0]
    require(row['id'] == proof['changed_ID'] == 'DK4_MES_B43_R0017', 'reviewed identity')
    require(row['compiled_hex'] == proof['change']['compiled_hex'], 'reviewed compiled bytes')
    require(native['changed_parent_cases'] == 2 and native['native_whole_loads_andcache_hits'] == 343 and
            len(native['new_record_catalogue_miss_cases']) == 8, 'native lookup/loader coverage')
    require(actual['normal_F_I_andactual_Rafael_expansion_observed'] and
            actual['complete_four_rows_Julio_header_andfollowing_town_UI_observed'] and
            actual['cold_boot'] and not actual['savestate_loaded'], 'actual formatting and name substitution')
    path, number = row['file_path'], row['block']
    require(path == '/data/SC0.DK4' and number == 43, 'source scene ownership')
    archive = image.read_file(path)
    require(sha(archive) == proof['source_archive_sha256'], 'source archive')
    bank = IlnkContainer.parse(archive).blocks
    clean = IlnkContainer.parse(NdsImage.open(conf['clean_ROM']).read_file(path)).blocks
    inventory, _, _ = scoped_inventory()
    target, planned_proof = rebuild_sparse_block(image.read_file('/__arm9__.bin'), clean[number],
        bank[number], path, number, {row['id']: proof['change']}, inventory)
    require(planned_proof == proof['block_proof'] and sha(target) == proof['target_block_sha256'],
            'complete tested sparse reconstruction')
    blocks = list(bank)
    blocks[number] = target
    result = IlnkContainer(blocks).to_bytes()
    require(sha(result) == proof['target_archive_sha256'], 'whole tested target archive')
    require([i for i, (a, b) in enumerate(zip(bank, blocks, strict=True)) if a != b] == [number],
            'only selected block changes')
    inverse = list(blocks)
    inverse[number] = bank[number]
    require(IlnkContainer(inverse).to_bytes() == archive, 'whole archive inverse')
    planned = deepcopy(image)
    planned.replace_file(path, result)
    require(sha(bytes(planned.rom.save())) == conf['target_ROM_sha256'], 'whole pre-runtime target')
    require([p for _, p, v in image.iter_files() if planned.read_file(p) != v] == [path] and
            all(planned.read_file(p) == v for p, v in image.iter_components()), 'unowned bytes unchanged')
    require(bytes(image.rom.save()) == before and bytes(baseline.rom.save()) == base_before,
            'caller objects unchanged')
    text = next(r for r in planned_proof['text_records'] if r['id'] == row['id'])
    changes = [dict(id=row['id'], file_path=path, block=number,
                    old_offset=text['old_offset'], new_offset=text['new_offset'])]
    return planned.rom, dict(manuscripts=[conf['manuscript']], changed_records=changes,
        files=[dict(file_path=path, source_sha256=sha(archive), target_sha256=sha(result), changed_records=changes)],
        one_complete_NDS_object_commit_after_all_gates=True,
        unselected11_speech_records_andall_nontext_commands_preserved=True,
        entire_ARM9_fonts_names_andright_bound_layer_unchanged=True,
        actual_normal_glyphs_Rafael_substitution_andtown_return_observed=True,
        new_editorial_completion_credit=0, full_goal_complete=False)
