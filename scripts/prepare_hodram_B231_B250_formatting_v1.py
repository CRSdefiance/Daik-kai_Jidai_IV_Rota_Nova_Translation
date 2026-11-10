"""Bind logical prose, scoped identity/terms and distinct progressive/FE macro ABIs."""
from copy import deepcopy
from pathlib import Path
import re
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as FE_expand
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.refine_hodram_B231_B250_terms_v2 import OUT as PROSE
from scripts.review_hodram_B231_B250_contextual_v1 import CURRENT,OBJECTS
from scripts.review_hodram_B231_B250_names_terms_v1 import NATIVE as NAMES,REVIEW as NAME_REVIEW,TERMS,ROLES,ROOT

OUT=ROOT/'formatting_v1'
FORMATTING=OUT/'formatting_input.json'
MACROS=OUT/'native_macro_measurements.json'
PREFERENCES=OUT/'initial_preferences.json'
PROGRESSIVE=Path('work/Hodram_B211_B230_resume_20261106/formatting_v1/native_macro_measurements.json')
FE=Path('work/analysis/Hodram_B61_B70_logical_v8891/logical_paragraphs.json')

def main():
    assert not OUT.exists()
    prose,current,objects,names,terms,roles=map(load,(PROSE,CURRENT,OBJECTS,NAMES,TERMS,ROLES))
    runtime=current['runtime'];assert runtime==objects['runtime']==names['runtime']==terms['runtime']==roles['runtime']
    assert len(prose['records'])==225 and prose['counts']=={'retention':110,'revision':115} and not prose['remaining_contextual_comparisons']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=1)
    assert ctx.receipt()==runtime and digest('translations/release_stack.json')==ctx.release['registry_sha256']
    prog_source=load(PROGRESSIVE)['source_owned_progressive_adapter'];fe_source=load(FE)['source_owned_FE_adapter']
    p_env=dict(progressive_expand.__globals__);f_env=dict(FE_expand.__globals__)
    exec(compile(prog_source,__file__+'::original-progressive-macro-ABI','exec'),p_env)
    exec(compile(fe_source,__file__+'::original-null-actor-FE-macro-ABI','exec'),f_env)
    defaults={}
    for token in ('FI','FA','FO'):
        proof=ctx.execute(p_env['expand'],token.encode(),1)
        assert len(proof['cases'])==4 and len({r['output_hex'] for r in proof['cases']})==1
        defaults[token]=dict(text=bytes.fromhex(proof['cases'][0]['output_hex']).decode('ascii'),native=proof)
    assert {k:len(v['text']) for k,v in defaults.items()}==dict(FI=6,FA=9,FO=15)
    macro_rows=[]
    for row in prose['records']:
        if '{MACRO:' not in row['english']:continue
        body=re.sub(r'\{MACRO:(FI|FA|FO)\}',lambda m:m[1],row['english']).encode('ascii')
        expected=re.sub(r'\{MACRO:(FI|FA|FO)\}',lambda m:defaults[m[1]]['text'],row['english']).encode('ascii')
        is_FE=row['source_selector']==254
        proof=ctx.execute(f_env['expand'] if is_FE else p_env['expand'],body,*(() if is_FE else (row['source_selector'],)))
        assert len(proof['cases'])==4 and all(c['output_hex']==expected.hex() for c in proof['cases'])
        macro_rows.append(dict(id=row['id'],kind='null-actor-FE' if is_FE else 'progressive',expected_hex=expected.hex(),native=proof))
    assert len(macro_rows)==4 and sum(r['kind']=='null-actor-FE' for r in macro_rows)==1
    rows=[]
    fe_kinds={'DK4_MES_B242_R0036':'item-handover','DK4_MES_B243_R0163':'permanent-attribute-result',
        'DK4_MES_B250_R0010':'gold-award','DK4_MES_B250_R0034':'market-share-result'}
    for original in prose['records']:
        row=deepcopy(original);row.update(editorial_logical_English=row['english'],fresh_formatting_binding_pending=True)
        if row.get('kind')!='typed-choice-label':
            row['kind']='system-FE' if row['source_selector']==254 else 'progressive'
            if 'source_style_indices' in row:row['native_object_kind']='4100-style-alternative'
            ref=row['source_reference'];row['source_record_index']=ref.get('record_index',ref.get('physical_record_index'))
            assert isinstance(row['source_record_index'],int)
            row['planned_English_markup']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english']
            row['prior_macro_normalized_comparison']=row['english'] if row['decision']=='retention' else None
            if row['kind']=='system-FE':
                row['source_FE_presentation_kind']=fe_kinds[row['id']];row['FE_is_not_an_ordinary_actor_nameplate']=True
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        rows.append(row)
    assert sum(r['kind']=='progressive' for r in rows)==219 and sum(r['kind']=='system-FE' for r in rows)==4
    OUT.mkdir()
    save(MACROS,dict(runtime=runtime,macro_ascii_lengths=dict(FI=6,FA=9,FO=15),defaults=defaults,logical_macro_records=macro_rows,
        source_owned_progressive_adapter=prog_source,source_owned_FE_adapter=fe_source,
        progressive_andFE_original_distinct_ABIs_preserved=True,all_four_native_alignment_cases_andcanaries_pass=True,new_credit=0,
        evidence={str(p):digest(p) for p in (PROGRESSIVE,FE,PROSE,CURRENT,Path(__file__))}))
    save(FORMATTING,{**prose,'records':rows,'runtime':runtime,'current_ROM':current['current_ROM'],
        'current_ROM_sha256':current['current_ROM_sha256'],'current_archive_sha256':current['current_archive_sha256'],
        'blocks':[g['block'] for g in current['groups']],'physical_speech_objects':223,'ordinary_speech_objects':209,
        'style_physical_speech_objects':14,'style_command_objects':2,'typed_choice_objects':2,'typed_choice_commands':1,
        'all_individual_four_prose_gates_pass':True,'source_full_manuscript':str(PROSE),'source_full_manuscript_sha256':digest(PROSE),
        'scoped_names':str(NAME_REVIEW),'scoped_names_sha256':digest(NAME_REVIEW),'native_names_sha256':digest(NAMES),
        'macro_proof_sha256':digest(MACROS),'term_proof_sha256':digest(TERMS),'dynamic_roles_sha256':digest(ROLES),
        'no_editorial_wording_or_decision_changes':True})
    save(PREFERENCES,dict(records={},progressive_width_px=216,FE_physical_width_px=228,
        no_old_record_specific_guard_orsemantic_preference_inherited=True,author_inserted_ordinary_breaks=0,new_credit=0))
    print('Prepared 223 logical bodies/two captions; four macro speeches pass both original ABIs in all alignments.')

if __name__=='__main__':main()
