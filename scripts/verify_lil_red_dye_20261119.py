"""Verify the seven revised Red Dye story pages with their original consumers."""
from inspect import getsource

from scripts import stage_lil_red_dye_20261119 as build
from scripts import verify_rafael_first_voyage_debrief_20261119 as workflow
from scripts.source_locked_derivation_v5118 import checked_text

base = build.base
ROOT = build.ROOT / "native_display"
PROOF = ROOT / "native_display.json"

if __name__ == "__main__":
    source = checked_text(getsource(workflow.main), {
        '{"/data/SC0.DK4": [44, 47]}': '{"/data/SC2.DK4": [26, 129, 130, 131]}',
        'path = "/data/SC0.DK4"': 'path = "/data/SC2.DK4"',
        'build.review.TOKEN': 'build.review.workflow.TOKEN',
        'assert len(checked) == 39 and len(retained) == 93': 'assert len(checked) == 7 and len(retained) == 80',
        '{f"DK4_MES_B44_R{i:04}" for i in (17, 152, 308, 316, 327)}': 'set()',
        'Checked 39 revised pages, five macro records and 93 exact retentions.':
            'Verified seven revised pages and 80 exact retentions.',
    })
    scope = vars(workflow) | globals()
    exec(compile(source, __file__ + "::red_dye_native_pages", "exec"), scope)
    scope["main"]()
