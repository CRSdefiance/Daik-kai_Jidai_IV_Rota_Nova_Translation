"""Check all stored B221–B240 text, relative branches and mixed native commands."""
import inspect
from pathlib import Path

from scripts import check_rafael_B166_B167_stored_v1 as prior
from scripts.check_editorial_stored_batch_v3 import compound_storage
from scripts.source_locked_derivation_v5118 import checked_text

storage = checked_text(inspect.getsource(compound_storage), {
    'exact_compiled_body_font_runtime_and64_slot_getter_proof_reuse':
        'exact_compiled_body_font_runtime_and_source_slot_getter_proof_reuse',
})
source = checked_text(prior.source, {
    "    rows,relatives=[],[];fresh_pages=reused_pages=0":
        """    rows,relatives=[],[];fresh_pages=reused_pages=0;typed=[];style_records=[]
    menu_path=Path(rebuilt['menu']);styles_path=Path(rebuilt['styles'])
    assert sha(menu_path.read_bytes())==rebuilt['menu_sha256'] and sha(styles_path.read_bytes())==rebuilt['styles_sha256']
    menu,styles=map(load,(menu_path,styles_path))
    assert menu['runtime']==styles['runtime']==runtime
    assert menu['offline_visual_approved'] and not menu['direct_view_pending']
    assert styles['native_target_slot_cases']==32 and styles['source_alias_equivalence_exact']""",
    "        for text in group['text_records']:":
        """        choices,style_bodies,style_pages=compound_storage(group,block,menu,styles,compiled)
        typed.extend(choices);style_records.extend(style_bodies);reused_pages+=style_pages
        for text in group['text_records']:""",
    "    assert len(relatives)==rebuilt['relative_sites']":
        """    assert len(relatives)==rebuilt['relative_sites']==34
    assert len(rows)==234 and len(style_records)==rebuilt['style_physical_speech_count']==29
    assert len(rows)+len(style_records)==rebuilt['total_rendered_speech_count']==263
    assert len(typed)==3 and sum(len(item['labels']) for item in typed)==rebuilt['typed_choice_count']==7
    assert sorted(item['word'] for item in typed)==[0x2100,0x2100,0x2200]
    assert fresh_pages+reused_pages==279""",
    "records=rows,relative_cases=relatives,":
        "records=rows,style_records=style_records,style_proof=rebuilt['styles'],style_proof_sha256=rebuilt['styles_sha256'],"
        "typed_objects=typed,typed_labels_checked=7,relative_cases=relatives,",
    "args.native,args.identity,macro_path,ownpath,MACROS,PREVIOUS_NAMES[0],Path(__file__)":
        "args.native,args.identity,macro_path,ownpath,MACROS,PREVIOUS_NAMES[0],menu_path,styles_path,Path(__file__)",
})

if __name__ == '__main__':
    storage_env = dict(compound_storage.__globals__)
    exec(compile(storage, __file__+'::same-storage-helper-with-scope-neutral-field', 'exec'), storage_env)
    env = {**prior.env, 'compound_storage': storage_env['compound_storage'], '__file__': __file__,
           '__name__': 'stored_B221_B240'}
    exec(compile(source, __file__+'::same-native-guards-with-seven-mixed-commands', 'exec'), env)
    env['main']()

