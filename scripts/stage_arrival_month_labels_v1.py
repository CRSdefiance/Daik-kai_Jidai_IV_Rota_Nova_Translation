"""Stage two terminated arrival-month labels in their source-owned ARM9 slots."""

from hashlib import sha256
from pathlib import Path
from struct import pack, unpack_from

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from capstone.arm import ARM_OP_MEM, ARM_REG_PC

from scripts import register_golden_route_exchanges_v1 as parent


base, review = parent.base, parent.stage.review
ARM, COMMON, CLEAN, BASE = review.ARM, review.COMMON, review.CLEAN, review.BASE
ROOT = Path('out/arrival_month_labels_staged_20261111_v1')
ROM = ROOT / 'arrival_month_labels_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
RENDERER = 0x020D5404
CURRENT = b'Arr. Mo.'
ORIGINAL = '入荷月'.encode('cp932') + b'\0\0'
SLOTS = (
    ('Trade', 0x0215A000, 0x020C2090, 0x020C1FC8, 0x020C209C, b'Arr.', '所持金'.encode('cp932')),
    ('Golden Route Found', 0x0216AFB0, 0x020F2208, 0x020F20B8, 0x020F20C0, b'Arrival', b'%s\x81D%s\0'),
)


def transform(current, clean):
    """The existing consumers and their neighboring strings must remain exact."""
    disassembler = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    disassembler.detail = True
    target = bytearray(current)
    records = []
    for screen, field, pool, load, call, label, adjacent in SLOTS:
        pos, literal = field - BASE, pool - BASE
        assert clean[pos:pos + 8] == ORIGINAL and current[pos:pos + 8] == CURRENT
        assert clean[pos + 8:pos + 8 + len(adjacent)] == adjacent
        neighboring = b'Funds\0' if screen == 'Trade' else adjacent
        assert current[pos + 8:pos + 8 + len(neighboring)] == neighboring
        assert unpack_from('<I', clean, literal)[0] == unpack_from('<I', current, literal)[0] == field
        assert [BASE + off for off in range(0, len(current) - 3, 4) if current[off:off + 4] == pack('<I', field)] == [pool]
        source_code = clean[load - BASE:call - BASE + 4]
        assert source_code == current[load - BASE:call - BASE + 4]
        instruction = next(disassembler.disasm(source_code[:4], load))
        argument = instruction.operands[1]
        assert instruction.mnemonic == 'ldr' and argument.type == ARM_OP_MEM and argument.mem.base == ARM_REG_PC
        assert load + 8 + argument.mem.disp == pool
        branch = next(disassembler.disasm(source_code[-4:], call))
        assert branch.mnemonic == 'bl' and branch.operands[0].imm == RENDERER
        encoded = label.ljust(8, b'\0')
        assert encoded.index(0) == len(label) < 8
        target[pos:pos + 8] = encoded
        records.append(dict(id=f'ARM9_ARRIVAL_MONTH_{field:08X}', screen=screen, field=field, load_PC=load,
            literal_address=pool, call_PC=call, renderer=RENDERER, bound_original_code_hex=source_code.hex(),
            clean_hex=ORIGINAL.hex(), clean_Japanese='入荷月', previous_hex=CURRENT.hex(),
            next_string_hex=neighboring.hex(), revised_hex=encoded.hex(), visible=label.decode('ascii'),
            rationale=('Use the calendar’s short label in the narrower Trade column.' if screen == 'Trade'
                       else 'Name the arrival calendar in the full-width heading field.')))
    inverse = bytearray(target)
    for row in records:
        pos = row['field'] - BASE
        inverse[pos:pos + 8] = CURRENT
    assert bytes(inverse) == current
    return bytes(target), records


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256'] and base.digest(parent.ROM) == release['candidate_sha256']
    image = base.NdsImage.open(parent.ROM)
    current = image.read_file(ARM)
    assert sha256(current).hexdigest() == release['target_ARM9_sha256']
    original = base.NdsImage.open(CLEAN).read_file(ARM)
    target, records = transform(current, original)
    image.replace_file(ARM, target)
    raw = bytes(image.rom.save())
    image.replace_file(ARM, current)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    with ROM.open('xb') as stream:
        stream.write(raw)
    base.save(PROOF, dict(research_ROM=str(ROM), research_ROM_sha256=base.digest(ROM),
        parent_ROM=str(parent.ROM), parent_sha256=release['candidate_sha256'],
        source_ARM9_sha256=sha256(current).hexdigest(), research_ARM9_sha256=sha256(target).hexdigest(),
        research_COMMON_sha256=release['target_COMMON_sha256'], records=records,
        original_label_renderer_preserved=True, parent_inverse_exact=True,
        original_executable_and_non_ARM9_resources_preserved=True,
        registration_and_display_pending=True, new_dialogue_credit=0))
    print('Staged the two source-owned label slots. Complete parent inverse passed.')


if __name__ == '__main__':
    main()
