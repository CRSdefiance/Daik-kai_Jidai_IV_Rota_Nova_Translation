"""Independent saved-ROM, complete native-font and original-art screen checks."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.regional_fleet_plaques import FILE, RECORDS
from dk4tool.patch.regional_policy_wrap import transform
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/regional_fleet_v616')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v616_candidate.nds')


def native5(im):
    return im.convert('RGB').point(lambda v: (v * 31 + 127) // 255)


def report(context, frames, digest):
    p = CAP / ('regional_ui_v616_' + context) / 'capture_report.json'
    r = read(p)
    assert r['frames'] == frames and r['ROM_sha256'] == digest
    assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
    assert not any(value for key, value in r.items() if key.startswith('synthetic_'))
    shots = {row['frame']: row for row in r['frames_captured']}
    for row in shots.values():
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    return r, shots, {'path': str(p), 'sha256': sha(p.read_bytes())}


def glyphs(font, text, advance=6):
    return {(i * advance + x, y) for i, ch in enumerate(text)
            for y in range(11) for x in range(6) if font.decode(ch).getpixel((x, y))}


def full_cells(im, font, text, x0, y0, foreground, background=None):
    ink = glyphs(font, text)
    assert ink
    actual = {(x, y) for y in range(11) for x in range(len(text) * 6)
              if im.getpixel((x0 + x, y0 + y)) == foreground}
    assert actual == ink, (text, sorted(actual ^ ink)[:8])
    if background is not None:
        assert all(im.getpixel((x0 + x, y0 + y)) == background for y in range(11)
                   for x in range(len(text) * 6) if (x, y) not in ink)
    controls = []
    for index in (0, len(text) - 1):
        edge = {(index * 6 + x, y) for x, y in glyphs(font, text[index])}
        assert edge and ink - edge != ink
        controls.append(len(edge))
    return {'English': text, 'origin': [x0, y0], 'complete_ink_points': len(ink),
            'complete_glyph_blank_cells': len(text) * 6 * 11,
            'first_final_letter_erasure_controls': controls}


def main():
    digest = sha(ROM.read_bytes())
    manifest, registry = read(ROM.with_suffix('.manifest.json')), read('translations/release_stack.json')
    assert manifest['profile'] == 'all-routes-unified-v616' and manifest['candidate_sha256'] == digest
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches']) == 470 and len(registry['accepted_layers']) == 114 and all(manifest['checks'].values())
    assert manifest['base_sha256'] == registry['canonical_baseline']['sha256'] == sha(Path(manifest['base_rom']).read_bytes())
    parent, current = NdsImage.open('out/all_routes_combined_v615_candidate.nds'), NdsImage.open(ROM)
    old = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    new = {p: d for _, p, d in current.iter_files()} | dict(current.iter_components())
    assert old.keys() == new.keys() and [p for p in old if old[p] != new[p]] == ['/__arm9__.bin']
    arm, transform_proof = transform(old['/__arm9__.bin'])
    assert arm == new['/__arm9__.bin']
    native = read(ROOT / 'native_dispatch_proof.json')
    assert native['transform'] == transform_proof and native['all3668_native_IDs_exercised'] and native['unrelated_IDs_exact'] == 3660
    font = GameAsciiFont.from_arm9(arm)
    source_control = read(ROOT / 'source_art_control.json')
    source_hash = source_control['ROM_sha256']
    assert sha(Path(source_control['ROM']).read_bytes()) == source_hash
    candidate_run, candidate_shots, candidate_receipt = report('policy', 15800, digest)
    source_run, source_shots, source_receipt = report('source', 15800, source_hash)
    fixture = read('work/analysis/regional_fleet_v615/formed_fixture_manifest.json')
    for r in (candidate_run, source_run):
        assert r['battery_save_preloaded']['source_sha256'] == fixture['fixture_sha256']
    assert candidate_run['scripted_input_schedule'] == source_run['scripted_input_schedule']
    atlas = native5(PxlImage.from_bytes(new[FILE]).render())
    original = native5(PxlImage.from_bytes(NdsImage.open('work/clean.nds').read_file(FILE)).render())
    composites, regional_frames, native_region_pixels = [], [], 0
    for frame in (3400, 6200, 6600, 7000, 7400, 9800, 10600, 13000, 13800, 14600, 15800):
        source = native5(Image.open(source_shots[frame]['path']))
        candidate = native5(Image.open(candidate_shots[frame]['path']))
        active = all(source.crop(box).tobytes() == original.crop(box).tobytes() for _, _, _, box, _, _ in RECORDS)
        expected = source.copy()
        if active:
            regional_frames.append(frame)
            for _, _, _, box, _, _ in RECORDS:
                expected.paste(atlas.crop(box), box[:2])
                native_region_pixels += (box[2] - box[0]) * (box[3] - box[1])
        assert candidate.tobytes() == expected.tobytes(), frame
        composites.append({'frame': frame, 'active_regional_identified_only_from_Japanese_control': active,
                           'whole_native5_pixels': 256 * 384, 'every_expected_and_outside_pixel_exact': True})
    assert regional_frames == [6200, 6600, 7000, 7400]
    # Inspect the actual initialized resource owner and original fleet predicates
    # from captured RAM; do not invent a persistent backdrop view binding.
    resources = []
    for frame in regional_frames:
        snap = next(s for s in candidate_run['read_only_capture_RAM_snapshots'] if s['frame'] == frame)
        raw = Path(snap['path']).read_bytes()
        assert sha(raw) == snap['sha256'] and len(raw) == 0x400000
        data = new[FILE]
        assert raw.find(data) >= 0
        u = machine(arm)
        u.mem_write(BASE, raw)
        owner = 0x02313380
        pointer = struct.unpack('<I', u.mem_read(owner + 12, 4))[0]
        assert bytes(u.mem_read(pointer, 64)).split(b'\0')[0] == b'_pxl/chihofleetinfo.pxl'
        call(u, 0xCB1A8, ())
        fleet = u.reg_read(UC_ARM_REG_R0) + 4 + 57 * 0x84
        predicates = []
        for entry in (0x36914, 0x36948, 0x367FC):
            call(u, entry, (fleet,))
            predicates.append(u.reg_read(UC_ARM_REG_R0))
        assert predicates[:2] == [1, 0] and predicates[2]
        resources.append({'frame': frame, 'owner': owner, 'whole_named_resource_resident': BASE + raw.find(data),
                          'regional_record': fleet, 'original_own_main_finance_getters': predicates})
    menu = Image.open(candidate_shots[7000]['path']).convert('RGB')
    menu_masks = [full_cells(menu, font, text, x, y, (8, 8, 8), (205, 198, 180))
                  for text, x, y in (('Manage Area', 95, 252), ('Patrol', 110, 272), ('Dock', 116, 292), ('Attack Town', 95, 312))]
    prompt_masks = []
    for frame, lines in ((7400, ['Choose a base city.']), (10600, ['You have no contract with that city.']),
                         (13800, ['Choose a city for patrol. You must', 'have a contract there.']),
                         (15800, ['To dock the fleet, choose a city', 'under contract.'])):
        image = Image.open(candidate_shots[frame]['path']).convert('RGB')
        origin_x = 22 if len(lines) > 1 else 16
        masks = [full_cells(image, font, text, origin_x, 296 + i * 16, (0, 8, 0)) for i, text in enumerate(lines)]
        expected_ink = {(origin_x + x, 296 + i * 16 + y) for i, text in enumerate(lines) for x, y in glyphs(font, text)}
        actual_ink = {(x, y) for y in range(294, 328) for x in range(12, 244) if image.getpixel((x, y)) == (0, 8, 0)}
        assert actual_ink == expected_ink
        prompt_masks.append({'frame': frame, 'complete_lines': masks, 'no_missing_or_stray_text_pixels': True,
                             'all_lines_same_left_origin': origin_x})
    names_run, names_shots, names_receipt = report('names_final', 10200, digest)
    assert names_run['battery_save_preloaded']['source_sha256'] == fixture['fixture_sha256']
    name_masks = [dict(frame=frame, caller=caller, **full_cells(Image.open(names_shots[frame]['path']).convert('RGB'),
                  font, 'Ship Name', 48, 224, (213, 214, 213), (0, 0, 0)))
                  for frame, caller in ((6200, 'original ship purchase'), (10200, 'original existing-ship rename'))]
    market, market_shots, market_receipt = report('market', 24100, digest)
    previous = read(CAP / 'golden_route_plaques_v613_market_current/capture_report.json')
    assert market['scripted_input_schedule'] == previous['scripted_input_schedule']
    assert 'battery_save_preloaded' not in market
    previous_shots = {r['frame']: r for r in previous['frames_captured']}
    assert market_shots.keys() == previous_shots.keys() and len(market_shots) == 19
    for frame, row in market_shots.items():
        assert Image.open(row['path']).convert('RGB').tobytes() == Image.open(previous_shots[frame]['path']).convert('RGB').tobytes()
    preservation, patch = read(ROOT / 'preservation_proof.json'), read(ROOT / 'patch_proof.json')
    assert preservation['candidate_sha256'] == patch['candidate_sha256'] == digest
    assert preservation['current921_format_palette_extent_checks'] and preservation['all57_embedded_block_extents_exact']
    assert patch['exact_all_byte_reconstruction'] and sha(ROM.with_suffix('.xdelta').read_bytes()) == patch['patch_sha256']
    save(ROOT / 'release_proof.json', {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
         'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'], 'patch_sha256': patch['patch_sha256'],
         'all470_batches114_accepted_layers_and_prior_graphics_exact': True, 'only_existing128_byte_wrapper_changes_from_V615': True,
         'native_dispatch_proof': native, 'actual_resources_and_fleet_predicates': resources,
         'actual_all5_regional_plaque_frames': regional_frames, 'complete_native_regional_pixels': native_region_pixels,
         'whole_source_composites': composites, 'menu_complete_font_masks': menu_masks,
         'actual_complete_prompt_font_masks': prompt_masks, 'both_complete_Ship_Name_font_masks': name_masks,
         'ordinary_no_fixture_19_New_Game_Market_full_screens_exact_V613': True,
         'reports': [candidate_receipt, source_receipt, names_receipt, market_receipt],
         'all921_graphics57_embedded_formats_palettes_extents_preserved': True, 'exact_clean_patch_reconstruction': True,
         'remaining_in_this_family': ['Attack Town dispatch and contract/war rejection branches132..134 in actual gameplay',
              'four assignment confirmations and Patrol/Dock/Attack mission description display', 'nonzero monthly financial display variants'],
         'persistent_top_backdrop_view_binding_not_claimed': True,
         'source_control_is_original_art_only_not_clean_Japanese_gameplay': True,
         'earned_money_abilities_regional_progression_hardware_and_human_acceptance_not_claimed': True,
         'all18_original_plaque_entries_incomplete_and22_historical_scopes_retained': True,
         'full_goal_complete': False, 'canonical_promoted': False, 'script_sha256': sha(Path(__file__).read_bytes())})
    print('V616:all5 regional plaques,11 whole source pairs,4 complete menu labels,Patrol/Dock wrapping,both Ship Name callers,19 ordinary regression screens and exact patch pass. Remaining family/gameplay gates stay open.')


if __name__ == '__main__':
    main()
