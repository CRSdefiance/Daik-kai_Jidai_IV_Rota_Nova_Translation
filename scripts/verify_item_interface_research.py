"""Verify native item UI prose/columns with explicit resource-provider fixtures."""

import argparse
import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.item_interface_research import BASE, SOURCE
from dk4tool.patch.ordinary_name_fidelity_release import POOL
from dk4tool.rom.nds import NdsImage
from scripts.execute_scene_caption_raster import TEXT, execute
from scripts.probe_common_itcm_arena_reservation import initialize as arenas
from scripts.probe_common_itcm_arena_reservation import verify as arena_bounds
from scripts.probe_item_lookup_abi import verify as lookup_abi
from scripts.probe_item_source_canvas import source_canvas
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels
from scripts.probe_persistent_name_arm7_boot_overlap import execute as boot

EFFECTS = (0, 1, 9, 99, 100, 255)
# Clean native 02007C34 maps item attribute IDs to the sixteen crew stations.
ATTRIBUTE_ROLES = (5, 7, 15, 4, 6, 0, 1, 8, 9, 17, 17, 17, 17, 13, 11, 12, 17, 14, 10, 2, 3)
ROLE_ATTRIBUTES = tuple(ATTRIBUTE_ROLES.index(role) for role in range(16))
PREVIEWS = [('counter', n) for n in (0, 99, 100, 198)] + [
    ('main', (0, 0)), ('main', (1, 2)), ('main', (255, 2)), ('main', (255, 3)),
    ('main', (255, 4)), ('standalone', (0, 0)), ('standalone', (255, 1)),
    ('main', (255, 3, 1, 7)), ('standalone', (255, 1, 9, 19)),
]


