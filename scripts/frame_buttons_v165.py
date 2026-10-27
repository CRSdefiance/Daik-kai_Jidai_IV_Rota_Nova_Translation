"""Six complete shared buttons, paired storage, and actual-format font proof."""

import argparse
import copy
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import REFERENCE_ASCII_FONT_SHA256, GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
    CANONICAL_BASELINE_SHA256,
    RELEASE_STACK_PATH,
    accepted_batch_paths,
    apply_ilnk_pxl_sync_batch,
    apply_pxl_native_label_batch,
    load_release_stack,
    resolve_release_batches,
    rom_files,
    verify_golden_content,
)
from scripts.fleet_row_graphics_v162 import save
from scripts.probe_button_prompt_native import HEADER, STACK, call, machine
from scripts.probe_name_treasure_graphics_v161 import sizing

BASE = Path('out/raphael_natural_v2_accepted_base.nds')
PRIOR = Path('out/all_routes_combined_v164_candidate.nds')
PRIOR_SHA = 'b09e54f664c51cadb40ecc8287b19069cc4c544199e3c4eb3cde9b1d4ddf43fb'
CANDIDATE = Path('out/all_routes_combined_v165_candidate.nds')
PROFILE = 'all-routes-unified-v165'
RESOURCE = '/_pxl/__frame.pxl'
ARCHIVE = '/GRP/CMMNIMG.DK4'
BATCH = Path('translations/frame_action_buttons_graphics_v1.json')
SYNC = Path('translations/frame_action_buttons_cmmnimg_sync_v1.json')
OUT = Path('work/qa/frame_buttons_v165')
ART = Path('work/analysis/frame_buttons_v165_artwork.json')
NATIVE = Path('work/analysis/frame_buttons_v165_native.json')
LABELS = [('装備', 'Equip', [3, 122, 37, 133]),
          ('助言', 'Advice', [3, 138, 37, 149]),
          ('はい', 'Yes', [3, 194, 37, 205]),
          ('いいえ', 'No', [43, 194, 77, 205]),
          ('はずす', 'Remove', [3, 210, 37, 221]),
          ('使う', 'Use', [43, 210, 77, 221])]


def atlas_indices(raw):
    block = IlnkContainer.parse(raw).blocks[5]
    if struct.unpack_from('<IIIIHH', block) != (18, 0, 65548, 16777792, 128, 256):
        raise ValueError('Exact CMMNIMG packed atlas header required')
    return bytes(part for value in block[20:] for part in (value & 15, value >> 4))


def sources():
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256 or sha(PRIOR.read_bytes()) != PRIOR_SHA:
        raise ValueError('Exact canonical and V164 sources required')
    base, prior, clean = [NdsImage.open(p) for p in (BASE, PRIOR, Path('work/clean.nds'))]
    raw = base.read_file(RESOURCE)
    p = PxlImage.from_bytes(raw)
    archived = base.read_file(ARCHIVE)
    indices = atlas_indices(archived)
    right = b''.join(indices[y * 512 + 256:y * 512 + 512] for y in range(256))
    if (raw != prior.read_file(RESOURCE) or raw != clean.read_file(RESOURCE)
            or archived != prior.read_file(ARCHIVE) or archived != clean.read_file(ARCHIVE)
            or (p.width, p.height, p.bits_per_pixel) != (256, 256, 4)
            or bytes(p.indices) != right):
        raise ValueError('Exact Japanese source and matching embedded frame half required')
    return base, prior, p


def targets():
    base, prior, _ = sources()
    arm9 = prior.read_file('/__arm9__.bin')
    target, _ = apply_pxl_native_label_batch(BATCH, base.read_file(RESOURCE), arm9)
    embedded, _ = apply_ilnk_pxl_sync_batch(SYNC, base.read_file(ARCHIVE), target)
    return target, embedded


def embedded_preview(raw):
    a = IlnkContainer.parse(raw)
    # A provisional bank-zero storage view; native bank selection is unproved.
    palette = [bgr555(v) for v, in struct.iter_unpack('<H', a.blocks[4][20:52])]
    image = Image.new('RGBA', (512, 256))
    image.putdata([palette[v] for v in atlas_indices(raw)])
    return image


