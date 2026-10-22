"""Clean-source Market stock/letter packet and original decision fragments.

Research only: this script does not build or register a playable ROM. Formatter,
integration and actual gameplay gates remain pending for the new English.
"""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import BASE, STACK, machine
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/market_stock_v755')
MANUSCRIPT = Path('translations/market_stock_manuscript_v1.json')
CURRENT = Path('out/all_routes_combined_v754_candidate.nds')
IDS = tuple(range(767, 784))
TEXT = {
    767: "%s and %s! They're flying off the shelves, so we're often out of stock.",
    768: "You're selling us %s? Thanks! Demand's so high, we often run out.",
    769: "All right, I'll sweeten the deal. You're selling us %s and %s, and they're flying off the shelves!",
    770: "Hmm... I'll sweeten the deal, then. You're selling us %s, and demand's booming!",
    771: "I wish this war would end soon. It's making business difficult.",
    772: "With the economy picking up lately, business has been easier.",
    773: "The economy's been so bad lately, doing business is a real struggle.",
    774: "Oh, I know! I'll write you a letter of introduction to thank you for selling us those popular goods.",
    775: "And I'll write you a letter of recommendation to thank you for selling us so many popular goods.",
    776: "Oh, I know! I'll write you a letter of introduction to thank you for selling us so many popular goods.",
    777: "Oh, you have a letter of introduction? Let me add a few words. That'll make it a letter of recommendation.",
    778: "Oh, I know! I'll write you a letter of recommendation to thank you for selling us so many popular goods.",
    779: "Take it to a palace or governor's office in a small town. They should grant you some market share.",
    780: "Take it to a palace or governor's office in any town. They should grant you some market share.",
    781: "A letter of introduction only works in small towns. A letter of recommendation will do in any town.",
    782: "Hmm... All right! Since you're selling us those popular goods, I'll throw in a little extra.",
    783: "Oh, you're selling us those popular goods? Thanks! Keep them coming!",
}
GLOSS = {
    767: 'Recognizes two supplied products; they sell extremely quickly, so the merchant often runs out.',
    768: 'Gratefully acknowledges the player selling the supplied product; fast sales cause frequent stockouts, so the delivery helps.',
    769: 'Agrees enthusiastically to provide favorable treatment because the player is selling two products that are currently selling extremely quickly.',
    770: 'After a hesitation agrees to provide favorable treatment because the supplied product is currently selling extremely quickly.',
    771: 'Wishes the war would end soon because it makes doing business difficult.',
    772: 'The economy has improved recently, making it easier to do business.',
    773: 'The economy has worsened recently, making doing business extremely difficult.',
    774: 'Has an idea: write a letter of introduction in thanks for selling popular goods.',
    775: 'As an additional offer, write a letter of recommendation in thanks for selling such a large quantity of popular goods.',
    776: 'Has an idea: write a letter of introduction in thanks for selling such a large quantity of popular goods.',
    777: 'Notices the player already has a letter of introduction; adding a few words upgrades it to a letter of recommendation.',
    778: 'Has an idea: write a letter of recommendation in thanks for selling such a large quantity of popular goods.',
    779: 'Taking the letter to a palace or governor office in a small town should secure preferential market share.',
    780: 'Taking the letter to a palace or governor office in any town should secure preferential market share.',
    781: 'A letter of introduction only works in small towns; a letter of recommendation works in any town.',
    782: 'After deliberation agrees to add an extra favor because the player is selling popular goods.',
    783: 'Gratefully acknowledges the player selling popular goods and asks for continued business.',
}
SPANS = ((0xBA334, 0xBA390), (0xBB894, 0xBBC08),
         (0xBBC8C, 0xBC0DC), (0xBC260, 0xBC2A8))


