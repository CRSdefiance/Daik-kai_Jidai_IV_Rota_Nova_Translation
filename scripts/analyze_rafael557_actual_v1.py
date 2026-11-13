"""Check standalone source punctuation in both foreground and shadow colors."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

TEMPLATE=Path('scripts/analyze_reviewed_scene_fixture.py')
ELLIPSIS=Path('work/analysis/Rafael557_native_v1_20261105/DK4_MES_B143_R0311_p1.bin')
PALETTE_CAPTURE=Path('work/rf557a_1105/frame_011760_cold_boot.png')
PALETTE_REPORT=Path('work/rf557a_1105/capture_report.json')

def exact_ellipsis_palette(source):
    return checked_text(source,{
        '    expected = []':"""    expected = []
    ellipsis=ELLIPSIS.read_bytes();assert len(ellipsis)==216*64 and set(ellipsis)=={0,1,15}
    palette_report=load(PALETTE_REPORT)
    palette_cap=next(c for c in palette_report['frames_captured'] if Path(c['path'])==PALETTE_CAPTURE)
    assert sha(PALETTE_CAPTURE.read_bytes())==palette_cap['PNG_sha256'] and palette_report['cold_boot']
    palette_sample=list(Image.open(PALETTE_CAPTURE).convert('RGB').crop((16,296,232,360)).getdata())
    for index,color in [(1,(0,8,0)),(15,(197,198,197))]:
        assert [v==index for v in ellipsis]==[rgb==color for rgb in palette_sample]""",
        '            expected.append(dict(id=row':"""            shadow=None
            if width==216 and 15 in plane:
                assert set(plane)=={0,1,15}
                punctuation=body.rstrip(b' ')
                if punctuation==bytes.fromhex('8163'):assert plane==ellipsis
                else:assert row['id']=='DK4_MES_B145_R0093' and punctuation==bytes.fromhex('81498149')
                shadow=sha(bytes(v==15 for v in plane));plane=bytes(v==1 for v in plane)
            expected.append(dict(source_ellipsis_shadow_mask_sha256=shadow,id=row""",
        "        if sha(bytes(rgb == (0, 8, 0) for rgb in crop.getdata())) != page['pixel_mask_sha256']:":
            """        colors=list(crop.getdata())
        if page['source_ellipsis_shadow_mask_sha256'] is not None:
            if sha(bytes(rgb==(197,198,197) for rgb in colors))!=page['source_ellipsis_shadow_mask_sha256']:continue
        if sha(bytes(rgb == (0, 8, 0) for rgb in colors)) != page['pixel_mask_sha256']:""",
        "NAMES, report_path, observer_path, Path(__file__)]":
            "NAMES, decisions_path, report_path, observer_path, ELLIPSIS, PALETTE_REPORT, PALETTE_CAPTURE, TEMPLATE, Path(__file__)]",
    })

if __name__=='__main__':
    source=checked_text(TEMPLATE.read_text(encoding='utf-8'),{
        "exec(compile(source,__file__+'::same-ordered-calls-complete-pixels-andblank-guards','exec'),globals())":
            "exec(compile(exact_ellipsis_palette(source),__file__+'::same-pixels-with-exact-source-ellipsis-palette','exec'),globals())",
    })
    exec(compile(source,__file__+'::qualified-source-ellipsis-palette','exec'),globals())
