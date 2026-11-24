"""Bind the new-game fleet seeds and Claudio's observed wrap to the registered ROM."""

from collections import Counter
from pathlib import Path
from struct import pack, unpack_from

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.font_audit import GameAsciiFont

from scripts import observe_rafael_new_game_fleet_20261124 as play
from scripts import stage_london_guild_assignments_20261118 as formatter
from scripts import verify_riga_trade_deck_20261124 as gameplay
from scripts.reconcile_class_names_20261123 import type_name, word
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write

BASE = 0x02000000
FLEET_SEED = 0x0211C1C0
COMPANY_SEED = 0x0211BC70
SEED_STORES = {0x020CDBD0: ("docking", FLEET_SEED, 24, 63, 16),
               0x020CDBE8: ("destination", FLEET_SEED, 24, 63, 19),
               0x020CD4CC: ("headquarters", COMPANY_SEED, 68, 20, 6)}
WRAP_ID = "DK4_MES_B44_R0131"
STORY = "/data/SC0.DK4"
HISTORICAL = Path("releases/all_routes_editorial_20261122_rafael_proof_and_financing_candidate")
OLD_REVIEW = HISTORICAL / "verification/registered_review.json"
OUT = gameplay.OUT.with_name("rafael_new_game_fleet_and_wrap_20261124.json")
POINTERS = gameplay.OUT.with_name("archived_thumb_entry_scope_20261124.json")
KNOWN_POINTERS = {0x0205529C: 0x020534F4, 0x02059134: 0x02053FE4, 0x020BF334: 0x020546B8}


def span(raw, begin, end):
    result = raw[begin - BASE:end - BASE]
    assert begin >= BASE and end > begin and len(result) == end - begin
    return result


def capture(release):
    leaf = play.ROOT / play.CASE
    paths = [leaf / name for name in ("capture/capture_report.json", "requests.json", "source_contract.json", "terminal.json")]
    report, trace, contract, terminal = map(read, paths)
    events, frames, end, _, donor = play.schedule(play.CASE)
    assert donor is None and report["scripted_input_schedule"] == events
    assert report["ROM_sha256"] == terminal["ROM_sha256"] == release["candidate_sha256"]
    assert report["frames"] == terminal["completed_frames"] == end
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not report.get("battery_save_preloaded") and not any(v for k, v in report.items() if k.startswith("synthetic_"))
    assert all(digest(path) == expected for path, expected in terminal["evidence"].items())
    assert trace["source_contract_sha256"] == digest(paths[2]) and trace["observer_sha256"] == digest(play.__file__)
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert contract["ARM9_sha256"] == release["target_ARM9_sha256"]
    assert trace["rows"] == terminal["caption_calls"] and not terminal["target_COMMON_calls"]
    assert [row["message_ID"] for row in trace["source_requests"]] == [120, 120]
    assert {row["PC"] for row in trace["source_requests"]} == {0x020534F4, 0x0205528C}
    snapshots = report["read_only_capture_RAM_snapshots"]
    assert tuple(row["frame"] for row in snapshots) == frames
    assert all(row["read_only_export"] and digest(row["path"]) == row["sha256"] for row in snapshots)
    return report, trace, contract, snapshots, list(map(reference, paths))


def seed_bindings(clean, arm, ram, trace, contract):
    instructions = {
        0x020CDBC4: 0xE5D74010, 0x020CDBD0: 0xE5C8403C,
        0x020CDBE4: 0xE5D74013, 0x020CDBE8: 0xE5C8403F,
        0x020CD4C8: 0xE5D01006, 0x020CD4CC: 0xE5C4100B,
        0x020CDCA0: 0xE59F2008, 0x020CDCA4: 0xE3A01018, 0x020CDCA8: 0xE0202091, 0x020CDCB0: FLEET_SEED,
        0x020CD53C: 0xE59F2008, 0x020CD540: 0xE3A01044, 0x020CD544: 0xE0202091, 0x020CD54C: COMPANY_SEED,
        0x02035A28: 0xE5C0203F,
    }
    installed = {row["PC"]: row["word"] for row in contract["targets"]}
    for pc, word in instructions.items():
        exact = pack("<I", word)
        assert all(span(raw, pc, pc + 4) == exact for raw in (clean, arm, ram)), hex(pc)
        if pc in {*SEED_STORES, 0x02035A28}:
            assert installed[pc] == word
    results = {}
    for pc, (field, start, stride, count, at) in SEED_STORES.items():
        source = span(clean, start, start + stride * count)
        assert all(source == span(raw, start, start + stride * count) for raw in (arm, ram))
        final = [r for r in trace["rows"] if r["PC"] == pc]
        values = list(source[at::stride])
        assert [(r["index"], r["value"], r["field"]) for r in final] == [(i, v, field) for i, v in enumerate(values)]
        assert set(values) <= {*range(90), 115}
        results[field] = dict(store=pc, table=start, stride=stride, column=at, values=values,
                              source_table_sha256=sha256(source).hexdigest(), source_table_exact_hex=source.hex())
    return dict(seeds=results, original_instruction_words=instructions)


