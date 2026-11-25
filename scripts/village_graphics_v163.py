"""Eight original village caption images with source-faithful complete English."""

import argparse
import copy
import json
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
from scripts.fleet_row_graphics_v162 import packed_proof, save
from scripts.probe_name_treasure_graphics_v161 import glyph_case, sizing

BASE = Path('out/raphael_natural_v2_accepted_base.nds')
PRIOR = Path('out/all_routes_combined_v162_candidate.nds')
PRIOR_SHA = '0ece3348fd68b3c3ef9fb8e4104360806bd4cc007aef21d3780e28f9352b1f9c'
CANDIDATE = Path('out/all_routes_combined_v163_candidate.nds')
PROFILE = 'all-routes-unified-v163'
OUT = Path('work/qa/village_graphics_v163')
ART = Path('work/analysis/village_graphics_v163_artwork.json')
NATIVE = Path('work/analysis/village_graphics_v163_native.json')
LABELS = (
    (168, 'アラブの村 1', 'Arab Village 1', 'An Arab village, number 1.'),
    (169, '新大陸の村', 'New World Village', 'A village in the New World.'),
    (170, '中国 村', 'Chinese Village', 'A Chinese village.'),
    (171, '北海の村', 'North Sea Village', 'A village in the North Sea region.'),
    (206, '村 アラブ 発展後', 'Arab Village (Developed)', 'An Arab village after development.'),
    (207, '新大陸 発展後', 'New World Village (Developed)', 'The New World scene after development; paired with the village caption in image 169.'),
    (208, '中国の島 発展後', 'Chinese Island (Developed)', 'A Chinese island after development.'),
    (209, '北海の村 発展後', 'North Sea Village (Developed)', 'A North Sea village after development.'),
)
PATHS = {i: '/evstill/evstill' + str(i) + '.pxl' for i, *_ in LABELS}
BATCHES = {i: Path('translations/village_caption_evstill' + str(i) + '_graphics_v1.json') for i in PATHS}


def sources():
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256 or sha(PRIOR.read_bytes()) != PRIOR_SHA:
        raise ValueError('Exact canonical and V162 sources required')
    base, prior, clean = [NdsImage.open(p) for p in (BASE, PRIOR, Path('work/clean.nds'))]
    for path in PATHS.values():
        raw = base.read_file(path)
        p = PxlImage.from_bytes(raw)
        if (raw != clean.read_file(path) or raw != prior.read_file(path)
                or (p.width, p.height, p.bits_per_pixel) != (256, 192, 8)
                or p.palette[255] != (255, 255, 255, 255)):
            raise ValueError('Clean Japanese caption/white canvas differs: ' + path)
    return base, prior


