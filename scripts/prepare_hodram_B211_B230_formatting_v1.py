"""Prepare all reviewed objects on the exact own-Hodram runtime and measured macros."""
from copy import deepcopy
from pathlib import Path
import re
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_hodram_B211_B230_contextual_v1 import OUT as PROSE
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.generic_name_macro_owned_v5886b import expand as original_expand
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_hodram_B211_B230_names_v1 import NATIVE as NAMES,OUT as NAME_REVIEW
from scripts.review_hodram_B221_B230_contextual_v1 import CURRENT,OBJECTS,ROOT
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'formatting_v1'
FORMATTING=OUT/'formatting_input.json'
MACROS=OUT/'native_macro_measurements.json'
TERMS=OUT/'reused_term_dependencies.json'
PREFERENCES=OUT/'initial_preferences.json'
ROLES=ROOT/'role_bindings_v1.json'
OLD_TERMS=Path('work/analysis/Hodram_B211_B230_clean_20261104/source_current_term_checkpoint_v1.json')
ADAPTERS=Path('work/analysis/Rafael_early_tutorial_B42_B43_source_display_20261104/40_native_selectors_macros_andcomplete_preamble_bindings.json')

def main():
    assert not OUT.exists()
    prose,current,objects,names,roles,old_terms=map(load,(PROSE,CURRENT,OBJECTS,NAMES,ROLES,OLD_TERMS))
    runtime=current['runtime'];assert objects['runtime']==names['runtime']==roles['runtime']==runtime
    assert len(prose['records'])==277 and not prose['remaining_contextual_comparisons']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=1)
    assert ctx.receipt()==runtime and digest('translations/release_stack.json')==ctx.release['registry_sha256']
    for row in old_terms['equipment_terms']:
        at,pointer=row['pointer_field'],row['current_pointer']
        assert int.from_bytes(ctx.arm[at:at+4],'little')==pointer
        text=bytes.fromhex(row['current_hex']);start=pointer-0x02000000
        assert ctx.raw[start:start+len(text)+1]==text+b'\0'
    for row in old_terms['city_aliases']:
        at=row['current_pointer']-0x02000000
        raw=bytes.fromhex(row['current_span_hex'])
        assert ctx.arm[at:at+len(raw)]==raw
        field=row['pointer_field'];assert int.from_bytes(ctx.arm[field:field+4],'little')==row['current_pointer']
    adapter=checked_text(load(ADAPTERS)['source_owned_progressive_adapter'],{'assert identity==prefix and captain==0':'assert identity==prefix and captain==1'})
    env=dict(original_expand.__globals__)
    exec(compile(adapter,__file__+'::original-macro-ABI-own-Hodram','exec'),env)
    defaults={}
    for token in ['FI','FA','FO']:
        proof=ctx.execute(env['expand'],token.encode(),1)
        assert len(proof['cases'])==4 and len({c['output_hex'] for c in proof['cases']})==1
        text=bytes.fromhex(proof['cases'][0]['output_hex']).decode('ascii')
        defaults[token]=dict(text=text,native=proof)
    assert {k:len(v['text']) for k,v in defaults.items()}==dict(FI=6,FA=9,FO=15)
    macro_rows=[]
    for row in prose['records']:
        if '{MACRO:' not in row['english']:continue
        body=re.sub(r'\{MACRO:(FI|FA|FO)\}',lambda m:m[1],row['english'])
        expected=re.sub(r'\{MACRO:(FI|FA|FO)\}',lambda m:defaults[m[1]]['text'],row['english']).encode('cp932')
        proof=ctx.execute(env['expand'],body.encode('cp932'),row['source_selector'])
        assert len(proof['cases'])==4 and all(c['output_hex']==expected.hex() for c in proof['cases'])
        macro_rows.append(dict(id=row['id'],expected_hex=expected.hex(),native=proof))
    assert len(macro_rows)==1 and macro_rows[0]['id']=='DK4_MES_B215_R0040'
    rows=[]
    for original in prose['records']:
        row=deepcopy(original)
        row.update(editorial_logical_English=row['english'],fresh_formatting_binding_pending=True)
        if row.get('kind')!='typed-choice-label':
            row['kind']='system-FE' if row['source_selector']==254 else 'progressive'
            if 'source_style_indices' in row:row['native_object_kind']='4100-style-alternative'
            ref=row['source_reference'];row['source_record_index']=ref.get('record_index',ref.get('physical_record_index'))
            assert isinstance(row['source_record_index'],int)
            row['planned_English_markup']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english']
            row['prior_macro_normalized_comparison']=row['english'] if row['decision']=='retention' else None
            if row['kind']=='system-FE':
                row['source_FE_presentation_kind']='attribute-result' if row['block']==212 else 'swan-call-or-wingbeat'
                row['FE_is_not_an_ordinary_actor_nameplate']=True
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        rows.append(row)
    assert sum(r['kind']=='progressive' for r in rows)==266
    assert sum(r['kind']=='system-FE' for r in rows)==4
    OUT.mkdir(parents=True)
    save(MACROS,dict(runtime=runtime,macro_ascii_lengths=dict(FI=6,FA=9,FO=15),defaults=defaults,
        source_owned_progressive_adapter=adapter,logical_macro_records=macro_rows,
        all_four_native_alignment_cases_andcanaries_pass=True,new_credit=0,
        evidence={str(p):digest(p) for p in (ADAPTERS,PROSE,CURRENT,Path(__file__))}))
    save(TERMS,dict(runtime=runtime,prior=str(OLD_TERMS),prior_sha256=digest(OLD_TERMS),
        equipment_terms=18,Amsterdam_aliases=2,current_owned_term_bytes_andpointers_exact=True,
        source_term_proofs_reused_not_reexecuted=True,attribute=old_terms['attribute'],
        no_external_historical_or_extra_item_fact_claim=True,new_credit=0))
    save(FORMATTING,{**prose,'records':rows,'runtime':runtime,'current_ROM':current['current_ROM'],
        'current_ROM_sha256':current['current_ROM_sha256'],'current_archive_sha256':current['current_archive_sha256'],
        'blocks':list(range(211,231)),'physical_speech_objects':270,'ordinary_speech_objects':241,
        'style_physical_speech_objects':29,'style_command_objects':4,'typed_choice_objects':7,'typed_choice_commands':3,
        'all_individual_four_prose_gates_pass':True,'source_full_manuscript':str(PROSE),'source_full_manuscript_sha256':digest(PROSE),
        'scoped_names':str(NAME_REVIEW),'scoped_names_sha256':digest(NAME_REVIEW),'native_names_sha256':digest(NAMES),
        'macro_proof_sha256':digest(MACROS),'term_proof_sha256':digest(TERMS),'dynamic_roles_sha256':digest(ROLES),
        'no_editorial_wording_or_decision_changes':True})
    save(PREFERENCES,dict(records={},progressive_width_px=216,FE_physical_width_px=228,
        no_old_record_specific_guard_orsemantic_preference_inherited=True,author_inserted_ordinary_breaks=0,new_credit=0))
    print('Prepared 270 bodies and seven captions; one FI-bearing speech and all default macro lengths measured on current Hodram.')

if __name__=='__main__':main()
