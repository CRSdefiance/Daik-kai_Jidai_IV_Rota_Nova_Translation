"""Stage four Online caption revisions and verify all 13 native text planes."""

from hashlib import sha256
from inspect import getsource
from pathlib import Path
from struct import pack
from types import SimpleNamespace

from PIL import Image, ImageDraw

from scripts import review_visible_online_captions_v1 as review
from scripts import verify_common_alignment_native_v257 as raster_tools
from scripts.source_locked_derivation_v5118 import checked_text


base, parent = review.base, review.parent
ARM = review.ARM
ROOT = Path('out/visible_online_captions_staged_20261111_v1')
ROM = ROOT / 'visible_online_captions_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
SHEET = ROOT / 'all_13_captions.png'
SIZE = (256, 16)


def transform(original, clean, records):
    target = bytearray(original)
    slots = []
    for row in records:
        at, ptr = (row['source_reference'][name] for name in ('offset', 'pointer'))
        field = row['current_reference']['field']
        source = bytes.fromhex(row['source_reference']['original_hex'])
        prior = bytes.fromhex(row['current_reference']['stored_hex'])
        assert clean[at:at+len(source)] == source and original[at:at+len(prior)] == prior
        assert len(prior) == len(source) and source.endswith(b'\0')
        offsets = [n for n in range(0, len(original) - 3, 4) if original[n:n+4] == pack('<I', ptr)]
        assert offsets == [field], (row['id'], offsets)
        revised = row['english'].encode('ascii')
        assert 0 < len(revised) < len(prior) and b'\0' not in revised
        payload = revised.ljust(len(prior), b'\0')
        assert (payload != prior) == (row['decision'] == 'revision')
        if payload != prior:
            slots.append(dict(id=row['id'], offset=at, original=prior.hex(), target=payload.hex(), pointer_field=field))
            target[at:at+len(payload)] = payload
    assert len(slots) == 4
    inverse = bytearray(target)
    for slot in slots:
        original_bytes = bytes.fromhex(slot['original'])
        at = slot['offset']
        inverse[at:at+len(original_bytes)] = original_bytes
    assert bytes(inverse) == original
    return bytes(target), slots


def get_raster(image):
    source = checked_text(getsource(raster_tools.raster), {
        'glyph_events=None):': 'glyph_events=None, origin=0):',
        '    u.mem_write(string, text': '    u.mem_write(ctx + 36, struct.pack("<I", origin))\n'
                                      '    u.mem_write(ctx + 48, struct.pack("<I", 15))\n    u.mem_write(string, text',
    })
    env = vars(raster_tools) | {'NdsImage': SimpleNamespace(open=lambda _: image)}
    exec(compile(source, __file__ + '::Online-caption-style-and-origin', 'exec'), env)
    return env['raster']


def verify_masks(arm, image, records):
    raster = get_raster(image)
    font = review.GameAsciiFont.from_arm9(arm)
    width, height = SIZE
    sheet = Image.new('RGB', (540, len(records) * 51), '#263238')
    labels = ImageDraw.Draw(sheet)
    evidence = []
    for index, row in enumerate(records):
        text = row['english']
        x = row['output_origin'][0]
        events = []
        pixels = raster(arm, text.encode('ascii'), 0xD5404, size=SIZE, origin=x,
                        instruction_limit=2000000, glyph_events=events)
        expected = bytearray(width * height)
        visible = []
        for i, char in enumerate(text):
            at = x + i * 6
            assert 28 <= at and at + 6 <= 228
            if char != ' ':
                visible.append(dict(code=ord(char), style=15, x=at, y=0))
            glyph = font.decode(char)
            for gy in range(11):
                for gx in range(6):
                    if glyph.getpixel((gx, gy)):
                        expected[(gy + 1) * width + at + gx] = 15
        assert pixels == bytes(expected), (row['id'], set(pixels))
        assert [event for event in events if event['code'] != 32] == visible
        evidence.append(dict(id=row['id'], original_center=x, native_glyph_count=len(visible),
            native_plane_sha256=sha256(pixels).hexdigest(), complete_leading_internal_and_final_glyphs=True))
        y = index * 51
        labels.text((12, y + 2), row['context'], fill='white')
        plane = Image.frombytes('L', SIZE, bytes(20 if p else 245 for p in pixels))
        sheet.paste(plane.resize((512, 32), Image.Resampling.NEAREST), (12, y + 17))
    return evidence, sheet


def main():
    assert not ROOT.exists()
    release, draft = map(base.load, (parent.RELEASE, review.OUTPUT))
    assert base.digest(parent.ROM) == release['candidate_sha256'] == draft['current_ROM_sha256']
    assert base.digest(parent.CLEAN) == release['clean_input_sha256']
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    image, clean = (base.NdsImage.open(path) for path in (parent.ROM, parent.CLEAN))
    original = image.read_file(ARM)
    assert sha256(original).hexdigest() == draft['current_ARM9_sha256']
    target, slots = transform(original, clean.read_file(ARM), draft['records'])
    masks, sheet = verify_masks(target, image, draft['records'])
    image.replace_file(ARM, target)
    raw = bytes(image.rom.save())
    image.replace_file(ARM, original)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    with ROM.open('xb') as stream:
        stream.write(raw)
    sheet.save(SHEET)
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), parent_sha256=release['candidate_sha256'],
        target_ARM9_sha256=sha256(target).hexdigest(), parent_ARM9_sha256=sha256(original).hexdigest(),
        manuscript_sha256=base.digest(review.OUTPUT), sheet_sha256=base.digest(SHEET), slots=slots,
        unchanged_original_COMMON_sha256=release['target_COMMON_sha256'], complete_parent_inverse=True,
        original_code_and_artwork_preserved=True, all_native_caption_masks=masks,
        gameplay_and_startup_pending=True, registered=False))
    print('Staged four localized captions; all 13 complete native masks and the parent inverse passed.')


if __name__ == '__main__':
    main()
