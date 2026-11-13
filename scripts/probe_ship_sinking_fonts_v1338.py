"""All eighteen ASCII byte lengths,macro-like names,spaces and full-width input.

All416 cases compare the entire native glyph plane independently. Eight name
variants have PNGs/sheets for visual review;other planes retain exact hashes.
"""
import inspect
from pathlib import Path
from scripts import probe_ship_sinking_fonts_v1331 as previous

if __name__=='__main__':
    source = inspect.getsource(previous.main)
    old = """    for text in ['F','ABCDEFGHIJKLMNOPQRSTUVW','ABCDEFGHIJKLMNOPQRSTUVWXYZ12345','Santa Maria','長崎丸']:
        names.append({'kind':'synthetic-font-stress-not-proven-name-editor-limit','name':text,'hex':text.encode('cp932').hex()})
    assert len(names)==6"""
    new = """    bound_path = Path('work/analysis/ship_name_bound_v1335b/original_ship_rename_capacity.json')
    assert read(bound_path)['max_name_bytes_excluding_NUL']==18
    for text in ['F'+'A'*(n-1) for n in range(1,19)]+['FALCON','ICARUS','FIFOFOFU','Santa Maria',\"F's Hope\",'長崎丸長崎丸長崎丸','ＦＡＬＣＯＮ']:
        assert 0<len(text.encode('cp932'))<=18
        names.append({'kind':'CPU-input-within-captured-ship-editor-byte-cap-not-reachable-name-claim','name':text,'hex':text.encode('cp932').hex()})
    assert len(names)==26
    visual_variants = [0,1,18,19,20,22,24,25]"""
    assert source.count(old)==1
    source = source.replace(old,new)
    changes = [
        ("Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(path)",
         "if variant in visual_variants:\n                Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(path)\n            else:\n                path = None"),
        ("'preview':str(path),'preview_sha256':sha(path.read_bytes())", "'preview':str(path) if path else None,'preview_sha256':sha(path.read_bytes()) if path else None,'whole_native_font_plane_sha256':sha(bytes(pixels))"),
        ("six original substitution/macro/wrap/full-font cases pass.","26 original substitution/macro/wrap/full-font cases pass."),
        ("len(cases)==96", "len(cases)==416"),
        ("for variant in [0,1,2,3,4,5]:", "for variant in visual_variants:"),
        ("all96_complete_native_substitution_macro_wrap_and_font_planes_equal", "all416_complete_native_substitution_macro_wrap_and_font_planes_equal"),
        ("'visual_review_and_name_editor_supported_limit_pending':True", "'visual_review_pending':True,'captured_editor18_byte_bound_proof':str(bound_path),'captured_editor18_byte_bound_proof_sha256':sha(bound_path.read_bytes()),'all_ASCII_byte_lengths1_to18_and_macro_like_spaced_and_full_width_names_checked':True,'byte_capacity_does_not_prove_every_keyboard_page_or_legacy_saved_name':True"),
        ("96 complete native font cases pass;", "416 complete native font cases pass;")]
    for old,new in changes:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,
        'ROOT':Path('work/analysis/ship_sinking_fonts_v1338'),
        'PLAN':Path('work/analysis/ship_sinking_payload_v1337/native_payload_plan.json'),
        'MANUSCRIPT':Path('translations/ship_sinking_editorial_manuscript_v3.json')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
