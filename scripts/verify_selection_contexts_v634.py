"""Bind new ordinary two-ship screens and bounded trace to unchanged V633."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_blitter_trace_v603 import (
    CAPACITY,
    CONTROL,
    CORNER,
    END,
    ENTRY,
    FIELDS,
    RECORDS,
    STRIDE,
    TILE,
)
from scripts.prepare_selection_trace_v634 import ROOT, SOURCE
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.search_miniature_captures_v577 import scan_image, template
from scripts.verify_blitter_trace_v603 import target
from scripts.verify_regional_ui_v616 import full_cells, native5
from scripts.verify_village_wrap_v608 import read, save

CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
OWNER = 0x02313C7C
FRAMES = (19000, 19400, 19800, 20200, 20600, 21000, 21400, 21800, 22600)


def report(name, digest):
    path = CAP / name / 'capture_report.json'
    data = read(path)
    assert data['ROM_sha256'] == digest and data['frames'] == 22600
    assert data['cold_boot'] and not data['savestate_loaded'] and not data['callback_errors']
    assert not any(v for k, v in data.items() if k.startswith('synthetic_'))
    donor = data['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    assert donor['source_sha256'] == '958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb'
    shots = {r['frame']: r for r in data['frames_captured']}
    for row in shots.values():
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    return path.parent, data, shots, {'path': str(path), 'sha256': sha(path.read_bytes())}


def main():
    manifest = read(ROOT / 'fixture_manifest.json')
    abi = read(ROOT / 'ABI_proof.json')
    assert manifest['script_sha256'] == sha(Path('scripts/prepare_selection_trace_v634.py').read_bytes())
    assert abi['fixture_manifest_sha256'] == sha((ROOT / 'fixture_manifest.json').read_bytes())
    assert abi['script_sha256'] == sha(Path('scripts/verify_blitter_trace_abi_v603.py').read_bytes())
    assert len(abi['ABI_source_contract_cases']) == 20
    digest = sha(SOURCE.read_bytes())
    assert digest == manifest['production_ROM_sha256']
    research_path = Path(manifest['research_ROM'])
    assert sha(research_path.read_bytes()) == manifest['research_ROM_sha256']
    production, research = NdsImage.open(SOURCE), NdsImage.open(research_path)
    before = {p: d for _, p, d in production.iter_files()} | dict(production.iter_components())
    after = {p: d for _, p, d in research.iter_files()} | dict(research.iter_components())
    assert before.keys() == after.keys()
    assert sorted(p for p in before if before[p] != after[p]) == manifest['changed_components']
    assert research.rom.arm9OverlayTable == production.rom.arm9OverlayTable
    root, baseline, bs, br = report('selection_contexts_v634_two_ship_baseline', digest)
    _, trace, ts, tr = report('selection_contexts_v634_two_ship_trace', manifest['research_ROM_sha256'])
    assert baseline['scripted_input_schedule'] == trace['scripted_input_schedule'] == read(ROOT / 'full_inputs.json')
    assert baseline['core_options'] == trace['core_options'] and bs.keys() == ts.keys() and len(bs) == 80
    for f in bs:
        assert Image.open(bs[f]['path']).convert('RGB').tobytes() == Image.open(ts[f]['path']).convert('RGB').tobytes()
    state = trace['read_only_native_state']
    assert state['read_only_export'] and not state['state_loaded'] and state['main_RAM_unchanged_by_export']
    assert state['serialized_RAM_matches_same_frame_direct_export']
    assert sha(Path(state['path']).read_bytes()) == state['sha256']
    for row in state['regions'].values():
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    itcm = Path(state['regions']['ITCM']['path']).read_bytes()
    sections = MainCodeFile(after['/__arm9__.bin'], BASE).sections
    observer = next(bytes(s.data) for s in sections if s.ramAddress == ENTRY)
    assert itcm[ENTRY & 0x7FFF:CONTROL & 0x7FFF] == observer[:CONTROL - ENTRY]
    low = next(s for s in sections if s.ramAddress <= CORNER < s.ramAddress + len(s.data))
    assert itcm[CORNER & 0x7FFF:(CORNER & 0x7FFF) + 4] == low.data[CORNER - low.ramAddress:CORNER - low.ramAddress + 4]
    overlay = loadOverlayTable(research.rom.arm9OverlayTable, lambda _id, fid: research.rom.files[fid])[0]
    assert itcm[TILE & 0x7FFF:(TILE & 0x7FFF) + 4] == overlay.data[TILE - overlay.ramAddress:TILE - overlay.ramAddress + 4]
    control = struct.unpack_from('<6I', itcm, CONTROL & 0x7FFF)
    assert control[0] > 0 and control[2] <= CAPACITY and control[3:] == (0, 3, 0x603B117)
    rows = [dict(zip(FIELDS, struct.unpack_from('<20I', itcm, (RECORDS & 0x7FFF) + i * STRIDE), strict=True))
            for i in range(control[2])]
    assert control[1] == sum(r['hits'] for r in rows)
    assert len(rows) == 2 and {r['kind'] for r in rows} == {0, 1} and not any(target(r) for r in rows)
    assert all(r['source_y'] == 208 for r in rows)
    assert itcm[(RECORDS & 0x7FFF) + control[2] * STRIDE:END & 0x7FFF] == bytes(END - RECORDS - control[2] * STRIDE)
    snapshot = trace['read_only_RAM_snapshot']
    assert sha(Path(snapshot['path']).read_bytes()) == snapshot['sha256']
    arm, art = before['/__arm9__.bin'], before['/_pxl/tempcargo.pxl']
    font = GameAsciiFont.from_arm9(arm)
    atlas = native5(PxlImage.from_bytes(art).render())
    images, bindings, headings, slots = {}, [], [], {}
    for f in FRAMES:
        raw = (root / f'frame_{f:06d}_arm9_ram.bin').read_bytes()
        matches = [i - 12 for i in range(0x17000C, len(raw) - 48, 4)
                   if struct.unpack_from('<I', raw, i)[0] == OWNER
                   and struct.unpack_from('<2I', raw, i + 28) == (256, 16)]
        assert len(matches) == 1
        view = BASE + matches[0]
        parent = view - 0x3070
        assert struct.unpack_from('<I', raw, parent - BASE + 0x10)[0] == 0
        u = machine(arm)
        u.mem_write(BASE, raw)
        ptr = struct.unpack('<I', u.mem_read(OWNER + 12, 4))[0]
        assert bytes(u.mem_read(ptr, 32)).split(b'\0')[0] == b'_pxl/tempcargo.pxl'
        call(u, 0xD4170, (view,))
        resident = u.reg_read(UC_ARM_REG_R0)
        assert bytes(u.mem_read(resident, len(art))) == art
        bindings.append({'frame': f, 'view': view, 'parent': parent, 'mode': 0, 'owner': OWNER,
                         'resident_PXL': resident, 'entire_named_file_exact': True, 'RAM_sha256': sha(raw)})
        slots[f] = [raw[parent - BASE + off:parent - BASE + off + 12].hex() for off in (0x18, 0x24, 0x54)]
        im = images[f] = Image.open(bs[f]['path']).convert('RGB')
        ship = 'Latina' if f in (19800, 20200, 20600, 21000, 21800, 22600) else 'Vestaros'
        text = ship + ' Cargo Setup'
        heading = full_cells(im, font, text, (256 - len(text) * 6) // 2, 2, (230, 230, 230))
        native_image = native5(im)
        different = [(x, y) for y in range(16) for x in range(256)
                     if native_image.getpixel((x, 261 + y)) != atlas.getpixel((x, y))]
        if f == 20600:
            assert len(different) == 246 and all(16 <= x < 44 and 5 <= y < 16 for x, y in different)
        else:
            assert not different
        headings.append({'frame': f, 'title': heading, 'banner_differences': len(different),
                         'entire4096_banner_pixels_exact': not different})
    # These source-bound slot offsets are recorded as native view state, not a
    # claim that a final cartridge save or permanent cargo transfer was committed.
    assert bytes.fromhex(slots[19000][0])[0] == bytes.fromhex(slots[19000][1])[0] == 90
    assert bytes.fromhex(slots[19000][2])[0] == 125
    assert bytes.fromhex(slots[19400][0])[0] == 125
    assert bytes.fromhex(slots[21000][2]) == bytes.fromhex(slots[19000][0])
    assert slots[21000] == slots[21400] == slots[21800] == slots[22600]
    question = Image.open(bs[22200]['path']).convert('RGB')
    confirmation = full_cells(question, font, 'Is this cargo setup okay?', 16, 296, (0, 8, 0))
    frame = PxlImage.from_bytes(before['/_pxl/__frame.pxl'])
    batch = read('translations/frame_action_buttons_graphics_v7.json')
    templates = {r['text']: template(frame, r['box']) for r in batch['records'][15:] if r['text'] not in ('M', 'D')}
    colors = {tuple((w >> s) & 31 for s in (0, 5, 10)) for i in range(83)
              for w in [struct.unpack_from('<H', frame.source, 20 + i * 32 + 18)[0]]}
    leads = []
    for f, shot in bs.items():
        matches = scan_image(shot['path'], templates, colors)
        assert not matches
        leads.append({'frame': f, 'PNG_sha256': shot['PNG_sha256'], 'complete_mask_matches': matches})
    native_rows = []
    for f in (9400, 11800, 12200, 12600, 15000, 17000, 17400):
        raw = (root / f'frame_{f:06d}_arm9_ram.bin').read_bytes()
        u = machine(arm)
        u.mem_write(BASE, raw)
        call(u, 0xCB160, ())
        nations = u.reg_read(UC_ARM_REG_R0)
        call(u, 0x397D8, (nations,))
        own = u.reg_read(UC_ARM_REG_R0)
        call(u, 0x3CCC8, (nations + 4 + own * 0x4C,))
        native_rows.append({'frame': f, 'funds': u.reg_read(UC_ARM_REG_R0), 'own_nation': own})
    assert native_rows == read(ROOT / 'ordinary_purchase_funds.json')
    assert [r['funds'] for r in native_rows] == [38371, 35771, 35771, 35771, 35771, 35671, 35671]
    proof = {'candidate': str(SOURCE), 'candidate_sha256': digest, 'production_ROM_patch_registry_unchanged': True,
             'baseline_frames': sorted(bs), 'all80_whole_two_screen_comparisons_exact': True,
             'unique_compared_pixel_positions': len(bs) * 256 * 384,
             'both22600_frame_cold_boots_no_savestate_or_gameplay_fixtures': True,
             'reports': [br, tr], 'native_read_only_export': state,
             'drawing_calls': control[0], 'filtered_calls': control[1], 'trace_records': rows,
             'overflow': control[3], 'both_positive_controls_and_intact_helper_hooks_tail': True,
             'five_miniature_or_Confirm_shaped_records': 0,
             'negative_scope_only_these_two_original_draw_entries_and_actual_input_path': True,
             'all80_sampled_frames_no_complete_miniature_masks_in_original_bank_colors': leads,
             'original_cached_header_resource_bindings': bindings, 'complete_headings_and_banners': headings,
             'whole_unoccluded_banner_pixels': 8 * 4096, 'source_view_slot_bytes': slots,
             'complete_normal_finish_confirmation_and_B_returns_to_transfer': confirmation,
             'normal_purchase_and_resupply_getter_observations': native_rows,
             'final_cargo_setup_not_committed_or_saved': True,
             'resource_identity_of_earlier_logged_positive_pointer_not_inferred_from_later_RAM': True,
             'ordinary_Confirm_and_five_miniature_parents_and_other_graphics_gates_open': True,
             'all18_original_plaques_incomplete_all22_historical_scopes_retained': True,
             'source_tooltip_control_still_pending': True,
             'full_goal_complete': False, 'script_sha256': sha(Path(__file__).read_bytes())}
    original_report = CAP / 'selection_contexts_v634_two_ship_original' / 'capture_report.json'
    if original_report.exists():
        clean_digest = sha(Path('work/clean.nds').read_bytes())
        original_root, source_run, source_shots, source_receipt = report('selection_contexts_v634_two_ship_original', clean_digest)
        assert source_run['scripted_input_schedule'] == baseline['scripted_input_schedule']
        clean_art = PxlImage.from_bytes(NdsImage.open('work/clean.nds').read_file('/_pxl/tempcargo.pxl'))
        source_banner = native5(clean_art.render())
        diffs = []
        for f in (19000, 19400, 19800, 20200, 20600, 21000, 21400, 21800, 22600):
            im = native5(Image.open(source_shots[f]['path']))
            changed = [(x, y) for y in range(16) for x in range(256)
                       if im.getpixel((x, 261 + y)) != source_banner.getpixel((x, y))]
            if f == 20600:
                # Original 鉄鉱石 has three12-pixel cells and a40-wide hint;
                # current Iron has four6-pixel cells and a28-wide hint.
                assert len(changed) == 371 and all(16 <= x < 56 and 5 <= y < 16 for x, y in changed)
            else:
                assert not changed
            diffs.append({'frame': f, 'different_pixels': len(changed), 'source_tooltip_overlap_only_at20600': f == 20600})
        proof.update({'source_tooltip_control_still_pending': False, 'original_source_banner_controls': diffs})
        proof['reports'].append(source_receipt)
        proof['original_control_root'] = str(original_root)
    save(ROOT / 'release_proof.json', proof)
    print('V634:', control[0], 'bounded draws,80 exact whole frames,9 complete headings,8 full banners;source control pending:',
          proof['source_tooltip_control_still_pending'])


if __name__ == '__main__':
    main()
