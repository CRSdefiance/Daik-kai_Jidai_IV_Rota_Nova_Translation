"""Source-locked fleet labels, complete native glyph proof and saved release checks."""

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
from scripts.probe_button_prompt_native import call, machine
from scripts.probe_name_treasure_graphics_v161 import glyph_case, mask_for

BASE = Path('out/raphael_natural_v2_accepted_base.nds')
PRIOR = Path('out/all_routes_combined_v161_candidate.nds')
CANDIDATE = Path('out/all_routes_combined_v162_candidate.nds')
PROFILE = 'all-routes-unified-v162'
RESOURCE = '/Iseki/dock.pxl'
BATCH = Path('translations/fleet_row_graphics_v1.json')
OUT = Path('work/qa/fleet_row_graphics_v162')
ART = Path('work/analysis/fleet_row_graphics_v162_artwork.json')
NATIVE = Path('work/analysis/fleet_row_graphics_v162_native.json')
PRIOR_SHA = 'a3cf17dd8b434c5c93af39c89fe3623da3f00832a03a59f5993d4aa9126b4835'
LABELS = [('旗艦', 'Flagship', 'The flagship, first ship in the fleet.')] + [
    (str(i) + '番艦', 'Ship ' + str(i), 'Ship number ' + str(i) + ' in the fleet.')
    for i in range(2, 6)]


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sources():
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256 or sha(PRIOR.read_bytes()) != PRIOR_SHA:
        raise ValueError('Exact canonical and V161 source ROMs required')
    base, prior, clean = [NdsImage.open(p) for p in (BASE, PRIOR, Path('work/clean.nds'))]
    raw = base.read_file(RESOURCE)
    if raw != prior.read_file(RESOURCE) or raw != clean.read_file(RESOURCE):
        raise ValueError('Original clean Japanese fleet artwork required')
    p = PxlImage.from_bytes(raw)
    if (p.width, p.height, p.bits_per_pixel) != (256, 192, 8):
        raise ValueError('Fleet image geometry differs')
    return base, prior, p


def materialize():
    _, prior, p = sources()
    batch = {
        'format': 'dk4-pxl-native-label-batch-v1', 'file_path': RESOURCE,
        'source_file_sha256': sha(p.source), 'font_file_path': '/__arm9__.bin',
        'font_sha256': REFERENCE_ASCII_FONT_SHA256, 'target_locale': 'en-US',
        'editorial_policy': 'natural-dialogue-v2', 'glyph_width': 6, 'advance': 6,
        'color_index': 226, 'erase_palette_indices': [226], 'records': [],
        'scope': 'Five fleet row captions; preserve dividers, header, right half and remaining artwork.',
    }
    for i, (jp, text, gloss) in enumerate(LABELS):
        y = 18 + i * 28
        box = [3, y, 53, y + 16]
        # The untouched left-half pattern repeats every 32 pixels. Two periods
        # to the right avoid all source lettering and its antialias/shadow pixels.
        # Reconstruct only each owned text rectangle, without changing palette.
        background = bytes(p.indices[yy * 256 + xx + 64]
                           for yy in range(y, y + 16) for xx in range(3, 53))
        if 226 in background:
            raise ValueError('Donor region contains lettering')
        batch['records'].append({
            'id': 'DK4_FLEET_ROW_' + str(i + 1) + '_GRAPHIC_V1',
            'source_japanese': jp, 'source_meaning': gloss, 'text': text,
            'box': box, 'background_indices_zlib_hex': zlib.compress(background).hex(),
            'context': 'Baked fleet list: flagship, then ships 2 through 5.',
            'localization_note': 'Retains the original fleet position and meaning in natural English. All original native glyph pixels fit; no abbreviations.',
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': True, 'visual': False,
                       'physical_gameplay': False},
        })
    save(BATCH, batch)
    target, _ = apply_pxl_native_label_batch(BATCH, p.source, prior.read_file('/__arm9__.bin'))
    OUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1056, 432), '#303030')
    draw = ImageDraw.Draw(sheet)
    for i, (label, raw) in enumerate((('Original fleet labels', p.source), ('English fleet labels', target))):
        raster = PxlImage.from_bytes(raw).render().convert('RGB')
        raster.save(OUT / ('source_native.png' if i == 0 else 'english_native.png'))
        draw.text((8 + i * 528, 8), label, fill='white')
        sheet.paste(raster.resize((512, 384), Image.Resampling.NEAREST), (8 + i * 528, 30))
    sheet.save(OUT / 'review.png')
    save(ART, {'status': 'draft-five-fleet-labels', 'source_file_sha256': sha(p.source),
               'target_file_sha256': sha(target), 'labels': [x[1] for x in LABELS],
               'background': 'Owned text rectangles reconstructed from untouched repeating pattern at x+64; includes removal of old glyph antialias/shadows.',
               'visual_review': False})
    print('Materialized five source-locked fleet labels and complete preview.')


def packed_proof(source, batch, row, target):
    mask, _ = mask_for(source, batch, row)
    p = PxlImage.from_bytes(target)
    x0, y0, x1, y1 = row['box']
    for y in range(y0, y1):
        for x in range(x0, x1):
            if (p.indices[y * 256 + x] == batch['color_index']) != bool(mask.getpixel((x, y + 2))):
                raise ValueError('Packed complete label/first character differs')


