import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_common_tribute_transfer import execute


@pytest.fixture(scope='module')
def source():
    return NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')


@pytest.mark.parametrize('sender', [0, 99, 100, 99_999_999, 0xFFFFFFFF])
@pytest.mark.parametrize('receiver', [0, 99_999_998, 99_999_999])
def test_native_payment_direction_cap_and_skip(source, sender, receiver):
    result = execute(source, sender, receiver)
    amount = sender // 100
    assert result['tribute'] == amount
    assert result['sender_after'] == sender - amount
    assert result['receiver_after'] == (min(receiver + amount, 99_999_999) if amount else receiver)
    assert result['native_field_writes'] == (2 if amount else 0)
    assert result['adjacent_fields_intact']


@pytest.mark.parametrize('offset,word', [
    (0x2DE58, 0xE1A01004),  # MOV r1,r4 reverses the payer debit.
    (0x2DE48, 0xE1A04224),  # LSR r4,r4,#4 doubles the tribute.
    (0x3CCC8, 0xE5900008),  # LDR r0,[r0,#8] reads an adjacent field.
])
def test_mutated_native_transfer_is_rejected(source, offset, word):
    changed = bytearray(source)
    struct.pack_into('<I', changed, offset, word)
    with pytest.raises(ValueError):
        execute(bytes(changed), 10_000, 0)


@pytest.mark.parametrize('offset', [0x2DEF0, 0x3CCC4])
def test_changed_divisor_or_cap_is_rejected(source, offset):
    changed = bytearray(source)
    changed[offset] ^= 1
    with pytest.raises(ValueError, match='divisor or treasury cap'):
        execute(bytes(changed), 10_000, 0)


@pytest.mark.parametrize('sender,receiver', [(-1, 0), (0x100000000, 0), (100, -1)])
def test_fields_require_uint32(source, sender, receiver):
    with pytest.raises(ValueError, match='uint32'):
        execute(source, sender, receiver)
