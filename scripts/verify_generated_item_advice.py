"""Complete generated-item names/paragraphs, termination and native parent crops."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.patch.generated_item_advice_research import transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import machine_for
from scripts.execute_scene_caption_raster import execute
from scripts.probe_common_itcm_arena_reservation import initialize as arenas
from scripts.probe_common_itcm_arena_reservation import verify as arena_bounds
from scripts.probe_item_counter_canvas import verify as counter_canvas
from scripts.probe_item_lookup_abi import verify as lookup_abi
from scripts.probe_item_native_initialization import initialize_item_object
from scripts.probe_item_parent_crops import verify as parent_crops
from scripts.probe_persistent_name_arm7_boot_overlap import execute as boot
from scripts.probe_promotional_item_full import verify as full_promotional
from scripts.verify_item_interface_research import verify_page
from scripts.verify_item_parent_layout import EXPECTED, compose


def main():
    old = Path('work/analysis/item_parent_layout_research_arm9.bin').read_bytes()
    image = NdsImage.open('out/all_routes_combined_v158_candidate.nds')
    common, font = image.read_file('/COMMON/MESFILE.DK4'), image.read_file('/GRP/KANJI.FNT')
    old_plan = json.loads(Path('work/analysis/item_interface_plan.json').read_text(encoding='utf-8'))
    source, plan = transform(old, common, old_plan)
    if source != Path('work/analysis/generated_item_advice_research_arm9.bin').read_bytes():
        raise ValueError('Saved generated-item repair differs')
    before = execute(old, 'fixture', item_page='main', item_case=(0, 4), surface_size=(240, 96),
                     kanji_font=font, item_resource_index=198, item_common=common)
    before_lines = [r for r in before['item_draws'] if r['y'] >= 36 and r['y'] < 84]
    if len(before_lines) <= 1 or not any(ord(c) > 126 for r in before_lines for c in r['text']):
        raise ValueError('Original generated-item continuation defect was not reproduced')
    seeds = [0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF] + list(range(2, 34))
    full_cases = [full_promotional(source, seed) for seed in seeds]
    machine = machine_for(source)
    context = machine.context_save()
    full_promotional(source, 0, machine)
    machine.context_restore(context)
    metadata = [initialize_item_object(source, machine, index) for index in range(218)]
    seen, chosen = set(), []
    for case in full_cases:
        additions = set(case['selected_default_indices']) - seen
        if additions:
            chosen.append(case['seed'])
            seen.update(additions)
    if seen != set(range(188, 198)):
        raise ValueError('Full native seed/name coverage misses a source name')
    longest = max((row['name_byte_length'], case['seed'], row['index'])
                  for case in full_cases if case['seed'] in chosen for row in case['names'][10:])
    parent = parent_crops(source)
    if [(r['source_origin'], r['size'], r['destination_origin']) for r in parent['requests']] != EXPECTED:
        raise ValueError('Generated-item repair changes verified parent positions')
    cases, panels = [], []
    destination = Path('work/qa/generated_item_advice_native')
    destination.mkdir(parents=True, exist_ok=True)
    for seed in chosen:
        for index in range(198, 218):
            for page in ('main', 'standalone'):
                for mode in (4, 16):
                    native = verify_page(source, plan, page, (0, 4 if page == 'main' else 1), font, mode,
                                         item_index=index, common=common, promotional_seed=seed)
                    lines = [r for r in native['item_draws'] if r['y'] >= (36 if page == 'main' else 24)
                             and r['y'] < 84]
                    if len(lines) != 1 or lines[0]['text'] != 'Map fragment. Collect all four.':
                        raise ValueError('Generated map contains junk, extra continuations or missing prose')
                    pixels = native['pixels']
                    if page == 'main':
                        pixels, _cells = compose(native, parent['requests'])
                    cases.append({'seed': seed, 'index': index, 'page': page, 'mode': mode,
                                  'draws': native['item_draws'], 'pixels_sha256': sha(native['pixels']),
                                  'complete_glyphs_pixels_bounds_native_metadata_and_COMMON_pass': True,
                                  'native_parent_complete_glyph_pixels_pass': page == 'main'})
                    if mode == 16 and ((seed == chosen[0] and index in (198, 201, 214, 217))
                                       or (seed, index) == longest[1:]):
                        panel = Image.new('RGB', (256, 192))
                        panel.putdata([(255, 255, 255) if c == 0 else (128, 128, 128) if c == 14 else (0, 0, 0)
                                       for c in struct.unpack('<49152H', pixels)])
                        panel = panel.resize((768, 576), Image.Resampling.NEAREST)
                        panel.save(destination / f'panel_{len(panels)}.png')
                        panels.append((f'{page}; generated index {index}; seed {seed}', panel))
        print(f'{len(cases)} generated map native raster cases pass', flush=True)
    regressions = []
    for index in (5, 22, 151, 188, 197):
        for page in ('main', 'standalone'):
            for mode in (4, 16):
                native = verify_page(source, plan, page, (0, 4 if page == 'main' else 1), font, mode,
                                     item_index=index, common=common)
                if page == 'main':
                    compose(native, parent['requests'])
                regressions.append({'index': index, 'page': page, 'mode': mode, 'pixels_sha256': sha(native['pixels'])})
    sheet = Image.new('RGB', (1552, 604 * ((len(panels) + 1) // 2)), 'white')
    draw = ImageDraw.Draw(sheet)
    for n, (label, panel) in enumerate(panels):
        x, y = 8 + n % 2 * 776, n // 2 * 604
        draw.text((x, y + 2), label + '; native text; physical art/background pending', fill='black')
        sheet.paste(panel, (x, y + 24))
    sheet.save(destination / 'native_sheet.png')
    payload = bytes(MainCodeFile(source, 0x02000000).sections[3].data[:-48])
    loading = boot(source, bytes(image.rom.arm7), image.rom.arm7RamAddress, True, payload)
    if (loading['arm7_source_changed_bytes_after_arm9_autoload']
            or not all(r['matches_original'] for r in loading['arm7_native_loaded_sections'])
            or not all(loading[k] for k in ('repaired_pool_matches_complete_payload', 'repair_returns_with_stack_preserved',
                                            'actual_startup_call_preserves_r0_r3'))
            or not all(loading['SDK_staged_code_cache_line_coverage'][k]
                       for k in ('all_instruction_lines_selected', 'all_data_lines_selected'))
            or not loading['late_copy_cache_model']['worst_case_dirty_data_and_stale_instruction_model_visible']):
        raise ValueError('Generated map payload fails native startup/cache/ARM7 checks')
    allocation = arenas(source)
    resident_bounds = arena_bounds(source, 0x01FFA000)
    if allocation['low'][0] != plan['final_pool_span'][1]:
        raise ValueError('Complete generated-item payload is not reserved by the native arena')
    report = {'status': 'pass-native-generated-map-description-repair', 'target_arm9_sha256': sha(source),
              'original_defect': {'target_arm9_sha256': sha(old), 'index': 198,
                                  'description_draw_count': len(before_lines),
                                  'extra_non_ASCII_continuations_reproduced': True},
              'full_native_initializers': full_cases, 'all_218_native_metadata_initializers': metadata,
              'generated_raster_seeds': chosen, 'generated_rasters': cases, 'static_default_regressions': regressions,
              'lookup_ABI': lookup_abi(source, plan), 'parent': parent, 'boot': loading,
              'arena': allocation, 'resident_arena': resident_bounds, 'counter_canvas': counter_canvas(source),
              'visual_review': {'complete': False, 'panel_count': len(panels), 'sheet': str(destination / 'native_sheet.png')},
              'limitations': ['37 controlled RNG states execute complete native initialization without RNG/name/metadata callbacks.',
                              'All native generated index slots and all ten base names/four templates have raster coverage; not all random sequences.',
                              'Original 198 compiled paragraphs, full labels/helper code and repaired parent positions remain exact.',
                              'Only the advice range/table literals change in the prior payload; appended terminated map presentation and table are source-word preserving.',
                              'Warm cache/font/outer widget origin, artwork/background/physical GPU/input and downloaded-save states remain contracts.',
                              'Role-dependent eligibility and inherited paths have separate exact-target evidence; physical cold boot remains unverified.',
                              'Research only; no new ROM or registry changes.']}
    Path('work/analysis/generated_item_advice_native_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'Pass: {len(cases)} generated rasters, 20 static/default regressions, 218 metadata initializers, 257 ABI cases, boot/cache/arena/counter/parent.')


if __name__ == '__main__':
    main()
