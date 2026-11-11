"""Use the dialogue font for whole CP932 digit pairs in two fleet reports."""

from dk4tool.patch.ship_emergency_wrap_v1 import LITERAL_PARAGRAPH


AMOUNT_TABLES = (0x02117F20, 0x02117FA0)
BUFFER = 144


def amount_assembly():
    # The native printf output arrives in r1. Retain it and format an ASCII
    # copy on the stack. Mixed non-digit CP932, no digits, or no terminating
    # NUL within the qualified input bound take the original formatter path.
    return f"""
amount_wrap:
    pop {{r3-r5}}
    push {{r1-r7, lr}}
    sub sp, sp, #{BUFFER}
    mov r4, r1
    mov r5, sp
    mov r6, #{BUFFER}
    mov r3, #0
amount_next:
    subs r6, r6, #1
    blo amount_original
    ldrb r7, [r4], #1
    cmp r7, #0
    beq amount_done
    cmp r7, #0x80
    blo amount_copy
    cmp r7, #0x82
    bne amount_original
    subs r6, r6, #1
    blo amount_original
    ldrb r7, [r4], #1
    cmp r7, #0x4f
    blo amount_original
    cmp r7, #0x58
    bhi amount_original
    sub r7, r7, #0x1f
    mov r3, #1
amount_copy:
    strb r7, [r5], #1
    b amount_next
amount_done:
    cmp r3, #0
    beq amount_original
    strb r7, [r5]
    mov r1, sp
    ldr r2, [sp, #{BUFFER + 4}]
    ldr r3, [sp, #{BUFFER + 8}]
    bl {LITERAL_PARAGRAPH:#x}
    add sp, sp, #{BUFFER}
    pop {{r1-r7, pc}}
amount_original:
    add sp, sp, #{BUFFER}
    pop {{r1-r7, lr}}
    b {LITERAL_PARAGRAPH:#x}
"""
