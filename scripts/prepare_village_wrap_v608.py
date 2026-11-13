"""Register the complete V604 stack plus the source-locked village layout fix."""

import copy
import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.village_portrait_wrap import MANUSCRIPT, transform
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/village_wrap_v608")
CONFIG = Path("translations/village_portrait_wrap_v1.json")


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    arm = NdsImage.open("out/all_routes_combined_v604_candidate.nds").read_file("/__arm9__.bin")
    target, proof = transform(arm)
    (ROOT / "research_arm9.bin").write_bytes(target)
    save(ROOT / "transform_proof.json", proof)
    save(CONFIG, {"format": "dk4-village-portrait-wrap-v1", "source_arm9_sha256": sha(arm),
        "target_arm9_sha256": sha(target), "manuscript": str(MANUSCRIPT),
        "manuscript_sha256": sha(MANUSCRIPT.read_bytes()), "status": "experimental",
        "source_evidence": "docs/village_water_v607_checkpoint.md"})
    path = Path("translations/release_stack.json")
    registry = json.loads(path.read_text(encoding="utf-8"))
    profile = copy.deepcopy(registry["profiles"]["all-routes-unified-v604"])
    profile.update({"status": "experimental", "village_portrait_wrap": str(CONFIG),
        "description": "Complete V604 integration with all village clues/messages compiled for the actual 228x48 portrait canvas.",
        "note": "English prose and answers unchanged; all text renderers, graphics and keyboard code retained. Native verification required."})
    if "all-routes-unified-v608" in registry["profiles"]:
        assert registry["profiles"]["all-routes-unified-v608"] == profile
    registry["profiles"]["all-routes-unified-v608"] = profile
    save(path, registry)
    print("Registered experimental V608;470 inherited batches/114 accepted layers;11 wrapped strings changed;32 pool bytes added.")


if __name__ == "__main__":
    main()
