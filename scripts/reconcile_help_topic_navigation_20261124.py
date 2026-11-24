"""Join all installed Help pages to their source reviews and native navigation."""

from collections import Counter
from pathlib import Path
from struct import iter_unpack, unpack_from

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from dk4tool.dialogue.help_source_links import readable_source, source_links
from dk4tool.formats.ilnk import IlnkContainer

from scripts import register_claudio_opening_wrap_20261124 as current
from scripts.inventory_arm9_text import loaded_components
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write

HELP = "/COMMON/HELP.DK4"
BASE = 0x02000000
OUT = Path("translations/editorial_checkpoints/shared_display_20261123/help_topic_navigation_current_20261124.json")
REVIEWS = (
    "help_early23_contextual_final_review_v1",
    "help_town23_contextual_final_review_v2",
    "help_shipyard_sea59_integrated_final_review_v1",
    "Help97_Rafael330_integrated_final_review_v1",
)
AMENDMENTS = (
    "20261119_help_market_terms", "20261120_palace_help", "20261120_sailing_help",
    "20261120_tavern_help", "20261124_tavern_buy_a_round",
)
DIRECT = {
    0x0207C768: (0x020C7EDC,),
    0x0207D160: (0x0207C7A4,),
    0x0207D070: (0x0207C830, 0x0207C87C, 0x0207C8A8, 0x0207C8F4, 0x0207D248),
    0x0207CCA4: (0x0207C83C, 0x0207C888, 0x0207C8B4, 0x0207C900, 0x0207C93C, 0x0207D288),
}


def pages(image):
    data = image.read_file(HELP)
    assert data[:4] == b"ILNK"
    bank = IlnkContainer.parse(data)
    offsets = [unpack_from("<I", data, 8 + 4 * i)[0] for i in range(len(bank.blocks))]
    assert all(data[at:at + len(raw)] == raw for raw, at in zip(bank.blocks, offsets, strict=True))
    return data, bank.blocks, offsets


def entry(path, ref):
    return read(path), ref | reference(path)


def review_sources(original):
    topics, approved = {}, {}
    for name in REVIEWS:
        path = Path("translations") / (name + ".json")
        manifest, evidence = entry(path, dict(review_type="original five-gate Help decision"))
        for row in manifest["records"]:
            if row.get("file_path", HELP) != HELP or "topic_id" not in row:
                continue
            ident = row["topic_id"]
            assert set(row["review"]) == set(GATES) and all(row["review"].values()), ident
            assert bytes.fromhex(row["source_hex"]) == original[ident]
            topics[ident] = row | dict(review_evidence=evidence)
            for part in row["planned_stored_pages"]:
                key = part["block"]
                approved[key] = dict(owner=ident, expected_sha256=sha256(bytes.fromhex(part["exact_stored_hex"])).hexdigest(),
                    native_page_locator=dict(preview_sha256=part.get("native_preview_sha256"), source_page=part.get("source_page_proof")),
                    evidence=evidence)
    assert set(topics) == set(range(202)) and set(approved) == set(range(217)) - {203, 205}
    return topics, approved


def amendment_sources(original, topics, approved):
    for suffix in AMENDMENTS:
        root = Path("releases") / f"all_routes_editorial_{suffix}_candidate"
        checksums = read(root / "checksums.json")
        path = root / "verification/registered_review.json"
        assert digest(path) == checksums["verification/registered_review.json"]
        ledger, evidence = entry(path, dict(review_type="registered Help amendment"))
        for row in ledger["records"]:
            if row.get("file_path") != HELP:
                continue
            ident = row["topic_id"]
            assert set(row["review"]) == set(GATES) and all(row["review"].values())
            assert bytes.fromhex(row["clean_source_hex"]) == original[ident]
            ref = row["registered_reference"]
            topics[ident] = row | dict(review_evidence=evidence)
            approved[ident] = dict(owner=ident, expected_sha256=ref["block_sha256"], evidence=evidence)
        plan = root / "verification/plan.json"
        if plan.is_file():
            assert digest(plan) == checksums["verification/plan.json"]
            for row in read(plan).get("pages", []):
                key, owner = row["topic_id"], row["source_article_id"]
                if key < 202:
                    assert sha256(bytes.fromhex(row["encoded_hex"])).hexdigest() == approved[key]["expected_sha256"]
                    continue
                assert key not in (203, 205) and approved[key]["owner"] == owner
                approved[key] = dict(owner=owner, expected_sha256=sha256(bytes.fromhex(row["encoded_hex"])).hexdigest(),
                    evidence=evidence, continuation_layout=reference(plan))


def graph(blocks):
    found = [[link["topic_id"] for link in source_links(raw)] for raw in blocks]
    assert all(0 <= other < len(blocks) for links in found for other in links)
    seen, queue = set(), [0]
    while queue:
        ident = queue.pop()
        if ident not in seen:
            seen.add(ident)
            queue.extend(found[ident])
    return found, seen


def original_military_investment_display():
    package = Path("releases/all_routes_editorial_20261120_palace_help_candidate")
    name = "verification/ordinary_gameplay_verification.json"
    path = package / name
    proof = read(path)
    assert digest(path) == read(package / "checksums.json")[name]
    assert proof["actual_ordinary_controls_no_state_injection"]
    assert proof["all_selected_complete_actual_pages_andnative_child_targets_pass"]
    page, = [row for row in proof["actual_HELP_cases"] if row["topic_id"] == 204]
    assert page["source_article_id"] == 37
    return dict(source_article=37, displayed_continuation=204, earlier_ordinary_gameplay=reference(path),
                earlier_native_hold=page)


