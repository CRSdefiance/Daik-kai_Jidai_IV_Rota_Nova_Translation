"""Prepare the complete confirmed-name text migration with source and layout evidence."""

import copy
import json
import re
from dataclasses import asdict, replace
from pathlib import Path

from dk4tool.dialogue.codec import tokenize_raw, tokens_to_markup
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import export_mesfile_rows

ROOT = Path("work/analysis/confirmed_names_v198")
PATHS = ("/data/SC0.DK4", "/data/SC1.DK4", "/data/SC2.DK4", "/data/SC3.DK4",
         "/COMMON/MESFILE.DK4", "/COMMON/HELP.DK4")
OLD = re.compile(r"\b(?:Raphael|Kamil|Joachim|Hoamei|Hoa-mei|Lee)\b")
REPLACEMENTS = {"Raphael": "Rafael", "Kamil": "Camille", "Joachim": "Joakim",
                "Hoamei": "Huamei", "Hoa-mei": "Huamei", "Lee": "Li"}


def renamed(text):
    return OLD.sub(lambda match: REPLACEMENTS[match[0]], text)


def macro_affected(path, english):
    return (path == PATHS[0] and any(m in english for m in ("{MACRO:FI}", "{MACRO:FU}"))) or (
        path == PATHS[3] and "{MACRO:FA}" in english)


def selected_profile(name, path):
    profile = get_dialogue_profile(name)
    lengths, widths = dict(profile.macro_ascii_lengths), dict(profile.macro_widths)
    if path == PATHS[0]:
        if lengths.get("FI") != 7:
            raise ValueError("Original Rafael route first-name calibration differs")
        lengths["FI"], widths["FI"] = 6, 36
        if "FU" in lengths:
            if lengths["FU"] != 14:
                raise ValueError("Original full-name calibration differs")
            lengths["FU"], widths["FU"] = 13, 78
    elif path == PATHS[3]:
        if lengths.get("FA") != 3:
            raise ValueError("Original Maria surname calibration differs")
        lengths["FA"], widths["FA"] = 2, 12
    return replace(profile, name=profile.name + "-confirmed-names-v1",
                   macro_ascii_lengths=lengths, macro_widths=widths)


