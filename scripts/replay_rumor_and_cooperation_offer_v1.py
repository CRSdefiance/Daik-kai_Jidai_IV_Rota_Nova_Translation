"""Check the paid trader offer using one declared experience word and the original decision."""

import inspect
from pathlib import Path
import struct

from dk4tool.rom.nds import NdsImage
from scripts import replay_rumor_and_cooperation_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_personal_gameplay_v841 import get_machine


ROOT = Path('out/rumor_and_cooperation_offer_replay_20261111_v1')
ACTION = {'mode': 'isolated-trader-offer'}
TOWN, RIVAL, XP = 0, 4, 300000


def set_condition(arm, raw, request):
    assert request == ACTION
    after, proof = previous.set_condition(arm, raw, previous.ACTION)
    clean = NdsImage.open(previous.CLEAN).read_file(previous.ARM)
    assert arm[0x7E670:0x7E678] == clean[0x7E670:0x7E678]
    assert arm[0x7DCC8:0x7DE20] == clean[0x7DCC8:0x7DE20]
    cpu, get = get_machine(arm, raw)
    town = get(0xCB178) + 4 + 108 * TOWN
    assert get(0xB4AA8, town, RIVAL) == 100
    actor = get(0xCB184) + 0x19E4
    assert get(0x7F244) == 1 and get(0x7E670, actor) == struct.unpack_from('<I', raw, actor + 16 - previous.BASE)[0]
    xp_at = actor + 16 - previous.BASE
    before = get(0x7DCC8, actor, 8)
    slot = get(0xCB130) + 4 + 16 * previous.SLOT - previous.BASE
    target = bytearray(after)
    struct.pack_into('<I', target, xp_at, XP)
    target[slot + 7:slot + 9] = bytes((RIVAL, TOWN))
    cpu.mem_write(previous.BASE, bytes(target))
    assert get(0x7E670, actor) == XP
    speech = get(0x7DCC8, actor, 8)
    assert speech > before
    owned = set(range(slot, slot + 16)) | set(range(xp_at, xp_at + 4))
    changes = [dict(address=previous.BASE + at, before=a, after=b)
               for at, (a, b) in enumerate(zip(raw, target, strict=True)) if a != b]
    assert {row['address'] - previous.BASE for row in changes} <= owned
    return bytes(target), proof | dict(mode=ACTION['mode'], rival_faction=RIVAL, selected_town=TOWN,
        original_rival_share=100, original_trader=get(0xB2CD8, town, 1), only_letter_slot_bytes_changed=False,
        seeded_slot_hex=target[slot:slot + 16].hex(), original_speech=before, initialized_speech=speech,
        experience_word_address=actor + 16, initialized_experience=XP,
        changes=changes, outcome_forced=False)


def main():
    source = checked_text(inspect.getsource(previous.previous.main), {
        "effective = source.replace(token, 'from scripts.run_diplomatic_outcome_live_v2 import set_condition')":
            "effective = source.replace(token, 'from scripts.replay_rumor_and_cooperation_offer_v1 import set_condition')",
        "folder = ROOT / ('truce_' + args.run_name)": "folder = ROOT / ('cooperation_' + args.run_name)",
    })
    env = vars(previous.previous) | {'ROOT': ROOT, 'ROM': previous.ROM, 'EVIDENCE': previous.EVIDENCE,
                                     'ACTION': ACTION, '__file__': __file__}
    ROOT.mkdir(exist_ok=True)
    exec(compile(source, __file__ + '::same-deferred-letter-harness', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
