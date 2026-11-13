"""V653 eight-byte location fixture using unchanged, pinned original point logic."""

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_village_backgrounds_v643 import ARM as REFERENCE_SHA
from scripts.native_village_backgrounds_v643 import relocate as reference_relocate

ARM = 'ab9f748b46388257c9fb847a65b9c06da7920146b985224f5bb0670459ae3fcc'
SPANS = ((0xCB118, 0xCB124), (0xCACAC, 0xCACBC), (0xCB1A8, 0xCB1B4),
         (0x2E58C, 0x2E5A8), (0x36C70, 0x36C94), (0x578E0, 0x57908),
         (0x78654, 0x78840), (0x2C1C4, 0x2C204), (0x69B5C, 0x69E00))


def relocate(arm, raw, village):
    if sha(arm) != ARM or len(raw) != 0x400000 or type(village) is not int or not 0 <= village < 24:
        raise ValueError('Requires exact V653, 4MiB live RAM and original village index0..23')
    reference = NdsImage.open('out/all_routes_combined_v640_candidate.nds').read_file('/__arm9__.bin')
    assert sha(reference) == REFERENCE_SHA
    assert all(arm[a:b] == reference[a:b] for a, b in SPANS)
    current = NdsImage.open('out/all_routes_combined_v653_candidate.nds')
    assert current.read_file('/data/WORLDMAP.DK4') == NdsImage.open('work/clean.nds').read_file('/data/WORLDMAP.DK4')
    # The retained helper already executes the source-pinned V604 coordinate and
    # terrain functions against supplied RAM. Current versions of every relevant
    # function above are exact; no version guard in a historical file is changed.
    after, receipt = reference_relocate(reference, raw, village)
    receipt.update(actual_candidate_ARM9_sha256=sha(arm),
        fixture_current_guard='V664-current-V653',
        unchanged_V640_reference_ARM9_sha256=REFERENCE_SHA,
        original_reference_code_spans_exact_current=[list(s) for s in SPANS])
    return after, receipt
