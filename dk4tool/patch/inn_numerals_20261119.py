"""Use the regular dialogue digits for the three Inn number-format calls."""

from ndspy.code import MainCodeFile

from dk4tool.patch.ascii_glyph_right_bounds import END, assemble
from dk4tool.patch.main_pool_cache_visibility import cache_plan, target
from dk4tool.patch.square_font_scratch_20261027 import ENTRY, stack_painter

BASE = 0x02000000
NUMBER = 0x020ABF50
CALLS = (0x0205CAEC, 0x0205CB0C, 0x0205D274)
HELPER = 0x01FFC334
ITCM = 0x01FFC000


def propose(arm):
    code = MainCodeFile(arm, BASE)
    main, itcm = code.sections[0], code.sections[4]
    if main.ramAddress != BASE or itcm.ramAddress != ITCM or len(itcm.data) != 4096:
        raise ValueError("Unexpected Inn call or ITCM section")
    if bytes(code.save()) != arm:
        raise ValueError("ARM9 must have an exact unmodified round trip")
    if bytes(itcm.data[ENTRY-ITCM:ENTRY-ITCM+len(stack_painter())]) != stack_painter():
        raise ValueError("Square still requires the former static scratch")
    if any(target(arm, call-BASE) != NUMBER for call in CALLS):
        raise ValueError("Each original Inn call must select the native number formatter")

    offset = HELPER-ITCM
    if itcm.data[offset:END-ITCM] != bytes(END-HELPER):
        raise ValueError("Retired Square scratch already in use")
    # These callers supply positive decimal numbers. The original formatter
    # allocates its ring slot and produces 82 4F through 82 58 for digits 0–9.
    # Compact that string in place and return the same pointer.
    body = assemble(f"""
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
    if len(body) != END-HELPER:
        raise ValueError("Inn number helper must fit the retired scratch tail")
    itcm.data[offset:offset+len(body)] = body
    for call in CALLS:
        main.data[call-BASE:call-BASE+4] = assemble(f"bl {HELPER}",call)
    installed = bytes(code.save())
    if cache_plan(installed) != cache_plan(arm):
        raise ValueError("Inn helper changed the staged cache plan")
    for call in CALLS:
        main.data[call-BASE:call-BASE+4] = arm[call-BASE:call-BASE+4]
    itcm.data[offset:offset+len(body)] = bytes(len(body))
    if bytes(code.save()) != arm:
        raise ValueError("Inn helper changed data outside its owned instructions")
    return installed,body
