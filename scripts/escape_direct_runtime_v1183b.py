"""Direct escape correction retaining the live status suffix constant."""
import struct
from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB
from dk4tool.patch.grand_race_menu_release import sha
from scripts import escape_direct_runtime_v1183 as previous
from scripts.escape_direct_runtime_v1183 import (BASE,SOURCE,CONTRACTS,END,GATE,TABLE_BYTES,
    PACKED_PHRASES,STATUS_LITERAL,DIRECT_PARENT,KEYS,contract_rows,table,gate)

STATUS_LOAD, SUFFIX_SLOT = 0x02147D42, 0x02147D4C


def apply(arm):
    target, plan = previous.apply(arm)
    assert arm[STATUS_LOAD-BASE:STATUS_LOAD-BASE+2].hex()=='6d48'
    assert arm[SUFFIX_SLOT-BASE:SUFFIX_SLOT-BASE+8].hex()=='6a4b18476f726500'
    # The source-owned status tail spans44 bytes. Its current36-byte function
    # ends in an unconditional BLX; the old8-byte tail has no incoming accesses
    # in the complete literal/branch/PC-relative census recorded by1184b.
    literal=arm[GATE-BASE+164:GATE-BASE+168]
    assert literal.hex()=='68de1602'
    load=bytes(Ks(KS_ARCH_ARM,KS_MODE_THUMB).asm(f'ldr r0,[pc,#{SUFFIX_SLOT-((STATUS_LOAD+4)&~3)}]',STATUS_LOAD)[0])
    assert len(load)==2
    result=bytearray(target)
    for at,data in ((STATUS_LOAD,load),(SUFFIX_SLOT,literal)):
        before=arm[at-BASE:at-BASE+len(data)]
        result[at-BASE:at-BASE+len(data)]=data
        plan['patches'].append({'address':at,'source_hex':before.hex(),'target_hex':data.hex()})
    result=bytes(result)
    restored=bytearray(result)
    for row in plan['patches']:
        data=bytes.fromhex(row['source_hex']);at=row['address']-BASE
        restored[at:at+len(data)]=data
    assert bytes(restored)==arm
    plan.update(target_ARM9_sha256=sha(result),
        private_spans=plan['private_spans']+[[0x02147D28,0x02147D54]],
        status_suffix_constant_moved_within_original44_byte_status_tail=True,
        live_status_PC_relative_load_rebound_to_exact_preserved_pointer=True,
        failed_1184_status_regression_retained_as_evidence=True)
    return result,plan
