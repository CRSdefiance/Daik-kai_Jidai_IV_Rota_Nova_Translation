"""Prove complete native names/components; retain distinct Sailor/Retainer fallback consumers."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.Al_Ferid_name_style_v6520 import native_name_raster,style_source_proof
from scripts.Al_Ferid_font_oracles_v6520 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B214_name_planes_v6710');INPUT=Path('work/analysis/current_V6686_native_v6696/current_native_input.json')
NAMES=Path('work/analysis/lil_B214_names_v6699/four_names_eight_getters_signature_mismatch_and_other_raw_occurrence_leads.json')
if __name__=='__main__':
    assert not ROOT.exists();names=read(NAMES);strings={};components=[]
    for row in names['source_name_fields']:
        ident=row['actor_ID']
        for key in ['progressive','catalogue']:strings.setdefault(row[key],ident)
        for col in row['fields']:
            if not col.get('current_English') or ident==151 and col['column']!=0:continue
            value=col['current_English'];strings.setdefault(value,ident);components.append(dict(actor_ID=ident,column=col['column'],text=value,source_terminated_hex=col['source_terminated_hex'],current_terminated_hex=col['current_terminated_hex'],pointer_field=col['pointer_field'],literal_component_plane_not_catalogue_UI=True))
    assert len(strings)==11 and {'Janus Pasar','Manuel Almeida','Sailor','Retainer'}<=strings.keys()
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');results=[];sheet=Image.new('RGB',(864,len(strings)*82),'#263238');draw=ImageDraw.Draw(sheet)
    for index,(text,actor) in enumerate(strings.items()):
        raw=text.encode('ascii');alignment=ctx.execute(expand,raw,actor);ctx.machines.pop();assert len(alignment['cases'])==4 and all(c['output_hex']==raw.hex() for c in alignment['cases'])
        pixels,events,font=native_name_raster(ctx.arm,raw);assert pixels==expected_pixels(ctx.arm,font,events);emitted,flushes=original_name_events(events,raw)
        assert emitted==codes(raw) and all(e['y']==0 and 0<=e['x'] and e['x']+6<=216 for e in events);physical=max(e['x']+6 for e in events);width=max(e['x']+6 for e in events if e['code']!=32)
        assert width==len(raw)*6 and width<=physical<=216 and physical-width in [0,6]
        plane=ROOT/f'name{index+1}_style11.bin';plane.write_bytes(pixels);picture=Image.new('RGB',(216,64));picture.putdata([(65,53,42) if b else (250,245,223) for b in pixels]);preview=plane.with_suffix('.png');picture.save(preview)
        draw.text((4,index*82+2),text+' complete native style11',fill='white');sheet.paste(picture.crop((0,0,216,16)).resize((864,64),Image.Resampling.NEAREST),(0,index*82+18))
        results.append(dict(text=text,actor_for_literal_pipeline=actor,native_alignment=alignment,native_plane=str(plane),native_plane_sha256=sha(pixels),events=events,zero_ink_flushes=flushes,complete_sequence_single_row_and_bounds=True,width=width,original_pair_flush_width=physical,zero_ink_flush_sequence_independently_verified=True,preview=str(preview),preview_sha256=sha(preview.read_bytes()),actual_header_or_catalogue_UI_not_observed_here=True))
    assert not ctx.machines;sp=ROOT/'eleven_native_name_and_component_planes.png';sheet.save(sp)
    save(ROOT/'four_actors_eight_getters_eleven_name_planes44_alignments.json',dict(candidate=str(ctx.rompath),candidate_sha256=ctx.doc['current_ROM_sha256'],source_name_binding=str(NAMES),source_name_binding_sha256=sha(NAMES.read_bytes()),name_planes=results,component_fields=components,native_name_literal_alignment_cases=44,source_current_style11_caller=style_source_proof(ctx.arm),all_first_internal_final_name_characters_and_original_blank_flushes_in_bounds=True,no_font_name_asset_or_runtime_change=True,three_proper_name_retention_proposals_native_display_bound=True,actor151_Sailor_Retainer_difference_not_new_editorial_approval=True,unused_actor151_secondary_metadata_not_appended=True,full_catalogue_UI_unvisited_and_component_planes_not_catalogue_field_layout_approval=True,actual_source_headers_separate_proof_and_Manuel_header_unvisited=True,all207_names_aliases_and_older_consumers_still_open=True,review_sheet=dict(path=str(sp),sha256=sha(sp.read_bytes())),visual_review_pending=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [INPUT,NAMES,Path(__file__)]},full_goal_complete=False))
    print('Eleven complete name/component planes and44 literal alignments pass; original odd-run flush preserved. Three proper-name proposals, actor151 review and full catalogue UI stay separately scoped.')
