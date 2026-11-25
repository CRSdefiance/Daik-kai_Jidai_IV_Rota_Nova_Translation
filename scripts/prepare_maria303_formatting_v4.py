"""Project all four choice references to the native binder's complete typed-object schema."""
from scripts.prepare_maria303_formatting_v3 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "out=ROOT/'formatting_v1'":"out=ROOT/'formatting_v2'",
    '    rows=[];tokens=0':
    "    choice_objects=load(ROOT/'current_objects_v1/current_objects.json')\n    assert choice_objects['runtime']==runtime\n    choice_refs={r['id']:r['source_reference'] for r in choice_objects['choice_records']}\n    assert len(choice_refs)==4\n    rows=[];tokens=0;choice_projections=[]",
    "        row['editorial_logical_English']=row['english']":
    """        if row['kind']=='typed-choice-label':
            prior=row['source_reference'];complete=choice_refs[row['id']]
            assert all(complete[k]==v for k,v in prior.items())
            assert set(complete)-set(prior)=={'file_path','source_index'}
            assert complete['file_path']==row['file_path'] and complete['source_index']==row['source_index']
            choice_projections.append(dict(id=row['id'],original_reference=prior,complete_native_reference=complete))
            row['source_reference']=deepcopy(complete)
        row['editorial_logical_English']=row['english']""",
    "'macro_proof_sha256':digest(macro_path),'all_individual_four_prose_gates_pass':True":
    "'macro_proof_sha256':digest(macro_path),'choice_source_reference_schema_projections':choice_projections,'all_individual_four_prose_gates_pass':True",
})
if __name__=='__main__':exec(compile(source,__file__+'::complete-exact-typed-choice-source-references','exec'),globals())
