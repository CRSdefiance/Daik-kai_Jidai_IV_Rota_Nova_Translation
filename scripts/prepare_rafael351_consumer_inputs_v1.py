"""Restore exact compound-caption metadata and expose already qualified macro dependencies."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from dk4tool.patch.grand_race_menu_release import sha

DOC=Path('translations/rafael_B121_B140_formatting_manuscript_v4.json')
OBJECTS=Path('work/analysis/Rafael351_current_objects_v1_20261105/current_objects.json')
IDENTITY=Path('work/analysis/Rafael351_identity_note_alignment_v1_20261105/qualified_names_roles_andparticle_findings.json')
MACROS=Path('work/analysis/Rafael261_names_terms_20261105/names_macros_andconsumer_dependency_qualification_v1.json')
PLAN=Path('work/analysis/Rafael351_automatic_plans_v6_20261105/automatic_plans.json')
NATIVE=Path('work/analysis/Rafael351_native_final_v3_20261105/compiled_native_pages.json')
STYLE=Path('work/analysis/Rafael351_style_objects_v1_20261105/compiled_style_objects.json')
ROOT=Path('work/analysis/Rafael351_consumer_inputs_v1_20261105')
OUT=Path('translations/rafael_B121_B140_consumer_manuscript_v5.json')

if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    old,objects,identity,macros,plan,native,styles=map(load,[DOC,OBJECTS,IDENTITY,MACROS,PLAN,NATIVE,STYLE])
    assert objects['runtime']==identity['runtime']==native['runtime']==styles['runtime']
    assert native['manuscript_sha256']==styles['manuscript_sha256']==plan['manuscript_sha256']==sha(DOC.read_bytes())
    doc=deepcopy(old);captions={r['id']:r for r in objects['choice_records']};changed=[]
    for a,b in zip(old['records'],doc['records'],strict=True):
        if b['kind']=='typed-choice-label':
            actual=captions[b['id']]
            assert all(b[k]==actual[k] for k in ['source_reference','current_reference','source_hex','current_hex','source_choice_object_hex'])
            assert 'current_choice_object_hex' not in b
            b['current_choice_object_hex']=actual['current_choice_object_hex'];changed.append(b['id'])
        else:assert a==b
    assert len(changed)==10
    doc.update(previous_consumer_input=str(DOC),previous_consumer_input_sha256=sha(DOC.read_bytes()),
        ten_exact_current_compound_caption_bindings_restored_no_prose_controls_decisions_or_gates_changed=True)
    ctx=RegisteredRuntime(identity['runtime']['release_proof'],identity['runtime']['startup_proof'],captain=0)
    previous=RegisteredRuntime(macros['runtime']['release_proof'],macros['runtime']['startup_proof'],captain=0)
    assert ctx.receipt()==identity['runtime'] and ctx.arm==previous.arm and ctx.common==previous.common
    assert ctx.actor_root==previous.actor_root and ctx.actor_bytes==previous.actor_bytes
    assert ctx.image.read_file('/GRP/KANJI.FNT')==previous.image.read_file('/GRP/KANJI.FNT')
    assert macros['complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified'] and macros['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10)
    default_path=Path(macros['same_Rafael_default_macro_proof']);default=load(default_path)
    assert sha(default_path.read_bytes())==macros['same_Rafael_default_macro_proof_sha256']
    assert all(c['output_hex']==b'Rafael Castor Castor Co.'.hex() for c in default['own_native_default_macro_cases']['cases'])
    ROOT.mkdir(parents=True);save(OUT,doc)
    qualified=deepcopy(identity);qualified.update(complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified=True,
        macro_ascii_lengths=macros['macro_ascii_lengths'],same_Rafael_default_macro_proof=str(default_path),
        same_Rafael_default_macro_proof_sha256=sha(default_path.read_bytes()),
        exact_current_code_COMMON_font_complete_actor_array_andmacro_data_reuse=True,
        no_new_name_getter_or_macro_permutation_execution=True)
    qualified['evidence'].update({str(p):sha(p.read_bytes()) for p in [IDENTITY,MACROS,default_path,Path(__file__)]})
    save(ROOT/'qualified_identity.json',qualified)
    for name,source,path in [('plans',plan,PLAN),('native',native,NATIVE),('styles',styles,STYLE)]:
        view=deepcopy(source);view.update(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),
            metadata_only_parent_proof=str(path),metadata_only_parent_proof_sha256=sha(path.read_bytes()),
            exact_body_records_words_andcompiled_bytes_orobjects_unchanged=True)
        if name=='plans':assert view['records']==source['records']
        elif name=='native':assert view['records']==source['records']
        else:assert view['objects']==source['objects']
        save(ROOT/(name+'.json'),view)
    save(ROOT/'input_qualification.json',dict(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),
        restored_caption_compound_metadata_IDs=changed,all341_body_records_exact=True,
        no_prose_review_controls_native_pages_orstyle_objects_changed=True,no_repeated_native_rendering=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,OBJECTS,IDENTITY,MACROS,PLAN,NATIVE,STYLE,OUT,Path(__file__)]}))
    print('Restored ten exact current compound-caption fields;341 bodies andall compiled pages/styles unchanged.Qualified compatible macro/name dependencies withoutrepeating getters/rendering.')
