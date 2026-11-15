"""Fresh fixed-selector paragraphs with dependency-exact native macro proof reuse."""
from copy import deepcopy
from pathlib import Path
import re
from scripts.meaning_maria337_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

PROSE=Path('translations/maria_B125_B136_contextual_review_v1.json')

def main():
    out=ROOT/'formatting_v1'; assert not out.exists()
    currentpath=ROOT/'current_v1/current_effective.json'; namepath=ROOT/'scoped_names_macros_reference_v1.json'
    oldpath=Path('work/Maria_B96_B124_clean_20261109/formatting_v1/native_macro_measurements.json')
    doc,current,names,prior=map(load,[PROSE,currentpath,namepath,oldpath]); runtime=current['runtime']
    assert runtime==doc['runtime']==names['runtime']
    now=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=3)
    old=RegisteredRuntime(prior['runtime']['release_proof'],prior['runtime']['startup_proof'],captain=3)
    assert now.receipt()==runtime and old.receipt()==prior['runtime']
    assert digest('translations/release_stack.json')==now.release['registry_sha256']
    assert now.arm==old.arm and now.common==old.common and now.actor_root==old.actor_root and now.actor_bytes==old.actor_bytes
    assert now.arm[0x7f244:0x7f248]==old.arm[0x7f244:0x7f248]
    assert now.expected_captain==old.expected_captain==now.startup['actual_captain_getter']==old.startup['actual_captain_getter']==3
    assert now.image.read_file('/GRP/KANJI.FNT')==old.image.read_file('/GRP/KANJI.FNT')
    expected={r['token']:r['text'] for r in names['default_macro_cases']}
    assert {t:v['text'] for t,v in prior['defaults'].items()}==expected==dict(FI='Maria',FA='Li',FO='Li Clan',FU='Maria Huamei Li')
    assert prior['default_macro_all_four_alignment_cases_pass'] and prior['FE_null_actor_FI_four_alignment_cases_pass']
    adapter=prior['source_owned_progressive_adapter']
    assert 'assert captain==3 and identity==(prefix if prefix<207 else DYNAMIC_BINDINGS[prefix])' in adapter
    rows=[]; tokens=0
    for original in doc['records']:
        row=deepcopy(original)
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        row['editorial_logical_English']=row['english']
        row['english']=re.sub(r'\b(FI|FA|FO|FU)\b',lambda m:'{MACRO:'+m[0]+'}',row['english'])
        assert re.sub(r'\{MACRO:(FI|FA|FO|FU)\}',lambda m:m[1],row['english'])==row['editorial_logical_English']
        for token,count in row['source_macros'].items():
            assert row['english'].count('{MACRO:'+token+'}')==count; tokens+=count
        if row['kind']!='typed-choice-label':
            assert row['source_selector']<207 or row['source_selector']==254
            assert isinstance(row['source_record_index'],int) and not row.get('native_object_kind')
            row['planned_English_markup']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english']
            row['prior_macro_normalized_comparison']=row['english'] if row['decision']=='retention' else None
        rows.append(row)
    assert len(rows)==337 and sum(r['kind']=='progressive' for r in rows)==329
    assert sum(r['kind']=='system-FE' for r in rows)==6 and sum(r['kind']=='typed-choice-label' for r in rows)==2 and tokens==13
    out.mkdir(); rolepath=out/'role_bindings.json'
    save(rolepath,dict(runtime=runtime,source_records=[],source_selectors=[],native_roles=dict(rows=[]),
        no_dynamic_source_selectors_orstyle_objects=True,all335_speech_selectors_exact_fixed_orFE=True,
        FE_not_resolved_as_actor254=True,no_role_roster_event_RNG_orname_assignment=True,new_credit=0,
        evidence={str(PROSE):digest(PROSE)}))
    macropath=out/'native_macro_measurements.json'
    save(macropath,{**prior,'runtime':runtime,'source_owned_progressive_adapter':adapter,
        'reused_original_runtime':prior['runtime'],'prior_native_measurements':str(oldpath),'prior_native_measurements_sha256':digest(oldpath),
        'exact_dependency_reuse':dict(complete_ARM9=True,complete_COMMON=True,complete_font=True,actor_root=True,
            complete_actor_model_block=True,captain3_original_native_getter=True,all_four_default_expansions=True),
        'native_assertion_only_dynamic_identity_extension':dict(role_proof=str(rolepath),role_proof_sha256=digest(rolepath),
            no_dynamic_roles_in_this_scope=True,no_original_instruction_orABI_change=True,per_record_native_expansion_alignment_still_required=True),
        'no_native_default_macro_cases_reexecuted':True,'fresh_formatted_record_alignment_andpixels_still_pending':True,
        'evidence':{**prior['evidence'],**{str(p):digest(p) for p in [PROSE,currentpath,namepath,oldpath,rolepath,Path(__file__)]}}})
    save(out/'formatting_input.json',{**doc,'records':rows,'current_archive_sha256':current['current_archive_sha256'],
        'physical_speech_objects':335,'ordinary_speech_objects':335,'style_physical_speech_objects':0,'style_command_objects':0,
        'typed_choice_objects':2,'typed_choice_commands':1,'source_full_manuscript':str(PROSE),'source_full_manuscript_sha256':digest(PROSE),
        'native_macro_tokens_explicitly_marked_no_other_prose_changes':True,'macro_proof_sha256':digest(macropath),
        'all_individual_four_prose_gates_pass':True,'source_macro_occurrences':tokens})
    save(out/'initial_preferences.json',dict(records={},progressive_width_px=216,FE_physical_width_px=228,
        no_inherited_record_specific_narrowing_orbreaks=True,author_inserted_ordinary_breaks=0,new_credit=0))
    print('Prepared335 bodies/two captions/13 explicit macros;exact20 default macro proofs reused,fresh formatting pending.')

if __name__=='__main__':main()
