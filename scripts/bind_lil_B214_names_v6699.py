"""Bind native proper-name consumers and letter signature; keep D0 fallback review separate."""
import inspect,struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,POOL,TABLE,cstring
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prove_lil_B167_names_v4124b import names
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
SOURCE=Path('work/analysis/lil_B214_source_v6697/all17_clean_current_letter_notices_reactions_full1316_inverse.json')
CONSUMERS=Path('work/analysis/lil_B214_consumers_v6698/all17_effective_bodies34_dispatches_two_whole_commands414_style_pointers.json')
INPUT=Path('work/analysis/current_V6686_native_v6696/current_native_input.json')
ROOT=Path('work/analysis/lil_B214_names_v6699')
REASONS={2:'Retain established Lil Argot from clean リル/アーゴット and the current captain identity. Preserve her separate custom captain getter and all complete characters.',4:'Retain the existing proper name Janus Pasar from clean ジェナス/パサー and the two native consumers. The current letter alone signs Janus Pasha, contradicting these getters; correct this signature to Janus Pasar in the B214 manuscript. This is a contextual consistency decision, not new user approval of a historical Latin spelling or an inferred title. No global name asset is changed.',23:'Retain Manuel Almeida from clean マヌエル/アルメイダ and the current getters. The letter explicitly calls him devout; this does not establish a clerical office, rank or kinship.',151:'This is the current opening D0 role1 fallback only. Progressive Sailor and catalogue Retainer must stay distinct in evidence. No new editorial approval of actor151 or natural B214 crew identity is supplied; the full earlier role-label lead remains open.'}
if __name__=='__main__':
    assert not ROOT.exists();packet,current=read(SOURCE),read(CONSUMERS);assert current['source_context_sha256']==sha(SOURCE.read_bytes())
    text=checked_text(inspect.getsource(names),{'for ident in [2,4,13,23,109]:':'for ident in [2,4,23,151]:','actor = root+4+32*ident':'actor = root+0x19E4 if ident==2 else root+4+32*ident','all_ten_original_consumers_and_owned_or_readonly_memory_paths_exact':'all_eight_original_consumers_and_owned_or_readonly_memory_paths_exact'})
    env=dict(names.__globals__);exec(compile(text,__file__+'::four-source-or-fallback-names','exec'),env)
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');native=ctx.execute(env['names']);ctx.machines.pop();assert not ctx.machines and len(native['rows'])==8
    original=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');arm=ctx.arm;payload=bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]);assert len(payload)==123264 and arm.count(payload)==1
    payload_at=arm.index(payload);catalog={r['actor_ID']:r for r in current['catalog']['rows']};fields=[]
    for ident in [2,4,23,151]:
        row=[]
        for delta in [0,4,8]:
            at=TABLE+ident*32+delta;sp,cp=[struct.unpack_from('<I',code,at)[0] for code in [original,arm]];assert bool(sp)==bool(cp)
            if not sp:row.append(dict(pointer_field=at,column=delta,source_null=True,current_null=True));continue
            source=cstring(original,sp-BASE)
            if POOL<=cp<POOL+len(payload):off=cp-POOL;value=cstring(payload,off);storage=payload_at+off;kind='verified-current-staged-payload'
            else:storage=cp-BASE;value=cstring(arm,storage);kind='original-static-ARM9'
            row.append(dict(pointer_field=at,column=delta,source_pointer=sp,source_storage_offset=sp-BASE,source_terminated_hex=source.hex(),Japanese=source[:-1].decode('cp932'),current_pointer=cp,current_storage_offset=storage,current_storage_kind=kind,current_terminated_hex=value.hex(),current_English=value[:-1].decode('cp932')))
        progressive=next(r['text'] for r in native['rows'] if r['actor_ID']==ident and r['consumer']=='progressive-nameplate');full=next(r['text'] for r in native['rows'] if r['actor_ID']==ident and r['consumer']=='full-catalogue');assert full==catalog[ident]['current_catalog_name']
        fields.append(dict(actor_ID=ident,fields=row,progressive=progressive,catalogue=full,voice=catalog[ident]['original_voice_class'],retention_proposal=ident!=151,editorial_reason=REASONS[ident],full_catalogue_UI_unvisited=True,native_glyph_planes_actual_headers_and_final_approval_pending=True,new_asset_bytes=0,new_name_credit=0))
    byid={r['id']:r for r in packet['records']};signature=byid['DK4_MES_B214_R0068'];old=bytes.fromhex(signature['current_hex'])[1:].decode('cp932');assert 'Janus Pasha' in old and fields[1]['catalogue']=='Janus Pasar'
    hits=[];image=NdsImage.open(packet['current_ROM'])
    for path in ['/data/SC0.DK4','/data/SC1.DK4','/data/SC2.DK4','/data/SC3.DK4']:
        for bi,block in enumerate(__import__('dk4tool.formats.ilnk',fromlist=['IlnkContainer']).IlnkContainer.parse(image.read_file(path)).blocks):
            for term in [b'Janus Pasha',b'Janus Pasar']:
                at=block.find(term)
                while at>=0:
                    hits.append(dict(file_path=path,block=bi,offset=at,bytes=len(term),term=term.decode('ascii'),block_sha256=sha(block),surrounding_hex=block[max(0,at-32):min(len(block),at+len(term)+32)].hex(),raw_current_occurrence_only_not_contextual_approval_or_new_credit=True));at=block.find(term,at+1)
    save(ROOT/'four_names_eight_getters_signature_mismatch_and_other_raw_occurrence_leads.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),current_consumers=str(CONSUMERS),current_consumers_sha256=sha(CONSUMERS.read_bytes()),source_name_fields=fields,native_eight_consumer_cases=native,source_owned_adapter=text,full_source_signature='ジェナス・パサー',current_signature_record=signature,current_stored_signature='Janus Pasha',current_native_progressive_and_catalogue_name='Janus Pasar',proposed_signature='Janus Pasar',other_raw_story_occurrences_for_contextual_review=hits,no_global_substitution_or_name_asset_change=True,no_new_name_editorial_completion_credit=True,three_proper_name_retention_reasons_recorded_not_all_native_glyph_consumers_approved=True,full_catalogue_UI_unvisited=True,native_complete_font_planes_actual_headers_and_signature_display_pending=True,dynamic151_fallback_not_forced_role_or_natural_event214_speaker_claim=True,actor151_Sailor_Retainer_full_contextual_review_stays_open=True,all207_name_role_alias_review_open=True,current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONSUMERS,INPUT,Path(names.__code__.co_filename),Path(__file__)]},full_goal_complete=False))
    print([(r['actor_ID'],r['progressive'],r['catalogue'],r['voice']) for r in fields]);print('Signature mismatch Pasha -> existing native Pasar; raw story occurrences:',len(hits),'. No global rename or credit.')
