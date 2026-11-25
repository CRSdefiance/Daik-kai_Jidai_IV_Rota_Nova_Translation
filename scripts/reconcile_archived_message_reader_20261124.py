"""Check for alternate entries directly into the native COMMON record reader."""

from itertools import pairwise
from pathlib import Path
from struct import iter_unpack, unpack_from

from scripts import checkpoint_shared_reader_and_crew_bypasses_20261119 as reader
from scripts import duel_special_dispatch_v1217 as duel
from scripts import reconcile_archived_message_arguments_20261124 as bounded
from scripts import register_nagasaki_contract_wrap_20261124 as current
from scripts import register_tavern_buy_a_round_20261124 as tavern
from scripts import verify_nagasaki_contract_decline_20261124 as gameplay
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


OUT = bounded.OUT.with_name("archived_message_reader_20261124.json")
BASE = reader.BASE
START, END = 0x020534F4, 0x02053660
GETTER, LITERAL = 0x0205528C, 0x0205529C
EXPECTED = [("ARM9 section 0", LITERAL, START, "exact_pointer_word")]
DUEL_REFERENCE = ("ARM9 section 0", 0x0200DB00, duel.HELPER, "thumb_bl")
DUEL_HISTORY = Path("docs/duel_special_v1237_checkpoint.md")


def linked_immediates(raw, base, destinations):
    """Extend the prior scanner for Thumb BL and ARM BLX immediate."""
    for index, (word,) in enumerate(iter_unpack("<I", raw[:len(raw) & ~3])):
        if word & 0xFE000000 == 0xFA000000:
            offset = word & 0xFFFFFF
            offset -= 0x1000000 if offset & 0x800000 else 0
            pc = base + 4 * index
            target = (pc + 8 + 4 * offset + ((word >> 23) & 2)) & 0xFFFFFFFF
            if target in destinations:
                yield pc, target, "arm_blx_immediate"
    halves = (value for value, in iter_unpack("<H", raw[:len(raw) & ~1]))
    for index, (first, second) in enumerate(pairwise(halves)):
        if first & 0xF800 == 0xF000 and second & 0xF800 == 0xF800:
            offset = ((first & 0x7FF) << 12) | ((second & 0x7FF) << 1)
            offset -= 0x800000 if offset & 0x400000 else 0
            pc = base + 2 * index
            target = (pc + 4 + offset) & 0xFFFFFFFF
            if target in destinations:
                yield pc, target, "thumb_bl"


def references(image, wrappers, *, installed):
    # Inspect the entire range. This includes the cache and block-selector bodies
    # below the documented first instruction, as well as odd mode-bit words.
    byte_addresses = set(range(START, END))
    components = reader.inventory.components(image.rom)
    findings = [(name, pc, target, kind) for name, base, raw in components
                for pc, target, kind in reader.inventory.branch_hits(raw, base, byte_addresses) if not START <= pc < END]
    extra = [(name, pc, target, kind) for name, base, raw in components
             for pc, target, kind in linked_immediates(raw, base, byte_addresses | wrappers) if not START <= pc < END]
    assert findings == EXPECTED and extra == ([DUEL_REFERENCE] if installed else [])
    alternate = [r for r in bounded.addressing_candidates(image, set(range(START, END, 2)))
                 if not START <= r[1] < END]
    assert not alternate
    return findings + extra


def main():
    release, previous, upstream, observed = map(read, (current.RELEASE, tavern.RELEASE, bounded.OUT, gameplay.OUT))
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(current.ROM) == release["candidate_sha256"] == observed["candidate_sha256"]
    assert digest(tavern.ROM) == previous["candidate_sha256"] == upstream["candidate_sha256"]
    assert upstream["fully_bounded_census_sites"] == 827 and observed["ordinary_gameplay"]
    original, before, image = map(NdsImage.open, (CLEAN, tavern.ROM, current.ROM))
    ja, prior, arm = [rom.read_file(current.ARM) for rom in (original, before, image)]
    assert arm == prior and sha256(arm).hexdigest() == release["target_ARM9_sha256"] == previous["target_ARM9_sha256"]
    start, end = START - BASE, END - BASE
    cache = reader.CACHE_AT
    assert start <= cache < end - 7 and ja[cache:cache + 8] == reader.ORIGINAL and arm[cache:cache + 8] == reader.SINGLE
    h, h_end = duel.HELPER - BASE, duel.HELPER_END - BASE
    assert h == cache + 8 and arm[h:h_end] == duel.helper()[0]
    assert arm[duel.FRONT - BASE:duel.FRONT_END - BASE] == duel.front(1480)[0]
    assert ja[start:cache] == arm[start:cache] and ja[h_end:end] == arm[h_end:end]
    gt = GETTER - BASE
    getter = arm[gt:gt + 24]
    assert getter == ja[gt:gt + 24] == bytes.fromhex("08c09fe50010a0e104009fe51cff2fe1f4340502dce62802")
    assert unpack_from("<I", getter, LITERAL - GETTER) == (START,)
    wrappers = {row["entry"] for row in read(bounded.prior.OUT)["references"]}
    assert len(wrappers) == 13
    source_refs = references(original, wrappers, installed=False)
    current_refs = references(image, wrappers, installed=True)
    table = reader.references(CLEAN)
    assert table == reader.references(current.ROM)

    old, installed = [common_rows(rom.read_file(current.COMMON), arm) for rom in (before, image)]
    seen = sorted({r["message_ID"] for r in observed["exact_source_requests"]})
    keys = upstream["archived_ids"]
    assert all(old[key] == installed[key] for key in keys) and set(keys).isdisjoint(seen)
    assert set(keys).isdisjoint({1931, *duel.IDS})
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], unchanged_827_site_argument_proof=reference(bounded.OUT),
        reader_range=[START, END], clean_external_references=source_refs, current_external_references=current_refs,
        additional_simple_address_sources=[], checked_wrapper_entries=sorted(wrappers),
        original_getter=dict(entry=GETTER, exact_hex=getter.hex(), transfers_original_ID_from_r0_to_r1=True),
        approved_cache_difference=dict(offset=cache, source_hex=reader.ORIGINAL.hex(), installed_hex=reader.SINGLE.hex()),
        registered_duel_selector=dict(entry=duel.HELPER, end=duel.HELPER_END, caller=DUEL_REFERENCE[1],
            installed_hex=arm[h:h_end].hex(), carrier_message=1931, numeric_duel_messages=list(duel.IDS),
            proof=reference(DUEL_HISTORY)),
        filename_directory_and_offset_literal_readers=table, preserved_archived_messages=keys,
        ordinary_Nagasaki_request_ids=seen, ordinary_Nagasaki=reference(gameplay.OUT),
        evidence=list(map(reference, (current.RELEASE, tavern.RELEASE, reader.OUTPUT))),
        scope="Original and current components checked for ARM B/BL/BLX immediate, Thumb BL/BLX, exact pointer words, and simple PC-relative address formation into the mapped reader. The separate registered duel helper occupies the retired cache tail. Other computed routing or archive access remains open.",
        ROM_changed=False, new_editorial_credit=0))
    print("The checked reader range has the original getter reference and one verified Thumb call to the separate registered duel selector.")


if __name__ == "__main__":
    main()
