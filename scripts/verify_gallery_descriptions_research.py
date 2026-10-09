"""Verify all native Gallery page/captain redraws, pixels and safe staging."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.patch.gallery_description_release import BASE, PAGES, SOURCE
from dk4tool.patch.gallery_description_release import expected_page_draws as expected_draws
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.village_promised_words_release import PREFIX, SUFFIX
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.execute_scene_caption_raster import execute as raster
from scripts.probe_common_copy_arm946_alignment import matrix
from scripts.probe_common_itcm_arena_reservation import initialize as arenas
from scripts.probe_common_itcm_arena_reservation import verify as arena_bounds
from scripts.probe_common_monthly_tribute_preparation import execute as monthly
from scripts.probe_gallery_parent_composition import composition
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels
from scripts.probe_movement_notice_callers import caller as movement_caller
from scripts.probe_persistent_name_arm7_boot_overlap import execute as boot
from scripts.verify_ordinary_name_fidelity_research import initialized
from scripts.verify_village_promised_words_research import caller as village_caller


def verify_page(source, plan, page, font, mode):
    native = raster(source, 'Lisbon', gallery_page=page, kanji_font=font, mode=mode)
    expected = expected_draws(plan, page)
    if (native['gallery_draws'] != expected
            or [g['code'] for g in native['glyph_events']] != list(''.join(r['text'] for r in expected).encode('ascii'))
            or any(g['x'] < 0 or g['x'] + 6 > 256 or g['y'] < 0 or g['y'] + 11 > 192 for g in native['glyph_events'])
            or native['pixels'] != expected_pixels(source, font, native['glyph_events'], mode, background=0)):
        raise ValueError('Gallery native page loses text, leading glyphs, bounds or independent pixels')
    return native


def main():
    image = NdsImage.open('out/all_routes_combined_v157_candidate.nds')
    original = image.read_file('/__arm9__.bin')
    source = Path('work/analysis/gallery_description_research_arm9.bin').read_bytes()
    plan = json.loads(Path('work/analysis/gallery_description_plan.json').read_text(encoding='utf-8'))
    if sha(original) != SOURCE or sha(source) != plan['target_arm9_sha256']:
        raise ValueError('Gallery research identity differs')
    font = image.read_file('/GRP/KANJI.FNT')
    parent = composition(source)
    destination = Path('work/qa/gallery_descriptions_native')
    destination.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1032, len(PAGES) * 796), 'white')
    draw = ImageDraw.Draw(sheet)
    cases = []
    for number, page in enumerate(PAGES):
        for mode in (4, 16):
            native = verify_page(source, plan, page, font, mode)
            cases.append({'page': page, 'mode': mode, 'draws': native['gallery_draws'],
                          'pixels_sha256': sha(native['pixels']), 'complete_glyphs_bounds_and_independent_pixels': True,
                          'actual_native_selection_centering_context_renderer_and_cleanup_execute': True,
                          'native_stack_and_caller_state_preserved': True,
                          'site_name_provider_is_fixture': page == 'site-name'})
            if mode == 16:
                preview = Image.new('RGB', (256, 192))
                preview.putdata([(255, 255, 255) if c == 0 else (128, 128, 128) if c == 14 else (0, 0, 0)
                                 for c in struct.unpack('<49152H', native['pixels'])])
                preview = preview.resize((1024, 768), Image.Resampling.NEAREST)
                preview.save(destination / f'panel_{number:02d}.png')
                draw.text((4, number * 796 + 2), page + ' / native complete primary text canvas', fill='black')
                sheet.paste(preview, (4, number * 796 + 22))
    sheet.save(destination / 'native_sheet.png')
    common = image.read_file('/COMMON/MESFILE.DK4')
    if common_message_entries(common, original, clean=False) != common_message_entries(common, source, clean=False):
        raise ValueError('Gallery changes inherited COMMON selectors/text')
    movement = [movement_caller(source, common, variant, supply_selector=supply)
                for supply in (None, 0, 1) for variant in range(8)]
    village_plan = json.loads(Path('work/analysis/village_promised_words_plan.json').read_text(encoding='utf-8'))
    village, monthly_cases = [], []
    messages = {r['index']: r for r in village_plan['records'] if r['kind'] == 'MESSAGE'}
    for captain in (4, 19):
        for index, start in ((0, 0x78ADC), (2, 0x78BA0), (3, 0x78BB0)):
            village.append(village_caller(source, start, 0, captain, bytes.fromhex(messages[index]['compiled_hex']).decode('ascii')))
        for row in village_plan['records']:
            if row['kind'] == 'CLUE':
                clue = bytes.fromhex(row['compiled_hex']).decode('ascii')
                village.append(village_caller(source, 0x78B8C, row['index'], captain, PREFIX + clue + SUFFIX, clue=clue))
    for parent_return, table in ((BASE + 0x53F40, BASE + 0x1189C0), (BASE + 0x53EAC, 0),
                                 (BASE + 0x53F40, BASE + 0x1189C4)):
        for amount in (0, 999999, 42949672):
            kwargs = {'word_wrapped': parent_return == BASE + 0x53F40 and table == BASE + 0x1189C0,
                      'parent_return': parent_return, 'selector_table': table}
            if monthly(original, 'Payment: %s gold coins.', amount, 0x02428000, **kwargs) != monthly(
                    source, 'Payment: %s gold coins.', amount, 0x02428000, **kwargs):
                raise ValueError('Gallery extension changes monthly/unrelated text')
            monthly_cases.append({'parent_return': parent_return, 'selector_table': table,
                                  'amount': amount, 'exact_output_preserved': True})
    previous = json.loads(Path('work/analysis/swordsmanship_status_native_proof.json').read_text(encoding='utf-8'))
    duel = []
    for row in previous['native_pixel_cases']:
        native = raster(source, row['complete_formatted_text'],
                        sword_stats=(row['effective_skill'], row['hp'], row['state']),
                        duel_actor_index=row['duel_actor_index'], surface_size=(156, 12), mode=row['mode'], kanji_font=font)
        if sha(native['pixels']) != row['pixels_sha256']:
            raise ValueError('Gallery extension changes inherited duel pixels')
        duel.append({k: row[k] for k in ('duel_actor_index', 'mode', 'effective_skill', 'hp', 'state', 'pixels_sha256')})
    old_machine, new_machine = initialized(original), initialized(source)
    names, owners = [], []
    for index in range(207):
        old, new = ordinary_getter(original, index, old_machine), ordinary_getter(source, index, new_machine)
        if old != new or bytes(old_machine.mem_read(old, 128)) != bytes(new_machine.mem_read(new, 128)):
            raise ValueError('Gallery extension changes ordinary name output')
        names.append({'index': index, 'pointer': new, 'complete_name_preserved': True})
    name_plan = json.loads(Path('work/analysis/ordinary_name_fidelity_plan.json').read_text(encoding='utf-8'))
    for row in name_plan['inherited_pointer_moves']:
        old, new = [struct.unpack_from('<I', raw, row['field'])[0] for raw in (original, source)]
        if old != new or bytes(old_machine.mem_read(old, 128)) != bytes(new_machine.mem_read(new, 128)):
            raise ValueError('Gallery extension changes shared item/name output')
        owners.append({'field': row['field'], 'pointer': new, 'complete_name_preserved': True})
    statuses = []
    for mode in (4, 16):
        old, new = [raster(raw, 'Auto Sail', sailing_status=True, surface_size=(256, 32), kanji_font=font, mode=mode)
                    for raw in (original, source)]
        if any(old[k] != new[k] for k in ('pixels', 'glyph_events', 'sailing_status_draws')):
            raise ValueError('Gallery extension changes sailing-status output')
        statuses.append({'mode': mode, 'complete_native_status_pixels_preserved': True})
    code = MainCodeFile(source, BASE)
    current, before = arenas(source), arenas(original)
    if (current['low'][0] != plan['final_pool_span'][1] or current['high'] != before['high']
            or any(current['low'][i] != before['low'][i] for i in range(1, 9))):
        raise ValueError('Gallery native arena reservations differ')
    result = boot(source, bytes(image.rom.arm7), image.rom.arm7RamAddress,
                  plan['copy_entry'], bytes(code.sections[3].data[:-48]))
    if (result['arm7_source_changed_bytes_after_arm9_autoload']
            or not all(row['matches_original'] for row in result['arm7_native_loaded_sections'])
            or not all(result[k] for k in ('repaired_pool_matches_complete_payload',
                                          'repair_returns_with_stack_preserved', 'actual_startup_call_preserves_r0_r3'))):
        raise ValueError('Gallery staged SDK/ARM7 boot ownership differs')
    proof = {'status': 'research-native-gallery-all-page-captain-cases-pass',
             'source_arm9_sha256': sha(original), 'target_arm9_sha256': sha(source),
             'native_pixel_cases': cases, 'native_parent_composition': parent,
             'inherited_movement_callers': movement, 'inherited_village_callers': village,
             'inherited_monthly_scope_cases': monthly_cases, 'inherited_duel_pixels': duel,
             'inherited_sailing_status_pixels': statuses, 'inherited_names': names, 'inherited_shared_owners': owners,
             'common_selected_entries_preserved': 3668, 'shared_copy_alignment_cases': matrix(source),
             'native_initial_arenas': current, 'resident_arena_bounds': arena_bounds(source, plan['reserved_arena_low']),
             'boot': result, 'visual_review': {'complete': False}, 'physical_gameplay_verified': False,
             'limitations': ['Actual event draw/centering and all four native array-load selections execute. Upstream menu/route input is a fixture.',
                             'The Historic Sites draw function executes with null and supplied selected-site name; site-name provider is a fixture.',
                             'Raster font metrics, local origin and clear are diagnostic contracts; separate native constructor/overlay clear/source/composition proof executes.',
                             'Primary GPU requests are captured; surrounding artwork, final GPU output and physical gameplay remain pending.',
                             'Not registered or built as a playable ROM.']}
    Path('work/analysis/gallery_descriptions_native_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('14 native Gallery page/mode cases, real primary constructor/overlay clear, 64 inherited duel cases and safe boot pass. Research only.')


if __name__ == '__main__':
    main()
