"""Two sighting memberships in the same212/128-byte banks; no memory growth."""
import struct
from types import FunctionType
from keystone import Ks,KS_ARCH_ARM,KS_MODE_ARM,KS_MODE_THUMB
from ndspy.code import MainCodeFile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts import reinforcement_sniping_runtime_v1025 as previous

BASE=0x02000000
SOURCE='cd9a7d894047d655f72d6d6152d253aafeb9d5c2e5082a7b1e934d590e7fa028'
CONTRACTS=previous.CONTRACTS
TABLE_BYTES=184
PACKED_PHRASES=CONTRACTS+TABLE_BYTES
END=previous.END
MODAL=previous.MODAL
STATUS_LITERAL=previous.STATUS_LITERAL
GATE=previous.GATE


def contract_rows():
    result=[]
    for parent,offset,high,values in previous.contract_rows():
        values=set(values)
        if parent==0x02053DB8:
            assert (offset,high)==(0x27C,0x0211)
            assert not values&{0x8540,0x8560}
            values.update((0x8540,0x8560))
        result.append((parent,offset,high,tuple(sorted(values))))
    return result


def table():
    build=FunctionType(previous.previous.table.__code__,{**previous.previous.table.__globals__,
        'TABLE_BYTES':TABLE_BYTES,'contract_rows':contract_rows})
    return build()


def modal_code():
    assembly=previous.modal_code()[2]
    old=f'bl {previous.FILTER}'
    assert assembly.count(old)==1
    # The old four-byte BL + six-byte leaf helper becomes four inline bytes.
    # Carry0 keeps r3;carry1 MOVS58 is exactly the previous helper semantics.
    assembly=assembly.replace(old,'bcc sighting_filter_done\nmovs r3,#58\nsighting_filter_done:')
    ka,kt=Ks(KS_ARCH_ARM,KS_MODE_ARM),Ks(KS_ARCH_ARM,KS_MODE_THUMB)
    stub=bytes(ka.asm('add ip,pc,#1;bx ip',MODAL)[0])
    body=bytes(kt.asm(assembly,MODAL+8)[0])
    assert len(stub)==8 and len(stub+body)==128
    return stub+body,assembly


def apply(arm):
    assert sha(arm)==SOURCE
    assert arm[CONTRACTS-BASE:CONTRACTS-BASE+previous.TABLE_BYTES]==previous.table()
    assert arm[previous.FILTER-BASE:END-BASE]==previous.modal_code()[1]
    assert struct.unpack_from('<I',arm,STATUS_LITERAL-BASE)[0]==previous.PACKED_PHRASES
    packed=arm[previous.PACKED_PHRASES-BASE:previous.PACKED_PHRASES-BASE+24]
    wrap,assembly=modal_code();public=table()+packed+bytes(4)
    assert len(public)==END-CONTRACTS==212 and PACKED_PHRASES+24+4==END
    old=MainCodeFile(arm,BASE);offset=MODAL-old.sections[4].ramAddress
    assert bytes(old.sections[4].data[offset:offset+128])==previous.modal_code()[0]
    changed=[];target=bytearray(arm)
    for at,data in ((CONTRACTS,public),(STATUS_LITERAL,struct.pack('<I',PACKED_PHRASES))):
        source=arm[at-BASE:at-BASE+len(data)];target[at-BASE:at-BASE+len(data)]=data
        changed.append({'address':at,'source_hex':source.hex(),'target_hex':data.hex()})
    final=MainCodeFile(bytes(target),BASE);final.sections[4].data[offset:offset+128]=wrap
    result=bytes(final.save());new=MainCodeFile(result,BASE)
    shape=lambda code:[(s.ramAddress,len(s.data),s.bssSize) for s in code.sections]
    assert shape(old)==shape(new) and cache_plan(arm)==cache_plan(result)
    assert len(new.sections[3].data)-48==123040
    assert all(old.sections[i].data==new.sections[i].data for i in (1,2,3))
    assert arm[GATE-BASE:GATE-BASE+164]==result[GATE-BASE:GATE-BASE+164]
    restore=MainCodeFile(result,BASE);restore.sections[4].data[offset:offset+128]=previous.modal_code()[0]
    restored=bytearray(restore.save())
    for row in changed:
        at=row['address']-BASE;data=bytes.fromhex(row['source_hex']);restored[at:at+len(data)]=data
    assert bytes(restored)==arm
    return result,{'source_ARM9_sha256':sha(arm),'research_ARM9_sha256':sha(result),
        'public_changes':changed,'ITCM_modal_address':MODAL,
        'ITCM_modal_source_hex':previous.modal_code()[0].hex(),'ITCM_modal_target_hex':wrap.hex(),
        'only_new_membership':{'parent02053DB8':[0x02118540,0x02118560]},
        'contract_table_bytes_before_after':[182,184],'public_bank_bytes_before_after':[212,212],
        'ITCM_modal_bytes_before_after':[128,128],'previous_six_byte_leaf_inlined_in_same_four_byte_call_slot':True,
        'unreferenced_public_tail_bytes':4,'packed_status24_bytes_exact_moved2':True,
        'native_gate164_bytes_exact':True,'all_sections_BSS_cache_and_entire123040_staged_payload_exact':True,
        'all_other_ARM9_bytes_restore_exactly':True,'modal_assembly':assembly,
        'private_spans':[[CONTRACTS,END],[MODAL,MODAL+128],[STATUS_LITERAL,STATUS_LITERAL+4]],
        'research_only_full_selector_ABI_regressions_fonts_and_gameplay_pending':True}