def fragments(arm):
    """Execute original selection/argument code with explicitly supplied states.

    The product root/virtual-name getter are tagged stubs, not runtime product
    evidence. Support call1096F8 is observed and skipped. No stock, earned letter,
    full transaction, economic-state getter or persistence claim is made.
    """
    cases = []
    products, vtable, getter = 0x02450000, 0x02451000, 0x02452000
    for kind, starts in (
        ('two_products', (0xBBB10, 0xBBCCC, 0xBBDFC, 0xBBF54)),
        ('one_product', (0xBBBB4, 0xBBD4C, 0xBBE7C, 0xBBFD4)),
    ):
        for start in starts:
            for discount in (0, 1):
                for side in ((0,) if kind == 'two_products' else (0, 1)):
                    cpu = machine(arm)
                    cpu.mem_write(products + 4, struct.pack('<I', vtable))
                    cpu.mem_write(products + 20, struct.pack('<I', vtable))
                    cpu.mem_write(vtable + 8, struct.pack('<I', getter))
                    cpu.mem_write(STACK + 0x10, struct.pack('<I', discount))
                    cpu.mem_write(STACK + 0x28, struct.pack('<I', side))
                    cpu.reg_write(UC_ARM_REG_SP, STACK)
                    cpu.reg_write(UC_ARM_REG_R6, side)
                    cpu.reg_write(UC_ARM_REG_R7, 0 if not side else 125)
                    cpu.reg_write(UC_ARM_REG_R8, 1)
                    calls = []

                    def observe(u, address, size, unused, calls=calls):
                        if address == BASE + 0xCB124:
                            u.reg_write(UC_ARM_REG_R0, products)
                            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
                        elif address == getter:
                            index = (u.reg_read(UC_ARM_REG_R0) - products - 4) // 16
                            assert index in (0, 1)
                            u.reg_write(UC_ARM_REG_R0, 0x02460000 + index * 64)
                            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
                        elif address == BASE + 0x53FE4:
                            calls.append(tuple(u.reg_read(r) for r in (UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)))
                            u.emu_stop()

                    hook = cpu.hook_add(UC_HOOK_CODE, observe)
                    try:
                        cpu.emu_start(BASE + start, 0x027E0000, count=200)
                    finally:
                        cpu.hook_del(hook)
                    expected = (769 if discount else 767) if kind == 'two_products' else (770 if discount else 768)
                    assert len(calls) == 1 and calls[0][0] == expected
                    assert calls[0][1] == 0x02460000 + (side * 64 if kind == 'one_product' else 0), (kind, start, side, calls)
                    if kind == 'two_products':
                        assert calls[0][2] == 0x02460040
                    cases.append({'kind': kind, 'start': start, 'discount_flag': discount,
                                  'single_product_side': side, 'call_arguments': calls[0]})

    # The original branch consumes the economic-state getter result in r0.
    for state, expected in ((0, 771), (3, 772), (4, 773), (1, 8), (2, 8), (5, 8)):
        cpu = machine(arm)
        cpu.reg_write(UC_ARM_REG_R0, state)
        events = []

        def war(u, address, size, unused, events=events):
            if address == BASE + 0x53FE4:
                events.append(u.reg_read(UC_ARM_REG_R1))
                u.emu_stop()

        hook = cpu.hook_add(UC_HOOK_CODE, war)
        try:
            cpu.emu_start(BASE + 0xBA354, 0x027E0000, count=40)
        finally:
            cpu.hook_del(hook)
        assert events == [expected]
        cases.append({'kind': 'supplied_economic_result', 'state': state, 'IDs': events})

    for start, terminal, flag, expected in (
        (0xBBDA4, 0xBBDC8, 0, [774, 779, 766]),
        (0xBBED4, 0xBBF04, 0, [778, 780, 766]),
        (0xBBED4, 0xBBF04, 1, [775, 780, 766]),
        (0xBC018, 0xBC05C, 0, [776, 777, 781, 766]),
        (0xBC08C, 0xBC0B8, 0, [783, 766]),
        (0xBC08C, 0xBC0B8, 1, [782, 766]),
    ):
        cpu = machine(arm)
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.reg_write(UC_ARM_REG_R5, 1)
        cpu.mem_write(STACK + 0x10, struct.pack('<I', flag))
        events, support_calls = [], []

        def letters(u, address, size, unused, events=events, support_calls=support_calls, terminal=terminal):
            if address == BASE + 0x53FE4:
                events.append(u.reg_read(UC_ARM_REG_R1))
                u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
            elif address == BASE + 0x1096F8:
                support_calls.append([u.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)])
                u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
            elif address == BASE + terminal:
                u.emu_stop()

        hook = cpu.hook_add(UC_HOOK_CODE, letters)
        try:
            cpu.emu_start(BASE + start, 0x027E0000, count=200)
        finally:
            cpu.hook_del(hook)
        assert events == expected and cpu.reg_read(UC_ARM_REG_PC) == BASE + terminal
        cases.append({'kind': 'letter_or_thanks_fragment', 'start': start, 'terminal': terminal,
                      'flag': flag, 'IDs': events, 'observed_skipped_support_calls': support_calls})
    return cases


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    clean, current, canonical = (NdsImage.open(p) for p in (
        'work/clean.nds', CURRENT, 'out/raphael_natural_v2_accepted_base.nds'))
    path = '/COMMON/MESFILE.DK4'
    clean_arm, arm = clean.read_file('/__arm9__.bin'), current.read_file('/__arm9__.bin')
    assert sha(CURRENT.read_bytes()) == 'a44acfb6431fd2ec48e1ae5b5899ddbf1744bcac8a68e1ca6c5ec1fbc14fd246'
    assert all(clean_arm[a:b] == arm[a:b] for a, b in SPANS)
    first, second = fragments(clean_arm), fragments(arm)
    assert first == second and len(first) == 36
    save(ROOT / 'native_context.json', {
        'source_spans': [{'start': a, 'end': b, 'sha256': sha(clean_arm[a:b])} for a, b in SPANS],
        'all36_original_decision_fragments_each_clean_and_current': first,
        'product_name_getters_are_tagged_stubs_for_argument_order_only': True,
        'whole_eligibility_item_effects_earned_letters_and_actual_gameplay_not_claimed': True,
        'source_ARM9_sha256': sha(clean_arm), 'current_ARM9_sha256': sha(arm),
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    source = common_message_entries(clean.read_file(path), clean_arm)
    before = common_message_entries(current.read_file(path), arm, clean=False)
    accepted = common_message_entries(canonical.read_file(path), canonical.read_file('/__arm9__.bin'), clean=False)
    records = []
    for n in IDS:
        context = ('Original four paired/single product branches select767/768 when the supplied stack flag is zero and769/770 otherwise. Two names retain r7 then r8 order; one name retains whichever original product is present. Native getter stubs prove argument order, not which real goods qualify.' if n < 771
                   else 'Original economic-state result0/3/4 selects771/772/773; supplied other results select original8. Getter eligibility and actual economic events are not claimed.' if n < 774
                   else 'Original Market reward fragments bind774 then779,775 or778 then780,and776 then777 then781; each ends with766.782/783 are original alternative closing favors/thanks. Each fragment is executed with supplied state; full reward eligibility, item effects and gameplay remain unverified.')
        note = ('Keep both product names in source order; two named goods permit plural they. Preserve fast sales and frequent stockouts.' if n == 767
                else 'Avoid singular/plural pronouns for the substituted product. Restore gratitude and repeated stockouts; remove the invented service-price offer.' if n == 768
                else 'Preserve the enthusiastic favorable-treatment offer and both products. Sweeten the deal does not invent a precise discount.' if n == 769
                else 'Preserve hesitation and favorable treatment; use number-neutral demand language. No precise discount or stockout condition is invented.' if n == 770
                else 'Preserve recent economic direction, difficulty or improvement, and the desire for the war to end; no forecast or new event is invented.' if n < 774
                else 'Distinguish introduction from recommendation, large quantities where stated, and small towns from any town. Preserve item-upgrade wording rather than infer storage adjacency as spoken sequence. Generic service-price placeholders are removed.' if n < 782
                else 'Restore the actual extra favor or grateful request for continued supply; no numeric bonus is invented.')
        records.append({'id': f'COMMON_MESSAGE_{n}', 'message_id': n,
                        'japanese': source[n].text.decode('cp932'), 'source_hex': source[n].text.hex(),
                        'source_reference': {'block': source[n].block, 'record': source[n].record_index, 'offset': source[n].block_offset},
                        'current_English': before[n].text.decode('cp932'), 'current_text_hex': before[n].text.hex(),
                        'current_reference': {'block': before[n].block, 'record': before[n].record_index, 'offset': before[n].block_offset},
                        'canonical_source_hex': accepted[n].text.hex(), 'english': TEXT[n] + '{PAD}',
                        'source_meaning': GLOSS[n], 'localization_note': note,
                        'speaker': 'Market Trader, original town merchant', 'context': context,
                        'decision': 'retain-wording' if n in (779, 780) else 'revise',
                        'review': {'source': True, 'context': True, 'localization': True, 'naturalness': True, 'formatting': False},
                        'status': 'source-context-prose-draft-formatting-integration-gameplay-pending'})
    doc = {'format': 'dk4-common-entry-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
           'encoder': 'dialogue-fixed-v1', 'target_locale': 'en-US', 'file_path': path,
           'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
           'source_clean_COMMON_sha256': sha(clean.read_file(path)),
           'source_canonical_COMMON_sha256': sha(canonical.read_file(path)),
           'source_pins': {kind: {'path': str(p), 'sha256': sha(Path(p).read_bytes())} for kind, p in (
               ('japanese', 'work/clean.nds'), ('current', CURRENT), ('canonical', 'out/raphael_natural_v2_accepted_base.nds'))},
           'context_evidence': str(ROOT / 'native_context.json'), 'status': 'research-draft-not-integrated',
           'records': records, 'full_goal_complete': False}
    if MANUSCRIPT.exists():
        assert json.loads(MANUSCRIPT.read_text(encoding='utf-8')) == doc
    else:
        save(MANUSCRIPT, doc)
    save(ROOT / 'clean_and_current_neighbors.json', {
        kind: [{'id': n, 'text': entries[n].text.decode('cp932'), 'hex': entries[n].text.hex()}
               for n in range(750, 785)] for kind, entries in (('Japanese', source), ('current_V754', before))})
    print('17 source/context prose drafts;36 native fragments each clean/current pass. Formatting/integration/gameplay pending.', flush=True)


if __name__ == '__main__':
    main()
