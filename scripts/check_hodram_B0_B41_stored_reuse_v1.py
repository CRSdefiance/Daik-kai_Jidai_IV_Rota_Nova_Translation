"""Reuse exact stored-body proofs; freshly check changed parity and all relocated branches."""
from scripts import check_hodram_B0_B41_stored_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

compound_storage=previous.compound_storage
check_FE_rows=previous.check_FE_rows
ROOT=previous.ROOT
digest=previous.digest
source=checked_text(previous.source,{
    "    args=parser.parse_args();assert not args.out.exists()":
        "    parser.add_argument('--previous',type=Path,required=True)\n    args=parser.parse_args();assert not args.out.exists()",
    '    rows,relatives=[],[];fresh_pages=reused_pages=0;typed=[];style_records=[]':
        """    stored_previous=load(args.previous)
    assert stored_previous['runtime']==runtime
    assert stored_previous['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored_previous['all_stored_planes_equal_directly_viewed_compiled_planes']
    old_native=load(stored_previous['native'])
    assert sha(Path(stored_previous['native']).read_bytes())==stored_previous['native_sha256']
    assert old_native['font_sha256']==native['font_sha256'] and old_native['runtime']==runtime
    prior_rows={r['id']:r for r in stored_previous['records']}
    assert len(prior_rows)==rebuilt['speech_count']
    rows,relatives=[],[];fresh_pages=reused_pages=0;typed=[];style_records=[];cached_records=[]""",
    "            if text['parity_space_added']:":
        """            prior=prior_rows[text['id']]
            current_planes=[dict(path=p['native_plane'],sha256=p['native_plane_sha256']) for p in old_pages]
            exact=(prior['stored_hex']==raw.hex() and prior['expanded_hex']==expanded.hex()
                and prior['new_offset']==at and prior['new_record_index']==text['new_record_index']
                and prior['parity_space_added']==text['parity_space_added'] and prior['directly_viewed_planes']==current_planes)
            if exact:
                assert prior['all_stored_planes_equal_directly_viewed_compiled_planes']
                for p in current_planes:assert sha(Path(p['path']).read_bytes())==p['sha256']
                rendered=dict(exact_stored_bytes_position_prefix_parity_runtime_font_andall_planes_reused=True,
                    previous_stored_proof=str(args.previous),previous_stored_proof_sha256=sha(args.previous.read_bytes()),id=text['id'])
                reused_pages+=len(old_pages);cached_records.append(text['id'])
            elif text['parity_space_added']:""",
    'fresh_parity_dependent_pages=fresh_pages,exact_compiled_pages_reused=reused_pages,':
        "fresh_parity_dependent_pages=fresh_pages,exact_compiled_pages_reused=reused_pages, exact_stored_speech_records_reused=cached_records, previous_stored_proof=str(args.previous),previous_stored_proof_sha256=sha(args.previous.read_bytes()),",
})
exec(compile(source,__file__+'::same-stored-guards-qualified-exact-record-cache','exec'),globals())
