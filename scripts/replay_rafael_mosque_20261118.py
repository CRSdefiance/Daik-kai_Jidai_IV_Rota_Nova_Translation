"""Cold boot the candidate and sample Rafael's unchanged scene commands in the initialized opening."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_london_guild_assignments_20261118 as previous
from scripts import stage_rafael_mosque_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
ROOT = stage.ROOT / "rafael_initialized"
ROM = ROOT / "Rafael_Mosque_Excerpts_RESEARCH_ONLY.nds"
FILE = "/data/SC0.DK4"
SETUP = ROOT / "fixture.json"
LIVE = ROOT / "verified.json"
LAST = 11301
EXCERPTS = (
    (313, (22, 25, 34, 50, 58)),
    (316, (14, 18, 22, 26, 30, 35, 38, 41, 46, 50, 55)),
    (317, (23, 52, 103)),
    (318, (133, 137, 141, 146, 151, 160, 163, 168, 198, 202, 205, 212)),
)

scope = vars(previous) | globals()
prep = checked_text(getsource(previous.prepare), {
    'range(3800, 8101, 250)': 'range(3800, LAST - 100, 225)',
})
audit = checked_text(getsource(previous.verify), {
    '    photos = quest.prior.TOOL.photos(report)':
        """    release = base.load(stage.parent.RELEASE)
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, release["own_registered_startup"], captain=3)
    assert ctx.arm == arm
    fe_paint = stage.stage.system.native_painter(ctx)
    photos = quest.prior.TOOL.photos(report)""",
    '        raster = paint(arm, font, body)':
        """        if raw[5] == 254:
            surface = fe_paint(body)
            plane = surface["physical"]
            visible = bytes(int(bool(v)) for y in range(64) for v in plane[y * 228:y * 228 + 216])
            raster = {"pages": [{"page": 1, "native_plane_hex": visible.hex()}]}
        else:
            raster = paint(arm, font, body)""",
    'actual_Castor_and_Rafael_macro_glyphs=True':
        'actual_Rafael_macro_and_speakerless_FE=True',
    "including both captain name substitutions.":
        "including the Rafael substitution and speakerless FE panels.",
})
for source, label in ((prep, "exact-entry-with-Rafael-excerpts"), (audit, "matched-progressive-and-FE")):
    exec(compile(source, __file__ + "::" + label, "exec"), scope)

capture = FunctionType(previous.capture.__code__, scope)
startup = FunctionType(previous.startup.__code__, scope)

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "verify", "startup"))
    action = parser.parse_args().action
    (capture if action == "capture" else startup if action == "startup" else scope[action])()
