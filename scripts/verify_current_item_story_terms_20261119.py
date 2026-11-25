"""Check the revised story labels and item-loss notices on their native renderers."""
from inspect import getsource

from scripts import stage_current_item_story_terms_20261119 as build
from scripts import verify_rafael_first_voyage_debrief_20261119 as workflow
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
ROOT = build.ROOT / "native_display"
PROOF = ROOT / "native_display.json"

if __name__ == "__main__":
    source = checked_text(getsource(workflow.main), {
        '{"/data/SC0.DK4": [44, 47]}': '{"/data/SC0.DK4": [214, 219], "/data/SC2.DK4": [61]}',
        '    path = "/data/SC0.DK4"\n    bank = native.IlnkContainer.parse(image.read_file(path)).blocks':
            '    fe = build.stage.system.native_painter(ctx)\n'
            '    banks = {p: native.IlnkContainer.parse(image.read_file(p)).blocks for p in stored["changed_blocks"]}',
        '        assert group["file_path"] == path\n        block = bank[group["block"]]':
            '        path = group["file_path"]\n        block = banks[path][group["block"]]',
        'expand, None, model_names': 'expand, fe, model_names',
        'build.review.TOKEN': 'build.review.workflow.TOKEN',
        'assert len(checked) == 39 and len(retained) == 93':
            'assert len(checked) == 12 and len(retained) == 71\n'
            '    assert sum(r["kind"] == "system-FE" for r in checked) == 8',
        '{f"DK4_MES_B44_R{i:04}" for i in (17, 152, 308, 316, 327)}': 'set()',
        'Checked 39 revised pages, five macro records and 93 exact retentions.':
            'Verified four progressive pages, eight system notices and 71 exact retentions.',
    })
    scope = vars(workflow) | globals()
    exec(compile(source, __file__ + "::item_story_native", "exec"), scope)
    scope["main"]()
