push {r4-r11,lr}
mov r4,r0
mov r5,r1
mov r8,r1
mov r6,#0
mov r7,#36
mov r3,#1
next:
mov r9,#0
spaces:
ldrb r0,[r4]
cmp r0,#32
cmpne r0,#10
bne word
add r4,r4,#1
mov r9,#1
b spaces
word:
mov r10,r4
mov r11,#0
scan:
ldrb r0,[r10,r11]
cmp r0,#0
cmpne r0,#32
cmpne r0,#10
beq ready
add r11,r11,#1
b scan
ready:
cmp r11,#0
beq finish
sub r2,r5,r8
add r2,r2,r9
add r2,r2,r11
cmp r2,#236
bhi fail
add r2,r6,r9
add r2,r2,r11
cmp r2,r7
bls copy_spaces
mov r0,#10
strb r0,[r5],#1
mov r0,#32
strb r0,[r5],#1
strb r0,[r5],#1
cmp r9,#0
subne r9,r9,#1
mov r6,#0
bl 0x01ffcb40
add r3,r3,#1
cmp r3,#4
bhi fail
add r2,r9,r11
cmp r2,r7
bhi fail
copy_spaces:
cmp r9,#0
beq copy_word
mov r0,#32
space_copy:
strb r0,[r5],#1
add r6,r6,#1
subs r9,r9,#1
bne space_copy
copy_word:
mov r4,r10
word_copy:
ldrb r0,[r4],#1
strb r0,[r5],#1
add r6,r6,#1
subs r11,r11,#1
bne word_copy
b next
finish:
mov r0,#0
strb r0,[r5]
sub r0,r5,r8
b done
fail:
mov r0,#0
done:
pop {r4-r11,pc}
