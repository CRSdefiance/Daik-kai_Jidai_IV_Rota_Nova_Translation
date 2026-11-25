"""Apply protected phrase wraps while preserving unowned story text and control flow."""

from inspect import getsource
from types import SimpleNamespace

from scripts import prepare_story_tag_wraps_20261118 as paired
from scripts import review_story_tag_wraps_20261118 as review
from scripts import stage_london_guild_assignments_20261118 as precedent
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage, parent = precedent.base, precedent.native, precedent.stage, paired.parent
ROOT = paired.ROOT / "research_v2"
ROM = ROOT / "Story_Tag_Wraps_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"
logical_end = stage.logical_end


def rebuild_function():
    scope = vars(stage) | {"plan_progressive": precedent.plan_progressive}
    exec(getsource(stage.changed_speech), scope)
    source = checked_text(getsource(stage.rebuild), {
        "        if w == SPEECH:": "        if w == SPEECH and owners:",
        "        elif w == STYLE:": "        elif w == STYLE and owners:",
        "        elif w in MENU:": "        elif w in MENU and owners:",
        "            else:\n                assert old == now":
            "            elif w not in (SPEECH, STYLE, *MENU):\n                assert old == now",
    })
    exec(compile(source, __file__ + "::only-reviewed-speech", "exec"), scope)
    def rebuild(rows, source, current, inventory, clean_arm, arm, painter):
        if (rows[0]["route"], rows[0]["block"]) == (0, 84):
            return fit_training_offer(rows, source, current, inventory, arm)
        return scope["rebuild"](rows, source, current, inventory, clean_arm, arm, painter)

    return rebuild


def fit_training_offer(rows, source, current, inventory, arm):
    row, = rows
    old = bytes.fromhex(row["current_hex"])
    japanese = bytes.fromhex(row["source_hex"])
    at = row["current_reference"]["offset"]
    jp_at = row["source_reference"]["offset"]
    assert old[0] == japanese[0] == 16
    assert source[jp_at:jp_at + len(japanese)] == japanese and current[at:at + len(old)] == old
    assert source[jp_at - 5:jp_at] == current[at - 5:at] == bytes.fromhex("0040ffff00")
    body, plan = precedent.plan_progressive(row, old[0], old[1:], japanese[1:])
    assert len(body) + 1 <= len(old)
    wanted = old[:1] + body.ljust(len(old) - 1, b" ")
    target = current[:at] + wanted + current[at + len(old):]
    assert target[:at] + old + target[at + len(old):] == current
    before, after = (inventory(arm, block)[0] for block in (current, target))
    assert len(before) == len(after)
    commands = []
    for a, b in zip(before, after, strict=True):
        for field in ("word", "offset", "native_extent", "ancestor_0100_offsets"):
            assert a[field] == b[field]
        if a["offset"] == at - 5:
            assert a["word"] == 0x4000
            exact = bytes.fromhex(b["whole_command_hex"])
            assert exact[5:5 + len(wanted)] == wanted and not any(exact[5 + len(wanted):])
            commands.append(dict(word=0x4000, source_offset=jp_at - 5, current_offset=at - 5, stored_offset=at - 5,
                                 current=a["whole_command_hex"], stored=exact.hex(), record_ids=[row["id"]]))
        else:
            assert a["whole_command_hex"] == b["whole_command_hex"]
    assert len(commands) == 1
    return target, commands, {row["id"]: plan | {"original_allocation_right_padded": len(old) - len(body) - 1}}


def catalogue_membership(arm, initial, final):
    config = base.load(parent.MANIFEST)["relocations"][native.ARM]["reviewed_name_integration"]["catalog"]
    banks = [[native.IlnkContainer.parse(files[f"/data/SC{i}.DK4"]).blocks for i in range(4)]
             for files in (initial, final)]
    org, out = (stage.progressive.native.catalogue(arm, config, bank) for bank in banks)
    assert org == out


source = checked_text(getsource(precedent.main), {
    "    final = native.files(target)": "    final = native.files(target)\n    catalogue_membership(ctx.arm, initial, final)",
    "Assembled all revised guild exchanges with exact relative branches and whole-ROM inverse.":
        "Staged 17 source-bound wraps with exact catalogue ownership, branches and whole-ROM inverse.",
})
blocks = SimpleNamespace(BLOCKS=(tuple(paired.LEADS[0]), *paired.BLOCKS[1:]))
env = vars(precedent) | globals() | {"paired": blocks}
exec(compile(source, __file__ + "::cumulative-story-wraps", "exec"), env)

if __name__ == "__main__":
    env["main"]()
