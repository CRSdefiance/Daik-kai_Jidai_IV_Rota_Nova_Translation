"""Bind the original nine phrase fixes and two Rafael priorities to the current release."""

from pathlib import Path

from scripts import checkpoint_story_glyph_consistency_20261115 as glyph
from scripts import register_save_location_labels_20261119 as current
from scripts import register_story_phrase_wraps_20261118 as original

base, native = original.base, original.native
OUTPUT = glyph.OUTPUT.with_name("flagged_phrase_and_julio_20261119_v1.json")
QUEUE = current.stage.ROOT / "followup_wrap_queue.json"
EARLY = "rafael_early_phrase_wraps"
FINAL = "lil_maria_flagged_wraps"
REFINEMENTS = {
    (2, 213): FINAL,
    (3, 53): "continuing_phrase_wraps",
    (3, 54): "continuing_phrase_wraps",
    (3, 130): "next_review_wraps",
}
PHRASES = {
    (0, 48): "Proof of Conquest",
    (0, 79): "Proof of Conquest",
    (1, 81): "Indian Ocean",
    (1, 146): "Indian Ocean",
    (2, 213): "Shandong Peninsula",
    (3, 53): "Proof of Conquest",
    (3, 54): "Proof of Conquest",
    (3, 112): "Southeast Asia",
    (3, 130): "trade house",
}


def package(name, receipt):
    return Path(f"releases/all_routes_editorial_20261118_{name}_candidate/verification") / receipt


def speech(arm, block, inventory, field, value):
    commands, strings = native.raw_speeches(arm, block, inventory)
    row, = (row for row in native.references(commands, strings) if row[field] == value)
    return row | dict(block_sha256=native.digest(block))


def find_review(path, record_id):
    row, = (row for row in base.load(path)["records"] if row["id"] == record_id)
    return row


def bind_phrase(row, proof, source, installed, phrase, historical=None):
    stored = row["registered_reference"]
    assert source["raw_hex"] == row["source_hex"], row["id"]
    assert source["complete_preamble_hex"] == installed["complete_preamble_hex"]
    assert installed["raw_hex"] == (stored.get("exact_stored_hex") or stored["raw_hex"]), row["id"]
    assert installed["command_offset"] == stored["command_offset"]
    assert all(row["review"][gate] for gate in native.GATES)
    lines = bytes.fromhex(installed["raw_hex"])[1:].decode("cp932").splitlines()
    assert any(phrase.casefold() in line.casefold() for line in lines), (row["id"], lines)
    return dict(file_path=stored.get("file_path", row.get("file_path")), block=row["block"], id=row["id"],
                source_reference=source, current_reference=installed, wrapped_lines=lines, intact_phrase=phrase,
                historical_reference=historical, review_reference=dict(path=proof.as_posix(), sha256=base.digest(proof)),
                review=row["review"], localization_note=row["localization_note"])


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release["candidate_sha256"]
    assert base.digest(current.stage.CLEAN) == release["clean_input_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    final_release = package(FINAL, "registered_release_verification.json")
    final = base.load(final_release)
    ja, en = (base.NdsImage.open(p) for p in (current.stage.CLEAN, current.ROM))
    clean_arm, arm = (i.read_file(current.stage.ARM) for i in (ja, en))
    inventory, _, _ = native.scoped_inventory()
    routes = {}
    hashes = {}
    for route in range(4):
        path = f"/data/SC{route}.DK4"
        clean_archive, archive = (i.read_file(path) for i in (ja, en))
        sha = native.digest(archive)
        assert sha == release[f"target_SC{route}_sha256"] == final[f"target_SC{route}_sha256"]
        hashes[path] = sha
        routes[route] = tuple(native.IlnkContainer.parse(x).blocks for x in (clean_archive, archive))

    def records(route, block, index, offset):
        source, installed = (blocks[block] for blocks in routes[route])
        return (speech(clean_arm, source, inventory, "record_index", index),
                speech(arm, installed, inventory, "offset", offset))

    findings = []
    for prior in base.load(original.REVIEW)["records"]:
        if prior["decision"] == "retention":
            continue
        route, block = prior["route"], prior["block"]
        key = route, block
        proof = (package(REFINEMENTS[key], "registered_review.json") if key in REFINEMENTS else original.REVIEW)
        row = find_review(proof, prior["id"])
        source, installed = records(route, block, prior["source_reference"]["record_index"],
                                    row["registered_reference"]["offset"])
        history = prior["registered_reference"] if key in REFINEMENTS else None
        findings.append(bind_phrase(row, proof, source, installed, PHRASES[key], history))
    assert len(findings) == 9 and sum(r["historical_reference"] is not None for r in findings) == 4

    proof = package(EARLY, "registered_review.json")
    reveal = find_review(proof, "DK4_MES_B0_R0005")
    source, installed = records(0, 0, 5, reveal["registered_reference"]["offset"])
    reveal = bind_phrase(reveal, proof, source, installed, "Africa's Proof of Conquest")

    previous = base.load(glyph.OUTPUT)
    prior_julio = previous["julio_tutorial"]
    row, = (r for r in prior_julio["exchange_context"] if r["selected"])
    source, installed = records(0, 43, row["source"]["record_index"], row["current"]["offset"])
    assert source["raw_hex"] == row["source"]["raw_hex"]
    assert installed["raw_hex"] == row["current"]["raw_hex"]
    payload = bytes.fromhex(installed["raw_hex"])
    assert payload[:2] == b"\x06F" and payload[1:].isascii() and payload.count(b"FI") == 1
    lookups = glyph.lookup_cases(arm, previous["catalogue"], payload)
    assert lookups == prior_julio["lookups"] and len(lookups) == 12
    pixels, events, font = glyph.raster(arm, payload[1:].replace(b"FI", b"Rafael"))
    assert pixels == glyph.independent_pixels(arm, font, events)
    assert glyph.digest(pixels) == prior_julio["native_pixels_sha256"]
    assert events[0]["code"] == ord("F") and all(e["kind"] == "ascii" for e in events)
    assert len({e["y"] for e in events}) == 4
    julio = dict(file_path=prior_julio["file"], block=43, source_reference=source, current_reference=installed,
                 full_font_plane_exact=True, first_glyph="F", name_substitution="FI",
                 offline_supplied_name="Rafael", original_lookup_cases=lookups,
                 earlier_emulator_replay=prior_julio["earlier_initialized_gameplay"])
    queue = base.load(QUEUE)
    assert queue["candidate_sha256"] == release["candidate_sha256"]
    assert queue["counts"]["open editorial lead"] == queue["stored_bad_title_patterns"] == 0
    base.save(OUTPUT, dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        current_archive_hashes=hashes, original_flagged_phrase_breaks=findings, early_rafael_reveal=reveal,
        julio_tutorial=julio, wrap_queue_counts=queue["counts"], new_gameplay_runs=0, new_editorial_credit=0,
        evidence={p.as_posix(): base.digest(p) for p in (Path(__file__), final_release, current.RELEASE,
                                                        original.REVIEW, QUEUE, glyph.OUTPUT)}))
    print("All nine flagged phrases, Rafael's reveal, and Julio's tutorial glyph match the current release.")


if __name__ == "__main__":
    main()
