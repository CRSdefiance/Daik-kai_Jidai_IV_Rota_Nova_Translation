"""Recheck only changed stored body bytes and relocated branch behavior; reuse exact proofs."""
from scripts import check_qualified_rafael_stored_with_fu_v1 as previous
from scripts.check_editorial_stored_batch_v3 import compound_storage
from scripts.source_locked_derivation_v5118 import checked_text

check_FE_rows=previous.check_FE_rows
progressive_expand=previous.progressive_expand
FE_expand=previous.FE_expand
CHANGED={'DK4_MES_B154_R0084','DK4_MES_B154_R0114'}

source=checked_text(previous.source,{
    "for arg in ('reconstruction','native','identity','out'):":"for arg in ('reconstruction','native','identity','previous-stored','out'):",
    '    args.out.mkdir(parents=True)\n    rows,relatives=[],[];fresh_pages=reused_pages=0':"""    old=load(args.previous_stored);old_rebuild_path=Path(old['reconstruction']);old_rebuilt=load(old_rebuild_path)
    assert old['reconstruction_sha256']==sha(old_rebuild_path.read_bytes()) and old['runtime']==runtime
    old_native_path=Path(old['native']);assert old['native_sha256']==sha(old_native_path.read_bytes())
    old_native={r['id']:r for r in load(old_native_path)['records']}
    assert old['all_stored_planes_equal_directly_viewed_compiled_planes'] and old['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert {k for k,v in compiled.items() if v!=old_native[k]}==CHANGED and set(compiled)==set(old_native)
    old_rows={r['id']:r for r in old['records']};old_groups={g['block']:g for g in old_rebuilt['groups']}
    assert {g['block'] for g in rebuilt['groups'] if g['target_sha256']!=old_groups[g['block']]['target_sha256']}=={154}
    assert {r['id'] for g in rebuilt['groups'] for r in g['text_records'] if r['stored_hex']!=old_rows[r['id']]['stored_hex']}==CHANGED
    menu_path,styles_path=Path(rebuilt['menu']),Path(rebuilt['styles']);menu,styles=map(load,[menu_path,styles_path])
    assert sha(menu_path.read_bytes())==rebuilt['menu_sha256'] and sha(styles_path.read_bytes())==rebuilt['styles_sha256']
    assert menu['runtime']==styles['runtime']==runtime and menu['manuscript_sha256']==styles['manuscript_sha256']==rebuilt['manuscript_sha256']
    assert menu['offline_visual_approved'] and not menu['direct_view_pending'] and not styles['objects']
    args.out.mkdir(parents=True)
    rows,relatives,typed=[],[],[];fresh_pages=reused_pages=reused_stored_pages=0""",
    "        for text in group['text_records']:":"""        choices,style_rows,style_pages=compound_storage(group,block,menu,styles,compiled)
        assert not style_rows and style_pages==0;typed.extend(choices)
        for text in group['text_records']:""",
    "            if text['parity_space_added']:":"""            if text['id'] not in CHANGED:
                previous_row=old_rows[text['id']]
                assert previous_row['stored_hex']==raw.hex() and previous_row['expanded_hex']==expanded.hex()
                assert previous_row['parity_space_added']==text['parity_space_added']
                assert previous_row['all_stored_planes_equal_directly_viewed_compiled_planes'] and len(old_pages)==expected_pages
                for page in old_pages:assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
                alignment=previous_row['native_alignment'];rendered=previous_row['complete_stored_native_display']
                reused_stored_pages+=len(old_pages)
            elif text['parity_space_added']:""",
    "        for fix in group['relative_fixups']:":"""        if group['block']!=154:
            old_group=old_groups[group['block']]
            for key in ['target_sha256','all_target_commands','relative_fixups','text_records']:
                assert group[key]==old_group[key]
            prior=[r for r in old['relative_cases'] if r['block']==group['block']]
            assert len(prior)==len(group['relative_fixups'])
            relatives.extend({**r,'exact_previous_native_branch_proof':True} for r in prior)
        for fix in group['relative_fixups'] if group['block']==154 else []:""",
    "    assert len(rows)==rebuilt['speech_count'] and fresh_pages+reused_pages==native['pages']":
        "    assert len(rows)==rebuilt['speech_count'] and fresh_pages+reused_pages+reused_stored_pages==native['pages']\n    assert len(typed)==4 and sum(len(t['labels']) for t in typed)==rebuilt['typed_choice_count']==8",
    'records=rows,relative_cases=relatives,complete_stored_pages=fresh_pages+reused_pages,':
        'records=rows,relative_cases=relatives,typed_objects=typed,typed_labels_checked=8,style_records=[],complete_stored_pages=fresh_pages+reused_pages+reused_stored_pages,',
    "        fresh_relocated_native_relative_cases=sum(len(r['cases']) for r in relatives),":
        "        exact_previous_stored_pages_reused=reused_stored_pages,\n        fresh_relocated_native_relative_cases=sum(len(r['cases']) for r in relatives if not r.get('exact_previous_native_branch_proof')),\n        total_relocated_native_relative_cases=sum(len(r['cases']) for r in relatives),",
    '[args.reconstruction,args.native,args.identity,macro_path,ownpath,Path(__file__)]':
        '[args.reconstruction,args.native,args.identity,args.previous_stored,old_rebuild_path,old_native_path,menu_path,styles_path,macro_path,ownpath,Path(__file__)]',
    'pages=fresh_pages+reused_pages,fresh_parity_pages=fresh_pages,':
        'pages=fresh_pages+reused_pages+reused_stored_pages,fresh_parity_pages=fresh_pages,exact_previous_stored_pages=reused_stored_pages,',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-storage-checks-exact-record-andblock-reuse','exec'),globals())
