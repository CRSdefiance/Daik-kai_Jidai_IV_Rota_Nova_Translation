"""Complete source commands and exact original-font nameplate masks in both target fixtures."""
from collections import Counter
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/generic_speaker_scenes_v5885')
FIXTURE=Path('work/analysis/generic_speaker_label_fixtures_v5882/two_complete_existing_exchanges_with_target_name_data.json')
NAMES=Path('work/analysis/generic_speaker_names_v5884/all207_progressive_catalogue_names_eight_voices_and_exact_three_changes.json')
INK=(98,97,98)

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    manifest=read(FIXTURE);native=read(NAMES)
    values={r['actor_ID']:r['text'] for r in native['native_versions'][1]['original_consumers']['rows'] if r['consumer']=='progressive-nameplate'}
    versions=[];evidence={str(p):sha(p.read_bytes()) for p in [FIXTURE,NAMES,Path(__file__)]};pictures=[];changed=Counter()
    for fixture in manifest['fixtures']:
        case=fixture['case'];run=Path(f'work/analysis/generic_speaker_label_run_v5883_{case}')
        terminal,plan=read(run/'terminal.json'),read(run/'run_plan.json');cap=Path(plan['capture_folder'])
        report,trace=read(cap/'capture_report.json'),read(cap/'observer/commands.json')
        assert terminal['terminal'] and terminal['observer_instances']==1 and terminal['observer_host_slots_restored']
        assert report['frames']==8001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not report.get('battery_save_preloaded') and not any(v for k,v in report.items() if k.startswith('synthetic_'))
        assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes())
        assert plan['original_event_not_naturally_selected'] and plan['all_complete_original_source_commands_retained']
        assert sha(Path(plan['original_inputs']).read_bytes())==plan['inputs_sha256']
        assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
        image=NdsImage.open(fixture['research_ROM']);blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
        assert blocks[22].hex()==fixture['fixture_block_hex']
        font=GameAsciiFont.from_arm9(image.read_file('/__arm9__.bin'));photos={}
        for r in report['frames_captured']:
            p=Path(r['path']);assert sha(p.read_bytes())==r['PNG_sha256'];photo=Image.open(p).convert('RGB');assert photo.size==(256,384)
            photos[r['frame']]=(r,photo)
        expected={r['offset']:r for r in fixture['all_stored_fixture_commands']};texts={r['fixture_command_offset']:r for r in fixture['original_text_records']}
        pairs=[];intervals=[];following=set()
        for row in trace['rows']:
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
            s=row['source'];assert s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(blocks[s['block']])
            if s['block']!=22:following.add(s['block'])
            if row['kind']!='after_command' or s['block']!=22:continue
            entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];command=expected[at]
            assert s['first_word']==command['word'] and row['decoded_length']==command['native_extent']
            assert blocks[22][at:at+command['native_extent']].hex()==command['whole_command_hex']
            pairs.append(dict(offset=at,word=command['word'],start=entry['frame'],returned=row['frame'],result=row['result_words']))
            if at in texts:
                t=texts[at];prefix=t['source_selector'];holds=[];name=None if prefix==254 else values[prefix]
                if name is not None:
                    width=6*len(name);assert width<=6*len({164:'Man in a Couple',165:'Woman in a Couple',172:'Collapsed Person'}.get(prefix,name))
                    glyphs={c:font.decode(c) for c in name};ink={(i*6+x,y) for i,c in enumerate(name) for y in range(11) for x in range(6) if glyphs[c].getpixel((x,y))}
                    assert ink and all(any(x//6==i for x,y in ink) for i in [0,len(name)-1])
                    for frame,(r,photo) in photos.items():
                        if not entry['frame']<frame<row['frame']:continue
                        # Actual name origin and gray palette were measured in the unmodified tea frame4000.
                        # Check the entire glyph cell rectangle plus a 4px horizontal/1px vertical blank guard.
                        actual={(x-4,y-1) for y in range(13) for x in range(width+8) if photo.getpixel((12+x,276+y))==INK}
                        if actual!=ink:continue
                        holds.append(dict(frame=frame,capture=r['path'],capture_sha256=r['PNG_sha256'],
                            complete_first_to_final_glyphs_and_blank_guards_exact=True,no_wrap_pagination_or_trailing_old_label_ink=True))
                    assert holds,(case,t['id'],name)
                    pictures.append((case,t['id'],name,Path(holds[-1]['capture'])))
                    if prefix in [164,165,172]:changed[prefix]+=1
                intervals.append(dict(id=t['id'],source_record_index=t['source_record_index'],prefix=prefix,name=name,
                    start=entry['frame'],returned=row['frame'],holds=holds,null_FE_not_misidentified_as_actor=prefix==254))
        assert len(pairs)==len(expected)==fixture['original_source_command_count']+9
        assert [p['offset'] for p in pairs]==list(expected) and pairs[-1]['word']==0 and pairs[-1]['result']==[0,0]
        assert len(intervals)==fixture['original_source_speech_count'] and len(intervals)=={'tea':9,'recovery':19}[case]
        assert 120 in following and not fixture['explicitly_excluded_original_commands']
        versions.append(dict(case=case,complete_command_pairs=pairs,complete_speech_intervals=intervals,
            end_return_frame=pairs[-1]['returned'],following_observed_blocks=sorted(following),capture_report=str(cap/'capture_report.json'),
            trace=str(cap/'observer/commands.json'),all_complete_original_commands_and_speeches_observed=True))
        for p in [run/'terminal.json',run/'run_plan.json',Path(plan['original_inputs']),cap/'capture_report.json',cap/'observer/commands.json']:
            evidence[str(p)]=sha(p.read_bytes())
    assert changed==Counter({164:4,165:4,172:8})
    sheets=[]
    for start in range(0,len(pictures),6):
        sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(case,ident,name,path) in enumerate(pictures[start:start+6]):
            x,y=i%3*520,i//3*416;draw.text((x+4,y+3),case+' / '+ident+' / '+name,fill='white')
            sheet.paste(Image.open(path).convert('RGB').crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
        p=ROOT/f'actual_nameplates_complete_context_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    save(ROOT/'two_complete_exchanges_original_commands_and_exact_nameplate_glyphs.json',dict(
        versions=versions,changed_actor_speech_observations={str(k):v for k,v in changed.items()},
        complete_speech_observations=28,complete_nameplate_observations=len(pictures),
        actual_target_nameplate_cases=16,actual_nameplate_gray_palette=list(INK),actual_name_origin=[16,277],
        complete_native_ASCII_glyph_masks_first_final_characters_and_blank_guards_exact=True,
        no_authored_wrap_metrics_runtime_control_substitution_font_or_scene_prose_changes=True,
        review_sheets=sheets,visual_review_pending=True,
        initialized_Amsterdam_B22_content_fixtures_not_natural_event_184_200_activation_original_location_or_hardware=True,
        source_C200_preserved_without_new_effect_semantics_claim=True,
        new_cold_boots=2,frames_each=8001,new_frames=16002,all_jobs_terminal=True,
        actual_catalogue_UI_not_visited_native_getters_checked_separately=True,
        no_unvisited_conditional_dialogue_full_route_or_broad_simulation_claim=True,
        evidence=evidence,new_dialogue_or_name_completion_credit=0,full_goal_complete=False))
    print(dict(complete_exchanges=2,speeches=28,complete_nameplates=len(pictures),changed_nameplates=16,sheets=len(sheets)))
