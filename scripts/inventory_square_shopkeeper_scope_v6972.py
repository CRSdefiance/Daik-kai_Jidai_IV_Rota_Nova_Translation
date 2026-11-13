"""Expand the existing role lead to ten source-identical actors and every raw story consumer."""
import struct
from collections import Counter
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,POOL,TABLE,cstring
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/square_shopkeeper_scope_v6972');CURRENT=Path('work/analysis/editorial_handoff_verification_v6962/verified_handoff.json');SOURCE_CONTEXT=Path('work/analysis/lil_B221_clean_context_v6965/all14_clean_speeches_two_choice_labels_Crusades_Saladin_glosses_before_old_English.json')
if __name__=='__main__':
    assert not ROOT.exists();v=read(CURRENT);clean,current=[NdsImage.open(p) for p in ['work/clean.nds',v['candidate']]];assert sha(Path(v['candidate']).read_bytes())==v['candidate_sha256'];jp,arm=[im.read_file('/__arm9__.bin') for im in [clean,current]];payload=bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]);assert len(payload)==123264 and arm.count(payload)==1;payload_at=arm.index(payload);actors=[];allfields=[]
    for ident in range(207):
        fields=[]
        for delta in [0,4,8]:
            at=TABLE+ident*32+delta;sp,cp=[struct.unpack_from('<I',a,at)[0] for a in [jp,arm]];assert bool(sp)==bool(cp)
            if not sp:fields.append(dict(column=delta,pointer_field=at,source_null=True,current_null=True));continue
            raw=cstring(jp,sp-BASE);storage=payload_at+cp-POOL if POOL<=cp<POOL+len(payload) else cp-BASE;value=cstring(arm,storage);field=dict(actor_ID=ident,column=delta,pointer_field=at,source_pointer=sp,source_storage_offset=sp-BASE,source_terminated_hex=raw.hex(),Japanese=raw[:-1].decode('cp932'),current_pointer=cp,current_storage_offset=storage,current_terminated_hex=value.hex(),current_English=value[:-1].decode('cp932'));fields.append(field);allfields.append(field)
        if fields[0].get('Japanese')=='広場の店主':actors.append(dict(actor_ID=ident,fields=fields))
    ids=[r['actor_ID'] for r in actors];assert ids==list(range(82,92));owners={(r['fields'][0]['current_pointer'],r['fields'][0]['current_storage_offset'],r['fields'][0]['current_terminated_hex']) for r in actors};ranges=[dict(pointer=p,file_offset=o,bytes=len(bytes.fromhex(h)),terminated_hex=h) for p,o,h in sorted(owners)];aliases=[]
    for f in allfields:
        for owner in ranges:
            if owner['pointer']<=f['current_pointer']<owner['pointer']+owner['bytes']:aliases.append(dict(actor_ID=f['actor_ID'],column=f['column'],pointer_field=f['pointer_field'],pointer=f['current_pointer'],interior_delta=f['current_pointer']-owner['pointer']))
    pointer_hits=[]
    for owner in ranges:
        needle=struct.pack('<I',owner['pointer'])
        for name,data in [('ARM9',arm),*[(name,data) for name,data in current.iter_components() if name!='/__arm9__.bin']]:
            at=data.find(needle)
            while at>=0:pointer_hits.append(dict(owner_pointer=owner['pointer'],component=name,offset=at));at=data.find(needle,at+1)
    inventory,_,_=scoped_inventory();hits=[];contexts=[]
    for route in range(4):
        path=f'/data/SC{route}.DK4';source_bank,target_bank=[IlnkContainer.parse(im.read_file(path)).blocks for im in [clean,current]]
        for number,block in enumerate(source_bank):
            found=[]
            for ident in ids:
                needle=bytes.fromhex('0040ffff00')+bytes([ident]);at=block.find(needle)
                while at>=0:found.append((at,ident));at=block.find(needle,at+1)
            if not found:continue
            commands,speeches=inventory(jp,block);selected={c['offset']:c for c in speeches};transcript=[]
            for speech in speeches:
                at=speech['offset']+5;end=block.index(0,at+1);raw=block[at:end];transcript.append(dict(source_reference=dict(block=number,offset=at,bytes=len(raw),record_index=block[:at].count(b'\0'),header_offset=at-5),source_selector=raw[0],source_hex=raw.hex(),Japanese=raw[1:].decode('cp932'),ancestor_0100_offsets=speech['ancestor_0100_offsets']))
            for at,ident in sorted(found):
                assert at in selected;end=block.index(0,at+6);raw=block[at+5:end];hits.append(dict(file_path=path,block=number,header_offset=at,source_selector=ident,source_hex=raw.hex(),Japanese=raw[1:].decode('cp932'),current_same_position_preamble_hex=target_bank[number][at:at+6].hex(),current_position_not_assumed_valid_after_prior_relocation=True))
            contexts.append(dict(file_path=path,block=number,source_block_sha256=sha(block),source_block_hex=block.hex(),all_clean_commands=commands,whole_clean_transcript=transcript,no_predecessor_English_prose_read=True,role_name_localization_context_review_pending=True))
    ROOT.mkdir(parents=True);save(ROOT/'ten_source_identical_roles_current_owners_alias_fields_and_whole_clean_story_contexts.json',dict(current_ROM=v['candidate'],current_ROM_sha256=v['candidate_sha256'],current_ARM9_sha256=sha(arm),clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),actors=actors,current_literal_owners=ranges,all621_name_pointer_fields_examined=True,current_declared_name_field_aliases=aliases,raw_pointer_hits_in_ARM9_and_components=pointer_hits,raw_static_story_preamble_hits=hits,story_contexts=contexts,raw_static_story_hit_count=len(hits),source_role_actor_hit_counts=dict(Counter(r['source_selector'] for r in hits)),source_context_count=len(contexts),dynamic_shared_COMMON_ui_macros_pair_names_and_remaining_native_callers_still_require_binding=True,raw_story_hits_not_closed_global_consumer_census=True,Shopkeeper_candidate_not_approved_or_integrated=True,no_region_gender_rank_or_biography_metadata_appended=True,no_ROM_asset_or_prose_change_and_no_review_credit=True,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,SOURCE_CONTEXT,Path(__file__)]},full_goal_complete=False));print(dict(actors=ids,owners=ranges,declared_alias_fields=aliases,raw_story_hits=len(hits),contexts=len(contexts),hit_counts=dict(Counter(r['source_selector'] for r in hits)),closed_consumer_census=False,credit=0))
