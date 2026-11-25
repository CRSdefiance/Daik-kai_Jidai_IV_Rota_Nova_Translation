"""Prepare fresh303 layout inputs while reusing exactly matching native macro dependencies."""
from copy import deepcopy
from pathlib import Path
import re
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

ROOT=Path('work/Maria_B58_B70_clean_20261109')
PROSE=Path('translations/maria_B58_B70_contextual_review_v2.json')

def main():
    out=ROOT/'formatting_v1';assert not out.exists()
    current_path=ROOT/'current_v1/current_effective.json';reference_path=ROOT/'scoped_names_macros_reference_v1.json'
    old_path=Path('work/Maria_B51_B57_clean_20261109/formatting_v1/native_macro_measurements.json')
    doc,current,reference,prior=map(load,[PROSE,current_path,reference_path,old_path])
    runtime=current['runtime'];assert runtime==doc['runtime']==reference['runtime']
    now=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=3)
    old=RegisteredRuntime(prior['runtime']['release_proof'],prior['runtime']['startup_proof'],captain=3)
    assert now.receipt()==runtime and old.receipt()==prior['runtime']
    assert digest('translations/release_stack.json')==now.release['registry_sha256']
    assert now.arm==old.arm and now.common==old.common
    assert now.actor_root==old.actor_root and now.actor_bytes==old.actor_bytes
    assert now.raw[0x7f244:0x7f248]==old.raw[0x7f244:0x7f248]==b'\x03\0\0\0'
    assert now.image.read_file('/GRP/KANJI.FNT')==old.image.read_file('/GRP/KANJI.FNT')
    expected={r['token']:r['text'] for r in reference['default_macro_cases']}
    assert {t:v['text'] for t,v in prior['defaults'].items()}==expected==dict(FI='Maria',FA='Li',FO='Li Clan',FU='Maria Huamei Li')
    assert prior['default_macro_all_four_alignment_cases_pass'] and prior['FE_null_actor_FI_four_alignment_cases_pass']
    rows=[];tokens=0
    for original in doc['records']:
        row=deepcopy(original);assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        row['editorial_logical_English']=row['english']
        row['english']=re.sub(r'\b(FI|FA|FO|FU)\b',lambda m:'{MACRO:'+m[0]+'}',row['english'])
        assert re.sub(r'\{MACRO:(FI|FA|FO|FU)\}',lambda m:m[1],row['english'])==row['editorial_logical_English']
        for token,count in row['source_macros'].items():
            assert row['english'].count('{MACRO:'+token+'}')==count;tokens+=count
        if row['kind']!='typed-choice-label':
            row['planned_English_markup']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english']
            row['prior_macro_normalized_comparison']=row['english'] if row['decision']=='retention' else None
            if row['kind']=='system-FE':
                row.update(source_presentation_kind='system-FE',source_FE_presentation_kind='system-FE',
                    FE_is_not_an_ordinary_actor_nameplate=True)
        rows.append(row)
    assert len(rows)==303 and sum(r['kind']=='progressive' for r in rows)==287
    assert sum(r['kind']=='system-FE' for r in rows)==12 and sum(r['kind']=='typed-choice-label' for r in rows)==4 and tokens==16
    out.mkdir()
    macro_path=out/'native_macro_measurements.json'
    save(macro_path,{**prior,'runtime':runtime,'reused_original_runtime':prior['runtime'],
        'prior_native_measurements':str(old_path),'prior_native_measurements_sha256':digest(old_path),
        'exact_dependency_reuse':dict(complete_ARM9=True,complete_COMMON=True,complete_font=True,
            actor_root=True,complete_actor_model_block=True,captain3_word=True,all_four_default_expansions=True),
        'no_native_macro_cases_reexecuted':True,'fresh_formatted_record_alignment_andpixels_still_pending':True,
        'evidence':{**prior['evidence'],**{str(p):digest(p) for p in [PROSE,current_path,reference_path,old_path,Path(__file__)]}}})
    save(out/'role_bindings.json',dict(runtime=runtime,source_records=[],native_roles=dict(rows=[]),
        no_dynamic_selectors_in_source_batch=True,FE_not_resolved_as_actor254_orfallback208=True,new_credit=0))
    save(out/'formatting_input.json',{**doc,'records':rows,'current_archive_sha256':current['current_archive_sha256'],
        'physical_speech_objects':299,'ordinary_speech_objects':299,'style_physical_speech_objects':0,'style_command_objects':0,
        'typed_choice_objects':4,'typed_choice_commands':2,'source_full_manuscript':str(PROSE),
        'source_full_manuscript_sha256':digest(PROSE),'native_macro_tokens_explicitly_marked_no_other_prose_changes':True,
        'macro_proof_sha256':digest(macro_path),'all_individual_four_prose_gates_pass':True,'source_macro_occurrences':tokens})
    save(out/'initial_preferences.json',dict(records={},progressive_width_px=216,FE_physical_width_px=228,
        no_inherited_record_specific_narrowing_orbreaks=True,author_inserted_ordinary_breaks=0,new_credit=0))
    print('Prepared299 bodies/four captions and16 tokens. Reused20 native macro cases after exact ARM9/COMMON/font/actor/captain/default matches;fresh formatting pending.')

if __name__=='__main__':main()
