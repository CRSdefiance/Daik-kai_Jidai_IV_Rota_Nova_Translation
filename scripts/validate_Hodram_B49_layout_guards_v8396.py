"""Focused changed-input checks for source-bound ellipses, ordinary wrap scope and typed-label padding."""
from copy import deepcopy
from pathlib import Path
from scripts import plan_Hodram_B49_layout_v8394 as owned
from scripts.prove_lil_B212_controls_v6603b import compile_menu
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_layout_guards_v8396')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(owned.DOC);planned=read(owned.ROOT/'automatic_plans.json');assert len(planned['records'])==14 and not planned['failures'];cases=[]
    def add(label,index,field,value):
        original=next(r for r in doc['records'] if r['source_record_index']==index);row=deepcopy(original);assert row[field]!=value;row[field]=value;row['english']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english'];cases.append((label,row))
    silence=next(r for r in doc['records'] if r['source_record_index']==15);reply=next(r for r in doc['records'] if r['source_record_index']==67);directions=next(r for r in doc['records'] if r['source_record_index']==33)
    add('ellipsis-unapproved-record',67,'id','DK4_MES_B49_R9999')
    add('ellipsis-unapproved-source',67,'source_hex',reply['source_hex'][:-2]+'21')
    add('ellipsis-changed-prose',67,'english','…I want it now!')
    add('ellipsis-not-leading',67,'english',"It's… not that I don't want it.")
    add('doubled-ellipsis',15,'english','……')
    add('unapproved-nonASCII-punctuation',19,'english','But there’s one thing I would trade it for.')
    add('literal-NUL-in-prose',6,'english',"You're\0 here!")
    add('authored-LF-in-prose',6,'english',"You're\nhere!")
    add('directions-ordinary-boundary-changed-source',33,'source_hex',directions['source_hex'][:-2]+'21')
    add('directions-ordinary-boundary-changed-prose',33,'english',directions['english']+'!')
    add('wrong-progressive-selector',19,'source_selector',254)
    results=[]
    for label,row in cases:
        try:owned.plan(row)
        except (AssertionError,ValueError) as error:results.append(dict(case=label,rejected=True,error_type=type(error).__name__,error=str(error),actual_changed_input=True))
        else:raise AssertionError('Changed unsafe input accepted:'+label)
    for label,values in [('typed-label-trailing-padding',[b'All right.',b'No.   ']),('typed-label-leading-padding',[b' All right.',b'No.']),('typed-wrong-option-count',[b'All right.',b'No.',b'Other'])]:
        try:compile_menu(0x2100,values)
        except (AssertionError,ValueError) as error:results.append(dict(case=label,rejected=True,error_type=type(error).__name__,actual_changed_input=True))
        else:raise AssertionError('Unsafe typed-label input accepted:'+label)
    assert len(results)==14;ROOT.mkdir(parents=True);save(ROOT/'focused_guard_rejections.json',dict(cases=results,negative_count=14,all_actual_changed_inputs_rejected=True,existing14_plans_unchanged=True,no_global_Unicode_NUL_font_profile_viewport_orQA_guard_changed=True,only_exact_source_andapproved_ellipsis_paragraphs_anddirections_boundary_accepted=True,no_ROM_native_emulator_orcredit_change=True,new_credit=0,full_goal_complete=False))
    print('Private B49 guards:14changed-input rejections;ellipsis identity/source/prose/position,NUL/LF,ordinary boundary scope,selector andtyped padding/count remainblocked.No native/emulator replay orcredit.')
