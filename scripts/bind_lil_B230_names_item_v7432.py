"""Bind source personal fields andthe exact item name;keep the untranslated catalogue middle field open."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,POOL,TABLE,cstring
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B230_name_item_v7432');SOURCE=Path('work/analysis/lil_B230_source_v7428/seventeen_clean_current_phoenix_bascinet_callback_source_references.json');CURRENT=Path('work/analysis/lil_B230_consumers_v7429/seventeen_effective_bodies34_dispatches_two_actors_four_name_consumers.json');CATALOG=Path('translations/all_item_names_arm9_v1.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,consumer,cat=map(read,[SOURCE,CURRENT,CATALOG]);assert consumer['source_context_sha256']==sha(SOURCE.read_bytes());forms={(r['actor_ID'],r['consumer']):r['text'] for r in consumer['native_four_distinct_name_consumers']['rows']}
    assert forms=={(2,'progressive-nameplate'):'Lil Argot',(2,'full-catalogue'):'Lil Argot',(22,'progressive-nameplate'):'Samwell Khan',(22,'full-catalogue'):'Samwell ダ Khan'}
    clean,current=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]];jp,arm=[im.read_file('/__arm9__.bin') for im in [clean,current]];payload=bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]);assert len(payload)==123264;found=[]
    for row in cat['records']:
        if not str(row.get('id','')).startswith('DK4_ITEM_POINTER_'):continue
        at=row['offset'];sp=struct.unpack_from('<I',jp,at)[0];assert jp[at:at+4].hex()==row['source_hex'].lower();raw=cstring(jp,sp-BASE)
        if raw[:-1].decode('cp932')!='不死鳥のバシネット':continue
        cp=struct.unpack_from('<I',arm,at)[0]
        if POOL<=cp<POOL+len(payload):value=cstring(payload,cp-POOL);storage='verified-current-staged-payload';offset=cp-POOL
        else:value=cstring(arm,cp-BASE);storage='static-current-ARM9';offset=cp-BASE
        assert value==b'Phoenix Bascinet\0'
        found.append(dict(record_ID=row['id'],pointer_field=at,source_pointer=sp,source_storage_offset=sp-BASE,source_terminated_hex=raw.hex(),Japanese=raw[:-1].decode('cp932'),current_pointer=cp,current_storage_kind=storage,current_storage_offset=offset,current_terminated_hex=value.hex(),English=value[:-1].decode('cp932'),legacy_registered_English=row['english'],legacy_registered_pointer_hex=row.get('replacement_hex'),current_native_item_getter_card_bounds_and_all_other_consumers_not_reviewed_here=True))
    assert len(found)==1;samwell=next(r for r in consumer['source_name_fields'] if r['actor_ID']==22);middle=next(r for r in samwell['fields'] if r['column']==8);assert middle['Japanese']==middle['current_English']=='ダ' and middle['source_terminated_hex']==middle['current_terminated_hex']=='835f00';aliases=[]
    for actor in range(207):
        for column in [0,4,8]:
            at=TABLE+actor*32+column;pointer=struct.unpack_from('<I',arm,at)[0]
            if pointer==middle['current_pointer']:aliases.append(dict(actor_ID=actor,column=column,pointer_field=at))
    ROOT.mkdir(parents=True);save(ROOT/'two_progressive_names_exact_phoenix_bascinet_item_andunapproved_catalogue_middle.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),consumer_proof=str(CURRENT),consumer_proof_sha256=sha(CURRENT.read_bytes()),actors=[dict(actor_ID=i,source_fields=next(r['fields'] for r in consumer['source_name_fields'] if r['actor_ID']==i),progressive=forms[i,'progressive-nameplate'],catalogue=forms[i,'full-catalogue']) for i in [2,22]],source_named_item=found[0],registered_item_batch=str(CATALOG),registered_item_batch_sha256=sha(CATALOG.read_bytes()),current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],current_ARM9_sha256=sha(arm),Samwell_middle_field=middle,all_current_actor_primary_secondary_middle_pointer_aliases=aliases,Samwell_progressive_getter_omits_middle_full_getter_includes_it=True,Samwell_mixed_Japanese_full_catalogue_wording_not_editorially_approved=True,source_bound_da_romanization_candidate_for_later_consumer_andasset_review='da',candidate_spelling_not_shipped_or_globally_approved=True,source_named_helmet_not_runtime_FI_substitution=True,current_Phoenix_Bascinet_asset_andreported_iron_flame_forging_anduncertain_name_bound=True,older_dialogue_Phoenix_Bascinet_name_matches_exact_registered_item=True,no_item_or_actor_asset_change_or_duplicate_credit=True,no_inventory_card_orcomplete_item_mechanic_approval=True,full207_name_role_alias_andSamwell_middle_consumer_review_remains_open=True,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CURRENT,CATALOG,Path(__file__)]},new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print(dict(item=found[0],Samwell_middle_current='ダ',Samwell_catalogue_current='Samwell ダ Khan',middle_aliases=aliases,full_catalogue_wording_approved=False,new_credit=0))
