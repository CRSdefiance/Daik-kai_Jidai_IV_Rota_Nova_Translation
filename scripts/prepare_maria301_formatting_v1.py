"""Prepare logical paragraphs with measured current Maria macros andexact source/style headers."""
from copy import deepcopy
import inspect
from pathlib import Path
import re
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text

ROOT=Path('work/Maria_B0_B32_clean_20261109')
OUT=ROOT/'formatting_v1'
PROSE=Path('translations/maria_B0_B32_contextual_review_v1.json')


def main():
    assert not OUT.exists()
    doc,current,roles,packet,reference=map(load,[PROSE,ROOT/'current_v1/current_effective.json',
        ROOT/'dynamic_roles_current_v1.json',ROOT/'clean_source_packet.json',ROOT/'scoped_names_items_macros_reference_v1.json'])
    runtime=current['runtime']
    assert runtime==doc['runtime']==roles['runtime']==reference['runtime'] and runtime['captain']==3
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=3)
    assert ctx.receipt()==runtime and digest('translations/release_stack.json')==ctx.release['registry_sha256']
    dynamic={r['source_selector']:r['resolved_actor_ID'] for r in roles['native_roles']['rows']}
    adapter=checked_text(inspect.getsource(expand),{
        'assert identity==prefix and captain==2':
            'assert captain==3 and identity==(prefix if prefix<207 else DYNAMIC_BINDINGS[prefix])'})
    env={**expand.__globals__,'DYNAMIC_BINDINGS':dynamic}
    exec(compile(adapter,__file__+'::original-progressive-macro-wrapper-current-captain-androles','exec'),env)
    defaults={}
    expected={r['token']:r['text'] for r in reference['default_macro_cases']}
    for token in ['FI','FA','FO','FU']:
        proof=ctx.execute(env['expand'],token.encode(),3)
        assert len(proof['cases'])==4 and all(bytes.fromhex(c['output_hex']).decode('ascii')==expected[token] for c in proof['cases'])
        defaults[token]=dict(text=expected[token],native=proof)
    assert {k:len(v['text']) for k,v in defaults.items()}==dict(FI=5,FA=2,FO=7,FU=15)
    rows=[];tokens=0
    for original in doc['records']:
        row=deepcopy(original)
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        row['editorial_logical_English']=row['english']
        row['english']=re.sub(r'\b(FI|FA|FO|FU)\b',lambda m:'{MACRO:'+m[0]+'}',row['english'])
        assert re.sub(r'\{MACRO:(FI|FA|FO|FU)\}',lambda m:m[1],row['english'])==row['editorial_logical_English']
        for macro,count in row['native_literal_token_counts'].items():
            assert row['english'].count('{MACRO:'+macro+'}')==count
            tokens+=count
        if row['kind']!='typed-choice-label':
            assert isinstance(row['source_record_index'],int)
            row['planned_English_markup']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english']
            row['prior_macro_normalized_comparison']=row['english'] if row['decision']=='retention' else None
            if row.get('native_object_kind')=='4100-style-alternative':
                row['virtual_formatter_prefix_is_not_part_of_stored_alternative_text']=True
                row['source_choice_object_hex']=row['source_object_hex']
        rows.append(row)
    assert len(rows)==301 and sum(r['kind']=='progressive' for r in rows)==299
    assert sum(r['kind']=='typed-choice-label' for r in rows)==2
    OUT.mkdir()
    macros=OUT/'native_macro_measurements.json'
    save(macros,dict(runtime=runtime,macro_ascii_lengths={k:len(v['text']) for k,v in defaults.items()},defaults=defaults,
        source_owned_progressive_adapter=adapter,
        source_owned_FE_adapter=load('work/analysis/Hodram_B61_B70_logical_v8891/logical_paragraphs.json')['source_owned_FE_adapter'],
        no_FE_records_orFE_ABI_approval_in_this_batch=True,default_macro_all_four_alignment_cases_pass=True,
        original_wrapper_name_ring_input_output_andunowned_memory_guards_preserved=True,
        per_record_formatted_expansion_andall_pages_still_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [PROSE,ROOT/'dynamic_roles_current_v1.json',ROOT/'scoped_names_items_macros_reference_v1.json',Path(__file__)]}))
    projected_roles=deepcopy(roles)
    originals={r['id']:r for g in packet['groups'] for r in g['records']}
    for row in projected_roles['source_records']:
        source=originals[row['id']]
        assert row['source_reference']==source['source_reference'] and source['kind']=='physical-style-alternative'
        row.update(kind='4100-style-alternative',source_header_hex=source['source_header_hex'],
            source_style_indices=source['source_style_indices'],virtual_prefix_not_in_stored_body=True)
    projected_roles.update(original_role_proof=str(ROOT/'dynamic_roles_current_v1.json'),
        original_role_proof_sha256=digest(ROOT/'dynamic_roles_current_v1.json'),header_schema_projection_only=True)
    save(OUT/'role_bindings.json',projected_roles)
    save(OUT/'formatting_input.json',{**doc,'records':rows,'runtime':runtime,
        'current_archive_sha256':current['current_archive_sha256'],'physical_speech_objects':299,
        'ordinary_speech_objects':292,'style_physical_speech_objects':7,'style_command_objects':1,
        'typed_choice_objects':2,'typed_choice_commands':1,
        'source_full_manuscript':str(PROSE),'source_full_manuscript_sha256':digest(PROSE),
        'native_macro_tokens_explicitly_marked_no_other_prose_changes':True,
        'macro_proof_sha256':digest(macros),'no_historical_Maria_FA3_orfive_row_assumption':True,
        'all_individual_four_prose_gates_pass':True,'source_macro_occurrences':tokens})
    save(OUT/'initial_preferences.json',dict(records={},progressive_width_px=216,FE_physical_width_px=228,
        no_inherited_record_specific_narrowing_orbreaks=True,author_inserted_ordinary_breaks=0,new_credit=0))
    print('Prepared299 bodies/two captions;',tokens,'substitutions;current macro lengths5/2/7/15;four alignments each;zero credit.')


if __name__=='__main__':main()
