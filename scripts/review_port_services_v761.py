"""Clean-source review of Port/companion/Tavern services; no completion credit."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shipyard_continuation_v761')
CURRENT = Path('out/all_routes_combined_v760_candidate.nds')
MANUSCRIPT = Path('translations/port_services_editorial_manuscript_v1.json')
RAM_REPORT = Path('E:/Rota Nova translations/Generated/work/emulation_v193/shipyard_v760_copy_funded_FALCON_760/capture_report.json')
IDS = (267, *range(805, 820), 1245, 1246)
TEXT = {
    267: "You can't sell any more ships!",
    805: "You're the admiral! You have to captain a ship!",
    806: 'Any excess food will be thrown away. Is that okay?',
    807: "You really can't manage without me beside you!",
    808: "I'm worried about you, %s... Can I stay with you?",
    809: "No. I will remain the Admiral's aide.",
    810: "I... don't want... to leave...",
    811: "I'm your guardian. I can't leave this ship.",
    812: 'Any excess water will be dumped. Is that okay?',
    813: "You're running low on water. Need to stock up?",
    814: 'Your sailors look tired. Why not let them rest at the inn?',
    815: 'You have no cargo.',
    816: "You don't have enough for a full resupply. Want to buy what you can?",
    817: 'Do you want to change the ratio of water to food?',
    818: "I'm sorry, but we're quite clear about our prices...",
    819: "Drinks aren't free.",
    1245: "You'll need %s gold, but you don't have enough.",
    1246: "It'll cost %s gold. Is that okay?",
}
GLOSS = {
    267: 'No more ships can be disposed of. The sole original ARM caller is the Sell path when its eligible ship list is empty.',
    805: 'Rhetorical objection: what is the admiral doing if they are not serving as a captain?',
    806: 'Excess food will have to be discarded; asks for confirmation.',
    807: 'Insists the player cannot manage without the speaker beside them.',
    808: 'The speaker is worried about the named admiral and asks to remain together.',
    809: 'Politely declines and insists on continuing to assist the admiral.',
    810: 'Halting, reluctant objection to being separated or leaving.',
    811: 'As the player\'s guardian, the speaker cannot leave this ship.',
    812: 'Excess water will have to be discarded; asks for confirmation.',
    813: 'Water seems low; asks whether to resupply.',
    814: 'The sailors look tired; suggests resting at the inn.',
    815: 'The player has no cargo.',
    816: 'Not enough money for a full resupply; asks whether to buy only what is affordable.',
    817: 'Asks whether to change the water/food resupply proportions.',
    818: 'Polite incomplete refusal, invoking the establishment\'s policy of clear and honest billing.',
    819: 'There is no free liquor to serve.',
    1245: 'The required gold-coin amount exceeds available money.',
    1246: 'States the gold-coin price and asks for confirmation.',
}
NOTES = {
    267: 'Sell is bound by the observed original caller; scrap described the wrong operation. No last-ship rule is invented: the original list can include docked ships and excludes the admiral\'s ship.',
    805: 'Restore the rhetorical objection and actual requirement. The old question asking whether the admiral will captain reverses the scene\'s purpose.',
    806: 'Restore explicit future disposal and a conversational confirmation. No manual line breaks.',
    807: 'Retain the existing natural insistence, with fresh generated formatting rather than old breaks/padding.',
    808: 'The original virtual name getter supplies the current admiral\'s short name. Direct you makes the address natural; do not use an unverified third-person gender. Runtime name preservation still requires a scoped literal adapter.',
    809: 'Retain the established formal register. Its lower informality suits Gerhard\'s polite source; do not force a contraction or add a family relationship.',
    810: 'Remove the unrelated trade fragment. Three natural hesitations convey Sera\'s broken, reluctant speech without splitting English words or authoring line breaks.',
    811: 'Remove the remaining trade fragment. Guardian is explicit source content for Xien, not an invented father/grandfather relationship.',
    812: 'Dumped is natural nautical language for discarding water. Keep confirmation distinct from the food message.',
    813: 'Restore the observation and personal question instead of a telegraphic menu fragment.',
    814: 'Use a natural suggestion and preserve the inn, the sailors and apparent fatigue; do not turn it into a mandatory rest command.',
    815: 'Retain the complete natural statement; the familiar source address needs no extra English vocative.',
    816: 'Restore the full-resupply shortfall and offer to buy an affordable quantity without inventing a precise fraction or guaranteeing full replenishment.',
    817: 'Name both water and food; the old supply ratio omitted what the proportions refer to.',
    818: 'Remove the trade placeholder. Clear about our prices conveys meiro kaikei in idiomatic service language. Preserve the polite trailing refusal without inventing posted signs, cheap prices, customer gender or a charity line.',
    819: 'Retain the concise natural refusal; the source roughness does not require extra profanity.',
    1245: 'Restore the complete funds shortfall. Gold is a natural mass currency noun, faithful to the gold coins, and works with the original unchanged numeric argument for both1 and plural amounts.',
    1246: 'Restore a complete natural price confirmation. Gold keeps singular/plural grammar correct without changing the original numeric callers or silently adding source arguments.',
}
# Exact original ID load/call pairs; nonliteral companion dispatch is tested below.
BINDINGS = {
    267: (0x62570, 0x62574, 0x546B8), 805: (0x5AA34, 0x5AA38, 0x53FE4),
    806: (0x60808, 0x60810, 0x53F9C), 807: (0x5AEE8, 0x5AEF8, 0x53FE4),
    808: (0x5AFAC, 0x5AFB0, 0x53FE4), 809: (0x5AF1C, 0x5AF2C, 0x53FE4),
    810: (0x5AF50, 0x5AF60, 0x53FE4), 811: (0x5AFD4, 0x5AFE4, 0x53FE4),
    812: (0x60834, 0x60838, 0x53F9C), 813: (0x607E8, 0x607F0, 0x53F9C),
    814: (0x60BC4, 0x60BCC, 0x53FE4), 815: (0x603EC, 0x603F0, 0x53FE4),
    816: (0x60888, 0x6088C, 0x53F9C), 817: (0x604E4, 0x604E8, 0x53F9C),
    818: (0x584A0, 0x584A8, 0x53FE4), 819: (0x5850C, 0x58514, 0x53FE4),
    1245: (0x63104, 0x6310C, 0x53FE4), 1246: (0x17EFC, 0x17F04, 0x53F9C),
}


def context(arm, clean_arm):
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM); cs.detail = True
    bindings = []
    for n, (load, end, consumer) in BINDINGS.items():
        span = arm[load:end + 4]
        assert span == clean_arm[load:end + 4]
        ins = list(cs.disasm(span, BASE + load)); first, last = ins[0], ins[-1]
        if first.mnemonic == 'ldr':
            lit = first.address + 8 + first.operands[1].mem.disp - BASE
            assert struct.unpack_from('<I', arm, lit)[0] == n
            assert arm[lit:lit + 4] == clean_arm[lit:lit + 4]
        else:
            assert first.mnemonic == 'mov' and first.operands[1].imm == n
        assert last.mnemonic == 'bl' and last.operands[0].imm == BASE + consumer
        bindings.append({'id': n, 'load': BASE + load, 'call': BASE + end, 'consumer': BASE + consumer,
            'original_parent': BASE + (0x54014 if consumer == 0x53FE4 else 0x53FCC if consumer == 0x53F9C else 0x546E8)})
    assert clean_arm[0x5AE6C:0x5B0A4] == arm[0x5AE6C:0x5B0A4]
    assert clean_arm[0x17E90:0x17F98] == arm[0x17E90:0x17F98]
    u = machine(arm); raw = snapshot(read(RAM_REPORT), 3200); u.mem_write(BASE, raw)
    def get(fn, args=()):
        call(u, fn, args); return u.reg_read(UC_ARM_REG_R0)
    root = get(0xCB184)
    flag = struct.unpack_from('<I', arm, 0x5B0A0)[0] + 0x48
    observed = []
    events = []
    def stop(cpu, pc, size, unused):
        if pc in (BASE + 0x53FE4, BASE + 0x546B8, BASE + 0x5466C):
            n = cpu.reg_read(UC_ARM_REG_R1 if pc == BASE + 0x53FE4 else UC_ARM_REG_R0)
            arg = cpu.reg_read(UC_ARM_REG_R2)
            data = bytes(cpu.mem_read(arg, 64)).split(b'\0')[0] if n == 808 else None
            events.append({'consumer': pc, 'message_id': n, 'portrait_actor': cpu.reg_read(UC_ARM_REG_R0),
                'name_argument_hex': data.hex() if data else None})
            cpu.reg_write(UC_ARM_REG_R0, 0); cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))
    hook = u.hook_add(UC_HOOK_CODE, stop)
    try:
        for route_flag in (0, 1):
            u.mem_write(flag, struct.pack('<I', route_flag))
            admiral = get(0x7F244)
            for actor in range(208):
                events.clear(); call(u, 0x5AE6C, (actor,)); result = u.reg_read(UC_ARM_REG_R0)
                expected = {5: 807, 9: 808, 10: 811, 24: 810}.get(actor)
                if actor == 16 and route_flag == 1: expected = 809
                if actor == admiral: expected = 272
                expected_events = [272, 273] if expected == 272 else [] if expected is None else [expected]
                assert [e['message_id'] for e in events] == expected_events, (actor, route_flag, events)
                assert result == (1 if expected is None else 0)
                if expected not in (None, 272):
                    assert events[0]['portrait_actor'] == root + 4 + actor * 32
                observed.append({'actor_ID': actor, 'supplied_route_flag': route_flag, 'return': result, 'events': list(events)})
    finally:
        u.hook_del(hook)
    actors = []
    for actor in (5, 9, 10, 16, 24):
        ptr = root + 4 + actor * 32; vt = struct.unpack('<I', u.mem_read(ptr, 4))[0]
        p = get(struct.unpack('<I', u.mem_read(vt + 0x20, 4))[0] - BASE, (ptr,))
        actors.append({'actor_ID': actor, 'actual_current_name': bytes(u.mem_read(p, 64)).split(b'\0')[0].decode('cp932')})
    assert actors == [{'actor_ID': a, 'actual_current_name': b} for a, b in ((5, 'Claudio'), (9, 'Camille'), (10, 'Xien'), (16, 'Gerhard'), (24, 'Sera'))]
    names = {e['name_argument_hex'] for row in observed for e in row['events'] if e['message_id'] == 808}
    assert names == {b'Hodram'.hex()}
    # Both global script-cost and Shipyard insufficiency use the same numeric
    # message. No source argument is a place or item name.
    assert clean_arm[0x630EC:0x63114] == arm[0x630EC:0x63114]
    return {'original_call_bindings': bindings, 'all416_original_companion_actor_flag_cases': observed,
        'actual_current_actor_getters': actors, '808_actual_admiral_short_name': 'Hodram',
        'original_selector_and_dispatch_spans_clean_current_exact': True,
        'original_generic_charge_and_Yard_price_fragments_clean_current_exact': True,
        'initialized_current_RAM_prerequisites': str(RAM_REPORT), 'RAM_sha256': sha(raw),
        'UI_consumers_intercepted_at_boundary_no_whole_scene_or_earned_activation_claim': True}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    roms = [NdsImage.open(p) for p in ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds', CURRENT)]
    source, canonical, current = [common_message_entries(r.read_file('/COMMON/MESFILE.DK4'), r.read_file('/__arm9__.bin'), clean=(i == 0)) for i, r in enumerate(roms)]
    proof = context(roms[2].read_file('/__arm9__.bin'), roms[0].read_file('/__arm9__.bin'))
    save(ROOT / 'native_context.json', {**proof, 'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    records = []
    for n in IDS:
        binding = next(r for r in proof['original_call_bindings'] if r['id'] == n)
        speaker = ({807: 'Claudio', 808: 'Camille', 809: 'Gerhard', 810: 'Sera', 811: 'Xien'}.get(n)
            or ('System, original Sell refusal' if n == 267 else 'Original contextual service NPC'))
        records.append({'id': f'COMMON_MESSAGE_{n}', 'message_id': n, 'source_hex': source[n].text.hex(),
            'japanese': source[n].text.decode('cp932'), 'canonical_source_hex': canonical[n].text.hex(),
            'current_text_hex': current[n].text.hex(), 'current_English': current[n].text.decode('cp932'),
            'source_reference': {'block': source[n].block, 'record': source[n].record_index, 'offset': source[n].block_offset},
            'current_reference': {'block': current[n].block, 'record': current[n].record_index, 'offset': current[n].block_offset},
            'english': TEXT[n] + '{PAD}', 'source_meaning': GLOSS[n], 'localization_note': NOTES[n], 'speaker': speaker,
            'context': ('Original companion reassignment veto; original actor selector and portrait object proven for every208 actors under both route-flag cases.808 receives the current admiral short name.' if 807 <= n <= 811 else
                'Original Sell branch when the native sellable-list builder returns zero; separate system-modal consumer.' if n == 267 else
                'Original generic script charge or Yard insufficient-funds price.1245 is a refusal;1246 Yes/No confirmation can debit the quoted value only on acceptance.' if n >= 1245 else
                'Original Port captain/resupply/rest/cargo service or Tavern payment-refusal branch, bound to the exact source ID load and consumer. Preceding/following messages are archived independently, not joined by table adjacency.'),
            'native_binding': binding, 'decision': 'retain-wording' if n in (807, 809, 815, 819) else 'revise',
            'review': {'source': True, 'context': True, 'localization': True, 'naturalness': True, 'formatting': False},
            'status': 'source-context-prose-reviewed-native-layout-and-integration-pending'})
    save(MANUSCRIPT, {'format': 'dk4-common-entry-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
        'encoder': 'dialogue-fixed-v1', 'target_locale': 'en-US', 'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'file_path': '/COMMON/MESFILE.DK4', 'source_clean_COMMON_sha256': sha(roms[0].read_file('/COMMON/MESFILE.DK4')),
        'source_canonical_COMMON_sha256': sha(roms[1].read_file('/COMMON/MESFILE.DK4')),
        'source_ROM_sha256': sha(roms[0].source.read_bytes()), 'current_ROM_sha256': sha(CURRENT.read_bytes()),
        'context_evidence': str(ROOT / 'native_context.json'), 'records': records,
        'status': 'source-prose-research-not-integrated-not-completed'})
    print('18 clean-source prose reviews;416 original companion selector/portrait cases pass. Formatting/integration/gameplay remain open.', flush=True)


if __name__ == '__main__':
    main()
