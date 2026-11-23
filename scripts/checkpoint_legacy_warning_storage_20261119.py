"""Rebind the exhibition warning and inventory exact legacy text copies in the ROM."""

from collections import Counter
from pathlib import Path
from struct import iter_unpack

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import checkpoint_exhibition_quit_warning_20261115 as earlier
from scripts import checkpoint_pending_shared_native_20261115 as inventory
from scripts import checkpoint_shared_display_owners_20261119 as observed
from scripts import register_rafael_iberian_aftermath_20261119 as current
from scripts.review_sound_bgm_titles_v1 import reference

base, native = current.base, current.native
OUTPUT = observed.OUTPUT.with_name("legacy_warning_storage_scope_20261119_v2.json")
COMMON = "/COMMON/MESFILE.DK4"
WARNING_KEY = 318


def binary_copies(rom, owners):
    files = native.files(rom)
    results = {}
    for key, value in owners.items():
        matches = [
            dict(path=path, offset=at)
            for path, data in files.items()
            for at in inventory.find(data, value + b"\0")
        ]
        results[key] = matches
    return results, len(files)


def aligned_warning_values(rom):
    return [
        dict(component=name, address=base_address + 4 * i)
        for name, base_address, data in inventory.components(rom.rom)
        for i, (word,) in enumerate(iter_unpack("<I", data[:len(data) & ~3]))
        if word == WARNING_KEY
    ]


def shared_glyphs(source, installed, pending, legacy_keys):
    counts, japanese, mixed = Counter(), [], []
    for key, entry in enumerate(installed):
        text = entry.text.decode("cp932")
        if text.isascii():
            counts["ASCII"] += 1
            continue
        wide = [dict(index=i, character=c, codepoint=f"U+{ord(c):04X}")
                for i, c in enumerate(text) if "\uff01" <= c <= "\uff5e"]
        if any(c.isascii() and c.isalpha() for c in text):
            assert wide, key
            mixed.append(dict(message_ID=key, full_width_ascii=wide,
                              current_reference=reference(entry), current_text=text))
            counts["mixed_ASCII_letters_and_full_width_ASCII"] += 1
        else:
            assert entry.text == source[key].text
            japanese.append(key)
            counts["unchanged_source_Japanese"] += 1
    assert len(installed) == 3668
    assert len(japanese) == pending["remaining_promotional_and_scene_keys"] == 245
    assert not legacy_keys.intersection(japanese)
    assert japanese == [*range(3289, 3320), *range(3393, 3607)]
    assert [row["message_ID"] for row in mixed] == [WARNING_KEY]
    assert mixed[0]["full_width_ascii"] == [dict(index=25, character="Ｉ", codepoint="U+FF29")]
    return dict(mapped_keys=len(installed), counts=dict(counts), mixed_width_records=mixed,
                unchanged_source_Japanese_keys=japanese, CP932_decode_errors=0)


def main():
    assert not OUTPUT.exists()
    release, ledger, ownership, warning = map(base.load, (current.RELEASE, base.LEDGER, observed.OUTPUT, earlier.OUTPUT))
    assert base.digest(current.ROM) == ledger["current_integrated_candidate"]["sha256"] == release["candidate_sha256"]
    assert base.digest(native.CLEAN) == ownership["clean_sha256"] == release["clean_input_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    clean, final = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    ja, arm = (x.read_file(native.ARM) for x in (clean, final))
    assert native.digest(arm) == release["target_ARM9_sha256"]
    assert native.digest(final.read_file(COMMON)) == release["target_COMMON_sha256"]
    clean_entries = common_message_entries(clean.read_file(COMMON), ja)
    installed_entries = owned_entries(final.read_file(COMMON), arm, native.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    pending = ledger["pending_shared_consumer_checkpoint_20261114"]
    keys = set(pending["remaining_legacy_keys"])
    rows = [r for r in ownership["records"] if r["message_ID"] in keys]
    assert len(rows) == len(keys) == 31 and pending["remaining_total"] == 276
    glyphs = shared_glyphs(clean_entries, installed_entries, pending, keys)
    for record in rows:
        key = record["message_ID"]
        assert reference(clean_entries[key]) == record["source_reference"]
        assert reference(installed_entries[key]) == record["current_reference"]
        assert clean_entries[key].text.hex() == record["source_hex"]
        assert installed_entries[key].text.hex() == record["current_hex"]
    source, clean_files = binary_copies(clean, {k: clean_entries[k].text for k in keys})
    target, current_files = binary_copies(final, {k: installed_entries[k].text for k in keys})
    for side in (source, target):
        assert all(m["path"] == COMMON for matches in side.values() for m in matches)
    for record in rows:
        k = record["message_ID"]
        record["exact_terminated_copies"] = dict(clean=source[k], registered=target[k])

    caller = warning["normal_quit"]["caller_bound"]
    rebased = earlier.sites(final)
    assert earlier.sites(clean) == rebased
    assert [list(r) for r in rebased["direct_ARM_callers"]] == caller["direct_ARM_callers"]
    assert not rebased["literal_entry_pointer_references"] and not caller["literal_entry_pointer_references"]
    graphics_slot = 0x0214599C + 4 * WARNING_KEY
    for lo, hi in (
                   (earlier.CALLER, earlier.CALLER + 4),
                   (earlier.HELPER, earlier.SELECTOR_END),
                   (earlier.WRAPPER, earlier.WRAPPER + 0x4C),
                   (0x020F56AC, 0x020F56B4), (0x020692D4, 0x020692F0), (graphics_slot, graphics_slot + 4)):
        assert ja[lo - earlier.BASE:hi - earlier.BASE] == arm[lo - earlier.BASE:hi - earlier.BASE]
    literals = aligned_warning_values(final)
    assert aligned_warning_values(clean) == literals == [dict(component="ARM9 section 0", address=0x020F57A4)]
    assert installed_entries[319].text.decode("ascii").strip() == "Quit the game?"
    proposed = warning["exhibition_warning"]
    assert installed_entries[WARNING_KEY].text.hex() == proposed["current_hex"]
    assert reference(clean_entries[WARNING_KEY]) == proposed["source_reference"]
    assert proposed["controlled_native_confirmation"]["complete_glyphs_bounds_and_words"]
    assert base.digest(warning["sheet"]) == warning["sheet_sha256"]
    base.save(OUTPUT, dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        compared_files=dict(clean=clean_files, registered=current_files), records=rows, shared_glyph_census=glyphs,
        clean_and_current_aligned_warning_literals=literals, known_literal_role="graphics register table index",
        original_quit=dict(caller=caller, observed_ordinary_message_ID=319, exact_compatible_selection_code=True),
        exhibition_warning=dict(message_ID=WARNING_KEY, ascii_draft=proposed["english"],
            draft_preview=warning["sheet"], other_display_paths_open=True),
        scope="Exact bytes ending with NUL in extracted files and aligned 32-bit literals in executable components. Alternate punctuation, line breaks, compressed variants and computed arguments are outside this inventory.",
        new_gameplay_runs=0, new_editorial_credit=0, outstanding_shared_keys=276,
        evidence={str(p):base.digest(p) for p in (observed.OUTPUT, earlier.OUTPUT, current.RELEASE, Path(__file__))}))
    print(f"Checked exact copies of 31 original and current legacy records in {clean_files} clean and {current_files} registered files.")


if __name__ == "__main__":
    main()
