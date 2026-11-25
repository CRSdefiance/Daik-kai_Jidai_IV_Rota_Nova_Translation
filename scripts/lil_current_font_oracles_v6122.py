"""Exact V5891 name-data-only successor font oracles; preserve the old typed FE geometry evidence.

The current ASCII painter shifts complete11-row glyph ink down one pixel.
Historical FE object/geometry proofs remain the descriptor source; they are
not represented as current-font gameplay. New B201 English FE observation remains separate;earlier source geometry is retained.
"""
from pathlib import Path
import inspect
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_name_catalog_glyphs_v278 import expected_pixels as old_expected
from scripts import lil_kuhn_china_FE_painter_v2909 as old_FE

CURRENT_ARM9='03a905a9e4a4df117b8a4b5280ec3c669a4db00547972397413bc8bebc4afbbd'

source=inspect.getsource(old_expected)
source=source.replace('(6, 11) if event["kind"] == "ascii"','(6, 12) if event["kind"] == "ascii"')
needle='ink = [(xx, yy) for yy in range(11) for xx in range(6) if bitmap.getpixel((xx, yy))]'
assert source.count(needle)==1
source=source.replace(needle,'ink = [(xx, yy + 1) for yy in range(11) for xx in range(6) if bitmap.getpixel((xx, yy))]')
namespace=dict(old_expected.__globals__);exec(compile(source,__file__+'::current-progressive-independent-pixels','exec'),namespace)
_expected=namespace['expected_pixels']
PROGRESSIVE_ORACLE_SOURCE=source


def expected_pixels(arm,font,events,**kwargs):
    assert sha(arm)==CURRENT_ARM9
    return _expected(arm,font,events,**kwargs)


def make_painter(image):
    assert sha(image.read_file('/__arm9__.bin'))==CURRENT_ARM9
    source=inspect.getsource(old_FE.make_painter)
    old="assert sha(arm)==proof['ARM9_sha256'] and proof['all22_complete_native_independent_planes_all_glyphs_and_canaries_equal']"
    new="assert sha(arm)==CURRENT_ARM9 and proof['ARM9_sha256']==sha(NdsImage.open('out/all_routes_combined_v4749_candidate.nds').read_file('/__arm9__.bin')) and proof['all22_complete_native_independent_planes_all_glyphs_and_canaries_equal']"
    assert source.count(old)==1;source=source.replace(old,new)
    old="expected[(e['y']+y)*288+e['x']+x]=e['style'];physical[(e['y']//12*16+y)*228+e['x']+x]=1"
    new="expected[(e['y']+y+1)*288+e['x']+x]=e['style'];physical[(e['y']//12*16+y+1)*228+e['x']+x]=1"
    assert source.count(old)==1;source=source.replace(old,new)
    start=source.index('    calibration=paint(')
    source=source[:start]+'''    calibration=paint(bytes.fromhex(captured['text_hex']))
    return paint,dict(source_proof=str(PROOF),source_proof_sha256=sha(PROOF.read_bytes()),
        historical_geometry_capture=prior['current_actual_checks'][0]['capture'],
        historical_geometry_and_rebound_descriptor_vtables_palette_clip_metrics_exact=True,
        current_font_native_logical_and_physical_planes_equal_independent_model=True,
        current_native_calibration_plane_sha256=sha(calibration['logical']),
        current_font_actual_FE_gameplay_calibration_not_claimed=True,
        complete_ASCII_ink_offset_y=1,descriptor_geometry_and_6x12_logical_metrics_unchanged=True)
'''
    namespace={**old_FE.__dict__,'CURRENT_ARM9':CURRENT_ARM9}
    exec(compile(source,__file__+'::current-FE-typed-painter','exec'),namespace)
    paint,receipt=namespace['make_painter'](image)
    receipt.update(effective_painter_sha256=sha(source.encode('utf-8')),
        current_oracle_module_sha256=sha(Path(__file__).read_bytes()),
        earlier_oracle_source_sha256=sha(Path(old_FE.__file__).read_bytes()))
    return paint,receipt
