import copy
import json
import struct
from pathlib import Path

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.compile_deck_explanation_pool import compile_pool
from scripts.probe_deck_explanation_connected import execute


def test_stale_neighboring_owner_cannot_be_repacked():
    proof = json.loads(Path('work/analysis/deck_explanations_source_proof.json').read_text(encoding='utf-8'))
    changed = copy.deepcopy(proof)
    owner = changed['adjacent_complete_owned_pool_lead']['owners'][4]
    raw = bytearray.fromhex(owner['current_bytes_hex'])
    raw[0] ^= 1
    owner['current_bytes_hex'] = raw.hex()
    with pytest.raises(ValueError, match='source owners are not exact'):
        compile_pool(NdsImage.open('out/all_routes_combined_v145_candidate.nds'), changed)


def test_connected_caller_detects_wrong_relocated_description_pointer():
    source = Path('work/analysis/deck_explanations_pool_arm9.bin').read_bytes()
    pool = json.loads(Path('work/analysis/deck_explanations_pool_proof.json').read_text(encoding='utf-8'))
    moves = {m['old_offset']: m for m in pool['moves']}
    assert execute(source, 0, 0, moves[0x133024])['full_pixels_independently_verified']
    changed = bytearray(source)
    struct.pack_into('<I', changed, 0x169F0, 0x02000000 + moves[0x13305C]['new_offset'])
    with pytest.raises(ValueError, match='caller loses full text'):
        execute(bytes(changed), 0, 0, moves[0x133024])
