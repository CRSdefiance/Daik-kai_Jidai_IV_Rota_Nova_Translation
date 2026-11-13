"""Use mapped 4100 headers for virtual prefixes; retain ordinary full preamble checks."""
from scripts import check_editorial_compiled_pages_v3 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "            assert row['source_reference']==bound['source_reference'] and row['source_complete_preamble_hex']==bound['source_complete_preamble_hex']":
    """            assert row['source_reference']==bound['source_reference']
            if row.get('native_object_kind')=='4100-style-alternative':
                assert bound['kind']=='4100-style-alternative' and bound['virtual_prefix_not_in_stored_body']
                assert row['source_header_hex']==bound['source_header_hex'] and row['source_style_indices']==bound['source_style_indices']
                assert row['virtual_formatter_prefix_is_not_part_of_stored_alternative_text']
            else:
                assert row['source_complete_preamble_hex']==bound['source_complete_preamble_hex']""",
})
exec(compile(source,__file__+'::source-bound-style-header-not-fictional-speech-preamble','exec'),globals())
