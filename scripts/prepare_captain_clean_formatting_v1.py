"""Prepare reviewed mixed objects using explicit captain and original macro guards."""
import argparse
from collections import Counter
from copy import deepcopy
import inspect
from pathlib import Path
import re
from dk4tool.patch.main_pool_cache_visibility import BASE
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for key in ['root','prose','FE-source-macros']:
        ap.add_argument('--'+key,type=Path,required=True)
    ap.add_argument('--captain',type=int,choices=range(4),required=True)
    args = ap.parse_args()
    out = args.root/'formatting_v1'
    assert not out.exists()
    currentpath = args.root/'current_v1/current_effective.json'
    namespath = args.root/'scoped_names_macros_reference_v1.json'
    rolespath = args.root/'dynamic_roles_current_v1.json'
    objectspath = args.root/'current_objects_v1/current_objects.json'
    doc,current,names,roles,objects = map(load,[args.prose,currentpath,namespath,rolespath,objectspath])
    runtime = current['runtime']
    assert all(d['runtime']==runtime for d in [doc,names,roles,objects]) and runtime['captain']==args.captain
    ctx = RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=args.captain)
    assert ctx.receipt()==runtime and digest('translations/release_stack.json')==ctx.release['registry_sha256']
    dynamic = {r['source_selector']:r['resolved_actor_ID'] for r in roles['native_roles']['rows']}
    adapter = checked_text(inspect.getsource(expand), {
        'assert identity==prefix and captain==2':
        f'assert captain=={args.captain} and identity==(prefix if prefix<207 else DYNAMIC_BINDINGS[prefix])'})
    env = {**expand.__globals__,'BASE':BASE,'DYNAMIC_BINDINGS':dynamic}
    exec(compile(adapter,__file__+'::same-original-progressive-ABI-explicit-captain-androles','exec'),env)
    expected = {r['token']:r['text'] for r in names['default_macro_cases']}
    defaults = {}
    for token in ['FI','FA','FO','FU']:
        proof = ctx.execute(env['expand'],token.encode(),args.captain)
        assert len(proof['cases'])==4
        assert all(bytes.fromhex(c['output_hex']).decode('ascii')==expected[token] for c in proof['cases'])
        defaults[token] = dict(text=expected[token],native=proof)
    prior = load(args.FE_source_macros)
    replacements = {repr(prior['defaults'][t]['text'].encode()):repr(expected[t].encode()) for t in ['FI','FA','FO']}
    fe_source = checked_text(prior['source_owned_FE_adapter'],replacements)
    fe_env = {**expand.__globals__,'BASE':BASE}
    exec(compile(fe_source,__file__+'::same-original-null-actor-FE-ABI-explicit-default-expectations','exec'),fe_env)
    fe = ctx.execute(fe_env['expand'],b'FI')
    assert len(fe['cases'])==4 and all(bytes.fromhex(c['output_hex']).decode('ascii')==expected['FI'] for c in fe['cases'])
    rows = []
    tokens = 0
    for original in doc['records']:
        row = deepcopy(original)
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        row['editorial_logical_English'] = row['english']
        row['english'] = re.sub(r'\b(FI|FA|FO|FU)\b',lambda m:'{MACRO:'+m[0]+'}',row['english'])
        assert re.sub(r'\{MACRO:(FI|FA|FO|FU)\}',lambda m:m[1],row['english'])==row['editorial_logical_English']
        for token,count in row['source_macros'].items():
            assert row['english'].count('{MACRO:'+token+'}')==count
            tokens += count
        if row['kind']!='typed-choice-label':
            assert isinstance(row['source_record_index'],int)
            row['planned_English_markup'] = '{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english']
            row['prior_macro_normalized_comparison'] = row['english'] if row['decision']=='retention' else None
            if row.get('native_object_kind')=='4100-style-alternative':
                row['virtual_formatter_prefix_is_not_part_of_stored_alternative_text'] = True
                assert row['source_choice_object_hex']==row['source_object_hex']
        rows.append(row)
    kinds = Counter(r['kind'] for r in rows)
    assert sum(kinds.values())==doc['source_objects']
    assert kinds['typed-choice-label']==len(objects['choice_records'])
    styles = sum(r.get('native_object_kind')=='4100-style-alternative' for r in rows)
    assert styles==len(objects['style_records'])
    out.mkdir()
    macrospath = out/'native_macro_measurements.json'
    save(macrospath,dict(runtime=runtime,macro_ascii_lengths={k:len(v['text']) for k,v in defaults.items()},defaults=defaults,
        source_owned_progressive_adapter=adapter,source_owned_FE_adapter=fe_source,FE_FI_preflight=fe,
        default_macro_all_four_alignment_cases_pass=True,FE_null_actor_FI_four_alignment_cases_pass=True,
        original_wrapper_input_output_canaries_andunowned_memory_guards_preserved=True,
        fresh20_native_preflight_cases_not_new_renderer_characterization=True,
        per_record_formatted_expansion_pages_andrendering_still_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [args.prose,currentpath,namespath,rolespath,objectspath,args.FE_source_macros,Path(__file__)]}))
    save(out/'role_bindings.json',roles)
    save(out/'formatting_input.json',{**doc,'records':rows,'current_archive_sha256':current['current_archive_sha256'],
        'physical_speech_objects':len(rows)-kinds['typed-choice-label'],
        'ordinary_speech_objects':len(rows)-kinds['typed-choice-label']-styles,
        'style_physical_speech_objects':styles,'style_command_objects':len(objects['style_objects']),
        'typed_choice_objects':kinds['typed-choice-label'],'typed_choice_commands':len(objects['choice_objects']),
        'source_full_manuscript':str(args.prose),'source_full_manuscript_sha256':digest(args.prose),
        'native_macro_tokens_explicitly_marked_no_other_prose_changes':True,
        'macro_proof_sha256':digest(macrospath),'all_individual_four_prose_gates_pass':True,'source_macro_occurrences':tokens})
    save(out/'initial_preferences.json',dict(records={},progressive_width_px=216,FE_physical_width_px=228,
        no_inherited_record_specific_narrowing_orbreaks=True,author_inserted_ordinary_breaks=0,new_credit=0))
    print(dict(records=len(rows),kinds=dict(kinds),macro_occurrences=tokens,macro_lengths={k:len(v['text']) for k,v in defaults.items()},
        fresh_native_macro_preflight_cases=20,formatting_andpixels_pending=True,new_credit=0))


if __name__ == '__main__':
    main()
