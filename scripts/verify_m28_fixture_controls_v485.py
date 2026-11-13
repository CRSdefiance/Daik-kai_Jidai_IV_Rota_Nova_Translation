"""Matched playback controls; no rendering credit for stopped current fixtures."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_fleet_release_v375 import files

ROOT=Path('work/analysis/m28_planes_v485')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    current=Path('out/all_routes_combined_v484_candidate.nds')
    parent=NdsImage.open(current)
    digest=sha(current.read_bytes())
    assert digest=='f2036bafc3736a353cb0a2de8f40bd5eee8bed3cd16e779f68e3ebb1914b875c'
    source=parent.read_file('/FLS/M28.fls')
    texture=FlsArchive(source).texture(46)
    points=[(12+i%texture.width,167+i//texture.width,tuple(v>>3 for v in texture.palette[n][:3]))
            for i,n in enumerate(texture.indices)if n]
    assert len(points)==3047
    specs=[('v326','movie_gpu_fixture_v336/m28_fixture_manifest.json','m28_control_v326_v485'),
           ('v342','m28_planes_v485/v342_control_manifest.json','m28_control_v342_v485'),
           ('v360','m28_planes_v485/v360_control_manifest.json','m28_control_v360_v485'),
           ('v474','m28_planes_v485/v474_control_manifest.json','m28_control_v474_v485'),
           ('v484','m28_planes_v485/fixture_manifest.json','m28_planes_v485_touch'),
           ('v484-mode0','m28_planes_v485/mode0_fixture_manifest.json','m28_planes_mode0_v485')]
    cases=[]
    options=None
    inputs=read(ROOT/'inputs.json')
    for label,manifest_name,folder in specs:
        manifest_path=Path('work/analysis')/manifest_name
        manifest=read(manifest_path)
        fixture=Path(manifest['research_ROM'])
        report_path=Path('work/emulation_v193')/folder/'capture_report.json'
        report=read(report_path)
        assert sha(fixture.read_bytes())==manifest['research_ROM_sha256']==report['ROM_sha256']
        original=NdsImage.open(manifest['parent']);image=NdsImage.open(fixture)
        assert sha(Path(manifest['parent']).read_bytes())==manifest['parent_sha256']
        before,after=files(original),files(image)
        permitted=['/FLS/M20.fls','/__arm9__.bin']if label.endswith('mode0')else['/FLS/M20.fls']
        assert [p for p in before if before[p]!=after[p]]==permitted
        assert original.read_file('/FLS/M28.fls')==image.read_file('/FLS/M20.fls')==source
        assert original.read_file('/__arm9__.bin')[0xFD000:0x100E90]==parent.read_file('/__arm9__.bin')[0xFD000:0x100E90]
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['scripted_start_frame']==-1 and report['scripted_input_schedule']==inputs
        assert not report.get('battery_save_preloaded') and not report.get('synthetic_inventory_fixtures')
        if options is None:options=report['core_options']
        assert report['core_options']==options and report['core_DLL_sha256']=='42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
        for shot in report['frames_captured']:
            assert sha(Path(shot['path']).read_bytes())==shot['PNG_sha256']
        shot=next(r for r in report['frames_captured']if r['frame']==3700)
        im=Image.open(shot['path']).convert('RGB').point(lambda x:x>>3)
        pixels=im.load()
        matched=sum(pixels[x,y]==color for x,y,color in points)
        complete=matched==len(points)
        assert complete==(label in ('v326','v342'))
        native=read(Path('work/emulation_v193')/folder/'native_state/native_state.json')
        assert native['state_loaded']is False and native['read_only_export']
        cases.append({'control':label,'manifest':str(manifest_path),'report':str(report_path),'report_sha256':sha(report_path.read_bytes()),
                      'frame3700':shot,'complete_Hodram_name_plane_exact':complete,'expected_ink_shadow_pixels':len(points),
                      'matching_pixels':matched,'terminal_ARM9_PC':native['ARM9_instruction_address'],
                      'ending_unlock_or_complete_movie_credit':False})
    mode=read(ROOT/'original_mode_domain.json')
    assert len(mode['cases'])==33 and mode['cases'][20]['native_mode']==1 and mode['cases'][28]['native_mode']==0
    proof={'candidate':str(current),'candidate_sha256':digest,'production_ROM_changed':False,
           'movie_source_sha256':sha(source),'source_M28_exact_in_all_controls':True,'original_movie_engine_range_unchanged':True,
           'identical_emulator_options_and_inputs':True,'cases':cases,'original_mode_domain':str(ROOT/'original_mode_domain.json'),
           'fixture_failure_interval':'afterV342 and no later thanV360; exact cause unproven',
           'latest_Square_repair_not_first_introduction_of_fixture_failure':True,
           'limits':['File substitution is not the original movie caller or normal ending unlock.',
                     'The setup override does not establish exact cause or normal M28 failure.',
                     'Terminal PCs are diagnostics; they do not prove every prior frame or the reason for stopping.'],
           'all20_progressive_name_planes_still_pending_current_GPU_coverage':True,
           'all22_historical_requirements_retained':True,'all18_plaques_incomplete':True,'full_goal_complete':False}
    (ROOT/'control_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('Matched controls: V326/V342 names exact; V360/V474/V484 fixtures do not display it. Production unchanged.')


if __name__=='__main__':
    main()
