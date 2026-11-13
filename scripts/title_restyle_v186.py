"""Beveled English wordmark and redundant phonetic-caption omission.

The generated RGBA asset is source locked. Indexed conversion preserves soft
coverage against the source scene; native texture geometry and palettes stay
unchanged. This focused correction does not resume the paused graphics goal.
"""

import argparse
import copy
import json
import zlib
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
    CANONICAL_BASELINE_SHA256,
    RELEASE_STACK_PATH,
    accepted_batch_paths,
    apply_fls_indexed_region_batch,
    apply_pxl_indexed_region_batch,
    load_release_stack,
    resolve_release_batches,
    rom_files,
    verify_golden_content,
)
from scripts.fleet_row_graphics_v162 import save
from scripts.rota_title_copies_v175 import SPECS as ORIGINAL_SPECS
from scripts.rota_title_copies_v175 import nearest

BASE = Path('out/raphael_natural_v2_accepted_base.nds')
PRIOR = Path('out/all_routes_combined_v185_candidate.nds')
PRIOR_SHA = 'f81509cdd809b40f654347b4b21be9a2229c80ff76204d9f2b51a60f9e0c613c'
CANDIDATE = Path('out/all_routes_combined_v186_candidate.nds')
PROFILE = 'all-routes-unified-v186'
OUT = Path('work/qa/title_restyle_v186')
PROOF = Path('work/analysis/title_restyle_v186_saved_proof.json')
ASSET = Path('translations/assets/blue_title_wordmark_v2.png')
ASSET_SHA = 'e357836b83dc8c527a16954d4fd5a007a102d59a33a5e7663903f9f950822d28'
FLS_PATH = '/FLS/M28.fls'
FLS_BATCH = Path('translations/opening_m28_title_art_v2.json')
OLD_FLS_BATCH = Path('translations/opening_m28_title_art_v1.json')
FLS_BOXES = {4: [6, 1, 251, 50], 5: [151, 39, 203, 52]}
SPECS = copy.deepcopy(ORIGINAL_SPECS)
SPECS[0]['caption'][3] = 135  # Include the original caption's lower white fringe.


@lru_cache(maxsize=1)
def sources():
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256 or sha(PRIOR.read_bytes()) != PRIOR_SHA:
        raise ValueError('Exact canonical and V185 required')
    if sha(ASSET.read_bytes()) != ASSET_SHA:
        raise ValueError('Generated wordmark asset identity differs')
    return NdsImage.open(BASE), NdsImage.open(PRIOR)


def batch_path(spec):
    return Path('translations/rota_title_' + spec['name'] + '_art_v2.json')


def replacements():
    return {OLD_FLS_BATCH.as_posix(): FLS_BATCH.as_posix()} | {
        'translations/rota_title_' + s['name'] + '_art_v1.json': batch_path(s).as_posix() for s in SPECS}


@lru_cache(maxsize=2)
def wordmark(height=42):
    sources()
    image = Image.open(ASSET).convert('RGBA')
    # Ignore only virtually transparent generation dust; full visible letters
    # and their shadows are included. Pad before Lanczos projection.
    box = image.getchannel('A').point(lambda a: 255 if a >= 8 else 0).getbbox()
    box = (box[0] - 4, box[1] - 4, box[2] + 4, box[3] + 4)
    cropped = image.crop(box)
    width = round(cropped.width * height / cropped.height)
    resized = cropped.resize((width, height), Image.Resampling.LANCZOS)
    if resized.getchannel('A').getbbox() is None:
        raise ValueError('Empty wordmark')
    return resized, box


