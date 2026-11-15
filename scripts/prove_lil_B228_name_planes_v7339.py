"""Check two actors,four original getters andeight name/component planes;untranslated catalogue middle stays unapproved."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.square_shopkeeper_name_style_v7020 import native_name_raster,style_source_proof
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B228_name_planes_v7339');INPUT=Path('work/analysis/current_V7324_native_v7329/current_native_input.json');CONSUMER=Path('work/analysis/lil_B228_consumers_v7335/thirteen_effective_bodies26_dispatches_two_actors_four_name_consumers.json')
if __name__=='__main__':
    assert not ROOT.exists();c=read(CONSUMER);fields=c['source_name_fields'];returned=c['native_four_distinct_name_consumers']['rows'];assert len(returned)==4 and [r['actor_ID'] for r in fields]==[2,22]
    strings={r['text']:r['actor_ID'] for r in returned};components=[]
    for r in fields:
        for col in r['fields']:
            if not col.get('current_English'):continue
            text=col['current_English'];strings.setdefault(text,r['actor_ID']);components.append(dict(actor_ID=r['actor_ID'],column=col['column'],text=text,source_terminated_hex=col['source_terminated_hex'],current_terminated_hex=col['current_terminated_hex'],source_pointer_field=col['pointer_field'],literal_field_not_automatic_name_suffix=True))
    assert set(strings)=={'Lil Argot','Lil','Argot','Samwell Khan','Samwell ダ Khan','Samwell','Khan','ダ'}
    assert {(r['actor_ID'],r['consumer']):r['text'] for r in returned}=={(2,'progressive-nameplate'):'Lil Argot',(2,'full-catalogue'):'Lil Argot',(22,'progressive-nameplate'):'Samwell Khan',(22,'full-catalogue'):'Samwell ダ Khan'}
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');rows=[];sheet=Image.new('RGB',(864,656),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(text,actor) in enumerate(strings.items()):
        raw=text.encode('cp932');alignment=ctx.execute(expand,raw,actor);ctx.machines.pop();assert len(alignment['cases'])==4 and all(v['output_hex']==raw.hex() for v in alignment['cases'])
        pixels,events,font=native_name_raster(ctx.arm,raw);assert pixels==expected_pixels(ctx.arm,font,events);emitted,flushes=original_name_events(events,raw);assert emitted==codes(raw) and all(e['y']==0 and 0<=e['x'] and e['x']+(6 if e['kind']=='ascii' else 12)<=216 for e in events)
        width=max(e['x']+(6 if e['kind']=='ascii' else 12) for e in events if e['code']!=32);flush=max(e['x']+(6 if e['kind']=='ascii' else 12) for e in events);assert width==len(raw)*6 and width<=flush<=216 and flush-width in [0,6]
        plane=ROOT/f'name{i+1}_style11.bin';plane.write_bytes(pixels);picture=Image.new('RGB',(216,64));picture.putdata([(65,53,42) if b else (250,245,223) for b in pixels]);preview=plane.with_suffix('.png');picture.save(preview)
        draw.text((4,i*82+2),text+' complete native style11',fill='white');sheet.paste(picture.crop((0,0,216,16)).resize((864,64),Image.Resampling.NEAREST),(0,i*82+18))
        rows.append(dict(text=text,actor_for_literal_pipeline=actor,native_alignment=alignment,native_plane=str(plane),native_plane_sha256=sha(pixels),events=events,zero_ink_flushes=flushes,width=width,original_pair_flush_width=flush,complete_sequence_single_row_and_bounds=True,preview=str(preview),preview_sha256=sha(preview.read_bytes()),actual_header_or_full_catalogue_UI_not_observed=True))
    assert not ctx.machines;sp=ROOT/'eight_complete_name_and_literal_component_planes.png';sheet.save(sp)
    save(ROOT/'two_actors_four_getters_eight_literal_planes32_alignments.json',dict(candidate=c['candidate'],candidate_sha256=c['candidate_sha256'],consumer_proof=str(CONSUMER),consumer_proof_sha256=sha(CONSUMER.read_bytes()),source_fields=fields,distinct_native_getter_values=returned,source_current_literal_components=components,name_planes=rows,name_literal_alignment_count=32,complete_name_component_plane_count=8,source_style11_proof=style_source_proof(ctx.arm),source_personal_fields_Lil_Argot_Samwell_Khan_anduntranslated_middle_getter_bytes_bound_not_catalogue_wording_approval=True,no_surname_nationality_occupation_or_scene_location_inferred_from_secondary_field=True,all_first_internal_final_name_glyphs_and_zero_ink_flushes_complete=True,actual_headers_and_full_catalogue_UI_unvisited=True,no_name_asset_or_duplicate_credit=True,full207_name_role_alias_review_open=True,review_sheet=dict(path=str(sp),sha256=sha(sp.read_bytes())),visual_review_pending=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [INPUT,CONSUMER,Path(__file__)]},full_goal_complete=False))
    print('Two actors,four original getters,eight complete planes/32 alignments. Lil Argot andSamwell Khan headers arebound;Samwell ダ Khan istechnical evidence,not approved catalogue wording. Actual headers/catalogue UI unvisited;zero credit.')
