"""Produce/pin an explicitly provisional source-owned title research ROM."""
import json,os,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,cstring
from dk4tool.patch.shachihoko_item_name_data_v1 import FIELD,STORAGE,OLD,NEW,transform
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_item_name_research_v6079')
SOURCE=Path('work/analysis/shachihoko_source_context_v6075/four_complete_clean_exchanges_and_two_nonitem_sobriquet_contexts.json')
ITEM=Path('work/analysis/lil_B204_item_fields_v6073/clean_item116_current_name_and_original_picture_descriptor.json')
ROM=Path('out/shachihoko_item_name_v6079_RESEARCH_ONLY.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();context,item=map(read,[SOURCE,ITEM]);parent_path=Path(item['candidate']);assert sha(parent_path.read_bytes())==item['candidate_sha256']
    parent,clean=NdsImage.open(parent_path),NdsImage.open('work/clean.nds');arm=parent.read_file('/__arm9__.bin');original=clean.read_file('/__arm9__.bin')
    batchpath=Path('translations/all_item_names_arm9_v1.json');batch=read(batchpath);storage=next(r for r in batch['records'] if r['id']=='DK4_ITEM_NAME_STORAGE_15E890');ptr=next(r for r in batch['records'] if r['id']=='DK4_ITEM_POINTER_116')
    assert storage['offset']==STORAGE and arm[STORAGE:STORAGE+len(bytes.fromhex(storage['replacement_hex']))]==bytes.fromhex(storage['replacement_hex']) and bytes.fromhex(ptr['replacement_hex'])==arm[FIELD:FIELD+4]
    sp=struct.unpack_from('<I',original,FIELD)[0];cp=struct.unpack_from('<I',arm,FIELD)[0]
    row=dict(id='ITEM_116_CULTURAL_NAME',item_ID=116,source_Japanese='鯱の像',current_English='Orca Figurehead',english='Shachihoko',translation_policy='natural-dialogue-v2',target_locale='en-US',
        source_reference=dict(file_path='/__arm9__.bin',pointer_field=FIELD,pointer=sp,terminated_hex=cstring(original,sp-BASE).hex(),whole24byte_row_hex=original[FIELD:FIELD+24].hex()),
        current_reference=dict(file_path='/__arm9__.bin',pointer_field=FIELD,pointer=cp,file_offset=STORAGE,terminated_hex=OLD.hex()),
        source_meaning='A shachi/shachihoko statue;the four complete castle exchanges explicitly name the missing ornament シャチホコ.',
        context=str(SOURCE),localization_note=context['provisional_localization_reason'],
        speaker='Shared item title,not Jam speaking',editorial_decision='revise',review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
        native_glyph_bounds_first_final_characters_consumers_gameplay_and_release_pending=True,new_dialogue_or_name_review_credit=0)
    target,plan=transform(arm,original,row);image=NdsImage.open(parent_path);image.replace_file('/__arm9__.bin',target);image.save(ROM);after=NdsImage.open(ROM)
    assert not [p for _,p,v in parent.iter_files() if after.read_file(p)!=v]
    assert [p for p,v in parent.iter_components() if after.read_file(p)!=v]==['/__arm9__.bin'] and after.read_file('/__arm9__.bin')==target
    ROOT.mkdir(parents=True);(ROOT/'target_ARM9.bin').write_bytes(target)
    save(ROOT/'provisional_item116_manuscript.json',dict(format='dk4-cultural-item-name-review-v1',source_ROM='work/clean.nds',current_ROM=str(parent_path),current_ROM_sha256=sha(parent_path.read_bytes()),
        records=[row],data_plan=plan,target_ARM9=str(ROOT/'target_ARM9.bin'),target_ARM9_sha256=sha(target),
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),all207_speaker_name_review_and_all_story_prose_scope_remain_open=True,
        no_native_formatting_or_registered_release_approval=True,new_review_credit=0,full_goal_complete=False))
    pins=Path('translations/rom_retention_pins.json');raw=pins.read_bytes();values=json.loads(raw);assert not any(Path(r['path']).resolve()==ROM.resolve() for r in values)
    added=dict(path=str(ROM.resolve()),reason='Provisional source-owned shachihoko item116 data-only research;native/display/release pending. Preserve every ROM. SHA256 '+sha(ROM.read_bytes()))
    encoded=(json.dumps(values+[added],ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8');(ROOT/'pins.before.json').write_bytes(raw);assert pins.read_bytes()==raw
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    save(ROOT/'research_image_receipt.json',dict(parent=str(parent_path),parent_sha256=sha(parent_path.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        target_ARM9_sha256=sha(target),changed_components=['/__arm9__.bin'],changed_files=[],data_plan=plan,
        original_item_name_batch=str(batchpath),original_item_name_batch_sha256=sha(batchpath.read_bytes()),original_storage_record=storage,original_pointer_record=ptr,
        all_story_UI_name_and_graphic_files_exact_to_V6050=True,not_registered_candidate_or_release_parent=True,
        native_consumers_glyphs_gameplay_and_registered_release_pending=True,new_pin=added,pins_before_sha256=sha(raw),pins_after_sha256=sha(encoded),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,ITEM,Path(__file__),Path('dk4tool/patch/shachihoko_item_name_data_v1.py')]},new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Item116 Shachihoko provisional research pinned;only owned terminated11-byte prefix changes;all files and other components exact. Native/display/release pending;zero credit.')
