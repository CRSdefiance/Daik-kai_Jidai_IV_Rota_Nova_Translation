"""Measure newly scoped FU with the original wrapper; reuse exact FI/FA/FO dependencies."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.generic_name_macro_owned_v5886b import expand as original_expand

SOURCE=Path('translations/rafael_B141_B160_formatting_manuscript_v1.json')
OUT=Path('translations/rafael_B141_B160_formatting_manuscript_v2.json')
IDENTITY=Path('work/analysis/Rafael557_names_terms_v1_20261105/names_terms_andconsumer_dependency_qualification.json')
MACROS=Path('work/analysis/Rafael261_names_terms_20261105/names_macros_andconsumer_dependency_qualification_v1.json')
ADAPTERS=Path('work/analysis/Rafael_early_tutorial_B42_B43_source_display_20261104/40_native_selectors_macros_andcomplete_preamble_bindings.json')
ROOT=Path('work/analysis/Rafael557_macros_inputs_v1_20261105')

if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    doc,identity,macros,adapters=map(load,[SOURCE,IDENTITY,MACROS,ADAPTERS])
    ctx=RegisteredRuntime(identity['runtime']['release_proof'],identity['runtime']['startup_proof'],captain=0)
    previous=RegisteredRuntime(macros['runtime']['release_proof'],macros['runtime']['startup_proof'],captain=0)
    assert ctx.receipt()==identity['runtime'] and ctx.arm==previous.arm and ctx.common==previous.common
    assert ctx.actor_root==previous.actor_root and ctx.actor_bytes==previous.actor_bytes
    assert ctx.image.read_file('/GRP/KANJI.FNT')==previous.image.read_file('/GRP/KANJI.FNT')
    assert macros['complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified']
    assert macros['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10)
    default_path=Path(macros['same_Rafael_default_macro_proof'])
    assert sha(default_path.read_bytes())==macros['same_Rafael_default_macro_proof_sha256']
    default=load(default_path)
    assert all(c['output_hex']==b'Rafael Castor Castor Co.'.hex() for c in default['own_native_default_macro_cases']['cases'])
    actor0=next(r for r in identity['name_bindings'] if r['actor_ID']==0)
    fullname=next(r['text'] for r in actor0['current_consumers'] if r['consumer']=='full-catalogue')
    assert fullname=='Rafael Castor' and fullname.isascii()
    adapter=adapters['source_owned_progressive_adapter']
    env=dict(original_expand.__globals__);exec(compile(adapter,__file__+'::unchanged-original-wrapper-own-current-runtime','exec'),env)
    expand=env['expand'];cases=[]
    new_default=ctx.execute(expand,b'FU',0)
    assert len(new_default['cases'])==4 and all(c['output_hex']==fullname.encode().hex() for c in new_default['cases'])
    for row in doc['records']:
        if 'FU' not in row['native_literal_token_counts']:continue
        body=row['editorial_logical_English'].encode('ascii')
        result=ctx.execute(expand,body,row['source_selector'])
        expected=body.replace(b'FU',fullname.encode('ascii'))
        assert all(c['output_hex']==expected.hex() for c in result['cases'])
        cases.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],
            source_complete_preamble_hex=row['source_complete_preamble_hex'],source_hex=row['source_hex'],
            logical_English=row['editorial_logical_English'],expected_hex=expected.hex(),native_wrapper=result))
    assert [r['id'] for r in cases]==['DK4_MES_B143_R0067','DK4_MES_B146_R0006']
    ROOT.mkdir(parents=True)
    qualified=deepcopy(identity)
    qualified.update(complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified=True,
        exact_current_code_COMMON_font_complete_actor_array_andmacro_data_reuse=True,
        same_Rafael_default_macro_proof=str(default_path),same_Rafael_default_macro_proof_sha256=sha(default_path.read_bytes()),
        macro_ascii_lengths=dict(FI=6,FA=6,FO=10,FU=len(fullname)),
        macro_widths=dict(FI=36,FA=36,FO=60,FU=6*len(fullname),I=12),
        full_name=fullname,fresh_FU_default=new_default,fresh_FU_records=cases,
        fresh_FU_original_wrapper_alignment_cases=12,source_owned_progressive_adapter=adapter,
        prior_FI_FA_FO_macro_proof=str(MACROS),prior_FI_FA_FO_macro_proof_sha256=sha(MACROS.read_bytes()),
        dynamic_roles=[],no_new_FI_FA_FO_permutation_oractor_name_getter_execution=True,
        no_new_page_font_plane_gameplay_ROM_orcredit=True)
    qualified['evidence'].update({str(p):sha(p.read_bytes()) for p in [IDENTITY,MACROS,ADAPTERS,default_path,SOURCE,Path(__file__)]})
    proof=ROOT/'qualified_identity_andmacros.json';save(proof,qualified)
    prepared=deepcopy(doc);fe=[]
    kinds={(143,233):'market share grant',(143,258):'NPC gold receipt',(143,274):'player campaign funds receipt',
        (145,52):'knocking sound',(148,121):'market share grant',(148,152):'market share grant'}
    for row in prepared['records']:
        if row['kind']=='system-FE':
            assert row['source_complete_preamble_hex']=='0040ffff00fe'
            row['source_FE_presentation_kind']=kinds[row['block'],row['source_record_index']]
            row['FE_is_not_an_ordinary_actor_nameplate']=True;fe.append(row['id'])
        if row['kind']!='typed-choice-label' and not row['english'].isascii():
            assert row['decision']=='retention' and row['deliberate_source_punctuation_retention']
            prior=row['current_comparison_paragraph'].strip()
            import re
            row['prior_macro_normalized_comparison']=re.sub(r'\b(FI|FA|FO|FU)\b',lambda m:'{MACRO:'+m[0]+'}',prior)
            assert row['english']==row['prior_macro_normalized_comparison']
        if row.get('FU_current_expansion_width_anddisplay_pending'):
            row['FU_current_expansion_parity_andwidth_qualified']=True
            row['FU_current_expansion_width_anddisplay_pending']=True # Complete rendered display remains pending.
    assert len(fe)==6
    prepared.update(previous_formatting_input=str(SOURCE),previous_formatting_input_sha256=sha(SOURCE.read_bytes()),
        scoped_identity_proof=str(proof),scoped_identity_proof_sha256=sha(proof.read_bytes()),
        macro_ascii_lengths=qualified['macro_ascii_lengths'],macro_widths=qualified['macro_widths'],source_FE_objects=fe,
        current_FU_expansion_parity_width_anddisplay_proof_pending=False,current_FU_native_display_still_pending=True,
        scoped_identity_andmacro_proofs_qualified=True,no_prose_controls_decisions_orreview_gates_changed=True)
    assert all(a['english']==b['english'] and a['review']==b['review'] for a,b in zip(doc['records'],prepared['records'],strict=True))
    prepared['evidence'].update({str(p):sha(p.read_bytes()) for p in [SOURCE,proof,Path(__file__)]})
    save(OUT,prepared)
    print('QualifiedFU=Rafael Castor:13ASCII/78px;12 original-wrapper alignment cases. ReusedFI/FA/FO exactdependencies. Classified6FE panels;retained punctuation bound. Allnewdisplay/formatting gates pending.')
