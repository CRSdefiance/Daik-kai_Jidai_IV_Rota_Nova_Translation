"""Reconstruct the first ordinary post-load fleet and headquarters state."""

from collections import Counter

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

from scripts import check_fleet_special_neighbor_centers_20261124 as special
from scripts import observe_postload_fleet_fields_20261124 as play
from scripts import reconcile_fleet_destination_lists_20261123 as lists
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


OUT = play.verified.OUT.with_name("fleet_postload_writes_20261124.json")
BASE = play.BASE
CURRENT = play.battery.current
DESTINATION_STORE, DOCKING_STORE = 0x02035A28, 0x020347A4
BACKGROUND_ORDER_CALL, BACKGROUND_ORDER_RETURN = 0x0202F07C, 0x0202F080


def bind_capture(release, earlier):
    root = play.ROOT / "copenhagen"
    paths = [root / name for name in ("capture/capture_report.json", "requests.json", "terminal.json", "source_contract.json")]
    cap, trace, terminal, contract = map(read, paths)
    inputs, holds, end, _, donor = play.battery.schedule("copenhagen")
    assert cap["ROM_sha256"] == terminal["ROM_sha256"] == release["candidate_sha256"]
    assert cap["cold_boot"] and not cap["savestate_loaded"] and not cap["callback_errors"]
    assert not any(v for k, v in cap.items() if k.startswith("synthetic_"))
    assert cap["scripted_input_schedule"] == inputs and cap["frames"] == terminal["completed_frames"] == end
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert trace["source_contract_sha256"] == digest(paths[-1]) and contract["ARM9_sha256"] == release["target_ARM9_sha256"]
    assert all(digest(path) == value for path, value in terminal["evidence"].items())
    save = cap["battery_save_preloaded"]
    assert save["copied_byte_exact_before_cold_boot"] and digest(save["source"]) == save["source_sha256"] == donor["source_sha256"]
    assert reference(donor["source"]) == earlier["pristine_donor"]
    snapshot, = cap["read_only_capture_RAM_snapshots"]
    assert (snapshot["frame"],) == holds
    same_hold = earlier["restored_graphics_hold"]
    assert sha256(lists.prior.read_ram(same_hold)).hexdigest() == snapshot["sha256"]
    return trace, terminal, contract, snapshot, list(map(reference, paths))


def reconstruct(saved, trace, terminal, snapshot, prior_docking):
    rows = trace["rows"]
    assert rows == terminal["caption_calls"] and not trace["source_requests"]
    initial = {row["live_address"]: row for row in saved["all_read_fields"]}
    values = {loc: row["saved"] for loc, row in initial.items()}
    assert len(values) == 146
    for row in rows:
        loc = row["address"]
        assert row["frame"] >= max(saved["restore_frames"]) and row["frame"] <= snapshot["frame"]
        assert (row["field"], row["index"]) == (initial[loc]["field"], initial[loc]["index"])
        assert values[loc] == row["before"] and 0 <= row["value"] < 90
        values[loc] = row["value"]
    assert len(rows) == 51
    counts = Counter((row["PC"], row["field"]) for row in rows)
    assert counts == {(DOCKING_STORE, "docking"): 21, (DESTINATION_STORE, "destination"): 30}
    destinations = [row for row in rows if row["PC"] == DESTINATION_STORE]
    assert all(row["LR"] == BACKGROUND_ORDER_RETURN for row in destinations)
    observed_docks = [dict(frame=row["frame"], PC=row["PC"], LR=row["LR"], fleet=row["address"] - 0x3C,
                          before=row["before"], town=row["value"]) for row in rows if row["PC"] == DOCKING_STORE]
    assert observed_docks == prior_docking["other_fleet_docking_stores"]
    raw = lists.prior.read_ram(snapshot)
    assert all(raw[loc - BASE] == value for loc, value in values.items())
    changed = Counter(row["field"] for loc, row in initial.items() if values[loc] != row["saved"])
    assert sum(changed.values()) == 45
    return raw, dict(total_writes=len(rows), docking_writes=len(observed_docks), destination_writes=len(destinations),
                     final_bytes_reconstructed=len(values), changed_fields=dict(changed), all_observed_writes=rows)


