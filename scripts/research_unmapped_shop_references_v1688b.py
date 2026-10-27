"""Successor to the aborted V1688 scan: distinguish production and test headers."""
from pathlib import Path


if __name__ == '__main__':
    previous = Path('scripts/research_unmapped_shop_references_v1688.py')
    source = previous.read_text(encoding='utf-8')
    edits = [
        ("work/analysis/unmapped_shop_references_v1688'", "work/analysis/unmapped_shop_references_v1688b'"),
        ("length_field=at==4 and body[:4]==b'CS\\0\\1'", "length_field=at==4 and body[:4]==b'CS\\0\\1' and 8+struct.unpack_from('<H',body,4)[0]<=len(body) and not any(body[8+struct.unpack_from('<H',body,4)[0]:])"),
        ("'block_bytes':len(body)", "'block_bytes':len(body),'header_hex':body[:8].hex(),'unclassified_test_header_word_at4':path.startswith('/testdata/') and at==4 and body[:4]!=b'CS\\0\\1'"),
        ("assert all(hit['CS_header_length_field_not_dialogue_call'] for c in containers for hit in c['packed_halfword_matches'])", "assert all(hit['CS_header_length_field_not_dialogue_call'] for c in containers if c['path'].startswith('/data/SC') for hit in c['packed_halfword_matches'])"),
        ("'all_route_and_test_script_short_matches_are_CS_header_lengths':True", "'all_production_route_script_short_matches_are_validated_CS_body_lengths':True,'CS_body_length_contract_reference':'dk4tool/dialogue/relocation.py:CS v1 declared_size and logical_end validation','alternate_test_header_not_classified_as_message_or_length':True,'aborted_predecessor':'scripts/research_unmapped_shop_references_v1688.py'"),
        ("'The earlier natural English drafts remain context-unmapped", "'The alternate CS0101 testdata/SC3 block164 header word at4 remains explicitly unclassified;no production caller is established by it.',\n                       'The earlier natural English drafts remain context-unmapped"),
        ("750-752 wider reference inventory saved:route/test matches are CS lengths;overlay/main direct scans yield no bound caller.", "750-752 wider reference inventory saved:production route matches are validated CS lengths;alternate test header remains unclassified. Direct scans establish no bound caller."),
    ]
    for old, new in edits:
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    exec(compile(source, __file__, 'exec'), {'__file__': __file__, '__name__': '__main__'})
