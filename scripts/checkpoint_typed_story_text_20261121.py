"""Scout non-ASCII bytes and long captions in typed story text."""

from collections import Counter
from pathlib import Path
import re

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import register_hodram_execution_20261121 as current


base, native = current.parent.base, current.parent.native
OUTPUT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/"
              "typed_story_text_scout_20261121_v1.json")
# Choice label tables start at zero. A style table contains a zero offset
# in at least one of its eight slots, which need not be the first slot.
HEADER = re.compile(rb'\x00[!"]\x00\x00|\x00A(?:..){0,7}\x00\x00', re.DOTALL)
WORDS = (0x2100, 0x2200, 0x4100)
CONTEXT_WORDS = (0x4000, *WORDS)


def reference(path, number, command, record):
    offset, selector, body, slots = record
    return dict(
        file_path=path, block=number, command_offset=command["offset"],
        text_offset=command["offset"] + offset, word=hex(command["word"]),
        selector=selector, slots=slots, body_hex=body.hex(), text=body.decode("cp932"),
    )


def records(command):
    return paired.text_records(bytes.fromhex(command["whole_command_hex"]), command["word"])


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    clean, english = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    clean_arm, english_arm = [image.read_file(native.ARM) for image in (clean, english)]
    assert native.digest(english_arm) == release["target_ARM9_sha256"]
    inventory, _, _ = native.scoped_inventory()
    routes = []
    leads = []
    for route in range(4):
        path = f"/data/SC{route}.DK4"
        source, target = [image.read_file(path) for image in (clean, english)]
        clean_blocks, english_blocks = [native.IlnkContainer.parse(bank).blocks for bank in (source, target)]
        objects = Counter()
        bodies = Counter()
        for n, block in enumerate(english_blocks):
            if not HEADER.search(block, 8):
                continue
            commands, _ = inventory(english_arm, block)
            for command in commands:
                word = command["word"]
                if word not in WORDS:
                    continue
                objects[hex(word)] += 1
                for j, record in enumerate(records(command)):
                    _, _, body, _ = record
                    bodies[hex(word)] += 1
                    glyph_lead = not body.isascii() or any(byte < 32 and byte not in (10, 13) for byte in body)
                    caption_lead = word != 0x4100 and (len(body) > 28 or b"  " in body or b"\n" in body)
                    if not (glyph_lead or caption_lead):
                        continue
                    clean_commands, _ = inventory(clean_arm, clean_blocks[n])
                    source_owners, current_owners = [
                        [c for c in sequence if c["word"] in WORDS]
                        for sequence in (clean_commands, commands)
                    ]
                    assert [c["word"] for c in source_owners] == [c["word"] for c in current_owners]
                    clean_command = source_owners[current_owners.index(command)]
                    source_record = records(clean_command)[j]
                    assert source_record[1] == record[1] and source_record[3] == record[3]
                    context = {}
                    for label, sequence, owner in (("source", clean_commands, clean_command),
                                                   ("current", commands, command)):
                        index = sequence.index(owner)
                        context[label] = [reference(path, n, nearby, value)
                                          for nearby in sequence[max(0, index - 3):index + 4]
                                          if nearby["word"] in CONTEXT_WORDS
                                          for value in records(nearby)]
                    leads.append(dict(source=reference(path, n, clean_command, source_record),
                                      current=reference(path, n, command, record),
                                      source_object_hex=clean_command["whole_command_hex"],
                                      current_object_hex=command["whole_command_hex"],
                                      glyph_lead=glyph_lead, caption_lead=caption_lead, context=context))
        routes.append(dict(path=path, source_sha256=native.digest(source), current_sha256=native.digest(target),
                           objects=dict(objects), bodies=dict(bodies)))
    base.save(OUTPUT, dict(
        candidate_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
        ARM9_sha256=release["target_ARM9_sha256"], routes=routes, leads=leads,
        findings_scope="Native text objects with aligned zero-offset tables in the four production story archives. "
        "The 28-byte caption threshold is a screening heuristic. No pixel, gameplay, or editorial credit.",
    ))
    print(f"Checked {sum(sum(route['bodies'].values()) for route in routes)} typed text bodies. "
          f"{sum(row['glyph_lead'] for row in leads)} glyph leads and "
          f"{sum(row['caption_lead'] for row in leads)} caption leads.")


if __name__ == "__main__":
    main()