def materialize():
    base, prior = sources()
    OUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1056, 8 * 424), '#303030')
    draw = ImageDraw.Draw(sheet)
    rows = []
    for row_index, (i, jp, text, gloss) in enumerate(LABELS):
        source = base.read_file(PATHS[i])
        p = PxlImage.from_bytes(source)
        # Choose the original palette's closest dark blue to the source ink.
        color = min(range(256), key=lambda v: sum((a - b) ** 2 for a, b in zip(p.palette[v][:3], (0, 57, 115))))
        batch = {
            'format': 'dk4-pxl-native-label-batch-v1', 'file_path': PATHS[i],
            'source_file_sha256': sha(source), 'font_file_path': '/__arm9__.bin',
            'font_sha256': REFERENCE_ASCII_FONT_SHA256, 'target_locale': 'en-US',
            'editorial_policy': 'natural-dialogue-v2', 'glyph_width': 6, 'advance': 6,
            'color_index': color, 'erase_palette_indices': [color],
            'scope': 'Complete caption on original white placeholder artwork; native usage remains pending.',
            'records': [{
                'id': 'DK4_VILLAGE_CAPTION_' + str(i) + '_GRAPHIC_V1',
                'source_japanese': jp, 'source_meaning': gloss, 'text': text,
                'box': [0, 0, 256, 192],
                'background_indices_zlib_hex': zlib.compress(bytes([255]) * (256 * 192)).hex(),
                'context': 'Original handwritten village/development scene caption on a white image.',
                'localization_note': 'Preserve region, number and completed development state. Image 208 explicitly says island. Image 207 uses the village context of paired image 169. A single complete natural English heading uses the original game font and palette blue; no new scene art or unused-resource exclusion is asserted.',
                'review': {'source': True, 'context': True, 'localization': True,
                           'naturalness': True, 'formatting': True, 'visual': False,
                           'physical_gameplay': False},
            }],
        }
        save(BATCHES[i], batch)
        target, _ = apply_pxl_native_label_batch(BATCHES[i], source, prior.read_file('/__arm9__.bin'))
        for col, (name, raw) in enumerate((('source', source), ('english', target))):
            raster = PxlImage.from_bytes(raw).render().convert('RGB')
            raster.save(OUT / ('evstill' + str(i) + '_' + name + '_native.png'))
            draw.text((8 + col * 528, row_index * 424 + 8), str(i) + ' ' + name, fill='white')
            sheet.paste(raster.resize((512, 384), Image.Resampling.NEAREST), (8 + col * 528, row_index * 424 + 30))
        rows.append({'image': PATHS[i], 'japanese': jp, 'english': text,
                     'source_sha256': sha(source), 'target_sha256': sha(target),
                     'source_palette_blue': color})
    sheet.save(OUT / 'review.png')
    save(ART, {'status': 'draft-eight-source-faithful-village-captions', 'rows': rows,
               'visual_review': False,
               'source_interpretation_limits': ['Image 207 has an isolated top-edge clipped stroke that is not confidently transcribable as a complete character. English uses the readable New World/after-development lines and paired village 169 context. Revisit source interpretation with actual scene usage.'],
               'scope': 'Original white placeholder captions; no claim of unused resources or live scene reachability.'})
    print('Materialized eight complete village captions and full side-by-side preview.')


def image_geometry(source, target):
    # Exercise the unmodified common sizing/view routine with a controlled
    # loaded image and selector binding, independent of event reachability.
    result = sizing(source, target, 20, 0x02600000, supplied_table=True)
    result['table_input'] = 'controlled-village-image-sizing-contract'
    return result


def native():
    base, prior = sources()
    source = prior.read_file('/__arm9__.bin')
    cases, geometries = [], []
    for i, path in PATHS.items():
        batch = json.loads(BATCHES[i].read_text(encoding='utf-8'))
        target, _ = apply_pxl_native_label_batch(BATCHES[i], base.read_file(path), source)
        row = batch['records'][0]
        cases.append(glyph_case(source, dict(batch, color_index=15), row))
        packed_proof(source, batch, row, target)
        geometries.append({'image': path, **image_geometry(source, target)})
    save(NATIVE, {'status': 'pass-eight-complete-native-glyphs-packed-captions-and-scoped-image-sizes',
                  'source_arm9_sha256': sha(source), 'cases': cases, 'image_geometries': geometries,
                  'limitations': ['Complete original glyph cells execute in four-bit scratch; actual eight-bit caption packing is checked separately.',
                                  'Loaded resource/header and selector binding are controlled inputs; actual event file loading and live crops remain pending.',
                                  'Physical widget/GPU palette/alpha and input, event reachability and gameplay remain unverified.']})
    print('Pass: eight complete native captions, eight-bit packing and eight scoped native image-size cases.')


def register():
    if (json.loads(ART.read_text(encoding='utf-8'))['visual_review'] is not True
            or json.loads(NATIVE.read_text(encoding='utf-8'))['status'] != 'pass-eight-complete-native-glyphs-packed-captions-and-scoped-image-sizes'):
        raise ValueError('Reviewed full preview and native proof required')
    for path in BATCHES.values():
        batch = json.loads(path.read_text(encoding='utf-8'))
        batch['records'][0]['review']['visual'] = True
        save(path, batch)
    registry = load_release_stack()
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v162'])
    profile['batches'] += [p.as_posix() for p in BATCHES.values()]
    profile['note'] = 'Full V162 inheritance plus eight village caption images; experimental, live event load/crop and physical gameplay pending.'
    profile['description'] = 'All 441 V162 batches and terminal stages plus eight original-source village graphics batches (449 total).'
    registry['profiles'][PROFILE] = profile
    save(RELEASE_STACK_PATH, registry)
    print('Registered experimental V163 with 449 batches.')


