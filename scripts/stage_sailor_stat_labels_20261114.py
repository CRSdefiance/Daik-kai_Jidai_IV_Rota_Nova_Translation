"""Stage an isolated Sailor Info label-layer correction on the registered ROM."""

from hashlib import sha256
from pathlib import Path
from struct import pack_into, unpack_from

from dk4tool.graphics.pxl import PxlImage
from scripts import register_rafael_early_wraps_20261111 as parent
from scripts.probe_common_display_name_hook import branch_link
from scripts.verify_release_baseline import files


base = parent.base
ROOT = Path('out/sailor_stat_labels_20261114_v1')
ROM = ROOT / 'sailor_stat_labels_RESEARCH_ONLY.nds'
ARM, ART = '/__arm9__.bin', '/_pxl/personinfo.pxl'
LABELS = ('Stamina', 'Agility', 'Charm', 'Wits', 'Spirit', 'Luck')
BEFORE_ART = '524f13ead0fbe026bc795e09cf39d6b74912736e87c99f219143f82a08a43328'


def change_word(data, changes, offset, old, new):
    assert unpack_from('<I', data, offset)[0] == old, hex(offset)
    pack_into('<I', data, offset, new)
    changes.append(dict(offset=offset, before=old.to_bytes(4, 'little').hex(), after=new.to_bytes(4, 'little').hex()))


def change_arm(source, clean):
    arm = bytearray(source)
    changes = []
    assert source[0x7FA6C:0x7FB74] == clean[0x7FA6C:0x7FB74]
    assert source[0x81528:0x8158C] == clean[0x81528:0x8158C]
    # Re-enable the original label draw. Its y anchor now includes the existing
    # two-pixel numeric alignment correction, so the value baselines stay put.
    old_draw = branch_link(0x02080898, 0x020D5404)
    assert unpack_from('<I', clean, 0x80898)[0] == old_draw
    change_word(arm, changes, 0x80898, 0xE2866002, old_draw)
    for table in (0x11964C, 0x11967C):
        for index in range(6):
            x_offset = table + index * 8
            change_word(arm, changes, x_offset, 127, 126)
            change_word(arm, changes, x_offset + 4, 99 + 15 * index, 101 + 15 * index)
    # Keep the value and shadow at their original absolute horizontal origins.
    change_word(arm, changes, 0x8089C, 0xE2870065, 0xE2870066)
    change_word(arm, changes, 0x808CC, 0xE2870064, 0xE2870065)

    # The Japanese clear string occupied two 12-pixel glyph cells. Clear all
    # seven English cells through that same stat-selection consumer.
    blank_address = 0x02148CA8
    assert [offset for offset in range(0, len(source) - 3, 4)
            if unpack_from('<I', source, offset)[0] == blank_address] == [0x7FB70]
    change_word(arm, changes, 0x148CA8, 0x40814081, 0x20202020)
    change_word(arm, changes, 0x148CAC, 0, 0x00202020)
    table = unpack_from('<6I', arm, 0x148398)
    assert tuple(bytes(arm[p - 0x02000000:p - 0x02000000 + 8]).split(b'\0')[0].decode('ascii')
                 for p in table) == LABELS
    restored = bytearray(arm)
    for row in changes:
        offset = row['offset']
        restored[offset:offset + 4] = bytes.fromhex(row['before'])
    assert restored == source
    return bytes(arm), changes


def clear_labels(source):
    pxl = PxlImage.from_bytes(source)
    assert sha256(source).hexdigest() == BEFORE_ART
    assert (pxl.bits_per_pixel, pxl.width, pxl.height) == (8, 256, 192)
    pixels = []
    for index, label in enumerate(LABELS):
        x, y = 126, 101 + 15 * index
        box = (x, y, 168, y + 11)
        before = bytes(pxl.indices)
        pxl.erase_palette_indices(box, {1})
        changed = [(at % 256, at // 256, value) for at, (old, value) in enumerate(zip(before, pxl.indices, strict=True))
                   if old != value]
        assert changed and all(x <= u < 168 and y <= v < y + 11 and before[v * 256 + u] == 1
                               for u, v, _ in changed)
        pixels.append(dict(label=label, box=list(box), removed_ink_pixels=len(changed)))
    result = pxl.to_bytes()
    assert len(result) == len(source) and result[:pxl.pixels_offset] == source[:pxl.pixels_offset]
    return result, pixels


def main():
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(parent.stage.CLEAN) == release['clean_input_sha256']
    image, clean = map(base.NdsImage.open, (parent.ROM, parent.stage.CLEAN))
    before = files(image)
    assert sha256(before[ARM]).hexdigest() == release['target_ARM9_sha256']
    arm, words = change_arm(before[ARM], clean.read_file(ARM))
    art, rows = clear_labels(before[ART])
    for path, raw in ((ARM, arm), (ART, art)):
        image.replace_file(path, raw)
    after = files(image)
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {ARM, ART}
    ROOT.mkdir(parents=True)
    image.save(ROM)
    for path in (ARM, ART):
        image.replace_file(path, before[path])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    base.save(ROOT / 'stage.json', dict(parent_sha256=release['candidate_sha256'],
        sha256=base.digest(ROM), ARM9_sha256=sha256(arm).hexdigest(), asset_sha256=sha256(art).hexdigest(),
        words=words, stripped_plaques=rows, whole_parent_inverse_exact=True))


if __name__ == '__main__':
    main()