def checked_fields(snapshots, trace):
    fleet_root, company_root = 0x022CFD70, 0x022D8E68
    layout = {address: field for address, field in play.FIELDS.items() if field[1] < 63}
    values = {}
    checks = []
    writes = trace["rows"]
    assert len(play.FIELDS) == 148 and len(layout) == 146 and len(writes) == 234
    first = Path(snapshots[0]["path"]).read_bytes()
    values = {address: first[address - BASE] for address in layout}
    index = 0
    for snap in snapshots:
        raw = Path(snap["path"]).read_bytes()
        while index < len(writes) and writes[index]["frame"] <= snap["frame"]:
            row = writes[index]
            address = row["address"]
            assert (row["field"], row["index"]) == layout[address]
            assert values[address] == row["before"] and row["value"] in {*range(90), 115}
            values[address] = row["value"]
            index += 1
        assert all(raw[address - BASE] == value for address, value in values.items())
        groups = {}
        for address, (field, _) in layout.items():
            groups.setdefault(field, Counter())[values[address]] += 1
        checks.append(dict(snapshot=snap, field_values=groups, applied_writes=index))
    assert index == len(writes)
    assert Counter((row["PC"], row["field"]) for row in writes) == {
        (0x020CDBD0, "docking"): 63, (0x020CDBE8, "destination"): 63,
        (0x020CD4CC, "headquarters"): 20, (0x02035A28, "destination"): 88,
    }
    assert [type_name(raw, word(raw, fleet_root + 132 * i)) for i in range(63)] == ["6CFleet"] * 63
    assert word(raw, fleet_root + 132 * 63) == 0x04060540
    assert [type_name(raw, word(raw, company_root + 76 * i)) for i in range(21)] == ["6CForce"] * 20 + ["13CForceFailure"]
    return dict(holds=checks, real_fleet_objects=63, real_company_objects=20,
                adjacent_after_fleets=dict(address=fleet_root + 132 * 63, first_word=word(raw, fleet_root + 132 * 63)),
                adjacent_after_companies="13CForceFailure")


def pointer_snapshot(arm, snapshots):
    earlier = read(POINTERS)
    targets = {0x020534F4, *earlier["reader_and_wrappers"]}
    for snap in snapshots:
        raw = Path(snap["path"]).read_bytes()
        matches = {}
        for target in sorted(targets):
            for pointer in (target, target | 1):
                token = pack("<I", pointer)
                at = raw.find(token)
                while at >= 0:
                    matches[at + BASE] = pointer
                    at = raw.find(token, at + 1)
        assert matches == KNOWN_POINTERS
    assert all(unpack_from("<I", arm, addr - BASE)[0] == pointer for addr, pointer in KNOWN_POINTERS.items())
    return dict(known_resident_words=KNOWN_POINTERS, checked_entry_addresses=sorted(targets),
                snapshots_checked=len(snapshots), all_byte_alignments_and_both_pointer_tags=True,
                earlier_census=reference(POINTERS), ordinary_archived_requests=0)


