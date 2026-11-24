"""Trace saved fleet fields as the ordinary Copenhagen simulation resumes."""

from inspect import getsource
from struct import iter_unpack

from ndspy.code import MainCodeFile

from scripts import observe_fleet_battery_fields_20261124 as battery
from scripts import verify_fleet_battery_fields_20261124 as verified
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read


ROOT = battery.ROOT.with_name("fleet_postload_writes_20261124")
BASE = battery.BASE
OFFSETS = {"docking": 0x3C, "destination": 0x3F, "headquarters": 0x0B}


def sites(image):
    """ARM immediate byte stores without base writeback in the main section."""
    main = MainCodeFile(image.read_file(battery.current.ARM), BASE).sections[0]
    assert main.ramAddress == BASE
    return {BASE + index * 4: word for index, (word,) in enumerate(iter_unpack("<I", main.data[:len(main.data) & ~3]))
            if word >> 28 != 15 and word & 0x0FF00000 == 0x05C00000 and word & 0xFFF in OFFSETS.values()}


def observe(rom, folder):
    clean, active = map(NdsImage.open, (CLEAN, rom))
    stores = sites(clean)
    assert stores == sites(active)
    release, saved = map(read, (battery.current.RELEASE, verified.OUT))
    assert saved["candidate_sha256"] == release["candidate_sha256"]
    row, = [item for item in saved["ordinary_restores"] if item["case"] == "copenhagen"]
    fields = {item["live_address"]: (item["field"], item["index"]) for item in row["all_read_fields"]}
    assert len(fields) == 146
    first_frame = max(row["restore_frames"])
    source = checked_text(getsource(battery.playback.observer), {
        'REQUESTS=REQUESTS, ONLINE=ONLINE, GALLERY=GALLERY)':
            'REQUESTS=REQUESTS, ONLINE=ONLINE, GALLERY=GALLERY, STORES=STORES, FIELDS=FIELDS, START=START, BASE=BASE, __file__=__file__)',
        '    ptr=v[6]\n': '''    if frame < START:
     return
    opcode = STORES[pc]
    address = v[4 + ((opcode >> 16) & 15)] + (opcode & 0xfff)
    if address in FIELDS:
     field, index = FIELDS[address]
     before = ct.c_ubyte.from_address(self.wram + address - BASE).value
     value = v[4 + ((opcode >> 12) & 15)] & 0xff
     self.rows.append(dict(frame=frame, PC=pc, LR=v[18], field=field, index=index,
                           address=address, before=before, value=value))
    return
    ptr=v[6]
''',
    })
    scope = vars(battery.playback) | dict(TARGETS=tuple(stores), STORES=stores, FIELDS=fields, START=first_frame,
        BASE=BASE, __file__=__file__)
    exec(compile(source, __file__ + "::postload-field-stores", "exec"), scope)
    return scope["observer"](rom, folder)


def main():
    assert digest(REGISTRY) == read(battery.current.RELEASE)["registry_sha256"]
    source = checked_text(getsource(battery.playback.main), {
        "'--capture-at', *map(str, frames)]": "'--dump-capture-ram', '--capture-at', *map(str, frames)]",
    })
    scope = vars(battery.playback) | dict(ROOT=ROOT, parent=battery.current, get_schedule=battery.schedule,
        observer=observe, FOCUS=set(), __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-copenhagen-postload", "exec"), scope)
    scope["main"]("copenhagen")


if __name__ == "__main__":
    main()
