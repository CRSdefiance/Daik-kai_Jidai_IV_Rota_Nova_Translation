"""Measure complete native body/name holds and retain every paired trace/RGB difference."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_name_style_v7020 import native_name_raster
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events
from scripts.audit_lil_B221_English_paths_v7004 import body_masks,photos
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/square_shopkeeper_actual_v7024b')
FIXTURE=Path('work/analysis/square_shopkeeper_scenes_v7022/four_complete_static_staged_nameplate_fixtures.json')
NAMES=Path('work/analysis/square_shopkeeper_names_v7021/all_name_field_voice_dynamic_macro_and_complete_native_label_consumers.json')
OLD_FONT=Path('work/analysis/lil_B221_native_pages_v6980c/all14_paragraphs16_complete_native_pages112_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();manifest,names=read(FIXTURE),read(NAMES);target=NdsImage.open(names['research_ROM']);arm=target.read_file('/__arm9__.bin')
    assert sha(arm)==names['target_ARM9_sha256'];font=target.read_file('/GRP/KANJI.FNT')
    adapter=checked_text(read(OLD_FONT)['source_owned_AA5_page_adapter'],{names['source_ARM9_sha256']:names['target_ARM9_sha256']})
    env={**old_pages.__globals__,'expected_pixels':expected_pixels};exec(compile(adapter,__file__+'::exact-target-body-pages','exec'),env)
    ROOT.mkdir(parents=True);native_pages={};name_planes={};evidence={str(p):sha(p.read_bytes()) for p in [FIXTURE,NAMES,OLD_FONT,Path(__file__)]}
    for fixture in manifest['fixtures']:
        for row in fixture['original_text_records']:
            key=row['id'];raw=bytes.fromhex(row['current_text_hex'])[1:]
            assert raw and all(b<128 for b in raw) and not any(m in raw for m in [b'FI',b'FA',b'FO',b'FU'])
            if key in native_pages:assert native_pages[key]['input_hex']==raw.hex();continue
            rendered=env['pages'](arm,font,raw)
            for page in rendered['pages']:
                pixels=bytes.fromhex(page.pop('native_plane_hex'));path=ROOT/(key+f'_page{page["page"]}.bin');path.write_bytes(pixels)
                page.update(native_plane=str(path),native_plane_sha256=sha(pixels))
            native_pages[key]=dict(input_hex=raw.hex(),**rendered)
    values={v['case']:{r['actor_ID']:r['text'] for r in v['name_getters']['rows'] if r['consumer']=='progressive-nameplate'} for v in names['versions']}
    for fixture in manifest['fixtures']:
        for row in fixture['original_text_records']:
            if row['source_selector']==254:continue
            word=values[fixture['version']][row['source_selector']]
            if word in name_planes:continue
            raw=word.encode('cp932');pixels,events,f=native_name_raster(arm,raw);assert pixels==expected_pixels(arm,f,events)
            visible,flushes=original_name_events(events,raw);assert visible==codes(raw) and all(e['y']==0 and 0<=e['x'] and e['x']+(6 if e['kind']=='ascii' else 12)<=216 for e in events)
            path=ROOT/(f'name{len(name_planes):02d}.bin');path.write_bytes(pixels)
            name_planes[word]=dict(text=word,plane=str(path),plane_sha256=sha(pixels),events=events,flushes=flushes,complete_first_internal_final_glyphs=True)
    versions=[];pictures=[];captures={};changed_headers=0
    old_B221=read('work/analysis/lil_B221_English_actual_v7004/two_English_choices_all14_speeches30_native_pages_complete_masks_and_source_differences.json')['versions'][0]
    for fixture in manifest['fixtures']:
        case=fixture['case'];run=Path(f'work/analysis/square_shopkeeper_scene_{case}_v7023')
        terminal,plan=read(run/'terminal.json'),read(run/'run_plan.json');cap=Path(plan['capture_folder']);rp,tp=cap/'capture_report.json',cap/'observer/commands.json'
        report,trace=read(rp),read(tp);assert terminal['terminal'] and terminal['observer_instances']==1 and terminal['observer_host_slots_restored']
        assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes())
        assert report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
        assert not report['hardware_device_verification'] and not report['goal_complete'] and not any(v for k,v in report.items() if k.startswith('synthetic_'))
        assert plan['explicit_B22_entry_ROM_fixture'] and plan[f'source_event{fixture["source_block"]}_not_naturally_selected']
        assert plan[f'all{fixture["original_source_command_count"]}_source_commands_retained']
        assert sha(Path(plan['original_inputs']).read_bytes())==plan['inputs_sha256'] and report['scripted_input_schedule']==read(plan['original_inputs'])
        assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
        bank=IlnkContainer.parse(NdsImage.open(fixture['research_ROM']).read_file('/data/SC2.DK4')).blocks
        assert bank[22].hex()==fixture['fixture_block_hex'];captured=photos(report);captures[case]=captured
        body_cache={f:body_masks(im) for f,(_,im) in captured.items()}
        expected={c['offset']:c for c in fixture['all_stored_fixture_commands']};texts={t['fixture_command_offset']:t for t in fixture['original_text_records']}
        pairs=[];panels=[];following=[]
        for row in trace['rows']:
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
            source=row['source'];assert source['whole_resident_payload_exact_ROM'] and source['actual_sha256']==sha(bank[source['block']])
            if row['kind']!='after_command':continue
            entry=trace['rows'][row['entry_row']]
            if source['block']!=22:
                following.append(dict(block=source['block'],offset=entry['source']['instruction_offset'],word=source['first_word'],frame=row['frame'],result=row['result_words']));continue
            at=entry['source']['instruction_offset'];command=expected[at];word=source['first_word']
            assert word==command['word'] and bank[22][at:at+command['native_extent']].hex()==command['whole_command_hex']
            # Relative commands return the native selected span; their stored bytes
            # and exact original destinations are already independently preserved.
            if word not in [0x100,0x200,0x300]:assert row['decoded_length']==command['native_extent']
            pair=dict(offset=at,word=word,start=entry['frame'],returned=row['frame'],result=row['result_words'],UI_after=row['native_UI_request_words'],
                before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],decoded_length=row['decoded_length']);pairs.append(pair)
            if at not in texts:continue
            t=texts[at];native=native_pages[t['id']];page_masks=[]
            for page in native['pages']:
                pixels=Path(page['native_plane']).read_bytes();assert sha(pixels)==page['native_plane_sha256']
                page_masks.append([{(i%216,i//216) for i,v in enumerate(pixels) if v==color} for color in [1,15]])
            name=None if t['source_selector']==254 else values[fixture['version']][t['source_selector']]
            if name:
                p=name_planes[name];pixels=Path(p['plane']).read_bytes();assert sha(pixels)==p['plane_sha256'];nameink={(i%216,i//216) for i,v in enumerate(pixels) if v}
                span=max(17,len(name.encode('cp932')))*6+8;assert span<=224
            holds=[[] for _ in page_masks];nameholds=[]
            for frame,(photo,im) in captured.items():
                if not entry['frame']<frame<row['frame']:continue
                complete_name=name is None or {(x-4,y) for y in range(13) for x in range(span) if im.getpixel((12+x,276+y))==(98,97,98)}==nameink
                if name is not None and complete_name:nameholds.append(dict(frame=frame,capture=photo['path'],sha256=photo['PNG_sha256']))
                for index,mask in enumerate(page_masks):
                    if body_cache[frame]==mask:
                        assert complete_name,(case,t['id'],name,frame)
                        holds[index].append(dict(frame=frame,capture=photo['path'],sha256=photo['PNG_sha256']))
            assert all(holds),(case,t['id'],'missing complete native page',list(map(len,holds)))
            if name is not None:assert nameholds,(case,t['id'],'missing name')
            for index,h in enumerate(holds):
                if fixture['version']=='target':pictures.append(dict(case=case,id=t['id'],page=index+1,name=name,**h[-1]))
            if fixture['version']=='target' and t['source_selector']==fixture['target_actor']:changed_headers+=1
            panels.append(dict(id=t['id'],actor_ID=t['source_selector'],name=name,start=entry['frame'],returned=row['frame'],native_pages=len(holds),complete_page_holds=holds,complete_name_holds=nameholds))
        expected_offsets=list(expected) if fixture['scene']=='static' else [p['fixture_offset'] for p in old_B221['command_pairs']]
        assert [p['offset'] for p in pairs]==expected_offsets and pairs[-1]['word']==0 and pairs[-1]['result']==[0,0]
        assert len(panels)==(17 if fixture['scene']=='static' else 13)
        versions.append(dict(case=case,scene=fixture['scene'],version=fixture['version'],command_pairs=pairs,panels=panels,exit_frame=pairs[-1]['returned'],
            actual_complete_page_observations=sum(p['native_pages'] for p in panels),actual_complete_body_holds=sum(sum(map(len,p['complete_page_holds'])) for p in panels),
            actual_complete_name_holds=sum(len(p['complete_name_holds']) for p in panels),following_commands=following,report=str(rp),report_sha256=sha(rp.read_bytes()),
            trace=str(tp),trace_sha256=sha(tp.read_bytes()),final_RAM_snapshot=report['read_only_RAM_snapshot']))
        for p in [run/'terminal.json',run/'run_plan.json',Path(plan['original_inputs']),rp,tp]:evidence[str(p)]=sha(p.read_bytes())
    comparisons=[]
    for scene in ['static','staged']:
        parent,child=[next(v for v in versions if v['case']==scene+'_'+label) for label in ['parent','target']]
        diffs=[]
        for a,b in zip(parent['command_pairs'],child['command_pairs'],strict=True):
            assert a['offset']==b['offset'] and a['word']==b['word']
            fields=[k for k in a if a[k]!=b[k]]
            if fields:diffs.append(dict(offset=a['offset'],word=a['word'],different_fields=fields,before=a,after=b))
            assert a['result']==b['result'] and a['UI_after']==b['UI_after'] and a['decoded_length']==b['decoded_length']
        left,right=[captures[scene+'_'+label] for label in ['parent','target']];assert left.keys()==right.keys();rgb=[]
        for frame in left:
            a,b=[z[frame][1] for z in [left,right]];whole=a.tobytes()==b.tobytes();outside=True
            for rect in [(0,0,256,272),(0,290,256,384),(0,272,8,290),(240,272,256,290)]:outside &= a.crop(rect).tobytes()==b.crop(rect).tobytes()
            if not whole:rgb.append(dict(frame=frame,all_differences_within_nameplate_strip=outside,parent=left[frame][0]['path'],target=right[frame][0]['path']))
        comparisons.append(dict(scene=scene,command_differences=diffs,RGB_differences=rgb,total_sampled_RGB_pairs=len(left),normal_exit_frames=[parent['exit_frame'],child['exit_frame']],
            no_full_RAM_final_components_future_or_complete_causal_equivalence_claim=True))
    assert changed_headers==9 and len(pictures)==32
    sheets=[]
    for scene in ['static','staged']:
        selected=[p for p in pictures if p['case']==scene+'_target']
        for start in range(0,len(selected),6):
            chunk=selected[start:start+6];sheet=Image.new('RGB',(768,820),'#263238');draw=ImageDraw.Draw(sheet)
            for i,p in enumerate(chunk):
                x,y=i%3*256,i//3*410;draw.text((x+2,y+3),f'{p["id"].split("_B")[-1]} p{p["page"]} f{p["frame"]}',fill='white');sheet.paste(Image.open(p['capture']).convert('RGB'),(x,y+24))
            path=ROOT/(scene+f'_target_sheet{start//6+1}.png');sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),panes=chunk))
    save(ROOT/'four_full_scenes_complete_native_bodies_names_commands_and_measured_differences.json',dict(fixtures=str(FIXTURE),fixtures_sha256=sha(FIXTURE.read_bytes()),native_names=str(NAMES),native_names_sha256=sha(NAMES.read_bytes()),
        native_body_source_adapter=adapter,native_pages=native_pages,native_name_planes=name_planes,versions=versions,comparisons=comparisons,
        target_changed_nameplate_observations=changed_headers,target_complete_page_observations=32,target_speech_observations=30,
        all_complete_source_owned_commands_retained_and_both_normal_returns_observed=True,all_native_body_glyphs_black_gray_and_nameplate_first_internal_final_glyphs_and_blank_guards_pass=True,
        no_stale_old_label_ink_wrap_or_nameplate_pagination=True,new_cold_boots=4,new_frames=64004,all_jobs_terminal_and_reaped=True,
        original_schedules_no_RAM_roles_roster_funds_RNG_conditions_or_results_forced=True,all_measured_timing_RNG_UI_and_RGB_differences_retained=True,
        initialized_scenes_not_natural_activation_original_location_earned_progress_full_effects_full_route_or_hardware=True,
        original_A000_C200_opaque_effect_semantics_not_newly_certified=True,full_catalogue_UI_and_every_conditional_nameplate_not_visited=True,
        no_new_prose_approval_or_duplicate_credit=True,B189_early_line_breaks_separate_retrospective_editorial_lead=True,
        review_sheets=sheets,visual_review_pending=True,evidence=evidence,new_review_credit=0,full_goal_complete=False))
    print(dict(target_speech_observations=30,target_pages=32,changed_nameplates=changed_headers,review_sheets=len(sheets),comparison_differences=[len(c['command_differences']) for c in comparisons],visual_review_pending=True),flush=True)
