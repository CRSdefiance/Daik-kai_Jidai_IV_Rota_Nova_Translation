"""Prepare progressive-only complete glyph validation,no unrelated FE calibration."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    s=Path('scripts/prove_Rafael_B47_pages_v7985.py').read_text(encoding='utf8')
    a=s.index('    assert warnings==[');b=s.index("    assert not any(i['severity']=='error'",a)
    c=s.index("    r53=next(");d=s.index('    sheets=[]',c)
    print(derive('scripts/prove_Rafael_B47_pages_v7985.py','scripts/prove_Rafael_B49_pages_v8091.py',{
        s[a:b]:'    assert not warnings\n',s[c:d]:'',
        'B47':'B49','Rafael_B47_pages_v7985':'Rafael_B49_pages_v8091',
        'Rafael_B47_layout_v7984e/15_automatic_plans_full_native_width_zero_preamble_separate_body.json':'Rafael_B49_layout_v8090/61_automatic_plans_full_native_width_exact_source00_02_09_no_FE.json',
        'Rafael_B47_logical_v7983/15_logical_paragraphs60_original_native_progressive_alignments.json':'Rafael_B49_logical_v8089/61_logical_paragraphs244_original_native_alignments_no_FE.json',
        'Rafael_B47_names_v7976/four_static_speakers_eight_getters_clean_fields16_synthetic_macro_alignments.json':'Rafael_B49_names_v8078/seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json',
        '[0,4,5,6]':'[0,2,4,5,6,8,9]',
        "assert len(result['cases'])==4 and all(c['output_hex']==body.hex() for c in result['cases'])":"expected=body.replace(b'FI',b'Rafael').replace(b'FA',b'Castor').replace(b'FO',b'Castor Co.')\n        assert len(result['cases'])==4 and all(c['output_hex']==expected.hex() for c in result['cases'])",
        "assert ' '.join(body.decode('ascii').split())==row['english'] and all(t not in body for t in [b'FI',b'FA',b'FO'])":"assert ' '.join(expected.decode('ascii').split())==row['english'].replace('{MACRO:FI}','Rafael')\n        assert all(t not in body for t in [b'FA',b'FO']) and body.count(b'FI')==int(row['source_record_index'] in [311,388])",
        "pe['pages'](arm,font,body)":"pe['pages'](arm,font,expected)",
        "rendered['complete_consumed_bytes']==len(body)":"rendered['complete_consumed_bytes']==len(expected)",
        "p['expected_native_pages']==(2 if row['source_record_index']==53 else 1)":"p['expected_native_pages']==1",
        "segment=body[page['start']:page['end']]":"segment=expected[page['start']:page['end']]",
        'block=47':'block=49','expanded_native_hex=body.hex()':'expanded_native_hex=expected.hex()',
        "len(rows)==15 and not ctx.machines and sum(len(r['pages']) for r in rows)==16":"len(rows)==61 and not ctx.machines and sum(len(r['pages']) for r in rows)==61",
        '15_complete_native_paragraphs16_pages60_compiled_alignments':'61_complete_native_paragraphs61_pages244_compiled_alignments',
        'fresh_compiled_alignment_cases=60,progressive_alignment_cases=60':'fresh_compiled_alignment_cases=244,progressive_alignment_cases=244',
        'complete_progressive_paragraphs=15,complete_progressive_pages=16':'complete_progressive_paragraphs=61,complete_progressive_pages=61',
        'R53_two_original_four_row_pages_sentence_boundary_then_complete_conditional_clause':'all61_single_original_four_row_pages_complete',
        'all_words_punctuation_andzero_macros':'all_words_punctuation_andtwo_source_FI_macros',
        'all15_formatting_gates_false':'all61_formatting_gates_false',
        'warning_waivers_not_yet_authored_orapproved':'no_warnings_andno_warning_waivers_needed',
        '15 complete native paragraphs/16 pages/60 alignments;allglyphs/bounds pass.Two exact warnings retained forindividual review;actual R53 page-turn pending.':'61complete native paragraphs/61pages/244alignments;allglyphs/bounds pass.Zero warnings;eleven sheets need direct viewing,actual/stored/release pending.',
    }))
