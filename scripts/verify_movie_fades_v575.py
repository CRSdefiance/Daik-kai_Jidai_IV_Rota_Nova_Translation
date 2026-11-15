"""Bounded native fade/color checks using black and white coverage controls."""
import json
from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import rom_files
from scripts.prepare_movie_fade_controls_v575 import EDITED, FILE, ROM, ROOT
from scripts.verify_m28_progressive_v503 import points
from scripts.verify_source_plaque_grain_v542 import capture_report

CAPTURE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    fixture=read(ROOT/'color_control_fixtures.json');rom=NdsImage.open(ROM)
    digest=sha(ROM.read_bytes());assert digest==fixture['production_ROM_sha256']
    archive=FlsArchive(rom.read_file(FILE));reports={};tables={}
    paths={'actual':ROM}|{f['kind']:Path(f['ROM']) for f in fixture['fixtures']}
    for kind,path in paths.items():
        altered=NdsImage.open(path)
        if kind!='actual':
            a,b=rom_files(rom),rom_files(altered)
            assert a.keys()==b.keys() and [p for p in a if a[p]!=b[p]]==[FILE]
            assert sha(path.read_bytes())==next(f['ROM_sha256'] for f in fixture['fixtures'] if f['kind']==kind)
        report=capture_report(CAPTURE/f'movie_fades_v575_{kind}',sha(path.read_bytes()))
        assert report['frames']==5000 and not report['scripted_input_schedule'] and not report.get('battery_save_preloaded')
        assert not any(k.startswith('synthetic_') for k in report)
        assert report['core_options']==reports.get('actual',report)['core_options']
        reports[kind]=report
        tables[kind]={s['frame']:s for s in report['frames_captured'] if 'cold_boot' in s['path']}
    frames=sorted(tables['actual']);assert len(frames)==1251
    assert all(sorted(t)==frames for t in tables.values())
    fields={}
    for i in EDITED:
        ox,oy=(0,48) if i==4 else (0,82) if i==5 else (12,167)
        fields[i]={(x+ox,y+oy):c for x,y,c in points(archive.texture(i))}
        assert all(0<=x<256 and 0<=y<192 for x,y in fields[i])
    name_groups=[]
    for i in range(27,47):
        found=next((g for g in name_groups if g['field']==fields[i]),None)
        if found:found['textures'].append(i)
        else:name_groups.append({'textures':[i],'field':fields[i]})
    assert len(name_groups)==19 and [g['textures'] for g in name_groups if len(g['textures'])>1]==[[30,31]]
    union=set().union(*(set(f) for f in fields.values()));assert len(union)==11425
    assert not (set(fields[4])&set(fields[5]))
    assert not ((set(fields[4])|set(fields[5]))&set(fields[46]))
    mask=Image.new('L',(256,384));mp=mask.load()
    for p in union:mp[p]=255
    frame_cases=[];opaque_names={};opaque_titles={};modulated=[];max_error=0;checked_color_channels=0
    best_midfade=None;largest_response=None
    for frame in frames:
        ims={k:Image.open(t[frame]['path']).convert('RGB').point(lambda v:v>>3) for k,t in tables.items()}
        a,b,w=(ims[k] for k in ('actual','black','white'))
        difference=ImageChops.difference(b,w)
        for other in (w,a):
            outside=ImageChops.difference(b,other);outside.paste((0,0,0),(0,0),mask)
            assert outside.getbbox() is None,('change outside English coverage',frame,outside.getbbox())
        if difference.getbbox() is None:
            assert a.tobytes()==b.tobytes()==w.tobytes()
            frame_cases.append({'frame':frame,'black_white_influence_points':0,'entire_three_screens_exact':True})
            continue
        ap,bp,wp=(im.load() for im in (a,b,w))
        active={p for p in union if bp[p]!=wp[p]}
        assert active
        assert all(wp[p][ch]>=bp[p][ch] for p in active for ch in range(3))
        unaffected=union-active
        assert all(ap[p]==bp[p]==wp[p] for p in unaffected)

        def error(field, *, active=active, ap=ap, bp=bp, wp=wp):
            if any(p not in field for p in active if p[1]>=167):return None
            worst=0
            for p,c in field.items():
                if p not in active:continue
                for ch in range(3):
                    # Rounded endpoint interpolation at native 5-bit precision.
                    expected=(bp[p][ch]*31+(wp[p][ch]-bp[p][ch])*c[ch]+15)//31
                    worst=max(worst,abs(ap[p][ch]-expected))
            return worst

        title_cases=[]
        for i in (4,5):
            active_title=active&set(fields[i])
            if not active_title:continue
            # Title fields must be checked independently of the name coverage.
            worst=0
            for p in active_title:
                c=fields[i][p]
                for ch in range(3):
                    expected=(bp[p][ch]*31+(wp[p][ch]-bp[p][ch])*c[ch]+15)//31
                    worst=max(worst,abs(ap[p][ch]-expected))
            assert worst<=1,('title endpoint model',frame,i,worst)
            max_error=max(max_error,worst);checked_color_channels+=3*len(active_title)
            opaque=active_title==set(fields[i]) and all(ap[p]==c for p,c in fields[i].items())
            if opaque:opaque_titles.setdefault(i,frame)
            title_cases.append({'texture':i,'influence_points':len(active_title),'max_native_channel_error':worst,
                                'complete_source_colors_exact':opaque})
        name_active={p for p in active if p[1]>=167};name_case=None
        if name_active:
            candidates=[(error(g['field']),n) for n,g in enumerate(name_groups)]
            candidates=[(e,n) for e,n in candidates if e is not None]
            assert candidates,('name coverage outside any complete source state',frame)
            worst,n=min(candidates);assert worst<=1,('name endpoint model',frame,worst)
            group=name_groups[n];max_error=max(max_error,worst);checked_color_channels+=3*len(name_active)
            opaque=name_active==set(group['field']) and all(ap[p]==c for p,c in group['field'].items())
            if opaque:opaque_names.setdefault(n,frame)
            name_case={'textures':group['textures'],'influence_points':len(name_active),
                       'max_native_channel_error':worst,'complete_source_colors_exact':opaque}
        partial=[p for p in active if any(0<wp[p][ch]-bp[p][ch]<31 for ch in range(3))]
        average=sum(sum(wp[p][ch]-bp[p][ch] for ch in range(3)) for p in active)/(len(active)*3)
        case={'frame':frame,'black_white_influence_points':len(active),'partially_modulated_points':len(partial),
              'average_native_endpoint_response':average,'title_cases':title_cases,'name_case':name_case}
        frame_cases.append(case)
        if partial:
            modulated.append(frame)
            score=abs(average-15.5)
            if best_midfade is None or score<best_midfade[0]:best_midfade=(score,case)
        if largest_response is None or average>largest_response['average_native_endpoint_response']:largest_response=case
        if frame%400==0:print(f'Checked capture at frame{frame}',flush=True)
    assert set(opaque_titles)=={4,5} and len(opaque_names)==19
    assert modulated and best_midfade is not None
    for name in ('graphics_completion_campaign_v1.json','graphics_visual_audit_v150.json'):
        plaques=read(Path('translations')/name)['plaque_style_v247']['ongoing_plaque_inventory']
        assert len(plaques)==18 and all(p['fully_completed'] is False for p in plaques)
    assert len(read('translations/graphics_completion_requirements_v313.json')['historical_pending_items_retained'])==22
    proof={'candidate':str(ROM),'candidate_sha256':digest,'movie':FILE,'movie_sha256':sha(rom.read_file(FILE)),
           'fixture_manifest':str(ROOT/'color_control_fixtures.json'),'fixture_manifest_sha256':sha((ROOT/'color_control_fixtures.json').read_bytes()),
           'reports':{k:{'path':str(CAPTURE/f'movie_fades_v575_{k}'/'capture_report.json'),
                         'sha256':sha((CAPTURE/f'movie_fades_v575_{k}'/'capture_report.json').read_bytes())} for k in reports},
           'three_cold_boots_no_inputs_saves_or_slot_substitution':True,'unique_captures_per_run':len(frames),'frames_per_run':5000,
           'all11425_source_coverage_points_fit_native_screen':True,'all_unowned_screen_pixels_exact_between_controls_and_current':True,
           'unowned_points_per_capture':256*384-len(union),'unowned_comparison_points':2*len(frames)*(256*384-len(union)),
           'native_color_channels_checked':checked_color_channels,'rounded_native_5bit_endpoint_tolerance':1,
           'maximum_observed_native_channel_error':max_error,'modulated_captures':modulated,
           'complete_production_color_title_frames':opaque_titles,
           'all19_complete_production_color_name_states':[{'textures':g['textures'],'first_exact_frame':opaque_names[n],
                                                          'complete_ink_shadow_pixels':len(g['field'])} for n,g in enumerate(name_groups)],
           'representative_midfade':best_midfade[1],'largest_response':largest_response,'capture_cases':frame_cases,
           'scope':'Exact spatial influence and bounded rounded endpoint-color model at four-frame cadence. It does not extract internal GPU alpha/vertex attributes, prove unsampled frames or distinguish identical textures30/31.',
           'production_ROM_modified':False,'all18_plaques_remain_incomplete':True,'all22_historical_requirements_retained':True,
           'hardware_device_verification':False,'full_goal_complete':False}
    (ROOT/'native_fade_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print(f'V575:1251 synchronized captures; {len(modulated)} modulated captures; all19 name states and both titles complete; maximum rounded native color error{max_error}; all unowned screen pixels exact.')


if __name__=='__main__':main()