def bind_pages(current_pages, topics, approved):
    original, installed, offsets = current_pages
    source_graph, source_reachable = graph(original)
    live, reachable = graph(installed)
    assert source_reachable == set(range(202)) and reachable == set(range(217)) - {203, 205}
    assert installed[203] == b"\0"
    archived = readable_source(installed[205])
    assert archived.startswith("Military Investment (continued)")
    assert "lets you buy\nbetter ships and cannons" in readable_source(installed[204])
    assert "allows you to buy better ships and\ncannons." in archived
    rows = []
    for key, raw in enumerate(installed):
        incoming = [owner for owner, links in enumerate(live) if key in links]
        ref = dict(archive_offset=offsets[key], bytes=len(raw), sha256=sha256(raw).hexdigest(), exact_hex=raw.hex())
        if key in (203, 205):
            assert not incoming
            result = dict(page=key, installed=ref, incoming_links=incoming, outgoing_links=live[key],
                disposition="blank history sentinel" if key == 203 else "unlinked duplicate of the ending of article 37",
                reached_from_help_index=False, direct_opener_checked=False,
                current_text=archived if key == 205 else "")
            if key == 205:
                result["independent_display"] = original_military_investment_display()
                result["independent_display"]["current_approved_sha256"] = approved[204]["expected_sha256"]
            rows.append(result)
            continue
        sealed = approved[key]
        assert sealed["expected_sha256"] == ref["sha256"], (key, sealed["evidence"], ref["sha256"])
        owner = sealed["owner"]
        row = topics[owner]
        if key != owner:
            assert incoming == [owner] and live[key][-1] == owner
        rows.append(dict(page=key, source_article=owner, source_reference=row["source_reference"],
            source_block_sha256=sha256(original[owner]).hexdigest(), installed=ref, incoming_links=incoming,
            outgoing_links=live[key], original_review=row["review_evidence"], exact_layout_proof=sealed,
            decision=row["decision"], localization_note=row["localization_note"], review=row["review"]))
    for owner, original_links in enumerate(source_graph):
        parts = [r["page"] for r in rows if r.get("source_article") == owner]
        assert parts[0] == owner and len(parts) in (1, 2)
        logical = live[owner] if len(parts) == 1 else [*live[owner], *live[parts[1]][:-1]]
        assert Counter(link for link in logical if link < 202) == Counter(original_links), owner
    return rows, dict(original_links=sum(map(len, source_graph)), installed_links=sum(map(len, live)),
        original_articles_reachable=len(source_reachable), current_linked_pages=len(reachable),
        linked_continuations=len(reachable) - 202, no_inbound_link=[203, 205])


def references(image):
    calls, literals = [], []
    for name, base, raw in loaded_components(image):
        for i, (word,) in enumerate(iter_unpack("<I", raw[:len(raw) & ~3])):
            pc = base + 4 * i
            if word & ~1 in DIRECT:
                literals.append(dict(component=name, PC=pc, value=word))
            if word >> 28 == 15 or word & 0x0E000000 != 0x0A000000:
                continue
            rel = word & 0xFFFFFF
            if rel & 0x800000:
                rel -= 1 << 24
            target = pc + 8 + 4 * rel
            if target in DIRECT:
                calls.append(dict(component=name, PC=pc, target=target, exact_hex=raw[4 * i:4 * i + 4].hex()))
    return calls, literals


def native_scope(clean, image):
    calls, literals = references(clean)
    assert (calls, literals) == references(image) and not literals
    assert all(row["component"] == "arm9_section_0" for row in calls)
    actual = {target: tuple(row["PC"] for row in calls if row["target"] == target) for target in DIRECT}
    assert actual == DIRECT
    before, after = (rom.read_file(current.ARM) for rom in (clean, image))
    engine = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    spans = {}
    for low, high in ((0x020C7EB8, 0x020C7EE4), (0x0207C768, 0x0207C960),
                      (0x0207CCA4, 0x0207CCDC), (0x0207D070, 0x0207D114), (0x0207D160, 0x0207D3F8)):
        selected = after[low - BASE:high - BASE]
        assert before[low - BASE:high - BASE] == selected
        spans[low] = dict(end=high, exact_hex=selected.hex(),
            instructions=[dict(pc=ins.address, mnemonic=ins.mnemonic, operands=ins.op_str)
                          for ins in engine.disasm(selected, low)])
    return dict(aligned_ARM_calls=calls, aligned_literal_references=literals, same_clean_and_installed_code=spans,
        index_and_history_bound=True,
        scope="The opener at 0x020C7EDC receives the virtual +0x8C topic result. That indirect input is outside the index hyperlink traversal. The five native history callers handle direct entry, index, link, bookmark, or history values.",
        exhaustive_dynamic_virtual_input_proof=False)


def main():
    release = read(current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(current.ROM) == release["candidate_sha256"]
    clean, image = map(NdsImage.open, (CLEAN, current.ROM))
    original, clean_blocks, _ = pages(clean)
    archive, installed, offsets = pages(image)
    assert sha256(archive).hexdigest() == release["target_HELP_sha256"]
    assert len(clean_blocks) == 202 and len(installed) == 217
    topics, approved = review_sources(clean_blocks)
    amendment_sources(clean_blocks, topics, approved)
    records, structure = bind_pages((clean_blocks, installed, offsets), topics, approved)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], release=reference(current.RELEASE),
        source_archive_sha256=sha256(original).hexdigest(), current_archive_sha256=sha256(archive).hexdigest(),
        records=records, link_structure=structure, direct_opener_scope=native_scope(clean, image),
        ROM_changed=False, new_editorial_credit=0, new_gameplay_runs=0, legacy_205_outside_index_path=True,
        remaining_direct_virtual_topic_scope=True))
    print(f"Verified {structure['current_linked_pages']} exact reachable Help pages and all {structure['original_links']} original article links.")


if __name__ == "__main__":
    main()
