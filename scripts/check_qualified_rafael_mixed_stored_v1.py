"""Keep Rafael parity/macro guards andadd the proven complete menu/style storage checks."""
import inspect
from scripts import check_qualified_rafael_stored_batch_v1 as ordinary
from scripts import check_editorial_stored_batch_v3 as mixed
from scripts.source_locked_derivation_v5118 import checked_text

check_FE_rows=ordinary.check_FE_rows
progressive_expand=ordinary.progressive_expand
FE_expand=ordinary.FE_expand
compound_source=checked_text(inspect.getsource(mixed.compound_storage),{
    'stored_hex=body.hex(),compiled_virtual_prefix_hex=value.hex(),':
        'stored_hex=body.hex(),expanded_hex=body.hex(),native_alignment=old[\'native_alignment\'],compiled_virtual_prefix_hex=value.hex(),',
    'exact_compiled_body_font_runtime_and64_slot_getter_proof_reuse=True':
        'exact_compiled_body_font_runtime_andall_slot_getter_proof_reuse=True',
})
compound_env={**mixed.compound_storage.__globals__}
exec(compile(compound_source,__file__+'::same-complete-compound-storage-andcorrect-explicit-slot-scope', 'exec'),compound_env)
compound_storage=compound_env['compound_storage']

source=checked_text(ordinary.source,{
    "    progressive_env=dict(progressive_expand.__globals__)":
        "    progressive_env={**progressive_expand.__globals__,'DYNAMIC_BINDINGS':native['dynamic_role_bindings']}",
    "exec(compile(macros['source_owned_progressive_adapter'],":
        "exec(compile(native['source_owned_progressive_macro_adapter'],",
    '    rows,relatives=[],[];fresh_pages=reused_pages=0':
        """    rows,relatives=[],[];fresh_pages=reused_pages=0;typed=[];style_records=[]
    menu_path=Path(rebuilt['menu']);assert sha(menu_path.read_bytes())==rebuilt['menu_sha256']
    menu=load(menu_path);assert menu['runtime']==runtime and menu['offline_visual_approved'] and not menu['direct_view_pending']
    assert menu['manuscript_sha256']==rebuilt['manuscript_sha256']
    styles_path=Path(rebuilt['styles']);assert sha(styles_path.read_bytes())==rebuilt['styles_sha256']
    styles=load(styles_path);assert styles['runtime']==runtime and styles['manuscript_sha256']==rebuilt['manuscript_sha256']""",
    "        for text in group['text_records']:":
        """        more_typed,more_styles,style_pages=compound_storage(group,block,menu,styles,compiled)
        typed.extend(more_typed);style_records.extend(more_styles);reused_pages+=style_pages
        for text in group['text_records']:""",
    "    assert len(relatives)==rebuilt['relative_sites']":
        """    assert len(relatives)==rebuilt['relative_sites']
    assert len(style_records)==rebuilt['style_physical_speech_count']==14
    assert len(rows)+len(style_records)==rebuilt['total_rendered_speech_count']==243
    assert sum(len(t['labels']) for t in typed)==rebuilt['typed_choice_count']==12""",
    '        records=rows,relative_cases=relatives,':
        "        records=rows,style_records=style_records,style_proof=rebuilt['styles'],style_proof_sha256=rebuilt['styles_sha256'],typed_objects=typed,typed_labels_checked=sum(len(t['labels']) for t in typed),relative_cases=relatives,",
})
exec(compile(source,__file__+'::same-complete-stored-parity-pages-macros-relatives-andnative-compounds-own-Rafael', 'exec'),globals())
