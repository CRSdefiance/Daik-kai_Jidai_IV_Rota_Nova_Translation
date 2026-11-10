"""Record viewed actual final English pages andall measured differences without recasting speakers."""
from copy import deepcopy
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.lil_B225_final_paths_v7223 import ACTUAL,LATER,PAIRS,NAMES,VIEW
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    assert not VIEW.parent.exists() and not NAMES.exists();a,later,pairs=map(read,[ACTUAL,LATER,PAIRS]);assert a['actual_unique_speeches']==13 and a['actual_native_pages']==14 and a['all_jobs_terminal_and_reaped'] and not a['incomplete_sampled_body_holds'];sheets=[*a['review_sheets'],a['transition_sheet'],dict(path=pairs['review_sheet'],sha256=pairs['review_sheet_sha256'])];assert len(sheets)==5
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
    VIEW.parent.mkdir(parents=True);panes=[]
    for p in a['actual_page_panels']:
        h=p['selected_capture'];assert sha(Path(h['capture']).read_bytes())==h['sha256'];im=Image.open(h['capture']).convert('RGB').crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST);path=VIEW.parent/(p['id']+'_page'+str(p['native_page'])+'.png');im.save(path);assert Image.open(path).convert('RGB').tobytes()==im.tobytes();panes.append(dict(id=p['id'],native_page=p['native_page'],frame=h['frame'],whole_capture=h['capture'],whole_capture_sha256=h['sha256'],panel=str(path),panel_sha256=sha(path.read_bytes()),byte_equal_saved_whole_frame_crop=True,present_in_viewed_final_sheet=True))
    oldpath=Path('translations/lil_B225_speaker_name_review_v1.json');n=deepcopy(read(oldpath))
    for r in n['records']:
        holds=[h for p in a['actual_panels'] for h in p['complete_name_holds'] if h['actor_ID']==r['actor_ID']];assert holds and all(h['text']==r['english'] and h['complete_name_and_blank_guards_equal'] for h in holds);r['historical_actual_English_body_scene_pending']=r.pop('actual_English_body_scene_pending');r.update(actual_English_body_scene_observed=True,actual_English_complete_header_holds=len(holds),original_retention_scope_unchanged=True)
    n.update(previous_review=str(oldpath),previous_review_sha256=sha(oldpath.read_bytes()),actual_English_proof=str(ACTUAL),actual_English_proof_sha256=sha(ACTUAL.read_bytes()),all_four_actual_final_English_progressive_names_complete=True,no_new_name_or_dialogue_credit=True);save(NAMES,n)
    save(VIEW,dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),later_scope_proof=str(LATER),later_scope_proof_sha256=sha(LATER.read_bytes()),later_pairs=str(PAIRS),later_pairs_sha256=sha(PAIRS.read_bytes()),viewed_sheets=sheets,all_five_final_English_andunmasked_later_sheets_individually_viewed=True,all14_final_page_panels_viewed=True,stored_panels=panes,R16_fuller35_cell_opening_viewed_in_actual_gameplay=True,R26_complete_two_pages_andoriginal_A_advance_viewed=True,all_four_names_complete_source_Sailor_not_recast_as_child=True,catalogue151_Retainer_andfull207_scope_open=True,all_measured_source_English_timing_RNG_later_RGB_andcomponents_retained=True,no_whole_RAM_future_sequence_orcomplete_causal_equivalence_claim=True,visual_review_pending=False,speaker_name_review=str(NAMES),speaker_name_review_sha256=sha(NAMES.read_bytes()),new_emulator_runs=0,new_credit=0,full_goal_complete=False));print('Final English:14 actual pages andfive sheets viewed;four names complete,R16 fuller opening/R26 guard andordinary A advance retained. No completion credit.')
