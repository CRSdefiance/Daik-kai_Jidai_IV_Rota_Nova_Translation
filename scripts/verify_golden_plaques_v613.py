"""Source materials, full native Golden Route screens and exact integration."""

import copy
import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.golden_route_plaques import FILES, apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.native_golden_route_fixture_v613 import BASE, TABLE, discount_salt_purchase, populate
from scripts.probe_button_prompt_native import call, machine
from scripts.run_golden_plaques_v613 import DONOR, ROOT, SOURCE
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_save_load_plaques_v612 import snapshot
from scripts.verify_village_wrap_v608 import read, report, save

ROM = Path('out/all_routes_combined_v613_candidate.nds')
PARENT = Path('out/all_routes_combined_v612_candidate.nds')
RECORDS = (5000, 5400, 5800, 6200, 6600, 7000, 7400, 7800, 8200, 8600, 9000, 9400)
CUMULATIVE = (5800, 6200, 6600, 7000, 7400)
OWNERS = ((0x0210F9D8, 0x023133F8), (0x0210F990, 0x02313420), (0x0210F9B4, 0x0231340C))


def rejected(function, *args):
    try:
        function(*args)
    except (ValueError, AssertionError):
        return True
    raise AssertionError('Unsafe fixture was not rejected')


def fixture_checks(arm, runs):
    rows = read(ROOT / 'fixture_rows.json')
    negatives = []
    for run in runs['records'].values():
        raw = snapshot(run, 4600)
        after, proof = populate(arm, raw, rows)
        actual = run['synthetic_golden_route_display_fixtures']
        assert actual == [dict(proof, frame=4600)]
        assert len(proof['changes']) == 41
        negatives.append(rejected(populate, arm, after, rows))
        assert all(struct.unpack_from('<7I', snapshot(run, f), TABLE - BASE + i * 28)[0] == 0x1803
                   for f in RECORDS for i in range(5))
    raw = snapshot(runs['records']['old'], 4600)
    for value in (-1, 18, True):
        invalid = copy.deepcopy(rows)
        invalid[0]['sea_area'] = value
        negatives.append(rejected(populate, arm, raw, invalid))
    negatives.append(rejected(populate, arm, raw, []))
    for run in runs['sale'].values():
        raw = snapshot(run, 22000)
        _, proof = discount_salt_purchase(arm, raw, 1)
        assert run['synthetic_golden_route_display_fixtures'] == [dict(proof, frame=22000)]
        assert len(proof['changes']) == 2 and all(raw[TABLE - BASE + i * 28] == 0 for i in range(77))
        for frame, state in ((22900, 1), (25300, 2), (33400, 3)):
            words = struct.unpack_from('<7I', snapshot(run, frame), TABLE - BASE)
            assert words == (0x1800 + state, 1, 288, 11, 11, 13, 1)
        negatives.append(rejected(discount_salt_purchase, arm, snapshot(run, 22900), 1))
    for value in (0, 11, True):
        negatives.append(rejected(discount_salt_purchase, arm, snapshot(runs['sale']['old'], 22000), value))
    return {'unsafe_or_existing_history_negative_controls': len(negatives),
            'record_fixture_only_declared41_bytes': True, 'cost_fixture_only_two_bytes_in_one_cost_word': True,
            'original_sale_then_tutorial_then_Guild_state1_2_3_observed': True,
            'same_port_and_synthetic_cost_explicit_not_earned_profit_or_progress': True}


