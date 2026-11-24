"""Check register-built addresses around the native COMMON reader and wrappers."""

from struct import iter_unpack, pack, unpack_from

from scripts import audit_historical_common_fallbacks_20261124 as history
from scripts import register_deck_skill_guidance_20261124 as current
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, REGISTRY, digest, read, reference, write

OUT = history.OUT.with_name("archived_pointer_materialization_20261124.json")
MASK = 0xFFFFFFFF


def arm_imm(word):
    value, shift = word & 255, 2 * (word >> 8 & 15)
    return (value >> shift | value << (32 - shift)) & MASK


def arm_update(word, value):
    immediate = arm_imm(word)
    opcode = word >> 21 & 15
    if opcode == 0:
        return value & immediate
    if opcode == 1:
        return value ^ immediate
    if opcode == 2:
        return (value - immediate) & MASK
    if opcode == 3:
        return (immediate - value) & MASK
    if opcode == 4:
        return (value + immediate) & MASK
    if opcode == 12:
        return value | immediate
    if opcode == 14:
        return value & ~immediate
    return None


def arm_sequences(raw, base, wanted):
    words = [word for word, in iter_unpack("<I", raw[:len(raw) & ~3])]
    for i, seed in enumerate(words):
        condition, register = seed >> 28, seed >> 12 & 15
        if condition == 15 or register == 15:
            continue
        if seed & 0x0FEF0000 in (0x03A00000, 0x03E00000):
            value = arm_imm(seed)
            if seed & 0x00400000:
                value ^= MASK
        elif seed & 0x0F7F0000 == 0x051F0000:
            offset = seed & 4095
            literal = 4 * i + 8 + (offset if seed & 0x00800000 else -offset)
            if not 0 <= literal <= len(raw) - 4:
                continue
            value, = unpack_from("<I", raw, literal)
        else:
            continue
        initial = value
        for j in range(i + 1, min(i + 5, len(words))):
            step = words[j]
            predicate = step >> 28
            if (predicate == 15 or (condition != 14 and predicate not in {condition, 14})
                    or step & 0x0E000000 != 0x02000000 or step >> 16 & 15 != register):
                break
            if condition == 14:
                condition = predicate
            register = step >> 12 & 15
            value = arm_update(step, value)
            if value is None or register == 15:
                break
            if value & ~1 in wanted:
                yield dict(start=base + 4 * i, end=base + 4 * (j + 1), encoding="ARM",
                           initial=initial, value=value, exact_hex=raw[4 * i:4 * (j + 1)].hex())


def thumb_step(word, register, value):
    opcode = word & 0xF800
    if opcode in {0x3000, 0x3800} and word >> 8 & 7 == register:
        immediate = word & 255
        return register, (value + (immediate if opcode == 0x3000 else -immediate)) & MASK
    if opcode in {0x0000, 0x0800, 0x1000} and word >> 3 & 7 == register:
        amount = word >> 6 & 31
        signed = value - (1 << 32) if value >> 31 else value
        result = ((value << amount) & MASK if opcode == 0 else
                  value >> (amount or 32) if opcode == 0x0800 else
                  (signed >> (amount or 32)) & MASK)
        return word & 7, result
    if word & 0xFC00 == 0x1C00 and word >> 3 & 7 == register:
        amount = word >> 6 & 7
        return word & 7, (value + (-amount if word & 0x0200 else amount)) & MASK
    return None


def thumb_sequences(raw, base, wanted):
    words = [word for word, in iter_unpack("<H", raw[:len(raw) & ~1])]
    for i, seed in enumerate(words):
        opcode, register = seed & 0xF800, seed >> 8 & 7
        if opcode == 0x2000:
            value = seed & 255
        elif opcode in {0x4800, 0xA000}:
            literal = ((base + 2 * i + 4) & ~3) - base + (seed & 255) * 4
            if opcode == 0xA000:
                value = base + literal
            elif 0 <= literal <= len(raw) - 4:
                value, = unpack_from("<I", raw, literal)
            else:
                continue
        else:
            continue
        initial = value
        for j in range(i + 1, min(i + 5, len(words))):
            result = thumb_step(words[j], register, value)
            if result is None:
                break
            register, value = result
            if value & ~1 in wanted:
                yield dict(start=base + 2 * i, end=base + 2 * (j + 1), encoding="Thumb",
                           initial=initial, value=value, exact_hex=raw[2 * i:2 * (j + 1)].hex())


def inventory(image, wanted):
    components = history.acceptance.reader.reader.inventory.components(image.rom)
    return [row | {"component": name} for name, base, raw in components
            for scanner in (arm_sequences, thumb_sequences) for row in scanner(raw, base, wanted)]


def calibrate():
    base = 0x02000000
    arm = pack("<3I", 0xE3A01402, 0xE3811801, 0xE2811050)
    thumb = pack("<3H", 0x2102, 0x0609, 0x3110)
    literal = pack("<4I", 0xE59F2004, 0xE3822001, 0xE1A00000, base + 0x200)
    checked = []
    for scan, raw, target, expected in (
        (arm_sequences, arm, base + 0x10050, base + 0x10050),
        (arm_sequences, literal, base + 0x200, base + 0x201),
        (thumb_sequences, thumb, base + 0x10, base + 0x10),
    ):
        hit, = scan(raw, base, {target})
        assert hit["value"] == expected and hit["start"] == base
        assert not list(scan(raw, base, {target + 4}))
        checked.append(hit)
    return checked


def main():
    calibration = calibrate()
    release = read(current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(current.ROM) == release["candidate_sha256"]
    clean, image = map(NdsImage.open, (CLEAN, current.ROM))
    continuity = history.acceptance.archived_arguments(clean, image, release)
    previous = read(history.HISTORY)
    lo, hi = history.acceptance.reader.START, history.acceptance.reader.END
    wanted = set(range(lo, hi, 2)) | set(previous["reader_and_wrappers"])
    source, installed = (inventory(rom, wanted) for rom in (clean, image))
    assert source == installed
    receipt = read(history.OUT)
    assert receipt["open_archived_display_ids"] == list(history.ARCHIVED)
    archive = image.read_file(current.COMMON)
    rows = history.square.tools.common_rows(archive, image.read_file(current.ARM))
    exact = []
    for message_id in history.ARCHIVED:
        row = rows[message_id]
        exact.append(history.square.panels.text_reference(row) | dict(message_id=message_id, exact_hex=row.text.hex()))
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
        current_release=reference(current.RELEASE), earlier_fallback_audit=reference(history.OUT),
        same_verified_827_sites=continuity, target_addresses=sorted(wanted), matches=installed, positive_controls=calibration,
        scanner=reference(__file__),
        scope="ARM MOV/MVN or literal seeds with up to four adjacent immediate Boolean/arithmetic operations. Thumb MOV/ADR or literal seeds with up to four adjacent immediate shifts or arithmetic operations. Unchecked register inputs and nonadjacent dependency chains are outside this scan.",
        unresolved_records=exact, all_ARCHIVED_display_ownership_open=True, ordinary_gameplay=False, ROM_changed=False, new_editorial_credit=0))
    print(f"Bound all {continuity['aligned_callers']} current sites and found {len(installed)} matching register-built addresses in the scanned sequences.")


if __name__ == "__main__":
    main()
