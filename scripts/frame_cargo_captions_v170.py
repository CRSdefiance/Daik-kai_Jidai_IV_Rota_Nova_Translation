"""Complete cargo/ship captions, exact ornament boundary and V169 inheritance."""

import argparse
import copy
import json
import struct
import zlib
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.compact_font import FONT_FACE, FONT_SHA256, GLYPHS
from dk4tool.graphics.pxl import PxlImage
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
from scripts.frame_buttons_v165 import (
    ARCHIVE,
    BASE,
    RESOURCE,
    atlas_indices,
    embedded_preview,
)
from scripts.frame_select_captions_v169 import BATCH as OLD_BATCH
from scripts.frame_select_captions_v169 import SYNC as OLD_SYNC
from scripts.frame_select_captions_v169 import targets as old_targets
from scripts.frame_upper_headings_v168 import real_format_glyphs as prior_glyph_proof
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.probe_name_treasure_graphics_v161 import sizing

PRIOR = Path('out/all_routes_combined_v169_candidate.nds')
PRIOR_SHA = '3a8df5e28429281c476c56742de585d0ebf6fd5303f959d2de4ba1b35194ab34'
CANDIDATE = Path('out/all_routes_combined_v170_candidate.nds')
PROFILE = 'all-routes-unified-v170'
BATCH = Path('translations/frame_action_buttons_graphics_v6.json')
SYNC = Path('translations/frame_action_buttons_cmmnimg_sync_v6.json')
OUT = Path('work/qa/frame_cargo_v170')
ART = Path('work/analysis/frame_cargo_v170_artwork.json')
NATIVE = Path('work/analysis/frame_cargo_v170_native.json')
LABELS = [
    ('積み荷選択', 'Pick Cargo', [208, 32, 256, 40], 'Select which cargo to use.'),
    ('船選択', 'Pick Ship', [208, 40, 240, 48], 'Select which ship to use.'),
]



def sources():
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256 or sha(PRIOR.read_bytes()) != PRIOR_SHA:
        raise ValueError('Exact canonical and V169 sources required')
    base, prior, clean = [NdsImage.open(p) for p in (BASE, PRIOR, Path('work/clean.nds'))]
    for path in (RESOURCE, ARCHIVE):
        if base.read_file(path) != clean.read_file(path):
            raise ValueError('Exact clean Japanese source required')
    if tuple(prior.read_file(p) for p in (RESOURCE, ARCHIVE)) != old_targets():
        raise ValueError('V169 does not match its reviewed graphics batches')
    return base, prior


def targets():
    base, prior = sources()
    target, _ = apply_pxl_native_label_batch(BATCH, base.read_file(RESOURCE), prior.read_file('/__arm9__.bin'))
    embedded, _ = apply_ilnk_pxl_sync_batch(SYNC, base.read_file(ARCHIVE), target)
    return target, embedded


def source_context():
    raw = NdsImage.open('work/clean.nds').read_file(RESOURCE)
    p = PxlImage.from_bytes(raw)
    colors = [[int(value) for value in sorted({p.indices[y * 256 + x]
               for y in range(box[1], box[3]) for x in range(box[0], box[2])})]
              for _, _, box, _ in LABELS]
    if colors != [[0, 6, 9], [0, 4, 5, 6, 9]]:
        raise ValueError('Exact original lettering palette footprint differs')
    return {'file': RESOURCE, 'source_sha256': sha(raw),
            'entries': [{'japanese': jp, 'english': text, 'box': box, 'meaning': meaning,
                         'original_cell_palette_indices': color}
                        for (jp, text, box, meaning), color in zip(LABELS, colors, strict=True)],
            'evidence_scope': 'Read from exact original bitmap; Pick Cargo/Pick Ship retain the explicit selection action.',
            'border_boundary': 'The rounded input field lies at x<=207; the lettering cells begin at x=208. Every field pixel x=181..207,y=30..47 is preserved exactly.',
            'previous_overwide_trial_boxes': 'The earlier x=206 trial rectangles included input chrome. They were never inserted into a candidate. Exact x=208 ownership excludes it.',
            'remaining': 'Date fields and other graphics remain. Actual parent consumers/loading/crops/banks/GPU/input/gameplay remain pending.'}