def check_material(arm, before, current, source, transforms):
    font = GameAsciiFont.from_arm9(arm)
    masks, rims = [], 0
    for transform in transforms:
        path = transform['file_path']
        old, atlas, original = [PxlImage.from_bytes(d[path]) for d in (before, current, source)]
        assert atlas.source[:atlas.pixels_offset] == original.source[:original.pixels_offset]
        owned = set()
        for row in transform['records']:
            l, t, r, b = row['plaque_box']
            sl, st, sr, _sb = row['original_plaque_box']
            x0 = l + (r - l - len(row['English']) * 5) // 2
            y0 = t + 2
            ink = {(x0 + n * 5 + x, y0 + y) for n, ch in enumerate(row['English'])
                   for y in range(11) for x in range(6) if font.decode(ch).getpixel((x, y))}
            fl, ft, fr, fb = row['font_box']
            actual = {(x, y) for y in range(ft, fb) for x in range(fl, fr) if atlas.indices[y * 256 + x] == 1}
            assert actual == ink and len(ink) == row['complete_font_ink']
            erasures = []
            for n in (0, len(row['English']) - 1):
                points = {(x0 + n * 5 + x, y0 + y) for y in range(11) for x in range(6)
                          if font.decode(row['English'][n]).getpixel((x, y))}
                assert points and actual - points != ink
                erasures.append(len(points))
            for y in range(b - t):
                for x in range(r - l):
                    if 2 <= x < r - l - 2 and 2 <= y < 14:
                        continue
                    sx = sl + (x if x < 2 else sr - sl - ((r - l) - x) if x >= r - l - 2
                               else 2 + (x - 2) % (sr - sl - 4))
                    assert atlas.indices[(t + y) * 256 + l + x] == original.indices[(st + y) * 256 + sx]
                    rims += 1
            rl, rt, rr, rb = row['restore_box']
            owned.update(y * 256 + x for y in range(rt, rb) for x in range(rl, rr))
            masks.append({'file': path, 'English': row['English'], 'Japanese': row['Japanese'],
                          'complete_native_font_ink': len(ink), 'first_final_letter_erasure_controls': erasures})
        assert all(a == b for i, (a, b) in enumerate(zip(old.indices, atlas.indices, strict=True)) if i not in owned)
    assert [r['English'] for r in masks] == ['Goods', 'Profit %', 'Reward', 'Goods', 'Profit %', 'Reward', 'Goods', 'Total Rewards']
    return masks, rims


def resource_bindings(arm, clean_arm, resource_sets, runs):
    u, clean_u = machine(arm), machine(clean_arm)
    owners = {}
    for path, (start, owner) in zip(FILES, OWNERS, strict=True):
        assert bytes(u.mem_read(start, 36)) == bytes(clean_u.mem_read(start, 36))
        u.emu_start(start, start + 36, count=100)
        assert u.reg_read(UC_ARM_REG_PC) == start + 36 and u.reg_read(UC_ARM_REG_R0) == owner
        pointer = struct.unpack('<I', u.mem_read(owner + 12, 4))[0]
        assert bytes(u.mem_read(pointer, 64)).split(b'\0')[0] == path[1:].encode()
        owners[path] = owner
    bindings = []
    for context, frames in (('records', RECORDS), ('sale', (33400,))):
        for variant, run in runs[context].items():
            for frame in frames:
                path = FILES[2 if frame in CUMULATIVE else 1] if context == 'records' else FILES[0]
                raw, views = snapshot(run, frame), []
                for off in range(0x170000, len(raw) - 48, 4):
                    words = struct.unpack_from('<12I', raw, off)
                    if words[3] == owners[path] and words[7:9] == (0, 0) and words[9] & 0xFFFF == 0 and words[10:12] == (256, 192):
                        views.append((BASE + off, words))
                assert views, (context, variant, frame, 'No actual native Golden Route view')
                uc = machine(arm)
                uc.mem_write(BASE, raw)
                data = resource_sets[variant][path]
                for address, words in views:
                    call(uc, 0xD4170, (address,))
                    header = uc.reg_read(UC_ARM_REG_R0)
                    assert bytes(uc.mem_read(header, len(data))) == data
                    bindings.append({'context': context, 'variant': variant, 'frame': frame, 'file': path,
                                     'owner': owners[path], 'actual_view': address, 'view_words': list(words),
                                     'actual_resident_PXL_header': header, 'whole_named_PXL_sha256': sha(data),
                                     'original_getter_without_supplied_owner_or_cache': True})
    return bindings


