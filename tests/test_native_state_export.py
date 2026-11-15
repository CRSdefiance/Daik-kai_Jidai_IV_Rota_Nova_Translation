"""State reader must reject metadata that could misattribute runtime evidence."""

import struct
import zlib

import pytest

from scripts.inspect_desmume_state_v249 import parse


def state(*, compressed=False, duplicate=False):
    body=bytearray()
    for kind,tag,payload in [(1,b"9REG",bytes(64)),(4,b"DTCM",b"\x12\x34"),(60,b"MDTC",struct.pack("<I",0x027E0000))]:
        record=tag+struct.pack("<2I",1,len(payload))+payload
        if duplicate and kind==4:
            record+=record
        body.extend(struct.pack("<2I",kind,len(record))+record)
    body.extend(struct.pack("<I",0xFFFFFFFF))
    encoded=zlib.compress(body) if compressed else bytes(body)
    return b"DeSmuME SState\0\0"+struct.pack("<4I",12,1,len(body) if compressed else len(body)+32,len(encoded) if compressed else 0xFFFFFFFF)+encoded


@pytest.mark.parametrize("compressed",[False,True])
def test_both_native_encodings_preserve_tag_identity(compressed):
    fields,proof=parse(state(compressed=compressed))
    assert fields[4]["DTCM"]==b"\x12\x34"
    assert fields[60]["MDTC"]==struct.pack("<I",0x027E0000)
    assert proof["chunk_ids"]==[1,4,60]


def test_duplicate_region_cannot_replace_original_memory():
    with pytest.raises(ValueError,match="field extent"):
        parse(state(duplicate=True))


@pytest.mark.parametrize("compressed",[False,True])
def test_export_truncation_cannot_pass_declared_bounds(compressed):
    with pytest.raises(ValueError,match="extent escapes"):
        parse(state(compressed=compressed)[:-1])
