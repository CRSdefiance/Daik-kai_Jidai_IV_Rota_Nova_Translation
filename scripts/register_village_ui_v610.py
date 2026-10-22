"""Register the complete village localization with no staged-pool growth."""

import copy
import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.village_ui_compact import transform
from dk4tool.rom.nds import NdsImage
from scripts.prepare_village_ui_v609 import MANUSCRIPT, save

ROOT = Path("work/analysis/village_ui_v610")


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    source = NdsImage.open("out/all_routes_combined_v608_candidate.nds")
    arm, route = source.read_file("/__arm9__.bin"), source.read_file("/data/SC2.DK4")
    target, target_route, proof = transform(arm, route, json.loads(MANUSCRIPT.read_text(encoding="utf-8")))
    (ROOT / "research_arm9.bin").write_bytes(target)
    save(ROOT / "transform_proof.json", proof)
    config = Path("translations/village_ui_text_v2.json")
    save(config, {"format": "dk4-village-ui-text-v2", "source_arm9_sha256": sha(arm),
        "source_SC2_sha256": sha(route), "target_arm9_sha256": sha(target),
        "target_SC2_sha256": sha(target_route), "manuscript": str(MANUSCRIPT),
        "manuscript_sha256": sha(MANUSCRIPT.read_bytes()), "status": "experimental"})
    path = Path("translations/release_stack.json")
    d = json.loads(path.read_text(encoding="utf-8"))
    profile = copy.deepcopy(d["profiles"]["all-routes-unified-v608"])
    profile.update({"village_ui_text": str(config), "village_ui_text_version": 2, "status": "experimental",
        "description": "Complete V608 integration plus all24 village names/six menu captions and three same-width Leveque story-name corrections.",
        "note": "Compact source-owned text bins;all staged-pool/startup/arena/cache bytes exact V608. V609 larger-pool candidate rejected. Native verification required."})
    if "all-routes-unified-v610" in d["profiles"]:
        assert d["profiles"]["all-routes-unified-v610"] == profile
    d["profiles"]["all-routes-unified-v610"] = profile
    d["profiles"]["all-routes-unified-v609"]["note"] = "REVOKED candidate: ordinary and late-START schedules reproduce black upper screen;growth-only research also fails. Do not hand off or use as a parent. V610 retains identical localization without pool growth."
    save(path, d)
    print("Registered V610:30 complete UI labels+3 same-width names;zero staged-pool growth;V609 explicitly rejected.")


if __name__ == "__main__":
    main()