def story_context(clean, current, arm, capture_report):
    assert digest(OLD_REVIEW) == read(HISTORICAL / "checksums.json")["verification/registered_review.json"]
    pairs = {row["id"]: row for row in read(OLD_REVIEW)["records"] if row["file_path"] == STORY and row["block"] == 44}
    reviews = {}
    before, after = (rom.read_file(STORY) for rom in (clean, current))
    clean_block, block = (IlnkContainer.parse(data).blocks[44] for data in (before, after))
    held = {
        "DK4_MES_B44_R0020": (4001, ("Hmm... That's hard to answer...",)),
        "DK4_MES_B44_R0094": (9600, ("I'm going to see Julio right now!",)),
        WRAP_ID: (12000, ("Yeah. Rafael needs someone at his", "side. That's me.")),
    }
    context_ids = ("DK4_MES_B44_R0127", WRAP_ID, "DK4_MES_B44_R0135")
    panels = gameplay.panels
    frames = panels.shots(capture_report, "_cold_boot.png")
    font = GameAsciiFont.from_arm9(arm)
    for ident in dict.fromkeys((*held, *context_ids)):
        earlier = pairs[ident]
        assert all(earlier["review"].values())
        source = earlier["source_reference"]
        raw = bytes.fromhex(source["exact_command_hex"])
        begin = source["command_offset"]
        assert clean_block[begin:begin + len(raw)] == raw and sha256(clean_block).hexdigest() == source["block_sha256"]
        old = earlier["registered_reference"]
        command = bytes.fromhex(old["exact_command_hex"])
        offset = block.find(command)
        assert offset >= 0 and block.find(command, offset + 1) == -1
        exact = old | dict(command_offset=offset, offset=offset + 5,
                           block_sha256=sha256(block).hexdigest(), archive_sha256=sha256(after).hexdigest(),
                           candidate_sha256=capture_report["ROM_sha256"])
        result = {key: earlier[key] for key in ("id", "speaker", "Japanese", "source_meaning", "context", "english", "localization_note")}
        result.update(source_reference=source, current_reference=exact, installed_reference=exact,
                      review=dict.fromkeys(GATES, True), decision="retention")
        if ident in held:
            frame, rows = held[ident]
            pixels = panels.picture(frames[frame])
            result.update(observed_frame=frames[frame], observed_lines=rows,
                          body_pixels=panels.exact_body(font, rows, pixels),
                          nameplate=panels.nameplate(font, earlier["speaker"], pixels))
        if ident == WRAP_ID:
            body = command[6:command.index(0, 6)]
            original = raw[6:raw.index(0, 6)]
            proposed, plan = formatter.plan_progressive(
                earlier | dict(protected_phrases=["at his side."]), command[5], body, original)
            assert body != proposed and proposed.count(b"FI") == body.count(b"FI") == 1
            assert proposed.count(b"\n") == 1 and b"at his side." in proposed
            result.update(decision="pending_wrap_only", proposed_layout=plan,
                          prior_wording_retained=True, review=dict.fromkeys(GATES, True) | dict(formatting=False),
                          finding="Ordinary gameplay breaks the phrase between his and side. Keep Claudio's boast and the FI substitution, and reflow the full phrase.",
                          staged_or_installed_revision=False)
        reviews[ident] = result
    return dict(original_registered_review=reference(OLD_REVIEW), encounter_records=reviews,
                changed_required="Native renderer, checked stored record and ordinary paired replay for Claudio's proposed layout.")


def main():
    release = read(play.current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(play.current.ROM) == release["candidate_sha256"]
    report, trace, contract, snapshots, evidence = capture(release)
    clean, current = map(NdsImage.open, (CLEAN, play.current.ROM))
    clean_arm, arm = (rom.read_file(play.current.ARM) for rom in (clean, current))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    final = Path(snapshots[-1]["path"]).read_bytes()
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], ordinary_controller_new_game=True,
        evidence=evidence + list(map(reference, (play.current.RELEASE, play.HISTORY, play.PRIOR))),
        fleet_and_company_stock_seeds=seed_bindings(clean_arm, arm, final, trace, contract),
        sampled_fields=checked_fields(snapshots, trace), exact_writes=trace["rows"], checked_write_count=234,
        reached_missionary_destination=False, archived_COMMON=pointer_snapshot(arm, snapshots),
        ordinary_COMMON_requests=trace["source_requests"], story=story_context(clean, current, arm, report),
        ROM_changed=False, new_editorial_credit=0))
    print("Verified 234 ordinary New Game writes and identified Claudio's source-bound wrap follow-up.")


if __name__ == "__main__":
    main()
