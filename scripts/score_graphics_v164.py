"""Complete Won/Lost atlas labels and scoped native selector/crop evidence."""

import argparse
import copy
import json
import struct
import zlib
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import REFERENCE_ASCII_FONT_SHA256
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
    CANONICAL_BASELINE_SHA256,
    RELEASE_STACK_PATH,
    accepted_batch_paths,
    apply_pxl_native_label_batch,
    load_release_stack,
    resolve_release_batches,
    rom_files,
    verify_golden_content,
)
from scripts.fleet_row_graphics_v162 import save
from scripts.probe_button_prompt_native import HEADER, STACK, call, machine
from scripts.probe_name_treasure_graphics_v161 import glyph_case, mask_for, sizing

BASE = Path('out/raphael_natural_v2_accepted_base.nds')
PRIOR = Path('out/all_routes_combined_v163_candidate.nds')
PRIOR_SHA = 'e37d81b0ba5f12c21d5a586966944f087b9ec348ce85e5fdc03c8d02d4721cd9'
CANDIDATE = Path('out/all_routes_combined_v164_candidate.nds')
PROFILE = 'all-routes-unified-v164'
RESOURCE = '/_pxl/deck04.pxl'
BATCH = Path('translations/score_won_lost_graphics_v1.json')
OUT = Path('work/qa/score_graphics_v164')
ART = Path('work/analysis/score_graphics_v164_artwork.json')
NATIVE = Path('work/analysis/score_graphics_v164_native.json')
OWNER = 0x023139FC
VIEW = 0x02480000
LABELS = [('勝', 'Won', 'Games or matches won.', [160, 0, 184, 24]),
          ('敗', 'Lost', 'Games or matches lost.', [184, 0, 208, 24])]


def sources():
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256 or sha(PRIOR.read_bytes()) != PRIOR_SHA:
        raise ValueError('Exact canonical and V163 sources required')
    base, prior, clean = [NdsImage.open(p) for p in (BASE, PRIOR, Path('work/clean.nds'))]
    raw = base.read_file(RESOURCE)
    p = PxlImage.from_bytes(raw)
    if (raw != clean.read_file(RESOURCE) or raw != prior.read_file(RESOURCE)
            or (p.width, p.height, p.bits_per_pixel) != (208, 72, 4)
            or p.palette[0] != (0, 0, 0, 255) or p.palette[15] != (246, 246, 246, 255)):
        raise ValueError('Exact clean Japanese score artwork required')
    return base, prior, p


def materialize():
    _, prior, p = sources()
    batch = {
        'format': 'dk4-pxl-native-label-batch-v1', 'file_path': RESOURCE,
        'source_file_sha256': sha(p.source), 'font_file_path': '/__arm9__.bin',
        'font_sha256': REFERENCE_ASCII_FONT_SHA256, 'target_locale': 'en-US',
        'editorial_policy': 'natural-dialogue-v2', 'glyph_width': 5, 'advance': 5,
        'color_index': 15, 'erase_palette_indices': [15], 'records': [],
        'scope': 'Two score tally words in original 24x24 cells; preserve all digits and Perfect artwork.',
    }
    for jp, text, gloss, box in LABELS:
        batch['records'].append({
            'id': 'DK4_SCORE_' + text.upper() + '_GRAPHIC_V1',
            'source_japanese': jp, 'source_meaning': gloss, 'text': text,
            'box': box, 'background_indices_zlib_hex': zlib.compress(bytes(24 * 24)).hex(),
            'context': 'Win/loss tally symbols beside digit sprites in the deck04 atlas.',
            'localization_note': 'Won/Lost are natural English tally labels with the original victory/defeat meanings. Complete words fit the original symbol cells; all native glyph pixels are preserved.',
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': True, 'visual': False,
                       'physical_gameplay': False},
        })
    save(BATCH, batch)
    target, _ = apply_pxl_native_label_batch(BATCH, p.source, prior.read_file('/__arm9__.bin'))
    OUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (864, 664), '#303030')
    draw = ImageDraw.Draw(sheet)
    for i, (label, raw) in enumerate((('Original score atlas', p.source), ('English score atlas', target))):
        raster = PxlImage.from_bytes(raw).render().convert('RGB')
        raster.save(OUT / ('source_native.png' if i == 0 else 'english_native.png'))
        draw.text((16, i * 328 + 8), label, fill='white')
        sheet.paste(raster.resize((832, 288), Image.Resampling.NEAREST), (16, i * 328 + 28))
    sheet.save(OUT / 'review.png')
    save(ART, {'status': 'draft-complete-won-lost-score-labels', 'labels': [x[1] for x in LABELS],
               'source_sha256': sha(p.source), 'target_sha256': sha(target), 'visual_review': False,
               'source_cell_bounds': [x[3] for x in LABELS],
               'scope': 'Two original score glyph cells; complete parent score display/loading/GPU/input remain pending.'})
    print('Materialized complete Won/Lost labels and full atlas preview.')