def verify():
    base, prior = sources()
    new = NdsImage.open(CANDIDATE)
    manifest = json.loads(CANDIDATE.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    old = json.loads(PRIOR.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    registry = load_release_stack()
    if (manifest['candidate_sha256'] != sha(CANDIDATE.read_bytes())
            or manifest['base_sha256'] != CANONICAL_BASELINE_SHA256 or manifest['profile'] != PROFILE
            or manifest['release_stack_sha256'] != sha(RELEASE_STACK_PATH.read_bytes())
            or manifest['batches'] != [str(p) for p in resolve_release_batches(PROFILE, [], registry)]
            or len(manifest['batches']) != 449 or manifest['batches'][:441] != old['batches']
            or manifest['required_batches'] != [str(p) for p in accepted_batch_paths(registry)]
            or not all(manifest['checks'].values()) or manifest['relocations'] != old['relocations']):
        raise ValueError('Saved V163 identity, full stack or inherited stages differ')
    before, after, canonical = rom_files(prior), rom_files(new), rom_files(base)
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    if changed != sorted(PATHS.values()):
        raise ValueError('Unexpected prior text/code/graphics changes')
    canonical_changed = sorted(p for p in canonical.keys() | after.keys() if canonical.get(p) != after.get(p))
    if manifest['changed_paths'] != canonical_changed or canonical_changed != sorted(old['changed_paths'] + list(PATHS.values())):
        raise ValueError('Canonical changed paths differ')
    for path, ids in old['changed_records'].items():
        if manifest['changed_records'][path] != ids:
            raise ValueError('Inherited changed records differ')
    for i, path in PATHS.items():
        target, ids = apply_pxl_native_label_batch(BATCHES[i], base.read_file(path), new.read_file('/__arm9__.bin'))
        if new.read_file(path) != target or manifest['changed_records'][path] != ids:
            raise ValueError('Saved caption differs from reviewed batch: ' + path)
    verify_golden_content(base, new)
    clean = Path('work/clean.nds')
    if sha(clean.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Wrong clean patch base')
    patch = CANDIDATE.with_suffix('.xdelta')
    reconstruction = Path('work/analysis/village_v163_patch_reconstruction.nds')
    make_xdelta(clean, CANDIDATE, patch)
    apply_xdelta(clean, patch, reconstruction)
    if reconstruction.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError('Clean patch reconstruction differs')
    report = {'status': 'pass-saved-v163-complete-artwork-inheritance-and-clean-patch',
              'candidate': str(CANDIDATE), 'candidate_sha256': sha(CANDIDATE.read_bytes()),
              'candidate_arm9_sha256': sha(new.read_file('/__arm9__.bin')),
              'canonical_base': str(BASE), 'canonical_base_sha256': CANONICAL_BASELINE_SHA256,
              'previous_sha256': PRIOR_SHA, 'profile': PROFILE, 'profile_status': 'experimental',
              'batch_count': 449, 'accepted_batches': manifest['required_batches'],
              'registry_sha256': manifest['release_stack_sha256'], 'changed_paths_vs_v162': changed,
              'changed_paths_vs_canonical': canonical_changed,
              'all_prior_components_resources_stages_and_records_preserved': True,
              'patch': str(patch), 'patch_bytes': patch.stat().st_size, 'patch_sha256': sha(patch.read_bytes()),
              'clean_patch_base_sha256': sha(clean.read_bytes()), 'patch_reconstruction_exact': True,
              'new_logical_labels': 8, 'physical_load_crop_palette_input_and_gameplay_verified': False}
    save(Path('work/analysis/village_v163_saved_proof.json'), report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['materialize', 'native', 'register', 'verify'])
    globals()[parser.parse_args().action]()
