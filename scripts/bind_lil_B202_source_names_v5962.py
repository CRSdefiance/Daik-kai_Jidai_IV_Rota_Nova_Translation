"""Keep clean name fields, source-defined sailor alias and current consumers distinct."""
import inspect,struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,POOL,TABLE,cstring
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.reconcile_lil_B156_actual_nameplate_v3737a import names
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B202_source_names_v5962')
SOURCE=Path('work/analysis/lil_B202_source_v5959/all19_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B202_names_v5961/eight_original_progressive_and_catalogue_name_consumers.json')
VOICE=Path('work/analysis/lil_B202_voices_v5960/current207_catalog_eight_voices_and_four_source_selectors.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,native,voices=map(read,[SOURCE,NAMES,VOICE]);clean,current=[NdsImage.open(p).read_file('/__arm9__.bin') for p in ['work/clean.nds',packet['current_ROM']]]
    assert current[0x7ED88:0x7EDD4]==clean[0x7ED88:0x7EDD4] and current[0x541C0:0x541C8]==clean[0x541C0:0x541C8]
    payload=bytes(MainCodeFile(current,BASE).sections[3].data[:-48]);assert len(payload)==123040 and current.count(payload)==1;payload_at=current.index(payload);rows=[]
    for ident in [2,18,147,157]:
        fields=[]
        for delta in [0,4,8]:
            field=TABLE+ident*32+delta;sp,cp=[struct.unpack_from('<I',a,field)[0] for a in [clean,current]]
            assert bool(sp)==bool(cp)
            if not sp:fields.append(dict(field=field,column=delta,source_null=True,current_null=True));continue
            src=cstring(clean,sp-BASE)
            if POOL<=cp<POOL+len(payload):off=cp-POOL;value=cstring(payload,off);current_offset=payload_at+off;storage='verified-staged-payload'
            else:current_offset=cp-BASE;value=cstring(current,current_offset);storage='original-static-ARM9'
            fields.append(dict(pointer_field=field,column=delta,source_pointer=sp,source_storage_offset=sp-BASE,source_terminated_hex=src.hex(),Japanese=src[:-1].decode('cp932'),current_pointer=cp,current_storage_offset=current_offset,current_storage=storage,current_terminated_hex=value.hex(),current_English=value[:-1].decode('cp932')))
        rows.append(dict(actor_ID=ident,fields=fields,progressive=native['progressive_nameplate_values'][str(ident)],catalogue=native['full_catalogue_values'][str(ident)],voice=next(r['original_voice_class'] for r in voices['fresh4_actor_names']['rows'] if r['actor_ID']==ident)))
    pointer=struct.unpack_from('<I',current,0x7EDD0)[0];assert pointer==struct.unpack_from('<I',clean,0x7EDD0)[0];at=pointer-BASE;source_alias=cstring(clean,at);target_alias=cstring(current,at)
    assert source_alias[:-1].decode('cp932')=='水夫' and target_alias==b'Sailor\0'
    adapter=checked_text(inspect.getsource(names),{'[150,151,152,159,160]':'[150,151,152,157,159,160]'})
    env=dict(names.__globals__);exec(compile(adapter,__file__+'::source-alias-borders-and-selected-actor','exec'),env)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B202_voices_v5960/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context');cases=ctx.execute(env['names']);ctx.machines.pop();assert not ctx.machines and len(cases['rows'])==6
    assert next(r['nameplate_text'] for r in cases['rows'] if r['actor_ID']==157)=='Sailor'
    save(ROOT/'four_exact_source_name_fields_voices_and_original_Sailor_alias.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_name_fields=rows,
        original_progressive_alias=dict(source='水夫',source_terminated_hex=source_alias.hex(),current='Sailor',current_terminated_hex=target_alias.hex(),pointer_field=0x7EDD0,pointer=pointer,storage_offset=at,original_inclusive_actor_range=[151,159],selected_actor=157,source_same_getter_code_sha256=sha(current[0x7ED88:0x7EDD4]),source_same_progressive_callsite=0x020541C4),
        six_fresh_alias_border_and_selected_actor_consumers=cases,source_owned_alias_adapter=adapter,current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        contextual_name_decisions={
         '2':'Retain Lil Argot in both consumers and Lil in speech;the source first/last fields are distinct and source voice3 remains.',
         '18':'Retain Charles Rochefort in the progressive nameplate and Charles Jean Rochefort in the full catalogue. Clean シャルル/ロシュフォール/ジャン fields support Charles/Rochefort/Jean;do not add Jean to an original consumer that omits middle names. Voice0,not Carlo voice7 or Camille9. Further whole-route name review remains open.',
         '147':'Retain Guildmaster as the natural role label for ギルドの元締め in this pursuit;do not invent police rank or kinship. Unused secondary ヨーロッパ remains evidence,not an extra nameplate nationality.',
         '157':'Retain Sailor in this scene:the original progressive getter explicitly supplies 水夫 forIDs151..159. Catalogue 配下/Retainer and unused 韓国/Korea are distinct fields and do not create a spoken rank,nationality or allegiance. The source handoff/pursuit alone does not prove theft or legitimate ownership. Keep all aliases/fields unchanged and verify the actual scene nameplate separately.'},
        no_name_asset_or_runtime_change=True,no_global_207_name_closure_or_new_name_completion_credit=True,
        current_native_getters_not_actual_B202_speech_or_nameplate_observation=True,
        whole_exchange_clean_gloss_precedes_current_prose_comparison=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,VOICE,Path(__file__),Path('scripts/reconcile_lil_B156_actual_nameplate_v3737a.py')]},new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print([(r['actor_ID'],r['progressive'],r['catalogue'],r['voice']) for r in rows]);print('157 source-defined 水夫/Sailor alias verified across borders and selected actor. Separate catalogue/metadata retained;no fabricated relationship or global name credit.')
