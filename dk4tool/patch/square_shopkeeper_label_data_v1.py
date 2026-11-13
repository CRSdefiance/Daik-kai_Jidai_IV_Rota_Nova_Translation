"""Owned, reversible two-literal research transform for ten reviewed shopkeepers."""
import struct
from ndspy.code import MainCodeFile
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.grand_race_menu_release import sha

BASE,POOL,TABLE=0x02000000,0x02387A20,0x120B80
SOURCE='aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'
OWNERS=[(34984072,1429640),(37256580,1518832)]
OLD,NEW=b'Square Shopkeeper\0',b'Shopkeeper\0'

def require(ok,why):
    if not ok:raise ValueError('Shopkeeper data '+why)

def cstring(data,at):
    require(0<=at<len(data),'string address');end=data.find(b'\0',at)
    require(end>=at,'complete string');return data[at:end+1]

def transform(arm,clean,rows):
    require(sha(arm)==SOURCE,'exact predecessor ARM9')
    require([r['actor_ID'] for r in rows]==list(range(82,92)),'ten ordered actors')
    code=MainCodeFile(arm,BASE);payload=bytes(code.sections[3].data[:-48])
    require(len(code.sections)==5 and code.sections[3].ramAddress==0x023A7200 and len(payload)==123264 and arm.count(payload)==1,'complete current section/payload')
    payload_at=arm.index(payload);allfields=[struct.unpack_from('<3I',arm,TABLE+i*32) for i in range(207)]
    aliases=[];hits=[]
    for pointer,at in OWNERS:
        require(arm[at:at+len(OLD)]==OLD and (at==pointer-BASE or at==payload_at+pointer-POOL),'complete literal owner')
        for ident,fields in enumerate(allfields):
            for column,p in zip([0,4,8],fields,strict=True):
                if pointer<=p<pointer+len(OLD):aliases.append((ident,column,p-pointer))
        for delta in range(len(OLD)):
            needle=struct.pack('<I',pointer+delta);where=arm.find(needle)
            while where>=0:hits.append((where,pointer+delta,delta));where=arm.find(needle,where+1)
    require(sorted(aliases)==[(i,0,0) for i in range(82,92)],'all621 fields/no interior aliases')
    require(sorted((p,d) for p,_,d in hits)==[(TABLE+i*32,0) for i in range(82,92)],'unaligned base/interior ARM9 pointer census')
    for row in rows:
        ident=row['actor_ID'];field=TABLE+ident*32
        require(row['id']==f'DK4_ACTOR_{ident:03d}_PRIMARY_LABEL' and row['target_locale']=='en-US','source identity/locale')
        require((row['source_Japanese'],row['current_English'],row['english'],row['editorial_decision'])==('広場の店主','Square Shopkeeper','Shopkeeper','revise'),'source/current/proposed wording')
        require(all(row['review'][k] is True for k in ['source','context','localization','naturalness']),'four contextual prose gates')
        require(all(row[k] for k in ['source_meaning','speaker','context','localization_note']),'individual whole-context notes')
        require(row['new_dialogue_completion_credit']==0,'no surrounding-dialogue credit')
        sp,cp=[struct.unpack_from('<I',a,field)[0] for a in [clean,arm]]
        at=payload_at+cp-POOL if POOL<=cp<POOL+len(payload) else cp-BASE
        require(row['source_reference']==dict(source_file='/__arm9__.bin',pointer_field=field,pointer=sp,storage_offset=sp-BASE,terminated_hex=cstring(clean,sp-BASE).hex()),'exact clean reference')
        require(cstring(clean,sp-BASE)[:-1].decode('cp932')=='広場の店主','clean role')
        require(row['current_reference']==dict(source_file='/__arm9__.bin',pointer_field=field,runtime_pointer=cp,file_offset=at,terminated_hex=OLD.hex()),'exact predecessor reference')
        require(len(row['all_three_source_current_name_fields'])==3,'three original fields')
        for column,part in zip([0,4,8],row['all_three_source_current_name_fields'],strict=True):
            f=field+column;p,q=[struct.unpack_from('<I',a,f)[0] for a in [clean,arm]]
            require(part['column']==column and part['pointer_field']==f,'field identity')
            if not p:
                require(q==0 and part['source_null'] and part['current_null'],'null fields');continue
            storage=payload_at+q-POOL if POOL<=q<POOL+len(payload) else q-BASE
            require(part['source_pointer']==p and part['source_storage_offset']==p-BASE and part['source_terminated_hex']==cstring(clean,p-BASE).hex(),'clean field')
            require(part['current_pointer']==q and part['current_storage_offset']==storage and part['current_terminated_hex']==cstring(arm,storage).hex(),'current field')
    changed=bytearray(arm);slots=[]
    for pointer,at in OWNERS:
        # Stop at the new terminator; preserve every unread byte of the old slot.
        changed[at:at+len(NEW)]=NEW
        slots.append(dict(runtime_pointer=pointer,file_offset=at,original_complete_slot_hex=OLD.hex(),target_complete_slot_hex=bytes(changed[at:at+len(OLD)]).hex(),
            target_terminated_hex=NEW.hex(),untouched_old_tail_offset=at+len(NEW),untouched_old_tail_hex=OLD[len(NEW):].hex()))
    target=bytes(changed);parsed=MainCodeFile(target,BASE)
    require(len(target)==len(arm) and parsed.codeSettingsOffs==code.codeSettingsOffs,'file/header layout')
    for a,b in zip(code.sections,parsed.sections,strict=True):
        require((a.ramAddress,a.bssSize,a.implicit,len(a.data))==(b.ramAddress,b.bssSize,b.implicit,len(b.data)),'section/BSS shapes')
    require(bytes(code.sections[3].data[-48:])==bytes(parsed.sections[3].data[-48:]) and cache_plan(arm)==cache_plan(target),'copy/cache wrapper')
    require([struct.unpack_from('<3I',target,TABLE+i*32) for i in range(207)]==allfields,'all621 pointer values')
    restored=bytearray(target)
    for _,at in OWNERS:
        require(cstring(target,at)==NEW and target[at+len(NEW):at+len(OLD)]==arm[at+len(NEW):at+len(OLD)],'new terminator/unread tail')
        restored[at:at+len(OLD)]=OLD
    require(bytes(restored)==arm,'complete ARM9 inverse')
    differences=[i for i,(a,b) in enumerate(zip(arm,target,strict=True)) if a!=b]
    require(differences and all(any(at<=i<at+len(NEW) for _,at in OWNERS) for i in differences),'two owned prefix spans only')
    return target,dict(source_ARM9_sha256=sha(arm),target_ARM9_sha256=sha(target),actors=list(range(82,92)),literal_slots=slots,
        changed_byte_offsets=differences,all621_pointers_exact=True,only_ten_primary_fields_reference_complete_owners=True,no_interior_pointer=True,
        all_unowned_bytes_code_fonts_sections_BSS_cache_copy_and123264_extent_exact=True,all_unread_old_tail_bytes_preserved=True,complete_ARM9_inverse=True,
        native_shared_dynamic_macro_and_representative_display_validation_pending=True,no_release_or_completion_approval=True,full_goal_complete=False)
