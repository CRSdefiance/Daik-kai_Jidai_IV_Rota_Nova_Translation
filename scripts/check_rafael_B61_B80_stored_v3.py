"""Reuse identical tested stored records; refresh the revised page and all relocated branches."""
from pathlib import Path
from copy import deepcopy
from scripts import check_rafael_B61_B80_stored_v2 as base
from scripts.source_locked_derivation_v5118 import checked_text

check_FE_rows=base.check_FE_rows
progressive_expand=base.progressive_expand
FE_expand=base.FE_expand
FRESH=base.FRESH
OWN=base.OWN
QUAL=base.QUAL
PREVIOUS_PRODUCER=base.PREVIOUS_PRODUCER
PREV_NATIVE=Path('work/analysis/Rafael_B61_B80_formatting_20261104/combined_native_v10.json')
PREV_STORED=Path('work/analysis/Rafael_B61_B80_stored_native_v2_20261104/stored_native_verification.json')

source=checked_text(base.source,{
    "    assert sha(FRESH.read_bytes())==full_native['evidence'][str(FRESH)]\n    fresh=load(FRESH);assert fresh['runtime']==runtime\n    adapter=fresh['source_owned_target_page_adapter']":
        """    assert Path(native['previous_native']).resolve()==PREV_NATIVE.resolve()
    adapter=native['source_owned_target_page_adapter']""",
    "    compiled={r['id']:r for r in native['records']}":
        """    compiled={r['id']:r for r in native['records']}
    old_native,old_stored=map(load,[PREV_NATIVE,PREV_STORED])
    assert old_native['runtime']==old_stored['runtime']==runtime
    assert old_native['font_sha256']==native['font_sha256']
    assert old_stored['native_sha256']==sha(PREV_NATIVE.read_bytes())
    assert old_stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert old_stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    old_compiled={r['id']:r for r in old_native['records']}
    old_records={r['id']:r for r in old_stored['records']}
    reused_record_IDs=[]""",
    "            if text['parity_space_added']:":
        """            prior_record=old_records[text['id']]
            previous_compiled=old_compiled[text['id']]
            if prior_record['stored_hex']==text['stored_hex'] and previous_compiled==row:
                assert prior_record['expanded_hex']==expanded.hex()
                for page in old_pages:
                    assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
                rendered=deepcopy(prior_record['complete_stored_native_display'])
                alignment=deepcopy(prior_record['native_alignment'])
                reused_pages+=len(old_pages)
                reused_record_IDs.append(text['id'])
            elif text['parity_space_added']:""",
    "        actual_gameplay=False,actual_headers_transitions_loaders_andregistered_release_pending=True,":
        """        actual_gameplay=False,actual_headers_transitions_loaders_andregistered_release_pending=True,
        exact_previous_stored_records_reused=len(reused_record_IDs),reused_record_IDs=reused_record_IDs,
        previous_stored=str(PREV_STORED),previous_stored_sha256=sha(PREV_STORED.read_bytes()),""",
    '[args.reconstruction,args.native,FRESH,OWN,QUAL,macro_path,PREVIOUS_PRODUCER,Path(__file__)]':
        '[args.reconstruction,args.native,FRESH,OWN,QUAL,macro_path,PREV_NATIVE,PREV_STORED,PREVIOUS_PRODUCER,Path(__file__)]',
})
exec(compile(source,__file__+'::exact-record-scoped-storage-reuse-andfresh-reassurance-page','exec'),globals())
