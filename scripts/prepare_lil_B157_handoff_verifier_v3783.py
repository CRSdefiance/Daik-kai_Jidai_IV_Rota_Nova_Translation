"""Derive an independent audit with the exact B157 FE, pause and coverage scope."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    src=Path('scripts/verify_editorial_handoff_v3743.py');dst=Path('scripts/verify_editorial_handoff_v3783.py');assert not dst.exists();t=src.read_text(encoding='utf-8')
    a="    alias=read(doc['actual_nameplate_reconciliation']);";start=t.index(a);end=t.index('\n',start)
    t=t[:start]+"    transitions=read('work/analysis/lil_B157_transition_review_v3775/full_screen_transition_and_all13_sheet_review.json');assert transitions['full_town_return_RGB_identical'] and transitions['source_C281_4885_pause_picture_FE_and_normal_return_visually_reviewed'] and len(transitions['viewed_actual_sheets'])==13 and len(transitions['viewed_full_screens'])==6"+t[end:]
    changes={
        'v3743':'v3783','v3742':'v3782','V3742':'V3782','v3719':'v3759','V3719':'V3759',
        'Lil-B156-Ian-tavern-harassment-rescue-recruitment76':'Lil-B157-Carlo-trade-illness-grief-chosen-family75',
        'B156':'B157',
        'release_v3739':'release_v3779','startup_v3741':'startup_v3781','registration_v3737':'registration_v3777',
        'actual_v3733/actual_source_English_all76_panels_ten_actors_resources_C200_and_return':'actual_v3773/actual_source_English_all75_panels_seven_actors_two_FE_pause_C281_4885_and_return',
        'all-routes-unified-v3738':'all-routes-unified-v3778','all_routes_combined_v3692':'all_routes_combined_v3738',
        '(3388,3340)':'(4092,3824)',
        '{2,9,14,20,21,92,96,152,164,165}':'{2,9,14,19,20,105,142,254}',
        "len(controls['relocated_predicate_pairs'])==3":"len(controls['relocated_predicate_pairs'])==2",
        "len(controls['relocated_C200_pairs'])==1":"len(controls['relocated_C200_pairs'])==2",
        '[1,1,1]':'[1,1]',
        'all43_source_current_target_nonrelative_nonspeech_leaves':'all27_source_current_target_nonrelative_nonspeech_leaves',
        '[(3380,3332),(3384,3336)]':'[(4084,3814),(4088,3818)]',
        'complete_native_independent216x64_plane_equal':'complete_native_independent_plane_equal',
        'all_visible_origins_zero_and16px_rows_within4rows':'all_visible_origins_zero_and_native_rows_within4rows',
        '[21097,21096]':'[21096,21095]',
        "==123":"==106",'equal_V3692':'equal_V3738',
        "newinv['lil_B152_B154_completed_v3654']==oldinv['lil_B152_B154_completed_v3654'] and newinv['lil_B155_completed_v3696']==oldinv['lil_B155_completed_v3696']":"newinv['lil_B152_B154_completed_v3654']==oldinv['lil_B152_B154_completed_v3654'] and newinv['lil_B155_completed_v3696']==oldinv['lil_B155_completed_v3696'] and newinv['lil_B156_completed_v3742']==oldinv['lil_B156_completed_v3742']",
        'now_reviewed76_completed_in_V3738':'now_reviewed75_completed_in_V3778','now_reviewed76_pending_integration':'now_reviewed75_pending_integration',
        'other157_B157_B160':'other82_B158_B160',
        'actual_two_disclosed_B22_fixtures76_panels123_commands_ten_actors_source_Sailor_alias_and_transitions_verified':'actual_two_disclosed_B22_fixtures75_panels106_commands_seven_actors_two_FE_pause_C281_4885_and_transitions_verified',
        'all76_clean_predecessor_integrated_references_and_retentions_verified':'all75_clean_predecessor_integrated_references_and_retentions_verified',
        'all131_commands12_spans60_skips304_stored_cases_C200_and_two_endwords_bound':'all110_commands8_spans40_skips300_stored_cases_two_C200_pause_and_two_endwords_bound',
        'all76_displayed':'all75_displayed',
        '5254':'5329','5257':'5332','3388':'3419','1866':'1910','3401':'3476',
        "{'revise':41,'retain-wording':35}":"{'revise':31,'retain-wording':44}",
        'all43':'all27',
    }
    for a in changes:assert a in t,a
    t=re.sub('|'.join(re.escape(a) for a in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],t)
    # Bare numeric assertions are replaced only after the specific tuple/metadata substitutions.
    numbers={76:75,41:31,35:44,531:532,304:300,608:600,29:24,131:110,12:8,60:40,43:27,3655:3730,50:64,156:157}
    t=re.sub(r'(?<![\w])(?:'+ '|'.join(map(str,numbers))+r')(?![\w])',lambda m:str(numbers[int(m.group())]),t)
    # The old B156 completion inventory remains a historical object, not a newly renamed one.
    t=t.replace("newinv['lil_B157_completed_v3782']==oldinv['lil_B157_completed_v3782']","newinv['lil_B156_completed_v3742']==oldinv['lil_B156_completed_v3742']")
    needle="    actual=read('work/analysis/lil_B157_actual_v3773/"
    pos=t.index(needle)
    t=t[:pos]+"    assert native['progressive_planes']==73 and native['FE_planes']==2 and native['source_FE_null_actor_logical228x48_physical228x64_complete_one_page_proven']\n    for c in native['cases']:\n        if c['geometry']==[228,64]:assert c['logical_row_pitch']==12 and c['physical_row_pitch']==16 and c['one_native_page_consumes_complete_target'] and all(v['null_source_actor'] for p in c['current_native_macro_pipelines'] for v in p['cases'])\n        else:assert c['geometry']==[216,64] and c['logical_row_pitch']==c['physical_row_pitch']==16\n    assert mapping['blocks'][0]['research_logical_end']==3822 and mapping['blocks'][0]['original2000_pause_and_resume_maps']==[dict(old_offset=3052,new_offset=2774,source_resume=3054,target_resume=2776,source_two_byte_pause_and_mapped_resumption_boundary_exact=True)]\n"+t[pos:]
    compile(t,str(dst),'exec');dst.write_text(t,encoding='utf-8',newline='\n');root=Path('work/analysis/lil_B157_handoff_verifier_tools_v3783');assert not root.exists();root.mkdir(parents=True);save(root/'source_derivation.json',dict(source=str(src),source_sha256=sha(src.read_bytes()),successor=str(dst),successor_sha256=sha(dst.read_bytes()),FE_null_actor_geometry_and_pause_independently_checked=True,no_ledger_or_docs_mutation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
