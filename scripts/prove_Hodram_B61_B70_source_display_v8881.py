"""Render every complete clean source utterance with original dispatch/macros and distinct FE painter."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B54_B60_registered_route_context_v8868 import RouteCurrentContext
from scripts.Hodram_FE_font_oracles_v8315 import bind
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.research_lil_B209_native_pages_v6461 import pages as original_pages
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B61_B70_source_display_v8881')
GLOSS=Path('work/analysis/Hodram_B61_B70_clean_gloss_v8877/224_complete_clean_first_meanings_all_ten_exchanges_before_current_English.json')
CONTROL=Path('work/analysis/Hodram_B61_B70_source_controls_v8878/source_controls.json')
NAMES=Path('work/analysis/Hodram_B61_B70_names_v8879/sixteen_source_identities_current_getters_voices_andplanes.json')
CLEAN_NAMES=Path('work/analysis/Hodram_B61_B70_clean_names_v8880/thirtytwo_clean_full_andprogressive_compositions_current_binding.json')
INPUT=Path('work/analysis/current_V8865_Hodram_native_v8868/current_native_input.json')
PRIOR=Path('work/analysis/Hodram_B52_source_display_v8626/source_display.json')
FE_PRIOR=Path('work/analysis/Hodram_B50_source_display_v8487/source_display.json')

if __name__=='__main__':
    assert not ROOT.exists();gloss,control,names,clean_names,inp,prior,feprior=map(read,[GLOSS,CONTROL,NAMES,CLEAN_NAMES,INPUT,PRIOR,FE_PRIOR])
    assert control['current_B61_B70_English_dialogue_bodies_still_unconsulted'] and names['current_B61_B70_English_dialogue_bodies_unconsulted'] and clean_names['current_B61_B70_English_dialogue_bodies_unconsulted']
    image=NdsImage.open(inp['current_ROM']);arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
    assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256']==control['candidate_sha256']==names['candidate_sha256']
    assert sha(arm)==prior['ARM9_sha256']==feprior['ARM9_sha256'] and sha(font)==prior['font_sha256']==feprior['font_sha256']
    ns={**inherited.__dict__,'SOURCE':INPUT,'route':1,'route_mask':2,'CATALOG_LOOKUP':{}}
    for key,text in prior['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::'+key,'exec'),ns)
    ns['CATALOG_LOOKUP'],catalogue=ns['bind_current_catalog'](image)
    exec(compile(prior['source_owned_macro_body_adapter'],__file__+'::captain1-macros','exec'),ns)
    pe=dict(progressive_expand.__globals__);exec(compile(prior['source_owned_progressive_adapter'],__file__+'::progressive-macros','exec'),pe)
    # The FE adapter has its own trusted original globals, not a progressive actor.
    from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as original_FE_expand
    fe_env=dict(original_FE_expand.__globals__);exec(compile(feprior['source_owned_FE_adapter'],__file__+'::null-actor-FE-macros','exec'),fe_env)
    pixels,factory,oracle=bind(image);FE,calibration=factory(image)
    pages_env={**original_pages.__globals__,'expected_pixels':pixels,'codes':codes}
    exec(compile(prior['source_owned_target_page_adapter'],__file__+'::original-fullwidth-pages','exec'),pages_env)
    voices={r['source_selector']:r['original_voice_class'] for r in names['sixteen_source_selector_voices']['rows']}
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');rows=[];sheets=[];page_count=0
    for group in gloss['groups']:
        pictures=[]
        for row in group['records']:
            raw=bytes.fromhex(row['source_hex']);prefix,body=raw[0],raw[1:];is_FE=prefix==254
            assert (prefix in voices or is_FE) and body not in ns['CATALOG_LOOKUP'] and row['source_complete_preamble_hex']=='0040ffff00'+bytes([prefix]).hex()
            result=ctx.execute(ns['dispatch'],prefix,body);ctx.machines.pop()
            assert result['resolved_actor_ID']==(None if is_FE else prefix) and result['source_voice_class']==(None if is_FE else voices[prefix])
            expected=body.replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')
            boundary=next(b for b in result['boundaries'] if b['kind']==('unexecuted-FE-modal-body' if is_FE else 'unexecuted-progressive-body'))
            assert boundary['text_hex']==expected.hex() and result['registered_catalog_match'] is None
            aligned=ctx.execute(fe_env['expand'] if is_FE else pe['expand'],body,*(() if is_FE else (prefix,)));ctx.machines.pop()
            assert len(aligned['cases'])==4 and all(c['output_hex']==expected.hex() for c in aligned['cases'])
            if is_FE:
                assert len(result['FE_original_null_actor_calls'])==1 and result['FE_original_null_actor_calls'][0]['args'][2]==0
                rendered=FE(expected);plane=rendered.pop('physical');logical=rendered.pop('logical')
                file=ROOT/(row['id']+'_FE_physical.bin');file.write_bytes(plane);logicalfile=file.with_name(row['id']+'_FE_logical.bin');logicalfile.write_bytes(logical)
                rendered.update(native_physical_plane=str(file),native_physical_plane_sha256=sha(plane),native_logical_plane=str(logicalfile),native_logical_plane_sha256=sha(logical),pages=1)
                picture=Image.new('RGB',(228,64));picture.putdata([(0,8,0) if v else (239,232,201) for v in plane]);pictures.append((row['id']+' original FE null-actor',picture));page_count+=1
            else:
                assert not result['FE_original_null_actor_calls'];rendered=pages_env['pages'](arm,font,expected)
                assert rendered['complete_consumed_bytes']==len(expected)
                for page in rendered['pages']:
                    plane=bytes.fromhex(page.pop('native_plane_hex'));file=ROOT/(row['id']+f'_page{page["page"]}.bin');file.write_bytes(plane);page.update(native_plane=str(file),native_plane_sha256=sha(plane))
                    picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};picture.putdata([colors[v] for v in plane]);pictures.append((row['id']+f' original p{page["page"]}',picture));page_count+=1
            rows.append(dict(id=row['id'],file_path=row['file_path'],block=row['block'],source_reference=row['source_reference'],source_selector=prefix,
                source_hex=raw.hex(),source_complete_preamble_hex=row['source_complete_preamble_hex'],source_0100_ancestors=row['source_0100_ancestors'],expanded_source_hex=expected.hex(),
                original_dispatch=result,original_four_alignments=aligned,complete_native_source_display=rendered))
        for start in range(0,len(pictures),12):
            part=pictures[start:start+12];sheet=Image.new('RGB',(912,((len(part)+1)//2)*160),'#263238');draw=ImageDraw.Draw(sheet)
            for i,(label,picture) in enumerate(part):
                x,y=i%2*456,i//2*160;draw.text((x+3,y+3),label+' offline source',fill='white');sheet.paste(picture.resize((picture.width*2,128),Image.Resampling.NEAREST),(x,y+24))
            sheetfile=ROOT/f'B{group["block"]}_source_part{start//12+1}.png';sheet.save(sheetfile);sheets.append(dict(block=group['block'],path=str(sheetfile),sha256=sha(sheetfile.read_bytes()),source_page_count=len(part)))
        save(ROOT/f'B{group["block"]}_completed_source_rows.json',dict(records=[r for r in rows if r['block']==group['block']],older_English_unread=True,new_credit=0))
        print('Complete source block',group['block'],'utterances',len(group['records']),'pages',len(pictures),flush=True)
    assert len(rows)==224 and sum(len(r['original_four_alignments']['cases']) for r in rows)==896 and not ctx.machines
    macro_counts={m:sum(g['source_macro_counts'][m] for g in control['groups']) for m in ['FI','FA','FO']}
    save(ROOT/'224_complete_source_dispatches_alignments_pages_andmacro_binding.json',dict(candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],ARM9_sha256=sha(arm),font_sha256=sha(font),
        records=rows,source_macro_counts=macro_counts,default_FI6_FA9_FO15=dict(FI=6,FA=9,FO=15),
        source_FI_expands_to_current_captain_given_Hodram_andFA_to_surname_Bergstrom_not_company=True,
        original_default_macro_expansions_measured_onall_actual_source_macro_occurrences_fouralignments=True,
        custom_player_names_lengths_parities_andall207_name_contexts_remain_unverified=True,
        current_source_pages_use_current_English_name_substitutions_not_all_Japanese_UI=True,
        source_FE_count=0,FE_no_source_occurrences_prior_calibration_only=True,
        FE_factory_calibration=calibration,target_oracle_binding=oracle,registered_catalogue_binding=catalogue,
        source_owned_dispatch_adapters=prior['source_owned_dispatch_adapters'],source_owned_macro_body_adapter=prior['source_owned_macro_body_adapter'],
        source_owned_progressive_adapter=prior['source_owned_progressive_adapter'],source_owned_FE_adapter=feprior['source_owned_FE_adapter'],source_owned_target_page_adapter=prior['source_owned_target_page_adapter'],
        complete_native_source_page_count=page_count,review_sheets=sheets,direct_view_pending=True,
        current_B61_B70_English_dialogue_bodies_unconsulted=True,source_controls_proved_context_name_editorial_current_localization_actual_andrelease_still_pending=True,
        offline_native_CPU_tests_not_new_gameplay_natural_activation_fullcatalogue_orcustomnames_approval=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [GLOSS,CONTROL,NAMES,CLEAN_NAMES,INPUT,PRIOR,FE_PRIOR,Path(__file__)]}))
    print('All224source dispatches/896alignments/'+str(page_count)+'complete native pages pass;macro counts'+str(macro_counts)+'. Direct source view/branch context pending;no priorEnglish,capture,ROM orcredit.',flush=True)
