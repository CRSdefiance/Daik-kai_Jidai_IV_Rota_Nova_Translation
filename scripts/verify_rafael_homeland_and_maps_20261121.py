"""Verify the native and stored display of Rafael's homeland and map scenes."""

from inspect import getsource
from types import SimpleNamespace

from scripts import stage_rafael_homeland_and_maps_20261121 as stage
from scripts import verify_rafael_palace_and_alliance_20261121 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


base, native, display, town, PATH = precedent.base, precedent.native, precedent.display, precedent.town, precedent.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
prior_root = stage.ROOT.with_name("homeland_and_maps_staged_v2")
first = SimpleNamespace(ROOT=prior_root, ROM=prior_root / stage.ROM.name, PROOF=prior_root / stage.PROOF.name)

main = getsource(precedent.main)
text = checked_text(main, {
    "stage.parent.display.audit_company_name": "stage.parent.parent.display.audit_company_name",
    "len(entries) == 270 and fe_count == 6": "len(entries) == 287 and fe_count == 0",
    '[m["block"] for m in menus] == [143, 146, 148]': '[m["block"] for m in menus] == [154]',
    'retained_fu == ["DK4_MES_B143_R0067", "DK4_MES_B146_R0006"]': "not retained_fu",
    '"refined_palace_speech"': '"refined_homeland_speech"',
    "six speakerless notices, six captions and two retained full-name substitutions":
        "two typed choice captions",
})
scope = vars(precedent) | globals() | {"precedent": precedent.precedent}
exec(compile(text, __file__ + "::native", "exec"), scope)
exec(compile(getsource(precedent.verify_names), __file__ + "::names", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
    scope["verify_names"]()
