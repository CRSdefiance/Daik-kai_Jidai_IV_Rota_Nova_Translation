"""Stage the revised Gallery captions within their existing owned data spans."""

from hashlib import sha256
from pathlib import Path
from struct import pack_into

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.gallery_caption_bounds import validate
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan
from scripts import review_visible_gallery_captions_v1 as review
from scripts.compile_scene_caption_allocation import pack
from scripts.plan_grand_race_ui_allocation_v136 import byte_pointer_references, merge_ranges
from scripts.stage_sound_bgm_titles_v1 import get_raster


base, parent = review.base, review.parent
ARM, COMMON = parent.ARM, parent.COMMON
ROOT = Path('out/visible_gallery_captions_staged_20261111_v1')
ROM = ROOT / 'visible_gallery_captions_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
SHEET = ROOT / 'revised_gallery_captions.png'
ALLOCATION = Path('work/analysis/scene_caption_complete_allocation_v137/report.json')
SIZE = (256, 16)


def storage_offset(arm, ranges):
    sections = MainCodeFile(arm, BASE).sections
    main, = [row for row in sections if row.ramAddress == BASE]
    stage, = [row for row in sections if row.ramAddress == STAGE]
    assert bytes(main.data) == arm[:len(main.data)]
    saved = bytes(stage.data)
    section_at = arm.find(saved)
    assert section_at >= 0 and arm.find(saved, section_at + 1) == -1
    plan = cache_plan(arm)
    assert plan['payload_bytes'] == len(saved) - 48
    old_caption_ranges = base.load(ALLOCATION)['owned_ranges']

    def physical(lo, hi):
        if lo >= POOL - BASE:
            assert POOL - BASE <= lo < hi <= POOL - BASE + plan['payload_bytes']
            return section_at + lo - (POOL - BASE)
        assert any(start <= lo < hi <= end for start, end in old_caption_ranges)
        assert hi <= len(main.data)
        return lo

    return [(lo, hi, physical(lo, hi)) for lo, hi in ranges]


def transform(original, records):
    revised = [r for r in records if r['decision'] == 'revision']
    old = {row['field']: row for row in validate(original)}
    assert len(records) == len(old) == 164
    assert all(old[r['current_reference']['field']]['English'] == r['current_English'] for r in records)
    fields = {r['current_reference']['field']: r['current_reference']['pointer'] - BASE for r in revised}
    owned = {fields[r['current_reference']['field']]: bytes.fromhex(r['current_reference']['stored_hex'])
             for r in revised}
    ranges = merge_ranges((at, at + len(raw)) for at, raw in owned.items())
    assert byte_pointer_references(original, ranges) == fields
    mapped = storage_offset(original, ranges)

    def file_offset(at, width):
        start, _, physical = next(row for row in mapped if row[0] <= at < at + width <= row[1])
        return physical + at - start

    for at, raw in owned.items():
        pos = file_offset(at, len(raw))
        assert original[pos:pos+len(raw)] == raw
    encoded = {row['english']: row['english'].encode('ascii') + b'\0' for row in revised}
    placement, unused = pack(encoded, ranges)
    result = bytearray(original)
    inverse_slots = []
    for lo, hi, at in mapped:
        inverse_slots.append((at, original[at:at+hi-lo]))
        result[at:at+hi-lo] = bytes(hi-lo)
    for text, at in placement.items():
        raw = encoded[text]
        pos = file_offset(at, len(raw))
        result[pos:pos+len(raw)] = raw
    targets = {}
    for row in revised:
        field = row['current_reference']['field']
        inverse_slots.append((field, original[field:field+4]))
        target = BASE + placement[row['english']]
        pack_into('<I', result, field, target)
        targets[field] = target - BASE
    target = bytes(result)
    assert byte_pointer_references(target, ranges) == targets
    inverse = bytearray(target)
    for at, raw in inverse_slots:
        inverse[at:at+len(raw)] = raw
    assert bytes(inverse) == original
    after = {row['field']: row for row in validate(target)}
    for row in records:
        n = row['current_reference']['field']
        assert after[n]['English'] == row['english'] and after[n]['bounds'] == row['output_bounds']
        if row['decision'] == 'retention':
            assert after[n] == old[n]
    return target, dict(owned_file_and_runtime_spans=mapped, unused_runtime_relative_spans=unused,
        original_pointers=fields, target_pointers=targets, all_untouched_caption_owners_exact=True,
        inverse_spans_count=len(inverse_slots), total=164, changed_titles=13)


def verify_masks(arm, image, records):
    font = GameAsciiFont.from_arm9(arm)
    raster = get_raster(image)
    width, height = SIZE
    sheet = Image.new('RGB', (540, 13 * 51), '#263238')
    labels = ImageDraw.Draw(sheet)
    evidence = []
    shown = 0
    for row in records:
        text = row['english']
        x = row['output_bounds'][0]
        events = []
        pixels = raster(arm, text.encode('ascii'), 0xD5404, tracking=-1, size=SIZE, origin=x,
                        instruction_limit=2000000, glyph_events=events)
        expected = bytearray(width * height)
        visible = []
        for i, char in enumerate(text):
            at = x + i * 5
            assert 32 <= at and at + 6 <= 224
            if char != ' ':
                visible.append(dict(code=ord(char), style=1, x=at, y=0))
            glyph = font.decode(char)
            for gy in range(11):
                for gx in range(6):
                    if glyph.getpixel((gx, gy)):
                        expected[(gy + 1) * width + at + gx] = 1
        assert pixels == bytes(expected), row['id']
        assert [event for event in events if event['code'] != 32] == visible
        evidence.append(dict(id=row['id'], complete_glyphs=len(visible), all_glyph_positions_exact=True,
                             full_native_mask_sha256=sha256(pixels).hexdigest()))
        if row['decision'] == 'revision':
            y = shown * 51
            labels.text((12, y + 2), row['context'], fill='white')
            plane = Image.frombytes('L', SIZE, bytes(20 if p else 245 for p in pixels))
            sheet.paste(plane.resize((512, 32), Image.Resampling.NEAREST), (12, y + 17))
            shown += 1
    assert len(evidence) == 164 and shown == 13
    return evidence, sheet


def main():
    assert not ROOT.exists()
    release, draft = map(base.load, (parent.RELEASE, review.OUTPUT))
    assert base.digest(parent.ROM) == release['candidate_sha256'] == draft['current_ROM_sha256']
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    image = base.NdsImage.open(parent.ROM)
    original = image.read_file(ARM)
    assert sha256(original).hexdigest() == draft['current_ARM9_sha256']
    target, storage = transform(original, draft['records'])
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
        manuscript_sha256=base.digest(review.OUTPUT), sheet_sha256=base.digest(SHEET), storage=storage,
        complete_parent_inverse=True, original_code_and_artwork_preserved=True, all_native_caption_masks=masks,
        unchanged_original_COMMON_sha256=release['target_COMMON_sha256'],
        gameplay_and_startup_pending=True, registered=False))
    print('All 164 Gallery title masks and exact parent inverse passed. Thirteen revised captions are staged.')


if __name__ == '__main__':
    main()
