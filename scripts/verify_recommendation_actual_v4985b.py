"""Audit paired actual reward transitions,whole text planes and disclosed input fixtures."""
from pathlib import Path
import struct,json
from PIL import Image,ImageDraw,ImageChops
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_recommendation_stock_fixture_v4983 import assign
from scripts.review_early_shop_breaks_v4763e import expected_plane
from scripts.primary_town_native_font_v2102 import font_tools,glyph_codes
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.probe_button_prompt_native import machine,BASE,STACK
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.review_lil_B183_actual_v4961 import state,models,persistent_objects,tasks,calendar,native_json
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/recommendation_actual_verification_v4985')
APPROVAL=Path('work/analysis/earlier_common_wraps_approval_v4979/four_retentions_one_reflow_source_native_approval.json')
if __name__=='__main__':
    assert not ROOT.exists();approval=read(APPROVAL);versions=[];photos=[];final=[];paths=[APPROVAL,Path(__file__)]
    for case in ['current','reviewed']:
        rp=Path('work/analysis/recommendation_actual_v4984c_'+case);plan=read(rp/'run_plan.json');terminal=read(rp/'terminal.json')
        report=read(terminal['report']);obs=read(terminal['observer']);image=NdsImage.open(plan['ROM']);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
        assert terminal['terminal'] and sha(Path(plan['ROM']).read_bytes())==report['ROM_sha256']==plan['ROM_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and report['frames']==12001
        assert sha(Path(terminal['report']).read_bytes())==terminal['report_sha256'] and not obs['errors'] and not obs['mismatches']
        assert obs['all_host_slots_restored_and_core_file_exact'] and len(obs['synthetic_recommendation_reward_input_fixtures'])==1
        fixture=obs['synthetic_recommendation_reward_input_fixtures'][0]
        assert fixture==report['synthetic_recommendation_reward_input_fixtures'][0]
        assert fixture['PC']==0x020BBCA4 and fixture['original_sale_hold_total']==2 and fixture['supplied_reward_quantity_input']==16
        assert fixture['supplied_qualification_result']==2 and fixture['supplied_bonus_flag']==1
        spans={k:Path(v['path']).read_bytes() for k,v in fixture['snapshots'].items()}
        for k,v in fixture['snapshots'].items():assert len(spans[k])==v['bytes'] and sha(spans[k])==v['sha256'];paths.append(Path(v['path']))
        before_cpu=struct.unpack('<32I',spans['before_CPU']);after_cpu=struct.unpack('<32I',spans['after_CPU'])
        assert after_cpu[4]==2 and after_cpu[8]==16 and all(before_cpu[i]==after_cpu[i] for i in range(32) if i not in [4,8])
        assert before_cpu[8]==2 and before_cpu[2]==after_cpu[2]==0x020BBCA4
        for k in ['CPU','WRAM','DTCM','ITCM']:
            diff=[i for i,(a,b) in enumerate(zip(spans['before_'+k],spans['after_'+k],strict=True)) if a!=b]
            assert diff==fixture['exact_changed_offsets'][k]
            allowed=(set(range(16,20))|set(range(32,36))) if k=='CPU' else (set(range(fixture['stack_memory_offset'],fixture['stack_memory_offset']+4)) if k==fixture['stack_memory_kind'] else set())
            assert set(diff)<=allowed
        pause=next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame']==3200);raw=Path(pause['path']).read_bytes()
        assert sha(raw)==pause['sha256'];after,receipt=assign(arm,raw,{'mode':'edge'})
        stock=report['synthetic_market_display_fixtures'];assert len(stock)==1 and stock[0]['frame']==3200
        assert receipt=={k:v for k,v in stock[0].items() if k!='frame'} and len(receipt['changes'])==8
        assert receipt['cargo_product_names']==['Tea','Rum'] and receipt['existing_cargo_hold_count_unchanged_at2']
        assert sha(Path(plan['donor']).read_bytes())==plan['donor_sha256']==report['battery_save_preloaded']['source_sha256']
        rows=[r for r in obs['rows'] if r['source_request']['ID'] in [775,780,766]]
        assert [r['source_request']['ID'] for r in rows]==[775,780,766]
        picture={r['frame']:r for r in report['frames_captured']};photos.append(picture)
        for r in picture.values():assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']
        entries=owned_entries(common,arm,approval['directory_sha256']);cpu=machine(arm)
        cpu.mem_write(0x02387A20,bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]));cpu.mem_write(STACK+0x27C,struct.pack('<I',0x02118480))
        raster,_,_=font_tools(image);holds=[]
        for row in rows:
            n=row['source_request']['ID'];assert row['bounds']==[0,0,228,48] and row['CPU_WRAM_DTCM_ITCM_configuration_exact']
            formatted,lines=native_layout(cpu,entries[n].text,n,(),0x02054014)
            assert formatted.hex()==row['text_hex']
            events=[];plane=raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000,glyph_events=events)
            assert plane==expected_plane(arm,lines,1) and [r['code'] for r in events if r['code']!=32]==glyph_codes(formatted)
            assert all(0<=r['x'] and r['x']+6<=228 and 0<=r['y'] and r['y']+12<=64 for r in events)
            end=min([r['frame'] for r in obs['rows'] if r['frame']>row['frame']]+[12002])
            matched=[]
            expected={(16+i%228,296+i//228) for i,p in enumerate(plane) if p==1}
            for frame,photo in sorted(picture.items()):
                if not row['frame']<frame<end:continue
                rgb=Image.open(photo['path']).convert('RGB')
                actual={(x,y) for y in range(294,356) for x in range(16,244) if rgb.getpixel((x,y))==(0,8,0)}
                if actual==expected:matched.append(dict(frame=frame,capture=photo['path'],capture_sha256=photo['PNG_sha256']))
            assert matched,(case,n,row['frame'],end)
            if n==775:assert len(lines)==(4 if case=='current' else 3)
            holds.append(dict(message_ID=n,font_frame=row['frame'],next_original_message_frame=end,lines=lines,text_hex=formatted.hex(),
                native_plane_sha256=sha(plane),complete_ink_and_blank_paper_match=True,complete_first_internal_final_glyphs_bounds_and_one_page=True,matching_holds=matched))
        snap=report['read_only_RAM_snapshot'];raw=Path(snap['path']).read_bytes();assert sha(raw)==snap['sha256']
        components={f.__name__:f(arm,raw) for f in [state,models,persistent_objects,tasks,calendar]}
        u,get=get_machine(arm,raw);actor_root,captain=get(0xCB184),get(0x7F244);assert captain==1
        final.append(dict(components=components,actor=bytes(u.mem_read(actor_root,0x1A04)),captain=captain,seed=struct.unpack_from('<I',raw,0x168EB8)[0]))
        versions.append(dict(case=case,plan=str(rp/'run_plan.json'),terminal=str(rp/'terminal.json'),report=terminal['report'],observer=terminal['observer'],
            ROM_sha256=plan['ROM_sha256'],holds=holds,qualification_input_fixture=fixture,stock_input_fixture=stock[0],snapshot=snap,
            all_font_rows=[dict(message_ID=r['source_request']['ID'],frame=r['frame']) for r in obs['rows']]))
        paths.extend([rp/'run_plan.json',rp/'terminal.json',Path(terminal['report']),Path(terminal['observer']),Path(snap['path']),Path(pause['path'])])
    assert photos[0].keys()==photos[1].keys()
    comparisons=[]
    for f in sorted(photos[0]):
        a,b=[Image.open(p[f]['path']).convert('RGB') for p in photos]
        comparisons.append(dict(frame=f,nontext_upper_portrait_name_regions_equal=a.crop((0,0,256,294)).tobytes()==b.crop((0,0,256,294)).tobytes(),
            whole_RGB_equal=a.tobytes()==b.tobytes(),unmasked_difference_bbox=ImageChops.difference(a,b).getbbox()))
    after=[r for r in comparisons if r['frame']>max(v['holds'][-1]['next_original_message_frame'] for v in versions)]
    equality={k:final[0]['components'][k]==final[1]['components'][k] for k in final[0]['components']}
    ROOT.mkdir(parents=True);frames=[versions[1]['holds'][i]['matching_holds'][0]['frame'] for i in range(3)]+[after[0]['frame'],12001]
    sheet=Image.new('RGB',(1048,800*len(frames)),'#263238');draw=ImageDraw.Draw(sheet)
    for i,f in enumerate(frames):
        for col,(label,p) in enumerate(zip(['current_four_rows','reviewed_three_rows'],photos,strict=True)):
            photo=p[f];picture=Image.open(photo['path']).convert('RGB');x,y=col*524,i*800
            draw.text((x+4,y+4),label+' / frame'+str(f),fill='white');sheet.paste(picture.resize((512,768),Image.Resampling.NEAREST),(x+4,y+24));paths.append(Path(photo['path']))
    sp=ROOT/'paired_original_reward_sequence_and_return.png';sheet.save(sp)
    save(ROOT/'paired775_780_766_actual_planes_fixtures_and_return.json',dict(versions=versions,actual_original_reward_sequence=[775,780,766],
        actual_panel_observations=6,exact_native_and_independent_ink_blank_glyph_bounds_and_page_checks=True,
        captured_comparisons=comparisons,nontext_equal_samples=sum(r['nontext_upper_portrait_name_regions_equal'] for r in comparisons),
        nontext_differences=[r for r in comparisons if not r['nontext_upper_portrait_name_regions_equal']],
        sampled_after_original_farewell=[r for r in after],whole_final_RGB_equal=comparisons[-1]['whole_RGB_equal'],
        native_final_component_equality=equality,whole_actor_and_actual_captain_equal=final[0]['actor']==final[1]['actor'],
        actual_donor_captain_IDs=[v['captain'] for v in final],PRNG_seeds=[v['seed'] for v in final],PRNG_equal=final[0]['seed']==final[1]['seed'],
        no_PRNG_causal_future_world_full_RAM_or_hardware_equivalence_claim=True,
        final_component_hashes=[{k:sha(json.dumps(value,sort_keys=True,default=native_json).encode()) for k,value in v['components'].items()} for v in final],
        input_fixtures_are_counterfactual_not_earned_large_sale_share_inventory_qualification_or_letter=True,
        source_code_portraits_and_original_effect_bodies_unchanged=True,no_PC_or_emulator_code_or_RNG_fixture=True,
        all_jobs_terminal=True,new_cold_boot_runs=2,total_frames=24002,review_sheet=str(sp),review_sheet_sha256=sha(sp.read_bytes()),visual_review_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in paths},producer_sha256=sha(Path(__file__).read_bytes()),new_editorial_credit=0,full_goal_complete=False))
    print(dict(actual_sequence=[775,780,766],current_reviewed_panels=6,paired_samples=len(comparisons),nontext_equal=sum(r['nontext_upper_portrait_name_regions_equal'] for r in comparisons),
        final_RGB_equal=comparisons[-1]['whole_RGB_equal'],components_equal=equality,PRNG_seeds=[v['seed'] for v in final],visual_review_pending=True))
