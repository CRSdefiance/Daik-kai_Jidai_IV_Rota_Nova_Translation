"""Preserve the rejected total-byte parity prototype;track native ASCII runs."""
from pathlib import Path


def main():
    old = Path('scripts/duel_postmacro_layout_v1114.py')
    new = Path('scripts/duel_postmacro_layout_v1119.py')
    assert not new.exists()
    source = old.read_text(encoding='utf-8')
    before = "        if i<len(lines)-1 and len(value)&1:value+=b' '"
    assert source.count(before) == 1
    source = source.replace(before, "        if i<len(lines)-1 and trailing_ascii_phase(line):value+=b' '")
    source += '''

def trailing_ascii_phase(text):
    """A native double-byte glyph ends the preceding ASCII draw batch."""
    phase=0
    for character in text:
        encoded=character.encode('cp932')
        if len(encoded)==2:phase=0
        else:
            if len(encoded)!=1 or encoded[0]>=128:
                raise ValueError('Unmapped one-byte non-ASCII glyph in duel prototype')
            phase^=1
    return phase
'''
    new.write_text(source, encoding='utf-8')
    old_probe = Path('scripts/probe_duel_full_name_fonts_v1118.py')
    new_probe = Path('scripts/probe_duel_full_name_fonts_v1119.py')
    assert not new_probe.exists()
    probe = old_probe.read_text(encoding='utf-8')
    changes = {
        'from scripts.duel_postmacro_layout_v1114 import layout':
            'from scripts.duel_postmacro_layout_v1119 import layout,trailing_ascii_phase',
        "ROOT=Path('work/analysis/duel_full_name_fonts_v1118')":
            "ROOT=Path('work/analysis/duel_full_name_fonts_v1119')",
        "'odd_byte_native_batch_flush_is_one_invisible_space_not_authored_text':bool(len(text)&1)":
            "'odd_trailing_ASCII_run_flush_is_one_invisible_space_not_authored_text':bool(trailing_ascii_phase(draw['generated_lines'][-1]))",
        "    ROOT.mkdir(parents=True)\n    for index,":
            """    ROOT.mkdir(parents=True)
    corrected=[]
    for item in catalog['all4160_complete_word_layouts']:
        paragraph=bytes.fromhex(item['paragraph_hex'])
        output,lines=layout(paragraph)
        assert lines==item['lines']
        corrected.append({**item,'generated_hex':output.hex(),
            'trailing_ASCII_run_parity_after_last_double_byte_glyph':True})
    assert len(corrected)==4160
    save(ROOT/'all4160_source_name_layouts_corrected_phase.json',{
        'original_name_catalogue':str(names_path),'original_name_catalogue_sha256':sha(names_path.read_bytes()),
        'layouts':corrected,'prior_total_byte_parity_encoding_is_superseded_not_a_font_pass':True,
        'complete_words_and_all_name_bytes_preserved':True})
    for index,""",
        "'not_assembled_runtime_or_actual_gameplay':True,'all33_formatting_gates_still_pending':True,":
            "'not_assembled_runtime_or_actual_gameplay':True,'all33_formatting_gates_still_pending':True,\n"
            "        'mixed_phase_counterexample_retained':'work/analysis/duel_full_name_failure_v1118/first_CP932_request_failure.json',\n"
            "        'phase_uses_trailing_ASCII_run_after_last_double_byte_glyph_not_whole_row_byte_count':True,\n"
            "        'layout_module_sha256':sha(Path('scripts/duel_postmacro_layout_v1119.py').read_bytes()),",
        "native_all_source_name_fonts=str(proof),":
            "native_all_source_name_fonts=str(proof),\n"
            "        corrected_all4160_source_name_phase_catalogue=str(ROOT/'all4160_source_name_layouts_corrected_phase.json'),",
    }
    for before, after in changes.items():
        assert probe.count(before) == 1, before
        probe = probe.replace(before, after)
    new_probe.write_text(probe, encoding='utf-8')
    print('Created mixed-glyph phase successor;original failed prototype preserved.')


if __name__ == '__main__':
    main()