def real_format_glyphs(source, target, batch, expected_mask=None):
    p = PxlImage.from_bytes(target)
    packed = bytes(p.indices)
    masks = [mask_for(source, batch, row) for row in batch['records']]
    expected = Image.new('L', (208, 72))
    for mask, _ in masks:
        expected.paste(mask.crop((0, 2, 208, 74)), (0, 0), mask.crop((0, 2, 208, 74)))
    if expected_mask is not None:
        expected = expected_mask
    p.indices[:] = bytes(len(p.indices))
    blank = p.to_bytes()
    uc = machine(source)
    uc.mem_write(HEADER - 16, b'\xA5' * (len(blank) + 32))
    uc.mem_write(HEADER, blank)
    executed = set()
    for row, (_, origin) in zip(batch['records'], masks):
        for i, character in enumerate(row['text']):
            uc.mem_write(STACK, struct.pack('<2I', ord(character), batch['color_index']))
            executed |= call(uc, 0xD16B4, (0, HEADER, origin[0] + i * batch['advance'], origin[1] - 2))
    actual = PxlImage.from_bytes(bytes(uc.mem_read(HEADER, len(blank))))
    pixels = bytes(batch['color_index'] if value else 0 for value in expected.tobytes())
    if (bytes(actual.indices) != pixels or not {0x020D16B4, 0x020D1820} <= executed
            or actual.source[:actual.pixels_offset] != blank[:p.pixels_offset]
            or bytes(uc.mem_read(HEADER - 16, 16)) != b'\xA5' * 16
            or bytes(uc.mem_read(HEADER + len(blank), 16)) != b'\xA5' * 16):
        raise ValueError('Actual four-bit score format complete raster/first character/guards differ')
    for row in batch['records']:
        x0, y0, x1, y1 = row['box']
        for y in range(y0, y1):
            for x in range(x0, x1):
                if packed[y * 208 + x] != pixels[y * 208 + x]:
                    raise ValueError('Packed score glyph pixels differ')
    return {'dimensions': [208, 72], 'format': 'actual-source-four-bit-PXL',
            'complete_native_pixel_sha256': sha(pixels), 'complete_raster_ABI_header_and_guards_pass': True}


