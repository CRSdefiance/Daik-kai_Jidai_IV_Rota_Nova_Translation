"""Source-locked, fixed-slot Abkhaz/Elysion data plan; no renderer or allocation changes."""
import struct
from dk4tool.patch.grand_race_menu_release import sha

BASE=0x02000000
CLEAN='0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731'
SPECS=[('ABKHAZ_CITY',0x124CCC,0x15CF74,'アブハーズ','Abhaz','Abkhaz',11),
       ('ELYSION_CODE_LITERAL',0x2BA2C,0x134D54,'エリュシオン','エリュシオン','Elysion',13)]
CODE_SPANS=[(0xB5600,0xB5648),(0xB5690,0xB56A8),(0xCD6B8,0xCD6CC),
            (0x2B994,0x2BA30),(0xA48F8,0xA4908),(0xCED98,0xCEDC8),(0x1A4E0,0x1A4E8),(0xA43C0,0xA443C)]

def references(arm,pointer,capacity):
    return [dict(offset=i,pointer=struct.unpack_from('<I',arm,i)[0]) for i in range(len(arm)-3)
            if pointer<=struct.unpack_from('<I',arm,i)[0]<pointer+capacity]

def plan_static_labels(arm,proposal,clean):
    def need(value,message):
        if not value:raise ValueError(message)
    need(sha(clean)==CLEAN,'Exact clean ARM9 required')
    need(sha(arm)==proposal['parent_ARM9_sha256'],'Exact complete parent ARM9 required')
    need([r['id'] for r in proposal['fields']]==[s[0] for s in SPECS],'Both exact source-owned labels required')
    for lo,hi in CODE_SPANS:need(arm[lo:hi]==clean[lo:hi],f'Source-native label consumer changed:{lo:x}')
    need(struct.unpack_from('<I',arm,0xCD6C8)[0]==0x2122560,'Original city record table required')
    need(0x122560+87*0x74==0x124CCC,'Source Abkhaz city87 owner required')
    need(struct.unpack_from('<I',arm,0xA4904)[0]==0x20CED98,'Original name setter must tailcall native C-string copy')
    result=bytearray(arm);fields=[]
    for row,(ident,field,at,ja,old,en,capacity) in zip(proposal['fields'],SPECS,strict=True):
        pointer=BASE+at;encoded=en.encode('ascii')+b'\0'
        need((row['pointer_field_offset'],row['pointer'],row['physical_offset'],row['source_slot_capacity'])==(field,pointer,at,capacity),'Exact typed owner/slot geometry required')
        need(struct.unpack_from('<I',arm,field)[0]==struct.unpack_from('<I',clean,field)[0]==pointer,'Original pointer changed')
        source=ja.encode('cp932')+b'\0';need(len(source)==capacity and clean[at:at+capacity]==source,'Clean complete text/NUL slot required')
        need(bytes.fromhex(row['clean_slot_hex'])==source and row['source_text']==ja,'Clean ownership binding changed')
        current=arm[at:at+capacity];need(current==bytes.fromhex(row['current_full_slot_hex']) and current.split(b'\0')[0].decode('cp932')==old,'Complete current slot changed')
        need(row['current_text']==old and row['english']==en and bytes.fromhex(row['target_span_hex'])==encoded,'Exact reviewed wording required')
        need(0<len(encoded)<=capacity and row['owned_span_bytes']==len(encoded),'Target must fit complete source slot with NUL')
        need(bytes.fromhex(row['old_span_hex'])==current[:len(encoded)],'Owned prefix changed')
        expected=[dict(offset=field,pointer=pointer)]
        need(references(arm,pointer,capacity)==references(clean,pointer,capacity)==expected,'All-byte direct/interior pointer ownership changed')
        result[at:at+len(encoded)]=encoded
        fields.append(dict(id=ident,source_typed_pointer_field=field,pointer=pointer,physical_offset=at,
            source_complete_slot_hex=source.hex(),parent_complete_slot_hex=current.hex(),owned_prefix_bytes=len(encoded),
            target_prefix_hex=encoded.hex(),parent_prefix_hex=current[:len(encoded)].hex(),all_byte_pointer_references=expected,
            following16_unchanged_hex=arm[at+capacity:at+capacity+16].hex(),
            typed_owner='city-table-record87.first-field' if ident=='ABKHAZ_CITY' else 'original-2B994-index3-ship-name-override-literal',
            computed_alias_scope='Original typed table/command consumer checked; pointer scan alone is not the ownership proof.'))
    target=bytes(result);need(sha(target)==proposal['proposed_ARM9_sha256'],'Exact complete proposed ARM9 required')
    inverse=bytearray(target)
    for row in fields:
        at=row['physical_offset'];inverse[at:at+row['owned_prefix_bytes']]=bytes.fromhex(row['parent_prefix_hex'])
    need(bytes(inverse)==arm,'Complete parent inverse failed')
    need(sum(a!=b for a,b in zip(arm,target,strict=True))==proposal['changed_bytes']==12,'Unexpected changed bytes')
    need(sum(r['owned_prefix_bytes'] for r in fields)==proposal['owned_span_bytes']==15,'Exact owned prefix budget required')
    return target,dict(fields=fields,owned_span_bytes=15,changed_bytes=12,parent_ARM9_sha256=sha(arm),target_ARM9_sha256=sha(target),
        complete_parent_inverse_exact=True,all_unowned_bytes_pointer_fields_sections_fonts_andallocations_unchanged=True,
        source_qualified_consumer_code_spans=[dict(offset=lo,bytes=hi-lo,sha256=sha(arm[lo:hi])) for lo,hi in CODE_SPANS],
        native_andvisual_checks_required_before_registered_release=True,no_ROM_mutation=True)