def native_frames(resources, transforms, runs, shots):
    pairs, atlas_counts = [], {}
    for context in ('records', 'sale'):
        assert shots[context]['old'].keys() == shots[context]['new'].keys() == shots[context]['original'].keys()
        for frame in shots[context]['old']:
            images = {k: Image.open(v[frame]['path']).convert('RGB') for k, v in shots[context].items()}
            wanted = list(images['old'].get_flattened_data())
            source_wanted = wanted.copy()
            active = frame in RECORDS if context == 'records' else frame == 33400
            pixels, covered = 0, []
            if active:
                path = FILES[2 if frame in CUMULATIVE else 1] if context == 'records' else FILES[0]
                transform = next(r for r in transforms if r['file_path'] == path)
                atlases = {k: PxlImage.from_bytes(v[path]).render().convert('RGB') for k, v in resources.items()}
                for row in transform['records']:
                    l, t, r, b = row['restore_box']
                    for y in range(t, b):
                        for x in range(l, r):
                            point = (x, y + 192)
                            old_pixel = native5(images['old'].getpixel(point))
                            original_pixel = native5(images['original'].getpixel(point))
                            exposed = (old_pixel == native5(atlases['old'].getpixel((x, y)))
                                       and original_pixel == native5(atlases['original'].getpixel((x, y))))
                            if not exposed:
                                # The actual first-row selection covers rows13..17.
                                # Derive this exclusively from the independent old
                                # and original-art controls, never candidate output.
                                # Every complete English glyph is above this band.
                                assert context == 'records' and 13 <= y < 18 and old_pixel == original_pixel
                                covered.append((x, y))
                                continue
                            wanted[(y + 192) * 256 + x] = atlases['new'].getpixel((x, y))
                            source_wanted[(y + 192) * 256 + x] = atlases['original'].getpixel((x, y))
                            pixels += 1
                atlas_counts[path] = atlas_counts.get(path, 0) + 1
            assert list(map(native5, images['new'].get_flattened_data())) == list(map(native5, wanted)), ('current composite', context, frame)
            assert list(map(native5, images['original'].get_flattened_data())) == list(map(native5, source_wanted)), ('source composite', context, frame)
            pairs.append({'context': context, 'frame': frame, 'whole_both_screen_positions': 98304,
                          'actual_changed_atlas': active, 'complete_visible_restoration_pixels': pixels,
                          'original_first_row_selection_cover_pixels': len(covered),
                          'source_control_cover_map_sha256': sha(bytes((x, y) in set(covered) for y in range(18) for x in range(256))) if covered else None,
                          'candidate_independent_cover_all_at_y13_or_below_all_complete_glyphs_at_y2_to12': True,
                          'all_live_values_selection_portraits_and_surroundings_exact': True})
    assert set(atlas_counts) == set(FILES)
    return pairs, atlas_counts


