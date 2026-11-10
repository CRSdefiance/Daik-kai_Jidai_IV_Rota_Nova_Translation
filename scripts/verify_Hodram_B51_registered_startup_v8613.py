"""Record direct own registered startup review and exact reuse of unchanged native names/code."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B51_registered_startup_view_v8613')
CURRENT=Path('work/analysis/Hodram_B51_registered_binding_v8612/own_Hodram_startup_andstrict_captain1_context.json')
PARENT=Path('work/analysis/Hodram_B50_registered_binding_v8546/own_Hodram_startup_andstrict_captain1_context.json')
RELEASE=Path('work/analysis/Hodram_B51_release_v8610/registered_release_verification.json')
NAMES=Path('work/analysis/Hodram_target_names_v8271/six_current_identities12_getters6_native_nameplanes_own_captain1_context.json')
if __name__=='__main__':
    assert not ROOT.exists();current,parent,release,names=map(read,[CURRENT,PARENT,RELEASE,NAMES])
    assert current['candidate_sha256']==release['candidate_sha256'] and current['actual_frames']==parent['actual_frames']==4001
    assert current['actual_original_captain_ID']==parent['actual_original_captain_ID']==1 and current['all_strict_targetARM9_inverse_Blades_COMMON_directory_and123264_payload_guards_pass']
    assert current['whole_actor_sha256']==parent['whole_actor_sha256']
    old,new=[NdsImage.open(r['candidate']) for r in [parent,current]]
    assert old.read_file('/__arm9__.bin')==new.read_file('/__arm9__.bin') and old.read_file('/COMMON/MESFILE.DK4')==new.read_file('/COMMON/MESFILE.DK4') and old.read_file('/GRP/KANJI.FNT')==new.read_file('/GRP/KANJI.FNT')
    assert sha(new.read_file('/__arm9__.bin'))==names['ARM9_sha256']==release['ARM9_sha256']
    reports=[]
    for spec in [parent,current]:
        rp=Path(spec['capture_report']);assert sha(rp.read_bytes())==spec['capture_report_sha256'];reports.append(read(rp))
    assert reports[0]['scripted_input_schedule']==reports[1]['scripted_input_schedule']
    photos=[{p['frame']:p for p in r['frames_captured']} for r in reports];assert set(photos[0])==set(photos[1]) and len(photos[0])==6
    pairs=[]
    for frame in sorted(photos[0]):
        a,b=photos[0][frame],photos[1][frame]
        assert sha(Path(a['path']).read_bytes())==a['PNG_sha256'] and sha(Path(b['path']).read_bytes())==b['PNG_sha256'] and Path(a['path']).read_bytes()==Path(b['path']).read_bytes()
        pairs.append(dict(frame=frame,parent_capture=a['path'],registered_capture=b['path'],whole_PNG_sha256=b['PNG_sha256'],whole_frame_equal=True))
    sheet=current['review_sheet'];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    rp=Path(current['capture_report']);report=read(rp);snap=next(s for s in report['read_only_capture_RAM_snapshots'] if s['frame']==4000);raw=Path(snap['path']).read_bytes()
    assert sha(raw)==snap['sha256'] and raw[1435252:1435264]==b'Adernkatz\0\0\0' and raw[1435264:1435272]==b'Blades\0\0'
    for row in names['name_planes']:assert sha(Path(row['native_plane']).read_bytes())==row['native_plane_sha256']
    ROOT.mkdir(parents=True);save(ROOT/'own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json',dict(
        candidate=current['candidate'],candidate_sha256=current['candidate_sha256'],profile=release['profile'],viewed=True,
        directly_viewed_sheet=sheet,six_whole_RGB_pairs=pairs,whole_actors_equal=True,actual_original_captain_ID=1,fresh_ordinary_registered_coldboot_frames=4001,
        current_native_input=current['current_native_input'],current_native_input_sha256=current['current_native_input_sha256'],
        target_family12_andprotected_Blades8_measured_inactual_coldboot_RAM=True,
        exact_unchanged_twelve_name_getters_and_six_native_nameplanes_reused=str(NAMES),exact_unchanged_name_proof_sha256=sha(NAMES.read_bytes()),
        reuse_requires_identical_complete_ARM9_COMMON_font_andwhole_actual_actors=True,
        no_repeat_name_getter_orfont_calls_andno_historical_RAM_overlay=True,
        no_natural_optional_B51_activation_catalogue_UI_customnames_fullroute_orhardware_claim=True,
        new_credit=0,new_emulator_runs=1,new_actual_frames=4001,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,PARENT,RELEASE,NAMES,Path(__file__)]}))
    print('Own registered V8609 Hodram:4001ordinaryframes/six exactstartup RGBpairs/wholeactors/current name12+Blades8;directly viewed.Names/getters reused through exactcode/font/actor binding.')
