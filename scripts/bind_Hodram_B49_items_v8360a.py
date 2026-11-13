"""Bind the clean trade's two item names to existing native assets, without consulting current dialogue."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_item_identity_v8360a')
ASSET=Path('translations/all_item_names_arm9_v1.json')
SOURCE=Path('work/analysis/Hodram_B49_clean_gloss_v8358/fourteen_first_clean_glosses_two_choice_labels_wristband_trade_direction_andqualified_Hodram_reply.json')
PARENT=Path('out/all_routes_combined_v8300_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists();asset,source=map(read,[ASSET,SOURCE]);clean=NdsImage.open('work/clean.nds');current=NdsImage.open(PARENT);ja,en=clean.read_file('/__arm9__.bin'),current.read_file('/__arm9__.bin');release=read('work/analysis/Hodram_three_blocks_release_v8301/registered_release_verification.json')
    assert sha(PARENT.read_bytes())==release['candidate_sha256'] and sha(en)==release['ARM9_sha256'];items=[]
    for number,wantedja,wanteden in [(84,'天佑のリストバンド','Heavenly Wristband'),(148,'狩猟神ウルの弓矢',"Ullr's Bow")]:
        record=next(r for r in asset['records'] if r['id']==f'DK4_ITEM_POINTER_{number:03d}');at=record['offset'];assert ja[at:at+4]==bytes.fromhex(record['source_hex']) and en[at:at+4]==bytes.fromhex(record['replacement_hex']);fields=[]
        for label,code in [('clean_Japanese',ja),('registered_current',en)]:
            pointer=int.from_bytes(code[at:at+4],'little');start=pointer-0x02000000;assert 0<=start<len(code);end=code.index(0,start);raw=code[start:end]
            fields.append(dict(version=label,metadata_field=at,metadata_pointer_hex=code[at:at+4].hex(),name_pointer=pointer,name_offset=start,bytes=end-start,complete_name_hex=raw.hex(),terminated_hex=code[start:end+1].hex(),text=raw.decode('cp932')))
        assert [f['text'] for f in fields]==[wantedja,wanteden] and record['english']==wanteden and ja[at+4:at+24]==en[at+4:at+24]
        items.append(dict(item_ID=number,registered_asset_record=record,source_current_native_fields=fields,all20_nonname_metadata_bytes_unchanged=True,established_English_name=wanteden))
    rows=source['groups'][0]['records'];notice=next(r for r in rows if r['source_record_index']==81);spoken=next(r for r in rows if r['source_record_index']==22)
    assert notice['source_selector']==254 and '『天佑のリストバンド』を渡しました'==notice['source_Japanese'] and '『てんゆーのリストバンド』' in spoken['source_Japanese']
    ROOT.mkdir(parents=True);save(ROOT/'clean_trade_item84_Heavenly_Wristband_item148_Ullr_Bow_exact_native_name_fields.json',dict(source_first_gloss=str(SOURCE),source_first_gloss_sha256=sha(SOURCE.read_bytes()),registered_parent=str(PARENT),registered_parent_sha256=sha(PARENT.read_bytes()),current_ARM9_sha256=sha(en),items=items,source_phonetic_spoken_title=spoken['source_Japanese'],source_formal_FE_notice=notice['source_Japanese'],source_notice_reports_outgoing_wristband_not_receipt=True,no_new_item_name_asset_mechanics_rank_quest_location_orevent_eligibility_claim=True,current_B49_English_dialogue_bodies_still_unconsulted=True,full_source_control_choice_effects_FE_native_actual_localization_andrelease_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [ASSET,SOURCE,PARENT,Path(__file__)]}))
    print('B49 itemidentity:84HeavenlyWristband/148UllrBow,exact source/current nativepointers/fullNUL names/20unowned metadata bytes;FEhands overwristband.Currentdialogue still unread;no credit.')
