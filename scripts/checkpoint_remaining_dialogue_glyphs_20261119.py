"""Census remaining mixed-width Latin and Japanese scripts in stored dialogue."""

from collections import Counter
import re

from scripts import checkpoint_shared_display_owners_20261119 as shared
from scripts import register_story_short_phrase_wraps_20261119 as current

base, native = current.base, current.native
OUTPUT = shared.OUTPUT.with_name("remaining_dialogue_glyphs_20261119_v1.json")
JAPANESE = re.compile("[ぁ-ゖァ-ヺ一-龯]")
FULL_WIDTH = re.compile("[Ａ-Ｚａ-ｚ]")
SPEECH = re.compile(rb"\x00\x40\xff\xff\x00")


def glyphs(raw):
    text = raw.decode("cp932", errors="replace")
    return tuple(name for name, test in (("Japanese script", JAPANESE), ("full-width Latin", FULL_WIDTH))
                 if test.search(text))


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(current.ROM) == release["candidate_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    japanese, english = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    arm = english.read_file(native.ARM)
    assert native.digest(arm) == release["target_ARM9_sha256"]
    common = english.read_file(shared.stage.COMMON)
    assert native.digest(common) == release["target_COMMON_sha256"]
    wf = shared.stage.workflow
    entries = wf.owned_entries(common, arm, native.digest(arm[wf.DIRECTORY_OFFSET:wf.TABLE_OFFSET]))
    pending = {r["message_ID"]: r for r in base.load(shared.OUTPUT)["records"]}
    assert len(entries) == 3668 and len(pending) == 276
    flags, counts = [], Counter()
    for ident, entry in enumerate(entries):
        if ident in pending:
            assert wf.reference(entry) == pending[ident]["current_reference"]
            assert entry.text.hex() == pending[ident]["current_hex"]
        tags = glyphs(entry.text)
        if tags:
            row = pending[ident]
            counts.update(tags)
            flags.append({k: row[k] for k in ("message_ID", "kind", "source_reference", "current_reference",
                                                "source_hex", "current_hex")} | {"script_flags": tags})
    assert len(flags) == 246 and counts == {"Japanese script": 245, "full-width Latin": 20}
    assert [r["message_ID"] for r in flags if r["script_flags"] == ("full-width Latin",)] == [318]

    candidates, count_by_route = [], Counter()
    for route in range(4):
        path = f"/data/SC{route}.DK4"
        blocks = native.IlnkContainer.parse(english.read_file(path)).blocks
        for number, block in enumerate(blocks):
            for match in SPEECH.finditer(block):
                if match.start() % 2:
                    continue
                body, _, _ = block[match.end() + 1:].partition(b"\0")
                if not body:
                    continue
                count_by_route[path] += 1
                if glyphs(body):
                    candidates.append((route, number, match.start(), body))
    (route, number, offset, body), = candidates
    assert (route, number, offset) == (1, 40, 982) and body.decode("cp932") == "○×ーッ！！"
    path = "/data/SC1.DK4"
    target_blocks = [native.IlnkContainer.parse(im.read_file(path)).blocks[40] for im in (japanese, english)]
    inventory, _, _ = native.scoped_inventory()
    speeches = [[c for c in inventory(im.read_file(native.ARM), block)[0] if c["word"] == 0x4000]
                for im, block in zip((japanese, english), target_blocks, strict=True)]
    assert len(speeches[0]) == len(speeches[1])
    position = next(i for i, c in enumerate(speeches[1]) if c["offset"] == offset)
    exchange = []
    for i in range(max(0, position - 6), min(len(speeches[1]), position + 8)):
        references = []
        for block, commands in zip(target_blocks, speeches, strict=True):
            command = commands[i]
            at = command["offset"]
            payload = bytes.fromhex(command["whole_command_hex"])[5:].split(b"\0", 1)[0]
            references.append(dict(file_path=path, block=number, command_offset=at, selector=payload[0],
                record_index=block[:at + 5].count(b"\0"), exact_stored_hex=payload.hex(),
                text=payload[1:].decode("cp932")))
        assert references[0]["selector"] == references[1]["selector"]
        exchange.append(dict(source_reference=references[0], current_reference=references[1]))
    assert exchange[6]["source_reference"]["exact_stored_hex"] == exchange[6]["current_reference"]["exact_stored_hex"]
    base.save(OUTPUT, dict(candidate_sha256=release["candidate_sha256"], ARM9_sha256=release["target_ARM9_sha256"],
        COMMON_sha256=release["target_COMMON_sha256"], common_checked=len(entries), shared_keys_pending=len(pending),
        common_flags=flags, common_flag_counts=dict(counts), pending_display_ownership=276,
        story_aligned_standard_speech_header_hits=dict(count_by_route), story_glyph_lead=exchange,
        scope="This scan covers the stored COMMON catalogue and aligned standard 4000 speech headers. "
              "It does not classify display callers, custom substitutions, other object types, or artwork.",
        new_editorial_credit=0, new_gameplay=False))
    print("Checked 3,668 shared keys. All 246 script flags belong to the existing pending set.")
    print("Bound the isolated Hodram B40 glyph lead and its surrounding exchange.")


if __name__ == "__main__":
    main()
