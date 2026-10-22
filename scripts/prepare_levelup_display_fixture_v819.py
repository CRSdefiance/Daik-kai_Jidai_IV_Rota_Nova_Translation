"""Disposable six-stat display fixture; never a playable release or earned XP.

User-authorized testing cheats force the source's legitimate maximum row count.
Only the Temple physical-XP test is run. The original caller already reserves
six ID words for the case where both groups grow, and the two source tables
are contiguous0..5. Native stat setters, cap handling, number formatting, raw
modal construction, pager and input remain in use. Two fixture-only instructions
must never enter a production adapter or registered candidate.
"""

import struct

from keystone import Ks,KS_ARCH_ARM,KS_MODE_ARM

from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.levelup_format_runtime_v819 import ROOT,BASE,apply
from scripts.verify_village_wrap_v608 import save


def main():
    rom=NdsImage.open('out/all_routes_combined_v809_candidate.nds')
    old=rom.read_file('/__arm9__.bin');production=apply(old);arm=bytearray(production)
    first,second=struct.unpack_from('<2I',old,0x7E2E0)
    assert second==first+12 and struct.unpack_from('<6I',old,first-BASE)==tuple(range(6))
    ka=Ks(KS_ARCH_ARM,KS_MODE_ARM);patches=[]
    for at,before,after in ((0x7E240,'cmp r3,#3','cmp r3,#6'),
                            (0x7E4C0,'add sl,r8,r0,asr#1','mov sl,#3')):
        original=bytes(ka.asm(before,BASE+at)[0]);new=bytes(ka.asm(after,BASE+at)[0])
        assert len(original)==len(new)==4 and old[at:at+4]==original
        arm[at:at+4]=new
        patches.append(dict(address=BASE+at,before_hex=original.hex(),after_hex=new.hex(),
            original_instruction=before,fixture_instruction=after))
    assert sum(a!=b for a,b in zip(production,arm,strict=True))<=8
    rom.replace_file('/__arm9__.bin',bytes(arm))
    path=ROOT/'levelup_v819_SIX_STAT_DISPLAY_FIXTURE.nds'
    assert not path.exists();rom.save(path)
    save(ROOT/'six_stat_display_fixture_provenance.json',dict(
        synthetic_display_fixture=True,not_a_release_and_never_for_handoff=True,
        ROM=str(path),ROM_sha256=sha(path.read_bytes()),
        parent='out/all_routes_combined_v809_candidate.nds',parent_sha256=sha(rom.source.read_bytes()),
        repair_ARM9_sha256=sha(production),fixture_ARM9_sha256=sha(bytes(arm)),
        fixture_only_patches=patches,original_six_ID_order=list(range(6)),
        original_maximum_six_ID_stack_capacity_proven=True,
        synthetic_growth_does_not_claim_earned_levels_or_ordinary_outcomes=True,
        runtime_pager_names_numbers_stat_setters_and_input_not_replaced=True,
        scenario='Only isolated Temple preparations, copied V815 day24 donor.',
        production_module_must_not_contain_these_two_fixture_changes=True,
        producer_sha256=sha(open(__file__,'rb').read())))
    print('Separate six-stat display fixture created; two extra test-only instructions, never a release.',flush=True)


if __name__=='__main__':main()