def main():
    parent, rom, clean, original_control = [NdsImage.open(p) for p in (PARENT, ROM, 'work/clean.nds', SOURCE)]
    before = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    current = {p: d for _, p, d in rom.iter_files()} | dict(rom.iter_components())
    assert before.keys() == current.keys() and {p for p in before if before[p] != current[p]} == set(FILES)
    originals = {p: clean.read_file(p) for p in FILES}
    expected, transforms = apply_release(parent, clean, 'translations/golden_route_plaques_v1.json')
    assert all(expected[p] == current[p] == rom.read_file(p) for p in FILES)
    assert original_control.read_file('/__arm9__.bin') == current['/__arm9__.bin']
    assert all(original_control.read_file(p) == originals[p] for p in FILES)
    manifest, previous, registry = read(ROM.with_suffix('.manifest.json')), read(PARENT.with_suffix('.manifest.json')), read('translations/release_stack.json')
    digest = sha(ROM.read_bytes())
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v613'
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['base_sha256'] == registry['canonical_baseline']['sha256'] == sha(Path(manifest['base_rom']).read_bytes())
    assert manifest['batches'] == previous['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == previous['required_batches'] and len(registry['accepted_layers']) == 114
    assert all(manifest['checks'].values())
    masks, rims = check_material(current['/__arm9__.bin'], before, current, originals, transforms)
    make_xdelta(Path('work/clean.nds'), ROM, ROM.with_suffix('.xdelta'))
    apply_xdelta(Path('work/clean.nds'), ROM.with_suffix('.xdelta'), ROOT / 'patch_reconstructed.nds')
    assert (ROOT / 'patch_reconstructed.nds').read_bytes() == ROM.read_bytes()
    runs, shots, receipts = {}, {}, {}
    for context, frames in (('records', 10200), ('sale', 34300)):
        runs[context], shots[context], receipts[context] = {}, {}, {}
        for key, path, suffix in (('old', PARENT, 'control' if context == 'records' else 'sale_control'),
                                  ('new', ROM, context + '_current'), ('original', SOURCE, context + '_original')):
            name = 'golden_route_plaques_v613_' + suffix
            run, captures, receipt = report(name, frames, sha(path.read_bytes()))
            assert run['scripted_input_schedule'] == read(ROOT / ('complete_' + context + '_inputs.json'))
            assert run['earned_golden_route_discovery_reporting_or_payment_verified'] is False
            assert not any(v for k, v in run.items() if k.startswith('synthetic_') and k != 'synthetic_golden_route_display_fixtures')
            if context == 'records':
                assert run['battery_save_preloaded']['source_sha256'] == sha(DONOR.read_bytes()) == '958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb'
            else:
                assert not run.get('battery_save_preloaded')
            runs[context][key], shots[context][key], receipts[context][key] = run, captures, receipt
        assert all(r['core_options'] == runs[context]['old']['core_options'] for r in runs[context].values())
    fixture = fixture_checks(current['/__arm9__.bin'], runs)
    resources = {'old': {p: before[p] for p in FILES}, 'new': {p: current[p] for p in FILES}, 'original': originals}
    bindings = resource_bindings(current['/__arm9__.bin'], clean.read_file('/__arm9__.bin'), resources, runs)
    pairs, counts = native_frames(resources, transforms, runs, shots)
    market, market_shots, market_receipt = report('golden_route_plaques_v613_market_current', 24100, digest)
    prior, prior_shots, prior_receipt = report('save_load_plaques_v612_market', 24100, sha(PARENT.read_bytes()))
    assert market['scripted_input_schedule'] == prior['scripted_input_schedule'] and market['core_options'] == prior['core_options']
    assert not market.get('battery_save_preloaded') and not any(v for k, v in market.items() if k.startswith('synthetic_'))
    assert market_shots.keys() == prior_shots.keys() and len(market_shots) == 19
    assert all(market_shots[f]['PNG_sha256'] == prior_shots[f]['PNG_sha256'] for f in market_shots)
    preservation = read(ROOT / 'preservation_proof.json')
    assert preservation['candidate_sha256'] == digest and preservation['current921_format_palette_extent_checks']
    assert preservation['all57_embedded_block_extents_exact']
    sheet = Image.new('RGB', (1152, 540), '#263238')
    draw = ImageDraw.Draw(sheet)
    for col, variant in enumerate(('original', 'old', 'new')):
        draw.text((col * 384 + 8, 8), {'original': 'Original Japanese art control', 'old': 'Actual V612', 'new': 'Actual V613'}[variant], fill='white')
        for y, context, frame in ((32, 'sale', 33400), (244, 'records', 5000), (420, 'records', 5800)):
            image = Image.open(shots[context][variant][frame]['path']).convert('RGB')
            crop = image.crop((0, 192, 256, 292 if context == 'sale' else 228))
            sheet.paste(crop.resize((384, crop.height * 3 // 2), Image.Resampling.NEAREST), (col * 384, y))
    sheet.save(ROOT / 'actual_original_current_repair.png')
    save(ROOT / 'release_proof.json', {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
         'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'], 'patch_sha256': sha(ROM.with_suffix('.xdelta').read_bytes()),
         'exact_clean_patch_reconstruction': True, 'only_three_Golden_atlases_changed_from_V612': list(FILES),
         'all_code_pool_other_art_dialogue_and_470_batches114_layers_retained': True,
         'transforms': transforms, 'independent_font_masks': masks, 'original_rim_samples': rims,
         'fixtures': fixture, 'actual_native_bindings': bindings, 'actual_whole_composites': pairs,
         'observed_atlas_context_counts': counts, 'all19_ordinary_Market_New_Game_regression_frames_exact': True,
         'reports': receipts, 'market_reports': {'new': market_receipt, 'old': prior_receipt},
         'preservation_proof_sha256': sha((ROOT / 'preservation_proof.json').read_bytes()),
         'original_Japanese_art_control_not_a_clean_Japanese_playthrough': True,
         'ordinary_earned_trade_discovery_reporting_payment_hardware_or_user_acceptance_not_claimed': True,
         'inherited_regional_native_context_still_open': True, 'all18_original_plaques_incomplete_all22_historical_scopes_retained': True,
         'full_goal_complete': False, 'canonical_promoted': False, 'script_sha256': sha(Path(__file__).read_bytes())})
    print(f'V613:8 complete headings,{rims} original rim samples,{len(bindings)} real getter bindings,{len(pairs)} whole screen pairs,19 ordinary regression frames and exact patch pass.')


if __name__ == '__main__':
    main()
