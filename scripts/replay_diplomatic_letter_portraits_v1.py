"""Replay an outgoing submission demand using the game's original deferred letter."""

import inspect
from pathlib import Path
import struct

from dk4tool.rom.nds import NdsImage
from scripts import run_diplomatic_outcome_live_v2 as prior
from scripts import run_diplomatic_outcome_startup_v2 as startup
from scripts import stage_diplomatic_letter_portraits_v1 as stage
from scripts import stage_rumor_and_cooperation_v1 as predecessor
from scripts.checkpoint_sailing_alert_review_v1 import branch_target
from scripts.seal_shared_text_source_v1 import ARM, CLEAN
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_personal_gameplay_v841 import get_machine


ACTION = {'mode': 'isolated-outgoing-submission'}
EVIDENCE, ROOT, ROM = stage.PROOF, stage.ROOT, stage.ROM
BASE, SLOT, TARGET = prior.BASE, 4, 5
STARTUP, PRIOR = ROOT / 'own_startup', predecessor.ROOT / 'own_startup'


def set_condition(arm, raw, request):
    assert request == ACTION and len(raw) == 0x400000
    assert arm == NdsImage.open(ROM).read_file(ARM)
    clean = NdsImage.open(CLEAN).read_file(ARM)
    for lo, hi in ((0x91464, 0x91480), (0x91598, 0x91658), (0x917B0, 0x918A8), (0x927F0, 0x92B78)):
        assert arm[lo:hi] == clean[lo:hi]
    assert branch_target(clean, 0x9181C) == BASE + 0x927F0
    cpu, get = get_machine(arm, raw)
    assert get(0xB65E4) == 22 and get(0x7F244) == 1
    company_root = get(0xCB160)
    own = get(0x397D8, company_root)
    assert own == 2
    target = company_root + 4 + TARGET * 76
    assert get(0x3CBF4, target) != own
    leader = get(0x3CD2C, target)
    assert leader
    key = get(0x53F4C, leader, 0x021187E0)
    assert key in range(2757, 2761)
    clock = get(0xCB1B4)
    tick = struct.unpack('<I', cpu.mem_read(clock + 8, 4))[0]
    slot = get(0xCB130) + 4 + 16 * SLOT
    at = slot - BASE
    before = raw[at:at + 16]
    assert before == bytes.fromhex('18c614020b0000000000000000000000')
    assert get(0x91464, slot) == 0
    after = before[:4] + bytes((5, own, 1, TARGET)) + before[8:12] + struct.pack('<I', tick + 48)
    cpu.mem_write(slot, after)
    assert get(0x91464, slot) == 1
    changes = [dict(address=slot + i, before=a, after=b) for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b]
    return raw[:at] + after + raw[at + 16:], dict(mode=ACTION['mode'], original_type=5,
        slot=SLOT, sender_faction=own, recipient_faction=TARGET, chosen_agent_actor=1,
        recipient_actor_ID=get(0x7EE08, leader), expected_native_demand_ID=key,
        original_dispatcher=BASE + 0x917B0, original_submission_handler=BASE + 0x927F0,
        original_slot_hex=before.hex(), seeded_slot_hex=after.hex(), current_tick=tick, due_tick=tick + 48,
        only_letter_slot_bytes_changed=True, outcome_forced=False, changes=changes)


def main():
    source = checked_text(inspect.getsource(prior.main), {
        "effective = source.replace(token, 'from scripts.run_diplomatic_outcome_live_v2 import set_condition')":
            "effective = source.replace(token, 'from scripts.replay_diplomatic_letter_portraits_v1 import set_condition')",
        "folder = ROOT / ('truce_' + args.run_name)": "folder = ROOT / ('submission_' + args.run_name)",
    })
    env = vars(prior) | globals()
    exec(compile(source, __file__ + '::same-deferred-letter-harness', 'exec'), env)
    env['main']()


def cold_boot():
    from types import FunctionType
    FunctionType(startup.main.__code__, vars(startup) | globals())()


if __name__ == '__main__':
    import sys
    if sys.argv[1:] == ['--cold-boot']:
        cold_boot()
    else:
        main()

