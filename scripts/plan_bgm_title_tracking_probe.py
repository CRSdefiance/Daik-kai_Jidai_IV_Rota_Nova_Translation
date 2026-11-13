"""Save an isolated ARM9 rendering probe; this does not create a playable ROM."""
import hashlib
import json
from pathlib import Path

from dk4tool.patch.bgm_title_tracking import PATCH_OFFSET, REPLACEMENT, SOURCE, apply_probe
from dk4tool.rom.nds import NdsImage
from scripts.verify_native_sound_selector import BASE, BASE_SHA


def main():
    if hashlib.sha256(BASE.read_bytes()).hexdigest() != BASE_SHA:
        raise ValueError('Canonical probe baseline changed')
    arm9 = NdsImage.open(BASE).read_file('/__arm9__.bin')
    patched = apply_probe(arm9)
    destination = Path('work/analysis/bgm_title_tracking_probe')
    destination.mkdir(parents=True, exist_ok=True)
    (destination / 'ARM9.bin').write_bytes(patched)
    report = {
        'status': 'research-component-only-not-integrated',
        'base_rom_sha256': BASE_SHA, 'arm9_sha256': hashlib.sha256(patched).hexdigest(),
        'patch_offset': PATCH_OFFSET, 'source_hex': SOURCE.hex(),
        'replacement_hex': REPLACEMENT.hex(),
        'ascii_advance': 5, 'panel_width': 128, 'title_center': 64,
        'draw_local_context_tracking': -1,
        'scope': 'BGM title and following Volume heading in the same local context',
        'font_sixth_column_empty_for_all_printable_ascii': True,
        'runtime_font_metrics_and_visual_behavior_verified': False,
        'runtime_playback_verified': False,
        'limitations': ['Cold-boot visual verification remains required.',
                        'No playable ROM, profile or release layer was produced.',
                        'Packed promotional owners still require classification.'],
    }
    (destination / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
