"""Bind clean-only personal fields and original item97 while the current release builds."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,TABLE,cstring
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B233_clean_names_item_v7525');CONTEXT=Path('work/analysis/lil_B233_clean_context_v7524/all11_clean_legendary_chisel_paper_library_tools_joke_glosses_before_old_English.json');CATALOG=Path('translations/all_item_names_arm9_v1.json')
if __name__=='__main__':
    assert not ROOT.exists();context=read(CONTEXT);rom=Path('work/clean.nds');image=NdsImage.open(rom);arm=image.read_file('/__arm9__.bin');assert sha(rom.read_bytes())==context['source_ROM_sha256'] and sha(arm)==context['clean_ARM9_sha256'];rows=[]
    for actor in context['source_actor_selectors']:
        fields=[]
        for column in [0,4,8]:
            at=TABLE+actor*32+column;pointer=struct.unpack_from('<I',arm,at)[0];raw=cstring(arm,pointer-BASE) if pointer else bytes(1)
            fields.append(dict(column=column,pointer_field=at,source_pointer=pointer,source_storage_offset=pointer-BASE if pointer else None,source_terminated_hex=raw.hex(),Japanese=raw[:-1].decode('cp932'),source_null=pointer==0))
        rows.append(dict(source_selector=actor,fields=fields,actual_actor_resolution_voice_getters_anddisplay_not_yet_bound=True))
    r=next(r for r in read(CATALOG)['records'] if r['id']=='DK4_ITEM_POINTER_097');at=r['offset'];pointer=struct.unpack_from('<I',arm,at)[0];assert arm[at:at+4].hex()==r['source_hex'].lower();raw=cstring(arm,pointer-BASE);item=dict(record_ID=r['id'],pointer_field=at,source_pointer=pointer,source_storage_offset=pointer-BASE,source_terminated_hex=raw.hex(),Japanese=raw[:-1].decode('cp932'))
    assert bytes.fromhex(next(c for c in context['commands'] if c['word']==0xA000)['whole_command_hex'])==bytes.fromhex('00a0ffff61000110')
    ROOT.mkdir(parents=True);save(ROOT/'clean_personal_fields_anditem97_before_current_getters.json',dict(source_context=str(CONTEXT),source_context_sha256=sha(CONTEXT.read_bytes()),source_ROM=str(rom),source_ROM_sha256=sha(rom.read_bytes()),clean_ARM9_sha256=sha(arm),source_personal_fields=rows,source_named_item=item,original_A000_item_operand97_is_lead_not_complete_effect_interpretation=True,historical_sculptor_spelling_requires_source_identity_item_andreported_legend_context=True,no_new_current_English_getter_name_role_item_mechanic_orUI_approval=True,no_predecessor_story_English_exposed=True,new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [CONTEXT,CATALOG,Path(__file__)]},full_goal_complete=False));print(dict(source_fields=rows,source_item97=item,new_credit=0))
