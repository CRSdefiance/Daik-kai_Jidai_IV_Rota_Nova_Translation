"""Register the complete inherited stack and the village UI text stage."""

import copy
import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.village_ui_text import transform
from dk4tool.rom.nds import NdsImage
from scripts.prepare_village_ui_v609 import MANUSCRIPT, ROOT, save


def main():
    source = NdsImage.open("out/all_routes_combined_v608_candidate.nds")
    arm = source.read_file("/__arm9__.bin")
    route = source.read_file("/data/SC2.DK4")
    a, s, proof = transform(arm, route, json.loads(MANUSCRIPT.read_text(encoding="utf-8")))
    (ROOT / "research_arm9.bin").write_bytes(a)
    save(ROOT / "transform_proof.json", proof)
    config = Path("translations/village_ui_text_v1.json")
    save(config, {"format": "dk4-village-ui-text-v1", "source_arm9_sha256": sha(arm),
        "source_SC2_sha256": sha(route), "target_arm9_sha256": sha(a), "target_SC2_sha256": sha(s),
        "manuscript": str(MANUSCRIPT), "manuscript_sha256": sha(MANUSCRIPT.read_bytes()),
        "status": "experimental"})
    path = Path("translations/release_stack.json")
    d = json.loads(path.read_text(encoding="utf-8"))
    profile = copy.deepcopy(d["profiles"]["all-routes-unified-v608"])
    profile.update({"village_ui_text": str(config), "status": "experimental",
        "description": "Complete V608 stack plus all24 original village name descriptors and six menu captions in English.",
        "note": "Retain original menu actions and place identities; same-width Leveque consistency in three Lil records. Actual UI/native verification required."})
    if "all-routes-unified-v609" in d["profiles"]:
        assert d["profiles"]["all-routes-unified-v609"] == profile
    d["profiles"]["all-routes-unified-v609"] = profile
    save(path, d)
    print("Registered V609:24 names/6 menu captions/3 same-width story name fixes;pool growth", proof["pool_growth"])


if __name__ == "__main__":
    main()
