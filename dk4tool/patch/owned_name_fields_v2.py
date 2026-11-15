"""Plan fixed-slot, exclusively owned source-bound name edits without ROM mutation."""
import struct
from ndspy.code import MainCodeFile
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.grand_race_menu_release import sha

def plan_arm9_name_fields(arm,proposal,clean):
    def require(ok,message):
        if not ok:raise ValueError(message)
    require(sha(arm)==proposal['runtime']['ARM9_sha256'],'Exact registered ARM9 parent required')
    require(proposal['format']=='dk4-owned-name-fields-proposal-v2','Owned name field schema required')
    sections=MainCodeFile(arm,BASE).sections
    payload=bytes(sections[3].data[:-48])
    require(len(payload)==123264,'Existing complete staged allocation required')
    staged=arm.find(bytes(sections[3].data))
    require(staged>=0 and arm.find(bytes(sections[3].data),staged+1)<0,'Unique physical staged allocation required')
    table=struct.unpack_from('<I',arm,0xCDAC0)[0]
    clean_table=struct.unpack_from('<I',clean,0xCDAC0)[0]
    target=bytearray(arm);owned=set();proofs=[]
    require(bool(proposal['fields']),'At least one source-bound field required')
    for row in proposal['fields']:
        actor,column=row['actor'],row['column']
        require(0<=actor<207 and column in [0,4,8],'Ordinary given/surname/middle field required')
        require(all(row['review'][gate] is True for gate in ['source','context','localization','naturalness']) and bool(row['reason'].strip()),'Individual editorial gates and reason required')
        field=table-BASE+32*actor+column;pointer=struct.unpack_from('<I',arm,field)[0]
        require((field,pointer)==(row['table_field_offset'],row['pointer']),'Exact source table field required')
        old,new=bytes.fromhex(row['source_hex']),bytes.fromhex(row['target_hex'])
        require(0<len(old)==len(new)==row['owned_bytes'] and b'\0' not in old,'One fixed complete source name span required')
        require(old.decode('cp932')==row['current_text'],'Exact current spelling required')
        require(new.rstrip(b'\0')==row['target_text'].encode('ascii') and all(32<=b<127 for b in new.rstrip(b'\0')) and new==new.rstrip(b'\0')+bytes(len(new)-len(new.rstrip(b'\0'))),'Complete printable ASCII target and trailing compiler zeros only')
        at=staged+pointer-POOL if POOL<=pointer<POOL+len(payload) else pointer-BASE
        require(at==row['physical_offset'] and 0<=at<=len(arm)-len(old)-16,'Exact original physical mapping required')
        require(arm[at:at+len(old)]==old and arm[at+len(old):at+len(old)+16].hex()==row['following16_hex'] and arm[at+len(old)]==0,'Source, original terminator and adjacent sixteen bytes required')
        require(not owned.intersection(range(at,at+len(old))),'Overlapping name spans forbidden')
        source=row['source_clean_component'];clean_field=clean_table-BASE+32*actor+column
        clean_pointer=struct.unpack_from('<I',clean,clean_field)[0]
        clean_bytes=bytes.fromhex(source['hex'])
        require(source['column']==column and clean_field==source['source_ARM9_field_offset'] and clean_pointer==source['pointer'] and clean_pointer-BASE==source['offset'] and clean[clean_pointer-BASE:clean_pointer-BASE+len(clean_bytes)+1]==clean_bytes+b'\0' and clean_bytes.decode('cp932')==source['text'],'Exact clean Japanese name component required')
        owners=[]
        for ident in range(207):
            for col in [0,4,8]:
                f=table-BASE+32*ident+col;p=struct.unpack_from('<I',arm,f)[0]
                if pointer<=p<pointer+len(old):owners.append(dict(actor=ident,column=col,pointer=p,field_offset=f))
        require(owners==row['owners']==[dict(actor=actor,column=column,pointer=pointer,field_offset=field)],'Exclusive name ownership including all interior aliases required')
        references=[dict(offset=i,pointer=struct.unpack_from('<I',arm,i)[0]) for i in range(0,len(arm)-3,4) if pointer<=struct.unpack_from('<I',arm,i)[0]<pointer+len(old)]
        require(references==row['aligned_ARM9_references']==[dict(offset=field,pointer=pointer)],'Unexpected aligned pointer reference blocks the edit')
        target[at:at+len(old)]=new;owned.update(range(at,at+len(old)))
        proofs.append(dict(actor=actor,column=column,physical_offset=at,RAM_pointer=pointer,old_hex=old.hex(),new_hex=new.hex(),owned_bytes=len(old),exclusive_owners=owners,aligned_pointer_references=references,clean_component=source))
    target=bytes(target);after=MainCodeFile(target,BASE).sections
    require(len(target)==len(arm) and len(after)==len(sections),'ARM9 size or section allocation changed')
    for before,now in zip(sections,after,strict=True):
        require(before.ramAddress==now.ramAddress and len(before.data)==len(now.data),'Section allocation changed')
        start=arm.find(bytes(before.data));require(start>=0,'Original section storage required')
        expected=target[start:start+len(before.data)]
        require(bytes(now.data)==expected,'Unowned section or staged mapping changed')
    inverse=bytearray(target)
    for p in proofs:inverse[p['physical_offset']:p['physical_offset']+p['owned_bytes']]=bytes.fromhex(p['old_hex'])
    require(bytes(inverse)==arm,'Whole ARM9 inverse failed')
    return target,dict(parent_ARM9_sha256=sha(arm),target_ARM9_sha256=sha(target),clean_ARM9_sha256=sha(clean),fields=proofs,
        owned_span_bytes=len(owned),changed_bytes=sum(a!=b for a,b in zip(arm,target,strict=True)),
        all_unowned_ARM9_bytes_sections_pointer_tables_andallocations_exact=True,
        complete_staged_payload_size=123264,complete_parent_inverse_exact=True,no_ROM_mutation=True)
