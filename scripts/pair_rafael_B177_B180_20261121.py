"""Bind the clean Rafael recruitment and tutorial scenes, including all choice slots."""

from collections import Counter
from pathlib import Path

from scripts import register_rafael_B170_B176_20261121 as parent
from scripts.prepare_london_guild_assignments_20261118 import text_records


base, native = parent.base, parent.native
ROOT = Path("work/analysis/rafael_B177_B180_followup_20261121")
PAIRED = ROOT / "paired_source_registered_candidate.json"
EARLIER = Path("translations/rafael_B177_B180_integrated_final_review_v1.json")
ARCHIVE = "/data/SC0.DK4"
TEXT = (0x4000, 0x2100, 0x2200)


def main():
    release, prior = map(base.load, (parent.RELEASE, EARLIER))
    assert not PAIRED.exists()
    assert base.digest(parent.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    images = list(map(base.NdsImage.open, (native.CLEAN, parent.ROM)))
    archives = [image.read_file(ARCHIVE) for image in images]
    bank = [native.IlnkContainer.parse(value).blocks for value in archives]
    archive_hashes = list(map(native.digest, archives))
    arms = [image.read_file(native.ARM) for image in images]
    assert native.digest(arms[1]) == release["target_ARM9_sha256"]
    assert native.digest(images[1].read_file("/COMMON/MESFILE.DK4")) == release["target_COMMON_sha256"]
    inventory, _, _ = native.scoped_inventory()
    references = {(r["block"], r["source_reference"]["offset"]): r for r in prior["records"]}
    groups = []
    for n in range(177, 181):
        original, installed = [blocks[n] for blocks in bank]
        source_cmd, _ = inventory(arms[0], original)
        current_cmd, _ = inventory(arms[1], installed)
        assert [r["word"] for r in source_cmd] == [r["word"] for r in current_cmd]
        assert not any(r["word"] == 0x4100 for r in source_cmd)
        hashes = list(map(native.digest, (original, installed)))
        records = []
        for left, right in zip(source_cmd, current_cmd, strict=True):
            word = left["word"]
            if word not in TEXT:
                continue
            raw = [bytes.fromhex(r["whole_command_hex"]) for r in (left, right)]
            pair = zip(*(text_records(command, word) for command in raw), strict=True)
            for (a, selector, ja, slots), (b, selected, en, installed_slots) in pair:
                assert selector == selected and slots == installed_slots
                old = references.pop((n, left["offset"] + a))
                prefix = bytes([selector]) if selector is not None else b""
                assert (prefix + ja).hex() == old["source_hex"] and ja.decode("cp932") == old["source_Japanese"]
                if selector is not None:
                    assert raw[0][:6] == raw[1][:6]
                source_ref, current_ref = [dict(command_offset=command["offset"], offset=command["offset"] + rel,
                    archive_sha256=arc, block_sha256=block, exact_body_hex=body.hex())
                    for command, rel, arc, block, body in zip(
                        (left, right), (a, b), archive_hashes, hashes, (ja, en), strict=True)]
                records.append(dict(id=old["id"], block=n, file_path=ARCHIVE, selector=selector, slots=slots,
                    native_command_word=word, Japanese=ja.decode("cp932"), current_English=en.decode("cp932"),
                    source_reference=source_ref, current_reference=current_ref, earlier_speaker=old["speaker"],
                    earlier_context=old["context"], earlier_source_meaning=old["source_meaning"]))
        groups.append(dict(route=0, file_path=ARCHIVE, block=n, source_block_sha256=hashes[0],
            current_block_sha256=hashes[1], source_archive_sha256=archive_hashes[0], current_archive_sha256=archive_hashes[1],
            command_counts=dict(Counter(f"0x{r['word']:04x}" for r in source_cmd)), records=records))
    ready = [r for g in groups for r in g["records"]]
    assert not references and len(ready) == 183
    assert sum(r["selector"] is None for r in ready) == 8
    ROOT.mkdir(exist_ok=True)
    base.save(PAIRED, dict(candidate_sha256=release["candidate_sha256"], profile=release["profile"],
        clean_sha256=release["clean_input_sha256"], registered_review=str(EARLIER), registered_review_sha256=base.digest(EARLIER),
        release_proof=str(parent.RELEASE), release_proof_sha256=base.digest(parent.RELEASE), groups=groups,
        complete_source_current_binding=True, contextual_review_pending=True, new_credit=0))
    print("183 exact source and current records bound across Rafael B177–180, including eight choice labels.")


if __name__ == "__main__":
    main()
