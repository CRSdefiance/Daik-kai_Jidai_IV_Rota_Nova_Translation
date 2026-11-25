"""Read only the ship and Narvik positions from ordinary navigation holds."""

from argparse import ArgumentParser
from gzip import decompress
from inspect import getsource
from pathlib import Path

from scripts import read_lisbon_azores_navigation_20261123 as navigation
from scripts.register_tripoli_hodram_warning_20261124 import RELEASE
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(getsource(navigation.position), {
    "get(0xCB118), 13)": "get(0xCB118), 15)",
    "azores_point=target": "narvik_point=target",
    "data = snapshot.read_bytes()": "data = load_snapshot(snapshot)",
})


def load_snapshot(snapshot):
    data = snapshot.read_bytes()
    return decompress(data) if snapshot.suffix == ".gz" else data


scope = vars(navigation) | dict(RELEASE=RELEASE, load_snapshot=load_snapshot)
exec(source, scope)
position = scope["position"]


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path, nargs="+")
    for frame in parser.parse_args().snapshot:
        print(frame.name, position(frame))
