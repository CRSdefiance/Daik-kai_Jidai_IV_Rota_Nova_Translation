"""Verify saved full UI, every inherited component, selections and native boundaries."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_complete_release import (
    ALLOCATION,
    MANUSCRIPT,
    PROPOSAL_SHA,
    read,
    sha,
)
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.execute_grand_race_name_append import execute as execute_append
from scripts.execute_grand_race_waiting_widgets import TABLE
from scripts.execute_grand_race_waiting_widgets import execute as execute_widgets
from scripts.plan_grand_race_ui_allocation_v136 import CANDIDATE, CANDIDATE_SHA
from scripts.register_grand_race_complete_v137 import overlay
from scripts.register_grand_race_help_v134 import components


def main():
    path = Path('out/all_routes_combined_v137_candidate.nds')
    if sha(CANDIDATE.read_bytes()) != CANDIDATE_SHA:
        raise ValueError('Previous full candidate differs')
    old = components(NdsImage.open(CANDIDATE))
    saved = components(NdsImage.open(path))
    if old.keys() != saved.keys():
        raise ValueError('Saved component identities differ')
    for name, data in old.items():
        if saved[name] != (overlay(data) if name == '/__arm9__.bin' else data):
            raise ValueError(f'Unexpected full candidate component change: {name}')
    arm9 = saved['/__arm9__.bin']
    if sha(arm9) != PROPOSAL_SHA:
        raise ValueError('Saved ROM differs from complete native-reviewed ARM9')
    allocation = read(ALLOCATION)
    messages = {}
    for selection in allocation['selections']:
        lo = selection['offset']
        if arm9[lo:arm9.index(0, lo) + 1] != bytes.fromhex(selection['raw_hex']):
            raise ValueError('Saved complete string, leading/last character or NUL differs')
        for field in selection['pointer_fields']:
            if struct.unpack_from('<I', arm9, field)[0] != 0x02000000 + lo:
                raise ValueError('Saved mapped consumer selects different text')
        messages.setdefault(selection['message'], []).append(selection)
    for row in read(MANUSCRIPT)['records']:
        parts = sorted(messages[row['id'].removeprefix('GRAND_RACE_UI_')],
                       key=lambda part: int(part['key'].rsplit(':', 1)[1]))
        if ' '.join(part['line'] for part in parts) != row['english']:
            raise ValueError('Saved logical English paragraph changed')
    old_common = common_message_entries(old['/COMMON/MESFILE.DK4'], old['/__arm9__.bin'], clean=False)
    new_common = common_message_entries(saved['/COMMON/MESFILE.DK4'], arm9, clean=False)
    if old_common != new_common or len(new_common) != 3668:
        raise ValueError('Inherited native COMMON selections changed')
    widget = execute_widgets(arm9, struct.unpack_from('<3I', arm9, TABLE), scratch_table=False)
    for length in range(17):
        for inserted in (b'B', 'ア'.encode('cp932')):
            case = execute_append(arm9, b'A' * length, inserted, 16, full_return=True)
            expected = b'A' * length + (inserted if length + len(inserted) <= 16 else b'')
            if bytes.fromhex(case['result_hex']) != expected or not case['stack_balanced']:
                raise ValueError('Saved native name entry splits text or damages its stack')
    manifest = read(path.with_suffix('.manifest.json'))
    for key, value in (('candidate_sha256', sha(path.read_bytes())),
                       ('base_sha256', sha(Path(manifest['base_rom']).read_bytes())),
                       ('release_stack_sha256', sha(Path('translations/release_stack.json').read_bytes()))):
        if manifest[key] != value:
            raise ValueError('Saved manifest lineage differs')
    if manifest['profile'] != 'all-routes-unified-v137' or len(manifest['batches']) != 435 or not all(manifest['checks'].values()):
        raise ValueError('Saved complete profile/checks differ')
    report = {'status': 'pass', 'candidate_sha256': sha(path.read_bytes()),
              'arm9_sha256': sha(arm9), 'profile': manifest['profile'], 'batch_count': 435,
              'complete_messages': len(messages), 'saved_strings': len(allocation['selections']),
              'all_other_V136_components_byte_exact': True, 'native_COMMON_selections_exact': 3668,
              'saved_native_waiting_widgets': widget, 'saved_native_name_boundary_cases': 34,
              'full_native_printf_and_frame_proposal_sha_matches': True,
              'runtime_verified': False}
    Path('work/analysis/grand_race_complete_v137_saved_proof.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Saved V137 passes: 51 complete messages / 60 strings; 435 batches; all inherited components and 3,668 COMMON selections preserved.')


if __name__ == '__main__':
    main()
