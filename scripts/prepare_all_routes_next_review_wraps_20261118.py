"""Pair follow-up dialogue without assigning extra FE pages new source IDs."""

from inspect import getsource

from scripts import prepare_london_guild_assignments_20261118 as pair
from scripts import register_all_routes_continuing_phrase_wraps_20261118 as parent
from scripts.source_locked_derivation_v5118 import checked_text

base = parent.base
ROOT = parent.stage.ROOT.parent.with_name("all_routes_next_review_wraps_20261118")
QUEUE = parent.stage.ROOT / "followup_wrap_queue.json"


def existing_continuations(route, block, japanese, source, current):
    if (route, block) != (3, 116):
        return []
    assert len(current) == len(source) + 2
    result = []
    for shift, (ident, expected_at) in enumerate(((41, 630), (51, 1026))):
        owner, = [i for i, command in enumerate(source) if command["word"] == 0x4000
                  and japanese[:command["offset"] + 5].count(b"\0") == ident]
        first, second = current[owner + shift:owner + shift + 2]
        assert source[owner]["word"] == first["word"] == second["word"] == 0x4000
        prefix = bytes.fromhex("0040ffff00fe")
        assert all(bytes.fromhex(c["whole_command_hex"]).startswith(prefix) for c in (source[owner], first, second))
        assert first["ancestor_0100_offsets"] == second["ancestor_0100_offsets"]
        assert second["offset"] == expected_at
        body = bytes.fromhex(second["whole_command_hex"])[6:].split(b"\0", 1)[0]
        result.append(dict(owner_id=f"DK4_MES_B116_R{ident:04}", command_offset=expected_at,
            exact_command_hex=second["whole_command_hex"], current_English=body.decode("cp932")))
    return result


def main():
    queue = base.load(QUEUE)
    assert queue["candidate_sha256"] == base.digest(parent.ROM)
    leads = [lead for lead in queue["records"] if lead["disposition"] == "open editorial lead"]
    blocks = tuple(tuple(dict.fromkeys(lead["block"] for lead in leads
                  if lead["file_path"] == f"/data/SC{i}.DK4"))[:5] for i in range(4))
    assert 116 in blocks[3]
    source = checked_text(getsource(pair.main), {
        "            before = stage.offsets(a, stage.logical_end(japanese))":
            """            extra = existing_continuations(route, n, japanese, a, b)
            excluded = {page["command_offset"] for page in extra}
            b = [command for command in b if command["offset"] not in excluded]
            before = stage.offsets(a, stage.logical_end(japanese))""",
        "native_commands=len(a), counts=counts, records=records))":
            """native_commands=len(a), counts=counts, records=records, existing_FE_continuations=extra))""",
    })
    contexts = tuple(f"Review {name}'s next open wraps in the complete exchange."
                     for name in ("Rafael", "Hodram", "Lil", "Maria"))
    scope = vars(pair) | globals() | {"BLOCKS": blocks, "CONTEXT": contexts}
    exec(compile(source, __file__ + "::paired-native-commands", "exec"), scope)
    scope["main"]()
    packet = ROOT / "paired_source.json"
    refs = {(g["file_path"],g["block"],row["current_offset"],row["current_body_hex"]):row["source_record_index"]
            for g in base.load(packet)["groups"] for row in g["records"]}
    selected = []
    for lead in leads:
        key = (lead["file_path"],lead["block"],lead["offset"],lead["stored_body_hex"])
        if key in refs:
            selected.append(lead | {"source_record_index": refs[key]})
    assert len(selected) >= 20 and any(row["file_path"] == "/data/SC3.DK4" and row["block"] == 116 for row in selected)
    base.save(ROOT / "selected_wrap_leads.json",dict(candidate_sha256=queue["candidate_sha256"],
        queue_sha256=base.digest(QUEUE),paired_source_sha256=base.digest(packet),records=selected))
    print(f"Bound {len(selected)} wrap leads and preserved the two existing B116 FE page references.")


if __name__ == "__main__":
    main()
