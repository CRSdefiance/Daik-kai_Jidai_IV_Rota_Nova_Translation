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
    require(conf['format'] == 'dk4-reviewed-scene-release-v2', 'release format')
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
    require(len(approved['records']) == conf['record_count'] and conf['record_count'] > 0, 'complete batch membership')
    require(set(approved['blocks']) == set(conf['blocks']) == {g['block'] for g in reconstruction['groups']} and bool(conf['blocks']), 'complete scene blocks')
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
    require(native['complete_stored_pages'] == conf['native_pages'] and
            native['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass'] and
            native['fresh_relocated_native_relative_cases'] == conf['relative_cases'], 'complete stored display/branch checks')
    require(native['all_stored_planes_equal_directly_viewed_compiled_planes'], 'exact visual review inheritance')
    visual = load(conf['visual_review'])
    require(visual['all_final_pages_directly_viewed_or_exact_plane_reuse'] and
            visual['final_pages'] == conf['native_pages'], 'complete readable page review')
    require(loaders['fresh_whole_archive_loads_andcache_hits'] == 325 and
            loaders['fresh_parent_cases'] == 2 * len(conf['blocks']) and
            loaders['exact_reused_parent_cases'] == 650 - 2 * len(conf['blocks']) and
            loaders['prior_executed_parent_instructions_match_current_runtime'], 'native loaders')
    require(actual['total_frames'] == conf['actual_frames'] and
            len(actual['runs']) == conf['actual_runs'] and
            len(actual['all_review_sheets_directly_viewed']) == conf['actual_sheets'] and
            actual['representative_progressive_FE_pagination_andscene_transition_observed'] and
            actual['no_new_blank_box_lost_glyph_orportrait_issue_seen_in_reviewed_samples'] and
            actual['no_natural_event_activation_original_location_earned_chronology_fullroute_orhardware_claim'],
            'representative gameplay and honest coverage')
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
        all_source_controls_commands_relatives_andunowned_bytes_preserved=True,
        native_pages=conf['native_pages'], fresh_relative_cases=conf['relative_cases'], native_loads=325,
        parent_modes=dict(fresh=2*len(conf['blocks']), exact_reused=650-2*len(conf['blocks'])), actual_frames=conf['actual_frames'],
        representative_initialized_gameplay_not_natural_event_activation=True,
        canonical_stage_requires_registered_right_bound_runtime_layer=conf['right_bound_configuration'],
        no_completion_credit_orpromotion_granted=True, full_goal_complete=False)
