"""Source-lock exhaustive B50 policy challenges without unrelated B49 menu cases."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B50_policy_tools_v8515');assert not root.exists()
    source=Path('scripts/validate_Hodram_B49_policy_v8425b.py').read_text(encoding='utf-8')
    start=source.index("    typed=compile_choices(");end=source.index("    for key,value in [('target_locale'",start)
    no_menu="""    assert not frozen['choice_bindings'] and not doc.get('typed_choice_records')
    changed=deepcopy(doc);changed['typed_choice_records']=[dict(id='UNAPPROVED_TYPED_CHOICE',english='Yes.')]
    reject('no-typed-menu-authorized',doc,changed,validate_approved_batch,'typed menu records authorized')
"""
    result=derive('scripts/validate_Hodram_B49_policy_v8425b.py','scripts/validate_Hodram_B50_policy_v8515.py',{
        'Hodram_B49_policy_validation_v8425b':'Hodram_B50_policy_validation_v8515',
        'hodram_B49_profile_v2':'hodram_B50_profile_v1','hodram_B49_layout_v2':'hodram_B50_layout_v1','hodram_B49_names_v2':'hodram_B50_names_v1',
        'from dk4tool.dialogue.hodram_B49_choices_v2 import compile_choices\n':'',
        'translations/hodram_B49_editorial_manuscript_v4.json':'translations/hodram_B50_editorial_manuscript_v4.json',
        'translations/hodram_B49_speaker_name_review_v2.json':'translations/hodram_B50_speaker_name_review_v2.json',
        'translations/hodram_B49_native_contract_v2.json':'translations/hodram_B50_native_contract_v1.json',
        "('hodram_B49_'+suffix+'_v2.py')":"('hodram_B50_'+suffix+'_v1.py')",
        "['profile','layout','plan','choices','names']":"['profile','layout','plan','names']",
        "block=bank[49]":"block=bank[50]",
        source[start:end]:no_menu,
        "changed['records'][index]['current_name']='Unapproved Name'":"changed['records'][index]['current']='Unapproved Name'",
        "changed['system_FE_record_IDs']=[]":"changed['no_FE_personal_actor_name']=False",
        'len(positives)==14':'len(positives)==3',
        "sum(len(p['qa']['issues']) for p in positives)==7":"sum(len(p['qa']['issues']) for p in positives)==3",
        'positive_typed_menu=dict(bytes=22,hex=typed.hex(),records=2)':'positive_no_typed_menu=True',
        'positive_batch_andtwo_scoped_names=True,positive_editorial_units=16':'positive_batch_andone_scoped_name=True,positive_editorial_units=3',
        'seven_original_infos_zero_warnings_waivers_preserved':'three_original_infos_zero_warnings_waivers_preserved',
        'source_bound_standalone_andmixed_ellipsis_andordinary_New_World_boundary_frozen':'complete_original_B50_prose_controls_andcoherent_gift_phrase_boundary_frozen',
        'B49 policy:14 speech compiler positives/two typedlabels/allfivegates/scopednames':'B50 policy:3 speech compiler positives/no typedmenu/allfivegates/one scopedname',
        'Frozen Hodram-B49 contract changed':'Frozen Hodram-B50 contract changed',
        'approved B49':'approved B50',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,all_three_records_five_gates_source_current_final_references_profile_prose_names_no_menu_guards_tested=True,all_mutations_must_actually_change_inputs_andnot_be_hidden_by_dependency_failure=True,new_credit=0,full_goal_complete=False))
