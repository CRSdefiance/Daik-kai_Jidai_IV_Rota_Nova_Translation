"""Three exact announcement memberships in the existing212-byte contract bank.

An8-byte ARM-to-Thumb entry replaces the12-byte literal entry,freeing four
bytes for the original bitmap shift in the modal caller. The helper then
shrinks10 to6 bytes,leaving room for two additional contract-range words.
"""
import struct
from types import FunctionType
from keystone import Ks,KS_ARCH_ARM,KS_MODE_ARM,KS_MODE_THUMB
from ndspy.code import MainCodeFile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts import battle_declaration_runtime_v993b as previous

BASE=0x02000000
SOURCE='42a31b92893961132530ab4ef86ec64e99969fe37a7a3bc56f7984a47edc74db'
CONTRACTS=previous.CONTRACTS
TABLE_BYTES=182
PACKED_PHRASES=CONTRACTS+TABLE_BYTES
FILTER=PACKED_PHRASES+24
END=previous.END
MODAL=previous.MODAL
STATUS_LITERAL=previous.STATUS_LITERAL
GATE=previous.previous.previous.bank.GATE


def contract_rows():
    rows=[]
    for parent,offset,high,values in previous.contract_rows():
        values=set(values)
        if parent==0x02053DB8:
            assert (offset,high)==(0x27C,0x0211)
            values.update((0x7300,0x73C0,0x73E0))
        rows.append((parent,offset,high,tuple(sorted(values))))
    return rows


def table():
    build=FunctionType(previous.table.__code__,{**previous.table.__globals__,
        'TABLE_BYTES':TABLE_BYTES,'contract_rows':contract_rows})
    return build()


def modal_code():
    assembly=previous.modal_code()[2]
    old=f'bl {previous.FILTER}'
    new=f'movs r4,#119\nlsrs r4,r3\nbl {FILTER}'
    assert assembly.count(old)==1;assembly=assembly.replace(old,new)
    helper='''bcc done
movs r3,#58
done:
bx lr
'''
    ka,kt=Ks(KS_ARCH_ARM,KS_MODE_ARM),Ks(KS_ARCH_ARM,KS_MODE_THUMB)
    stub=bytes(ka.asm('add ip,pc,#1; bx ip',MODAL)[0])
    body=bytes(kt.asm(assembly,MODAL+8)[0])
    filt=bytes(kt.asm(helper,FILTER)[0])
    assert len(stub)==8 and len(stub+body)==128 and len(filt)==6
    assert FILTER+len(filt)==END
    return stub+body,filt,assembly,helper


def apply(arm):
    assert sha(arm)==SOURCE
    assert arm[CONTRACTS-BASE:CONTRACTS-BASE+previous.TABLE_BYTES]==previous.table()
    assert arm[GATE-BASE:GATE-BASE+164]==previous.previous.gate()[0]
    assert struct.unpack_from('<I',arm,STATUS_LITERAL-BASE)[0]==previous.PACKED_PHRASES
    packed=arm[previous.PACKED_PHRASES-BASE:previous.PACKED_PHRASES-BASE+24]
    assert arm[previous.FILTER-BASE:END-BASE]==previous.modal_code()[1]
    wrap,filt,assembly,helper=modal_code();public=table()+packed+filt
    assert len(public)==END-CONTRACTS==212
    old=MainCodeFile(arm,BASE);itcm=old.sections[4];offset=MODAL-itcm.ramAddress
    assert bytes(itcm.data[offset:offset+128])==previous.modal_code()[0]
    target=bytearray(arm);changes=[]
    for at,value in ((CONTRACTS,public),(STATUS_LITERAL,struct.pack('<I',PACKED_PHRASES))):
        before=arm[at-BASE:at-BASE+len(value)]
        target[at-BASE:at-BASE+len(value)]=value
        changes.append({'address':at,'source_hex':before.hex(),'target_hex':value.hex()})
    new=MainCodeFile(bytes(target),BASE);new.sections[4].data[offset:offset+128]=wrap
    result=bytes(new.save());final=MainCodeFile(result,BASE)
    shape=lambda code:[(s.ramAddress,len(s.data),s.bssSize) for s in code.sections]
    assert shape(old)==shape(final) and cache_plan(arm)==cache_plan(result)
    assert all(old.sections[i].data==final.sections[i].data for i in (1,2,3))
    assert len(final.sections[3].data)-48==123040
    restore=MainCodeFile(result,BASE);restore.sections[4].data[offset:offset+128]=previous.modal_code()[0]
    restored=bytearray(restore.save())
    for c in changes:
        at=c['address']-BASE;value=bytes.fromhex(c['source_hex']);restored[at:at+len(value)]=value
    assert bytes(restored)==arm
    return result,{'source_ARM9_sha256':sha(arm),'research_ARM9_sha256':sha(result),
        'public_changes':changes,'ITCM_modal_address':MODAL,
        'ITCM_modal_source_hex':previous.modal_code()[0].hex(),'ITCM_modal_target_hex':wrap.hex(),
        'contract_table_bytes_before_after':[178,182],'filter_bytes_before_after':[10,6],
        'ARM_Thumb_entry_bytes_before_after':[12,8],'inlined_original_bitmap_shift_bytes':4,
        'entire_public_bank_bytes_before_after':[212,212],'entire_ITCM_modal_bytes_before_after':[128,128],
        'native_gate164_bytes_exact':True,'packed_status24_bytes_exact_moved4':True,
        'only_new_membership':{'parent02053DB8':[0x02117300,0x021173C0,0x021173E0]},
        'all_other_memberships_unchanged':True,'private_spans':[[CONTRACTS,END],[MODAL,MODAL+128],[STATUS_LITERAL,STATUS_LITERAL+4]],
        'all_sections_BSS_cache_and_entire123040_staged_payload_unchanged':True,
        'all_other_ARM9_bytes_restore_exactly':True,'modal_assembly':assembly,'filter_assembly':helper,
        'research_only_not_registered_or_gameplay_verified':True}
