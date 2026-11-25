"""Use character boundaries when deleting from a marked captain name field."""

from struct import pack_into, unpack_from

from ndspy.code import MainCodeFile

from dk4tool.patch.captain_name_latin import EDIT_APPEND, EDIT_CONSTRUCTOR
from dk4tool.patch.main_pool_cache_visibility import BASE, cache_plan, target
from dk4tool.patch.sailing_no_target import Assembly
from scripts.probe_common_display_name_hook import branch_link


DELETE_CALL = 0xAFCD8
STOCK_DELETE = BASE + 0xB0A18
MOVE_CURSOR_END = BASE + 0xB0B54
MOVE_CURSOR = BASE + 0xB0B7C
REDRAW = BASE + 0xB0C70
CAPTAIN_PROVIDERS = 0x01FFB860
SECTION_LIMIT = 0x01FFC000


def deletion(entry):
    code = Assembly()

    def invoke(address, *, linked=True):
        at = entry + 4 * len(code.words)
        instruction = branch_link(at, address)
        code.emit(instruction if linked else instruction & ~0x01000000)

    code.emit(0xE510C034)  # ldr ip,[r0,#-0x34]  editor's keyboard provider
    code.load(1, "captain_provider", CAPTAIN_PROVIDERS)
    code.emit(0xE15C0001)  # cmp ip,r1
    code.branch("stock", 1)

    code.emit(0xE92D4010)  # push {r4,lr}
    code.emit(0xE1A04000)  # mov r4,r0  retain the native text widget
    code.emit(0xE59410A0)  # ldr r1,[r4,#0xa0]  byte capacity (excludes NUL)
    code.emit(0xE3510012)  # cmp r1,#18
    code.branch("restore_stock", 8)
    code.emit(0xE5940040)  # ldr r0,[r4,#0x40]  byte cursor
    code.emit(0xE3500000)  # cmp r0,#0
    code.emit(0x03A00001)  # moveq r0,#1  native Delete works forward at the first position
    code.emit(0xE1500001)  # cmp r0,r1
    code.branch("restore_stock", 8)
    code.emit(0xE284307C)  # add r3,r4,#0x7c  first input byte
    code.emit(0xE0830000)  # add r0,r3,r0  original cursor address
    code.emit(0xE0831001)  # add r1,r3,r1  last address for NUL

    code.mark("scan_character")
    code.emit(0xE5D32000)  # ldrb r2,[r3]
    code.emit(0xE3520000)  # cmp r2,#0
    code.branch("restore_stock", 0)
    code.emit(0xE3520081)  # cmp r2,#0x81
    code.branch("single_byte", 3)
    code.emit(0xE352009F)  # cmp r2,#0x9f
    code.branch("two_bytes", 9)
    code.emit(0xE35200E0)  # cmp r2,#0xe0
    code.branch("single_byte", 3)
    code.emit(0xE35200FC)  # cmp r2,#0xfc
    code.branch("two_bytes", 9)
    code.branch("restore_stock")

    code.mark("two_bytes")
    code.emit(0xE5D32001)  # ldrb r2,[r3,#1]
    code.emit(0xE3520040)  # cmp r2,#0x40
    code.branch("restore_stock", 3)
    code.emit(0xE352007F)  # cmp r2,#0x7f
    code.branch("restore_stock", 0)
    code.emit(0xE35200FC)  # cmp r2,#0xfc
    code.branch("restore_stock", 8)
    code.emit(0xE2833002)  # add r3,r3,#2
    code.emit(0xE1530000)  # cmp r3,r0
    code.branch("scan_character", 3)
    code.branch("restore_stock")  # native deletion already removes one two-byte character

    code.mark("single_byte")
    code.emit(0xE2833001)  # add r3,r3,#1
    code.emit(0xE1530000)  # cmp r3,r0
    code.branch("scan_character", 3)
    code.emit(0xE5D02000)  # ldrb r2,[r0]
    code.emit(0xE3520000)  # cmp r2,#0
    code.branch("end_character", 0)
    code.emit(0xE1A0C000)  # mov ip,r0

    code.mark("find_suffix_end")
    code.emit(0xE15C0001)  # cmp ip,r1  check NUL before writing anything
    code.branch("restore_stock", 8)
    code.emit(0xE4DC2001)  # ldrb r2,[ip],#1
    code.emit(0xE3520000)  # cmp r2,#0
    code.branch("find_suffix_end", 1)

    code.mark("move_suffix")
    code.emit(0xE5D02000)  # ldrb r2,[r0]
    code.emit(0xE5402001)  # strb r2,[r0,#-1]
    code.emit(0xE2800001)  # add r0,r0,#1
    code.emit(0xE3520000)  # cmp r2,#0
    code.branch("move_suffix", 1)
    code.emit(0xE0431004)  # sub r1,r3,r4
    code.emit(0xE241107D)  # sub r1,r1,#0x7d  previous cursor index
    code.emit(0xE1A00004)  # mov r0,r4
    invoke(MOVE_CURSOR)
    code.branch("refresh")

    code.mark("end_character")
    code.emit(0xE5402001)  # strb r2,[r0,#-1]
    code.emit(0xE1A00004)  # mov r0,r4
    invoke(MOVE_CURSOR_END)

    code.mark("refresh")
    code.emit(0xE1A00004)  # mov r0,r4
    invoke(REDRAW)
    code.emit(0xE3A00001)  # mov r0,#1  original nonempty deletion result
    code.emit(0xE8BD8010)  # pop {r4,pc}

    code.mark("restore_stock")
    code.emit(0xE1A00004)  # mov r0,r4
    code.emit(0xE8BD4010)  # pop {r4,lr}
    code.mark("stock")
    invoke(STOCK_DELETE, linked=False)
    return code.finish()


