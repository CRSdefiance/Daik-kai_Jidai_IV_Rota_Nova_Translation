"""Original source art composed at observed scanline reads, with no delay fit."""

import struct
from pathlib import Path

from capstone import CS_ARCH_X86, CS_MODE_64, Cs
from capstone.x86 import X86_OP_IMM, X86_OP_MEM
from ndspy.code import loadOverlayTable
from PIL import Image
from unicorn import UC_ARCH_X86, UC_MODE_64, Uc
from unicorn import x86_const as xr
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.compression_probe import decompress_lz10
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.observe_transition_scanlines_v659 import ENTRIES, PROLOGUES, jump
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.research_committed_composition_v646 import render_order, vram_bindings
from scripts.research_ending_transitions_v642 import compose
from scripts.verify_movie_transition_bitmaps_v648 import BAYER, rgb
from scripts.verify_opening_composition_v646 import checked_export
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/transition_scanlines_v659')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def core_entries(observer):
    """Bind the three host methods to declared VCount-driven HBlank calls."""
    raw = CORE.read_bytes()
    pe = struct.unpack_from('<I', raw, 60)[0]
    count, optional = struct.unpack_from('<H', raw, pe + 6)[0], pe + 24
    imagebase = struct.unpack_from('<Q', raw, optional + 24)[0]
    optsize = struct.unpack_from('<H', raw, pe + 20)[0]
    sections = [struct.unpack_from('<4I', raw, optional + optsize + i * 40 + 8) for i in range(count)]

    def span(rva, size):
        for _, start, length, offset in sections:
            if start <= rva and rva + size <= start + length:
                return raw[offset + rva - start:offset + rva - start + size]
        raise ValueError('Core code span not file-backed')

    rva, size = struct.unpack_from('<2I', raw, optional + 112 + 3 * 8)
    pdata = span(rva, size)
    functions = {start: end for start, end, unwind in struct.iter_unpack('<3I', pdata)}
    decoder = Cs(CS_ARCH_X86, CS_MODE_64)
    decoder.detail = True
    instructions = list(decoder.disasm(span(0x10CEE0, functions[0x10CEE0] - 0x10CEE0), imagebase + 0x10CEE0))
    indexes = {ins.address - imagebase: i for i, ins in enumerate(instructions)}
    runtimebase = observer['host_core_entry_detours_only_in_diagnostic_process'][0]['address'] - ENTRIES[0][0]
    vcount = observer['SFORMAT_anchors']['_VCT']['runtime_address'] - runtimebase + imagebase
    rows = []
    for (target, count, label), prefix, caller in zip(ENTRIES, PROLOGUES, (0x10D93D, 0x10DF62, 0x10DF4F), strict=True):
        assert target in functions and span(target, count).hex() == prefix
        i = indexes[caller]
        ins = instructions[i]
        assert ins.mnemonic == 'call' and ins.operands[0].type == X86_OP_IMM
        assert ins.operands[0].imm == imagebase + target
        load_count, load_this = instructions[i - 2:i]
        assert load_this.mnemonic == 'mov' and load_this.op_str == 'rcx, qword ptr [rdi]'
        assert load_count.mnemonic == 'mov' and load_count.reg_name(load_count.operands[0].reg) == 'edx'
        source = load_count.operands[1]
        assert source.type == X86_OP_MEM and load_count.reg_name(source.mem.base) == 'rip'
        assert load_count.address + load_count.size + source.mem.disp == vcount
        rows.append({'format': label, 'source_HBlank_call_RVA': caller,
                     'declared_host_function_RVAs': [target, functions[target]],
                     'line_argument_from_exact_original_VCount_SFORMAT': True,
                     'this_argument_from_original_GPU_pointer': True,
                     'complete_relocation_free_prefix': prefix})
    assert all(any(ins.mnemonic == 'cmp' and ins.operands[-1].type == X86_OP_IMM
                   and ins.operands[-1].imm == value for ins in instructions)
               for value in (0x20005145, 0x20006186, 0x20008208))
    return rows