def compact_pixels(target, batch, expected_mask=None):
    """Independent decoder/layout from fixed row strings; inspect raw packed nibbles."""
    p = PxlImage.from_bytes(target)
    canvas = Image.new('L', (256, 256))
    cases = []
    for row in batch['records'][15:]:
        text = row['text']
        left, top, right, bottom = row['box']
        space = row.get('compact_word_space_width', 2)
        width = sum(space if c == ' ' else len(GLYPHS[c][0]) for c in text) + len(text) - 1
        if width > right - left or bottom - top < 7:
            raise ValueError('Complete compact label does not fit original cell')
        x, y = left + (right - left - width) // 2, top + (bottom - top - 7) // 2
        origins = []
        for c in text:
            rows = ('0' * space,) * 7 if c == ' ' else GLYPHS[c]
            origins.append([x, y])
            for dy, bits in enumerate(rows):
                for dx, bit in enumerate(bits):
                    if bit == '1':
                        canvas.putpixel((x + dx, y + dy), 9)
            x += len(rows[0]) + 1
        cases.append({'id': row['id'], 'text': text, 'box': row['box'],
                      'full_cell_width': width, 'full_cell_height': 7,
                      'all_letter_origins': origins})
    if expected_mask is not None and expected_mask.tobytes() != canvas.tobytes():
        raise ValueError('Complete compact glyph mask/first or final letter differs')
    for case in cases:
        left, top, right, bottom = case['box']
        for y in range(top, bottom):
            for x in range(left, right):
                offset = y * 256 + x
                packed = target[p.pixels_offset + offset // 2]
                actual = (packed >> 4) & 15 if offset & 1 else packed & 15
                if actual != canvas.getpixel((x, y)):
                    raise ValueError('Packed compact glyph/first or final letter differs')
    return {'font_face': FONT_FACE, 'font_sha256': FONT_SHA256,
            'authoring': 'New complete seven-row bitmap face baked into image only; no native glyph or runtime text font was cropped or replaced.',
            'independent_packed_nibble_decode_exact': True, 'cases': cases,
            'full_mask_sha256': sha(canvas.tobytes())}, canvas


def scoped_crop(source, row):
    uc = machine(source)
    view, owner = 0x02480000, 0x02313F60
    x0, y0, x1, y1 = row['box']
    uc.mem_write(view - 16, b'\xA5' * 80)
    uc.mem_write(view, bytes(48))
    uc.mem_write(STACK, struct.pack('<4I', x1 - x0, y1 - y0, 0, 0))
    executed = call(uc, 0xD3B34, (view, owner, x0, y0))
    if (int.from_bytes(uc.mem_read(view + 12, 4), 'little') != owner
            or struct.unpack('<2I', uc.mem_read(view + 28, 8)) != (x0, y0)
            or struct.unpack('<2I', uc.mem_read(view + 40, 8)) != (x1 - x0, y1 - y0)
            or not {0x020D3B34, 0x020D3ED0, 0x020D41A4} <= executed
            or bytes(uc.mem_read(view - 16, 16)) != b'\xA5' * 16
            or bytes(uc.mem_read(view + 48, 16)) != b'\xA5' * 16):
        raise ValueError('Native supplied crop origin/extent/ABI/guards differ')
    return {'id': row['id'], 'supplied_cell': row['box'],
            'native_crop_descriptor_dimensions': [x1 - x0, y1 - y0],
            'actual_generic_constructor_and_ABI_guards_pass': True,
            'scope': 'Controlled crop constructor inputs; actual selection parent/GPU consumer pending.'}


def materialize():
    base, prior = sources()
    batch = copy.deepcopy(json.loads(OLD_BATCH.read_text(encoding='utf-8')))
    for jp, text, box, meaning in LABELS:
        batch['records'].append({
            'id': 'DK4_FRAME_' + text.upper().replace(' ', '_') + '_GRAPHIC_V6',
            'source_japanese': jp, 'source_meaning': meaning, 'text': text, 'box': box,
            'context': 'Shared cargo and ship selection action captions; actual contexts/crops remain pending.',
            'font_face': FONT_FACE, 'compact_font_sha256': FONT_SHA256,
            'compact_word_space_width': 1,
            'glyph_spacing': 'fixed',
            'color_index': 9,
            'background_indices_zlib_hex': zlib.compress(bytes((box[2]-box[0]) * (box[3]-box[1]))).hex(),
            'localization_note': 'Complete natural English in the original eight-row cell using a new authored seven-row bitmap face. Original gold color; no native glyph clipping/runtime font change.',
            'background_note': 'These two lettering cells beginning at x=208 have a solid index-zero backdrop; restore only those cells. The adjacent input-field ornament at x<=207 and all older labels remain exact.',
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': True, 'visual': False,
                       'physical_gameplay': False}})
    batch['supersedes'] = OLD_BATCH.as_posix()
    batch['preserved_record_ids'] = [r['id'] for r in batch['records'][:18]]
    save(BATCH, batch)
    target, _ = apply_pxl_native_label_batch(BATCH, base.read_file(RESOURCE), prior.read_file('/__arm9__.bin'))
    sync = copy.deepcopy(json.loads(OLD_SYNC.read_text(encoding='utf-8')))
    sync['source_image_sha256'] = sha(target)
    sync['supersedes'] = OLD_SYNC.as_posix()
    sync['scope'] = 'Exact canonical matching right half, all eighteen prior labels plus two selection captions; no unrelated storage changes. Native banks/consumers pending.'
    save(SYNC, sync)
    target, embedded = targets()
    OUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1100, 900), '#303030')
    draw = ImageDraw.Draw(sheet)
    for i, (label, raw) in enumerate((('Original Japanese frame', base.read_file(RESOURCE)), ('English frame: V170', target))):
        raster = PxlImage.from_bytes(raw).render().convert('RGB')
        x = 12 + i * 550
        draw.text((x, 8), label, fill='white')
        sheet.paste(raster.resize((512, 512), Image.Resampling.NEAREST), (x, 28))
        draw.text((x, 552), 'Miniature selection captions', fill='white')
        sheet.paste(raster.crop((181, 30, 256, 57)).resize((525, 189), Image.Resampling.NEAREST), (x, 576))
    sheet.save(OUT / 'review.png')
    embedded_preview(embedded).save(OUT / 'english_embedded_bank_zero.png')
    save(ART, {'status': 'draft-two-selection-captions-eighteen-prior-labels-exact',
               'source_sha256': sha(base.read_file(RESOURCE)), 'target_sha256': sha(target),
               'visual_review': False, 'embedded_bank_zero_review': False,
               'labels_added': [x[1] for x in LABELS], 'prior_labels_preserved': 18,
               'native_palette_bank_and_live_consumers_proved': False})
    save(OUT / 'source_context.json', source_context())
    print('Materialized two selection captions in expanded canonical batches; eighteen earlier labels retained.')


