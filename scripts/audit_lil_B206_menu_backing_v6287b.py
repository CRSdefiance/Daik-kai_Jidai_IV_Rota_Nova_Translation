"""Own only the two actual caption views;unused physical backing contains unrelated old pixels."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=Path('scripts/audit_lil_B206_menu_backing_v6287.py')
if __name__=='__main__':
    text=checked_text(source.read_text('utf-8'),{
      "ROOT=Path('work/analysis/lil_B206_menu_actual_v6287')":"ROOT=Path('work/analysis/lil_B206_menu_actual_v6287b')",
      "    assert pixels==bytes(expected),'Actual complete physical backing differs from independent glyph plane'":"    owned=[yy*256+xx for yy in range(24) for xx in range(114)]\n    actual_owned=bytes(pixels[i] for i in owned);expected_owned=bytes(expected[i] for i in owned)\n    assert actual_owned==expected_owned,'Actual complete caption views differ from independent glyphs'\n    unowned_differences=sum(pixels[i]!=expected[i] for i in range(len(pixels)) if i%256>=114 or i//256>=24)\n    assert unowned_differences>0",
      'actual_full114px_two_labels256x36_backing_equals_independent_native_font':'actual_two_complete114x12_views_inside_observed256x36_backing',
      'complete_actual_backing_plane_sha256=sha(pixels),complete_independent_plane_sha256=sha(bytes(expected)),all4608_actual_packed_backing_bytes_and9216_pixels_equal=True':'actual_full_physical_capture_sha256=sha(pixels),independent_label_model_sha256=sha(bytes(expected)),actual_owned_view_sha256=sha(actual_owned),independent_owned_view_sha256=sha(expected_owned),all2736_owned_caption_pixels_equal=True,unowned_physical_pixels_with_unrelated_data=unowned_differences,no_blank_or_equal_unowned_backing_claim=True',
      'Actual whole256x36 caption backing equals independent font pixels:':'Both actual complete114x12 caption views equal independent font pixels:',
    })
    exec(compile(text,str(source)+'::exact-owned-views','exec'),dict(__name__='__main__',__file__=__file__))
