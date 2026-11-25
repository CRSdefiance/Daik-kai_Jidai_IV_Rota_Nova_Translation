"""Stage proof-bound wrap changes and preserve Maria's two registered FE continuations."""

from inspect import getsource
from types import FunctionType

from scripts import prepare_all_routes_next_review_wraps_20261118 as pair
from scripts import review_all_routes_next_review_wraps_20261118 as review
from scripts import stage_all_routes_next_phrase_wraps_20261118 as template
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage, paired = template.base, template.native, template.stage, template.paired
parent, ROOT = review.parent, review.ROOT / "research_v1"
ROM, PROOF = ROOT / "All_Routes_Next_Wraps_RESEARCH_ONLY.nds", ROOT / "stored_proof.json"
company = template.company
logical_end = template.logical_end


def fit_original_allocation(body, width):
    rows = body.split(b"\n")
    remaining = width - len(body)
    assert remaining >= 0
    for i, row in enumerate(rows):
        assert len(row) <= 36
        inserted = min(remaining, 36 - len(row))
        rows[i] = row + b" " * inserted
        remaining -= inserted
    assert not remaining
    fitted = b"\n".join(rows)
    assert len(fitted) == width and review.common.logical(fitted.decode("ascii")) == review.common.logical(body.decode("ascii"))
    return fitted


def preserve_fe_panels(rows, source, current, inventory, clean_arm, arm, _painter):
    originals, installed = inventory(clean_arm, source)[0], inventory(arm, current)[0]
    pages = pair.existing_continuations(3, 116, source, originals, installed)
    extra_offsets = {page["command_offset"] for page in pages}
    assert len(extra_offsets) == 2
    paired_commands = dict(zip(
        (cmd["offset"] for cmd in installed if cmd["offset"] not in extra_offsets), originals, strict=True))
    for command in installed:
        at = command["offset"]
        if at in extra_offsets:
            continue
        source_command = paired_commands[at]
        assert source_command["word"] == command["word"]
        assert [paired_commands[p]["offset"] for p in command["ancestor_0100_offsets"]] == source_command["ancestor_0100_offsets"]

    revision, = [row for row in rows if row["decision"] == "revision"]
    assert revision["id"] == "DK4_MES_B116_R0024"
    old, jp = (bytes.fromhex(revision[key]) for key in ("current_hex", "source_hex"))
    assert old[0] == jp[0] == 21
    body, plan = company.plan_progressive(revision, old[0], old[1:], jp[1:])
    fitted = fit_original_allocation(body, len(old) - 1)
    offset = revision["current_reference"]["offset"]
    value = old[:1] + fitted
    target = current[:offset] + value + current[offset + len(old):]
    assert current[offset:offset+len(old)] == old
    assert target[:offset] + old + target[offset+len(old):] == current

    owners = {}
    for row in rows:
        sa, ca = (row[key]["offset"] for key in ("source_reference", "current_reference"))
        s, c = (bytes.fromhex(row[key]) for key in ("source_hex", "current_hex"))
        assert source[sa:sa+len(s)] == s and current[ca:ca+len(c)] == c
        assert source[sa-5:sa+1] == current[ca-5:ca+1]
        assert paired_commands[ca-5]["offset"] == sa-5
        owners[ca-5] = row["id"]
    commands = []
    for before, after in zip(installed, inventory(arm, target)[0], strict=True):
        for k in ("word", "offset", "native_extent", "ancestor_0100_offsets"):
            assert before[k] == after[k]
        at = before["offset"]
        raw = bytes.fromhex(after["whole_command_hex"])
        if at == offset - 5:
            assert raw[5:5+len(value)] == value and not any(raw[5+len(value):])
        else:
            assert after["whole_command_hex"] == before["whole_command_hex"]
        commands.append(dict(word=before["word"], source_offset=paired_commands[at]["offset"] if at in paired_commands else None,
            current_offset=at, stored_offset=at, current=before["whole_command_hex"],
            stored=after["whole_command_hex"], record_ids=[owners[at]] if at in owners else []))
    assert pair.existing_continuations(3, 116, source, originals, inventory(arm, target)[0]) == pages
    return target, commands, {revision["id"]: plan | {
        "encoded_hex": value.hex(),
        "lines": [line.strip().decode("ascii") for line in fitted.split(b"\n")],
        "exact_original_FE_continuations": pages,
        "allocation_padding_bytes": len(fitted) - len(body),
    }}


def main():
    precedent = template.prior.precedent
    main_build = precedent.env["main"]
    env = main_build.__globals__ | globals() | {"paired": review}
    source = checked_text(getsource(precedent.rebuild_function), {
        "precedent.plan_progressive": "company.plan_progressive",
        '        if (rows[0]["route"], rows[0]["block"]) == (0, 84):':
            '''        if (rows[0]["route"], rows[0]["block"]) == (3, 116):
            return preserve_fe_panels(rows, source, current, inventory, clean_arm, arm, painter)
        if (rows[0]["route"], rows[0]["block"]) == (0, 84):''',
    })
    exec(compile(source, __file__ + "::preserve-maria-voyage-panels", "exec"), env)
    env["catalogue_membership"] = FunctionType(precedent.catalogue_membership.__code__, env)
    FunctionType(main_build.__code__, env)()
    proof = base.load(PROOF)
    assert proof["whole_parent_inverse"] and proof["candidate_sha256"] == base.digest(ROM)
    assert proof["changed_blocks"] == {f"/data/SC{i}.DK4": list(blocks) for i, blocks in enumerate(review.BLOCKS)}


if __name__ == "__main__":
    main()
