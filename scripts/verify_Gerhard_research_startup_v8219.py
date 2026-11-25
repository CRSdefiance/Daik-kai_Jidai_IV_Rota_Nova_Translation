"""Own research startup RGB/actors plus fresh native getters; optional surname scenes remain unvisited."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Gerhard_research_route_context_v8218 import RouteCurrentContext
from scripts.prove_lil_B167_names_v4124b import names
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_research_startup_view_v8219')
REFERENCE=Path('work/analysis/Gerhard_reference_v8215/research_image_receipt.json')
CURRENT=Path('work/analysis/Gerhard_research_binding_v8218/own_research_startup_andstrict_captain2_context.json')
PARENT=Path('work/analysis/Lil_Gerhard_current_binding_v8198/own_Lil_startup_andstrict_captain2_context.json')
BEFORE_NAMES=Path('work/analysis/Gerhard_before_names_v8200/four_identities8_getters3_source_voices16_synthetic_Lil_alignments.json')
TARGET_NAMES=Path('work/analysis/Gerhard_target_name_v8210c/owned12byte_input8_getters4_complete_name_planes_Blades_protected.json')
if __name__=='__main__':
    assert not ROOT.exists();ref,current,parent,before,target=map(read,[REFERENCE,CURRENT,PARENT,BEFORE_NAMES,TARGET_NAMES])
    assert current['candidate_sha256']==ref['research_ROM_sha256'] and parent['candidate_sha256']==ref['parent_sha256']
    assert not current['registered_candidate'] and current['all_strict_targetARM9_inverse_COMMON_directory_and123264_payload_guards_pass']
    assert current['actual_frames']==parent['actual_frames']==4001 and current['actual_original_captain_ID']==parent['actual_original_captain_ID']==2
    assert current['whole_actor_sha256']==parent['whole_actor_sha256']
    reports=[]
    for spec in [parent,current]:
        rp=Path(spec['capture_report']);assert sha(rp.read_bytes())==spec['capture_report_sha256'];reports.append(read(rp))
    assert reports[0]['scripted_input_schedule']==reports[1]['scripted_input_schedule']
    photos=[{p['frame']:p for p in report['frames_captured']} for report in reports];assert set(photos[0])==set(photos[1]) and len(photos[0])==6
    pairs=[]
    for frame in sorted(photos[0]):
        a,b=photos[0][frame],photos[1][frame]
        assert sha(Path(a['path']).read_bytes())==a['PNG_sha256'] and sha(Path(b['path']).read_bytes())==b['PNG_sha256']
        assert Path(a['path']).read_bytes()==Path(b['path']).read_bytes()
        pairs.append(dict(frame=frame,parent_capture=a['path'],research_capture=b['path'],whole_PNG_sha256=a['PNG_sha256'],whole_frame_equal=True))
    sheet=current['review_sheet'];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(current['current_native_input'],'unused-no-historical-ROM',ROOT/'own_research_context')
    env={**names.__globals__,'SELECTED_ACTORS':[1,2,9,16]}
    exec(compile(before['source_owned_name_adapter'],__file__+'::own-research-eight-getters','exec'),env)
    getters=ctx.execute(env['names']);ctx.machines.pop();assert not ctx.machines
    old={(r['actor_ID'],r['consumer']):r['text'] for r in target['native_eight_getters']['rows']}
    assert {(r['actor_ID'],r['consumer']):r['text'] for r in getters['rows']}==old
    parentimage=NdsImage.open(ref['parent']);research=NdsImage.open(ref['research_ROM'])
    assert parentimage.read_file('/GRP/KANJI.FNT')==research.read_file('/GRP/KANJI.FNT')
    slot=ref['only_changed_name_span'];at=slot['offset'];arm=research.read_file('/__arm9__.bin')
    assert arm[at:at+12].hex()==slot['target_hex'] and ctx.raw[at:at+12].hex()==slot['target_hex']
    assert ctx.raw[at+12:at+20]==b'Blades\0\0'
    save(ROOT/'own_research_startup6_RGBpairs_actor_equal8_fresh_getters_direct_view.json',dict(
        reference=str(REFERENCE),reference_sha256=sha(REFERENCE.read_bytes()),research_ROM=ref['research_ROM'],research_ROM_sha256=ref['research_ROM_sha256'],
        research_startup=str(CURRENT),research_startup_sha256=sha(CURRENT.read_bytes()),parent_startup=str(PARENT),parent_startup_sha256=sha(PARENT.read_bytes()),
        fresh_ordinary_research_coldboot_frames=4001,parent_frames_reused=4001,no_extra_parent_run=True,
        six_whole_RGB_pairs=pairs,whole_actor_sha256=current['whole_actor_sha256'],actual_original_captain_ID=2,
        directly_viewed_startup_sheet=sheet,viewed=True,complete_Lil_Argot_header_andopening_body_visible=True,
        original_research_input=current['current_native_input'],original_research_input_sha256=current['current_native_input_sha256'],
        native_eight_getters_from_actual_own_research_snapshot=getters,all_original_ABI_scratch_unowned4MiB_guards_preserved=True,
        all8_getter_values_equal_prior_owned_input_proof=True,target_family_bytes_andprotected_Blades_measured_inactual_coldboot_RAM=True,
        no_research_RAM_data_overlay_orborrowed_parent_snapshot=True,font_andall_ARM9_except_owned12_exact_byreference_inverse=True,
        optional_Stockholm_Hamburg_surname_body_andGerhard_header_actual_UI_not_visited=True,
        full_catalogue_UI_hardware_fullroute_custom_names_andnatural_optional_activation_not_claimed=True,
        fullreference_loaders_callers_actual_focused_scenes_policy_atomic_registered_release_pending=True,
        registered_current_V8172_andmainV4701_unchanged=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [REFERENCE,CURRENT,PARENT,BEFORE_NAMES,TARGET_NAMES,Path(__file__)]},
        new_credit=0,new_emulator_runs=1,new_actual_frames=4001,full_goal_complete=False))
    print('Research startup4001:6wholeRGBpairs/wholeactors/captain2 equal;8fresh getters/actualRAM surname+Blades/strict own input/directview pass.No optional scene coverage.')