def stage(arm, clean, owner):
    """Bind the existing name hook and extend its dedicated autoload within its free tail."""
    original = MainCodeFile(arm, BASE)
    assert bytes(original.save()) == arm
    assert clean[DELETE_CALL-4:DELETE_CALL+8] == arm[DELETE_CALL-4:DELETE_CALL+8]
    assert clean[0xB0A18:0xB0B2C] == arm[0xB0A18:0xB0B2C]
    assert unpack_from("<I", arm, DELETE_CALL)[0] == branch_link(BASE + DELETE_CALL, STOCK_DELETE)
    assert original.sections[-1].ramAddress == owner["provider"] == CAPTAIN_PROVIDERS
    inherited = bytes(original.sections[-1].data)
    historical = bytes.fromhex(owner["registered_provider_and_helpers_hex"])
    assert inherited.startswith(historical)
    assert all(target(arm, hook) == owner["hooks"][str(hook)] for hook in (EDIT_APPEND, EDIT_CONSTRUCTOR))
    start = CAPTAIN_PROVIDERS + len(inherited)
    payload = deletion(start)
    assert original.sections[-1].bssSize == 0 and start % 4 == 0
    assert start + len(payload) <= SECTION_LIMIT
    assert all(s.ramAddress + len(s.data) + s.bssSize <= CAPTAIN_PROVIDERS
               or s.ramAddress >= SECTION_LIMIT for s in original.sections[:-1])
    original_plan = cache_plan(arm)
    section = original.sections[-1]
    section.data = bytearray(inherited + payload)
    pack_into("<I", original.sections[0].data, DELETE_CALL, branch_link(BASE+DELETE_CALL,start))
    result = bytes(original.save())
    packed = MainCodeFile(result, BASE)
    assert bytes(packed.save()) == result
    assert cache_plan(result) == original_plan
    assert bytes(packed.sections[-1].data) == inherited + payload
    packed.sections[-1].data = bytearray(inherited)
    packed.sections[0].data[DELETE_CALL:DELETE_CALL+4] = arm[DELETE_CALL:DELETE_CALL+4]
    assert bytes(packed.save()) == arm
    return result, dict(call_site=BASE+DELETE_CALL, original_delete=STOCK_DELETE, entry=start,
        size=len(payload), helper_hex=payload.hex(), inherited_autoload_size=len(inherited),
        inherited_autoload_base=CAPTAIN_PROVIDERS, interval_end_exclusive=start+len(payload),
        exact_ARM9_inverse=True, original_code_other_callers_and_cache_plan_preserved=True)

