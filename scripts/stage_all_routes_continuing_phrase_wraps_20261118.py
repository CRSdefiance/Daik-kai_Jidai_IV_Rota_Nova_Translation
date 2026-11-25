"""Stage the new dialogue while preserving the Sphinx's registered FE continuation."""

from inspect import getsource
from types import FunctionType

from scripts import prepare_all_routes_continuing_phrase_wraps_20261118 as pairing
from scripts import review_all_routes_continuing_phrase_wraps_20261118 as review
from scripts import stage_all_routes_next_phrase_wraps_20261118 as template
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage, paired = template.base, template.native, template.stage, template.paired
parent = review.parent
ROOT = review.ROOT / "research_v3"
ROM, PROOF = ROOT / "All_Routes_Continuing_Phrase_RESEARCH_ONLY.nds", ROOT / "stored_proof.json"
logical_end = template.logical_end
company = template.company


def preserve_sphinx_layout(rows, source, current, inventory, clean_arm, arm, _painter):
    originals = inventory(clean_arm, source)[0]
    installed = inventory(arm, current)[0]
    extra = pairing.existing_continuation(3, 87, source, originals, installed)
    assert extra is not None
    existing = {cmd["offset"]: cmd for cmd in installed}
    paired_commands = dict(zip((cmd["offset"] for cmd in installed if cmd["offset"] != extra["command_offset"]),
                               originals, strict=True))
    for old_at, source_cmd in paired_commands.items():
        current_cmd = existing[old_at]
        assert source_cmd["word"] == current_cmd["word"]
        assert [paired_commands[p]["offset"] for p in current_cmd["ancestor_0100_offsets"]] == source_cmd["ancestor_0100_offsets"]
    new_row, = [row for row in rows if row["decision"] == "revision"]
    assert new_row["id"] == "DK4_MES_B87_R0198" and new_row["finding"] == "wrap"
    now = bytes.fromhex(new_row["current_hex"])
    original = bytes.fromhex(new_row["source_hex"])
    assert now[0] == original[0] == 10
    body, plan = company.plan_progressive(new_row, now[0], now[1:], original[1:])
    assert len(body) == len(now) - 1
    offset = new_row["current_reference"]["offset"]
    target = current[:offset] + now[:1] + body + current[offset + len(now):]
    assert target[:offset] + now + target[offset+len(now):] == current
    assert current[offset:offset+len(now)] == now
    receipt = {}
    for row in rows:
        sa, ca = (row[key]["offset"] for key in ("source_reference", "current_reference"))
        old, prior = (bytes.fromhex(row[key]) for key in ("source_hex", "current_hex"))
        assert source[sa:sa + len(old)] == old and current[ca:ca + len(prior)] == prior
        assert source[sa-5:sa+1] == current[ca-5:ca+1]
        assert paired_commands[ca-5]["offset"] == sa-5
        receipt[ca - 5] = row["id"]
    commands = []
    for old, new in zip(installed, inventory(arm, target)[0], strict=True):
        for k in ("word", "offset", "native_extent", "ancestor_0100_offsets"):
            assert old[k] == new[k]
        at = new["offset"]
        if at != offset - 5:
            assert old["whole_command_hex"] == new["whole_command_hex"]
        else:
            raw = bytes.fromhex(new["whole_command_hex"])
            assert raw[5:6 + len(body)] == now[:1] + body and not any(raw[6 + len(body):])
        source_command = paired_commands.get(at)
        commands.append(dict(word=old["word"], source_offset=source_command["offset"] if source_command else None,
            current_offset=at, stored_offset=at, current=old["whole_command_hex"], stored=new["whole_command_hex"],
            record_ids=[receipt[at]] if at in receipt else []))
    assert existing[extra["command_offset"]]["whole_command_hex"] == extra["exact_command_hex"]
    return target, commands, {new_row["id"]: plan | {"exact_original_FE_continuation": extra}}


def main():
    precedent = template.prior.precedent
    build = precedent.env["main"]
    env = build.__globals__ | globals() | {"paired": review}
    source = checked_text(getsource(precedent.rebuild_function), {
        "precedent.plan_progressive": "company.plan_progressive",
        "        if (rows[0][\"route\"], rows[0][\"block\"]) == (0, 84):":
            """        if (rows[0]["route"], rows[0]["block"]) == (3, 87):
            return preserve_sphinx_layout(rows, source, current, inventory, clean_arm, arm, painter)
        if (rows[0]["route"], rows[0]["block"]) == (0, 84):""",
    })
    exec(compile(source, __file__ + "::preserve-sphinx-continuation", "exec"), env)
    env["catalogue_membership"] = FunctionType(precedent.catalogue_membership.__code__, env)
    FunctionType(build.__code__, env)()
    proof = base.load(PROOF)
    assert proof["whole_parent_inverse"] and proof["candidate_sha256"] == base.digest(ROM)
    assert proof["changed_blocks"] == {f"/data/SC{i}.DK4": list(blocks) for i, blocks in enumerate(review.BLOCKS)}


if __name__ == "__main__":
    main()
