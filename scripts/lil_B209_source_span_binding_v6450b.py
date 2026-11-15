"""Distinguish unchanged instructions from three already-registered renderer pointer words."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read
def source_span_matches_registered_pointer_literals(arm,source,start,end):
    # Both exact image hashes are mandatory; this is no arbitrary masked span allowance.
    assert sha(source)=='0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731'
    assert sha(arm)=='4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351'
    predecessor=NdsImage.open('out/all_routes_combined_v6380_candidate.nds').read_file('/__arm9__.bin');assert arm==predecessor
    if (start,end)!=(0x2425C,0x243A0):return arm[start:end]==source[start:end]
    expected={0x242C8:(0x0200BD91,0x020E02BD),0x24310:(0x0200BD7F,0x020E02AB),0x24330:(0x0200BD77,0x020E02A3)}
    restored=bytearray(arm[start:end])
    for at,(old,new) in expected.items():
        assert struct.unpack_from('<I',source,at)[0]==old and struct.unpack_from('<I',arm,at)[0]==new
        restored[at-start:at-start+4]=source[at:at+4]
    assert restored==source[start:end]
    return True
