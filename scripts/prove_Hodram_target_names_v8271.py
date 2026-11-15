"""Own-current captain1 startup,12 original getters/six voices andsix complete native style11 nameplanes."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_target_route_context_v8270 import RouteCurrentContext
from scripts.prove_lil_B167_names_v4124b import names as original_names
from scripts.reconcile_lil_B142_B145_voices_v3572 import selectors as original_voices
from scripts.prove_maria_B109_macro_profile_v3507 import expand as original_expand
from scripts import lil_B207_name_style_v6354d as style
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels as original_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_target_names_v8271')
START=Path('work/analysis/Hodram_current_binding_v8270/own_Hodram_startup_andstrict_captain1_context.json')
PRIOR_START=Path('work/analysis/Hodram_current_binding_v8187/own_Hodram_startup_andstrict_captain1_context.json')
BEFORE=Path('work/analysis/Hodram_B137_B45_B46_names_v8192/six_static_speakers12_getters_clean_fields24_synthetic_macro_alignments.json')
INPUT=Path('work/analysis/current_V8259_Hodram_native_v8270/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();start,oldstart,before=map(read,[START,PRIOR_START,BEFORE])
    assert start['actual_frames']==4001 and start['actual_original_captain_ID']==1 and start['all_strict_targetARM9_inverse_Blades_COMMON_directory_and123264_payload_guards_pass']
    assert start['whole_actor_sha256']==oldstart['whole_actor_sha256']
    reports=[read(s['capture_report']) for s in [oldstart,start]]
    assert reports[0]['scripted_input_schedule']==reports[1]['scripted_input_schedule']
    photos=[{p['frame']:p for p in r['frames_captured']} for r in reports];assert set(photos[0])==set(photos[1]) and len(photos[0])==6
    pairs=[]
    for frame in sorted(photos[0]):
        a,b=photos[0][frame],photos[1][frame]
        assert sha(Path(a['path']).read_bytes())==a['PNG_sha256'] and sha(Path(b['path']).read_bytes())==b['PNG_sha256'] and Path(a['path']).read_bytes()==Path(b['path']).read_bytes()
        pairs.append(dict(frame=frame,previous_capture=a['path'],current_capture=b['path'],whole_PNG_sha256=b['PNG_sha256'],whole_frame_equal=True))
    sheet=start['review_sheet'];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    env={**original_names.__globals__,'SELECTED_ACTORS':[1,2,9,16,18,113]};exec(compile(before['source_owned_name_adapter'],__file__+'::unchanged-six-identities','exec'),env)
    getters=ctx.execute(env['names']);ctx.machines.pop()
    old={(r['actor_ID'],r['consumer']):r['text'] for r in before['native_twelve_progressive_andfull_getters']['rows']}
    expected={k:'Gerhard Adernkatz' if k[0]==16 else v for k,v in old.items()}
    assert {(r['actor_ID'],r['consumer']):r['text'] for r in getters['rows']}==expected
    env=dict(original_voices.__globals__);exec(compile(before['source_owned_voice_adapter'],__file__+'::unchanged-captain1-source-voices','exec'),env)
    voices=ctx.execute(env['selectors'],[1,2,9,16,18,113]);ctx.machines.pop()
    assert [(r['source_selector'],r['resolved_actor_ID'],r['original_voice_class']) for r in voices['rows']]==[(r['source_selector'],r['resolved_actor_ID'],r['original_voice_class']) for r in before['native_static_selector_andvoice_resolution']['rows']]
    env=dict(original_expand.__globals__);exec(compile(before['source_owned_macro_adapter'],__file__+'::unchanged-captain1-defaults','exec'),env)
    defaults=ctx.execute(env['expand'],b'FI FA FO',1);ctx.machines.pop()
    assert len(defaults['cases'])==4 and all(bytes.fromhex(c['output_hex'])==b'Hodram Bergstrom Bergstrom Fleet' for c in defaults['cases']) and not ctx.machines
    image=NdsImage.open(start['candidate']);arm=image.read_file('/__arm9__.bin');digest=sha(arm)
    assert digest=='12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b'
    caller=FunctionType(style.style_source_proof.__code__,{**style.style_source_proof.__globals__,'ARM9':digest},argdefs=style.style_source_proof.__defaults__)
    raster=FunctionType(style.native_name_raster.__code__,{**style.native_name_raster.__globals__,'style_source_proof':caller},argdefs=style.native_name_raster.__defaults__)
    pixels=FunctionType(original_pixels.__code__,{**original_pixels.__globals__,'CURRENT_ARM9':digest},argdefs=original_pixels.__defaults__)
    plane_rows=[];sheetimage=Image.new('RGB',(912,480),'#263238');draw=ImageDraw.Draw(sheetimage)
    for i,actor in enumerate([1,2,9,16,18,113]):
        text=expected[actor,'progressive-nameplate'];raw=text.encode('cp932');plane,events,font=raster(arm,raw)
        assert font==image.read_file('/GRP/KANJI.FNT') and plane==pixels(arm,font,events)
        emitted,flushes=original_name_events(events,raw);assert emitted==codes(raw)
        assert all(e['style']==11 and e['y']==0 and 0<=e['x'] and e['x']+6<=216 for e in events)
        width=max(e['x']+6 for e in events);ink={(n%216,n//216) for n,v in enumerate(plane) if v};assert ink and max(y for x,y in ink)<13
        path=ROOT/f'actor{actor}_native_name.bin';path.write_bytes(plane)
        picture=Image.new('RGB',(216,64));picture.putdata([(98,97,98) if v else (250,245,223) for v in plane]);preview=path.with_suffix('.png');picture.save(preview)
        x,y=i%2*456,i//2*160;draw.text((x+3,y+3),f'Actor{actor} {text} offline native',fill='white');sheetimage.paste(picture.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
        plane_rows.append(dict(actor_ID=actor,text=text,input_hex=raw.hex(),native_glyph_events=events,source_owned_final_zero_ink_flushes=flushes,original_pair_flush_width=width,
            native_plane=str(path),native_plane_sha256=sha(plane),preview=str(preview),preview_sha256=sha(preview.read_bytes()),complete_first_internal_final_characters_andbounds=True))
    outsheet=ROOT/'six_current_Hodram_source_speaker_names.png';sheetimage.save(outsheet)
    save(ROOT/'six_current_identities12_getters6_native_nameplanes_own_captain1_context.json',dict(candidate=start['candidate'],candidate_sha256=start['candidate_sha256'],ARM9_sha256=digest,
        current_native_input=str(INPUT),current_native_input_sha256=sha(INPUT.read_bytes()),fresh_ordinary_coldboot_frames=4001,six_whole_startup_RGB_pairs=pairs,
        whole_actors_equal_to_prior_Hodram_context=True,actual_captain=1,startup_sheet=sheet,startup_sheet_directly_viewed=True,
        native_twelve_progressive_andfull_getters=getters,native_six_source_voices=voices,measured_default_macro_lengths=dict(FI=6,FA=9,FO=15),fresh_synthetic_default_macro_alignments=defaults,
        synthetic_default_check_not_source_macro_orcustom_player_name_coverage=True,source_macro_counts=dict(FI=0,FA=0,FO=0),
        name_planes=plane_rows,original_style11_caller_proof=caller(arm),exact_target_hash_bound_local_style_andfont_oracles_no_global_change=True,
        only_Gerhard_two_getter_strings_change_all_other_given_middle_role_surname_values_retained=True,
        all_original_ABI_scratch_unowned4MiB_actor_role_RNG_andinput_guards_preserved=True,
        review_sheet=dict(path=str(outsheet),sha256=sha(outsheet.read_bytes())),six_nameplanes_visual_review_pending=True,
        no_actual_B137_B45_B46_nameheader_body_item_panel_transition_ororiginal_event_activation_claim=True,
        full_catalogue_UI_all207_aliases_custom_names_andhardware_coverage_not_claimed=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_credit=0,new_emulator_runs=1,new_actual_frames=4001,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [START,PRIOR_START,BEFORE,INPUT,Path(style.__file__),Path(__file__)]}))
    print('OwncurrentHodram:6startupRGBpairs/actorsmatch;12getters/sixvoices/fourdefaultalignments/sixnative nameplanes pass;plane directview/actualscenes pending.')
