"""Verify stored speech, parity-dependent pages, mixed menu indices and relocated branches."""
from scripts import check_rafael_B166_B167_stored_v1 as prior
from scripts.check_editorial_stored_batch_v3 import compound_storage
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(prior.source, {
    "    rows,relatives=[],[];fresh_pages=reused_pages=0":
        """    rows,relatives=[],[];fresh_pages=reused_pages=0;typed=[]
    menu_path=Path(rebuilt['menu']);styles_path=Path(rebuilt['styles'])
    assert sha(menu_path.read_bytes())==rebuilt['menu_sha256'] and sha(styles_path.read_bytes())==rebuilt['styles_sha256']
    menu,styles=map(load,(menu_path,styles_path))
    assert menu['runtime']==styles['runtime']==runtime and not styles['objects']
    assert menu['offline_visual_approved'] and not menu['direct_view_pending']""",
    "        for text in group['text_records']:":
        """        choices,style_records,style_pages=compound_storage(group,block,menu,styles,compiled)
        assert not style_records and style_pages==0
        typed.extend(choices)
        for text in group['text_records']:""",
    "    assert len(relatives)==rebuilt['relative_sites']":
        """    assert len(relatives)==rebuilt['relative_sites']==104
    assert len(typed)==rebuilt['compound_objects']==10
    assert sum(len(m['labels']) for m in typed)==rebuilt['typed_choice_count']==21
    assert [m['word'] for m in typed].count(0x2200)==1
    assert len(rows)==382 and fresh_pages+reused_pages==383""",
    "records=rows,relative_cases=relatives,":
        "records=rows,typed_objects=typed,typed_labels_checked=21,relative_cases=relatives,",
    "args.native,args.identity,macro_path,ownpath,MACROS,PREVIOUS_NAMES[0],Path(__file__)":
        "args.native,args.identity,macro_path,ownpath,MACROS,PREVIOUS_NAMES[0],menu_path,styles_path,Path(__file__)",
})

if __name__=='__main__':
    env={**prior.env,'compound_storage':compound_storage,'__file__':__file__,'__name__':'stored_B201_B220'}
    exec(compile(source,__file__+'::same-stored-guards-with-source-qualified-mixed-menus','exec'),env)
    env['main']()
