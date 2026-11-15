"""Stored speech checks plus exact separately proven native-menu object reuse."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/check_editorial_stored_batch.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    "    full_native=load(native['previous_native']) if 'previous_native' in native else native":
    """    full_native=native;seen=set()
    while 'source_owned_target_page_adapter' not in full_native:
        prior=Path(full_native['previous_native']);assert str(prior) not in seen;seen.add(str(prior))
        assert sha(prior.read_bytes())==full_native['previous_native_sha256']
        full_native=load(prior)
        assert full_native['runtime']==native['runtime'] and full_native['font_sha256']==native['font_sha256']""",
    "    rows,relatives=[],[];fresh_pages=reused_pages=0":
    """    rows,relatives=[],[];fresh_pages=reused_pages=0;typed=[]
    if rebuilt.get('typed_choice_count'):
        menu_path=Path(rebuilt['menu']);assert sha(menu_path.read_bytes())==rebuilt['menu_sha256']
        menu=load(menu_path)
        assert menu['runtime']==runtime and menu['offline_visual_approved'] and not menu['direct_view_pending']
        assert menu['manuscript_sha256']==rebuilt['manuscript_sha256']""",
    "        for text in group['text_records']:":
    """        for choice in group.get('typed_objects',[]):
            raw=bytes.fromhex(choice['compiled_hex']);at=choice['new_offset']
            assert block[at:at+len(raw)]==raw and raw.hex()==menu['native_choice_object_hex']
            command=next(c for c in group['all_target_commands'] if c['offset']==at)
            assert command['word']==0x2100 and command['native_extent']==len(raw)
            assert choice['source_index_order']==[0,1] and choice['count']==2
            typed.append(dict(block=group['block'],offset=at,object_hex=raw.hex(),
                source_index_order=[0,1],labels=[r['english'] for r in choice['records']],
                exact_native_provider_andcomplete_planes_reused_from=rebuilt['menu'],
                no_new_native_provider_run_for_identical_stored_object=True))
        for text in group['text_records']:""",
    "        records=rows,relative_cases=relatives,complete_stored_pages=fresh_pages+reused_pages,":
        "        records=rows,typed_objects=typed,typed_labels_checked=sum(len(t['labels']) for t in typed),relative_cases=relatives,complete_stored_pages=fresh_pages+reused_pages,",
})
exec(compile(source,__file__+'::stored-speech-and-menu','exec'),globals())
