"""Pair early Hodram exchanges and carry exact November editorial decisions."""

from collections import Counter
from pathlib import Path

from scripts.prepare_london_guild_assignments_20261118 import text_records
from scripts.reconcile_rafael_B188_B200_20261121 import reviewed_body
from scripts import register_rafael_B306_B309_20261122 as parent


base, native = parent.base, parent.native
ARCHIVE = "/data/SC1.DK4"
CENSUS = Path("work/Hodram_source_coverage_20261109_v2/coverage.json")
ROOT = Path("work/analysis/hodram_B24_B53_followup_20261122")
PACKET, CARRY = [ROOT / name for name in ("paired_source_registered_candidate.json", "prior_contextual_decisions.json")]
RANGE = range(24, 54)
TEXT_WORDS = (0x4000, 0x4100, 0x2100, 0x2200)
PACKAGES = (
    "20261121_hodram_alexandria_tutorial", "20261121_hodram_execution",
    "20261121_hodram_baltic_trade", "20261119_hodram_early_confrontations",
    "20261114_hodram_opening_wraps",
)


def source_and_current(build=parent, blocks=RANGE):
    release, census = map(base.load, (build.RELEASE, CENSUS))
    assert release["candidate_sha256"] == base.digest(build.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert release["clean_input_sha256"] == census["source_ROM_sha256"] == base.digest(native.CLEAN)
    assert not census["missing"] and not census["inventory_failures"] and not census["legacy_source_bindings_not_exact"]
    images = [base.NdsImage.open(path) for path in (native.CLEAN, build.ROM)]
    archives = [image.read_file(ARCHIVE) for image in images]
    hashes = list(map(native.digest, archives))
    assert hashes[0] == census["source_archive_sha256"]
    arms = [image.read_file(native.ARM) for image in images]
    assert native.digest(arms[1]) == release["target_ARM9_sha256"]
    assert native.digest(images[1].read_file("/COMMON/MESFILE.DK4")) == release["target_COMMON_sha256"]
    banks = [native.IlnkContainer.parse(archive).blocks for archive in archives]
    inventory, _, _ = native.scoped_inventory()
    refs = {(row["block"], row["source_reference"]["offset"]): row
            for row in census["records"] if row["block"] in blocks}
    groups = []
    for block in blocks:
        bodies = [bank[block] for bank in banks]
        block_hashes = list(map(native.digest, bodies))
        commands = [inventory(arm, body)[0] for arm, body in zip(arms, bodies, strict=True)]
        rows = []
        for original, current in zip(*commands, strict=True):
            word = original["word"]
            assert word == current["word"], (block, original["offset"])
            if word not in TEXT_WORDS:
                continue
            raw = [bytes.fromhex(row["whole_command_hex"]) for row in (original, current)]
            if word == 0x4000:
                assert raw[0][:6] == raw[1][:6]
            elif word == 0x4100:
                assert raw[0][:2] == raw[1][:2] and raw[0][18:20] == raw[1][18:20]
            for jp, en in zip(*(text_records(body, word) for body in raw), strict=True):
                offsets = original["offset"] + jp[0], current["offset"] + en[0]
                selector, slots = jp[1], jp[3]
                assert (selector, slots) == (en[1], en[3]), (block, offsets)
                old = refs.pop((block, offsets[0]))
                prefix = bytes([selector]) if word == 0x4000 else b""
                assert old["covered"] and old["source_hex"] == (prefix + jp[2]).hex()
                references = [dict(command_offset=cmd["offset"], offset=at, archive_sha256=archive_sha,
                                   block_sha256=block_sha, exact_body_hex=row[2].hex())
                              for cmd, at, archive_sha, block_sha, row in
                              zip((original, current), offsets, hashes, block_hashes, (jp, en), strict=True)]
                rows.append(dict(id=old["id"], block=block, file_path=ARCHIVE, selector=selector, slots=slots,
                                 native_command_word=word, Japanese=jp[2].decode("cp932"), current_English=en[2].decode("cp932"),
                                 source_reference=references[0], current_reference=references[1]))
        groups.append(dict(route=1, file_path=ARCHIVE, block=block, source_archive_sha256=hashes[0],
                           current_archive_sha256=hashes[1], source_block_sha256=block_hashes[0],
                           current_block_sha256=block_hashes[1], records=rows,
                           command_counts=dict(Counter(str(row["word"]) for row in commands[0]))))
    assert not refs
    return dict(candidate_sha256=release["candidate_sha256"], profile=release["profile"], release_proof=str(build.RELEASE),
                release_proof_sha256=base.digest(build.RELEASE), census=str(CENSUS), census_sha256=base.digest(CENSUS),
                clean_sha256=release["clean_input_sha256"], groups=groups, new_credit=0)


def prior_decisions(packet, packet_path=PACKET, packages=PACKAGES):
    evidence, sources = {}, {}
    for name in packages:
        folder = Path("releases") / f"all_routes_editorial_{name}_candidate/verification"
        review, ver = [folder / label for label in ("registered_review.json", "registered_release_verification.json")]
        doc, release = map(base.load, (review, ver))
        assert (doc.get("registered_candidate_sha256") or doc["candidate_sha256"]) == release["candidate_sha256"]
        sources[name] = {(r.get("block"), r["id"]): r for r in doc["records"] if r["file_path"] == ARCHIVE}
        evidence[name] = dict(review_path=str(review), review_sha256=base.digest(review), release_path=str(ver),
                              release_sha256=base.digest(ver), candidate_sha256=release["candidate_sha256"])

    reused, pending = [], []
    for group in packet["groups"]:
        for row in group["records"]:
            key = row["block"], row["id"]
            preamble = f"0040ffff00{row['selector']:02x}" if row["native_command_word"] == 0x4000 else None
            prefix = preamble[-2:] if preamble else ""
            jp, en = [prefix + row[side + "_reference"]["exact_body_hex"] for side in ("source", "current")]
            for name, records in sources.items():
                old = records.get(key)
                if not old or old.get("source_hex") != jp:
                    continue
                registered = old["registered_reference"]
                if reviewed_body(registered, preamble) != en:
                    continue
                assert registered["candidate_sha256"] == evidence[name]["candidate_sha256"] and all(old["review"].values())
                reused.append(row | dict(previous_release=name, previous_registered_reference=registered,
                    prior_review_gates=old["review"], prior_decision=old["decision"],
                    localization_note=old["localization_note"], source_meaning=old["source_meaning"], speaker=old["speaker"]))
                break
            else:
                pending.append(row)
    return dict(candidate_sha256=packet["candidate_sha256"], source_packet=str(packet_path), source_packet_sha256=base.digest(packet_path),
                reused_records=reused, pending_records=pending, evidence=evidence, new_editorial_credit=0, new_gameplay=False)


def main():
    assert not PACKET.exists() and not CARRY.exists()
    packet = source_and_current()
    ROOT.mkdir(exist_ok=True)
    base.save(PACKET, packet)
    carry = prior_decisions(packet)
    base.save(CARRY, carry)
    print("Early Hodram records", sum(len(group["records"]) for group in packet["groups"]))
    print("Exact previous decisions", dict(Counter(row["block"] for row in carry["reused_records"])))
    print("Pending decisions", dict(Counter(row["block"] for row in carry["pending_records"])))


if __name__ == "__main__":
    main()
