"""Observe the first expansion and second prepared body through the original story callers."""

from pathlib import Path
from struct import unpack

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP

from scripts import register_captain_name_delete_20261122 as current
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.verify_personal_gameplay_v841 import get_machine


base, native = current.base, current.native
FIRST = {18: (0x02054020, 0x02054160), 254: (0x0205473C, 0x02054798), 255: (0x02053AC4, 0x02053AF0)}
STORY = 0x0202425C
INPUT = 0x02660000
FINDING = current.VERIFY / "first_mate_surname_expansion_finding.json"


def observe(arm, raw, text, selector, *, direct=False):
    cpu, get = get_machine(arm, raw)
    actor_root = get(0xCB184)
    actor_model = bytes(cpu.mem_read(actor_root, 0x1A04))
    actor = actor_root + 4 + 32 * 18
    cpu.mem_write(INPUT - 16, b"\xA5" * 1056)
    cpu.mem_write(INPUT, text + b"\0")
    first, second = FIRST[selector]
    if direct:
        assert selector == 18
    trace = {}
    last = second + 4

    def c_string(u, p):
        buf = bytes(u.mem_read(p, 1024))
        return buf[:buf.index(0)]

    def visit(u, pc, _size, _):
        if pc == 0x020940B0:
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
        elif pc == 0x0205408C:
            u.reg_write(UC_ARM_REG_PC, 0x02054144)
        elif pc == first:
            p = u.reg_read(UC_ARM_REG_R1 if selector == 18 else UC_ARM_REG_R0)
            trace["first"] = c_string(u, p)
            trace["caller"] = u.reg_read(UC_ARM_REG_LR)
        elif pc == second:
            sp = u.reg_read(UC_ARM_REG_SP)
            off, words = {18: (0x264, 3), 254: (0xC4, 3), 255: (0x14, 1)}[selector]
            trace["saved_frames"] = list(unpack(f"<{words}I",u.mem_read(sp+off,words*4)))
            trace["destination"] = u.reg_read(UC_ARM_REG_R0)
            trace["formatter_input"] = c_string(u, u.reg_read(UC_ARM_REG_R1))
        elif pc == last:
            trace["output"] = c_string(u, trace["destination"])
            u.emu_stop()

    for address in {0x020940B0, 0x0205408C, first, second, last}:
        cpu.hook_add(UC_HOOK_CODE, visit, begin=address, end=address)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    cpu.reg_write(UC_ARM_REG_R0, actor if direct else selector)
    cpu.reg_write(UC_ARM_REG_R1, INPUT)
    cpu.emu_start(first if direct else STORY, STOP, count=700000)
    assert cpu.reg_read(UC_ARM_REG_PC) == last and bytes(cpu.mem_read(actor_root,0x1A04))==actor_model
    assert bytes(cpu.mem_read(INPUT-16,16)) == b"\xA5"*16
    assert bytes(cpu.mem_read(INPUT,len(text)+17)) == text + b"\0" + b"\xA5"*16
    return trace


def read_finding():
    note = base.load(FINDING)
    shot = note["first_page"]["read_only_RAM"]
    assert base.digest(shot["path"]) == shot["sha256"]
    return note, Path(shot["path"]).read_bytes()


if __name__ == "__main__":
    note, raw = read_finding()
    body = bytes.fromhex(note["exact_record"]["current_ref"]["exact_stored_hex"])[1:]
    arm = base.NdsImage.open(current.ROM).read_file(native.ARM)
    for selector, text, direct in ((18,body,False),(254,b"Hello FA!",False),(255,b"Hello FA!",False),(18,b"Hello FA!",True)):
        case = observe(arm,raw,text,selector,direct=direct)
        print(selector,direct,{key: [hex(n) for n in v] if isinstance(v,list) else hex(v) if isinstance(v,int) else v for key,v in case.items()})

