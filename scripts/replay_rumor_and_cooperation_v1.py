"""Test the original trader cooperation path with one isolated deferred letter."""

import inspect
from pathlib import Path
import struct

from dk4tool.rom.nds import NdsImage
from scripts import run_diplomatic_outcome_live_v2 as previous
from scripts import stage_rumor_and_cooperation_v1 as stage
from scripts.checkpoint_sailing_alert_review_v1 import branch_target
from scripts.review_rumor_and_cooperation_v1 import ARM, BASE, CLEAN
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_personal_gameplay_v841 import get_machine


ACTION = {'mode': 'isolated-trader-cooperation'}
EVIDENCE, ROOT, ROM = stage.PROOF, stage.ROOT, stage.ROM
SLOT, TOWN, RIVAL = 4, 22, 9


def set_condition(arm, raw, request):
    assert request == ACTION and len(raw) == 0x400000
    assert arm == NdsImage.open(ROM).read_file(ARM)
    clean = NdsImage.open(CLEAN).read_file(ARM)
    for lo, hi in ((0x91464, 0x91480), (0x91598, 0x91658), (0x917B0, 0x918A8), (0x918A8, 0x91DB8)):
        assert arm[lo:hi] == clean[lo:hi]
    assert branch_target(clean, 0x9183C) == BASE + 0x918A8
    cpu, get = get_machine(arm, raw)
    assert get(0xB65E4) == TOWN
    captain = get(0x7F244)
    assert captain == 1
    faction = get(0x397D8, get(0xCB160))
    assert faction == 2
    town = get(0xCB178) + 4 + 108 * TOWN
    share = get(0xB4AA8, town, RIVAL)
    assert share == 99
    trader = get(0xB2CD8, town, 1)
    assert trader
    assert bytes(cpu.mem_read(BASE, len(raw))) == raw
    clock = get(0xCB1B4)
    tick = struct.unpack('<I', cpu.mem_read(clock + 8, 4))[0]
    slot = get(0xCB130) + 4 + 16 * SLOT
    at = slot - BASE
    before = raw[at:at + 16]
    assert before == bytes.fromhex('18c614020b0000000000000000000000')
    assert get(0x91464, slot) == 0
    after = before[:4] + bytes((9, faction, captain, RIVAL, TOWN, 0, 0, 0)) + struct.pack('<I', tick + 48)
    cpu.mem_write(slot, after)
    assert get(0x91464, slot) == 1
    changes = [dict(address=slot + i, before=a, after=b) for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b]
    return raw[:at] + after + raw[at + 16:], dict(mode=ACTION['mode'], original_type=9, slot=SLOT,
        sender_faction=faction, rival_faction=RIVAL, selected_town=TOWN, original_rival_share=share,
        original_trader=trader, chosen_agent_actor=captain, original_dispatcher=BASE + 0x917B0,
        original_cooperation_handler=BASE + 0x918A8, original_slot_hex=before.hex(), seeded_slot_hex=after.hex(),
        current_tick=tick, due_tick=tick + 48, only_letter_slot_bytes_changed=True, outcome_forced=False,
        changes=changes)


def main():
    source = checked_text(inspect.getsource(previous.main), {
        "effective = source.replace(token, 'from scripts.run_diplomatic_outcome_live_v2 import set_condition')":
            "effective = source.replace(token, 'from scripts.replay_rumor_and_cooperation_v1 import set_condition')",
        "folder = ROOT / ('truce_' + args.run_name)": "folder = ROOT / ('cooperation_' + args.run_name)",
    })
    env = vars(previous) | {'ROOT': ROOT, 'ROM': ROM, 'EVIDENCE': EVIDENCE, 'ACTION': ACTION, '__file__': __file__}
    exec(compile(source, __file__ + '::same-isolated-letter-and-original-inputs', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