def materialize():
    base, prior, p = sources()
    batch = {'format': 'dk4-pxl-native-label-batch-v1', 'file_path': RESOURCE,
             'source_file_sha256': sha(p.source), 'font_file_path': '/__arm9__.bin',
             'font_sha256': REFERENCE_ASCII_FONT_SHA256, 'target_locale': 'en-US',
             'editorial_policy': 'natural-dialogue-v2', 'glyph_width': 5, 'advance': 5,
             'trim_blank_top_rows': 2, 'color_index': 15, 'erase_palette_indices': [0, 15],
             'records': []}
    for jp, text, box in LABELS:
        batch['records'].append({
            'id': 'DK4_FRAME_' + text.upper() + '_GRAPHIC_V1',
            'source_japanese': jp, 'text': text, 'box': box,
            'context': 'Shared equipment/advice/confirmation/item action button atlas.',
            'localization_note': 'Complete natural English button label. Remove means taking equipped gear off, not deleting it. Trim only the two proven blank native glyph rows.',
            'background_note': 'Erase original white faces and dark shadows only inside the owned lettering rectangle, reconstructing those pixels from the nearest original row background. Original chrome outside the rectangle is exact.',
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': True, 'visual': False,
                       'physical_gameplay': False}})
    save(BATCH, batch)
    target, _ = apply_pxl_native_label_batch(BATCH, p.source, prior.read_file('/__arm9__.bin'))
    archive = base.read_file(ARCHIVE)
    save(SYNC, {'format': 'dk4-ilnk-pxl-sync-v1', 'file_path': ARCHIVE,
                'source_file_sha256': sha(archive), 'source_image_path': RESOURCE,
                'source_image_sha256': sha(target), 'block_index': 5,
                'source_block_sha256': sha(IlnkContainer.parse(archive).blocks[5]),
                'block_header_size': 20, 'target_width': 512, 'target_height': 256,
                'target_x': 256, 'target_y': 0, 'id': 'DK4_FRAME_ACTION_CMMNIMG_SYNC_V1',
                'scope': 'Synchronize the exact matching right-half pixel indices. Preserve all palette banks, flags, left half and unrelated blocks. Native palette bank/consumer equivalence remains unproved.'})
    target, embedded = targets()
    OUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1048, 1144), '#303030')
    draw = ImageDraw.Draw(sheet)
    for i, (label, image) in enumerate((('Original shared frame', p.render()),
                                       ('English shared frame', PxlImage.from_bytes(target).render()))):
        x = 12 + i * 520
        draw.text((x, 8), label, fill='white')
        sheet.paste(image.resize((512, 512), Image.Resampling.NEAREST).convert('RGB'), (x, 28))
        draw.text((x, 550), 'Action buttons: original' if i == 0 else 'Action buttons: English', fill='white')
        sheet.paste(image.crop((0, 116, 82, 224)).resize((328, 432), Image.Resampling.NEAREST).convert('RGB'), (x, 570))
    sheet.save(OUT / 'review.png')
    for name, raw in (('source', archive), ('english', embedded)):
        embedded_preview(raw).save(OUT / (name + '_embedded_bank_zero.png'))
    save(ART, {'status': 'draft-six-complete-frame-buttons-and-matching-storage',
               'labels': [x[1] for x in LABELS], 'source_sha256': sha(p.source),
               'target_sha256': sha(target), 'embedded_sha256': sha(embedded),
               'visual_review': False, 'embedded_bank_zero_review': False,
               'native_palette_bank_and_live_consumers_proved': False})
    print('Materialized six buttons, exact paired pixel storage and full previews.')