def expected_draws(source, plan, page, case, item_index=None, crew_index=None, player_name=None,
                   ship_index=None, ship_name=None, promotional_seed=0):
    fields = {move['field']: move for move in plan['pointer_moves']}
    result = []
    tracking = 0 if page == 'counter' else 0xFFFFFFFF

    def label(field, x, y):
        row = fields[field]
        result.append({'pointer': row['target_pointer'], 'text': bytes.fromhex(row['compiled_hex'])[:-1].decode('ascii'),
                       'x': x, 'y': y, 'tracking': tracking})

    def supplied(pointer, text, x, y):
        result.append({'pointer': pointer, 'text': text, 'x': x, 'y': y, 'tracking': tracking})

    printf = struct.unpack_from('<I', source, 0xD529C)[0]
    if page == 'counter':
        supplied(printf, f'Items Acquired {case:3d}/198', 0, 12)
        return result
    effect, kind = case[:2]
    category, attribute = case[2:] if len(case) == 4 else (1, 24)
    price = 999999
    name_pointer, name = TEXT + 0x100, 'Compass '
    if item_index is not None:
        at = (0x11E210 + item_index * 24 if item_index < 188
              else struct.unpack_from('<I', source, 0x102E40)[0] - BASE + (item_index - 188) * 24)
        name_pointer, price = struct.unpack_from('<2I', source, at)
        category, attribute, effect = source[at + 16], source[at + 18], source[at + 19]
        if 188 <= item_index < 198:
            names = struct.unpack_from('<I', source, 0x102E44)[0] - BASE
            name_pointer = struct.unpack_from('<I', source, names + (item_index - 188) * 8)[0]
        if item_index >= 198:
            from scripts.probe_promotional_item_full import verify as full_promotional
            name = full_promotional(source, promotional_seed)['names'][item_index - 188]['name']
        else:
            loaded = MainCodeFile(source, BASE)
            if POOL <= name_pointer < POOL + len(loaded.sections[3].data) - 48:
                section, offset = loaded.sections[3], name_pointer - POOL
            else:
                section = next(s for s in loaded.sections if s.ramAddress <= name_pointer < s.ramAddress + len(s.data))
                offset = name_pointer - section.ramAddress
            name = bytes(section.data[offset:]).split(b'\0', 1)[0].decode('cp932')
        if item_index >= 188:
            from scripts.probe_promotional_item_defaults import OWNER
            name_pointer = OWNER + 0x22 + (item_index - 188) * 32
    if page == 'main':
        supplied(struct.unpack_from('<I', source, 0x4D260)[0], 'Items', 108, 84)
    supplied(name_pointer, name, 48 if page == 'main' else 0, 0)

    def projected(kind, index, x):
        projection = next(row for row in plan['item_only_projection'] if row['kind'] == kind)
        record = next(row for row in plan['records'] if row.get('kind') == kind and row['index'] == index)
        supplied(projection['compiled_pointers'][index], record['compiled'], x, 12)

    projected('CATEGORY', category, 0)
    if attribute == 24:
        supplied(struct.unpack_from('<I', source, 0x4D860 if page == 'main' else 0x4E52C)[0], '－', plan['role_x'], 12)
    else:
        role = ATTRIBUTE_ROLES[attribute]
        if role != 17:
            projected('ROLE', role, plan['role_x'])
        elif page == 'standalone':
            raise ValueError('Invalid source attribute would dereference a null role')
    if effect:
        label(0x4D864 if page == 'main' else 0x4E530, plan['effect_label_x'], 12)
        supplied(printf, f'{effect:2d} ', plan['effect_numeric_x'], 12)
    if page == 'main' and kind in (2, 3, 4):
        if kind == 2:
            label(0x4D86C, 0, 24)
            if crew_index is None:
                supplied(TEXT + 0x140, 'Raphael ', plan['owner_name_x'], 24)
            elif player_name is not None:
                root = struct.unpack_from('<I', source, 0xCB18C)[0]
                pointer = root + struct.unpack_from('<I', source, 0x4D870)[0] + 0x20
                supplied(pointer, player_name.decode('ascii'), plan['owner_name_x'], 24)
            else:
                table = struct.unpack_from('<I', source, 0xCDAC0)[0] - BASE
                pointer = struct.unpack_from('<I', source, table + crew_index * 32)[0]
                loaded = MainCodeFile(source, BASE)
                if POOL <= pointer < POOL + len(loaded.sections[3].data) - 48:
                    data, at = loaded.sections[3].data, pointer - POOL
                else:
                    data, at = source, pointer - BASE
                name = bytes(data[at:]).split(b'\0', 1)[0].decode('cp932')
                supplied(pointer, name, plan['owner_name_x'], 24)
        elif kind == 3:
            label(0x4D884, 0, 24)
            if ship_index is None:
                supplied(TEXT + 0x160, 'Falcon', plan['owner_name_x'], 24)
            else:
                root = struct.unpack_from('<I', source, 0xCB150)[0]
                pointer = root + 4 + ship_index * 0x8C + 8
                if ship_name is None:
                    table = struct.unpack_from('<I', source, 0xCD3CC)[0] - BASE
                    original = struct.unpack_from('<I', source, table + (ship_index - 50) * 44)[0]
                    loaded = MainCodeFile(source, BASE)
                    if POOL <= original < POOL + len(loaded.sections[3].data) - 48:
                        data, at = loaded.sections[3].data, original - POOL
                    else:
                        data, at = source, original - BASE
                    ship_name = bytes(data[at:]).split(b'\0', 1)[0]
                supplied(pointer, ship_name.decode('cp932'), plan['owner_name_x'], 24)
        else:
            supplied(struct.unpack_from('<I', source, 0x4D878)[0], 'Price', 0, 24)
            supplied(struct.unpack_from('<I', source, 0x4D87C)[0] + 12, f'{price:6d}', plan['owner_name_x'], 24)
    if page == 'main' or kind:
        advice = plan['item_advice_projection'][item_index or 0]
        pointer = advice['pointer']
        for line_index, line in enumerate(advice['compiled'].splitlines()):
            supplied(pointer, line, 0, (36 if page == 'main' else 24) + 12 * line_index)
            pointer += len(line) + 1
    return result


