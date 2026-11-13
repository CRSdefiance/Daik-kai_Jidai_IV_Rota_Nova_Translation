"""Keep clean name fields and distinct current name consumers source-bound."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,POOL,TABLE,cstring
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B206_source_names_v6235')
SOURCE=Path('work/analysis/lil_B206_source_v6232/all28_clean_current_complete_context_with_four_choice_labels.json')
NAMES=Path('work/analysis/lil_B206_names_v6234/six_original_progressive_and_catalogue_name_consumers.json')
VOICE=Path('work/analysis/lil_B206_voices_v6233/current207_catalog_eight_voices_and_three_source_selectors.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,native,voices=map(read,[SOURCE,NAMES,VOICE])
    clean,current=[NdsImage.open(p).read_file('/__arm9__.bin') for p in ['work/clean.nds',packet['current_ROM']]]
    payload=bytes(MainCodeFile(current,BASE).sections[3].data[:-48]);assert len(payload)==123264 and current.count(payload)==1
    payload_at=current.index(payload);rows=[]
    for ident in [2,7,173]:
        fields=[]
        for delta in [0,4,8]:
            field=TABLE+ident*32+delta;sp,cp=[struct.unpack_from('<I',a,field)[0] for a in [clean,current]];assert bool(sp)==bool(cp)
            if not sp:fields.append(dict(field=field,column=delta,source_null=True,current_null=True));continue
            src=cstring(clean,sp-BASE)
            if POOL<=cp<POOL+len(payload):
                off=cp-POOL;value=cstring(payload,off);current_offset=payload_at+off;storage='verified-staged-payload'
            else:current_offset=cp-BASE;value=cstring(current,current_offset);storage='original-static-ARM9'
            fields.append(dict(pointer_field=field,column=delta,source_pointer=sp,source_storage_offset=sp-BASE,source_terminated_hex=src.hex(),Japanese=src[:-1].decode('cp932'),current_pointer=cp,current_storage_offset=current_offset,current_storage=storage,current_terminated_hex=value.hex(),current_English=value[:-1].decode('cp932')))
        rows.append(dict(actor_ID=ident,fields=fields,progressive=native['progressive_nameplate_values'][str(ident)],catalogue=native['full_catalogue_values'][str(ident)],voice=next(r['original_voice_class'] for r in voices['fresh3_actor_names']['rows'] if r['actor_ID']==ident)))
    ROOT.mkdir(parents=True)
    save(ROOT/'three_exact_source_name_fields_voices_and_distinct_name_consumers.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_name_fields=rows,
        name_wording_decisions_pending_exact_source_field_and_scene_review=True,
        no_name_asset_or_runtime_change=True,no_global_207_name_closure_or_new_name_completion_credit=True,
        current_native_getters_not_actual_B206_speech_or_nameplate_observation=True,
        whole_exchange_clean_gloss_precedes_current_prose_comparison=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,VOICE,Path(__file__)]},new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    for r in rows:print(r['actor_ID'],[(f.get('Japanese'),f.get('current_English')) for f in r['fields']],r['progressive'],r['catalogue'],r['voice'])
