"""Bind the next contextual review to clean Japanese and the installed candidate."""

from collections import Counter
from pathlib import Path

from scripts import register_rafael_B161_B169_20261121 as parent


base, native = parent.base, parent.native
ROOT = Path("work/analysis/rafael_B170_B176_followup_20261121")
PAIRED = ROOT / "paired_source_registered_candidate.json"
EARLIER = Path("translations/rafael_B170_B176_integrated_final_review_v1.json")
PATH = "/data/SC0.DK4"


def speech(command):
    raw = bytes.fromhex(command["whole_command_hex"])
    assert command["word"] == 0x4000 and raw.startswith(b"\x00\x40\xff\xff\x00")
    end = raw.index(0, 6)
    assert not any(raw[end:])
    return raw[:6], raw[6:end]


def main():
    release, earlier = map(base.load, (parent.RELEASE, EARLIER))
    assert not PAIRED.exists()
    assert base.digest(parent.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    clean, current = map(base.NdsImage.open, (native.CLEAN, parent.ROM))
    source, installed = [image.read_file(PATH) for image in (clean, current)]
    source_bank, installed_bank = [native.IlnkContainer.parse(raw).blocks for raw in (source, installed)]
    source_hash, installed_hash = map(native.digest, (source, installed))
    clean_arm, current_arm = [image.read_file(native.ARM) for image in (clean, current)]
    assert native.digest(current_arm) == release["target_ARM9_sha256"]
    assert native.digest(current.read_file("/COMMON/MESFILE.DK4")) == release["target_COMMON_sha256"]
    inventory, _, _ = native.scoped_inventory()
    reference = {(r["block"], r["source_reference"]["header_offset"]): r for r in earlier["records"]}
    groups = []
    for n in range(170, 177):
        source_block, installed_block = source_bank[n], installed_bank[n]
        source_cmd, _ = inventory(clean_arm, source_block)
        installed_cmd, _ = inventory(current_arm, installed_block)
        assert [r["word"] for r in source_cmd] == [r["word"] for r in installed_cmd]
        assert not any(r["word"] in (0x2100, 0x2200, 0x4100) for r in source_cmd)
        old_hash, new_hash = map(native.digest, (source_block, installed_block))
        records = []
        for old, new in zip(source_cmd, installed_cmd, strict=True):
            if old["word"] != 0x4000:
                continue
            old_header, ja = speech(old)
            new_header, en = speech(new)
            assert old_header == new_header
            previous = reference.pop((n, old["offset"]))
            assert previous["source_complete_preamble_hex"] == old_header.hex()
            assert previous["source_hex"] == (old_header[5:] + ja).hex()
            assert ja.decode("cp932") == previous["source_Japanese"]
            records.append(dict(id=previous["id"], block=n, file_path=PATH, selector=old_header[5],
                Japanese=ja.decode("cp932"), current_English=en.decode("cp932"),
                source_reference=dict(command_offset=old["offset"], offset=old["offset"] + 5,
                    archive_sha256=source_hash, block_sha256=old_hash, exact_body_hex=ja.hex()),
                current_reference=dict(command_offset=new["offset"], offset=new["offset"] + 5,
                    archive_sha256=installed_hash, block_sha256=new_hash, exact_body_hex=en.hex()),
                complete_preamble_hex=old_header.hex(), earlier_speaker=previous["speaker"],
                earlier_context=previous["context"], earlier_source_meaning=previous["source_meaning"]))
        groups.append(dict(route=0, file_path=PATH, block=n, source_block_sha256=old_hash,
            current_block_sha256=new_hash, source_archive_sha256=source_hash, current_archive_sha256=installed_hash,
            command_counts=dict(Counter(f"0x{r['word']:04x}" for r in source_cmd)), records=records))
    assert not reference and sum(len(g["records"]) for g in groups) == 190
    ROOT.mkdir(exist_ok=True)
    base.save(PAIRED, dict(candidate_sha256=release["candidate_sha256"], profile=release["profile"],
        clean_sha256=release["clean_input_sha256"], registered_review=str(EARLIER),
        registered_review_sha256=base.digest(EARLIER), release_proof=str(parent.RELEASE),
        release_proof_sha256=base.digest(parent.RELEASE), groups=groups,
        complete_source_current_binding=True, contextual_review_pending=True, new_credit=0))
    print("190 clean Japanese and installed English records bound across Rafael B170–176.")


if __name__ == "__main__":
    main()