def masks(source, batch):
    font = GameAsciiFont.from_arm9(source)
    full = Image.new('L', (256, 256))
    origins = []
    for row in batch['records']:
        x0, y0, x1, y1 = row['box']
        width = len(row['text']) * batch['advance']
        origin = (x0 + (x1 - x0 - width) // 2, y0 + (y1 - y0 - 9) // 2 - 2)
        if origin[0] < x0:
            raise ValueError('Complete English word exceeds its button')
        for i, char in enumerate(row['text']):
            glyph = font.decode(char).convert('L')
            bounds = glyph.getbbox()
            if glyph.crop((0, 0, 6, 2)).getbbox() or (bounds and bounds[2] > 5):
                raise ValueError('Native glyph would lose visible pixels')
            full.paste(glyph, (origin[0] + i * batch['advance'], origin[1]))
        origins.append(origin)
    return full, origins


def real_format_glyphs(source, target, batch, expected_mask=None):
    p = PxlImage.from_bytes(target)
    expected, origins = masks(source, batch)
    if expected_mask is not None:
        expected = expected_mask
    packed = bytes(p.indices)
    p.indices[:] = bytes(len(p.indices))
    blank = p.to_bytes()
    uc = machine(source)
    uc.mem_write(HEADER - 16, b'\xA5' * (len(blank) + 32))
    uc.mem_write(HEADER, blank)
    executed = set()
    for row, origin in zip(batch['records'], origins, strict=True):
        for i, char in enumerate(row['text']):
            uc.mem_write(STACK, struct.pack('<2I', ord(char), batch['color_index']))
            executed |= call(uc, 0xD16B4, (0, HEADER, origin[0] + i * batch['advance'], origin[1]))
    result = PxlImage.from_bytes(bytes(uc.mem_read(HEADER, len(blank))))
    pixels = bytes(batch['color_index'] if value else 0 for value in expected.tobytes())
    if (bytes(result.indices) != pixels or not {0x020D16B4, 0x020D1820} <= executed
            or result.source[:p.pixels_offset] != blank[:p.pixels_offset]
            or bytes(uc.mem_read(HEADER - 16, 16)) != b'\xA5' * 16
            or bytes(uc.mem_read(HEADER + len(blank), 16)) != b'\xA5' * 16):
        raise ValueError('Complete native button raster/first letter/header/guards differ')
    for row in batch['records']:
        x0, y0, x1, y1 = row['box']
        for y in range(y0, y1):
            for x in range(x0, x1):
                # Background uses other indices. No source white glyph remains.
                if (packed[y * 256 + x] == batch['color_index']) != bool(pixels[y * 256 + x]):
                    raise ValueError('Packed button glyph pixels/first letter differ')
    return {'dimensions': [256, 256], 'format': 'actual-source-four-bit-PXL',
            'complete_native_pixel_sha256': sha(pixels), 'all_glyph_cells_ABI_header_and_guards_pass': True,
            'trimmed_rows': 'Only two proven blank leading rows; every visible native pixel retained.'}


def preservation(target, embedded):
    base, _, a = sources()
    b = PxlImage.from_bytes(target)
    owned = {(x, y) for _, _, box in LABELS for y in range(box[1], box[3]) for x in range(box[0], box[2])}
    if (len(target) != len(a.source) or target[:b.pixels_offset] != a.source[:a.pixels_offset]
            or any(a.indices[y * 256 + x] != b.indices[y * 256 + x]
                   for y in range(256) for x in range(256) if (x, y) not in owned)):
        raise ValueError('Unowned frame artwork/header/palette changed')
    before, after = [IlnkContainer.parse(raw) for raw in (base.read_file(ARCHIVE), embedded)]
    if (len(embedded) != len(base.read_file(ARCHIVE))
            or before.blocks[5][:20] != after.blocks[5][:20]
            or any(a != b for i, (a, b) in enumerate(zip(before.blocks, after.blocks, strict=True)) if i != 5)):
        raise ValueError('Archive header/palette/unrelated blocks changed')
    old, new = atlas_indices(base.read_file(ARCHIVE)), atlas_indices(embedded)
    if any(old[y * 512 + x] != new[y * 512 + x]
           for y in range(256) for x in range(512) if x < 256 or (x - 256, y) not in owned):
        raise ValueError('Unowned embedded pixels changed')
    if b''.join(new[y * 512 + 256:y * 512 + 512] for y in range(256)) != bytes(b.indices):
        raise ValueError('Embedded English frame half differs')
    return {'chrome_unowned_pixels_header_palette_and_extents_exact': True,
            'embedded_left_half_all_palette_banks_flags_and_other_blocks_exact': True,
            'embedded_right_half_exact_translated_frame_indices': True,
            'background': 'Owned glyph/shadow pixels reconstructed from original nearest row colors.',
            'native_bank_selection_and_palette_equivalence_proved': False}


def native():
    _, prior, _ = sources()
    source = prior.read_file('/__arm9__.bin')
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    target, embedded = targets()
    image_size = sizing(source, target, 20, 0x02313F60, supplied_table=True)
    image_size['table_input'] = 'controlled-frame-image-sizing-contract'
    if source[0x10F19C:0x10F1A4] != struct.pack('<2I', 0x02313F60, 0x02160558):
        raise ValueError('Original frame filename descriptor differs')
    save(NATIVE, {'status': 'pass-six-complete-buttons-actual-format-and-paired-storage',
                  'source_arm9_sha256': sha(source), 'actual_format': real_format_glyphs(source, target, batch),
                  'preservation': preservation(target, embedded), 'scoped_image_size': image_size,
                  'source_filename_descriptor': {'owner': 0x02313F60, 'path_address': 0x02160558},
                  'limitations': ['Loaded resource class/header and sizing selector binding are controlled inputs.',
                                  'CMMNIMG pairing is exact storage content, not mapped native palette bank/loading proof.',
                                  'Actual loose/embedded loading, all live button crops/contexts, GPU alpha/palette and input/gameplay remain pending.']})
    print('Pass: complete actual-format native glyphs, exact paired storage, chrome and scoped sizing.')


def register():
    art = json.loads(ART.read_text(encoding='utf-8'))
    if (not art['visual_review'] or not art['embedded_bank_zero_review']
            or json.loads(NATIVE.read_text(encoding='utf-8'))['status'] != 'pass-six-complete-buttons-actual-format-and-paired-storage'):
        raise ValueError('Full loose/embedded previews and native evidence required')
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    for row in batch['records']:
        row['review']['visual'] = True
    save(BATCH, batch)
    registry = load_release_stack()
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v164'])
    profile['batches'].extend([BATCH.as_posix(), SYNC.as_posix()])
    profile['note'] = 'Full V164 inheritance plus six complete frame buttons and matching embedded pixel copy; experimental, live crops/loading/palette/input pending.'
    profile['description'] = 'All 450 V164 batches and terminal stages plus two source-locked graphics batches (452 total).'
    registry['profiles'][PROFILE] = profile
    save(RELEASE_STACK_PATH, registry)
    print('Registered experimental V165 with 452 batches.')


def verify():
    base, prior, _ = sources()
    new = NdsImage.open(CANDIDATE)
    manifest = json.loads(CANDIDATE.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    old = json.loads(PRIOR.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    registry = load_release_stack()
    if (manifest['candidate_sha256'] != sha(CANDIDATE.read_bytes())
            or manifest['base_sha256'] != CANONICAL_BASELINE_SHA256 or manifest['profile'] != PROFILE
            or manifest['release_stack_sha256'] != sha(RELEASE_STACK_PATH.read_bytes())
            or manifest['batches'] != [str(p) for p in resolve_release_batches(PROFILE, [], registry)]
            or len(manifest['batches']) != 452 or manifest['batches'][:450] != old['batches']
            or manifest['required_batches'] != [str(p) for p in accepted_batch_paths(registry)]
            or not all(manifest['checks'].values()) or manifest['relocations'] != old['relocations']):
        raise ValueError('Saved V165 identity, full stack or inherited stages differ')
    before, after, canonical = rom_files(prior), rom_files(new), rom_files(base)
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    if changed != sorted([RESOURCE, ARCHIVE]):
        raise ValueError('Unexpected prior text/code/graphics changes')
    canonical_changed = sorted(p for p in canonical.keys() | after.keys() if canonical.get(p) != after.get(p))
    if manifest['changed_paths'] != canonical_changed or canonical_changed != sorted(old['changed_paths'] + [RESOURCE, ARCHIVE]):
        raise ValueError('Canonical changed path set differs')
    if any(manifest['changed_records'][path] != ids for path, ids in old['changed_records'].items()):
        raise ValueError('Inherited changed records differ')
    target, embedded = targets()
    if target != new.read_file(RESOURCE) or embedded != new.read_file(ARCHIVE):
        raise ValueError('Saved button graphics differ from reviewed batches')
    preservation(target, embedded)
    real_format_glyphs(new.read_file('/__arm9__.bin'), target, json.loads(BATCH.read_text(encoding='utf-8')))
    verify_golden_content(base, new)
    clean = Path('work/clean.nds')
    if sha(clean.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Wrong clean patch base')
    patch = CANDIDATE.with_suffix('.xdelta')
    reconstruction = Path('work/analysis/frame_v165_patch_reconstruction.nds')
    make_xdelta(clean, CANDIDATE, patch)
    apply_xdelta(clean, patch, reconstruction)
    if reconstruction.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError('Clean patch reconstruction differs')
    report = {'status': 'pass-saved-v165-complete-buttons-inheritance-and-clean-patch',
              'candidate': str(CANDIDATE), 'candidate_sha256': sha(CANDIDATE.read_bytes()),
              'candidate_arm9_sha256': sha(new.read_file('/__arm9__.bin')),
              'canonical_base': str(BASE), 'canonical_base_sha256': CANONICAL_BASELINE_SHA256,
              'previous_sha256': PRIOR_SHA, 'profile': PROFILE, 'profile_status': 'experimental',
              'batch_count': 452, 'accepted_batches': manifest['required_batches'],
              'registry_sha256': manifest['release_stack_sha256'], 'changed_paths_vs_v164': changed,
              'changed_paths_vs_canonical': canonical_changed,
              'all_prior_components_resources_stages_and_records_preserved': True,
              'patch': str(patch), 'patch_bytes': patch.stat().st_size, 'patch_sha256': sha(patch.read_bytes()),
              'clean_patch_base_sha256': sha(clean.read_bytes()), 'patch_reconstruction_exact': True,
              'new_logical_labels': 6, 'live_crops_palette_loading_input_and_gameplay_verified': False}
    save(Path('work/analysis/frame_v165_saved_proof.json'), report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['materialize', 'native', 'register', 'verify'])
    globals()[parser.parse_args().action]()
