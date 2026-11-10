"""Prepare full-width paragraphs and qualify the separate current Maria FE macro path."""
from copy import deepcopy
import inspect
from pathlib import Path
import re
from dk4tool.patch.main_pool_cache_visibility import BASE
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text

ROOT=Path('work/Maria_B37_B50_clean_20261109')
OUT=ROOT/'formatting_v1'
PROSE=Path('translations/maria_B37_B50_contextual_review_v1.json')

def main():
    assert not OUT.exists()
    current_path=ROOT/'current_v1/current_effective.json';reference_path=ROOT/'scoped_names_macros_reference_v1.json'
    old_macros=Path('work/Maria_B0_B32_clean_20261109/formatting_v1/native_macro_measurements.json')
    doc,current,reference=map(load,[PROSE,current_path,reference_path])
    runtime=current['runtime'];assert runtime==doc['runtime']==reference['runtime'] and runtime['captain']==3
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=3)
    assert ctx.receipt()==runtime and digest('translations/release_stack.json')==ctx.release['registry_sha256']
    adapter=checked_text(inspect.getsource(expand),{'assert identity==prefix and captain==2':'assert identity==prefix and captain==3'})
    env={**expand.__globals__,'BASE':BASE}
    exec(compile(adapter,__file__+'::same-original-progressive-macro-ABI-current-Maria','exec'),env)
    defaults={};expected={r['token']:r['text'] for r in reference['default_macro_cases']}
    for token in ['FI','FA','FO','FU']:
        proof=ctx.execute(env['expand'],token.encode(),3)
        assert len(proof['cases'])==4 and all(bytes.fromhex(c['output_hex']).decode('ascii')==expected[token] for c in proof['cases'])
        defaults[token]=dict(text=expected[token],native=proof)
    fe_source=checked_text(load(old_macros)['source_owned_FE_adapter'],{
        "b'Hodram'":"b'Maria'","b'Bergstrom'":"b'Li'","b'Bergstrom Fleet'":"b'Li Clan'"})
    fe_env={**expand.__globals__,'BASE':BASE}
    exec(compile(fe_source,__file__+'::same-original-null-actor-FE-expander-Maria-default-expectations','exec'),fe_env)
    fe=ctx.execute(fe_env['expand'],b'FI')
    assert len(fe['cases'])==4 and all(bytes.fromhex(c['output_hex'])==b'Maria' for c in fe['cases'])
    rows=[];tokens=0
    for original in doc['records']:
        row=deepcopy(original)
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        row['editorial_logical_English']=row['english']
        row['english']=re.sub(r'\b(FI|FA|FO|FU)\b',lambda m:'{MACRO:'+m[0]+'}',row['english'])
        assert re.sub(r'\{MACRO:(FI|FA|FO|FU)\}',lambda m:m[1],row['english'])==row['editorial_logical_English']
        for macro,count in row['native_literal_token_counts'].items():
            assert row['english'].count('{MACRO:'+macro+'}')==count;tokens+=count
        if row['kind']!='typed-choice-label':
            row['planned_English_markup']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english']
            row['prior_macro_normalized_comparison']=row['english'] if row['decision']=='retention' else None
            if row['kind']=='system-FE':
                row.update(source_FE_presentation_kind=row['source_presentation_kind'],FE_is_not_an_ordinary_actor_nameplate=True)
        rows.append(row)
    assert len(rows)==286 and sum(r['kind']=='progressive' for r in rows)==269
    assert sum(r['kind']=='system-FE' for r in rows)==13 and sum(r['kind']=='typed-choice-label' for r in rows)==4 and tokens==21
    OUT.mkdir()
    macros=OUT/'native_macro_measurements.json'
    save(macros,dict(runtime=runtime,macro_ascii_lengths={k:len(v['text']) for k,v in defaults.items()},defaults=defaults,
        source_owned_progressive_adapter=adapter,source_owned_FE_adapter=fe_source,FE_FI_preflight=fe,
        default_macro_all_four_alignment_cases_pass=True,FE_null_actor_FI_four_alignment_cases_pass=True,
        original_wrapper_input_output_canaries_andunowned_memory_guards_preserved=True,
        per_record_formatted_expansion_pages_andrendering_still_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [PROSE,current_path,reference_path,old_macros,Path(__file__)]}))
    save(OUT/'role_bindings.json',dict(runtime=runtime,source_records=[],native_roles=dict(rows=[]),
        no_dynamic_selectors_in_source_batch=True,FE_not_resolved_as_actor254_orfallback208=True,new_credit=0))
    save(OUT/'formatting_input.json',{**doc,'records':rows,'current_archive_sha256':current['current_archive_sha256'],
        'physical_speech_objects':282,'ordinary_speech_objects':282,'style_physical_speech_objects':0,'style_command_objects':0,
        'typed_choice_objects':4,'typed_choice_commands':2,'source_full_manuscript':str(PROSE),
        'source_full_manuscript_sha256':digest(PROSE),'native_macro_tokens_explicitly_marked_no_other_prose_changes':True,
        'macro_proof_sha256':digest(macros),'no_historical_Maria_FA3_orfive_row_assumption':True,
        'all_individual_four_prose_gates_pass':True,'source_macro_occurrences':tokens})
    save(OUT/'initial_preferences.json',dict(records={},progressive_width_px=216,FE_physical_width_px=228,
        no_inherited_record_specific_narrowing_orbreaks=True,author_inserted_ordinary_breaks=0,new_credit=0))
    print('Prepared282 bodies/four captions;21 substitutions;16 default progressive andfour null-actor FE macro cases pass;zero credit.')

if __name__=='__main__':main()
