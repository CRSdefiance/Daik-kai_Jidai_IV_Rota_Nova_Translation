"""Source-bound owned-prefix item116 data transform;research until release gates pass."""
import struct
from ndspy.code import MainCodeFile
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,POOL,TABLE,cstring
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.grand_race_menu_release import sha
SOURCE='bceb685cd92f2ecf26746999fc7fc5e3c0a82b681f269d4e8a00044bb234360e'
FIELD=0x11E210+116*24
STORAGE=0x15E890
OLD=b'Orca Figurehead\0'
NEW=b'Shachihoko\0'

def require(value,message):
    if not value:raise ValueError('Shachihoko item116: '+message)

def transform(source,clean,row):
    require(sha(source)==SOURCE,'exact current ARM9 required')
    require(row['item_ID']==116 and row['source_Japanese']=='鯱の像' and row['current_English']=='Orca Figurehead' and row['english']=='Shachihoko','exact reviewed identity/title required')
    require(row['translation_policy']=='natural-dialogue-v2' and row['target_locale']=='en-US','v2 American localization required')
    require(all(row['review'][k] is True for k in ['source','context','localization','naturalness']),'complete source/context/prose gates required')
    sp=struct.unpack_from('<I',clean,FIELD)[0];pointer=struct.unpack_from('<I',source,FIELD)[0]
    require(cstring(clean,sp-BASE)[:-1].decode('cp932')=='鯱の像','clean title differs')
    require(row['source_reference']==dict(file_path='/__arm9__.bin',pointer_field=FIELD,pointer=sp,terminated_hex=cstring(clean,sp-BASE).hex(),whole24byte_row_hex=clean[FIELD:FIELD+24].hex()),'exact clean row required')
    require(pointer==BASE+STORAGE and cstring(source,STORAGE)==OLD and source[STORAGE-1]==0,'complete current owned static string differs')
    require(row['current_reference']==dict(file_path='/__arm9__.bin',pointer_field=FIELD,pointer=pointer,file_offset=STORAGE,terminated_hex=OLD.hex()),'exact current owner required')
    require(len(NEW)<=len(OLD) and not any(c in NEW[:-1] for c in b'%\r\n') and all(32<=c<127 for c in NEW[:-1]),'safe complete ASCII prefix required')
    require([i for i in range(len(source)-3) if source[i:i+4]==struct.pack('<I',pointer)]==[FIELD],'unclassified literal pointer alias')
    aliases=[]
    for ident in range(218):
        f=0x11E210+ident*24;p=struct.unpack_from('<I',source,f)[0]
        if pointer<=p<pointer+len(OLD):aliases.append((ident,f,p))
    require(aliases==[(116,FIELD,pointer)],'shared/interior item-table pointer')
    require(not any(pointer<=p<pointer+len(OLD) for i in range(207) for p in struct.unpack_from('<3I',source,TABLE+i*32)),'actor name alias')
    saved=source[:STORAGE]+NEW+source[STORAGE+len(NEW):]
    require(len(saved)==len(source) and saved[STORAGE+len(NEW):STORAGE+len(OLD)]==source[STORAGE+len(NEW):STORAGE+len(OLD)],'unread tail or extent changed')
    require(saved[:STORAGE]+source[STORAGE:STORAGE+len(NEW)]+saved[STORAGE+len(NEW):]==source,'exact inverse failed')
    before,after=[MainCodeFile(a,BASE).sections for a in [source,saved]]
    require(len(before)==len(after)==5,'decoded section count differs')
    for a,b in zip(before,after,strict=True):require((a.ramAddress,a.bssSize,len(a.data))==(b.ramAddress,b.bssSize,len(b.data)),'section metadata/extent changed')
    require(bytes(before[3].data)==bytes(after[3].data) and len(before[3].data)==123088,'staged pool/copy wrapper changed')
    require(cache_plan(source)==cache_plan(saved),'startup/cache contract changed')
    require(saved[0x11E210:0x11E210+218*24]==source[0x11E210:0x11E210+218*24] and saved[TABLE:TABLE+207*32]==source[TABLE:TABLE+207*32],'item or actor table changed')
    return saved,dict(source_ARM9_sha256=sha(source),target_ARM9_sha256=sha(saved),item_ID=116,source_Japanese='鯱の像',before='Orca Figurehead',after='Shachihoko',
        pointer_field=FIELD,runtime_pointer=pointer,owned_file_offset=STORAGE,owned_terminated_capacity=len(OLD),written_prefix_bytes=len(NEW),
        old_terminated_hex=OLD.hex(),new_terminated_hex=NEW.hex(),all_unread_old_tail_bytes_preserved=True,
        all218_item_rows_and207_actor_rows_code_pointers_font_graphics_and_staged123040_plus48_bytes_preserved=True,
        exact_inverse_and_all_unowned_serialized_bytes_preserved=True,no_global_substitution=True,no_ROM_mutation_performed=True,
        native_consumers_glyphs_gameplay_and_registered_release_pending=True,full_goal_complete=False)