def preservation(target, embedded):
    base, prior = sources()
    before, after = [PxlImage.from_bytes(raw) for raw in (prior.read_file(RESOURCE), target)]
    owned = {(x, y) for _, _, box, _ in LABELS for y in range(box[1], box[3]) for x in range(box[0], box[2])}
    if (len(target) != len(before.source) or target[:after.pixels_offset] != before.source[:before.pixels_offset]
            or any(before.indices[y * 256 + x] != after.indices[y * 256 + x]
                   for y in range(256) for x in range(256) if (x, y) not in owned)):
        raise ValueError('Prior labels or unowned frame artwork/header/palette changed')
    a, b = [IlnkContainer.parse(raw) for raw in (prior.read_file(ARCHIVE), embedded)]
    if (len(embedded) != len(prior.read_file(ARCHIVE)) or a.blocks[5][:20] != b.blocks[5][:20]
            or any(x != y for i, (x, y) in enumerate(zip(a.blocks, b.blocks, strict=True)) if i != 5)):
        raise ValueError('Archive header/flags/palette/unrelated blocks changed')
    ai, bi = atlas_indices(prior.read_file(ARCHIVE)), atlas_indices(embedded)
    if any(ai[y * 512 + x] != bi[y * 512 + x]
           for y in range(256) for x in range(512) if x < 256 or (x - 256, y) not in owned):
        raise ValueError('Prior embedded labels or unowned pixels changed')
    if b''.join(bi[y * 512 + 256:y * 512 + 512] for y in range(256)) != bytes(after.indices):
        raise ValueError('Embedded English half differs')
    if base.read_file(RESOURCE)[:after.pixels_offset] != target[:after.pixels_offset]:
        raise ValueError('Canonical frame header/palette differs')
    return {'all_eighteen_prior_labels_and_unowned_pixels_exact': True,
            'headers_palettes_flags_other_blocks_and_extents_exact': True,
            'embedded_right_half_exact_translated_frame_indices': True}


