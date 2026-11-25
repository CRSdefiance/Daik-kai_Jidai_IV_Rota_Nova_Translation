"""Bind the clean named artifact to the established item148 label,without reading current dialogue."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B48_artifact_identity_v8313')
ASSET=Path('translations/all_item_names_arm9_v1.json')
SOURCE=Path('work/analysis/Hodram_B48_clean_v8311/complete_clean_SC1_B48_EV1_andcoverage_before_current_English.json')
PARENT=Path('out/all_routes_combined_v8259_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists();asset,source=map(read,[ASSET,SOURCE]);record=next(r for r in asset['records'] if r['id']=='DK4_ITEM_POINTER_148')
    clean=NdsImage.open('work/clean.nds');current=NdsImage.open(PARENT);ja,en=clean.read_file('/__arm9__.bin'),current.read_file('/__arm9__.bin')
    assert sha(Path('work/clean.nds').read_bytes())==source['source_ROM_sha256'] and sha(PARENT.read_bytes())=='a3f11bad910fd7ffa2ba87fc85d82caeb5025b1863da7a2a1405725ff94ec42f'
    at=record['offset'];assert at==1175536 and ja[at:at+4]==bytes.fromhex(record['source_hex']) and en[at:at+4]==bytes.fromhex(record['replacement_hex'])
    fields=[]
    for version,arm in [('clean',ja),('current',en)]:
        pointer=int.from_bytes(arm[at:at+4],'little');offset=pointer-0x02000000;assert 0<=offset<len(arm)
        end=arm.index(0,offset);raw=arm[offset:end]
        fields.append(dict(version=version,metadata_field=at,metadata_pointer_hex=arm[at:at+4].hex(),name_pointer=pointer,name_offset=offset,
            complete_name_hex=raw.hex(),terminated_hex=arm[offset:end+1].hex(),text=raw.decode('cp932')))
    assert fields[0]['text']=='狩猟神ウルの弓矢' and fields[1]['text']==record['english']=="Ullr's Bow"
    assert ja[at+4:at+24]==en[at+4:at+24]
    notice=source['groups'][0]['records'][0];assert notice['source_selector']==254 and '『'+fields[0]['text']+'』' in notice['source_Japanese']
    ROOT.mkdir(parents=True);save(ROOT/'clean_notice_anditem148_established_Ullr_Bow_identity_not_current_dialogue_review.json',dict(
        source_notice=notice,artifact_item_ID=148,registered_asset_record=record,source_current_native_fields=fields,
        all20_nonname_metadata_bytes_unchanged=True,source_named_artifact_anditem148_label_concordant=True,
        established_English_name="Ullr's Bow",no_new_name_asset_orofficial_Latin_canon_claim=True,
        source_hunting_deity_identity_andbow_reference_preserved_inclean_gloss=True,
        current_B47_B48_English_dialogue_bodies_unconsulted=True,complete_source_controls_FE_geometry_FI_music_note_actual_scene_andlocalization_approval_pending=True,
        no_player_item_acquisition_transfer_quest_outcome_orevent_eligibility_inferred=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [ASSET,SOURCE,PARENT,Path(__file__)]}))
    print('B48 artifact identity:clean狩猟神ウルの弓矢=item148/currentcomplete Ullr\'s Bow;only name asset consulted,not currentdialogue.No newasset orcredit.')
