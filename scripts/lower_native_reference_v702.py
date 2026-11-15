"""Version-bound complete native cursor states, not a same-frame clock oracle."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine
from scripts.verify_movie_transition_bitmaps_v648 import rgb
from scripts.verify_village_wrap_v608 import read

ROOT = Path('work/analysis/equipment_cursor_v663')


def reference(current):
    pre = read(ROOT / 'preflight.json')
    historical = Path(pre['candidate'])
    assert sha(historical.read_bytes()) == pre['candidate_sha256']
    old = NdsImage.open(historical)
    pxls = [(p, data) for _, p, data in current.iter_files() if p.lower().endswith('.pxl')]
    assert len(pxls) == 660 and all(data == old.read_file(p) for p, data in pxls)
    phase_path = ROOT / 'phase_candidates.json'
    phase = read(phase_path)
    assert phase['native_script_sha256'] == sha(Path('scripts/research_equipment_cursor_v663.py').read_bytes())
    rows = [r for r in phase['native_rows'] if r['frame'] == 8000]
    assert len(rows) == 2 and {r['controlled_blink_visible'] for r in rows} == {False, True}
    models = []
    for image in (old, current):
        arm = image.read_file('/__arm9__.bin')
        u = machine(arm)
        u.mem_write(POOL, bytes(MainCodeFile(arm, 0x02000000).sections[3].data[:-48]))
        overlay = loadOverlayTable(image.rom.arm9OverlayTable, lambda _, f, image=image: image.rom.files[f])[0]
        u.mem_write(overlay.ramAddress, bytes(overlay.data))
        models.append(u)
    outputs, references = {}, []
    for row in rows:
        assert row['whole98304_bytes_written_over_poison']
        assert row['original_fragment_ABI_guards_and_registered_instruction_bytes_pass']
        assert row['no_output_read_before_write_no_visible_VRAM_source_no_VRAM_write']
        assert all(pc % 4 == 0 and bytes(models[0].mem_read(pc, 4)) == bytes(models[1].mem_read(pc, 4)) for pc in row['executed'])
        label = 'on' if row['controlled_blink_visible'] else 'off'
        path = ROOT / ('native_lower_8000_' + label + '.bin')
        binary = path.read_bytes()
        assert len(binary) == 98304 and sha(binary) == row['lower_sha256']
        image = Image.new('RGB', (256, 192))
        image.putdata(rgb(struct.unpack('<49152H', binary)))
        outputs[label] = image.tobytes()
        references.append({'state': label, 'binary': str(path), 'sha256': sha(binary),
            'all_recorded_current_instruction_words_exact': len(row['executed']),
            'whole49152_pixel_original_native_scene_not_a_ring_mask': True})
    return outputs, {'historical_ROM': str(historical), 'historical_ROM_sha256': pre['candidate_sha256'],
        'phase_proof': str(phase_path), 'phase_proof_sha256': sha(phase_path.read_bytes()),
        'all660_production_PXL_files_exact_historical_source': True, 'states': references,
        'SDK_clock_inputs_were_explicit_native_reference_inputs_not_observed_current_tick_values': True,
        'membership_in_complete_native_state_does_not_predict_current_clock_phase': True,
        'source_sha256': sha(Path(__file__).read_bytes())}
