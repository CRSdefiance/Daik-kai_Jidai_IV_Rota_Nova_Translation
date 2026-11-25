"""Preserve the original typed compiler and derive strict B223 reconstruction."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B223_atomic_tools_v7114')
if __name__=='__main__':
    assert not ROOT.exists()
    a='dk4tool/patch/lil_B214_editorial_v1.py';b='dk4tool/patch/lil_B223_editorial_v1.py'
    oldseal="all17_five_gates_and_exact_references_approved=True,all_names_controls_slots_aliases_eight_relatives_bounds_and_single_pages_bound=True,actual9_objects9_pages29_body29_name_holds_and8_offline_objects_explicit=True,observed_results_UI_timing_RNG_durations_later_samples_final_components_equal_with_scope=True,original_event214_dependency87_not_natural_activation_or_earned_progress=True"
    newseal="all17_five_gates_and_exact_references_approved=True,all22_commands_four_relatives_typed_aliases_and19_native_pages_bound=True,actual9_objects11_pages37_body37_headers8_offline_objects_explicit=True,all_measured_later_differences_and_final_captain0_2_retained=True,original_event223_dependency90_not_natural_activation_or_earned_progress=True"
    oldqa="row['reviewed_ordinary_boundaries']==qa['reviewed_ordinary_boundaries'] and row.get('qa_waivers',[])==(['line-break-count'] if bindings[ident]['row_count_reason'] else [])"
    newqa="row['reviewed_ordinary_boundaries']==qa['reviewed_ordinary_boundaries']==bindings[ident]['ordinary_wrap_reasons'] and row['qa_waivers']==qa['qa_waivers']==bindings[ident]['qa_waivers'] and row['base_QA_report']['base_QA_issues']==qa['base_QA_issues']==bindings[ident]['base_QA_issues'] and row['exact_reviewed_base_warnings']==qa['exact_reviewed_base_warnings']==bindings[ident]['exact_reviewed_base_warnings'] and qa['all_original_base_QA_issues_preserved']"
    c={
      'B214':'B223',oldseal:newseal,
      'actual_objects=9,actual_pages=9,actual_complete_body_holds=29,actual_complete_name_holds=29':'actual_objects=9,actual_pages=11,actual_complete_body_holds=37,actual_complete_name_holds=37',
      'no_name_asset_change_or_new_name_UI_credit=True':'three_personal_name_retentions_actor151_review_separate_no_duplicate_credit=True',
      "{'revise':12,'retain-wording':5}":"{'revise':16,'retain-wording':1}",
      'blocks[214]':'blocks[223]',"spec['block']==214":"spec['block']==223","row['block']==214":"row['block']==223","r['block']==214":"r['block']==223",'block=214':'block=223',
      '(1316,1316,1314,2,1304,1302,2)':'(1316,1316,1316,0,1384,1384,0)',
      'block[1310:]==bytes(6)':'block[1312:]==bytes(4)',
      'Source D0 role1 speaker, automatic original actor voice style ':'Source D0 role1 speaker;automatic original voice style ',
      "{2:'Lil Argot',4:'Janus Pasar',23:'Manuel Almeida'}":"{2:'Lil Argot',13:'Cesare Tony',21:'Ian Dukov'}",
      oldqa:newqa,
      "not bindings[ident]['row_count_reason'] or row.get('qa_waiver_reason')==bindings[ident]['row_count_reason']":"row['row_count_reason']==bindings[ident]['row_count_reason'] and row['qa_waiver_reason']==bindings[ident]['qa_waiver_reason']",
      'rowcount==11':'rowcount==6','block[last:1314]':'block[last:1316]','mapped(1314)==1302':'mapped(1316)==1384',
      '[(890,512,4,898),(894,768,4,902),(898,256,68,970),(966,256,0,970),(1172,512,4,1180),(1176,768,4,1184),(1180,256,118,1302),(1298,256,0,1302)]':'[(1146,512,4,1154),(1150,768,4,1158),(1154,256,146,1304),(1300,256,0,1304)]',
      'target=bytes(logical)+bytes(2)':'target=bytes(logical)',
      'len(target)==1304':'len(target)==1384','len(commands)==27':'len(commands)==22',
      'dict(source_offset=1310,target_offset=1298,extent=4)':'dict(source_offset=1312,target_offset=1380,extent=4)',
      'target[1298:]==bytes(6)':'target[1380:]==bytes(4)','len(cases)==40':'len(cases)==20',
      "struct.pack_into('<H',inverse,4,1306)":"struct.pack_into('<H',inverse,4,1308)",
      'bytes(inverse)+block[1314:]==block':'bytes(inverse)==block','newblocks[214]':'newblocks[223]',
      'source_bytes=1316,target_bytes=1304,source_logical_end=1314,target_logical_end=1302,relative_operands=8,source_commands=27':'source_bytes=1316,target_bytes=1384,source_logical_end=1316,target_logical_end=1384,relative_operands=4,source_commands=22',
      'native17_pages_actual9_objects9_pages29_holds_offline8_explicit':'native19_pages_actual9_objects11_pages37_holds_offline8_explicit',
      'all_observed_equality_and_final_scope_limits_retained':'all_measured_later_differences_and_final_scope_limits_retained',
      '20 exact decisions/kinds':'17 exact decisions/kinds','all1148 predecessor bytes inverse':'all1316 predecessor bytes inverse',
      'all18 independent command maps':'all22 independent command maps',
    }
    assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c);row=derive(a,b,c)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_atomic_compiler.json',dict(tool=row,all_native_high_integer_constants_and_multiplicity_preserved=True,all_gates_before_sole_archive_write=True,source1316_full_inverse_target1384_no_tail=True,exact_QA_waivers_base_diagnostics_and_actual_late_scope_preserved=True,new_credit=0,full_goal_complete=False))
