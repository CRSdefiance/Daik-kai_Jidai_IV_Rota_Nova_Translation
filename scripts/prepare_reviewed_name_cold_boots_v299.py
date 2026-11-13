"""Ordinary route input schedules and a declared Maria selection test fixture."""

import json
import struct

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_reviewed_name_release_v299 import ROOT, read
from scripts.verify_reviewed_name_release_v299 import ROM


def main():
    for name in ('rafael', 'hodram', 'maria'):
        report = read(f'work/emulation_v193/name_editorial_v280_{name}/capture_report.json')
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        (ROOT / f'{name}_inputs.json').write_text(json.dumps(report['scripted_input_schedule'], indent=2) + '\n', encoding='utf-8')
    previous = read('work/emulation_v193/artwork_captions_v298/capture_report.json')
    (ROOT / 'lil_inputs.json').write_text(json.dumps(previous['scripted_input_schedule'], indent=2) + '\n', encoding='utf-8')
    image = NdsImage.open(ROM)
    original = image.read_file('/__arm9__.bin')
    assert struct.unpack_from('<I', original, 0x9F068)[0] == 0x03A00003
    arm = bytearray(original)
    struct.pack_into('<I', arm, 0x9F068, 0x03A00004)
    assert [i for i, (a, b) in enumerate(zip(original, arm, strict=True)) if a != b] == [0x9F068]
    image.replace_file('/__arm9__.bin', bytes(arm))
    fixture = ROOT / 'maria_selection_research_only.nds'
    image.save(fixture)
    manifest = {'format': 'dk4-review-name-route-cold-boot-fixtures-v299',
                'production_ROM': str(ROM), 'production_ROM_sha256': sha(ROM.read_bytes()),
                'Maria_test_ROM': str(fixture), 'Maria_test_ROM_sha256': sha(fixture.read_bytes()),
                'only_Maria_test_arm9_byte': 0x9F068, 'Maria_is_not_legitimate_unlock_or_playable_handoff': True,
                'production_full_goal_complete': False}
    (ROOT / 'cold_boot_fixture_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print('Three production route schedules; Maria declared one-byte test selection fixture; no savestate.')


if __name__ == '__main__':
    main()
