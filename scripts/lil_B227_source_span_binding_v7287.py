"""Bind three existing renderer BL replacements exactly, with all other instructions unchanged."""
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
def source_span_matches_registered_renderer_branches(arm,source,start,end):
    assert sha(source)=='0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731'
    assert sha(arm)=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
    assert arm==NdsImage.open('out/all_routes_combined_v7277_candidate.nds').read_file('/__arm9__.bin')
    if (start,end)!=(0x2425C,0x243A0):return arm[start:end]==source[start:end]
    # Full 32-bit source/current BL instructions, not pointers or masked wildcard bytes.
    expected={0x242C8:(0xEB00BD91,0xEB0E02BD),0x24310:(0xEB00BD7F,0xEB0E02AB),0x24330:(0xEB00BD77,0xEB0E02A3)}
    restored=bytearray(arm[start:end])
    for at,(old,new) in expected.items():
        assert struct.unpack_from('<I',source,at)[0]==old and struct.unpack_from('<I',arm,at)[0]==new
        restored[at-start:at-start+4]=source[at:at+4]
    assert restored==source[start:end]
    return True
