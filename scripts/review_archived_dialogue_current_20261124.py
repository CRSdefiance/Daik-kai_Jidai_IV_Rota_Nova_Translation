"""Rebind five archived drafts and preflight the two established warning previews."""

from pathlib import Path

from PIL import Image, ImageDraw

from scripts import audit_archived_pointer_materialization_20261124 as coverage
from scripts import preflight_setup_save_equipment_v1 as modal
from scripts import register_deck_skill_guidance_20261124 as current
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write

PREVIOUS = Path("translations/editorial_checkpoints/SharedText_20261110_v1/legacy_dialogue_review_20261115_v1.json")
OUT = coverage.OUT.with_name("archived_dialogue_current_drafts_20261124.json")
SHEET = OUT.with_suffix(".png")
KEYS = (284, 318, 750, 751, 752)
DECISIONS = {
    284: ("That fleet is operating at a loss. You can't afford to pay its debt!",
          "State the fleet's losses plainly and keep the debt warning's emphasis. The installed line is unrelated trade-goods text."),
    318: (None, "Keep the earlier warning's explicit exhibition data loss and its clear decision. The installed copy starts If with a full-width I."),
    750: ("Really start over?", "Restore the emphasis in the source's short question. It asks for confirmation without naming an unverified transaction step."),
    751: (None, "The earlier draft sounds like an irritated aside. It keeps the complaint stand-alone and needs a larger allocation."),
    752: (None, "The earlier draft preserves the impatience and explicit remark about joking. The installed copy loses that remark."),
}
SUPPLIED_WRAPPERS = {284: 0x020546B8, 318: 0x0205466C}


def textual(entry):
    return current.paired.source_ref(entry)


def main():
    release = read(current.RELEASE)
    proof = read(coverage.OUT)
    assert digest(current.ROM) == release["candidate_sha256"] == proof["candidate_sha256"]
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    startup = read(release["own_registered_startup"])
    ctx = RegisteredRuntime(current.RELEASE, release["own_registered_startup"], captain=startup["actual_captain_getter"])
    clean = NdsImage.open(CLEAN)
    original = current.paired.base.common_message_entries(clean.read_file(current.COMMON), clean.read_file(current.ARM))
    installed = current.paired.base.common_rows(ctx.common, ctx.arm)
    assert sha256(ctx.common).hexdigest() == release["target_COMMON_sha256"]
    source = {r["message_ID"]: r for r in read(PREVIOUS)["records"] if r["message_ID"] in KEYS}
    locked = {r["message_id"]: r for r in proof["unresolved_records"]}
    assert set(source) == set(locked) == set(KEYS)
    painter, _, _ = modal.font_tools(ctx.image)
    font = modal.GameAsciiFont.from_arm9(ctx.arm)
    panels, records = [], []
    for key in KEYS:
        historic = source[key]
        a, b = original[key], installed[key]
        assert a.text.hex() == historic["source_hex"] and b.text.hex() == historic["current_hex"]
        assert textual(b) | dict(message_id=key) == locked[key]
        draft, reason = DECISIONS[key]
        proposed = draft or historic["english"]
        assert proposed.isascii() and "%" not in proposed and b"%" not in a.text + b.text
        shape = None
        content = proposed.encode("ascii")
        if key in SUPPLIED_WRAPPERS:
            wrapper = SUPPLIED_WRAPPERS[key]
            shape, plane = modal.check_modal(ctx, dict(id=historic["id"], message_ID=key, current_hex=b.text.hex(),
                english=proposed, native_callers=[dict(target=wrapper)]), (), painter, font)
            assert plane and shape["complete_glyphs_bounds_and_words"]
            assert " ".join(" ".join(shape["native_lines"]).split()) == proposed
            if key == 284:
                assert shape["native_lines"] == ["That fleet is operating at a loss.", "You can't afford to pay its debt!"]
            content = shape["storage_markup"].replace("{LB}", "\n").encode("ascii")
            panels.append((key, plane))
        free = len(b.text) - len(content)
        records.append(dict(id=historic["id"], file_path=current.COMMON, message_ID=key,
            clean_Japanese=a.text.decode("cp932"), source_meaning=historic["source_meaning"],
            current_English=b.text.decode("cp932").strip(), earlier_draft=historic["english"], proposed_English=proposed,
            context=historic["context"], localization_note=reason, preview_storage_hex=content.hex(),
            current_reference=textual(b), installed_reference=textual(b), source_reference=textual(a),
            current_allocation_text_bytes=len(b.text), remaining_bytes_after_proposal=free,
            relocation_required_if_proposal_accepted=free < 0,
            preview_supplied_wrapper=SUPPLIED_WRAPPERS.get(key), native_controlled_preview=shape,
            original_display_ownership_open=True, decision="revision proposed", review=dict.fromkeys(GATES, True) | {"formatting": False}))
    width, height = 3 * modal.WIDTH, 3 * modal.HEIGHT
    sheet = Image.new("RGB", (width, (height + 23) * len(panels)), "#263238")
    labels = ImageDraw.Draw(sheet)
    for i, (key, plane) in enumerate(panels):
        y = i * (height + 23)
        labels.text((6, y + 4), f"COMMON {key} / supplied message ID", fill="white")
        panel = Image.frombytes("L", (modal.WIDTH, modal.HEIGHT), bytes(255 - 255 * byte for byte in plane))
        sheet.paste(panel.resize((width, height), Image.Resampling.NEAREST), (0, y + 23))
    sheet.save(SHEET)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], release=reference(current.RELEASE),
        source_ledger=reference(PREVIOUS), current_reference_audit=reference(coverage.OUT), records=records,
        visual_preview=reference(SHEET), ordinary_gameplay=False, ROM_changed=False, new_editorial_credit=0))
    print(f"Reviewed {len(records)} archived wordings and verified {len(panels)} controlled native warning previews.")


if __name__ == "__main__":
    main()
