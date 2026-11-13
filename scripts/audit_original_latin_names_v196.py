"""Lock the original Latin name evidence and inventory active spelling changes."""

import hashlib
import json
import re
from pathlib import Path

from dk4tool.graphics.fls import FlsArchive
from dk4tool.rom.nds import NdsImage


DECISIONS = [
    ("Raphael", "Rafael", "Rafael Castor", 22),
    ("Hodram", "Hoodlum", "Hoodlum Joakim Bergstrom", 46),
    ("Kamil", "Camille", "Camille Overijssel", 71),
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    registry_path = Path("translations/release_stack.json")
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    profile = registry["profiles"]["all-routes-unified-v190"]
    rom_paths = [
        Path("work/clean.nds"),
        Path("out/raphael_natural_v2_accepted_base.nds"),
        Path("out/all_routes_combined_v190_candidate.nds"),
    ]
    archives = [FlsArchive(NdsImage.open(p).read_file("/FLS/M28.fls")) for p in rom_paths]
    root = Path("work/qa/original_latin_names_v196")
    root.mkdir(parents=True, exist_ok=True)
    decisions = []
    for before, after, full_name, texture_index in DECISIONS:
        textures = [a.texture(texture_index) for a in archives]
        source = textures[0]
        assert all((t.width, t.height, t.palette, t.indices) ==
                   (source.width, source.height, source.palette, source.indices) for t in textures)
        image_path = root / f"M28_texture_{texture_index}.png"
        source.render().save(image_path)
        decisions.append({
            "previous_project_spelling": before,
            "preferred_spelling": after,
            "original_full_name": full_name,
            "resource": "/FLS/M28.fls",
            "texture_index": texture_index,
            "dimensions": [source.width, source.height],
            "source_indices_sha256": sha(source.indices),
            "review_image": image_path.as_posix(),
            "review_image_sha256": sha(image_path.read_bytes()),
            "unchanged_in_clean_canonical_and_V190": True,
            "ASCII_expansion_bytes_before": len(before),
            "ASCII_expansion_bytes_after": len(after),
            "changes_ASCII_pair_parity": len(before) % 2 != len(after) % 2,
        })
    # Later active batches can supersede a record. Report the last registered
    # manuscript value rather than counting obsolete drafts as shipped text.
    effective = {}
    for batch_path in profile["batches"]:
        batch = json.loads(Path(batch_path).read_text(encoding="utf-8"))
        for record in batch.get("records", []):
            english = record.get("english")
            if not isinstance(english, str):
                continue
            owner = (batch.get("file_path"), record["id"])
            effective[owner] = (batch_path, batch.get("format"), english)
    hits = []
    for (file_path, record_id), (batch_path, batch_format, english) in sorted(effective.items()):
        changes = [
            {"from": old, "to": new, "occurrences": len(re.findall(r"\b" + old + r"\b", english))}
            for old, new, _, _ in DECISIONS if re.search(r"\b" + old + r"\b", english)
        ]
        if changes:
            hits.append({"file_path": file_path, "id": record_id,
                         "batch": batch_path, "format": batch_format,
                         "changes": changes})
    report = {
        "format": "dk4-original-latin-name-decision-audit-v1",
        "policy": "Use original Latin name artwork when it establishes the character's name.",
        "user_decision": "If latin artwork has already established a name shouldn't we use that?",
        "profile": "all-routes-unified-v190",
        "registry_sha256": sha(registry_path.read_bytes()),
        "source_ROMs": [{"path": p.as_posix(), "sha256": sha(p.read_bytes())} for p in rom_paths],
        "decisions": decisions,
        "Lil_Argot": "Retain the established Latin spelling; visible with Camille in texture 71.",
        "effective_active_batch_records_with_old_spelling": hits,
        "effective_active_batch_record_count": len(hits),
        "migration_complete": False,
        "coverage_note": "Manuscript inventory only. Terminal name pools, biographies, macros and baked canonical records also need review; these counts are not a complete shipped-ROM audit.",
        "required_migration_checks": [
            "Use clean Japanese/source locks and original Latin art; preserve executable speaker and macro controls.",
            "Regenerate logical English through each route formatter; verify allocations, wrapping and complete glyphs.",
            "Review runtime macro lengths and parity for Rafael and Hoodlum, whose ASCII parity changes.",
            "Verify shared name ownership, allocated capacity and aliases before changing name pools.",
            "Reproduce the prior integrated ROM, preserve all registered layers, and cold-boot changed nameplates and dialogue.",
        ],
        "ROM_modified": False,
    }
    destination = Path("work/analysis/original_latin_names_v196.json")
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"report": destination.as_posix(), "records": len(hits),
                      "decisions": [{"from": d["previous_project_spelling"], "to": d["preferred_spelling"]}
                                    for d in decisions], "ROM_modified": False}))


if __name__ == "__main__":
    main()
