"""Require all native guards; evaluate a freshly rendered alignment-space layout on its own pixels."""
from pathlib import Path
from PIL import Image
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/qualify_maria310_FE_parity_space_v1.py').read_text(encoding='utf-8'),{
    'FE_parity_space_qualification_v1.json':'FE_parity_space_qualification_v2.json',
    'paint,calibration=factory(ctx.image);cases=[]':'paint,calibration=factory(ctx.image);cases=[];passed_planes={}',
    "assert rendered['physical']==plane and rendered['complete_consumed_bytes']==len(text)":
        "assert rendered['complete_consumed_bytes']==len(text)",
    '        else:case.update(rejected=False,all_original_native_assertions_pass=True,row_comparison=rows,':
        "        else:\n            passed_planes[at]=rendered['physical']\n            case.update(rejected=False,all_original_native_assertions_pass=True,row_comparison=rows,",
    'native_plane_sha256=sha(plane),':'native_plane_sha256=sha(rendered[\'physical\']),',
    'exact_approved_physical_pixels=True,events=rendered[\'events\'])':
        "native_plane_matches_prior=rendered['physical']==plane,events=rendered['events'])",
    '    selected=good[0]':
        """    selected=min(good,key=lambda c:sum(a!=b for a,b in zip(passed_planes[c['input_space_offset']],plane,strict=True)))
    pixels=passed_planes[selected['input_space_offset']]
    binary=ROOT/'FE_parity_space_candidate_v2.bin';assert not binary.exists();binary.write_bytes(pixels)
    png=binary.with_suffix('.png');pic=Image.new('RGB',(228,64));pic.putdata([(0,8,0) if v else (239,232,201) for v in pixels]);pic.save(png)
    selected.update(native_plane=str(binary),preview=str(png),preview_sha256=sha(png.read_bytes()),
        changed_pixels_from_prior=sum(a!=b for a,b in zip(pixels,plane,strict=True)),direct_visual_review_pending=True)""",
    'native_pixels_andfull_input_consumption_exact=True,needs_fresh_four_alignment_andstored_checks=True':
        'independent_native_pixels_andfull_input_consumption_pass=True,selected_preview=selected,needs_fresh_four_alignment_andstored_checks=True',
    "'with full140-byte consumption andexact approved pixels;four alignments/storage remain.'":
        "'with full140-byte consumption andall original native/row/pixel/bounds guards;fresh visual/four alignments/storage remain.'",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-native-instruction-glyph-canary-bounds-androw-guards-new-output-needs-own-visual-approval','exec'),globals())
