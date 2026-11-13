"""Bind proper names, full signature and dynamic fallback separately; native glyph review remains pending."""
import inspect,struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,POOL,TABLE,cstring
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prove_lil_B167_names_v4124b import names
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.current_build_native_context_v6261b import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
SOURCE=Path('work/analysis/lil_B209_source_v6450d/all20_clean_current_letter_and_voice_alternative_context.json')
CONSUMERS=Path('work/analysis/lil_B209_current_consumers_v6451/all20_bodies40_dispatches4_whole_style_commands828_catalog_slots_and_names.json')
INPUT=Path('work/analysis/current_V6439_native_v6449/current_native_input.json')
ROOT=Path('work/analysis/lil_B209_names_v6455')
if __name__=='__main__':
    assert not ROOT.exists();packet,current=read(SOURCE),read(CONSUMERS);assert current['source_context_sha256']==sha(SOURCE.read_bytes())
    text=checked_text(inspect.getsource(names),{
        'for ident in [2,4,13,23,109]:':'for ident in [2,11,12,151]:',
        'actor = root+4+32*ident':'actor = root+0x19E4 if ident==get(0x7F244) else root+4+32*ident',
        'all_ten_original_consumers_and_owned_or_readonly_memory_paths_exact':'all_eight_original_consumers_and_owned_or_readonly_memory_paths_exact',
    })
    env=dict(names.__globals__);exec(compile(text,__file__+'::four-source-or-original-fallback-names','exec'),env)
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');native=ctx.execute(env['names']);ctx.machines.pop();assert not ctx.machines and len(native['rows'])==8
    original=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');arm=ctx.arm;payload=bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]);assert len(payload)==123264 and arm.count(payload)==1
    payload_at=arm.index(payload);catalog={r['actor_ID']:r for r in current['catalog']['rows']};fields=[]
    for ident in [2,11,12,151]:
        row=[]
        for delta in [0,4,8]:
            at=TABLE+ident*32+delta;sp,cp=[struct.unpack_from('<I',code,at)[0] for code in [original,arm]];assert bool(sp)==bool(cp)
            if not sp:row.append(dict(pointer_field=at,column=delta,source_null=True,current_null=True));continue
            source=cstring(original,sp-BASE)
            if POOL<=cp<POOL+len(payload):off=cp-POOL;value=cstring(payload,off);storage=payload_at+off;kind='verified-current-staged-payload'
            else:storage=cp-BASE;value=cstring(arm,storage);kind='original-static-ARM9'
            row.append(dict(pointer_field=at,column=delta,source_pointer=sp,source_storage_offset=sp-BASE,source_terminated_hex=source.hex(),Japanese=source[:-1].decode('cp932'),current_pointer=cp,current_storage_offset=storage,current_storage_kind=kind,current_terminated_hex=value.hex(),current_English=value[:-1].decode('cp932')))
        progressive=next(r['text'] for r in native['rows'] if r['actor_ID']==ident and r['consumer']=='progressive-nameplate');full=next(r['text'] for r in native['rows'] if r['actor_ID']==ident and r['consumer']=='full-catalogue');assert full==catalog[ident]['current_catalog_name']
        fields.append(dict(actor_ID=ident,fields=row,progressive=progressive,catalogue=full,voice=catalog[ident]['original_voice_class'],retention_proposal=True,editorial_reason={2:'Established Lil Argot matches cleanリル/アーゴット and current captain identity. Preserve approved working name and custom captain getter.',11:'Jam Jack Ludwyan is the existing proper-name spelling supported by cleanジャム/ルドワイヤン/ジャック and its distinct progressive/full-name getters. No evidence here authorizes replacing an uncommon proper name with a more familiar one or changing Jack to Jacques. Preserve all fields;middle/additional-field consumer scope stays explicit.',12:'Yukihisa Genjo Shiraki matches cleanユキヒサ/シラキ/ゲンジョウ and the source signature白樹玄丞行尚（ユキヒサ）. Full English signature follows current given/additional/family catalogue order. Do not invent rank,kinship or original-Latin-artwork/user-approved spelling claims.',151:'Retainer is only the current unassigned-D0 fallback identity. Its current clean label and native getters are preserved;this does not make a generic retainer the naturally eligible story speaker or close the wider role-label review.'}[ident]))
    save(ROOT/'four_source_or_fallback_names_eight_getters_full_signature_and_exact_fields.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),current_consumers=str(CONSUMERS),current_consumers_sha256=sha(CONSUMERS.read_bytes()),source_name_fields=fields,native_eight_consumer_cases=native,source_owned_adapter=text,full_source_signature='白樹玄丞行尚（ユキヒサ）',current_proposed_signature='Yukihisa Genjo Shiraki',no_name_asset_or_font_or_runtime_change=True,no_new_name_editorial_completion_credit=True,proper_name_retention_reasons_recorded_not_all_native_glyph_consumers_approved=True,native_complete_font_planes_macro_alignments_actual_headers_and_full_catalogue_UI_visit_pending_or_unvisited=True,dynamic151_fallback_not_forced_role_or_natural_event209_speaker_claim=True,all207_name_role_alias_review_open=True,current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONSUMERS,INPUT,Path(names.__code__.co_filename),Path(__file__)]},full_goal_complete=False))
    print([(r['actor_ID'],r['progressive'],r['catalogue']) for r in fields]);print('Exact fields/eight getters and contextual name retentions bound;native font/actual headers remain pending. No global name approval.')