def original_gold_mask(texture):
    result = Image.new('L', (texture.width, texture.height))
    for i, index in enumerate(texture.indices):
        r, g, b, _ = texture.palette[index]
        if r > g + 6 and g > b + 18 and r > 90:
            result.putpixel((i % texture.width, i // texture.width), 255)
    return result.filter(ImageFilter.MaxFilter(5))


def paint(pixels, width, height, palette, protected):
    word, crop = wordmark()
    ox, oy = (width - word.width) // 2, 0
    if ox < 3 or word.height + 1 > height:
        raise ValueError('Whole wordmark escapes original main-title box')
    lookup = {}
    fractional = 0
    for y in range(word.height):
        for x in range(word.width):
            r, g, b, alpha = word.getpixel((x, y))
            if not alpha:
                continue
            i = (y + oy) * width + x + ox
            if i in protected:
                if alpha > 8:
                    raise ValueError('Wordmark touches original Latin ornament')
                continue
            bg = palette[pixels[i]][:3]
            rgb = tuple(round((c * alpha + background * (255 - alpha)) / 255)
                        for c, background in zip((r, g, b), bg, strict=True))
            if rgb not in lookup:
                lookup[rgb] = nearest(palette, rgb)
            pixels[i] = lookup[rgb]
            fractional += 0 < alpha < 255
    return {'asset': str(ASSET), 'asset_sha256': ASSET_SHA, 'source_crop': crop,
            'projected_size': word.size, 'position': [ox, oy],
            'full_visible_box': word.getchannel('A').getbbox(), 'soft_coverage_pixels': fractional,
            'exact_text': ['UNCHARTED', 'WATERS IV'], 'hard_alpha_threshold_used': False}


def pxl_regions(spec):
    expected = next(s for s in SPECS if s['name'] == spec['name'])
    if spec != expected:
        raise ValueError('Title resource ownership specification differs')
    return _pxl_regions(spec['name'])


@lru_cache(maxsize=3)
def _pxl_regions(name):
    spec = next(s for s in SPECS if s['name'] == name)
    base, _ = sources()
    p = PxlImage.from_bytes(base.read_file(spec['path']))
    bg = PxlImage.from_bytes(base.read_file(spec['background'])) if spec['background'] else None
    mapping = [nearest(p.palette, c[:3]) for c in bg.palette] if bg else None
    latin = FlsArchive(base.read_file(FLS_PATH)).texture(5)
    gold = original_gold_mask(latin)
    ox, oy = spec['latin_offset']
    output, proofs = [], []
    for kind in ('main', 'caption'):
        x0, y0, x1, y1 = spec[kind]
        w, h = x1 - x0, y1 - y0
        pixels = bytearray()
        protected = set()
        for y in range(y0, y1):
            for x in range(x0, x1):
                i = (y - y0) * w + x - x0
                lx, ly = x - ox, y - oy
                r, g, b, _ = p.palette[p.indices[y * 256 + x]]
                within = 0 <= lx < 256 and 0 <= ly < 64
                if kind == 'main':
                    keep = within and latin.indices[ly * 256 + lx] != 0 and not (b > r + 25 and b > g + 20)
                else:
                    keep = within and gold.getpixel((lx, ly)) and not (b > r + 2 and b > g + 2)
                if keep:
                    protected.add(i)
                    pixels.append(p.indices[y * 256 + x])
                else:
                    pixels.append(mapping[bg.indices[y * 256 + x]] if bg else nearest(p.palette, (0, 0, 0)))
        proof = paint(pixels, w, h, p.palette, protected) if kind == 'main' else {
            'caption_policy': 'omit-redundant-phonetic-label', 'source': 'ロッタ ノヴァ', 'meaning': 'Rota Nova'}
        output.append(bytes(pixels))
        proofs.append(proof | {'kind': kind, 'protected_original_indices': sorted(protected),
                               'background_source': spec['background']})
    return output, proofs


@lru_cache(maxsize=1)
def fls_regions():
    base, _ = sources()
    archive = FlsArchive(base.read_file(FLS_PATH))
    output, proofs = [], []
    for index in (4, 5):
        texture = archive.texture(index)
        x0, y0, x1, y1 = FLS_BOXES[index]
        w, h = x1 - x0, y1 - y0
        if index == 4:
            pixels = bytearray(w * h)
            proof = paint(pixels, w, h, texture.palette, set())
        else:
            gold = original_gold_mask(texture)
            pixels = bytearray(texture.indices[y * texture.width + x] if gold.getpixel((x, y)) else 0
                               for y in range(y0, y1) for x in range(x0, x1))
            proof = {'caption_policy': 'omit-redundant-phonetic-label', 'source': 'ロッタ ノヴァ', 'meaning': 'Rota Nova'}
        output.append(bytes(pixels))
        proofs.append(proof)
    return output, proofs


def targets():
    base, _ = sources()
    return {FLS_PATH: apply_fls_indexed_region_batch(FLS_BATCH, base.read_file(FLS_PATH))[0]} | {
        s['path']: apply_pxl_indexed_region_batch(batch_path(s), base.read_file(s['path']))[0] for s in SPECS}


def verify_art(targets_by_path):
    base, prior = sources()
    cases = []
    for spec in SPECS:
        path = spec['path']
        p, old = [PxlImage.from_bytes(r.read_file(path)) for r in (base, prior)]
        new = PxlImage.from_bytes(targets_by_path[path])
        payloads, proof = pxl_regions(spec)
        expected = bytearray(p.indices)
        owned = set()
        for kind, pixels in zip(('main', 'caption'), payloads, strict=True):
            x0, y0, x1, y1 = spec[kind]
            for y in range(y0, y1):
                for x in range(x0, x1):
                    i = y * 256 + x
                    expected[i] = pixels[(y - y0) * (x1 - x0) + x - x0]
                    owned.add(i)
        if new.indices != expected or new.source[:new.pixels_offset] != p.source[:p.pixels_offset]:
            raise ValueError('Saved full wordmark/header/palette differs')
        if any(new.indices[i] != old.indices[i] for i in range(49152) if i not in owned):
            raise ValueError('Earlier gold/copyright/scenery outside ownership changed')
        for i, value in enumerate(p.indices):
            r, g, b, _ = p.palette[value]
            if r > g + 10 and g > b + 30 and r > 120 and new.indices[i] != value:
                raise ValueError('Original gold logo pixel changed')
        cases.append({'path': path, 'header_palette_unowned_gold_copyright_exact': True, 'proof': proof})
    source = base.read_file(FLS_PATH)
    a, b = FlsArchive(source), FlsArchive(targets_by_path[FLS_PATH])
    if a.records != b.records or a.data_offset != b.data_offset or len(source) != len(b.source):
        raise ValueError('Opening movie records/extent changed')
    payloads, proofs = fls_regions()
    for index, payload in zip((4, 5), payloads, strict=True):
        original, edited = a.texture(index), b.texture(index)
        expected = bytearray(original.indices)
        x0, y0, x1, y1 = FLS_BOXES[index]
        for y in range(y0, y1):
            expected[y * 256 + x0:y * 256 + x1] = payload[(y - y0) * (x1 - x0):(y - y0 + 1) * (x1 - x0)]
        if edited.indices != expected or edited.palette != original.palette:
            raise ValueError('Opening artwork/palette/unowned pixels differ')
    for i in range(a.count):
        if i not in (4, 5) and a.texture(i).indices != b.texture(i).indices:
            raise ValueError('Unrelated opening texture changed')
    owned_bytes = set()
    for index in (4, 5):
        start = a.data_offset + a.records[index][4]
        owned_bytes.update(range(start, start + a.records[index][5]))
    if any(x != y for i, (x, y) in enumerate(zip(source, b.source, strict=True)) if i not in owned_bytes):
        raise ValueError('Unrelated movie/header/palette bytes changed')
    original_latin, edited_latin = a.texture(5), b.texture(5)
    for i, value in enumerate(original_latin.indices):
        r, g, blue, _ = original_latin.palette[value]
        if r > g + 10 and g > blue + 30 and r > 120 and edited_latin.indices[i] != value:
            raise ValueError('Opening original gold logo pixel changed')
    cases.append({'path': FLS_PATH, 'original_records_palettes_other_textures_exact': True, 'proof': proofs})
    return cases


def materialize():
    base, prior = sources()
    OUT.mkdir(parents=True, exist_ok=True)
    for spec in SPECS:
        p = PxlImage.from_bytes(base.read_file(spec['path']))
        payloads, proofs = pxl_regions(spec)
        batch = {'format': 'dk4-pxl-indexed-region-batch-v1', 'file_path': spec['path'],
                 'source_file_sha256': sha(p.source), 'target_locale': 'en-US',
                 'scope': 'Smooth beveled English wordmark; duplicate Japanese phonetic caption omitted; source gold logo retained.', 'records': []}
        for kind, payload, proof in zip(('main', 'caption'), payloads, proofs, strict=True):
            box = spec[kind]
            original = bytes(p.indices[y * 256 + x] for y in range(box[1], box[3]) for x in range(box[0], box[2]))
            batch['records'].append({'id': 'DK4_ROTA_' + spec['name'].upper() + '_' + kind.upper() + '_V1',
                                    'box': box, 'source_region_sha256': sha(original),
                                    'indices_zlib_hex': zlib.compress(payload).hex(), 'indices_sha256': sha(payload),
                                    'source_japanese': '大航海時代IV' if kind == 'main' else 'ロッタ ノヴァ',
                                    'english': 'Uncharted Waters IV' if kind == 'main' else '', 'artwork_proof': proof})
        save(batch_path(spec), batch)
    archive = FlsArchive(base.read_file(FLS_PATH))
    payloads, proofs = fls_regions()
    batch = {'format': 'dk4-fls-indexed-region-batch-v1', 'file_path': FLS_PATH,
             'source_file_sha256': sha(base.read_file(FLS_PATH)), 'target_locale': 'en-US', 'records': []}
    for index, payload, proof in zip((4, 5), payloads, proofs, strict=True):
        t = archive.texture(index)
        batch['records'].append({'id': 'DK4_OPENING_M28_TITLE_' + str(index) + '_V1', 'asset_index': index,
                                'box': FLS_BOXES[index], 'source_texture_sha256': sha(bytes(t.indices)),
                                'source_record': archive.records[index], 'indices_zlib_hex': zlib.compress(payload).hex(),
                                'indices_sha256': sha(payload), 'source_japanese': '大航海時代IV' if index == 4 else 'ロッタ ノヴァ',
                                'english': ['Uncharted Waters IV'] if index == 4 else [], 'artwork_proof': proof})
    save(FLS_BATCH, batch)
    result = targets()
    cases = verify_art(result)
    for spec in SPECS:
        path = spec['path']
        images = [PxlImage.from_bytes(r.read_file(path)).render() for r in (base, prior)]
        images.append(PxlImage.from_bytes(result[path]).render())
        sheet = Image.new('RGB', (1568, 412), '#303030')
        d = ImageDraw.Draw(sheet)
        for col, (label, im) in enumerate(zip(('Original', 'V185', 'Restyled; caption omitted'), images, strict=True)):
            d.text((12 + col * 520, 8), label, fill='white')
            sheet.paste(im.resize((512, 384), Image.Resampling.NEAREST).convert('RGB'), (12 + col * 520, 28))
        sheet.save(OUT / (spec['name'] + '_review.png'))
        images[-1].save(OUT / (spec['name'] + '_native.png'))
    sheet = Image.new('RGB', (1048, 328), '#303030')
    d = ImageDraw.Draw(sheet)
    for col, raw in enumerate((prior.read_file(FLS_PATH), result[FLS_PATH])):
        f = FlsArchive(raw)
        d.text((12 + col * 520, 8), 'V185' if col == 0 else 'Restyled', fill='white')
        for row, index in enumerate((4, 5)):
            sheet.paste(f.texture(index).render().resize((512, 128), Image.Resampling.NEAREST).convert('RGB'), (12 + col * 520, 28 + row * 144))
    sheet.save(OUT / 'opening_review.png')
    save(OUT / 'evidence.json', {'cases': cases, 'visual_review': False, 'native_display_verified': False,
                              'generated_with': 'built-in image_gen', 'asset_sha256': ASSET_SHA})
    print('Prepared all four Rota Nova title copies with soft beveled lettering and omitted duplicate caption.')


def register():
    if not json.loads((OUT / 'evidence.json').read_text(encoding='utf-8'))['visual_review']:
        raise ValueError('Review all native-sized conversions first')
    s = load_release_stack()
    p = copy.deepcopy(s['profiles']['all-routes-unified-v185'])
    replace = replacements()
    if any(p['batches'].count(old) != 1 for old in replace):
        raise ValueError('Expected exactly four title layers to replace')
    p['batches'] = [replace.get(b, b) for b in p['batches']]
    p.update(description='Full V185 stack with four corrected Rota Nova title layers; smooth beveled blue wordmark, duplicate phonetic caption omitted.',
             note='Focused title-art correction while broader graphics goal remains paused. Original gold logo, source palettes/headers/records and all unrelated content retained. Experimental.')
    s['profiles'][PROFILE] = p
    save(RELEASE_STACK_PATH, s)


def verify():
    base, prior = sources()
    new = NdsImage.open(CANDIDATE)
    manifest = json.loads(CANDIDATE.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    old = json.loads(PRIOR.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    stack = load_release_stack()
    replace = replacements()
    expected = [str(Path(replace.get(Path(p).as_posix(), Path(p).as_posix()))) for p in old['batches']]
    if (manifest['candidate_sha256'] != sha(CANDIDATE.read_bytes()) or manifest['base_sha256'] != CANONICAL_BASELINE_SHA256
            or manifest['profile'] != PROFILE or manifest['release_stack_sha256'] != sha(RELEASE_STACK_PATH.read_bytes())
            or manifest['batches'] != expected or len(expected) != 463
            or manifest['batches'] != [str(p) for p in resolve_release_batches(PROFILE, [], stack)]
            or manifest['required_batches'] != [str(p) for p in accepted_batch_paths(stack)]
            or manifest['relocations'] != old['relocations'] or manifest['changed_records'] != old['changed_records']
            or manifest['changed_paths'] != old['changed_paths'] or not all(manifest['checks'].values())):
        raise ValueError('Full registered inheritance/identity/record IDs differ')
    repro = Path('work/analysis/v185_title_restyle_reproduction.nds')
    if sha(repro.read_bytes()) != PRIOR_SHA:
        raise ValueError('Full prior V185 reproduction differs')
    before, after = rom_files(prior), rom_files(new)
    paths = sorted([FLS_PATH] + [s['path'] for s in SPECS])
    if sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p)) != paths:
        raise ValueError('Unexpected internal file delta')
    result = targets()
    if any(new.read_file(path) != data for path, data in result.items()):
        raise ValueError('Saved complete title artwork differs')
    cases = verify_art(result)
    verify_golden_content(base, new)
    clean = Path('work/clean.nds')
    clean_sha = sha(clean.read_bytes())
    if clean_sha != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Wrong clean patch base')
    patch = CANDIDATE.with_suffix('.xdelta')
    reconstruction = Path('work/analysis/title_v186_patch_reconstruction.nds')
    make_xdelta(clean, CANDIDATE, patch)
    apply_xdelta(clean, patch, reconstruction)
    if reconstruction.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError('Patch reconstruction differs')
    save(PROOF, {'status': 'pass-saved-v186-title-restyle-and-full-inheritance', 'cases': cases,
                 'candidate': str(CANDIDATE), 'candidate_sha256': sha(CANDIDATE.read_bytes()),
                 'canonical_base': str(BASE), 'canonical_base_sha256': CANONICAL_BASELINE_SHA256,
                 'previous_sha256': PRIOR_SHA, 'profile': PROFILE, 'profile_status': 'experimental', 'batch_count': 463,
                 'candidate_arm9_sha256': sha(new.read_file('/__arm9__.bin')), 'registry_sha256': manifest['release_stack_sha256'],
                 'builder_sha256': sha(Path('scripts/build_integrated_release.py').read_bytes()), 'asset_sha256': ASSET_SHA,
                 'changed_paths_vs_v185': paths, 'changed_paths_vs_canonical': manifest['changed_paths'],
                 'complete_v185_reproduction_exact': True, 'all_prior_records_stages_retained': True,
                 'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()), 'patch_bytes': patch.stat().st_size,
                 'clean_patch_base_sha256': clean_sha, 'patch_reconstruction_exact': True,
                 'native_display_verified': False, 'broader_graphics_goal_status': 'paused'})
    print('Verified saved V186 title artwork, complete prior stack and exact patch reconstruction.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['materialize', 'register', 'verify'])
    globals()[parser.parse_args().action]()