def extend_port_list_evidence(arm, raw):
    earlier, hidden, sentinel = map(read, (lists.OUT, special.docking.OUT, special.OUT))
    _, graph = lists.port_graph(raw)
    assert all(graph[field] == earlier["initialized_port_graph"][field]
               for field in ("edge_bytes_sha256", "exact_neighbor_rows_hex"))
    graph_sha = graph["edge_bytes_sha256"]
    assert all(row["port_graph_sha256"] == graph_sha for row in sentinel["states"])
    for row in earlier["matched_clean_installed_and_resident_ranges"]:
        start, end = row["address"], row["end"]
        assert lists.prior.code_at(arm, start, end) == lists.prior.code_at(raw, start, end) == bytes.fromhex(row["exact_hex"])
    for row in sentinel["checked_code_spans"]:
        start, end = row["start"], row["end"]
        value = lists.prior.code_at(arm, start, end)
        assert value == lists.prior.code_at(raw, start, end) and sha256(value).hexdigest() == row["sha256"]
    base = lists.NEIGHBORS + 8
    hidden_data = lists.prior.code_at(raw, base + 90 * 7, base + 114 * 7)
    assert hidden_data == bytes(24 * 7)
    assert all(row["exact_hidden_rows"] == hidden_data.hex() and row["indices"] == [90, 113]
               for row in hidden["hidden_port_neighbor_checks"])
    for center, expected in ((114, []), (115, [0, 0, 0, 3])):
        row = next(r for r in sentinel["states"][0]["tests"] if r["center"] == center and r["function"] == special.NEIGHBOR_GETTER)
        at = base + center * 7
        assert lists.prior.code_at(raw, at, at + 7).hex() == row["bytes_read"] and row["output_ports"] == expected
    envelopes = {row["call"]: row["possible_port_slots"] for row in earlier["conditional_list_writer_sites"]}
    assert envelopes == {pc: [0, 113 if pc == BACKGROUND_ORDER_CALL else 89] for pc in lists.LIST_SITES}
    return dict(graph_sha256=graph_sha, qualified_center_range=[0, 115], earlier_list_outputs=envelopes,
        previously_checked_special_centers={114: [], 115: [0, 0, 0, 3]},
        evidence=list(map(reference, (lists.OUT, special.docking.OUT, special.OUT))),
        scope="Earlier selector and filter code matches the live copy. Neighbor centers 90–114 yield no candidate, and 115 adds only ports 0 and 3. This extends those seven list-result bounds in this initialized graph. Headquarters and docking fields fed directly to other writers have distinct provenance.")


def main():
    release, before, prior_docking = map(read, (CURRENT.RELEASE, play.verified.OUT, play.verified.docking.OUT))
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(CURRENT.ROM) == release["candidate_sha256"] == before["candidate_sha256"]
    history = {row["case"]: row for row in before["ordinary_restores"]}
    trace, terminal, contract, snapshot, bindings = bind_capture(release, history["copenhagen"])
    clean, image = map(NdsImage.open, (CLEAN, CURRENT.ROM))
    stock, active = play.sites(clean), play.sites(image)
    assert stock == active == {row["PC"]: row["word"] for row in contract["targets"]} and len(stock) == 37
    arm = image.read_file(CURRENT.ARM)
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    site_bytes = lists.prior.code_at(arm, BACKGROUND_ORDER_CALL - 12, BACKGROUND_ORDER_RETURN)
    assert [(i.mnemonic, i.op_str) for i in md.disasm(site_bytes, BACKGROUND_ORDER_CALL - 12)] == [
        ("ldr", "r0, [sp, #8]"), ("mov", "r2, r4"), ("ldrb", "r1, [r0, #0x3e]"), ("bl", "#0x2035a24")]
    raw, replay = reconstruct(history["copenhagen"], trace, terminal, snapshot, prior_docking)
    immediate = lists.prior.read_ram(history["nagasaki"]["restored_graphics_hold"])
    nagasaki = history["nagasaki"]["all_read_fields"]
    assert len(nagasaki) == 146 and all(immediate[row["live_address"] - BASE] == row["saved"] for row in nagasaki)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], ordinary_gameplay=True,
        copenhagen_postload=replay, nagasaki_first_town_matching_save_fields=len(nagasaki),
        copenhagen_snapshot=snapshot, bound_ordinary_docking=reference(play.verified.docking.OUT),
        original_background_order_call=dict(PC=BACKGROUND_ORDER_CALL, bytes=site_bytes.hex()),
        selector_results=extend_port_list_evidence(arm, raw),
        stock_candidate_store_sites=dict(scope="ARM positive immediate byte stores in the main section", sites=stock),
        evidence=bindings + list(map(reference, (CURRENT.RELEASE, play.verified.OUT))),
        scope_limit="Reconstructs the observed endpoints and selected writes. Other saved inputs, later ordinary sessions and other store encodings remain outside the trace.",
        ROM_changed=False, new_editorial_credit=0))
    print("Verified 51 ordinary stores, explaining all 45 changed fields. The first Nagasaki town hold matches all 146 restored bytes.")


if __name__ == "__main__":
    main()
