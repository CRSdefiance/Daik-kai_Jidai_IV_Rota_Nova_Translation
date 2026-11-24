"""Verify native command boundaries for known retail fleet-order markers."""

from collections import defaultdict
from struct import pack, unpack_from

from dk4tool.formats.ilnk import IlnkContainer
from scripts.checkpoint_story_still_commands_20261120 import explicit_walk, interpreter
from scripts.check_fleet_authored_fallback_20261124 import OUT as FALLBACK
from scripts.register_yard_numerals_20261124 import ARM, RELEASE
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, digest, read, reference, sha256, write


OUT = FALLBACK.with_name("fleet_authored_command_boundaries_20261124.json")
DISPATCH, RETURN = 0x0202BE8C, 0x020297E4


def command_boundaries(walk, arm, block, locations):
    found = {}

    def visit(start, end, offsets, parents):
        body = block[start:end]
        trace = walk(arm, block[:4] + pack("<2H", len(body), 0) + body)
        bridges = defaultdict(list)
        for call in trace["opaque_effect_bridges"]:
            bridges[call["source_offset"]].append(call)
        for row in trace["rows"]:
            absolute = start + row["offset"] - 8
            stop = absolute + row["native_extent"]
            relevant = {offset for offset in offsets if absolute <= offset < stop}
            if not relevant:
                continue
            if row["word"] == 0x0100:
                assert stop == absolute + 4 + unpack_from("<H", block, absolute + 2)[0]
                assert min(relevant) >= absolute + 4
                visit(absolute + 4, stop, relevant, [*parents, absolute])
                continue
            assert relevant == {absolute} and row["word"] == 0xA000 and stop == absolute + 8
            marker, docking, operand_high = unpack_from("<3H", block, absolute + 2)
            assert marker == 0xFFFF and docking == 0 and operand_high >> 8 == 0x82
            call, = bridges[row["offset"]]
            assert call["PC"] == DISPATCH and call["LR"] == RETURN and call["args"][3] == interpreter.STREAM + row["offset"]
            found[absolute] = dict(block_offset=absolute, command_hex=block[absolute:stop].hex(),
                native_extent=row["native_extent"], opcode=row["word"], packed_operand=operand_high << 16,
                fleet_operand_low_byte=operand_high & 0xFF, ancestor_0100_offsets=parents,
                native_effect_entry=call["PC"], native_effect_return=call["LR"])
        assert offsets <= found.keys(), (offsets - found.keys(), trace["error"], trace["stopped_offset"])

    end = 8 + unpack_from("<H", block, 4)[0]
    assert end <= len(block) and not any(block[end:])
    visit(8, end, locations, [])
    return found


def receipt(walk, image, archive, *, clean):
    raw = image.read_file(archive["path"])
    origin = "clean" if clean else "installed"
    assert sha256(raw).hexdigest() == archive[f"{origin}_archive_sha256"]
    blocks = IlnkContainer.parse(raw).blocks
    arm = image.read_file(ARM)
    markers = defaultdict(dict)
    for row in archive[f"{origin}_marker_candidates"]:
        markers[row["block"]][row["block_offset"]] = row["exact_hex"]
    matches = []
    for block_id, candidates in markers.items():
        block = blocks[block_id]
        found = command_boundaries(walk, arm, block, candidates.keys())
        for offset, value in candidates.items():
            assert found[offset]["command_hex"] == value
            matches.append(dict(block=block_id, block_sha256=sha256(block).hexdigest(), **found[offset]))
    return matches


def main():
    release = read(RELEASE)
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(release["candidate"]) == release["candidate_sha256"]
    source, installed = map(NdsImage.open, (CLEAN, release["candidate"]))
    walk = explicit_walk()
    results = []
    for archive in read(FALLBACK)["usual_marker_candidates"][:4]:
        assert archive["path"].startswith("/data/")
        clean = receipt(walk, source, archive, clean=True)
        current = receipt(walk, installed, archive, clean=False)
        assert [(row["block"], row["command_hex"]) for row in clean] == [(row["block"], row["command_hex"]) for row in current]
        results.append(dict(path=archive["path"], clean=clean, installed=current))
    count = sum(len(archive["installed"]) for archive in results)
    assert count == 11
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
                    earlier_marker_and_selector_proof=reference(FALLBACK), release=reference(RELEASE), retail_commands=count,
                    archives=results, scope="The native extent walker bridges the gameplay effect at the decoded command boundary. These checks establish which retail bytes form real commands, with gameplay branch activation and saved input bounds still open.",
                    ROM_changed=False, ordinary_gameplay=False, new_editorial_credit=0))
    print(f"Verified all {count} retail zero-order command boundaries in both ROMs.")


if __name__ == "__main__":
    main()
