"""Bind the spoken title to clean item data and record complete actual source scope."""
import argparse,struct
from pathlib import Path
from PIL import Image,ImageDraw
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,POOL,cstring
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B202_source_reconciliation_v5970')
SOURCE=Path('work/analysis/lil_B202_source_v5959/all19_clean_current_complete_context.json')
ACTUAL=Path('work/analysis/lil_B202_source_paths_v5969/one_actual_source_path_and_complete_command_intervals.json')
NAMES=Path('work/analysis/lil_B202_source_names_v5962/four_exact_source_name_fields_voices_and_original_Sailor_alias.json')
CONTROL=Path('work/analysis/lil_B202_controls_v5966/seven_exact_leaves632A_picture47xx_two_A000_pairs_and_guarded_end.json')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['stage','viewed']);mode=p.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists();packet,actual,names,control=map(read,[SOURCE,ACTUAL,NAMES,CONTROL]);assert actual['unvisited_source_indices']==[] and len(actual['speech_observations'])==19 and len(actual['command_pairs'])==35 and actual['source_end582_return_frame']==7657
        clean,current=[NdsImage.open(path).read_file('/__arm9__.bin') for path in ['work/clean.nds',packet['current_ROM']]];payload=bytes(MainCodeFile(current,BASE).sections[3].data[:-48]);assert len(payload)==123040 and current.count(payload)==1;payload_at=current.index(payload)
        field=0x11E210+14*24;sp,cp=[struct.unpack_from('<I',a,field)[0] for a in [clean,current]];src=cstring(clean,sp-BASE)
        if POOL<=cp<POOL+len(payload):off=cp-POOL;value=cstring(payload,off);current_offset=payload_at+off;storage='verified-staged-payload'
        else:current_offset=cp-BASE;value=cstring(current,current_offset);storage='original-static-ARM9'
        assert src[:-1].decode('cp932')=='ガラスの製法辞典' and value==b'Glassmaking Guide\0'
        assert next(r for r in packet['records'] if r['source_record_index']==55)['source_Japanese'].find('ガラスの製法辞典')>=0
        descriptor=control['source_one_picture_pair'][0]['cases'][0]['original_picture_boundary_calls'][0];assert descriptor['descriptor']==[0,14,1,5] and descriptor['layout']==[3,1,1]
        run=Path('work/analysis/lil_B202_source_run_v5968_clean_Japanese');rp=Path(read(run/'run_plan.json')['capture_folder'])/'capture_report.json';report=read(rp);photos={r['frame']:r for r in report['frames_captured']};ROOT.mkdir(parents=True)
        frames=[7390,7690,7750,10030,12970,13001];sheet=Image.new('RGB',(768,820),'#263238');draw=ImageDraw.Draw(sheet);selected=[]
        for i,frame in enumerate(frames):
            photo=photos[frame];assert sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'];pic=Image.open(photo['path']).convert('RGB');assert pic.size==(256,384);x,y=i%3*256,i//3*410;draw.text((x+3,y+3),'Japanese source '+str(frame),fill='white');sheet.paste(pic,(x,y+24));selected.append(photo)
        image=ROOT/'source_final_speech_complete_return_and_later_frames.png';sheet.save(image)
        save(ROOT/'spoken_title_source_fields_and_transition_sheet.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
            source_item14=dict(item_ID=14,pointer_field=field,source_pointer=sp,source_storage_offset=sp-BASE,source_terminated_hex=src.hex(),Japanese=src[:-1].decode('cp932'),current_pointer=cp,current_storage_offset=current_offset,current_storage=storage,current_terminated_hex=value.hex(),current_English='Glassmaking Guide',source_complete_static_item_row_hex=clean[field:field+24].hex()),
            original_source_picture_descriptor=descriptor,source_spoken_title_index=55,
            title_decision='Use the established Glassmaking Guide when Charles reads the title. Clean speech and clean item14 both explicitly name ガラスの製法辞典;Guide is natural English for this book of manufacturing methods and matches the actual existing item card. Preserve the technical/reference subject without inventing recipes,rarity,provenance,value,guaranteed trade effects or a different book. The source glossary Dictionary of Glassmaking is a literal gloss,not a competing canonical target. Item category/effect labels and all other item prose remain outside new completion credit.',
            actual_existing_item_widget=['Glassmaking Guide','Local Product','—'],
            source_name_consumer_proof=str(NAMES),source_name_consumer_proof_sha256=sha(NAMES.read_bytes()),source_control_proof=str(CONTROL),source_control_proof_sha256=sha(CONTROL.read_bytes()),
            return_sheet=dict(path=str(image),sha256=sha(image.read_bytes()),captures=selected),source_dialogue_sheets=actual['review_sheets'],source_full_screen_sheets=actual['transition_sheets'],
            visual_review_pending=True,prior_English_speech_comparison_pending=True,source_actual_speech_count=19,source_actual_command_count=35,source_return_frame=7657,
            actual_source_event202_natural_activation_original_location_full_effects_full_route_hardware_unclaimed=True,
            source_gameplay_fixture_runs=1,source_gameplay_fixture_frames=13001,
            evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,ACTUAL,NAMES,CONTROL,rp,run/'terminal.json',Path(__file__)]},new_review_credit=0,full_goal_complete=False))
        print('Spoken title bound to clean item14/current Glassmaking Guide;source return sheet ready. No new title/effect or editorial completion credit.')
    else:
        inp=ROOT/'spoken_title_source_fields_and_transition_sheet.json';d=read(inp);out=ROOT/'viewed_complete_source_exchange_names_title_and_return_scope.json';assert not out.exists()
        sheets=d['source_dialogue_sheets']+d['source_full_screen_sheets']+[d['return_sheet']];assert len(sheets)==9
        for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
        run=Path('work/analysis/lil_B202_source_run_v5968_clean_Japanese');tracepath=Path(read(run/'run_plan.json')['capture_folder'])/'observer/commands.json';trace=read(tracepath);following=[r for r in trace['rows'] if r['source']['block']!=22];assert {(r['source']['route'],r['source']['block']) for r in following}=={(2,43)}
        save(out,dict(following_observed_block43_not_new_editorial_credit=True,following_command_observer=str(tracepath),following_command_observer_sha256=sha(tracepath.read_bytes()),following_source_item_terminology_lead=dict(file_path='/data/SC2.DK4',block=43,command_offset=12,observed_frame=7690,current_wording='a source item',current_wording_needs_contextual_terminology_revisit=True,no_new_review_credit=True),previous_source_reconciliation=str(inp),previous_source_reconciliation_sha256=sha(inp.read_bytes()),
            all_nine_source_dialogue_fullscreen_and_return_sheets_viewed_after_image_return=True,viewed_sheets=[dict(path=s['path'],sha256=s['sha256'],viewed=True,original_detail=True) for s in sheets],
            review='Viewed all19 Japanese speeches in order and complete handoff,chase,Charles conversation,book card and final payoff. Sailor is the observed original progressive alias,not a Retainer rank spoken in this scene. Guildmaster and Charles Rochefort labels agree with bound consumers;Jean remains catalogue-only. The book appears while Lil tentatively identifies it,and Charles reads the exact glassmaking title. Preserve two separate rough stop commands,the interrupted objection and later-reading motive. Whole screens show B202 ending7657 followed by unchanged SC2B43 teaching dialogue,including the existing source item wording,and later town/port UI by12970. Do not call that following prose newly reviewed or claim an immediate return to an idle town screen. No natural event trigger or complete item-effect semantics is established. The existing Local Product category is recorded separately,not freshly approved by spoken-title matching. No English target prose has been approved by this source-only observation.',
            all19_source_speeches_observed=True,all26_source_commands_and9_original_initializers_observed=True,
            no_unvisited_source_speech_indices=True,source_return_frame=7657,source_item14=d['source_item14'],title_decision=d['title_decision'],
            actual_existing_item_widget=d['actual_existing_item_widget'],source_names=str(NAMES),
            ordinary_inputs_original_funds_roster_conditions_RNG_results_and_effects_unforced=True,
            initialized_Amsterdam_B22_not_natural_event202_activation_original_location_earned_inventory_full_route_or_hardware=True,
            no_duplicate_name_dialogue_or_item_widget_completion_credit=True,no_ROM_or_runtime_change=True,
            source_gameplay_fixture_runs=1,source_gameplay_fixture_frames=13001,terminal_reaped_tool_session=48349,
            visual_review_pending=False,prior_English_speech_comparison_pending=True,evidence={**d['evidence'],str(inp):sha(inp.read_bytes())},full_goal_complete=False))
        print('Nine source sheets viewed;all19 speeches/35 commands/title/name consumers and complete return bound. English contextual comparison next;zero review credit.')
