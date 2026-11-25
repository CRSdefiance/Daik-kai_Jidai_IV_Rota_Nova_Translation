"""Honor compiler-generated breaks in the original declaration-response portraits."""

from types import FunctionType

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch import mutiny_static_wrap_v1 as guarded
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.sea_event_static_wrap_v1 import BASE, HOOK


PRIOR = 0x01FFFEE8
PARENT, STACK_KEY, TABLE = 0x02053F40, 0x274, 0x021184E0
EXTENT = 0x01FFB860
ENTRY = 0x01FFBA34


def transform(source, exact_source_sha256):
    if sha(source) != exact_source_sha256:
        raise ValueError("Exact registered declaration wrap input required")
    code = MainCodeFile(source, BASE)
    assert bytes(code.save()) == source
    itcm = next(section for section in code.sections if section.ramAddress == 0x01FFC000)
    extension = next(section for section in code.sections if section.ramAddress == EXTENT)
    assert not extension.bssSize and extension.ramAddress + len(extension.data) == ENTRY
    scope = {(PARENT, STACK_KEY): (TABLE,)}
    assembly = FunctionType(guarded.assembly.__code__, vars(guarded) | {"SCOPE": scope, "PRIOR": PRIOR})()
    assembler = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    payload = bytes(assembler.asm(assembly, ENTRY)[0])
    end = ENTRY + len(payload)
    assert all(section is extension or end <= section.ramAddress
               or section.ramAddress + len(section.data) + section.bssSize <= ENTRY for section in code.sections)
    at = HOOK - itcm.ramAddress
    old_branch = bytes(assembler.asm(f"b {PRIOR:#x}", HOOK)[0])
    assert itcm.data[at:at + 4] == old_branch
    itcm.data[at:at + 4] = bytes(assembler.asm(f"b {ENTRY:#x}", HOOK)[0])
    extension.data.extend(payload)
    target = bytes(code.save())
    del extension.data[-len(payload):]
    itcm.data[at:at + 4] = old_branch
    assert bytes(code.save()) == source
    return target, dict(entry=ENTRY, end=end, prior=PRIOR, hook=HOOK, parent=PARENT,
                        stack_selector_offset=STACK_KEY, table=TABLE, complete_ARM9_inverse=True)
