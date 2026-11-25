"""Compare the focused Narvik replays with exact position ownership."""

from inspect import getsource

from scripts import stage_narvik_lookout_20261124 as build
from scripts.source_locked_derivation_v5118 import checked_text


def coordinate_proof(receipt):
    """The fixture can own identical writes on different loaded ROMs."""
    return {key: value for key, value in receipt["location_fixture"].items()
            if key not in ("before_RAM_sha256", "after_RAM_sha256")}


if __name__ == "__main__":
    source = checked_text(getsource(build.verify), {
        'test["location_fixture"] == source["location_fixture"]':
            'coordinate_proof(test) == coordinate_proof(source)',
    })
    scope = vars(build) | dict(coordinate_proof=coordinate_proof)
    exec(compile(source, __file__ + "::paired-coordinate-comparison", "exec"), scope)
    scope["verify"](build.read(build.STORED))
