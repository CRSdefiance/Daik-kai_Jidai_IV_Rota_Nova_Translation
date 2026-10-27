"""Audit every complete route string that can match the research catalog."""

import json
from pathlib import Path

from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import DialogueProfile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/confirmed_names_v201")


def main():
    plan = json.loads((ROOT / "catalog_plan.json").read_text(encoding="utf-8"))
    preparation = json.loads(Path("work/analysis/confirmed_names_v198/confirmed_source_locked_drafts.json").read_text(encoding="utf-8"))
    drafts = {(r["file_path"], r["id"]): dict(r) for r in preparation["records"]}
    overrides = json.loads(Path("translations/confirmed_name_editorial_overrides_v1.json").read_text(encoding="utf-8"))
    for override in overrides["records"]:
        draft = drafts[override["file_path"], override["id"]]
        assert draft["source_hex"] == override["expected_source_hex"]
        draft.update({field: override[field] for field in ("english", "review", "localization_note")})
    source_path = Path("out/all_routes_combined_v190_candidate.nds")
    image = NdsImage.open(source_path)
    assert sha(source_path.read_bytes()) == plan["source_ROM_sha256"]
    canonical = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
    clean = NdsImage.open("work/clean.nds")
    source_locks = []
    for path in (f"/data/SC{index}.DK4" for index in range(4)):
        rows = [r for r in plan["prepared_records"] if r["file_path"] == path]
        if not rows:
            continue
        canonical_raw = canonical.read_file(path)
        canonical_blocks = IlnkContainer.parse(canonical_raw).blocks
        clean_blocks = IlnkContainer.parse(clean.read_file(path)).blocks
        for row in rows:
            draft = drafts[path, row["id"]]
            assert sha(canonical_raw) == draft["source_file_sha256"]
            block_id = int(row["id"].split("_B")[1].split("_")[0])
            record_id = int(row["id"].split("_R")[1])
            expected = bytes.fromhex(row["canonical_source_hex"])
            assert canonical_blocks[block_id].split(b"\0")[record_id] == expected
            assert clean_blocks[block_id].split(b"\0")[record_id] == expected
            source_locks.append({"file_path": path, "id": row["id"], "canonical_file_and_record_exact": True,
                                 "clean_Japanese_record_exact": True})
    keys = {bytes.fromhex(row["key_hex"]): bytes.fromhex(row["target_hex"]) for row in plan["records"]}
    selected = {(r["file_path"], r["id"]) for r in plan["prepared_records"]}
    matches, covered, scanned = [], set(), 0
    for path in (f"/data/SC{index}.DK4" for index in range(4)):
        for block_id, block in enumerate(IlnkContainer.parse(image.read_file(path)).blocks):
            for record_id, raw in enumerate(block.split(b"\0")):
                scanned += 1
                forms = [("whole", raw)]
                if raw:
                    forms.append(("body", raw[1:]))
                for form, key in forms:
                    if key not in keys:
                        continue
                    owner = path, f"DK4_MES_B{block_id}_R{record_id:04d}"
                    if owner not in drafts:
                        raise ValueError(f"Catalog can affect an unreviewed source owner: {owner} ({form})")
                    draft = drafts[owner]
                    payload = dict(preparation["proposed_profiles_not_registered"][draft["proposed_profile"]])
                    payload["leading_speaker_bytes"] = frozenset(payload["leading_speaker_bytes"])
                    target = encode_relocatable_dialogue(bytes.fromhex(draft["source_hex"]), draft["english"].removesuffix("{PAD}"), DialogueProfile(**payload)).encoded
                    expected = target if form == "whole" else target[1:]
                    if keys[key] != expected:
                        raise ValueError(f"Same native key has incompatible source-derived output: {owner} ({form})")
                    covered.add(owner)
                    matches.append({"file_path": path, "id": owner[1], "form": form,
                                    "in_selected25": owner in selected,
                                    "complete_target_matches_own_source_dossier": True})
    assert selected <= covered
    report = {"format": "dk4-confirmed-name-catalog-route-scope-audit-v1",
              "source_ROM_sha256": plan["source_ROM_sha256"], "catalog_ARM9_sha256": plan["target_arm9_sha256"],
              "route_files_scanned": 4, "NUL_segments_scanned": scanned, "matches": matches,
              "selected_source_locks": source_locks,
              "unique_source_records_matched": len(covered), "selected25_all_covered": True,
              "all_extra_matches_have_identical_own_source_derived_targets": True,
              "unreviewed_or_conflicting_route_matches": 0,
              "scope": "Every whole or single-speaker-stripped NUL string in the four current route resources; not every runtime pointer, other consumer, or original deep scene.",
              "research_only": True, "goal_complete": False}
    (ROOT / "catalog_route_scope_audit.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"segments": scanned, "matched_source_records": len(covered), "selected25_covered": True, "conflicting_matches": 0}))


if __name__ == "__main__":
    main()
