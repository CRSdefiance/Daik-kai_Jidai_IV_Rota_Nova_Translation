"""Load the exact current item projection and both resident ITCM extensions."""

from ndspy.code import MainCodeFile

from scripts import current_item_detail_machine_v6102c as earlier
from scripts.source_locked_derivation_v5118 import checked_text


SOURCE = checked_text(earlier.SOURCE, {
    "        assert len(extra_sections)==1 and len(extra_sections[0].data)==4096\n"
    "        extra=extra_sections[0]\n"
    "        assert extra.ramAddress==CURRENT_EXTRA_ITCM_ADDRESS and bytes(extra.data)==CURRENT_EXTRA_ITCM_BYTES\n"
    "        machine.mem_write(extra.ramAddress,bytes(extra.data))\n"
    "        itcm_ranges.append((extra.ramAddress,extra.ramAddress+len(extra.data)))":
        "        assert len(extra_sections)==2 and len(extra_sections[0].data)==4096\n"
        "        assert [(s.ramAddress, bytes(s.data)) for s in extra_sections] == CURRENT_EXTRA_ITCM_SECTIONS\n"
        "        for extra in extra_sections:\n"
        "            machine.mem_write(extra.ramAddress,bytes(extra.data))\n"
        "            itcm_ranges.append((extra.ramAddress,extra.ramAddress+len(extra.data)))",
})


def make_execute(directory, arm):
    base = earlier.original.__globals__['BASE']
    sections = MainCodeFile(arm, base).sections
    assert len(sections) == 6 and arm[earlier.OFFSET + 3] == 0xEA
    cursor = base + earlier.OFFSET + 8 + int.from_bytes(arm[earlier.OFFSET:earlier.OFFSET + 3], 'little', signed=True) * 4
    cursor_bytes = earlier.buffered_helper(cursor)
    payload = bytes(sections[3].data[:-48])
    assert payload[cursor - earlier.POOL:cursor - earlier.POOL + len(cursor_bytes)] == cursor_bytes
    extra = [(s.ramAddress, bytes(s.data)) for s in sections[-2:]]
    assert len(extra[0][1]) == 4096 and extra[0][0] + 4096 == extra[1][0]
    env = earlier.original.__globals__ | dict(CURRENT_DIRECTORY_SHA256=directory, CURRENT_EXTRA_ITCM_SECTIONS=extra,
        CURRENT_CURSOR_ENTRY=cursor, CURRENT_CURSOR_BYTES=cursor_bytes)
    exec(compile(SOURCE, __file__ + '::exact-current-item-display', 'exec'), env)
    return env['execute']

