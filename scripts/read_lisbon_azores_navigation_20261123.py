"""Read stock fleet, village and supply coordinates from a navigation snapshot."""

from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
from struct import unpack

from dk4tool.rom.nds import NdsImage
from scripts.reconcile_editorial_acceptance_20261123 import ARM, BASE, digest, read
from scripts.verify_personal_gameplay_v841 import get_machine


RELEASE = Path("releases/all_routes_editorial_20261123_supply_ratio_hint_candidate/verification/registered_release_verification.json")
SCRATCH = 0x02450000


def position(snapshot):
    release = read(RELEASE)
    assert digest(release["candidate"]) == release["candidate_sha256"]
    arm = NdsImage.open(release["candidate"]).read_file(ARM)
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    original = NdsImage.open("work/clean.nds").read_file(ARM)
    for start, end in ((0xCACAC, 0xCACBC), (0xCB118, 0xCB124), (0xCB1A8, 0xCB1B4), (0x2E58C, 0x2E5A8), (0x36C70, 0x36C94)):
        assert arm[start:end] == original[start:end]
    data = snapshot.read_bytes()
    assert len(data) == 0x400000
    cpu, get = get_machine(arm, data)
    fleet = get(0xCB1A8) + 4 + get(0x2E58C) * 132
    identity = get(0x36C70, fleet + 12)
    assert BASE <= identity < BASE + len(data) - 24
    location = unpack("<2i", cpu.mem_read(identity + 16, 8))
    sailors = get(0x55444, identity)
    get(0x34EB0, fleet, SCRATCH)
    supply = unpack("<2I", cpu.mem_read(SCRATCH, 8))
    village = get(0xCACAC, get(0xCB118), 13)
    vtable, = unpack("<I", cpu.mem_read(village, 4))
    assert vtable == 0x0215AF74
    coordinate_getter, = unpack("<I", cpu.mem_read(vtable + 0x1C, 4))
    get(coordinate_getter - BASE, SCRATCH, village)
    target = unpack("<2i", cpu.mem_read(SCRATCH, 8))
    assert cpu.mem_read(BASE, len(data)) == data
    return dict(ship_position=tuple(round(x / 128, 2) for x in location), sailors=sailors,
                water_and_food=supply, azores_point=target)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    print(position(parser.parse_args().snapshot))
