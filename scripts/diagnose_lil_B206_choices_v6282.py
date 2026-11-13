"""Preserve the failed second-menu model and record its actual complete native plane."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=Path('scripts/prove_lil_B206_choices_v6281.py')
if __name__=='__main__':
    extra="""    diagnostic='''    if pixels != bytes(expected):
        from PIL import Image
        from scripts.verify_village_wrap_v608 import save
        root=Path(DIAG_ROOT);root.mkdir(parents=True,exist_ok=True)
        tag='label_'+sha(text)[:12]+'_width'+str(width)+'_style'+str(style)
        def bounds(v):
            pts=[(i%stride,i//stride) for i,b in enumerate(v) if b]
            return [min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts),max(y for x,y in pts)]
        save(root/(tag+'.json'),dict(text=text.decode(),style=style,width=width,stride=stride,expected_origin=[x,y],native_ink_bounds=bounds(pixels),expected_ink_bounds=bounds(expected),mismatched_pixels=sum(a!=b for a,b in zip(pixels,expected)),actual_plane_sha256=sha(pixels),expected_plane_sha256=sha(bytes(expected))))
        (root/(tag+'_actual.bin')).write_bytes(pixels);(root/(tag+'_expected.bin')).write_bytes(bytes(expected))
        im=Image.new('RGB',(stride,height));im.putdata([(0,0,0) if b else (240,228,200) for b in pixels]);im.resize((stride*4,height*4),Image.Resampling.NEAREST).save(root/(tag+'.png'))
    assert pixels == bytes(expected)'''
    assert painter.count('    assert pixels == bytes(expected)')==1
    painter=painter.replace('    assert pixels == bytes(expected)',diagnostic)
"""
    text=checked_text(source.read_text('utf-8'),{
      "MAINROOT = Path('work/analysis/lil_B206_choices_v6281')":"MAINROOT = Path('work/analysis/lil_B206_choices_diagnostic_v6282')",
      "    cases,pictures = [],[]":extra+"    cases,pictures = [],[]",
      "'CURRENT_ARM9':CURRENT_ARM9}":"'CURRENT_ARM9':CURRENT_ARM9,'DIAG_ROOT':str(MAINROOT/'failed_native_model_diagnostic')}",
    })
    exec(compile(text,str(source)+'::complete-native-plane-diagnostic','exec'),dict(__name__='__main__',__file__=__file__))
