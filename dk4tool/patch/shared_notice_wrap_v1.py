"""Select the existing native modal paragraph formatter for six shared notices."""

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.market_goods_info_terminator_v1 import PAYLOAD as MARKET_LITERAL
from dk4tool.patch.ship_command_label_v1 import ALLOCATION as SHIP_LITERAL


BASE = 0x02000000
SOURCE_SHA256 = 'f9afa693ba4f7abd8ebf59c46585a7522aed52a9cfd07534965bb867b72fdfb0'
HOOK = 0x01FFC8EC
LEGACY = 0x01FFC900
SELECTOR = 0x01FFD020
NOTICE_PARENT = 0x020546E8
MESSAGE_IDS = (93, 94, 95, 96, 125, 126)
ASM = '''
    ldr r3, [sp, #0xc4]
    ldr ip, =0x020546e8
    cmp r3, ip
    bne 0x01ffc900
    ldr r3, [sp, #0xd0]
    sub ip, r3, #93
    cmp ip, #3
    bls wrap
    sub ip, r3, #125
    cmp ip, #1
    bhi 0x01ffc900
wrap:
    push {r4-r6, lr}
    ldr r6, =0x01ffca00
    ldr ip, =0x01ffc941
    bx ip
    .ltorg
'''


def transform(source):
    if sha(source) != SOURCE_SHA256:
        raise ValueError('Exact registered Abandon Ship ARM9 required')
    code = MainCodeFile(source, BASE)
    if bytes(code.save()) != source:
        raise ValueError('Source ARM9 serialization differs')
    dispatcher, tail = code.sections[-2:]
    literals = MARKET_LITERAL + SHIP_LITERAL
    if (len(code.sections), dispatcher.ramAddress, len(dispatcher.data),
            tail.ramAddress, bytes(tail.data), tail.bssSize) != (
            6, 0x01FFC000, 0x1000, SELECTOR - len(literals), literals, 0):
        raise ValueError('Exact dispatcher and Market/ship literal geometry required')
    assembler = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    original = bytes(assembler.asm(f'b {LEGACY:#x}', HOOK)[0])
    branch = bytes(assembler.asm(f'b {SELECTOR:#x}', HOOK)[0])
    allocation = bytes(assembler.asm(ASM, SELECTOR)[0])
    at = HOOK - dispatcher.ramAddress
    if dispatcher.data[at:at + 4] != original or len(allocation) % 4:
        raise ValueError('Original fallback branch or selector alignment differs')
    if not SELECTOR + len(allocation) <= BASE or any(
        SELECTOR < section.ramAddress + len(section.data) + section.bssSize
        and section.ramAddress < SELECTOR + len(allocation) for section in code.sections
    ):
        raise ValueError('Selector overlaps an existing section or leaves ITCM')
    dispatcher.data[at:at + 4] = branch
    tail.data.extend(allocation)
    target = bytes(code.save())

    restored = MainCodeFile(target, BASE)
    assert restored.sections[-2].data[at:at + 4] == branch
    assert bytes(restored.sections[-1].data) == literals + allocation
    restored.sections[-2].data[at:at + 4] = original
    del restored.sections[-1].data[len(literals):]
    assert bytes(restored.save()) == source
    return target, dict(source_ARM9_sha256=sha(source), target_ARM9_sha256=sha(target),
        hook=HOOK, legacy_dispatch=LEGACY, selector=SELECTOR, selector_bytes=len(allocation),
        message_IDs=list(MESSAGE_IDS), original_notice_parent=NOTICE_PARENT,
        reused_native_modal_body=0x01FFC940, reused_native_paragraph_helper=0x01FFCA00,
        Market_and_ship_literal_prefix_exact=True, complete_serialized_parent_inverse=True)