def glyph_codes(text, tracking=0):
    result = []
    tail = 0
    for char in text:
        if char == '\n':
            tail = 0
            continue
        raw = char.encode('cp932')
        result.append(raw[0] if len(raw) == 1 else int.from_bytes(raw, 'big'))
        tail = tail + 1 if len(raw) == 1 else 0
    # This renderer emits a synthetic space for an odd trailing ASCII pair.
    if tracking == 0 and tail % 2:
        result.append(32)
    return result


def verify_page(source, plan, page, case, font, mode, *, item_index=None, common=None,
                crew_index=None, player_name=None, ship_index=None, ship_name=None, promotional_seed=0,
                role_state=None, equipment_slot=None):
    geometry = (144, 36) if page == 'counter' else (240, 96)
    native = execute(source, 'fixture', item_page=page, item_case=case,
                     surface_size=geometry, kanji_font=font, mode=mode,
                     item_resource_index=item_index, item_common=common,
                     item_crew_owner=crew_index, item_player_name=player_name,
                     item_ship_owner=ship_index, item_ship_name=ship_name, item_promotional_seed=promotional_seed,
                     item_role_state=role_state, item_equipment_slot=equipment_slot)
    expected = expected_draws(source, plan, page, case, item_index, crew_index, player_name, ship_index, ship_name, promotional_seed)
    if native['item_draws'] != expected:
        raise ValueError(f'Item native field, value, complete prose or columns differ: {native["item_draws"]!r} != {expected!r}')
    codes = [code for draw in expected for code in glyph_codes(draw['text'], draw['tracking'])]
    if [glyph['code'] for glyph in native['glyph_events']] != codes:
        raise ValueError('Item native glyphs lose first/interior/final characters')
    start, rectangles = 0, []
    for draw in expected:
        count = len(glyph_codes(draw['text'], draw['tracking']))
        glyphs = native['glyph_events'][start:start + count]
        start += count
        if any(g['x'] < 0 or g['x'] + (6 if g['kind'] == 'ascii' else 12) > geometry[0]
               or g['y'] < 0 or g['y'] + 12 > geometry[1] for g in glyphs):
            raise ValueError('Item native glyph escapes its actual view')
        end = max(g['x'] + (6 if g['kind'] == 'ascii' else 12) for g in glyphs)
        rectangle = (min(g['x'] for g in glyphs), min(g['y'] for g in glyphs), end, max(g['y'] for g in glyphs) + 12)
        if any(rectangle[0] < old[2] and old[0] < rectangle[2]
               and rectangle[1] < old[3] and old[1] < rectangle[3] for old in rectangles):
            raise ValueError('Item native label/value cells overlap')
        rectangles.append(rectangle)
    if native['pixels'] != expected_pixels(source, font, native['glyph_events'], mode, background=0):
        raise ValueError('Item native pixels differ from independent complete font decoding')
    native['geometry'] = list(geometry)
    return native


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reuse-synthetic-phase', action='store_true',
                        help='Reuse the saved same-hash synthetic raster phase when only a later resource/startup gate needs repair.')
    args = parser.parse_args()
    image = NdsImage.open('out/all_routes_combined_v158_candidate.nds')
    original = image.read_file('/__arm9__.bin')
    source = Path('work/analysis/item_interface_research_arm9.bin').read_bytes()
    plan = json.loads(Path('work/analysis/item_interface_plan.json').read_text(encoding='utf-8'))
    if sha(original) != SOURCE or sha(source) != plan['target_arm9_sha256']:
        raise ValueError('Item research identity differs')
    font = image.read_file('/GRP/KANJI.FNT')
    cases = [('counter', count) for count in range(199)]
    cases += [('main', (effect, kind)) for effect in EFFECTS for kind in range(7)]
    cases += [('standalone', (effect, advice)) for effect in EFFECTS for advice in (0, 1)]
    cases += [(page, (255, 3 if page == 'main' else 1, category, attribute))
              for page in ('main', 'standalone') for category in range(13) for attribute in ROLE_ATTRIBUTES]
    cases += [entry for entry in PREVIEWS if entry not in cases]
    destination = Path('work/qa/item_interface_native')
    destination.mkdir(parents=True, exist_ok=True)
    previews, records = {}, []
    if args.reuse_synthetic_phase:
        saved = json.loads(Path('work/analysis/item_interface_synthetic_phase.json').read_text(encoding='utf-8'))
        if (saved['target_arm9_sha256'] != sha(source)
                or sha(Path('out/all_routes_combined_v158_candidate.nds').read_bytes())
                != '9a197373ba448718f3c0d887fdd27f01ce19b75dae11bb22515fed36981a7f5f'):
            raise ValueError('Saved synthetic proof or immutable font/source ROM identity differs')
        records = saved['native_pixel_cases']
        expected_keys = [(page, list(case) if isinstance(case, tuple) else case, mode)
                         for page, case in cases for mode in (4, 16)]
        if [(r['page'], r['case'], r['mode']) for r in records] != expected_keys:
            raise ValueError('Saved synthetic coverage differs')
        for record in records:
            if (record['draws'] != expected_draws(source, plan, record['page'], record['case'])
                    or not record['complete_glyphs_pixels_nonoverlap_and_bounds_pass']
                    or not record['native_caller_context_printf_and_renderer_execute']):
                raise ValueError('Saved synthetic expected fields or complete raster proof differs')
        print(f'Reused {len(records)} exact-hash synthetic raster cases; resources/loading still execute', flush=True)
    for page, case in ([] if args.reuse_synthetic_phase else cases):
        for mode in (4, 16):
            native = verify_page(source, plan, page, case, font, mode)
            records.append({'page': page, 'case': case, 'mode': mode,
                            'draws': native['item_draws'], 'provider_contracts': native['item_provider_contracts'],
                            'private_pool_executed_addresses': native['item_pool_executed_addresses'],
                            'pixels_sha256': sha(native['pixels']), 'geometry': native['geometry'],
                            'complete_glyphs_pixels_nonoverlap_and_bounds_pass': True,
                            'native_caller_context_printf_and_renderer_execute': True})
            if mode == 16 and (page, case) in PREVIEWS:
                preview = Image.new('RGB', (256, 192))
                preview.putdata([(255, 255, 255) if c == 0 else (128, 128, 128) if c == 14 else (0, 0, 0)
                                 for c in struct.unpack('<49152H', native['pixels'])])
                preview = preview.crop((0, 0, *native['geometry'])).resize(tuple(n * 3 for n in native['geometry']), Image.Resampling.NEAREST)
                previews[(page, case)] = preview
        if len(records) % 128 == 0:
            print(f'{len(records)} synthetic native cases passed', flush=True)
    Path('work/analysis/item_interface_synthetic_phase.json').write_text(json.dumps({
        'target_arm9_sha256': sha(source), 'native_pixel_cases': records,
        'status': 'synthetic-local-raster-pass-real-resources-and-loading-pending'}, indent=2) + '\n', encoding='utf-8')
    if not args.reuse_synthetic_phase:
        sheet = Image.new('RGB', (1456, ((len(PREVIEWS) + 1) // 2) * 316), 'white')
        draw = ImageDraw.Draw(sheet)
        for number, (page, case) in enumerate(PREVIEWS):
            origin = (8 + number % 2 * 728, number // 2 * 316)
            draw.text((origin[0], origin[1] + 2), f'{page} {case}; native text canvas; resource providers are fixtures', fill='black')
            sheet.paste(previews[(page, case)], (origin[0], origin[1] + 22))
            previews[(page, case)].save(destination / f'panel_{number:02d}.png')
        sheet.save(destination / 'native_sheet.png')
    real_records = []
    common = image.read_file('/COMMON/MESFILE.DK4')
    for item_index in range(188):
        for page in ('main', 'standalone'):
            for mode in (4, 16):
                native = verify_page(source, plan, page, (0, 4 if page == 'main' else 1), font, mode,
                                     item_index=item_index, common=common)
                real_records.append({'index': item_index, 'page': page, 'mode': mode,
                                     'draws': native['item_draws'], 'actual_common_ids': native['item_actual_common_ids'],
                                     'provider_contracts': native['item_provider_contracts'],
                                     'native_item_name_metadata_common_copy_and_complete_pixels_pass': True,
                                     'pixels_sha256': sha(native['pixels'])})
        if len(real_records) % 128 == 0:
            print(f'{len(real_records)} actual static-resource native cases passed', flush=True)
    Path('work/analysis/item_interface_real_phase.json').write_text(json.dumps({
        'target_arm9_sha256': sha(source), 'actual_static_resource_cases': real_records,
        'status': 'native-real-resource-raster-pass-loading-and-composition-pending'}, indent=2) + '\n', encoding='utf-8')
    code = MainCodeFile(source, BASE)
    current, before = arenas(source), arenas(original)
    if (current['low'][0] != plan['final_pool_span'][1] or current['high'] != before['high']
            or any(current['low'][i] != before['low'][i] for i in range(1, 9))):
        raise ValueError('Item native arena reservations differ')
    loading = boot(source, bytes(image.rom.arm7), image.rom.arm7RamAddress,
                   plan['copy_entry'], bytes(code.sections[3].data[:-48]))
    if (loading['arm7_source_changed_bytes_after_arm9_autoload']
            or not all(row['matches_original'] for row in loading['arm7_native_loaded_sections'])
            or not all(loading[k] for k in ('repaired_pool_matches_complete_payload',
                                           'repair_returns_with_stack_preserved', 'actual_startup_call_preserves_r0_r3'))):
        raise ValueError('Item staging changes native SDK/ARM7 ownership')
    proof = {'status': 'research-native-local-item-cases-pass-parent-and-resource-integration-pending',
             'source_arm9_sha256': sha(original), 'target_arm9_sha256': sha(source),
             'native_pixel_cases': records, 'native_initial_arenas': current,
             'actual_static_resource_cases': real_records,
             'private_lookup_abi': lookup_abi(source, plan),
             'same_hash_synthetic_phase_reused': args.reuse_synthetic_phase,
             'native_item_source_canvas': source_canvas(source),
             'resident_arena_bounds': arena_bounds(source, plan['reserved_arena_low']), 'boot': loading,
             'visual_review': {'complete': False}, 'physical_gameplay_verified': False,
             'limitations': ['Actual Gallery counter draw instructions execute all counts 0..198; total198 is loaded by native instructions.',
                             'Both complete item-detail draw functions execute. Property index division, byte getters and numeric printf are native.',
                             'Items title uses the existing source field 0204D260. Separate Advice command fields 02045664/0204D254 are not selected by these draw functions; their actual menu consumers remain pending.',
                             'Category and crew-role getters execute private exact-ABI copies over complete natural-English tables; global tables remain unchanged. All 13 categories by 16 roles execute both callers and pixel formats.',
                             'All 188 static item indices execute actual native item-name virtual, CB190, CDAFC, unsigned properties and warm-cache COMMON copy, with whole paragraph lines, independent pixels and bounds in both callers/formats. Runtime item-object initialization and COMMON warm cache initialization remain supplied contracts.',
                             'Ten promotional item indices 188..197 use an unresolved dynamic metadata provider. Their advice is word-preserving compiled but actual provider/render proof remains pending.',
                             'Crew/ship names, ownership and artwork remain explicit fixtures; their full real-name bounds remain unproven.',
                             'Use has a native sole code owner, but its branch leaves the name null and skips the heading draw. No visible-use translation credit.',
                             'Local raster image/view/origin/font initialization and clear are contracts; separate native item constructor/seeded overlay clear/shared primary dispatch execute.',
                             'Gallery counter image initialization and complete parent composition/crops/artwork/physical gameplay remain pending.',
                             'Not registered, built or handed off as a playable candidate.']}
    Path('work/analysis/item_interface_native_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(records)} synthetic and {len(real_records)} real-static item native raster cases pass complete glyphs, word-wrapped paragraphs, pixels, bounds, lookup ABI and safe SDK staging. Research only.')


if __name__ == '__main__':
    main()
