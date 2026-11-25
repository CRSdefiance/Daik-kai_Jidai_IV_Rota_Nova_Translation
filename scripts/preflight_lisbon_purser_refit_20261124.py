"""Test the source-based Purser wording in the accepted Refit help consumer."""

from inspect import getsource

from dk4tool.dialogue.refit_help import PROFILE, compile_paragraph
from dk4tool.formats.ilnk import IlnkContainer
from scripts import observe_lisbon_stock_quota_20261124 as play
from scripts import verify_refit_editorial_v830 as native
from scripts import verify_riga_trade_deck_20261124 as scope
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write


ROOT = play.ROOT / "purser_refit_preflight"
OUT = scope.OUT.with_name("lisbon_purser_refit_preflight_20261124.json")
KEY = 1255
ENGLISH = "A purser can bargain and buy out local stock."


def main():
    current = play.current
    manifest = read(current.RELEASE)
    assert digest(CLEAN) == manifest["clean_input_sha256"] and digest(REGISTRY) == manifest["registry_sha256"]
    assert digest(current.ROM) == manifest["candidate_sha256"]
    clean, image = map(NdsImage.open, (CLEAN, current.ROM))
    arm, archive = image.read_file(current.ARM), image.read_file(current.COMMON)
    assert sha256(arm).hexdigest() == manifest["target_ARM9_sha256"]
    assert sha256(archive).hexdigest() == manifest["target_COMMON_sha256"]
    source = scope.base.common_message_entries(clean.read_file(current.COMMON), clean.read_file(current.ARM))[KEY]
    assert source.text.decode("cp932") == "主計長がいれば、値切りや\n買い占めができます"
    before = scope.base.common_rows(archive, arm)
    old = before[KEY]
    assert " ".join(old.text.decode("ascii").split()) == "A purser lets you bargain and corner markets."
    compiled, lines = compile_paragraph(ENGLISH)
    assert lines == ["A purser can bargain and", "buy out local stock."]
    assert b"%" not in source.text + old.text + compiled
    blocks = list(IlnkContainer.parse(archive).blocks)
    offsets = old.block, old.block_offset, old.copy_end
    block, start, end = offsets
    target = blocks[block]
    original = target[start:end]
    assert original == old.text + b"\0" and len(compiled) <= len(original)
    padded = compiled.ljust(len(original), b"\0")
    blocks[block] = target[:start] + padded + target[end:]
    deployed = IlnkContainer(blocks).to_bytes()
    after = scope.base.common_rows(deployed, arm)
    assert len(deployed) == len(archive)
    assert [prev.message_id for prev, new in zip(before, after, strict=True) if prev.text != new.text] == [KEY]
    assert after[KEY].text == compiled[:-1]
    assert all((a.block, a.block_offset, a.copy_end) == (b.block, b.block_offset, b.copy_end)
               for a, b in zip(before, after, strict=True))
    blocks[block] = blocks[block][:start] + original + blocks[block][end:]
    assert IlnkContainer(blocks).to_bytes() == archive

    ROOT.mkdir(exist_ok=True)
    path = ROOT / "input.json"
    write(path, dict(current_candidate_sha256=manifest["candidate_sha256"],
                     records=[dict(message_id=KEY, english=ENGLISH, editorial_decision="Proposed")]))
    body = checked_text(getsource(native.main), {
        "(line_index * 12 + y) * 168": "(line_index * 12 + y + 1) * 168",
    })
    env = vars(native) | dict(ROM=current.ROM, MANUSCRIPT=path, ROOT=ROOT)
    exec(compile(body, __file__ + "::refit-native-font", "exec"), env)
    env["main"]()
    native_proof = ROOT / "native_font_verification.json"
    report = read(native_proof)
    result, = report["records"]
    assert result["compiled_hex"] == compiled.hex() and result["lines"] == lines
    write(OUT, dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(GATES), formatter=PROFILE, candidate_sha256=manifest["candidate_sha256"],
        proposed_COMMON_sha256=sha256(deployed).hexdigest(), exact_allocation_inverse=True,
        record=dict(id=f"COMMON_MESSAGE_{KEY}", message_ID=KEY, file_path=current.COMMON,
            speaker="Refit help", clean_Japanese=source.text.decode("cp932"), english=ENGLISH,
            context="The player inspects the Purser room while refitting the ship in Lisbon.",
            source_meaning="A purser makes it possible to bargain and buy out the stock.",
            localization_note="Bargain and buy out local stock describe two separate abilities and match the Trade Help terminology.",
            source_reference=scope.source_ref(source), current_reference=scope.source_ref(old),
            proposed_reference=scope.source_ref(after[KEY]), decision="revision_proposed",
            review=dict.fromkeys(GATES, True) | dict(formatting=False)),
        owned_allocation=dict(block=block, start=start, end=end, before=original.hex(), proposed=padded.hex()),
        native_proof=reference(native_proof), sheet=report["review_sheets"][0], ROM_changed=False, registered=False))
    print("Verified the proposed Purser paragraph with the current Refit font, allocation and inverse.")


if __name__ == "__main__":
    main()
