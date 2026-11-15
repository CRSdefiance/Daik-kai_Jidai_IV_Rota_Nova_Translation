"""Exact five-table static-duel scope inside the original108-byte owned tail."""
from keystone import Ks,KS_ARCH_ARM,KS_MODE_THUMB
from scripts.duel_cache_front_v1142 import assemble as prior,ADDRESS,END

TABLES=(0x02117340,0x02117360,0x021174E0,0x02117560,0x021175C0)


def assemble(size):
    _,source=prior(size)
    old='movs r3,#208\nlsls r3,r3,#1\ncmp r2,r3\nbne original'
    new='subs r2,#208\nsubs r2,#208\nbeq selected\ncmp r2,#128\nbeq selected\ncmp r2,#224\nbne original'
    assert source.count(old)==1;source=source.replace(old,new)
    assert source.count('mov r0,r6\nsubs r0,#1')==2
    source=source.replace('mov r0,r6\nsubs r0,#1','mov r0,r6')
    assert source.count('blx r6')==1
    source=source.replace('blx r6','adds r6,#1\nblx r6')
    assert source.count('cache: .word 0x0228e70d')==1
    source=source.replace('cache: .word 0x0228e70d','cache: .word 0x0228e70c')
    code=bytes(Ks(KS_ARCH_ARM,KS_MODE_THUMB).asm(source,ADDRESS)[0])
    assert len(code)==END-ADDRESS==108,len(code)
    return code,source
