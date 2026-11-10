"""Record the viewed clean exchange,source-bound names,item card and return scope."""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B203_source_reconciliation_v6022')
SOURCE=Path('work/analysis/lil_B203_source_v6010/all22_clean_current_complete_context.json')
ACTUAL=Path('work/analysis/lil_B203_source_paths_v6020/one_actual_source_path_and_complete_command_intervals.json')
NAMES=Path('work/analysis/lil_B203_source_names_v6013/three_exact_source_name_fields_voices_and_distinct_name_consumers.json')
CONTROL=Path('work/analysis/lil_B203_controls_v6017/nine_exact_leaves_resource632E_6003_picture47xx_four_A000_pairs_and_end.json')
ITEM=Path('work/analysis/lil_B203_item_fields_v6021/clean_item18_current_name_and_original_picture_descriptor.json')
RUN=Path('work/analysis/lil_B203_source_run_v6019_clean_Japanese')
DECISIONS={
 '2':'Retain Lil Argot in both native consumers and Lil as the runtime FI first name. The clean リル/アーゴット fields,actual portrait/nameplate and source voice3 agree. No new proper-name credit.',
 '76':'Retain Mikhail Letzel in the progressive nameplate and Mikhail Volk Letzel in the full catalogue. Clean ミハイル/レッツェル/フォルク fields and actual source portrait/nameplate support the distinction;do not expand the original progressive consumer or borrow a previous older speaker. Voice5 and the colloquial older dialogue remain. Do not infer a medical profession,rank or kinship from his interest in the book.',
 '170':'Retain Mysterious Old Man for the explicit source 謎の老人. This is a natural anonymous role label supported by the Japanese,including age and masculine reference,rather than an invented biography. The actual nameplate agrees with both consumers and voice0. Keep secondary 国籍不明/Unknown as internal nationality metadata;do not append Unknown or infer a nationality from his knowledge of Chinese medicinal use. No doctor,teacher,relative or clergy title is established.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['stage','viewed']);phase=p.parse_args().phase
    if phase=='stage':
        assert not ROOT.exists();packet,actual,names,control,item=map(read,[SOURCE,ACTUAL,NAMES,CONTROL,ITEM])
        assert not actual['unvisited_source_indices'] and len(actual['speech_observations'])==22 and len(actual['command_pairs'])==40 and actual['source_end810_return_frame']==8374
        assert item['Japanese']=='漢方医の聖典' and item['current_English']=="Herbalist's Bible" and item['item_ID']==18
        assert control['source_one_picture_pair'][0]['cases'][0]['original_picture_boundary_calls'][0]['descriptor']==[0,18,1,5]
        assert control['source_one_picture_pair'][0]['cases'][0]['original_picture_boundary_calls'][0]['layout']==[2,0,0]
        assert [(r['actor_ID'],r['fields'][0]['Japanese'],r['voice']) for r in names['source_name_fields']]==[(2,'リル',3),(76,'ミハイル',5),(170,'謎の老人',0)]
        rp=Path(read(RUN/'run_plan.json')['capture_folder'])/'capture_report.json';report=read(rp);photos={r['frame']:r for r in report['frames_captured']}
        ROOT.mkdir(parents=True);sheet=Image.new('RGB',(768,820),'#263238');draw=ImageDraw.Draw(sheet);selected=[]
        for i,frame in enumerate([8110,8350,8410,8470,10030,12970]):
            photo=photos[frame];assert sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'];pic=Image.open(photo['path']).convert('RGB');assert pic.size==(256,384)
            x,y=i%3*256,i//3*410;draw.text((x+3,y+3),'Japanese source '+str(frame),fill='white');sheet.paste(pic,(x,y+24));selected.append(photo)
        image=ROOT/'source_FE_complete_return_and_later_frames.png';sheet.save(image)
        save(ROOT/'source_names_item18_and_transition_sheet.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),source_item18=item,
            existing_item_widget=["Herbalist's Bible",'Local Product','—'],
            title_policy='The clean item18 title is 漢方医の聖典 and the current card displays Herbalist\'s Bible. The dialogue describes a book about medicinal materials without speaking an explicit title. Do not insert the card title,an invented Chinese classic title,a recipe,guaranteed cure or trade effect into that explanation. Existing item name/category/effects receive no fresh completion credit;the Local Product terminology lead remains open separately.',
            contextual_name_decisions=DECISIONS,source_name_consumer_proof=str(NAMES),source_name_consumer_proof_sha256=sha(NAMES.read_bytes()),source_control_proof=str(CONTROL),source_control_proof_sha256=sha(CONTROL.read_bytes()),
            return_sheet=dict(path=str(image),sha256=sha(image.read_bytes()),captures=selected),source_dialogue_sheets=actual['review_sheets'],source_full_screen_sheets=actual['transition_sheets'],
            visual_review_pending=True,prior_English_speech_comparison_pending=True,source_actual_objects=22,source_actual_commands=40,source_return_frame=8374,
            actual_source_event203_natural_activation_original_location_payment_full_effects_full_route_hardware_unclaimed=True,source_gameplay_fixture_runs=1,source_gameplay_fixture_frames=13001,
            evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,ACTUAL,NAMES,CONTROL,ITEM,rp,RUN/'terminal.json',Path(__file__)]},new_review_credit=0,full_goal_complete=False))
    else:
        inp=ROOT/'source_names_item18_and_transition_sheet.json';d=read(inp);out=ROOT/'viewed_complete_source_exchange_names_item18_and_return_scope.json';assert not out.exists()
        sheets=d['source_dialogue_sheets']+d['source_full_screen_sheets']+[d['return_sheet']];assert len(sheets)==9
        for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
        tracepath=Path(read(RUN/'run_plan.json')['capture_folder'])/'observer/commands.json';trace=read(tracepath)
        following=[r for r in trace['rows'] if r['source']['block']!=22];assert {(r['source']['route'],r['source']['block']) for r in following}=={(2,43)}
        assert next(r for r in following if r['kind']=='before_command' and r['source']['instruction_offset']==12)['frame']==8377
        save(out,dict(previous_source_reconciliation=str(inp),previous_source_reconciliation_sha256=sha(inp.read_bytes()),all_nine_source_dialogue_fullscreen_and_return_sheets_viewed_after_image_return=True,viewed_sheets=[dict(path=s['path'],sha256=s['sha256'],viewed=True,original_detail=True) for s in sheets],
            review='Viewed all22 Japanese objects in order:surprise at a specimen,uncertain insect/grass observation,cordyceps identification and Chinese medicinal context,the offered book,reluctance over apparent value,the older man teasing Mikhail interest,his embarrassed reading request,and Lil1000/older man100 negotiation. Mikhail Letzel and Mysterious Old Man nameplates match the exact source fields and consumers;Volk stays catalogue-only and nationality metadata is not displayed. The existing card shows Herbalist\'s Bible/Local Product/dash;the explanation speaks no title. The final stored FE notice substitutes Lil and states charm+1 with no portrait or nameplate. A later original A000 also displays the existing item-acquired notice at8350;this is not a23rd stored speech and receives no new generic-notice or item-effect fidelity credit. Full screens and return sheet establish ending8374 followed by unchanged B43 teaching dialogue,not an immediate idle town return. Later town/port UI scope is recorded from the returned images only. No natural event activation,original location,earned payment or full effect-body semantics is established.',
            all22_source_objects_observed=True,all31_source_commands_and9_original_initializers_observed=True,no_unvisited_source_indices=True,source_return_frame=8374,
            source_item18=d['source_item18'],title_policy=d['title_policy'],actual_existing_item_widget=d['existing_item_widget'],contextual_name_decisions=DECISIONS,
            existing_generated_acquisition_notice_observed_at8350=True,generated_acquisition_notice_not_an_extra_stored_speech_or_new_credit=True,final_HUD34900_gold_visible_no_new_payment_body_semantics_claim=True,following_observed_block43_not_new_editorial_credit=True,following_command_observer=str(tracepath),following_command_observer_sha256=sha(tracepath.read_bytes()),
            following_source_item_terminology_lead=dict(file_path='/data/SC2.DK4',block=43,command_offset=12,observed_frame=8410,current_wording='a source item',current_wording_needs_contextual_terminology_revisit=True,no_new_review_credit=True),
            ordinary_inputs_original_funds_roster_conditions_RNG_results_and_effects_unforced=True,initialized_Amsterdam_B22_not_natural_event203_activation_original_location_earned_inventory_full_route_or_hardware=True,
            no_duplicate_name_dialogue_or_item_widget_completion_credit=True,no_ROM_or_runtime_change=True,source_gameplay_fixture_runs=1,source_gameplay_fixture_frames=13001,terminal_reaped_tool_session=40707,
            visual_review_pending=False,prior_English_speech_comparison_pending=True,evidence={**d['evidence'],str(inp):sha(inp.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())},full_goal_complete=False))
        print('Nine source sheets viewed;all22 objects/40 commands,exact names,item18 and complete return bound. English comparison next;zero review credit.')
