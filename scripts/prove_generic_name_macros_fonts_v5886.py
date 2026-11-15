"""Current original macro processor and independent complete native-font planes for three labels."""
import inspect
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.prove_maria_B109_macro_profile_v3507 import expand
from scripts.verify_name_catalog_glyphs_v278 import raster,expected_pixels
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/generic_name_macros_fonts_v5886')

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    adapted=checked_text(inspect.getsource(expand),{
        'captain==3':'captain==2',
        "expected=body.replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan');assert value==expected and":"assert"})
    env=dict(expand.__globals__);exec(compile(adapted,__file__+'::unchanged-original-macro-processor','exec'),env)
    versions=[];target=None
    for label,inp in [('parent','work/analysis/lil_B200_voices_v5827/current_native_input.json'),('target','work/analysis/generic_speaker_names_v5884/target_native_input.json')]:
        ctx=CurrentContext(inp,'unused-no-historical-ROM-read',ROOT/(label+'_current_context'));cases=[]
        for ident in [2,164,165,172]:
            for body in [b'FI FA FO FU',b'Man Woman Stranger']:
                value=ctx.execute(env['expand'],body,ident);ctx.machines.pop();cases.append(dict(input_hex=body.hex(),actor_ID=ident,native=value))
        assert not ctx.machines;versions.append(dict(case=label,cases=cases,context_plan=str(ctx.proof_path),context_plan_sha256=sha(ctx.proof_path.read_bytes())))
        if label=='target':target=ctx
    for a,b in zip(versions[0]['cases'],versions[1]['cases'],strict=True):
        assert a['input_hex']==b['input_hex'] and a['actor_ID']==b['actor_ID']
        assert a['native']['cases']==b['native']['cases']
        expected=b'Lil Argot Argot Co. Lil Argot' if bytes.fromhex(a['input_hex'])==b'FI FA FO FU' else b'Man Woman Stranger'
        assert all(bytes.fromhex(c['output_hex'])==expected for c in b['native']['cases'])
    glyphs=[]
    for word in ['Man','Woman','Stranger']:
        pixels,events,font=raster(target.arm,word.encode('ascii'));expected=expected_pixels(target.arm,font,events)
        assert pixels==expected and len(events)==len(word)
        assert [r['code'] for r in events]==list(word.encode('ascii')) and all(r['kind']=='ascii' for r in events)
        assert len({r['y'] for r in events})==1 and max(r['x']+6 for r in events)<=216
        glyphs.append(dict(label=word,events=events,whole_native_plane_sha256=sha(pixels),
            complete_first_final_glyphs_order_bounds_canaries_and_single_row_native_plane_exact=True))
    actual=Path('work/analysis/generic_speaker_scenes_v5885b/two_complete_exchanges_original_commands_and_exact_nameplate_glyphs.json');scene=read(actual)
    assert len(scene['review_sheets'])==5 and scene['actual_target_nameplate_cases']==16
    for row in scene['review_sheets']:assert sha(Path(row['path']).read_bytes())==row['sha256']
    save(ROOT/'unchanged_runtime_substitutions_three_native_planes_and_visual_review.json',dict(
        versions=versions,source_owned_original_macro_adapter=adapted,
        native_macro_alignment_cases=64,parent_target_macro_and_literal_outputs_exact=True,
        native_FI_FA_FO_FU_outputs='Lil / Argot / Argot Co. / Lil Argot',
        all_original_4MiB_models_RNG_inputs_outputs_ABI_and_canaries_exact=True,
        synthetic_offline_macro_inputs_not_added_to_any_shipped_scene=True,
        original_UI_constructor_boundary_unexecuted_explicit=True,
        three_complete_original_font_native_planes=glyphs,
        full_catalogue_UI_not_visited_native_strings_and_font_bounds_checked=True,
        actual_nameplate_independent_masks_and_five_complete_context_sheets_viewed=True,
        viewed_sheets=scene['review_sheets'],actual_proof=str(actual),actual_proof_sha256=sha(actual.read_bytes()),
        failed_first_audit_expected_following_B120_too_early_preserved='scripts/audit_generic_speaker_scenes_v5885.py',
        corrected_audit_keeps_real_recovery_return7677_no_following_command_before8001=True,
        no_new_dialogue_review_credit_or_registered_ROM=True,new_emulator_runs=0,new_name_completion_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('scripts/audit_generic_speaker_scenes_v5885.py'),Path('scripts/audit_generic_speaker_scenes_v5885b.py'),actual]},
        full_goal_complete=False))
    print('64 parent/target alignment cases:FI/FA/FO/FU and literal labels exact;three native planes pass. Five actual context sheets viewed;catalogue UI remains offline.')
