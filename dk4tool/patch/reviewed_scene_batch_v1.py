"""Pure registered integration of a fully reviewed and tested scene batch.

Keep the historical builder and renderer unchanged. Reconstruct the source-bound
blocks again, verify evidence and whole-image identities, then return one staged
NDS object to the existing atomic extension framework.
"""
from copy import deepcopy
import json
from pathlib import Path

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.reviewed_scene_rebuild import rebuild_block
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory


def load(path):
    return json.loads(Path(path).read_bytes())


def require(value, message):
    if not value:
        raise ValueError('Reviewed scene integration: ' + message)


def plan_release(image, baseline, config_path):
    conf = load(config_path)
    require(conf['format'] == 'dk4-reviewed-scene-release-v1', 'release format')
    for path, digest in conf['dependencies'].items():
        require(sha(Path(path).read_bytes()) == digest, 'changed dependency: ' + path)
    before = bytes(image.rom.save())
    baseline_before = bytes(baseline.rom.save())
    require(sha(before) == conf['parent_ROM_sha256'], 'complete ordered predecessor')
    require(sha(baseline.source.read_bytes()) == conf['canonical_ROM_sha256'], 'canonical baseline')
    require(sha(image.read_file('/__arm9__.bin')) == conf['pre_runtime_ARM9_sha256'], 'pre-runtime ARM9')
    clean_path = Path(conf['clean_ROM'])
    require(sha(clean_path.read_bytes()) == conf['clean_ROM_sha256'], 'clean Japanese input')
    clean_image = NdsImage.open(clean_path)
    approved, layout, reconstruction, native, loaders, actual = [load(conf[k]) for k in
        ['manuscript', 'plan', 'reconstruction', 'stored_native', 'loaders', 'actual']]
    validate_natural_dialogue_batch(approved)
    require(approved['translation_policy'] == 'natural-dialogue-v2', 'individual v2 review')
    require(approved['target_locale'] == 'en-US', 'American English locale')
    require(len(approved['records']) == conf['record_count'] == 224, 'complete batch membership')
    require(set(approved['blocks']) == set(conf['blocks']) == set(range(61, 71)), 'complete scene blocks')
    require(all(all(r['review'][k] is True for k in REQUIRED_REVIEW_GATES)
                for r in approved['records']), 'all five per-record gates')
    require(all(not any(t in r['english'] for t in ('{LB', '{ALIGN', '{PAD}', '\n'))
                for r in approved['records']), 'logical prose without authored wrapping')
    compiled = {r['id']: r for r in layout['records']}
    require(len(compiled) == len(approved['records']) and not layout['failures'], 'unique complete plans')
    for row in approved['records']:
        plan = compiled[row['id']]
        require(row['english'] == plan['logical_English'] and
                row['planned_English_markup'] == plan['English'], 'approved prose/plan binding')
        require(not any(i['severity'] in ('warning', 'error') for i in plan['base_QA']['issues']),
                'unresolved per-record layout diagnostic')
    require(native['complete_stored_pages'] == 229 and
            native['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass'] and
            native['fresh_relocated_native_relative_cases'] == 300, 'complete stored display/branch checks')
    require(native['unchanged_directly_viewed_planes_reused_exactly'] == 227 and
            native['changed_stored_planes_match_two_new_directly_viewed_pages'], 'visual review inheritance')
    require(loaders['fresh_whole_archive_loads_andcache_hits'] == 325 and
            loaders['fresh_parent_cases'] == 20 and loaders['exact_reused_parent_cases'] == 630 and
            loaders['prior_executed_parent_instructions_match_current_runtime'], 'native loaders')
    require(actual['total_frames'] == 43003 and len(actual['runs']) == 3 and
            len(actual['all15_contact_sheets_directly_viewed']) == 15 and
            actual['both_changed_glyph_records_observed_with_normal_I_andcomplete_text'] and
            actual['scene_ends_andfollowing_town_UI_visually_observed'], 'representative gameplay')
    require(len(actual['five_two_page_utterances_observed']) == 5 and
            actual['not_natural_optional_event_activation_ororiginal_location_chronology'] and
            actual['no_world_state_equivalence_orhardware_full_route_claim'], 'pagination and honest coverage')
    path = approved['file_path']
    require(path == '/data/SC1.DK4', 'owned route archive')
    archive = image.read_file(path)
    require(sha(archive) == reconstruction['source_archive_sha256'], 'complete source archive')
    container = IlnkContainer.parse(archive)
    clean_blocks = IlnkContainer.parse(clean_image.read_file(path)).blocks
    require(len(container.blocks) == len(clean_blocks) == 325, 'whole route block count')
    inventory, _, _ = scoped_inventory()
    blocks = list(container.blocks)
    changes = []
    for group in reconstruction['groups']:
        number = group['block']
        require(sha(blocks[number]) == group['current_sha256'] and
                sha(clean_blocks[number]) == group['clean_sha256'], 'source/current block identities')
        rows = [r for r in approved['records'] if r['block'] == number]
        target, proof = rebuild_block(image.read_file('/__arm9__.bin'), clean_blocks[number],
                                      blocks[number], rows, compiled, inventory)
        require(sha(target) == group['target_sha256'] and
                target == Path(group['target_block']).read_bytes(), 'tested block reconstruction')
        for key, value in proof.items():
            require(value == group[key], 'complete reconstruction map: ' + key)
        blocks[number] = target
        for row in proof['text_records']:
            changes.append(dict(id=row['id'], file_path=path, block=number,
                                old_offset=row['old_offset'], new_offset=row['new_offset'],
                                stored_sha256=sha(bytes.fromhex(row['stored_hex']))))
    result = IlnkContainer(blocks).to_bytes()
    require(sha(result) == reconstruction['target_archive_sha256'] and
            result == Path(reconstruction['target_archive']).read_bytes(), 'whole tested archive')
    require({i for i, (a, b) in enumerate(zip(container.blocks, blocks, strict=True)) if a != b}
            == set(conf['blocks']), 'only reviewed blocks changed')
    inverse = list(blocks)
    for number in conf['blocks']:
        inverse[number] = container.blocks[number]
    require(IlnkContainer(inverse).to_bytes() == archive, 'complete archive inverse')
    planned = deepcopy(image)
    planned.replace_file(path, result)
    require(sha(bytes(planned.rom.save())) == conf['target_ROM_sha256'], 'whole tested pre-runtime target')
    require([p for _, p, value in image.iter_files() if planned.read_file(p) != value] == [path] and
            all(planned.read_file(p) == value for p, value in image.iter_components()), 'unowned bytes')
    require(bytes(image.rom.save()) == before and bytes(baseline.rom.save()) == baseline_before,
            'pure planner leaves caller objects unchanged')
    return planned.rom, dict(manuscripts=[conf['manuscript']], changed_records=changes,
        files=[dict(file_path=path, source_sha256=sha(archive), target_sha256=sha(result), changed_records=changes)],
        one_complete_NDS_object_commit_after_all_gates=True,
        all224_source_controls_and392_commands60_relatives_preserved=True,
        native_pages=229, fresh_relative_cases=300, native_loads=325,
        parent_modes=dict(fresh=20, exact_reused=630), actual_frames=43003,
        representative_initialized_gameplay_not_natural_event_activation=True,
        canonical_stage_requires_registered_right_bound_runtime_layer=conf['right_bound_configuration'],
        no_completion_credit_orpromotion_granted=True, full_goal_complete=False)