def selector(source):
    uc = machine(source)
    output, obj, table = 0x02610000, 0x02610100, 0x02610200
    uc.mem_write(output - 16, b'\xA5' * 36)
    uc.mem_write(obj, struct.pack('<I', table))
    # Controlled type virtual binding to existing native code returning type33.
    # This tests the actual selector branch/table, not a live score object ctor.
    uc.mem_write(table, struct.pack('<3I', 0, 0, 0x020093C8))
    executed = call(uc, 0x11D2C, (output, obj))
    owner, path = struct.unpack('<2I', uc.mem_read(0x0210F3A8, 8))
    if (int.from_bytes(uc.mem_read(output, 4), 'little') != OWNER or owner != OWNER
            or bytes(uc.mem_read(path, 16)) != b'_pxl/deck04.pxl\0'
            or not {0x02011D2C, 0x020093C8} <= executed
            or bytes(uc.mem_read(output - 16, 16)) != b'\xA5' * 16
            or bytes(uc.mem_read(output + 4, 16)) != b'\xA5' * 16):
        raise ValueError('Native type33 selector, source path or output guards differ')
    return {'native_selector': 0x02011D2C, 'type_input': 33, 'source_owner': OWNER,
            'source_filename': '_pxl/deck04.pxl', 'controlled_type_virtual': True,
            'actual_branch_table_and_ABI_pass': True}


def crop(source, target, row):
    uc = machine(source)
    x0, y0, x1, y1 = row['box']
    uc.mem_write(VIEW - 16, b'\xA5' * 80)
    uc.mem_write(VIEW, bytes(48))
    uc.mem_write(STACK, struct.pack('<4I', x1 - x0, y1 - y0, 0, 0))
    executed = call(uc, 0xD3B34, (VIEW, OWNER, x0, y0))
    resource = int.from_bytes(uc.mem_read(VIEW + 12, 4), 'little')
    geometry = struct.unpack('<2I', uc.mem_read(VIEW + 28, 8))
    dimensions = struct.unpack('<2I', uc.mem_read(VIEW + 40, 8))
    if (resource != OWNER or geometry != (x0, y0) or dimensions != (24, 24)
            or not {0x020D3B34, 0x020D3ED0, 0x020D41A4} <= executed
            or bytes(uc.mem_read(VIEW - 16, 16)) != b'\xA5' * 16
            or bytes(uc.mem_read(VIEW + 48, 16)) != b'\xA5' * 16):
        raise ValueError('Native crop source origin, extent or guards differ')
    mask, _ = mask_for(source, json.loads(BATCH.read_text(encoding='utf-8')), row)
    ink = mask.crop((x0, y0 + 2, x1, y1 + 2))
    actual = PxlImage.from_bytes(target).render().crop((x0, y0, x1, y1))
    if not ink.getbbox() or actual.size != (24, 24):
        raise ValueError('Complete score caption crop missing')
    return {'id': row['id'], 'supplied_source_cell': row['box'],
            'native_crop_dimensions': list(dimensions), 'native_descriptor_ABI_and_guards_pass': True,
            'scope': 'Real generic crop constructor with supplied original glyph-cell bounds; actual score parent caller pending.'}


def native():
    base, prior, _ = sources()
    source = prior.read_file('/__arm9__.bin')
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    target, _ = apply_pxl_native_label_batch(BATCH, base.read_file(RESOURCE), source)
    labels = [glyph_case(source, batch, row) for row in batch['records']]
    image_size = sizing(source, target, 20, OWNER, supplied_table=True)
    image_size['table_input'] = 'controlled-score-image-sizing-contract'
    save(NATIVE, {'status': 'pass-complete-score-glyphs-actual-four-bit-format-and-scoped-native-selector-crops',
                  'source_arm9_sha256': sha(source), 'labels': labels,
                  'actual_format': real_format_glyphs(source, target, batch),
                  'selector': selector(source), 'source_image_size': image_size,
                  'crops': [crop(source, target, row) for row in batch['records']],
                  'limitations': ['Type virtual and loaded header/resource binding are controlled inputs.',
                                  'Crop requests use supplied original glyph cells, not a mapped complete score parent caller.',
                                  'Actual file loading, all score contexts, full parent/GPU palette/alpha, input and physical gameplay remain pending.']})
    print('Pass: complete Won/Lost glyphs in actual source format, scoped native selector, size and crop descriptors.')


