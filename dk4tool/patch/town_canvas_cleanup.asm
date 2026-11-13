push {r0-r4,lr}
ldr r4,slot_address
ldr r0,[r4]
cmp r0,#0
beq done
bl 0x02005180
mov r0,#0
str r0,[r4]
done:
pop {r0-r4,lr}
b 0x020d2e90
slot_address: .word 33540348