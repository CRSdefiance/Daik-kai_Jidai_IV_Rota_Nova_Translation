"""Verify the staged Rafael text against each native renderer and original choice table."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import stage_rafael_midroute_exchanges_20261122 as stage
from scripts import verify_rafael_athens_and_maria_crew_20261122 as verification
from scripts.prepare_london_guild_assignments_20261118 import text_records
from scripts.stage_rafael_fleet_and_crew_exchanges_20261122 import renderer_source
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
GLYPHS = stage.ROOT / "glyph_and_sheet_verification.json"
CHOICES = stage.ROOT / "original_choice_tables.json"

progressive_source = checked_text(renderer_source, {
    'sum(bool(r["layouts"]) for r in checked)': 'sum(bool(r["layouts"]) or r.get("modal_consumer", False) for r in checked)',
    '            before = bytes.fromhex(row["current_hex"])[1:].decode("ascii")':
        '            if raw[5] == 254:\n'
        '                checked.append(result | dict(modal_consumer=True))\n'
        '                continue\n'
        '            before = bytes.fromhex(row["current_hex"])[1:].decode("ascii")',
})
progressive = stage.compiler_scope.copy()
exec(compile(progressive_source, __file__ + "::progressive-renderer", "exec"), progressive)

modal_source = checked_text(getsource(verification.check_modal), {
    '            assert raw.startswith(bytes.fromhex("0040ffff00fe")) and command["current"] == command["stored"]':
        '            assert raw.startswith(bytes.fromhex("0040ffff00fe"))',
    '            owner = owners[path, ident]':
        '            owner = owners[path, ident]\n'
        '            changed = owner["decision"] == "revision"\n'
        '            assert changed == (command["current"] != command["stored"])',
    '            page = paint(body)':
        '            page = paint(body)\n'
        '            if changed:\n'
        '                plan = group["plans"][ident]\n'
        '                assert not second and raw[5:raw.index(0, 6)].rstrip(b" ") == bytes.fromhex(plan["encoded_hex"])\n'
        '                assert " ".join(body.decode("ascii").split()) == owner["english"]\n'
        '                assert native.digest(page["physical"]) == plan["physical_plane_sha256"]',
    'stored_offset=at, exact_command_hex=raw.hex(), row_membership=membership,':
        'stored_offset=at, exact_command_hex=raw.hex(), row_membership=membership, changed=changed,',
    'assert len(records) == 10 and sum(r["second_page"] for r in records) == 2':
        'assert len(records) == 17 and not any(r["second_page"] for r in records)\n'
        '    assert [(r["block"], r["id"]) for r in records if r["changed"]] == [(118, "DK4_MES_B118_R0125")]',
    '"retained_FE"': '"FE"',
    'f"retained_FE_{original.name}"': 'f"FE_{original.name}"',
    'Verified all ten modal pages, including both original two-page Maria sequences.':
        'Verified all 17 modal panels, including the reflowed Colosseum award.',
})
modal = vars(verification) | {"stage": stage}
exec(compile(modal_source, __file__ + "::modal-renderer", "exec"), modal)


def check_choices():
    source, installed = (base.load(file) for file in (stage.REVIEW, stage.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == installed["candidate_sha256"] and installed["draft_sha256"] == base.digest(stage.REVIEW)
    assert installed["whole_parent_inverse"]
    owners = {(r["source_reference"]["block"], r["source_reference"]["command_offset"], r["slot"]): r
              for r in source["retained_choice_labels"]}
    image = base.NdsImage.open(stage.ROM)
    bank = native.IlnkContainer.parse(image.read_file("/data/SC0.DK4"))
    choices = []
    for group in installed["groups"]:
        block = group["block"]
        for command in (r for r in group["commands"] if r["word"] in (0x2100, 0x2200)):
            raw = bytes.fromhex(command["stored"])
            at = command["stored_offset"]
            assert command["current"] == command["stored"] and bank.blocks[block][at:at + len(raw)] == raw
            for rel, actor, body, slots in text_records(raw, command["word"]):
                slot, = slots
                assert actor is None
                row = owners.pop((block, command["source_offset"], slot))
                assert body.hex() == row["current_reference"]["exact_body_hex"]
                assert body.decode("ascii") == row["english"]
                choices.append(dict(id=row["id"], block=block, slot=slot, command_word=command["word"],
                                    caption=row["english"], offset=at + rel, exact_command_hex=raw.hex()))
    assert not owners and len(choices) == 5
    base.save(CHOICES, dict(candidate_sha256=candidate, choices=choices, stored_tables_exact=True,
                            live_selection_and_response_pending=True))
    print("Verified all five original choice captions, slots and complete objects.", flush=True)


def formatting():
    progressive["native_display"]()
    glyphs = verification.glyphs
    FunctionType(glyphs.verify.__code__, vars(glyphs) | dict(stage=stage, OUTPUT=GLYPHS))()
    modal["check_modal"]()
    check_choices()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("formatting", "check_choices"))
    globals()[parser.parse_args().action]()
