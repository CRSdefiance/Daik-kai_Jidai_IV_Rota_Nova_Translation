"""Match the two retained Japanese ellipses with their native shadow color."""
from scripts.analyze_rafael_B221_B240_actual_v1 import TEMPLATE, source as previous
from scripts.analyze_reviewed_dynamic_fixture_v1 import dynamic_headers
from scripts.source_locked_derivation_v5118 import checked_text


scope = {'DK4_MES_B251_R0020', 'DK4_MES_B251_R0039'}
plane_scope = {
    "            expected.append(dict(id=row['id'], page=number, selector=row['selector'], width=width,": """
            ellipsis_shadow = row['id'] in ELLIPSES
            if ellipsis_shadow:
                assert body == bytes.fromhex('8163') and width == 216 and set(plane) == {0,1,15}
                assert plane.count(1) == plane.count(15) == 6
            expected.append(dict(ellipsis_shadow=ellipsis_shadow, id=row['id'], page=number, selector=row['selector'], width=width,""",
    "pixel_mask_sha256=sha(bytes(bool(v) for v in plane))": "pixel_mask_sha256=sha(bytes(v==1 if ellipsis_shadow else bool(v) for v in plane))",
    "        samples.append(dict(**page, capture=cap, frame=cap['frame'], live_modal_frame=active['frame'],": """
        if page['ellipsis_shadow']:
            plane = Path(page['native_plane']).read_bytes()
            assert bytes(rgb == (197,198,197) for rgb in crop.getdata()) == bytes(v==15 for v in plane)
        samples.append(dict(**page, capture=cap, frame=cap['frame'], live_modal_frame=active['frame'],""",
}
source = checked_text(previous, {
    "    exec(compile(source,__file__+'::complete-dynamic-headers-and-body-crops','exec'),globals())":
        """    source=checked_text(source,plane_scope)
    exec(compile(source,__file__+'::complete-dynamic-headers-and-ellipsis-palette','exec'),globals())""",
})
ELLIPSES = scope

if __name__ == '__main__':
    exec(compile(source, __file__+'::source-bound-rose-ellipsis-analysis', 'exec'), globals())