def prologue_controls():
    regs = [getattr(xr, 'UC_X86_REG_' + name) for name in
            ('RAX', 'RBX', 'RCX', 'RDX', 'RSI', 'RDI', 'RBP', 'R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'RSP', 'EFLAGS')]
    rows = []
    for (_, count, label), pattern in zip(ENTRIES, PROLOGUES, strict=True):
        prefix = bytes.fromhex(pattern)
        assert len(prefix) == count
        for line in (0, 79, 80, 191):
            outcomes = []
            for relocated in (False, True):
                u = Uc(UC_ARCH_X86, UC_MODE_64)
                for address in (0x1000000, 0x2000000, 0x3000000):
                    u.mem_map(address, 0x10000)
                u.mem_write(0x3000000, b'\xA5' * 0x10000)
                for i, reg in enumerate(regs):
                    u.reg_write(reg, 0x55550000 + 16 * i)
                u.reg_write(xr.UC_X86_REG_RCX, 0x123456789ABC)
                u.reg_write(xr.UC_X86_REG_RDX, line)
                u.reg_write(xr.UC_X86_REG_RSP, 0x3008008)
                u.reg_write(xr.UC_X86_REG_EFLAGS, 0x202)
                u.mem_write(0x1000000, prefix)
                u.mem_write(0x2000000, prefix + jump(0x1000000 + count))
                u.emu_start(0x2000000 if relocated else 0x1000000, 0x1000000 + count, count=100)
                assert u.reg_read(xr.UC_X86_REG_RIP) == 0x1000000 + count
                outcomes.append(([u.reg_read(r) for r in regs], bytes(u.mem_read(0x3000000, 0x10000))))
            assert outcomes[0] == outcomes[1]
            rows.append({'format': label, 'line_argument': line,
                         'original_and_relocated_prefix_all_GPR_flags_stack_exact': True})
    return rows


def pixels(shot):
    assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
    image = Image.open(shot['path']).convert('RGB')
    assert image.size == (256, 384)
    return list(image.get_flattened_data())


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(CORE.read_bytes()) == CORE_SHA
    assert sha(Path(pre['prior_transition_proof']).read_bytes()) == pre['prior_transition_proof_sha256']
    prior = read(pre['prior_transition_proof'])
    assert prior['32_controlled_original_phase_calls_all98304_bitmap_bytes_exact']
    assert prior['all16_replayed_upper_scene_instructions_exact_original_clean_ARM9_and_overlay0']
    roms = {'current': NdsImage.open(pre['candidate']), 'clean': NdsImage.open('work/clean.nds')}
    original_code = machine(roms['clean'].read_file('/__arm9__.bin'))
    current_code = machine(roms['current'].read_file('/__arm9__.bin'))
    for label, cpu in (('clean', original_code), ('current', current_code)):
        rom = roms[label]
        for overlay in loadOverlayTable(rom.rom.arm9OverlayTable, lambda _, fid, rom=rom: rom.files[fid]).values():
            cpu.mem_write(overlay.ramAddress, bytes(overlay.data))
    inherited_instructions = set()
    for case in prior['routes']['lil']['controlled_original_dissolve_phase_family'].values():
        inherited_instructions.update(case['execution']['all_executed_instruction_words_exact_registered_ROM'])
    for address in inherited_instructions:
        assert current_code.mem_read(address, 4) == original_code.mem_read(address, 4)
    for address, size in ((0x020E2744, 0x80), (0x01FF9898, 0x6C)):
        assert current_code.mem_read(address, size) == original_code.mem_read(address, size)
    packed = roms['current'].read_file('/towngrp/towngrp03.pxl')
    assert packed == roms['clean'].read_file('/towngrp/towngrp03.pxl')
    decoded = decompress_lz10(packed) if packed[0] == 16 else packed
    picture = PxlImage.from_bytes(decoded)
    assert (picture.width, picture.height, picture.bits_per_pixel) == (256, 192, 8)
    palette_bytes = decoded[struct.unpack_from('<I', decoded, 12)[0]:][:512]
    palette = struct.unpack('<256H', palette_bytes)
    photo_words = [palette[i] for i in picture.indices]
    assert all(w & 32768 for w in photo_words)
    photo_rgb = rgb(photo_words)
    exporter = sha(Path('scripts/inspect_committed_gpu_v646.py').read_bytes())
    reports, observed, source_cases, row_masks, models = {}, {}, [], {}, {}
    source_entries = {}
    baseline_pairs = []
    for label, rom in roms.items():
        folder = CAP / ('transition_scanlines_v659_' + label + '_observed')
        rp, bp = folder / 'capture_report.json', CAP / ('transition_scanlines_v659_' + label + '_baseline/capture_report.json')
        report, baseline = read(rp), read(bp)
        digest = sha(rom.source.read_bytes())
        for r in (report, baseline):
            assert r['ROM_sha256'] == digest and r['core_DLL_sha256'] == CORE_SHA
            assert r['frames'] == 2868 and r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
            assert not r.get('battery_save_preloaded') and not any(k.startswith('synthetic_') for k in r)
            assert r['scripted_input_schedule'] == read(pre['inputs'])
            seen_frames = {}
            for shot in r['frames_captured']:
                values = pixels(shot)
                if shot['frame'] in seen_frames:
                    assert values == seen_frames[shot['frame']]
                seen_frames[shot['frame']] = values
        assert report['core_options'] == baseline['core_options']
        shots, base = ({s['frame']: s for s in r['frames_captured']} for r in (report, baseline))
        assert shots.keys() == base.keys() and len(shots) == 15
        for frame in shots:
            assert pixels(shots[frame]) == pixels(base[frame])
            baseline_pairs.append({'build': label, 'frame': frame,
                'observed': shots[frame], 'unmodified_core_baseline': base[frame],
                'all98304_two_screen_RGB_pixels_exact': True})
        op = folder / 'scanlines/scanline_observer.json'
        observer = read(op)
        assert observer['all_entry_bytes_restored_and_DLL_file_unchanged'] and not observer['errors']
        assert observer['script_sha256'] == sha(Path('scripts/observe_transition_scanlines_v659.py').read_bytes())
        assert observer['no_game_ROM_RAM_VRAM_register_or_input_writes']
        source_entries[label] = core_entries(observer)
        assert set(map(int, observer['frames'])) == set(pre['scanline_frames'])
        for patch, (rva, count, fmt), expected in zip(observer['host_core_entry_detours_only_in_diagnostic_process'], ENTRIES, PROLOGUES, strict=True):
            assert (patch['RVA'], patch['stolen_bytes'], patch['format'], patch['original_hex']) == (rva, count, fmt, expected)
            assert bytes.fromhex(patch['detour_hex'])[:6] == b'\xff\x25\0\0\0\0'
            assert bytes.fromhex(patch['trampoline_hex']) == bytes.fromhex(expected) + jump(patch['address'] + count)
            assert patch['relocated_prefix_has_no_PC_relative_memory_branch_or_call']
        observed[label] = {'shots': shots, 'observer': observer, 'report': report}
        row_masks[label] = {}
        for frame, value in observer['frames'].items():
            frame = int(frame)
            for f in value['files'].values():
                assert sha(Path(f['path']).read_bytes()) == f['sha256']
            words = struct.unpack('<49152H', Path(value['files']['bitmap_row']['path']).read_bytes())
            io = Path(value['files']['IO']['path']).read_bytes()
            assert len(value['rows']) == 192
            for line, row in enumerate(value['rows']):
                assert (row['line'], row['VCount'], row['frame'], row['format']) == (line, line, frame, '555')
                assert row['original_render_called_once_and_returned']
                registers = io[line * 8192:(line + 1) * 8192]
                assert struct.unpack_from('<I', registers)[0] == 0x1191B
                assert struct.unpack_from('<H', registers, 14)[0] == 0x4084
                assert struct.unpack_from('<H', registers, 8)[0] & 3 == 1
                assert registers[0x243] == 0x81
                assert struct.unpack_from('<4h2I', registers, 0x30) == (256, 0, 0, 256, 0, line * 256)
                assert struct.unpack_from('<3H', registers, 0x50) == (0, 0, 0)
                assert struct.unpack_from('<H', registers, 0x6C)[0] == 0
                actual = words[line * 256:(line + 1) * 256]
                source = photo_words[line * 256:(line + 1) * 256]
                assert all(w == 0 or w == expected for w, expected in zip(actual, source, strict=True))
                assert any(all(bool(w & 32768) == (BAYER[(line % 4) * 4 + x % 4] <= phase)
                    for x, w in enumerate(actual)) for phase in range(-1, 16))
            row_masks[label][frame] = words
        movie = FlsArchive(rom.read_file('/FLS/M22.fls'))
        for state in report['read_only_capture_GPU_states']:
            frame = state['frame']
            committed = checked_export(state, exporter)
            raw = Path(state['files']['arm9_main_ram.bin']['path']).read_bytes()
            assert sha(raw) == state['main_RAM_sha256']
            cpu = machine(rom.read_file('/__arm9__.bin'))
            cpu.mem_write(BASE, raw)
            call(cpu, 0x7F244, ())
            assert cpu.reg_read(UC_ARM_REG_R0) == 2
            header = 0x02276D74 - BASE
            flags, width, height, paloff, pixoff = struct.unpack_from('<5I', raw, header)
            assert (flags, width, height) == struct.unpack_from('<3I', decoded)
            assert raw[header + paloff:header + paloff + 512] == palette_bytes
            assert raw[header + pixoff:header + pixoff + 49152] == picture.indices
            bindings, resources = vram_bindings(committed, movie)
            ordered, order = render_order(committed)
            backdrop, draws = compose(ordered, movie, bindings)
            raster = Path(state['files']['gpu_framebuffer_RGBA8888.bin']['path']).read_bytes()
            diagnostic = rgb([raster[i] >> 3 | (raster[i + 1] >> 3) << 5 | (raster[i + 2] >> 3) << 10
                              for i in range(0, len(raster), 4)])
            assert diagnostic == backdrop
            words = row_masks[label][frame]
            expected = [photo_rgb[i] if w & 32768 else backdrop[i] for i, w in enumerate(words)]
            actual = pixels(shots[frame])[:49152]
            assert expected == actual
            models[label, frame] = expected
            source_cases.append({'build': label, 'frame': frame, 'whole49152_upper_RGB_pixels_exact': True,
                'source_photo_palette_indices_and_every_opaque_sample_exact_original': True,
                'opacity_observed_before_original_RenderLine_not_from_PNG_or_finished_framebuffer': True,
                'original_affine_origin_size_priority_no_blend_and_bankD_mapping_pass': True,
                'original_FLS_ROM_resources': resources, 'render_order': order, 'native_draws': draws,
                'full3D_framebuffer_compared_only_as_diagnostic_not_used_as_source': True,
                'no_per_frame_or_per_row_delay_fit_no_waived_pixels': True})
        reports[label] = {'observed': str(rp), 'observed_sha256': sha(rp.read_bytes()),
                         'baseline': str(bp), 'baseline_sha256': sha(bp.read_bytes()),
                         'scanline_observer': str(op), 'scanline_observer_sha256': sha(op.read_bytes())}
    comparisons = []
    for frame in pre['scanline_frames']:
        a, b = [pixels(observed[label]['shots'][frame]) for label in ('current', 'clean')]
        delta = [i for i, (x, y) in enumerate(zip(a, b, strict=True)) if x != y]
        assert bool(delta) == (frame == 2865)
        if delta:
            assert len(delta) == 63 and {i // 256 for i in delta} == {79}
            assert all(i % 4 == 3 for i in delta)
        comparisons.append({'frame': frame, 'two_screen_RGB_differences': len(delta), 'positions': delta})
    new, old = (row_masks[label][2865] for label in ('current', 'clean'))
    mask_delta = [i for i, (a, b) in enumerate(zip(new, old, strict=True)) if a != b]
    assert len(mask_delta) == 64 and {i // 256 for i in mask_delta} == {79}
    assert all(i % 4 == 3 and new[i] == 0 and old[i] == photo_words[i] and BAYER[15] == 5 for i in mask_delta)
    expected_delta = [i for i, (a, b) in enumerate(zip(models['current', 2865], models['clean', 2865], strict=True)) if a != b]
    assert expected_delta == next(r['positions'] for r in comparisons if r['frame'] == 2865)
    coincident = sorted(set(mask_delta) - set(expected_delta))
    assert len(coincident) == 1
    pcs = {}
    for label, pc in (('current', 0x020E2750), ('clean', 0x01FF98D4)):
        value = observed[label]['observer']['frames']['2865']
        row = value['rows'][79]
        assert row['ARM9_PC'] == pc
        registers = struct.unpack_from('<16I', Path(value['files']['CPU_registers']['path']).read_bytes(), 79 * 64)
        if label == 'current':
            assert registers[:4] == (3, 0x022F9794, 0x06000000, 0x18000)
        else:
            assert (registers[3], registers[4], registers[5], registers[6], registers[7]) == (
                0x040000D4, 0x8000C000, 0x06000000, 0x022F9794, 3)
        pcs[label] = {'pending_ARM9_PC': pc, 'all_registers': registers,
                      'source_and_destination_same_original_upper_bitmap_DMA_channel3': True}
    proof = {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'reports': reports, 'four_terminal2868_frame_ordinary_New_Game_runs_no_savestate_or_gameplay_fixtures': True,
        'three_declared_host_RenderLine_methods_bound_to_original_VCount_HBlank_calls': source_entries,
        'twelve_relocated_host_prefix_GPR_flags_and_full_stack_controls': prologue_controls(),
        'all30_whole_two_screen_observer_vs_unmodified_core_baselines': baseline_pairs,
        'all4608_original_RenderLine_calls_before_read_IO_CPU_and_source_bitmap_rows': True,
        'all1179648_source_bitmap_words_zero_or_exact_original_photo_and_native_dissolve_phase': True,
        'inherited_original_dissolve_instruction_words_current_clean_exact': sorted(inherited_instructions),
        'inherited_V648_phase_family_proof_sha256': pre['prior_transition_proof_sha256'],
        'ten_complete_independent_same_frame_upper_RGB_source_compositions': source_cases,
        'independent_whole_upper_RGB_comparisons': len(source_cases) * 49152,
        'current_vs_clean_twelve_transition_frames': comparisons,
        'frame2865_source_opacity_changes64_original_threshold5_positions': mask_delta,
        'frame2865_exact63_RGB_differences_predicted_with_no_delay_fit': expected_delta,
        'one_source_opacity_change_has_coincident_original_photo_and_3D_RGB': coincident,
        'scanline79_original_DMA_program_positions': pcs,
        'host_observer_does_not_write_game_RAM_VRAM_CPU_registers_ROM_or_inputs': True,
        'this_resolves_the_specific_V648_Lil63_pixel_scanline_timing_comparison': True,
        'not_an_independent_emulation_of_every_DMA_cycle_or_hardware_device_verification': True,
        'other_routes_transitions_unsampled_frames_and_broader_graphics_gates_remain_open': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
        'all18_original_plaques_incomplete22_historical_scopes_retained': True, 'full_goal_complete': False,
        'scripts': {str(p): sha(p.read_bytes()) for p in (Path(__file__),
            Path('scripts/observe_transition_scanlines_v659.py'), Path('scripts/run_transition_scanlines_v659.py'))}}
    save(ROOT / 'proof.json', proof)
    print('V659: 4608 observed source scanlines;30 full baselines;10 whole source RGB compositions;64 opacity/63 RGB edge independently predicted.')


if __name__ == '__main__':
    main()