def native():
    base, prior, _ = sources()
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    source = prior.read_file('/__arm9__.bin')
    target, _ = apply_pxl_native_label_batch(BATCH, base.read_file(RESOURCE), source)
    cases = []
    for row in batch['records']:
        # Real ASCII primitive draws four-bit scratch pixels; the palette index
        # 226 belongs to the packed eight-bit dock artwork, verified separately.
        scratch = dict(batch, color_index=15)
        cases.append(glyph_case(source, scratch, row))
        packed_proof(source, batch, row, target)
    uc = machine(source)
    executed = call(uc, 0x10DAF4, ())
    descriptor = bytes(uc.mem_read(0x022A44B8, 20))
    vt, flag1, flag2, path, sentinel = struct.unpack('<5I', descriptor)
    source_path = bytes(uc.mem_read(path, 15))
    if (vt != 0x02160538 or source_path != b'Iseki/dock.pxl\0'
            or sentinel != 0xFFFFFFFF or flag1 != flag2 or flag1 != 0x022A44BC
            or 0x0210DAF4 not in executed):
        raise ValueError('Native dock descriptor/path initializer differs')
    save(NATIVE, {'status': 'pass-five-complete-native-glyph-and-eight-bit-packing-cases',
                  'source_arm9_sha256': sha(source), 'cases': cases,
                  'native_resource_descriptor': descriptor.hex(), 'native_path': 'Iseki/dock.pxl',
                  'native_initializer_ABI_pass': True,
                  'limitations': ['Glyph shapes execute in a four-bit scratch canvas; full eight-bit asset packing checked separately.',
                                  'Native descriptor initializer is real; resource loading, live crops and GPU palette/alpha remain unproved.',
                                  'Complete widget, controller input and physical gameplay remain pending.']})
    print('Pass: five complete native font rasters, exact eight-bit artwork and actual resource descriptor initializer.')


def register():
    art = json.loads(ART.read_text(encoding='utf-8'))
    evidence = json.loads(NATIVE.read_text(encoding='utf-8'))
    if art['visual_review'] is not True or evidence['status'] != 'pass-five-complete-native-glyph-and-eight-bit-packing-cases':
        raise ValueError('Reviewed preview and native evidence required')
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    for row in batch['records']:
        row['review']['visual'] = True
    save(BATCH, batch)
    registry = load_release_stack()
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v161'])
    profile['batches'].append(BATCH.as_posix())
    profile['note'] = 'Full V161 inheritance plus five fleet row graphics; experimental, live load/crop and physical gameplay pending.'
    profile['description'] = 'All 440 V161 batches and terminal stages plus one canonical-source fleet artwork batch (441 total).'
    registry['profiles'][PROFILE] = profile
    save(RELEASE_STACK_PATH, registry)
    print('Registered V162, 441 batches; experimental.')


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
            or len(manifest['batches']) != 441 or manifest['batches'][:440] != old['batches']
            or manifest['required_batches'] != [str(p) for p in accepted_batch_paths(registry)]
            or not all(manifest['checks'].values()) or manifest['relocations'] != old['relocations']):
        raise ValueError('Saved identity, full stack or inherited repair metadata differs')
    before, after, canonical = rom_files(prior), rom_files(new), rom_files(base)
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    if changed != [RESOURCE]:
        raise ValueError('V162 changed prior text/code/graphics')
    canonical_changed = sorted(p for p in canonical.keys() | after.keys() if canonical.get(p) != after.get(p))
    if manifest['changed_paths'] != canonical_changed or canonical_changed != sorted(old['changed_paths'] + [RESOURCE]):
        raise ValueError('Changed paths differ')
    for path, ids in old['changed_records'].items():
        if manifest['changed_records'][path] != ids:
            raise ValueError('Inherited records differ')
    target, ids = apply_pxl_native_label_batch(BATCH, base.read_file(RESOURCE), new.read_file('/__arm9__.bin'))
    if new.read_file(RESOURCE) != target or manifest['changed_records'][RESOURCE] != ids:
        raise ValueError('Saved fleet graphics differ from reviewed batch')
    verify_golden_content(base, new)
    clean = Path('work/clean.nds')
    if sha(clean.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Wrong clean patch base')
    patch = CANDIDATE.with_suffix('.xdelta')
    reconstruction = Path('work/analysis/fleet_row_v162_patch_reconstruction.nds')
    make_xdelta(clean, CANDIDATE, patch)
    apply_xdelta(clean, patch, reconstruction)
    if reconstruction.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError('Patch reconstruction differs')
    report = {'status': 'pass-saved-v162-complete-artwork-inheritance-and-clean-patch',
              'candidate': str(CANDIDATE), 'candidate_sha256': sha(CANDIDATE.read_bytes()),
              'candidate_arm9_sha256': sha(new.read_file('/__arm9__.bin')),
              'canonical_base': str(BASE), 'canonical_base_sha256': CANONICAL_BASELINE_SHA256,
              'previous_sha256': PRIOR_SHA, 'profile': PROFILE, 'profile_status': 'experimental',
              'batch_count': 441, 'accepted_batches': manifest['required_batches'],
              'registry_sha256': manifest['release_stack_sha256'],
              'changed_paths_vs_v161': changed, 'changed_paths_vs_canonical': canonical_changed,
              'all_prior_components_resources_stages_and_records_preserved': True,
              'patch': str(patch), 'patch_bytes': patch.stat().st_size, 'patch_sha256': sha(patch.read_bytes()),
              'clean_patch_base_sha256': sha(clean.read_bytes()), 'patch_reconstruction_exact': True,
              'new_logical_labels': 5, 'physical_load_crop_palette_input_and_gameplay_verified': False}
    save(Path('work/analysis/fleet_row_v162_saved_proof.json'), report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['materialize', 'native', 'register', 'verify'])
    globals()[parser.parse_args().action]()
