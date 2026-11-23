"""Rebind the earlier contextual town decisions to the current registered ROM."""

from collections import Counter
from pathlib import Path

from scripts import pair_rafael_B181_B200_20261121 as pairing
from scripts import register_rafael_B181_B187_20261121 as current


ROOT = pairing.ROOT
OUTPUT = ROOT / "town_contextual_reconciliation_B188_B200_v2.json"
ASSETS = ("/__arm9__.bin", "/COMMON/MESFILE.DK4", "/GRP/KANJI.FNT")
RELEASES = (
    "20261121_alexandria_dialogue",
    "20261121_athens_london_trends",
    "20261121_lisbon_fragrance_wraps",
    "20261121_sao_jorge_basra_trends",
    "20261121_seville_stockholm_trends",
    "20261121_sofala_malacca_osaka_trends",
    "20261121_hangzhou_veracruz_trends",
    "20261121_havana_calicut_istanbul_trends",
    "20261120_genoa_tomatoes",
    "20261115_town_trend_exchanges",
)


def reviewed_body(reference, preamble):
    if not preamble:
        return reference.get("exact_stored_hex") or reference.get("raw_hex")
    if command := reference.get("exact_command_hex") or reference.get("complete_command_hex"):
        raw = bytes.fromhex(command)
        assert raw[:6].hex() == preamble and raw.endswith(b"\0")
        return raw[5:].rstrip(b"\0").hex()
    return reference.get("exact_stored_hex") or reference["raw_hex"]


def reconcile(packet_path, output, wanted_blocks, packages, previous, current=current):
    base, native = current.base, current.native
    release = base.load(current.RELEASE)
    packet = base.load(packet_path)
    assert base.digest(current.ROM) == release["candidate_sha256"]
    assert base.digest(previous.ROM) == packet["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    prior, installed = [base.NdsImage.open(build) for build in (previous.ROM, current.ROM)]
    assets = {path: native.digest(installed.read_file(path)) for path in ASSETS}
    assert all(native.digest(prior.read_file(path)) == h for path, h in assets.items())
    archive = "/data/SC0.DK4"
    old_archive, current_archive = [image.read_file(archive) for image in (prior, installed)]
    old_bank, new_bank = [native.IlnkContainer.parse(raw).blocks for raw in (old_archive, current_archive)]
    packets = {}
    for name in packages:
        folder = Path("releases") / f"all_routes_editorial_{name}_candidate" / "verification"
        review_path, proof_path = [folder / f"registered_{label}.json" for label in ("review", "release_verification")]
        review, proof = map(base.load, (review_path, proof_path))
        assert (review.get("registered_candidate_sha256") or review["candidate_sha256"]) == proof["candidate_sha256"]
        records = {(r["file_path"], r.get("block"), r["id"]): r for r in review["records"]}
        packets[name] = (records, dict(
            review_path=str(review_path), review_sha256=base.digest(review_path),
            release_proof=str(proof_path), release_proof_sha256=base.digest(proof_path),
            candidate_sha256=proof["candidate_sha256"],
            target_ARM9_sha256=proof["target_ARM9_sha256"], target_COMMON_sha256=proof["target_COMMON_sha256"]))

    reused, pending = [], []
    for group in packet["groups"]:
        block = group["block"]
        if block not in wanted_blocks:
            continue
        assert old_bank[block] == new_bank[block]
        assert native.digest(new_bank[block]) == group["current_block_sha256"]
        for row in group["records"]:
            ident = row["id"]
            word = row.get("native_command_word", 0x4000)
            reference = dict(row["current_reference"], archive_sha256=native.digest(current_archive))
            begin = reference["command_offset"]
            jp, en = row["source_reference"]["exact_body_hex"], reference["exact_body_hex"]
            if word in (0x4100, 0x2100, 0x2200):
                preamble = None
                assert new_bank[block][begin:begin + 2] == word.to_bytes(2, "little")
                at = reference["offset"]
                body = bytes.fromhex(en)
                assert new_bank[block][at:at + len(body) + 1] == body + b"\0"
                assert row["slots"]
            else:
                assert word == 0x4000
                preamble = row.get("complete_preamble_hex") or f"0040ffff00{row['selector']:02x}"
                jp, en = preamble[-2:] + jp, preamble[-2:] + en
                assert new_bank[block][begin:begin + 5 + len(bytes.fromhex(en))].hex() == preamble[:10] + en
            pair = dict(id=ident, block=block, file_path=archive, source_reference=row["source_reference"],
                        current_reference=reference, complete_preamble_hex=preamble)
            if word != 0x4000:
                pair.update(native_command_word=word, native_slots=row["slots"])
            for name, (records, proof) in packets.items():
                prior_row = records.get((archive, block, ident))
                if not prior_row or prior_row["source_hex"] != jp:
                    continue
                registered = prior_row["registered_reference"]
                if reviewed_body(registered, preamble) != en:
                    continue
                assert registered["candidate_sha256"] == proof["candidate_sha256"]
                gates = prior_row["review"]
                assert all(gates[k] is True for k in ("source", "context", "localization", "naturalness", "formatting"))
                reused.append(pair | dict(previous_release=name, decision=prior_row["decision"],
                    speaker=prior_row["speaker"], finding=prior_row.get("finding"), source_meaning=prior_row["source_meaning"],
                    context=prior_row["context"], localization_note=prior_row["localization_note"],
                    reviewed_english=prior_row["english"], previous_registered_reference=registered,
                    prior_review_gates=gates, editorial_decision_carried=True,
                    prior_render_dependencies_match=(proof["target_ARM9_sha256"] == assets[ASSETS[0]]
                                                    and proof["target_COMMON_sha256"] == assets[ASSETS[1]])))
                break
            else:
                pending.append(pair | dict(Japanese=row["Japanese"], current_English=row["current_English"]))
    count = sum(len(g["records"]) for g in packet["groups"] if g["block"] in wanted_blocks)
    assert len(reused) + len(pending) == count
    used = {row["previous_release"] for row in reused}
    base.save(output, dict(candidate_sha256=release["candidate_sha256"], assets=assets,
        source_packet=str(packet_path), source_packet_sha256=base.digest(packet_path),
        prior_build=packet["candidate_sha256"], town_blocks_byte_exact=True,
        relevant_assets_unchanged_since_prior_build=True, total_records=count,
        source_current_exact_count=len(reused), counts_per_block=dict(Counter(r["block"] for r in reused)),
        evidence={name: proof for name, (_, proof) in packets.items() if name in used},
        reused_records=reused, pending_records=pending, new_editorial_credit=0,
        prior_gameplay_is_historical=True))
    print(f"Rebound {len(reused)} prior contextual decisions to exact installed records. {len(pending)} pending.")


if __name__ == "__main__":
    reconcile(pairing.PAIRED, OUTPUT, range(188, 201), RELEASES, pairing.parent)
