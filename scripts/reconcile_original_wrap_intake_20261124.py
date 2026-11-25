"""Trace the 277 original wrap leads into their registered decisions."""

from collections import defaultdict
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from scripts import reconcile_original_story_packets_20261124 as packets
from scripts.stage_cartridge_title_20261123 import GATES, NdsImage, digest, read, reference, sha256, write

INTAKE = packets.INTAKE / "current_wrap_queue.json"
BASE = Path("releases/all_routes_editorial_20261122_palace_eirene_pereira_london_candidate/verification/registered_release_verification.json")
OUT = packets.OUT.with_name("original_wrap_intake_current_20261124.json")
STORIES = tuple(f"/data/SC{i}.DK4" for i in range(4))


def files(image):
    return {path: IlnkContainer.parse(image.read_file(path)).blocks for path in STORIES}


def exact_entry(row, side):
    ref = row.get(f"{side}_reference", {})
    text = ref.get("exact_command_hex", ref.get("complete_command_hex", row.get(f"{side}_command_hex")))
    offset = ref.get("command_offset", row.get(f"{side}_command_offset"))
    return ref, offset, bytes.fromhex(text) if text else b""


def keys_from_successors(manifest, start):
    index = defaultdict(list)
    approved = defaultdict(list)
    evidence = {}
    for raw in manifest[start:]:
        path = Path(raw)
        assert path.name == "registered_review.json"
        sums = read(path.parent.parent / "checksums.json")
        assert digest(path) == sums["verification/registered_review.json"]
        review = read(path)
        for row in review["records"]:
            route, block = row.get("file_path"), row.get("block")
            if route not in STORIES or not isinstance(block, int):
                continue
            if set(row["review"]) != set(GATES) or not all(row["review"].values()):
                continue
            old_ref, at, old = exact_entry(row, "current")
            installed_ref, installed_at, installed = exact_entry(row, "registered")
            ident = (route, block, row["id"])
            if installed and isinstance(installed_at, int):
                approved[ident].append((path, row, installed_ref, installed_at, installed))
            if old[:2] != b"\0\x40" or not isinstance(at, int) or len(old) < 7:
                continue
            terminator = old.find(b"\0", 6)
            if terminator == -1:
                continue
            visible_command = old[:terminator + 1]
            index[route, block, at + 5, visible_command].append((path, row, old_ref, old))
            evidence[str(path)] = sums["verification/registered_review.json"]
    return index, approved, evidence


def reconcile(initial, final, old_flags, earlier, manifest):
    index, approved, evidence = keys_from_successors(manifest, len(earlier))
    results, unresolved = [], []
    for flag in old_flags:
        asset, block, at = (flag[k] for k in ("file_path", "block", "offset"))
        native = bytes.fromhex(flag["native_preamble_hex"] + flag["stored_body_hex"] + "00")
        assert flag["native_preamble_hex"].endswith(f"{flag['source_selector']:02x}")
        assert sha256(initial[asset][block]).hexdigest() == flag["block_sha256"]
        assert initial[asset][block][at - 5:at - 5 + len(native)] == native
        head = []
        for path, row, lock, whole in index[asset, block, at, native]:
            # B84 gives the pre-edit command directly in its paired-source row.
            same_hash = lock.get("block_sha256") == flag["block_sha256"]
            b84 = (asset, block) == ("/data/SC0.DK4", 84) and "current_command_hex" in row
            if same_hash or b84:
                assert initial[asset][block][at - 5:at - 5 + len(whole)] == whole
                head.append((path, row))
        owners = {row["id"] for _, row in head}
        if len(owners) != 1:
            unresolved.append(dict(flag=flag, possible_owners=sorted(owners)))
            continue
        approved_intake, row = head[0]
        ident = (asset, block, row["id"])
        actual = final[asset][block]
        block_hash = sha256(actual).hexdigest()
        current_ref = None
        for path, last, ref, at_final, stored in reversed(approved[ident]):
            if ref.get("block_sha256") == block_hash:
                assert actual[at_final:at_final + len(stored)] == stored
                basis = "registered exact block and command offset"
            elif actual.count(stored) == 1:
                at_final = actual.index(stored)
                basis = "unique exact reviewed command in the same final story block"
            else:
                continue
            current_ref = dict(review_path=path.as_posix(), command_offset=at_final,
                exact_command_hex=stored.hex(), block_sha256=block_hash, decision=last["decision"], basis=basis)
            break
        if current_ref:
            results.append(dict(intake=flag, id=row["id"], first_review_path=approved_intake.as_posix(),
                first_decision=row["decision"], reason=row["localization_note"], installed=current_ref))
        else:
            unresolved.append(dict(flag=flag, possible_owners=sorted(owners), original_review=approved_intake.as_posix()))
    assert len(results) + len(unresolved) == len(old_flags) == 277
    return results, unresolved, evidence


def main():
    source, release, queue = map(read, (BASE, packets.current.current.RELEASE, INTAKE))
    assert digest(source["candidate"]) == source["candidate_sha256"] == queue["candidate_sha256"]
    current_receipt = read(packets.current.OUT)
    assert digest(release["candidate"]) == release["candidate_sha256"] == current_receipt["candidate_sha256"]
    assert digest(source["manifest"]) == source["manifest_sha256"] and digest(release["manifest"]) == release["manifest_sha256"]
    earlier, current = [read(r["manifest"])["batches"] for r in (source, release)]
    assert current[:len(earlier)] == earlier and len(current) == 1142 and len(earlier) == 1065
    initial, final = [files(NdsImage.open(r["candidate"])) for r in (source, release)]
    open_flags = [r for r in queue["records"] if "reviewed" not in r]
    assert len(queue["records"]) == 308
    reviews, unresolved, hashes = reconcile(initial, final, open_flags, earlier, current)
    prepared = read(packets.OUT)
    assert prepared["candidate_sha256"] == release["candidate_sha256"] and prepared["prepared_story_texts"] == 521
    packet_positions = {(p["asset"], p["block"], item["id"]) for p in prepared["packets"] for item in p["exact_texts"]}
    wrap_positions = {(item["intake"]["file_path"], item["intake"]["block"], item["id"]) for item in reviews}
    assert len(wrap_positions) == len(reviews)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], starting_queue=reference(INTAKE),
        starting_release=reference(BASE), exact_manifest_prefix=len(earlier), successors_checked=len(current) - len(earlier),
        original_open_count=len(open_flags), latest_scan_reviewed_flags=len(current_receipt["coverage"]["bound_story_wrap_dispositions"]),
        latest_scan_open_flags=current_receipt["coverage"]["current_open_story_wrap_flags"],
        prepared_packet_overlap=len(wrap_positions & packet_positions), prepared_packet_receipt=reference(packets.OUT),
        linked=reviews, unresolved=unresolved, verified_review_hashes=hashes, ordinary_gameplay_added=False))
    print(f"Linked {len(reviews)} of the original 277 wrap leads to exact current decisions, with {len(unresolved)} pending links.")


if __name__ == "__main__":
    main()
