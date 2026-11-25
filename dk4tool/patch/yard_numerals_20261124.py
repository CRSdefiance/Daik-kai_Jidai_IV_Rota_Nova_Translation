"""Reuse the installed Inn ASCII digit conversion for Yard numeric arguments."""

from keystone import KS_ARCH_ARM, KS_MODE_THUMB, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.ascii_glyph_right_bounds import assemble
from dk4tool.patch.inn_numerals_20261119 import BASE, HELPER, ITCM, NUMBER
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.shipyard_editorial import DAY_RETURN, PRICE_RETURNS, QUANTITY


QUANTITY_DIGITS = 0x02131F66
REFIT_DAY_RETURN = 0x02017B90
DURATION_CALLS = {DAY_RETURN - 4, REFIT_DAY_RETURN - 4}
QUANTITY_CALLS = tuple(sorted({pc - 4 for pc in PRICE_RETURNS} | DURATION_CALLS))
REFUND = "ARM9_REFIT_REFUND"
BARE_CALLS = {
    0x02017B18: 1263,
    0x02017ED4: 1245,
    0x02017EF4: 1246,
    0x02017F50: REFUND,
    0x020624D0: 798,
    0x020630FC: 1245,
    0x0206347C: 786,
    0x0206348C: 786,
}
SUFFIX_CALLS = {
    0x02017B8C: 1267,
    0x020620B8: 802,
    0x02062354: 799,
    0x02062374: 800,
    0x02062648: 789,
    0x02063140: 804,
    0x02063174: 803,
    0x02063180: 803,
}


def compact_helper():
    """Exact bytes already installed by the registered Inn numeral fix."""
    return assemble(f"""
        push {{r4,lr}}
        bl {NUMBER}
        mov r1,r0
        mov r2,r0
    digit:
        ldrb r3,[r1],#2
        cmp r3,#0
        ldrbne r3,[r1,#-1]
        subne r3,r3,#0x1f
        strb r3,[r2],#1
        bne digit
        pop {{r4,pc}}
    """, HELPER)


def thumb_call(destination):
    return bytes(Ks(KS_ARCH_ARM, KS_MODE_THUMB).asm(f"blx {destination}", QUANTITY_DIGITS)[0])


def propose(arm, original):
    code = MainCodeFile(arm, BASE)
    main, itcm = code.sections[0], code.sections[4]
    assert main.ramAddress == BASE and itcm.ramAddress == ITCM and len(itcm.data) == 4096
    assert bytes(code.save()) == arm and tuple(SUFFIX_CALLS) == QUANTITY_CALLS
    helper = compact_helper()
    assert len(helper) == 44 and bytes(itcm.data[HELPER - ITCM:HELPER - ITCM + len(helper)]) == helper
    assert arm[NUMBER - BASE:NUMBER - BASE + 0x7C] == original[NUMBER - BASE:NUMBER - BASE + 0x7C]
    paths = []
    for address, message_id in SUFFIX_CALLS.items():
        expected = assemble(f"bl {QUANTITY}", address)
        assert bytes(main.data[address-BASE:address-BASE+4]) == expected
        stock = assemble(f"bl {NUMBER}", address)
        assert original[address-BASE:address-BASE+4] == stock
        paths.append(dict(call=address, message_ID=message_id, clean_hex=stock.hex(), previous_hex=expected.hex()))
    replacement = {site: (assemble(f"bl {NUMBER}", site), assemble(f"bl {HELPER}", site)) for site in BARE_CALLS}
    assert all(original[loc-BASE:loc-BASE+4] == old for loc, (old, _) in replacement.items())
    replacement[QUANTITY_DIGITS] = (thumb_call(NUMBER), thumb_call(HELPER))
    assert replacement[QUANTITY_DIGITS][0] == bytes.fromhex("79f7f4ef")
    mutations = []
    for site, (before, after) in replacement.items():
        offset = site - BASE
        assert len(before) == len(after) == 4 and bytes(main.data[offset:offset+4]) == before
        main.data[offset:offset+4] = after
        mutations.append(dict(address=site, before_hex=before.hex(), after_hex=after.hex()))
    target = bytes(code.save())
    assert cache_plan(target) == cache_plan(arm)
    for site, (before, _) in replacement.items():
        main.data[site-BASE:site-BASE+4] = before
    assert bytes(code.save()) == arm
    return target, mutations, paths
