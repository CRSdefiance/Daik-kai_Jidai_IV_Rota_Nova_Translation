"""Register the complete V540 stack plus a bounded original-grain stage."""

import copy
import hashlib
import json
from pathlib import Path

from dk4tool.patch.source_plaque_grain import apply_release
from dk4tool.rom.nds import NdsImage


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    root = Path("work/analysis/plaque_texture_v542")
    root.mkdir(parents=True, exist_ok=True)
    parent = NdsImage.open("out/all_routes_combined_v540_candidate.nds")
    clean = NdsImage.open("work/clean.nds")
    proof = read("work/analysis/plaque_texture_v541/source_texture_prototype_proof.json")
    config = {"format": "dk4-source-plaque-grain-release-v1",
              "donor_file": "/_pxl/towninfo.pxl",
              "donor_file_sha256": sha(clean.read_file("/_pxl/towninfo.pxl")),
              "dependencies": {}, "files": [],
              "scope": "Original grain for 17 plaque interiors; existing letters, bevels, "
                       "atlas dimensions and palette unchanged. Other plaques and hints remain open."}
    for group, name in zip(proof["groups"],
                           ("assign_sailors_graphics_v5", "person_info_graphics_v3"), strict=True):
        path = f"translations/{name}.json"
        batch = read(path)
        config["dependencies"][path] = sha(Path(path).read_bytes())
        config["files"].append({
            "file_path": batch["file_path"],
            "source_sha256": sha(parent.read_file(batch["file_path"])),
            "target_sha256": group["prototype_sha256"],
            "records": [{"id": r["id"], "english": r["text"],
                         "source_japanese": r["source_japanese"],
                         "plaque_box": r["plaque_box"], "draw_box": r["draw_box"],
                         "ink_palette_index": batch["color_index"]} for r in batch["records"]]})
    cfg = Path("translations/source_plaque_grain_v1.json")
    write(cfg, config)
    files, result = apply_release(parent, clean, cfg)
    assert len(files) == 2 and sum(len(r["changed_records"]) for r in result["files"]) == 17
    write(root / "stage_proof.json", result)
    path = Path("translations/release_stack.json")
    stack = read(path)
    profile = copy.deepcopy(stack["profiles"]["all-routes-unified-v540"])
    profile["source_plaque_grain"] = cfg.as_posix()
    profile["description"] = profile["note"] = (
        "Complete V540 stack plus clean-source grain for 17 plaque interiors. All plaque audits remain open.")
    profile["status"] = "experimental"
    stack["profiles"]["all-routes-unified-v542"] = profile
    write(path, stack)
    for name in ("crew", "person"):
        report = read(f"work/emulation_v193/plaque_audit_v300_{name}/capture_report.json")
        write(root / f"{name}_inputs.json", report["scripted_input_schedule"])
    print("Registered V542: 17 plaques, 470 inherited batches, 114 accepted layers.")


if __name__ == "__main__":
    main()
