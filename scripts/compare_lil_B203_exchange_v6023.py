"""Expose predecessor English only after clean gloss,names and whole source playback."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B203_comparison_v6023')
SOURCE=Path('work/analysis/lil_B203_source_v6010/all22_clean_current_complete_context.json')
ACTUAL=Path('work/analysis/lil_B203_source_paths_v6020/one_actual_source_path_and_complete_command_intervals.json')
RECON=Path('work/analysis/lil_B203_source_reconciliation_v6022/viewed_complete_source_exchange_names_item18_and_return_scope.json')
DISPATCH=Path('work/analysis/lil_B203_dispatches_v6014/all22_source_current_dispatches_FI_and9_control_leaves.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,actual,recon,dispatch=map(read,[SOURCE,ACTUAL,RECON,DISPATCH]);gloss=read(packet['whole_exchange_context_notes'])
    assert gloss['prior_English_speech_unread'] and recon['all_nine_source_dialogue_fullscreen_and_return_sheets_viewed_after_image_return'] and recon['all22_source_objects_observed'] and not actual['unvisited_source_indices']
    binding_path=Path(dispatch['registered_catalog_binding']);assert sha(binding_path.read_bytes())==dispatch['registered_catalog_binding_sha256'];binding=read(binding_path);rows=[];matched=[]
    for r in packet['records']:
        row=deepcopy(r);raw=bytes.fromhex(r['current_hex']);body=raw[1:].decode('cp932');assert raw[0]==r['source_selector']
        current=next(x for x in dispatch['speech_dispatch_cases'] if x['id']==r['id'] and x['version']=='current-English');match=current['registered_catalog_match'];effective=body;entry=None
        if match is not None:
            entry=binding['records'][match['table_index']];assert entry['key_hex']==raw[1:].hex() and entry['route_mask']&4 and dict(owner=['/data/SC2.DK4',r['id']],form='body') in entry['requests'];effective=bytes.fromhex(entry['target_hex']).decode('cp932');matched.append(r['id'])
        assert current['boundaries'][1]['text_hex']==effective.encode('cp932').hex();paragraph=' '.join(effective.split());observation=next(x for x in actual['speech_observations'] if x['id']==r['id']);assert observation['selected_capture'] is not None
        row.update(previous_raw_storage_body=body,previous_effective_template_body=effective,previous_registered_catalog_match=match,previous_registered_catalog_entry=entry,previous_display_body=effective,previous_paragraph=paragraph,previous_macro_template_paragraph=paragraph,previous_effective_runtime_paragraph=paragraph,previous_bytes_retained_for_exact_comparison=True,actual_source_fixture_observed=True,actual_source_paths=['complete_linear_source'],source_actual_observation=observation,clean_first_whole_exchange_gloss_precedes_old_English_comparison=True,prior_English_is_comparison_only_not_translation_source=True);rows.append(row)
    assert len(rows)==22 and not matched
    ROOT.mkdir(parents=True);save(ROOT/'all22_complete_clean_source_and_predecessor_exchange.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),whole_exchange_progression=gloss['whole_exchange_progression'],source_reconciliation=str(RECON),source_reconciliation_sha256=sha(RECON.read_bytes()),records=rows,registered_name_catalogue_matches=matched,all22_effective_predecessors_match_original_current_dispatch=True,no_target_wording_authored_yet=True,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,ACTUAL,RECON,DISPATCH,binding_path,Path(__file__)]},new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    for r in rows:print(r['source_record_index'],r['source_Japanese'].replace('\n',' / '),'| PREVIOUS:',r['previous_paragraph'])
