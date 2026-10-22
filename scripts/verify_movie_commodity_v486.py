"""Matched constructor/allocation controls; prototypes are not release fixes."""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT=Path('work/analysis/movie_commodity_v486')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    current=Path('out/all_routes_combined_v484_candidate.nds')
    digest=sha(current.read_bytes())
    assert digest=='f2036bafc3736a353cb0a2de8f40bd5eee8bed3cd16e779f68e3ebb1914b875c'
    movie=NdsImage.open(current).read_file('/FLS/M28.fls')
    texture=FlsArchive(movie).texture(46)
    points=[(12+i%texture.width,167+i//texture.width,tuple(v>>3 for v in texture.palette[n][:3]))
            for i,n in enumerate(texture.indices)if n]
    cases=[]
    options=None
    expected=[('bank_only',True),('data_only',True),('without_town_hooks',True),
              ('without_market_hooks',False),('without_town_canvas',True),('without_town_painter',False),
              ('clone_v360',False),('allocation_only_v484',False),('allocate_16',True),('allocate_4096',False)]
    for label,complete_expected in expected:
        manifest=read(ROOT/f'{label}_manifest.json')
        fixture=Path(manifest['research_ROM'])
        folder=Path('work/emulation_v193')/f'movie_commodity_v486_{label}'
        report_path=folder/'capture_report.json';r=read(report_path)
        assert r['ROM_sha256']==sha(fixture.read_bytes())==manifest['research_ROM_sha256']
        assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors'] and r['frames']==6000
        assert r['scripted_input_schedule']==read(ROOT/'inputs.json')
        if options is None:options=r['core_options']
        assert r['core_options']==options
        assert NdsImage.open(fixture).read_file('/FLS/M20.fls')==movie
        for shot in r['frames_captured']:assert sha(Path(shot['path']).read_bytes())==shot['PNG_sha256']
        shot=next(x for x in r['frames_captured']if x['frame']==3700)
        image=Image.open(shot['path']).convert('RGB').point(lambda x:x>>3);p=image.load()
        matches=sum(p[x,y]==rgb for x,y,rgb in points);complete=matches==3047
        assert complete==complete_expected,label
        raw=(folder/'final_arm9_ram.bin').read_bytes()
        header=list(struct.unpack_from('<5I',raw,0x022BD774-0x02000000))
        cases.append({'variant':label,'manifest':str(ROOT/f'{label}_manifest.json'),
                      'report':str(report_path),'report_sha256':sha(report_path.read_bytes()),'frame3700':shot,
                      'Hodram_plane46_complete_3047_pixels':complete,'matching_pixels':matches,
                      'terminal_shared_numeric_bitmap_header':header})
    # Compare all genuine town prototype frames as pixels; the terminal report
    # contains a duplicate5900 capture, so do not infer equality from filenames.
    reference=read('work/emulation_v193/square_cells_v484/capture_report.json')
    prototype=read('work/emulation_v193/town_private_v486/capture_report.json')
    a={x['frame']:x for x in reference['frames_captured']};b={x['frame']:x for x in prototype['frames_captured']}
    differing=[f for f in a if a[f]['PNG_sha256']!=b[f]['PNG_sha256']]
    proof={'candidate':str(current),'candidate_sha256':digest,'production_ROM_changed':False,'cases':cases,
           'town_constructor_call_isolated':0x020B59AC,'source_shared_header':0x022BD774,
           'original_shared_image_size':[228,72],'legacy_enlarged_height':132,'legacy_allocation_bytes':15104,
           'removing_constructor_restores_matched_preview_with_translated_data_retained':True,
           'allocation_size_sensitivity':{'16_bytes':'name_plane_matches','4096_bytes':'name_plane_does_not_match','15104_bytes':'name_plane_does_not_match'},
           'capacity_exhaustion_vs_allocation_layout_exact_mechanism_unproven':True,
           'private_header_native_proof':str(ROOT/'private_native_proof.json'),
           'private_header_prototype_does_not_restore_movie':True,
           'genuine_town_prototype_unchanged_frame_count':len(a)-len(differing),'genuine_town_prototype_differing_frames':differing,
           'invalid_hooks_only_controls_excluded_missing_scattered_helper_code':True,
           'normal_ending_unlock_or_caller_not_proven':True,'all22_requirements_retained':True,'all18_plaques_incomplete':True,'full_goal_complete':False}
    (ROOT/'control_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('Town constructor isolated;allocation-size sensitivity verified;no production fix or rendering clearance.')


if __name__=='__main__':
    main()
