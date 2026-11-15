"""Create a CPU-only post-expansion prototype;no production ARM9 is patched."""
from pathlib import Path


def main():
    target=Path('scripts/probe_duel_postmacro_v1115.py');assert not target.exists()
    body=Path('scripts/probe_duel_text_surface_v1113b.py').read_text(encoding='utf-8')
    body=body.replace('duel_text_surface_v1113b','duel_postmacro_v1115').replace(
        "from scripts.verify_village_wrap_v608 import read,save",
        "from scripts.verify_village_wrap_v608 import read,save\nfrom scripts.duel_postmacro_layout_v1114 import layout")
    before="        assert value==text\n        draw.update(context=context,string=pointer,expanded_hex=value.hex(),"
    assert body.count(before)==1
    body=body.replace(before,"""        assert value==text
        output,lines=layout(value)
        assert context-pointer==0x400 and len(output)<0x400
        # Controlled CPU prototype at the post-macro font boundary. Only the
        # callers own expanded-text buffer and its private Y cursor change.
        # This is NOT an assembled runtime fix or an emulator injection.
        u.mem_write(pointer,output+b'\\0')
        u.mem_write(context+40,struct.pack('<i',12 if len(lines)==1 else 0))
        draw.update(context=context,string=pointer,expanded_hex=value.hex(),
            generated_postmacro_hex=output.hex(),generated_lines=lines,
""")
    body=body.replace("    assert draw['initial_x']==0 and draw['initial_y']==12",
        "    assert draw['initial_x']==0 and draw['initial_y']==(12 if len(draw['generated_lines'])==1 else 0)")
    lo=body.index("    assert bytes(e['code'] for e in events)==text+b' '*(len(text)&1)")
    hi=body.index('    source_ink=sum(native)',lo)
    body=body[:lo]+"""    expected=bytearray(208*36);full_ink=0;expected_letters=[]
    for row,line in enumerate(draw['generated_lines']):
        ybase=12 if len(draw['generated_lines'])==1 else row*12
        for i,ch in enumerate(line):
            if ch!=' ':expected_letters.append((ord(ch),i*6,ybase))
            glyph=font.decode(ch)
            for y in range(12):
                for x in range(6):
                    value=int(y<11 and bool(glyph.getpixel((x,y))))
                    full_ink+=value
                    expected[(ybase+y)*208+i*6+x]=value
    assert [(e['code'],e['x'],e['y']) for e in events if e['code']!=32]==expected_letters
    assert all(e['style']==15 and 0<=e['x'] and e['x']+6<=144 and 0<=e['y'] and e['y']+12<=36 for e in events)
    assert native==bytes(expected),'Complete native font plane differs from independently laid-out source words'
"""+body[hi:]
    body=body.replace("native[(12+y)*208+x]", "native[(draw['initial_y']+y)*208+x]")
    body=body.replace("'source_bitmap_exact_to_independent_font_replay_at_observed_native_positions':True,",
        "'whole_source_plane_exact_to_independently_laid_out_complete_words_and_font':True,")
    body=body.replace("'correct_visible_layout_approved':False", "'CPU_prototype_has_complete_correct_visible_layout':True")
    body=body.replace("'source_return_consumes_complete_string':draw['consumed_bytes']==len(text)",
        "'native_font_consumes_complete_generated_string':draw['consumed_bytes']==len(bytes.fromhex(draw['generated_postmacro_hex']))")
    body=body.replace("'translations/duel_editorial_manuscript_v2.json'", "'translations/duel_editorial_manuscript_v3.json'")
    before="    for r in doc['records']:\n        if r['message_id'] in (1931,1932,1939,1949):texts.append((f'draft{r[\"message_id\"]}',r['english'].encode('ascii').replace(b'%s',name)))"
    assert body.count(before)==1
    body=body.replace(before,"""    for r in doc['records']:
        if r['message_id']<1951:
            for label,argument in (('native',name),('max16',b'Abcdefghijklmnop')):
                texts.append((f'draft{r["message_id"]}_{label}',r['english'].encode('ascii').replace(b'%s',argument)))""")
    body=body.replace("    assert any(r['glyph_ink_absent_from_final_crop']>0 for r in results[1:])",
        "    assert len(results)==41 and all(r['glyph_ink_absent_from_final_crop']==0 and not r['first_glyph_damaged_by_later_stride_spill'] and not r['glyphs_crossing_source_rows'] and not r['glyphs_outside_final_visible_crop'] and r['native_font_consumes_complete_generated_string'] for r in results)")
    body=body.replace("ROOT/'native_duel_surface_proof.json'", "ROOT/'native_postmacro_layout_prototype.json'")
    body=body.replace("'current_default_renderer_advances_after_an_already_out_of_row_glyph':True,",
        "'original_default_renderer_can_advance_after_out_of_row_glyph_as_prior_diagnostic_proves':True,\n        'CPU_only_postmacro_boundary_transformation_not_assembled_runtime_or_actual_gameplay':True,\n        'all20_duel_paragraphs_normal_and_legal16_character_ASCII_name_cases_pass':True,\n        'all208_source_opponent_names_CP932_and_runtime_scope_ABI_and_footprint_pending':True,")
    body=body.replace("'source_stride_spill_can_corrupt_first_glyph_even_when_input_is_fully_consumed':True,",
        "'all41_prototype_cases_have_no_row_stride_spill_and_complete_first_and_final_letters':True,")
    body=body.replace("'current_single_line_y12_centering_would_hide_wrapped_third_row_without_correct_postexpansion_measurement':True,",
        "'native_single_line_y12_centering_preserved_multiline_source_rows_begin_y0':True,")
    body=body.replace("native_surface_proof=str(ROOT/'native_duel_surface_proof.json')", "native_postmacro_prototype=str(ROOT/'native_postmacro_layout_prototype.json')")
    body=body.replace("original_automatic_glyph_wrap_can_spill_into_next_pixel_row_and_corrupt_initial_letter=True,",
        "postmacro_CPU_prototype41_ASCII_cases_without_any_row_spill_or_lost_letters=True,")
    body=body.replace("formatting_status='original backing208x36 is finally cropped to144x36;postexpansion24x3 layout and measured centering required;not approved'",
        "formatting_status='41-ASCII-case-postmacro24x3-CPU-prototype-pass;all-real-CP932-names-assembled-runtime-footprint-and-actual-still-pending'")
    body=body.replace("Original duel constructor/measurement/glyphs mapped:208x36 backing,144px/24-cell final crops,3 rows. Unwrapped drafts lose visible ink despite full byte consumption;no formatting approval.",
        "41 post-macro CPU prototype cases pass:all20 duel paragraphs with normal/max16 ASCII names;complete independent font masks,24x3 final crops,uniform margins,no source spill or lost letters. Runtime/CP932/actual gates remain open.")
    target.write_text(body,encoding='utf-8')
    print('Created explicit CPU-only postmacro layout prototype;no ROM code or formatting gate changed.')


if __name__=='__main__':main()
