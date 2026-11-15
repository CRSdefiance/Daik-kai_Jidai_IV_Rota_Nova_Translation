
ldr r3,[sp,#0x264]
ldr ip,parent
cmp r3,ip
bne fallback
ldr r3,[sp,#0x274]
bic r3,r3,#1
cmp r3,#820
bne fallback
push {r4,lr}
mov r4,r0
bl 0x01ff9edc
sub sp,sp,#240
mov r0,r4
ldrb r3,[r0]
cmp r3,#32
beq wrap
mov r2,#0
length:
ldrb r3,[r0,r2]
cmp r3,#0
beq shift_start
add r2,r2,#1
b length
shift_start:
cmp r2,#237
bhi wrap
shift:
ldrb r3,[r0,r2]
add ip,r2,#1
strb r3,[r0,ip]
subs r2,r2,#1
bpl shift
mov r3,#32
strb r3,[r0]
wrap:
mov r0,r4
mov r1,sp
bl 0x01ffca00
cmp r0,#0
beq done
add r2,r0,#1
mov r0,r4
mov r1,sp
bl 0x020cec74
done:
mov r0,#0
add sp,sp,#240
pop {r4,pc}
fallback:
b 0x01ff9edc
parent:
.word 0x02054014
