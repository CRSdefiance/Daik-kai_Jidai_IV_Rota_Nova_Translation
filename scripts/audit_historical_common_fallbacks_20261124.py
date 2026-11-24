"""Reconcile historical stock wording and a computed-reference case on the Palace candidate."""

import ast
from pathlib import Path
from struct import unpack_from

from scripts import reconcile_chooser_and_online_dispositions_20261123 as chooser
from scripts import reconcile_tunis_editorial_acceptance_20261124 as acceptance
from scripts import register_palace_investment_wording_20261124 as active
from scripts import verify_archived_message_storage_20261124 as archived
from scripts import verify_riga_town_services_20261124 as square
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write

ROOT = chooser.OUT.parent
OUT = ROOT / "historical_common_fallbacks_20261124.json"
TEMPLATE_SOURCE = Path("scripts/build_50pct_text_batches.py")
SAVE_OWNERS = Path("translations/editorial_checkpoints/SharedText_20261110_v1/shared_display_owners_20261119_v1.json")
DRIVE = ROOT / "palace_investment_wording_drive_20261124.json"
HISTORY = ROOT / "archived_thumb_entry_scope_20261124.json"
ARCHIVED = (284, 318, 750, 751, 752)


def templates():
    source = ast.parse(TEMPLATE_SOURCE.read_text(encoding="utf-8"))
    function, = [node for node in source.body if isinstance(node, ast.FunctionDef) and node.name == "shared_translation"]
    return sorted({n.value.value for n in ast.walk(function) if isinstance(n, ast.Assign) and
                   any(isinstance(t, ast.Name) and t.id == "body" for t in n.targets)})


def adjacent_address_constructions(image, wanted):
    hits = []
    for area, base, raw in acceptance.reader.reader.inventory.components(image.rom):
        for pos in range(0, len(raw) - 7, 4):
            load, update = unpack_from("<II", raw, pos)
            opcode = update & 0x0FE00000
            cond = update >> 28
            if (load & 0x0F7F0000 != 0x051F0000 or opcode not in (0x02400000, 0x02800000) or
                cond == 15 or load >> 28 not in (cond, 14) or (load >> 12 & 15) == 15 or
                (load >> 12 & 15) != (update >> 16 & 15)):
                continue
            delta = load & 4095
            literal = pos + 8 + (delta if load & 0x00800000 else -delta)
            if not 0 <= literal <= len(raw) - 4:
                continue
            address, = unpack_from("<I", raw, literal)
            rot, imm = 2 * (update >> 8 & 15), update & 255
            amount = (imm >> rot | imm << (32 - rot)) & 0xFFFFFFFF
            target = (address + (amount if opcode == 0x02800000 else -amount)) & 0xFFFFFFFF
            if target & ~1 in wanted:
                hits.append(dict(component=area, pc=base + pos, target=target, literal=base + literal,
                                 literal_value=address, exact_hex=raw[pos:pos + 8].hex(), kind="ARM literal load and immediate arithmetic"))
        for pos in range(0, len(raw) - 3, 2):
            load, update = unpack_from("<HH", raw, pos)
            opcode = update & 0xF800
            if load & 0xF800 != 0x4800 or opcode not in (0x3000, 0x3800) or (load >> 8 & 7) != (update >> 8 & 7):
                continue
            literal = ((pos + 4) & ~3) + 4 * (load & 255)
            if literal + 4 > len(raw):
                continue
            address, = unpack_from("<I", raw, literal)
            amount = update & 255
            target = (address + (amount if opcode == 0x3000 else -amount)) & 0xFFFFFFFF
            if target & ~1 in wanted:
                hits.append(dict(component=area, pc=base + pos, target=target, literal=base + literal,
                                 literal_value=address, exact_hex=raw[pos:pos + 4].hex(), kind="Thumb literal load and immediate arithmetic"))
    return hits


