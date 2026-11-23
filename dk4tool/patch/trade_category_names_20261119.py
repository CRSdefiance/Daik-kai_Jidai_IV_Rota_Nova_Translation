"""Use full category names in the Goods Info panel's two native callers."""

from struct import pack_into, unpack_from

from ndspy.code import MainCodeFile

from dk4tool.patch.ascii_glyph_right_bounds import assemble
from dk4tool.patch.category_dialogue_lookup import ADDRESS_BASE, BASE, GETTER, TABLE
from dk4tool.patch.main_pool_cache_visibility import cache_plan, target
from dk4tool.patch.market_goods_info_terminator_v1 import CAPTURE, OLD_FORMAT
from dk4tool.patch.square_font_scratch_20261027 import ENTRY, stack_painter

CALLS = (0x020C3DE8,0x020C3F64)
HELPER, END = 0x01FFC1DC,0x01FFC200
ITCM = 0x01FFC000
TEXTILE_INDEX = 8
TEXTILES = b"Textiles\0"


def propose(arm):
    code = MainCodeFile(arm,BASE)
    main,itcm = code.sections[0],code.sections[4]
    if main.ramAddress!=BASE or itcm.ramAddress!=ITCM or bytes(code.save())!=arm:
        raise ValueError("Unexpected Trade instruction or section ownership")
    if bytes(itcm.data[ENTRY-ITCM:ENTRY-ITCM+len(stack_painter())])!=stack_painter():
        raise ValueError("Square still uses its former static scratch")
    if any(target(arm,pc-BASE)!=GETTER for pc in CALLS):
        raise ValueError("Goods Info no longer calls the expected category getter")
    start,stop = HELPER-ITCM,END-ITCM
    if itcm.data[start:stop]!=bytes(stop-start):
        raise ValueError("Trade helper has no verified empty span")
    string_start,string_end = OLD_FORMAT-ITCM,CAPTURE-ITCM
    if bytes(itcm.data[string_start:string_end])!=b"%s\n  %s %d%%":
        raise ValueError("Former Goods Info format bytes changed")

    offset = TABLE+TEXTILE_INDEX*4
    old_row, = unpack_from("<I",main.data,offset)
    old_pointer = (old_row & 0xFFFFFF)+ADDRESS_BASE
    if arm[old_pointer-BASE:old_pointer-BASE+6]!=b"Fiber\0":
        raise ValueError("The full textile category no longer selects Fiber")
    new_row = (old_row & 0xFF000000)|(OLD_FORMAT-ADDRESS_BASE)
    pack_into("<I",main.data,offset,new_row)
    itcm.data[string_start:string_end] = TEXTILES.ljust(string_end-string_start,b"\0")

    # The percentage can occupy five digits. Keep Metals in this view so the
    # longest supported value fits. An out-of-domain ID uses the original path.
    body = assemble(f"""
        cmp r0,#6
        cmpne r0,#18
        bhs {GETTER}
        ldr r1,table
        ldr r1,[r1,r0,lsl #2]
        bic r0,r1,#0xff000000
        add r0,r0,#{ADDRESS_BASE}
        bx lr
    table: .word {BASE+TABLE}
    """,HELPER)
    if len(body)!=stop-start:
        raise ValueError("Trade helper changed size")
    itcm.data[start:stop] = body
    for call in CALLS:
        main.data[call-BASE:call-BASE+4] = assemble(f"bl {HELPER}",call)
    installed = bytes(code.save())
    if cache_plan(arm)!=cache_plan(installed):
        raise ValueError("Trade category change affected the cache plan")
    for call in CALLS:
        main.data[call-BASE:call-BASE+4] = arm[call-BASE:call-BASE+4]
    itcm.data[start:stop] = bytes(stop-start)
    itcm.data[string_start:string_end] = b"%s\n  %s %d%%"
    pack_into("<I",main.data,offset,old_row)
    if bytes(code.save())!=arm:
        raise ValueError("Trade category change affected unowned ARM9 data")
    return installed,body
