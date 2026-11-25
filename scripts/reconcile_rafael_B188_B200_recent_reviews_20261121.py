"""Bind recent whole-exchange town reviews to the current Rafael archive."""

from collections import Counter
from pathlib import Path

from scripts import pair_rafael_B181_B200_20261121 as paired


base, native = paired.pairing.base, paired.pairing.native
OUTPUT = paired.ROOT / "recent_town_review_reconciliation.json"
ARCHIVE = "/data/SC0.DK4"
GATES = {"source", "context", "localization", "naturalness", "formatting"}
RELEASES = ("sao_jorge_basra", "sofala_malacca_osaka", "seville_stockholm")
ASSETS = ("/__arm9__.bin", "/COMMON/MESFILE.DK4", "/GRP/KANJI.FNT")


def main():
    current, packet, manifest = map(base.load, (paired.parent.RELEASE, paired.PAIRED, paired.parent.MANIFEST))
    assert not OUTPUT.exists()
    assert base.digest(paired.parent.MANIFEST) == current["manifest_sha256"]
    assert base.digest(paired.parent.ROM) == current["candidate_sha256"] == packet["candidate_sha256"]
    assert packet["release_proof_sha256"] == base.digest(paired.parent.RELEASE)
    manifest_paths = {Path(path) for path in manifest["batches"]}
    image = base.NdsImage.open(paired.parent.ROM)
    assets = {path: native.digest(image.read_file(path)) for path in ASSETS}
    targets = {row["id"]: row for g in packet["groups"] if g["block"] >= 188 for row in g["records"]}
    evidence, matched = {}, []
    for name in RELEASES:
        root = Path(f"releases/all_routes_editorial_20261121_{name}_trends_candidate/verification")
        review, proof = root / "registered_review.json", root / "registered_release_verification.json"
        assert review in manifest_paths
        previous = base.load(proof)
        assert base.digest(previous["candidate"]) == previous["candidate_sha256"]
        assert base.digest(previous["manifest"]) == previous["manifest_sha256"]
        old = base.NdsImage.open(previous["candidate"])
        archive = native.IlnkContainer.parse(old.read_file(ARCHIVE)).blocks
        prior_assets = {path: native.digest(old.read_file(path)) for path in ASSETS}
        assert prior_assets[ASSETS[0]] == previous["target_ARM9_sha256"]
        assert prior_assets[ASSETS[1]] == previous["target_COMMON_sha256"]
        evidence[str(review)] = dict(sha256=base.digest(review), release=str(proof), release_sha256=base.digest(proof),
            prior_candidate_sha256=previous["candidate_sha256"], prior_assets=prior_assets,
            matching_asset_paths=[path for path in ASSETS if prior_assets[path] == assets[path]])
        for row in base.load(review)["records"]:
            ident = row["id"]
            if row["file_path"] != ARCHIVE or ident not in targets:
                continue
            target = targets[ident]
            assert target["block"] == row["block"]
            selector = bytes([target["selector"]])
            source, installed = [bytes.fromhex(target[side + "_reference"]["exact_body_hex"]) for side in ("source", "current")]
            registered = row["registered_reference"]
            assert bytes.fromhex(row["source_hex"]) == selector + source
            if bytes.fromhex(registered["exact_stored_hex"]) != selector + installed:
                continue
            assert registered["candidate_sha256"] == previous["candidate_sha256"]
            assert all(row["review"].get(gate) is True for gate in GATES)
            assert row["context"] and row["localization_note"]
            at = registered["offset"]
            assert archive[row["block"]][at:at + 1 + len(installed)] == selector + installed
            matched.append(dict(id=ident, block=row["block"], source_reference=target["source_reference"],
                current_reference=target["current_reference"], earlier_registered_reference=registered,
                review=str(review), decision=row["decision"], localization_note=row["localization_note"]))
    keys = {row["id"] for row in matched}
    assert len(matched) == len(keys) == 93
    counts = Counter(row["block"] for row in matched)
    assert counts == {188: 10, 191: 14, 195: 25, 196: 9, 197: 8, 199: 16, 200: 11}
    base.save(OUTPUT, dict(candidate_sha256=packet["candidate_sha256"], packet=str(paired.PAIRED),
        packet_sha256=base.digest(paired.PAIRED), current_assets=assets, evidence=evidence,
        identical_source_and_installed_recent_editorial_records=matched,
        more_recent_exact_review_not_located=[r["id"] for r in targets.values() if r["id"] not in keys],
        new_editorial_credit=0, fresh_gameplay=False, renderer_compatibility_pending=True))
    print("93 recent town decisions match the clean and current bytes. Renderer compatibility remains pending.")


if __name__ == "__main__":
    main()