def native():
    _, prior = sources()
    source = prior.read_file('/__arm9__.bin')
    target, embedded = targets()
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    size = sizing(source, target, 20, 0x02313F60, supplied_table=True)
    size['table_input'] = 'controlled-frame-image-sizing-contract'
    save(NATIVE, {'status': 'pass-twenty-complete-frame-labels-and-two-selection-captions',
                  'source_arm9_sha256': sha(source), 'inherited_native_glyphs': prior_glyph_proof(source, target, dict(batch, records=batch['records'][:15])),
                  'compact_bitmap': compact_pixels(target, batch)[0],
                  'scoped_crops': [scoped_crop(source, row) for row in batch['records'][15:]],
                  'preservation': preservation(target, embedded), 'scoped_image_size': size,
                  'source_context': source_context(),
                  'limitations': ['Sizing loaded header/resource/selector are controlled inputs.',
                                  'Embedded exact pixel storage and bank-zero preview do not prove native bank selection/loading.',
                                  'Actual loaders, all live crops/contexts, parent/GPU palette/alpha, controller/gameplay pending.']})
    print('Pass: twenty complete labels, five compact words/phrases, exact input-field boundary and prior/artwork preservation.')


def register():
    art = json.loads(ART.read_text(encoding='utf-8'))
    if (not art['visual_review'] or not art['embedded_bank_zero_review']
            or json.loads(NATIVE.read_text(encoding='utf-8'))['status'] != 'pass-twenty-complete-frame-labels-and-two-selection-captions'):
        raise ValueError('Full previews and native evidence required')
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    for row in batch['records']:
        row['review']['visual'] = True
    save(BATCH, batch)
    registry = load_release_stack()
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v169'])
    replacements = {OLD_BATCH.as_posix(): BATCH.as_posix(), OLD_SYNC.as_posix(): SYNC.as_posix()}
    profile['batches'] = [replacements.get(p, p) for p in profile['batches']]
    profile['description'] = 'All V169 text/code/stages, with its two frame batches explicitly superseded by expanded canonical v6 batches; 452 total, all eighteen prior labels exact.'
    profile['note'] = 'Pick Cargo and Pick Ship retain complete selection actions with existing seven-row bitmap face; eighteen prior labels and input chrome exact. Date fields and actual parent/loading/crops/banks/GPU/input pending; experimental.'
    registry['profiles'][PROFILE] = profile
    save(RELEASE_STACK_PATH, registry)
    print('Registered experimental V170: 450 unchanged batches plus two expanded frame batches.')


