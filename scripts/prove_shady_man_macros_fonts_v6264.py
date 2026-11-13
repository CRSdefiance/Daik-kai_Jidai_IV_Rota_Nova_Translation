"""Original substitutions and complete unchanged-font native label plane with exact hash guards."""
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v6097 import CurrentContext as ParentContext
from scripts.current_build_native_context_v6261 import CurrentContext as TargetContext
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.verify_name_catalog_glyphs_v278 import raster
from scripts.shady_man_font_oracles_v6263 import expected_pixels
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shady_man_macros_fonts_v6264')
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True);versions=[];target=None
    for case,path,Context in [('parent','work/analysis/current_V6220_native_v6228/current_native_input.json',ParentContext),('target','work/analysis/shady_man_names_v6263/target_native_input.json',TargetContext)]:
        ctx=Context(path,'unused-no-historical-ROM',ROOT/(case+'_current_context'));cases=[]
        for ident in [2,7,164,165,172,173]:
            for body in [b'FI FA FO FU',b'Shady Man Suspicious Person']:
                value=ctx.execute(expand,body,ident);ctx.machines.pop();cases.append(dict(input_hex=body.hex(),actor_ID=ident,native=value))
        assert not ctx.machines;versions.append(dict(case=case,cases=cases,context_plan=str(ctx.proof_path),context_plan_sha256=sha(ctx.proof_path.read_bytes())))
        if case=='target':target=ctx
    for a,b in zip(versions[0]['cases'],versions[1]['cases'],strict=True):
        assert a['input_hex']==b['input_hex'] and a['actor_ID']==b['actor_ID']
        assert [r['output_hex'] for r in a['native']['cases']]==[r['output_hex'] for r in b['native']['cases']]
        expected=b'Lil Argot Argot Co. Lil Argot' if bytes.fromhex(a['input_hex'])==b'FI FA FO FU' else b'Shady Man Suspicious Person'
        assert all(bytes.fromhex(r['output_hex'])==expected for r in b['native']['cases'])
    word='Shady Man';pixels,events,font=raster(target.arm,word.encode());expected=expected_pixels(target.arm,font,events)
    assert pixels==expected and [r['code'] for r in events]==list(b'Shady Man ')
    assert len({r['y'] for r in events})==1 and max(r['x']+6 for r in events)<=216
    plane=ROOT/'complete_native_Shady_Man_plane.png';photo=Image.new('RGB',(216,64),'#faf5df');photo.putdata([(65,53,42) if b else (250,245,223) for b in pixels]);photo.resize((864,256),Image.Resampling.NEAREST).save(plane)
    save(ROOT/'unchanged96_macro_alignments_and_complete_single_row_label.json',dict(versions=versions,native_macro_alignment_cases=96,parent_target_macro_and_literal_outputs_exact=True,native_FI_FA_FO_FU_outputs='Lil / Argot / Argot Co. / Lil Argot',all_unowned4MiB_models_RNG_inputs_outputs_ABI_canaries_and_source_owned_name_ring_restoration_exact=True,synthetic_offline_macro_inputs_not_added_to_any_shipped_scene=True,original_UI_constructor_boundary_unexecuted_explicit=True,complete_original_font_native_plane=dict(label=word,events=events,whole_native_plane_sha256=sha(pixels),image=str(plane),image_sha256=sha(plane.read_bytes()),complete_first_final_glyphs_order_bounds_canaries_and_single_row_native_plane_exact=True),full_catalogue_UI_not_visited_native_strings_and_font_bounds_checked=True,representative_actual_label_and_visual_review_pending=True,no_name_completion_credit=True,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('scripts/shady_man_font_oracles_v6263.py'),Path('scripts/generic_name_macro_owned_v5886b.py'),Path('work/analysis/shady_man_names_v6263/all207_distinct_names621_fields_eight_voices_and_one_changed_primary.json')]}))
    print('96 original macro/literal alignment cases exact;complete Shady Man plane and odd final pair pass. Actual/visual approval pending.')
