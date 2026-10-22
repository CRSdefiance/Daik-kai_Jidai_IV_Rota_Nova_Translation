"""Account for the observed native invisible flush cell,not an extra text glyph."""
from pathlib import Path


def main():
    target=Path('scripts/probe_duel_text_surface_v1113b.py');assert not target.exists()
    body=Path('scripts/probe_duel_text_surface_v1113.py').read_text(encoding='utf-8')
    body=body.replace('duel_text_surface_v1113','duel_text_surface_v1113b')
    before="    assert bytes(e['code'] for e in events)==text\n";assert body.count(before)==1
    body=body.replace(before,"    assert bytes(e['code'] for e in events)==text+b' '*(len(text)&1)\n")
    body=body.replace("'observed_native_glyphs':events,", "'observed_native_glyphs':events,\n        'odd_byte_native_batch_flush_is_one_invisible_space_not_authored_text':bool(len(text)&1),")
    body=body.replace("'failed_reference_assumed_no_automatic_row_advance_and_was_rejected':True,",
        "'failed_reference_assumed_no_automatic_row_advance_and_was_rejected':True,\n        'strict_odd_length_stream_predecessor':'scripts/probe_duel_text_surface_v1113.py',\n        'native_appends_only_one_blank_cell_for_odd_final_ASCII_batch':True,")
    target.write_text(body,encoding='utf-8')
    print('Native final odd-byte blank cell explicitly accounted;source/input text remains unchanged and no glyph errors waived.')


if __name__=='__main__':main()
