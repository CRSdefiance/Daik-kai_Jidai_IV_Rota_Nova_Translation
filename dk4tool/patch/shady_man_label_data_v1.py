"""Exact in-place primary-label data transform;no code,pointer,allocation or prose rewrite."""
import struct
from ndspy.code import MainCodeFile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
BASE,POOL,STAGE=0x02000000,0x02387A20,0x023A7200
TABLE=0x120B80
SOURCE='03a905a9e4a4df117b8a4b5280ec3c669a4db00547972397413bc8bebc4afbbd'
EXPECTED={173:('怪しい人','Suspicious Person','Shady Man')}

def require(value,message):
    if not value:raise ValueError('Shady Man label '+message)

def cstring(data,at):
    require(0<=at<len(data),'string address outside owned storage')
    end=data.find(b'\0',at);require(end>=at,'complete terminated string required');return data[at:end+1]

def transform(source,clean,rows):
    require(sha(source)==SOURCE,'exact current ARM9 required')
    require(len(rows)==1 and [r['actor_ID'] for r in rows]==[173],'one exact source-owned actor required')
    code=MainCodeFile(source,BASE);require(len(code.sections)==5 and code.sections[3].ramAddress==STAGE,'current decoded section layout differs')
    payload=bytes(code.sections[3].data[:-48]);require(len(payload)==123264 and source.count(payload)==1,'complete unique current staged payload required')
    raw_at=source.index(payload);target=bytearray(source);changes=[];spans=[]
    all_fields=[struct.unpack_from('<3I',source,TABLE+i*32) for i in range(207)]
    for row in rows:
        ident=row['actor_ID'];japanese,current,english=EXPECTED[ident];field=TABLE+ident*32;pointer=all_fields[ident][0]
        require(row['source_Japanese']==japanese and row['current_English']==current and row['english']==english,'reviewed label wording differs')
        require(all(row['review'][g] for g in ['source','context','localization','naturalness']),'complete contextual prose gates required')
        require(row['editorial_decision']=='revise' and row['target_locale']=='en-US' and row['localization_note'],'contextual label revision required')
        require(row['source_reference']['pointer_field']==field and row['source_reference']['source_file']=='/__arm9__.bin','source primary field differs')
        source_pointer=struct.unpack_from('<I',clean,field)[0];original=cstring(clean,source_pointer-BASE)
        require(original[:-1].decode('cp932')==japanese and row['source_reference']['pointer']==source_pointer
            and row['source_reference']['terminated_hex']==original.hex(),'exact clean primary label differs')
        require(len(row['all_three_source_name_fields'])==3,'all clean primary/secondary/middle fields required')
        for delta,part in zip([0,4,8],row['all_three_source_name_fields'],strict=True):
            p=struct.unpack_from('<I',clean,field+delta)[0]
            require(part['pointer_field']==field+delta and part.get('pointer',0)==p,'clean name metadata ownership differs')
            if p:require(part['terminated_hex']==cstring(clean,p-BASE).hex(),'clean name metadata bytes differ')
            else:require(part['null'],'clean null field differs')
        at=pointer-POOL;old=current.encode('ascii')+b'\0';new=english.encode('ascii')+b'\0'
        require(0<=at and at+len(old)<=len(payload) and payload[at:at+len(old)]==old,'current owned staged label differs')
        require(len(new)<=len(old) and len(new)>1 and all(32<=b<127 for b in new[:-1]),'complete safe ASCII target must fit old owned label')
        require(not any(p in new for p in [b'%',b'FI',b'FA',b'FO',b'FU',b'\n',b'\r']),'label may not introduce format or substitution syntax')
        hits=[i for i in range(len(source)-3) if source[i:i+4]==struct.pack('<I',pointer)]
        require(hits==[field],'unclassified literal ARM9 pointer owner')
        aliases=[dict(actor_ID=i,pointer_field=TABLE+i*32+d,pointer=p,interior_delta=p-pointer)
            for i,parts in enumerate(all_fields) for d,p in zip([0,4,8],parts,strict=True) if pointer<=p<pointer+len(old)]
        require(aliases==[dict(actor_ID=ident,pointer_field=field,pointer=pointer,interior_delta=0)],'shared or interior primary/secondary/middle alias')
        reference=row['current_reference']
        require(reference['pointer_field']==field and reference['runtime_pointer']==pointer and reference['staged_payload_offset']==at
            and reference['file_offset']==raw_at+at and reference['terminated_hex']==old.hex(),'exact current reference differs')
        start=raw_at+at;require(all(start+len(new)<=a or b<=start for a,b in spans),'overlapping owned target prefixes')
        target[start:start+len(new)]=new;spans.append((start,start+len(new)))
        require(target[start+len(new):start+len(old)]==source[start+len(new):start+len(old)],'unread old tail must remain exact')
        changes.append(dict(actor_ID=ident,source_Japanese=japanese,before=current,after=english,pointer_field=field,runtime_pointer=pointer,
            file_offset=start,staged_payload_offset=at,old_terminated_hex=old.hex(),new_terminated_hex=new.hex(),
            owned_capacity=len(old),written_prefix_bytes=len(new),literal_pointer_occurrences=hits,all207_name_field_aliases=aliases,
            all_unread_tail_bytes_preserved=True))
    saved=bytes(target);parsed=MainCodeFile(saved,BASE)
    require(len(saved)==len(source) and len(parsed.sections)==len(code.sections),'ARM9/section extent changed')
    for index,(a,b) in enumerate(zip(code.sections,parsed.sections,strict=True)):
        require((a.ramAddress,a.bssSize,len(a.data))==(b.ramAddress,b.bssSize,len(b.data)),'decoded section metadata changed')
        if index!=3:require(bytes(a.data)==bytes(b.data),'unrelated code/data/ITCM/DTCM section changed')
    require(bytes(parsed.sections[3].data[-48:])==bytes(code.sections[3].data[-48:]),'pool copy/cache wrapper changed')
    require(cache_plan(source)==cache_plan(saved),'startup cache/arena/copy contract changed')
    require([struct.unpack_from('<3I',saved,TABLE+i*32) for i in range(207)]==all_fields,'one of621 name-table fields changed')
    restore=bytearray(saved)
    for a,b in spans:restore[a:b]=source[a:b]
    require(bytes(restore)==source,'unrelated serialized ARM9 bytes changed')
    require([cstring(bytes(parsed.sections[3].data[:-48]),r['staged_payload_offset']).decode('ascii')[:-1] for r in changes]==['Shady Man'],'complete target strings differ')
    return saved,dict(source_ARM9_sha256=sha(source),target_ARM9_sha256=sha(saved),changes=changes,
        exact_621_name_table_pointers_and_all_source_secondary_middle_fields_preserved=True,
        original_five_decoded_sections_extents_BSS_and_all_unowned_bytes_exact=True,
        original123264_payload_extent_and_final48_byte_copy_wrapper_exact=True,
        only_one_owned_ASCII_prefix_changed_no_global_substitution=True,no_ROM_image_mutation_performed=True,
        native_target_getters_glyphs_substitutions_representative_and_registered_release_pending=True,full_goal_complete=False)