def verify():
    base, prior = sources()
    reproduction = json.loads(Path('work/analysis/v169_word_space_builder_reproduction.json').read_text(encoding='utf-8'))
    if (reproduction['status'] != 'pass-byte-identical-v169-reproduction'
            or reproduction['candidate_sha256'] != PRIOR_SHA
            or reproduction['registry_sha256'] != sha(RELEASE_STACK_PATH.read_bytes())
            or reproduction['builder_sha256'] != sha(Path('scripts/build_integrated_release.py').read_bytes())
            or reproduction['compact_font_module_sha256'] != sha(Path('dk4tool/graphics/compact_font.py').read_bytes())):
        raise ValueError('Fresh exact V169 builder/font reproduction required')
    new = NdsImage.open(CANDIDATE)
    manifest = json.loads(CANDIDATE.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    old = json.loads(PRIOR.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    registry = load_release_stack()
    if (manifest['candidate_sha256'] != sha(CANDIDATE.read_bytes()) or manifest['base_sha256'] != CANONICAL_BASELINE_SHA256
            or manifest['profile'] != PROFILE or manifest['release_stack_sha256'] != sha(RELEASE_STACK_PATH.read_bytes())
            or manifest['batches'] != [str(p) for p in resolve_release_batches(PROFILE, [], registry)]
            or len(manifest['batches']) != 452 or not all(manifest['checks'].values())
            or manifest['required_batches'] != [str(p) for p in accepted_batch_paths(registry)]
            or manifest['relocations'] != old['relocations']):
        raise ValueError('Saved identity/profile/stages differ')
    replacements = {str(OLD_BATCH): str(BATCH), str(OLD_SYNC): str(SYNC)}
    if manifest['batches'] != [replacements.get(p, p) for p in old['batches']]:
        raise ValueError('Prior batches differ beyond explicit frame supersession')
    before, after = rom_files(prior), rom_files(new)
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    if changed != sorted([RESOURCE, ARCHIVE]):
        raise ValueError('Unexpected prior text/code/graphics changes')
    canonical = rom_files(base)
    canonical_changed = sorted(p for p in canonical.keys() | after.keys() if canonical.get(p) != after.get(p))
    if manifest['changed_paths'] != canonical_changed or canonical_changed != old['changed_paths']:
        raise ValueError('Canonical changed paths differ')
    for path, ids in old['changed_records'].items():
        if path == RESOURCE:
            if manifest['changed_records'][path][:18] != ids or len(manifest['changed_records'][path]) != 20:
                raise ValueError('Prior frame record IDs lost')
        elif manifest['changed_records'][path] != ids:
            raise ValueError('Inherited changed-record sets differ')
    target, embedded = targets()
    if (target, embedded) != tuple(new.read_file(p) for p in (RESOURCE, ARCHIVE)):
        raise ValueError('Saved graphics differ from reviewed batches')
    preservation(target, embedded)
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    prior_glyph_proof(new.read_file('/__arm9__.bin'), target, dict(batch, records=batch['records'][:15]))
    compact_pixels(target, batch)
    verify_golden_content(base, new)
    clean = Path('work/clean.nds')
    if sha(clean.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Wrong clean patch base')
    patch, reconstruction = CANDIDATE.with_suffix('.xdelta'), Path('work/analysis/frame_v170_patch_reconstruction.nds')
    make_xdelta(clean, CANDIDATE, patch)
    apply_xdelta(clean, patch, reconstruction)
    if reconstruction.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError('Patch reconstruction differs')
    report = {'status': 'pass-saved-v170-two-selection-captions-and-complete-inheritance',
              'candidate': str(CANDIDATE), 'candidate_sha256': sha(CANDIDATE.read_bytes()),
              'candidate_arm9_sha256': sha(new.read_file('/__arm9__.bin')),
              'canonical_base': str(BASE), 'canonical_base_sha256': CANONICAL_BASELINE_SHA256,
              'previous_sha256': PRIOR_SHA, 'profile': PROFILE, 'profile_status': 'experimental',
              'batch_count': 452, 'accepted_batches': manifest['required_batches'],
              'explicitly_superseded_batches': replacements, 'registry_sha256': manifest['release_stack_sha256'],
              'builder_sha256': reproduction['builder_sha256'],
              'compact_font_module_sha256': reproduction['compact_font_module_sha256'], 'compact_font_sha256': FONT_SHA256, 'complete_v169_builder_reproduction_exact': True,
              'changed_paths_vs_v169': changed, 'changed_paths_vs_canonical': canonical_changed,
              'all_prior_translations_components_stages_and_records_preserved': True,
              'patch': str(patch), 'patch_bytes': patch.stat().st_size, 'patch_sha256': sha(patch.read_bytes()),
              'clean_patch_base_sha256': sha(clean.read_bytes()), 'patch_reconstruction_exact': True,
              'new_logical_labels': 2, 'physical_live_loading_crops_banks_input_gameplay_verified': False}
    save(Path('work/analysis/frame_v170_saved_proof.json'), report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['materialize', 'native', 'register', 'verify'])
    globals()[parser.parse_args().action]()