def main():
    release, drive = read(active.RELEASE), read(DRIVE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(active.ROM) == release["candidate_sha256"] == drive["readback_sha256"]
    assert drive["verified"] and drive["sole_nds"]
    clean, current = map(NdsImage.open, (CLEAN, active.ROM))
    old_arm, arm = (im.read_file(active.ARM) for im in (clean, current))
    text = current.read_file(active.COMMON)
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"] and sha256(text).hexdigest() == release["target_COMMON_sha256"]
    continuity = acceptance.archived_arguments(clean, current, release)
    earlier, bounded = map(read, (acceptance.callers.OUT, acceptance.reader.bounded.OUT))
    supported = {key for r in earlier["references"] for key in (r["possible_COMMON_ids"] or ())}
    supported.update(key for r in bounded["completed_bindings"] for key in r["ids"])
    assert len(supported) == 3381 and supported.isdisjoint(ARCHIVED)
    old = square.tools.common_message_entries(clean.read_file(active.COMMON), old_arm)
    current_rows = square.tools.common_rows(text, arm)
    signatures = templates()
    matches = {}
    ref = square.panels.text_reference
    for row in current_rows:
        en = b" ".join(row.text.split()).decode("cp932", errors="replace")
        signature = next((s for s in signatures if en == s or en.startswith(s + " %")), None)
        if signature is None:
            continue
        key = row.message_id
        matches[key] = dict(id=key, legacy_template=signature, current_English=en, clean_Japanese=old[key].text.decode("cp932"),
            source=ref(old[key]) | dict(exact_hex=old[key].text.hex()), installed=ref(row) | dict(exact_hex=row.text.hex()),
            in_bounded_caller_sets=key in supported)
    assert set(matches) == {104, 105, 106, 107, 113, 114, 284} and supported.isdisjoint(matches)
    inspected_help = current.read_file("/COMMON/HELP.DK4")
    assert b"This section explains " not in inspected_help
    assert b"Use the listed commands and review the related data." not in inspected_help

    snapshot = read(release["own_registered_startup"])["read_only_snapshot"]
    raw = Path(snapshot["path"]).read_bytes()
    assert snapshot["read_only_export"] and sha256(raw).hexdigest() == snapshot["sha256"]
    for bio in read(chooser.OUT)["chooser_biographies"]:
        idx = bio["chooser_index"]
        info = bio["installed_reference"]
        at = info["ARM9_offset"]
        assert arm[at:at + info["byte_count"]].hex() == info["exact_hex"]
        assert unpack_from("<I", arm, info["pointer_field"] - chooser.BASE) == (info["runtime_address"],)
        owner = chooser.native_selector(arm, raw, dict(chooser_index=idx, staged_reference=info))
        matches[104 + idx]["displayed_biography"] = dict(english=bio["english"],
            original_renderer=owner, historical_frames=[r["screenshot"] for r in bio["live_holds"]])
    sink = acceptance.reader.bounded.displays.legacy_sink(clean, current)
    assert sink == read(SAVE_OWNERS)["legacy_save_diagnostic_sink"]
    assert set(sink["common_getter_calls"].values()) == {111, 112}
    # Extend the prior literal/reference work to address arithmetic in one adjacent instruction.
    previous = read(HISTORY)
    targets = set(previous["reader_and_wrappers"]) | set(range(acceptance.reader.START, acceptance.reader.END, 2))
    before, after = (adjacent_address_constructions(rom, targets) for rom in (clean, current))
    assert before == after
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], active_release=reference(active.RELEASE),
        common_entries=len(current_rows), complete_bounded_sites=continuity, bounded_numeric_coverage=len(supported),
        fallback_producer=reference(TEMPLATE_SOURCE), fallback_signatures=signatures, current_matches=matches,
        active_chooser=reference(chooser.OUT), legacy_save_diagnostic=sink,
        additional_adjacent_address_constructions=after, inherited_archived_scope=reference(HISTORY),
        help_generic_template_fragments_absent=True, open_archived_display_ids=list(ARCHIVED),
        new_editorial_credit=0, ROM_changed=False))
    print(f"Seven stored fallback matches, zero within the verified bounded call sets, and {len(after)} adjacent address candidates.")


if __name__ == "__main__":
    main()