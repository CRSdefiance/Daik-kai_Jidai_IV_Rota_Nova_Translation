"""Bind Angelo's visited and conditional recruitment dialogue for the next editorial batch."""

from pathlib import Path

from scripts import cleanup_hodram_midroute_followups_20261123 as checkpoint
from scripts import pair_hodram_midroute_followups_20261123 as pairing
from scripts import register_hodram_midroute_followups_20261123 as release
from scripts import verify_shared_town_dialogue_20261123 as town

base, native, ARCHIVE = pairing.base, pairing.native, pairing.ARCHIVE
EARLIER = Path("releases/all_routes_editorial_20261122_hodram_B151_B160_candidate/verification/registered_review.json")
OUTPUT = town.OUTPUT.parent / "angelo_recruitment_paired.json"
OBSERVED = {
    "0058": (6350, "Told", "you I was strong!"),
    "0081": (7750, "There's something about", "this fellow."),
    "0101": (8750, "He's still green, and", "look how hard he pushed you."),
    "0112": (9350, "Well, if you feel", "that strongly, Hodram..."),
    "0175": (11550, "to Europe should bring", "in a fortune."),
}


def main():
    assert not OUTPUT.exists()
    active, earlier, queue, visits = map(base.load, (release.RELEASE, EARLIER, checkpoint.QUEUE, town.OUTPUT))
    candidate = base.digest(release.ROM)
    assert candidate == active["candidate_sha256"] == queue["candidate_sha256"] == visits["candidate_sha256"]
    assert base.digest(native.CLEAN) == active["clean_input_sha256"]
    assert base.digest(base.REGISTRY) == active["registry_sha256"]
    images = [base.NdsImage.open(path) for path in (native.CLEAN, release.ROM)]
    files = [image.read_file(ARCHIVE) for image in images]
    hashes = [native.digest(data) for data in files]
    assert hashes[1] == active["target_SC1_sha256"]
    arms = [image.read_file(native.ARM) for image in images]
    blocks = [native.IlnkContainer.parse(data).blocks for data in files]
    records = [record for record in earlier["records"] if record["block"] == 158]
    leads = {row["offset"]: row for row in queue["records"]
             if row["file_path"] == ARCHIVE and row["block"] == 158 and "reviewed" not in row}
    bound = pairing.binding["bind_block"](158, records, [bank[158] for bank in blocks], hashes, arms, leads)
    indexed = {row["id"].rsplit("_R", 1)[1]: row for row in bound["records"]}
    frames, _, _ = town.load_visit("athens", candidate)
    observations, pictures = [], []
    for ident, (frame, line_end, next_line) in OBSERVED.items():
        stored = indexed[ident]
        capture = frames[frame]
        picture = town.check.captured(capture).convert("RGB")
        assert line_end in stored["current_English"]
        assert next_line.replace("Hodram", "FI") in " ".join(stored["current_English"].split())
        observations.append(dict(id=stored["id"], current_offset=stored["current_offset"], capture=capture,
            shown_line_end=line_end, shown_next_line=next_line, decision_pending=True))
        pictures.append((f"Istanbul / SC1 B158 R{ident} / frame {frame}", picture))
    path, sha = town.visual.make_sheet(OUTPUT.parent / "istanbul_angelo_phrase_breaks.png", pictures)
    base.save(OUTPUT, dict(candidate_sha256=candidate, clean_sha256=active["clean_input_sha256"],
        source_review=dict(path=str(EARLIER), sha256=base.digest(EARLIER)), group=bound,
        ordinary_Istanbul_display_leads=observations, capture_sheet=dict(path=path, sha256=sha),
        conditional_Julio_dialogue_unvisited=True, new_editorial_credit=0))
    print(f"Bound {len(indexed)} recruitment records, including {len(observations)} observed phrase breaks.")


if __name__ == "__main__":
    main()