def register():
    if (json.loads(ART.read_text(encoding='utf-8'))['visual_review'] is not True
            or json.loads(NATIVE.read_text(encoding='utf-8'))['status'] != 'pass-complete-score-glyphs-actual-four-bit-format-and-scoped-native-selector-crops'):
        raise ValueError('Reviewed full preview and native evidence required')
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    for row in batch['records']:
        row['review']['visual'] = True
    save(BATCH, batch)
    registry = load_release_stack()
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v163'])
    profile['batches'].append(BATCH.as_posix())
    profile['note'] = 'Full V163 inheritance plus complete Won/Lost score graphics; experimental, live parent/loading/GPU/input checks pending.'
    profile['description'] = 'All 449 V163 batches and terminal stages plus one canonical-source score graphics batch (450 total).'
    registry['profiles'][PROFILE] = profile
    save(RELEASE_STACK_PATH, registry)
    print('Registered experimental V164 with 450 batches.')


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
            or len(manifest['batches']) != 450 or manifest['batches'][:449] != old['batches']
            or manifest['required_batches'] != [str(p) for p in accepted_batch_paths(registry)]
            or not all(manifest['checks'].values()) or manifest['relocations'] != old['relocations']):
        raise ValueError('Saved V164 identity, full stack or prior stages differ')
    before, after, canonical = rom_files(prior), rom_files(new), rom_files(base)
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    if changed != [RESOURCE]:
        raise ValueError('Unexpected prior text/code/graphics changes')
    canonical_changed = sorted(p for p in canonical.keys() | after.keys() if canonical.get(p) != after.get(p))
    if manifest['changed_paths'] != canonical_changed or canonical_changed != sorted(old['changed_paths'] + [RESOURCE]):
        raise ValueError('Canonical changed path set differs')
    for path, ids in old['changed_records'].items():
        if manifest['changed_records'][path] != ids:
            raise ValueError('Inherited records differ')
    target, ids = apply_pxl_native_label_batch(BATCH, base.read_file(RESOURCE), new.read_file('/__arm9__.bin'))
    if target != new.read_file(RESOURCE) or ids != manifest['changed_records'][RESOURCE]:
        raise ValueError('Saved score artwork differs from reviewed batch')
    verify_golden_content(base, new)
    clean = Path('work/clean.nds')
    if sha(clean.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Wrong clean patch base')
    patch = CANDIDATE.with_suffix('.xdelta')
    reconstruction = Path('work/analysis/score_v164_patch_reconstruction.nds')
    make_xdelta(clean, CANDIDATE, patch)
    apply_xdelta(clean, patch, reconstruction)
    if reconstruction.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError('Clean patch reconstruction differs')
    report = {'status': 'pass-saved-v164-complete-artwork-inheritance-and-clean-patch',
              'candidate': str(CANDIDATE), 'candidate_sha256': sha(CANDIDATE.read_bytes()),
              'candidate_arm9_sha256': sha(new.read_file('/__arm9__.bin')),
              'canonical_base': str(BASE), 'canonical_base_sha256': CANONICAL_BASELINE_SHA256,
              'previous_sha256': PRIOR_SHA, 'profile': PROFILE, 'profile_status': 'experimental',
              'batch_count': 450, 'accepted_batches': manifest['required_batches'],
              'registry_sha256': manifest['release_stack_sha256'], 'changed_paths_vs_v163': changed,
              'changed_paths_vs_canonical': canonical_changed,
              'all_prior_components_resources_stages_and_records_preserved': True,
              'patch': str(patch), 'patch_bytes': patch.stat().st_size, 'patch_sha256': sha(patch.read_bytes()),
              'clean_patch_base_sha256': sha(clean.read_bytes()), 'patch_reconstruction_exact': True,
              'new_logical_labels': 2, 'physical_parent_load_crop_palette_input_and_gameplay_verified': False}
    save(Path('work/analysis/score_v164_saved_proof.json'), report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['materialize', 'native', 'register', 'verify'])
    globals()[parser.parse_args().action]()
