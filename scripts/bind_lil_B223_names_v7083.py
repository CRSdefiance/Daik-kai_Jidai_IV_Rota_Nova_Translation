"""Review the letter's names and full signature; keep dynamic Sailor/Retainer evidence separate."""
import inspect,struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,POOL,TABLE,cstring
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prove_lil_B167_names_v4124b import names
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
SOURCE=Path('work/analysis/lil_B223_source_v7078/all17_clean_current_letter_notices_reactions_full1316_inverse.json')
CONSUMERS=Path('work/analysis/lil_B223_consumers_v7079/all17_effective_bodies34_dispatches_two_whole_commands414_style_pointers.json')
INPUT=Path('work/analysis/current_V7067_native_v7077/current_native_input.json')
ROOT=Path('work/analysis/lil_B223_names_v7083')
REASONS={2:'Retain the established Lil Argot identity from cleanリル/アーゴット and both current native consumers. The actual captain uses its separate object. Her interest in Ian\'s letter gives no basis for a new title,relationship or identity.',13:'Retain the established Cesare Tony pair from cleanチェザーレ/トーニ and both native consumers. Cesare is a readable given-name rendering,and Tony preserves the established fictional family component without an observed English readability or identity defect. This conditional explanatory reply gives no basis for respelling the family name,adding a rank or treating unused metadata as nationality. No claim of verified original Latin artwork or authentic national surname is made.',21:'Retain Ian Dukov from cleanイアン/ドゥーコフ and both current original getters. The letter explicitly signs the full given/family pair;restore Ian Dukov in its signature rather than the old Dukov-only closing. Lil and every automatic delivery notice use sourceイアン,so use Ian there. Do not invent Ivan,a patronymic,rank,kinship or nationality from the surrounding Russian-history discussion. The established fictional family rendering remains;original Latin artwork is not independently inspected here.',151:'This is the unforced current opening D0 role1 fallback only. Preserve progressive Sailor and catalogue Retainer as distinct outputs,with the wider actor151 role-label localization review still open. No source B223 natural crew identity,age,rank or new editorial approval is inferred.'}
if __name__=='__main__':
    assert not ROOT.exists();packet,current=read(SOURCE),read(CONSUMERS);assert current['source_context_sha256']==sha(SOURCE.read_bytes())
    text=checked_text(inspect.getsource(names),{'for ident in [2,4,13,23,109]:':'for ident in [2,13,21,151]:','actor = root+4+32*ident':'actor = root+0x19E4 if ident==2 else root+4+32*ident','all_ten_original_consumers_and_owned_or_readonly_memory_paths_exact':'all_eight_original_consumers_and_owned_or_readonly_memory_paths_exact'})
    env=dict(names.__globals__);exec(compile(text,__file__+'::source-names-and-disclosed-fallback','exec'),env)
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');native=ctx.execute(env['names']);ctx.machines.pop();assert not ctx.machines and len(native['rows'])==8
    original=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');arm=ctx.arm;payload=bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]);assert len(payload)==123264 and arm.count(payload)==1
    payload_at=arm.index(payload);catalog={r['actor_ID']:r for r in current['catalog']['rows']};fields=[]
    for ident in [2,13,21,151]:
        row=[]
        for delta in [0,4,8]:
            at=TABLE+ident*32+delta;sp,cp=[struct.unpack_from('<I',code,at)[0] for code in [original,arm]];assert bool(sp)==bool(cp)
            if not sp:row.append(dict(pointer_field=at,column=delta,source_null=True,current_null=True));continue
            source=cstring(original,sp-BASE)
            if POOL<=cp<POOL+len(payload):off=cp-POOL;value=cstring(payload,off);storage=payload_at+off;kind='verified-current-staged-payload'
            else:storage=cp-BASE;value=cstring(arm,storage);kind='original-static-ARM9'
            row.append(dict(pointer_field=at,column=delta,source_pointer=sp,source_storage_offset=sp-BASE,source_terminated_hex=source.hex(),Japanese=source[:-1].decode('cp932'),current_pointer=cp,current_storage_offset=storage,current_storage_kind=kind,current_terminated_hex=value.hex(),current_English=value[:-1].decode('cp932')))
        progressive=next(r['text'] for r in native['rows'] if r['actor_ID']==ident and r['consumer']=='progressive-nameplate');full=next(r['text'] for r in native['rows'] if r['actor_ID']==ident and r['consumer']=='full-catalogue');assert full==catalog[ident]['current_catalog_name']
        fields.append(dict(actor_ID=ident,fields=row,progressive=progressive,catalogue=full,voice=catalog[ident]['original_voice_class'],retention_proposal=ident!=151,editorial_reason=REASONS[ident],full_catalogue_UI_unvisited=True,native_glyph_planes_actual_header_scope_and_final_approval_pending=True,new_asset_bytes=0,new_name_credit=0))
    assert [(r['actor_ID'],r['progressive'],r['catalogue'],r['voice']) for r in fields]==[(2,'Lil Argot','Lil Argot',3),(13,'Cesare Tony','Cesare Tony',0),(21,'Ian Dukov','Ian Dukov',1),(151,'Sailor','Retainer',4)]
    signature=next(r for r in packet['records'] if r['source_record_index']==48);old=bytes.fromhex(signature['current_hex'])[1:].decode('cp932');assert '-- Dukov' in old and 'イアン・ドゥーコフ' in signature['source_Japanese']
    save(ROOT/'four_names_eight_getters_full_Ian_signature_and_direct_given_name_binding.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),current_consumers=str(CONSUMERS),current_consumers_sha256=sha(CONSUMERS.read_bytes()),source_name_fields=fields,native_eight_consumer_cases=native,source_owned_adapter=text,full_source_signature='イアン・ドゥーコフ',current_signature_record=signature,current_stored_signature=old,current_native_progressive_and_catalogue_name='Ian Dukov',proposed_full_signature='Ian Dukov',source_direct_given_name='イアン',proposed_direct_given_name='Ian',no_global_substitution_or_name_asset_change=True,no_new_name_editorial_completion_credit=True,three_proper_name_retention_reasons_not_global207_approval=True,full_catalogue_UI_unvisited=True,native_complete_font_planes_actual_headers_and_signature_display_pending=True,dynamic151_fallback_not_forced_or_natural_event223_identity=True,actor151_Sailor_Retainer_review_remains_open=True,current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONSUMERS,INPUT,Path(names.__code__.co_filename),Path(__file__),Path('docs/glossary.md'),Path('translations/character_name_localization_policy_v1.json')]},full_goal_complete=False))
    print([(r['actor_ID'],r['progressive'],r['catalogue'],r['voice']) for r in fields]);print('Restore source Ian/full Ian Dukov in prose;three contextual name retentions proposed. Actor151 and207-name scope open;no asset or credit.')
