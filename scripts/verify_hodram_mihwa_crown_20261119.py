"""Run complete native display checks for the Crown scene."""
from inspect import getsource

from scripts import stage_hodram_mihwa_crown_20261119 as build
from scripts import verify_rafael_first_voyage_debrief_20261119 as workflow
from scripts.source_locked_derivation_v5118 import checked_text

base = build.base
ROOT = build.ROOT / "native_display"
PROOF = ROOT / "native_display.json"

if __name__ == "__main__":
    source = checked_text(getsource(workflow.main), {
        '{"/data/SC0.DK4": [44, 47]}': '{"/data/SC1.DK4": [89]}',
        "build.review.TOKEN": "build.review.workflow.TOKEN",
        'path = "/data/SC0.DK4"': 'path = "/data/SC1.DK4"',
        'assert len(checked) == 39 and len(retained) == 93': 'assert len(checked) == 7 and len(retained) == 11',
        '{f"DK4_MES_B44_R{i:04}" for i in (17, 152, 308, 316, 327)}': '{"DK4_MES_B89_R0035"}',
        '"Rafael opening"': '"Hodram default"',
        'Checked 39 revised pages, five macro records and 93 exact retentions.':
            'Checked seven revised pages, the name substitution and 11 exact retentions.',
    })
    scope = vars(workflow) | globals() | {"STOCK": {"FI": "Hodram", "FA": "Bergstrom", "FO": "Bergstrom Fleet"}}
    exec(compile(source, __file__ + "::crown_native_pages", "exec"), scope)
    scope["main"]()
