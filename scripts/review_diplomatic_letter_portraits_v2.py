"""Bind the pact-break reactions to the captain surname getter."""

import inspect
import struct
from pathlib import Path

from scripts import review_diplomatic_letter_portraits_v1 as draft
from scripts.source_locked_derivation_v5118 import checked_text


OUTPUT = draft.OUTPUT.with_name('diplomatic_letter_portraits_context_v2.json')


def surnames(runtime):
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)

    def word(at):
        return struct.unpack('<I', cpu.mem_read(at, 4))[0]

    actor_root = get(0xCB184)
    actor_offset = word(draft.prior.BASE + 0x93408)
    assert actor_offset == 0x19E4
    names = {}
    for n in range(4):
        actor = actor_root + (actor_offset if n == 3 else 4 + 32 * n)
        getter = word(word(actor) + 0x24)
        value = get(getter - draft.prior.BASE, actor)
        names[n] = bytes(cpu.mem_read(value, 64)).split(b'\0', 1)[0].decode('cp932')
    assert names == {0: 'Castor', 1: 'Bergstrom', 2: 'Argot', 3: 'Li'}
    runtime.calls.clear()
    return names


def main():
    source = checked_text(inspect.getsource(draft.main), {
        'previously_credited_neighbors=results,': 'previously_credited_neighbors=results, native_pact_break_surnames=surnames(runtime),',
        '(RELEASE, Path(__file__))': '(RELEASE, draft.OUTPUT, Path(draft.__file__), Path(__file__))',
    })
    groups = tuple(
        (table, literal, calls, slots, ('sending captain surname',),
         'After the receipt notice, the other leader reacts to the player breaking their existing pact. '
         'The native caller uses the player captain’s surname.')
        if table == 0x117A40 else (table, literal, calls, slots, args, context)
        for table, literal, calls, slots, args, context in draft.GROUPS
    )
    env = vars(draft) | globals() | {'GROUPS': groups}
    # The inherited voice-table resolver takes GROUPS from the function globals.
    exec(compile(source, __file__ + '::whole-exchange-reference-and-surname-binding', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()