def paragraph(text):
    # These are reviewed-name migrations, not preservation of legacy positioned
    # wrapping. Keep punctuation/words and let the formatter determine layout.
    if "{LB@" in text or "{ALIGN@" in text:
        raise ValueError("Positioned markup needs separate reviewed migration")
    return re.sub(r"\s+", " ", text.replace("{LB}", " ")).strip()


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    canonical = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
    clean = NdsImage.open("work/clean.nds")
    policy_path = Path("translations/character_name_localization_policy_v1.json")
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    assert policy["reviewed_name_decisions_settled"]
    assert any(row.get("localized_first_name") == "Camille" for row in policy["confirmed_decisions"])
    registry_path = Path("translations/release_stack.json")
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registered = registry["profiles"]["all-routes-unified-v190"]["batches"]
    originals = {path: canonical.read_file(path) for path in PATHS}
    source_rows = {path: {r["id"]: r for r in export_mesfile_rows(raw, path, include_non_japanese=True)}
                   for path, raw in originals.items()}
    japanese_rows = {path: {r["id"]: r for r in export_mesfile_rows(clean.read_file(path), path, include_non_japanese=True)}
                     for path in PATHS}
    effective, active_ids, calibrated_profiles = {}, set(), {path: [] for path in PATHS[:4]}
    for batch_path in registered:
        batch = json.loads(Path(batch_path).read_text(encoding="utf-8"))
        path = batch.get("file_path")
        if path not in originals:
            continue
        assert batch["source_file_sha256"] == sha(originals[path])
        if path in calibrated_profiles and batch.get("dialogue_profile"):
            name = batch["dialogue_profile"]
            if name not in calibrated_profiles[path]:
                calibrated_profiles[path].append(name)
        for row in batch.get("records", []):
            if isinstance(row.get("english"), str):
                key = path, row["id"]
                active_ids.add(key)
                effective[key] = (batch_path, batch, row)
    # Recover source-approved markup/context for baked records where retained.
    # If its original batch is unavailable, decode the immutable canonical record
    # with the conservative route profile, paired with clean Japanese evidence.
    baked = {}
    for layer in registry["accepted_layers"]:
        batch_path = layer["batch"]
        if not Path(batch_path).is_file():
            continue
        batch = json.loads(Path(batch_path).read_text(encoding="utf-8"))
        if batch.get("file_path") not in PATHS:
            continue
        for row in batch.get("records", []):
            if isinstance(row.get("english"), str):
                baked[batch["file_path"], row["id"]] = batch_path, batch, row
    fallback = dict(zip(PATHS[:4], ("raphael-story-live", "hodram-story-live",
                                   "lil-story-deep-route-live", "maria-story-shared-events-live"), strict=True))
    baked_control_review, recovered_baked_controls = [], []
    for path in PATHS[:4]:
        profile = get_dialogue_profile(fallback[path])
        for record_id, row in source_rows[path].items():
            key = path, record_id
            if key in active_ids:
                continue
            raw = bytes.fromhex(row["source_hex"])
            record_profile = profile
            jp_record = japanese_rows[path].get(record_id)
            jp_raw = bytes.fromhex(jp_record["source_hex"]) if jp_record else b""
            if raw and jp_raw and raw[0] == jp_raw[0] and raw[0] >= 0x80 and raw[0] not in profile.leading_speaker_bytes:
                candidates = [get_dialogue_profile(name) for name in calibrated_profiles[path]
                              if raw[0] in get_dialogue_profile(name).leading_speaker_bytes]
                if candidates:
                    # Reuse a registered, route-specific presentation-state
                    # calibration rather than treating the byte as Shift-JIS
                    # or declaring a new global speaker-byte rule.
                    record_profile = candidates[0]
                    recovered_baked_controls.append({"file_path": path, "id": record_id,
                                                     "leading_byte": raw[0], "profile": record_profile.name,
                                                     "clean_and_canonical_leading_byte_agree": True})
            markup = tokens_to_markup(tokenize_raw(raw, leading_speaker_bytes=record_profile.leading_speaker_bytes)).strip()
            if not OLD.search(markup) and not macro_affected(path, markup):
                continue
            if any("\u3040" <= character <= "\u30ff" or "\u3400" <= character <= "\u9fff"
                   for character in markup):
                # An unmapped high presentation byte can combine with the first
                # Latin letter into a CP932 glyph. Do not silently turn that
                # decoder artifact into newly authored English or discard bytes.
                baked_control_review.append({"file_path": path, "id": record_id,
                                             "source_hex": row["source_hex"],
                                             "decoder_observation": markup,
                                             "clean_Japanese_source": japanese_rows[path].get(record_id),
                                             "requires_native_baked_lead_mapping": True})
                continue
            if key in baked:
                batch_path, batch, authored = baked[key]
                # Old source batches can be positioned/legacy or revoked probes.
                # Use their context, but encode from current source-owned bytes.
                authored = copy.deepcopy(authored)
                authored["english"] = markup + "{PAD}"
            else:
                batch_path = "immutable-canonical-baked-record"
                batch, authored = {}, {"id": record_id, "english": markup + "{PAD}"}
            batch = {**batch, "encoder": "dialogue-fixed-v1", "dialogue_profile": record_profile.name}
            effective[key] = batch_path, batch, authored
    overrides_path = Path("translations/confirmed_name_editorial_overrides_v1.json")
    overrides = {(row["file_path"], row["id"]): row for row in
                 json.loads(overrides_path.read_text(encoding="utf-8"))["records"]}
    additional_override_paths = [Path("translations/confirmed_name_route_editorial_v232.json"),
                                 Path("translations/confirmed_name_route_editorial_v234.json"),
                                 Path("translations/confirmed_name_route_editorial_v236.json")]
    additional_override_sources = {}
    for additional_path in additional_override_paths:
        if not additional_path.is_file():
            continue
        additional = json.loads(additional_path.read_text(encoding="utf-8"))
        for row in additional["records"]:
            key = row["file_path"], row["id"]
            if key in overrides:
                raise ValueError("Duplicate separately reviewed editorial override")
            overrides[key] = row
            additional_override_sources[key] = additional_path.as_posix()
    checks, drafts, profiles = [], [], {}
    for (path, record_id), (batch_path, batch, old_row) in sorted(effective.items()):
        old_text = old_row["english"]
        if not OLD.search(old_text) and not macro_affected(path, old_text) and (path, record_id) not in overrides:
            continue
        old_source = source_rows[path][record_id]
        jp_source = japanese_rows[path].get(record_id)
        english = paragraph(renamed(old_text))
        authored = copy.deepcopy(old_row)
        authored.update({"id": record_id, "file_path": path, "english": english,
                         "original_english": old_text, "original_batch": batch_path,
                         "source_hex": old_source["source_hex"],
                         "source_file_sha256": sha(originals[path]),
                         "japanese_source": jp_source["japanese"] if jp_source else None,
                         "canonical_baked_record": (path, record_id) not in active_ids,
                         "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
                         "status": "source-locked-migration-draft-not-registered",
                         "review": {gate: False for gate in ("source", "context", "localization", "naturalness", "formatting")}})
        authored.pop("manual_break_reason", None)
        for field in ("speaker", "context", "source_meaning", "localization_note"):
            if isinstance(authored.get(field), str):
                authored[field] = renamed(authored[field])
        if (path, record_id) in overrides:
            override = overrides[path, record_id]
            if old_source["source_hex"] != override["expected_source_hex"]:
                raise ValueError("Editorial correction's exact canonical/Japanese source differs")
            for field in ("english", "speaker", "context", "source_meaning", "localization_note"):
                authored[field] = override[field]
            english = authored["english"]
            authored["editorial_override"] = additional_override_sources.get((path, record_id), overrides_path.as_posix())
            if "clean_spoken_neighbors" in override:
                authored["clean_spoken_neighbors"] = override["clean_spoken_neighbors"]
            authored["review"] = dict(override["review"])
        if jp_source:
            ids = list(japanese_rows[path])
            at = ids.index(record_id)
            authored["Japanese_context_neighbors"] = [
                {"id": other, "japanese": japanese_rows[path][other]["japanese"]}
                for other in ids[max(0, at - 1):at + 2]]
        check = {"file_path": path, "id": record_id, "canonical_baked_record": authored["canonical_baked_record"],
                 "literal_name_changed": renamed(old_text) != old_text,
                 "default_macro_changed": bool(macro_affected(path, old_text))}
        if batch.get("encoder") == "dialogue-fixed-v1":
            profile = selected_profile(batch["dialogue_profile"], path)
            audit = audit_fixed_dialogue_record(bytes.fromhex(old_source["source_hex"]), english, profile)
            recovered = False
            if any(i["severity"] == "error" and "pair-phase-auto-wrap" in i["message"] for i in audit["issues"]):
                profile = replace(profile, name=profile.name + "-balanced", balanced_wrapping=True)
                audit = audit_fixed_dialogue_record(bytes.fromhex(old_source["source_hex"]), english, profile)
                recovered = not any(i["severity"] == "error" for i in audit["issues"])
            payload = asdict(profile)
            payload["leading_speaker_bytes"] = sorted(profile.leading_speaker_bytes)
            profiles[profile.name] = payload
            authored["proposed_profile"] = profile.name
            check.update({"audit": audit, "phase_auto_wrap_recovered_by_formatter": recovered,
                          "encoding_errors": [i for i in audit["issues"] if i["severity"] == "error"]})
        else:
            check["requires_native_common_help_review"] = True
        drafts.append(authored)
        checks.append(check)
    output = {"format": "dk4-confirmed-name-migration-preparation-v1", "not_a_release_batch": True,
              "policy_sha256": sha(policy_path.read_bytes()), "registry_sha256": sha(registry_path.read_bytes()),
              "editorial_override_sha256": sha(overrides_path.read_bytes()),
              "additional_editorial_override_sources": [{"path": path.as_posix(), "sha256": sha(path.read_bytes())}
                                                         for path in additional_override_paths if path.is_file()],
              "proposed_profiles_not_registered": profiles, "records": drafts,
              "baked_control_review_not_safe_to_author_yet": baked_control_review}
    (ROOT / "confirmed_source_locked_drafts.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    failures = [r for r in checks if r.get("encoding_errors")]
    report = {"format": "dk4-confirmed-name-text-preparation-report-v1", "checks": checks,
              "records": len(checks), "literal_name_records": sum(r["literal_name_changed"] for r in checks),
              "macro_dependent_records": sum(r["default_macro_changed"] for r in checks),
              "canonical_baked_records": sum(r["canonical_baked_record"] for r in checks),
              "encoding_failure_records": failures,
              "recovered_phase_auto_wrap_records": sum(r.get("phase_auto_wrap_recovered_by_formatter", False) for r in checks),
              "native_common_help_records_pending": sum(r.get("requires_native_common_help_review", False) for r in checks),
              "baked_control_review": baked_control_review,
              "baked_controls_using_existing_route_calibration": recovered_baked_controls,
              "complete_editorial_and_native_checks_pending": True, "playable_ROM_modified": False}
    (ROOT / "text_preparation_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("records", "literal_name_records", "macro_dependent_records", "canonical_baked_records",
                                           "recovered_phase_auto_wrap_records", "native_common_help_records_pending")} |
                     {"encoding_failures": len(failures), "playable_ROM_modified": False}))


if __name__ == "__main__":
    main()
